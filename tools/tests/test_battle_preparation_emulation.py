"""Native task-five calculation invariants and stable byte-level evidence."""
import hashlib
import importlib.util
import struct
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.battle_preparation_emulation import report, PreparationEmulator
    from tools.tactics_exit_emulation import ROOT, report_text


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class BattlePreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()
        cls.cases = {c['name']: c for c in cls.report['cases']}

    def test_native_input_and_three_preparation_bodies_execute_in_order(self):
        for case in self.report['cases']:
            self.assertEqual([e['va'] for e in case['preparation_events']],
                             ['0x473860', '0x4bd210', '0x4bca40', '0x4bbd40'])
            self.assertEqual([e['caller_return_va'] for e in case['preparation_events'][1:]],
                             ['0x4bbce5', '0x4bbced', '0x4bbcf5'])
            self.assertTrue(case['native_preparation_executed'])
            self.assertEqual([e['state'] for e in case['dispatch_events'] if e['kind'] == 'state_request'], [11, 10])
            self.assertEqual(case['requested_state'], 10)
            for name in case['stub_calls']:
                self.assertFalse(name.startswith('unresolved_result_'))
            for va in ('0x4d56a0', '0x4d58e0', '0x56e230', '0x570fd0', '0x570fe0'):
                self.assertIn(va, case['visited_original_addresses'])

    def test_character_templates_pools_and_nonparticipants_are_unchanged(self):
        for case in self.report['cases']:
            self.assertEqual(case['before']['nonparticipant_package'], case['after']['nonparticipant_package'])
            for before, after in zip(case['before']['characters'], case['after']['characters']):
                self.assertEqual(before['character_id'], after['character_id'])
                self.assertEqual(before['character_record_sha256'], after['character_record_sha256'])
                self.assertEqual(before['growth_pools'], after['growth_pools'])
                self.assertEqual(after['staged_total'], sum(after['staged_package'][:7]))
                self.assertTrue(all(value >= 0 for value in after['staged_package']))
            summary = case['result_summary']
            self.assertEqual(summary['display_character_ids'][:3], [3, 4, 9])
            self.assertEqual(summary['display_packages'][:3],
                             [c['staged_total'] for c in case['after']['characters']])
            self.assertEqual(summary['display_packages'][3:], [0]*17)

    def test_grade_display_and_global_total_are_not_conflated_with_unit_packages(self):
        for name, grade, total, packages in (
                ('task5_sub2', 1, 79486, [93957, 102057, 65607]),
                ('task5_selector14_sub8', 5, 24254, [27839, 30239, 19438])):
            case = self.cases[name]
            summary = case['result_summary']
            self.assertEqual(case['after']['task_grade'], grade)
            self.assertEqual(summary['grade_index'], grade-1)
            self.assertEqual(case['after']['round_grade_index'], grade-1)
            self.assertEqual(summary['total_after'], total)
            self.assertEqual(case['after']['global_total_511c'], total)
            self.assertEqual(summary['total_before']+summary['total_delta'], total)
            self.assertEqual(summary['display_packages'][:3], packages)
            self.assertEqual((summary['unit_count'], summary['sum_count_field_aa'],
                              summary['sum_contribution_field_ac'], summary['sum_status_field_ae']), (3, 30, 100, 3))
        self.assertEqual(self.cases['task5_sub2']['result_summary']['time_display'], 0)
        self.assertEqual(self.cases['task5_selector14_sub8']['result_summary']['time_display'], 3)

    def test_cap_probe_removes_only_capped_characters_package(self):
        normal = self.cases['task5_sub2']
        capped = self.cases['character3_cap_probe']
        self.assertEqual(capped['after']['characters'][0]['staged_package'], [0]*8)
        self.assertEqual(capped['after']['characters'][0]['staged_total'], 0)
        self.assertEqual(capped['after']['characters'][1:], normal['after']['characters'][1:])
        self.assertEqual(capped['after']['global_total_511c'], 98277)
        self.assertEqual(capped['after']['item_flags'], normal['after']['item_flags'])

    def test_loot_flags_match_display_candidates_and_native_seeded_rand(self):
        expected = {'task5_sub2': [12, 32, 37, 39, 62, 89],
                    'task5_selector14_sub8': [11, 23],
                    'character3_cap_probe': [12, 32, 37, 39, 62, 89]}
        for name, case in self.cases.items():
            items = case['after']['item_flags']
            self.assertEqual([item['item_id'] for item in items], expected[name])
            self.assertTrue(all(item['flags'] == 0x101 for item in items))
            displayed = sorted(item for group in case['result_summary']['loot_groups'] for item in group if item)
            self.assertEqual(displayed, expected[name])
            state = case['synthetic_inputs']['clock_seed']
            for _ in range(case['stub_calls']['isolated_crt_thread_data']-1):
                state = (state*214013+2531011) & 0xFFFFFFFF
            self.assertEqual(case['native_rand_state'], state)
            self.assertEqual(case['stub_calls']['declared_clock_seed'], 1)

    def test_participant_initialization_does_not_overwrite_nearby_task_counters(self):
        emulator = PreparationEmulator()
        self.assertEqual(emulator.read(0x7A5294, 'h'), 5)
        self.assertEqual(emulator.read(0x7A5296, 'h'), 1)
        self.assertEqual(emulator.read(0x7A5298, 'h'), 1)
        self.assertEqual(emulator.read(0x7A528E, 'h'), 4)
        self.assertEqual(emulator.read(0x7A5290, 'h'), 5)
        self.assertEqual([emulator.read(0x7A5210+i*2, 'h') for i in range(20)], [3, 4, 9]+[-1]*17)

    def test_original_prepare_calls_and_character_template_hashes(self):
        image = (ROOT / 'analysis/hermit_game.exe').read_bytes()
        for call, target in ((0x4BBCE0, 0x4BD210), (0x4BBCE8, 0x4BCA40), (0x4BBCF0, 0x4BBD40),
                             (0x4BCA48, 0x56E230), (0x4D1CCD, 0x570FE0)):
            at = call-0x400000
            self.assertEqual(image[at], 0xE8)
            self.assertEqual(call+5+struct.unpack_from('<i', image, at+1)[0], target)
        for template in self.cases['task5_sub2']['synthetic_inputs']['character_templates']:
            at = int(template['template_va'], 16)-0x400000
            self.assertEqual(hashlib.sha256(image[at:at+0x4A0]).hexdigest(), template['template_sha256'])

    def test_canonical_report_reexecutes_without_persistent_application(self):
        self.assertEqual((ROOT / 'analysis/battle-preparation-v1-20261002.json').read_bytes().decode(),
                         report_text(self.report))
        for case in self.report['cases']:
            self.assertFalse(case['authorizes_persistent_write'])
            self.assertFalse(case['live_witness'])
            for va in ('0x4c1aa0', '0x4c1350', '0x4d3510'):
                self.assertNotIn(va, case['visited_original_addresses'])


if __name__ == '__main__':
    unittest.main()
