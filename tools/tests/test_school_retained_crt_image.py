"""Retained CRT projection, real IMAGE ownership and corruption rejection."""
import copy,gzip,json,unittest
from tools import school_retained_crt_image_verification as v

class RetainedImageTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads(gzip.decompress((v.ROOT/'analysis/school-retained-crt-image-v3-20261022.json.gz').read_bytes()))
 def reject(self,edit,full=True):
  c=copy.deepcopy(self.r['cases'][0]);edit(c)
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):(v.verify_case if full else v.protocol)(c)
 def test_00_six_continuous_original_prefixes(self):
  proof=v.verify(self.r);self.assertEqual(len(proof['cases']),6);self.assertTrue(proof['six_continuous_original_IMAGE_prefixes_verified']);self.assertFalse(proof['historical_heap_restored']);self.assertTrue(all(c['full_file_bytes']==262168 and c['vector_bytes']==88 and c['normal_native_cleanup'] for c in proof['cases']))
 def test_cpu_projection_corruption(self):self.reject(lambda c:c['projection']['architectural_cpu'].update(MXCSR=c['projection']['architectural_cpu']['MXCSR']^1))
 def test_projection_source_byte_corruption(self):self.reject(lambda c:c['projection']['rows'][0].update(source_hex='00'*15))
 def test_projection_before_byte_corruption(self):self.reject(lambda c:c['projection']['rows'][0].update(before_hex='00'*15))
 def test_projection_range_expansion(self):self.reject(lambda c:c['projection']['rows'][0].update(bytes=16),False)
 def test_game_accounting_reset_claim(self):self.reject(lambda c:c['projection'].update(game_accounting_reset=True),False)
 def test_old_heap_restore_claim(self):self.reject(lambda c:c['projection'].update(historical_heap_restored=True),False)
 def test_unrelated_retained_memory_corruption(self):self.reject(lambda c:c['projection']['full_memory'][0].update(sha256='0'*64))
 def test_retained_game_accounting_corruption(self):self.reject(lambda c:c.update(game_accounting_baseline=c['game_accounting_baseline']+1))
 def test_source_cold_origin_corruption(self):self.reject(lambda c:c['fixture_inputs'].update(source_data_sha256='0'*64))
 def test_no_legacy_heap_adoption(self):
  g=v.work.Guest.__new__(v.work.Guest);g.allocations={}
  for p in (0x4d605b8,0x4d68fa0,0x4d60000):
   with self.assertRaises(ValueError):g.owned(p)
 def test_driver_precreated_heap(self):self.reject(lambda c:c['initial_native_hello'].update(heap=1),False)
 def test_driver_precreated_lock(self):self.reject(lambda c:c['initial_native_hello'].update(critical=1),False)
 def test_helper_source_corruption(self):self.reject(lambda c:c['helper_build'].update(source_sha256='0'*64),False)
 def test_native_wire_sequence_corruption(self):self.reject(lambda c:c['native_trace'][0]['request'].update(id=2),False)
 def test_original_heap_create_flags(self):self.reject(lambda c:c['native_trace'][0]['request'].update(flags=1))
 def test_native_heap_identity_corruption(self):self.reject(lambda c:c.update(source_heap_created=1))
 def test_original_file_open_flags(self):self.reject(lambda c:next(a for a in c['step']['api_calls'] if a['name']=='CreateFileA')['args'].__setitem__(1,0))
 def test_original_ReadFile_caller(self):self.reject(lambda c:next(a for a in c['step']['api_calls'] if a['name']=='ReadFile').update(return_va=1))
 def test_native_file_content_corruption(self):
  def edit(c):
   r=next(t['reply']['result'] for t in c['native_trace'] if t['request']['op']=='read');b=bytearray.fromhex(r['after_hex']);b[100]^=1;r['after_hex']=b.hex()
  self.reject(edit)
 def test_missing_original_file_close(self):self.reject(lambda c:c['step']['api_calls'].__delitem__(7))
 def test_original_instruction_corruption(self):self.reject(lambda c:c['step'].update(instruction_sha256='0'*64))
 def test_original_write_corruption(self):self.reject(lambda c:c['step'].update(write_sha256='0'*64))
 def test_complete_CPU_corruption(self):self.reject(lambda c:c['step']['architectural_cpu'].update(MXCSR=c['step']['architectural_cpu']['MXCSR']^1))
 def test_complete_memory_corruption(self):self.reject(lambda c:c['step']['full_memory'][0].update(sha256='0'*64))
 def test_debug_list_corruption(self):self.reject(lambda c:c['step']['ledger'].update(last=0))
 def test_vector_padding_cannot_be_zeroed(self):
  def edit(c):
   b=bytearray.fromhex(c['boundary']['record_hex']);b[70:72]=bytes(2);c['boundary']['record_hex']=b.hex()
  self.reject(edit)
 def test_natural_frame_corruption(self):self.reject(lambda c:c['boundary']['pending_texture']['frames'][0].update(return_va=1))
 def test_texture_entry_unexecuted(self):self.reject(lambda c:c['boundary']['pending_texture'].update(first_instruction_executed=True))
 def test_full_native_readback_corruption(self):self.reject(lambda c:c['readbacks'][0]['result'].update(hex='00'))
 def test_cleanup_must_use_original_free(self):self.reject(lambda c:c['steps'][2]['root'].update(va=0x428a40))
 def test_forced_cleanup_rejected(self):self.reject(lambda c:c['helper_cleanup'].update(forced_cleanup=True),False)
 def test_nonzero_helper_exit_rejected(self):self.reject(lambda c:c.update(helper_exit_code=1),False)
 def test_mainline_scope_overclaims(self):
  for k in ('historical_heap_restored','new_GPU','image_loader_completed','same_native_lifetime','R3_complete','R6_complete'):
   r=dict(self.r);r[k]=True
   with self.assertRaises(ValueError):v.verify(r)

if __name__=='__main__':unittest.main()
