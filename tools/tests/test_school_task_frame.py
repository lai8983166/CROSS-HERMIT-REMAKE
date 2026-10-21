import unittest
from tools.school_task_frame import source_contract,ActualIME

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

if __name__=='__main__':unittest.main()
