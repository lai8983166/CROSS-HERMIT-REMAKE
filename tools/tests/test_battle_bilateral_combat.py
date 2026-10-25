"""Bilateral original combat contracts, guards and evidence tamper rejection."""
from copy import deepcopy
import json
import struct
import unittest
from tools.battle_bilateral_combat import corpus,validate,expand
from tools.battle_bilateral_combat_emulation import ROOT,CTRL,UNIT,TARGET,RECORD,REGIONS,BilateralMachine,ALLOWED,source_contract,sha
from tools.battle_bilateral_combat_verification import load_case,verify_case
from tools.battle_bilateral_combat_model import apply_delta,hit_contract,scan_contract,hp_contract,regen_contract,ai_contract
from tools import battle_enemy_engagement_emulation as parent

REPORT='analysis/battle-bilateral-combat-source-v3-20261025.json'
REPORT_SHA='7ce6ef0be0d81f53fa9a4ed342252433ad6b7613cc39aa947253501710df6d02'


class BilateralTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw=(ROOT/REPORT).read_bytes()
        if sha(raw)!=REPORT_SHA:raise ValueError('fixed bilateral source bundle')
        cls.data=json.loads(raw);cls.rows={r['name']:load_case(r) for r in cls.data['case_reports']}

    def bad(self,edit,name='bilateral_job1'):
        r=deepcopy(self.rows[name]);edit(r)
        with self.assertRaises(ValueError):verify_case(r,False)

    def event(self,entry):return next(e for e in self.rows['bilateral_job1']['contracts'] if e['entry']==entry)

    def test_corpus_and_original_contract(self):
        self.assertEqual(self.data['source_contract'],source_contract());self.assertEqual([r['input'] for r in self.rows.values()],corpus());self.assertEqual(len(REGIONS),37)

    def test_both_begin_idle_with_no_selected_target(self):
        for j in range(1,5):
            r=self.rows['bilateral_job'+str(j)]
            for key in ('unit','target'):
                u=bytes.fromhex(r['bind_after'][key]);self.assertEqual(u[0x290:0x294],bytes((2,0,0,0)));self.assertEqual(struct.unpack_from('<h',u,0x4EE)[0],-1)
            self.assertNotIn('request',r);self.assertFalse(any(f['controls'] for f in r['world_frames']))

    def test_four_jobs_have_two_hits_in_each_direction(self):
        for j in range(1,5):
            r=self.rows['bilateral_job'+str(j)]
            for u in (UNIT,TARGET):self.assertGreaterEqual(sum(h['attacker']==u for h in r['hit_sides']),2)
            self.assertEqual(r['terminal_index'],len(r['world_frames'])-2)

    def test_both_records_receive_real_HP_stores(self):
        for j in range(1,5):
            r=self.rows['bilateral_job'+str(j)];self.assertEqual({w['address'] for w in r['both_hp_writes']},{RECORD+0x16,RECORD+0x116})
            self.assertEqual({w['pc'] for w in r['both_hp_writes']},{0x472658})

    def test_neutral_and_disabled_controls_have_no_hits(self):
        for name in ('mutual_neutral','both_search_disabled'):
            r=self.rows[name];self.assertFalse(r['hit']);self.assertFalse(r['both_hp_writes']);self.assertEqual(len(r['world_frames']),96)

    def test_passive_player_does_not_attack(self):
        r=self.rows['passive_player'];self.assertGreaterEqual(len(r['hit']),2);self.assertEqual({h['attacker'] for h in r['hit_sides']},{UNIT})

    def test_driver_and_guard_algorithm_frozen(self):
        self.assertIs(BilateralMachine.call,parent.EnemyMachine.call);self.assertIs(BilateralMachine.base_call,parent.EnemyMachine.base_call)
        self.assertIs(BilateralMachine.source_code.__code__,parent.EnemyMachine.source_code.__code__)

    def test_both_guards_reject_unknown_and_assertions(self):
        cc=next(at for at in sorted(ALLOWED) if parent.CODE[at-0x400000]==0xCC)
        for reference in (False,True):
            m=BilateralMachine(corpus()[0],reference)
            for at in (0x400000,cc):
                with self.assertRaises(ValueError):m.source_code(m.uc,at,1,None)
            self.assertEqual(m.instructions,0)

    def test_entry_contract_checks_both_roles(self):
        r=self.rows['bilateral_job1'];effects=[e for e in r['contracts'] if e['entry']==0x48AAE0]
        self.assertEqual({hit_contract(e)['attacker'] for e in effects},{UNIT,TARGET})

    def test_reverse_packet_uses_byte2_attacker_and_byte3_target(self):
        r=self.rows['bilateral_job1'];e=next(e for e in r['contracts'] if e['entry']==0x48AAE0 and e['args'][0]==TARGET)
        packet=bytes.fromhex(e['input_packet']);self.assertEqual(packet[:4],bytes((0,0,1,0)));self.assertEqual(hit_contract(e)['victim'],UNIT)

    def test_disabled_control_has_no_predeclared_reaction_target(self):
        r=self.rows['both_search_disabled']
        for k in ('unit','target'):
            self.assertEqual(struct.unpack_from('<h',bytes.fromhex(r['bind_after'][k]),0x4FA)[0],-1)

    def test_attack_range_alone_does_not_predict_player_reentry(self):
        events=[e for e in self.rows['bilateral_job1']['contracts'] if e['entry']==0x477980 and e['args'][0]==TARGET and bytes.fromhex(e['before']['units'][1])[0x293]==24]
        self.assertTrue(events)
        for e in events:
            self.assertEqual(bytes.fromhex(e['after']['units'][1])[0x292],15);ai_contract(e)

    def test_survival_and_clamping_rule(self):
        self.assertEqual(apply_delta(10,100,10,-39),1);self.assertEqual(apply_delta(9,100,10,-39),0);self.assertEqual(apply_delta(90,100,0,20),100)

    def test_extra_input_rejected(self):
        c=deepcopy(corpus()[0]);c['injected']=True
        with self.assertRaises(ValueError):validate(c)

    def test_non_boolean_autonomy_rejected(self):
        c=deepcopy(corpus()[0]);c['player_active']=1
        with self.assertRaises(ValueError):validate(c)

    def test_external_request_rejected(self):self.bad(lambda r:r.__setitem__('request',{}))
    def test_external_frame_control_rejected(self):self.bad(lambda r:r['world_frames'][0]['controls'].append({}))
    def test_missing_world_slot_rejected(self):self.bad(lambda r:r['world_frames'][0]['scanned_slots'].pop())
    def test_wrong_unit_order_rejected(self):self.bad(lambda r:r['world_frames'][0]['unit_calls'].reverse())
    def test_wrong_world_root_rejected(self):self.bad(lambda r:r['world_frames'][0]['call'].__setitem__('entry',0x475700))
    def test_wrong_helper_order_rejected(self):self.bad(lambda r:r['world_frames'][0]['entries'].reverse())
    def test_missing_extra_world_rejected(self):self.bad(lambda r:r['world_frames'].pop())
    def test_wrong_terminal_rejected(self):self.bad(lambda r:r.__setitem__('terminal_index',0))
    def test_missing_hit_identity_rejected(self):self.bad(lambda r:r['hit_sides'].pop())
    def test_forged_reverse_attacker_rejected(self):self.bad(lambda r:r['hit_sides'][1].__setitem__('attacker',UNIT))
    def test_missing_raw_hit_rejected(self):self.bad(lambda r:r['hit'].pop())
    def test_wrong_HP_PC_rejected(self):self.bad(lambda r:r['both_hp_writes'][0].__setitem__('pc',0x46B470))
    def test_missing_HP_store_rejected(self):self.bad(lambda r:r['both_hp_writes'].pop())
    def test_wrong_HP_value_rejected(self):self.bad(lambda r:r['both_hp_writes'][0].__setitem__('value',1000))
    def test_missing_contract_return_rejected(self):self.bad(lambda r:r['contracts'][0].pop('after'))
    def test_forged_effect_caller_rejected(self):self.bad(lambda r:next(e for e in r['contracts'] if e['entry']==0x48AAE0).__setitem__('caller',0x12100000))
    def test_forged_request_caller_rejected(self):self.bad(lambda r:next(e for e in r['contracts'] if e['entry']==0x475270).__setitem__('caller',0x12100000))
    def test_wrong_hit_math_rejected(self):self.bad(lambda r:next(e for e in r['contracts'] if e['entry']==0x48AAE0)['resolved'].__setitem__('kind',4))
    def test_wrong_scan_result_rejected(self):self.bad(lambda r:next(e for e in r['contracts'] if e['entry']==0x47A920).__setitem__('result',0))
    def test_forged_OS_input_rejected(self):self.bad(lambda r:r.__setitem__('OS_input_submitted',True))
    def test_game_stub_claim_rejected(self):self.bad(lambda r:r.__setitem__('game_function_results_stubbed',True))
    def test_forged_page_rejected(self):self.bad(lambda r:r['blobs'].__setitem__(next(iter(r['blobs'])),'ff'))
    def test_modified_readonly_source_rejected(self):self.bad(lambda r:r['final'][2].__setitem__('hex','ff'*r['final'][2]['bytes']))


def add_case_test(name):
    def test(self):self.assertTrue(verify_case(self.rows[name],False)['independent_function_contracts'])
    setattr(BilateralTests,'test_complete_case_'+name,test)


for cfg in corpus():add_case_test(cfg['name'])


if __name__=='__main__':unittest.main()
