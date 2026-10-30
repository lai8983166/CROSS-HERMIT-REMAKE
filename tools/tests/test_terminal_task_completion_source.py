"""Finite original task handoff, exact parent prefix and retained ownership."""
import contextlib,copy,io,unittest
from types import SimpleNamespace
from unittest.mock import patch
from tools import terminal_task_completion_emulation as e

class TerminalTaskCompletionSourceTests(unittest.TestCase):
 def test_source_guard_algorithm_and_reference_unchanged(self):
  old=e.parent.ScriptExitMachine.source_code;new=e.TaskCompletionMachine.source_code
  self.assertEqual(old.__code__,new.__code__);self.assertIs(new.__globals__['ALLOWED'],e.ALLOWED)
  self.assertEqual(e.REFERENCE.__code__,e.parent.REFERENCE.__code__)
  self.assertEqual(e.ALLOWED-e.parent.ALLOWED,frozenset(range(0x454EE0,0x454F4D)))
 def test_only_new_body_is_complete_original_group_loop(self):
  from capstone import Cs,CS_ARCH_X86,CS_MODE_32
  d=Cs(CS_ARCH_X86,CS_MODE_32);lo,hi=e.EXTRA_RANGES[0];raw=e.CODE[lo-0x400000:hi-0x400000];ins=list(d.disasm(raw,lo))
  self.assertEqual(raw[:3],bytes.fromhex('558bec'));self.assertEqual(ins[-1].mnemonic,'ret');self.assertEqual(ins[-1].address+ins[-1].size,hi)
  self.assertEqual([i.op_str for i in ins if i.mnemonic=='call'],['0x41f4e0','0x56ce80'])
  self.assertEqual(len(e.GROUPS),78);self.assertEqual(e.GROUPS,tuple(i for i in range(10,89) if i!=20))
 def test_phase5_original_fields_and_unconditional_debug_bypass(self):
  from capstone import Cs,CS_ARCH_X86,CS_MODE_32
  d=Cs(CS_ARCH_X86,CS_MODE_32)
  ins=list(d.disasm(e.CODE[0x454E38-0x400000:0x454EA5-0x400000],0x454E38))
  self.assertTrue(any(i.mnemonic=='cmp' and i.op_str=='dword ptr [ecx + 0x4c], 1' for i in ins))
  self.assertEqual([i.op_str for i in ins if i.mnemonic=='call'],['0x467850','0x41f710'])
  bypass=list(d.disasm(e.CODE[0x41F72D-0x400000:0x41F732-0x400000],0x41F72D))
  self.assertEqual([(i.mnemonic,i.op_str) for i in bypass],[('jmp','0x41f811')])
 def test_natural_event_abi_matches_original_rets(self):
  from capstone import Cs,CS_ARCH_X86,CS_MODE_32
  d=Cs(CS_ARCH_X86,CS_MODE_32)
  for at,end in [(0x41F4E0,0x41F59F),(0x41F2A0,0x41F333),(0x56DE40,0x56DEE4)]:
   ins=list(d.disasm(e.CODE[at-0x400000:end-0x400000],at));rets=[i for i in ins if i.mnemonic=='ret'];self.assertTrue(rets)
   self.assertEqual(int(rets[-1].op_str or '0',0),e.EVENTS[at][1])
 def test_namespaced_recorders_keep_parent_algorithms(self):
  for name in ('mark','capture','prefix_counts','observe','segment','frame'):
   old=getattr(e.followup.FollowupMachine,'fu_'+name);new=getattr(e.TaskCompletionMachine,'tc_'+name)
   self.assertEqual(old.__code__.co_code,new.__code__.co_code);self.assertIs(old.__globals__,new.__globals__)
  for oldname,newname in [('fu_actual_root','_tc_actual_root'),('gpu_api','_tc_gpu_api'),('api_crt','_tc_api_crt')]:
   self.assertEqual(getattr(e.followup.FollowupMachine,oldname).__code__.co_code,getattr(e.TaskCompletionMachine,newname).__code__.co_code)
 def test_inherited_crt_observer_has_no_new_role_file_branch(self):
  with patch.object(e.parent.ScriptExitMachine,'__init__',lambda m,*a,**k:setattr(m,'mutable',[])):m=e.TaskCompletionMachine()
  self.assertEqual(m.tc_branch,dict(role=None))
 def test_only_original_two_handshake_bytes_admitted_without_guest_writes(self):
  import ast,inspect,textwrap
  original=[(10,20),(40,50)]
  with patch.object(e.parent.ScriptExitMachine,'__init__',lambda m,*a,**k:setattr(m,'mutable',list(original))):m=e.TaskCompletionMachine()
  self.assertEqual(e.NEW_MUTABLE,((e.TASK+0x171,e.TASK+0x173),))
  self.assertEqual(m.mutable,original+list(e.NEW_MUTABLE))
  tree=ast.parse(textwrap.dedent(inspect.getsource(e.TaskCompletionMachine.__init__)))
  self.assertFalse(any(isinstance(n,ast.Attribute) and n.attr in ('put','mem_write','reg_write') for n in ast.walk(tree)))
  from capstone import Cs,CS_ARCH_X86,CS_MODE_32
  d=Cs(CS_ARCH_X86,CS_MODE_32)
  for pc,off in [(0x454E4B,0x171),(0x454E55,0x172)]:
   i=next(d.disasm(e.CODE[pc-0x400000:pc-0x400000+7],pc));self.assertEqual(i.mnemonic,'mov');self.assertIn('+ 0x'+format(off,'x')+'], 1',i.op_str)
 def prefix(self,change=False):
  want=dict(instructions=10,writes=5,code_sha256='a'*64,write_sha256='b'*64)
  machine=SimpleNamespace(live_input=dict(name='neutral_running'),mark=lambda:dict(want,writes=6) if change else want)
  with patch.object(e,'fixed_parent_forward_summaries',return_value=dict(neutral_running=want)),contextlib.redirect_stdout(io.StringIO()):return e.validate_parent_prefix(machine)
 def test_all_four_parent_cumulative_fields_exact(self):self.assertEqual(self.prefix()['expected'],self.prefix()['actual'])
 def test_changed_parent_prefix_refused(self):
  with self.assertRaises(ValueError):self.prefix(True)
 def test_completed_parent_guard_is_not_relaxed(self):
  import inspect
  self.assertIn("need(at!=0x454E18,'successor task cleanup body remains unexecuted')",inspect.getsource(e.parent.ScriptExitMachine.code))
  self.assertIn("need(not self.script_exit_active",inspect.getsource(e.TaskCompletionMachine.code))
 def gpu_machine(self):
  from tools.tests.test_terminal_script_exit_source import TerminalScriptExitSourceTests
  m,memory=TerminalScriptExitSourceTests().gpu_machine();m.__class__=e.TaskCompletionMachine
  m.task_completion_ready=m.task_completion_active=True;m.task_completion_cleaning=False
  m.tc_current=None;m.tc_gpu=[];m.tc_leaves=[];m.tc_resources=copy.deepcopy(m.se_resources);m.tc_live={r['texture']['pointer']:r for r in m.tc_resources}
  return m,memory
 def test_actual_describe_release_updates_all_inherited_lifetimes_once(self):
  m,memory=self.gpu_machine();f=m._fixture;m.gpu_api(f['target']);self.assertTrue(m.tc_resources[0]['alive'])
  memory[f['sp']]=0x40378D;m.methods[f['target']]=8;m.gpu_api(f['target'])
  self.assertFalse(m.tc_live);self.assertEqual(m.gpu.trace,[('describe',123),('release',123)])
  for prefix in ('tc','se','ld','ml','nd','nx','fu'):
   self.assertFalse(getattr(m,prefix+'_live'));self.assertFalse(getattr(m,prefix+'_resources')[0]['alive'])
  with self.assertRaises(ValueError):m.gpu_api(f['target'])
 def test_new_texture_creation_refused(self):
  m,_=self.gpu_machine();m.methods[m._fixture['target']]=80
  with self.assertRaises(ValueError):m.gpu_api(m._fixture['target'])
 def test_cleared_container_is_not_destroyed_twice(self):
  m=object.__new__(e.TaskCompletionMachine);m.tc_cleanup_skips=[];m.read=lambda at,n:bytes(n)
  m._tc_actual_root=lambda *a: self.fail('cleared original bank may not execute a second root')
  self.assertIsNone(m.tc_actual_root('dead_group',0x41F4E0,[32],e.MAIN+0x844))
  self.assertEqual(m.tc_cleanup_skips[0]['slot'],e.MAIN+0x844+32*8)
 def test_surviving_container_uses_unchanged_original_root(self):
  m=object.__new__(e.TaskCompletionMachine);m.tc_cleanup_skips=[];m.read=lambda at,n:b'\x01'+bytes(n-1);calls=[]
  m._tc_actual_root=lambda *a:calls.append(a) or 17
  self.assertEqual(m.tc_actual_root('live_group',0x41F4E0,[20],e.MAIN+0x844),17);self.assertEqual(len(calls),1);self.assertFalse(m.tc_cleanup_skips)
 def test_helpers_retain_original_capacity_and_ABI(self):self.assertTrue(e.helper_contract()['capacity_and_ABI_unchanged'])

if __name__=='__main__':unittest.main()
