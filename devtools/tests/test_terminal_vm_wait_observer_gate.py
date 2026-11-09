import unittest
from unittest.mock import patch
from devtools import terminal_vm_wait_observer_gate as gate


class WaitMonitorGateTests(unittest.TestCase):
    def test_acknowledged_request_does_not_qualify_observer(self):
        result = gate.witness()
        self.assertTrue(result['hidden_breakpoint_request_acknowledged'])
        self.assertFalse(result['native_wait_monitor_supported'])
        self.assertFalse(result['actual_wait_return_observed'])

    def test_launch_rejected_without_reading_source_or_opening_socket(self):
        with patch.object(gate.Path, 'read_bytes', side_effect=AssertionError('no launch dependency')):
            with self.assertRaisesRegex(RuntimeError, 'disabled'):
                gate.require_supported_monitor()


if __name__ == '__main__':
    unittest.main()
