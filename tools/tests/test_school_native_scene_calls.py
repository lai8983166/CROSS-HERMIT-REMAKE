import gzip,json,struct,unittest
from types import SimpleNamespace
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_EBP,UC_X86_REG_ESP,UC_X86_REG_EBX,UC_X86_REG_ESI,UC_X86_REG_EDI,UC_X86_REG_EFLAGS
from tools.school_native_scene import ROOT,NativeSceneCalls,SOURCE,source_contract,cdecl_thunk,ScriptBoundary

class NativeSceneCallTests(unittest.TestCase):
 def instance(self):
  c=NativeSceneCalls.__new__(NativeSceneCalls);c.pid=7;c.owned=SimpleNamespace(members=lambda:[7]);c.scene=76;c.main=0x1080000;c.phase=0;return c
 def test_source_factory_scheduler_callback_contract(self):
  r=source_contract();self.assertEqual((r['event'],r['callback'],r['source_scenarios']),(16,0x451670,[76,77]));self.assertFalse(r['physical_input_injected']);self.assertFalse(r['retained_checkpoint_rehydrated'])
 def test_no_arbitrary_scene_or_foreign_process(self):
  with self.assertRaisesRegex(ValueError,'source selected scenarios'):NativeSceneCalls(7,None,0)
  c=self.instance();c.owned=SimpleNamespace(members=lambda:[])
  with self.assertRaisesRegex(ValueError,'owned native runtime'):c.validate(0x4e1b60,0,())
 def test_ordered_context_selection_event(self):
  c=self.instance()
  for phase,(va,recv,args) in enumerate([(0x4e1b60,0,()),(0x4da860,0,(76,)),(0x439e30,c.main+0x10,(16,))]):c.phase=phase;c.validate(va,recv,args)
  c.phase=3
  with self.assertRaisesRegex(ValueError,'ordered exact'):c.validate(0x4e1b60,0,())
 def test_no_direct_scene_callback_or_factory_shortcut(self):
  c=self.instance()
  for va in (0x451080,0x451670,0x4539b0,0x454cf0,0x46b470,0x4217c0):
   with self.assertRaisesRegex(ValueError,'ordered exact'):c.validate(va,0,())
 def test_wrong_main_event_or_cdecl_arity_is_rejected(self):
  c=self.instance();c.phase=2
  for receiver,args in [(c.main,(16,)),(c.main+0x10,(0,)),(c.main+0x10,())]:
   with self.assertRaisesRegex(ValueError,'ordered exact'):c.validate(0x439e30,receiver,args)
  c.phase=1
  for args in [(),(77,),(76,0)]:
   with self.assertRaisesRegex(ValueError,'ordered exact'):c.validate(0x4da860,0,args)
 def test_original_scenario_function_under_real_cdecl_thunk(self):
  raw=SOURCE.read_bytes()
  for scene in (76,77):
   with self.subTest(scene=scene):
    u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x400000,(len(raw)+4095)&~4095);u.mem_write(0x400000,raw)
    for at,n in [(0x31000000,65536),(0x32000000,4096),(0x33000000,4096),(0x34000000,4096)]:u.mem_map(at,n)
    u.mem_write(0x32000000,cdecl_thunk());u.mem_write(0x33000000,struct.pack('<11I',0x4da860,0,1,scene,0,0,0,0,0,0,0));sp=0x3100ff00;u.mem_write(sp,struct.pack('<2I',0x34000000,0x33000000))
    expected={UC_X86_REG_EBX:0x12345678,UC_X86_REG_ESI:0x23456789,UC_X86_REG_EDI:0x3456789a,UC_X86_REG_EBP:0x456789ab}
    for reg,value in expected.items():u.reg_write(reg,value)
    u.reg_write(UC_X86_REG_ESP,sp);u.reg_write(UC_X86_REG_EFLAGS,0x202);u.emu_start(0x32000000,0x34000000,count=50000)
    b=bytes(u.mem_read(0x33000000,44));self.assertEqual(struct.unpack_from('<I',b,32),struct.unpack_from('<I',b,36));self.assertEqual(struct.unpack_from('<I',b,40)[0],0x4c4c4143);self.assertEqual(u.reg_read(UC_X86_REG_ESP),sp+8)
    for reg,value in expected.items():self.assertEqual(u.reg_read(reg),value)
    self.assertEqual(bytes(u.mem_read(0x7f4488,2)),struct.pack('<H',scene));self.assertEqual(bytes(u.mem_read(0x8093f8,0x29a)),bytes(0x29a))
 def test_recorded_early_world_loop_cannot_finish_script_capture(self):
  r=json.loads(gzip.decompress((ROOT/'analysis/school-native-scene-76-v6-20261021.json.gz').read_bytes()))['case']['probe'];boundary=ScriptBoundary()
  for s in r['samples']:
   if 'node_head_hex' in s:self.assertEqual(boundary.observe(bytes.fromhex(s['node_head_hex']),bytes.fromhex(s['VM_hex']),s['elapsed']),(False,False))
 def test_recorded_active_script_does_finish_without_waiting_for_recapture(self):
  r=json.loads(gzip.decompress((ROOT/'analysis/school-native-scene-76-v5-20261021.json.gz').read_bytes()))['case']['probe'];boundary=ScriptBoundary();finished=[]
  for s in r['samples']:
   if s.get('active_original_script'):finished.append(boundary.observe(bytes.fromhex(s['node_head_hex']),bytes.fromhex(s['VM_hex']),s['elapsed'])[1])
  self.assertTrue(any(finished));self.assertGreater(len(boundary.PCs),1)

if __name__=='__main__':unittest.main()
