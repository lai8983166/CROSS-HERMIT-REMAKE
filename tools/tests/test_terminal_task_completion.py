"""Original resource-group order, no-input handshake, full replay rejections."""
import copy,struct,os,unittest
from unittest.mock import patch
from tools import terminal_task_completion_emulation as e
from tools import terminal_task_completion_verification as v
REPORT=os.environ.get('TERMINAL_TASK_COMPLETION_REPORT','analysis/terminal-task-completion-source-v4-20261030.json.gz')

class TaskCompletionStaticTests(unittest.TestCase):
 def test_exact_original_group_loop_and_handshake_instructions(self):
  r=v.source({});self.assertEqual(len(r['groups']),78);self.assertNotIn(20,r['groups']);self.assertEqual(r['groups'][0],10);self.assertEqual(r['groups'][-1],88)
 def test_only_original_completion_flag_write_permission_added(self):
  self.assertEqual(e.NEW_MUTABLE,((e.TASK+0x171,e.TASK+0x173),))
  with patch.object(e,'NEW_MUTABLE',((e.TASK,e.TASK+0x190),)):
   with self.assertRaises(ValueError):v.source({})
 def test_exact_original_observer_abi(self):self.assertEqual(e.EVENTS,v.EVENT_ABI);self.assertEqual(v.EVENT_ABI[0x56DE40],(4,16))
 def test_guard_extension_cannot_be_widened(self):
  with patch.object(e,'EXTRA_RANGES',e.EXTRA_RANGES+((0x400000,0x592000),)):
   with self.assertRaises(ValueError):v.source({})
 def test_complete_resource_group_list_required(self):
  with patch.object(e,'GROUPS',tuple(range(10,89))):
   with self.assertRaises(ValueError):v.source({})
 def test_initialization_and_cleanup_machine_algorithms_preserved(self):
  for n in ('_initialize','cleanup'):
   a=getattr(v.Replay,n).__code__;b=getattr(v.previous_stage.Replay,n).__code__;self.assertEqual(a.co_code,b.co_code);self.assertEqual(a.co_names,b.co_names)
 def test_only_declared_contract_observations_change(self):
  a=v.Replay.execute.__globals__['OBSERVER_SCHEMA_AUDIT'];self.assertEqual(a['declared_changes'],dict(queries=1,commands=1,write_observer=1,input_partition=1));self.assertTrue(a['zero_new_input_bindings']);self.assertFalse(a['original_machine_events_filtered'])
 def test_current_stage_creation_selector(self):
  row=dict(terminal_task_completion=dict(prefix=dict(GPU_wire=9),resources=[dict(create_wire_index=1),dict(create_wire_index=9)]));self.assertEqual(v.new_resources(row),[dict(create_wire_index=9)]);self.assertIs(v.Replay.execute.__globals__['new_resources'],v.new_resources)
 def test_complete_table_added_to_query_payload(self):
  class Fake:
   def read(self,p,n):return bytes(n)
  f=Fake();q=v.capture_query(f,0x41F4E0,dict(ESP=0,ECX=e.MAIN+0x844));self.assertEqual(len(bytes.fromhex(q['state']['resource_table_hex'])),0x800);self.assertEqual(len(bytes.fromhex(q['state']['task_full_hex'])),0x190)
 def test_no_input_contract_checked_before_replay(self):
  for frames,bindings in (([],[]),([{},{}],[{}])):
   with self.assertRaises(ValueError):v.Replay(dict(terminal_task_completion=dict(frames=frames,bindings=bindings)))
 def test_cleanup_plan_requires_proven_empty_original_group(self):
  plan=[dict(label='group30',entry=0x41F4E0,args=[30],receiver=e.MAIN+0x844,cdecl=False)]
  row=dict(terminal_task_completion=dict(final=dict(memory=[dict(pointer=e.MAIN+0x844,bytes=0x800,hex=bytes(0x800).hex())])),task_completion_cleanup=[],task_completion_cleanup_skips=[])
  with patch.object(v,'parent_case',return_value=dict(cleanup_steps=plan)):
   with self.assertRaises(ValueError):v.cleanup_plan(row)
   row['task_completion_cleanup_skips']=[dict(plan[0],slot=e.MAIN+0x844+30*8,slot_hex=bytes(8).hex(),record_pointer=0,reason='original forward resource loop already cleared this container')];self.assertEqual(v.cleanup_plan(row),dict(cleanup_steps=[]))
 def test_group20_cannot_be_skipped_in_cleanup(self):
  plan=[dict(label='group20',entry=0x41F4E0,args=[20],receiver=e.MAIN+0x844,cdecl=False)]
  row=dict(terminal_task_completion=dict(final=dict(memory=[dict(pointer=e.MAIN+0x844,bytes=0x800,hex=bytes(0x800).hex())])),task_completion_cleanup=[],task_completion_cleanup_skips=[])
  with patch.object(v,'parent_case',return_value=dict(cleanup_steps=plan)):
   with self.assertRaises(ValueError):v.cleanup_plan(row)
 def test_full_named_capture_requires_each_compact_region_sha(self):
  full=dict(CPU={'EAX':1},state={},queue={},trace={},local_trace={},memory=[dict(pointer=4096,bytes=2,hex='0102')]);compact=dict(full,memory=[dict(pointer=4096,bytes=2,sha256=v.sha(bytes((1,2))))]);self.assertTrue(v.capture_boundary(full,compact));compact['memory'][0]['sha256']='0'*64
  with self.assertRaises(ValueError):v.capture_boundary(full,compact)
 def test_current_stage_allocation_cursor_is_parent_cursor(self):self.assertEqual(v.e.helper_contract(),v.previous_stage.e.helper_contract())

class TaskCompletionTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.data=v.load_report(e.ROOT/REPORT);cls.rows=cls.data['cases']
 @staticmethod
 def changed(obj,path,value):
  if not path:return value
  out=copy.copy(obj);out[path[0]]=TaskCompletionTests.changed(obj[path[0]],path[1:],value);return out
 def reject(self,path,value,check,index=0):
  with self.assertRaises((ValueError,KeyError,IndexError,StopIteration,AssertionError)):check(self.changed(self.rows[index],path,value))
 def stage(self,path,value,check,index=0):self.reject(('terminal_task_completion',)+tuple(path),value,check,index)
 def test_both_complete_original_task_handshakes(self):
  self.assertEqual(self.data['source_contract'],e.source_contract())
  for row in self.rows:
   with self.subTest(case=row['input']['name']):p=v.verify_case(row);self.assertEqual(p['timing']['task_phase'],6);self.assertEqual(p['timing']['completion_flags'],[1,1]);self.assertFalse(p['terminal_battle_exit_executed'])
 def test_no_extra_frame_allowed(self):self.stage(('frames',),self.rows[0]['terminal_task_completion']['frames']+[{}],v.protocol)
 def test_no_new_input_binding_allowed(self):self.stage(('bindings',),[{}],v.protocol)
 def test_no_new_vm_dispatch_allowed(self):self.stage(('commands',),[dict(opcode=19)],v.protocol)
 def test_queue_continuity_required(self):self.stage(('frames',0,'queue_before'),{},v.protocol)
 def test_complete_task_bytes_required(self):self.stage(('frames',1,'after','task'),'00',v.protocol)
 def test_phase4_capture_is_complete_frame(self):self.stage(('phase4','CPU','EAX'),999,v.protocol)
 def test_no_host_final_task_return(self):self.stage(('frames',1,'capture','CPU','EAX'),0,v.protocol)
 def test_no_early_vm_restart(self):self.stage(('frames',0,'after','VM'),'00',v.protocol)
 def test_original_world_pause_required(self):self.stage(('frames',0,'after','remaining'),-999,v.protocol)
 def test_every_original_resource_group_required(self):
  events=[r for r in self.rows[0]['terminal_task_completion']['events'] if not(r['entry']==0x41F4E0 and r['args']==[88])];self.stage(('events',),events,v.protocol)
 def test_each_original_resource_record_destructor_required(self):
  row=self.rows[0];events=copy.deepcopy(row['terminal_task_completion']['events']);r=next(r for r in events if r['entry']==0x403730 and r['caller']==0x41F54D);r['receiver']+=0x54;self.stage(('events',),events,v.protocol)
 def test_group20_must_remain_unchanged(self):
  row=self.rows[0];events=copy.deepcopy(row['terminal_task_completion']['events']);r=next(r for r in events if r['entry']==0x41F4E0);r['after']['resource_table_hex']='00';self.stage(('events',),events,v.protocol)
 def test_battle_exit_cannot_be_claimed(self):self.stage(('terminal_battle_exit_executed',),True,v.protocol)
 def test_rewards_cannot_be_claimed(self):self.stage(('rewards_or_school_executed',),True,v.protocol)
 def test_parent_cumulative_digest_required(self):self.stage(('prefix_preflight','actual'),{},v.prefix_trace)
 def test_parent_full_cpu_required(self):self.stage(('before','CPU','EAX'),0xDEADBEEF,lambda r:v.prefix(r,replay=False))
 def test_native_capacity_unchanged(self):self.reject(('current_GPU_hello','max_textures'),11,v.native)
 def test_all_native_generations_required(self):self.reject(('task_completion_resources_after_cleanup',),[],v.native)
 def test_no_new_gdi_call(self):self.stage(('calls',),[dict(name='CreateFontA')],v.native)
 def test_every_native_leaf_required(self):self.stage(('leaves',),[],v.native)
 def test_cleanup_skip_cannot_be_added(self):self.reject(('task_completion_cleanup_skips',),self.rows[0]['task_completion_cleanup_skips']+[{}],v.cleanup_plan)
 def test_cleanup_root_cannot_be_removed(self):self.reject(('task_completion_cleanup',),[],v.cleanup_plan)
 def replay(self,row):return v.execute_with_events(v.Replay(row))
 def test_full_new_cpu_required(self):self.stage(('segments',0,'CPU','EAX'),0xDEADBEEF,self.replay)
 def test_full_new_trace_required(self):self.stage(('segments',0,'local_after','code_sha256'),'0'*64,self.replay)
 def test_full_frame_memory_sha_required(self):self.stage(('frames',0,'capture','memory',0,'sha256'),'0'*64,self.replay)
 def test_complete_final_terminal_summary_required(self):self.reject(('final_state','terminal_state'),{},v.final_summary)
 def test_all_original_call_events_required(self):self.stage(('events',),[],self.replay)

if __name__=='__main__':unittest.main()
