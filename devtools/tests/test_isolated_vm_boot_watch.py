import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from devtools import isolated_vm_boot_watch as boot
from devtools.isolated_windows_vm import WORKER


class BootOwnershipTests(unittest.TestCase):
    def setUp(self):
        temp = WORKER / 'tmp'
        temp.mkdir(parents=True, exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(dir=temp)
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.vmx = self.root / 'owned.vmx'
        self.vmx.write_text('test fixture', encoding='utf8')
        (self.root / 'vmware.log').write_text('WinBSOD: fixture\n', encoding='utf8')
        for name, value in [('WORKER', self.root), ('VMX', self.vmx)]:
            p = patch.object(boot, name, value)
            p.start();self.addCleanup(p.stop)
        for name in ('validate_vmx', 'validate_disk'):
            p = patch.object(boot, name)
            p.start();self.addCleanup(p.stop)

    def test_active_worker_is_refused_without_start_or_stop(self):
        with patch.object(boot, 'vmrun', return_value=str(self.vmx)) as call:
            with self.assertRaises(ValueError):
                boot.watch('active', 30)
        self.assertEqual([c.args[0] for c in call.call_args_list], [['list']])

    def test_bugcheck_cleanup_cannot_target_another_vm(self):
        calls = []
        def invoke(args, **kwargs):
            calls.append(args)
            if args[0] == 'list':
                return '' if len(calls) == 1 or any(c[0] == 'stop' for c in calls) else str(self.vmx)
            return ''
        with patch.object(boot, 'vmrun', side_effect=invoke):
            report = boot.watch('crash', 30)
        self.assertEqual(report['stop_reason'], 'guest_bugcheck')
        self.assertEqual([c for c in calls if c[0] == 'stop'], [['stop', self.vmx, 'hard']])
        self.assertEqual(report['cleanup_errors'], [])
        self.assertEqual(json.loads((self.root / 'boot-crash.json').read_bytes()), report)

    def test_query_and_stop_failure_still_preserve_failure_report(self):
        calls = []
        def invoke(args, **kwargs):
            calls.append(args)
            if len(calls) == 1 or args[0] == 'start':
                return ''
            raise RuntimeError('fixture unavailable')
        with patch.object(boot, 'vmrun', side_effect=invoke):
            report = boot.watch('cleanup-failure', 30)
        self.assertEqual([c for c in calls if c[0] == 'stop'], [['stop', self.vmx, 'hard']])
        self.assertEqual(len(report['cleanup_errors']), 3)
        self.assertFalse(report['accepted'])
        self.assertTrue((self.root / 'boot-cleanup-failure.json').is_file())


if __name__ == '__main__':
    unittest.main()
