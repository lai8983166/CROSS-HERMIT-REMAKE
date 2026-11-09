import contextlib
import struct
import threading
import unittest
from unittest.mock import patch
from devtools import terminal_battle_wait_clock as c
from devtools import terminal_battle_wait_clock_etl as etl


class ClockDiagnosticTests(unittest.TestCase):
    def candidate(self,tid):
        raw=bytearray(48);struct.pack_into('<I',raw,0x24,tid)
        return dict(pointer=123,head_hex=raw.hex())

    def test_unconstructed_or_other_owner_tid_never_becomes_candidate(self):
        for tid in (0,0xffffffff,0xcdcdcdcd,51,60):
            self.assertIsNone(c.current_candidate(self.candidate(tid),[51,52],51))
        row=self.candidate(52);self.assertIs(c.current_candidate(row,[51,52],51),row)

    def clock_window(self):
        w=object.__new__(c.ClockWindow);w.lock=threading.RLock();w.result=dict(non_wait_samples=[])
        ticks=iter((10,11,30,31));w.qpc=lambda:next(ticks)
        return w

    def test_raw_qpc_brackets_do_not_overwrite_UTC(self):
        w=self.clock_window();times=iter((12345678900,12345679900))
        def replacement(template,**namespace):
            def snapshot(obj):
                first=namespace['original'].utc_now_ns(None);last=namespace['original'].utc_now_ns(None)
                return dict(snapshot_begin_ns=first,snapshot_end_ns=last)
            return snapshot
        with patch.object(c,'clone',replacement),patch.object(c.original,'utc_now_ns',lambda _:next(times)):
            row=w.snapshot()
        self.assertEqual(row['snapshot_begin_ns'],12345678900)
        self.assertEqual(row['snapshot_end_ns'],12345679900)
        self.assertEqual(row['timing_diagnostic']['data_interval_qpc'],[10,31])
        self.assertFalse(row['timing_diagnostic']['includes_original_context_acquisition'])

    def test_unretained_nonwait_does_not_fabricate_end_timestamp(self):
        w=self.clock_window()
        def replacement(template,**namespace):
            def snapshot(obj):namespace['original'].utc_now_ns(None);return None
            return snapshot
        with patch.object(c,'clone',replacement),patch.object(c.original,'utc_now_ns',lambda _:123):
            self.assertIsNone(w.snapshot())
        self.assertEqual(w.result['unretained_non_wait_timing_samples'],1)
        self.assertEqual(w.result['non_wait_samples'],[])

    def test_snapshot_failure_does_not_leave_lock_held(self):
        w=self.clock_window()
        with patch.object(c,'clone',return_value=lambda _:(_ for _ in ()).throw(ValueError('actual context failure'))):
            with self.assertRaisesRegex(ValueError,'actual context failure'):w.snapshot()
        acquired=[]
        def check():
            ok=w.lock.acquire(timeout=.1);acquired.append(ok)
            if ok:w.lock.release()
        t=threading.Thread(target=check);t.start();t.join();self.assertEqual(acquired,[True])

    def test_raw_clock_decoder_requires_frozen_parent(self):
        self.assertTrue(callable(etl.raw_decoder()))
        with patch.object(etl,'PARENT_SHA','0'*64):
            with self.assertRaisesRegex(ValueError,'fixed full ETL'):etl.raw_decoder()
        for value in (0,-1,True,1.5):
            with self.assertRaises(ValueError):etl.raw_qpc(value)


if __name__=='__main__':unittest.main()
