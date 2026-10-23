"""Original third text, exact GDI/COM contracts, source state and cleanup gates."""
import copy,gzip,json,unittest
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
from tools import school_retained_third_dialogue_verification as v

def clone(seed):
 r=copy.copy(seed);r.u=Uc(UC_ARCH_X86,UC_MODE_32)
 for p,end,_ in seed.u.mem_regions():r.u.mem_map(p,end-p+1);r.u.mem_write(p,bytes(seed.u.mem_read(p,end-p+1)))
 r.u.context_restore(seed.u.context_save());r.task_code=dict(seed.task_code);r.region_hashes=dict(seed.region_hashes);return r

class ThirdDialogueTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.path=v.ROOT/'analysis/school-retained-third-dialogue-v1-20261023.json.gz';cls.r=json.loads(gzip.decompress(cls.path.read_bytes()));cls.c=cls.r['cases'][0];cls.e=cls.c['third_dialogue'];cls.seed=v.prepare_boundary(cls.c);cls.raster=clone(cls.seed);cls.raster.replay_new(cls.e['raster_step'])
 def reject(self,edit):
  c=copy.deepcopy(self.c);edit(c['third_dialogue'])
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):v.protocol(c)
 def step_reject(self,edit,completion=False):
  r=clone(self.raster if completion else self.seed);s=copy.deepcopy(self.e['completion' if completion else 'raster_step']);edit(s)
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):r.replay_new(s)
 def api_reject(self,name,edit,completion=False):
  def change(s):edit(next(a for a in s['result']['api_calls'] if a.get('name')==name))
  self.step_reject(change,completion)
 def com_reject(self,index,edit):
  def change(s):edit([a for a in s['result']['api_calls'] if a['kind']=='recorded_third_GPU_only'][index])
  self.step_reject(change,True)
 def test_00_full_original_case_and_bound_six_case_proof(self):
  proof=json.loads((v.ROOT/'analysis/school-retained-third-dialogue-proof-v1-20261023.json').read_bytes());self.assertEqual(proof['source_report_sha256'],v.sha(self.path.read_bytes()));self.assertTrue(proof['six_original_third_dialogues_verified']);self.assertEqual(len(proof['cases']),6);self.assertTrue(all(c['third']['final_PC']==290 and c['third']['original_readiness_updates']==26 for c in proof['cases']));self.assertEqual(v.verify_case(self.c)['third']['new_original_forward_instructions'],1408112)
 def test_independent_VM_root(self):self.reject(lambda e:e['frames'][0]['steps'][-1]['root'].update(va=0x4ce8f0))
 def test_new_font_continuation_root(self):self.reject(lambda e:e['raster_step'].update(root=dict(va=0x4cabd0)))
 def test_new_texture_continuation_root(self):self.reject(lambda e:e['completion'].update(root=dict(va=0x403bd0)))
 def test_missing_readiness_update(self):self.reject(lambda e:e['frames'].pop(14))
 def test_missing_queue_reset(self):self.reject(lambda e:e['frames'][1]['steps'].pop(1))
 def test_early_wait_release(self):self.reject(lambda e:e['frames'][24]['state']['animation'].update(wait=0))
 def test_wait_counter_reset(self):self.reject(lambda e:e['frames'][25]['state']['animation'].update(waiting_count=0))
 def test_readiness_predicate_omitted(self):self.reject(lambda e:next(r for r in e['frames'][1]['steps'][-1]['result']['instruction_counts'] if r['va']==0x4cb5f0).update(count=9))
 def test_mouse_query_body_omitted(self):self.reject(lambda e:next(r for r in e['frames'][1]['steps'][-1]['result']['instruction_counts'] if r['va']==0x4d5ec0).update(count=0))
 def test_host_input_reset(self):self.reject(lambda e:e.update(retained_input_host_writes=1))
 def test_changed_retained_input(self):self.reject(lambda e:e['before'].update(input_words=[0,1,0]))
 def test_missing_font_source_CPU(self):self.reject(lambda e:e['entry']['cpu'].update(EIP=0x4cabd0))
 def test_font_weight_from_other_text(self):self.reject(lambda e:e['entry']['font_args'].__setitem__(4,700))
 def test_historical_source_pin(self):self.reject(lambda e:e['contract'].update(native_report_sha256='0'*64))
 def test_incomplete_native_font_cleanup(self):self.reject(lambda e:e['offscreen_cleanup'].update(fonts=1))
 def test_original_texture_cleanup_root(self):self.reject(lambda e:e['cleanup']['root'].update(va=0x41f4e0))
 def test_next_confirmation_claim(self):self.reject(lambda e:e['final']['animation'].update(pc=294))
 def test_missing_queue_evidence(self):self.reject(lambda e:e['raster_step'].pop('queue'))
 def test_actual_font_arguments(self):self.api_reject('CreateFontA',lambda a:a['args'].__setitem__(4,700))
 def test_actual_font_face(self):self.api_reject('CreateFontA',lambda a:a.update(face_hex='41'))
 def test_font_handle_result(self):self.api_reject('CreateFontA',lambda a:a.update(result=1))
 def test_GDI_target_rebound(self):self.api_reject('CreateFontA',lambda a:a.update(target=a['target']+4))
 def test_old_DC_sent_to_Windows(self):self.api_reject('GetTextExtentPoint32A',lambda a:a['dc_translated_args'].__setitem__(0,a['args'][0]))
 def test_measurement_result(self):self.api_reject('GetTextExtentPoint32A',lambda a:a.update(measured=[1,20]))
 def test_wrong_source_DIB(self):self.api_reject('CreateDIBSection',lambda a:a.update(header_hex='00'))
 def test_DIB_output_into_game_state(self):self.api_reject('CreateDIBSection',lambda a:a['memory_outputs'].append(dict(pointer=v.base.VM+28,hex='00000000')))
 def test_actual_glyph_output(self):self.api_reject('TextOutA',lambda a:a['memory_outputs'][0].update(hex='00'))
 def test_GDI_state_return(self):self.api_reject('SetBkMode',lambda a:a.update(result=1))
 def test_full_CPU_corruption(self):self.step_reject(lambda s:s['architectural_cpu'].update(MXCSR=s['architectural_cpu']['MXCSR']^1))
 def test_full_mapping_digest(self):self.step_reject(lambda s:s['full_memory'][-1].update(sha256='0'*64))
 def test_original_instruction_digest(self):self.step_reject(lambda s:s['result'].update(instruction_sha256='0'*64))
 def test_original_write_digest(self):self.step_reject(lambda s:s['result'].update(write_sha256='0'*64))
 def test_complete_queue_heads(self):self.step_reject(lambda s:s['queue'].update(head_hex='00'))
 def test_complete_queue_records(self):self.step_reject(lambda s:s['queue'].update(arena_hex='00'))
 def test_COM_response_failure(self):self.com_reject(0,lambda a:a.update(value=1))
 def test_COM_method_owner(self):self.com_reject(0,lambda a:a['args'].__setitem__(0,1))
 def test_COM_descriptor(self):self.com_reject(1,lambda a:a['result'].update(hex='00'))
 def test_COM_lock_pitch(self):self.com_reject(2,lambda a:a['result'].update(pitch=514))
 def test_COM_expired_native_pointer(self):self.com_reject(2,lambda a:a['result'].update(bits=1))
 def test_COM_converted_pixel_hash(self):self.com_reject(3,lambda a:a['result'].update(uploaded_sha256='0'*64))
 def test_source_conversion_rect(self):self.step_reject(lambda s:s['conversions'][0]['rect'].__setitem__(0,1),True)
 def test_original_bitmap_deletion(self):self.api_reject('DeleteObject',lambda a:a['args'].__setitem__(0,1),True)
 def test_original_DC_deletion_result(self):self.api_reject('DeleteDC',lambda a:a.update(result=0),True)
 def test_original_source_byte(self):
  r=clone(self.seed);r.u.mem_write(0x4cad09,bytes([0x90]))
  with self.assertRaises(ValueError):r.replay_new(self.e['raster_step'])
 def test_independent_pixel_stage(self):
  c=copy.deepcopy(self.c);c['third_dialogue']['raster']['stages'][1]['hex']='00'
  with self.assertRaises(ValueError):v.reproduce_pixels(c)
 def test_independent_native_metrics(self):
  c=copy.deepcopy(self.c);c['third_dialogue']['raster']['measured']=[1,20]
  with self.assertRaises(ValueError):v.reproduce_pixels(c)
 def test_overclaims(self):
  for k in ('new_OS_input','new_window','new_GPU','original_outer_scheduler','historical_heap_restored','new_GPU_draw_or_Present','R3_complete','R6_complete'):
   r=dict(self.r);r[k]=True
   with self.assertRaises(ValueError):v.verify(r)
 def test_no_fresh_font(self):
  r=dict(self.r);r['third_font_created']=False
  with self.assertRaises(ValueError):v.verify(r)

if __name__=='__main__':unittest.main()
