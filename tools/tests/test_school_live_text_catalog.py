import json,struct,unittest
from copy import deepcopy
from tools.school_live_text_catalog import *
from tools.school_font_raster_emulation import read_text_parent

class LiveSourceTests(unittest.TestCase):
 def test_complete_prefix_regions_pixels_and_accounting(self):
  self.assertEqual(len(source_catalog()['code_inputs']),24)
  for c in native_fixture()['cases']:
   p=c['live_text'];e=expected(p)
   self.assertEqual(e['after'],p['after']);self.assertEqual(e['pixel_hex'],p['lock']['after_hex']);self.assertEqual(e['pixel_hex'],p['actual_readback']['hex']);self.assertEqual(e['accounting_after'],p['accounting_after'])
   self.assertEqual(len(p['lock']['before_hex'])//2,16384);self.assertTrue(p['retained_ranges_unchanged']);self.assertEqual(p['retained_bytes'],120549305)

 def test_exact_remote_methods_and_original_stack_arguments(self):
  for i,c in enumerate(native_fixture()['cases']):
   p=c['live_text'];font=read_text_parent()['cases'][i]['text_preparation']['pending_font']['frames']['font'];f=font-0x1DC;device=p['binding']['bound'];tex=p['texture']['pointer']
   args=[[device,256,32,1,0,25,1,VM+TEXTURE_OFFSET+0x2C],[tex,0,font-0x318],[tex,0,f-0x84,0,0x800],[tex,0]]
   for call,at,off,a in zip(p['COM_calls'],('0x403c87','0x403cbb','0x40395b','0x4039d0'),(80,56,64,68),args):
    identity=p['platform_hello']['device'] if off==80 else p['texture']
    self.assertEqual((call['source_va'],call['offset'],call['args']),(at,off,a));self.assertEqual(call['vtable'],identity['vtable']);self.assertEqual(call['actual_method'],identity['methods'][str(off)]);self.assertEqual(call['result']['hr'],0)
   self.assertEqual(struct.unpack('<8I',bytes.fromhex(p['COM_calls'][1]['result']['hex'])),(25,1,0,1,16384,0,256,32))
   conv=p['conversion_calls'];self.assertEqual(len(conv),1);self.assertEqual(conv[0],{'source_va':'0x405869','args':[0x10100000,f-0x84,174,24,f-0x98,f-0xA8],'lock_hex':struct.pack('<2I',512,0x37000000).hex(),'rect':[0,0,174,24],'point':[0,0]})

 def test_first_natural_activation_and_presentation_do_not_finish_text(self):
  for i,c in enumerate(native_fixture()['cases']):
   p=c['live_text'];e=expected(p);vm=bytes.fromhex(p['after'][3]['hex']);o=OBJECT_OFFSET
   self.assertEqual(struct.unpack_from('<I',vm,28)[0],238);self.assertEqual(struct.unpack_from('<7H',vm,o+22),(1,3,0,24,1,12,0))
   self.assertEqual(p['first_text_updates'],[{'args':e['first_update_args'],'return_va':'0x4cd541','receiver':VM+o}]);self.assertFalse(p['text_readiness_executed'])
   self.assertEqual(p['presentation'],read_text_parent()['cases'][i]['text_preparation']['presentation']);self.assertEqual(len(p['presentation']),54)

 def test_native_GDI_restores_bitmap_then_deletes_objects(self):
  for c in native_fixture()['cases']:
   p=c['live_text'];api=p['raster']['font_api'];dc=next(r['result'] for r in api if r['name']=='CreateCompatibleDC');bitmap=next(r['result'] for r in api if r['name']=='CreateDIBSection');font=api[0]['result'];old=next(r['result'] for r in api if r['return_va']=='0x40541b')
   self.assertEqual(p['GDI_cleanup_calls'],[{'name':'SelectObject','args':[dc,old],'return_va':'0x4058d8','result':bitmap},
    {'name':'DeleteObject','args':[bitmap],'return_va':'0x405921','result':1},{'name':'DeleteDC','args':[dc],'return_va':'0x40596a','result':1},{'name':'DeleteObject','args':[font],'return_va':'0x4d1c1b','result':1}])

 def test_malformed_binding_geometry_mirror_refused_and_exports_separated(self):
  p=native_fixture()['cases'][0]['live_text']
  for section,key,value in (('binding','before',1),('binding','bound',True),('lock','pitch',True),('lock','pitch',350),('platform_hello','window_visible',True)):
   bad=deepcopy(p);bad[section][key]=value
   with self.assertRaises(ValueError):expected(bad)
  rules=json.loads((ROOT/'prototype/data/school_live_text_rules.json').read_text('utf-8'));evidence=json.loads((ROOT/'prototype/data/school_live_text_evidence.json').read_text('utf-8'))
  self.assertEqual(rules,source_catalog());self.assertNotIn('cases',rules);self.assertEqual(evidence['cases'],native_fixture()['cases']);self.assertFalse(evidence['runtime_fixture'])

if __name__=='__main__':unittest.main()
