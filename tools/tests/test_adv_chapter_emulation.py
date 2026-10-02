"""Native chapter END and state7 request require actual sourced VM progress."""
import hashlib
import importlib.util
import json
import struct
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.adv_chapter_emulation import report, AdvChapterEmulator, CH003
    from tools.tactics_exit_emulation import ROOT, SOURCE, report_text

REPORT_SHA256 = '92e398d84d052b62207fd9d334208992eee8ed85b6b618511603f65738a1a54a'


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class AdvChapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()
        cls.cases = {c['name']: c for c in cls.report['cases']}

    def test_report_reexecutes_exact_bytes_and_source_resources(self):
        path = ROOT / 'analysis/adv-chapter-v1-20261002.json'
        self.assertEqual(path.read_text(encoding='utf-8'), report_text(self.report))
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), REPORT_SHA256)
        self.assertNotIn(b'\r', path.read_bytes())
        for c in self.cases.values():
            for load in c['loads']:
                source = (CH003.parent / load['path']).read_bytes()
                self.assertEqual(hashlib.sha256(source).hexdigest(), load['source_sha256'])
            for command in c['commands']:
                source = (CH003.parent / command['path']).read_bytes()
                self.assertEqual(struct.unpack_from('<HH', source, command['offset']),
                                 (command['opcode'], command['advance']))

    def test_native_router_and_replacement_load_preserve_parent_next7(self):
        c = self.cases['chapter020_021_complete']
        self.assertEqual([v['path'] for v in c['loads']], ['ch003.ybc', 'chapter020.ybc', 'chapter021.ybc'])
        loads = [v for v in c['commands'] if v['opcode'] == 15]
        self.assertEqual([(v['path'], v['offset']) for v in loads],
                         [('ch003.ybc', 0x4B0), ('chapter020.ybc', 0x237C)])
        self.assertEqual(c['stored_next_task_state'], 7)
        self.assertEqual(c['frames'], 2893)
        self.assertEqual(len(c['commands']), 1833)
        for entry in ('0x4c21f0', '0x4ce6e0', '0x4ce260', '0x4ce560', '0x4d1a80'):
            self.assertIn(entry, c['visited_original_addresses'])

    def test_actual_chapter021_end_requests_next7_after_native_cleanup(self):
        c = self.cases['chapter020_021_complete']
        self.assertTrue(c['chapter_completed'])
        self.assertIsNone(c['stop_reason'])
        self.assertEqual(c['commands'][-1], {'frame': 2893, 'offset': 0x61E,
            'opcode': 19, 'advance': 4, 'path': 'chapter021.ybc'})
        self.assertEqual((c['vm_active'], c['vm_wait']), (0, 0))
        self.assertEqual(c['state_requests'], [{'va': '0x439e30', 'state': 7}])
        self.assertEqual((c['pending_flag'], c['pending_state']), (1, 7))
        self.assertEqual(c['stub_calls']['task_destructor'], 1)
        for entry in ('0x4ce090', '0x4ce800', '0x4d0750', '0x4d0790', '0x439e30'):
            self.assertIn(entry, c['visited_original_addresses'])
        for forbidden in ('vm_update', 'unresolved_mvp_vm_update', 'unresolved_mvp_or_school_script_load'):
            self.assertNotIn(forbidden, c['stub_calls'])
        self.assertFalse(any(v['path'] == 'chapter020.ybc' and v['opcode'] == 19 for v in c['commands']))

    def test_ui_key_and_fade_waits_keep_native_join_but_prevent_completion(self):
        for name, opcode in [('key_wait_blocks_completion', 51), ('ui_wait_blocks_completion', 56),
                             ('fade_wait_blocks_completion', 63)]:
            c = self.cases[name]
            self.assertEqual(c['stop_reason'], 'bounded_pending_chapter')
            self.assertFalse(c['chapter_completed'])
            self.assertEqual(c['state_requests'], [])
            self.assertEqual(c['pending_flag'], 0)
            self.assertEqual((c['vm_active'], c['vm_wait']), (1, 1))
            self.assertEqual(c['commands'][-1]['opcode'], opcode)
            self.assertFalse(any(v['opcode'] == 19 for v in c['commands']))
            self.assertNotIn('task_destructor', c['stub_calls'])
            self.assertNotIn('0x4d0750', c['visited_original_addresses'])
            self.assertEqual(c['after']['student_count'], 4)

    def test_whole_chapter_paths_preserve_exact_native_join_snapshots(self):
        prefix = json.loads((ROOT / 'analysis/roster-join-v1-20261002.json').read_text(encoding='utf-8'))['cases'][0]
        for c in self.cases.values():
            self.assertEqual(c['before'], prefix['before'])
            self.assertEqual(c['after'], prefix['after'])
            self.assertEqual(len(c['join_entries']), 1)
            self.assertEqual(c['join_entries'][0], prefix['join_entries'][0])
        for c in self.cases.values():
            self.assertFalse(c['school_initialized'])
            self.assertFalse(c['live_witness'])
            self.assertFalse(c['authorizes_persistent_write'])

    def test_character_effect_wait_policy_runs_native_mode_switch(self):
        c = self.cases['chapter020_021_complete']
        self.assertIn('0x4c66e0', c['visited_original_addresses'])
        self.assertEqual(c['stub_calls']['character_effect_show'], 1)
        self.assertNotIn('character_effect', c['stub_calls'])
        # Third dispatcher arg3 is replaced with0/1 by the ORIGINAL wrapper.
        image = SOURCE.read_bytes()
        self.assertEqual(image[0x4C6794-0x400000:0x4C679B-0x400000], bytes.fromhex('c7451000000000'))
        self.assertEqual(image[0x4C67AF-0x400000:0x4C67B6-0x400000], bytes.fromhex('c7451001000000'))
        # Fade-install is cdecl; caller balances its argument. Popping4 in a
        # readiness boundary would corrupt the native VM stack.
        self.assertEqual(image[0x4DB05C-0x400000], 0xC3)

    def test_invalid_readiness_and_frame_bound_are_rejected(self):
        for kwargs in ({'ui_ready': 1}, {'key_ready': None}, {'fade_ready': 'yes'},
                       {'max_frames': 0}, {'max_frames': 6001}, {'difficulty': 1}):
            with self.assertRaises(ValueError):
                AdvChapterEmulator(**kwargs)


if __name__ == '__main__':
    unittest.main()
