"""Actual pending9 must construct both source tasks, without claiming school init."""
import hashlib
import importlib.util
import json
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.school_dispatch_emulation import report, SchoolDispatchEmulator, GROUP_TASK, PERSON_TASK
    from tools.tactics_exit_emulation import ROOT, report_text
    from tools.adv_chapter_emulation import CONTROLLER
    from tools.scene5_script_emulation import VM

REPORT_SHA256 = '2a12cb13114c9b372da7ce565bdddb811c1c97ebcc943b9dee0ce626fa2774dd'


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class SchoolDispatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()
        cls.cases = {c['name']: c for c in cls.report['cases']}

    def test_report_is_exact_native_reexecution(self):
        path = ROOT / 'analysis/school-dispatch-v1-20261003.json'
        self.assertEqual(path.read_text(encoding='utf-8'), report_text(self.report))
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), REPORT_SHA256)
        self.assertNotIn(b'\r', path.read_bytes())

    def test_all_cases_preserve_same_cpu_workroom_output_and_whole_role_snapshots(self):
        prior = json.loads((ROOT / 'analysis/workroom-return-v1-20261002.json').read_text(encoding='utf-8'))['cases']
        for c, predecessor in zip(self.report['cases'], [prior[0], prior[2], prior[1], prior[3]]):
            self.assertEqual(c['before'], predecessor['after'])
            self.assertEqual(c['after'], c['before'])
            self.assertEqual(c['school_state_requests'], [])
            for flag in ('school_initialized', 'school_task_bodies_executed', 'live_witness', 'authorizes_persistent_write'):
                self.assertFalse(c[flag])

    def test_real_dispatch_consumes9_and_constructs_registers_both_tasks_in_order(self):
        for name in ('ch002_end_constructs_school', 'visited_workroom_constructs_school'):
            c = self.cases[name]
            self.assertTrue(c['school_constructed'])
            self.assertEqual(c['consumed_request'], {'pending_flag': 1, 'state': 9,
                'adv_active': 0, 'native_dispatch_va': '0x49e2b0'})
            self.assertEqual((c['pending_flag'], c['pending_state']), (0, 9))
            self.assertEqual([r['pointer'] for r in c['school_tasks']], [hex(GROUP_TASK), hex(PERSON_TASK)])
            self.assertEqual([r['vtable'] for r in c['school_tasks']], ['0x5a0a40', '0x5a0c18'])
            self.assertEqual([r['size'] for r in c['school_tasks']], [0x1419C, 0x3A5E4])
            self.assertEqual([r['active'] for r in c['school_tasks']], [1, 1])
            registered = [e for e in c['school_events'] if e['kind'] == 'registration_boundary']
            self.assertEqual([e['global_pointer_va'] for e in registered], ['0x7a4ad8', '0x7a4adc'])
            self.assertEqual([e['args'] for e in registered], [[GROUP_TASK, 0, 2], [PERSON_TASK, 0, 2]])
            for va in ('0x4aba70', '0x4ab570', '0x4b89a0', '0x4b8a90', '0x56dda0'):
                self.assertIn(va, c['visited_original_addresses'])
            for va in ('0x4ab7a0', '0x4b8d50', '0x4a5ce0'):
                self.assertNotIn(va, c['visited_original_addresses'])
            self.assertEqual(c['stub_calls']['isolated_school_allocation'], 2)
            self.assertEqual(c['stub_calls']['isolated_school_registration'], 2)

    def test_original_vector_calls_five_distinct_embedded_text_constructors(self):
        for name in ('ch002_end_constructs_school', 'visited_workroom_constructs_school'):
            c = self.cases[name]
            vector = [e for e in c['school_events'] if e['kind'] == 'native_constructor_vector']
            self.assertEqual(vector, [{'kind': 'native_constructor_vector', 'base': hex(PERSON_TASK+0x19D20),
                'stride': 0x6424, 'count': 5, 'constructor': '0x4d5fb0', 'destructor': '0x4d6010'}])
            receivers = [e['receiver'] for e in c['school_events'] if e['kind'] == 'presentation_constructor_boundary'
                         and e['va'] == '0x4d5fb0']
            for index in range(5):
                self.assertEqual(receivers.count(hex(PERSON_TASK+0x19D20+index*0x6424)), 1)
            self.assertEqual(len(receivers), 12)
            self.assertEqual(c['person_font_handle'], 0x2345)

    def test_pending_continue_and_ch002_fade_cannot_construct_school(self):
        for name in ('continue_wait_blocks_school', 'ch002_wait_blocks_school'):
            c = self.cases[name]
            self.assertFalse(c['school_constructed'])
            self.assertIsNone(c['consumed_request'])
            self.assertEqual(c['school_events'], [])
            self.assertEqual([r['vtable'] for r in c['school_tasks']], ['0x0', '0x0'])
            self.assertEqual([r['active'] for r in c['school_tasks']], [0, 0])
            self.assertNotIn('isolated_school_allocation', c['stub_calls'])
            self.assertNotEqual(c['pending_state'], 9)

    def test_missing_wrong_or_active_adv_requests_and_duplicate_probe_reject_before_allocation(self):
        x = SchoolDispatchEmulator()
        x.phase = 'school_dispatch'
        before = x.flow_snapshot()
        for state, pending, active in ((9, 0, 0), (8, 1, 0), (9, 1, 1)):
            x.write(CONTROLLER+0x30, state)
            x.write(CONTROLLER+0x2C, pending)
            x.write(VM+4, active, 'B')
            with self.assertRaisesRegex(RuntimeError, 'actual unconsumed request9'):
                x.call(0x49E2B0)
            self.assertEqual(x.flow_snapshot(), before)
            self.assertEqual(x.school_events, [])
            self.assertEqual(x.school_allocated, [])
        x._ran_school = True
        with self.assertRaisesRegex(RuntimeError, 'single-run'):
            x.run_school_dispatch('again')
        self.assertEqual(x.flow_snapshot(), before)


if __name__ == '__main__':
    unittest.main()
