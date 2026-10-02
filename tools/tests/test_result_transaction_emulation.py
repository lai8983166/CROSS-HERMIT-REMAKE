"""Joint native task snapshots prove role→week order and immutable provenance."""
import hashlib
import importlib.util
import json
import struct
import unittest

HAS_UNICORN = importlib.util.find_spec('unicorn') is not None
if HAS_UNICORN:
    from tools.result_transaction_emulation import report, ResultTransactionEmulator
    from tools.result_transaction_fixture import fixture, REPORT, REPORT_SHA256
    from tools.tactics_exit_emulation import ROOT, SOURCE, report_text


@unittest.skipUnless(HAS_UNICORN, 'requires tools/requirements-audit.txt')
class ResultTransactionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = report()
        cls.cases = {c['name']: c for c in cls.report['cases']}

    def test_joint_native_report_reexecutes_byte_for_byte(self):
        self.assertEqual(REPORT.read_text(encoding='utf-8'), report_text(self.report))
        self.assertEqual(hashlib.sha256(REPORT.read_bytes()).hexdigest(), REPORT_SHA256)
        self.assertNotIn(b'\r', REPORT.read_bytes())

    def test_same_task_instance_completes_roles_then_all_week_helpers(self):
        c = self.cases['special_complete_week']
        self.assertEqual([e['state'] for e in c['dispatch_events'] if e['kind'] == 'state_request'], [11, 10, 12, 6])
        self.assertFalse(c['bounded_stop'])
        self.assertEqual(c['week_events'][0], {'va': '0x4d3510', 'caller_return_va': '0x4c1c5d'})
        self.assertEqual([e['va'] for e in c['week_events']], ['0x4d3510']+['0x4d3aa0']*3
            +['0x4d31f0', '0x4d34a0']+['0x4d33a0']*3)
        before, entry, after = c['before'], c['before_week'], c['after']
        self.assertEqual((entry['month'], entry['week']), (15, 4))
        self.assertEqual((after['month'], after['week']), (15, 5))
        self.assertEqual(entry['recipient_id'], 4)
        for original, applied, final in zip(before['characters'], entry['characters'], after['characters']):
            self.assertNotEqual(original['growth_pools'], applied['growth_pools'])
            self.assertEqual(applied['growth_pools'], final['growth_pools'])
            self.assertEqual(applied['job_progress'], 1)
            self.assertEqual(applied['recipient_count'], int(applied['character_id'] == 4))
            self.assertEqual(bytes.fromhex(applied['week_records_hex'])[174:177], b'\x02\x05\x07')
            self.assertEqual(applied['unlock_flags'], [0]*30)
            self.assertEqual(final['unlock_flags'][:10], [1]*10)
        self.assertEqual(entry['characters'][0]['skill_statuses'][:2], [6, 6])
        self.assertEqual(after['characters'][0]['skill_statuses'][:2], [6, 5])
        self.assertEqual(entry['item_flags'][:5], [0x301, 0x307, 0x407, 0x40B, 0x205])
        self.assertEqual(after['item_flags'][:5], [0x101, 0x307, 0x107, 0x10B, 0x205])
        image = SOURCE.read_bytes()
        call = 0x4C1C58
        at = call-0x400000
        self.assertEqual(image[at], 0xE8)
        self.assertEqual(call+5+struct.unpack_from('<i', image, at+1)[0], 0x4D3510)

    def test_other_branches_never_consume_week_side_effects(self):
        for name, c in self.cases.items():
            if name == 'special_complete_week':
                continue
            self.assertIsNone(c['before_week'])
            self.assertEqual(c['week_events'], [])
            self.assertFalse(c['native_week_body_executed'])
            for key in ('month', 'week', 'flags', 'availability', 'item_flags'):
                self.assertEqual(c['before'][key], c['after'][key])
            for b, a in zip(c['before']['characters'], c['after']['characters']):
                for key in ('unlock_flags', 'equipped_items', 'equipped_skills'):
                    self.assertEqual(b[key], a[key])
        self.assertEqual(self.cases['ordinary_confirm']['requested_state'], 6)
        self.assertEqual(self.cases['ordinary_unconfirmed']['requested_state'], 12)
        self.assertEqual(self.cases['mvp_boundary_busy']['requested_state'], 12)
        self.assertEqual(self.cases['mode1_flag0']['requested_state'], 15)
        self.assertEqual(self.cases['mode1_flag1']['requested_state'], 13)

    def test_complete_snapshots_include_slot0_and_preserve_nonparticipants(self):
        for c in self.report['cases']:
            for snapshot in (c['before'], c['after']):
                self.assertEqual(len(snapshot['relationships']), 12)
                self.assertEqual(len(snapshot['availability']), 45)
                self.assertEqual(len(snapshot['item_flags']), 360)
                for character in snapshot['characters']:
                    self.assertEqual(len(character['job_progress_values']), 31)
                    self.assertEqual(len(character['unlock_flags']), 30)
                    self.assertEqual(len(character['equipped_items']), 8)
            for key in ('nonparticipant_character_sha256', 'nonparticipant_package_hex'):
                self.assertEqual(c['before'][key], c['after'][key])
            self.assertFalse(c['live_witness'])
            self.assertFalse(c['authorizes_persistent_write'])
            self.assertFalse(c['school_task_executed'])

    def test_joint_fixture_and_school_requests_have_native_provenance(self):
        f = fixture()
        path = ROOT / 'prototype/data/result_transaction_evidence.json'
        self.assertEqual(path.read_text(encoding='utf-8'), report_text(f))
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
            'f4ed8cb1f35e4ef7a22737099562d7cbaea8157593a8793c6daaa57d0f630be6')
        self.assertEqual(f['cases'][-1]['expected_school_script'],
                         [{'path': 'Data\\Adv\\dat\\CH003.ybc', 'subroutine': 18}])
        self.assertEqual(f['cases'][0]['expected_school_script'],
                         [{'path': 'Data\\Adv\\dat\\CH003.ybc', 'subroutine': 7}])
        self.assertEqual(f['cases'][3]['expected_school_script'], [])
        self.assertEqual(f['cases'][-1]['expected_before_week']['characters'][1]['recipient_count'], 1)
        self.assertEqual(f['source_role_rules_report_sha256'],
            '3f83ad1337309c70e1f9154569a7f9267ef205bcdf7a83e4d8ff538b6c03385f')
        self.assertEqual(f['source_week_rules_report_sha256'],
            'f4d954f44de9b0c95a4747e8a92bbb0c55a42f047c4123ca20ec28a9019a2364')
        self.assertFalse(f['authorizes_persistent_write'])

    def test_undeclared_mode_inputs_reject(self):
        for kwargs in ({'mode': 2}, {'mode': 0.5}, {'result_flag': 2}):
            with self.assertRaises(ValueError):
                ResultTransactionEmulator(**kwargs)


if __name__ == '__main__':
    unittest.main()
