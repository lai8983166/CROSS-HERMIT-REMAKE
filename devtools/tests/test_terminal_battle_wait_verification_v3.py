import copy
from pathlib import Path
import time
import unittest
from unittest.mock import patch
from devtools import terminal_battle_wait_verification_v3 as v
from devtools import terminal_battle_wait_etl_v2 as reader
from devtools.tests.test_terminal_battle_wait_verification import cycles,window_source


class CompleteExpandedOfflineSequence(unittest.TestCase):
    def test_larger_complete_sequence_and_pairing_without_truncation(self):
        source,rows,proofs=cycles(3000)
        self.assertEqual(len(rows),18000)
        with self.assertRaisesRegex(ValueError,'bounded complete'):v.v1.validate_records(rows,source['subject'],2)
        pairs,ledger=v.validate_records(rows,source['subject'],2)
        self.assertEqual(len(pairs),3000);self.assertEqual(ledger['closed_calls'],3000)
        groups,ledger,boundaries,_=v.pair_snapshots(source,rows,proofs[:3])
        self.assertEqual(len(groups),3);self.assertEqual(ledger['closed_calls'],3000);self.assertEqual(boundaries,[])
        with self.assertRaisesRegex(ValueError,'bounded complete'):
            v.validate_records([rows[0]]*65537,source['subject'],2)

    def test_interior_raw_corruption_is_still_rejected_after_old_capacity(self):
        source,rows,_=cycles(3000);rows[17000]['payload_hex']='00'*8
        with self.assertRaises(ValueError):v.validate_records(rows,source['subject'],2)

    def test_capture_declaration_is_not_rewritten_to_new_offline_budget(self):
        source=window_source();original=copy.deepcopy(source)
        self.assertTrue(v.source_contract(source,source['ETL'])['strict_source_cleanup_verified'])
        self.assertEqual(source,original);self.assertEqual(source['trace_limits']['max_selected_records'],16384)
        source['trace_limits']['max_selected_records']=65536
        with self.assertRaises(ValueError):v.source_contract(source,source['ETL'])
        self.assertEqual(reader.OFFLINE_LIMITS['max_selected_records'],65536)
        self.assertEqual(reader.SELECTED_GZIP_LIMIT,2*1024*1024)

    def test_guest_qualification_remains_before_native_reader(self):
        result={};source=dict(trace_limits=copy.deepcopy(reader.parent.LIMITS))
        with patch.object(reader.parent.frozen,'qualify',side_effect=ValueError('unqualified')):
            with self.assertRaisesRegex(ValueError,'unqualified'):
                reader.decode_etl(Path('unused'),source,result,time.monotonic()+180,lambda r:None)
        self.assertFalse(result['events_truncated']);self.assertFalse(result['source_rewritten'])

    def test_changed_parent_verification_is_rejected(self):
        with patch.object(v,'V2_SHA','0'*64):
            with self.assertRaises(ValueError):v.make_decoder()


if __name__=='__main__':unittest.main()
