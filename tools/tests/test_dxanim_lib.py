# -*- coding: utf-8 -*-
import struct
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))

import dxanim_lib as dx  # noqa: E402


DXANIM_DIR = ROOT / 'CROSS HERMIT' / 'CROSS HERMIT' / 'DATA' / 'DXANIM'


def visible(descriptor, duration, flags=0):
    ids = [descriptor, 0xfff, 0xfff, 0xfff]
    high = sum(((value >> 8) & 0x0f) << (slot * 4) for slot, value in enumerate(ids))
    return struct.pack('<BB4BHh', flags, 0, *(value & 0xff for value in ids), high, duration)


def child(animation, x, y, flags=1):
    return struct.pack('<BBhhhh', flags, 0, animation, x, y, 0)


def loop(repeat, jump, flags=3):
    return struct.pack('<BBhhhh', flags, repeat, jump, 0, 0, 0)


def program_block(programs):
    header_size = 8 + 4 * len(programs)
    offsets = []
    payload = bytearray()
    for program in programs:
        offsets.append(header_size + len(payload))
        payload.extend(b''.join(program))
    physical_size = header_size + len(payload)
    return struct.pack(f'<II{len(offsets)}I', max(0, physical_size - 8), len(programs), *offsets) + payload


def descriptor(frame, x=0, y=0, flags=0, palette=0xff, draw_group=7):
    return struct.pack('<hhhBBh', x, y, frame, flags, palette, draw_group)


def dxanim_file(blocks):
    blocks = list(blocks) + [b''] * (9 - len(blocks))
    header_size = 8 + 4 * len(blocks)
    offsets = []
    payload = bytearray()
    for block_data in blocks:
        offsets.append(header_size + len(payload))
        payload.extend(block_data)
    total = header_size + len(payload)
    return struct.pack(f'<II{len(blocks)}I', total, len(blocks), *offsets) + payload


class DxAnimGoldenTests(unittest.TestCase):
    EXPECTED = {
        'A0A': {
            11: (list(range(569, 575)), list(range(244, 250)), 8),
            12: (list(range(563, 569)), list(range(238, 244)), 8),
            13: (list(range(557, 563)), list(range(232, 238)), 8),
            14: (list(range(551, 557)), list(range(226, 232)), 8),
            15: (list(range(545, 551)), list(range(220, 226)), 8),
        },
        'B1A': {
            11: (list(range(463, 469)), list(range(224, 230)), 10),
            12: (list(range(457, 463)), list(range(218, 224)), 10),
            13: (list(range(451, 457)), list(range(212, 218)), 10),
            14: (list(range(445, 451)), list(range(206, 212)), 10),
            15: (list(range(439, 445)), list(range(200, 206)), 10),
        },
    }

    def test_a0a_b1a_move_descriptor_chains(self):
        for archive, animations in self.EXPECTED.items():
            data = (DXANIM_DIR / f'{archive}.BIN').read_bytes()
            offs = dx.parse_dxanim(data)
            programs = dx.parse_program_blocks(data, offs)
            descriptors = dx.parse_block4_descriptors(data, offs)
            for animation, (descriptor_ids, frames, duration) in animations.items():
                visible_ops = [op for op in programs[0][animation] if op['opcode'] == 0]
                self.assertEqual([op['descriptors'][0] for op in visible_ops], descriptor_ids)
                self.assertEqual([op['duration_ticks'] for op in visible_ops], [duration] * 6)
                self.assertEqual([descriptors[index]['frame'] for index in descriptor_ids], frames)
                self.assertEqual([descriptors[index]['draw_group'] for index in descriptor_ids], [7] * 6)

    def test_engine_move_table_is_direct_block0_with_mirror_flags(self):
        animations = [{'records': [{'frame': 0, 'dur': 1}]} for _ in range(16)]
        walk, idle = dx.engine_dir_map(animations, [], 1)
        self.assertEqual(idle, {})
        self.assertEqual(set(walk), {'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'})
        self.assertEqual(
            {direction: (entry['anim'], entry['flags']) for direction, entry in walk.items()},
            {
                'W': (13, 0), 'E': (13, 1), 'NW': (12, 0), 'NE': (12, 1),
                'S': (15, 0), 'N': (11, 0), 'SW': (14, 0), 'SE': (14, 1),
            },
        )
        self.assertTrue(all(entry['block'] == 0 and entry['action'] == 3 for entry in walk.values()))

    def test_engine_attack_table_is_action5_with_mirror_flags(self):
        animations = [{'records': [{'frame': 0, 'dur': 1}]} for _ in range(26)]
        attack = dx.engine_attack_dir_map(animations, 1)
        self.assertEqual(
            {direction: (entry['anim'], entry['flags']) for direction, entry in attack.items()},
            {
                'W': (23, 0), 'E': (23, 1), 'NW': (22, 0), 'NE': (22, 1),
                'S': (25, 0), 'N': (21, 0), 'SW': (24, 0), 'SE': (24, 1),
            },
        )
        self.assertTrue(all(entry['block'] == 0 and entry['action'] == 5 for entry in attack.values()))

    def test_skill_actions_11_through_16_use_five_program_direction_groups(self):
        animations = [{'records': [{'frame': 0, 'dur': 1}]} for _ in range(81)]
        expected_offsets = {
            'N': (0, 0), 'NE': (1, 1), 'E': (2, 1), 'SE': (3, 1),
            'S': (4, 0), 'SW': (3, 0), 'W': (2, 0), 'NW': (1, 0),
        }
        for action in range(11, 17):
            mapping = dx.engine_action_dir_map(animations, action)
            base = action * 5 - 4
            self.assertEqual(
                {direction: (entry['anim'] - base, entry['flags'])
                 for direction, entry in mapping.items()},
                expected_offsets,
            )
            self.assertTrue(all(entry['action'] == action for entry in mapping.values()))


class DxAnimInterpreterTests(unittest.TestCase):
    def test_child_animation_runs_concurrently_with_parent(self):
        parent = [visible(0, 2), child(0, 5, 6), visible(1, 2, 0x80)]
        spawned = [visible(2, 3, 0x80)]
        data = dxanim_file([
            program_block([parent]), b'', b'', program_block([spawned]),
            descriptor(10) + descriptor(11) + descriptor(12),
        ])
        timeline = dx.interpret_animation(data, 0, 0)
        self.assertEqual(timeline['loop_from'], None)
        self.assertEqual(timeline['duration_ticks'], 5)
        self.assertEqual([layer['frame'] for layer in timeline['steps'][1]['layers']], [11, 12])
        child_layer = timeline['steps'][1]['layers'][1]
        self.assertEqual((child_layer['x'], child_layer['y']), (5, 6))

    def test_zero_distance_loop_fails_instead_of_hanging(self):
        data = dxanim_file([program_block([[loop(0x7f, 0)]])])
        with self.assertRaisesRegex(dx.DxAnimError, 'zero-distance loop'):
            dx.interpret_animation(data, 0, 0, max_steps=20)

    def test_loop_that_respawns_transient_child_converges(self):
        parent = [child(0, 0, 0), visible(0, 1), loop(0x7f, 2)]
        spawned = [visible(1, 1, 0x80)]
        data = dxanim_file([
            program_block([parent]), b'', b'', program_block([spawned]),
            descriptor(10) + descriptor(11),
        ])
        timeline = dx.interpret_animation(data, 0, 0, max_ticks=20)
        self.assertEqual(timeline['loop_from'], 0)
        self.assertEqual(timeline['duration_ticks'], 1)
        self.assertEqual([layer['frame'] for layer in timeline['steps'][0]['layers']], [10, 11])

    def test_efct_sustained_cast_animations_converge(self):
        data = (DXANIM_DIR / 'EFCT.BIN').read_bytes()
        offs = dx.parse_dxanim(data)
        for global_id in range(2044, 2052):
            timeline = dx.interpret_animation(
                data,
                global_id // 1000 - 1,
                global_id % 1000,
                offs=offs,
            )
            self.assertIsNotNone(timeline['loop_from'], global_id)
            self.assertGreater(timeline['duration_ticks'], 0, global_id)

    def test_truncated_instruction_is_rejected(self):
        malformed = program_block([[visible(0, 1) + b'\x01']])
        data = dxanim_file([malformed])
        with self.assertRaisesRegex(dx.DxAnimError, 'truncated 10-byte instruction'):
            dx.parse_program_blocks(data)


if __name__ == '__main__':
    unittest.main()
