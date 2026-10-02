"""Check the handoff fixture against the original T0005.BIN bytes and container."""
import json
import struct
import unittest
from pathlib import Path

from tools.ybc32_disasm import parse


ROOT = Path(__file__).resolve().parents[2]


class BattleScriptSignalFixtureTests(unittest.TestCase):
    def test_source_offset_and_raw_instruction(self):
        fixture = json.loads((ROOT / 'prototype/data/battle_script_signals.json').read_text('utf-8'))
        self.assertEqual(fixture['schema_version'], 2)
        self.assertEqual(len(fixture['signals']), 1)
        request = fixture['signals'][0]
        data = (ROOT / 'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/SCRIPT' /
                request['script']).read_bytes()
        records = parse(data)
        matching = [(code, pool) for block, sub, code, pool in records
                    if (block, sub) == (request['block'], request['sub'])]
        self.assertEqual(matching, [(0x24a8, 0x2b38)])
        offset = request['instruction_offset']
        self.assertGreaterEqual(offset, matching[0][0])
        self.assertLess(offset + request['advance'], matching[0][1])
        opcode, advance = struct.unpack_from('<HH', data, offset)
        self.assertEqual((opcode, advance), (request['opcode'], request['advance']))
        self.assertEqual((opcode, advance), (112, 16))
        self.assertEqual(request['handler_va'], 0x42dcf0)
        self.assertEqual(request['dispatcher_switch_index'], opcode-5)
        self.assertEqual(list(struct.unpack_from('<III', data, offset + 4)),
                         request['raw_cells'])
        self.assertEqual(data[offset:offset + advance].hex(), request['raw_instruction_hex'])
        self.assertEqual(struct.unpack_from('<H', data, offset + advance)[0], 146)
        self.assertEqual(request['interpretation'], 'intermediate_script_signal_only')


if __name__ == '__main__':
    unittest.main()
