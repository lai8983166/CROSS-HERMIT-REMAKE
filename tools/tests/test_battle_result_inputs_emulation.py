"""Native result keys and unit data copying, never live/persistent authority."""
import importlib.util
import struct
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.battle_result_inputs_emulation import report, InputEmulator, UNITCTRL
    from tools.tactics_exit_emulation import ROOT, TASK, report_text


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class BattleResultInputsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()
        cls.cases = {c['name']: c for c in cls.report['cases']}

    def test_same_task_finalization_copies_real_terminal_selector(self):
        for name, selector, unit_key in (('terminal_sub2', 1, 2),
                                         ('terminal_selector14_sub8', 5, 1)):
            case = self.cases[name]
            self.assertTrue(case['integrated_task_run'])
            self.assertEqual(case['result_inputs']['result_selector'], selector)
            self.assertEqual(case['task_result_selector'], selector)
            self.assertEqual(case['result_inputs']['unit_condition_key'], unit_key)
            self.assertTrue(case['battle_handoff']['state11_dispatched_in_emulation'])
            entries = case['native_input_events']
            self.assertEqual([e['va'] for e in entries],
                             ['0x473860', '0x4307b0', '0x473940', '0x473ab0'])
            self.assertEqual(entries[0]['receiver'], hex(UNITCTRL))
            self.assertEqual(entries[0]['caller_return_va'], '0x454798')
            self.assertNotIn('unitctrl_finalize', case['stub_calls'])

    def test_native_time_comparison_boundaries(self):
        for name, key in (('time_disabled', 0), ('time_first_boundary', 1),
                          ('time_middle', 2), ('time_second_boundary', 2), ('time_late', 3)):
            case = self.cases[name]
            self.assertFalse(case['integrated_task_run'])
            self.assertIsNone(case['battle_handoff'])
            self.assertEqual(case['result_inputs']['time_key'], key)

    def test_identity_checked_copy_preserves_multiple_unit_fields(self):
        for case in self.report['cases']:
            self.assertEqual(case['result_inputs']['field_4512'], 7)
            for ordinal, (actual, expected) in enumerate(zip(
                    case['result_inputs']['units'], case['synthetic_unit_inputs']['units'])):
                self.assertEqual(actual['ordinal'], ordinal)
                for key in ('character_id', 'count_field_aa', 'contribution_field_ac', 'status_field_ae'):
                    self.assertEqual(actual[key], expected[key])

    def test_identity_mismatch_is_rejected_by_original_assert_path(self):
        emulator = InputEmulator()
        emulator.write(TASK+0x174, 1)
        emulator.write(0x7F451A, 4, 'h')
        with self.assertRaisesRegex(RuntimeError, 'undeclared external code at 0x424f80'):
            emulator.call(0x473860, receiver=UNITCTRL)

    def test_raw_call_operands_match_integrated_input_chain(self):
        image = (ROOT / 'analysis/hermit_game.exe').read_bytes()
        for call, target in ((0x454793, 0x473860), (0x4738F5, 0x4307B0),
                             (0x473915, 0x473940), (0x47391D, 0x473AB0)):
            at = call-0x400000
            self.assertEqual(image[at], 0xE8)
            self.assertEqual(call+5+struct.unpack_from('<i', image, at+1)[0], target)

    def test_report_reexecutes_and_never_authorizes_state_application(self):
        self.assertEqual((ROOT / 'analysis/battle-result-inputs-v1-20261002.json').read_bytes().decode(),
                         report_text(self.report))
        for case in self.report['cases']:
            self.assertFalse(case['live_witness'])
            self.assertFalse(case['authorizes_persistent_write'])
            self.assertNotIn('0x4bbd40', case['visited_original_addresses'])


if __name__ == '__main__':
    unittest.main()
