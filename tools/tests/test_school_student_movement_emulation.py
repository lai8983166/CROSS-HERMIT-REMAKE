import hashlib
import json
import struct
import unittest
from pathlib import Path

from tools.school_student_movement_emulation import (
    ROOT, TASK, GROUP_BASE, WRITE_RANGES, StudentMovementEmulator,
    report, fixture, report_text, apply_patch)

REPORT = ROOT/'analysis/school-student-movement-v1-20261006.json'
FIXTURE = ROOT/'prototype/data/school_student_movement_evidence.json'


def word(snapshot, group, slot):
    return struct.unpack_from('<h',bytes(snapshot['group_raw_bytes']),28*group+16+2*slot)[0]


class StudentMovementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.native = json.loads(REPORT.read_text(encoding='utf-8'))
        cls.cases = {row['name']:row for row in cls.native['cases']}

    def snapshots(self,name):
        row = self.cases[name]
        before = row['before']
        after = apply_patch(before,row['movement']['changed_fields'])
        clean = apply_patch(after,row['reconciliation']['changed_fields'])
        rated = apply_patch(clean,row['rating']['changed_fields'])
        return before,after,clean,rated

    def test_report_and_compact_export_regenerate_byte_exactly(self):
        regenerated = report()
        self.assertEqual(report_text(regenerated).encode(),REPORT.read_bytes())
        self.assertEqual(report_text(fixture(regenerated)).encode(),FIXTURE.read_bytes())
        self.assertEqual(json.loads(FIXTURE.read_text())['native_report_sha256'],
                         hashlib.sha256(REPORT.read_bytes()).hexdigest())

    def test_all_cases_execute_drag_and_preserve_unrelated_records(self):
        self.assertEqual(len(self.cases),37)
        for row in self.cases.values():
            self.assertIn('0x4a4680',row['movement']['visited_function_entries'])
            self.assertGreater(row['movement']['visited_instruction_count'],100)
            phases = self.snapshots(row['name'])
            for key in ['student_ids','teacher_ids','availability','relationships','month','week',
                        'global_total_511c','student_record_sha256','lecture_work_fields']:
                self.assertTrue(all(p[key] == phases[0][key] for p in phases),row['name']+key)
            for group in range(5):
                for offset in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,15,24,25,26,27]:
                    self.assertTrue(all(p['group_raw_bytes'][group*28+offset] ==
                                        phases[0]['group_raw_bytes'][group*28+offset] for p in phases))

    def test_waiting_add_and_replacement_execute_rating_and_auto_sort(self):
        for mode in range(3):
            before,after,clean,rated = self.snapshots(f'waiting_empty_mode{mode}')
            self.assertEqual(word(after,0,3),4)
            self.assertNotIn(4,after['idle_student_ids'])
            self.assertEqual(after['group_raw_bytes'][14],1)
            self.assertEqual(after['derived_student_ids'][0],[-1,-1,-1,4])
            row = self.cases[f'waiting_empty_mode{mode}']
            self.assertIn('0x4a8bf0',row['movement']['visited_function_entries'])
            self.assertIn('0x4a95f0',row['movement']['visited_function_entries'])
            before,after,clean,rated = self.snapshots(f'waiting_replace_mode{mode}')
            self.assertEqual(word(after,0,0),4)
            self.assertIn(3,after['idle_student_ids'])
            self.assertNotIn(4,after['idle_student_ids'])
        self.assertEqual(self.snapshots('waiting_replace_mode0')[1]['idle_student_ids'],[9,3,5])
        self.assertEqual(self.snapshots('waiting_replace_mode2')[1]['idle_student_ids'],[5,3,9])

    def test_cross_class_move_exchange_and_later_cleanup(self):
        before,after,clean,rated = self.snapshots('class_empty_mode0')
        self.assertEqual(word(after,0,0),-1)
        self.assertEqual(word(after,1,3),3)
        self.assertEqual([after['group_raw_bytes'][g*28+14] for g in range(2)],[2,1])
        self.assertEqual([clean['group_raw_bytes'][g*28+14] for g in range(2)],[1,2])
        self.assertEqual(after['derived_student_ids'][0],before['derived_student_ids'][0])
        self.assertEqual(rated['derived_student_ids'][0],[-1,4,-1,-1])
        before,after,clean,rated = self.snapshots('class_exchange_mode0')
        self.assertEqual(word(after,0,0),9)
        self.assertEqual(word(after,1,0),3)
        self.assertEqual(set(after['idle_student_ids']),set(before['idle_student_ids']))

    def test_same_class_and_same_slot_exchange(self):
        self.assertEqual(word(self.snapshots('same_class_empty_mode0')[1],0,3),3)
        after = self.snapshots('same_class_exchange_mode0')[1]
        self.assertEqual([word(after,0,i) for i in range(2)],[4,3])
        before,after,_,_ = self.snapshots('same_slot_mode0')
        self.assertEqual(after['group_raw_bytes'],before['group_raw_bytes'])
        self.assertEqual(after['idle_student_ids'],before['idle_student_ids'])

    def test_teacherless_class_drop_is_outside_and_waiting_drop_is_noop(self):
        for mode in range(3):
            outside = self.snapshots(f'class_outside_mode{mode}')[1]
            teacherless = self.snapshots(f'class_teacherless_mode{mode}')[1]
            self.assertEqual(teacherless,outside)
            self.assertEqual(word(teacherless,0,0),-1)
            self.assertIn(3,teacherless['idle_student_ids'])
            for kind in ['waiting_outside','waiting_teacherless']:
                before,after,_,_ = self.snapshots(f'{kind}_mode{mode}')
                self.assertEqual(after['idle_student_ids'],before['idle_student_ids'])
                self.assertEqual(after['group_raw_bytes'],before['group_raw_bytes'])
                self.assertNotIn('0x4a8bf0',self.cases[f'{kind}_mode{mode}']['movement']['visited_function_entries'])

    def test_held_and_released_controls_are_distinct(self):
        for row in self.cases.values():
            before,after,_,_ = self.snapshots(row['name'])
            self.assertEqual(after['task_drag_state'],2)
            if row['command']['released']:
                for key in ['drag_kind','drag_origin','drag_group','drag_slot','drag_id']:
                    self.assertEqual(after[key],-1)
                self.assertEqual(after['task_command'],0)
            else:
                for key in ['drag_kind','drag_origin','drag_group','drag_slot','drag_id','task_command',
                            'group_raw_bytes','idle_student_ids','derived_student_ids']:
                    self.assertEqual(after[key],before[key])
                self.assertNotIn('0x4a95f0',row['movement']['visited_function_entries'])
                self.assertNotIn('0x4a8bf0',row['movement']['visited_function_entries'])
        self.assertEqual(self.snapshots('class_exchange_held')[1]['selected_group'],1)

    def test_cleanup_resets_sort_mode_and_only_defined_work_words_are_exported(self):
        for row in self.cases.values():
            before,after,clean,rated = self.snapshots(row['name'])
            self.assertEqual(after['idle_sort_mode'],before['idle_sort_mode'])
            self.assertEqual(clean['idle_sort_mode'],0)
            for rating in row['rating']['ratings']:
                self.assertEqual(len(rating['work_fields']),4 if rating['state'] in [2,4] else 0)

    def test_guard_and_declared_selection_refuse_unrelated_write_or_empty_source(self):
        emulator = StudentMovementEmulator([{'teacher':117},{'teacher':118}])
        with self.assertRaisesRegex(RuntimeError,'undeclared student drag write'):
            emulator._write_hook(emulator.uc,0,0x7A511C,4,1,None)
        with self.assertRaises(ValueError):
            emulator.run_movement('bad',0,0,1,0)
        for row in self.cases.values():
            for phase in ['movement','reconciliation','rating']:
                for write in row[phase]['native_writes']:
                    address,size = int(write['address'],16),write['size']
                    self.assertTrue(any(a <= address and address+size <= b for a,b in WRITE_RANGES))

    def test_no_live_campaign_or_teacher_movement_authority(self):
        for key in ['school_initialized','interactive_school_ready','live_witness','authorizes_persistent_write']:
            self.assertFalse(self.native[key])
        for row in self.cases.values():
            self.assertEqual(row['command']['kind'],'student')
            self.assertNotIn('0x4d48a0',row['movement']['visited_function_entries'])
            self.assertNotIn('0x4a2980',row['movement']['visited_function_entries'])


if __name__ == '__main__':
    unittest.main()
