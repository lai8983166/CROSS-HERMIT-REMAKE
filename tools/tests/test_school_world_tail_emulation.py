import json,hashlib,unittest
from copy import deepcopy
from tools.school_world_tail_verification import REPORT,REPORT_SHA,verify_case
from tools.school_world_tail import source_contract


class NativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=json.loads(REPORT.read_bytes())

    def test_three_actual_original_returns_and_counter_probes(self):
        self.assertEqual(hashlib.sha256(REPORT.read_bytes()).hexdigest(),REPORT_SHA)
        self.assertEqual(self.data['source_contract'],source_contract())
        self.assertEqual([c['name'] for c in self.data['cases']],['initial','student9_waiting','fifth_class'])
        for c in self.data['cases']:self.assertTrue(verify_case(c))
        self.assertTrue(self.data['first_paused_46B470_body_completed'])
        for k in ('enabled_gameplay_tick_completed','original_outer_task_frame_completed','original_opening_completed','persistent_write_authority'):self.assertIs(self.data[k],False)

    def test_full_effect_secondary_control_queue_corruption_refuse(self):
        for i in range(10):
            bad=deepcopy(self.data['cases'][0]);r=bad['actual_tail']['after'][i];r['hex']=r['hex'][:-2]+('00' if r['hex'][-2:]!='00' else '01')
            with self.assertRaises(ValueError):verify_case(bad)

    def test_false_completion_wrong_stack_calls_or_provenance_refuse(self):
        bad=deepcopy(self.data['cases'][0]);bad['actual_tail']['real_ret']['original_outer_caller']=True
        with self.assertRaises(ValueError):verify_case(bad)
        bad=deepcopy(self.data['cases'][0]);bad['actual_tail']['driver_return']['sp']-=4
        with self.assertRaises(ValueError):verify_case(bad)
        bad=deepcopy(self.data['cases'][0]);bad['actual_tail']['effect_calls'].pop()
        with self.assertRaises(ValueError):verify_case(bad)
        bad=deepcopy(self.data['cases'][0]);bad['parent_checkpoint']['sha256']='0'*64
        with self.assertRaises(ValueError):verify_case(bad)
        bad=deepcopy(self.data['cases'][0]);bad['actual_tail']['enabled_gameplay_tick_completed']=True
        with self.assertRaises(ValueError):verify_case(bad)

    def test_changed_declared_probe_binding_and_restoration_refuse(self):
        bad=deepcopy(self.data['cases'][0]);bad['declared_probes']['counter'][1]['declared_counter_word']=7
        with self.assertRaises(ValueError):verify_case(bad)
        bad=deepcopy(self.data['cases'][0]);bad['declared_probes']['counter'][1]['restoration']['cpu_after_sha256']='0'*64
        with self.assertRaises(ValueError):verify_case(bad)
        bad=deepcopy(self.data['cases'][0]);bad['declared_probes']['counter'][1]['effect_returns'][0]=0
        with self.assertRaises(ValueError):verify_case(bad)


if __name__=='__main__':unittest.main()
