"""Reject false mandatory-wait and historical-event interpretations offline."""
import copy
import struct
import unittest

from devtools import terminal_new_game_boundary_contract as boundary


class BoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = boundary.source('image')
        cls.menu = boundary.unpack(boundary.source('menu'), 16*1024*1024)
        cls.audio, cls.projection = boundary.audio_projection(cls.menu)

    def test_changed_original_branch_is_rejected(self):
        changed = bytearray(self.raw)
        changed[0x49F518-boundary.BASE] ^= 1
        with self.assertRaisesRegex(ValueError, 'original image identity'):
            boundary.checked_instructions(bytes(changed))

    def test_actual_instruction_tail_has_two_nonwaiting_paths(self):
        for mode, branch in [('recorded_early_inactive', '0x41e820'),
                             ('synthetic_second_guard', '0x41e835')]:
            case = boundary.tail_case(self.raw, self.audio, mode)
            self.assertIn(branch, case['pcs'])
            self.assertIn('0x49f51a', case['pcs'])
            self.assertNotIn('0x49f521', case['pcs'])
            self.assertEqual(case['stop_before'], '0x49f528')
            self.assertEqual(case['synthesized_leaf_returns'], 0)
        self.assertFalse(self.projection['contemporaneous_with_NEW_GAME'])

    def test_active_audio_stops_before_unowned_COM_call(self):
        case = boundary.tail_case(self.raw, self.audio, 'synthetic_active')
        self.assertEqual(case['stop_before'], '0x41daed')
        self.assertNotIn('0x41daed', case['pcs'])
        self.assertFalse(case['ready_return_observed'])
        self.assertEqual(case['OS_or_COM_calls'], 0)

    def test_truncated_audio_capture_is_not_zero_filled(self):
        menu = copy.deepcopy(self.menu)
        menu['lifecycle']['ready']['game']['hex'] = '00'*0x8C88
        with self.assertRaisesRegex(ValueError, 'fixed ready game bytes'):
            boundary.audio_projection(menu)

    def test_NT_state8_cannot_be_labelled_Win32_debug_string8(self):
        # An intentionally invalid NT record with the Win32 number substituted.
        raw = bytearray(96)
        struct.pack_into('<4I', raw, 0, 8, 10, 11, 0x40010006)
        wait = dict(state_hex=raw.hex(), state=8, child_pid=10, child_tid=11)
        case = dict(parent_waits=[wait], child_pid=10)
        with self.assertRaisesRegex(ValueError, 'NT exception record ownership'):
            boundary.historical_debug_strings(dict(cases=[case]*8))


if __name__ == '__main__':
    unittest.main()
