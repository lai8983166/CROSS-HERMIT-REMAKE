"""Full independent bytes, band packing, stack and real resource comparisons."""
import struct,unittest
from copy import deepcopy
from tools.school_second_live_text_catalog import *

class SecondSourceTests(unittest.TestCase):
 def test_all_three_actual_cases_full_regions_pixels_stack_counters_cleanup(self):
  self.assertEqual(len(source_catalog()['band_code_inputs']),9)
  for c in native_fixture()['cases']:
   r=compare_case(c);self.assertEqual(r['complete_regions_compared'],8);self.assertEqual(r['PC'],244);self.assertEqual(r['completed_text_records'],2)
   self.assertEqual(r['first_actual_texture_bytes'],16384);self.assertEqual(r['band_calls'],2);self.assertEqual(r['terminal_text_draws'],1)

 def test_band_split_keeps_partial_last_column_and_allocation_padding(self):
  cfg=geometry([300,20]);self.assertEqual(bands(cfg),[{'rect':[0,0,256,24],'point':[0,0]},{'rect':[256,0,48,24],'point':[0,24]}])
  raw=bytes([8,16,32,255])*304*24;dest=bytes([0x5A])*512*64;out=dest
  for b in bands(cfg):out=convert_surface(raw,[304,24],b['rect'],out,512,b['point'])
  self.assertEqual(out[512*48:],dest[512*48:]);self.assertEqual(out[512*24+96:512*25],dest[512*24+96:512*25])
  with self.assertRaises(ValueError):bands(geometry([252,20]))

 def test_malformed_pitch_pointer_string_and_raster_digest_refused(self):
  c=native_fixture()['cases'][0];p=c['second_live_text'];first=c['first_live_text']
  for section,key,value in (('lock','pitch',True),('lock','pitch',500),('lock','mirror',0),('texture','pointer',first['texture']['pointer']),('raster','text_hex','00')):
   bad=deepcopy(p);bad[section][key]=value
   with self.assertRaises(ValueError):expected(bad,first)
  bad=deepcopy(p);bad['raster']['raster']['sha256']='0'*64
  with self.assertRaises(ValueError):expected(bad,first)

 def test_complete_memory_com_draw_and_first_padding_tampering_rejected(self):
  c=native_fixture()['cases'][0]
  for kind in ('memory','COM','draw','first_padding','cleanup','host_bits','readback_pitch','DIB'):
   bad=deepcopy(c);p=bad['second_live_text']
   if kind=='memory':p['after'][3]['hex']=f"{int(p['after'][3]['hex'][:2],16)^1:02x}"+p['after'][3]['hex'][2:]
   elif kind=='COM':p['COM_calls'][2]['args'][4]=0
   elif kind=='draw':p['text_draws'][0]['args'][4]=11
   elif kind=='first_padding':p['first_actual_readback']['hex']=p['first_actual_readback']['hex'][:-2]+f"{int(p['first_actual_readback']['hex'][-2:],16)^1:02x}"
   elif kind=='cleanup':bad['first_live_text']['COM_process_cleanup']['texture_releases'][0]['count']=1
   elif kind=='host_bits':p['lock']['host_bits']+=4
   elif kind=='readback_pitch':p['actual_readback']['pitch']+=2
   else:next(r for r in p['raster']['font_api'] if r['name']=='CreateDIBSection')['header_hex']='00'*40
   with self.subTest(kind=kind):
    with self.assertRaises(ValueError):compare_case(bad)

if __name__=='__main__':unittest.main()
