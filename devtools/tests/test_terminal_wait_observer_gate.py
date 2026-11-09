import unittest
from unittest.mock import patch
from devtools import terminal_wait_observer_gate as gate


class KnownIncompatibleGateTests(unittest.TestCase):
    def test_fixed_native_failure_is_not_a_wait_or_cleanup_success(self):
        r=gate.witness()
        self.assertFalse(r['accepted']or r['observed_wait_return']or r['native_wait_relay_supported'])
        self.assertTrue(r['forced_Job_cleanup']and r['child_exit_queried_only_after_emergency_cleanup'])
    def test_runner_rejects_before_VM_or_deployment(self):
        from devtools import isolated_vm_run as runner
        with patch.object(runner,'vmrun',side_effect=AssertionError('must not reach VM')),patch.object(runner,'run_script',side_effect=AssertionError('must not deploy')):
            with self.assertRaisesRegex(RuntimeError,'disabled'):runner.run('wait-probe','not-a-retry')
    def test_direct_probe_and_relay_reject_before_qualification_or_native_calls(self):
        from devtools import terminal_wait_native_probe as probe,terminal_debug_relay as relay
        with patch.object(probe,'require_qualified_guest',side_effect=AssertionError('must not reach qualification')):
            with self.assertRaisesRegex(RuntimeError,'disabled'):probe.run(None)
        with patch('devtools.native_input_isolation.require_qualified_guest',side_effect=AssertionError('must not reach qualification')):
            with self.assertRaisesRegex(RuntimeError,'disabled'):relay.observe(None,None,0,0,None)


if __name__=='__main__':unittest.main()
