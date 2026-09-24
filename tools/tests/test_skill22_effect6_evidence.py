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
        cls.skill_attributes = json.loads(
            (ROOT / 'prototype/data/skill_attributes_table.json').read_text('utf-8'))

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
            self.image[0x6c2dc8 + 22 * 0x48 + 0x1a - IMAGE_BASE],
            6,
        )
        self.assertEqual(
            self.image[0x6d4e58 + 22 * 7 + 6 - IMAGE_BASE],
            2,  # 491EF0 dispatches this damage type to MP damage.
        )
        self.assertEqual(
            self.image[0x611538 + 22 * 0x10 - IMAGE_BASE:
                       0x611538 + 23 * 0x10 - IMAGE_BASE],
            bytes.fromhex('0d 1f 10 00 fc 07 d3 0b 16 00 00 00 ed 07 00 00'),
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

    def test_skill22_mp_loss_uses_signed_magic_hit_value_not_condition_duration(self):
        attack = (ROOT / 'analysis/decomp_all/488bc0.c').read_text('utf-8')
        magic = (ROOT / 'analysis/decomp_all/4826f0.c').read_text('utf-8')
        dispatch = (ROOT / 'analysis/decomp_all/491ef0.c').read_text('utf-8')
        queue = (ROOT / 'analysis/decomp_all/493180.c').read_text('utf-8')
        apply_queue = (ROOT / 'analysis/decomp_all/493450.c').read_text('utf-8')
        apply_value = (ROOT / 'analysis/decomp_all/472550.c').read_text('utf-8')

        self.assertIn('FUN__text__004826f0(local_44,local_70)', attack)
        self.assertIn('sStack_e = -local_1c;', attack)
        self.assertIn('((100 - (uint)*(byte *)(param_2 + 10)) + *(int *)(param_2 + 0x1c))',
                      magic)
        self.assertIn('(uint)*(byte *)(param_2 + 0xb) * *(int *)(param_2 + 0x18)', magic)
        self.assertIn('*(uint *)(param_1 + 0x14) = local_c;', magic)
        self.assertIn('FUN__text__00493180(param_2,*(undefined2 *)(param_3 + 10))', dispatch)
        self.assertIn('*(short *)(local_c + 2) = param_2;', queue)
        self.assertIn('FUN__text__00472550(param_2,1,(int)*(short *)(local_c + 2))', apply_queue)
        self.assertIn('*(undefined2 *)(*(int *)(param_1 + 600) + 0x1c) =', apply_value)

    def test_skill_attribute_export_preserves_indexed_and_fallback_rows(self):
        self.assertEqual(self.skill_attributes['_meta']['source_va'], 0x6d4e58)
        self.assertEqual(len(self.skill_attributes['rows']), 101)
        self.assertEqual(self.skill_attributes['rows'][22]['bytes'],
                         [1, 1, 1, 3, 1, 1, 2])
        self.assertEqual(self.skill_attributes['fallback']['bytes'],
                         [1, 1, 1, 1, 1, 1, 0])
        self.assertEqual(
            self.image[0x738af0 - IMAGE_BASE:0x738af7 - IMAGE_BASE],
            bytes(self.skill_attributes['fallback']['bytes']),
        )


if __name__ == '__main__':
    unittest.main()
