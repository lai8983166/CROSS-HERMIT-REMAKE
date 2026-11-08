import unittest
from types import SimpleNamespace
from devtools.terminal_input_window import observe


class WindowTests(unittest.TestCase):
    def run_window(self,finish,fail_capture=False):
        clock=[0.0];record={'input_samples':[{'t':0.0,'button':0,'wall_time_ns':1_000_000_000}],
                          'action':{'up_wall_time_ns':int((1+finish)*1e9)}}
        worker=SimpleNamespace(is_alive=lambda:clock[0]<finish)
        def sleep(seconds):clock[0]+=seconds
        def capture():
            if fail_capture and clock[0]>.1:raise OSError('capture failed')
            return dict(t=clock[0],wall_time_ns=int((1+clock[0])*1e9),button=(1 if 8.7<=clock[0]<8.795 else
                                          2 if 8.795<=clock[0]<8.825 else 0))
        try:observe(worker,capture,record,clock=lambda:clock[0],sleep=sleep,
                    wall_clock=lambda:int((1+clock[0])*1e9))
        finally:self.record=record
        return record

    def test_slow_prechecks_do_not_leave_the_actual_press_unobserved(self):
        r=self.run_window(8.795)
        self.assertTrue(r['input_window']['complete'])
        self.assertEqual(len(r['input_samples']),1024)
        self.assertGreater(r['input_window']['evicted_samples'],0)
        self.assertIn(1,[s['button']for s in r['input_samples']])
        self.assertIn(2,[s['button']for s in r['input_samples']])
        self.assertLess(r['input_samples'][0]['t'],8.7)
        self.assertGreater(r['input_samples'][-1]['t'],8.825)

    def test_late_action_is_failure_not_an_unobserved_success(self):
        with self.assertRaisesRegex(ValueError,'continuous observation'):
            self.run_window(20)
        self.assertFalse(self.record['input_window']['complete'])
        self.assertLessEqual(len(self.record['input_samples']),1024)

    def test_capture_failure_preserves_bounded_partial_evidence(self):
        with self.assertRaisesRegex(OSError,'capture failed'):
            self.run_window(1,True)
        self.assertFalse(self.record['input_window']['complete'])
        self.assertGreater(len(self.record['input_samples']),1)

    def test_short_action_keeps_release_observation_tail(self):
        r=self.run_window(.2)
        self.assertTrue(r['input_window']['complete'])
        self.assertGreaterEqual(r['input_samples'][-1]['t'],.3)
        self.assertEqual(r['input_window']['evicted_samples'],0)

    def test_independent_retention_contract_and_tampering(self):
        import copy
        from devtools.terminal_school_handoff_verification import verify_input_window
        r=self.run_window(8.795)
        verify_input_window(r)
        for key,value in [('complete',False),('captured_samples',1),('retained_samples',1),
                          ('maximum_retained_samples',2048),('elapsed_seconds',13)]:
            changed=copy.deepcopy(r);changed['input_window'][key]=value
            with self.assertRaises(ValueError):verify_input_window(changed)
        short=copy.deepcopy(r);short['input_samples']=short['input_samples'][-20:]
        short['input_window']['retained_samples']=20
        short['input_window']['evicted_samples']=short['input_window']['captured_samples']-20
        with self.assertRaises(ValueError):verify_input_window(short)
        tail=copy.deepcopy(r)
        tail['input_window']['finished_wall_time_ns']=tail['input_samples'][-1]['wall_time_ns']-5_500_000
        with self.assertRaises(ValueError):verify_input_window(tail)


if __name__=='__main__':unittest.main()
