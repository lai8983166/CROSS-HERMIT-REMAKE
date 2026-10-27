"""Reject fabricated layer7 group resources, current receipts and forward state."""
import copy,gzip,json,os,struct,unittest
from types import SimpleNamespace
from tools import terminal_panel_dialogue_emulation as e
from tools import terminal_panel_dialogue_verification as v
REPORT=os.environ.get('TERMINAL_PANEL_DIALOGUE_REPORT','analysis/terminal-panel-dialogue-source-v1-20261026.json.gz')

class TerminalPanelDialogueTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.report=json.loads(gzip.decompress((e.ROOT/REPORT).read_bytes()));cls.rows=cls.report['cases'];cls.refs={r['input']['name']:v.pixels(r)[1] for r in cls.rows}
 def reject(self,edit,check,index=0):
  row=dict(self.rows[index]);row['terminal_panel_dialogue']=copy.deepcopy(row['terminal_panel_dialogue']);edit(row)
  with self.assertRaises((ValueError,KeyError,IndexError,StopIteration,AssertionError)):check(row)
 def replay(self,row):return v.Replay(row,self.refs[row['input']['name']]).execute()
 def native(self,row):return v.native(row)
 def test_two_complete_independent_original_groups(self):
  self.assertEqual(self.report['source_contract'],e.source_contract())
  for r in self.rows:
   with self.subTest(name=r['input']['name']):self.assertEqual(v.verify_case(r)['timing']['VM_PC'],156 if r['input']['name']=='neutral_running' else 168)
 def test_fixed_parent_references(self):self.assertEqual(e.fixed_parents()['source']['sha256'],v.PARENT_SOURCE_SHA)
 def test_live_integer_allocation_keys_equal_JSON_report_without_changing_bytes(self):
  p=0x30000000;live=dict(prefix=dict(allocations={p:dict(guest=p,bytes=128,freed=False,hex='0123456789abcdef')}));report=json.loads(json.dumps(live));self.assertEqual(v.guest(live),v.guest(report));self.assertEqual(v.guest(live)['prefix']['allocations'][str(p)]['hex'],'0123456789abcdef')
 def test_JSON_object_key_collision_and_non_JSON_key_rejected(self):
  for bad in ({1:'integer','1':'string'},{None:0},{True:0},{(1,):0}):
   with self.subTest(keys=list(bad)):
    with self.assertRaises(ValueError):v.guest(bad)
 def test_runtime_source_guard_inherited(self):self.assertIs(e.PanelDialogueMachine.source_code.__code__,e.parent.ConfirmationMachine.source_code.__code__)
 def test_runtime_rejects_unknown_branch(self):
  with self.assertRaises(ValueError):e.branch('fake')
 def test_runtime_rejects_fourth_or_out_of_order_sentence_before_memory_access(self):
  g=e.PanelDialogueMachine.__new__(e.PanelDialogueMachine);g.pd_branch=e.branch('timeout_before_combat');g.pd_sentences=[];g.pd_current=None
  for i in (-1,1,3):
   with self.assertRaises(ValueError):g.pd_prepare_sentence(i)
 def test_runtime_original_host_and_code_guards(self):
  r=self.rows[0];g=e.PanelDialogueMachine(r['input'],SimpleNamespace(hello=r['current_CRT_hello']),SimpleNamespace(hello=r['current_GPU_hello'],device=r['current_GPU_hello']['device']))
  try:
   for p in (e.VM+28,e.VM+32,e.OBJECT+22,e.TEXTURE+44,e.NODE,e.parent.KEYBOARD+0x4B9):
    with self.assertRaises(ValueError):g.put(p,0)
   g.put(e.STACK+0xF000,e.RETURN)
   with self.assertRaises(ValueError):g.source_code(g.uc,0x401000,1,None)
   with self.assertRaises(ValueError):g.write_hook(g.uc,0,0x5920A0,4,0,None)
  finally:g.name_platform.close()
 def test_wrong_text_index(self):self.reject(lambda r:r['terminal_panel_dialogue']['sentences'][0].update(text_index=0),v.source)
 def test_wrong_branch_command_PC(self):self.reject(lambda r:r['terminal_panel_dialogue']['sentences'][0].update(PC=104),v.source)
 def test_wrong_record_stride(self):self.reject(lambda r:r['terminal_panel_dialogue']['sentences'][1].update(record=e.TEXTURE),v.source,1)
 def test_missing_timeout_line(self):self.reject(lambda r:r['terminal_panel_dialogue']['sentences'].pop(),v.source,1)
 def test_wrong_font_weight(self):self.reject(lambda r:r['terminal_panel_dialogue']['sentences'][0]['pending_font']['args'].__setitem__(4,700),v.source)
 def test_template_font_size_substituted(self):self.reject(lambda r:r['terminal_panel_dialogue']['sentences'][0]['pending_font']['args'].__setitem__(0,24),v.source)
 def test_font_falsely_already_executed(self):self.reject(lambda r:r['terminal_panel_dialogue']['sentences'][0]['pending_font'].update(first_instruction_executed=True),v.source)
 def test_wrong_stage_bytes(self):self.reject(lambda r:r['terminal_panel_dialogue']['sentences'][0]['raster']['stages'][1].update(hex='00'),v.pixels)
 def test_wrong_selected_face(self):self.reject(lambda r:r['terminal_panel_dialogue']['sentences'][0]['raster'].update(selected_face='fake'),v.pixels)
 def test_wrong_geometry(self):self.reject(lambda r:r['terminal_panel_dialogue']['sentences'][0]['geometry'].update(padding=3),v.pixels)
 def test_wrong_conversion_band(self):self.reject(lambda r:r['terminal_panel_dialogue']['sentences'][0]['conversions'][0]['point'].__setitem__(1,9),v.pixels)
 def test_wrong_texture_upload(self):self.reject(lambda r:r['terminal_panel_dialogue']['sentences'][0].update(upload_hex='00'),v.pixels)
 def test_nonzero_initial_surface(self):self.reject(lambda r:r['terminal_panel_dialogue']['sentences'][0]['lock'].update(hex='ff'),v.pixels)
 def test_wrong_whole_readback(self):self.reject(lambda r:r['terminal_panel_dialogue']['sentences'][0]['readback'].update(sha256='0'*64),v.pixels)
 def test_wrong_original_dispatch(self):self.reject(lambda r:r['terminal_panel_dialogue']['commands'][0].update(opcode=27),v.source)
 def test_missing_hold(self):self.reject(lambda r:r['terminal_panel_dialogue']['frames'].pop(),v.timing)
 def test_wrong_final_wait(self):self.reject(lambda r:r['terminal_panel_dialogue']['final']['state'].update(VM=r['terminal_panel_dialogue']['before']['state']['VM']),v.timing)
 def test_wrong_old_final_resource(self):self.reject(lambda r:r['terminal_panel_dialogue']['readbacks_old4']['dialogue'].update(hex='00'),self.native)
 def test_wrong_appended_texture_owner(self):self.reject(lambda r:r['terminal_panel_dialogue']['sentences'][0].update(alive=False),v.timing)
 def test_wrong_original_root(self):self.reject(lambda r:next(x for x in r['terminal_panel_dialogue']['segments'] if x['root'])['root'].update(receiver=e.VM),self.replay)
 def test_fake_first_continuation_root(self):self.reject(lambda r:r['terminal_panel_dialogue']['segments'][0].update(root=dict(receiver=e.TASK,args=[])),self.replay)
 def test_wrong_original_entry(self):self.reject(lambda r:r['terminal_panel_dialogue']['segments'][0].update(entry=0x4CAD09),self.replay)
 def test_early_arbitrary_stop(self):self.reject(lambda r:r['terminal_panel_dialogue']['segments'][0].update(stop=0x4CAD09),self.replay)
 def test_wrong_CPU(self):self.reject(lambda r:r['terminal_panel_dialogue']['segments'][0]['CPU'].update(EAX=1),self.replay)
 def test_wrong_PC_digest(self):self.reject(lambda r:r['terminal_panel_dialogue']['segments'][0]['local_after'].update(code_sha256='0'*64),self.replay)
 def test_wrong_store_digest(self):self.reject(lambda r:r['terminal_panel_dialogue']['segments'][0]['local_after'].update(write_sha256='0'*64),self.replay)
 def test_wrong_original_store(self):self.reject(lambda r:r['terminal_panel_dialogue']['writes'][0].update(value=1234),self.replay)
 def test_wrong_original_real_draw_metadata_store(self):self.reject(lambda r:next(x for x in r['terminal_panel_dialogue']['writes'] if x['pc']==0x4CBF3A).update(value=1),self.replay)
 def test_wrong_whole_frame_memory(self):self.reject(lambda r:r['terminal_panel_dialogue']['frames'][0]['capture']['memory'][0].update(sha256='0'*64),self.replay)
 def test_wrong_frame_queue(self):self.reject(lambda r:r['terminal_panel_dialogue']['frames'][0]['queue_after'].update(heads='00'),self.replay)
 def test_wrong_query_ABI(self):self.reject(lambda r:r['terminal_panel_dialogue']['queries'][0].update(receiver=1),self.replay)
 def test_fake_platform_result(self):self.reject(lambda r:r['terminal_panel_dialogue']['leaves'][0]['call'].update(result=1),self.replay)
 def test_fake_platform_output(self):self.reject(lambda r:next(x for x in r['terminal_panel_dialogue']['leaves'] if x['call']['memory_outputs'])['call'].update(memory_outputs=[]),self.replay)
 def test_wrong_full_key_memory(self):self.reject(lambda r:r['terminal_panel_dialogue']['sentences'][0]['completion']['memory'][0].update(hex='00'),self.replay)
 def test_wrong_predecessor_before_CPU(self):self.reject(lambda r:r['terminal_panel_dialogue']['before']['CPU'].update(EAX=1),lambda r:v.prefix(r,replay=False))
 def test_wrong_predecessor_opaque_actual_SHA(self):self.reject(lambda r:r['terminal_panel_dialogue']['before']['trace'].update(code_sha256='0'*64),lambda r:v.prefix(r,replay=False))
 def test_wrong_fixed_clock_sample(self):
  r=dict(self.rows[0]);r['APIs']=copy.deepcopy(r['APIs']);next(x for x in r['APIs'] if x['name']=='GetTickCount')['result']^=1
  with self.assertRaises(ValueError):v.prefix(r,replay=False)
 def test_false_current_clock_execution_claim(self):
  r=dict(self.rows[0]);r['APIs']=copy.deepcopy(r['APIs']);next(x for x in r['APIs'] if x['name']=='GetTickCount')['actual_API_executed']=True
  with self.assertRaises(ValueError):v.prefix(r,replay=False)
 def test_fake_content_addressed_page(self):
  r=dict(self.rows[0]);r['blobs']=dict(r['blobs']);r['blobs']['0'*64]='00'
  with self.assertRaises(ValueError):v.prefix(r,replay=False)
 def test_changed_fixed_intermediate_page(self):
  r=dict(self.rows[0]);r['blobs']=dict(r['blobs']);key=next(iter(r['blobs']));r['blobs'][key]='ff'+r['blobs'][key][2:]
  with self.assertRaises(ValueError):v.prefix(r,replay=False)
 def test_valid_but_unrelated_final_VM_page(self):
  r=dict(self.rows[0]);r['blobs']=dict(r['blobs']);r['final_state']=copy.deepcopy(r['final_state']);page=bytes([0x11])*4096;key=e.sha(page);r['blobs'][key]=page.hex();r['final_state']['terminal_state']['VM']['pages'][0]=key
  with self.assertRaises(ValueError):v.final_summary(r)
 def test_wrong_raw_GPU_receipt(self):
  r=dict(self.rows[0]);r['GPU_trace']=copy.deepcopy(r['GPU_trace']);r['GPU_trace'][30]['reply']['id']=0
  with self.assertRaises(ValueError):self.native(r)
 def test_cross_owner_raw_GPU_pointer(self):
  r=dict(self.rows[0]);r['GPU_trace']=copy.deepcopy(r['GPU_trace']);r['GPU_trace'][31]['request']['pointer']=1
  with self.assertRaises((ValueError,KeyError)):self.native(r)
 def test_wrong_raw_CRT_output(self):
  r=dict(self.rows[0]);r['CRT_trace']=copy.deepcopy(r['CRT_trace']);r['CRT_trace'][0]['reply']['result']['pointer']=1
  with self.assertRaises((ValueError,KeyError)):self.native(r)
 def test_actual_uninitialized_allocation_input_must_match_receipt(self):
  r=dict(self.rows[0]);r['CRT_trace']=copy.deepcopy(r['CRT_trace']);wire=next(x for x in r['CRT_trace'] if x['request']['op']=='alloc');raw=bytearray.fromhex(wire['reply']['result']['hex']);raw[0]^=1;wire['reply']['result']['hex']=raw.hex()
  with self.assertRaises(ValueError):self.native(r)
 def test_legitimate_coordinated_uninitialized_header_input_is_overwritten(self):
  r=dict(self.rows[0]);r['CRT_APIs']=copy.deepcopy(r['CRT_APIs']);r['CRT_trace']=copy.deepcopy(r['CRT_trace']);a=next(x for x in r['CRT_APIs'] if x['name']=='HeapAlloc');raw=bytearray.fromhex(a['memory_outputs'][0]['hex']);raw[0]^=1;a['memory_outputs'][0]['hex']=raw.hex();r['CRT_trace'][a['wire_end']-1]['reply']['result']['hex']=raw.hex()
  result=v.ResourceInitializationReplay(r).execute();self.assertEqual(result['CPU_registers'],57);self.assertTrue(result['uninitialized_native_inputs_consumed_by_original_constructors'])
 def test_coordinated_native_file_pixel_corruption_fails_original_construction(self):
  r=dict(self.rows[0]);r['CRT_APIs']=copy.deepcopy(r['CRT_APIs']);r['CRT_trace']=copy.deepcopy(r['CRT_trace']);a=next(x for x in r['CRT_APIs'] if x['name']=='ReadFile');raw=bytearray.fromhex(a['memory_outputs'][0]['hex']);raw[32+24]^=1;a['memory_outputs'][0]['hex']=raw.hex();r['CRT_trace'][a['wire_end']-1]['reply']['result']['after_hex']=raw.hex()
  with self.assertRaises(ValueError):v.ResourceInitializationReplay(r).execute()
 def test_wrong_native_GDI_domain(self):self.reject(lambda r:r['terminal_panel_dialogue']['GDI_handle_projection'][0].update(domain='overlay'),self.native)
 def test_unclassified_readback(self):self.reject(lambda r:r['terminal_panel_dialogue']['sentences'][0]['observer_wire_indices'].pop(),self.native)
 def test_wrong_actual_cleanup_CPU(self):
  r=dict(self.rows[0]);r['panel_dialogue_cleanup']=copy.deepcopy(r['panel_dialogue_cleanup']);r['panel_dialogue_cleanup'][0]['after']['CPU']['EAX']=1;replay=v.Replay(r,self.refs[r['input']['name']]);replay.execute()
  with self.assertRaises(ValueError):replay.cleanup()
 def test_wrong_actual_cleanup_memory(self):
  r=dict(self.rows[0]);r['panel_dialogue_cleanup']=copy.deepcopy(r['panel_dialogue_cleanup']);r['panel_dialogue_cleanup'][0]['after']['memory'][0]['hex']='00';replay=v.Replay(r,self.refs[r['input']['name']]);replay.execute()
  with self.assertRaises(ValueError):replay.cleanup()
 def test_wrong_actual_old_dialogue_cleanup_CPU(self):
  r=dict(self.rows[0]);r['dialogue_cleanup']=copy.deepcopy(r['dialogue_cleanup']);r['dialogue_cleanup']['CPU']['EAX']=1;replay=v.Replay(r,self.refs[r['input']['name']]);replay.execute()
  with self.assertRaises(ValueError):replay.cleanup()
 def test_wrong_actual_cleanup_root(self):
  r=dict(self.rows[0]);r['cleanup_steps']=copy.deepcopy(r['cleanup_steps']);r['cleanup_steps'][0]['entry']=0x403BD0;replay=v.Replay(r,self.refs[r['input']['name']]);replay.execute()
  with self.assertRaises(ValueError):replay.cleanup()
 def test_wrong_current_native_cleanup_sync_bytes(self):
  r=dict(self.rows[0]);r['CRT_trace']=copy.deepcopy(r['CRT_trace']);end=r['CRT_APIs'][r['terminal_panel_dialogue']['prefix']['CRT_APIs']-1]['wire_end'];wire=next(x for x in r['CRT_trace'][end:] if x['request']['op']=='sync');raw=bytearray.fromhex(wire['request']['hex']);raw[-1]^=1;wire['request']['hex']=wire['reply']['result']['hex']=raw.hex();replay=v.Replay(r,self.refs[r['input']['name']]);replay.execute()
  with self.assertRaises(ValueError):replay.cleanup()

if __name__=='__main__':unittest.main()
