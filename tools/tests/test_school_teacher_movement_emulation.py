import hashlib
import json
import struct
import unittest

from tools.school_teacher_movement_emulation import (
    ROOT, report, fixture, report_text, source_rules, TeacherMovementEmulator)
from tools.school_student_movement_emulation import apply_patch

REPORT = ROOT/'analysis/school-teacher-movement-v1-20261006.json'
FIXTURE = ROOT/'prototype/data/school_teacher_movement_evidence.json'


def teacher(s,g):
    return struct.unpack_from('<h',bytes(s['group_raw_bytes']),g*28)[0]


def students(s,g):
    return list(struct.unpack_from('<4h',bytes(s['group_raw_bytes']),g*28+16))


class TeacherMovementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(REPORT.read_text(encoding='utf-8'))
        cls.cases = {c['name']:c for c in cls.data['cases']}
        cls.selections = {c['name']:c for c in cls.data['selections']}

    def snapshots(self,name):
        c = self.cases[name]
        before = c['before']
        after = apply_patch(before,c['movement']['changed_fields'])
        clean = apply_patch(after,c['reconciliation']['changed_fields'])
        rated = apply_patch(clean,c['rating']['changed_fields'])
        return before,after,clean,rated

    def test_reports_and_export_regenerate_byte_exactly(self):
        r = report()
        self.assertEqual(report_text(r).encode(),REPORT.read_bytes())
        self.assertEqual(report_text(fixture(r)).encode(),FIXTURE.read_bytes())

    def test_source_rules_are_original_fields_and_teacher_template_not_student_profile(self):
        self.assertEqual(self.data['work_rules'],source_rules())
        self.assertEqual(len(self.data['work_rules']['templates']),99)
        self.assertEqual(self.data['work_rules']['template_fields_sha256'],
                         '7206ac045306b139a742d678b52ba1c29d602e73245e90cb06774d6801ac651e')
        for p in self.data['work_rules']['teacher_profiles']:
            self.assertEqual((p['job'],p['level_50'],p['attributes']),(1,0,[0]*7))

    def test_waiting_placement_and_replacement_preserve_students(self):
        for gate in range(2):
            for mode in range(3):
                _,a,_,_ = self.snapshots(f'waiting_empty_mode{mode}_gate{gate}')
                self.assertEqual(teacher(a,1),117)
                self.assertEqual(a['idle_teacher_ids'],[])
                self.assertEqual(a['group_raw_bytes'][31],0 if gate else 1)
                before,a,_,_ = self.snapshots(f'waiting_replace_mode{mode}_gate{gate}')
                self.assertEqual(teacher(a,0),118)
                self.assertEqual(a['idle_teacher_ids'],[117])
                self.assertEqual(students(a,0),students(before,0))
                self.assertEqual(a['group_raw_bytes'][3],before['group_raw_bytes'][3])

    def test_move_empty_returns_source_students_without_immediate_student_sort(self):
        for gate in range(2):
            for mode in range(3):
                b,a,c,r = self.snapshots(f'class_empty_mode{mode}_gate{gate}')
                self.assertEqual((teacher(a,0),teacher(a,1)),(-1,117))
                self.assertEqual(students(a,0),[-1]*4)
                self.assertEqual(a['idle_student_ids'],[9,5,3,4])
                self.assertEqual(a['group_raw_bytes'][14],2)
                self.assertEqual(c['group_raw_bytes'][14],0)
                self.assertEqual(a['derived_student_ids'][0],b['derived_student_ids'][0])
                self.assertEqual(r['derived_student_ids'][0],[-1]*4)
                self.assertEqual(a['group_raw_bytes'][31],0 if gate else 1)

    def test_exchange_and_same_group_clear_only_defined_work_fields(self):
        b,a,_,_ = self.snapshots('class_exchange_mode0_gate0')
        self.assertEqual((teacher(a,0),teacher(a,1)),(118,117))
        for g in range(2):
            self.assertEqual(students(a,g),students(b,g))
            for offset in [6,8]:
                self.assertEqual(a['group_raw_bytes'][g*28+offset:g*28+offset+2],[255,255])
            for offset in [3,10,11,12,13]:
                self.assertEqual(a['group_raw_bytes'][g*28+offset],b['group_raw_bytes'][g*28+offset])
        b,a,_,_ = self.snapshots('same_group_mode0_gate0')
        self.assertEqual(teacher(a,0),117)
        self.assertEqual(students(a,0),students(b,0))
        self.assertEqual(a['group_raw_bytes'][6:10],[255]*4)

    def test_outside_sorts_students_but_does_not_immediately_refresh_work(self):
        b,a,c,r = self.snapshots('class_outside_no_teacher_mode0_gate0')
        self.assertEqual(a['idle_student_ids'],[9,4,3,5])
        self.assertEqual(a['idle_teacher_ids'],[118,117])
        for key in ['selected_group','work_counts','work_rows']:
            self.assertEqual(a[key],b[key])
            self.assertEqual(c[key],b[key])  # no available class to select in cleanup
        b,a,c,r = self.snapshots('class_outside_other_teacher_mode0_gate0')
        self.assertEqual(a['selected_group'],0)
        self.assertEqual(c['selected_group'],1)
        self.assertEqual(c['work_counts'],[1,1,1])

    def test_held_teacher_hover_does_not_change_class_selection(self):
        for name in ['waiting_empty_held','waiting_replace_held','class_empty_held','class_exchange_held']:
            b,a,_,_ = self.snapshots(name)
            expected = dict(b,task_drag_state=2)
            self.assertEqual(a,expected)
        for c in self.cases.values():
            self.assertNotIn('0x4a95f0',c['movement']['visited_function_entries'])
            self.assertIn('0x4a4680',c['movement']['visited_function_entries'])

    def test_work_projection_executes_actual_function_and_filters_in_slot_order(self):
        self.assertEqual(len(self.selections),11)
        c = self.selections['mixed_active']
        s = apply_patch(c['before'],c['selection']['changed_fields'])
        self.assertEqual(s['work_counts'],[2,1,1])
        self.assertEqual(s['work_rows'],[[[1,2,0],[0,1,1]],[[6,7,0]],[[8,9,0]]])
        for c in self.selections.values():
            self.assertIn('0x4a2980',c['selection']['visited_function_entries'])
            self.assertNotIn('teacher_work_table_boundary',c['selection']['stub_calls'])
        for name in ['teacherless','cleared']:
            c = self.selections[name]
            s = apply_patch(c['before'],c['selection']['changed_fields'])
            self.assertEqual(s['work_counts'],[0]*3)
            self.assertEqual(s['work_rows'],[[],[],[]])

    def test_page_boundaries_and_maximum_slot_count(self):
        for count in [0,1,10,11,12,13,99,100]:
            c = self.selections[f'page_count_{count}']
            s = apply_patch(c['before'],c['selection']['changed_fields'])
            self.assertEqual(s['work_counts'],[count,0,0])
            self.assertEqual(s['work_page_limits'],[(count-9)//2 if count>10 else 0,0,0])
            self.assertEqual(s['work_pages'],[0,0,0])
            self.assertEqual([r[2] for r in s['work_rows'][0]],list(range(count)))

    def test_unrelated_records_and_authority_remain_unchanged(self):
        self.assertEqual(len(self.cases),52)
        for c in self.cases.values():
            phases = self.snapshots(c['name'])
            for key in ['student_ids','teacher_ids','availability','month','week','global_total_511c',
                        'relationships','student_record_sha256','teacher_work_records','teacher_work_record_sha256']:
                self.assertTrue(all(s[key] == phases[0][key] for s in phases),key)
        for key in ['school_initialized','interactive_school_ready','live_witness','authorizes_persistent_write']:
            self.assertFalse(self.data[key])
        emulator = TeacherMovementEmulator([{'teacher':117}])
        with self.assertRaises(RuntimeError):
            emulator._write_hook(emulator.uc,0,0x7A511C,4,1,None)


if __name__ == '__main__':
    unittest.main()
