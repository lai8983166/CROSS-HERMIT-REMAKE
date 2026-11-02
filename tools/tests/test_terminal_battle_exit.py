"""Independent prefix protocol and native evidence guard regressions."""
import copy,struct,unittest
from unittest.mock import patch
from tools import terminal_battle_exit_verification as v

class ExitGuardTests(unittest.TestCase):
 def test_current_cleanup_state_rebuilds_world_fields_instead_of_portrait_cache(self):
  e=v.e;blocks={e.CTRL+0x108B32:bytes(12),e.CTRL+0x2A2FD:bytes(4),e.CTRL+0x2E6F4:struct.pack('<i',20),e.CTRL+0x2E6F8:struct.pack('<i',0),e.terminal.UNIT:bytes(0x520),e.terminal.TARGET:bytes(0x520)}
  class RAM:
   def read(self,p,n):return blocks.get(p,bytes(n))[:n]
   mem_read=read
  ram=RAM();source=e.BattleExitMachine.__new__(e.BattleExitMachine);source.uc=ram
  old=source.task_state();fake=type('State',(),dict(read=ram.read))();fake.p=dict(before=dict(state=old))
  blocks[e.CTRL+0x108B32]=b'\x01'*12;blocks[e.CTRL+0x2A2FD]=b'\x02'*4;blocks[e.CTRL+0x2E6F4]=struct.pack('<i',7);blocks[e.CTRL+0x2E6F8]=struct.pack('<i',13);blocks[e.terminal.UNIT]=b'\xA5'*0x520;blocks[e.terminal.TARGET]=b'\x5A'*0x520
  expected=source.task_state();actual=v.current_terminal_state(fake);self.assertEqual(actual,expected)
  legacy=v.parent.Replay.state(fake);self.assertNotEqual(legacy,expected)
  self.assertEqual({k for k in expected if legacy[k]!=expected[k]},{'gates','owner_flags','remaining','elapsed','units'})
  self.assertEqual(actual['remaining'],7);self.assertEqual(actual['elapsed'],13);self.assertEqual(actual['units'][1],(b'\x5A'*0x520).hex());self.assertEqual(old['remaining'],20)
 def test_inherited_capture_failure_stays_failure_and_preserves_components(self):
  fake=type('Capture',(),dict(cpu=lambda self:{'EAX':1},state=lambda self:{'remaining':7},queue=lambda self:{'used':0}))();fake.row=dict(input=dict(name='test_case'));expected=dict(CPU={'EAX':2},state={'remaining':8},queue={'used':1})
  with patch.object(v.parent.Replay,'capture',side_effect=ValueError('original check failed')) as original,patch.object(v.e.terminal,'save') as saved,patch('builtins.print'),self.assertRaisesRegex(ValueError,'original check failed'):v.current_terminal_capture(fake,expected)
  original.assert_called_once_with(fake,expected);report=saved.call_args.args[1];self.assertFalse(report['acceptance']);self.assertEqual(report['actual_state'],{'remaining':7});self.assertEqual(report['expected_state'],{'remaining':8})
 def test_segment_failure_preserves_CPU_and_digest_differences(self):
  replay=type('CPU',(),dict(cpu=lambda self:dict(EAX=1,EIP=2)))();segment=dict(label='common_register',CPU=dict(EAX=1,EIP=2),local_after=dict(instructions=10,writes=5,code_sha256='a',write_sha256='b'));actual=dict(segment['local_after'],instructions=9)
  with patch.object(v.e.terminal,'save') as saved,patch('builtins.print'),self.assertRaises(ValueError):v.check_segment_result(replay,segment,actual,'test_case')
  report=saved.call_args.args[1];self.assertEqual(report['CPU_differences'],{});self.assertEqual(report['actual_trace']['instructions'],9);self.assertEqual(report['expected_trace']['instructions'],10);self.assertFalse(report['acceptance'])
 def test_first_forward_write_difference_is_not_deferred(self):
  original=dict(pc=0x4043A1,address=0x20020000,bytes=2,value=15);v.check_forward_write([original],0,dict(original))
  with self.assertRaisesRegex(ValueError,'index'):v.check_forward_write([original],0,dict(original,value=14))
  with self.assertRaises(ValueError):v.check_forward_write([original],1,dict(original))
 def test_real_parent_optional_witness_lookup_survives_rebinding(self):
  # Exercise the real parent entry and its default before any expensive machine
  # construction. The lost-default bug raises TypeError instead of reaching it.
  lookup=unittest.mock.Mock(side_effect=RuntimeError('accepted witness lookup reached'))
  bound=v.bind_original(v.parent.verify_case,dict(vars(v.parent),accepted_case_witness=lookup))
  with self.assertRaisesRegex(RuntimeError,'accepted witness lookup reached'):bound(dict(input=dict(name='neutral_running')))
  lookup.assert_called_once_with();self.assertIs(bound.__code__,v.parent.verify_case.__code__)
 def test_original_keyword_defaults_and_closure_survive_rebinding(self):
  closed=7
  def original(value=3,*,scale=2):return (value+closed)*scale
  bound=v.bind_original(original,dict(original.__globals__))
  self.assertEqual(bound(),20);self.assertEqual(bound(1,scale=4),32)
 def projection_row(self):
  domain='overlay-battle-exit-common-0';native=list(range(100,107));guests=[0x20000000+(i+1)*4096 for i in range(6)]+[0x20020000]
  ledger=[dict(domain=domain,native=a,guest=b) for a,b in zip(native,guests)]
  create=dict(pointer=100,vtable=101,methods={'8':102,'56':103,'64':104,'68':105})
  leaf=dict(kind='GPU',call=dict(index=0,op='lock',native_result=dict(bits=106)))
  resource=dict(source=dict(index=0),projection_domain=domain,create_wire_index=0,lock=dict(hex='00'*128))
  before=dict(next=0x49601000,ledger=[])
  return dict(typed_GPU_projection=ledger,GPU_trace=[dict(reply=dict(result=dict(texture=create)))],terminal_battle_exit_prefix=dict(common_projection_before=before,common_projection_after=dict(next=before['next'],ledger=ledger),common_resources=[resource],leaves=[leaf],before=dict(memory=[])))
 def test_deterministic_resource_projection_and_parent_cursor(self):
  out=v.projection(self.projection_row());self.assertEqual(out['overlay-battle-exit-common-0'][106],0x20020000)
 def test_native_lifetime_domain_must_follow_original_index(self):
  row=self.projection_row();row['terminal_battle_exit_prefix']['common_resources'][0]['projection_domain']='overlay'
  with self.assertRaises(ValueError):v.projection(row)
 def test_projection_cannot_move_parent_allocation_cursor(self):
  row=self.projection_row();row['terminal_battle_exit_prefix']['common_projection_after']['next']+=4096
  with self.assertRaises(ValueError):v.projection(row)
 def test_projection_cannot_overlap_any_original_region(self):
  row=self.projection_row();row['terminal_battle_exit_prefix']['before']['memory']=[dict(pointer=0x20020000,bytes=4096)]
  with self.assertRaises(ValueError):v.projection(row)
 def test_projection_cannot_add_unclassified_native_identity(self):
  row=self.projection_row();extra=dict(domain='overlay-battle-exit-common-1',native=999,guest=0x20100000);row['typed_GPU_projection'].append(extra)
  with self.assertRaises(ValueError):v.projection(row)
 def indexed_row(self):
  def wire(i):return dict(request=dict(id=i+1,op='test',opaque=50+i),reply=dict(id=i+1,ok=True,result=dict(opaque=80+i)))
  d=dict(prefix=dict(CRT_wire=1,GPU_wire=1,extra_counts={'old':4}),leaves=[dict(kind='CRT',call=dict(wire_start=1,wire_end=2)),dict(kind='GPU',call=dict(wire_index=1))],cleanup=dict(leaves=[]),common_resources=[dict(readback_wire_index=2)],common_projection_before=dict(ledger=[]),before=dict(memory=[],CPU={},trace=dict(instructions=10,writes=5,code_sha256='a',write_sha256='b')),parent_entries={'old':1})
  return dict(terminal_battle_exit_prefix=d,CRT_trace=[wire(i) for i in range(3)],GPU_trace=[wire(i) for i in range(4)],CRT_APIs=[dict(wire_start=i,wire_end=i+1) for i in range(3)],final_state=dict(terminal_state={}),old_resource=dict(create_wire_index=0,release_wire_index=3),typed_GPU_projection=[])
 def test_parent_protocol_view_uses_current_payloads_and_exact_index_map(self):
  row=self.indexed_row();frozen=copy.deepcopy(row)
  with patch.object(v,'compact_terminal',return_value={'verified':'parent boundary'}):view,audit=v.parent_view(row)
  self.assertEqual(row,frozen);self.assertEqual(view['old_resource']['release_wire_index'],1)
  self.assertEqual([r['request']['id'] for r in view['GPU_trace']],[1,2]);self.assertEqual(view['GPU_trace'][-1]['reply']['result'],row['GPU_trace'][-1]['reply']['result'])
  self.assertFalse(audit['historical_cleanup_CPU_or_SHA_projection'])
 def test_old_reference_cannot_point_into_removed_common_interval(self):
  row=self.indexed_row();row['old_resource']['release_wire_index']=1
  with patch.object(v,'compact_terminal',return_value={}),self.assertRaises(ValueError):v.parent_view(row)
 def test_parent_checker_adapts_only_two_real_helper_capacity_assertions(self):
  fn,audit=v.adapted_parent_native();self.assertEqual(audit['declared_assertion_changes'],['max_creates','max_textures']);self.assertFalse(audit['parent_machine_algorithm_changed'])
 def test_actual_protocol_replaces_cached_cleanup_views_without_machine_state_changes(self):
  class Cache:pass
  obj=Cache();obj.d={'leaves':[{'call':{'wire_start':1}}]};obj.crt_case={};obj.wire=9;obj.history=[];obj.objects={};obj.u=object()
  original=(obj.history,obj.objects,obj.u);resource=dict(generation=3,label='old',release_wire_index=45);d=dict(leaves=[dict(call=dict(wire_start=100))],resources=[resource]);row=dict(terminal_task_completion=d,CRT_trace=[{'actual':'wire'}],current_CRT_hello={'actual':'owner'})
  v.attach_current_protocol(obj,row);self.assertIs(obj.d,d);self.assertIs(obj.by_gen[3],resource);self.assertIs(obj.by_label['old'],resource);self.assertEqual(obj.d['leaves'][0]['call']['wire_start'],100)
  self.assertEqual(obj.wire,9);self.assertTrue(all(a is b for a,b in zip(original,(obj.history,obj.objects,obj.u))))
 def test_new_parent_proof_does_not_repeat_legacy_task_count_unqualified(self):
  proof=dict(forward_summary=dict(complete_tasks=762));account=dict(accepted_task_completion=762,complete_tasks=1111)
  with patch.object(v.contract,'parent_task_accounting',return_value=account):v.corrected_parent_summary(proof,{})
  self.assertEqual(proof['forward_summary']['complete_tasks'],1111);self.assertEqual(proof['forward_summary']['legacy_reported_complete_tasks'],762)
 def test_unproven_parent_count_correction_rejected(self):
  with patch.object(v.contract,'parent_task_accounting',return_value=dict(accepted_task_completion=762,complete_tasks=1112)),self.assertRaises(ValueError):v.corrected_parent_summary(dict(forward_summary=dict(complete_tasks=762)),{})
 def test_common_catalog_is_complete_original_asset(self):
  raw,rows=v.catalog();self.assertEqual(len(raw),1793036);self.assertEqual(len(rows),580);self.assertEqual(sum(x['kind']=='indexed_bmp' for x in rows),461)
 def test_original_call_ABI_source_contract_is_exact(self):self.assertEqual(v.EXPECTED_ABI,v.e.EVENT_ABI)

class RetainedCaseIndexTests(unittest.TestCase):
 def test_exact_hash_and_only_forward_namespace_write_PC_union(self):
  import hashlib,json,tempfile
  from pathlib import Path
  from tools import terminal_battle_exit_resume as r
  row=dict(input=r.e.overlay.parent.corpus()[0],older=dict(writes=[dict(pc=999,address=0)]),terminal_battle_exit_prefix=dict(before=dict(trace=dict(writes=1)),writes=[dict(pc=123,address=1,bytes=4,value=0),dict(pc=456,address=2,bytes=4,value=0)],cleanup=dict(writes=[dict(pc=888,address=3)])),later=dict(pc=777))
  with tempfile.TemporaryDirectory(prefix='case-index-test-',dir=r.ROOT/'.venv-audit') as directory:
   path=Path(directory)/'case-0.json';raw=json.dumps(row,separators=(',',':')).encode();path.write_bytes(raw)
   for block in (17,31,1024):
    with self.subTest(block=block):
     identity,pcs,case=r.scan_case(path,block);self.assertEqual(pcs,{123,456});self.assertEqual(identity['sha256'],hashlib.sha256(raw).hexdigest());self.assertEqual(identity['bytes'],len(raw));self.assertEqual(case,row['input'])
 def test_incomplete_retained_case_is_rejected(self):
  import tempfile
  from pathlib import Path
  from tools import terminal_battle_exit_resume as r
  with tempfile.TemporaryDirectory(prefix='case-index-test-',dir=r.ROOT/'.venv-audit') as directory:
   path=Path(directory)/'case-0.json';path.write_bytes(b'{"input":{"name":"neutral_running"},"terminal_battle_exit_prefix":{"writes":[{"pc":123,')
   with self.assertRaises(ValueError):r.scan_case(path,17)

class CorpusAssemblyTests(unittest.TestCase):
 def test_ordinary_complete_run_needs_no_resume_metadata(self):
  self.assertEqual(v.corpus_provenance({}),dict(kind='whole_native_corpus_run'))
 def test_partial_resume_metadata_is_rejected(self):
  with self.assertRaises(ValueError):v.corpus_provenance(dict(resume_inputs={}))
 def test_restored_guest_or_native_state_is_rejected(self):
  with self.assertRaises(ValueError):v.corpus_provenance(dict(case_provenance=[],guest_or_native_state_restored=True))
 def test_helper_comparison_keeps_actual_machine_code_bytes(self):
  from tools import terminal_battle_exit_resume as r
  path=r.ROOT/'.venv-audit/terminal-battle-exit-gpu.exe'
  if not path.exists():self.skipTest('local helper not built')
  original=path.read_bytes();modified=bytearray(original);modified[0x300]^=1
  self.assertNotEqual(r.normalized_managed_image(original),r.normalized_managed_image(modified))

class MarkerSchemaTests(unittest.TestCase):
 def item(self):
  return dict(kind='COMMON_STRING',call=dict(name='lstrlenA',entry=0x770206E0,import_slot=0x5922C4,caller=0x41F416,return_va=0x41F416,args=[0x594734],pop=4,value=13,result=13,string_hex=b'Dm-No-MakeTex'.hex(),actual_API_executed=True,memory_outputs=[],new_mappings=[]))
 def test_marker_uses_actual_entry_field_without_fabricated_target(self):
  item=self.item();self.assertNotIn('target',item['call']);self.assertEqual(v.leaf_entry(item),0x770206E0)
 def test_full_marker_schema(self):
  row=dict(terminal_battle_exit_prefix=dict(leaves=[self.item() for _ in range(119)]));self.assertEqual(v.common_strings(row)['actual_marker_string_calls'],119)
 def test_marker_cannot_be_misclassified_as_owned_task_text(self):
  rows=[self.item() for _ in range(119)];rows[0]['call']['caller']=0x425A7E
  with self.assertRaises(ValueError):v.common_strings(dict(terminal_battle_exit_prefix=dict(leaves=rows)))

class PendingResourceProtocolTests(unittest.TestCase):
 def fixture(self):
  e=v.e;sp=e.STACK+0xE000;bp=e.STACK+0xF000-4;stack=bytearray(0x20000)
  for p,n in ((sp,0),(sp+4,11),(bp-8,1),(bp+4,e.RETURN)):struct.pack_into('<I',stack,p-e.STACK,n)
  memory=[dict(pointer=e.STACK,bytes=len(stack),hex=stack.hex()),dict(pointer=e.MAIN+0x844,bytes=8,hex=bytes(8).hex()),dict(pointer=e.CTRL+0xDE4B0+0x4C,bytes=4,hex=struct.pack('<I',e.MAIN).hex())]
  cpu=dict(EIP=0x40B2EC,ECX=e.CTRL+0xDE4B0,ESP=sp,EBP=sp+128);trace=dict(instructions=0,writes=0,code_sha256='x',write_sha256='y');local=v.parent.mark_zero()
  cap=dict(memory=memory,CPU=cpu,trace=trace,local_trace=local,queue={});before=copy.deepcopy(cap)
  labels=[('common_read',0x42AE20),('common_register',0x416790),('common_file_free',0x428AD0),('original_scene_packet_constructor',0x4075E0),('original_scene_packet_owner_binding',0x4077C0)]
  labels += [('original_controller_packet_constructor_'+hex(o),0x4075E0) for o in (0xDE4B0,0xDE530,0xDE5B0,0xDE630,0xDE6B0,0xDE730)]
  labels += [('original_controller_packet_owner_'+hex(o),0x4077C0) for o in (0xDE4B0,0xDE530,0xDE5B0,0xDE630,0xDE6B0,0xDE730)]
  labels += [('heads',0x40DB90),('arena',0x40DC80),('input',0x425DE0),('original_scene_loop',0x4539B0)]
  segs=[dict(label=label,entry=entry,stop=e.RETURN,root=dict(receiver=e.TASK,args=[]),before_CPU=cpu,CPU=cpu,local_before=local,local_after=local,trace_before=trace,trace_after=trace) for label,entry in labels];segs[-1]['stop']=0x40B2EC
  file=0x30000000;inputs=[(0,[0x59A438],True),(e.MAIN,[file,90],False),(0,[file],True),(e.TASK+0x68,[],False),(e.TASK+0x68,[e.MAIN],False)]
  inputs += [(e.CTRL+o,[],False) for o in (0xDE4B0,0xDE530,0xDE5B0,0xDE630,0xDE6B0,0xDE730)]
  inputs += [(e.CTRL+o,[e.MAIN],False) for o in (0xDE4B0,0xDE530,0xDE5B0,0xDE630,0xDE6B0,0xDE730)]
  inputs += [(e.MANAGER,[],False),(e.MANAGER,[],False),(e.INPUT,[],False),(e.TASK,[],False)]
  for seg,(receiver,args,cdecl) in zip(segs,inputs):seg['root']=dict(receiver=receiver,args=args,cdecl=cdecl)
  f=dict(kind='unavailable_unit_graphics',unit_graphics_lookup_reached=True,entry=0x40B2EC,first_instruction_executed=False,call_site=0x40B2EC,call_target=0x407870,call_instruction_executed=False,return_address=0x40B2F1,receiver=e.CTRL+0xDE4B0,local_result=1,args=[0,11],frame_EBP=cpu['EBP'],outer_frame_EBP=bp,root_return_address=e.RETURN,resource_owner=e.MAIN,resource_slot=e.MAIN+0x844,resource_slot_hex=bytes(8).hex(),original_wait_reached=False,stack_pointer=e.STACK,stack_bytes=len(stack),stack_hex=stack.hex())
  d=dict(common_file=dict(pointer=file),before=before,final=cap,freeze=f,segments=segs,events=[dict(entry=0x454CF0,after_CPU={},phase='prefix')],complete_tasks=1112)
  d.update({k:False for k in ('terminal_battle_exit_executed','outer_result_consumed','rewards_or_school_executed','original_outer_thread_restored','terminal_presentation_complete')})
  return dict(input=dict(name='neutral_running'),terminal_battle_exit_prefix=d,terminal_battle_stage_handoff=dict(final=copy.deepcopy(before)))
 def check(self,row):
  count=1111 if row['input']['name']=='neutral_running' else 1138
  with patch.object(v.contract,'parent_task_accounting',return_value=dict(complete_tasks=count)),patch.object(v.contract,'strict_parent_text',return_value={}):return v.protocol(row)
 def MP_fixture(self):
  row=self.fixture();row['input']['name']='timeout_before_combat';d=row['terminal_battle_exit_prefix'];e=v.e;bp=e.STACK+0xE080;stack=bytearray.fromhex(d['final']['memory'][0]['hex']);unit=e.terminal.TARGET;record=e.terminal.RECORD+0x100;args=[unit,3,7,1]
  for at,value in [(bp-4,e.CTRL),(bp+4,0x46CF71)]+[(bp+8+j*4,n) for j,n in enumerate(args)]:struct.pack_into('<I',stack,at-e.STACK,value)
  memory=d['final']['memory'];memory[0]['hex']=stack.hex();obj=bytearray(0x520);struct.pack_into('<I',obj,0x258,record);record_bytes=bytes(0xB0);memory += [dict(pointer=unit,bytes=len(obj),hex=obj.hex()),dict(pointer=record,bytes=len(record_bytes),hex=record_bytes.hex())]
  cpu=dict(EIP=0x46D3F4,ECX=0,EAX=0,EDX=0,EBP=bp,ESP=bp-0x5C);d['final']['CPU']=cpu;d['before']['CPU']=cpu;row['terminal_battle_stage_handoff']['final']['CPU']=cpu
  for seg in d['segments']:seg['CPU']=seg['before_CPU']=cpu
  d['segments'][-1]['stop']=0x46D3F4;d['complete_tasks']=1139
  f=d['freeze'];keep=('outer_frame_EBP','local_result','root_return_address','original_wait_reached','stack_pointer','stack_bytes');d['freeze']={k:f[k] for k in keep};d['freeze'].update(kind='zero_MP_HUD_input',entry=0x46D3F4,first_instruction_executed=False,frame_EBP=bp,stack_hex=stack.hex(),idiv_instruction_executed=False,unit_graphics_lookup_reached=False,receiver=e.CTRL,HUD_args=args,frame_return_address=0x46CF71,unit=unit,stats_record=record,stats_record_hex=record_bytes.hex(),maximum_MP_pointer=record+0x1A,maximum_MP=0,current_MP=0,numerator=0,denominator=0)
  return row
 def test_consistent_zero_MP_original_frontier(self):self.assertEqual(self.check(self.MP_fixture())['frontend_frontier']['entry'],0x46D3F4)
 def test_zero_MP_instruction_cannot_be_claimed_executed(self):
  row=self.MP_fixture();row['terminal_battle_exit_prefix']['freeze']['idiv_instruction_executed']=True
  with self.assertRaises(ValueError):self.check(row)
 def test_zero_MP_operand_must_be_actual_owned_word(self):
  row=self.MP_fixture();row['terminal_battle_exit_prefix']['freeze']['maximum_MP']=1
  with self.assertRaises(ValueError):self.check(row)
 def test_zero_MP_frontier_cannot_claim_unit_query(self):
  row=self.MP_fixture();row['terminal_battle_exit_prefix']['freeze']['unit_graphics_lookup_reached']=True
  with self.assertRaises(ValueError):self.check(row)
 def test_zero_MP_frontier_cannot_carry_fabricated_CALL_metadata(self):
  row=self.MP_fixture();row['terminal_battle_exit_prefix']['freeze']['call_target']=0x407870
  with self.assertRaises(ValueError):self.check(row)
 def test_consistent_pending_call_fixture(self):self.assertEqual(self.check(self.fixture())['roots'],21)
 def reject(self,mutator):
  row=self.fixture();mutator(row['terminal_battle_exit_prefix'])
  with self.assertRaises(ValueError):self.check(row)
 def test_pending_CALL_cannot_be_claimed_executed(self):self.reject(lambda d:d['freeze'].update(call_instruction_executed=True))
 def test_wait_cannot_be_claimed_reached(self):self.reject(lambda d:d['freeze'].update(original_wait_reached=True))
 def test_arguments_must_be_actual_stack_bytes(self):self.reject(lambda d:d['freeze'].update(args=[0,12]))
 def test_result_must_be_real_outer_frame(self):self.reject(lambda d:d['freeze'].update(outer_frame_EBP=d['freeze']['frame_EBP']))
 def test_original_root_cannot_be_removed(self):self.reject(lambda d:d['segments'].pop(5))
 def test_packet_constructor_receiver_cannot_shift(self):self.reject(lambda d:d['segments'][5]['root'].update(receiver=v.e.CTRL+0xDE530))
 def test_COMMON_group_cannot_be_swapped(self):self.reject(lambda d:d['segments'][1]['root'].update(args=[0x30000000,0]))
 def test_binding_cannot_use_a_foreign_owner(self):self.reject(lambda d:d['segments'][11]['root'].update(args=[v.e.MAIN+4]))
 def test_complete_task_count_cannot_omit_new_root(self):self.reject(lambda d:d.update(complete_tasks=1111))
 def test_resource_slot_cannot_be_fabricated(self):self.reject(lambda d:d['freeze'].update(resource_slot_hex='01'+bytes(7).hex()))
 def test_scope_cannot_claim_exit(self):self.reject(lambda d:d.update(terminal_battle_exit_executed=True))
 def test_capture_state_matches_all_source_fields(self):
  fake=type('RAM',(),dict(read=lambda self,p,n:bytes(n)))()
  expected={'task_hex','VM_PC','VM_wait','VM_active','selector','result_type','packet_owner','time_packet_hex','group90'}
  self.assertEqual(set(v.state(fake)),expected)
 def test_original_CRT_algorithm_accepts_only_explicit_new_inputs(self):
  obj=type('ReplayInputs',(),dict(history=[dict(bytes=n) for n in (32816,65584,128)]))()
  audit=v.common_crt_algorithm(obj);self.assertFalse(audit['machine_algorithm_changed']);self.assertEqual(audit['additional_raw_allocation_sizes'],[1793072,48768])
  self.assertEqual(audit['input_adaptations'].count('complete_common_path'),2)
 def test_cleanup_binds_current_verified_boundary_without_mutating_parent(self):
  fn,audit=v.current_cleanup_driver();self.assertEqual(audit['declared_boundary_changes'],1);self.assertFalse(audit['historical_cleanup_projection'])
  self.assertIn('terminal_battle_exit_prefix',fn.__code__.co_consts);self.assertIn('task_completion_cleanup',fn.__code__.co_consts)
  self.assertEqual(fn.__globals__['parent_case'],v.parent.previous_stage.cleanup_plan)
 def test_static_exact_packet_and_sorting_guard(self):self.assertEqual(v.source_guard({})['complete_new_functions'],27)

if __name__=='__main__':unittest.main()
