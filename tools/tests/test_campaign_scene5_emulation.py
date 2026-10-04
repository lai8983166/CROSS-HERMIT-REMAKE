import hashlib
import struct
import unittest
from unittest.mock import patch

from tools.campaign_scene5_emulation import CampaignScene5Emulator, report
from tools.campaign_scene5_fixture import fixture, NATIVE_SHA256
from tools.tactics_exit_emulation import ROOT, report_text

FIXTURE_SHA256 = 'b349bb3d0bfcd51407595f8cec02e37fd744684332e31f08d3279d9f615f79f0'


class CampaignScene5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.instances = []

        def create(**inputs):
            instance = CampaignScene5Emulator(**inputs)
            cls.instances.append(instance)
            return instance

        with patch('tools.campaign_scene5_emulation.CampaignScene5Emulator', side_effect=create):
            cls.native = report()

    def test_report_and_fixture_reexecute_byte_for_byte(self):
        raw = report_text(self.native).encode('utf-8')
        self.assertEqual(hashlib.sha256(raw).hexdigest(), NATIVE_SHA256)
        self.assertEqual((ROOT / 'analysis/campaign-scene5-v1-20261004.json').read_bytes(), raw)
        exported = report_text(fixture(self.native)).encode('utf-8')
        self.assertEqual(hashlib.sha256(exported).hexdigest(), FIXTURE_SHA256)
        self.assertEqual((ROOT / 'prototype/data/campaign_scene5_evidence.json').read_bytes(), exported)

    def test_native_condition_predicates_choose_real_subs_and_terminal_flag(self):
        image = (ROOT / 'analysis/hermit_game.exe').read_bytes()
        for case, bit, sub, caller, selector in zip(self.native['cases'], (0, 1), (11, 8),
                ('0x43390d', '0x4338f9'), (4, 3)):
            before, after = case['event_before'], case['event_after']
            self.assertEqual(before['event_bit3_0_word'], bit << 31)
            self.assertEqual([r['wrapper_index'] for r in before['units']], [247, 239])
            returns = [e for e in case['event_trace'] if 'predicate_return_va' in e]
            self.assertEqual(returns, [{'predicate_return_va': '0x433826', 'value': 0},
                {'predicate_return_va': '0x43387c', 'value': 0},
                {'predicate_return_va': '0x4338e3', 'value': bit}])
            wrapper = [e for e in case['event_trace'] if e.get('va') == '0x454af0']
            self.assertEqual(len(wrapper), 1)
            self.assertEqual(wrapper[0]['args'], [sub, sub])
            self.assertEqual(wrapper[0]['caller_return_va'], caller)
            script = next(e for e in case['event_trace'] if e.get('va') == '0x454bb0')
            self.assertEqual(script['args'], [1, 0, sub])
            self.assertEqual((after['task']['exit_flag'], after['task']['result_selector']), (1, selector))
            self.assertEqual(struct.unpack_from('<i', image, 0x60CA7C+sub*4-0x400000)[0], selector)
            call = int(caller, 16)-5
            self.assertEqual(image[call-0x400000], 0xE8)
            displacement = struct.unpack_from('<i', image, call+1-0x400000)[0]
            self.assertEqual(call+5+displacement, 0x454AF0)

    def test_same_task_vm_end_actual_state11_to_school_and_only_one_week(self):
        for case in self.native['cases']:
            # Assert END from sourced script bytes, not an opcode name.
            campaign = case['campaign']
            tactical = campaign['upstream']['commands']
            self.assertNotIn(112, [c['opcode'] for c in tactical if 'path' not in c])
            source = ROOT / 'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/SCRIPT/T0005.BIN'
            ends = [c for c in tactical if 'path' not in c and c['opcode'] == 19 and c['frame'] >= 0]
            self.assertEqual(len(ends), 1)  # Exclude preflight parsing at frame -1.
            self.assertEqual(struct.unpack_from('<H', source.read_bytes(), ends[0]['offset'])[0], 19)
            final = case['tactical_frames'][-1]
            self.assertEqual((final['transition_phase'], final['script_phase'], final['exit_flag']), (20, 6, 1))
            self.assertEqual(final['transition_function_return'], 1)
            self.assertEqual(final['finish_flags'][1], 1)
            self.assertEqual([r['state'] for r in campaign['state_requests']], [11,10,12,6,7,6,8,6,9])
            self.assertEqual(len([e for e in campaign['upstream']['week_events'] if e['va']=='0x4d3510']), 1)
            self.assertTrue(campaign['group_initialized'])
            self.assertTrue(campaign['person_resource_initialized'])
            self.assertEqual(case['round_before'], case['round_after'])
            self.assertEqual((case['round_before']['current'], case['round_before']['total']), (1,1))

    def test_native_result_inputs_and_packages_continue_from_the_selected_world(self):
        for case, grade in zip(self.native['cases'], (3,2)):
            preparation = case['preparation']
            campaign = case['campaign']
            self.assertEqual(case['state11_entry_inputs'], preparation['native_result_inputs'])
            self.assertEqual(preparation['result_summary']['grade_index'], grade)
            self.assertEqual([r['character_id'] for r in case['state11_entry_inputs']['units']], [3,4,9])
            result_before = {r['character_id']:r for r in campaign['upstream']['before_result']['characters']}
            for record in preparation['after']['characters']:
                for key in ['growth_pools','staged_package','staged_total']:
                    self.assertEqual(record[key], result_before[record['character_id']][key])
            for key in ['characters','relationships','recipient_id','global_total_511c']:
                self.assertEqual(campaign['before'][key], campaign['after'][key])
            self.assertEqual(campaign['after']['recipient_id'], 4)
        self.assertNotEqual(self.native['cases'][0]['campaign']['upstream']['before_result'],
                            self.native['cases'][1]['campaign']['upstream']['before_result'])

    def test_single_run_no_selector_injection_and_declared_authority_boundaries(self):
        for instance in self.instances:
            with self.assertRaisesRegex(RuntimeError, 'single-run'):
                instance.run_scene5_campaign('duplicate')
            with self.assertRaisesRegex(RuntimeError, 'invocation'):
                instance.request(14,8)
        for value in [False, 2, -1, 0.5]:
            with self.assertRaises(ValueError):
                CampaignScene5Emulator(event_bit=value)
        for case in self.native['cases']:
            self.assertFalse(case['declared_scene_event_invocation']['parallel_dispatcher_executed'])
            for key in ['school_initialized','interactive_school_ready','live_witness','authorizes_persistent_write']:
                self.assertFalse(case[key])


if __name__ == '__main__':
    unittest.main()
