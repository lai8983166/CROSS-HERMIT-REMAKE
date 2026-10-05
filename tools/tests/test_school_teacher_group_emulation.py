"""Teacher and group rules are observed in original CPU execution."""
import hashlib
import importlib.util
import struct
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.school_teacher_group_emulation import report, fixture, CHAPTER, CHAPTER_SHA, TeacherGroupEmulator
    from tools.tactics_exit_emulation import ROOT, report_text

REPORT_SHA = 'bc7c37d43d8ab8027bd4f6b3e21705bfaa2afdb7c1b3a77de9ea4f7ae282263e'
FIXTURE_SHA = '431b323a590d30af500806a390679c64e3d7315489b5e0b722fc2f38b56638e4'


@unittest.skipUnless(HAS_UNICORN, 'requires audit dependencies')
class TeacherGroupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.native = report()
        cls.cases = {c['name']: c for c in cls.native['cases']}

    def test_report_and_export_reproduce_exactly(self):
        for name, data, sha in [('analysis/school-teacher-group-v1-20261006.json',self.native,REPORT_SHA),
                               ('prototype/data/school_teacher_group_evidence.json',fixture(self.native),FIXTURE_SHA)]:
            raw = (ROOT/name).read_bytes()
            self.assertEqual(raw, report_text(data).encode('utf-8'))
            self.assertEqual(hashlib.sha256(raw).hexdigest(),sha)
            self.assertNotIn(b'\r',raw)

    def test_actual_chapter_prefix_reaches_teacher_join_not_synthetic_end(self):
        source = CHAPTER.read_bytes()
        self.assertEqual(hashlib.sha256(source).hexdigest(), CHAPTER_SHA)
        self.assertEqual(struct.unpack_from('<HHI',source,20), (144,8,0x20000075))
        c = self.cases['chapter012_teacher_enables_existing_group']
        for address in ('0x4ce8f0','0x4d0900','0x4d3e90','0x4d4730'):
            self.assertIn(address,c['join_visited_addresses'])
        self.assertEqual((c['vm_pc'],c['vm_active']), (8,1))
        self.assertEqual(c['join_entries'][0]['character_id'],117)
        self.assertEqual((c['join_entries'][0]['group'],c['join_entries'][0]['slot']),(-1,-1))

    def test_registration_duplicate_and_direct_placement(self):
        duplicate = self.cases['chapter012_teacher_duplicate']
        self.assertEqual(duplicate['after_join_once'],duplicate['after_join'])
        self.assertEqual(duplicate['after_join']['teacher_count'],1)
        self.assertEqual(duplicate['after_join']['availability'][117],1)
        no_op = self.cases['teacher_already_available']
        self.assertEqual(no_op['before'],no_op['after_join'])
        direct = self.cases['direct_helper_places_teacher']
        self.assertEqual(direct['after_join']['derived_teacher_ids'][0],117)
        self.assertEqual(direct['after_join']['derived_teacher_indices'][0],0)
        self.assertNotIn('0x4d0900',direct['join_visited_addresses'])

    def test_reconciliation_executes_native_helpers_and_preserves_other_fields(self):
        for c in self.cases.values():
            for address in ('0x4a5f40','0x4ab250','0x4a95f0','0x4d46e0'):
                self.assertIn(address,c['visited_original_addresses'])
            for stage in ('after_join_once','after_join','after_reconcile','after_ratings'):
                for key in ('student_count','student_ids','month','week','global_total_511c','student_record_sha256','relationships'):
                    self.assertEqual(c[stage][key],c['before'][key],(c['name'],stage,key))
            for key in ('group_raw_bytes','availability','idle_student_ids','idle_teacher_ids'):
                self.assertEqual(c['after_reconcile'][key],c['after_ratings'][key])

    def test_teacherless_and_unavailable_groups_clear_but_students_remain_waiting(self):
        for name in ('unavailable_teacher_clears_group','teacherless_students_clear'):
            c=self.cases[name]
            raw=bytes(c['after_reconcile']['group_raw_bytes'])
            self.assertEqual(struct.unpack_from('<h',raw,0)[0],-1)
            self.assertEqual(struct.unpack_from('<4h',raw,16),(-1,)*4)
            self.assertEqual(c['after_reconcile']['idle_student_ids'],[3,4,9,5])
            self.assertEqual(c['ratings'][0]['defined'],{'state':0,'relationship_mean':0,'relationship_rank':0,'work_fields':[]})

    def test_unavailable_and_duplicate_student_cleanup(self):
        c=self.cases['unavailable_student_clears']
        raw=bytes(c['after_reconcile']['group_raw_bytes'])
        self.assertEqual(struct.unpack_from('<4h',raw,16),(3,-1,-1,-1))
        self.assertEqual(c['after_ratings']['derived_student_indices'][0],[0,-1,-1,-1])
        c=self.cases['duplicate_student_first_wins']
        self.assertEqual(struct.unpack_from('<4h',bytes(c['after_reconcile']['group_raw_bytes']),44),(-1,5,-1,-1))
        self.assertEqual(c['after_reconcile']['idle_student_ids'],[9])
        self.assertEqual(c['after_ratings']['derived_teacher_indices'],[0,1,-1,-1,-1])

    def test_all_states_and_only_initialized_work_words(self):
        names=['teacherless_students_clear','teacher_only','active_lecture_state2',
               'chapter012_teacher_enables_existing_group','assigned_adventure_state4','missing_adventure_state5']
        self.assertEqual([self.cases[n]['ratings'][0]['defined']['state'] for n in names],list(range(6)))
        for c in self.cases.values():
            for rating in c['ratings']:
                expected=rating['raw_words'][3:] if rating['raw_words'][0] in (2,4) else []
                self.assertEqual(rating['defined']['work_fields'],expected)
        self.assertEqual(self.cases['active_lecture_state2']['ratings'][0]['defined']['work_fields'],[7,2,3,4])

    def test_directed_means_and_all_rank_thresholds(self):
        c=self.cases['asymmetric_relationship_mean']
        self.assertEqual(c['ratings'][0]['defined']['relationship_mean'],301//6)
        self.assertIn('0x4d3a20',c['visited_original_addresses'])
        for v in (15,16,30,31,45,46,60,61,75,76,90,91):
            expected=1+sum(v>=t for t in (16,31,46,61,76,91))
            rating=self.cases[f'rank_boundary_{v}']['ratings'][0]['defined']
            self.assertEqual((rating['relationship_mean'],rating['relationship_rank']),(v,expected))

    def test_reset_group_bytes_and_opaque_bytes(self):
        c=self.cases['reset_groups_clears_work']
        before,after=c['before']['group_raw_bytes'],c['after_reconcile']['group_raw_bytes']
        self.assertEqual(after[3],0)  # Source unconditionally restores lecture mode for available teacher.
        self.assertEqual(after[4],255)
        self.assertEqual(after[6:10],[255]*4)
        self.assertEqual(after[10:14],before[10:14])
        for c in self.cases.values():
            for g in range(5):
                for offset in (2,5,15,24,25,26,27):
                    self.assertEqual(c['before']['group_raw_bytes'][g*28+offset],c['after_ratings']['group_raw_bytes'][g*28+offset])

    def test_external_teacher_identity_maps_to_relationship_coordinate(self):
        x=TeacherGroupEmulator(teachers=[117],groups=[{'teacher':117,'students':[3]}])
        self.assertEqual(x.matrix_id(117),62)
        self.assertEqual(x.read(0x7D3D71+62*68+3,'B'),50)
        self.assertEqual(x.read(0x7D3D71+3*68+62,'B'),50)

    def test_no_live_work_selection_drag_or_save_claim(self):
        for flag in ('school_initialized','interactive_school_ready','live_witness','authorizes_persistent_write'):
            self.assertFalse(self.native[flag])
        for c in self.cases.values():
            self.assertNotIn('0x4a4680',c['visited_original_addresses'])
            self.assertNotIn('0x4a2980',c['visited_original_addresses'])


if __name__=='__main__':
    unittest.main()
