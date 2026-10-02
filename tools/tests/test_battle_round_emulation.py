"""Native state10 branching and necessary roster writes, excluding unit derivation."""
import hashlib
import importlib.util
import json
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.battle_round_emulation import report, godot_fixture, RoundEmulator
    from tools.tactics_exit_emulation import ROOT, report_text


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class BattleRoundEmulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()
        cls.cases = {case['name']: case for case in cls.report['cases']}

    def test_same_instance_requests_eleven_ten_and_next_branch(self):
        for name, state, caller in (('all_complete', 12, '0x4b902f'),
                                    ('next_round', 16, '0x4b90ea'),
                                    ('empty_complete', 12, '0x4b902f')):
            case = self.cases[name]
            events = [event for event in case['dispatch_events'] if event['kind'] == 'state_request']
            self.assertEqual([event['state'] for event in events], [11, 10, state])
            self.assertEqual(events[-1]['caller_return_va'], caller)
            self.assertEqual((case['requested_state'], case['request_pending']), (state, 0))
            self.assertTrue(case['state10_dispatched_in_emulation'])
            self.assertIn('0x4b8ff0', case['visited_original_addresses'])
            self.assertEqual(case['round_events'][-1]['va'],
                             '0x4c1d30' if state == 12 else '0x451080')

    def test_completed_rounds_preserve_all_sentinel_fields(self):
        for name in ('all_complete', 'empty_complete'):
            case = self.cases[name]
            self.assertEqual(case['before'], case['after'])
            for va in ('0x4da860', '0x4b9210', '0x4b9270', '0x4b92c0'):
                self.assertNotIn(va, case['visited_original_addresses'])
            self.assertNotIn('unresolved_combat_unit_derivation', case['stub_calls'])

    def test_next_round_loads_configuration_resets_roster_and_increments_once(self):
        case = self.cases['next_round']
        self.assertEqual(case['after']['temp_roster'], [3, 4, 9]+[-1]*97)
        self.assertEqual((case['after']['temp_count'], case['after']['combat_count']), (3, 3))
        self.assertEqual((case['after']['current'], case['after']['total']), (2, 2))
        self.assertEqual(case['after']['scene_id'], 5)
        events = case['round_events']
        native = [event for event in events if event['kind'] == 'native_entry']
        self.assertEqual([event['va'] for event in native],
                         ['0x4b8ff0', '0x4da860', '0x4b9210']+['0x4b9270']*3+['0x4b92c0'])
        self.assertEqual([event['argument'] for event in native if event['va'] == '0x4b9270'], [3, 4, 9])
        units = [event for event in events if event['kind'] == 'unresolved_combat_unit_derivation']
        self.assertEqual([(event['character_id'], event['ordinal']) for event in units],
                         [(3, 0), (4, 1), (9, 2)])
        self.assertIn('0x4da8e0', case['visited_original_addresses'])

    def test_unsafe_audit_inputs_are_rejected_before_thread_execution(self):
        emulator = RoundEmulator()
        for current, total, roster, config in ((2, 1, [], 5), (0, 6, [], 5), (1.5, 2, [], 5),
                                              (0, 1, [-1], 5), (0, 1, [3]*21, 5),
                                              (0, 1, [3], 6)):
            with self.assertRaises(ValueError):
                emulator.run_round('invalid', current, total, roster, config)
        self.assertEqual(emulator.round_events, [])
        self.assertEqual(emulator.dispatch_events, [])

    def test_reports_reproduce_and_do_not_claim_full_preparation_or_school(self):
        raw = (ROOT / 'analysis/battle-round-gate-v1-20261002.json').read_bytes()
        self.assertEqual(raw.decode(), report_text(self.report))
        fixture = json.loads((ROOT / 'prototype/data/battle_round_execution_evidence.json').read_text())
        self.assertEqual(fixture, godot_fixture(self.report))
        self.assertEqual(fixture['source_report_sha256'], hashlib.sha256(raw).hexdigest())
        for case in self.report['cases']:
            for key in ('preparation_resolved', 'combat_units_ready', 'live_witness',
                        'authorizes_persistent_write'):
                self.assertFalse(case[key])
            for va in ('0x4b9340', '0x4c1d30', '0x451080', '0x4c1aa0', '0x4d3510'):
                self.assertNotIn(va, case['visited_original_addresses'])


if __name__ == '__main__':
    unittest.main()
