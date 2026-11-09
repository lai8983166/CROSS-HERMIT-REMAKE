from contextlib import contextmanager
from pathlib import Path
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from devtools import terminal_battle_wait_window as window


class WaitWindowTests(unittest.TestCase):
    def test_unqualified_host_rejected_before_output_or_native_code(self):
        with patch('devtools.native_input_isolation.require_qualified_guest',side_effect=PermissionError('not guest')):
            with patch.object(window,'startup_probe',side_effect=AssertionError('native must not run')):
                with self.assertRaisesRegex(PermissionError,'not guest'):
                    window.run(Path('not-created.json.gz'),'startup_preflight')
                with self.assertRaisesRegex(PermissionError,'not guest'):
                    window.WaitWindow(None,1,2,3,Path('not-created'),'startup_preflight',{})

    def test_start_occurs_before_second_query_without_replacing_button_value(self):
        events=[];values=iter((False,True))
        def query():events.append('query');return next(values)
        api=window.wrap_click_api(SimpleNamespace(left_button_down=query),lambda:events.append('start'))
        self.assertFalse(api.left_button_down());self.assertTrue(api.left_button_down())
        self.assertEqual(events,['query','start','query'])
        with self.assertRaisesRegex(ValueError,'two left-button'):
            api.left_button_down()

    def test_start_failure_prevents_last_query_and_input(self):
        api=SimpleNamespace(left_button_down=lambda:False)
        def fail():raise ValueError('trace unavailable')
        window.wrap_click_api(api,fail)
        self.assertFalse(api.left_button_down())
        with self.assertRaisesRegex(ValueError,'trace unavailable'):api.left_button_down()

    def test_explicit_trace_budget_preserves_modes_and_losses(self):
        _,p=window.properties(Path('owned.etl'))
        self.assertEqual((p.EnableFlags,p.MaximumFileSize,p.LogFileMode),(0x92,64,1))
        self.assertEqual((p.BufferSize,p.MinimumBuffers,p.MaximumBuffers),(64,4,8))
        self.assertEqual(window.TRACE_LIMITS['max_selected_records'],16384)

    def test_scoped_input_freeze_wrapper_restored_after_exception(self):
        from devtools import terminal_scene_owner as base
        calls=[]
        @contextmanager
        def frozen(*args):calls.append(args);yield ['original']
        observer=window.WaitWindow.__new__(window.WaitWindow);observer.lock=threading.RLock()
        with patch.object(base.original,'frozen',frozen):
            with self.assertRaisesRegex(RuntimeError,'test'):
                with observer.synchronized_input_snapshots():
                    with base.original.frozen(1,2)as frames:self.assertEqual(frames,['original'])
                    raise RuntimeError('test')
            self.assertIs(base.original.frozen,frozen)
        self.assertEqual(calls,[(1,2)])


if __name__=='__main__':unittest.main()
