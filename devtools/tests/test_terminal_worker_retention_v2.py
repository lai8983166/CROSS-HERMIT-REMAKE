import ctypes as C
import ctypes.wintypes as W
import struct
from types import SimpleNamespace
import unittest
from devtools import terminal_worker_retention_v2 as v


class RetentionTransitionTests(unittest.TestCase):
    def tracker(self,foreign=False,wait=0,code=0):
        calls=[]
        def exit_thread(handle,p):C.cast(p,C.POINTER(W.DWORD)).contents.value=code;return True
        def check(ok,msg):
            if not ok:raise OSError(msg)
        backend=SimpleNamespace(original=SimpleNamespace(wait=lambda h,t:wait,memory=lambda h,p,n:bytes(n),check=check),
            parent=SimpleNamespace(exit_thread=exit_thread),get_thread_pid=lambda h:8 if foreign else 7,get_thread_id=lambda h:88)
        c=SimpleNamespace(h=9,pid=7,get=lambda p,n:calls.append((p,n))or bytes(n))
        tracker=v.WorkerRetention(c,77,backend)
        tracker.handles[(100,88)]=999
        tracker.workers=[dict(pointer=100,thread_id=88,vtable=0x5C306C,original_handle=48,event=dict(remote_handle=44),first_elapsed=1)]
        raw=bytearray(64)
        for offset,value in ((0,0x594A54),(4,4),(0x1C,44),(0x20,48),(0x24,88)):struct.pack_into('<I',raw,offset,value)
        row=dict(elapsed=2,tasks=[dict(pointer=100,thread_id=88,vtable=0x594A54,header_hex=raw.hex())],
            frames=[dict(tid=77,chain=[dict(bp=0x2000,return_va=0x42182F)])],worker_retention=dict(tasks=[]))
        return tracker,row,calls

    def test_transition_keeps_raw_vtable_and_historical_owner_without_acceptance(self):
        tracker,row,calls=self.tracker();raw=row['tasks'][0]['header_hex'];tracker.retain(row)
        proof=row['worker_retention']['tasks'][0]
        self.assertEqual(proof['status'],'retained_vtable_transition')
        self.assertFalse(proof['transition']['transition_verified'])
        self.assertEqual(row['tasks'][0]['header_hex'],raw)
        self.assertEqual(tracker.workers[0]['vtable'],0x5C306C)
        self.assertEqual(calls,[(0x2000-0x5C,0x6C)])

    def test_foreign_handle_changed_event_and_bad_exit_still_fail(self):
        for kind in ('foreign','event','exit'):
            tracker,row,calls=self.tracker(foreign=kind=='foreign',code=5 if kind=='exit'else 0)
            if kind=='event':tracker.workers[0]['event']['remote_handle']=55
            with self.subTest(kind=kind),self.assertRaises(ValueError):tracker.retain(row)
            self.assertIs(tracker.failure['row'],row)

    def test_unclassified_live_vtable_is_recorded_but_never_promoted_to_retirement(self):
        tracker,row,_=self.tracker(wait=258,code=259);tracker.retain(row)
        proof=row['worker_retention']['tasks'][0]['transition']
        self.assertEqual(proof['thread_query']['exit_code'],259)
        self.assertFalse(proof['full_resource_PTD_cleanup_proved'])


if __name__=='__main__':unittest.main()
