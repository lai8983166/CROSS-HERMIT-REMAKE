import hashlib
import unittest

from tools.school_course_settlement_emulation import (
    report, fixture, source_rules, runtime_rules, CourseSettlementEmulator, CHAR, STRIDE)
from tools.tactics_exit_emulation import ROOT, report_text


class CourseSettlementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = report()

    def test_byte_exact_regeneration_and_runtime_rules(self):
        for name, value in [
            ('analysis/school-course-settlement-v1-20261007.json', self.data),
            ('prototype/data/school_course_settlement_evidence_v1.json', fixture(self.data)),
            ('prototype/data/school_course_settlement_rules.json', runtime_rules()),
        ]:
            self.assertEqual((ROOT/name).read_bytes(), report_text(value).encode())
        for key in ('cases', 'before', 'after', 'expected_after', 'packets'):
            self.assertNotIn(key, runtime_rules())
        self.assertEqual(runtime_rules()['initial_job_sums'],[
            {'character_id':r['character_id'],'job_sums':r['job_sums']} for r in self.data['cases'][0]['before_records']])

    def test_native_packets_and_declared_seed(self):
        cases = self.data['cases']
        self.assertEqual(len(cases), 8)
        self.assertNotEqual(cases[0]['learning_draws'], cases[3]['learning_draws'])
        self.assertEqual([r['character_id'] for r in cases[0]['packets']], [3,4,9])
        self.assertEqual([r['character_id'] for r in cases[4]['packets']], [3,4])
        self.assertEqual(cases[4]['before_records'][2], cases[4]['after_records'][2])
        self.assertEqual(cases[5]['packets'], cases[2]['packets'])
        for case in cases:
            self.assertIn('0x4a6a10', case['preparation_coverage']['visited_function_entries'])
            for entry in ('0x4bd870', '0x4c0400', '0x4d3600'):
                self.assertIn(entry, case['settlement_coverage']['visited_function_entries'])
            self.assertEqual(case['before']['month'], 4)
            self.assertEqual(case['before']['week'], 4)
            for key in ('month','week','relationships','group_raw_bytes','availability',
                        'raw_student_ids','raw_teacher_ids','course_buffers','course_counts'):
                self.assertEqual(case['before'][key],case['after'][key],(case['name'],key))
            for key in ('authorizes_persistent_write','interactive_school_ready','school_initialized','live_witness'):
                self.assertFalse(case[key])

    def test_caps_and_source_constant_average_factor(self):
        cases = self.data['cases']
        self.assertEqual(cases[2]['packets'][0]['packet'],[3450]*8)
        self.assertEqual(cases[6]['packets'][0]['packet'][0],0)
        self.assertGreater(cases[6]['bonus'],0)
        self.assertGreater(cases[7]['bonus'],0)
        self.assertLess(sum(cases[7]['packets'][0]['packet'][:7]),7*3450)
        self.assertEqual(cases[6]['setup']['counterfactual'],'attribute_cap')
        self.assertEqual(cases[7]['setup']['counterfactual'],'total_cap')

    def test_finite_guard_and_nonparticipants(self):
        e = CourseSettlementEmulator()
        e.initialize()
        nonparticipant = bytes(e.uc.mem_read(CHAR+5*STRIDE,STRIDE))
        e.declare_date(4,4)
        e.run('teaching','mode')
        e.run('assign','course',row=2)
        e.settle('entry_witness')
        for address in (0x4A6A10,0x4BD870,0x4BFFC0,0x4C00C0,0x4C0400,0x4C0060,0x4D3600,0x4D5600,0x4D58E0):
            # Preparation is separately traced and its source entry is in report.
            if address != 0x4A6A10:
                self.assertIn(address,e.visited)
        self.assertEqual(nonparticipant,bytes(e.uc.mem_read(CHAR+5*STRIDE,STRIDE)))
        with self.assertRaisesRegex(RuntimeError,'finite guard'):
            e._write_hook(e.uc,None,CHAR+5*STRIDE+0x10,4,1,None)
        with self.assertRaisesRegex(RuntimeError,'finite guard'):
            e._write_hook(e.uc,None,0x7A5290,2,5,None)


if __name__ == '__main__':
    unittest.main()
