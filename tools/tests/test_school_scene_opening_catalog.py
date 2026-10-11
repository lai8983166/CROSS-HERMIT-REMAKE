import json,struct,unittest
from copy import deepcopy
from tools.school_scene_opening_catalog import *
from tools.school_scene_opening_emulation import SchoolSceneOpeningEmulator

class OpeningSourceTests(unittest.TestCase):
 def test_complete_memory_and_all_presentation_arguments(self):
  for c in native_fixture()['cases']:
   p=c['scene_opening'];result=expected_opening(p['inputs'],p['initialization']['before'])
   expected={'initialization_after':p['initialization']['after'],'primitives':p['initialization']['primitives'],
    'opening_before':p['opening']['before'],'opening_after':p['opening']['after'],
    'updates':p['opening']['updates'],'native_increment_calls':p['opening']['native_increment_calls']}
   self.assertEqual(result,expected,c['name'])
   self.assertEqual(p['inputs']['timer_input'],108000)
   timer=next(r for r in result['initialization_after'] if r['bytes']==24)
   self.assertEqual(struct.unpack('<6i',bytes.fromhex(timer['hex'])),(108000,0,108000,0,30,0))

 def test_declared_original_signed_timer_boundaries_and_return(self):
  source_catalog();e=SchoolSceneOpeningEmulator()
  for value in (0,59,60,3599,3600,215999,216000,12959999,12960000,2147483647,-1,-59,-60,-3600,-216000,-2147483648):
   with self.subTest(value=value):
    e.uc.mem_write(UNITCTRL+0x2E6F4,bytes([165])*24)
    p=e.declared_timer_probe(value);expected,result=signed_timer(value)
    self.assertEqual(p['hex'],expected);self.assertEqual(p['return_value'],result)
    self.assertTrue(p['retained_ranges_unchanged']);self.assertGreater(p['retained_bytes'],100000000)
    self.assertEqual(p['driver'],'declared_signed32_timer_probe');self.assertFalse(e.opening_loading)
  self.assertEqual(struct.unpack('<6i',bytes.fromhex(signed_timer(-59)[0])),(-59,0,-59,0,0,0))
  for value in (False,1.5,'60',None,2147483648,-2147483649):
   with self.assertRaises(ValueError):signed_timer(value)
   with self.assertRaises(ValueError):e.declared_timer_probe(value)
  self.assertFalse(e.opening_loading)
  self.assertEqual(e.declared_timer_probe(60)['hex'],signed_timer(60)[0])

 def test_malformed_input_driver_and_types_refuse(self):
  p=native_fixture()['cases'][0]['scene_opening']
  for field,value in (('phase',True),('phase',3),('task_pointer',TASK+4),('max_updates',214),('timer_input',1.5),('driver','world_loop')):
   inputs=deepcopy(p['inputs']);inputs[field]=value
   with self.assertRaises(ValueError):expected_opening(inputs,p['initialization']['before'])
  inputs=deepcopy(p['inputs']);inputs['extra']=0
  with self.assertRaises(ValueError):expected_opening(inputs,p['initialization']['before'])

 def test_malformed_memory_ownership_and_active_vm_refuse(self):
  p=native_fixture()['cases'][0]['scene_opening']
  for kind in ('pointer','length','encoding','count','phase','active','boolean'):
   before=deepcopy(p['initialization']['before'])
   if kind=='pointer':before[0]['pointer']+=4
   elif kind=='length':before[1]['hex']='00'
   elif kind=='encoding':before[2]['hex']='zzzz'
   elif kind=='count':before.pop()
   elif kind=='boolean':before[2]['bytes']=True
   else:
    raw=bytearray.fromhex(before[0]['hex'])
    if kind=='phase':struct.pack_into('<I',raw,0x34,1)
    else:raw[0x43]=1
    before[0]['hex']=raw.hex()
   with self.assertRaises(ValueError):expected_opening(p['inputs'],before)

 def test_source_dispatch_same_call_fade_and_request_boundary(self):
  rules=source_catalog();self.assertEqual([rules['jump_table'][i] for i in (0,3,4)],['0x453f4a','0x45413b','0x454266'])
  self.assertEqual(rules['natural_initializer_return'],'0x45170e')
  for c in native_fixture()['cases']:
   p=c['scene_opening'];updates=expected_opening(p['inputs'],p['initialization']['before'])['updates']
   self.assertEqual((updates[0]['before_phase'],updates[0]['phase'],updates[0]['fade']),(0,3,-1018))
   self.assertEqual((updates[-2]['phase'],updates[-2]['fade'],updates[-2]['rectangle_count']),(4,260,128))
   self.assertEqual((updates[-1]['phase'],updates[-1]['fade'],updates[-1]['rectangle_count']),(5,260,0))
   self.assertEqual(updates[-1]['rectangle_arguments_sha256'],hashlib.sha256(b'').hexdigest())

 def test_separate_source_native_exports(self):
  rules=json.loads((ROOT/'prototype/data/school_scene_opening_rules.json').read_text('utf-8'))
  evidence=json.loads((ROOT/'prototype/data/school_scene_opening_evidence.json').read_text('utf-8'))
  self.assertEqual(rules,source_catalog());self.assertNotIn('cases',rules)
  self.assertEqual(evidence['native_report_sha256'],EVIDENCE_SHA256)
  self.assertEqual(evidence['cases'],native_fixture()['cases']);self.assertEqual(evidence['inherited_refusals'],native_fixture()['inherited_refusals'])
  self.assertFalse(evidence['runtime_fixture'])

if __name__=='__main__':unittest.main()
