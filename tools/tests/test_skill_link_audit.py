# -*- coding: utf-8 -*-
import unittest

from tools.skill_link_audit import audit_fx, audit_skill, load_sources


class SkillLinkAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = load_sources()

    def test_skill_22_exposes_two_valid_but_unexported_fx(self):
        result = audit_skill(22, 'C0A', 'N', self.sources)
        self.assertEqual(result['attack']['hit_effect'], 6)
        self.assertTrue(result['visual']['effect_id_matches_attack'])
        self.assertEqual(result['visual']['actions']['cast_action']['status'], 'exported')
        self.assertEqual(result['visual']['actions']['release_action']['status'], 'exported')
        self.assertEqual(result['visual']['actions']['release_action']['original']['block'], 1)
        self.assertEqual(result['visual']['actions']['release_action']['original']['animation'], 6)
        self.assertTrue(result['visual']['actions']['release_action']['original']['program_present'])
        self.assertEqual(result['visual']['fx']['cast_fx']['status'], 'valid_not_exported')
        self.assertEqual(result['visual']['fx']['release_fx']['status'], 'exported')
        self.assertEqual(result['visual']['fx']['impact_fx']['status'], 'valid_not_exported')

    def test_skill_29_distinguishes_action_gap_from_fx_export(self):
        result = audit_skill(29, 'D0A', 'N', self.sources)
        self.assertEqual(result['visual']['actions']['cast_action']['animation'], 56)
        self.assertEqual(result['visual']['actions']['release_action']['status'], 'not_exported')
        self.assertTrue(all(item['status'] == 'exported' for item in result['visual']['fx'].values()))

    def test_empty_direction_is_not_reported_as_absent_source_action(self):
        result = audit_skill(22, 'A0A', 'N', self.sources)
        self.assertEqual(result['visual']['actions']['cast_action']['status'], 'no_exported_direction')
        self.assertTrue(result['visual']['actions']['cast_action']['original']['program_present'])

    def test_e0a_action_31_is_not_present_in_original_archive(self):
        result = audit_skill(22, 'E0A', 'N', self.sources)
        action = result['visual']['actions']['release_action']
        self.assertEqual(action['status'], 'no_exported_direction')
        self.assertFalse(action['original']['program_present'])

    def test_archive_bounds_are_separate_from_export_coverage(self):
        fx = self.sources['fx']
        self.assertEqual(audit_fx(2044, fx)['status'], 'valid_not_exported')
        self.assertEqual(audit_fx(2050, fx)['status'], 'exported')
        self.assertEqual(audit_fx(3999, fx)['status'], 'outside_archive')

    def test_out_of_range_skill_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'outside visual table'):
            audit_skill(612, 'A0A', 'N', self.sources)


if __name__ == '__main__':
    unittest.main()
