"""Original command window, finite provenance and inherited source algorithms."""
import contextlib,copy,io,struct,unittest
from types import SimpleNamespace
from unittest.mock import patch
from tools import terminal_script_exit_emulation as e

class TerminalScriptExitSourceTests(unittest.TestCase):
 def test_exact_original_remaining_command_windows_and_parameters(self):
  from tools import terminal_next_dialogue_verification as v
  raw=(e.ROOT/e.terminal.SCRIPT_PATH).read_bytes();segments=v.previous.dialogue.script_commands(raw)['segments']
  for name,delta in [('neutral_running',0),('timeout_before_combat',30)]:
   b=e.branch(name);s=next(s for s in segments if s['index']==b['segment']);rows=[];pc=b['first_PC']
   while pc<=b['final_PC']:
    at=s['code_start']+pc;op,n=struct.unpack_from('<HH',raw,at);rows.append(dict(PC=pc,opcode=op,bytes=n));pc+=n
   self.assertEqual(rows,b['commands']);self.assertEqual(len(rows),12)
   for pc,values in [(324,[7]),(336,[8]),(348,[7,30]),(360,[8,30]),(372,[4,3]),(384,[60]),(396,[60])]:
    at=s['code_start']+pc+delta
    self.assertEqual(list(struct.unpack_from('<'+'I'*len(values),raw,at+4)),[0x20000000+x for x in values])
   self.assertEqual((b['first_PC'],b['final_PC'],b['scene_capture']),(320+delta,404+delta,76+(delta!=0)))
 def test_invalid_branch_refused(self):
  with self.assertRaises(ValueError):e.branch('neutral_running ')
 def test_source_guard_algorithm_and_original_reference_unchanged(self):
  old=e.parent.LastDialogueMachine.source_code;new=e.ScriptExitMachine.source_code
  self.assertEqual(old.__code__,new.__code__);self.assertIs(new.__globals__['ALLOWED'],e.ALLOWED)
  self.assertEqual(e.REFERENCE.__code__,e.parent.REFERENCE.__code__)
  self.assertTrue(e.parent.ALLOWED.issubset(e.ALLOWED))
 def test_extra_bodies_start_at_original_prologue_and_end_at_ret(self):
  from capstone import Cs,CS_ARCH_X86,CS_MODE_32
  d=Cs(CS_ARCH_X86,CS_MODE_32)
  for lo,hi in e.EXTRA_RANGES:
   raw=e.CODE[lo-0x400000:hi-0x400000];self.assertEqual(raw[:3],bytes.fromhex('558bec'))
   ins=list(d.disasm(raw,lo));self.assertEqual(ins[-1].mnemonic,'ret');self.assertEqual(ins[-1].address+ins[-1].size,hi)
   self.assertTrue(all(i.mnemonic!='int3' for i in ins))
 def test_namespaced_recorders_keep_actual_parent_algorithms(self):
  for name in ('mark','capture','prefix_counts','observe','segment','frame','actual_root'):
   old=getattr(e.followup.FollowupMachine,'fu_'+name);new=getattr(e.ScriptExitMachine,'se_'+name)
   self.assertEqual(old.__code__.co_code,new.__code__.co_code);self.assertIs(old.__globals__,new.__globals__)
  for oldname,newname in [('fu_captured','_se_captured'),('gpu_api','_se_gpu_api'),('api_crt','_se_api_crt')]:
   self.assertEqual(getattr(e.followup.FollowupMachine,oldname).__code__.co_code,getattr(e.ScriptExitMachine,newname).__code__.co_code)
 def prefix(self,change=False):
  want=dict(instructions=10,writes=5,code_sha256='a'*64,write_sha256='b'*64)
  machine=SimpleNamespace(live_input=dict(name='neutral_running'),mark=lambda:dict(want,writes=6) if change else want)
  with patch.object(e,'fixed_parent_forward_summaries',return_value=dict(neutral_running=want)),contextlib.redirect_stdout(io.StringIO()):return e.validate_parent_prefix(machine)
 def test_prefix_all_four_cumulative_fields_exact(self):self.assertEqual(self.prefix()['expected'],self.prefix()['actual'])
 def test_changed_original_prefix_refused(self):
  with self.assertRaises(ValueError):self.prefix(True)
 def test_original_special_19_has_two_real_calls(self):
  from capstone import Cs,CS_ARCH_X86,CS_MODE_32
  d=Cs(CS_ARCH_X86,CS_MODE_32);ins=list(d.disasm(e.CODE[0x4CEA1E-0x400000:0x4CEA3C-0x400000],0x4CEA1E))
  self.assertEqual([i.op_str for i in ins if i.mnemonic=='call'],['0x4ce090','0x4ce800'])
  self.assertEqual(ins[-1].op_str,'0x4cff1b')
 def test_helpers_keep_original_capacity_and_ABI(self):self.assertTrue(e.helper_contract()['capacity_and_ABI_unchanged'])
 def gpu_machine(self):
  m=object.__new__(e.ScriptExitMachine);m.script_exit_ready=m.script_exit_active=True;m.script_exit_cleaning=False
  m.se_current=None;m.se_gpu=[];m.se_leaves=[];m.pd_sentences=[]
  record=e.VM+0x458;pointer=0x64001000;target=0x65001000;sp=0x1000;bp=0x2000
  r=dict(generation=5,record=record,texture=dict(pointer=pointer),native_pointer=123,kind='text',label='inherited_text',alive=True)
  m.se_resources=[r];m.se_live={pointer:r}
  for prefix in ('ld','ml','nd','nx','fu'):
   old=copy.deepcopy(r);setattr(m,prefix+'_resources',[old]);setattr(m,prefix+'_live',{pointer:old})
  m.methods={target:56};m._fixture=dict(sp=sp,bp=bp,target=target,pointer=pointer,record=record)
  memory={sp:0x403A44,sp+4:pointer,sp+8:0,sp+12:bp-36,record+44:pointer}
  m.get=lambda at,*args:memory[at];m.getreg=lambda name:dict(ESP=sp,EBP=bp)[name]
  m.outputs=[];m.map_new=lambda p,n:None;m.uc=SimpleNamespace(mem_write=lambda p,b:m.outputs.append((p,b)))
  m.return_api=lambda esp,value,pop:m.outputs.append(('return',esp,value,pop))
  class GPU:
   def __init__(self):self.trace=[]
   def describe(self,p):
    self.trace.append(('describe',p));return dict(hr=0,hex='0011223344556677')
   def release(self,p):self.trace.append(('release',p));return dict(count=0)
  m.gpu=GPU();return m,memory
 def test_inherited_describe_and_release_preserve_generation_and_payload(self):
  m,memory=self.gpu_machine();f=m._fixture
  # Exercise the full wrapper and actual namespaced ABI algorithm with seeded owners.
  m.gpu_api(f['target']);self.assertEqual(m.outputs[0],(f['bp']-36,bytes.fromhex('0011223344556677')))
  self.assertTrue(m.se_resources[0]['alive']);self.assertEqual(m.se_gpu[0]['op'],'describe');self.assertEqual(m.se_gpu[0]['wire_index'],0)
  memory[f['sp']]=0x40378D;m.methods[f['target']]=8
  m.gpu_api(f['target']);self.assertFalse(m.se_resources[0]['alive']);self.assertFalse(m.se_live)
  self.assertEqual(m.gpu.trace,[('describe',123),('release',123)])
  self.assertEqual([c['generation'] for c in m.se_gpu],[5,5]);self.assertEqual(m.se_resources[0]['release_wire_index'],1)
  for prefix in ('ld','ml','nd','nx','fu'):
   self.assertFalse(getattr(m,prefix+'_live'));self.assertFalse(getattr(m,prefix+'_resources')[0]['alive'])
 def test_new_gpu_creation_refused(self):
  m,_=self.gpu_machine();m.methods[m._fixture['target']]=80
  with self.assertRaises(ValueError):m.gpu_api(m._fixture['target'])

if __name__=='__main__':unittest.main()
