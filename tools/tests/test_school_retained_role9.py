"""Original role9 name/SC009/task execution and independently owned platform contracts."""
import copy,gzip,json,unittest
from unittest.mock import patch
from tools import school_retained_role9_verification as v
from tools.tests.test_school_retained_third_dialogue import clone

def isolated(seed):
 r=clone(seed)
 for key in ('role_space','role_objects','history','blocks','criticals','all_copies','step_copies'):
  if hasattr(seed,key):setattr(r,key,copy.deepcopy(getattr(seed,key)))
 return r

class Role9Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.path=v.ROOT/'analysis/school-retained-role9-v1-20261023.json.gz';cls.r=json.loads(gzip.decompress(cls.path.read_bytes()));cls.c=cls.r['cases'][0];cls.e=cls.c['role9'];cls.seeds={};original=v.Replay.role_step;wanted={cls.e[k]['label']:k for k in ('name','name_upload','image_prefix','image','completion','image_cleanup','name_cleanup')}
  def observe(r,s):
   if s['label'] in wanted:cls.seeds[wanted[s['label']]]=isolated(r)
   return original(r,s)
  with patch.object(v.Replay,'role_step',observe):cls.proof=v.verify_case(cls.c)
 def reject(self,edit):
  c=copy.deepcopy(self.c);edit(c['role9'])
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):v.protocol(c)
 def step_reject(self,key,edit):
  r=isolated(self.seeds[key]);s=copy.deepcopy(self.e[key]);edit(s)
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):r.role_step(s)
 def gpu_reject(self,index,edit):
  key='name_upload' if index<4 else 'image' if index<8 else 'image_cleanup' if index<10 else 'name_cleanup'
  self.step_reject(key,lambda s:edit(next(a for a in s['result']['api_calls'] if a['kind']=='actual_role9_GPU' and a['index']==index)))
 def file_reject(self,name,edit):self.step_reject('image_prefix',lambda s:edit(next(a for a in s['result']['api_calls'] if a.get('name')==name)))
 def gdi_reject(self,name,edit):self.step_reject('name',lambda s:edit(next(a for a in s['result']['api_calls'] if a.get('name')==name)))
 def test_00_complete_case_and_six_independent_proofs(self):
  p=json.loads((v.ROOT/'analysis/school-retained-role9-proof-v1-20261023.json').read_bytes());self.assertEqual(p['source_report_sha256'],v.sha(self.path.read_bytes()));self.assertTrue(p['six_original_role9_resources_tasks_and_readiness_verified']);self.assertEqual(len(p['cases']),6);self.assertEqual(self.proof['role9']['new_original_forward_instructions'],4512473);self.assertTrue(all(c['role9']['final_PC']==332 and c['role9']['natural_readiness_updates']==77 and c['role9']['original_copy_rows']==512 for c in p['cases']))
 def test_parent_pin(self):self.reject(lambda e:e['contract'].update(parent_acceptance_sha256='0'*64))
 def test_original_name(self):self.reject(lambda e:e['contract']['role'].update(name_hex='41'))
 def test_original_configuration(self):self.reject(lambda e:e['contract']['configuration'].update(layer=7))
 def test_original_SC009(self):self.reject(lambda e:e['contract']['role'].update(image_sha256='0'*64))
 def test_texture_source_root(self):self.reject(lambda e:e['name_upload'].update(root=dict(va=0x403bd0)))
 def test_image_source_root(self):self.reject(lambda e:e['image_prefix'].update(root=dict(va=0x4cde10)))
 def test_VM_source_root(self):self.reject(lambda e:e['frames'][0]['steps'][-1]['root'].update(va=0x4ce8f0))
 def test_missing_complete_reset(self):self.reject(lambda e:e['frames'][0]['steps'].pop(1))
 def test_missing_wait_update(self):self.reject(lambda e:e['frames'].pop())
 def test_early_wait_release(self):self.reject(lambda e:e['frames'][75]['state'].update(wait=0))
 def test_host_input_write(self):self.reject(lambda e:e.update(input_host_writes=1))
 def test_host_control_write(self):self.reject(lambda e:e.update(PC_or_wait_host_writes=1))
 def test_retained_input_change(self):self.reject(lambda e:e['frames'][20]['state'].update(input_words=[0,128,0]))
 def test_next_instruction_claim(self):self.reject(lambda e:e.update(next_script_instruction_executed=True))
 def test_task_not_complete(self):self.reject(lambda e:e.update(role9_complete_task_returned=False))
 def test_not_ready(self):self.reject(lambda e:e.update(role9_naturally_ready=False))
 def test_fourth_resource_not_retained(self):self.reject(lambda e:e.update(fourth_domain_retained=False))
 def test_missing_nested_name_frame(self):self.reject(lambda e:e['pending_name_texture']['frames'].pop())
 def test_missing_nested_portrait_frame(self):self.reject(lambda e:e['image_record']['frames'].pop())
 def test_actual_GPU_failure(self):self.reject(lambda e:e.update(GPU_exit=1))
 def test_native_driver_forced_release(self):self.reject(lambda e:e['GPU'].update(texture_releases=[0]))
 def test_native_window_visible(self):self.reject(lambda e:e['GPU_hello'].update(window_visible=True))
 def test_native_pointer_width(self):self.reject(lambda e:e['GPU_hello'].update(pointer_bytes=8))
 def test_native_helper_identity(self):self.reject(lambda e:e['GPU_build'].update(source_sha256='0'*64))
 def test_missing_native_readback(self):self.reject(lambda e:e['GPU_trace'].pop(9))
 def test_native_transcript_ID(self):self.reject(lambda e:e['GPU_trace'][3]['reply'].update(id=55))
 def test_file_handle_unclosed(self):self.reject(lambda e:e['files'].update(open_handles=1))
 def test_GDI_objects_unclosed(self):self.reject(lambda e:e['GDI'].update(bitmaps=1))
 def test_missing_source_file_API(self):self.reject(lambda e:e['file_trace'].pop(2))
 def test_incomplete_source_file(self):self.reject(lambda e:e['image_record'].update(file_hex='00'))
 def test_missing_source_row(self):self.reject(lambda e:e['copy_rows'].pop())
 def test_texture_counter_reset(self):self.reject(lambda e:e.update(accounting_after_cleanup=0))
 def test_vector_counter_reset(self):self.reject(lambda e:e.update(game_bytes_with_role=e['game_bytes_before']))
 def test_old_fourth_native_call_added(self):self.reject(lambda e:e.update(fourth_trace_count_after=6))
 def test_missing_full_memory(self):self.reject(lambda e:e['completion'].pop('full_memory'))
 def test_font_caller(self):self.gdi_reject('CreateFontA',lambda a:a.update(return_va=0x4cad09))
 def test_GDI_measurement_translation(self):self.gdi_reject('GetTextExtentPoint32A',lambda a:a['dc_translated_args'].__setitem__(0,1))
 def test_GDI_source_name(self):self.gdi_reject('TextOutA',lambda a:a.update(text_hex='41'))
 def test_file_path(self):self.file_reject('CreateFileA',lambda a:a.update(source_relative_path_hex='41'))
 def test_file_write_access(self):self.file_reject('CreateFileA',lambda a:a['args'].__setitem__(1,0x40000000))
 def test_file_foreign_handle(self):self.file_reject('GetFileSize',lambda a:a['args'].__setitem__(0,1))
 def test_file_partial_read(self):self.file_reject('ReadFile',lambda a:a.update(bytes_read=512))
 def test_file_wrong_hash(self):self.file_reject('ReadFile',lambda a:a.update(file_sha256='0'*64))
 def test_file_foreign_allocation(self):self.file_reject('ReadFile',lambda a:a.update(source_allocation=0x50201000))
 def test_file_output_into_PC(self):self.file_reject('ReadFile',lambda a:a['memory_outputs'].append(dict(pointer=v.base.VM+28,hex='00000000')))
 def test_file_bad_close_caller(self):self.file_reject('CloseHandle',lambda a:a.update(return_va=0x40378d))
 def test_GPU_wrong_device(self):self.gpu_reject(0,lambda a:a['args'].__setitem__(0,1))
 def test_GPU_wrong_name_width(self):self.gpu_reject(0,lambda a:a['args'].__setitem__(1,128))
 def test_GPU_wrong_format(self):self.gpu_reject(0,lambda a:a['args'].__setitem__(5,21))
 def test_GPU_wrong_object(self):self.gpu_reject(4,lambda a:a.update(object_index=0))
 def test_GPU_wrong_portrait_request(self):self.gpu_reject(4,lambda a:a['native_request'].update(height=256))
 def test_GPU_wrong_native_response(self):self.gpu_reject(4,lambda a:a['native_result'].update(hr=1))
 def test_GPU_wrong_descriptor(self):self.gpu_reject(5,lambda a:a['result'].update(hex='00'))
 def test_GPU_foreign_method(self):self.gpu_reject(5,lambda a:a.update(target=1))
 def test_GPU_wrong_lock_flag(self):self.gpu_reject(6,lambda a:a['args'].__setitem__(4,16))
 def test_GPU_wrong_lock_pitch(self):self.gpu_reject(6,lambda a:a['result'].update(pitch=514))
 def test_GPU_foreign_locked_bits(self):self.gpu_reject(6,lambda a:a['result'].update(bits=1))
 def test_GPU_extra_host_output(self):self.gpu_reject(6,lambda a:a['memory_outputs'].append(dict(pointer=v.base.VM+28,hex='00000000')))
 def test_GPU_partial_upload(self):self.gpu_reject(7,lambda a:a.update(uploaded_hex='00'))
 def test_GPU_bad_upload_receipt(self):self.gpu_reject(7,lambda a:a['result'].update(uploaded_sha256='0'*64))
 def test_GPU_nonzero_Release(self):self.gpu_reject(9,lambda a:a['result'].update(count=1))
 def test_GPU_wrong_name_Release(self):self.gpu_reject(11,lambda a:a['args'].__setitem__(0,self.e['textures'][1]['texture']['pointer']))
 def test_source_instruction_digest(self):self.step_reject('name',lambda s:s['result'].update(instruction_sha256='0'*64))
 def test_source_write_digest(self):self.step_reject('name',lambda s:s['result'].update(write_sha256='0'*64))
 def test_source_full_CPU(self):self.step_reject('name',lambda s:s['architectural_cpu'].update(MXCSR=s['architectural_cpu']['MXCSR']^1))
 def test_source_full_memory(self):self.step_reject('name',lambda s:s['full_memory'][-1].update(sha256='0'*64))
 def test_source_queue_heads(self):self.step_reject('completion',lambda s:s['queue'].update(head_hex='00'))
 def test_source_live_records(self):self.step_reject('completion',lambda s:s['queue'].update(arena_hex='00'))
 def test_source_game_substitution(self):self.step_reject('name',lambda s:s['result']['api_calls'][0].update(kind='game_stub'))
 def test_source_copy_row_arguments(self):self.step_reject('image',lambda s:s['copy_rows'][17]['args'].__setitem__(2,510))
 def test_source_conversion_rectangle(self):self.step_reject('name_upload',lambda s:s['conversions'][0]['rect'].__setitem__(2,58))
 def test_source_original_byte(self):
  r=isolated(self.seeds['name']);r.u.mem_write(0x4ca7cb,b'\x90')
  with self.assertRaises(ValueError):r.role_step(self.e['name'])
 def test_independent_name_pixel(self):
  c=copy.deepcopy(self.c);c['role9']['textures'][0]['uploaded_hex']='00'
  with self.assertRaises(ValueError):v.pixels(c)
 def test_independent_portrait_readback(self):
  c=copy.deepcopy(self.c);c['role9']['textures'][1]['readback']['hex']='00'
  with self.assertRaises(ValueError):v.pixels(c)
 def test_overclaims(self):
  for key in ('new_OS_input','actual_D3D_draw_or_Present','original_outer_scheduler','historical_heap_restored','R3_complete','R6_complete'):
   r=dict(self.r);r[key]=True
   with self.assertRaises(ValueError):v.verify(r)

if __name__=='__main__':unittest.main()
