"""Score rules are original bytes; expectations are separately executed native code."""
import hashlib
import json
import struct
import unittest

from tools.battle_preparation_fixture import fixture, REPORT, REPORT_SHA256
from tools.tactics_exit_emulation import ROOT, SOURCE


class PreparationFixtureTests(unittest.TestCase):
    def test_canonical_fixture_is_generated_from_native_report_and_source(self):
        expected = fixture()
        actual = json.loads((ROOT / 'prototype/data/tactics_score_preparation_evidence.json').read_text())
        self.assertEqual(actual, expected)
        self.assertEqual(actual['source_report_sha256'], hashlib.sha256(REPORT.read_bytes()).hexdigest())
        self.assertEqual(actual['source_report_sha256'], REPORT_SHA256)

    def test_rules_addresses_and_character_classes_are_source_bytes(self):
        data = fixture()
        image = SOURCE.read_bytes()
        rules = data['rules']
        self.assertEqual(rules['base_points'], [60000, 50000, 40000, 30000, 20000])
        for class_id in range(6):
            for key, va, width in [('rates', 0x61C508, 11), ('distributions', 0x61C58C, 7)]:
                row = struct.unpack_from('<'+'h'*width, image, va-0x400000+class_id*width*2)
                self.assertEqual(rules[key][class_id], list(row))
        self.assertEqual(rules['growth_limit'], 8500000)
        self.assertEqual([c['rate_class'] for c in data['cases'][0]['inputs']['characters']], [5, 3, 4])

    def test_sortie_8_17_task_specific_reward_tables_match_original(self):
        catalogs = json.loads((ROOT / 'prototype/data/school_sortie_reward_rules.json').read_bytes())
        image = SOURCE.read_bytes()
        for task_id in (8, 17):
            def values(va, count, fmt='h'):
                return list(struct.unpack_from('<' + fmt * count, image, va + 256 * task_id - 0x400000))

            self.assertEqual(catalogs[str(task_id)], {
                'task_id': task_id, 'base_points': values(0x73BEF4, 5, 'i'),
                'unit_bonus': values(0x73BF08, 1)[0], 'time_bonuses': values(0x73BF0A, 3),
                'count_bonuses': values(0x73BF10, 6),
                'loot_quotas': [values(0x73BF1A + 14 * grade, 7) for grade in range(5)],
                'fixed_items': values(0x73BF60, 8),
                'objective_rewards': [values(0x73BF70 + 6 * slot, 3) for slot in range(16)]})

    def test_native_expectations_include_cap_probe_and_no_authority(self):
        native = json.loads(REPORT.read_bytes())
        for case, original in zip(fixture()['cases'], native['cases']):
            self.assertEqual(case['expected']['total_after'], original['after']['global_total_511c'])
            for expected, character in zip(case['expected']['characters'], original['after']['characters']):
                self.assertEqual(expected['staged_package'], character['staged_package'])
            self.assertFalse(case['authorizes_persistent_write'])


if __name__ == '__main__':
    unittest.main()
