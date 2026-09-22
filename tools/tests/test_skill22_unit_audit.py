# -*- coding: utf-8 -*-
import unittest

from tools.skill22_unit_audit import scan_all


class Skill22UnitAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.units = {unit['archive']: unit for unit in scan_all()}

    def test_ten_original_archives_are_scanned(self):
        self.assertEqual(set(self.units),
                         {'A0A', 'A1A', 'B0A', 'B1A', 'C0A', 'C1A',
                          'D0A', 'D1A', 'E0A', 'E1A'})
        self.assertFalse(self.units['E0A']['actions']['31']['all_directions_decoded'])
        self.assertFalse(self.units['E1A']['actions']['31']['all_directions_decoded'])

    def test_c1a_three_actions_have_original_eight_direction_mapping(self):
        unit = self.units['C1A']
        expected = {
            13: (0, (61, 62, 63, 64, 65, 64, 63, 62)),
            31: (1, (6, 7, 8, 9, 10, 9, 8, 7)),
            16: (0, (76, 77, 78, 79, 80, 79, 78, 77)),
        }
        directions = ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW')
        flags = (0, 1, 1, 1, 0, 0, 0, 0)
        for action_id, (block, animations) in expected.items():
            action = unit['actions'][str(action_id)]
            self.assertTrue(action['all_programs_present'], action_id)
            self.assertTrue(action['all_directions_decoded'], action_id)
            self.assertEqual(
                [(action['directions'][name]['block'],
                  action['directions'][name]['animation'],
                  action['directions'][name]['flags']) for name in directions],
                [(block, animation, flag) for animation, flag in zip(animations, flags)],
            )

    def test_c1a_is_visible_multiframe_and_bright_enough(self):
        unit = self.units['C1A']
        north = {action: unit['actions'][str(action)]['directions']['N']
                 for action in (13, 31, 16)}
        self.assertEqual([north[action]['distinct_visual_states']
                          for action in (13, 31, 16)], [1, 11, 6])
        self.assertGreaterEqual(north[31]['visible_steps'], 10)
        self.assertTrue(all(north[action]['mean_frame_luma'] >= 50
                            for action in (13, 31, 16)))
        self.assertEqual(self.units['C0A']['actions']['16']['directions']['N']
                         ['distinct_visual_states'], 1)


if __name__ == '__main__':
    unittest.main()
