import hashlib,json,struct,unittest
from tools.school_entry_control_emulation import *

EVIDENCE_SHA256='8d6640db841aaa25905022a711fc1f0aa9f1c6700a89b3c6dffdec78b794e8b8'
class EntryNativeTests(unittest.TestCase):
 def test_actual_entry_waiting_pending_call_and_provenance(self):
  raw=(ROOT/'analysis/school-entry-control-v1-20261011.json').read_bytes()
  self.assertEqual(hashlib.sha256(raw).hexdigest(),EVIDENCE_SHA256);data=json.loads(raw)
  self.assertEqual(len(data['cases']),3)
  for index,c in enumerate(data['cases']):
   self.assertEqual((c['name'],c['provenance']['checkpoint_sha256']),CHECKPOINTS[index])
   self.assertEqual(c['provenance']['parent_opening_sha256'],OPENING_SHA)
   for stage in ('complete_placement_equal','complete_deployment_equal','complete_opening_equal'):self.assertTrue(c['provenance'][stage])
   self.assertFalse(c['provenance']['upstream_rerun']);p=c['entry_control']
   self.assertTrue(p['retained_ranges_unchanged']);self.assertGreater(p['retained_bytes'],100000000)
   self.assertEqual(p['vm_before_sha256'],p['vm_after_sha256'])
   self.assertEqual(len(p['updates']),183);self.assertEqual(len(p['calls']),2)
   self.assertTrue(p['request_consumed']);self.assertFalse(p['completion_reported'])
   self.assertEqual(p['pending_call']['va'],'0x4551c0');self.assertEqual(p['pending_call']['args'],[0,1])
   self.assertTrue(p['pending_call']['natural_stack_verified']);self.assertFalse(p['pending_call']['first_instruction_executed'])
   self.assertEqual(p['pending_call']['return_va'],'0x49a0d4')
   self.assertEqual(p['updates'][-1]['after'],{'state':6,'delay':0,'request':0,'completion':0,'busy':0,'task_phase':5})
   for key in ('scene_vm_executed','preflight_executed','world_update_loop_executed','live_rendering'):self.assertFalse(p[key])
  self.assertEqual(data['inherited_refusals'],read_opening()['inherited_refusals'])

 def test_finite_guard_and_unsupported_native_caller_refuse(self):
  e=SchoolEntryControlEmulator()
  with self.assertRaises(RuntimeError):e.run_entry_control()
  self.assertFalse(e.entry_loading);e.entry_loading=True;e.entry_allowed=[(STACK,STACK+65536)]
  for at in (0,VM,TACT+0x171,TACT+0x43,UNITCTRL,CONTROL+10):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,1,0,None)
  e.uc.reg_write(UC_X86_REG_ESP,STACK+0xFF00);e.uc.mem_write(STACK+0xFF00,struct.pack('<I',RETURN))
  e.uc.reg_write(UC_X86_REG_ECX,UNITCTRL);e.uc.mem_write(CONTROL+12,b'\x07')
  for va in (0x499DA0,0x453F10,0x415070,0x456B20,0x4551C0,0x4CE8F0,0x46B470):
   with self.assertRaises(RuntimeError):e._hook(e.uc,va,1,None)
  with self.assertRaises(RuntimeError):e.run_entry_control()

 def test_parent_boundary_and_no_preflight_native_range(self):
  self.assertEqual(len(read_opening()['cases']),3)
  for c in read_opening()['cases']:
   self.assertEqual(c['scene_opening']['opening']['stop_phase'],5)
   self.assertFalse(c['scene_opening']['scene_vm_executed'])
  self.assertIn(0x41508D,CODE);self.assertIn(0x49A0CF,CODE)
  self.assertNotIn(0x4551C0,CODE);self.assertNotIn(0x4CE8F0,CODE);self.assertNotIn(0x49A310,CODE)

if __name__=='__main__':unittest.main()
