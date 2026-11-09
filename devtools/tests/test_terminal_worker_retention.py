from contextlib import contextmanager
import ctypes as C
import ctypes.wintypes as W
import copy
import struct
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from devtools import terminal_worker_retention as r


class RetentionTests(unittest.TestCase):
    def setup_tracker(self,pending=False,partial=False,foreign=False,duplicate_error=False):
        events=[];held=[False]
        head=bytearray(64);struct.pack_into('<I',head,0,0x5A0C18)
        struct.pack_into('<III',head,0x1C,44,0xCDCDCDCD if pending else 48,88)
        task=dict(pointer=100,vtable=0x5A0C18,header_hex=head.hex(),thread_id=88)
        if not pending and not partial:task['TLS']={'actual':'source'}
        chain=[] if pending else [dict(return_va=x) for x in ([0x421F8A] if partial else [0x421F8A,0x56E183])]
        frames=[dict(tid=88,chain=chain)]
        row=dict(elapsed=1,tasks=[task],frames=frames)
        @contextmanager
        def cohort(c,main_tid,b):
            events.append('suspend');held[0]=True
            try:yield frames
            finally:held[0]=False;events.append('resume')
        def snapshot(c,owned):
            with base.original.frozen(c.h,c.pid) as actual:
                self.assertIs(actual,frames);return copy.deepcopy(row)
        def duplicate(h,remote,current,p,access,inherit,options):
            self.assertTrue(held[0]);events.append(('duplicate',remote))
            if duplicate_error:return False
            C.cast(p,C.POINTER(W.HANDLE)).contents.value=999;return True
        def check(ok,msg):
            if not ok:raise OSError(msg)
        def close(h):events.append('close');return True
        api=SimpleNamespace(check=check,close=close)
        backend=SimpleNamespace(original=api,parent=SimpleNamespace(duplicate=duplicate,current_process=lambda:1),
            get_thread_pid=lambda h:8 if foreign else 7,get_thread_id=lambda h:88,
            event_identity=lambda c,h:dict(remote_handle=h))
        tracker=r.WorkerRetention(SimpleNamespace(h=9,pid=7),77,backend,cohort,snapshot)
        return tracker,events,row

    def test_raw_unconstructed_fields_preserved_and_never_duplicated(self):
        tracker,events,source=self.setup_tracker(pending=True)
        row=tracker.capture(None)
        self.assertEqual(row['tasks'],source['tasks'])
        self.assertEqual(row['worker_retention']['tasks'][0]['status'],'pending_callback_ancestry')
        self.assertEqual(events,['suspend','resume']);self.assertFalse(tracker.handles)

    def test_live_owner_retained_before_resume_and_not_duplicated_twice(self):
        tracker,events,_=self.setup_tracker()
        tracker.capture(None);row=tracker.capture(None)
        self.assertEqual(events,['suspend',('duplicate',48),'resume','suspend','resume'])
        self.assertEqual(row['worker_retention']['tasks'][0]['status'],'already_retained')
        self.assertFalse(tracker.close()['original_resource_cleanup_proved'])

    def test_partial_ancestry_hard_fails_with_original_row(self):
        tracker,events,source=self.setup_tracker(partial=True)
        with self.assertRaisesRegex(ValueError,'partial'):tracker.capture(None)
        self.assertEqual(events,['suspend','resume'])
        self.assertEqual(tracker.failure['row']['tasks'],source['tasks'])

    def test_foreign_duplicate_closed_before_restoring_suspend(self):
        tracker,events,_=self.setup_tracker(foreign=True)
        with self.assertRaisesRegex(ValueError,'exact original'):tracker.capture(None)
        self.assertEqual(events,['suspend',('duplicate',48),'close','resume'])

    def test_native_failure_preserves_exact_call_and_first_raw_row(self):
        tracker,events,source=self.setup_tracker(duplicate_error=True)
        with self.assertRaises(OSError):tracker.capture(None)
        first=tracker.failure
        self.assertEqual(first['call']['remote_handle'],48)
        self.assertEqual(first['row']['tasks'],source['tasks'])
        with self.assertRaises(OSError):tracker.capture(None)
        self.assertIs(tracker.failure,first)
        self.assertEqual(events[-1],'resume')

    def test_cohort_main_first_and_restores_all_own_scopes_after_new_thread_rejection(self):
        events=[];enumerations=iter([[88,77],[88,77,99]])
        @contextmanager
        def frames(c,tids,backend):
            tid=tids[0];events.append(('hold',tid))
            try:yield [dict(tid=tid)]
            finally:events.append(('restore',tid))
        backend=SimpleNamespace(original=SimpleNamespace(threads=lambda pid:next(enumerations)))
        with patch.object(r.original_wait,'owned_frames',frames):
            with self.assertRaisesRegex(ValueError,'appeared'):
                with r.owned_cohort(SimpleNamespace(pid=7),77,backend):self.fail('unstable cohort yielded')
        self.assertEqual(events,[('hold',77),('hold',88),('restore',88),('restore',77)])


if __name__=='__main__':unittest.main()
