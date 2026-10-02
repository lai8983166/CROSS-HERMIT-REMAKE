"""Native workroom control must follow actual CH001 and CH002 completion."""
import hashlib
import importlib.util
import json
import struct
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.workroom_return_emulation import report, WorkroomReturnEmulator, WORKROOM, CH003
    from tools.tactics_exit_emulation import ROOT, SOURCE, report_text

REPORT_SHA256 = '75bec06bce23826fb89228ab466b603c64cd030232fac05764df519f3d215bae'


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class WorkroomReturnTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()
        cls.cases = {c['name']: c for c in cls.report['cases']}

    def test_report_reexecutes_exact_bytes_and_declared_source_resources(self):
        path = ROOT / 'analysis/workroom-return-v1-20261002.json'
        self.assertEqual(path.read_text(encoding='utf-8'), report_text(self.report))
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), REPORT_SHA256)
        self.assertNotIn(b'\r', path.read_bytes())
        for c in self.cases.values():
            for event in c['work_events']:
                if event['kind'] == 'graphics_resource_boundary':
                    source = ROOT / 'CROSS HERMIT/CROSS HERMIT' / event['path']
                    self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), event['source_sha256'])
            for load in c['work_script_loads']:
                self.assertEqual(hashlib.sha256((CH003.parent / load['path']).read_bytes()).hexdigest(), load['source_sha256'])
            for instruction in c['ch002_commands']:
                source = (CH003.parent / instruction['path']).read_bytes()
                self.assertEqual(struct.unpack_from('<HH', source, instruction['offset']),
                                 (instruction['opcode'], instruction['advance']))

    def test_godot_fixture_comes_from_same_native_run_and_keeps_declared_authority(self):
        from tools.workroom_return_fixture import fixture
        path = ROOT / 'prototype/data/workroom_return_evidence.json'
        self.assertEqual(path.read_text(encoding='utf-8'), report_text(fixture(self.report)))
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                         '1b7a965ee08fef6e53bf5eddbfc3f7ca5787e02d3f1c778a6cf25afab8f89c8f')
        data = json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(data['native_report_sha256'], REPORT_SHA256)
        self.assertFalse(data['school_initialized'])
        self.assertFalse(data['live_witness'])
        self.assertFalse(data['authorizes_persistent_write'])

    def test_pending8_from_real_ch001_constructs_original_workroom(self):
        upstream = json.loads((ROOT / 'analysis/new-week-adv-v1-20261002.json').read_text())['cases'][0]
        for c in self.cases.values():
            self.assertEqual(c['before_override'], upstream['after_ch001'])
            self.assertTrue(c['upstream']['ch001_completed'])
            self.assertEqual(c['upstream']['state_requests'], [{'va': '0x439e30', 'state': 8}])
            self.assertEqual(c['consumed_request'], {'pending_flag': 1, 'state': 8,
                'adv_active': 0, 'native_dispatch_va': '0x49e2b0'})
            self.assertEqual((c['work_task']['pointer'], c['work_task']['vtable'], c['work_task']['active']),
                             (hex(WORKROOM), '0x5a0904', 1))
            for va in ('0x49e2b0', '0x4a16c0', '0x4a1350', '0x4a1570', '0x49f6c0', '0x49fd50', '0x56cda0'):
                self.assertIn(va, c['visited_original_addresses'])
            self.assertEqual(c['stub_calls']['isolated_workroom_allocation'], 1)
            self.assertEqual(c['stub_calls']['isolated_workroom_registration'], 1)

    def test_news_list_uses_original_date_table_and_background_selector(self):
        source = SOURCE.read_bytes()
        expected = set()
        for index in range(1, 200):
            month, week = struct.unpack_from('<bb', source, 0x750A41+index*8-0x400000)
            if month == -1:
                break
            date = month*5+week-1
            if date <= 25:
                expected.add((date, index))
        else:
            self.fail('source news table lacks bounded terminator')
        for c in self.cases.values():
            entries = c['work_task']['news_entries']
            self.assertEqual(c['work_task']['news_count'], 24)
            self.assertEqual({tuple(row) for row in entries}, expected)
            self.assertEqual([row[0] for row in entries], sorted([row[0] for row in entries], reverse=True))
            graphics = [e['path'] for e in c['work_events'] if e['kind'] == 'graphics_resource_boundary']
            self.assertEqual(graphics, ['data/workroom/workroom.bin', 'data/adv/bin/bg002_d.bin'])

    def test_first_visit_button_loads_ch002_and_real_end_requests9(self):
        c = self.cases['first_workroom_then_ch002']
        self.assertEqual([e['value'] for e in c['work_events'] if e['kind'] == 'control_phase'], [0, 1, 4])
        self.assertEqual(c['work_yields'], 63)
        self.assertEqual(c['work_state_requests'], [{'va': '0x439e30', 'state': 6}])
        self.assertEqual([v['path'] for v in c['work_script_loads']], ['ch002.ybc'])
        self.assertEqual(c['ch002_consumed_request']['next_task_state'], 9)
        self.assertTrue(c['ch002_completed'])
        self.assertEqual(c['ch002_commands'][-1], {'frame': 8, 'offset': 0x6D0,
            'opcode': 19, 'advance': 4, 'path': 'ch002.ybc'})
        self.assertEqual(c['ch002_state_requests'], [{'va': '0x439e30', 'state': 9}])
        self.assertEqual((c['pending_flag'], c['pending_state']), (1, 9))
        self.assertEqual(c['after_workroom']['flags']['0x7a4e62'], 1)
        self.assertEqual(c['after_workroom']['flags']['0x7a55f6'], 9)
        self.assertEqual((c['after']['flags']['0x7a55f6'], c['after']['flags']['0x7e11a0']), (11, 0))

    def test_continue_and_ch002_fade_waits_cannot_request_school(self):
        c = self.cases['workroom_waits_for_continue']
        self.assertEqual(c['work_task']['control_phase'], 1)
        self.assertEqual(c['stop_reason'], 'workroom_waiting_continue')
        self.assertEqual(c['work_state_requests'], [])
        self.assertEqual(c['work_script_loads'], [])
        self.assertIsNone(c['ch002_consumed_request'])
        self.assertEqual(c['before_workroom'], c['after'])
        c = self.cases['ch002_fade_wait_blocks9']
        self.assertEqual(c['stop_reason'], 'bounded_pending_chapter')
        self.assertFalse(c['ch002_completed'])
        self.assertEqual(c['ch002_state_requests'], [])
        self.assertNotEqual(c['pending_state'], 9)
        self.assertFalse(any(v['opcode'] == 19 for v in c['ch002_commands']))

    def test_declared_visited_branch_skips_ch002_preserving_all_roles_and_calendar(self):
        c = self.cases['visited_workroom_direct9_control']
        self.assertEqual(c['synthetic_visited_override'], 1)
        before = c['before_override'].copy()
        before['flags'] = before['flags'].copy()
        before['flags']['0x7a4e62'] = 1
        self.assertEqual(c['before_workroom'], before)
        self.assertEqual(c['work_state_requests'], [{'va': '0x439e30', 'state': 9}])
        self.assertEqual(c['work_script_loads'], [])
        self.assertEqual(c['ch002_commands'], [])
        self.assertIsNone(c['ch002_consumed_request'])
        self.assertFalse(c['ch002_completed'])
        self.assertEqual(c['before_workroom'], c['after'])
        for c in self.cases.values():
            for key, value in c['before_workroom'].items():
                if key != 'flags':
                    self.assertEqual(c['after'][key], value, key)
            for flag in ('school_initialized', 'live_witness', 'authorizes_persistent_write'):
                self.assertFalse(c[flag])
            for stub in ('vm_update', 'unresolved_mvp_vm_update', 'unresolved_mvp_or_school_script_load'):
                self.assertNotIn(stub, c['stub_calls'])

    def test_missing_pending_requests_single_use_and_invalid_inputs_reject_before_writes(self):
        for args in ({'continue_ready': 1}, {'school_fade_ready': None},
                     {'visited_override': True}, {'visited_override': 0}, {'visited_override': 2}):
            with self.assertRaises(ValueError):
                WorkroomReturnEmulator(**args)
        x = WorkroomReturnEmulator()
        before = x.flow_snapshot()
        x.phase = 'workroom'
        with self.assertRaisesRegex(RuntimeError, 'actual unconsumed next8'):
            x.call(0x49E2B0)
        self.assertEqual(x.flow_snapshot(), before)
        x.phase = 'ch002_adv'
        with self.assertRaisesRegex(RuntimeError, 'actual workroom load'):
            x.call(0x4D1A80, (0,))
        self.assertEqual(x.flow_snapshot(), before)
        x._ran_work = True
        with self.assertRaisesRegex(RuntimeError, 'single-run'):
            x.run_return('again')
        self.assertEqual(x.flow_snapshot(), before)


if __name__ == '__main__':
    unittest.main()
