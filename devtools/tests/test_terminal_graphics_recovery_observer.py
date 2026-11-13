import unittest
from unittest.mock import patch
from devtools.terminal_graphics_recovery_observer_v2 import GuardedReadOnlyWindowsBackend
from devtools import terminal_graphics_desktop as parent

class ReadOnlyEntryTests(unittest.TestCase):
    def test_all_exposed_mutation_routes_reject_before_native_api(self):
        observer=GuardedReadOnlyWindowsBackend.__new__(GuardedReadOnlyWindowsBackend)
        with patch.object(parent.C,'WinDLL',side_effect=AssertionError('unexpected native API')):
            for call in (lambda:observer.write('mode',{}),lambda:observer.repair({},{}),lambda:observer._gamma('DISPLAY1','00'*1536)):
                with self.assertRaisesRegex(ValueError,'read-only observer forbids'):call()
    def test_read_gamma_only_uses_parent_query(self):
        observer=GuardedReadOnlyWindowsBackend.__new__(GuardedReadOnlyWindowsBackend)
        with patch.object(parent.WindowsBackend,'_gamma',return_value='saved') as query:
            self.assertEqual(observer._gamma('DISPLAY1'),'saved');query.assert_called_once_with('DISPLAY1')
    def test_frozen_native_restoration_gate_remains_closed(self):
        self.assertFalse(parent.NATIVE_ADMISSION)

if __name__=='__main__':unittest.main()
