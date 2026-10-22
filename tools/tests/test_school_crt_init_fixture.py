"""Observed cold origin, source initialization and native teardown ownership checks."""
import copy,gzip,json,unittest
from pathlib import Path
from tools import school_crt_init_fixture_verification as v

class ColdFixtureTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads(gzip.decompress((v.ROOT/'analysis/school-crt-init-fixture-v2-20261022.json.gz').read_bytes()))
 def reject(self,edit,full=True):
  c=copy.deepcopy(self.r['cases'][0]);edit(c)
  with self.assertRaises((ValueError,KeyError,IndexError,RuntimeError)):(v.verify_case if full else v.protocol)(c)
 def test_00_both_source_initialization_lifecycles(self):
  r=v.verify(self.r);self.assertEqual([(c['original_instructions_replayed'],c['actual_source_OS_calls']) for c in r['cases']],[(268259,58)]*2);self.assertFalse(r['retained_heap_restored'])
 def test_manual_ledger_input(self):self.reject(lambda c:c.update(host_debug_ledger_or_lock_initialization=True),False)
 def test_retained_integration_overclaim(self):self.reject(lambda c:c.update(retained_integration=True),False)
 def test_whole_CRT_startup_overclaim(self):self.reject(lambda c:c.update(full_CRT_startup_replayed=True),False)
 def test_missing_original_teardown(self):self.reject(lambda c:c.update(original_heap_and_lock_teardown_executed=False),False)
 def test_driver_precreated_heap(self):self.reject(lambda c:c['initial_native_hello'].update(heap=1),False)
 def test_driver_precreated_lock(self):self.reject(lambda c:c['initial_native_hello'].update(critical=1),False)
 def test_missing_native_trace(self):self.reject(lambda c:c['native_trace'].pop(),False)
 def test_forced_helper_exit(self):self.reject(lambda c:c.update(helper_exit_code=1),False)
 def test_helper_source_corruption(self):self.reject(lambda c:c['helper_build'].update(source_sha256='0'*64),False)
 def test_cold_data_origin_corruption(self):self.reject(lambda c:c['fixture_inputs'].update(source_data_sha256='0'*64))
 def test_native_probe_pin_corruption(self):self.reject(lambda c:c['fixture_inputs'].update(native_probe_sha256='0'*64))
 def test_cold_initial_full_memory_corruption(self):self.reject(lambda c:c['fixture_inputs']['initial_memory'][0].update(sha256='0'*64))
 def test_source_HeapCreate_wrong_flags(self):self.reject(lambda c:c['native_trace'][0]['request'].update(flags=1))
 def test_source_HeapCreate_caller(self):self.reject(lambda c:c['steps'][0]['result']['api_calls'][0].update(return_va=1))
 def test_fake_heap_identity(self):self.reject(lambda c:c.update(source_heap_created=1))
 def test_changed_version_reply(self):self.reject(lambda c:c['native_trace'][1]['reply']['result'].update(hex='00'))
 def test_unowned_static_lock(self):self.reject(lambda c:c['native_trace'][2]['request'].update(guest=1))
 def test_lock_alias_identity(self):self.reject(lambda c:c['native_trace'][3]['reply']['result'].update(pointer=c['native_trace'][2]['reply']['result']['pointer']))
 def test_source_instruction_hash(self):self.reject(lambda c:c['steps'][0]['result'].update(instruction_sha256='0'*64))
 def test_source_write_hash(self):self.reject(lambda c:c['steps'][1]['result'].update(write_sha256='0'*64))
 def test_source_heap_mode_full_CPU(self):self.reject(lambda c:c['steps'][0]['architectural_cpu'].update(MXCSR=c['steps'][0]['architectural_cpu']['MXCSR']^1))
 def test_file_native_write_corruption(self):self.reject(lambda c:c['file_allocation'].update(file_sha256='0'*64))
 def test_source_delete_native_pointer(self):self.reject(lambda c:c['native_trace'][77]['request'].update(pointer=1))
 def test_source_delete_void_result(self):self.reject(lambda c:c['steps'][9]['result']['api_calls'][0].update(value=1))
 def test_source_heap_destroy_native_handle(self):self.reject(lambda c:c['native_trace'][81]['request'].update(heap=1))
 def test_source_heap_destroy_failure(self):self.reject(lambda c:c['native_trace'][81]['reply']['result'].update(value=0))
 def test_source_teardown_full_memory(self):self.reject(lambda c:c['steps'][10]['full_memory'][0].update(sha256='0'*64))
 def test_source_counter_after_teardown(self):self.reject(lambda c:c['steps'][10]['ledger'].update(current=1))

class InitNativeOwnershipTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  r=json.loads(gzip.decompress((v.ROOT/'analysis/school-crt-init-fixture-v2-20261022.json.gz').read_bytes()));cls.helper=Path(r['cases'][0]['helper_build']['helper_path'])
 def setUp(self):self.live=v.work.platform.Live(self.helper)
 def tearDown(self):self.assertTrue(self.live.close()['all_owned_resources_released'])
 def refuse(self,op,**args):
  with self.assertRaises(ValueError):self.live.request(op,**args)
 def test_no_precreated_resource(self):self.assertEqual((self.live.hello['heap'],self.live.hello['critical']),(0,0))
 def test_initialization_input_gates(self):
  self.refuse('heap_create',flags=1,initial=4096,maximum=0);self.refuse('initialize',guest=1);self.refuse('version',hex='00')
 def test_unowned_and_uninitialized_resource_gates(self):
  self.refuse('delete',guest=0x80a4b0,pointer=1);self.refuse('heap_destroy',heap=1);self.refuse('free',heap=1,flags=0,pointer=1)
 def test_source_objects_cannot_be_cleaned_by_driver(self):
  heap=self.live.request('heap_create',flags=0,initial=4096,maximum=0)['pointer'];critical=self.live.request('initialize',guest=0x80a4b0)['pointer']
  try:
   self.refuse('close');self.refuse('heap_create',flags=0,initial=4096,maximum=0);self.refuse('initialize',guest=0x80a4b0);self.refuse('delete',guest=0x80a4b0,pointer=1);self.refuse('heap_destroy',heap=heap+1)
  finally:
   self.live.request('delete',guest=0x80a4b0,pointer=critical);self.live.request('heap_destroy',heap=heap)
  self.refuse('delete',guest=0x80a4b0,pointer=critical)

if __name__=='__main__':unittest.main()
