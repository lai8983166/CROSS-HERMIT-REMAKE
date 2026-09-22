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

    def test_skill_actions_use_generic_direction_mapping_and_omit_blank_slots(self):
        expected_action12 = {
            'N': (56, 0), 'NE': (57, 1), 'E': (58, 1), 'SE': (59, 1),
            'S': (60, 0), 'SW': (59, 0), 'W': (58, 0), 'NW': (57, 0),
        }
        for unit_id, unit in self.data['units'].items():
            self.assertEqual(set(unit['anim_map']['skill_actions']),
                             {'11', '12', '13', '14', '15', '16', '31'}, unit_id)
        d0_action12 = self.data['units']['D0A']['anim_map']['skill_actions']['12']
        self.assertEqual(
            {direction: (entry['anim'], entry['flags'])
             for direction, entry in d0_action12.items()},
            expected_action12,
        )
        self.assertNotIn('N', self.data['units']['A0A']['anim_map']['skill_actions']['13'])

    def test_action31_uses_original_block_and_all_exported_frames_exist(self):
        expected = {
            'C1A': (1, 6), 'D0A': (0, 101),
        }
        for unit_id, (block, animation) in expected.items():
            unit = self.data['units'][unit_id]
            mapping = unit['anim_map']['skill_actions']['31']
            self.assertEqual(len(mapping), 8)
            self.assertEqual((mapping['N']['block'], mapping['N']['anim']),
                             (block, animation))
            for entry in mapping.values():
                timeline = (unit['anims'][entry['anim']] if entry['block'] == 0
                            else unit['anim_blocks'][str(entry['block'])][str(entry['anim'])])
                self.assertTrue(any(step['layers'] for step in timeline['steps']))
                for step in timeline['steps']:
                    for layer in step['layers']:
                        self.assertGreaterEqual(layer['frame'], 0)
                        self.assertLess(layer['frame'], unit['frame_count'])
        for unit_id in ('E0A', 'E1A'):
            self.assertFalse(self.data['units'][unit_id]['anim_map']['skill_actions']['31'])

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

    def test_global_ids_map_to_efct_program_blocks(self):
        self.assertEqual(self.data['_meta']['schema_version'], 3)
        self.assertEqual(self.data['_meta']['source'], 'CROSS HERMIT/CROSS HERMIT/DATA/DXANIM/EFCT.BIN')
        self.assertEqual(
            (self.data['animations']['2042']['block'], self.data['animations']['2042']['animation']),
            (1, 42),
        )
        self.assertEqual(
            (self.data['animations']['3027']['block'], self.data['animations']['3027']['animation']),
            (2, 27),
        )

    def test_skill_29_visual_chain_is_exported(self):
        for global_id in ('2050', '2098', '3017', '3032'):
            self.assertIn(global_id, self.data['animations'])
        cast = self.data['animations']['2050']
        self.assertIsNotNone(cast['loop_from'])
        self.assertEqual(self.data['animations']['3017']['duration_ticks'], 120)
        self.assertEqual(self.data['animations']['3017']['steps'], [
            {'duration_ticks': 120, 'layers': []},
        ])

    def test_skill_22_visual_chain_and_lifecycle_are_exported(self):
        expected = {
            2044: (1, 44, 97, 13, 25, 2),
            3027: (2, 27, 36, None, 10, 2),
            2029: (1, 29, 19, None, 7, 1),
        }
        for global_id, (block, animation, duration, loop_from, steps, max_layers) in expected.items():
            timeline = self.data['animations'][str(global_id)]
            self.assertEqual((timeline['block'], timeline['animation']), (block, animation))
            self.assertEqual(timeline['duration_ticks'], duration)
            self.assertEqual(timeline['loop_from'], loop_from)
            self.assertEqual(len(timeline['steps']), steps)
            self.assertEqual(max(len(step['layers']) for step in timeline['steps']), max_layers)
            self.assertTrue(any(step['layers'] for step in timeline['steps']))
        self.assertEqual(self.data['_meta']['exported_frame_count'], len(self.data['frames']))
        self.assertEqual(self.data['_meta']['exported_frame_count'], 86)

    def test_every_timeline_frame_is_exported_and_in_archive_range(self):
        frame_count = self.data['_meta']['frame_count']
        frames = self.data['frames']
        for global_id, animation in self.data['animations'].items():
            for step in animation['steps']:
                self.assertGreater(step['duration_ticks'], 0, global_id)
                for layer in step['layers']:
                    frame = layer['frame']
                    self.assertGreaterEqual(frame, 0, global_id)
                    self.assertLess(frame, frame_count, global_id)
                    self.assertIn(str(frame), frames, global_id)


class SkillVisualExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / 'prototype/data/skill_visuals.json').read_text('utf-8'))
        cls.rows = {row['id']: row for row in cls.data['rows']}

    def test_table_shape_and_visual_gameplay_separation(self):
        self.assertEqual(self.data['_meta']['source_va'], 0x611538)
        self.assertEqual(self.data['_meta']['stride'], 0x10)
        self.assertEqual(self.data['_meta']['count'], 612)
        self.assertEqual(len(self.rows), 612)

    def test_skill_22_golden_values(self):
        self.assertEqual(
            self.rows[22],
            {
                'id': 22, 'cast_action': 13, 'release_action': 31,
                'recover_action': 16, 'flags': 0, 'cast_fx': 2044,
                'release_fx': 3027, 'detail_id': 22, 'sync_fx': 0,
                'impact_fx': 2029, 'shape': 0, 'gameplay_effect_id': 6,
            },
        )

    def test_skill_29_golden_values(self):
        self.assertEqual(
            self.rows[29],
            {
                'id': 29, 'cast_action': 12, 'release_action': 7,
                'recover_action': 15, 'flags': 0, 'cast_fx': 2050,
                'release_fx': 2098, 'detail_id': 29, 'sync_fx': 3017,
                'impact_fx': 3032, 'shape': 0, 'gameplay_effect_id': 0,
            },
        )

    def test_basic_attacks_have_actions_but_no_external_visuals(self):
        for skill_id in (101, 103):
            row = self.rows[skill_id]
            self.assertEqual(
                (row['cast_action'], row['release_action'], row['recover_action']),
                (11, 5, 14),
            )
            self.assertEqual(
                (row['cast_fx'], row['release_fx'], row['sync_fx'], row['impact_fx']),
                (0, 0, 0, 0),
            )
            self.assertEqual(row['detail_id'], skill_id)
            self.assertEqual(row['gameplay_effect_id'], 0)


if __name__ == '__main__':
    unittest.main()
