import json,struct,unittest
from copy import deepcopy
from tools.school_script_preflight_catalog import *

class PreflightSourceTests(unittest.TestCase):
 def test_complete_owned_memory_both_returns_and_all_trace(self):
  for c in native_fixture()['cases']:
   p=c['script_preflight'];out=expected_preflight(p['inputs'],p['before'])
   self.assertEqual(out,{key:p[key] for key in out},c['name'])
   self.assertEqual([(v['offset'],v['opcode'],v['advance']) for v in out['commands']],[(452,167,8),(460,8,20),(480,166,8),(488,11,8),(944,19,4)])
   mid=bytes.fromhex(out['preflight_after'][3]['hex']);final=bytes.fromhex(out['after'][3]['hex'])
   self.assertEqual(struct.unpack_from('<I',mid,0x1C)[0],492);self.assertEqual(struct.unpack_from('<I',final,0x1C)[0],0)
   self.assertEqual(mid[4:6],bytes(2));self.assertEqual(final[4:6],b'\x01\x01')
   self.assertEqual(struct.unpack_from('<3I',final,0x9250),(1,1,0))
   self.assertEqual(final[0x3C:0x104],bytes(200));self.assertEqual(final[0x22:0x26],b'\x13\0\x04\0')
   self.assertEqual(bytes.fromhex(out['after'][0]['hex'])[0x170:0x172],bytes(2))

 def test_original_headers_comparison_and_sparse_reset_source(self):
  rules=source_catalog();_,s=script_layout()
  self.assertEqual((s['file_size'],s['groups'],s['sub_count']),(13752,[16,12936],101))
  self.assertEqual(s['selected_span'],[432,1208]);self.assertEqual(s['vm_offsets'],[20,516,516,516])
  self.assertEqual(s['code_span'],[452,948]);self.assertEqual(rules['comparison_operator1'],'equal')
  self.assertEqual(rules['outside_vm_reset_words'],42);self.assertEqual(len(REGIONS),47)
  self.assertEqual(rules['opcode_dispatch'],{'8':'0x4ceaf6','11':'0x4ceb35','166':'0x4cfe03','167':'0x4cfe22'})
  self.assertGreater(len(rules['code_inputs']),60)

 def test_source_recomputes_counter_and_resets_only_original_fields(self):
  p=native_fixture()['cases'][0]['script_preflight'];before=deepcopy(p['before'])
  before[4]['hex']=struct.pack('<2I',0xFFFFFFFE,99).hex()
  vm=bytearray.fromhex(before[3]['hex']);vm[0x1CF]=77;struct.pack_into('<H',vm,0x1DC,4)
  vm[0x92A0]=9;vm[0x400]=123;before[3]['hex']=vm.hex()
  before[-1]['hex']='ffff';out=expected_preflight(p['inputs'],before)
  self.assertEqual(out['after'][4]['hex'],struct.pack('<2I',2,0).hex())
  after=bytes.fromhex(out['after'][3]['hex']);self.assertEqual(after[0x1CF],0)
  self.assertEqual(after[0x1DC:0x1DE],b'\xff\xff');self.assertEqual(after[0x92A0],0)
  self.assertEqual(after[0x400],123);self.assertEqual(out['after'][-1]['hex'],'0000')
  self.assertNotEqual(out['after'],p['after'])

 def test_malformed_inputs_and_memory_ownership_refuse(self):
  p=native_fixture()['cases'][0]['script_preflight']
  for field,value in (('selector',True),('selector',1),('sub',0),('script_pointer',0),('script_pointer',WORK),
   ('script_sha256','bad'),('tick_value',1),('tick_import',1),('main_owner',0),('driver','world_loop')):
   inputs=deepcopy(p['inputs']);inputs[field]=value
   with self.assertRaises(ValueError):expected_preflight(inputs,p['before'])
  inputs=deepcopy(p['inputs']);inputs['extra']=0
  with self.assertRaises(ValueError):expected_preflight(inputs,p['before'])
  for kind in ('pointer','bool_pointer','size','encoding','count','owned_heap','active','controller','delay','completed','phase','script_binding'):
   before=deepcopy(p['before'])
   if kind=='pointer':before[-1]['pointer']+=2
   elif kind=='bool_pointer':before[-1]['pointer']=True
   elif kind=='size':before[3]['hex']='00'
   elif kind=='encoding':before[2]['hex']='invalid'
   elif kind=='count':before.pop()
   else:
    at,offset,value={'owned_heap':(3,5,2),'active':(3,4,1),'controller':(1,12,7),'delay':(1,14,1),
     'completed':(0,0x171,1),'phase':(0,0x38,15),'script_binding':(0,0x64,0)}[kind]
    data=bytearray.fromhex(before[at]['hex']);data[offset]=value;before[at]['hex']=data.hex()
   with self.assertRaises(ValueError):expected_preflight(p['inputs'],before)

 def test_malformed_nested_script_headers_refuse(self):
  raw,_=script_layout()
  for value in (b'',b'\0'*8,struct.pack('<3I',12,1,7),struct.pack('<3I',12,1,13),struct.pack('<3I',100,1,12)):
   with self.assertRaises(ValueError):package_offsets(value)
  with self.assertRaises(ValueError):package_offsets(raw,True)
  for value in (b'',struct.pack('<I',0),struct.pack('<2I',1,3),struct.pack('<2I',1,9),struct.pack('<3I',2,12,8)):
   with self.assertRaises(ValueError):vm_offsets(value,0,len(value))
  with self.assertRaises(ValueError):vm_offsets(raw,432,False)

 def test_separate_source_rules_and_native_exports(self):
  rules=json.loads((ROOT/'prototype/data/school_script_preflight_rules.json').read_text('utf-8'))
  evidence=json.loads((ROOT/'prototype/data/school_script_preflight_evidence.json').read_text('utf-8'))
  self.assertEqual(rules,source_catalog());self.assertNotIn('cases',rules)
  self.assertEqual(evidence['native_report_sha256'],EVIDENCE_SHA256)
  self.assertEqual(evidence['cases'],native_fixture()['cases']);self.assertFalse(evidence['runtime_fixture'])
  self.assertEqual(evidence['inherited_refusals'],native_fixture()['inherited_refusals'])

if __name__=='__main__':unittest.main()
