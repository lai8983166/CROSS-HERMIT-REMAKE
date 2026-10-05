"""Original waiting-sort command consumers, independent of the Godot port."""
import hashlib
import importlib.util
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.school_waitlist_emulation import report, fixture, WaitlistEmulator, category_rules, IDS, MODE
    from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256, report_text

REPORT_SHA = '0ac3a8ae61751ccac425056e969b6b5ad69716242f09ce889b1aa87d1919bdc3'
FIXTURE_SHA = '3dc11db027bf6e821055bbe7c06d204bfc98160b8797ece209547b61596e823a'


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class WaitlistTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.native = report()
        cls.cases = {c['name']: c for c in cls.native['cases']}

    def test_frozen_native_and_fixture_reproduce_byte_exactly(self):
        for path, data, sha in [('analysis/school-waitlist-v1-20261005.json', self.native, REPORT_SHA),
                                ('prototype/data/school_waitlist_evidence.json', fixture(self.native), FIXTURE_SHA)]:
            raw = (ROOT/path).read_bytes()
            self.assertEqual(raw, report_text(data).encode('utf-8'))
            self.assertEqual(hashlib.sha256(raw).hexdigest(), sha)
            self.assertNotIn(b'\r', raw)

    def test_all_three_commands_reach_original_helper_with_feedback(self):
        for case in self.cases.values():
            for step in case['steps']:
                if step['command'] == 55:
                    continue
                self.assertIn('0x4a3ca0', step['visited_original_addresses'])
                self.assertIn('0x4a8bf0', step['visited_original_addresses'])
                self.assertEqual(step['after']['idle_sort_mode'], step['command']-11)
                self.assertEqual(step['stub_calls']['button_feedback_boundary'], 1)
                self.assertEqual([e['argument_low16'] for e in step['stub_events'] if 'argument_low16' in e],
                                 [step['command'], 5])

    def test_native_operands_use_student_list_and_commit_mode(self):
        from capstone import Cs, CS_ARCH_X86, CS_MODE_32
        source = SOURCE.read_bytes()
        ins = {i.address: (i.mnemonic, i.op_str) for i in Cs(CS_ARCH_X86, CS_MODE_32).disasm(
            source[0x4A3E29-0x400000:0x4A3E40-0x400000], 0x4A3E29)}
        self.assertEqual(ins[0x4A3E29], ('push', '0'))
        self.assertEqual(ins[0x4A3E33], ('call', '0x4a8bf0'))
        self.assertEqual(ins[0x4A3E3B], ('mov', 'byte ptr [0x7d57da], al'))

    def test_source_category_table_and_category_order_are_not_job_id_order(self):
        rules = category_rules()
        self.assertEqual(rules['source_image_sha256'], SOURCE_SHA256)
        self.assertEqual(rules['job_categories'], [0]+[1,1,2,2,3,3,4,4,5,5]*3)
        for name in ('route_0', 'route_1'):
            self.assertEqual(self.cases[name]['steps'][0]['after']['idle_student_ids'], [5,4,9,3])
        c = self.cases['exchange_ties']
        self.assertEqual(c['steps'][2]['after']['idle_student_ids'], [4,3,9,5])
        self.assertEqual(c['steps'][2]['after'], c['steps'][3]['after'])

    def test_numeric_swaps_displace_ties_and_use_different_keys(self):
        c = self.cases['exchange_ties']
        self.assertEqual(c['steps'][0]['after']['idle_student_ids'], [9,4,3,5])
        self.assertNotEqual(c['steps'][0]['after']['idle_student_ids'], [9,3,4,5])
        d = self.cases['divergent_keys']
        self.assertEqual(d['steps'][0]['after']['idle_student_ids'], [4,5,9,3])
        self.assertEqual(d['steps'][1]['after']['idle_student_ids'], [3,9,5,4])

    def test_native_write_set_count_and_tail_boundaries(self):
        for c in self.cases.values():
            for step in c['steps']:
                count = step['before']['idle_student_count']
                self.assertEqual(step['after']['idle_student_count'], count)
                self.assertEqual(step['after']['buffer_tail'], [-1]*(20-count))
                expected = [] if step['command'] == 55 else [(hex(IDS+2*i),2) for i in range(count)]+[(hex(MODE),1)]
                self.assertEqual([(w['address'],w['size']) for w in step['native_writes']], expected)
                self.assertEqual(sorted(step['before']['idle_student_ids']), sorted(step['after']['idle_student_ids']))

    def test_empty_single_and_unknown_command(self):
        for name, ids in [('empty', []), ('single', [3])]:
            for step in self.cases[name]['steps']:
                self.assertEqual(step['after']['idle_student_ids'], ids)
        for c in self.cases.values():
            for step in c['steps']:
                if step['command'] == 55:
                    self.assertEqual(step['before'], step['after'])
                    self.assertNotIn('0x4a8bf0', step['visited_original_addresses'])
                    self.assertEqual(step['native_writes'], [])

    def test_emulator_rejects_undeclared_command_and_invalid_members(self):
        x = WaitlistEmulator([], [])
        before = x.waiting_snapshot()
        with self.assertRaisesRegex(ValueError, 'command outside'):
            x.run_command(0)
        self.assertEqual(x.waiting_snapshot(), before)
        with self.assertRaisesRegex(ValueError, 'outside declared domain'):
            WaitlistEmulator([], [3,3])
        with self.assertRaisesRegex(ValueError, 'missing waiting profile'):
            WaitlistEmulator([], [3])

    def test_evidence_does_not_claim_live_school_or_save_authority(self):
        for key in ('school_initialized', 'interactive_school_ready', 'live_witness', 'authorizes_persistent_write'):
            self.assertFalse(self.native[key])
        self.assertIn('Starting catalogs are declared frozen replay inputs, not native boot continuity.', self.native['limitations'])


if __name__ == '__main__':
    unittest.main()
