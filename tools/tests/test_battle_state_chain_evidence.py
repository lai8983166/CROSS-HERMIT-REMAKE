"""Verify the state-chain branch fixture against the original EXE bytes."""
import json
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
IMAGE_BASE = 0x400000


class BattleStateChainEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(
            (ROOT / 'prototype/data/battle_state_chain.json').read_text('utf-8'))
        cls.exe = (ROOT / cls.fixture['source']).read_bytes()

    @classmethod
    def at(cls, va, size):
        offset = va - IMAGE_BASE
        return cls.exe[offset:offset + size]

    @classmethod
    def call_target(cls, va):
        instruction = cls.at(va, 5)
        assert instruction[0] == 0xe8
        return va + 5 + struct.unpack_from('<i', instruction, 1)[0]

    def test_controller_dispatch_uses_original_jump_table(self):
        self.assertEqual(self.fixture['schema_version'], 1)
        self.assertEqual(self.fixture['evidence_kind'],
                         'original_branch_predicates_not_playthrough')
        self.assertEqual(self.at(0x49e304, 7),
                         bytes.fromhex('ff248dd3e44900'))
        table = self.fixture['controller_jump_table_va']
        self.assertEqual(table, 0x49e4d3)
        for entry in self.fixture['dispatch']:
            with self.subTest(state=entry['state']):
                case_va, = struct.unpack('<I', self.at(table + 4 * entry['state'], 4))
                self.assertEqual(case_va, entry['case_va'])
                self.assertEqual(self.call_target(case_va), entry['constructor_va'])

        # The constructors install task vtables; their first slots select the
        # update handlers, rather than direct calls from the controller switch.
        for vtable, state in [(0x5a0dfc, 11), (0x5a0c38, 10),
                              (0x5a0f74, 12), (0x59a430, 16)]:
            entry = next(item for item in self.fixture['dispatch']
                         if item['state'] == state)
            update, = struct.unpack('<I', self.at(vtable, 4))
            self.assertEqual(update, entry['task_update_va'])

    def test_result_and_preparation_transition_calls(self):
        for entry in self.fixture['transition_checks']:
            with self.subTest(va=hex(entry['va'])):
                va = entry['va']
                self.assertEqual(self.at(va, 2), bytes([0x6a, entry['next_state']]))
                tail = self.at(va + 2, 24)
                self.assertEqual(self.call_target(va + 11), 0x439e30)
                self.assertEqual(tail[:6], bytes.fromhex('8b0d004a7a00'))
                self.assertEqual(tail[6:9], bytes.fromhex('83c110'))

        # 4B8FF0 compares the two 16-bit counters and branches to the
        # preparation path only when they differ.
        self.assertEqual(self.at(0x4b900d, 18), bytes.fromhex(
            '0fbf0596527a000fbf0d98527a003bc17515'))
        self.assertEqual(self.call_target(0x4b9052), 0x4da860)
        self.assertEqual(self.call_target(0x4b905a), 0x4b9210)
        self.assertEqual(self.call_target(0x4b90af), 0x4b9270)
        self.assertEqual(self.call_target(0x4b90b9), 0x4b92c0)
        self.assertEqual(self.at(0x4b90c8, 18), bytes.fromhex(
            '668b0d96527a006683c10166890d96527a00'))

    def test_two_predicate_paths_do_not_skip_preparation(self):
        paths = {path['name']: path for path in self.fixture['preparation_paths']}
        self.assertEqual(set(paths), {'all_rounds_complete', 'another_round_pending'})
        for path in paths.values():
            with self.subTest(path=path['name']):
                before = path['counter_before']
                if before['current'] == before['total']:
                    self.assertEqual(path['next_state'], 12)
                    self.assertFalse(path['preparation_writes'])
                    self.assertEqual(path['counter_after'], before)
                else:
                    self.assertEqual(path['next_state'], 16)
                    self.assertTrue(path['preparation_writes'])
                    self.assertEqual(path['counter_after']['current'],
                                     before['current'] + 1)
                    self.assertEqual(path['counter_after']['total'], before['total'])


if __name__ == '__main__':
    unittest.main()
