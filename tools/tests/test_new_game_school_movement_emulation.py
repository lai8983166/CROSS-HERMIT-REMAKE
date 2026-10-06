import hashlib
import json
import unittest

from tools.new_game_school_movement_emulation import (
    ROOT, NewGameMovementEmulator, report, fixture, report_text, work_rules, AUTHORITY)
from tools.new_game_school_emulation import CHAR, STRIDE

REPORT = ROOT/'analysis/new-game-school-movement-v1-20261006.json'
FIXTURE = ROOT/'prototype/data/new_game_school_movement_evidence.json'


class NewGameMovementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(REPORT.read_text('utf-8'))

    def test_regeneration_and_godot_export_are_byte_exact(self):
        data = report()
        self.assertEqual(report_text(data).encode(),REPORT.read_bytes())
        self.assertEqual(report_text(fixture(data)).encode(),FIXTURE.read_bytes())

    def test_teacher_domain_is_source101_static_profile(self):
        self.assertEqual(work_rules(),self.data['work_rules'])
        self.assertEqual(work_rules()['teacher_profiles'],[
            {'teacher_id':101,'job':1,'level_50':0,'attributes':[1]*7}])

    def test_sequence_owns_one_roster_without_role_date_or_course_changes(self):
        immutable = ['month','week','difficulty','global_total_511c','student_ids','teacher_ids',
            'raw_student_ids','raw_teacher_ids','availability','member_profiles','relationships',
            'course_unlocked_flags','course_counts','course_buffers','student_count','teacher_count']
        self.assertEqual(len(self.data['cases']),20)
        previous = self.data['prepared']
        for row in self.data['cases']:
            for key in previous:
                self.assertEqual(row['before'][key],previous[key],row['name']+'/'+key)
            after = dict(row['before'])
            for phase in row['phases']:
                after.update(phase['changed_fields'])
                for key in immutable:
                    self.assertEqual(after[key],self.data['prepared'][key],row['name']+'/'+key)
            previous = row['canonical_after']
            for key in previous:
                self.assertEqual(after[key],previous[key])

    def test_actual_native_bodies_and_three_separate_phases_execute(self):
        for row in self.data['cases']:
            self.assertEqual([p['phase'] for p in row['phases']],['movement','move_reconcile','move_rate'])
            for phase,address in zip(row['phases'],['0x4a4680','0x4a5f40','0x4a95f0']):
                self.assertIn(address,phase['coverage']['visited_function_entries'])
                self.assertNotIn('teacher_work_rebuild',phase['coverage']['stub_calls'])
                self.assertEqual(phase['coverage']['member_record_sha256'],
                                 self.data['initialization_coverage']['member_record_sha256'])
            for rating in row['phases'][2]['ratings']:
                self.assertTrue(0 <= rating['relationship_rank'] <= 7)

    def test_teacher_relocation_returns_students_and_waiting_rejoins(self):
        cases = {r['name']:r for r in self.data['cases']}
        self.assertEqual(cases['teacher_empty']['canonical_after']['idle_student_ids'],[3,4,9])
        self.assertEqual(cases['teacher_outside']['canonical_after']['idle_teacher_ids'],[101])
        self.assertEqual(cases['teacher_waiting_empty']['canonical_after']['derived_teacher_ids'],[-1]*4+[101])
        self.assertEqual(cases['rejoin_student9']['canonical_after']['derived_student_ids'][4],[3,4,9,-1])

    def test_guard_refuses_roles_rosters_courses_and_authority_stays_closed(self):
        emulator = NewGameMovementEmulator()
        for stage in ['movement','move_reconcile','move_rate']:
            emulator.stage = stage
            for address in [0x7A528E,0x7A5260,0x7A511C,0x7A5BCA,0x7A55FA,
                            CHAR+3*STRIDE,0x6F5088+101*STRIDE]:
                with self.assertRaises(RuntimeError):
                    emulator._write_hook(emulator.uc,0,address,2,0,None)
        for key in AUTHORITY:
            self.assertFalse(self.data[key])
        self.assertEqual(fixture(self.data)['source_report_sha256'],hashlib.sha256(REPORT.read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main()
