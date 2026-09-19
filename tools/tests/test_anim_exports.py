# -*- coding: utf-8 -*-
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class UnitExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / 'prototype/data/unit_sprites.json').read_text('utf-8'))

    def test_v2_schema_and_all_eight_move_directions(self):
        self.assertEqual(self.data['_meta']['schema_version'], 2)
        expected_dirs = {'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'}
        expected_anims = {
            'W': (13, 0), 'E': (13, 1), 'NW': (12, 0), 'NE': (12, 1),
            'S': (15, 0), 'N': (11, 0), 'SW': (14, 0), 'SE': (14, 1),
        }
        self.assertEqual(len(self.data['units']), 10)
        for unit_id, unit in self.data['units'].items():
            mapping = unit['anim_map']['walk_by_dir']
            self.assertEqual(set(mapping), expected_dirs, unit_id)
            self.assertEqual(
                {direction: (entry['anim'], entry['flags']) for direction, entry in mapping.items()},
                expected_anims,
                unit_id,
            )

    def test_all_eight_attack_directions_use_action5(self):
        expected = {
            'N': (21, 0), 'NE': (22, 1), 'E': (23, 1), 'SE': (24, 1),
            'S': (25, 0), 'SW': (24, 0), 'W': (23, 0), 'NW': (22, 0),
        }
        for unit_id, unit in self.data['units'].items():
            mapping = unit['anim_map']['attack_by_dir']
            self.assertEqual(
                {direction: (entry['anim'], entry['flags']) for direction, entry in mapping.items()},
                expected,
                unit_id,
            )
            self.assertTrue(all(entry['action'] == 5 for entry in mapping.values()), unit_id)

    def test_every_exported_layer_references_an_existing_frame(self):
        for unit_id, unit in self.data['units'].items():
            self.assertEqual(len(unit['frames']), unit['frame_count'], unit_id)
            for timeline in unit['anims']:
                self.assertNotIn('records', timeline)
                for step in timeline['steps']:
                    self.assertGreater(step['duration_ticks'], 0, (unit_id, timeline['id']))
                    for layer in step['layers']:
                        self.assertGreaterEqual(layer['frame'], 0, (unit_id, timeline['id']))
                        self.assertLess(layer['frame'], unit['frame_count'], (unit_id, timeline['id']))

    def test_a0a_b1a_move_golden_output(self):
        expected = {
            'A0A': {
                11: list(range(244, 250)), 12: list(range(238, 244)),
                13: list(range(232, 238)), 14: list(range(226, 232)),
                15: list(range(220, 226)),
            },
            'B1A': {
                11: list(range(224, 230)), 12: list(range(218, 224)),
                13: list(range(212, 218)), 14: list(range(206, 212)),
                15: list(range(200, 206)),
            },
        }
        for unit_id, animations in expected.items():
            timelines = self.data['units'][unit_id]['anims']
            for animation, frames in animations.items():
                timeline = timelines[animation]
                self.assertEqual(timeline['loop_from'], 0)
                self.assertEqual(
                    [[layer['frame'] for layer in step['layers']] for step in timeline['steps']],
                    [[frame] for frame in frames],
                )


class FxExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / 'prototype/data/attack_effects.json').read_text('utf-8'))

    def test_slash_and_orb_use_resolved_descriptor_frames(self):
        self.assertEqual(self.data['_meta']['schema_version'], 2)
        self.assertNotIn('default', self.data)
        self.assertNotIn('0', self.data['effect_ids'])
        entry = self.data['files']['01E']
        slash_id = self.data['effects']['slash']['anim']
        orb_id = self.data['effects']['orb']['anim']
        self.assertEqual(slash_id, 21)
        self.assertEqual(orb_id, 28)
        self.assertEqual(
            [[layer['frame'] for layer in step['layers']] for step in entry['anims'][slash_id]['steps']],
            [[36], [37], [38], [39], [40, 4], [40, 5], [41, 5], [41], [42], [43], [12]],
        )
        self.assertEqual(
            [[layer['frame'] for layer in step['layers']] for step in entry['anims'][orb_id]['steps']],
            [[18], [19], [20], [21], [22], [6]],
        )


if __name__ == '__main__':
    unittest.main()
