"""Pin the conservative recipient selector to original AllResult EXE bytes."""
import json
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
IMAGE_BASE = 0x400000


class AllResultRecipientEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads((ROOT / 'prototype/data/all_result_recipient_evidence.json')
                                 .read_text('utf-8'))
        cls.exe = (ROOT / cls.fixture['source_exe']).read_bytes()

    @classmethod
    def at(cls, va, size):
        return cls.exe[va - IMAGE_BASE:va - IMAGE_BASE + size]

    def assert_call(self, va, target):
        instruction = self.at(va, 5)
        self.assertEqual(instruction[0], 0xe8)
        displacement, = struct.unpack_from('<i', instruction, 1)
        self.assertEqual(va + 5 + displacement, target)

    def test_only_mode_zero_calls_selector_and_resets_sentinel(self):
        f = self.fixture
        self.assertEqual(f['schema_version'], 1)
        self.assertEqual(f['evidence_kind'],
                         'original_selection_rule_not_runtime_result')
        self.assertEqual(f['reset_va'], 0x4bd8ed)
        self.assertEqual(self.at(f['reset_va'], 9),
                         bytes.fromhex('66c70580117e00ffff'))
        self.assertEqual(self.at(0x4bd8ff, 10),
                         bytes.fromhex('c70584117e0000000000'))
        self.assert_call(f['mode_zero_call_va'], f['selector_va'])
        self.assertEqual(self.at(0x4bd9c1, 15),
                         bytes.fromhex('33d28a1591447f0085d2750a8b4dfc'))

    def test_group_slot_maps_through_participant_id_to_rank(self):
        f = self.fixture
        self.assertEqual((f['group_count'], f['slots_per_group']), (5, 4))
        self.assertEqual(self.at(0x4c00f5, 3), bytes.fromhex('83f905'))
        self.assertEqual(self.at(0x4c0157, 3), bytes.fromhex('83f904'))
        self.assertEqual(f['group_slot_table_va'], 0x7aaae0)
        self.assertEqual(self.at(0x4c016a, 8), bytes.fromhex('668b8cd0e0aa7a00'))
        self.assertEqual(self.at(0x4c017a, 3), bytes.fromhex('83faff'))
        self.assertEqual(f['participant_id_table_va'], 0x7a5210)
        self.assertEqual(self.at(0x4c0187, 8), bytes.fromhex('668b0c4510527a00'))
        self.assertEqual(f['record_base_va'], 0x7cf34c)
        self.assertEqual(f['record_stride'], 0x124)
        self.assertEqual(f['rank_field_offset'], 0x20)
        self.assertEqual(self.at(0x4c022d, 6), bytes.fromhex('69c024010000'))
        self.assertEqual(self.at(0x4c0239, 6), bytes.fromhex('3b886cf37c00'))

    def test_strict_positive_max_and_id_cap_before_later_write(self):
        f = self.fixture
        self.assertEqual(f['initial_best_rank'], 0)
        self.assertEqual(f['initial_recipient_id'], 0xffff)
        self.assertEqual(f['tie_rule'], 'first_strictly_greater')
        self.assertEqual(self.at(0x4c023f, 2), bytes.fromhex('7d42'))
        self.assertEqual(f['recipient_id_max_exclusive'], 13)
        self.assertEqual(self.at(0x4c0245, 3), bytes.fromhex('83fa0d'))
        self.assertEqual(f['recipient_output_va'], 0x7e1180)
        self.assertEqual(self.at(0x4c0264, 7),
                         bytes.fromhex('66891580117e00'))
        self.assertEqual(f['branch_write_field_offset'], 0x120)
        self.assertEqual(self.at(0x4c1b71, 7),
                         bytes.fromhex('0fbf0580117e00'))
        self.assertEqual(self.at(0x4c1ba8, 7),
                         bytes.fromhex('6689826cf47c00'))
        self.assertEqual(f['scene5_reached_state12'], 'unresolved')
        self.assertEqual(f['role_mapping_for_current_battle_setup'], 'unresolved')
        self.assertFalse(f['authorizes_persistent_write'])


if __name__ == '__main__':
    unittest.main()
