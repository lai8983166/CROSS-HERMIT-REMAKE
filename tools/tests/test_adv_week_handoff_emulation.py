"""Native chapter completion and full four-student week share one memory."""
import hashlib
import importlib.util
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.adv_week_handoff_emulation import report, AdvWeekHandoffEmulator
    from tools.adv_week_handoff_fixture import fixture, REPORT, REPORT_SHA256
    from tools.tactics_exit_emulation import ROOT, report_text


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class AdvWeekHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()
        cls.cases = {c['name']: c for c in cls.report['cases']}

    def test_native_report_and_joint_fixture_reproduce_exact_bytes(self):
        self.assertEqual(REPORT.read_text(encoding='utf-8'), report_text(self.report))
        self.assertEqual(hashlib.sha256(REPORT.read_bytes()).hexdigest(), REPORT_SHA256)
        path = ROOT / 'prototype/data/adv_week_handoff_evidence.json'
        self.assertEqual(path.read_text(encoding='utf-8'), report_text(fixture()))
        self.assertNotIn(b'\r', REPORT.read_bytes())
        self.assertNotIn(b'\r', path.read_bytes())

    def test_consumes_actual_native_pending7_only_after_chapter_end(self):
        c = self.cases['adv_complete_then_week']
        self.assertEqual(c['chapter']['state_requests'], [{'va': '0x439e30', 'state': 7}])
        self.assertEqual([v['path'] for v in c['chapter']['loads']], ['ch003.ybc', 'chapter020.ybc', 'chapter021.ybc'])
        self.assertEqual(c['chapter']['after'], c['after_adv'])
        self.assertEqual(c['consumed_request'], {'state': 7, 'pending_flag': 1, 'adv_active': 0,
            'source': 'native_439e30_after_chapter021_end',
            'driver_boundary': 'consume_pending_request_without_scheduler_constructor'})
        self.assertEqual(c['state_requests'], [{'va': '0x439e30', 'state': 7}, {'va': '0x439e30', 'state': 6}])
        self.assertNotIn('0x49f410', c['visited_original_addresses'])

    def test_native_whole_week_includes_joined_student_and_all_cleanup_helpers(self):
        c = self.cases['adv_complete_then_week']
        self.assertTrue(c['week_executed'])
        self.assertEqual((c['after_adv']['month'], c['after_adv']['week']), (4, 5))
        self.assertEqual((c['after']['month'], c['after']['week']), (5, 1))
        self.assertEqual(c['week_events'][0], {'va': '0x4d3aa0', 'caller_return_va': '0x4d419e', 'character_id': 5})
        self.assertEqual(c['week_events'][1], {'va': '0x4d3510', 'caller_return_va': '0x49f507'})
        self.assertEqual([e['character_id'] for e in c['week_events'][2:6]], [3, 4, 9, 5])
        self.assertEqual([e['va'] for e in c['week_events'][6:8]], ['0x4d31f0', '0x4d34a0'])
        self.assertEqual([e['character_id'] for e in c['week_events'][8:]], [3, 4, 5, 9])
        self.assertEqual(c['after']['student_count'], 4)
        self.assertEqual(c['after']['student_ids'], [3, 4, 9, 5]+[-1]*16)
        for before, after in zip(c['after_adv']['participants'], c['after']['participants']):
            for key in ('character_id', 'job', 'attributes', 'growth_pools', 'job_progress', 'level_50', 'unlock_reserved_bytes'):
                self.assertEqual(before[key], after[key])

    def test_native_ch001_loader_runs_after_fade_then_requests6_without_ch001_body(self):
        c = self.cases['adv_complete_then_week']
        self.assertEqual([e['kind'] for e in c['week_start_events']],
                         ['fade_start', 'fade_ready', 'fade_release', 'script_load', 'state_request'])
        self.assertEqual(c['week_start_events'][0]['frames'], 90)
        self.assertEqual(c['week_start_events'][3], {'kind': 'script_load', 'path': 'ch001.ybc', 'next_task_state': 8})
        self.assertEqual(c['resource_loads'][-1]['path'], 'ch001.ybc')
        self.assertEqual((c['active_path'], c['vm_active'], c['vm_pc'], c['stored_next_task_state']), ('ch001.ybc', 1, 0, 8))
        self.assertEqual((c['pending_flag'], c['pending_state']), (1, 6))
        for c in self.cases.values():
            for key in ('ch001_body_executed', 'school_initialized', 'live_witness', 'authorizes_persistent_write'):
                self.assertFalse(c[key])

    def test_week_fade_wait_preserves_applied_week_without_loading_ch001(self):
        c = self.cases['week_fade_wait_after_adv']
        self.assertTrue(c['week_executed'])
        self.assertEqual(c['after'], self.cases['adv_complete_then_week']['after'])
        self.assertEqual(c['stop_reason'], 'week_fade_pending_after_settlement')
        self.assertEqual(c['state_requests'], [{'va': '0x439e30', 'state': 7}])
        self.assertEqual((c['pending_flag'], c['pending_state']), (0, 7))
        self.assertFalse(any(e['kind'] == 'script_load' for e in c['week_start_events']))
        self.assertEqual(len(c['resource_loads']), 3)

    def test_pending_adv_keeps_calendar_and_never_enters_week(self):
        c = self.cases['pending_adv_never_runs_week']
        self.assertFalse(c['week_executed'])
        self.assertFalse(c['chapter']['chapter_completed'])
        self.assertEqual(c['after'], c['after_adv'])
        self.assertEqual((c['after']['month'], c['after']['week']), (4, 5))
        self.assertIsNone(c['consumed_request'])
        self.assertEqual(c['state_requests'], [])
        self.assertEqual(c['week_start_events'], [])
        self.assertEqual(len(c['week_events']), 1)  # Join's unlock helper, not whole-week entry.
        self.assertNotIn('0x4d3510', c['visited_original_addresses'])

    def test_driver_refuses_unrequested_or_already_consumed_handoff_before_writes(self):
        x = AdvWeekHandoffEmulator()
        before = x.roster_snapshot()
        x.phase = 'week'
        with self.assertRaisesRegex(RuntimeError, 'requires unconsumed'):
            x.call(0x49F4E0, (0,))
        self.assertEqual(x.roster_snapshot(), before)
        x = AdvWeekHandoffEmulator(key_ready=False, max_frames=200)
        first = x.run_handoff('pending')
        with self.assertRaisesRegex(RuntimeError, 'single-run'):
            x.run_handoff('again')
        self.assertEqual(x.roster_snapshot(), first['after'])


if __name__ == '__main__':
    unittest.main()
