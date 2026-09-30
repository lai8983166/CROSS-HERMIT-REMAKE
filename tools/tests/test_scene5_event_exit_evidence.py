"""Tie scene 5's event branches to actual T0005 subrecords and EXE calls."""
import json
import struct
import unittest
from pathlib import Path

from tools.ybc32_disasm import parse


ROOT = Path(__file__).resolve().parents[2]
IMAGE_BASE = 0x400000


class Scene5EventExitEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads((ROOT / 'prototype/data/scene5_event_exit_evidence.json')
                                 .read_text('utf-8'))
        cls.exe = (ROOT / 'analysis/hermit_game.exe').read_bytes()
        cls.script = (ROOT / 'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/SCRIPT' /
                      cls.fixture['script']).read_bytes()
        cls.records = {(block, sub): code for block, sub, code, _ in parse(cls.script)}

    @classmethod
    def at(cls, va, size):
        offset = va - IMAGE_BASE
        return cls.exe[offset:offset + size]

    def assert_call(self, va, target):
        instruction = self.at(va, 5)
        self.assertEqual(instruction[0], 0xe8)
        displacement, = struct.unpack_from('<i', instruction, 1)
        self.assertEqual(va + 5 + displacement, target)

    def opcodes_in_sub(self, sub):
        pc = self.records[(0, sub)]
        opcodes = []
        while True:
            opcode, advance = struct.unpack_from('<HH', self.script, pc)
            opcodes.append((pc, opcode))
            if opcode == 19:
                break
            self.assertGreaterEqual(advance, 4)
            pc += advance
        return opcodes

    def test_scene_dispatch_and_parallel_gate(self):
        self.assertEqual(self.fixture['schema_version'], 1)
        self.assertEqual(self.fixture['scene_id'], 5)
        self.assertEqual(self.fixture['evidence_kind'],
                         'original_branch_conditions_not_runtime_trace')
        # UnitCtrl event dispatcher checks +108B48 before the scene switch.
        self.assertEqual(self.at(0x432140, 7), bytes.fromhex('0fbe91488b1000'))
        self.assert_call(0x432216, 0x4337f0)
        # Parallel controller's final phase clears that event-dispatch gate.
        self.assertEqual(self.at(0x49a29f, 4), bytes.fromhex('c6420a00'))

    def test_sub20_opcode_112_is_on_nonterminal_event_branch(self):
        event = self.fixture['intermediate_event']
        self.assertEqual((event['script_block'], event['script_sub']), (0, 20))
        self.assertEqual(event['unitctrl_event_call_va'], 0x433849)
        self.assertEqual(self.at(0x43383a, 6), bytes.fromhex('6a146a006a00'))
        self.assert_call(event['unitctrl_event_call_va'], 0x454bb0)
        self.assert_call(0x454bd8, 0x4551c0)
        self.assert_call(0x4551ed, 0x455060)
        self.assert_call(0x455203, 0x455060)
        self.assertEqual(event['tactics_exit_flag_argument'], 0)
        self.assertIn((event['script_opcode_112_offset'], 112),
                      self.opcodes_in_sub(event['script_sub']))
        self.assertEqual(event['event_bit'],
                         {'type': 3, 'offset': 0, 'written_value': 1})
        self.assertEqual(self.at(0x43384e, 6), bytes.fromhex('6a016a006a03'))
        self.assert_call(0x433854, 0x4e29a0)

    def test_other_scene5_branches_request_terminal_scripts(self):
        self.assertEqual(self.fixture['conditional_terminal_subs'], [2, 5, 8, 11, 14])
        for sub in self.fixture['conditional_terminal_subs']:
            with self.subTest(sub=sub):
                self.assertIn((0, sub), self.records)
                self.assertNotIn(112, [opcode for _, opcode in self.opcodes_in_sub(sub)])
        self.assertEqual(self.fixture['tactics_exit_flag_argument'], 1)
        for va in self.fixture['terminal_wrapper_calls']:
            with self.subTest(call=hex(va)):
                self.assert_call(va, 0x454ab0 if va in (0x4338ad, 0x4338bf)
                                 else 0x454af0)
        # 454AF0 always passes first argument 1 to 454BB0.
        self.assertEqual(self.at(0x454b71, 4), bytes.fromhex('6a006a01'))
        self.assert_call(0x454b78, 0x454bb0)
        self.assertEqual(self.fixture['scene5_reached_terminal_call'], 'unresolved')
        self.assertEqual(self.fixture['opcode_112_causes_terminal_call'], 'unresolved')


if __name__ == '__main__':
    unittest.main()
