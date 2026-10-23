"""Actual fourth GPU ownership, independent pixels, original task and role9 boundary."""
import copy,gzip,json,unittest
from tools import school_retained_fourth_texture_verification as v
from tools.tests.test_school_retained_third_dialogue import clone

class FourthTextureTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.path=v.ROOT/'analysis/school-retained-fourth-texture-v1-20261023.json.gz';cls.r=json.loads(gzip.decompress(cls.path.read_bytes()));cls.c=cls.r['cases'][0];cls.e=cls.c['fourth_texture'];seeds=[];cls.verified=v.verify_case(cls.c,lambda r:seeds.append(clone(r)));cls.seed=seeds[0];cls.seed.fourth_case=cls.e;cls.seed.native_count=0;cls.seed.fourth_space=v.work.AddressSpace();cls.seed.fourth_space.next=0x6d001000;ref=v.previous.reproduce_pixels(cls.c);cfg=v.geometry(cls.c['third_confirmation']['raster']['measured']);raw=bytes.fromhex(cls.e['lock']['hex'])
  for b in v.bands(cfg):raw=v.convert_surface(ref['stages'][-1],cfg['raster_size'],b['rect'],raw,cls.e['lock']['pitch'],b['point'])
  cls.seed.fourth_pixels=dict(bytes=raw);cls.done=clone(cls.seed);cls.done.fourth_space=copy.deepcopy(cls.seed.fourth_space);cls.done.next_step(cls.e['completion']);cls.role=clone(cls.done);cls.role.next_frame(cls.e['role_prefix'],True)
 def reject(self,edit):
  c=copy.deepcopy(self.c);edit(c['fourth_texture'])
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):v.protocol(c)
 def step_reject(self,edit,cleanup=False):
  r=clone(self.role if cleanup else self.seed);r.fourth_space=copy.deepcopy(r.fourth_space);s=copy.deepcopy(self.e['cleanup' if cleanup else 'completion']);edit(s)
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):r.next_step(s)
 def GPU_reject(self,index,edit):self.step_reject(lambda s:edit(next(a for a in s['result']['api_calls'] if a['kind']=='actual_owned_fourth_GPU' and a['index']==index)),index>=4)
 def GDI_reject(self,name,edit):self.step_reject(lambda s:edit(next(a for a in s['result']['api_calls'] if a.get('name')==name)))
 def test_00_complete_case_and_six_bound_proofs(self):
  p=json.loads((v.ROOT/'analysis/school-retained-fourth-texture-proof-v1-20261023.json').read_bytes());self.assertEqual(p['source_report_sha256'],v.sha(self.path.read_bytes()));self.assertTrue(p['six_actual_fourth_textures_and_role9_handoffs_verified']);self.assertEqual(len(p['cases']),6);self.assertEqual(self.verified['fourth']['new_original_forward_instructions'],82855);self.assertTrue(all(c['fourth']['role_index']==9 and c['fourth']['role_layer']==4 and c['fourth']['final_PC']==312 for c in p['cases']))
 def test_parent_acceptance_pin(self):self.reject(lambda e:e['contract'].update(parent_acceptance_sha256='0'*64))
 def test_current_GPU_source_pin(self):self.reject(lambda e:e['contract'].update(GPU_source_sha256='0'*64))
 def test_role9_name_source(self):self.reject(lambda e:e['contract']['role9'].update(name_hex='41'))
 def test_configuration7_layer(self):self.reject(lambda e:e['contract']['configuration7'].update(layer=7))
 def test_independent_VM_root(self):self.reject(lambda e:e['role_prefix']['steps'][-1]['root'].update(va=0x4ce8f0))
 def test_texture_game_root(self):self.reject(lambda e:e['completion'].update(root=dict(va=0x403bd0)))
 def test_missing_request_or_queue_reset(self):self.reject(lambda e:e['role_prefix']['steps'].pop(1))
 def test_texture_destructor_root(self):self.reject(lambda e:e['cleanup']['root'].update(va=0x41f4e0))
 def test_input_host_write(self):self.reject(lambda e:e.update(input_host_writes=1))
 def test_PC_wait_host_write(self):self.reject(lambda e:e.update(PC_or_wait_host_writes=1))
 def test_fourth_task_not_complete(self):self.reject(lambda e:e.update(fourth_task_completed=False))
 def test_role9_font_falsely_complete(self):self.reject(lambda e:e.update(role9_font_executed=True))
 def test_role9_task_falsely_complete(self):self.reject(lambda e:e.update(role9_task_completed=True))
 def test_wrong_next_opcode(self):self.reject(lambda e:e['final'].update(opcode=51))
 def test_wrong_font_weight(self):self.reject(lambda e:e['pending_font']['args'].__setitem__(4,400))
 def test_wrong_font_return(self):self.reject(lambda e:e['pending_font'].update(return_va=0x4cad09))
 def test_font_entry_executed(self):self.reject(lambda e:e['pending_font'].update(first_instruction_executed=True))
 def test_counter_reset(self):self.reject(lambda e:e.update(accounting_with_fourth=e['accounting_before']))
 def test_counter_cleanup_unbalanced(self):self.reject(lambda e:e.update(accounting_after_cleanup=e['accounting_before']+8192))
 def test_actual_GPU_failed_exit(self):self.reject(lambda e:e.update(GPU_helper_exit=1))
 def test_current_GPU_cleanup(self):self.reject(lambda e:e['GPU_cleanup'].update(all_owned_resources_released=False))
 def test_visible_GPU_window(self):self.reject(lambda e:e['GPU_hello'].update(window_visible=True))
 def test_wrong_native_pointer_width(self):self.reject(lambda e:e['GPU_hello'].update(pointer_bytes=8))
 def test_old_GPU_helper_source(self):self.reject(lambda e:e['GPU_build'].update(source_sha256='0'*64))
 def test_missing_actual_readback(self):self.reject(lambda e:e['GPU_trace'].pop(4))
 def test_current_native_sequence(self):self.reject(lambda e:e['GPU_trace'][2]['reply'].update(id=99))
 def test_readback_receipt_changed(self):self.reject(lambda e:e['actual_readback'].update(sha256='0'*64))
 def test_queue_evidence_missing(self):self.reject(lambda e:e['completion'].pop('queue'))
 def test_GPU_wrong_device(self):self.GPU_reject(0,lambda a:a['args'].__setitem__(0,1))
 def test_GPU_wrong_texture_dimensions(self):self.GPU_reject(0,lambda a:a['args'].__setitem__(1,256))
 def test_GPU_wrong_POOL(self):self.GPU_reject(0,lambda a:a['args'].__setitem__(6,0))
 def test_GPU_wrong_native_request(self):self.GPU_reject(0,lambda a:a['native_request'].update(width=256))
 def test_GPU_wrong_current_response(self):self.GPU_reject(0,lambda a:a['native_result'].update(hr=1))
 def test_GPU_wrong_method_target(self):self.GPU_reject(1,lambda a:a.update(target=a['target']+4))
 def test_GPU_wrong_descriptor(self):self.GPU_reject(1,lambda a:a['result'].update(hex='00'))
 def test_GPU_wrong_lock_flags(self):self.GPU_reject(2,lambda a:a['args'].__setitem__(4,16))
 def test_GPU_wrong_lock_pitch(self):self.GPU_reject(2,lambda a:a['result'].update(pitch=258))
 def test_GPU_expired_native_bits(self):self.GPU_reject(2,lambda a:a['result'].update(bits=1))
 def test_GPU_output_into_game_PC(self):self.GPU_reject(2,lambda a:a['memory_outputs'].append(dict(pointer=v.base.VM+28,hex='00000000')))
 def test_GPU_wrong_full_upload(self):self.GPU_reject(3,lambda a:a.update(uploaded_hex='00'))
 def test_GPU_bad_upload_receipt(self):self.GPU_reject(3,lambda a:a['result'].update(uploaded_sha256='0'*64))
 def test_GPU_Release_count(self):self.GPU_reject(5,lambda a:a['result'].update(count=1))
 def test_original_GDI_bitmap_delete(self):self.GDI_reject('DeleteObject',lambda a:a['args'].__setitem__(0,1))
 def test_original_GDI_DC_delete(self):self.GDI_reject('DeleteDC',lambda a:a.update(result=0))
 def test_full_CPU(self):self.step_reject(lambda s:s['architectural_cpu'].update(MXCSR=s['architectural_cpu']['MXCSR']^1))
 def test_full_memory(self):self.step_reject(lambda s:s['full_memory'][-1].update(sha256='0'*64))
 def test_instruction_digest(self):self.step_reject(lambda s:s['result'].update(instruction_sha256='0'*64))
 def test_write_digest(self):self.step_reject(lambda s:s['result'].update(write_sha256='0'*64))
 def test_queue_heads(self):self.step_reject(lambda s:s['queue'].update(head_hex='00'))
 def test_live_queue_records(self):self.step_reject(lambda s:s['queue'].update(arena_hex='00'))
 def test_source_conversion_rect(self):self.step_reject(lambda s:s['conversions'][0]['rect'].__setitem__(2,85))
 def test_source_conversion_point(self):self.step_reject(lambda s:s['conversions'][0]['point'].__setitem__(0,1))
 def test_game_function_substitution(self):self.step_reject(lambda s:s['result']['api_calls'][0].update(kind='game_stub'))
 def test_original_source_byte(self):
  r=clone(self.seed);r.fourth_space=copy.deepcopy(r.fourth_space);r.u.mem_write(0x403bd0,b'\x90')
  with self.assertRaises(ValueError):r.next_step(self.e['completion'])
 def test_independent_pixel_mismatch(self):
  c=copy.deepcopy(self.c);c['fourth_texture']['uploaded_hex']='00'
  with self.assertRaises(ValueError):v.pixels(c)
 def test_independent_native_readback(self):
  c=copy.deepcopy(self.c);c['fourth_texture']['actual_readback']['hex']='00'
  with self.assertRaises(ValueError):v.pixels(c)
 def test_overclaims(self):
  for k in ('new_OS_input','actual_D3D_draw_or_Present','original_outer_scheduler','historical_heap_restored','role9_font_executed','role9_task_completed','R3_complete','R6_complete'):
   r=dict(self.r);r[k]=True
   with self.assertRaises(ValueError):v.verify(r)
 def test_no_current_GPU(self):
  r=dict(self.r);r['new_native_fourth_texture']=False
  with self.assertRaises(ValueError):v.verify(r)

if __name__=='__main__':unittest.main()
