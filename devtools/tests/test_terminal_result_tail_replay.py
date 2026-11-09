"""Real retained-byte regressions; no native process and no proof output files."""
import copy
import gzip
import json
import os
from pathlib import Path
import unittest

from devtools import terminal_result_tail_replay as tail


ROOT = Path(__file__).resolve().parents[2]
WORKER = ROOT / '.venv-audit/native-worker'


class RetainedTailTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.window_path = Path(os.environ.get('TAIL_REPLAY_TEST_WINDOW',
            str(WORKER / 'terminal-battle-wait-window-battle-v6-20261109.json.gz')))
        cls.proof_path = Path(os.environ.get('TAIL_REPLAY_TEST_PROOF',
            str(ROOT / 'analysis/terminal-battle-wait-diagnostic-v1-20261109.json')))
        cls.inputs = tail.prepare(cls.window_path, cls.proof_path,
            os.environ.get('TAIL_REPLAY_TEST_IMAGE', str(ROOT / 'analysis/hermit_game.exe')),
            os.environ.get('TAIL_REPLAY_TEST_DLL', str(WORKER / 'guest-system-dlls/kernelbase.dll')))
        cls.window = json.loads(gzip.decompress(cls.window_path.read_bytes()))
        cls.proof = json.loads(cls.proof_path.read_bytes())

    def test_two_fresh_instances_naturally_consume_one_and_stop_before_missing_global(self):
        report = tail.diagnose(self.inputs)
        result = report['result']
        self.assertEqual(result['initial_integer_CPU']['EAX'], 0)
        self.assertEqual(result['initial_integer_CPU']['EIP'], 0x77D13BFC)
        self.assertEqual(result['final_integer_CPU']['EAX'], 1)
        self.assertEqual(result['frontier']['PC'], 0x451723)
        self.assertEqual(result['frontier']['address'], 0x7A49FC)
        self.assertFalse(result['frontier']['instruction_executed'])
        self.assertEqual(result['write_count'], result['frontier']['writes_before'])
        consumers = result['original_result_consumer_writes']
        self.assertEqual([(r['PC'], r['address'], r['after_hex']) for r in consumers],
                         [(0x451ABC, 0x27FFE60, '01000000'), (0x451716, 0x27FFED4, '01000000')])
        self.assertEqual([r['before_hex'] for r in consumers], ['cccccccc', '00000000'])
        returns = {(r['PC'], r['target']) for r in result['natural_returns']}
        self.assertTrue({(0x77D13BFC, 0x77B68229), (0x422431, 0x453CDD),
                         (0x453CFB, 0x451ABC), (0x451B0E, 0x451716)} <= returns)
        self.assertEqual(result['instruction_callbacks'], 118)
        self.assertEqual(result['write_count'], 36)
        self.assertTrue(report['second_fresh_Unicorn_exact_match'])
        self.assertFalse(report['accepted'])
        self.assertFalse(report['original_native_continuity'])
        self.assertFalse(report['pending_context_is_actual_post_syscall_context'])
        self.assertFalse(report['wrapper_live_code_authenticated'])
        self.assertFalse(report['first_result_consumer_453CB5_executed'])
        self.assertFalse(report['replay_record_4967B0_executed'])
        self.assertFalse(report['three_handshakes_executed'])
        self.assertLess(len(tail.canonical(report)), tail.REPORT_LIMIT)
        self.assertLess(result['mapped_storage_bytes'], tail.MEMORY_LIMIT)
        fs_writes = [r for r in result['writes'] if r['address'] == 0x302000]
        self.assertEqual(len(fs_writes), 1)
        self.assertEqual(fs_writes[0]['PC'], 0x77B6824B)
        self.assertFalse(result['segment_platform_inputs']['original_SS_selector_restored'])

    def test_each_crossing_snapshot_remains_rejected(self):
        for index in tail.EXCLUDED:
            with self.subTest(index=index):
                proof = copy.deepcopy(self.proof)
                item = next(x for x in proof['analysis']['unproven_switch_interval_snapshots']
                            if x['snapshot_index'] == index)
                item['used_to_prove_wait'] = True
                with self.assertRaisesRegex(ValueError, 'four crossing'):
                    tail.authenticate(self.window, proof)
                proof = copy.deepcopy(self.proof)
                proof['analysis']['waits'][0]['snapshot_indices'].append(index)
                with self.assertRaisesRegex(ValueError, '419 supported'):
                    tail.authenticate(self.window, proof)

    def test_nonzero_etw_return_or_other_pair_is_rejected(self):
        for field, value in (('NTSTATUS', 1), ('global_indices', [16929, 19426])):
            with self.subTest(field=field):
                proof = copy.deepcopy(self.proof)
                pair = next(x for x in proof['analysis']['waits'] if 15 in x['snapshot_indices'])
                pair[field] = value
                with self.assertRaisesRegex(ValueError, 'exact retained successful wait'):
                    tail.authenticate(self.window, proof)

    def test_context_and_original_result_are_not_patchable(self):
        for field in ('context', 'stack'):
            with self.subTest(field=field):
                window = copy.deepcopy(self.window)
                snap = window['window_snapshots'][15]
                if field == 'context':
                    raw = bytearray.fromhex(snap['frame']['context_hex'])
                    raw[176] = 1
                    snap['frame']['context_hex'] = raw.hex()
                else:
                    raw = bytearray.fromhex(snap['stack_regions'][0]['hex'])
                    raw[0] ^= 1
                    snap['stack_regions'][0]['hex'] = raw.hex()
                with self.assertRaisesRegex(ValueError, 'fixed complete selected snapshot'):
                    tail.authenticate(window, self.proof)

    def test_missing_known_stack_byte_is_not_zero_filled(self):
        inputs = copy.deepcopy(self.inputs)
        del inputs['sparse'].known[0x27FFCBC]
        # The first RET must stop, rather than treating mapped zero padding as a return address.
        with self.assertRaisesRegex(ValueError, 'exact first uncaptured original global'):
            tail.execute(inputs)

    def test_unknown_or_readonly_write_is_rejected_before_execution(self):
        inputs = copy.deepcopy(self.inputs)
        inputs['sparse'].writable.remove(0x302000)
        with self.assertRaisesRegex(ValueError, 'exact first uncaptured original global'):
            tail.execute(inputs)

    def test_unrestored_floating_point_instruction_is_rejected(self):
        inputs = copy.deepcopy(self.inputs)
        # Deliberate post-authentication in-memory corruption exercises the
        # executor's independent instruction-state guard, not source approval.
        for at, value in enumerate(bytes.fromhex('d9eec3'), 0x77D13BFC):
            inputs['sparse'].known[at] = value
        with self.assertRaisesRegex(ValueError, 'unsupported instruction/state: fldz'):
            tail.execute(inputs)

    def test_wrong_file_hash_and_conflicting_overlap_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'fixed input identity'):
            tail.pinned(self.proof_path, '0'*64, 512*1024)
        sparse = tail.Sparse()
        sparse.add(0x2000, b'ab')
        with self.assertRaisesRegex(ValueError, 'overlapping source bytes'):
            sparse.add(0x2001, b'c')
        self.assertEqual(sparse.missing(0x2000, 3), 0x2002)


if __name__ == '__main__':
    unittest.main()
