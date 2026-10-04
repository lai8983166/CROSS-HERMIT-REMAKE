import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from tools.campaign_return_chain_emulation import CampaignReturnChainEmulator, report
from tools.campaign_return_chain_fixture import fixture, NATIVE_SHA256
from tools.tactics_exit_emulation import ROOT, report_text

FIXTURE_SHA256 = '76f2cd6ef371840db07a383f067ae8002c28602389f3bc81eec4dbb85a4c2a1e'


class CampaignReturnChainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.instances = []

        def create(**inputs):
            instance = CampaignReturnChainEmulator(**inputs)
            cls.instances.append(instance)
            return instance

        with patch('tools.campaign_return_chain_emulation.CampaignReturnChainEmulator', side_effect=create):
            cls.native = report()

    def test_native_report_and_export_reexecute_byte_for_byte(self):
        path = ROOT / 'analysis/campaign-return-chain-v1-20261004.json'
        native = report_text(self.native).encode('utf-8')
        self.assertEqual(hashlib.sha256(native).hexdigest(), NATIVE_SHA256)
        self.assertEqual(path.read_bytes(), native)
        exported = report_text(fixture(self.native)).encode('utf-8')
        self.assertEqual(hashlib.sha256(exported).hexdigest(), FIXTURE_SHA256)
        self.assertEqual((ROOT / 'prototype/data/campaign_return_chain_evidence.json').read_bytes(), exported)

    def test_actual_result_load_is_retained_without_adv_reload_or_reset(self):
        layout = json.loads((ROOT / 'prototype/data/campaign_school_layout_evidence.json').read_text(encoding='utf-8'))
        for case in self.native['cases']:
            previous = layout['cases'][0 if case['declared_inputs']['result']['confirm'] else 1]
            self.assertEqual(case['before_result'], previous['before'])
            self.assertEqual(case['after_result'], previous['after_result'])
            if case['result_requested_state'] == 12:
                self.assertIsNone(case['native_result_return_load'])
                self.assertEqual(case['resource_loads'], [])
                continue
            load = case['native_result_return_load']
            self.assertEqual((load['loader_va'], load['path'], load['next_task_state'], load['caller_return_va']),
                             ('0x4ce210', 'ch003.ybc', 7, '0x4c1c91'))
            self.assertEqual(load['before'], case['after_result'])
            self.assertEqual([r['path'] for r in case['resource_loads']].count('ch003.ybc'), 1)
            self.assertEqual(case['result_controller'], {'pending_flag': 1, 'pending_state': 6,
                'vm_active': 1, 'vm_pc': 0, 'next_task_state': 7, 'active_path': 'ch003.ybc'})
            self.assertEqual(case['result_adv_consumed_request']['pending_flag'], 1)
            self.assertIn('0x4ce210', case['visited_original_addresses'])
            self.assertIn('0x4ce260', case['visited_original_addresses'])
            for resource in case['resource_loads']:
                path = ROOT / 'CROSS HERMIT/CROSS HERMIT/DATA/ADV/DAT' / resource['path']
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), resource['source_sha256'])

    def test_one_cpu_source_requests_and_week_reach_both_school_tasks(self):
        case = self.native['cases'][0]
        self.assertEqual([r['state'] for r in case['state_requests']], [11, 10, 12, 6, 7, 6, 8, 6, 9])
        phases = {v['phase']: v for v in case['boundaries']}
        self.assertEqual(list(phases), ['week', 'new_adv', 'workroom', 'ch002_adv', 'school_dispatch'])
        self.assertEqual(phases['week']['canonical_layout'], case['after_chapter'])
        self.assertEqual(phases['week']['controller']['pending_state'], 7)
        self.assertEqual(phases['week']['controller']['vm_active'], 0)
        self.assertEqual((phases['new_adv']['canonical_layout']['month'],
                          phases['new_adv']['canonical_layout']['week']), (5, 1))
        weeks = [e for e in case['week_events'] if e['va'] == '0x4d3510']
        self.assertEqual(len(weeks), 1)
        self.assertTrue(weeks[0]['caller_return_va'].startswith('0x49f'))
        self.assertFalse(case['result_native_week'])
        self.assertTrue(case['continuation']['school_constructed'])
        self.assertEqual([t['vtable'] for t in case['continuation']['school_tasks']], ['0x5a0a40', '0x5a0c18'])
        self.assertEqual(phases['school_dispatch']['canonical_layout'], case['after'])
        self.assertEqual((case['controller']['pending_flag'], case['controller']['pending_state']), (0, 9))
        self.assertEqual([r['path'] for r in case['resource_loads']],
            ['ch003.ybc', 'chapter020.ybc', 'chapter021.ybc', 'ch001.ybc',
             'chapter022.ybc', 'chapter208.ybc', 'ch002.ybc'])
        ends = [(c['path'], c['offset']) for c in case['commands'] if c.get('path') and c['opcode'] == 19]
        self.assertEqual(ends, [('chapter021.ybc', 0x61e), ('chapter208.ybc', 0x1b0), ('ch002.ybc', 0x6d0)])

    def test_waits_do_not_manufacture_downstream_completion(self):
        waiting, key, work, fade = self.native['cases'][1:]
        self.assertEqual([r['state'] for r in waiting['state_requests']], [11, 10, 12])
        self.assertEqual(waiting['after'], waiting['after_result'])
        self.assertEqual(waiting['boundaries'], [])
        self.assertEqual(waiting['after']['availability'][5], 0)
        self.assertEqual([r['state'] for r in key['state_requests']], [11, 10, 12, 6])
        self.assertEqual(key['after']['availability'][5], 1)
        self.assertEqual(key['week_events'][-1]['character_id'], 5)  # Join unlock helper, not a whole week.
        self.assertFalse(any(e['va'] == '0x4d3510' for e in key['week_events']))
        self.assertEqual(key['controller']['vm_active'], 1)
        self.assertEqual(work['controller']['pending_state'], 8)
        self.assertEqual(work['after']['flags']['0x7a4e62'], 0)
        self.assertEqual(work['after']['flags']['0x7a55f6'], 9)
        self.assertFalse(work['continuation']['school_constructed'])
        self.assertEqual(fade['controller']['pending_state'], 6)
        self.assertEqual(fade['after']['flags']['0x7a4e62'], 1)
        self.assertEqual(fade['after']['flags']['0x7a55f6'], 11)
        self.assertFalse(fade['continuation']['school_constructed'])
        self.assertFalse(any(c.get('path') == 'ch002.ybc' and c['opcode'] == 19 for c in fade['commands']))

    def test_recipient_history_relationships_and_growth_survive_actual_adv(self):
        for case in self.native['cases']:
            before = case['after_result']
            roles = {r['character_id']: r for r in before['characters']}
            for snapshot in [case['after_chapter'], case['after'],
                             *(b['canonical_layout'] for b in case['boundaries'])]:
                self.assertEqual(snapshot['recipient_id'], 4)
                self.assertEqual(snapshot['global_total_511c'], before['global_total_511c'])
                self.assertEqual(snapshot['relationships'], before['relationships'])
                self.assertEqual(len(snapshot['relationships']), 20)
                for role in snapshot['characters']:
                    for field in ['growth_pools', 'attributes', 'staged_package', 'staged_total',
                                  'recipient_count', 'week_records', 'job_progress']:
                        self.assertEqual(role[field], roles[role['character_id']][field])
            self.assertEqual(case['school_after']['adv_globals']['0x7e1180'], 4)
            self.assertFalse(case['after']['school']['adv_globals'].get('0x7e1180'))

    def test_single_run_and_false_authority_boundaries_remain_explicit(self):
        for instance in self.instances:
            with self.assertRaisesRegex(RuntimeError, 'single-run'):
                instance.run_chain('repeat')
        for inputs in [{'confirm': 1}, {'chapter_key_ready': 0}, {'chapter_max_frames': 0}, {'continue_ready': 1}]:
            with self.assertRaises(ValueError):
                CampaignReturnChainEmulator(**inputs)
        for case in self.native['cases']:
            for key in ['school_initialized', 'live_witness', 'authorizes_persistent_write']:
                self.assertFalse(case[key])
            self.assertFalse(case['continuation']['school_initialized'])
        self.assertIn('School construction is not complete school initialization or interaction; no live/save authority.',
                      self.native['limitations'])


if __name__ == '__main__':
    unittest.main()
