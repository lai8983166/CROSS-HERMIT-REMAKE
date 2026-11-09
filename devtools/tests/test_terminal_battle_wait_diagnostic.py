import copy
import unittest
from devtools import terminal_battle_wait_diagnostic as d
from devtools.tests.test_terminal_battle_wait_verification import cycles


class IndividualWaitDiagnosticTests(unittest.TestCase):
    def test_crossing_sample_is_unproven_and_never_supplies_counted_wait(self):
        source,rows,proofs=cycles();extra=copy.deepcopy(proofs[0]);extra['snapshot_interval']=[8500,10000];proofs.append(extra)
        before=copy.deepcopy(proofs)
        with self.assertRaisesRegex(ValueError,'switch-out interval'):d.v3.pair_snapshots(source,rows,proofs)
        groups,ledger,boundaries,unsupported=d.diagnostic_pairer()(source,rows,proofs)
        self.assertEqual(len(groups),3);self.assertEqual(proofs,before)
        self.assertEqual(unsupported[0]['snapshot_index'],3);self.assertFalse(unsupported[0]['used_to_prove_wait'])
        self.assertEqual(groups[0]['snapshot_indices'],[0])

    def test_no_wait_can_be_proved_using_only_crossing_samples(self):
        source,rows,proofs=cycles()
        for i,p in enumerate(proofs):p['snapshot_interval']=[i*30000+8500,i*30000+10000]
        with self.assertRaisesRegex(ValueError,'three distinct'):d.diagnostic_pairer()(source,rows,proofs)

    def test_unproven_sample_still_cannot_change_same_pending_frame_semantics(self):
        source,rows,proofs=cycles();extra=copy.deepcopy(proofs[0]);extra['snapshot_interval']=[8500,10000]
        extra['wait_frame_bp']+=4;proofs.append(extra)
        with self.assertRaisesRegex(ValueError,'same pending syscall semantics'):d.diagnostic_pairer()(source,rows,proofs)

    def test_raw_corruption_and_unexplained_intermediate_hole_still_rejected(self):
        source,rows,proofs=cycles();rows[1]['payload_hex']='00'*8
        with self.assertRaises(ValueError):d.diagnostic_pairer()(source,rows,proofs)
        source,rows,proofs=cycles();proofs[0]['snapshot_interval']=[21000,22000]
        with self.assertRaisesRegex(ValueError,'boundary explanation'):d.diagnostic_pairer()(source,rows,proofs)


if __name__=='__main__':unittest.main()
