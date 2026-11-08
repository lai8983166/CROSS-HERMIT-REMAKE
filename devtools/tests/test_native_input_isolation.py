import copy
import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch
from devtools import native_input_isolation as isolation
from devtools import terminal_school_handoff as collector
from devtools.tests.test_isolated_vm_preflight import fixture


class NativeIsolationTests(unittest.TestCase):
    def test_physical_host_and_other_virtual_desktops_refused(self):
        for machine in (
            dict(computer_name='DESKTOP-USER',manufacturer='Micro-Star International',uuid='0'*36),
            dict(computer_name='CHAOMOFA-WORKER',manufacturer='Micro-Star International',uuid='0'*36),
            dict(computer_name='OTHER-WINDOWS',manufacturer='VMware, Inc.',uuid='0'*36)):
            with self.assertRaises(RuntimeError):isolation.validate_machine(machine)
    def test_host_launch_refused_before_catalog_or_original_runtime(self):
        with patch.object(collector,'require_qualified_guest',side_effect=RuntimeError('shared desktop disabled')),patch.object(collector,'Catalog')as catalog,patch.object(collector,'clone')as clone:
            with self.assertRaisesRegex(RuntimeError,'shared desktop disabled'):collector.run(None,1800)
            catalog.assert_not_called();clone.assert_not_called()
    def test_guest_without_preflight_cannot_launch(self):
        with patch.object(isolation,'current_machine',return_value=fixture()['guest']['machine']),patch.object(isolation,'QUALIFICATION')as path:
            path.is_file.return_value=False
            with self.assertRaisesRegex(RuntimeError,'preflight must pass'):isolation.require_qualified_guest()

    def qualify(self,change=None):
        report=fixture();machine=copy.deepcopy(report['guest']['machine'])
        if change:change(machine)
        raw=json.dumps(report).encode()
        with patch.object(isolation,'current_machine',return_value=machine),patch.object(isolation,'QUALIFICATION')as path:
            path.is_file.return_value=True;path.stat.return_value=SimpleNamespace(st_size=len(raw));path.read_bytes.return_value=raw
            return isolation.require_qualified_guest()

    def test_current_boot_resources_qualified(self):
        result=self.qualify()
        self.assertEqual(result['current_guest_boot_utc'],'2026-11-08T01:02:03.1234560Z')
        self.assertEqual(result['current_guest_resources'],dict(logical_processors=2,memory_bytes=4*1024**3))

    def test_old_boot_qualification_rejected(self):
        with self.assertRaisesRegex(RuntimeError,'different guest boot'):
            self.qualify(lambda m:m.update(boot_utc='2026-11-08T01:03:03.1234560Z'))

    def test_changed_cpu_rejected(self):
        with self.assertRaisesRegex(RuntimeError,'resource bound'):self.qualify(lambda m:m.update(logical_processors=4))

    def test_memory_change_within_limit_still_rejected(self):
        with self.assertRaisesRegex(RuntimeError,'differ from qualified'):self.qualify(lambda m:m.update(memory_bytes=4*1024**3-4096))

    def test_memory_outside_limit_rejected(self):
        with self.assertRaisesRegex(RuntimeError,'resource bound'):self.qualify(lambda m:m.update(memory_bytes=5*1024**3))

    def test_current_boot_missing_rejected(self):
        with self.assertRaisesRegex(RuntimeError,'boot UTC'):self.qualify(lambda m:m.pop('boot_utc'))

    def test_machine_query_is_fresh_for_each_gate(self):
        machine=fixture()['guest']['machine']
        with patch.object(isolation.subprocess,'run',return_value=SimpleNamespace(stdout=json.dumps(machine)))as run:
            isolation.current_machine();isolation.current_machine()
            self.assertEqual(run.call_count,2)

    def test_guest_query_cannot_create_a_foreground_console(self):
        machine=fixture()['guest']['machine']
        with patch.object(isolation.subprocess,'run',return_value=SimpleNamespace(stdout=json.dumps(machine)))as run, \
             patch.object(isolation.subprocess,'CREATE_NO_WINDOW',0x08000000,create=True):
            self.assertEqual(isolation.current_machine(),machine)
            self.assertEqual(run.call_args.kwargs['creationflags'],0x08000000)
            self.assertTrue(run.call_args.kwargs['capture_output'])
            self.assertEqual(run.call_args.kwargs['timeout'],20)


if __name__=='__main__':unittest.main()
