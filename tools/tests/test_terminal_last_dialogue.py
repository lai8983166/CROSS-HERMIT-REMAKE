"""Independent multiline source, actual native ownership and replay rejection."""
import copy,os,struct,unittest,io,json,gzip,tempfile
from pathlib import Path
from tools import terminal_last_dialogue_emulation as e
from tools import terminal_last_dialogue_verification as v

REPORT=os.environ.get('TERMINAL_LAST_DIALOGUE_REPORT','analysis/terminal-last-dialogue-source-v3-20261029.json.gz')

class TerminalLastDialogueStaticTests(unittest.TestCase):
 @staticmethod
 def fixture(name):
  raw=(e.ROOT/e.terminal.SCRIPT_PATH).read_bytes();cfg=v.branch(name);s=next(s for s in v.previous.dialogue.script_commands(raw)['segments'] if s['index']==cfg['segment']);code=raw[s['code_start']:s['code_end']];base=0xE000000;vm=bytearray(0x9400);struct.pack_into('<I',vm,16,base);pc=cfg['first_PC'];commands=[]
  while pc<cfg['final_PC']:
   op,n=struct.unpack_from('<HH',code,pc);commands.append(dict(PC=pc,opcode=op,bytes=n,source_pointer=base+pc));pc+=n
  return dict(input=dict(name=name),terminal_last_dialogue=dict(before=dict(memory=[dict(pointer=e.VM,bytes=len(vm),hex=vm.hex()),dict(pointer=base,bytes=len(code),hex=code.hex())]),commands=commands))
 def test_both_full_original_groups_and_ANSI_identities(self):
  for name,pc,indices,layers in [('neutral_running',320,[9],[4]),('timeout_before_combat',350,[10,11,12],[7,7,7])]:
   s=v.source(self.fixture(name));self.assertEqual(s['final_PC'],pc);self.assertEqual([x['index'] for x in s['texts']],indices);self.assertEqual([x['layer'] for x in s['texts']],layers)
 def test_unknown_branch_refused(self):
  with self.assertRaises(ValueError):v.branch('timeout_before_combat ')
 def test_truncated_command_refused(self):
  r=self.fixture('neutral_running');r['terminal_last_dialogue']['commands'][2]['bytes']=4
  with self.assertRaises(ValueError):v.source(r)
 def test_extra_successor_dispatch_refused(self):
  r=self.fixture('timeout_before_combat');r['terminal_last_dialogue']['commands'].append(dict(PC=312,opcode=43,bytes=8,source_pointer=0))
  with self.assertRaises(ValueError):v.source(r)
 def test_frozen_engine_instruction_algorithm(self):
  for name in ('_initialize','execute'):
   a=getattr(v.previous_stage.Replay,name).__code__;b=getattr(v.Replay,name).__code__;self.assertEqual(a.co_code,b.co_code);self.assertEqual(a.co_names,b.co_names)
  self.assertIs(v.Replay.execute.__globals__['need'],v.replay_need)
 def test_replay_routes_current_stage_and_current_cleanup(self):
  self.assertIn('terminal_last_dialogue',v.Replay._initialize.__code__.co_consts);self.assertNotIn('terminal_multiline',v.Replay._initialize.__code__.co_consts)
  self.assertIn('last_dialogue_cleanup',v.Replay.execute.__code__.co_consts);self.assertNotIn('multiline_cleanup',v.Replay.execute.__code__.co_consts)
 def test_no_new_guest_code(self):self.assertIs(e.ALLOWED,e.parent.ALLOWED);self.assertIs(e.LastDialogueMachine.source_code,e.parent.MultilineMachine.source_code)
 def test_new_domain_allows_retired_native_token_reissue(self):
  r=dict(typed_GPU_projection=[dict(domain='overlay',native=1,guest=100),dict(domain='overlay-last-dialogue-0',native=1,guest=200)]);self.assertEqual(v.gpu_mappings(r)['overlay-last-dialogue-0'][1],200)
 def test_other_guest_alias_refused(self):
  with self.assertRaises(ValueError):v.gpu_mappings(dict(typed_GPU_projection=[dict(domain='overlay',native=1,guest=100),dict(domain='overlay-last-dialogue-0',native=2,guest=100)]))
 def test_unknown_projection_refused(self):
  with self.assertRaises(ValueError):v.gpu_mappings(dict(typed_GPU_projection=[dict(domain='guessed',native=1,guest=100)]))
 def test_creation_record_and_ordinal_derived_independently(self):
  cfg=v.branch('timeout_before_combat');line=cfg['lines'][2];r=dict(line,kind='text',creation_index=2,create_wire_index=10,record=v.text_record(7,2),projection_domain='overlay-last-dialogue-2');row=dict(input=dict(name='timeout_before_combat'),terminal_last_dialogue=dict(prefix=dict(GPU_wire=10)));self.assertEqual(v.resource_domain(row,r),'overlay-last-dialogue-2');r['record_index']=1
  with self.assertRaises(ValueError):v.resource_domain(row,r)
 def test_parent_preflight_refuses_any_digest_difference(self):
  with self.assertRaises(ValueError):v.prefix_trace(dict(input=dict(name='neutral_running'),terminal_last_dialogue=dict(before=dict(trace={}))))
 def test_stream_reader_matches_standard_values_at_chunk_boundaries(self):
  value=dict(raw='ab'*9000,unicode='夏朧'*5000,escaped='quote" slash\\ tab\t newline\n astral😀',numbers=[0,-17,1.25,1e100],empty=[{},[]],flags=[True,False,None]);text=json.dumps(value,ensure_ascii=True)
  for size in (1,7,16,4096,65536):self.assertEqual(v.StreamingJSON(io.StringIO(text),size).decode(),json.loads(text))
 def test_stream_reader_handles_literal_unicode_and_shared_long_values(self):
  value=[dict(raw='00'*9000,text='夏朧'*5000),dict(raw='00'*9000,text='夏朧'*5000)];result=v.StreamingJSON(io.StringIO(json.dumps(value,ensure_ascii=False)),7).decode();self.assertEqual(result,value);self.assertIs(result[0]['raw'],result[1]['raw'])
 def test_stream_reader_rejects_truncation_and_invalid_separators(self):
  for text in ('{"a":','[1,]','{"a" 1}','{"a":1,}','"abc','"bad\\q"','true false','01','[true false]','"a\nb"'):
   with self.subTest(text=text),self.assertRaises(ValueError):v.StreamingJSON(io.StringIO(text),1).decode()
 def test_stream_reader_preserves_escaped_surrogates_and_duplicate_key_semantics(self):
  text='{"same":1,"same":2,"text":"\\ud83d\\ude00\\ud800"}';self.assertEqual(v.StreamingJSON(io.StringIO(text),1).decode(),json.loads(text))
 def test_compressed_stream_reader_matches_standard_decoder(self):
  value=dict(cases=[dict(memory='cc'*10000),dict(memory='cc'*10000)],text='夏朧')
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'report.json.gz';p.write_bytes(gzip.compress(json.dumps(value,ensure_ascii=False).encode('utf8')));self.assertEqual(v.load_report(p),value)

 def test_exact_capacity_probe_actual_receipts(self):
  d=json.loads((e.ROOT/'analysis/terminal-last-dialogue-capacity-v1-20261029.json').read_text());self.assertEqual(d['helper'],e.experimental_helper_contract());self.assertTrue(d['normal_exit']);self.assertEqual(d['exit_code'],0);self.assertEqual((d['actual_hello']['max_textures'],d['actual_hello']['max_creates']),(11,32));self.assertEqual(d['original_VM_or_game_roots'],0);trace=d['trace'];self.assertEqual(len(trace),24)
  for i,t in enumerate(trace):self.assertEqual(t['request']['id'],i+1);self.assertEqual(t['reply']['id'],i+1);self.assertEqual(t['reply']['ok'],i!=11)
  created=[t['reply']['result']['texture']['pointer'] for t in trace[:11]];self.assertEqual(len(set(created)),11);self.assertTrue(all(t['request']['op']=='create' and t['request']['width']==t['request']['height']==1 for t in trace[:12]));self.assertIn('bounded multi texture capacity',trace[11]['reply']['error']);self.assertEqual([t['request']['pointer'] for t in trace[12:23]],list(reversed(created)));self.assertTrue(all(t['request']['op']=='release' and t['reply']['result']['count']==0 for t in trace[12:23]));self.assertEqual(trace[-1]['request']['op'],'close');self.assertTrue(d['cleanup']['all_owned_resources_released']);self.assertEqual(d['cleanup']['texture_releases'],[])

class TerminalLastDialogueTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=v.load_report(e.ROOT/REPORT);cls.rows=cls.data['cases'];cls.refs={r['input']['name']:v.pixels(r)[1] for r in cls.rows}
 @staticmethod
 def changed(obj,path,value):
  if not path:return value
  out=copy.copy(obj);out[path[0]]=TerminalLastDialogueTests.changed(obj[path[0]],path[1:],value);return out
 def reject(self,path,value,check,index=0):
  with self.assertRaises((ValueError,KeyError,IndexError,StopIteration,AssertionError)):check(self.changed(self.rows[index],path,value))
 def stage(self,path,value,check,index=0):self.reject(('terminal_last_dialogue',)+tuple(path),value,check,index)
 def test_complete_original_branches(self):
  self.assertEqual(self.data['source_contract'],e.source_contract())
  for r in self.rows:v.prefix_trace(r)
  for r,pc in zip(self.rows,[320,350]):
   with self.subTest(case=r['input']['name']):self.assertEqual(v.verify_case(r)['timing']['VM_PC'],pc)
 def test_complete_chronological_GDI_lifetimes(self):
  for row in self.rows:
   report=v.gdi_native(row,v.parent_case(row));self.assertTrue(report['all_argument_and_result_lifetimes_verified']);self.assertTrue(report['all_actual_API_outputs_preserved'])
 def test_GDI_hidden_lifetime_refused(self):
  r=self.rows[0];self.reject(('last_dialogue_GDI_lifetimes','lifetimes'),r['last_dialogue_GDI_lifetimes']['lifetimes']+[dict(id=999)],lambda x:v.gdi_native(x,v.parent_case(x)))
 def test_GDI_retirement_call_refused(self):
  self.reject(('last_dialogue_GDI_lifetimes','lifetimes',1,'deleted_call'),0,lambda x:v.gdi_native(x,v.parent_case(x)))
 def test_GDI_binding_lifetime_refused(self):
  self.reject(('last_dialogue_GDI_lifetimes','calls',2,'argument_bindings',1,'lifetime'),0,lambda x:v.gdi_native(x,v.parent_case(x)))
 def test_GDI_selected_previous_owner_refused(self):
  self.reject(('terminal_name','GDI_trace',5,'native_result','result'),1,lambda x:v.gdi_native(x,v.parent_case(x)))
 def test_GDI_unobserved_API_output_refused(self):
  self.reject(('terminal_name','GDI_trace',1,'native_result','result'),999,lambda x:v.gdi_native(x,v.parent_case(x)))
 def test_GDI_owner_close_refused(self):
  self.reject(('last_dialogue_GDI_lifetimes','owner_cleanup','retired_lifetimes'),[],lambda x:v.gdi_native(x,v.parent_case(x)))
 def test_GDI_latest_slot_native_refused(self):
  self.stage(('GDI_handle_projection',0,'native'),1,lambda x:v.gdi_native(x,v.parent_case(x)))
 def test_extra_dispatch_refused(self):self.stage(('commands',0,'PC'),0,v.source)
 def test_new_cycle_required(self):self.stage(('bindings',0,'cycle'),'previous_cycle',v.protocol)
 def test_full_raw_keyboard_required(self):self.stage(('bindings',0,'capture','raw_device_hex'),'00',v.protocol)
 def test_derived_keyboard_write_refused(self):self.stage(('bindings',0,'after_hex'),'00',v.protocol)
 def test_keyboard_owner_continuity_refused(self):self.stage(('bindings',0,'after','state','owner'),'00',v.protocol)
 def test_frame_remaining_refused(self):self.stage(('frames',0,'after','remaining'),-1,v.protocol)
 def test_frame_queue_refused(self):self.stage(('frames',0,'queue_after'),{},v.protocol)
 def test_clear_may_not_release(self):self.stage(('clears',0,'GPU_wire_after'),-1,v.protocol)
 def test_second_layer_clear_required(self):self.stage(('clears',),[],v.protocol,1)
 def test_both_real_replacements_required(self):self.stage(('replacements',),[],v.protocol)
 def test_original_replacement_caller_required(self):self.stage(('replacements',0,'caller'),0,v.protocol)
 def test_old_generation_identity_required(self):self.stage(('replacements',0,'generation'),0,v.protocol)
 def test_first_actual_text_font_abi_required(self):
  index=len(self.rows[0]['terminal_last_dialogue']['resources_before']);self.stage(('resources',index,'pending_font','args',0),99,v.pixels)
 def test_first_actual_text_upload_required(self):
  index=len(self.rows[0]['terminal_last_dialogue']['resources_before']);self.stage(('resources',index,'upload_hex'),'00',v.pixels)
 def test_third_record_required(self):
  index=len(self.rows[1]['terminal_last_dialogue']['resources_before'])+2;self.stage(('resources',index,'record'),v.text_record(7,1),v.pixels,1)
 def test_cross_layer_second_record_required(self):
  index=len(self.rows[1]['terminal_last_dialogue']['resources_before'])+1;self.stage(('resources',index,'layer'),4,v.pixels,1)
 def test_full_current_generation_cleanup_required(self):self.reject(('last_dialogue_resources_after_cleanup',),[],v.native)
 def test_all_current_observers_required(self):self.stage(('readback_observers',),[],v.native)
 def test_prefix_projection_next_required(self):self.stage(('GPU_projection_before','next'),0,v.native)
 def test_new_creation_domain_required(self):
  index=len(self.rows[0]['terminal_last_dialogue']['resources_before']);self.stage(('resources',index,'projection_domain'),'overlay',v.native)
 def test_declared_new_guest_identity_required(self):self.stage(('GPU_projection',0,'guest'),0,v.native)
 def test_source_preflight_metadata_required(self):self.stage(('prefix_preflight','actual'),{},v.prefix_trace)
 def test_frozen_parent_CPU_required(self):self.stage(('before','CPU','EAX'),0xDEADBEEF,lambda r:v.prefix(r,replay=False))
 def replay(self,row):return v.Replay(row,self.refs[row['input']['name']]).execute()
 def test_replay_full_CPU_required(self):self.stage(('segments',0,'CPU','EAX'),0xDEADBEEF,self.replay)
 def test_replay_digest_required(self):self.stage(('segments',0,'local_after','code_sha256'),'0'*64,self.replay)
 def test_replay_full_region_hash_required(self):self.stage(('frames',0,'capture','memory',0,'sha256'),'0'*64,self.replay)

 def test_actual_new_namespace_declaration_required(self):self.stage(('GPU_namespace','new_start'),0x64001000,v.native)
 def test_actual_parent_namespace_boundary_required(self):self.stage(('GPU_namespace','prefix_next'),0,v.native)
 def test_actual_current_capacity10_required(self):self.reject(('current_GPU_hello','max_textures'),11,v.native)

if __name__=='__main__':unittest.main()
