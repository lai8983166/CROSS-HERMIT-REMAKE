"""Original script tail, read-only replay observer, and integration rejection."""
import copy,os,struct,unittest
from unittest.mock import patch
from tools import terminal_script_exit_emulation as e
from tools import terminal_script_exit_verification as v
REPORT=os.environ.get('TERMINAL_SCRIPT_EXIT_REPORT','analysis/terminal-script-exit-source-v2-20261030.json.gz')

class TerminalScriptExitStaticTests(unittest.TestCase):
 @staticmethod
 def fixture(name):
  raw=(e.ROOT/e.terminal.SCRIPT_PATH).read_bytes();cfg=v.branch(name);s=next(s for s in v.previous_stage.previous.dialogue.script_commands(raw)['segments'] if s['index']==cfg['segment']);code=raw[s['code_start']:s['code_end']];base=0xE000000;vm=bytearray(0x9400);struct.pack_into('<I',vm,16,base)
  commands=[dict(c,source_pointer=base+c['PC'],raw_hex=code[c['PC']:c['PC']+c['bytes']].hex()) for c in cfg['commands']]
  return dict(input=dict(name=name),terminal_script_exit=dict(branch=cfg,before=dict(memory=[dict(pointer=e.VM,bytes=len(vm),hex=vm.hex()),dict(pointer=base,bytes=len(code),hex=code.hex())]),commands=commands))
 def test_exact_twelve_original_commands_and_all_operands(self):
  for name,pc in [('neutral_running',404),('timeout_before_combat',434)]:
   r=v.source(self.fixture(name));self.assertEqual(r['termination_PC'],pc);self.assertEqual(len(r['commands']),12);self.assertEqual(r['commands'][-1]['opcode'],19);self.assertEqual(r['operands'][118],[[60]])
 def test_unknown_original_case_refused(self):
  with self.assertRaises(ValueError):v.branch('neutral_running ')
 def test_extra_successor_dispatch_refused(self):
  r=self.fixture('neutral_running');r['terminal_script_exit']['commands'].append(dict(PC=408,opcode=19,bytes=4))
  with self.assertRaises(ValueError):v.source(r)
 def test_missing_termination_refused(self):
  r=self.fixture('neutral_running');r['terminal_script_exit']['commands'].pop()
  with self.assertRaises(ValueError):v.source(r)
 def test_full_command_bytes_required(self):
  r=self.fixture('timeout_before_combat');r['terminal_script_exit']['commands'][0]['raw_hex']='0000'
  with self.assertRaises(ValueError):v.source(r)
 def test_wrong_source_pointer_refused(self):
  r=self.fixture('neutral_running');r['terminal_script_exit']['commands'][0]['source_pointer']+=4
  with self.assertRaises(ValueError):v.source(r)
 def test_source_guard_range_extension_independently_bounded(self):
  with patch.object(e,'EXTRA_RANGES',e.EXTRA_RANGES+((0x400000,0x592000),)):
   with self.assertRaises(ValueError):v.source(self.fixture('neutral_running'))
 def test_frozen_replay_instruction_algorithms(self):
  for name in ('_initialize','cleanup'):
   a=getattr(v.Replay,name).__code__;b=getattr(v.previous_stage.Replay,name).__code__;self.assertEqual(a.co_code,b.co_code);self.assertEqual(a.co_names,b.co_names)
  a=v.Replay.execute.__globals__['OBSERVER_SCHEMA_AUDIT'];self.assertTrue(a['only_declared_observation_payloads_changed']);self.assertEqual(a['query_payload_builders_changed'],1);self.assertEqual(a['command_payload_builders_changed'],1);self.assertFalse(a['original_machine_events_filtered'])
 def test_replay_uses_current_stage_and_actual_cleanup(self):
  self.assertIn('terminal_script_exit',v.Replay._initialize.__code__.co_consts);self.assertNotIn('terminal_last_dialogue',v.Replay._initialize.__code__.co_consts)
  self.assertIn('script_exit_cleanup',v.Replay.execute.__code__.co_consts);self.assertNotIn('last_dialogue_cleanup',v.Replay.execute.__code__.co_consts)
  self.assertIs(v.Replay.execute.__globals__['need'],v.replay_need)
  self.assertEqual(v.Replay.execute.__globals__['branch']('neutral_running')['final_PC'],408);self.assertEqual(v.branch('neutral_running')['final_PC'],404)
  self.assertEqual(v.new_resources.__module__,'tools.terminal_script_exit_verification');self.assertIs(v.Replay.execute.__globals__['new_resources'],v.new_resources)
 def test_current_creation_cursor_never_uses_parent_new_resources(self):
  row=dict(terminal_script_exit=dict(prefix=dict(GPU_wire=100),resources=[dict(create_wire_index=20),dict(create_wire_index=99),dict(create_wire_index=100)]));self.assertEqual(v.new_resources(row),[dict(create_wire_index=100)])
 def work(self):
  w=bytearray(b'\xa5'*0x24C0);w[0x2499]=0;vm=bytearray(0x9400)
  return dict(work=w.hex(),VM=vm.hex())
 def test_inactive_work_retains_every_byte(self):
  s=self.work();w,g=v.work_after(s);self.assertEqual(w,s['work']);self.assertEqual(g,0)
 def test_all60_original_fade_steps_keep_remainder32(self):
  s=self.work();original=bytes.fromhex(s['work'])
  for i in range(1,61):
   w,g=v.work_after(s,start=i==1);s['work']=w;vm=bytearray.fromhex(s['VM']);vm[0x92E0]=g;s['VM']=vm.hex();f=v.work_fields(s)
   self.assertEqual(f,dict(value=38912-648*i,step=648,direction=0,active=int(i<60),status=int(i<60),remaining=60-i));raw=bytes.fromhex(w);self.assertEqual(raw[:0x2490],original[:0x2490]);self.assertEqual(raw[0x24A0:],original[0x24A0:]);self.assertEqual(g,int(i<60))
  self.assertEqual(v.work_after(s),(s['work'],0))
 def test_nonoriginal_step_refused(self):
  s=self.work();w=bytearray.fromhex(s['work']);w[0x2498:0x249B]=bytes((0,1,1));struct.pack_into('<i',w,0x2494,649);struct.pack_into('<i',w,0x249C,1);s['work']=w.hex()
  with self.assertRaises(ValueError):v.work_after(s)
 def test_invalid_work_direction_refused(self):
  s=self.work();w=bytearray.fromhex(s['work']);w[0x2498:0x249B]=bytes((1,1,1));struct.pack_into('<i',w,0x2494,648);struct.pack_into('<i',w,0x249C,1);s['work']=w.hex()
  with self.assertRaises(ValueError):v.work_after(s)
 def test_expired_active_work_refused(self):
  s=self.work();w=bytearray.fromhex(s['work']);w[0x2498:0x249B]=bytes((0,1,1));struct.pack_into('<i',w,0x2494,648);struct.pack_into('<i',w,0x249C,0);s['work']=w.hex()
  with self.assertRaises(ValueError):v.work_after(s)
 def test_original_timer_strict_comparison_and_offsets(self):
  from capstone import Cs,CS_ARCH_X86,CS_MODE_32
  md=Cs(CS_ARCH_X86,CS_MODE_32)
  expected={0x4CCBF0:('mov','dx, word ptr [ecx + eax + 0x28]'),0x4CCC03:('mov','si, word ptr [ecx + eax + 0x2a]'),0x4CCC1C:('add','ax, 1'),0x4CCC31:('cmp','edx, esi'),0x4CCC33:('jle','0x4ccc39')}
  for at,want in expected.items():
   i=next(md.disasm(e.CODE[at-0x400000:at-0x400000+16],at));self.assertEqual((i.mnemonic,i.op_str),want)
 def test_parent_preflight_requires_every_counter_and_digest(self):
  with self.assertRaises(ValueError):v.prefix_trace(dict(input=dict(name='neutral_running'),terminal_script_exit=dict(before=dict(trace={}))))
 def test_actual_original_helper_capacity_unchanged(self):self.assertEqual(v.helper_contract(),e.parent.helper_contract());self.assertTrue(v.helper_contract()['capacity_and_ABI_unchanged'])

class TerminalScriptExitTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=v.load_report(e.ROOT/REPORT);cls.rows=cls.data['cases']
 @staticmethod
 def changed(obj,path,value):
  if not path:return value
  out=copy.copy(obj);out[path[0]]=TerminalScriptExitTests.changed(obj[path[0]],path[1:],value);return out
 def reject(self,path,value,check,index=0):
  with self.assertRaises((ValueError,KeyError,IndexError,StopIteration,AssertionError)):check(self.changed(self.rows[index],path,value))
 def stage(self,path,value,check,index=0):self.reject(('terminal_script_exit',)+tuple(path),value,check,index)
 def test_both_full_original_script_terminations(self):
  self.assertEqual(self.data['source_contract'],e.source_contract())
  for r,pc in zip(self.rows,[404,434]):
   with self.subTest(case=r['input']['name']):p=v.verify_case(r);self.assertEqual(p['timing']['VM_PC'],pc);self.assertEqual(p['timing']['VM_active'],0);self.assertFalse(p['task_exit_complete'])
 def test_original19_cannot_be_removed(self):self.stage(('commands',),self.rows[0]['terminal_script_exit']['commands'][:-1],v.source)
 def test_captured_cycle_cannot_be_reused_label(self):self.stage(('bindings',0,'cycle'),'last_dialogue_confirmation',v.protocol)
 def test_all_raw_device_bytes_required(self):self.stage(('bindings',0,'capture','raw_device_hex'),'00',v.protocol)
 def test_derived_keyboard_substitution_refused(self):self.stage(('bindings',0,'after_hex'),'00',v.protocol)
 def test_full_owner_continuity_required(self):self.stage(('bindings',0,'after','state','owner'),'00',v.protocol)
 def test_original_world_clock_pause_required(self):self.stage(('frames',0,'after','remaining'),-999,v.protocol)
 def test_original_queue_continuity_required(self):self.stage(('frames',0,'queue_after'),{},v.protocol)
 def test_no_skipped_frame_required(self):self.stage(('frames',3,'index'),99,v.protocol)
 def test_vm_active_cannot_be_host_stopped_early(self):
  r=self.rows[0];raw=bytearray.fromhex(r['terminal_script_exit']['frames'][3]['after']['VM']);raw[4]=0;self.stage(('frames',3,'after','VM'),raw.hex(),v.protocol)
 def test_complete_work_bytes_required(self):self.stage(('frames',3,'after','work'),'00',v.protocol)
 def test_fade_remainder_cannot_be_normalized_to_zero(self):
  r=self.rows[0];i=next(i for i,f in enumerate(r['terminal_script_exit']['frames']) if v.work_fields(f['before'])['active'] and v.work_fields(f['after'])['remaining']==0);raw=bytearray.fromhex(r['terminal_script_exit']['frames'][i]['after']['work']);struct.pack_into('<i',raw,0x2490,0);bad=self.changed(r,('terminal_script_exit','frames',i,'after','work'),raw.hex());bad=self.changed(bad,('terminal_script_exit','frames',i,'capture','state','work'),raw.hex())
  with self.assertRaises(ValueError):v.protocol(bad)
 def test_timer_cannot_finish_at_old59(self):
  r=self.rows[0];i=next(i for i,f in enumerate(r['terminal_script_exit']['frames']) if struct.unpack_from('<H',bytes.fromhex(f['before']['VM']),0x22)[0]==12 and struct.unpack_from('<H',bytes.fromhex(f['before']['VM']),0x28)[0]==59 and struct.unpack_from('<H',bytes.fromhex(f['before']['VM']),32)[0]==1);raw=bytearray.fromhex(r['terminal_script_exit']['frames'][i]['after']['VM']);struct.pack_into('<H',raw,32,0);bad=self.changed(r,('terminal_script_exit','frames',i,'after','VM'),raw.hex());bad=self.changed(bad,('terminal_script_exit','frames',i,'capture','state','VM'),raw.hex())
  with self.assertRaises(ValueError):v.protocol(bad)
 def test_original_final_phase_required(self):self.stage(('final','CPU','EIP'),0,v.protocol)
 def test_vm_stop_does_not_claim_task_exit(self):self.stage(('terminal_task_exit_executed',),True,v.protocol)
 def test_no_reward_claim(self):self.stage(('rewards_or_school_executed',),True,v.protocol)
 def test_exact_parent_preflight_required(self):self.stage(('prefix_preflight','actual'),{},v.prefix_trace)
 def test_full_parent_cpu_required(self):self.stage(('before','CPU','EAX'),0xDEADBEEF,lambda r:v.prefix(r,replay=False))
 def test_actual_gpu_capacity10_required(self):self.reject(('current_GPU_hello','max_textures'),11,v.native)
 def test_no_extra_projection_required(self):self.stage(('GPU_projection',),[],v.native)
 def test_all_actual_generations_cleanup_required(self):self.reject(('script_exit_resources_after_cleanup',),[],v.native)
 def test_final_surviving_readbacks_required(self):
  r=self.rows[0];self.stage(('readback_observers',),r['terminal_script_exit']['readback_observers']+[dict(wire_index=-1)],v.native)
 def test_no_new_gdi_call_required(self):self.stage(('calls',),[dict(name='CreateFontA')],v.native)
 def test_no_game_api_leaf_dropped(self):self.stage(('leaves',),[],v.native)
 def replay(self,row):return v.execute_with_events(v.Replay(row))
 def test_complete_new_cpu_required(self):self.stage(('segments',0,'CPU','EAX'),0xDEADBEEF,self.replay)
 def test_complete_new_trace_required(self):self.stage(('segments',0,'local_after','code_sha256'),'0'*64,self.replay)
 def test_every_frame_memory_sha_required(self):self.stage(('frames',0,'capture','memory',0,'sha256'),'0'*64,self.replay)
 def test_every_original_call_event_required(self):self.stage(('events',),[],self.replay)

if __name__=='__main__':unittest.main()
