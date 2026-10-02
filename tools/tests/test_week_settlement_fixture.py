"""Week rules come from EXE bytes; expectations come from native execution."""
import hashlib
import json
import struct
import unittest

from tools.week_settlement_fixture import fixture, REPORT, REPORT_SHA256
from tools.tactics_exit_emulation import ROOT, SOURCE, report_text


class WeekFixtureTests(unittest.TestCase):
    def test_fixture_is_byte_exact_and_guarded_by_native_report(self):
        data = fixture()
        path = ROOT / 'prototype/data/week_settlement_evidence.json'
        self.assertEqual(path.read_bytes().decode(), report_text(data))
        self.assertEqual(data['source_report_sha256'], hashlib.sha256(REPORT.read_bytes()).hexdigest())
        self.assertEqual(data['source_report_sha256'], REPORT_SHA256)
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                         '5bdb406c2125c610c75942a9e589a9b427cdbcd5d97b0cbf35c014b1d793aedf')

    def test_all_thirty_rules_match_raw_image(self):
        data, image = fixture(), SOURCE.read_bytes()
        for index, rule in enumerate(data['rules']['unlock_rules']):
            at = 0x738CD3+(index+1)*0x32-0x400000
            self.assertEqual(rule['month'], image[at])
            self.assertEqual(rule['week'], image[at+1])
            self.assertEqual(rule['minimum_attributes'], list(struct.unpack_from('<7h', image, at+3)))
            self.assertEqual(rule['minimum_total'], struct.unpack_from('<h', image, at+17)[0])
            self.assertEqual(rule['job_requirements'],
                [{'type': image[at+19+j*2], 'count': image[at+20+j*2]} for j in range(3)])

    def test_every_expected_snapshot_is_native_and_probes_do_not_forge_context(self):
        native = json.loads(REPORT.read_bytes())
        for case, original in zip(fixture()['cases'], native['cases']):
            self.assertEqual(case['before'], original['before_week'])
            self.assertEqual(case['expected_after'], original['after_week'])
            self.assertFalse(case['authorizes_persistent_write'])
            self.assertEqual(bool(case['context']), 'all_result' in original)
        self.assertFalse(fixture()['authorizes_persistent_write'])


if __name__ == '__main__':
    unittest.main()
