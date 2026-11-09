import copy
import gzip
import hashlib
import json
from pathlib import Path
import unittest
from devtools import terminal_battle_wait_context_review as r


class ActualContextReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=Path(__file__).resolve().parents[2]/'.venv-audit/native-worker/terminal-battle-wait-window-context-v1-20261109.json.gz'
        raw=p.read_bytes()
        if hashlib.sha256(raw).hexdigest()!='84999db3df34e6581a2ea4381ec3a7360e75b6569d6b0e562cd661c45ed1d3b6':raise ValueError('fixed actual fixture')
        cls.source=json.loads(gzip.decompress(raw));cls.snap=cls.source['window_snapshots'][0]
    def fixture(self):return copy.deepcopy(self.source['context_attempts'][self.snap['context_attempt_index']])
    def check(self,x):return r.validate_attempt(x,self.source['subject'],[self.snap['scheduler_frame'],self.snap['frame']],self.snap['timing_diagnostic']['data_interval_qpc'])
    def test_actual_complete_context_and_data_bracket(self):
        result=self.check(self.fixture());self.assertTrue(result['all_716_bytes_equal'])
        self.assertLessEqual(result['full_worker_context_data_interval'][0],self.snap['timing_diagnostic']['data_interval_qpc'][0])
    def test_ending_extended_context_drift_is_observed_not_masked(self):
        x=self.fixture();t=x['threads'][1];raw=bytearray.fromhex(t['contexts'][1]['raw_hex']);raw[600]^=1
        t['contexts'][1]['raw_hex']=raw.hex();t['all_716_bytes_equal']=False
        self.assertFalse(self.check(x)['all_716_bytes_equal'])
        t['all_716_bytes_equal']=True
        with self.assertRaisesRegex(ValueError,'raw comparison'):self.check(x)
    def test_false_thread_owner_and_handle_alias_rejected(self):
        for alter in (lambda x:x['threads'][1].update(tid=1),lambda x:x['threads'][1].update(handle=x['threads'][0]['handle']),
                      lambda x:x['threads'][0].update(owner_verified_before_suspend=False)):
            x=self.fixture();alter(x)
            with self.assertRaises(ValueError):self.check(x)
    def test_suspend_increment_and_restore_order_rejected(self):
        x=self.fixture();x['operations'][2]['result']+=1
        with self.assertRaises(ValueError):self.check(x)
        x=self.fixture();x['operations'][2],x['operations'][3]=x['operations'][3],x['operations'][2]
        with self.assertRaises(ValueError):self.check(x)
    def test_context_query_after_resume_cannot_cover_data(self):
        x=self.fixture();x['threads'][1]['contexts'][1]['qpc_end']=x['operations'][2]['qpc_end']+1
        with self.assertRaises(ValueError):self.check(x)
    def test_bool_float_and_out_of_range_operation_results_rejected(self):
        for index,value in ((0,0.0),(4,True),(4,1.5),(2,-1),(2,0x100000000)):
            x=self.fixture();x['operations'][index]['result']=value
            with self.subTest(index=index,value=value),self.assertRaisesRegex(ValueError,'integer DWORD'):self.check(x)
    def test_incomplete_context_and_forged_frame_rejected(self):
        x=self.fixture();x['threads'][1]['contexts'][1]['raw_hex']=x['threads'][1]['contexts'][1]['raw_hex'][:-2]
        with self.assertRaises(ValueError):self.check(x)
        x=self.fixture();x['threads'][0]['contexts'][0]['raw_hex']=x['threads'][1]['contexts'][0]['raw_hex'];x['threads'][0]['all_716_bytes_equal']=False
        with self.assertRaises(ValueError):self.check(x)


if __name__=='__main__':unittest.main()
