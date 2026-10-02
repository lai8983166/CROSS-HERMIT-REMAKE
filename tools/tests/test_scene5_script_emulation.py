"""Source-backed VM control replay; simulated callbacks never become live evidence."""
import hashlib
import importlib.util
import json
from pathlib import Path
import struct
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.scene5_script_emulation import (Scene5Emulator, VM, SCRIPT, ROOT,
                                              report, godot_fixture)
    from tools.tactics_exit_emulation import report_text


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt in .venv-audit')
class Scene5ScriptEmulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = report()
        cls.cases = {case['name']: case for case in cls.evidence['cases']}
        cls.source = (ROOT / 'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/SCRIPT/T0005.BIN').read_bytes()

    def test_real_request_performs_preflight_and_restarts_at_script_entry(self):
        case = self.cases['terminal_sub2']
        self.assertEqual([c['opcode'] for c in case['preflight_commands']], [167, 8, 166, 11, 19])
        initial = case['initial_state']
        self.assertEqual(initial['script_phase'], 0)
        self.assertEqual(initial['vm_pc'], 0)
        self.assertEqual(initial['vm_active'], 1)
        self.assertEqual(initial['register'], 1)
        self.assertEqual(initial['exit_flag'], 1)
        self.assertEqual(initial['finish_flags'], [0, 0, 0])
        self.assertEqual([c['opcode'] for c in case['commands'][:3]], [167, 8, 136])

    def test_script_end_precedes_completion_flags_and_exit(self):
        case = self.cases['terminal_sub2']
        self.assertTrue(case['transition_returned'])
        end = case['commands'][-1]
        self.assertEqual((end['offset'], end['opcode']), (0x774, 19))
        at_end = case['states'][end['frame']]
        self.assertEqual(at_end['vm_active'], 0)
        self.assertEqual(at_end['script_phase'], 4)
        self.assertEqual(at_end['finish_flags'], [0, 0, 0])
        completed_frame = next(i for i, state in enumerate(case['states']) if state['script_phase'] == 6)
        self.assertGreater(completed_frame, end['frame'])
        self.assertEqual(case['states'][-1]['transition_phase'], 20)
        self.assertNotIn('vm_update', case['stub_calls'])
        self.assertIn('0x4ce8f0', case['visited_original_addresses'])

    def test_every_executed_script_instruction_matches_sourced_bytes(self):
        for case in self.evidence['cases']:
            for command in case['preflight_commands'] + case['commands']:
                self.assertEqual(struct.unpack_from('<HH', self.source, command['offset']),
                                 (command['opcode'], command['advance']))
        self.assertEqual(hashlib.sha256(self.source).hexdigest(), self.evidence['script_sha256'])

    def test_selector_fourteen_uses_sub_eight_but_distinct_result(self):
        case = self.cases['terminal_selector14_sub8']
        self.assertEqual((case['selector_argument'], case['script_sub']), (14, 8))
        image = (ROOT / 'analysis/hermit_game.exe').read_bytes()
        selector = struct.unpack_from('<I', image, 0x60CA7C-0x400000+14*4)[0]
        self.assertEqual(case['initial_state']['result_selector'], selector)
        self.assertEqual(selector, 5)
        self.assertTrue(case['transition_returned'])
        self.assertEqual(case['commands'][-1]['offset'], 0xFCE)

    def test_work_key_and_presentation_waits_do_not_auto_complete(self):
        expectations = [('sub2_work_completion_missing', 136, 4),
                        ('sub2_key_missing', 51, 1), ('sub2_ui_missing', 56, 1)]
        for name, opcode, state in expectations:
            case = self.cases[name]
            self.assertFalse(case['transition_returned'])
            self.assertEqual(case['commands'][-1]['opcode'], opcode)
            self.assertEqual(case['states'][-1]['vm_wait_state'], state)
            self.assertEqual(case['states'][-1]['finish_flags'], [0, 0, 0])

    def test_dispatch_uses_script_opcode_minus_five_switch_index(self):
        expected = {112: '0x42dcf0', 117: '0x42d960', 118: '0x42d9f0',
                    130: '0x42e340', 147: '0x4d0ed0', 148: '0x4d0fb0'}
        probes = {p['opcode']: p for p in self.evidence['dispatch_probes']}
        for opcode, handler in expected.items():
            self.assertEqual([p['handler_va'] for p in probes[opcode]['handler_entries']], [handler])
        self.assertEqual(probes[112]['world_requests'], [[60, 16, 40]])
        self.assertEqual(probes[112]['vm_work_wait'], 0)
        self.assertEqual(probes[112]['vm_wait_state'], 0)
        self.assertEqual(probes[130]['world_requests'], [[2, 3, 58, 3]])
        self.assertEqual(probes[148]['vm_temporaries'], [0, 16, 40, 0])
        for opcode in (147, 148):
            self.assertEqual(probes[opcode]['evidence_kind'], 'synthetic_instruction')

    def test_fixture_and_report_are_regenerated_from_original_control_code(self):
        saved = (ROOT / 'analysis/scene5-script-execution-v3-20261002.json').read_bytes()
        self.assertEqual(saved.decode('utf-8'), report_text(self.evidence))
        fixture = json.loads((ROOT / 'prototype/data/scene5_script_execution_evidence.json').read_text('utf-8'))
        self.assertEqual(fixture, godot_fixture(self.evidence))
        self.assertEqual(hashlib.sha256(saved).hexdigest(), fixture['source_report_sha256'])
        self.assertFalse(fixture['state11_observed'])
        self.assertFalse(fixture['authorizes_persistent_write'])
        for case in self.evidence['cases']:
            self.assertFalse(case['state11_observed'])
            self.assertFalse(case['authorizes_persistent_write'])
        for callback in fixture['external_callbacks']:
            self.assertEqual(callback['evidence_kind'], 'synthetic_work_completion_callback')

    def test_native_board_display_return_is_mode_dependent(self):
        # Original BORDDISP mode 3 writes incoming return argument to 1 at 4C5CC5.
        case = self.cases['terminal_sub2']
        board = next(command for command in case['commands'] if command['opcode'] == 24)
        self.assertEqual(case['states'][board['frame']]['vm_wait_state'], 1)
        self.assertEqual(case['states'][board['frame']+1]['vm_wait_state'], 0)

    def test_reject_wrong_selector_sub_and_unbounded_instruction(self):
        emulator = Scene5Emulator()
        with self.assertRaises(ValueError):
            emulator.request(2, 8)
        emulator.request()
        emulator.write(VM+0x10, SCRIPT+len(self.source))
        with self.assertRaises(RuntimeError):
            emulator.call(0x4CE8F0, receiver=VM)


if __name__ == '__main__':
    unittest.main()
