import copy,gzip,json,struct,unittest
from tools.school_retained_rendering import ROOT
from tools.school_retained_render_pipeline_verification import verify_output,verify

class OutputProofTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.case=json.loads(gzip.decompress((ROOT/'analysis/school-retained-render-initial-v1-20261021.json.gz').read_bytes()))['case']
 def test_real_framebuffer_contains_two_blended_glyph_masks(self):
  result=verify_output(self.case)
  self.assertEqual(result['indexed_text_draws'],2);self.assertGreaterEqual(result['white_glyph_pixels'],5);self.assertGreater(result['transparent_glyph_pixels'],1000)
 def test_rejects_changed_native_framebuffer(self):
  c=copy.deepcopy(self.case)
  row=next(x for x in c['native_device_trace'] if x['request']['op']=='render_readback')
  row['reply']['result']['hex']='ff'+row['reply']['result']['hex'][2:]
  with self.assertRaisesRegex(ValueError,'native framebuffer'):verify_output(c)
 def test_rejects_corrupted_original_index_data(self):
  c=copy.deepcopy(self.case)
  a=next(a for s in c['steps'] for a in s['result']['api_calls'] if a.get('slot')==73)
  a['request']['buffers'][0]['hex']='ffff'+a['request']['buffers'][0]['hex'][4:]
  with self.assertRaisesRegex(ValueError,'quad indices'):verify_output(c)
 def test_rejects_uploaded_texture_that_does_not_match_visible_glyph(self):
  c=copy.deepcopy(self.case)
  for a in (a for s in c['steps'] for a in s['result']['api_calls'] if a.get('op')=='text_unlock'):a['request']['hex']='00'*(len(a['request']['hex'])//2)
  with self.assertRaisesRegex(ValueError,'transparent glyph'):verify_output(c)
 def test_rejects_wrong_original_rectangle_alpha(self):
  c=copy.deepcopy(self.case)
  a=next(a for s in c['steps'] for a in s['result']['api_calls'] if a.get('slot')==72 and a['args'][4]==20 and struct.unpack_from('<2f',bytes.fromhex(a['request']['buffers'][0]['hex']))==(274,580))
  b=bytearray.fromhex(a['request']['buffers'][0]['hex']);struct.pack_into('<I',b,16,0xff223438);a['request']['buffers'][0]['hex']=b.hex()
  with self.assertRaisesRegex(ValueError,'rectangle color/opacity'):verify_output(c)
 def test_rejects_wrong_source_before_checkpoint_loading(self):
  c=copy.deepcopy(self.case);c['source_sha256']='0'*64
  with self.assertRaisesRegex(ValueError,'source identity'):verify(c)

if __name__=='__main__':unittest.main()
