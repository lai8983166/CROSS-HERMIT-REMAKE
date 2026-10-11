import json,struct,unittest
from copy import deepcopy
from tools.school_script_opening_catalog import *

class ScriptOpeningSourceTests(unittest.TestCase):
 def test_complete_memory_all_updates_commands_and_presentation(self):
  for c in native_fixture()['cases']:
   p=c['script_opening'];out=expected_opening(p['inputs'],p['before'])
   self.assertEqual(out,{k:p[k] for k in out},c['name'])
   self.assertEqual([v['opcode'] for v in out['commands']],[167,8,5,165,163,113,113,136,136,117,56,20,12,27])
   self.assertEqual([v['update'] for v in out['commands']],[0,1,2,3,4,5,6,7,9,11,72,74,75,107])
   self.assertEqual(out['after'][0],p['before'][0]);self.assertEqual(out['after'][1],p['before'][1])
   self.assertEqual(out['after'][-2:],p['before'][-2:])

 def test_native_fade_release_and_thirty_counter_delay_boundaries(self):
  p=native_fixture()['cases'][0]['script_opening'];u=expected_opening(p['inputs'],p['before'])['updates']
  self.assertEqual((u[1]['after']['pc'],u[1]['after']['variable0']),(44,1))
  self.assertEqual((u[2]['after']['variable0'],u[2]['after']['pc']),(0,56))
  self.assertEqual((u[11]['after']['fade_remaining'],u[11]['after']['fade_delta'],u[11]['after']['work_wait']),(59,648,1))
  self.assertEqual((u[69]['after']['fade_remaining'],u[69]['after']['work_wait']),(1,1))
  self.assertEqual((u[70]['after']['fade_remaining'],u[70]['after']['fade_active'],u[70]['after']['fade_status'],u[70]['after']['work_wait']),(0,0,2,0))
  self.assertEqual(u[70]['after']['fade_value'],38880)
  self.assertEqual((u[70]['after']['wait'],u[71]['after']['wait']),(4,0))
  self.assertEqual((u[75]['after']['wait_count'],u[75]['after']['wait_limit']),(0,30))
  self.assertEqual((u[105]['after']['wait_count'],u[105]['after']['wait']),(30,1))
  self.assertEqual((u[106]['after']['wait_count'],u[106]['after']['wait']),(31,0))
  self.assertEqual([i for i,x in enumerate(u) if x['fade_return']==0],list(range(11,70)))

 def test_original_group_global_dispatch_and_exact_partial_register_arguments(self):
  rules=source_catalog();self.assertEqual(rules['group20_target'],'0x49962e')
  self.assertEqual((rules['fade_limit'],rules['fade_counts'],rules['delay_counts']),(38912,60,30));self.assertGreater(len(rules['code_inputs']),40)
  records=presentation_records([0,0]);self.assertEqual(len(records),52)
  self.assertEqual(records[0]['args'][4:6],[0x1000000,0x7D0000])
  self.assertEqual(records[0]['receiver'],VM+0x94E8)
  self.assertEqual(records[-1]['receiver'],VM+0x228+19*0x1A)

 def test_independent_setters_preserve_unwritten_bits_and_work(self):
  p=native_fixture()['cases'][0]['script_opening'];before=deepcopy(p['before'])
  flags=bytearray.fromhex(before[4]['hex']);struct.pack_into('<I',flags,0x78,0xFFFFFFFF);struct.pack_into('<H',flags,0x28,99);flags[0]=77;before[4]['hex']=flags.hex()
  work=bytearray.fromhex(before[2]['hex']);work[0x100]=123;before[2]['hex']=work.hex()
  out=expected_opening(p['inputs'],before);flags=bytes.fromhex(out['after'][4]['hex'])
  self.assertEqual(struct.unpack_from('<I',flags,0x78)[0],0x7FFFFFFF);self.assertEqual(flags[0x28:0x2A],bytes(2));self.assertEqual(flags[0],77)
  self.assertEqual(bytes.fromhex(out['after'][2]['hex'])[0x100],123);self.assertNotEqual(out['after'],p['after'])

 def test_malformed_unsupported_driver_parent_and_presentation_refuse(self):
  p=native_fixture()['cases'][0]['script_opening']
  for field,value in (('script_pointer',True),('script_pointer',0),('completed_updates',108),('completed_updates',True),('driver','full_task'),('pending_handler','0x4c4b80'),('overlay_origin',[False,0]),('overlay_origin',[1,0])):
   inputs=deepcopy(p['inputs']);inputs[field]=value
   with self.assertRaises(ValueError):expected_opening(inputs,p['before'])
  for kind in ('pointer','size','encoding','count','phase','completion','control','active_fade','preflight','pc','layer','resource','board','presentation_fade'):
   before=deepcopy(p['before'])
   if kind=='pointer':before[4]['pointer']+=4
   elif kind=='size':before[3]['hex']='00'
   elif kind=='encoding':before[2]['hex']='invalid'
   elif kind=='count':before.pop()
   else:
    at,offset,value={'phase':(0,0x38,15),'completion':(0,0x171,1),'control':(1,12,6),'active_fade':(2,0x2499,1),
     'preflight':(3,0x92E1,1),'pc':(3,0x1C,8),'layer':(3,0x6F60,1),'resource':(3,0x228,1),'board':(3,0x1CF,1),'presentation_fade':(3,0x9248,1)}[kind]
    raw=bytearray.fromhex(before[at]['hex']);raw[offset]=value;before[at]['hex']=raw.hex()
   with self.assertRaises(ValueError):expected_opening(p['inputs'],before)

 def test_separate_source_rules_native_exports_and_playback_boundaries(self):
  rules=json.loads((ROOT/'prototype/data/school_script_opening_rules.json').read_text('utf-8'))
  evidence=json.loads((ROOT/'prototype/data/school_script_opening_evidence.json').read_text('utf-8'))
  self.assertEqual(rules,source_catalog());self.assertNotIn('cases',rules)
  self.assertEqual(evidence['native_report_sha256'],EVIDENCE_SHA256);self.assertFalse(evidence['runtime_fixture'])
  self.assertEqual(evidence['cases'],native_fixture()['cases']);self.assertEqual(evidence['inherited_refusals'],native_fixture()['inherited_refusals'])

if __name__=='__main__':unittest.main()
