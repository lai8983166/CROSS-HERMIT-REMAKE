import json,struct,unittest
from copy import deepcopy
from tools.school_entry_control_catalog import *

class EntrySourceTests(unittest.TestCase):
 def test_complete_owned_memory_and_all_update_states(self):
  for c in native_fixture()['cases']:
   p=c['entry_control'];result=expected_control(p['inputs'],p['before'])
   self.assertEqual(result,{k:p[k] for k in result},c['name'])
   task=bytes.fromhex(result['after'][0]['hex']);self.assertEqual(task[0x170:0x172],b'\x00\x00')
   self.assertEqual(struct.unpack_from('<I',task,0x38)[0],5)
   self.assertEqual(result['after'][2]['hex'],'00000000')

 def test_original_dispatch_delay_zero_boundary_and_waiting(self):
  rules=source_catalog();self.assertEqual([rules['jump_table'][i] for i in (0,4,5,6)],['0x499e03','0x49a02f','0x49a074','0x49a0b0'])
  self.assertEqual(rules['request170_meaning'],'entry_control_request')
  for c in native_fixture()['cases']:
   p=c['entry_control'];out=expected_control(p['inputs'],p['before']);u=out['updates']
   self.assertEqual((u[0]['after']['state'],u[0]['after']['request']),(4,1))
   self.assertEqual((u[1]['after']['state'],u[1]['after']['delay'],u[1]['after']['busy']),(5,180,1))
   self.assertEqual((u[181]['after']['state'],u[181]['after']['delay'],u[181]['after']['busy']),(5,0,1))
   self.assertEqual((u[182]['after']['state'],u[182]['after']['busy']),(6,0))
   self.assertEqual([x['waiting_return'] for x in u],[0]*183)
   self.assertTrue(all(x['after']['completion']==0 and x['after']['task_phase']==5 for x in u))

 def test_malformed_and_unsupported_driver_inputs_refuse(self):
  p=native_fixture()['cases'][0]['entry_control']
  for field,value in (('origin',[False,16]),('origin',[10,16]),('dimensions',[64,95]),('dimensions','64,96'),
   ('mode',True),('mode',1),('completed_updates',184),('driver','world_loop')):
   inputs=deepcopy(p['inputs']);inputs[field]=value
   with self.assertRaises(ValueError):expected_control(inputs,p['before'])
  inputs=deepcopy(p['inputs']);inputs['extra']=0
  with self.assertRaises(ValueError):expected_control(inputs,p['before'])

 def test_malformed_ownership_interaction_vm_and_completion_refuse(self):
  p=native_fixture()['cases'][0]['entry_control']
  for kind in ('pointer','size','encoding','count','active_vm','completed','no_request','phase','interactive','not_ready','delay','state','origin'):
   before=deepcopy(p['before'])
   if kind=='pointer':before[2]['pointer']+=2
   elif kind=='size':before[1]['hex']='00'
   elif kind=='encoding':before[2]['hex']='invalid'
   elif kind=='count':before.pop()
   else:
    task=bytearray.fromhex(before[0]['hex']);control=bytearray.fromhex(before[1]['hex'])
    if kind=='active_vm':task[0x43]=1
    elif kind=='completed':task[0x171]=1
    elif kind=='no_request':task[0x170]=0
    elif kind=='phase':struct.pack_into('<I',task,0x38,15)
    elif kind=='interactive':control[14]=1
    elif kind=='not_ready':control[24]=0
    elif kind=='delay':struct.pack_into('<h',control,28,-1)
    elif kind=='state':control[26]=4
    elif kind=='origin':struct.pack_into('<h',control,16,10)
    before[0]['hex']=task.hex();before[1]['hex']=control.hex()
   with self.assertRaises(ValueError):expected_control(p['inputs'],before)

 def test_separate_original_source_and_native_exports(self):
  rules=json.loads((ROOT/'prototype/data/school_entry_control_rules.json').read_text('utf-8'))
  evidence=json.loads((ROOT/'prototype/data/school_entry_control_evidence.json').read_text('utf-8'))
  self.assertEqual(rules,source_catalog());self.assertNotIn('cases',rules)
  self.assertEqual(evidence['native_report_sha256'],EVIDENCE_SHA256)
  self.assertEqual(evidence['cases'],native_fixture()['cases']);self.assertEqual(evidence['inherited_refusals'],native_fixture()['inherited_refusals'])
  self.assertFalse(evidence['runtime_fixture'])

if __name__=='__main__':unittest.main()
