"""Actual CH001 execution and control writes require native chapter completion."""
import hashlib
import importlib.util
import json
import struct
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.new_week_adv_emulation import report, NewWeekAdvEmulator, CH003
    from tools.tactics_exit_emulation import ROOT, report_text

REPORT_SHA256 = '30fd7f6cfd1c7a8bfa07800c6483e3c2ed96bdf2f384f1960849be93c621257a'


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class NewWeekAdvTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()
        cls.cases = {c['name']: c for c in cls.report['cases']}

    def test_report_reexecutes_exact_bytes_and_all_commands_have_source_provenance(self):
        path = ROOT / 'analysis/new-week-adv-v1-20261002.json'
        self.assertEqual(path.read_text(encoding='utf-8'), report_text(self.report))
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), REPORT_SHA256)
        self.assertNotIn(b'\r', path.read_bytes())
        for c in self.cases.values():
            for load in c['upstream']['loads']+c['loads']:
                self.assertEqual(hashlib.sha256((CH003.parent / load['path']).read_bytes()).hexdigest(), load['source_sha256'])
            for instruction in c['commands']:
                source = (CH003.parent / instruction['path']).read_bytes()
                self.assertEqual(struct.unpack_from('<HH', source, instruction['offset']),
                                 (instruction['opcode'], instruction['advance']))

    def test_real_predecessor_and_date_router_load_ch022_then_ch208_preserving_next8(self):
        prior = json.loads((ROOT / 'analysis/adv-week-handoff-v1-20261002.json').read_text(encoding='utf-8'))['cases'][0]
        for c in self.cases.values():
            snapshot = c['before_ch001'].copy()
            snapshot.pop('adv_globals')
            self.assertEqual(snapshot, prior['after'])
            self.assertEqual(c['consumed_request'], {'state': 6, 'pending_flag': 1, 'path': 'ch001.ybc',
                'next_task_state': 8, 'vm_active': 1, 'vm_pc': 0,
                'driver_boundary': 'consume_native_pending_request_without_scheduler_constructor'})
        c = self.cases['ch001_ch022_ch208_complete']
        self.assertEqual([r['path'] for r in c['loads']], ['chapter022.ybc', 'chapter208.ybc'])
        self.assertEqual([(v['path'], v['offset']) for v in c['commands'] if v['opcode'] == 15],
                         [('ch001.ybc', 0x648), ('chapter022.ybc', 0x9FC)])
        self.assertEqual(c['stored_next_task_state'], 8)

    def test_true_ch208_end_requests8_without_completion_or_loader_stubs(self):
        c = self.cases['ch001_ch022_ch208_complete']
        self.assertTrue(c['ch001_completed'])
        self.assertEqual((c['frames'], len(c['commands'])), (909, 505))
        self.assertEqual(c['commands'][-1], {'frame': 909, 'offset': 0x1B0, 'opcode': 19,
                                          'advance': 4, 'path': 'chapter208.ybc'})
        self.assertEqual(c['state_requests'], [{'va': '0x439e30', 'state': 8}])
        self.assertEqual((c['pending_flag'], c['pending_state'], c['vm_active']), (1, 8, 0))
        for name in ('vm_update', 'unresolved_mvp_vm_update', 'unresolved_mvp_or_school_script_load'):
            self.assertNotIn(name, c['stub_calls'])
        self.assertFalse(any(i['opcode'] == 19 and i['path'] != 'chapter208.ybc' for i in c['commands']))

    def test_native151_and91_change_only_proven_global_fields(self):
        c = self.cases['ch001_ch022_ch208_complete']
        before, after = c['before_ch001'], c['after_ch001']
        self.assertEqual([k for k in before if before[k] != after[k]], ['flags', 'adv_globals'])
        expected_flags = before['flags'].copy()
        expected_flags.update({'0x7a55f6': 9, '0x7e11a0': 1})
        self.assertEqual(after['flags'], expected_flags)
        expected_globals = before['adv_globals'].copy()
        expected_globals['0x7a5292'] = 8
        self.assertEqual(after['adv_globals'], expected_globals)
        for va in ('0x4c4750', '0x4d0da0'):
            self.assertIn(va, c['visited_original_addresses'])
        self.assertEqual([i['opcode'] for i in c['commands'][-3:]], [151, 91, 19])

    def test_movie_source_is_declared_boundary_and_or_key_timer_still_runs_natively(self):
        c = self.cases['ch001_ch022_ch208_complete']
        self.assertEqual(len(c['movie_events']), 1)
        movie = c['movie_events'][0]
        self.assertEqual(movie['path'], 'data/adv/bin/tc0501.bin')
        self.assertFalse(movie['body_executed'])
        self.assertEqual(hashlib.sha256((ROOT/'CROSS HERMIT/CROSS HERMIT'/movie['path']).read_bytes()).hexdigest(), movie['source_sha256'])
        c = self.cases['ch001_key_wait']
        timer = next(i for i in c['commands'] if i['opcode'] == 13)
        next_command = c['commands'][c['commands'].index(timer)+1]
        self.assertGreaterEqual(next_command['frame']-timer['frame'], 600)
        self.assertIn('0x4ccb90', c['visited_original_addresses'])
        self.assertIn('0x4ccb30', c['visited_original_addresses'])

    def test_key_ui_and_fade_waits_prevent8_and_keep_roster_week_and_globals(self):
        for name, opcode in [('ch001_key_wait', 51), ('ch001_ui_wait', 56), ('ch001_fade_wait', 63)]:
            c = self.cases[name]
            self.assertEqual(c['stop_reason'], 'bounded_pending_chapter')
            self.assertFalse(c['ch001_completed'])
            self.assertEqual(c['commands'][-1]['opcode'], opcode)
            self.assertEqual(c['state_requests'], [])
            self.assertEqual((c['pending_flag'], c['pending_state'], c['vm_active']), (0, 6, 1))
            self.assertEqual(c['before_ch001'], c['after_ch001'])
        for c in self.cases.values():
            for key in ('workroom_executed', 'school_initialized', 'live_witness', 'authorizes_persistent_write'):
                self.assertFalse(c[key])

    def test_missing_predecessor_and_invalid_inputs_reject_before_native_writes(self):
        for args in ({'new_ui_ready': 1}, {'new_key_ready': None}, {'new_fade_ready': 'yes'},
                     {'new_max_frames': 0}, {'new_max_frames': 6001}):
            with self.assertRaises(ValueError):
                NewWeekAdvEmulator(**args)
        x = NewWeekAdvEmulator()
        x.phase = 'new_adv'
        before = x.flow_snapshot()
        with self.assertRaisesRegex(RuntimeError, 'requires actual state7'):
            x.call(0x4D1A80, (0,))
        self.assertEqual(x.flow_snapshot(), before)
        x._ran_new_adv = True
        with self.assertRaisesRegex(RuntimeError, 'single-run'):
            x.run_new_adv('again')
        self.assertEqual(x.flow_snapshot(), before)


if __name__ == '__main__':
    unittest.main()
