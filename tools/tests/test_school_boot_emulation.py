"""School boot fields must come from original initialization, not a request9 flag."""
import hashlib
import importlib.util
import json
import struct
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.school_boot_emulation import report, SchoolBootEmulator, BOOT_NATIVE, GROUP_TASK, PERSON_TASK
    from tools.tactics_exit_emulation import ROOT, SOURCE, report_text

REPORT_SHA256 = '1537a81c4d92732464a1ce8182628b1e07a9b85ce469598784707da86514359a'


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class SchoolBootTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()
        cls.cases = {c['name']: c for c in cls.report['cases']}

    def test_exact_native_report_and_all_resource_hashes(self):
        path = ROOT / 'analysis/school-boot-v1-20261003.json'
        self.assertEqual(path.read_text(encoding='utf-8'), report_text(self.report))
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), REPORT_SHA256)
        self.assertNotIn(b'\r', path.read_bytes())
        for c in self.cases.values():
            for event in c['boot_events']:
                if 'path' in event:
                    source = ROOT / 'CROSS HERMIT/CROSS HERMIT' / event['path']
                    self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), event['source_sha256'])

    def test_godot_projection_fixture_is_exported_from_native_reexecution_and_source_templates(self):
        from tools.school_boot_fixture import fixture
        path = ROOT / 'prototype/data/school_boot_evidence.json'
        self.assertEqual(path.read_text(encoding='utf-8'), report_text(fixture(self.report)))
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                         '066ac6af7eb1f8b4b5a8b7d363cff5fcb62760652065b06fc9cf77cb8546301e')
        data = json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(data['native_report_sha256'], REPORT_SHA256)
        self.assertEqual([c['expected_supported'] for c in data['cases']], [True, True, False])
        self.assertEqual([len(data['boot_rules'][k]) for k in ('adventures', 'lectures')], [100, 100])
        self.assertEqual(data['boot_rules']['adventures'][7], {'id': 8, 'present': 1,
            'month': 5, 'week': 1, 'duration': 5, 'kind': 2, 'subkind': 2, 'gate': 1})
        for flag in ('school_initialized', 'interactive_school_ready', 'live_witness', 'authorizes_persistent_write'):
            self.assertFalse(data[flag])

    def test_full_same_cpu_predecessor_and_complete_native_group_initialization(self):
        prior = json.loads((ROOT/'analysis/school-dispatch-v1-20261003.json').read_text(encoding='utf-8'))['cases']
        for c, predecessor in zip(self.report['cases'], [prior[0], prior[1], prior[3]]):
            snapshot = c['before'].copy()
            snapshot.pop('school_control')
            self.assertEqual(snapshot, predecessor['after'])
        for name in ('first_school_boot', 'visited_school_boot'):
            c = self.cases[name]
            self.assertTrue(c['group_initialized'])
            self.assertTrue(c['person_resource_initialized'])
            self.assertEqual(c['person_idle_yields'], 2)
            self.assertEqual(c['stop_reason'], 'school_person_idle_boundary')
            for va in ('0x4ab7a0','0x4a5ce0','0x4a5a60','0x4a1c70','0x4a5f40',
                       '0x4a9ab0','0x4a17b0','0x4a2ba0','0x4a8bf0','0x4b8d50','0x4d46e0'):
                self.assertIn(va, c['visited_original_addresses'])
            for va in ('0x4a7c40','0x4b5600','0x4b5a00','0x4b5fc0'):
                self.assertNotIn(va, c['visited_original_addresses'])
            self.assertEqual([e['kind'] for e in c['boot_events'] if e['kind'].startswith('native_')],
                             ['native_group_body', 'native_person_body'])

    def test_unavailable_teacher_clears_groups_and_rebuilds_sorted_waiting_list_without_losing_students(self):
        for name in ('first_school_boot', 'visited_school_boot'):
            c = self.cases[name]
            after = c['after']
            self.assertEqual(after['group_student_ids'], [[-1]*4 for _ in range(5)])
            self.assertEqual(after['group_student_indices'], [[-1]*4 for _ in range(5)])
            self.assertEqual(after['student_ids'], c['before']['student_ids'])
            self.assertEqual(after['student_count'], 4)
            control = after['school_control']
            ids = after['student_ids'][:4]
            levels = {p['character_id']: p['level_50'] for p in after['participants']}
            self.assertEqual(control['idle_student_ids'], sorted(ids, key=lambda i: levels[i], reverse=True))
            self.assertEqual(control['idle_teacher_ids'], [])
            self.assertEqual(control['selected_group'], -1)
            self.assertEqual(control['group_task_controls'], [0, 1, 1, 2, 0])
            self.assertEqual((control['person_phase'], control['person_ready'], control['person_selection']), (0, 1, -1))

    def test_all_eight_rank_columns_come_from_persistent_attributes_and_total(self):
        for name in ('first_school_boot', 'visited_school_boot'):
            c = self.cases[name]
            records = {p['character_id']: p for p in c['before']['participants']}
            values = [records[i]['attributes']+[sum(records[i]['attributes'])] for i in c['before']['student_ids'][:4]]
            expected = [[1+sum(other[column] > row[column] for other in values) for column in range(8)] for row in values]
            self.assertEqual(c['after']['school_control']['group_rankings'], expected)

    def test_lecture_unlocks_use_original_six_step_date_comparison_and_adventure_rows(self):
        source = SOURCE.read_bytes()
        for name in ('first_school_boot', 'visited_school_boot'):
            c = self.cases[name]
            before, after = c['before']['school_control'], c['after']['school_control']
            expected = before['lecture_unlock_flags'].copy()
            for index in range(1, 101):
                a = 0x74BED0+index*0x60-0x400000
                month, week = struct.unpack_from('<BB', source, a+2)
                kind, subkind = struct.unpack_from('<hh', source, a+6)
                if month*6+week <= 31 and kind != 0 and subkind != 0:
                    expected[index-1] = 1
            self.assertEqual(after['lecture_unlock_flags'], expected)
            self.assertEqual(after['lecture_counts'], [0,0,0])
            self.assertEqual(after['adventure_counts'], [0,0,1])
            self.assertEqual([i+1 for i,v in enumerate(after['adventure_unlock_flags']) if v], [8])
            self.assertEqual(after['adventure_entries'][0:2], [[], []])
            template = 0x73BED0+8*0x100-0x400000
            self.assertEqual(list(source[template+2:template+4]), [5, 1])
            # 4A9D90 copies category/type minus one, ID, duration and work
            # index. The first two list columns are NOT the unlock calendar.
            self.assertEqual(after['adventure_entries'][2][0],
                             [source[template+6]-1, source[template+7]-1, 8, source[template+5], 0])

    def test_school_boot_preserves_whole_roles_calendar_music_and_pending9_without_new_week(self):
        for c in self.cases.values():
            for key,value in c['before'].items():
                if key not in ('group_student_ids', 'group_student_indices', 'school_control'):
                    self.assertEqual(c['after'][key], value, key)
            self.assertEqual(c['school_state_requests'], [])
            for flag in ('school_initialized','interactive_school_ready','live_witness','authorizes_persistent_write'):
                self.assertFalse(c[flag])
        first, visited = self.cases['first_school_boot'], self.cases['visited_school_boot']
        self.assertEqual((first['pending_flag'],first['pending_state']), (0,9))
        self.assertEqual((visited['pending_flag'],visited['pending_state']), (0,9))
        self.assertEqual([e['music'] for e in first['boot_events'] if e['kind']=='music_api_boundary'], [11])
        self.assertEqual([e for e in visited['boot_events'] if e['kind']=='music_api_boundary'], [])

    def test_unfinished_ch002_cannot_start_school_boot(self):
        c = self.cases['ch002_wait_blocks_boot']
        self.assertFalse(c['group_initialized'])
        self.assertFalse(c['person_resource_initialized'])
        self.assertEqual(c['person_idle_yields'], 0)
        self.assertEqual(c['boot_events'], [])
        self.assertEqual(c['before'], c['after'])
        self.assertFalse(c['upstream']['school_constructed'])

    def test_missing_constructor_chain_and_repeat_initialization_reject_before_fields(self):
        x = SchoolBootEmulator()
        x._function_ranges += BOOT_NATIVE
        before = x.boot_snapshot()
        x.phase = 'school_group_boot'
        with self.assertRaisesRegex(RuntimeError, 'both actual school constructors'):
            x._thread(0x4AB7A0, GROUP_TASK)
        self.assertEqual(x.boot_snapshot(), before)
        x.phase = 'school_person_boot'
        with self.assertRaisesRegex(RuntimeError, 'native group initialization'):
            x._thread(0x4B8D50, PERSON_TASK)
        self.assertEqual(x.boot_snapshot(), before)
        self.assertEqual(x.boot_events, [])
        x._ran_boot = True
        with self.assertRaisesRegex(RuntimeError, 'single-run'):
            x.run_boot('again')
        self.assertEqual(x.boot_snapshot(), before)


if __name__ == '__main__':
    unittest.main()
