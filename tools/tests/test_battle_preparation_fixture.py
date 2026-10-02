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

    def test_native_expectations_include_cap_probe_and_no_authority(self):
        native = json.loads(REPORT.read_bytes())
        for case, original in zip(fixture()['cases'], native['cases']):
            self.assertEqual(case['expected']['total_after'], original['after']['global_total_511c'])
            for expected, character in zip(case['expected']['characters'], original['after']['characters']):
                self.assertEqual(expected['staged_package'], character['staged_package'])
            self.assertFalse(case['authorizes_persistent_write'])


if __name__ == '__main__':
    unittest.main()
