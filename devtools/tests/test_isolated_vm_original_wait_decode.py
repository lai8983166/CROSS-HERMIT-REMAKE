import tempfile
import unittest
import json
from pathlib import Path, PureWindowsPath
from unittest.mock import patch

from devtools import isolated_vm_original_wait_decode as runner


class OfflineWaitResumeTests(unittest.TestCase):
    def test_invalid_labels_fail_before_guest_access(self):
        with patch.object(runner, 'run_script', side_effect=AssertionError('guest must not run')):
            for label in ('../old', '', 'a b', 'a;exit', 'A', 'a/b'):
                with self.subTest(label=label), self.assertRaises(ValueError):
                    runner.decode(label, 'source-v1')

    def test_existing_output_never_overwritten(self):
        with tempfile.TemporaryDirectory() as td, patch.object(runner, 'WORKER', Path(td)):
            path = Path(td) / 'terminal-original-wait-decode-new.json'
            path.write_bytes(b'preserve')
            with patch.object(runner, 'run_script', side_effect=AssertionError('guest must not run')):
                with self.assertRaisesRegex(ValueError, 'immutable'):
                    runner.decode('new', 'source-v1')
            self.assertEqual(path.read_bytes(), b'preserve')

    def test_guest_artifacts_cannot_escape_or_expand_transfer(self):
        expected = PureWindowsPath('C:/ChaomofaWorker/project/analysis/one.records.json.gz')
        valid = dict(path=str(expected), bytes=100, sha256='a' * 64)
        runner.checked_artifact(valid, expected, 65536)
        for changes in ({'path': 'C:/Windows/file'}, {'bytes': 65537}, {'bytes': 0}, {'sha256': 'unknown'}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                runner.checked_artifact(dict(valid, **changes), expected, 65536)

    def test_transfer_hash_rejection_survives_optimized_python(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'data'
            p.write_bytes(b'actual')
            good = runner.identity(p)
            self.assertEqual(runner.transferred(good, p), good)
            for changes in ({'bytes': 5}, {'sha256': '0' * 64}):
                with self.subTest(changes=changes), self.assertRaisesRegex(ValueError, 'mismatch'):
                    runner.transferred(dict(good, **changes), p)

    def test_existing_wrong_guest_file_is_never_overwritten(self):
        path = PureWindowsPath('C:/ChaomofaWorker/project/analysis/source.json.gz')
        expected = dict(bytes=10, sha256='a' * 64)
        with patch.object(runner, 'run_script', return_value=json.dumps(dict(exists=True, bytes=10, sha256='b' * 64))):
            with patch.object(runner, 'vmrun') as transfer:
                with self.assertRaisesRegex(ValueError, 'never overwrite'):
                    runner.restore_guest_artifact(Path('unused'), path, expected)
                transfer.assert_not_called()

    def test_retired_guest_copy_restored_with_pre_and_post_hash_checks(self):
        remote = PureWindowsPath('C:/ChaomofaWorker/project/analysis/source.json.gz')
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'source.json.gz'
            p.write_bytes(b'preserved')
            expected = runner.identity(p)
            replies = [json.dumps(dict(exists=False)), 'ready', json.dumps(dict(expected, exists=True))]
            with patch.object(runner, 'run_script', side_effect=replies):
                with patch.object(runner, 'vmrun') as transfer:
                    result = runner.restore_guest_artifact(p, remote, expected)
                    self.assertTrue(result['restored'])
                    transfer.assert_called_once_with(['CopyFileFromHostToGuest', runner.VMX, p, remote], guest=True)

    def test_restore_cannot_write_outside_guest_analysis(self):
        with patch.object(runner, 'run_script') as guest:
            for path in ('C:/Windows/test', 'C:/ChaomofaWorker/project/analysis/../test'):
                with self.subTest(path=path), self.assertRaises(ValueError):
                    runner.restore_guest_artifact(Path('unused'), PureWindowsPath(path), {})
            guest.assert_not_called()


if __name__ == '__main__':
    unittest.main()
