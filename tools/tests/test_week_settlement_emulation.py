"""Whole native week body, including participant unlocks and two cleanup passes."""
import hashlib
import importlib.util
import struct
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.week_settlement_emulation import report, WeekSettlementEmulator
    from tools.tactics_exit_emulation import ROOT, report_text


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class WeekSettlementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()
        cls.cases = {case['name']: case for case in cls.report['cases']}

    def test_full_state12_continuation_runs_all_three_helpers_and_requests_school(self):
        case = self.cases['special_all_result_week']
        result = case['all_result']
        self.assertEqual([e['state'] for e in result['dispatch_events'] if e['kind'] == 'state_request'],
                         [11, 10, 12, 6])
        self.assertFalse(result['bounded_stop'])
        self.assertIsNone(result['stop_reason'])
        events = case['week_events']
        self.assertEqual([e['va'] for e in events],
            ['0x4d3510']+['0x4d3aa0']*3+['0x4d31f0', '0x4d34a0']+['0x4d33a0']*3)
        self.assertEqual([e['character_id'] for e in events if e['va'] == '0x4d3aa0'], [3, 4, 9])
        self.assertEqual([e['character_id'] for e in events if e['va'] == '0x4d33a0'], [3, 4, 9])
        self.assertIn('0x4d3510', result['visited_original_addresses'])
        self.assertEqual(result['events'][-1]['sub'], 18)
        self.assertFalse(case['school_task_executed'])

    def test_calendar_probes_and_state12_path_are_distinguished(self):
        for name, expected in [('special_all_result_week', (15, 5)),
                ('ordinary_week_probe', (4, 5)), ('month_rollover_probe', (5, 1))]:
            case = self.cases[name]
            self.assertEqual((case['after_week']['month'], case['after_week']['week']), expected)
            self.assertTrue(case['native_week_body_executed'])
            self.assertFalse(case['authorizes_persistent_write'])
            if name != 'special_all_result_week':
                self.assertEqual(case['evidence_kind'], 'direct_week_function_probe')
                self.assertFalse(case['state12_executed'])
                self.assertNotIn('0x4c1aa0', case['visited_original_addresses'])

    def test_week_clears_and_sets_all_four_global_fields(self):
        for case in self.report['cases']:
            self.assertEqual(case['before_week']['flags'],
                             {'0x7a55fa': 9, '0x7a4e62': 8, '0x7a55f6': 2, '0x7e11a0': 99})
            self.assertEqual(case['after_week']['flags'],
                             {'0x7a55fa': 0, '0x7a4e62': 0, '0x7a55f6': 11, '0x7e11a0': 0})

    def test_inventory_cleanup_keeps_equipped_item_and_repairs_absent_or_unassigned_owners(self):
        for case in self.report['cases']:
            before, after = case['before_week']['item_flags'], case['after_week']['item_flags']
            self.assertEqual(before[:5], [0x301, 0x307, 0x407, 0x40B, 0x205])
            self.assertEqual(after[:5], [0x101, 0x307, 0x107, 0x10B, 0x205])
            self.assertEqual(before[5:], after[5:])

    def test_skill_cleanup_distinguishes_equipped_skill_and_leaves_equipment_unchanged(self):
        for case in self.report['cases']:
            before = case['before_week']['participants'][0]
            after = case['after_week']['participants'][0]
            self.assertEqual(before['skill_statuses'][:2], [6, 6])
            self.assertEqual(after['skill_statuses'][:2], [6, 5])
            self.assertEqual(before['equipped_skills'], after['equipped_skills'])
            self.assertEqual(before['equipped_items'], after['equipped_items'])
            self.assertEqual(before['attributes'], after['attributes'])
            self.assertEqual(before['job_progress'], after['job_progress'])

    def test_participant_unlocks_match_static_date_and_attribute_job_prerequisites(self):
        image = (ROOT / 'analysis/hermit_game.exe').read_bytes()
        for case in self.report['cases']:
            after = case['after_week']
            for original, actual in zip(case['before_week']['participants'], after['participants']):
                expected = original['unlock_flags'][:]
                for index in range(30):
                    base = 0x738CD3+(index+1)*0x32-0x400000
                    month, week = image[base], image[base+1]
                    dated = month != 0 and week != 0 and (original['job_progress'][index+1] == 100
                        or month*6+week <= after['month']*6+after['week'])
                    attrs = struct.unpack_from('<7h', image, base+3)
                    total = struct.unpack_from('<h', image, base+17)[0]
                    requirements = [(image[base+19+j*2], image[base+20+j*2]) for j in range(3)]
                    capable = all(a >= t for a, t in zip(original['attributes'], attrs)) \
                        and sum(original['attributes']) >= total \
                        and all(kind == 0 or original['job_progress'][kind] >= count for kind, count in requirements)
                    if dated or capable:
                        expected[index] = 1
                self.assertEqual(actual['unlock_flags'], expected)
                self.assertIn(1, actual['unlock_flags'])

    def test_nonparticipants_availability_and_original_source_edges_are_preserved(self):
        for case in self.report['cases']:
            for key in ('availability', 'nonparticipant_character_sha256', 'nonparticipant_package_sha256'):
                self.assertEqual(case['before_week'][key], case['after_week'][key])
        image = (ROOT / 'analysis/hermit_game.exe').read_bytes()
        for call, target in ((0x4D35B3, 0x4D3AA0), (0x4D35C5, 0x4D31F0),
                (0x4D35CF, 0x4D34A0), (0x4D32A0, 0x4D46E0), (0x4D34F6, 0x4D33A0)):
            at = call-0x400000
            self.assertEqual(image[at], 0xE8)
            self.assertEqual(call+5+struct.unpack_from('<i', image, at+1)[0], target)

    def test_report_reexecutes_and_adds_no_week_external_stubs(self):
        path = ROOT / 'analysis/week-settlement-v1-20261002.json'
        self.assertEqual(path.read_bytes().decode(), report_text(self.report))
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), REPORT_SHA256)
        self.assertEqual(self.report['additional_stub_manifest'], [])
        self.assertFalse(self.report['authorizes_persistent_write'])

    def test_probe_calendar_rejects_unsafe_dates(self):
        emulator = WeekSettlementEmulator()
        for month, week in [(3, 1), (16, 1), (4, 0), (4, 6), (4.0, 1)]:
            with self.assertRaises(ValueError):
                emulator.probe_calendar('bad', month, week)

    def test_unlock_date_sentinel_and_exact_attribute_job_boundary(self):
        from tools.battle_preparation_emulation import CHAR_BASE, CHAR_STRIDE, PACKAGE_BASE, PACKAGE_STRIDE
        # Original template is below the 700 total-attribute fallback threshold.
        before_date = WeekSettlementEmulator()
        before_date.write(0x7A5290, 2, 'h')
        before_date.call(0x4D3AA0, (3,))
        self.assertEqual(before_date.week_snapshot()['participants'][0]['unlock_flags'][:10], [0]*10)
        sentinel = WeekSettlementEmulator()
        sentinel.write(0x7A5290, 2, 'h')
        sentinel.write(PACKAGE_BASE+3*PACKAGE_STRIDE+0xD8, 100, 'B')
        sentinel.call(0x4D3AA0, (3,))
        self.assertEqual(sentinel.week_snapshot()['participants'][0]['unlock_flags'][:10], [1]+[0]*9)
        for progress, expected in [(14, 0), (15, 1)]:
            emulator = WeekSettlementEmulator()
            emulator.write(0x7A5290, 2, 'h')
            for k, value in enumerate([75, 0, 0, 0, 0, 75, 50]):
                emulator.write(CHAR_BASE+3*CHAR_STRIDE+0xC+k*8, value, 'B')
            emulator.write(PACKAGE_BASE+3*PACKAGE_STRIDE+0xD8, progress, 'B')
            emulator.call(0x4D3AA0, (3,))
            self.assertEqual(emulator.week_snapshot()['participants'][0]['unlock_flags'][10], expected)


REPORT_SHA256 = 'f4d954f44de9b0c95a4747e8a92bbb0c55a42f047c4123ca20ec28a9019a2364'


if __name__ == '__main__':
    unittest.main()
