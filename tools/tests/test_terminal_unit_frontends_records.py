import unittest
from unittest.mock import patch

from tools import terminal_unit_frontends_records as records


class TerminalUnitFrontendRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = {j: records.derive_target_record(j) for j in (1, 3)}

    def test_source_profile_and_native_MP_writers(self):
        for job, case in self.cases.items():
            with self.subTest(job=job):
                original = bytes.fromhex(case['original_profile_hex'])
                declared = bytes.fromhex(case['profile_hex'])
                self.assertEqual(original[:4], b'\x0b\x00\x09\x00')
                self.assertEqual(original[:2]+original[4:], declared[:2]+declared[4:])
                self.assertEqual(case['MP'], [238, 238, 426 if job == 1 else 246])
                self.assertTrue(case['original_CRT_instructions_executed'])
                self.assertFalse(case['function_return_stubs'])
                pcs = {w['pc'] for w in case['MP_writes']}
                self.assertTrue({0x4DFE3A, 0x4DFE48}.issubset(pcs))
                entries = [e['entry'] for e in case['original_entries']]
                self.assertEqual(entries.count(0x56CEC0), 2)
                self.assertEqual(entries.count(0x56CE80), 2)
                self.assertIn(0x4E0A00, entries)

    def test_full_original_record_matches_prior_bounded_reverse_probe(self):
        import hashlib
        import json
        frozen = json.loads((records.ROOT/'analysis/terminal-unit-frontends-record-source-v1-20261103.json').read_text(encoding='utf8'))
        for job, case in self.cases.items():
            prior = next(p for p in frozen['probes'] if p['identity'] == 11 and p['declared_profile_job_override'] == job)
            self.assertEqual(case['record_hex'], prior['record_hex'])
            self.assertEqual(case['record_sha256'], hashlib.sha256(bytes.fromhex(prior['record_hex'])).hexdigest())

    def test_overlay_preserves_every_undeclared_source_byte(self):
        for job, case in self.cases.items():
            derived = bytes.fromhex(case['record_hex'])
            old = bytes(256)
            spans = records.recommended_target_spans()
            result = records.apply_declared_record_fields(derived, old, spans)
            after = bytes.fromhex(result['record_hex'])
            covered = {o for s in spans for o in range(s['offset'], s['offset']+s['bytes'])}
            self.assertEqual(after[0x1A:0x20], derived[0x1A:0x20])
            self.assertEqual(len(result['overrides']), len(spans))
            for off in range(records.RECORD_BYTES):
                self.assertEqual(after[off], 0 if off in covered else derived[off])
            for row in result['overrides']:
                o, n = row['offset'], row['bytes']
                self.assertEqual(row['before_hex'], derived[o:o+n].hex())
                self.assertEqual(row['after_hex'], '00'*n)
                self.assertTrue(row['source'])
            self.assertEqual(derived, bytes.fromhex(case['record_hex']))

    def test_MP_recovery_whole_record_and_bad_span_refused(self):
        derived = bytes.fromhex(self.cases[1]['record_hex'])
        for offset, size in ((0x1A, 2), (0x1C, 2), (0x1E, 2), (0x19, 2), (0, 176), (175, 2), (-1, 1), (0, 0)):
            with self.subTest(offset=offset, size=size), self.assertRaises(ValueError):
                records.apply_declared_record_fields(derived, bytes(176), [dict(offset=offset, bytes=size, field='bad', source='test')])
        for spans in ([dict(offset=0, bytes=2, field='slot', source='')],
                      [dict(offset=0, bytes=2, field='a', source='test'), dict(offset=1, bytes=1, field='b', source='test')]):
            with self.assertRaises(ValueError):
                records.apply_declared_record_fields(derived, bytes(176), spans)

    def test_invalid_job_and_changed_source_refused(self):
        for job in (True, 2, 9, 1.0):
            with self.assertRaises(ValueError):
                records.derive_target_record(job)
        with patch.object(records.Path, 'read_bytes', return_value=bytes(5980160)):
            with self.assertRaisesRegex(ValueError, 'exact original source'):
                records.derive_target_record(1)


if __name__ == '__main__':
    unittest.main()
