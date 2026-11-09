import copy
import struct
import unittest
from unittest.mock import patch
from devtools import terminal_battle_wait_verification_v4 as v
from devtools.tests.test_terminal_battle_wait_verification import cycles,event


class ReportedEndTailTests(unittest.TestCase):
    def fixture(self):
        source,rows,proofs=cycles();tid=source['subject']['tid'];address=source['kernel_wait_export']['target']
        rows.extend([event(100,90000,36,0,dict(NewThreadId=tid,OldThreadId=9),9),
            event(101,94000,51,0,dict(SysCallAddress=address),tid),
            event(102,96000,36,0,dict(NewThreadId=9,OldThreadId=tid),tid),
            event(103,97000,36,1,dict(NewThreadId=tid,OldThreadId=10),10),
            event(104,98000,51,1,dict(SysCallAddress=address+16),tid),
            event(105,99000,52,1,dict(SysCallNtStatus=0),tid),
            event(106,100000,36,1,dict(NewThreadId=10,OldThreadId=tid),tid)])
        return source,rows

    def test_complete_raw_tail_is_kept_without_inferred_return_or_nesting(self):
        source,rows=self.fixture();before=copy.deepcopy(rows)
        with self.assertRaisesRegex(ValueError,'overlapping'):v.v3.validate_records(rows,source['subject'],2)
        pairs,ledger=v.validate_lifetime_records(rows,source['subject'],2,95000)
        self.assertEqual(len(pairs),3);self.assertEqual(rows,before)
        self.assertEqual(ledger['final_unpaired_entry'],19)
        self.assertEqual(ledger['post_end_unpaired_indices'],[22,23])
        self.assertFalse(ledger['full_global_pairing']);self.assertFalse(ledger['terminal_tail_syscalls_interpreted'])

    def test_before_end_overlap_still_rejected(self):
        source,rows=self.fixture()
        with self.assertRaisesRegex(ValueError,'overlapping'):
            v.validate_lifetime_records(rows,source['subject'],2,99001)

    def test_post_end_payload_owner_and_CPU_corruption_still_rejected(self):
        for mutate in (lambda r:r[22].update(payload_hex='00'*8),
                       lambda r:r[23].update(decoder_cpu_tid_before=999),
                       lambda r:r[24].update(cpu=0)):
            source,rows=self.fixture();mutate(rows)
            with self.assertRaises(ValueError):v.validate_lifetime_records(rows,source['subject'],2,95000)


class ReportedEndBindingTests(unittest.TestCase):
    def fixture(self):
        h=bytearray(80);struct.pack_into('<II',h,8,77,12)
        end=dict(opcode=2,ns=50,header_hex=h.hex(),payload_hex=struct.pack('<II',12,77).hex())
        receipt=dict(subject_thread_bindings=[dict(opcode=3,ns=1),end])
        source=dict(subject=dict(pid=12,tid=77),window_snapshots=[dict(snapshot_end_ns=20)],
            capture_interval=dict(end_ns=100),worker_exit=dict(code=0,wait_status=0,before_WM_CLOSE=True,
                duplicate_handle_query_only=True,PTDcleanup=False,observed_ns=90))
        return source,[dict(ns=30),dict(ns=60)],receipt

    def test_exact_event_and_later_actual_exit_required(self):
        s,rows,r=self.fixture()
        with patch.object(v.v3,'verify_receipt')as full:
            self.assertEqual(v.reported_end_boundary(s,rows,r)['ns'],50);full.assert_called_once_with(s,rows,r)

    def test_rundown_reuse_equal_time_late_snapshot_wrong_PID_rejected(self):
        changes=[lambda s,rows,r:r['subject_thread_bindings'][1].update(opcode=4),
            lambda s,rows,r:r['subject_thread_bindings'].append(dict(opcode=3,ns=51)),
            lambda s,rows,r:rows[0].update(ns=50),
            lambda s,rows,r:s['window_snapshots'][0].update(snapshot_end_ns=50),
            lambda s,rows,r:s['worker_exit'].update(observed_ns=49),
            lambda s,rows,r:r['subject_thread_bindings'][1].update(payload_hex=struct.pack('<II',13,77).hex())]
        for change in changes:
            s,rows,r=self.fixture();change(s,rows,r)
            with patch.object(v.v3,'verify_receipt'),self.assertRaises(ValueError):v.reported_end_boundary(s,rows,r)


if __name__=='__main__':unittest.main()
