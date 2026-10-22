"""Reject substituted copies/frees, wrong native contracts and false IMAGE returns."""
import copy,gzip,json,unittest
from tools import school_retained_image_return_verification as v

class ImageReturnTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads(gzip.decompress((v.ROOT/'analysis/school-retained-image-return-v1-20261022.json.gz').read_bytes()))
 def reject(self,edit,full=True):
  c=copy.deepcopy(self.r['cases'][0]);edit(c)
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):(v.verify_case if full else v.protocol)(c)
 def test_00_six_original_IMAGE_returns(self):
  p=v.verify(self.r);self.assertTrue(p['six_original_IMAGE_returns_verified']);self.assertEqual([(c['new_original_IMAGE_instructions'],c['original_memcpy_rows'],c['actual_OS_calls']) for c in p['cases']],[(163326,512,44)]*6);self.assertFalse(p['new_GPU'])
 def test_changed_platform_source_pin(self):
  r=copy.deepcopy(self.r);r['platform_contract']['native_report_sha256']='0'*64
  with self.assertRaises(ValueError):v.verify(r)
 def test_reused_old_heap_claim(self):
  r=dict(self.r,historical_heap_restored=True)
  with self.assertRaises(ValueError):v.verify(r)
 def test_false_new_native_GPU_claim(self):
  r=dict(self.r,new_GPU=True)
  with self.assertRaises(ValueError):v.verify(r)
 def test_false_handler_or_R3_completion(self):
  for k in ('handler_animation_completed','R3_complete','R6_complete'):
   r=dict(self.r);r[k]=True
   with self.assertRaises(ValueError):v.verify(r)
 def test_driver_precreated_heap(self):self.reject(lambda c:c['initial_native_hello'].update(heap=1),False)
 def test_forced_helper_cleanup(self):self.reject(lambda c:c['helper_cleanup'].update(forced_cleanup=True),False)
 def test_unsuccessful_helper_exit(self):self.reject(lambda c:c.update(helper_exit_code=1),False)
 def test_projection_outside_CRT(self):self.reject(lambda c:c['projection']['rows'][0].update(pointer=0x79fc74),False)
 def test_changed_projection_CPU(self):self.reject(lambda c:c['projection']['architectural_cpu'].update(MXCSR=c['projection']['architectural_cpu']['MXCSR']^1))
 def test_changed_parent_source(self):self.reject(lambda c:c['parent_boundary']['source'].update(acceptance_sha256='0'*64))
 def test_false_forward_game_root(self):self.reject(lambda c:c['step'].update(root=dict(va=0x403bd0)),False)
 def test_missing_memcpy_row(self):self.reject(lambda c:c['copy_rows'].pop(),False)
 def test_changed_memcpy_source(self):self.reject(lambda c:c['copy_rows'][300]['args'].__setitem__(1,1))
 def test_changed_memcpy_row_destination(self):self.reject(lambda c:c['copy_rows'][511]['args'].__setitem__(0,1))
 def test_memcpy_original_instruction_body_missing(self):
  def edit(c):c['step']['result']['instruction_counts']=[i for i in c['step']['result']['instruction_counts'] if i['va']!=0x56d4d0]
  self.reject(edit)
 def test_native_CreateTexture_shape(self):self.reject(lambda c:c['step']['result']['api_calls'][0]['args'].__setitem__(1,128))
 def test_wrong_recorded_texture_owner(self):self.reject(lambda c:c['typed_texture_projection'][0].update(domain='other_resource'))
 def test_changed_historical_COM_reply(self):self.reject(lambda c:c['step']['result']['api_calls'][1]['historical_origin']['response'].update(width=1))
 def test_lock_output_buffer_corruption(self):self.reject(lambda c:c['step']['result']['api_calls'][2]['memory_outputs'][0].update(hex='00'))
 def test_original_pixel_corruption(self):
  def edit(c):
   b=bytearray.fromhex(c['after']['pixel_hex']);b[12345]^=1;c['after']['pixel_hex']=b.hex()
  self.reject(edit)
 def test_upload_buffer_corruption(self):self.reject(lambda c:c['step']['result']['api_calls'][3].update(uploaded_hex='00'))
 def test_missing_original_free_API(self):self.reject(lambda c:c['step']['result']['api_calls'].pop())
 def test_original_instruction_hash_corruption(self):self.reject(lambda c:c['step']['result'].update(instruction_sha256='0'*64))
 def test_original_write_hash_corruption(self):self.reject(lambda c:c['step']['result'].update(write_sha256='0'*64))
 def test_full_memory_corruption(self):self.reject(lambda c:c['step']['full_memory'][0].update(sha256='0'*64))
 def test_full_CPU_corruption(self):self.reject(lambda c:c['step']['architectural_cpu'].update(MXCSR=c['step']['architectural_cpu']['MXCSR']^1))
 def test_natural_stack_return_corruption(self):self.reject(lambda c:c['after']['natural_return'].update(sp=1))
 def test_loaded_flag_corruption(self):self.reject(lambda c:c['after'].update(image_loaded_flag='00'))
 def test_original_SEH_restore_corruption(self):self.reject(lambda c:c.update(source_entry_SEH_hex='01000000'))
 def test_vector_CD_padding_corruption(self):
  def edit(c):
   b=bytearray.fromhex(c['after']['record_hex']);b[70]=0;c['after']['record_hex']=b.hex()
  self.reject(edit)
 def test_game_allocation_accounting_corruption(self):self.reject(lambda c:c['step']['ledger'].update(current=262256))
 def test_native_vector_readback_corruption(self):self.reject(lambda c:c['readback']['result'].update(hex='00'))
 def test_wrong_container_cleanup_receiver(self):self.reject(lambda c:c['cleanup']['root'].update(receiver=1))
 def test_cleanup_free_or_destructor_substitute(self):self.reject(lambda c:c['cleanup']['root'].update(va=0x428ad0))
 def test_cleanup_descriptor_reply_corruption(self):self.reject(lambda c:c['cleanup']['result']['api_calls'][0]['result'].update(size=0))
 def test_cleanup_Release_refcount_corruption(self):self.reject(lambda c:c['cleanup']['result']['api_calls'][1].update(value=1))
 def test_unfreed_allocation_history(self):self.reject(lambda c:c['allocation_history'][1].update(freed=False))

if __name__=='__main__':unittest.main()
