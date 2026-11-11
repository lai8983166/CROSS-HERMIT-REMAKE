"""Actual bounded microguest ledger and semantic tampering rejection."""
import copy
import hashlib
import json
from pathlib import Path
import unittest
import zipfile
from devtools.terminal_cr2_ledger_verify import verify


class LedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        capsule = Path(__file__).resolve().parents[2] / 'analysis/terminal-wait-tcg-cr2-source-v1-20261111.zip'
        with zipfile.ZipFile(capsule) as archive:
            cls.source = json.loads(archive.read('tcg-cr2-ledger-v1/report.json'))

    def test_actual_chain_without_acceptance(self):
        s = self.source
        result = verify(s['arm'], s['ledger'], s['start'], s['end'])
        self.assertTrue(result['cr2_chain_verified'], result)
        self.assertEqual(result['event_count'], 3)
        self.assertFalse(result['full_state_verified'])
        self.assertFalse(result['accepted'])

    def test_semantic_mutations(self):
        for mutation in ('drop', 'tail', 'duplicate', 'reorder', 'cpu', 'window', 'old', 'new',
                         'source', 'reason', 'overflow', 'poison', 'boundary', 'missing_state',
                         'wrong_type', 'digest', 'counter', 'fault_address', 'duplicate_key', 'deadline'):
            with self.subTest(mutation=mutation):
                s = copy.deepcopy(self.source)
                ledger = s['ledger']
                events = json.loads(ledger['events_json'])
                if mutation == 'drop':
                    events.pop(0)
                elif mutation == 'tail':
                    events.pop()
                elif mutation == 'duplicate':
                    events.insert(1, copy.deepcopy(events[0]))
                elif mutation == 'reorder':
                    events.reverse()
                elif mutation == 'cpu':
                    events[0]['cpu'] = 1
                elif mutation == 'window':
                    events[0]['window'] += 1
                elif mutation == 'old':
                    events[0]['old'] = '123456789abcdef0'
                elif mutation == 'new':
                    events[0]['new'] = '123456789abcdef0'
                elif mutation == 'source':
                    events[0]['source'] = '123456789abcdef0'
                elif mutation == 'reason':
                    events[0]['reason'] = 'migration'
                elif mutation == 'overflow':
                    ledger['overflow'] = True
                elif mutation == 'poison':
                    ledger['poisoned'] = True
                elif mutation == 'boundary':
                    ledger['end'][0]['cr2'] = '123456789abcdef0'
                elif mutation == 'missing_state':
                    del ledger['end'][0]['state']['cr0_cr2_cr3_cr4']
                elif mutation == 'wrong_type':
                    events[0]['cpu'] = False
                elif mutation == 'counter':
                    ledger['end'][0]['counter'] += 1
                elif mutation == 'fault_address':
                    events[-1]['fault_address'] = '123456789abcdef0'
                elif mutation == 'deadline':
                    ledger['elapsed_ns'] = 60_000_000_000
                # Rehash deliberately: semantic checks must fail beyond checksum.
                ledger['events_json'] = json.dumps(events, separators=(',', ':'))
                if mutation == 'duplicate_key':
                    ledger['events_json'] = ledger['events_json'].replace('"cpu":0', '"cpu":1,"cpu":0', 1)
                ledger['count'] = len(events)
                ledger['bytes'] = len(ledger['events_json'].encode())
                ledger['events_sha256'] = hashlib.sha256(ledger['events_json'].encode()).hexdigest()
                if mutation == 'digest':
                    ledger['events_sha256'] = '0' * 64
                result = verify(s['arm'], ledger, s['start'], s['end'])
                self.assertFalse(result['cr2_chain_verified'], result)


if __name__ == '__main__':
    unittest.main()
