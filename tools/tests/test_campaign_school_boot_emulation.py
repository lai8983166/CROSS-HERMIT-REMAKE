import hashlib
import json
import unittest
from unittest.mock import patch

from tools.campaign_school_boot_emulation import CampaignSchoolBootEmulator, report
from tools.campaign_school_boot_fixture import fixture, NATIVE_SHA256
from tools.tactics_exit_emulation import ROOT, report_text

FIXTURE_SHA256 = '96359d3c2fff36a97299312d70828f617c82d762b51d75b59e07e0226b727656'


class CampaignSchoolBootTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.instances = []

        def create(**inputs):
            instance = CampaignSchoolBootEmulator(**inputs)
            cls.instances.append(instance)
            return instance

        with patch('tools.campaign_school_boot_emulation.CampaignSchoolBootEmulator', side_effect=create):
            cls.native = report()

    def test_report_and_fixture_reexecute_byte_for_byte(self):
        raw = report_text(self.native).encode('utf-8')
        self.assertEqual(hashlib.sha256(raw).hexdigest(), NATIVE_SHA256)
        self.assertEqual((ROOT / 'analysis/campaign-school-boot-v1-20261004.json').read_bytes(), raw)
        exported = report_text(fixture(self.native)).encode('utf-8')
        self.assertEqual(hashlib.sha256(exported).hexdigest(), FIXTURE_SHA256)
        self.assertEqual((ROOT / 'prototype/data/campaign_school_boot_evidence.json').read_bytes(), exported)

    def test_predecessor_continues_without_reset_or_old_expected_snapshots(self):
        old = json.loads((ROOT / 'analysis/campaign-return-chain-v1-20261004.json').read_text(encoding='utf-8'))
        for case, previous in zip(self.native['cases'], [old['cases'][0], old['cases'][4]]):
            for key in ['before_result', 'after_result', 'after_chapter', 'after']:
                current = json.loads(json.dumps(case['upstream'][key]))
                current['school'].pop('school_control')
                self.assertEqual(current, previous[key])
            self.assertEqual(case['before'], case['upstream']['after'])
            self.assertEqual(case['before']['school']['school_control'],
                             case['upstream']['before_result']['school']['school_control'])
            self.assertEqual(case['state_requests'], case['upstream']['state_requests'])

    def test_full_boot_preserves_roles_history_recipient_relationships_and_unique_week(self):
        case = self.native['cases'][0]
        for checkpoint in [case['after'], *(b['after'] for b in case['boot_checkpoints'])]:
            for key in ['characters', 'relationships', 'global_total_511c', 'recipient_id',
                        'month', 'week', 'availability', 'item_flags']:
                self.assertEqual(checkpoint[key], case['before'][key])
            self.assertEqual(checkpoint['recipient_id'], 4)
            self.assertEqual(len(checkpoint['relationships']), 20)
        self.assertEqual(case['school_after']['adv_globals']['0x7e1180'], 4)
        self.assertEqual([r['state'] for r in case['state_requests']], [11, 10, 12, 6, 7, 6, 8, 6, 9])
        self.assertEqual(len([e for e in case['upstream']['week_events'] if e['va'] == '0x4d3510']), 1)
        self.assertTrue(case['group_initialized'])
        self.assertTrue(case['person_resource_initialized'])
        self.assertEqual(case['person_idle_yields'], 2)

    def test_group_clear_rankings_waiting_and_templates_are_actual_native_fields(self):
        case = self.native['cases'][0]
        after = case['after']['school']
        self.assertEqual(after['group_student_ids'], [[-1]*4 for _ in range(5)])
        self.assertEqual(after['group_student_indices'], [[-1]*4 for _ in range(5)])
        self.assertEqual(after['student_ids'], case['before']['school']['student_ids'])
        control = after['school_control']
        records = {r['character_id']: r for r in case['after']['characters']}
        values = [records[i]['attributes']+[sum(records[i]['attributes'])] for i in after['student_ids'][:4]]
        self.assertEqual(control['group_rankings'],
                         [[1+sum(other[k] > row[k] for other in values) for k in range(8)] for row in values])
        self.assertEqual(set(control['idle_student_ids']), {3, 4, 5, 9})
        levels = [records[i]['level_50'] for i in control['idle_student_ids']]
        self.assertEqual(levels, sorted(levels, reverse=True))
        self.assertEqual(control['adventure_entries'], [[], [], [[1, 1, 8, 5, 0]]])
        self.assertEqual(control['group_task_controls'], [0, 1, 1, 2, 0])
        self.assertEqual((control['person_ready'], control['person_selection']), (1, -1))

    def test_wait_blocks_boot_and_source_resources_are_hashed(self):
        wait = self.native['cases'][1]
        self.assertEqual(wait['before'], wait['after'])
        self.assertEqual(wait['boot_events'], [])
        self.assertEqual(wait['boot_checkpoints'], [])
        self.assertFalse(wait['group_initialized'])
        self.assertFalse(wait['person_resource_initialized'])
        self.assertEqual(wait['person_idle_yields'], 0)
        for case in self.native['cases']:
            for event in case['boot_events']:
                if 'path' in event:
                    path = ROOT / 'CROSS HERMIT/CROSS HERMIT' / event['path']
                    self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), event['source_sha256'])

    def test_single_run_and_interaction_authority_boundaries_stay_closed(self):
        for instance in self.instances:
            with self.assertRaisesRegex(RuntimeError, 'single-run'):
                instance.run_campaign_boot('duplicate')
        for case in self.native['cases']:
            for key in ['school_initialized', 'interactive_school_ready', 'live_witness', 'authorizes_persistent_write']:
                self.assertFalse(case[key])
        case = self.native['cases'][0]
        menu = [e for e in case['boot_events'] if e['kind'] == 'group_menu_entry_boundary']
        self.assertEqual(menu, [{'kind': 'group_menu_entry_boundary', 'va': '0x4a7c40', 'body_executed': False}])


if __name__ == '__main__':
    unittest.main()
