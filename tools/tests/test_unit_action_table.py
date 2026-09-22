# -*- coding: utf-8 -*-
import unittest

from tools.unit_action_table import (EXE, archive_for_type, check_archive_programs,
                                     decode_action, type_for_archive)


class UnitActionTableTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.image = EXE.read_bytes()

    def test_standard_move_and_attack_golden_directions(self):
        move = decode_action(self.image, 0, 3)['directions']
        attack = decode_action(self.image, 0, 5)['directions']
        self.assertEqual((move['N']['block'], move['N']['animation']), (0, 11))
        self.assertEqual((move['E']['animation'], move['E']['flags']), (13, 1))
        self.assertEqual((attack['N']['block'], attack['N']['animation']), (0, 21))
        self.assertEqual((attack['SE']['animation'], attack['SE']['flags']), (24, 1))

    def test_action_31_is_block_1_for_standard_type(self):
        result = decode_action(self.image, 0, 31)
        directions = result['directions']
        self.assertEqual(result['action_table_va'], 0x60D160)
        self.assertEqual(result['program_table_va'], 0x60DCF0)
        self.assertEqual({v['block'] for v in directions.values()}, {1})
        self.assertEqual(
            {d: (v['animation'], v['flags']) for d, v in directions.items()},
            {'N': (6, 0), 'NE': (7, 1), 'E': (8, 1), 'SE': (9, 1),
             'S': (10, 0), 'SW': (9, 0), 'W': (8, 0), 'NW': (7, 0)},
        )

    def test_special_type_17_uses_different_program_lookup(self):
        result = decode_action(self.image, 17, 31)
        self.assertEqual(result['archive'], 'D0A')
        self.assertEqual(result['action_table_va'], 0x60D160)
        self.assertEqual(result['program_table_va'], 0x60DFC8)
        self.assertEqual((result['directions']['N']['block'],
                          result['directions']['N']['animation']), (0, 101))

    def test_ten_archive_paths_share_the_runtime_type_index(self):
        expected = ['B0A', 'B1A', 'A0A', 'A1A', 'C0A', 'C1A',
                    'E0A', 'E1A', 'D0A', 'D1A']
        self.assertEqual([archive_for_type(self.image, i) for i in range(9, 19)],
                         expected)
        for index, archive in enumerate(expected, start=9):
            self.assertEqual(type_for_archive(self.image, archive), index)

    def test_c0a_action_31_uses_block_one(self):
        result = decode_action(self.image, type_for_archive(self.image, 'C0A'), 31)
        self.assertEqual(result['archive'], 'C0A')
        self.assertEqual((result['directions']['N']['block'],
                          result['directions']['N']['animation']), (1, 6))

    def test_action_31_program_availability_depends_on_archive(self):
        available = set()
        for type_index in range(9, 19):
            action = check_archive_programs(decode_action(self.image, type_index, 31))
            archive = action['archive']
            if action['all_programs_present']:
                available.add(archive)
        self.assertIn('C0A', available)
        self.assertIn('D0A', available)
        self.assertNotIn('E0A', available)

    def test_missing_type_table_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'no action/program table'):
            decode_action(self.image, 1, 31)


if __name__ == '__main__':
    unittest.main()
