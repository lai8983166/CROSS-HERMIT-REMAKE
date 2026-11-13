"""Offline regressions of the observed taskbar failure and recovery admission."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from devtools import terminal_window_desktop as desktop
from devtools.tests.test_terminal_host_desktop import healthy


def baseline():
    value = healthy()
    value.update(last_input_tick=123, foreground_identity=dict(hwnd=4, pid=5, process_created=77),
                 taskbar_identities=[dict(hwnd=1, pid=2, process_created=66)], mode_bytes={},
                 system_work_area=[0, 0, 3072, 1688])
    return value


class ScriptedDesktop:
    def __init__(self, states, fail_repair=False):
        self.states, self.calls, self.fail_repair = iter(states), [], fail_repair
    def read(self):
        value = next(self.states)
        if isinstance(value, Exception):
            raise value
        return copy.deepcopy(value)
    def repair(self, before, after):
        self.calls.append((before, after))
        if self.fail_repair:
            raise ValueError('original taskbar process lifetime changed')
        return [dict(api='model_only', actual_host_write=False)]


class WindowDesktopTests(unittest.TestCase):
    def run_case(self, backend, action, failure=False):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parents[2]/'.venv-audit') as folder:
            output = Path(folder)/'receipt.json'
            if failure:
                with self.assertRaises(ValueError):
                    desktop.guarded_run(action, output, backend=backend, sleep=lambda _: None)
            else:
                desktop.guarded_run(action, output, backend=backend, sleep=lambda _: None)
            return json.loads(output.read_text(encoding='utf8'))

    def test_observed_collapsed_taskbar_can_recover_only_after_job_empty(self):
        bad = baseline()
        bad['taskbars'][0]['rect'] = [0, 1727, 3072, 1728]
        backend = ScriptedDesktop([baseline(), bad, baseline(), baseline()])
        result = self.run_case(backend, lambda: dict(cleanup=dict(job_empty=True)))
        self.assertTrue(result['restored'])
        self.assertEqual(len(backend.calls), 1)
        self.assertEqual(result['checks'], [[], []])

    def test_live_job_prevents_any_desktop_writes(self):
        bad = baseline()
        bad['taskbars'][0]['visible'] = False
        backend = ScriptedDesktop([baseline(), bad])
        result = self.run_case(backend, lambda: dict(cleanup=dict(job_empty=False)), True)
        self.assertFalse(result['restored'])
        self.assertEqual(backend.calls, [])

    def test_new_user_input_preserves_the_users_current_desktop(self):
        bad = baseline()
        bad['last_input_tick'] += 1
        bad['input_desktop'].update(foreground_hwnd=9, foreground_pid=10)
        backend = ScriptedDesktop([baseline(), bad])
        result = self.run_case(backend, lambda: dict(cleanup=dict(job_empty=True)), True)
        self.assertIn('user resumed input', result['recovery_error'])
        self.assertEqual(backend.calls, [])

    def test_bad_initial_taskbar_never_launches_window(self):
        bad = baseline()
        bad['taskbars'] = []
        called = []
        backend = ScriptedDesktop([bad, bad, bad, bad])
        result = self.run_case(backend, lambda: called.append(True), True)
        self.assertEqual(called, [])
        self.assertFalse(result['action_started'])

    def test_partial_repair_does_not_pass(self):
        bad = baseline()
        bad['system_work_area'] = [0, 0, 3072, 1728]
        backend = ScriptedDesktop([baseline(), bad, baseline(), bad])
        result = self.run_case(backend, lambda: dict(cleanup=dict(job_empty=True)), True)
        self.assertFalse(result['restored'])

    def test_taskbar_lifetime_mismatch_does_not_expand_repair(self):
        bad = baseline()
        bad['taskbars'][0]['visible'] = False
        backend = ScriptedDesktop([baseline(), bad], fail_repair=True)
        result = self.run_case(backend, lambda: dict(cleanup=dict(job_empty=True)), True)
        self.assertIn('lifetime changed', result['recovery_error'])

    def test_query_timeout_cannot_count_as_restoration(self):
        backend = ScriptedDesktop([baseline(), TimeoutError('five second OS query limit')])
        result = self.run_case(backend, lambda: dict(cleanup=dict(job_empty=True)), True)
        self.assertFalse(result['restored'])
        self.assertIn('five second', result['recovery_error'])

    def test_failed_native_case_still_checks_restoration(self):
        backend = ScriptedDesktop([baseline()]*4)
        result = self.run_case(backend, lambda: dict(accepted=False, cleanup=dict(job_empty=True)))
        self.assertTrue(result['restored'])
        self.assertFalse(result['automatic_recovery_attempted'])

    def test_actor_exception_cannot_claim_test_success(self):
        backend = ScriptedDesktop([baseline()]*4)
        def fail():
            raise RuntimeError('owned process setup failed')
        result = self.run_case(backend, fail, True)
        self.assertTrue(result['restored'])
        self.assertIn('setup failed', result['action_error'])


if __name__ == '__main__':
    unittest.main()
