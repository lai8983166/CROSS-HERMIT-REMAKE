import hashlib
import json
import unittest

from tools.school_course_settlement_emulation import (
    report, fixture, source_rules, runtime_rules, may_five_lessons, june_five_lessons, august_four_lessons, september_one_lessons, CourseSettlementEmulator, CHAR, STRIDE)
from tools.tactics_exit_emulation import ROOT, report_text
from tools.school_course_unlock_emulation import CourseUnlockEmulator


class JuneCourseTableTests(unittest.TestCase):
    def test_june_rows_match_executable_and_newly_unlocked_lessons(self):
        rows = june_five_lessons()
        raw = (ROOT/'prototype/data/school_june_five_courses.json').read_bytes()
        self.assertEqual(json.loads(raw), rows)
        templates = json.loads((ROOT/'prototype/data/new_game_school_rules.json').read_bytes())['course_rules']['templates']
        dated = {row['work_id'] for row in templates if (row['month'],row['week']) == (6,5)
                 and any(row['teacher_mask'][teacher-101] for teacher in (101,110,115,118))}
        self.assertEqual(dated, {8,19,20,26,28,29})
        self.assertEqual({int(key) for key in rows}, dated-set(range(len(source_rules()['training']))))
        self.assertEqual(rows['26']['package'],[0]*7+[50000])
        self.assertEqual(rows['19']['package'],rows['20']['package'])
        self.assertNotEqual(rows['19']['learning_rates'],rows['20']['learning_rates'])


class AugustCourseTableTests(unittest.TestCase):
    def test_august_four_rows_match_original_teacher_masks_and_lesson_data(self):
        rules = json.loads((ROOT/'prototype/data/new_game_school_rules.json').read_bytes())
        dated = [(row['work_id'], [101+i for i,enabled in enumerate(row['teacher_mask']) if enabled])
                 for row in rules['course_rules']['templates'] if (row['month'],row['week']) == (8,4)]
        self.assertEqual([(work,teachers) for work,teachers in dated if set(teachers) & {101,110,115,118,116}],
                         [(30,[118]),(33,[116])])
        rows = json.loads((ROOT/'prototype/data/school_august_four_courses.json').read_bytes())
        self.assertEqual(rows,august_four_lessons())

    def test_week_four_adds_exact_original_rows_for_two_teachers(self):
        original = CourseUnlockEmulator(8,3)
        original.unlock()
        prior = original.snapshot()['course_buffers']
        original.write(0x7A5290,4,'h')
        original.unlock()
        current = original.snapshot()['course_buffers']
        for teacher, earlier, unlocked in [(116,[],[33]), (118,[29,28],[30,29,28])]:
            self.assertEqual([row[3] for row in prior[teacher-101]],earlier)
            self.assertEqual([row[3] for row in current[teacher-101]],unlocked)

    def test_september_first_week_opens_courses_24_and_36(self):
        original = CourseUnlockEmulator(8,5)
        original.unlock()
        before = original.snapshot()
        original.write(0x7A528E,9,'h')
        original.write(0x7A5290,1,'h')
        original.unlock()
        after = original.snapshot()
        added = [i for i,(old,new) in enumerate(zip(before['course_unlocked_flags'],after['course_unlocked_flags'])) if new and not old]
        self.assertEqual(added,[24,36])
        rows = json.loads((ROOT/'prototype/data/school_september_one_courses.json').read_bytes())
        self.assertEqual(rows,september_one_lessons())
        self.assertEqual(set(map(int,rows)),set(added))
        for teacher,work in [(115,24),(116,36)]:
            self.assertIn(work,[row[3] for row in after['course_buffers'][teacher-101]])


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

    def test_may_five_lessons_match_executable(self):
        import json
        source = may_five_lessons()
        self.assertEqual(json.loads((ROOT/'prototype/data/school_may_five_courses.json').read_bytes()),source)
        self.assertEqual(source['17']['package'],[2000]*8)
        self.assertEqual(source['27']['package'],[0,0,0,50000,0,0,0,0])

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
