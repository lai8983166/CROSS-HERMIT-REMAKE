import hashlib,json,unittest
from tools.school_scene_opening_emulation import *

EVIDENCE_SHA256='90b4896db16f17e321bd9ea362a92e75fd8b0fb0f1a19dccd8614c7c69aebd31'
class OpeningNativeTests(unittest.TestCase):
 def test_actual_return_opening_and_checkpoint_provenance(self):
  raw=(ROOT/'analysis/school-scene-opening-v1-20261011.json').read_bytes()
  self.assertEqual(hashlib.sha256(raw).hexdigest(),EVIDENCE_SHA256);data=json.loads(raw)
  self.assertEqual(len(data['cases']),3)
  for index,c in enumerate(data['cases']):
   self.assertEqual((c['name'],c['provenance']['checkpoint_sha256']),CHECKPOINTS[index])
   self.assertEqual(c['provenance']['parent_deployment_sha256'],DEPLOYMENT_SHA)
   self.assertTrue(c['provenance']['complete_placement_equal']);self.assertTrue(c['provenance']['complete_deployment_equal'])
   self.assertFalse(c['provenance']['upstream_rerun']);p=c['scene_opening']
   self.assertTrue(p['scene_initialization_completed'])
   for stage in ('initialization','opening'):
    self.assertTrue(p[stage]['retained_ranges_unchanged']);self.assertGreater(p[stage]['retained_bytes'],100000000)
   self.assertTrue(p['initialization']['natural_stack_verified'])
   self.assertEqual(p['initialization']['natural_returns'],['0x451a16','0x45170e'])
   self.assertEqual(p['initialization']['return_value'],0);self.assertEqual(len(p['initialization']['primitives']),4)
   self.assertEqual(len(p['opening']['updates']),215)
   self.assertEqual(sum(u['rectangle_count'] for u in p['opening']['updates']),27392)
   self.assertEqual(p['opening']['native_increment_calls'],214)
   self.assertEqual(p['opening']['stop_phase'],5);self.assertTrue(p['opening']['script_work_requested'])
   for key in ('scene_vm_executed','world_update_loop_executed','live_rendering'):self.assertFalse(p[key])
  self.assertEqual(data['inherited_refusals'],read_deployment()['inherited_refusals'])

 def test_finite_guard_foreign_call_and_invalid_entry_refusal(self):
  e=SchoolSceneOpeningEmulator()
  with self.assertRaises(RuntimeError):e.run_initialization_and_opening()
  self.assertFalse(e.opening_loading);e.opening_loading=True;e.opening_phase='opening'
  e.opening_allowed=[(STACK,STACK+65536)]
  for at in (0,TACT+0x43,TACT+0x34,UNITCTRL,0x7F44A8):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,1,0,None)
  e.uc.reg_write(UC_X86_REG_ESP,STACK+0xFF00);e.uc.reg_write(UC_X86_REG_ECX,TACT)
  e.uc.mem_write(STACK+0xFF00,struct.pack('<I',RETURN));e.uc.mem_write(TACT+0x38,struct.pack('<I',5))
  for va in (0x453F10,0x422360,0x415420,0x410310,0x467AA0,0x4077C0,0x451A60):
   with self.assertRaises(RuntimeError):e._hook(e.uc,va,1,None)

 def test_parent_identity_and_original_opening_ranges(self):
  self.assertEqual(len(read_deployment()['cases']),3)
  self.assertIn(0x4534A1,CODE);self.assertIn(0x467AA0,CODE);self.assertIn(0x41505D,CODE)
  self.assertNotIn(0x45170E,CODE);self.assertNotIn(0x4539B0,CODE);self.assertNotIn(0x4CE8F0,CODE)
  self.assertEqual(len(parent_evidence()['cases']),5)

if __name__=='__main__':unittest.main()
