# -*- coding: utf-8 -*-
"""Golden executable/table links for effect 6, before implementing semantics."""
import json
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
IMAGE_BASE = 0x400000


def image_at(image, va, fmt):
    return struct.unpack_from(fmt, image, va - IMAGE_BASE)[0]


class Effect6EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.image = (ROOT / 'analysis/hermit_game.exe').read_bytes()
        table = json.loads((ROOT / 'prototype/data/attack_table.json').read_text('utf-8'))
        cls.attacks = {row['id']: row for row in table['rows']}

    def test_condition6_dispatch_and_tick_callbacks(self):
        condition = self.image[0x6f4088 + 6 * 16 - IMAGE_BASE:
                               0x6f4088 + 7 * 16 - IMAGE_BASE]
        self.assertEqual(condition, bytes.fromhex('06 00 01 02 02 01 00 2e 2f 00 00 00 00 00 00 00'))
        self.assertEqual(image_at(self.image, 0x618fb8 + 6 * 4, '<I'), 0x48f330)
        self.assertEqual(image_at(self.image, 0x6190d0 + 6 * 4, '<I'), 0x4904a0)

    def test_both_attack_rows_use_effect6_but_have_distinct_power(self):
        rows = [row for row in self.attacks.values() if row['hit_effect'] == 6]
        self.assertEqual([row['id'] for row in rows], [22, 537])
        self.assertEqual(
            [(row['power_base'], row['power_scale'], row['target_filter']) for row in rows],
            [(3600, 1000, 2), (0, 0, 1)],
        )
        self.assertEqual(
            self.image[0x6d4e58 + 22 * 7 - IMAGE_BASE:
                       0x6d4e58 + 23 * 7 - IMAGE_BASE],
            bytes.fromhex('01 01 01 03 01 01 02'),
        )
        self.assertEqual(
            self.image[0x738af0 - IMAGE_BASE:0x738af7 - IMAGE_BASE],
            bytes.fromhex('01 01 01 01 01 01 00'),
        )

    def test_effect6_has_no_job_resistance_modifier_and_uses_magic(self):
        condition = self.image[0x6f4088 + 6 * 16 - IMAGE_BASE:
                               0x6f4088 + 7 * 16 - IMAGE_BASE]
        self.assertEqual((condition[3], condition[5], condition[14]), (2, 1, 0))
        # FUN_4DFBA0 indexes the job table at +0x22 with 64-byte rows.
        modifiers = [self.image[0x6b2daa + job * 0x40 - IMAGE_BASE] for job in range(30)]
        self.assertEqual(modifiers, [0] * 30)


if __name__ == '__main__':
    unittest.main()
