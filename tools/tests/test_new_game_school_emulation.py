import hashlib
import json
import unittest

from tools.new_game_school_emulation import (
    ROOT, STATE, STATE_SIZE, CHAR, STRIDE, IDS, CALLS, AUTHORITY,
    NewGameSchoolEmulator, report, fixture, report_text, origin_rules)

REPORT = ROOT/'analysis/new-game-school-v1-20261006.json'
FIXTURE = ROOT/'prototype/data/new_game_school_evidence.json'


class NewGameSchoolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(REPORT.read_text('utf-8'))

    def test_report_and_export_regenerate_byte_exactly(self):
        data = report()
        self.assertEqual(report_text(data).encode(),REPORT.read_bytes())
        self.assertEqual(report_text(fixture(data)).encode(),FIXTURE.read_bytes())

    def test_source_inputs_are_call_template_and_relationship_fields(self):
        rules = self.data['origin_rules']
        self.assertEqual(rules,origin_rules())
        self.assertEqual([r['member_id'] for r in rules['calls']],IDS)
        self.assertEqual([r['call_va'] for r in rules['calls']],CALLS)
        self.assertEqual([r['slot'] for r in rules['calls']],[-1,0,1,2])
        self.assertEqual(rules['member_profiles'][0]['storage_kind'],'static_teacher_template')
        self.assertEqual(rules['member_profiles'][0]['attributes'],[1]*7)
        self.assertEqual(len(rules['relationships']),12)

    def test_full_initializer_calls_actual_join_and_bounded_memset(self):
        for case in self.data['cases']:
            for key in ['initialized','reinitialized']:
                if key not in case:
                    continue
                coverage = case[key]['coverage']
                self.assertIn('0x49e930',coverage['visited_function_entries'])
                self.assertIn('0x4d3d00',coverage['visited_function_entries'])
                self.assertIn('0x4e1ca0',coverage['visited_function_entries'])
                self.assertEqual([r['character_id'] for r in coverage['join_entries']],IDS)
                self.assertEqual([int(r['caller_return_va'],16) for r in coverage['join_entries']],
                                 [a+5 for a in CALLS])
                self.assertEqual(set(coverage['stub_calls']),{'debug_stack_check','bounded_new_game_state_memset'})
                event = coverage['boundary_events'][0]
                self.assertEqual((event['target'],event['byte'],event['count']),(hex(STATE),0,STATE_SIZE))
                self.assertEqual(coverage['native_write_count'],8058)

    def test_raw_zero_rosters_and_initial_derived_placement(self):
        s = self.data['cases'][0]['initialized']['after']
        self.assertEqual((s['month'],s['week'],s['difficulty'],s['global_total_511c']),(4,0,1,0))
        self.assertEqual((s['student_count'],s['teacher_count']),(3,1))
        self.assertEqual(s['raw_student_ids'],[3,4,9]+[0]*37)
        self.assertEqual(s['raw_teacher_ids'],[101]+[0]*19)
        self.assertEqual(s['student_ids'],[3,4,9]+[-1]*17)
        self.assertEqual(s['teacher_ids'],[101]+[-1]*19)
        self.assertEqual([i for i,v in enumerate(s['availability']) if v],[3,4,9,101])
        self.assertEqual(s['derived_teacher_ids'],[101]+[-1]*4)
        self.assertEqual(s['derived_teacher_indices'],[0]+[-1]*4)
        self.assertEqual(s['derived_student_ids'][0],[3,4,9,-1])
        self.assertEqual(s['derived_student_indices'][0],[0,1,2,-1])
        self.assertEqual(s['group_raw_bytes'][14],0)
        self.assertEqual((s['reset_groups'],s['selected_group']),(1,-1))
        self.assertEqual(s['course_unlocked_flags'],[0]*101)
        self.assertEqual(s['course_counts'],[0]*20)

    def test_join_recomputes_student_level_from_source_points_and_skills(self):
        rules = self.data['origin_rules']
        profiles = self.data['cases'][0]['initialized']['after']['member_profiles']
        self.assertEqual(profiles[0],rules['member_profiles'][0])
        for source,p in zip(rules['student_level_inputs'],profiles[1:]):
            statuses = list(source['skill_statuses'])
            for skill in source['equipped_skills']:
                if skill > 0:
                    statuses[skill-1] = 6
            total = sum(source['growth_pools'])+sum(v for v,s in zip(rules['learned_points'],statuses) if s in [3,5,6])
            level = 2
            while level < 51 and rules['level_thresholds'][level-1] <= total:
                level += 1
            self.assertEqual(p['level_50'],level-1)
        self.assertEqual(rules['member_profiles'][1]['level_50'],45)
        self.assertEqual(profiles[1]['level_50'],31)

    def test_separate_unlock_reconcile_rating_lifecycle(self):
        for case in self.data['cases']:
            initial = case.get('reinitialized',case['initialized'])['after']
            phases = case['preparation']
            self.assertEqual([r['phase'] for r in phases],['unlock','reconcile','rate'])
            unlocked,clean,rated = [p['after'] for p in phases]
            self.assertEqual(unlocked['course_counts'],[0]*20)
            self.assertEqual(unlocked['course_unlocked_flags'][100],1)
            self.assertEqual(unlocked['group_raw_bytes'],initial['group_raw_bytes'])
            self.assertEqual(clean['group_raw_bytes'][14],3)
            self.assertEqual(clean['group_raw_bytes'][3],0)
            self.assertEqual((clean['reset_groups'],clean['selected_group']),(0,0))
            self.assertEqual((rated['idle_student_ids'],rated['idle_teacher_ids']),([],[]))
            self.assertEqual(phases[-1]['ratings'][0],
                             {'state':3,'relationship_mean':65,'relationship_rank':5,'work_fields':[]})
            self.assertIn('0x4a2980',phases[1]['coverage']['visited_function_entries'])
            for state in [unlocked,clean,rated]:
                for key in ['month','week','difficulty','member_profiles','relationships','availability',
                            'teacher_ids','student_ids','raw_teacher_ids','raw_student_ids','global_total_511c']:
                    self.assertEqual(state[key],initial[key])

    def test_dirty_and_repeated_initialization_clear_courses_but_preserve_external_selection(self):
        a,b,c = self.data['cases']
        self.assertEqual(a['initialized']['after'],b['initialized']['after'])
        second = c['reinitialized']['after']
        self.assertEqual(second,dict(c['initialized']['after'],selected_group=0))
        self.assertEqual(second['course_unlocked_flags'],[0]*101)
        self.assertEqual(second['course_buffers'],[[] for _ in range(20)])

    def test_finite_write_guard_and_source_teacher_storage_not_student_record(self):
        emulator = NewGameSchoolEmulator()
        emulator.stage = 'initialize'
        for address in [STATE-1,STATE+STATE_SIZE,CHAR+101*STRIDE,0x6F5088+101*STRIDE,0x7D6A36]:
            with self.assertRaises(RuntimeError):
                emulator._write_hook(emulator.uc,0,address,1,0,None)
        emulator.stage = 'reconcile'
        for address in [0x7A528E,0x7A528A,CHAR+3*STRIDE,STATE]:
            with self.assertRaises(RuntimeError):
                emulator._write_hook(emulator.uc,0,address,2,0,None)
        for case in self.data['cases']:
            self.assertEqual(case['initialized']['coverage']['teacher_template_sha256'],
                             self.data['origin_rules']['member_profiles'][0]['template_sha256'])
        for key in AUTHORITY:
            self.assertFalse(self.data[key])
        self.assertEqual(fixture(self.data)['source_report_sha256'],hashlib.sha256(REPORT.read_bytes()).hexdigest())


if __name__ == '__main__':
    unittest.main()
