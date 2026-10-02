"""Original work-update and dispatch instructions, with explicit synthetic world."""
import hashlib
import importlib.util
import json
import struct
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.scene5_task_emulation import report, godot_fixture, TaskEmulator, RESULT_TASK
    from tools.tactics_exit_emulation import ROOT, report_text
    from tools.scene5_script_emulation import VM


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt in .venv-audit')
class Scene5TaskEmulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()
        cls.cases = {case['name']: case for case in cls.report['cases']}
        cls.image = (ROOT / 'analysis/hermit_game.exe').read_bytes()

    def test_global_clear_is_the_actual_vm_wait_byte(self):
        # Absolute byte write is why a text search for VM+92E0 missed this path.
        self.assertEqual(VM+0x92E0, 0x7E0F08)
        offset = 0x4977B8-0x400000
        self.assertEqual(self.image[offset:offset+7], bytes.fromhex('c605080f7e0000'))
        clears = self.cases['terminal_sub2']['work_completions']
        self.assertEqual([event['caller_return_va'] for event in clears],
                         ['0x49973f', '0x4981f9', '0x497c16', '0x497c16'])
        self.assertTrue(all(event['previous'] == 1 for event in clears))
        self.assertTrue(all(event['target'] == '0x7e0f08' for event in clears))

    def test_original_fade_ticks_clear_wait_at_sixty_frames(self):
        case = self.cases['terminal_sub2']
        start = next(command['frame'] for command in case['commands'] if command['opcode'] == 117)
        cleared = next(event['frame'] for event in case['work_completions']
                       if event['caller_return_va'] == '0x497c16')
        at_start = case['frames'][start]
        self.assertEqual(at_start['work_fade_remaining'], 59)
        self.assertEqual(at_start['work_fade_delta'], 648)
        self.assertEqual(at_start['vm_work_wait'], 1)
        self.assertEqual(cleared-start, 59)
        self.assertEqual(case['frames'][cleared]['work_fade_remaining'], 0)
        self.assertEqual(case['frames'][cleared]['vm_work_wait'], 0)
        self.assertEqual(case['frames'][cleared]['work_fade_status'], 2)
        self.assertEqual(case['frames'][cleared+1]['vm_wait_state'], 0)

    def test_same_task_runs_end_exit_request_and_dispatch_in_order(self):
        for name in ('terminal_sub2', 'terminal_selector14_sub8'):
            case = self.cases[name]
            end = case['commands'][-1]
            self.assertEqual(end['opcode'], 19)
            self.assertEqual(case['frames'][end['frame']]['finish_flags'], [0, 0, 0])
            self.assertEqual(case['frames'][-1]['transition_function_return'], 1)
            self.assertEqual(case['frames'][-1]['transition_phase'], 20)
            self.assertEqual(case['frames'][-1]['request_pending'], 0)
            events = case['dispatch_events']
            self.assertEqual([event['kind'] for event in events],
                             ['state_request', 'result_constructor_enter', 'scheduler_register_result'])
            self.assertEqual(events[0]['caller_return_va'], '0x451968')
            self.assertEqual(events[0]['state'], 11)
            self.assertGreater(events[0]['frame'], end['frame'])
            self.assertEqual(events[1]['caller_return_va'], '0x49e3ad')
            self.assertEqual(case['final_state']['requested_state'], 11)
            self.assertEqual(case['final_state']['request_pending'], 0)
            self.assertTrue(case['state11_dispatched_in_emulation'])

    def test_real_constructor_installs_result_vtable_before_scheduler_boundary(self):
        for name in ('terminal_sub2', 'terminal_selector14_sub8'):
            case = self.cases[name]
            self.assertEqual(case['result_task'],
                             {'pointer': hex(RESULT_TASK), 'vtable': '0x5a0dfc', 'active': 1})
            event = case['dispatch_events'][-1]
            self.assertEqual(event['args'], [RESULT_TASK, 0, 2])
            self.assertEqual((event['vtable'], event['active']), ('0x5a0dfc', 1))
            visited = case['visited_original_addresses']
            for va in ('0x451670', '0x451a60', '0x4539b0', '0x439e30', '0x49e2b0',
                       '0x4bd6f0', '0x4bd540'):
                self.assertIn(va, visited)
            self.assertNotIn('0x4bd660', visited)  # Result body not executed by simulated scheduler.

    def test_missing_external_conditions_never_dispatch_result(self):
        states = {'key_missing': (1, 5), 'fade_tick_frozen': (4, 5),
                  'ui_missing': (1, 5), 'result_animation_missing': (0, 17)}
        for name, (wait, phase) in states.items():
            case = self.cases[name]
            self.assertTrue(case['bounded_stop'])
            self.assertEqual(case['dispatch_events'], [])
            self.assertFalse(case['state11_dispatched_in_emulation'])
            self.assertEqual(case['final_state']['vm_wait_state'], wait)
            self.assertEqual(case['final_state']['transition_phase'], phase)
            self.assertEqual(case['final_state']['request_pending'], 0)
            self.assertEqual(case['result_task']['pointer'], '0x0')

    def test_historical_synthetic_completion_is_absent_and_limits_remain_explicit(self):
        for case in self.report['cases']:
            self.assertNotIn('0x4cdf80', case['visited_original_addresses'])
            self.assertNotIn('vm_update', case['stub_calls'])
            self.assertNotIn('start_script_work_fade', case['stub_calls'])
            self.assertFalse(case['live_state11_observed'])
            self.assertFalse(case['authorizes_persistent_write'])
        self.assertEqual(self.cases['fade_tick_frozen']['counterfactual_overrides'], ['0x497aa0'])
        native_starts = {row[0] for row in self.report['native_function_ranges']}
        stub_addresses = {row['va'] for row in self.report['effective_stub_manifest']}
        for va in ('0x4977a0', '0x4978c0', '0x497aa0', '0x4bd6f0', '0x49e2b0'):
            self.assertIn(va, native_starts)
            self.assertNotIn(va, stub_addresses)
        self.assertIn('0x4216c0', stub_addresses)

    def test_canonical_report_and_godot_fixture_match_new_native_execution(self):
        path = ROOT / 'analysis/scene5-task-execution-v3-20261002.json'
        raw = path.read_bytes()
        self.assertEqual(raw.decode('utf-8'), report_text(self.report))
        fixture = json.loads((ROOT / 'prototype/data/scene5_task_execution_evidence.json').read_text('utf-8'))
        self.assertEqual(fixture, godot_fixture(self.report))
        self.assertEqual(fixture['source_report_sha256'], hashlib.sha256(raw).hexdigest())

    def test_original_dispatch_jump_table_and_call_operands(self):
        target = struct.unpack_from('<I', self.image, 0x49E4D3-0x400000+11*4)[0]
        self.assertEqual(target, 0x49E3A8)
        for call, destination in ((0x497C11, 0x4977A0), (0x49973A, 0x4977A0),
                                  (0x4981F4, 0x4977A0), (0x451963, 0x439E30),
                                  (0x49E3A8, 0x4BD6F0)):
            at = call-0x400000
            self.assertEqual(self.image[at], 0xE8)
            relative = struct.unpack_from('<i', self.image, at+1)[0]
            self.assertEqual(call+5+relative, destination)

    def test_menu_exit_overrides_scene_five_result_request(self):
        case = self.cases['menu_exit']
        self.assertFalse(case['bounded_stop'])
        self.assertEqual(case['frames'][-1]['transition_function_return'], 1)
        self.assertEqual(case['final_state']['exit_to_menu'], 1)
        self.assertEqual(case['final_state']['requested_state'], 1)
        self.assertEqual([event['kind'] for event in case['dispatch_events']], ['state_request'])
        self.assertEqual(case['dispatch_events'][0]['caller_return_va'], '0x4517db')
        self.assertFalse(case['state11_dispatched_in_emulation'])
        self.assertEqual(case['result_task']['pointer'], '0x0')
        self.assertIn('menu_task_boundary', case['stub_calls'])


if __name__ == '__main__':
    unittest.main()
