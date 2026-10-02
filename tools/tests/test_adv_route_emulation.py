"""Real CH003 dispatch distinguishes chapter loading, END and roster boundaries."""
import hashlib
import importlib.util
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.adv_route_emulation import report, AdvRouteEmulator, CH003
    from tools.tactics_exit_emulation import ROOT, report_text

REPORT_SHA256 = '7baa2020aee348d692ff42f404545603460f918963d7ca66e2a9a58b0a68498e'


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class AdvRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()
        cls.cases = {c['name']: c for c in cls.report['cases']}

    def test_report_reexecutes_original_bytes_and_hashes_each_resource(self):
        path = ROOT / 'analysis/adv-route-v1-20261002.json'
        self.assertEqual(path.read_text(encoding='utf-8'), report_text(self.report))
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), REPORT_SHA256)
        self.assertNotIn(b'\r', path.read_bytes())
        for case in self.cases.values():
            for load in case['resource_loads']:
                source = (CH003.parent / load['path']).read_bytes()
                self.assertEqual(hashlib.sha256(source).hexdigest(), load['source_sha256'])

    def test_source_dates_choose_chapters_without_running_chapter_body_or_requesting_next_state(self):
        for name, child, offset, state in [('april_week5', 'chapter020.ybc', 0x4B0, 7),
                ('may_week3', 'chapter028.ybc', 0x4C8, 7),
                ('special_final_week', 'chapter097.ybc', 0x5B0, 18)]:
            case = self.cases[name]
            self.assertEqual(case['active_path'], child)
            self.assertEqual(case['resource_loads'][-1]['path'], child)
            self.assertEqual(case['stop_reason'], 'chapter_execution_boundary')
            self.assertEqual(case['commands'][-1], {'path': 'ch003.ybc', 'offset': offset, 'opcode': 15, 'executed': True})
            self.assertEqual((case['pc'], case['active'], case['stored_next_task_state']), (0, 1, state))
            self.assertEqual(case['state_requests'], [])
            self.assertEqual(case['pending_flag'], 0)
            self.assertFalse(case['chapter_body_executed'])
            self.assertNotIn('vm_update', case['stub_calls'])
            for entry in ('0x4d0c80', '0x4c23f0', '0x4c21f0', '0x4ce6e0', '0x4ce560'):
                self.assertIn(entry, case['visited_original_addresses'])

    def test_valid_no_chapter_week_reaches_real_end_then_requests_state7(self):
        case = self.cases['valid_no_chapter_week']
        self.assertEqual(case['stop_reason'], None)
        self.assertEqual(case['commands'][-1], {'path': 'ch003.ybc', 'offset': 0x5D0, 'opcode': 19, 'executed': True})
        self.assertEqual(case['active'], 0)
        self.assertEqual(case['state_requests'], [{'kind': 'state_request', 'state': 7}])
        self.assertEqual(case['pending_state'], 7)
        self.assertEqual(case['pending_flag'], 1)
        self.assertEqual(len(case['resource_loads']), 1)

    def test_roster_opcode_stops_before_side_effect_and_never_substitutes_end(self):
        case = self.cases['router_world_side_effect_boundary']
        self.assertEqual(case['stop_reason'], 'unresolved_router_world_opcode')
        self.assertEqual(case['commands'][-1], {'path': 'ch003.ybc', 'offset': 0x5B8, 'opcode': 145, 'executed': False})
        self.assertEqual(case['state_requests'], [])
        self.assertEqual(case['pending_flag'], 0)
        self.assertNotIn('0x4d0990', case['visited_original_addresses'])
        self.assertFalse(any(c['opcode'] == 19 for c in case['commands']))

    def test_invalid_date_control_is_not_claimed_as_supported_gameplay(self):
        case = self.cases['invalid_week0_control']
        self.assertEqual(case['synthetic_week'], 0)
        self.assertEqual(case['state_requests'], [{'kind': 'state_request', 'state': 7}])
        self.assertTrue(any('invalid-date control' in message for message in self.report['limitations']))
        for case in self.cases.values():
            for key in ('chapter_body_executed', 'school_initialized', 'live_witness', 'authorizes_persistent_write'):
                self.assertFalse(case[key])

    def test_undeclared_probe_cannot_load_other_chapters(self):
        for args in [(4, 4, 7), (4, 5, 8), (15, 5, 7)]:
            with self.assertRaises(ValueError):
                AdvRouteEmulator().run('bad', *args)


if __name__ == '__main__':
    unittest.main()
