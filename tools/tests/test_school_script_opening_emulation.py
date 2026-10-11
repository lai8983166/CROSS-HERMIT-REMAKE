import hashlib,json,struct,unittest
from tools.school_script_opening_emulation import *

EVIDENCE_SHA256='b76eaae2a083ea1f71ea525778aac9e6e0ea978941e149705c6057773362521f'
class ScriptOpeningNativeTests(unittest.TestCase):
 def test_actual_normal_opening_native_waits_pending_and_parent_provenance(self):
  raw=(ROOT/'analysis/school-script-opening-v1-20261012.json').read_bytes()
  self.assertEqual(hashlib.sha256(raw).hexdigest(),EVIDENCE_SHA256);data=json.loads(raw)
  self.assertEqual(len(data['cases']),3)
  for index,c in enumerate(data['cases']):
   self.assertEqual((c['name'],c['provenance']['checkpoint_sha256']),CHECKPOINTS[index])
   self.assertEqual(c['provenance']['parent_preflight_sha256'],PARENT_SHA)
   self.assertTrue(c['provenance']['complete_parent_stages_equal']);self.assertFalse(c['provenance']['upstream_rerun'])
   p=c['script_opening'];self.assertTrue(p['retained_ranges_unchanged']);self.assertGreater(p['retained_bytes'],100000000)
   self.assertEqual(len(p['updates']),107);self.assertEqual(len(p['commands']),14)
   self.assertEqual(p['pending_call']['args'],[0,p['inputs']['script_pointer']+660,1])
   self.assertTrue(p['pending_call']['natural_stack_verified']);self.assertFalse(p['pending_call']['first_instruction_executed'])
   self.assertEqual(p['pending_call']['return_va'],'0x4ced48');self.assertEqual(p['presentation_calls'],5564)
   for stage in ('before','after'):self.assertEqual([(r['pointer'],r['bytes']) for r in p[stage]],list(REGIONS))
   digest=hashlib.sha256(trace_bytes(p['presentation_first_update'])).hexdigest()
   self.assertEqual(p['presentation_frames'],[{'update':i,'calls':52,'sha256':digest} for i in range(107)])
   self.assertEqual(hashlib.sha256(trace_bytes(p['presentation_first_update'])*107).hexdigest(),p['presentation_sha256'])
   self.assertTrue(p['normal_vm_executed']);self.assertTrue(p['native_fade_executed'])
   for key in ('synthetic_completion_callback','full_task_wrapper_executed','world_update_loop_executed','dialogue_executed','waves_executed','live_rendering','live_audio'):self.assertFalse(p[key])
   self.assertEqual(bytes.fromhex(p['after'][0]['hex'])[0x170:0x172],bytes(2))
  self.assertEqual(data['inherited_refusals'],read_parent()['inherited_refusals'])

 def test_finite_writes_and_actual_selected_parent_are_required(self):
  e=SchoolScriptOpeningEmulator()
  with self.assertRaises(RuntimeError):e.run_script_opening()
  self.assertFalse(e.script_opening_loading);e.script_opening_loading=True
  e.script_opening_allowed=[(STACK,STACK+65536),(VM,VM+0x9400),(WORK+0x1D,WORK+0x20)]
  for at in (0,TACT,WORK,WORK+0x1C,WORK+0x20,CONTROL+12,0x809372,0x8093C4):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,1,0,None)
  e._write_hook(e.uc,0,WORK+0x1E,2,1,None)
  with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,WORK+0x1E,3,1,None)

 def test_wrong_callers_active_presentation_and_full_world_are_refused(self):
  e=SchoolScriptOpeningEmulator();e.script_opening_loading=True;e.script_opening_inputs={'overlay_origin':[0,0]}
  e.uc.reg_write(UC_X86_REG_ESP,STACK+0xFF00);e.uc.mem_write(STACK+0xFF00,struct.pack('<17I',RETURN,*([0]*16)))
  e.uc.reg_write(UC_X86_REG_ECX,TACT)
  for va in (0x4CE8F0,0x497AA0,*PRESENTATION,0x454CF0,0x46B470,0x4C5EA0,0x4CDF80):
   with self.assertRaises(RuntimeError):e._hook(e.uc,va,1,None)
  self.assertIn(0x497C11,CODE);self.assertIn(0x4CCDFF,CODE)
  self.assertNotIn(0x454CF0,CODE);self.assertNotIn(0x4C5EA0,CODE);self.assertNotIn(0x4CDF80,CODE)

if __name__=='__main__':unittest.main()
