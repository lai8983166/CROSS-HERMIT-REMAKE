"""Regression for the real multi-instruction MOV PC bug and its correction."""
import copy
import gzip
import hashlib
import json
from pathlib import Path
import unittest
import zipfile
from devtools.terminal_cr2_micro_verify import verify_micro
from devtools.terminal_cr2_ledger_verify import verify


class MicroSemantics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[2] / 'analysis'
        with zipfile.ZipFile(root/'terminal-wait-tcg-cr2-source-v1-20261111.zip') as archive:
            cls.baseline = json.loads(archive.read('tcg-cr2-normal-baseline-v1/report.json'))
            cls.old_overflow = json.loads(gzip.decompress(archive.read('tcg-cr2-overflow-v2/end.json.gz')))
        with zipfile.ZipFile(root/'terminal-wait-tcg-cr2-source-v2-20261111.zip') as archive:
            cls.source = json.loads(archive.read('tcg-cr2-normal-ledger-v2/report.json'))
            cls.elf = archive.read('tcg-cr2-normal-ledger-v2/guest.elf')
            cls.new_overflow = json.loads(gzip.decompress(archive.read('tcg-cr2-overflow-v3/end.json.gz')))

    def test_actual_full_exported_equivalence_and_semantics(self):
        result = verify_micro(self.source, self.baseline, self.elf)
        self.assertTrue(result['micro_semantics_verified'], result)
        self.assertFalse(result['accepted'])
        self.assertFalse(result['windows_admitted'])

    def test_rehashed_pc_not_sufficient_for_semantics(self):
        source = copy.deepcopy(self.source)
        ledger = source['ledger']
        events = json.loads(ledger['events_json'])
        events[0]['pc'] = '0000000000100300'
        ledger['events_json'] = json.dumps(events, separators=(',', ':'))
        ledger['bytes'] = len(ledger['events_json'].encode())
        ledger['events_sha256'] = hashlib.sha256(ledger['events_json'].encode()).hexdigest()
        self.assertTrue(verify(source['arm'], ledger, source['start'], source['end'])['cr2_chain_verified'])
        self.assertFalse(verify_micro(source, self.baseline, self.elf)['micro_semantics_verified'])

    def test_actual_old_counterexample_and_fixed_all_events(self):
        old = json.loads(self.old_overflow['events_json'])
        new = json.loads(self.new_overflow['events_json'])
        self.assertEqual(old[0]['pc'], '0000000000100300')
        self.assertEqual(len(new), 50114)
        self.assertTrue(all(e['pc'] == '000000000010030a' for e in new))
        self.assertTrue(self.new_overflow['overflow'])
        self.assertTrue(self.new_overflow['poisoned'])


if __name__ == '__main__':
    unittest.main()
