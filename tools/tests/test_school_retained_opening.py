"""Tamper checks for the complete opening source, controls, ownership and terminal."""
import copy,gzip,json,unittest
from unittest.mock import patch
from tools import school_retained_opening_verification as v
from tools.tests.test_school_retained_third_dialogue import clone

def isolated(seed):
 r=clone(seed);keys=('opening_space','opening_objects','opening_refs','opening_pixels','opening_historical','opening_region_hashes','opening_pending_dirty','role_space','role_objects','history','blocks','criticals','files','all_copies','step_copies')
 values=copy.deepcopy({k:getattr(seed,k) for k in keys if hasattr(seed,k)})
 for k,value in values.items():setattr(r,k,value)
 return r

class OpeningTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.matrix=json.loads((v.ROOT/'analysis/school-retained-opening-matrix-v1-20261023.json').read_bytes());cls.row=cls.matrix['case_reports'][0]
  with gzip.open(v.ROOT/cls.row['path'],'rt',encoding='utf8') as f:cls.c=json.load(f)
  cls.e=cls.c['opening'];cls.seeds={};cls.binding_seed=None;original=v.Replay.source_step;old_binding=v.binding;wanted={'frame_0_0x425de0','frame_1_0x454cf0','frame_2_0x454cf0','frame_62_0x454cf0','frame_221_0x454cf0','supplemental_original_opening_glyph_0'}
  def observe(r,s):
   if s['label'] in wanted:cls.seeds[s['label']]=isolated(r)
   return original(r,s)
  def capture(r,b):
   if cls.binding_seed is None:cls.binding_seed=isolated(r)
   return old_binding(r,b)
  with patch.object(v.Replay,'source_step',observe),patch.object(v,'binding',capture):cls.proof=v.verify_case(cls.c)
 def reject(self,edit):
  c=copy.deepcopy(self.c);edit(c['opening'])
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):v.protocol(c)
 def step(self,label):
  return next(s for s in v.ordered(self.e)+self.e['supplemental_cleanup'] if s['label']==label)
 def step_reject(self,label,edit):
  r=isolated(self.seeds[label]);s=copy.deepcopy(self.step(label));edit(s)
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):r.source_step(s)
 def gpu_reject(self,index,edit):
  label='supplemental_original_opening_glyph_0' if index>=24 else 'frame_1_0x454cf0'
  self.step_reject(label,lambda s:edit(next(a for a in s['result']['api_calls'] if a.get('kind')=='actual_opening_GPU' and a['index']==index)))
 def gdi_reject(self,name,edit):self.step_reject('frame_1_0x454cf0',lambda s:edit(next(a for a in s['result']['api_calls'] if a.get('name')==name)))
 def test_bound_six_proofs_and_source_execution(self):
  p=json.loads((v.ROOT/'analysis/school-retained-opening-proof-v1-20261023.json').read_bytes());self.assertEqual(p['source_matrix_sha256'],v.sha((v.ROOT/'analysis/school-retained-opening-matrix-v1-20261023.json').read_bytes()));self.assertTrue(p['six_original_complete_openings_verified']);self.assertEqual(len(p['cases']),6);self.assertEqual(self.proof['new_original_forward_instructions'],11627289);self.assertEqual(self.proof['new_original_writes'],6115840);self.assertTrue(all(x['final_PC']==492 and x['final_wait']==0 and x['final_opcode']==19 and x['complete_original_tasks']==222 for x in p['cases']))
 def test_parent_acceptance_pin(self):self.reject(lambda e:e['contract'].update(parent_acceptance_sha256='0'*64))
 def test_remaining_command_bytes(self):self.reject(lambda e:e['contract']['commands'][-1].update(hex='00000000'))
 def test_remaining_source_text(self):self.reject(lambda e:e['contract']['texts'][1].update(hex='41'))
 def test_missing_frame(self):self.reject(lambda e:e['frames'].pop(190))
 def test_reordered_frames(self):self.reject(lambda e:e['frames'].reverse())
 def test_missing_queue_reset(self):self.reject(lambda e:e['frames'][70]['steps'].pop(1))
 def test_VM_function_root_substitution(self):self.reject(lambda e:e['frames'][70]['steps'][-1]['root'].update(va=0x4ce8f0))
 def test_host_PC_write(self):self.reject(lambda e:e.update(PC_or_wait_host_writes=1))
 def test_new_VM_root(self):self.reject(lambda e:e.update(new_VM_roots=1))
 def test_OS_input_claim(self):self.reject(lambda e:e.update(new_OS_input=True))
 def test_terminal_PC_advanced_to_extent(self):self.reject(lambda e:e['final'].update(PC=496))
 def test_terminal_wait_not_released(self):self.reject(lambda e:e['final'].update(wait=1))
 def test_terminal_opcode_omitted(self):self.reject(lambda e:e['final'].update(opcode=21))
 def test_terminal_channel_still_active(self):self.reject(lambda e:e['final'].update(vm_header_hex=e['before']['vm_header_hex']))
 def test_first_confirmation_omitted(self):self.reject(lambda e:e['bindings'].pop(0))
 def test_release_bound_to_wrong_PC(self):self.reject(lambda e:e['bindings'][3]['state'].update(PC=366))
 def test_font_missing(self):self.reject(lambda e:e['fonts'].pop())
 def test_glyph_cleanup_missing(self):self.reject(lambda e:e['supplemental_cleanup'].pop())
 def test_glyph_falsely_naturally_released(self):self.reject(lambda e:e['textures'][0].update(live=False,phase=6))
 def test_glyph_unreleased_after_supplement(self):self.reject(lambda e:e['textures_after_cleanup'][0].update(live=True))
 def test_forced_GPU_cleanup(self):self.reject(lambda e:e['GPU'].update(texture_releases=[1]))
 def test_failed_native_exit(self):self.reject(lambda e:e.update(GPU_exit=1))
 def test_visible_native_window(self):self.reject(lambda e:e['GPU_hello'].update(window_visible=True))
 def test_foreign_native_build(self):self.reject(lambda e:e['GPU_build'].update(source_sha256='0'*64))
 def test_GPU_request_ID(self):self.reject(lambda e:e['GPU_trace'][3]['request'].update(id=999))
 def test_GPU_readback_missing(self):self.reject(lambda e:e['GPU_trace'].pop(4))
 def test_GDI_bitmap_leak(self):self.reject(lambda e:e['GDI'][3].update(bitmaps=1))
 def test_parent_retirement_missing(self):self.reject(lambda e:e['parent_GPU_calls'].pop())
 def test_second_text_extent_wrong(self):self.reject(lambda e:e.update(natural_parent_texture_bytes_retired=57344))
 def test_incomplete_CPU_provenance(self):self.reject(lambda e:e['frames'][3]['steps'][-1].pop('architectural_cpu'))
 def test_font_caller(self):self.gdi_reject('CreateFontA',lambda a:a.update(return_va=0x4ca7cb))
 def test_original_font_weight(self):self.gdi_reject('CreateFontA',lambda a:a['args'].__setitem__(4,700))
 def test_raw_ANSI_text(self):self.gdi_reject('TextOutA',lambda a:a.update(text_hex='41'))
 def test_foreign_measurement_DC(self):self.gdi_reject('GetTextExtentPoint32A',lambda a:a['dc_translated_args'].__setitem__(0,1))
 def test_wrong_source_glyph_geometry(self):self.gpu_reject(0,lambda a:a['args'].__setitem__(1,128))
 def test_wrong_native_owner(self):self.gpu_reject(0,lambda a:a['native_request'].update(pool=0))
 def test_wrong_source_device(self):self.gpu_reject(0,lambda a:a['args'].__setitem__(0,1))
 def test_foreign_COM_method(self):self.gpu_reject(1,lambda a:a.update(target=1))
 def test_partial_descriptor(self):self.gpu_reject(1,lambda a:a['result'].update(hex='00'))
 def test_wrong_lock_flags(self):self.gpu_reject(2,lambda a:a['args'].__setitem__(4,16))
 def test_wrong_locked_pitch(self):self.gpu_reject(2,lambda a:a['result'].update(pitch=514))
 def test_extra_host_memory_output(self):self.gpu_reject(2,lambda a:a['memory_outputs'].append(dict(pointer=v.work.VM+28,hex='00000000')))
 def test_partial_glyph_upload(self):self.gpu_reject(3,lambda a:a.update(uploaded_hex='00'))
 def test_forged_upload_receipt(self):self.gpu_reject(3,lambda a:a['result'].update(uploaded_sha256='0'*64))
 def test_foreign_release_owner(self):self.gpu_reject(25,lambda a:a['args'].__setitem__(0,self.e['textures'][1]['texture']['pointer']))
 def test_nonzero_release(self):self.gpu_reject(25,lambda a:a['result'].update(count=1))
 def test_instruction_digest(self):self.step_reject('frame_0_0x425de0',lambda s:s['result'].update(instruction_sha256='0'*64))
 def test_write_digest(self):self.step_reject('frame_0_0x425de0',lambda s:s['result'].update(write_sha256='0'*64))
 def test_complete_architectural_CPU(self):self.step_reject('frame_0_0x425de0',lambda s:s['architectural_cpu'].update(MXCSR=s['architectural_cpu']['MXCSR']^1))
 def test_complete_memory_hash(self):self.step_reject('frame_0_0x425de0',lambda s:s['full_memory'][-1].update(sha256='0'*64))
 def test_all_queue_heads(self):self.step_reject('frame_0_0x425de0',lambda s:s['queue'].update(head_hex='00'))
 def test_live_queue_arena(self):self.step_reject('frame_0_0x425de0',lambda s:s['queue'].update(arena_hex='00'))
 def test_terminal_decode(self):self.step_reject('frame_221_0x454cf0',lambda s:s['decoded'][0].update(opcode=21))
 def test_source_conversion_bands(self):self.step_reject('frame_2_0x454cf0',lambda s:s['conversions'][1]['rect'].__setitem__(2,1))
 def test_historical_second_text_owner(self):self.step_reject('frame_62_0x454cf0',lambda s:next(a for a in s['result']['api_calls'] if a.get('kind')=='recorded_opening_historical_GPU').update(owner='historical_name4'))
 def test_capture_raw_binding(self):
  b=copy.deepcopy(self.e['bindings'][0]);b['capture']['raw_device_hex']='00'*256
  with self.assertRaises(ValueError):v.binding(isolated(self.binding_seed),b)
 def test_capture_before_image(self):
  b=copy.deepcopy(self.e['bindings'][0]);b['before_hex']='00'
  with self.assertRaises(ValueError):v.binding(isolated(self.binding_seed),b)
 def test_no_derived_keyboard_host_write(self):
  b=copy.deepcopy(self.e['bindings'][0]);b['binding']['pointer']+=256
  with self.assertRaises(ValueError):v.binding(isolated(self.binding_seed),b)
 def test_source_long_glyph_is_tiled(self):
  f=self.e['fonts'][1];cfg=v.geometry(f['raster_record']['measured']);self.assertEqual(cfg['raster_size'],[384,24]);self.assertEqual([self.e['textures'][1][k] for k in ('width','height')],[256,64]);self.assertEqual(len(self.step('frame_2_0x454cf0')['conversions']),2)
 def test_overclaim_rejection(self):
  for key in ('new_OS_input','actual_D3D_draw_or_Present','original_outer_scheduler','historical_heap_restored','R3_complete','R6_complete'):
   r=dict(self.matrix);r[key]=True
   with self.assertRaises(ValueError):v.verify_matrix(r)

if __name__=='__main__':unittest.main()
