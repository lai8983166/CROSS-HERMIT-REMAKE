"""Both layouts and direct continuation must remain in the same native memory."""
import hashlib
import importlib.util
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.campaign_school_layout_emulation import report, CampaignSchoolLayoutEmulator
    from tools.campaign_school_layout_fixture import fixture, NATIVE_SHA256
    from tools.tactics_exit_emulation import ROOT, report_text


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class CampaignSchoolLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.native = report()
        cls.cases = {c['name']: c for c in cls.native['cases']}

    def test_exact_native_reexecution_and_fixture_export(self):
        path = ROOT / 'analysis/campaign-school-layout-v1-20261004.json'
        self.assertEqual(path.read_text(encoding='utf-8'), report_text(self.native))
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), NATIVE_SHA256)
        path = ROOT / 'prototype/data/campaign_school_layout_evidence.json'
        self.assertEqual(path.read_text(encoding='utf-8'), report_text(fixture(self.native)))
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                         '28f572b0e770cddd8e3cdec3b338a447cb58ebde6d0a7e9d1712d51bacae5c4f')
        self.assertNotIn(b'\r', path.read_bytes())

    def test_source_views_match_all_fields_and_real_recipient_alias_at_every_stage(self):
        result_only = {'staged_package', 'staged_total', 'recipient_count', 'week_records'}
        for c in self.native['cases']:
            for canonical_key, school_key in [('before', 'school_before'), ('after_result', 'school_after_result'),
                    ('after_join_probe', 'school_after_join_probe'), ('after_week_probe', 'school_after_week_probe')]:
                canonical, school = c[canonical_key], c[school_key]
                if canonical is None:
                    self.assertIsNone(school)
                    continue
                for key in ('month', 'week', 'flags', 'availability', 'item_flags'):
                    self.assertEqual(canonical[key], school[key])
                self.assertEqual([{k: v for k, v in row.items() if k not in result_only}
                                  for row in canonical['characters']], school['participants'])
                self.assertEqual(canonical['recipient_id'], school['adv_globals']['0x7e1180'])
                for key in ('student_count', 'student_ids', 'teacher_count', 'teacher_ids',
                            'group_student_ids', 'group_student_indices'):
                    self.assertEqual(canonical['school'][key], school[key])

    def test_unavailable_candidate_and_twenty_relations_survive_result_application(self):
        for c in self.native['cases']:
            self.assertEqual([r['character_id'] for r in c['before']['characters']], [3, 4, 9, 5])
            self.assertEqual(len(c['before']['relationships']), 20)
            self.assertEqual(c['before']['characters'][3], c['after_result']['characters'][3])
            self.assertEqual(c['after_result']['availability'][5], 0)
            self.assertEqual(c['after_result']['school']['student_count'], 3)
            involving5 = lambda snapshot: [r for r in snapshot['relationships'] if 5 in (r['from'], r['to'])]
            self.assertEqual(involving5(c['before']), involving5(c['after_result']))

    def test_direct_join_retains_result_growth_history_and_relations_then_week_sees_four_students(self):
        c = self.cases['ordinary_layout_join_week']
        joined, settled = c['after_join_probe'], c['after_week_probe']
        self.assertEqual(joined['characters'][:3], c['after_result']['characters'][:3])
        self.assertEqual(joined['relationships'], c['after_result']['relationships'])
        self.assertEqual(joined['school']['student_ids'][:4], [3, 4, 9, 5])
        self.assertEqual(joined['availability'][5], 1)
        self.assertEqual(joined['characters'][3]['unlock_reserved_bytes'], [0, 0])
        self.assertEqual(joined['characters'][3]['level_50'], 28)
        self.assertEqual((settled['month'], settled['week']), (5, 1))
        self.assertEqual(settled['relationships'], joined['relationships'])
        week_start = next(i for i, e in enumerate(c['week_events']) if e['va'] == '0x4d3510')
        # Join also calls the unlock helper for candidate5. The whole week
        # then traverses the STUDENT ROSTER order, not sorted availability IDs.
        self.assertEqual([e['character_id'] for e in c['week_events'][week_start:] if e['va'] == '0x4d3aa0'],
                         joined['school']['student_ids'][:4])
        for va in ('0x4d3e90', '0x4d3510', '0x4d31f0', '0x4d34a0'):
            self.assertIn(va, c['visited_original_addresses'])

    def test_wait_does_not_run_join_or_week_and_special_date_runs_only_native_state12_week(self):
        waiting = self.cases['ordinary_layout_wait']
        self.assertEqual(waiting['result_requested_state'], 12)
        self.assertIsNone(waiting['after_join_probe'])
        self.assertEqual(waiting['week_events'], [])
        special = self.cases['special_layout_week']
        self.assertTrue(special['result_native_week'])
        self.assertIsNotNone(special['result_before_week'])
        self.assertEqual((special['after_result']['month'], special['after_result']['week']), (15, 5))
        self.assertIsNone(special['after_join_probe'])
        self.assertEqual(len([e for e in special['week_events'] if e['va'] == '0x4d3510']), 1)

    def test_direct_probes_never_claim_adv_school_or_live_completion(self):
        for c in self.native['cases']:
            for key in ('chapter_completed', 'school_initialized', 'live_witness', 'authorizes_persistent_write'):
                self.assertFalse(c[key])
            self.assertNotIn('0x4ab7a0', c['visited_original_addresses'])
            self.assertNotIn('0x4b8d50', c['visited_original_addresses'])
        emulator = CampaignSchoolLayoutEmulator()
        emulator._ran_layout = True
        with self.assertRaisesRegex(RuntimeError, 'single-run'):
            emulator.run_layout('duplicate')


if __name__ == '__main__':
    unittest.main()
