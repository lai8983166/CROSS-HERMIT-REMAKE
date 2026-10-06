import hashlib
import json
import struct
import unittest

from tools.school_course_unlock_emulation import (
    ROOT, SOURCE, FLAGS, RECORDS, COUNTS, AUTHORITY,
    CourseUnlockEmulator, report, fixture, report_text, source_rules, source_provenance)

REPORT = ROOT/'analysis/school-course-unlock-v1-20261006.json'
FIXTURE = ROOT/'prototype/data/school_course_unlock_evidence.json'


class CourseUnlockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(REPORT.read_text('utf-8'))
        cls.cases = {c['name']:c for c in cls.data['cases']}

    def states(self,name):
        case = self.cases[name]
        states = [case['before']]
        for step in case['steps']:
            before = dict(states[-1])
            if 'declared_date' in step:
                before['month'],before['week'] = step['declared_date']
            states.append(before | step['changed_fields'])
        return states

    def test_regeneration_and_fixture_are_byte_exact(self):
        data = report()
        self.assertEqual(report_text(data).encode(),REPORT.read_bytes())
        self.assertEqual(report_text(fixture(data)).encode(),FIXTURE.read_bytes())

    def test_source_template_rules_bind_every_original_field(self):
        self.assertEqual(self.data['rules'],source_rules())
        self.assertEqual(len(self.data['rules']['templates']),100)
        self.assertEqual(self.data['rules']['template_fields_sha256'],
                         'cf7c1a6b640a930e9ce9ccafd339c93ad4178d6683013d8163c9aa77bfdab890')
        self.assertEqual(self.data['rules']['templates'][31]['category'],0)
        self.assertNotEqual(self.data['rules']['templates'][99]['category'],0)

    def test_teacher_provenance_is_call_bytes_and_does_not_migrate_roster(self):
        self.assertEqual(self.data['teacher_provenance'],source_provenance())
        image = SOURCE.read_bytes()
        for call in self.data['teacher_provenance']['calls']:
            address = int(call['call_va'],16)
            self.assertEqual(address+5+struct.unpack_from('<i',image,address-0x400000+1)[0],0x4D3E90)
        self.assertEqual(self.data['teacher_provenance']['calls'][0]['instruction_bytes'],
                         '6aff6a006a65b910117e00e8e3500300')
        self.assertFalse(self.data['teacher_provenance']['roster_migration_authorized_by_evidence'])

    def test_thresholds_and_reversed_insertion_order(self):
        self.assertEqual(self.states('date_4_2')[1]['course_counts'],[0]*20)
        self.assertEqual([r[3] for r in self.states('date_4_3')[1]['course_buffers'][16]],[16,15,14])
        self.assertEqual([r[3] for r in self.states('date_4_4')[1]['course_buffers'][0]],[12,11,10])
        self.assertEqual([r[3] for r in self.states('date_5_1')[1]['course_buffers'][0]],
                         [12,11,10,5,4,3,2,1])
        self.assertEqual([r[3] for r in self.states('date_5_2')[1]['course_buffers'][16]],[16,15,14,13])

    def test_valid_empty_masks_unlock_and_invalid_hole_stays_locked(self):
        state = self.states('date_0_0')[1]
        self.assertEqual(state['course_counts'],[0]*20)
        self.assertEqual(state['course_unlocked_flags'][100],1)
        state = self.states('date_14_2')[1]
        self.assertEqual(sum(state['course_unlocked_flags']),99)
        self.assertEqual(state['course_unlocked_flags'][32],0)
        # Work49 is assigned to three distinct teachers.
        for slot in [12,14,17]:
            self.assertIn(49,[r[3] for r in state['course_buffers'][slot]])

    def test_shift_preserves_old_progress_and_physical_opaque_bytes(self):
        before,after,repeat = self.states('existing_progress_and_physical_opaque')
        rows = after['course_buffers'][16]
        self.assertEqual([r[3] for r in rows[:5]],[16,15,14,22,13])
        self.assertEqual(rows[3][1:6],[2,3,22,-7,123])
        self.assertEqual(rows[4][1:6],[1,0,13,9,45])
        self.assertTrue(all(r[5] == 0 for r in rows[:3]))
        self.assertEqual([r[6:] for r in rows],[r[6:] for r in before['course_buffers'][16]])
        self.assertEqual(after,repeat)

    def test_repeat_and_any_nonzero_flag_do_not_duplicate(self):
        for case in self.data['cases'][:12]:
            self.assertEqual(case['steps'][1]['changed_fields'],{})
            self.assertEqual(case['steps'][1]['native_writes'],[])
        state = self.states('nonzero_flags_skip')[1]
        self.assertEqual([state['course_unlocked_flags'][i] for i in [0,1,2,14]],[9,7,255,2])
        self.assertNotIn(1,[r[3] for r in state['course_buffers'][0]])
        self.assertNotIn(14,[r[3] for r in state['course_buffers'][16]])
        states = self.states('forward_repeat_and_earlier_date')
        self.assertEqual(states[4]['course_buffers'],states[3]['course_buffers'])
        self.assertEqual(states[4]['course_unlocked_flags'],states[3]['course_unlocked_flags'])
        self.assertEqual([r[3] for r in states[5]['course_buffers'][16]],[13,16,15,14])

    def test_native_entries_finite_write_guard_and_100_capacity(self):
        self.assertEqual(len(self.cases),15)
        self.assertEqual(self.states('capacity_exact_100')[1]['course_counts'][16],100)
        for case in self.data['cases']:
            for step in case['steps']:
                self.assertIn('0x4a2ba0',step['visited_function_entries'])
                self.assertEqual(set(step['stub_calls']),{'debug_stack_check'})
                for write in step['native_writes']:
                    a,size = int(write['address'],16),write['size']
                    self.assertTrue(FLAGS+1 <= a < FLAGS+101 or COUNTS <= a < COUNTS+40 or
                                    RECORDS <= a < RECORDS+20000 and (a-RECORDS)%10+size <= 8)
        emulator = CourseUnlockEmulator(4,3)
        for address in [0x7A511C,0x7A528E,FLAGS,RECORDS+8,COUNTS+40]:
            with self.assertRaises(RuntimeError):
                emulator._write_hook(emulator.uc,0,address,1,0,None)

    def test_zero_roster_and_non_target_fields_remain_unchanged(self):
        for case in self.data['cases']:
            for state in self.states(case['name']):
                for key in ['teacher_count','teacher_ids','availability','global_total_511c']:
                    self.assertEqual(state[key],case['before'][key])
            for step in case['steps']:
                self.assertNotIn('month',step['changed_fields'])
                self.assertNotIn('week',step['changed_fields'])
        for key in AUTHORITY:
            self.assertFalse(self.data[key])
        self.assertEqual(fixture(self.data)['source_report_sha256'],hashlib.sha256(REPORT.read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main()
