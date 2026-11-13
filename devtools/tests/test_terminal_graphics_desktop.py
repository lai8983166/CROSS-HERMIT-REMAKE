"""Bounded offline models exercising the real parent recovery orchestration."""
import copy
import unittest
from unittest.mock import patch

from devtools import terminal_graphics_desktop as d
from devtools.tests.test_terminal_window_desktop import baseline as window_baseline

DEVICE = 'DISPLAY1'
ORIGINAL_RAMP = (bytes(range(256)) * 6).hex()  # Deliberately not a linear ramp.
OTHER_RAMP = (bytes(reversed(range(256))) * 6).hex()
RESET_RAMP = (b'\x00\x13' * 768).hex()
OWNER = dict(run_id='offline-model-1', pid=11, process_created=22, main_tid=33, main_teb=44)


def state():
    value = window_baseline()
    value.update(display_identities={DEVICE: dict(adapter='adapter-A', monitor='monitor-A')},
        original_foreground_identity=copy.deepcopy(value['foreground_identity']),
        shell_identity=dict(hwnd=3, pid=2, process_created=66),
        cursor=dict(flags=1, handle=81, position=[21, 32], clip=[0, 0, 3072, 1728]),
        graphics=dict(device=DEVICE, gamma_hex=ORIGINAL_RAMP), tick64=1000,
        input_observer=dict(pid=101, process_created=202, session_id=1, last_input_tick=123))
    return value


class ModelBackend:
    evidence_kind = 'model'

    def __init__(self):
        self.state, self.calls, self.reads = state(), [], 0
        self.gamma_noop = False
        self.on_read = None

    def read(self, device, *, foreground_identity=None):
        self.reads += 1
        if self.on_read:
            self.on_read(self, self.reads)
        return copy.deepcopy(self.state)

    def write(self, kind, value, *, device, baseline):
        self.calls.append(kind)
        s = self.state
        if kind == 'mode':
            s['monitors'][0]['mode'] = copy.deepcopy(value)
            s['graphics']['gamma_hex'] = RESET_RAMP
        elif kind == 'gamma':
            if not self.gamma_noop:
                s['graphics']['gamma_hex'] = value
        elif kind == 'cursor_clip':
            s['cursor']['clip'] = copy.deepcopy(value)
        elif kind == 'cursor_position':
            s['cursor']['position'] = copy.deepcopy(value)
        elif kind == 'taskbars':
            s['taskbars'] = copy.deepcopy(value)
        elif kind == 'work_area':
            s['system_work_area'] = copy.deepcopy(value)
        elif kind == 'foreground':
            s['foreground_identity'] = copy.deepcopy(value)
            s['input_desktop']['foreground_hwnd'] = value['hwnd']
            s['input_desktop']['foreground_pid'] = value['pid']
        else:
            raise AssertionError(kind)
        return 1


def receipt(baseline, backend):
    events = []
    for index, kind in enumerate(('input_unacquire', 'input_release', 'graphics_gamma_restore',
                                 'graphics_release', 'window_destroy', 'job_empty')):
        events.append(dict(seq=index+1, kind=kind, observed=True, source_ref='model-explicit-'+str(index),
            baseline_token=baseline['baseline_token'], window_alive=True, main_tid=33, main_teb=44,
            window_identity=dict(hwnd=77, generation=1)))
    events[0].update(hresults=[0, 1])
    events[1].update(remaining_refs=0, objects=3)
    events[2].update(device_alive=True, saved_hex=ORIGINAL_RAMP, readback_hex=ORIGINAL_RAMP)
    events[3].update(remaining_refs=0, live_resources=0, locked_resources=0)
    events[4].update(is_window=False, destroy_result=1)
    events[5].update(active_processes=0)
    mutations = copy.deepcopy(d._mutable(backend.state, DEVICE))
    return dict(schema=d.SCHEMA, evidence_kind='model', owner=OWNER.copy(),
        window_identity=dict(hwnd=77, generation=1), baseline_token=baseline['baseline_token'],
        owner_cursor_receipt=dict(source_ref='model-cursor-owner', main_tid=33, main_teb=44,
            net_showcursor_delta=0, flags=1, handle=81), events=events, mutations=mutations,
        mutation_sources={key: dict(source_ref='model-mutation-'+key, owner=OWNER.copy(),
            baseline_token=baseline['baseline_token']) for key in mutations})


class GraphicsDesktopTests(unittest.TestCase):
    def prepare(self):
        backend = ModelBackend()
        baseline = d.capture_baseline(backend, DEVICE, OWNER)
        return backend, baseline

    def run_recovery(self, backend, baseline, rec=None, **kwargs):
        return d.recover(baseline, rec or receipt(baseline, backend), backend, sleep=lambda _: None, **kwargs)

    def test_import_and_constructor_do_not_load_windows_libraries(self):
        with patch.object(d.C, 'WinDLL', side_effect=AssertionError('forbidden native load')):
            for armed in (False, True):
                with self.assertRaisesRegex(ValueError, 'native recovery closed'):
                    d.WindowsBackend(armed=armed)

    def test_unchanged_state_requires_two_readbacks(self):
        backend, baseline = self.prepare()
        out = self.run_recovery(backend, baseline)
        self.assertTrue(out['restored'], out)
        self.assertEqual(out['checks'], [[], []])
        self.assertEqual(backend.calls, [])
        self.assertEqual(out['evidence_kind'], 'model')
        self.assertFalse(out['native_admission'])

    def test_mode_reset_then_original_gamma_then_cursor_and_shell(self):
        backend, baseline = self.prepare()
        backend.state['monitors'][0]['mode']['width'] = 800
        backend.state['graphics']['gamma_hex'] = OTHER_RAMP
        backend.state['cursor'].update(clip=[0, 0, 800, 600], position=[10, 10])
        backend.state['taskbars'][0]['visible'] = False
        backend.state['system_work_area'] = [0, 0, 800, 600]
        backend.state['foreground_identity'] = dict(hwnd=55, pid=56, process_created=57)
        backend.state['input_desktop'].update(foreground_hwnd=55, foreground_pid=56)
        out = self.run_recovery(backend, baseline)
        self.assertTrue(out['restored'], out)
        self.assertEqual(backend.calls, ['mode', 'gamma', 'cursor_clip', 'cursor_position',
                                        'taskbars', 'work_area', 'foreground'])
        gammas = [x['gamma_hex'] for x in out['observations']]
        self.assertIn(RESET_RAMP, gammas)
        self.assertEqual(gammas[-2:], [ORIGINAL_RAMP] * 2)

    def test_set_gamma_true_without_application_fails_actual_readback(self):
        backend, baseline = self.prepare()
        backend.state['graphics']['gamma_hex'] = OTHER_RAMP
        backend.gamma_noop = True
        out = self.run_recovery(backend, baseline)
        self.assertFalse(out['restored'])
        self.assertIn('gamma: actual readback mismatch', out['error'])
        self.assertEqual(out['actions'], [dict(kind='gamma', attempted=True, actual_return=1)])

    def test_live_job_refuses_before_any_observation_or_write(self):
        backend, baseline = self.prepare()
        rec = receipt(baseline, backend)
        rec['events'][-1]['active_processes'] = 1
        out = self.run_recovery(backend, baseline, rec)
        self.assertFalse(out['restored'])
        self.assertEqual(backend.reads, 1)
        self.assertEqual(backend.calls, [])

    def test_window_destroyed_before_input_release_refuses(self):
        backend, baseline = self.prepare()
        rec = receipt(baseline, backend)
        rec['events'][1]['window_alive'] = False
        out = self.run_recovery(backend, baseline, rec)
        self.assertIn('while original window alive', out['error'])
        self.assertEqual(backend.calls, [])

    def test_wrong_release_order_refuses(self):
        backend, baseline = self.prepare()
        rec = receipt(baseline, backend)
        rec['events'][1]['kind'], rec['events'][4]['kind'] = rec['events'][4]['kind'], rec['events'][1]['kind']
        self.assertIn('before graphics/window', self.run_recovery(backend, baseline, rec)['error'])

    def test_model_cannot_be_promoted_to_native(self):
        backend, baseline = self.prepare()
        rec = receipt(baseline, backend)
        rec['evidence_kind'] = 'native'
        self.assertIn('model/native', self.run_recovery(backend, baseline, rec)['error'])

    def test_baseline_tamper_and_missing_gamma_bytes_refuse(self):
        backend, baseline = self.prepare()
        rec = receipt(baseline, backend)
        baseline['state']['graphics']['gamma_hex'] = OTHER_RAMP
        self.assertIn('baseline token changed', self.run_recovery(backend, baseline, rec)['error'])
        with self.assertRaisesRegex(ValueError, '1536-byte'):
            d.ramp(ORIGINAL_RAMP[:-2])

    def test_new_input_adapter_shell_foreground_and_shape_are_preserved(self):
        changes = [
            lambda s: s['input_observer'].update(last_input_tick=124),
            lambda s: s['display_identities'][DEVICE].update(monitor='replacement'),
            lambda s: s['shell_identity'].update(process_created=999),
            lambda s: s['foreground_identity'].update(process_created=999),
            lambda s: s['original_foreground_identity'].update(process_created=999),
            lambda s: s['cursor'].update(flags=0),
            lambda s: s['cursor'].update(handle=999),
        ]
        for change in changes:
            with self.subTest(change=change):
                backend, baseline = self.prepare()
                rec = receipt(baseline, backend)
                change(backend.state)
                out = self.run_recovery(backend, baseline, rec)
                self.assertFalse(out['restored'])
                self.assertEqual(backend.calls, [])

    def test_input_between_attribution_and_write_refuses(self):
        backend, baseline = self.prepare()
        backend.state['graphics']['gamma_hex'] = OTHER_RAMP
        rec = receipt(baseline, backend)
        def new_input(b, reads):
            if reads == 3:
                b.state['input_observer']['last_input_tick'] += 1
        backend.on_read = new_input
        out = self.run_recovery(backend, baseline, rec)
        self.assertIn('new user input', out['error'])
        self.assertEqual(backend.calls, [])

    def test_final_gamma_drift_fails_second_stable_read(self):
        backend, baseline = self.prepare()
        def drift(b, reads):
            if reads == 4:
                b.state['graphics']['gamma_hex'] = OTHER_RAMP
        backend.on_read = drift
        out = self.run_recovery(backend, baseline)
        self.assertFalse(out['restored'])
        self.assertEqual(out['checks'], [[], ['gamma_changed']])

    def test_budget_exhaustion_is_not_success(self):
        backend, baseline = self.prepare()
        out = self.run_recovery(backend, baseline, budget=d.Budget(max_operations=1))
        self.assertFalse(out['restored'])
        self.assertIn('budget exhausted', out['error'])

    def test_unbalanced_owner_cursor_is_not_parent_showcursor_loop(self):
        backend, baseline = self.prepare()
        rec = receipt(baseline, backend)
        rec['owner_cursor_receipt']['net_showcursor_delta'] = -1
        self.assertIn('visibility count balanced', self.run_recovery(backend, baseline, rec)['error'])
        self.assertEqual(backend.calls, [])


if __name__ == '__main__':
    unittest.main()
