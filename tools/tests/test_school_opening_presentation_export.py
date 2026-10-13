import tempfile,unittest
from tools.school_opening_presentation_export import *

class PresentationExportTests(unittest.TestCase):
 def test_original_layer_banks_and_names(self):
  p=projection();self.assertEqual(p['actors']['4']['name'],'瑟希莉絲');self.assertEqual(p['actors']['9']['name'],'伊里安')
  self.assertEqual(p['pages'][1]['layers'][0]['text_indices'],[0,1]);self.assertEqual([r['actor'] for r in p['pages'][4]['layers']],[9,4,0]);self.assertEqual(p['pages'][7]['layers'][1]['text_indices'],[7])
 def test_export_is_byte_identical_and_correct_alpha_geometry(self):
  with tempfile.TemporaryDirectory() as d:
   export(Path(d));target=ROOT/'prototype/assets/school_opening'
   for p in Path(d).iterdir():self.assertEqual(p.read_bytes(),(target/p.name).read_bytes())
  im=dx_image((GAME/'SC004.BIN').read_bytes());self.assertEqual(im.size,(256,512));self.assertEqual(im.getpixel((0,0))[3],0)
 def test_malformed_geometry_header_and_length_refused(self):
  raw=(GAME/'SC004.BIN').read_bytes()
  for data in (raw[:-2],b'',bytes(24),raw[:14]+b'\x01\x00'+raw[16:],raw[:16]+b'\x80\x00'+raw[18:]):
   with self.assertRaises(ValueError):dx_image(data)
 def test_visual_expectations_are_regenerated_from_pinned_native_records(self):
  fixture=json.loads((ROOT/'prototype/ui/tests/fixtures/school_opening_native_visual.json').read_text(encoding='utf-8'))
  self.assertEqual(fixture,native_visual_fixture());self.assertFalse(fixture['runtime_fixture'])

if __name__=='__main__':unittest.main()
