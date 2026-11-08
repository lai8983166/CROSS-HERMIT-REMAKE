import sys
import types
import unittest
from unittest.mock import Mock, patch
from devtools import isolated_guest_focus as focus
from devtools import native_input_isolation
from tools import school_native_dialogue_input


class FocusTests(unittest.TestCase):
    def run_focus(self, *, foreign=False, detach=True, activation=True):
        state = {'foreground': 10}
        calls = []
        def foreground_window(hwnd):
            if len(calls) and calls[-1] is True and activation:
                state['foreground'] = hwnd
            return state['foreground'] == hwnd
        def attach(a, b, enabled):
            calls.append(bool(enabled))
            return True if enabled else detach
        def owner(hwnd, pid):
            pid._obj.value = 99
            return 44
        def session(pid, value):
            value._obj.value = 2 if foreign and pid == 99 else 1
            return True
        api = {'GetForegroundWindow': lambda: state['foreground'],
               'SetForegroundWindow': foreground_window, 'AttachThreadInput': attach}
        original = types.SimpleNamespace(ubind=lambda name, *args: api[name], ownerpid=owner)
        kernel = types.SimpleNamespace(GetCurrentThreadId=Mock(return_value=22),
            GetCurrentProcessId=Mock(return_value=33), WTSGetActiveConsoleSessionId=Mock(return_value=1),
            ProcessIdToSessionId=Mock(side_effect=session))
        def guard(c, hwnd, require_foreground=True):
            if require_foreground and state['foreground'] != hwnd:
                raise ValueError('foreground mismatch')
        self.calls = calls
        with patch.dict(sys.modules, {'tools.school_native_scene': types.SimpleNamespace(original=original)}), \
             patch('devtools.native_input_isolation.require_qualified_guest', return_value={
                 'current_guest_uuid':'guest-test', 'current_guest_boot_utc':'boot-test'}), \
             patch('tools.school_native_dialogue_input.owned_target_guard', side_effect=guard), \
             patch.object(focus.C, 'WinDLL', return_value=kernel, create=True):
            return focus.focus_owned_window(types.SimpleNamespace(pid=55), 20)

    def test_same_guest_queue_detached_after_success(self):
        receipt = self.run_focus()
        self.assertEqual(self.calls, [True, False])
        self.assertEqual(receipt['after'], 20)

    def test_other_session_refused_before_attachment(self):
        with self.assertRaisesRegex(ValueError, 'console session'):
            self.run_focus(foreign=True)
        self.assertEqual(self.calls, [])

    def test_failed_activation_still_detaches(self):
        with self.assertRaisesRegex(ValueError, 'foreground mismatch'):
            self.run_focus(activation=False)
        self.assertEqual(self.calls, [True, False])

    def test_detachment_failure_rejected(self):
        with self.assertRaisesRegex(ValueError, 'detachment failed'):
            self.run_focus(detach=False)


if __name__ == '__main__':
    unittest.main()
