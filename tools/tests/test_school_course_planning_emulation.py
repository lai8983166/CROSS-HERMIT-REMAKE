import hashlib
import json
import unittest

from tools.school_course_planning_emulation import ROOT, CoursePlanningEmulator, report, fixture, report_text, AUTHORITY

REPORT = ROOT/'analysis/school-course-planning-v2-20261007.json'
FIXTURE = ROOT/'prototype/data/school_course_planning_evidence_v2.json'


class CoursePlanningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(REPORT.read_text('utf-8'))

    def test_regeneration_is_byte_exact(self):
        data = report()
        self.assertEqual(report_text(data).encode(),REPORT.read_bytes())
        self.assertEqual(report_text(fixture(data)).encode(),FIXTURE.read_bytes())

    def test_actual_menu_click_getter_and_rating_execute(self):
        self.assertEqual(len(self.data['cases']),15)
        for row in self.data['cases']:
            entries = row['operation']['coverage']['visited_function_entries']
            self.assertIn('0x4a3ca0' if row['command']['kind'] == 'mode' else '0x4a2da0',entries)
            self.assertIn('0x4a8bc0',entries)
            self.assertIn('0x4a95f0',row['rating']['coverage']['visited_function_entries'])
            self.assertEqual(row['operation']['coverage']['member_record_sha256'],
                             self.data['initialization_coverage']['member_record_sha256'])

    def test_explicit_date_unlocks_and_assignment_do_not_advance_time_or_grow(self):
        dates = self.data['date_checkpoints']
        self.assertEqual([d['declared_date'] for d in dates],[[4,4],[6,5],[11,5]])
        self.assertEqual(dates[0]['after']['work_rows'][0],[[11,12,0],[10,11,1],[9,10,2]])
        for row in self.data['cases']:
            state = dict(row['before'])
            state.update(row['operation']['changed_fields'])
            state.update(row['rating']['changed_fields'])
            for key in ['month','week','member_profiles','relationships','availability','student_ids','teacher_ids',
                        'global_total_511c','course_buffers','course_counts','course_unlocked_flags']:
                self.assertEqual(state[key],row['before'][key])
            for key,value in row['canonical_after'].items():
                self.assertEqual(state[key],value)

    def test_only_four_work_words_and_activity_change_in_raw_groups(self):
        for row in self.data['cases']:
            raw = row['operation']['changed_fields'].get('group_raw_bytes',row['before']['group_raw_bytes'])
            changed = {i for i,(a,b) in enumerate(zip(raw,row['before']['group_raw_bytes'])) if a != b}
            self.assertTrue(changed <= ({3} if row['command']['kind'] == 'mode' else set(range(6,14))))
        cases = {r['name']:r for r in self.data['cases']}
        self.assertNotIn('group_raw_bytes',cases['hover_only']['operation']['changed_fields'])
        self.assertNotIn('group_raw_bytes',cases['adventure_click_ignored']['operation']['changed_fields'])
        self.assertNotIn('group_raw_bytes',cases['empty_category']['operation']['changed_fields'])
        self.assertEqual(cases['gate_forces_adventure']['canonical_after']['group_raw_bytes'][3],0)
        self.assertEqual(cases['advanced_course']['rating']['ratings'][0]['work_fields'][0],2)

    def test_finite_guard_and_closed_authority(self):
        e = CoursePlanningEmulator()
        for stage in ['mode','course','planning_rate']:
            e.stage = stage
            for address in [0x7A528E,0x7A511C,0x7A5BCA,0x7E17E8,0x7A55FA]:
                with self.assertRaises(RuntimeError):
                    e._write_hook(e.uc,0,address,2,0,None)
        for key in AUTHORITY:
            self.assertFalse(self.data[key])
        self.assertEqual(fixture(self.data)['source_report_sha256'],hashlib.sha256(REPORT.read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main()
