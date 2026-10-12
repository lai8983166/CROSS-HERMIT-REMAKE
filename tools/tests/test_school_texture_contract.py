import json,struct,unittest
from tools.school_texture_contract import *

class TextureContractTests(unittest.TestCase):
 def test_original_dimensions_and_signed_wrap_refusal(self):
  for v in (1,2,3,24,174,255,256,257,1024,16384):self.assertEqual(run_dimension(v),power_of_two(v))
  for bad in (True,0,-1,16385,32767,32768,65535,'174'):
   with self.assertRaises(ValueError):run_dimension(bad)

 def test_three_real_headers_prepare_exact_call_before_null_read(self):
  for c in native_fixture()['cases']:
   raw=bytes.fromhex(c['font_raster']['after'][3]['hex'])[TEXTURE_OFFSET:TEXTURE_OFFSET+0x48]
   for mode in (0,1):
    r=run_null_device(raw,mode);self.assertEqual(r['after_hex'],raw.hex());self.assertFalse(r['original_returned'])
    self.assertEqual(r['pending'],[{'va':'0x403c81','device':0,'prepared_args':[256,32,1,mode,25,1,OBJECT+0x2C],'device_this_not_yet_pushed':True,'null_dereference_executed':False,'COM_call_executed':False}])
    self.assertFalse(r['GPU_executed']);self.assertFalse(r['native_VM_continuation_executed'])

 def test_original_zero_dimension_or_format_returns_failure_without_COM(self):
  for width,height,fmt in ((0,24,25),(174,0,25),(174,24,0)):
   raw=bytearray(0x48);struct.pack_into('<I2h',raw,0x34,fmt,width,height);r=run_null_device(bytes(raw))
   self.assertEqual(r['pending'],[]);self.assertEqual(r['return_value'],1);self.assertTrue(r['original_returned']);self.assertEqual(r['after_hex'],raw.hex())
  raw=bytearray(0x48);struct.pack_into('<I',raw,0x2C,1)
  for bad,mode in ((b'',0),(bytes(raw),0),(bytes(0x48),True),(bytes(0x48),2)):
   with self.assertRaises(ValueError):run_null_device(bad,mode)

 def test_source_instructions_and_immutable_cases(self):
  source=source_catalog();self.assertEqual(source['device_fallbacks'],[[1,68],[1,36],[2,68],[2,36]])
  report=json.loads((ROOT/'analysis/school-texture-contract-v1-20261012.json').read_text('utf-8'))
  self.assertEqual(report['source'],source);self.assertEqual(len(report['cases']),3)
  for r in report['dimensions']:self.assertEqual(r['original'],r['independent'])

if __name__=='__main__':unittest.main()
