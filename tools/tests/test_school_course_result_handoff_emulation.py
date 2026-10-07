import unittest

from tools.school_course_result_handoff_emulation import (
    report,fixture,source_rules,CourseResultHandoffEmulator)
from tools.tactics_exit_emulation import ROOT,report_text
from tools.scene5_script_emulation import VM


class CourseResultHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = report()

    def test_byte_exact_native_report_fixture_and_source_rules(self):
        for name,value in [
            ('analysis/school-course-result-handoff-v1-20261007.json',self.data),
            ('prototype/data/school_course_result_handoff_evidence_v1.json',fixture(self.data)),
            ('prototype/data/school_course_result_handoff_rules.json',source_rules())]:
            self.assertEqual((ROOT/name).read_bytes(),report_text(value).encode())
        for key in ('cases','before','after','expected','recipient'):
            self.assertNotIn(key,source_rules())

    def test_real_mvp_end_before_confirmation_count_and_adv_entry(self):
        for case in self.data['cases'][:3]:
            self.assertTrue(case['result_completed'])
            self.assertEqual(case['result_requests'],[6])
            self.assertEqual(case['after_result']['stored_next_task'],7)
            self.assertEqual(case['after_result']['pending_flag'],1)
            self.assertEqual(case['after_result']['pending_state'],6)
            self.assertEqual(case['stop_reason'],'chapter016_entry_boundary')
            self.assertEqual(case['loads'][0]['path'],'allresult/dat/mvp.ybc')
            recipient = case['growth_checkpoint']['recipient']
            child = f'allresult/dat/mvp{recipient:03}.ybc'
            self.assertEqual([row['path'] for row in case['loads']],
                             ['allresult/dat/mvp.ybc',child,'adv/dat/ch003.ybc','adv/dat/chapter016.ybc'])
            self.assertTrue(any(c['path'] == child and c['opcode'] == 19 for c in case['commands']))
            self.assertFalse(any(c['path'] == 'adv/dat/chapter016.ybc' for c in case['commands']))
            entries = [row['va'] for row in case['task_entries']]
            for address in ('0x4bd870','0x4bdac0','0x4c1350','0x4d0750','0x439e30'):
                self.assertEqual(entries.count(address),1)
            self.assertLess(entries.index('0x4bdac0'),entries.index('0x4c1350'))
            for counts in (case['initialized_counts'],source_rules()['initial_counts']):
                self.assertTrue(all(row['count'] == 0 for row in counts))
            self.assertEqual([case['after_result']['school'][key] for key in ('month','week')],[4,4])
            self.assertFalse(case['chapter_body_executed'])
            self.assertFalse(case['week_executed'])
            for old,new in zip(case['growth_checkpoint']['records'],case['after_result']['growth_records']):
                for key in old:
                    if key != 'job_sums':
                        self.assertEqual(old[key],new[key],(case['name'],key))
            for address in ('0x4ce8f0','0x4d0c80','0x4c2190','0x4c5430'):
                self.assertIn(address,case['mvp_coverage']['visited_function_entries'])
            for key in ('authorizes_persistent_write','interactive_school_ready','school_initialized','live_witness'):
                self.assertFalse(case[key])
        cap = self.data['cases'][2]
        self.assertTrue(all(row['count'] == 5 for row in cap['after_result']['counts']))

    def test_waits_do_not_confirm_award_or_request_adv(self):
        for case in self.data['cases'][3:]:
            self.assertFalse(case['result_completed'])
            self.assertIsNone(case['confirmation_checkpoint'])
            self.assertEqual(case['after_result']['counts'],case['growth_checkpoint']['counts'])
            self.assertEqual(case['result_requests'],[])
            self.assertEqual(case['stop_reason'],'bounded_pending_result')
            self.assertFalse(any(row['path'].startswith('adv/') for row in case['loads']))
        key = self.data['cases'][4]
        self.assertEqual(key['commands'][-1]['opcode'],51)
        self.assertFalse(any(c['opcode'] == 19 for c in key['commands']))

    def test_native_tie_order_positive_gate_and_finite_guard(self):
        self.assertEqual([row['recipient'] for row in self.data['selection_probes']],[3,4,-1,9])
        for row in self.data['selection_probes']:
            self.assertTrue(row['counterfactual'])
            self.assertFalse(row['growth_executed'])
            self.assertIn('0x4c00c0',row['coverage']['visited_function_entries'])
        e = CourseResultHandoffEmulator()
        e.stage = 'course_result_presentation'
        for address,size in [(0x7A5290,2),(0x7CF34C+5*0x124+0x120,2),(VM+0x9400,4)]:
            with self.assertRaisesRegex(RuntimeError,'finite guard'):
                e._write_hook(e.uc,None,address,size,1,None)
        with self.assertRaisesRegex(ValueError,'readiness'):
            CourseResultHandoffEmulator(confirm=1)


if __name__ == '__main__':
    unittest.main()
