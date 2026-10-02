"""Synthetic decoder tests and original-byte checks, not runtime witnesses."""
from pathlib import Path
import struct
import unittest
from unittest.mock import patch
import tempfile
import hashlib
import json

from tools.battle_runtime_trace import BASE, PROBES, SCENE5_SCRIPT, TraceError, main, sample, verify_image

ROOT = Path(__file__).resolve().parents[2]


class FakeMemory:
    def __init__(self):
        self.bytes = {}

    def put(self, address, data):
        self.bytes.update({address+i: value for i, value in enumerate(data)})

    def number(self, address, value, fmt='I'):
        self.put(address, struct.pack('<'+fmt, value))

    def read(self, address, size):
        return bytes(self.bytes.get(address+i, 0) for i in range(size))


def memory(state=16):
    m = FakeMemory()
    m.number(0x7A4A00, 0x1000000)
    m.number(0x100002C, 0)
    m.number(0x1000030, state)
    for address, value in ((0x7A528E, 4), (0x7A5290, 5), (0x7A5296, 1),
                           (0x7A5298, 1), (0x7A5260, 3), (0x7F4488, 5),
                           (0x7AAB16, 5)):
        m.number(address, value, 'h')
    m.put(0x7A5210, struct.pack('<3h', 3, 4, 9))
    for g in range(5):
        m.put(0x7AAA22 + g*0x1c, struct.pack('<4h', *([3, 4, 9, -1] if not g else [-1]*4)))
    m.put(0x7AAAE0, struct.pack('<20h', 0, 1, 2, *([-1]*17)))
    m.put(0x7A52D0, struct.pack('<3h', 3, 4, 9))
    m.number(0x7A52F8, 3, 'H')
    m.number(0x7A5308, 5, 'h')
    m.number(0x7A4174, 0x1100000)
    m.number(0x1100000, 0x59A430)
    m.number(0x1100034, 2)
    m.number(0x110004C, 1)
    m.number(0x1100060, 0x1200000)
    m.number(0x120001C, 100)
    m.number(0x1200020, 4, 'H')
    m.number(0x12092E0, 1, 'B')
    return m


class RuntimeTraceTests(unittest.TestCase):
    def test_synthetic_snapshot_retains_id_index_distinction(self):
        result = sample(memory().read)
        self.assertTrue(result['valid'])
        obs = result['observation']
        self.assertEqual(obs['participant_ids'], [3, 4, 9])
        self.assertEqual(obs['group_member_ids'][0], [3, 4, 9, -1])
        self.assertEqual(obs['group_participant_indexes'][0], [0, 1, 2, -1])
        self.assertEqual(obs['first_round_member_ids'], [3, 4, 9])
        self.assertEqual(obs['first_round_config_id'], 5)
        self.assertEqual(obs['current_round'], obs['total_rounds'])
        self.assertEqual(obs['tactics']['exit_flag'], 1)
        self.assertEqual(obs['tactics']['vm']['script_work_wait'], 1)
        self.assertEqual(result['consistency'], 'equal_endpoints_not_atomic')
        self.assertFalse(result['authorizes_persistent_write'])

    def test_state11_slot_does_not_read_stale_tactics_pointer(self):
        m = memory(11)
        def read(address, size):
            self.assertNotEqual(address, 0x7A4174)
            return m.read(address, size)
        obs = sample(read)['observation']
        self.assertEqual(obs['request_dispatch_state'], 11)
        self.assertIsNone(obs['tactics'])

    def test_distinct_script_transition_and_completion_phases(self):
        m = memory()
        m.number(0x1100038, 19)
        m.number(0x1100044, 6, 'B')
        m.number(0x1100058, 0, 'B')
        m.number(0x1100059, 3, 'B')
        m.put(0x1100170, bytes([1, 1, 1]))
        result = sample(m.read)
        self.assertTrue(result['valid'])
        task = result['observation']['tactics']
        self.assertEqual(task['transition_phase'], 19)
        self.assertEqual(task['script_phase'], 6)
        self.assertEqual(task['control_phase'], 0)
        self.assertEqual(task['script_completion_phase'], 3)
        self.assertEqual(task['finish_flags'], [1, 1, 1])
        self.assertFalse(result['authorizes_persistent_write'])

    def test_changing_transition_phase_rejects_entire_snapshot(self):
        m, calls = memory(), 0
        def read(address, size):
            nonlocal calls
            if address == 0x1100000:
                calls += 1
                if calls == 2:
                    m.number(0x1100038, 20)
            return m.read(address, size)
        result = sample(read)
        self.assertFalse(result['valid'])
        self.assertNotIn('observation', result)

    def test_matches_real_subrecord_bytes_but_not_call_provenance(self):
        source = SCENE5_SCRIPT.read_bytes()
        block = struct.unpack_from('<I', source, 8)[0]
        for sub in (2, 5, 8, 11, 14, 20):
            record = block + struct.unpack_from('<I', source, block+8+sub*4)[0]
            code = record + struct.unpack_from('<I', source, record+4)[0]
            m = memory()
            m.number(0x1100064, 0x1300000)
            m.put(0x1300000, source)
            m.number(0x120000C, 0x1300000+record)
            m.number(0x1200010, 0x1300000+code)
            resolution = sample(m.read, source)['observation']['tactics']['scene5_script_selection']
            self.assertEqual(resolution['status'], 'selected_record_observed')
            self.assertEqual(resolution['sub'], sub)
            self.assertEqual(resolution['is_terminal_candidate'], sub != 20)
            self.assertFalse(resolution['call_site_proven'])
            self.assertFalse(resolution['authorizes_persistent_write'])
            m.number(0x1200010, 0x1300000+code+1)
            resolution = sample(m.read, source)['observation']['tactics']['scene5_script_selection']
            self.assertEqual(resolution['status'], 'unresolved')

    def test_unknown_loaded_script_is_not_identified(self):
        source = SCENE5_SCRIPT.read_bytes()
        m = memory()
        m.number(0x1100064, 0x1300000)
        result = sample(m.read, source)
        self.assertTrue(result['valid'])
        selection = result['observation']['tactics']['scene5_script_selection']
        self.assertEqual(selection['status'], 'unresolved')
        self.assertEqual(selection['reason'], 'loaded_script_differs_from_T0005')

    def test_reject_changed_endpoint(self):
        m, counts = memory(), {}
        def read(address, size):
            counts[address] = counts.get(address, 0) + 1
            if address == 0x7A4A00 and counts[address] == 2:
                return struct.pack('<I', 0x1300000)
            return m.read(address, size)
        result = sample(read)
        self.assertFalse(result['valid'])
        self.assertIn('endpoint changed', result['error'])
        self.assertNotIn('observation', result)

    def test_reject_partial_and_unreadable_data(self):
        for read in (lambda a, n: bytes(max(0, n-1)),
                     lambda a, n: (_ for _ in ()).throw(OSError('unreadable'))):
            result = sample(read)
            self.assertFalse(result['valid'])
            self.assertFalse(result['authorizes_persistent_write'])

    def test_reject_bad_vtable_and_oversized_count(self):
        for address, value, fmt in ((0x1100000, 0x59A431, 'I'), (0x7A5260, 41, 'H'),
                                    (0x7A4A00, 0, 'I'), (0x7A4174, 0, 'I')):
            m = memory()
            m.number(address, value, fmt)
            self.assertFalse(sample(m.read)['valid'])

    def test_refuses_overwriting_existing_trace_and_closes_handle(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'trace.jsonl'
            path.touch()
            with patch('tools.battle_runtime_trace.ProcessReader') as reader, \
                    patch('tools.battle_runtime_trace.select_pid', return_value=1), \
                    patch('tools.battle_runtime_trace.verify_image', return_value={}), \
                    patch('tools.battle_runtime_trace.sys.stderr'):
                self.assertEqual(main(['--once', '--out', str(path)]), 2)
                reader.return_value.close.assert_called_once()
            self.assertEqual(path.read_bytes(), b'')

    def test_failed_preflight_does_not_create_trace(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'trace.jsonl'
            with patch('tools.battle_runtime_trace.ProcessReader') as reader, \
                    patch('tools.battle_runtime_trace.select_pid', return_value=1), \
                    patch('tools.battle_runtime_trace.verify_image', side_effect=TraceError('wrong image')), \
                    patch('tools.battle_runtime_trace.sys.stderr'):
                self.assertEqual(main(['--once', '--out', str(path)]), 2)
                reader.return_value.close.assert_called_once()
            self.assertFalse(path.exists())

    def test_original_image_probes_and_fixed_header(self):
        source = (ROOT / 'analysis/hermit_game.exe').read_bytes()
        read = lambda a, n: source[a-BASE:a-BASE+n]
        verified = verify_image(read, source)
        self.assertEqual(len(verified['source_sha256']), 64)
        self.assertEqual(len(verified['probes']), len(PROBES))
        def wrong(a, n):
            data = read(a, n)
            return bytes(n) if a == PROBES[-1][0] else data
        with self.assertRaisesRegex(TraceError, 'probe mismatch'):
            verify_image(wrong, source)

    def test_valid_pe_header_must_match_expected_architecture(self):
        source = (ROOT / 'analysis/hermit_game.exe').read_bytes()
        m = FakeMemory()
        m.put(BASE, source[:0x1000])
        m.number(BASE+0x3c, 0x80)
        m.put(BASE+0x80, b'PE\0\0')
        m.number(BASE+0x84, 0x14c, 'H')
        m.number(BASE+0x98, 0x10b, 'H')
        m.number(BASE+0xb4, BASE)
        m.number(BASE+0xd0, len(source))
        for address, size in PROBES:
            m.put(address, source[address-BASE:address-BASE+size])
        self.assertEqual(verify_image(m.read, source)['header_status'], 'pe32')
        m.number(BASE+0x84, 0x8664, 'H')
        with self.assertRaisesRegex(TraceError, 'x86 PE32'):
            verify_image(m.read, source)

    def test_checked_in_startup_capture_is_not_a_scene5_witness(self):
        rows = [json.loads(line) for line in
                (ROOT / 'prototype/data/battle_runtime_startup_trace.jsonl').read_text('utf-8').splitlines()]
        self.assertEqual([r['kind'] for r in rows], ['trace_metadata', 'sample', 'trace_end'])
        source = (ROOT / 'analysis/hermit_game.exe').read_bytes()
        self.assertEqual(rows[0]['verification']['source_sha256'], hashlib.sha256(source).hexdigest())
        self.assertTrue(rows[1]['valid'])
        obs = rows[1]['observation']
        self.assertEqual(obs['scene_id'], 0)
        self.assertEqual(obs['selected_task_id'], 0)
        self.assertEqual(obs['request_dispatch_state'], 0xffffffff)
        self.assertEqual(obs['participant_ids'], [3, 4, 9])
        self.assertEqual(obs['group_participant_indexes'][0], [0, 1, 2, -1])
        self.assertEqual(obs['total_rounds'], 0)
        self.assertIsNone(obs['tactics'])
        self.assertFalse(rows[1]['authorizes_persistent_write'])

    def test_original_field_instructions(self):
        source = (ROOT / 'analysis/hermit_game.exe').read_bytes()
        at = lambda a, n: source[a-BASE:a-BASE+n]
        self.assertEqual(at(0x439EAC, 13), bytes.fromhex('8951208b45fcc7401c01000000'))
        self.assertEqual(at(0x4CE51C, 4), bytes.fromhex('894c100c'))
        self.assertEqual(at(0x4CE5C4, 4), bytes.fromhex('89441110'))
        self.assertEqual(at(0x4CE503, 4), bytes.fromhex('894c1008'))


if __name__ == '__main__':
    unittest.main()
