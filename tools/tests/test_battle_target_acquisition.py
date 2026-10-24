"""Original ordinary target priorities, filters and movement request handoff."""
from copy import deepcopy
import gzip
import json
import unittest
from tools.battle_target_acquisition import corpus,inputs,choose,candidate
from tools.battle_target_acquisition_emulation import ROOT,UNIT,CTRL,RECORD,COMMON,TargetMachine,validate,source_contract,sha
from tools.battle_target_acquisition_verification import verify_case

REPORT='analysis/battle-target-acquisition-source-v2-20261024.json.gz'
REPORT_SHA='4fa2dec7956d51668e49e4cab790d44a43293c4b6c7cf43bc9e9bd5f791f7d3b'


class TargetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw=(ROOT/REPORT).read_bytes()
        if sha(raw)!=REPORT_SHA:raise ValueError('immutable ordinary target source report')
        cls.report=json.loads(gzip.decompress(raw));cls.rows={r['input']['name']:r for r in cls.report['cases']}

    def bad(self,edit,name='policy_1',replay=False):
        row=deepcopy(self.rows[name]);edit(row)
        with self.assertRaises(ValueError):verify_case(row,replay)

    def test_source_identity_and_all_39_cases(self):
        self.assertEqual(self.report['source_contract'],source_contract());self.assertEqual([r['input'] for r in self.report['cases']],corpus());self.assertEqual(len(self.rows),39)
    def test_all_independent_complete_units_and_readonly_inputs(self):
        for row in self.rows.values():
            with self.subTest(case=row['input']['name']):verify_case(row,False)
    def test_fresh_original_scan_and_memory_trace(self):verify_case(self.rows['policy_1'],True)
    def test_fresh_original_dispatch_and_handoff(self):verify_case(self.rows['attack_request'],True)
    def test_all_ten_source_priorities(self):
        actual=[verify_case(self.rows['policy_'+str(p)],False)['selected_ids'][0] for p in range(1,11)]
        self.assertEqual(actual,[2,1,3,2,3,2,3,2,1,3])
    def test_duplicates_signed_unsigned_and_pixel_fraction(self):
        for a,b in ((3,5),(4,6)):self.assertEqual(self.rows['policy_'+str(a)]['steps'][0]['call']['result'],self.rows['policy_'+str(b)]['steps'][0]['call']['result'])
        self.assertEqual(verify_case(self.rows['unsigned_metric'],False)['selected_ids'],[2]);self.assertEqual(verify_case(self.rows['signed_hp'],False)['selected_ids'],[1])
        self.assertEqual(verify_case(self.rows['fixed_pixel_distance'],False)['selected_ids'],[2])
    def test_equal_priorities_keep_first_list_entry(self):
        for n in ('stable_tie','fixed_distance_tie'):self.assertEqual(verify_case(self.rows[n],False)['selected_ids'],[2])
    def test_unrecognized_priority_selects_first_without_replacement(self):
        for p in (0,11):self.assertEqual(verify_case(self.rows['unrecognized_policy_'+str(p)],False)['selected_ids'],[1])
    def test_scan_cadence_and_signed_overflow(self):
        self.assertEqual(verify_case(self.rows['cadence'],False)['selected_ids'],[None,None,1,None,None,1,None])
        self.assertEqual(verify_case(self.rows['counter_overflow'],False)['selected_ids'],[None,None])
    def test_negative_counter_reaching_zero_is_not_automatically_ready(self):
        c=deepcopy(corpus()[0]);c.update(counter=-1,interval=100)
        row=TargetMachine(c).run();v=verify_case(row,False);self.assertEqual(v['scans_ready'],0);self.assertEqual(v['selected_ids'],[None])
    def test_relation_zero_and_three_excluded_one_and_two_accepted(self):
        for relation in (0,3):self.assertEqual(verify_case(self.rows['relation_'+str(relation)],False)['selected_ids'],[None])
        for relation in (1,2):self.assertEqual(verify_case(self.rows['relation_'+str(relation)],False)['selected_ids'],[1])
        self.assertEqual(verify_case(self.rows['same_faction'],False)['selected_ids'],[None])
    def test_death_inactive_base_and_excluded_record_filters(self):
        self.assertEqual(verify_case(self.rows['filters'],False)['selected_ids'],[7]);self.assertEqual(verify_case(self.rows['base_allowed'],False)['selected_ids'],[1])
    def test_view_masks_are_original_nonbinary_payloads(self):
        data=inputs();self.assertEqual(len(data['masks']),33);self.assertIn(255,bytes.fromhex(data['masks'][0]['hex']))
        self.assertEqual(verify_case(self.rows['sight0'],False)['selected_ids'],[None]);self.assertEqual(verify_case(self.rows['sight1'],False)['selected_ids'],[1])
    def test_disabled_search_does_not_disable_movement(self):
        row=verify_case(self.rows['disabled_search_move'],False);self.assertEqual(row['requested_command'],0);self.assertGreater(row['position_changing_calls'],0)
    def test_normal_attack_packet_and_consumption(self):
        row=verify_case(self.rows['attack_request'],False);self.assertEqual((row['requested_command'],row['final_command'],row['target'],row['skill']),(6,6,1,101))
    def test_alternate_action_continues_primary_positioning_same_call(self):
        r=self.rows['alternate_target_action'];row=verify_case(r,False);self.assertEqual((row['requested_command'],row['final_command']),(29,29));self.assertGreater(r['entries']['0x476680'],0)
    def test_forced_action_retains_declared_skill_and_unfilled_target(self):
        r=verify_case(self.rows['forced_attack_method'],False);self.assertEqual((r['target'],r['skill']),(-1,101));self.assertEqual(r['requested_command'],6)
    def test_delayed_scan_and_no_target_move(self):
        self.assertEqual(len(self.rows['delayed_scan']['steps']),4)
        for name in ('move_without_enemy','move_scan_not_ready'):
            r=verify_case(self.rows[name],False);self.assertEqual(r['root_calls'],8);self.assertEqual(r['position_changing_calls'],4);self.assertFalse(r['command_consumed'])
    def test_invalid_declarations_rejected(self):
        for change in ({'policy':12},{'scope':3},{'view':33},{'interval':-1},{'counter':2147483648},{'calls':17},{'actor_faction':4},{'initial_skill':0},{'method':1}):
            c=deepcopy(corpus()[0]);c.update(change)
            with self.assertRaises(ValueError):validate(c)
    def test_candidate_capacity_and_field_bounds(self):
        for change in ({'id':9},{'metric':65536},{'hp':32768},{'faction':16},{'cell':[64,0]}):
            c=deepcopy(corpus()[0]);c['candidates'][0].update(change)
            with self.assertRaises(ValueError):validate(c)
    def test_forced_action_without_existing_skill_reaches_original_assertion(self):
        c=deepcopy(self.rows['forced_attack_method']['input']);c['initial_skill']=-1
        with self.assertRaisesRegex(ValueError,'0x424f80'):TargetMachine(c).run()
    def test_healing_admission_dependency_rejected(self):
        m=TargetMachine(corpus()[0]);m.put(RECORD+0xC,7,'H')
        with self.assertRaisesRegex(ValueError,'0x46c930'):m.call(0x47A920,(UNIT,))
    def test_full_attack_handler_remains_rejected(self):
        m=TargetMachine(self.rows['attack_request']['input'])
        m.call(0x475700,(UNIT,));m.call(0x475700,(UNIT,))
        with self.assertRaisesRegex(ValueError,'0x477980'):m.call(0x475700,(UNIT,))
    def test_candidate_record_mask_relation_and_code_writes_rejected(self):
        m=TargetMachine(corpus()[0])
        for at in (UNIT+0x520,RECORD,COMMON,CTRL+0x115AAC,0x47A920):
            with self.assertRaises(ValueError):m.write_hook(m.uc,0,at,1,0,None)
    def test_wrong_return_pointer_rejected(self):self.bad(lambda r:r['steps'][0]['call'].update(result=0))
    def test_wrong_scan_counter_rejected(self):self.bad(lambda r:r['steps'][0].update(after_hex='00'*0x520))
    def test_wrong_dispatch_root_rejected(self):self.bad(lambda r:r['steps'][0]['call'].update(entry=0x47A920),'attack_request')
    def test_wrong_consumer_root_rejected(self):self.bad(lambda r:r['consumer']['call'].update(entry=0x477980),'attack_request')
    def test_missing_consumer_rejected(self):self.bad(lambda r:r.update(consumer=None),'attack_request')
    def test_wrong_consumed_unit_rejected(self):self.bad(lambda r:r['consumer'].update(after_hex='00'*0x520),'attack_request')
    def test_wrong_coordinate_count_rejected(self):self.bad(lambda r:r.update(original_coordinate_writes=0),'move_without_enemy')
    def test_missing_owned_region_rejected(self):self.bad(lambda r:r['final'].pop())
    def test_readonly_view_corruption_rejected(self):
        def edit(r):
            p=next(v for v in r['final'] if v['pointer']==COMMON);p['hex']='00'+p['hex'][2:]
        self.bad(edit)
    def test_CPU_and_trace_corruption_rejected_by_replay(self):
        self.bad(lambda r:r['steps'][0]['call']['cpu_after'].update(EDX=17),replay=True)
        self.bad(lambda r:r.update(write_trace_sha256='0'*64),replay=True)
    def test_wrong_callee_pop_rejected(self):self.bad(lambda r:r['steps'][0]['call'].update(ESP_after=0))
    def test_no_global_damage_or_native_completion_claim(self):
        for k in ('R3_complete','R4_complete','R6_complete'):self.assertFalse(self.report[k])
        self.assertFalse(self.report['source_contract']['native_world_or_damage_complete']);self.assertFalse(self.report['source_contract']['healing_random_skill_and_full_attack_supported'])


if __name__=='__main__':unittest.main()
