import unittest,copy,gzip,json
from tools.school_task_frame import source_contract,ActualIME
from tools.school_task_frame_verification import verify_protocol,ROOT

class InputSourceTests(unittest.TestCase):
 def test_source_proves_pending_request_and_original_frame_order(self):
  c=source_contract();self.assertEqual(c['import_slot'],0x5920ec);self.assertEqual(c['request_flag_offset'],0x630)
  self.assertEqual(c['symbol'],'ImmGetOpenStatus');self.assertFalse(c['full_outer_thread_scheduler_executed'])
 def test_real_null_context_query_records_observed_API_and_loaded_module(self):
  p=ActualIME();r=p.query(0)
  self.assertTrue(r['actual_OS_observed']);self.assertEqual(r['result'],0);self.assertEqual(len(p.trace),1);self.assertEqual(len(p.identity['sha256']),64)
 def test_unknown_context_never_reaches_actual_API(self):
  p=ActualIME()
  for bad in (1,-1,0x12345678,None,False):
   with self.assertRaises(ValueError):p.query(bad)
  self.assertEqual(p.trace,[])

class CompleteTaskProtocolTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.case=json.loads(gzip.decompress((ROOT/'analysis/school-task-frame-initial-v1-20261021.json.gz').read_bytes()))['case']
 def test_67_real_requests_and_complete_tasks_replace_VM_roots(self):
  self.assertEqual(verify_protocol(self.case),dict(full_original_tasks=67,actual_IME_queries=67))
 def test_unconsumed_request_is_rejected(self):
  c=copy.deepcopy(self.case);c['frames'][10]['flag_after_original_reset']=255
  with self.assertRaisesRegex(ValueError,'natural pending request'):verify_protocol(c)
 def test_shortcut_VM_root_is_rejected(self):
  c=copy.deepcopy(self.case);s=next(s for s in c['steps'] if s['label'].startswith('complete_original_task_'));s['root']['va']=0x4ce8f0
  with self.assertRaisesRegex(ValueError,'complete tasks replace'):verify_protocol(c)
 def test_changed_actual_IME_result_is_rejected(self):
  c=copy.deepcopy(self.case);c['actual_IME_trace'][0]=dict(c['actual_IME_trace'][0],result=1)
  with self.assertRaisesRegex(ValueError,'all observed IMM calls'):verify_protocol(c)
 def test_omitted_original_task_epilogue_is_rejected(self):
  c=copy.deepcopy(self.case);s=next(s for s in c['steps'] if s['label'].startswith('complete_original_task_'));s['result']['instruction_counts']=[r for r in s['result']['instruction_counts'] if r['va']!=0x454ec1]
  with self.assertRaisesRegex(ValueError,'complete task/VM'):verify_protocol(c)

if __name__=='__main__':unittest.main()
