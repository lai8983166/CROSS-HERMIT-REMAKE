"""Captured input, original confirmation tasks, fourth raster and source cleanup."""
import copy,gzip,json,unittest
from tools import school_retained_third_confirmation_verification as v
from tools.tests.test_school_retained_third_dialogue import clone

class ThirdConfirmationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.path=v.ROOT/'analysis/school-retained-third-confirmation-v1-20261023.json.gz';cls.r=json.loads(gzip.decompress(cls.path.read_bytes()));cls.c=cls.r['cases'][0];cls.e=cls.c['third_confirmation'];seeds=[];cls.verified=v.verify_case(cls.c,lambda r:seeds.append(clone(r)));cls.seed=seeds[0];cls.seed.confirmation_case=cls.e;cls.seed.fourth_reference=v.reproduce_pixels(cls.c);cls.seed.existing_gpu_count=0
  cls.font=clone(cls.seed);r=cls.font;e=cls.e;r.capture_step(e['bindings'][0]);r.next_frame(e['enter'])
  for f in e['controls']:r.next_frame(f)
  r.capture_step(e['bindings'][1]);r.next_frame(e['confirmed']);r.capture_step(e['bindings'][2]);r.next_frame(e['activation']);r.next_frame(e['clearing']);r.next_frame(e['prefix'],True)
 def reject(self,edit):
  c=copy.deepcopy(self.c);edit(c['third_confirmation'])
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):v.protocol(c)
 def raster_reject(self,edit):
  r=clone(self.font);s=copy.deepcopy(self.e['raster_step']);edit(s)
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):r.next_step(s)
 def api_reject(self,name,edit):self.raster_reject(lambda s:edit(next(a for a in s['result']['api_calls'] if a.get('name')==name)))
 def old_gpu_reject(self,index,edit):self.raster_reject(lambda s:edit([a for a in s['result']['api_calls'] if a['kind']=='recorded_replaced_text_GPU'][index]))
 def test_00_all_six_proofs_and_whole_case(self):
  p=json.loads((v.ROOT/'analysis/school-retained-third-confirmation-proof-v1-20261023.json').read_bytes());self.assertEqual(p['source_report_sha256'],v.sha(self.path.read_bytes()));self.assertTrue(p['six_captured_third_confirmations_and_fourth_rasters_verified']);self.assertEqual(len(p['cases']),6);self.assertEqual(self.verified['confirmation']['new_original_instructions'],338281);self.assertTrue(all(c['confirmation']['final_PC']==306 and c['confirmation']['selected_layer']==7 for c in p['cases']))
 def test_source_capture_pin(self):self.reject(lambda e:e['contract'].update(parent_acceptance_sha256='0'*64))
 def test_source_command_bytes(self):self.reject(lambda e:e['contract']['commands'][2].update(hex='00'))
 def test_source_capture_order(self):self.reject(lambda e:e['bindings'].reverse())
 def test_source_device_bytes(self):self.reject(lambda e:e['bindings'][1]['capture'].update(raw_device_hex='00'*256))
 def test_derived_keyboard_host_write(self):self.reject(lambda e:e.update(derived_input_host_writes=1))
 def test_PC_wait_host_write(self):self.reject(lambda e:e.update(PC_or_wait_host_writes=1))
 def test_raw_binding_destination(self):self.reject(lambda e:e['bindings'][1]['binding'].update(pointer=v.work.KEYBOARD+0x480))
 def test_raw_binding_extent(self):self.reject(lambda e:e['bindings'][1]['binding'].update(bytes=257))
 def test_non_raw_binding_byte(self):self.reject(lambda e:e['bindings'][1].update(bound_hex='00'*0xa00))
 def test_normalized_keyboard_forged(self):self.reject(lambda e:e['bindings'][1].update(after_hex='00'*0xa00))
 def test_source_fragment_entry(self):self.reject(lambda e:e['bindings'][1]['fragment'].update(va=0x4113d6))
 def test_source_fragment_receiver(self):self.reject(lambda e:e['bindings'][1]['fragment'].update(receiver=1))
 def test_source_fragment_stack(self):self.reject(lambda e:e['bindings'][1]['fragment'].update(sp=1))
 def test_keyboard_new_root(self):self.reject(lambda e:e['bindings'][1]['step'].update(root=dict(va=0x4113d5)))
 def test_down_bit_is_not_boolean(self):self.reject(lambda e:e['confirmed']['state'].update(space_current=1))
 def test_missing_no_input_control(self):self.reject(lambda e:e['controls'].pop())
 def test_early_no_input_wait_release(self):self.reject(lambda e:e['controls'][1]['state'].update(wait=0))
 def test_confirmation_still_waiting(self):self.reject(lambda e:e['confirmed']['state'].update(wait=1))
 def test_missing_queue_reset(self):self.reject(lambda e:e['enter']['steps'].pop(1))
 def test_independent_VM_root(self):self.reject(lambda e:e['activation']['steps'][-1]['root'].update(va=0x4ce8f0))
 def test_wrong_layer_from_config4(self):self.reject(lambda e:e['activation']['state'].update(selected_layer=4))
 def test_wrong_clear_opcode(self):self.reject(lambda e:e['clearing']['state'].update(opcode=43))
 def test_fourth_text_not_cleared(self):self.reject(lambda e:e['clearing']['state'].update(fourth_text_count=2))
 def test_fourth_task_falsely_complete(self):self.reject(lambda e:e.update(fourth_task_completed=True))
 def test_fourth_texture_falsely_created(self):self.reject(lambda e:e.update(texture_create_executed=True))
 def test_fourth_font_new_game_root(self):self.reject(lambda e:e['raster_step'].update(root=dict(va=0x4cabd0)))
 def test_texture_entry_executed(self):self.reject(lambda e:e['pending_texture'].update(first_instruction_executed=True))
 def test_pending_font_entry_executed(self):self.reject(lambda e:e['pending_font'].update(first_instruction_executed=True))
 def test_ownership_cleanup(self):self.reject(lambda e:e['supplemental_GDI_cleanup'].update(dcs=1))
 def test_old_first_texture_identity(self):self.reject(lambda e:e['existing_resource']['texture'].update(pointer=1))
 def test_old_counter_reset(self):self.reject(lambda e:e.update(accounting_after=e['accounting_before']))
 def test_wrong_old_texture_byte_size(self):self.reject(lambda e:e.update(replaced_texture_bytes=32768))
 def test_queue_evidence_missing(self):self.reject(lambda e:e['raster_step'].pop('queue'))
 def test_fresh_font_ABI(self):self.api_reject('CreateFontA',lambda a:a['args'].__setitem__(4,700))
 def test_fresh_font_face(self):self.api_reject('CreateFontA',lambda a:a.update(face_hex='41'))
 def test_old_measurement_DC(self):self.api_reject('GetTextExtentPoint32A',lambda a:a['dc_translated_args'].__setitem__(0,a['args'][0]))
 def test_DIB_forged_mapping(self):self.api_reject('CreateDIBSection',lambda a:a['new_mappings'][0].update(pointer=v.work.VM))
 def test_DIB_output_in_game_PC(self):self.api_reject('CreateDIBSection',lambda a:a['memory_outputs'].append(dict(pointer=v.work.VM+28,hex='00000000')))
 def test_fresh_glyph_bytes(self):self.api_reject('TextOutA',lambda a:a['memory_outputs'][0].update(hex='00'))
 def test_old_descriptor_bytes(self):self.old_gpu_reject(0,lambda a:a['result'].update(hex='00'))
 def test_old_descriptor_wrong_object(self):self.old_gpu_reject(0,lambda a:a['args'].__setitem__(0,1))
 def test_old_Release_reference_count(self):self.old_gpu_reject(1,lambda a:a['result'].update(count=1))
 def test_old_Release_memory_output(self):self.old_gpu_reject(1,lambda a:a['memory_outputs'].append(dict(pointer=0x765720,hex='00000000')))
 def test_game_function_substitute(self):self.raster_reject(lambda s:s['result']['api_calls'][0].update(kind='game_stub'))
 def test_all_CPU_registers(self):self.raster_reject(lambda s:s['architectural_cpu'].update(MXCSR=s['architectural_cpu']['MXCSR']^1))
 def test_all_memory_digest(self):self.raster_reject(lambda s:s['full_memory'][-1].update(sha256='0'*64))
 def test_instruction_digest(self):self.raster_reject(lambda s:s['result'].update(instruction_sha256='0'*64))
 def test_write_digest(self):self.raster_reject(lambda s:s['result'].update(write_sha256='0'*64))
 def test_queue_heads(self):self.raster_reject(lambda s:s['queue'].update(head_hex='00'))
 def test_queue_live_records(self):self.raster_reject(lambda s:s['queue'].update(arena_hex='00'))
 def test_original_instruction_byte(self):
  r=clone(self.font);r.u.mem_write(0x4cad09,b'\x90')
  with self.assertRaises(ValueError):r.next_step(self.e['raster_step'])
 def test_fresh_pixel_stage(self):
  c=copy.deepcopy(self.c);c['third_confirmation']['raster']['stages'][1]['hex']='00'
  with self.assertRaises(ValueError):v.reproduce_pixels(c)
 def test_independent_fourth_metrics(self):
  c=copy.deepcopy(self.c);c['third_confirmation']['raster']['measured']=[1,20]
  with self.assertRaises(ValueError):v.reproduce_pixels(c)
 def test_overclaims(self):
  for k in ('new_OS_input','new_window','new_GPU','original_outer_scheduler','historical_heap_restored','fourth_texture_created','fourth_task_completed','R3_complete','R6_complete'):
   r=dict(self.r);r[k]=True
   with self.assertRaises(ValueError):v.verify(r)
 def test_no_fresh_font(self):
  r=dict(self.r);r['fourth_font_created']=False
  with self.assertRaises(ValueError):v.verify(r)

if __name__=='__main__':unittest.main()
