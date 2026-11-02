"""Actual x86 execution under delayed callbacks and host observation budgets."""
import ast,hashlib,inspect,struct,textwrap,time,unittest
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
import unicorn.x86_const as x86
from tools import terminal_battle_exit_budget as budget
from tools import terminal_battle_exit_emulation as source
from tools import terminal_battle_exit_verification as verifier

class HostSliceTests(unittest.TestCase):
 def execute(self,program,limit,delay=False,warm=False):
  u=Uc(UC_ARCH_X86,UC_MODE_32);base=0x100000;stop=base+0x100;data=0x200000;stack=0x300000
  for p in (base,data,stack):u.mem_map(p,4096)
  u.mem_write(base,program);u.mem_write(stack+0x800,struct.pack('<I',stop))
  def reset():
   for reg,value in ((x86.UC_X86_REG_EAX,0xA5A5A5A5),(x86.UC_X86_REG_ECX,0),(x86.UC_X86_REG_EDI,0),(x86.UC_X86_REG_EFLAGS,2),(x86.UC_X86_REG_ESP,stack+0x800)):u.reg_write(reg,value)
   u.mem_write(data,bytes(128))
  reset()
  if warm:
   for i in range(100):
    u.emu_start(base if i==0 else u.reg_read(x86.UC_X86_REG_EIP),stop,count=5)
    if u.reg_read(x86.UC_X86_REG_EIP)==stop:break
   else:self.fail('finite warmup')
   reset();u.ctl_flush_tb()
  pcs=[];writes=[];first=0;slept=False
  def code(uc,at,size,_):
   nonlocal slept
   if at==stop:uc.emu_stop();return
   if budget.yield_before_observation(uc,at,stop,len(pcs),first,limit):return
   if delay and not slept and at==base+10:time.sleep(0.02);slept=True
   pcs.append(at)
  u.hook_add(UC_HOOK_CODE,code);u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,access,p,n,v,_:writes.append((p,n,v)))
  for i in range(100):
   first=len(pcs);u.emu_start(base if i==0 else u.reg_read(x86.UC_X86_REG_EIP),0,timeout=0,count=0)
   if u.reg_read(x86.UC_X86_REG_EIP)==stop:break
  else:self.fail('finite host slices')
  cpu=[u.reg_read(reg) for reg in (x86.UC_X86_REG_EAX,x86.UC_X86_REG_ECX,x86.UC_X86_REG_EDI,x86.UC_X86_REG_ESP,x86.UC_X86_REG_EIP,x86.UC_X86_REG_EFLAGS)]
  return pcs,writes,cpu,bytes(u.mem_read(data,128))
 def test_REP_trace_writes_and_CPU_ignore_wall_time_and_slice_size(self):
  program=b'\xB9'+struct.pack('<I',20)+b'\xBF'+struct.pack('<I',0x200000)+b'\xF3\xAB\x90\xC3';expected=self.execute(program,1000)
  self.assertEqual(len(expected[0]),25);self.assertEqual(len(expected[1]),20);self.assertEqual(expected[3][:80],b'\xA5'*80)
  for limit in (1,5):
   for warm in (False,True):
    with self.subTest(limit=limit,warm=warm):self.assertEqual(self.execute(program,limit,True,warm),expected)
 def test_NOP_program_has_no_slice_boundary_observation(self):
  program=b'\x90'*20+b'\xB8'+struct.pack('<I',7)+b'\xC3';expected=self.execute(program,1000);self.assertEqual(len(expected[0]),22)
  for limit in (1,5):self.assertEqual(self.execute(program,limit,True,True),expected)
 def test_original_stop_is_processed_even_at_budget_boundary(self):
  fake=type('Stop',(),dict(emu_stop=lambda self:setattr(self,'stopped',True)))();self.assertFalse(budget.yield_before_observation(fake,8,8,5,0,5));self.assertFalse(hasattr(fake,'stopped'));self.assertTrue(budget.yield_before_observation(fake,7,8,5,0,5));self.assertTrue(fake.stopped)
 def test_source_yields_before_original_entry_and_return_observers(self):
  tree=ast.parse(textwrap.dedent(inspect.getsource(source.BattleExitMachine.code)));first=tree.body[0].body[0]
  self.assertIsInstance(first,ast.If);self.assertIn('budget.yield_before_observation',ast.unparse(first.test))
 def test_bulk_drivers_disable_engine_timeout_and_count(self):
  for fn in (source.BattleExitMachine.bex_segment,verifier.execute_current):
   tree=ast.parse(textwrap.dedent(inspect.getsource(fn)));calls=[n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='emu_start'];self.assertEqual(len(calls),1)
   options={k.arg:ast.literal_eval(k.value) for k in calls[0].keywords};self.assertEqual(options,dict(timeout=0,count=0))

if __name__=='__main__':unittest.main()
