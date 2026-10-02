"""State7 advances the whole week before the presentation completion gate."""
import hashlib
import importlib.util
import struct
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.week_start_emulation import WeekStartEmulator, report
    from tools.week_start_fixture import fixture, REPORT, REPORT_SHA256
    from tools.tactics_exit_emulation import ROOT, SOURCE, report_text


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class WeekStartTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()
        cls.cases = {c['name']: c for c in cls.report['cases']}

    def test_report_and_fixture_reproduce_independent_native_bytes(self):
        self.assertEqual(REPORT.read_text(encoding='utf-8'), report_text(self.report))
        self.assertEqual(hashlib.sha256(REPORT.read_bytes()).hexdigest(), REPORT_SHA256)
        self.assertNotIn(b'\r', REPORT.read_bytes())
        path = ROOT / 'prototype/data/week_start_evidence.json'
        self.assertEqual(path.read_text(encoding='utf-8'), report_text(fixture()))

    def test_ordinary_and_month_end_execute_full_week_before_ch001_request(self):
        for name, date in [('ordinary_week_start', (4, 5)), ('month_rollover_week_start', (5, 1))]:
            case = self.cases[name]
            after = case['after_week']
            self.assertEqual((after['month'], after['week']), date)
            self.assertEqual(case['week_events'][0], {'va': '0x4d3510', 'caller_return_va': '0x49f507'})
            self.assertEqual([e['va'] for e in case['week_events']], ['0x4d3510']+['0x4d3aa0']*3
                +['0x4d31f0', '0x4d34a0']+['0x4d33a0']*3)
            self.assertEqual(after['participants'][0]['skill_statuses'][:2], [6, 5])
            self.assertEqual(after['item_flags'][:5], [0x101, 0x307, 0x107, 0x10B, 0x205])
            self.assertEqual([e['kind'] for e in case['start_events']],
                             ['fade_start', 'fade_ready', 'fade_release', 'script_load_boundary', 'state_request'])
            self.assertEqual(case['start_events'][0]['frames'], 90)
            self.assertEqual((case['pending_flag'], case['requested_state']), (1, 6))

    def test_busy_fade_preserves_applied_week_and_blocks_script_and_state_request(self):
        case = self.cases['fade_busy_after_week']
        self.assertTrue(case['bounded_stop'])
        self.assertEqual(case['after_week'], self.cases['month_rollover_week_start']['after_week'])
        self.assertEqual((case['pending_flag'], case['requested_state']), (0, 7))
        self.assertEqual([e['kind'] for e in case['start_events']], ['fade_start']+['fade_ready']*5)
        self.assertEqual(len([e for e in case['week_events'] if e['va'] == '0x4d3510']), 1)

    def test_script_request_has_next_state8_without_claiming_school_initialization(self):
        for case in self.cases.values():
            for event in case['start_events']:
                if event['kind'] == 'script_load_boundary':
                    self.assertEqual((event['path'], event['next_task_state']), ('Data\\Adv\\dat\\CH001.ybc', 8))
            for key in ('adv_script_executed', 'school_initialized', 'live_witness', 'authorizes_persistent_write'):
                self.assertFalse(case[key])
            for key in ('nonparticipant_character_sha256', 'nonparticipant_package_sha256'):
                self.assertEqual(case['before_week'][key], case['after_week'][key])

    def test_original_state7_and_state18_dispatch_operands_are_distinct(self):
        image = SOURCE.read_bytes()
        for state, address, target in [(7, 0x49E339, 0x49F570), (18, 0x49E3D0, 0x4FB1E0)]:
            self.assertEqual(struct.unpack_from('<I', image, 0x49E4D3-0x400000+state*4)[0], address)
            offset = address-0x400000
            self.assertEqual(image[offset], 0xE8)
            self.assertEqual(address+5+struct.unpack_from('<i', image, offset+1)[0], target)
        self.assertEqual(struct.unpack_from('<I', image, 0x5A0824-0x400000)[0], 0x49F4E0)
        offset = 0x49F502-0x400000
        self.assertEqual(image[offset], 0xE8)
        self.assertEqual(0x49F507+struct.unpack_from('<i', image, offset+1)[0], 0x4D3510)

    def test_unknown_calendar_is_rejected_before_execution(self):
        for month, week in [(3, 1), (15, 5), (4, 0), (4, 6), (4.5, 1)]:
            with self.assertRaises(ValueError):
                WeekStartEmulator().run('bad', month, week)


if __name__ == '__main__':
    unittest.main()
