"""Original follow-up, real current resource generations and teardown guards."""
import copy,gzip,json,os,struct,unittest
from types import SimpleNamespace
from unittest.mock import patch
from tools import terminal_followup_emulation as e
from tools import terminal_followup_verification as v

REPORT=os.environ.get('TERMINAL_FOLLOWUP_REPORT','analysis/terminal-followup-source-v1-20261027.json.gz')

class TerminalFollowupStaticTests(unittest.TestCase):
 @staticmethod
 def declared_script_fixture(name):
  # Explicit static function input, never a claimed guest execution/capture.
  raw=(e.ROOT/e.terminal.SCRIPT_PATH).read_bytes();cfg=v.branch(name);segment=next(s for s in v.previous.dialogue.script_commands(raw)['segments'] if s['index']==cfg['segment']);code=raw[segment['code_start']:segment['code_end']];base=0xE000000;vm=bytearray(0x9400);struct.pack_into('<I',vm,16,base);pc=cfg['first_PC'];commands=[]
  while pc<cfg['final_PC']:
   op,n=struct.unpack_from('<HH',code,pc);commands.append(dict(PC=pc,opcode=op,bytes=n,source_pointer=base+pc));pc+=n
  return dict(input=dict(name=name),terminal_followup=dict(before=dict(memory=[dict(pointer=e.VM,bytes=len(vm),hex=vm.hex()),dict(pointer=base,bytes=len(code),hex=code.hex())]),commands=commands))
 def test_original_next_scripts_and_complete44_disassembly(self):
  for name in ('neutral_running','timeout_before_combat'):
   with self.subTest(name=name):self.assertEqual(v.source(self.declared_script_fixture(name))['final_PC'],198 if name=='neutral_running' else 194)
 def test_static_invented_dispatch_rejected(self):
  fixture=self.declared_script_fixture('neutral_running');fixture['terminal_followup']['commands'][0]['bytes']=16
  with self.assertRaises(ValueError):v.source(fixture)
 def test_unknown_branch_rejected(self):
  for name in ('fake','initial','neutral_running '):
   with self.subTest(name=name),self.assertRaises(ValueError):v.branch(name)
 def test_runtime_unknown_branch_rejected(self):
  with self.assertRaises(ValueError):e.branch('fake')
 def test_configuration_index_is_distinct_from_selected_layer(self):
  self.assertEqual([(e.branch(n)['configuration'],e.branch(n)['layer']) for n in ('neutral_running','timeout_before_combat')],[(7,4),(8,5)])
 def test_exact_live_address_reuse_helper_delta(self):self.assertTrue(v.helper_contract()['duplicate_live_address_refused'])
 def test_other_helper_ownership_change_rejected(self):
  old=(e.ROOT/'tools/terminal_portrait_d3d8_platform.cs').read_bytes();new=(e.ROOT/'tools/terminal_followup_d3d8_platform.cs').read_bytes();original=type(e.ROOT).read_bytes
  def altered(path):
   if path.name=='terminal_portrait_d3d8_platform.cs':return old
   if path.name=='terminal_followup_d3d8_platform.cs':return new.replace(b'resources.Count>=10',b'resources.Count>=11')
   return original(path)
  with patch.object(type(e.ROOT),'read_bytes',altered),self.assertRaises(ValueError):v.helper_contract()
 def test_runtime_source_guard_preserves_frozen_code_object(self):self.assertIs(e.FollowupMachine.source_code.__code__,e.parent.PanelDialogueMachine.source_code.__code__)
 def test_only_finite_original44_range_added(self):
  self.assertEqual(e.EXTRA_RANGES,((0x4C4EB0,0x4C4F23),));self.assertEqual(e.ALLOWED-e.parent.ALLOWED,frozenset(range(0x4C4EB0,0x4C4F23)))
 def test_runtime_unknown_resource_kind_before_native_access(self):
  machine=e.FollowupMachine.__new__(e.FollowupMachine);machine.fu_current=None
  with self.assertRaises(ValueError):machine.fu_prepare('fake','x',0)
 def test_runtime_second_pending_resource_rejected(self):
  machine=e.FollowupMachine.__new__(e.FollowupMachine);machine.fu_current={'kind':'text'}
  with self.assertRaises(ValueError):machine.fu_prepare('text','x',0)
 def test_runtime_unknown_raster_before_native_access(self):
  machine=e.FollowupMachine.__new__(e.FollowupMachine)
  with self.assertRaises(ValueError):machine.fu_set_raster(0x12345678)
 def test_live_integer_JSON_ownership_keys_preserve_every_raw_byte(self):
  x={0x30000000:dict(hex='abcdef001122334455',native_hex='6400100001020304',bytes=9)};self.assertEqual(v.guest(x),v.guest(json.loads(json.dumps(x))));self.assertEqual(v.guest(x)['805306368']['hex'],'abcdef001122334455')
 def test_JSON_key_collisions_and_non_JSON_keys_rejected(self):
  for x in ({1:0,'1':1},{True:0},{None:0},{(1,):0}):
   with self.subTest(keys=list(x)),self.assertRaises(ValueError):v.guest(x)
 def test_declared_partial_memory_rejected(self):
  x=[dict(pointer=0,bytes=2,hex='00')]
  with self.assertRaises(ValueError):v.equal(x,x,'declared fixture')
 def test_real_initial_surface_padding_is_preserved_without_zero_assumption(self):
  before=bytes([0xA5])*64;raw=struct.pack('<4I',0,0xFFFFFF,0x080808,0xC0C0C0);after=v.convert_surface(raw,[2,2],[0,0,2,2],before,8,[1,1]);touched={i for row in (1,2) for i in range(row*8+2,row*8+6)}
  self.assertEqual([after[i] for i in range(64) if i not in touched],[0xA5]*(64-len(touched)));self.assertEqual(after[10:14],struct.pack('<2H',0,0xFFFF));self.assertNotEqual(after,before)
 def test_nested_full_capture_inventory(self):
  c={k:{} for k in v.CAPTURE_KEYS};self.assertEqual(v.capture_list(dict(role=dict(ready=c),replacement=[dict(before=c)])),[('/role/ready',c),('/replacement/0/before',c)])
 def test_five_implementation_files_include_new_helper(self):self.assertEqual(len(v.IMPLEMENTATIONS),5);self.assertIn('tools/terminal_followup_d3d8_platform.cs',v.IMPLEMENTATIONS)
 def test_original_empty_text_group_preserves_all_stale_record_bytes(self):
  raw=bytearray([0xCD])*0xAB8;struct.pack_into('<H',raw,22,0);self.assertEqual(v.text_update(bytes(raw),[42,190],v.text_object(4)),dict(after_hex=raw.hex(),draws=[],readiness=True))
 def test_original_text_group_unknown_count_rejected(self):
  raw=bytearray(0xAB8);struct.pack_into('<H',raw,22,11)
  with self.assertRaises(ValueError):v.text_update(bytes(raw),[42,190],v.text_object(4))

class TerminalFollowupTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  with gzip.open(e.ROOT/REPORT,'rt',encoding='utf8') as f:cls.report=json.load(f)
  cls.rows=cls.report['cases'];cls.refs={r['input']['name']:v.pixels(r)[1] for r in cls.rows}
 def reject(self,edit,check,index=0,fields=()):
  row=dict(self.rows[index]);row['terminal_followup']=copy.deepcopy(row['terminal_followup'])
  for key in fields:row[key]=copy.deepcopy(row[key])
  edit(row)
  with self.assertRaises((ValueError,KeyError,IndexError,StopIteration,AssertionError)):check(row)
 def replay(self,row):return v.Replay(row,self.refs[row['input']['name']]).execute()
 def cleanup(self,row):
  replay=v.Replay(row,self.refs[row['input']['name']]);replay.execute();return replay.cleanup()
 @staticmethod
 def new(row,kind='text'):return next(r for r in v.new_resources(row) if r['kind']==kind)
 def test_complete_independent_original_branches(self):
  self.assertEqual(self.report['source_contract'],e.source_contract())
  for row in self.rows:
   with self.subTest(name=row['input']['name']):self.assertEqual(v.verify_case(row)['timing']['VM_PC'],198 if row['input']['name']=='neutral_running' else 194)
 def test_fixed_latest_parent_and_accepted_boundary(self):self.assertEqual(e.fixed_parents()['source']['sha256'],v.PARENT_SOURCE_SHA)
 def test_runtime_original_host_and_code_guards(self):
  r=self.rows[0];g=e.FollowupMachine(r['input'],SimpleNamespace(hello=r['current_CRT_hello']),SimpleNamespace(hello=r['current_GPU_hello'],device=r['current_GPU_hello']['device']))
  try:
   for p in (e.VM+28,e.VM+32,v.text_object(4)+22,v.text_record(5)+44,v.node(4),e.KEYBOARD+0x4B9):
    with self.subTest(pointer=p),self.assertRaises(ValueError):g.put(p,0)
   g.put(e.STACK+0xF000,e.RETURN)
   with self.assertRaises(ValueError):g.source_code(g.uc,0x401000,1,None)
   with self.assertRaises(ValueError):g.write_hook(g.uc,0,0x5920A0,4,0,None)
  finally:g.name_platform.close()
 def test_next43_dispatch_rejected(self):self.reject(lambda r:r['terminal_followup']['commands'].append(dict(PC=198,opcode=43,bytes=8,source_pointer=0)),v.source)
 def test_short_role_operands_or_wrong_PC_rejected(self):self.reject(lambda r:r['terminal_followup']['commands'][0].update(bytes=16),v.source)
 def test_configuration_index_used_as_layer_rejected(self):self.reject(lambda r:r['terminal_followup']['branch'].update(layer=7),v.protocol)
 def test_new_captured_input_cycle_cannot_reuse_old_bindings(self):self.reject(lambda r:r['terminal_followup']['bindings'][0].update(cycle='terminal_confirmation'),v.protocol)
 def test_full_raw_keyboard_sample_rejected(self):self.reject(lambda r:r['terminal_followup']['bindings'][0]['capture'].update(raw_device_hex='00'),v.protocol)
 def test_full_derived_keyboard_memory_rejected(self):
  def edit(r):
   b=r['terminal_followup']['bindings'][0];raw=bytearray.fromhex(b['after_hex']);raw[-1]^=1;b['after_hex']=raw.hex()
  self.reject(edit,v.protocol)
 def test_keyboard_fragment_stack_or_receiver_rejected(self):self.reject(lambda r:r['terminal_followup']['bindings'][0]['fragment'].update(receiver=e.VM),v.protocol)
 def test_keyboard_bridge_entire_owner_is_checked(self):
  def edit(r):
   f=r['terminal_followup']['frames'][2];raw=bytearray.fromhex(f['before']['owner']);raw[0]^=1;f['before']['owner']=raw.hex()
  self.reject(edit,v.protocol)
 def test_keyboard_bridge_preserves_every_other_state_field(self):self.reject(lambda r:r['terminal_followup']['bindings'][1]['after']['state'].update(SEH='ffffffff'),v.protocol)
 def test_keyboard_bridge_exact_previous_CPU_is_checked(self):
  def edit(r):r['terminal_followup']['bindings'][1]['before_CPU']['EAX']^=1
  self.reject(edit,v.protocol)
 def test_false_host_derived_input_write_rejected(self):self.reject(lambda r:r['terminal_followup']['bindings'][0]['only_device_output_written'].update(pointer=e.KEYBOARD+0x4B9),v.protocol)
 def test_missing_new_confirmation_hold_rejected(self):self.reject(lambda r:r['terminal_followup']['frames'].pop(),v.protocol)
 def test_wrong_new_confirmation_wait_rejected(self):
  def edit(r):
   d=r['terminal_followup'];raw=bytearray.fromhex(d['final']['state']['VM']);struct.pack_into('<H',raw,32,0);d['final']['state']['VM']=raw.hex()
  self.reject(edit,v.protocol)
 def test_world_clock_during_terminal_rejected(self):self.reject(lambda r:r['terminal_followup']['frames'][0]['after'].update(elapsed=-1),v.protocol)
 def test_wrong_actual_side_rejected(self):self.reject(lambda r:r['terminal_followup']['role']['pending_image'].update(side_byte=1),v.protocol)
 def test_wrong_actual_image_group_rejected(self):self.reject(lambda r:r['terminal_followup']['role']['pending_image']['args'].__setitem__(1,32),v.protocol)
 def test_wrong_original_slot_formula_rejected(self):self.reject(lambda r:r['terminal_followup']['role']['pending_image'].update(group_words=[32,33]),v.protocol)
 def test_SC002_substitution_rejected(self):self.reject(lambda r:r['terminal_followup']['role']['pending_image'].update(path='data\\adv\\bin\\sc002.bin'),v.protocol)
 def test_SC001_file_byte_rejected(self):self.reject(lambda r:self.new(r,'portrait')['constructed'].update(file_hex='00'),v.protocol)
 def test_missing_original_SC001_copy_row_rejected(self):self.reject(lambda r:self.new(r,'portrait')['copy_rows'].pop(),v.pixels)
 def test_wrong_original_SC001_copy_ABI_rejected(self):self.reject(lambda r:self.new(r,'portrait')['copy_rows'][311]['args'].__setitem__(2,510),v.pixels)
 def test_whole_SC001_texel_rejected(self):self.reject(lambda r:self.new(r,'portrait').update(upload_hex='00'),v.pixels)
 def test_name_source_font_weight_rejected(self):self.reject(lambda r:self.new(r,'name')['pending_font']['args'].__setitem__(4,400),v.pixels)
 def test_text_template_font_size_substitution_rejected(self):self.reject(lambda r:self.new(r)['pending_font']['args'].__setitem__(0,24),v.pixels)
 def test_font_entry_falsely_executed_rejected(self):self.reject(lambda r:self.new(r)['pending_font'].update(first_instruction_executed=True),v.pixels)
 def test_wrong_GDI_shadow_stage_rejected(self):self.reject(lambda r:self.new(r)['raster']['stages'][1].update(hex='00'),v.pixels)
 def test_wrong_GDI_face_rejected(self):self.reject(lambda r:self.new(r)['raster'].update(selected_face='fake'),v.pixels)
 def test_wrong_conversion_band_rejected(self):self.reject(lambda r:self.new(r)['conversions'][0]['point'].__setitem__(1,999),v.pixels)
 def test_partial_current_initial_surface_rejected(self):self.reject(lambda r:self.new(r)['lock'].update(hex='ff'),v.pixels)
 def test_whole_current_readback_hash_rejected(self):self.reject(lambda r:self.new(r)['readback'].update(sha256='0'*64),v.pixels)
 def test_44_cannot_release_old_texture_rejected(self):self.reject(lambda r:r['terminal_followup']['clear'].update(GPU_wire_after=-1),v.protocol,1)
 def test_44_cannot_clear_old_texture_pointer_rejected(self):
  def edit(r):
   b=r['terminal_followup']['clear']['after'];p=v.text_record(5)+44
   for x in b['memory']:
    if x['pointer']<=p<x['pointer']+x['bytes']:
     raw=bytearray.fromhex(x['hex']);struct.pack_into('<I',raw,p-x['pointer'],0);x['hex']=raw.hex();return
  self.reject(edit,v.protocol,1)
 def test_replacement_wrong_original_caller_rejected(self):self.reject(lambda r:r['terminal_followup']['replacements'][0].update(caller=0x4CAD09),v.protocol,1)
 def test_replacement_old_generation_lie_rejected(self):self.reject(lambda r:r['terminal_followup']['replacements'][0].update(generation=self.new(r)['generation']),v.protocol,1)
 def test_replacement_no_original_release_rejected(self):self.reject(lambda r:r['terminal_followup']['replacements'][0]['GPU_APIs'].pop(),v.protocol,1)
 def test_generation_creation_ordinal_rejected(self):self.reject(lambda r:self.new(r).update(generation=1),v.native)
 def test_generation_release_interval_rejected(self):self.reject(lambda r:r['followup_resources_after_cleanup'][-1].update(release_wire_index=0),v.native,fields=('followup_resources_after_cleanup',))
 def test_generation_false_alive_after_forward_rejected(self):self.reject(lambda r:self.new(r).update(alive_after_forward=False),v.native)
 def test_generation_observer_cannot_read_retired_old_text_rejected(self):
  def edit(r):
   d=r['terminal_followup'];old=next(x for x in d['resources_before'] if x['label']=='text5');d['readback_observers'][-1]['generation']=old['generation']
  self.reject(edit,v.native,1)
 def test_missing_current_observer_rejected(self):self.reject(lambda r:r['terminal_followup']['readback_observers'].pop(),v.native)
 def test_wrong_current_COM_generation_rejected(self):self.reject(lambda r:r['terminal_followup']['GPU_APIs'][0].update(generation=1),v.native)
 def test_wrong_current_COM_phase_rejected(self):self.reject(lambda r:r['terminal_followup']['GPU_APIs'][0].update(phase='cleanup'),v.native)
 def test_wrong_current_native_GPU_owner_rejected(self):
  def edit(r):
   i=r['terminal_followup']['readback_observers'][0]['wire_index'];r['GPU_trace'][i]['request']['pointer']=1
  self.reject(edit,v.native,fields=('GPU_trace',))
 def test_raw_GPU_wire_order_rejected(self):self.reject(lambda r:r['GPU_trace'][-1]['reply'].update(id=0),v.native,fields=('GPU_trace',))
 def test_raw_native_allocation_input_receipt_rejected(self):
  def edit(r):
   wire=next(x for x in r['CRT_trace'][r['terminal_followup']['prefix']['CRT_wire']:] if x['request']['op']=='alloc');raw=bytearray.fromhex(wire['reply']['result']['hex']);raw[-1]^=1;wire['reply']['result']['hex']=raw.hex()
  self.reject(edit,v.native,fields=('CRT_trace',))
 def test_raw_heap_bytes_resembling_gpu_addresses_not_masked(self):
  def edit(r):
   wire=next(x for x in r['CRT_trace'][r['terminal_followup']['prefix']['CRT_wire']:] if x['request']['op']=='alloc');raw=bytearray.fromhex(wire['reply']['result']['hex']);raw[:4]=struct.pack('<I',r['terminal_followup']['resources'][0]['texture']['pointer']);wire['reply']['result']['hex']=raw.hex()
  self.reject(edit,v.native,fields=('CRT_trace',))
 @staticmethod
 def coordinated_new_allocation_input(row,index,offset):
  d=row['terminal_followup'];a=[a for a in row['CRT_APIs'][d['prefix']['CRT_APIs']:] if a['name']=='HeapAlloc'][index];raw=bytearray.fromhex(a['memory_outputs'][0]['hex']);raw[offset]^=1;a['memory_outputs'][0]['hex']=raw.hex();row['CRT_trace'][a['wire_end']-1]['reply']['result']['hex']=raw.hex();leaf=next(x['call'] for x in d['leaves'] if x['kind']=='CRT' and x['call']['wire_start']==a['wire_start']);leaf['memory_outputs'][0]['hex']=raw.hex()
 def test_declared_new_uninitialized_header_input_is_naturally_overwritten(self):
  row=dict(self.rows[0])
  for key in ('terminal_followup','CRT_APIs','CRT_trace'):row[key]=copy.deepcopy(row[key])
  self.coordinated_new_allocation_input(row,0,0);self.assertEqual(self.replay(row)['CPU_registers'],57)
 def test_coordinated_new_uninitialized_padding_corruption_rejected(self):self.reject(lambda r:self.coordinated_new_allocation_input(r,1,-1),self.replay,fields=('CRT_APIs','CRT_trace'))
 def test_native_GDI_owner_domain_rejected(self):self.reject(lambda r:r['terminal_followup']['GDI_handle_projection'][0].update(domain='overlay'),v.native)
 def test_wrong_original_root_rejected(self):self.reject(lambda r:next(s for s in r['terminal_followup']['segments'] if s['root'])['root'].update(receiver=e.VM),self.replay)
 def test_new_VM_handler_root_rejected(self):self.reject(lambda r:next(s for s in r['terminal_followup']['segments'] if s['root']).update(entry=0x4CE8F0),self.replay)
 def test_arbitrary_stop_rejected(self):self.reject(lambda r:r['terminal_followup']['segments'][0].update(stop=0x4CAD09),self.replay)
 def test_wrong_57_CPU_rejected(self):self.reject(lambda r:r['terminal_followup']['segments'][0]['CPU'].update(EAX=1),self.replay)
 def test_wrong_PC_digest_rejected(self):self.reject(lambda r:r['terminal_followup']['segments'][0]['local_after'].update(code_sha256='0'*64),self.replay)
 def test_wrong_store_digest_rejected(self):self.reject(lambda r:r['terminal_followup']['segments'][0]['local_after'].update(write_sha256='0'*64),self.replay)
 def test_wrong_original_store_rejected(self):self.reject(lambda r:r['terminal_followup']['writes'][0].update(value=1234),self.replay)
 def test_wrong_frame_all_region_SHA_rejected(self):self.reject(lambda r:r['terminal_followup']['frames'][0]['capture']['memory'][0].update(sha256='0'*64),self.replay)
 def test_wrong_frame_queue_bytes_rejected(self):self.reject(lambda r:r['terminal_followup']['frames'][0]['queue_after'].update(heads='00'),self.replay)
 def test_wrong_query_all_nodes_or_ABI_rejected(self):self.reject(lambda r:r['terminal_followup']['queries'][0].update(receiver=1),self.replay)
 def test_wrong_original_replacement_full_CPU_rejected(self):self.reject(lambda r:r['terminal_followup']['replacements'][0]['before']['CPU'].update(EAX=1),self.replay,1)
 def test_wrong_full_resource_boundary_memory_rejected(self):self.reject(lambda r:self.new(r)['raster']['memory'][0].update(hex='00'),self.replay)
 def test_wrong_platform_output_rejected(self):self.reject(lambda r:next(x for x in r['terminal_followup']['leaves'] if x['call']['memory_outputs'])['call'].update(memory_outputs=[]),self.replay)
 def test_wrong_parent_boundary_CPU_rejected(self):self.reject(lambda r:r['terminal_followup']['before']['CPU'].update(EAX=1),lambda r:v.prefix(r,replay=False))
 def test_wrong_parent_cumulative_SHA_rejected(self):self.reject(lambda r:r['terminal_followup']['before']['trace'].update(code_sha256='0'*64),lambda r:v.prefix(r,replay=False))
 def test_false_current_clock_execution_rejected(self):self.reject(lambda r:next(a for a in r['APIs'] if a['name']=='GetTickCount').update(actual_API_executed=True),lambda r:v.prefix(r,replay=False),fields=('APIs',))
 def test_changed_fixed_clock_sample_rejected(self):self.reject(lambda r:next(a for a in r['APIs'] if a['name']=='GetTickCount').update(result=-1),lambda r:v.prefix(r,replay=False),fields=('APIs',))
 def test_invalid_content_addressed_page_rejected(self):self.reject(lambda r:r['blobs'].update({'0'*64:'00'}),lambda r:v.prefix(r,replay=False),fields=('blobs',))
 def test_valid_but_unrelated_final_VM_page_rejected(self):
  def edit(r):
   raw=bytes([0x11])*4096;key=v.sha(raw);r['blobs'][key]=raw.hex();r['final_state']['terminal_state']['VM']['pages'][0]=key
  self.reject(edit,v.final_summary,fields=('blobs','final_state'))
 def test_wrong_actual_cleanup_57_CPU_rejected(self):self.reject(lambda r:r['followup_cleanup'][0]['after']['CPU'].update(EAX=1),self.cleanup,fields=('followup_cleanup',))
 def test_wrong_actual_cleanup_full_memory_rejected(self):self.reject(lambda r:r['followup_cleanup'][0]['after']['memory'][0].update(hex='00'),self.cleanup,fields=('followup_cleanup',))
 def test_wrong_actual_cleanup_root_rejected(self):self.reject(lambda r:r['cleanup_steps'][0].update(entry=0x403BD0),self.cleanup,fields=('cleanup_steps',))
 def test_wrong_actual_old_name_cleanup_CPU_rejected(self):
  def edit(r):next(c for c in r['followup_cleanup'] if c['label']=='supplemental_original_name_texture_destructor')['after']['CPU']['EAX']=1
  self.reject(edit,self.cleanup,fields=('followup_cleanup',))
 def test_wrong_actual_native_cleanup_sync_buffer_rejected(self):
  def edit(r):
   wire=next(x for x in r['CRT_trace'][r['terminal_followup']['CRT_forward_wire_end']:] if x['request']['op']=='sync');raw=bytearray.fromhex(wire['request']['hex']);raw[-1]^=1;wire['request']['hex']=wire['reply']['result']['hex']=raw.hex()
  self.reject(edit,self.cleanup,fields=('CRT_trace',))

if __name__=='__main__':unittest.main()
