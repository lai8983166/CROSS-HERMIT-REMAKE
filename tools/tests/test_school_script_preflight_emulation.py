import hashlib,json,struct,unittest
from tools.school_script_preflight_emulation import *

EVIDENCE_SHA256='b3de8be5e282c4d2e00c2acca5722f7536746aa62c8aff1d6f58d32988ce7c42'
class PreflightNativeTests(unittest.TestCase):
 def test_actual_preflight_binding_and_retained_parent_provenance(self):
  raw=(ROOT/'analysis/school-script-preflight-v1-20261011.json').read_bytes()
  self.assertEqual(hashlib.sha256(raw).hexdigest(),EVIDENCE_SHA256);data=json.loads(raw)
  self.assertEqual(len(data['cases']),3)
  for index,c in enumerate(data['cases']):
   self.assertEqual((c['name'],c['provenance']['checkpoint_sha256']),CHECKPOINTS[index])
   self.assertEqual(c['provenance']['parent_entry_sha256'],ENTRY_SHA)
   self.assertTrue(c['provenance']['complete_parent_stages_equal']);self.assertFalse(c['provenance']['upstream_rerun'])
   p=c['script_preflight'];self.assertTrue(p['retained_ranges_unchanged']);self.assertGreater(p['retained_bytes'],100000000)
   for stage in ('before','preflight_after','after'):
    self.assertEqual([(r['pointer'],r['bytes']) for r in p[stage]],list(REGIONS))
   self.assertEqual([x['opcode'] for x in p['commands']],[167,8,166,11,19])
   self.assertEqual(p['natural_returns'],['0x49a0d4','0x3000000']);self.assertTrue(p['natural_stack_verified'])
   self.assertEqual((p['preflight_return'],p['controller_return']),(1,0))
   self.assertTrue(p['preflight_vm_executed']);self.assertTrue(p['selected_vm_bound'])
   for key in ('playback_vm_executed','world_update_loop_executed','live_rendering','live_audio'):self.assertFalse(p[key])
   self.assertEqual(p['after'][2]['hex'],'010101');self.assertEqual(bytes.fromhex(p['after'][1]['hex'])[12],7)
   vm=bytes.fromhex(p['after'][3]['hex']);self.assertEqual(vm[4:6],b'\x01\x01');self.assertEqual(vm[0x1C:0x20],bytes(4))
   self.assertEqual(vm[0x92E1],0);self.assertEqual(len(p['primitives']),7)
  self.assertEqual(data['inherited_refusals'],read_entry()['inherited_refusals'])

 def test_finite_guard_requires_natural_cpu_and_exact_sparse_ownership(self):
  e=SchoolScriptPreflightEmulator()
  with self.assertRaises(RuntimeError):e.run_script_preflight()
  self.assertFalse(e.preflight_loading);e.preflight_loading=True
  e.preflight_allowed=[(STACK,STACK+65536),(VM,VM+0x9400)]+[(at,at+n) for at,n in SPARSE]
  for at in (0,TACT+0x171,TACT+0x64,CONTROL+13,SPARSE[0][0]+2,SPARSE[-1][0]-1):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,1,0,None)
  for at,n in SPARSE:e._write_hook(e.uc,0,at,n,0,None)
  with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,SPARSE[0][0],3,0,None)

 def test_invalid_callers_and_unexecuted_playback_ranges_refuse(self):
  e=SchoolScriptPreflightEmulator();e.preflight_loading=True
  e.preflight_inputs={'strcmp_import':0x7000000,'tick_import':0x7000010,'script_pointer':0xE741BD0}
  e.uc.reg_write(UC_X86_REG_ESP,STACK+0xFF00);e.uc.mem_write(STACK+0xFF00,struct.pack('<8I',RETURN,*([0]*7)))
  e.uc.reg_write(UC_X86_REG_ECX,TACT)
  for va in (0x4551C0,0x455060,0x4CE8F0,0x4549D0,0x7000000,0x7000010,0x42B2D0,0x41E500,0x40D120,0x56CEC0,0x46B470):
   with self.assertRaises(RuntimeError):e._hook(e.uc,va,1,None)
  self.assertIn(0x4551C0,CODE);self.assertIn(0x4CE8F0,CODE)
  self.assertNotIn(0x46B470,CODE);self.assertNotIn(0x49A310,CODE)

if __name__=='__main__':unittest.main()
