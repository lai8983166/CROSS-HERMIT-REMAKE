import copy,json,struct,unittest
from pathlib import Path
from types import SimpleNamespace
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EAX,UC_X86_REG_EBX,UC_X86_REG_ESI,UC_X86_REG_EDI
from tools.school_scheduler_lifetime import ROOT,SOURCE,NativeCalls,call_thunk,source_contract

class CallContractTests(unittest.TestCase):
 def instance(self,members=(17,)):
  c=NativeCalls.__new__(NativeCalls);c.pid=17;c.owned=SimpleNamespace(members=lambda:list(members));c.active=None;c.data=0x10000000;c.kernel_close=0x76001000;c.allowed_closes=set();return c
 def test_source_thread_and_callback_contract(self):
  r=source_contract();self.assertEqual((r['worker'],r['base_callback']),(0x421f50,0x422330));self.assertFalse(r['source_callbacks_replaced']);self.assertFalse(r['retained_scene_or_world_execution'])
 def test_foreign_job_process_is_refused_before_open(self):
  with self.assertRaisesRegex(ValueError,'owned Job process'):NativeCalls(17,SimpleNamespace(members=lambda:[]))
 def test_unknown_entry_or_wrong_arity_never_reaches_native_call(self):
  c=self.instance()
  for va,args in [(0x49e540,()),(0x421540,(1,)),(0x4216c0,())]:
   with self.assertRaisesRegex(ValueError,'entry/ABI'):c.call(va,c.data+0x1000,args)
 def test_nonprivate_receiver_and_bad_bucket_are_refused(self):
  c=self.instance()
  with self.assertRaisesRegex(ValueError,'private source receiver'):c.call(0x421540,0x7a4a00)
  for bucket in (-1,32):
   with self.assertRaisesRegex(ValueError,'bounded original bucket'):c.call(0x4216c0,c.data+0x1000,(c.data+0x2000,bucket,0))
 def test_unobserved_handle_and_unsafe_write_are_refused(self):
  c=self.instance()
  with self.assertRaisesRegex(ValueError,'observed exited owned worker'):c.call(c.kernel_close,0,(123,),label='supplemental_CloseHandle')
  c.blocks=[(c.data,4096)]
  with self.assertRaisesRegex(ValueError,'only new private allocation'):c.put(0x421540,b'\x90')
 def test_thunk_runs_original_constructor_and_three_argument_registration(self):
  u=Uc(UC_ARCH_X86,UC_MODE_32);raw=SOURCE.read_bytes();u.mem_map(0x400000,(len(raw)+4095)&~4095);u.mem_write(0x400000,raw)
  u.mem_map(0x10000000,0x4000);u.mem_map(0x20000000,0x10000);u.mem_map(0x30000000,4096);u.mem_write(0x30000000,call_thunk());u.mem_map(0x40000000,4096)
  param=0x10000000;node=param+0x2000;manager=param+0x1000;sp=0x2000ff00
  def invoke(va,recv,args=()):
   u.mem_write(param,struct.pack('<11I',va,recv,len(args),*(list(args)+[0]*(3-len(args))),0,0,0,0,0));u.mem_write(sp,struct.pack('<2I',0x40000000,param))
   for reg,v in [(UC_X86_REG_ESP,sp),(UC_X86_REG_EBX,0x12345678),(UC_X86_REG_ESI,0x34567890),(UC_X86_REG_EDI,0x45678901)]:u.reg_write(reg,v)
   u.emu_start(0x30000000,0x40000000,count=200000)
   out=bytes(u.mem_read(param,44));self.assertEqual(struct.unpack_from('<I',out,32),struct.unpack_from('<I',out,36));self.assertEqual(struct.unpack_from('<I',out,40)[0],0x4c4c4143)
   self.assertEqual(u.reg_read(UC_X86_REG_ESP),sp+8);self.assertEqual(u.reg_read(UC_X86_REG_EAX),0)
   self.assertEqual([u.reg_read(r) for r in (UC_X86_REG_EBX,UC_X86_REG_ESI,UC_X86_REG_EDI)],[0x12345678,0x34567890,0x45678901])
  u.mem_write(node,b'\xa5'*128);invoke(0x422290,node)
  expected=bytearray(b'\xa5'*128);struct.pack_into('<I',expected,0,0x594a54);expected[0x28]=0;self.assertEqual(bytes(u.mem_read(node,128)),expected)
  invoke(0x4216c0,manager,(node,31,0x11223344))
  self.assertEqual(bytes(u.mem_read(manager+31*8,4)),struct.pack('<I',node));self.assertEqual(bytes(u.mem_read(node+8,4)),struct.pack('<I',manager));self.assertEqual(bytes(u.mem_read(node+0x18,4)),struct.pack('<I',0x11223344))

if __name__=='__main__':unittest.main()
