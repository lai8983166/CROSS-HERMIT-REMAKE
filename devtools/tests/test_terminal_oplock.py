"""Failure-path lifetime checks; native qualification is a separate receipt."""
import ctypes as C
import threading
import unittest
from types import SimpleNamespace
from unittest.mock import Mock
from devtools.terminal_oplock import ReadOplock, Output, Overlapped, PENDING_OWNERS, RW_LEVEL


class CleanupTests(unittest.TestCase):
    def make_lock(self, *, close=True, wait=0):
        obj=ReadOplock.__new__(ReadOplock)
        obj.handle=123;obj.event=456;obj.timer=Mock();obj.mutex=threading.Lock()
        obj.overlap=Overlapped();obj.output=Output(1,C.sizeof(Output),RW_LEVEL,0,1,0,0)
        obj.w=SimpleNamespace(close=Mock(return_value=close),wait=Mock(return_value=wait),qpc=lambda:123,
            check=lambda good,label: self.check(good,label))
        obj.receipt=dict(arm_ns=1,file_closed=False,async_completed=False,event_closed=False,watchdog_release=False)
        return obj

    @staticmethod
    def check(good,label):
        if not good:raise OSError(label)

    def tearDown(self):
        # These are inert fake handles, never real pending kernel requests.
        PENDING_OWNERS.clear()

    def test_file_close_precedes_async_buffer_and_event_retirement(self):
        obj=self.make_lock();r=obj.finish()
        self.assertEqual([c.args[0] for c in obj.w.close.call_args_list],[123,456])
        self.assertTrue(r['file_closed'] and r['async_completed'] and r['event_closed'])
        self.assertEqual(PENDING_OWNERS,[])

    def test_unconfirmed_completion_keeps_buffers_and_event_pinned(self):
        obj=self.make_lock(wait=258)
        with self.assertRaisesRegex(ValueError,'completed'):obj.finish()
        self.assertEqual(PENDING_OWNERS,[obj]);self.assertEqual(obj.event,456)
        self.assertEqual(obj.w.close.call_count,1)

    def test_failed_close_preserves_watchdog_and_async_owner(self):
        obj=self.make_lock(close=False)
        with self.assertRaises(OSError):obj.finish()
        obj.timer.cancel.assert_not_called();obj.w.wait.assert_not_called()
        self.assertEqual(obj.handle,123);self.assertEqual(PENDING_OWNERS,[obj])

    def test_read_handle_level_is_not_read_write_gate(self):
        obj=self.make_lock();obj.output.original_level=3
        with self.assertRaisesRegex(ValueError,'actual RW break'):obj.observe_break(0)

    def test_break_without_ack_requirement_cannot_gate(self):
        obj=self.make_lock();obj.output.flags=0
        with self.assertRaisesRegex(ValueError,'actual RW break'):obj.observe_break(0)


if __name__=='__main__':unittest.main()
