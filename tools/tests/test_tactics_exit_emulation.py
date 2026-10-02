"""Run original machine instructions; synthetic external inputs are explicit."""
import importlib.util
import hashlib
import json
from pathlib import Path
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.tactics_exit_emulation import (ExitEmulator, TASK, replay_case, report,
                                             report_text, godot_fixture)


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt in .venv-audit')
class TacticsExitEmulationTests(unittest.TestCase):
    def test_terminal_flag_and_transition_handshake(self):
        result = replay_case('terminal')
        self.assertTrue(result['transition_returned'])
        self.assertEqual(result['states'][0]['transition_phase'], 15)
        self.assertEqual(result['states'][0]['script_phase'], 6)
        self.assertEqual(result['states'][-1]['transition_phase'], 20)
        self.assertEqual(result['states'][-1]['transition_function_return'], 1)
        self.assertFalse(result['state11_observed'])
        self.assertFalse(result['authorizes_persistent_write'])

    def test_script_completion_is_not_task_exit(self):
        result = replay_case('intermediate', exit_flag=0)
        first = result['states'][0]
        self.assertEqual(first['script_function_return'], 1)
        self.assertEqual(first['script_control_active'], 0)
        self.assertEqual(first['finish_flags'][1], 0)
        self.assertFalse(result['transition_returned'])
        self.assertTrue(all(s['transition_phase'] == 5 for s in result['states']))
        self.assertTrue(all(s['script_function_return'] == 1 for s in result['states']))

    def test_checked_in_fixture_is_regenerated_from_original_instructions(self):
        root = Path(__file__).resolve().parents[2]
        expected = json.loads((root / 'prototype/data/tactics_exit_handshake_evidence.json')
                              .read_text(encoding='utf-8'))
        original_report = report()
        self.assertEqual(expected, godot_fixture(original_report))
        saved = (root / 'analysis/tactics-exit-emulation-v2-20261002.json').read_bytes()
        self.assertEqual(hashlib.sha256(saved).hexdigest(), expected['source_report_sha256'])
        self.assertEqual(saved.decode('utf-8'), report_text(original_report))

    def test_synthetic_out_of_order_initial_phase_loses_completion(self):
        result = replay_case('out_of_order', transition_phase=4)
        self.assertEqual(result['states'][0]['script_phase'], 6)
        self.assertEqual(result['states'][0]['finish_flags'][1], 0)
        self.assertTrue(all(s['transition_phase'] == 5 for s in result['states']))
        self.assertFalse(result['transition_returned'])

    def test_clock_and_animation_are_distinct_exit_prerequisites(self):
        clock = replay_case('clock', fade_step=0)
        animation = replay_case('animation', animation_ready=False)
        self.assertEqual(clock['states'][-1]['transition_phase'], 16)
        self.assertEqual(animation['states'][-1]['transition_phase'], 17)
        self.assertFalse(clock['transition_returned'])
        self.assertFalse(animation['transition_returned'])

    def test_vm_and_script_work_wait_before_finish_flags(self):
        emulator = ExitEmulator(vm_busy=True)
        emulator.write(TASK+0x44, 2, 'B')
        emulator.write(TASK+0x48, 1)
        emulator.write(TASK+0x4C, 1)
        emulator.write(TASK+0x50, 1)  # Nonzero request type takes the phase-3 path.
        emulator.call(0x454CF0)
        self.assertEqual(emulator.snapshot()['script_phase'], 2)
        self.assertEqual(emulator.snapshot()['finish_flags'], [0, 0, 0])
        emulator.external['vm_busy'] = False
        emulator.call(0x454CF0)
        self.assertEqual(emulator.snapshot()['script_phase'], 3)
        emulator.write(TASK+0x58, 1, 'B')
        emulator.external['script_work_busy'] = True
        emulator.call(0x454CF0)
        self.assertEqual(emulator.snapshot()['script_phase'], 4)
        emulator.call(0x454CF0)
        self.assertEqual(emulator.snapshot()['script_phase'], 4)
        emulator.external['script_work_busy'] = False
        emulator.call(0x454CF0)
        self.assertEqual(emulator.snapshot()['script_phase'], 5)
        emulator.call(0x454CF0)
        self.assertEqual(emulator.snapshot()['finish_flags'][1:], [1, 1])

    def test_zero_request_type_skips_phase_three_but_still_waits_for_work(self):
        emulator = ExitEmulator(script_work_busy=True)
        emulator.write(TASK+0x44, 2, 'B')
        emulator.write(TASK+0x48, 1)
        emulator.write(TASK+0x4C, 1)
        emulator.call(0x454CF0)
        self.assertEqual(emulator.snapshot()['script_phase'], 4)
        emulator.call(0x454CF0)
        self.assertEqual(emulator.snapshot()['script_phase'], 4)
        self.assertEqual(emulator.snapshot()['finish_flags'], [0, 0, 0])

    def test_report_cannot_claim_real_scene_or_authorize_transaction(self):
        evidence = report()
        self.assertEqual(evidence['evidence_kind'],
                         'original_x86_with_synthetic_external_inputs')
        self.assertFalse(evidence['authorizes_persistent_write'])
        self.assertGreater(len(evidence['stub_manifest']), 0)
        for case in evidence['cases']:
            self.assertFalse(case['state11_observed'])
            self.assertFalse(case['authorizes_persistent_write'])
            self.assertIn('synthetic_initial_state', case)

    def test_reject_invalid_entry_and_clock_input(self):
        emulator = ExitEmulator()
        with self.assertRaises(ValueError):
            emulator.call(0x451670)
        with self.assertRaises(ValueError):
            ExitEmulator(fade_step=-1)


if __name__ == '__main__':
    unittest.main()
