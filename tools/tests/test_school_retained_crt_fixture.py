"""Source/CPU/byte corruption rejection and native resource ownership gates."""
import copy,gzip,json,unittest
from pathlib import Path
from tools import school_retained_crt_fixture_verification as proof

class CrtFixtureTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads(gzip.decompress((proof.ROOT/'analysis/school-retained-crt-fixture-v1-20261022.json.gz').read_bytes()))
 def reject(self,edit,full=True):
  r=copy.deepcopy(self.r);edit(r)
  with self.assertRaises((ValueError,RuntimeError,KeyError,IndexError)):(proof.verify if full else proof.protocol)(r)
 def test_00_complete_original_lifecycle(self):
  r=proof.verify(self.r);self.assertEqual((r['original_instructions_replayed'],r['actual_OS_calls'],r['actual_allocations'],r['actual_frees'],r['complete_file_bytes']),(267698,47,3,3,262168));self.assertFalse(r['retained_integration'])
 def test_retained_restore_overclaim(self):self.reject(lambda r:r.update(retained_heap_restored=True),False)
 def test_R3_overclaim(self):self.reject(lambda r:r.update(R3_complete=True),False)
 def test_fixture_input_disguised_as_retained(self):self.reject(lambda r:r['fixture_inputs'].update(kind='retained restoration'),False)
 def test_debug_tracking_disabled(self):self.reject(lambda r:r.update(debug_tracking_enabled=False),False)
 def test_missing_native_close(self):self.reject(lambda r:r['native_trace'].pop(),False)
 def test_forced_process_exit(self):self.reject(lambda r:r.update(helper_exit_code=1),False)
 def test_cleanup_leftover(self):self.reject(lambda r:r['helper_cleanup'].update(allocations=1),False)
 def test_native_reply_failure(self):self.reject(lambda r:r['native_trace'][0]['reply'].update(ok=False),False)
 def test_native_sequence_reordered(self):self.reject(lambda r:r['native_trace'][0]['request'].update(id=2),False)
 def test_missing_original_API(self):self.reject(lambda r:r['steps'][1]['result']['api_calls'].pop(),False)
 def test_fake_helper_source(self):self.reject(lambda r:r['helper_build'].update(source_sha256='0'*64),False)
 def test_source_ledger_overlay(self):self.reject(lambda r:r['fixture_inputs']['overlays'][0].update(hex='01000000'))
 def test_extra_undeclared_overlay(self):self.reject(lambda r:r['fixture_inputs']['overlays'].append(dict(pointer=0x7619c0,hex='00000000')))
 def test_wrong_original_allocator_caller(self):self.reject(lambda r:r['steps'][1]['result']['api_calls'][1].update(return_va=1))
 def test_expired_heap_sent_to_Windows(self):self.reject(lambda r:r['native_trace'][1]['request'].update(heap=r['fixture_inputs']['heap_token_translation']['guest']))
 def test_native_allocation_shortened(self):self.reject(lambda r:r['native_trace'][1]['reply']['result'].update(bytes=32))
 def test_source_instruction_digest(self):self.reject(lambda r:r['steps'][1]['result'].update(instruction_sha256='0'*64))
 def test_source_write_digest(self):self.reject(lambda r:r['steps'][1]['result'].update(write_sha256='0'*64))
 def test_full_memory_corruption(self):self.reject(lambda r:r['steps'][1]['full_memory'][0].update(sha256='0'*64))
 def test_full_CPU_corruption(self):self.reject(lambda r:r['steps'][1]['architectural_cpu'].update(MXCSR=r['steps'][1]['architectural_cpu']['MXCSR']^1))
 def test_header_guard_corruption(self):
  b=bytearray.fromhex(self.r['first_allocation']['raw_hex']);b[28]=0
  with self.assertRaises(ValueError):proof.header(b.hex(),262168,1)
 def test_trailing_guard_corruption(self):
  b=bytearray.fromhex(self.r['first_allocation']['raw_hex']);b[262200]=0
  with self.assertRaises(ValueError):proof.header(b.hex(),262168,1)
 def test_CD_user_fill_corruption(self):
  b=bytearray.fromhex(self.r['first_allocation']['raw_hex']);b[32]=0
  with self.assertRaises(ValueError):proof.header(b.hex(),262168,1)
 def test_previous_node_corruption(self):
  b=self.r['concurrent_allocations'][1]['raw_hex']
  with self.assertRaises(ValueError):proof.header(b,88,2,prev=0)
 def test_counter_corruption(self):self.reject(lambda r:r['steps'][2]['ledger'].update(current=88))
 def test_source_sync_corruption(self):self.reject(lambda r:r['native_trace'][7]['request'].update(hex='00'))
 def test_native_file_read_corruption(self):self.reject(lambda r:r['native_trace'][49]['reply']['result'].update(after_hex='00'))
 def test_native_source_file_wrong_flags(self):self.reject(lambda r:r['native_trace'][43]['request'].update(access=0x40000000))
 def test_DD_free_poison_corruption(self):self.reject(lambda r:r['native_trace'][22]['reply']['result'].update(before_hex='00'))
 def test_unowned_pointer_replay(self):self.reject(lambda r:r['native_trace'][8]['request'].update(pointer=1))
 def test_native_readback_corruption(self):self.reject(lambda r:r['native_trace'][52]['reply']['result'].update(hex='00'))
 def test_unfreed_allocation_history(self):self.reject(lambda r:r['allocation_history'][0].update(freed=False))

class NativeOwnershipTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  r=json.loads(gzip.decompress((proof.ROOT/'analysis/school-retained-crt-fixture-v1-20261022.json.gz').read_bytes()));cls.helper=Path(r['helper_build']['helper_path'])
 def setUp(self):self.live=proof.work.platform.Live(self.helper)
 def tearDown(self):self.assertTrue(self.live.close()['all_owned_resources_released'])
 def refuse(self,op,**args):
  with self.assertRaises(ValueError):self.live.request(op,**args)
 def test_unknown_operation(self):self.refuse('rewrite_game_memory')
 def test_unowned_pointer_free(self):self.refuse('free',heap=self.live.hello['heap'],flags=0,pointer=1)
 def test_unowned_file_handle(self):self.refuse('file_close',handle=1)
 def test_unowned_critical_section(self):self.refuse('enter',critical=1)
 def test_unbalanced_leave(self):self.refuse('leave',critical=self.live.hello['critical'])
 def test_wrong_file_and_write_access(self):
  args=dict(path='data\\adv\\bin\\sc004.bin',access=0x40000000,share=1,security=0,disposition=3,attributes=1,template=0);self.refuse('open',**args);args.update(path='other.bin',access=0x80000000);self.refuse('open',**args)
 def test_locked_heap_bounds_double_free_and_cleanup(self):
  h=self.live.hello;self.live.request('enter',critical=h['critical'])
  try:
   self.refuse('alloc',heap=1,flags=0,bytes=64);self.refuse('alloc',heap=h['heap'],flags=0,bytes=1048577);r=self.live.request('alloc',heap=h['heap'],flags=0,bytes=64);p=r['pointer']
   try:
    self.refuse('close');self.refuse('badread',pointer=p,offset=60,bytes=32);self.refuse('sync',pointer=p,hex='00');self.refuse('free',heap=1,flags=0,pointer=p)
   finally:self.live.request('free',heap=h['heap'],flags=0,pointer=p)
   self.refuse('free',heap=h['heap'],flags=0,pointer=p)
  finally:self.live.request('leave',critical=h['critical'])

if __name__=='__main__':unittest.main()
