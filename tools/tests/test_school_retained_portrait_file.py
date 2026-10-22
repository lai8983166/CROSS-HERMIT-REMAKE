"""Original source replay, recorded platform rebasing and actual file ownership."""
import copy,gzip,json,unittest
from tools import school_retained_portrait_file_verification as proof


class FileHandoffTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.report=json.loads(gzip.decompress((proof.ROOT/'analysis/school-retained-portrait-file-v2-20261022.json.gz').read_bytes()))
 def reject(self,edit):
  c=copy.deepcopy(self.report['cases'][-1]);edit(c)
  with self.assertRaises((ValueError,RuntimeError,KeyError)):proof.verify_case(c)
 def test_00_all_six_protocols_and_last_complete_source_replay(self):
  self.assertEqual(len(self.report['cases']),6)
  for c in self.report['cases']:proof.protocol(c)
  c=proof.verify_case(self.report['cases'][-1]);self.assertEqual((c['recorded_GPU_calls'],c['recorded_GDI_cleanup_calls'],c['actual_read_only_file_APIs'],c['converted_texture_bytes'],c['natural_allocation_frames'],c['allocation_bytes']),(4,4,3,8192,8,262168));self.assertFalse(c['allocator_executed'])
 def test_added_game_root(self):self.reject(lambda c:c['steps'][0].update(root=dict(va=0x403bd0)))
 def test_IAT_rebinding_claim(self):self.reject(lambda c:c['steps'][0].update(IAT_unchanged=False))
 def test_changed_typed_identity(self):self.reject(lambda c:c['typed_projection'][0].update(guest=1))
 def test_forged_GPU_response(self):self.reject(lambda c:c['steps'][0]['api_calls'][0]['result'].update(hr=1))
 def test_wrong_source_GPU_caller(self):self.reject(lambda c:c['steps'][0]['api_calls'][0].update(return_va=1))
 def test_changed_locked_pixels(self):self.reject(lambda c:c['steps'][0]['api_calls'][2]['memory_outputs'][0].update(hex='00'))
 def test_changed_GDI_object_role(self):self.reject(lambda c:c['steps'][0]['api_calls'][4]['args'].__setitem__(0,0))
 def test_wrong_file_open_flags(self):self.reject(lambda c:c['steps'][1]['api_calls'][1]['args'].__setitem__(1,0x40000000))
 def test_wrong_native_file_path(self):self.reject(lambda c:c['steps'][1]['api_calls'][1].update(native_absolute_read_only_path='elsewhere.bin'))
 def test_wrong_file_size_result(self):self.reject(lambda c:c['steps'][1]['api_calls'][2].update(value=0))
 def test_zero_actual_handle(self):self.reject(lambda c:c.update(actual_open_files_at_boundary=[0]))
 def test_unclosed_actual_file(self):self.reject(lambda c:c['file_cleanup'].update(open_handles=1))
 def test_close_not_verified_invalid(self):self.reject(lambda c:c['file_cleanup']['invalid_handle_checks'][0].update(result=1,error=0))
 def test_changed_allocation_count(self):self.reject(lambda c:c['pending_allocation'].update(args=[1]))
 def test_changed_outer_task_stack(self):self.reject(lambda c:c['pending_allocation']['frames'][-1].update(return_va=1))
 def test_changed_complete_CPU(self):self.reject(lambda c:c['final_architectural_cpu'].update(MXCSR=c['final_architectural_cpu']['MXCSR']^1))
 def test_changed_complete_memory(self):self.reject(lambda c:c['final_memory'][0].update(sha256='0'*64))
 def test_changed_source_instruction_digest(self):self.reject(lambda c:c['steps'][0].update(instruction_sha256='0'*64))
 def test_changed_complete_write_digest(self):self.reject(lambda c:c['steps'][0].update(write_sha256='0'*64))
 def test_claim_unexecuted_allocator_executed(self):self.reject(lambda c:c['pending_allocation'].update(first_instruction_executed=True))
 def test_missing_platform_call(self):self.reject(lambda c:c['steps'][0]['api_calls'].pop())
 def test_bad_final_pixel_hash(self):self.reject(lambda c:c.update(converted_texture_sha256='0'*64))
 def test_no_fresh_GPU_overclaim(self):
  r=copy.deepcopy(self.report);r['new_GPU']=True
  with self.assertRaisesRegex(ValueError,'honest allocation'):proof.verify(r)
 def test_no_original_ReadFile_overclaim(self):
  r=copy.deepcopy(self.report);r['original_ReadFile_executed']=True
  with self.assertRaisesRegex(ValueError,'honest allocation'):proof.verify(r)
 def test_no_completed_image_loader_overclaim(self):
  r=copy.deepcopy(self.report);r['image_loader_completed']=True
  with self.assertRaisesRegex(ValueError,'honest allocation'):proof.verify(r)
 def test_actual_file_probe_close_and_invalid_handle(self):
  f=proof.work.Files()
  try:h=f.open([0x80000000,1,0,3,1,0]);self.assertEqual(f.size(h),262168)
  finally:cleanup=f.close_checked()
  self.assertEqual(cleanup['invalid_handle_checks'],[dict(handle=h,result=0,error=6)]);self.assertTrue(cleanup['all_owned_files_closed'])
 def test_file_service_rejects_non_read_only_flags(self):
  f=proof.work.Files()
  try:
   with self.assertRaisesRegex(ValueError,'read-only'):f.open([0x40000000,1,0,3,1,0])
  finally:self.assertTrue(f.close_checked()['all_owned_files_closed'])


if __name__=='__main__':unittest.main()
