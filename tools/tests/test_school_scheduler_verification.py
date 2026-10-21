"""Reject plausible but incorrect native scheduler/lifetime evidence."""
import copy,json,unittest
from tools.school_scheduler_lifetime_verification import ROOT,SOURCE,verify_report,verify_probe,verify_lifecycle

class SchedulerEvidenceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.report=json.loads((ROOT/'analysis/school-scheduler-lifetime-native-v2-20261021.json').read_text(encoding='utf8'));cls.raw=SOURCE.read_bytes()
 def probe(self,index=1):return copy.deepcopy(self.report['cases'][index]['native_scheduler_probe'])
 def reject(self,p,pattern):
  with self.assertRaisesRegex(ValueError,pattern):verify_probe(p,self.raw)
 def test_all_native_cases_and_normal_original_lifetimes(self):
  r=verify_report(self.report);self.assertEqual(sum(c['scheduler']['actual_CRT_workers'] for c in r['cases']),7);self.assertFalse(r['R3_complete'])
 def test_dirty_guard_write_is_rejected(self):
  p=self.probe();s=p['stages'][-1];b=bytearray.fromhex(s['nodes'][0]['hex']);b[127]^=1;s['nodes'][0]['hex']=b.hex();self.reject(p,'full manager/node/guard')
 def test_manager_guard_write_is_rejected(self):
  p=self.probe();s=p['stages'][2];b=bytearray.fromhex(s['manager_hex']);b[511]^=1;s['manager_hex']=b.hex();self.reject(p,'full manager/node/guard')
 def test_stale_link_in_removed_node_must_not_be_cleared(self):
  p=self.probe();s=next(s for s in p['stages'] if s['label']=='first_original_dispatch');b=bytearray.fromhex(s['nodes'][0]['hex']);b[12:16]=bytes(4);s['nodes'][0]['hex']=b.hex();self.reject(p,'full manager/node/guard')
 def test_disabled_node_must_remain_untouched(self):
  p=self.probe();s=next(s for s in p['stages'] if s['label']=='first_original_dispatch');b=bytearray.fromhex(s['nodes'][1]['hex']);b[4:8]=bytes(4);s['nodes'][1]['hex']=b.hex();self.reject(p,'full manager/node/guard')
 def test_worker_exit_and_handle_association_are_required(self):
  for key,value in [('exit_code',259),('wait_status',258),('handle',1),('thread_id',0)]:
   with self.subTest(key=key):
    p=self.probe();p['worker_threads'][0][key]=value;self.reject(p,'actual original CRT workers')
 def test_closed_event_is_an_actual_invalid_handle_observation(self):
  p=self.probe();p['closed_events'][0]['duplicate_succeeded']=True;self.reject(p,'actual closed source event')
 def test_supplemental_thread_close_cannot_be_omitted(self):
  p=self.probe();p['calls']=[c for c in p['calls'] if c['label']!='supplemental_CloseHandle'];self.reject(p,'exact original call order')
 def test_unbalanced_real_stack_is_rejected(self):
  p=self.probe();b=bytearray.fromhex(p['calls'][0]['parameter_after_hex']);b[36]^=4;p['calls'][0]['parameter_after_hex']=b.hex();self.reject(p,'actual call thread completion/ESP')
 def test_changed_IAT_and_original_code_are_rejected(self):
  for key in ['IAT','code']:
   with self.subTest(key=key):
    p=self.probe();p['source_after'][key].pop();self.reject(p,'before/after full code')
 def test_unrecorded_write_or_unfreed_private_allocation_is_rejected(self):
  p=self.probe();p['private_writes'].pop();self.reject(p,'all private process writes')
  p=self.probe();p['private_frees'][0]['released']=False;self.reject(p,'all private allocations released')
 def test_extra_source_call_is_rejected(self):
  p=self.probe();p['calls'].append(copy.deepcopy(p['calls'][-1]));self.reject(p,'omitted or additional')
 def test_forced_process_exit_is_not_source_cleanup(self):
  c=copy.deepcopy(self.report['cases'][0]['original_lifecycle']);c['lifetime']['forced_termination']=True
  with self.assertRaisesRegex(ValueError,'forced termination'):verify_lifecycle(c)
 def test_independent_scope_cannot_be_promoted_to_R3_completion(self):
  r=copy.deepcopy(self.report);r['R3_complete']=True
  with self.assertRaisesRegex(ValueError,'report scope'):verify_report(r)

if __name__=='__main__':unittest.main()
