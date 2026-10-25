"""Natural deaths, per-faction ledgers and unmodified result-input evidence."""
from copy import deepcopy
import json,struct,unittest
from tools.battle_lethal_combat import corpus,validate,expand
from tools.battle_lethal_combat_emulation import ROOT,UNIT,TARGET,RECORD,REGIONS,LethalMachine,ALLOWED,source_contract,sha,parent
from tools.battle_lethal_combat_verification import load_case,verify_case
from tools.battle_lethal_combat_model import death_contract,result_contract,max_add

REPORT='analysis/battle-lethal-combat-source-v2-20261025.json'
REPORT_SHA='23638812d4109f487130d2992deb7a9330a9b393ed72053f107f1eacc864a803'


class LethalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw=(ROOT/REPORT).read_bytes()
        if sha(raw)!=REPORT_SHA:raise ValueError('fixed lethal source bundle')
        cls.data=json.loads(raw);cls.rows={r['name']:load_case(r) for r in cls.data['case_reports']}

    def bad(self,edit,name='player_dies_job1'):
        r=deepcopy(self.rows[name]);edit(r)
        with self.assertRaises(ValueError):verify_case(r,False)

    def test_exact_corpus_and_38_owned_regions(self):
        self.assertEqual(self.data['source_contract'],source_contract());self.assertEqual([r['input'] for r in self.rows.values()],corpus());self.assertEqual(len(REGIONS),38)

    def test_both_act_before_each_natural_death(self):
        for r in list(self.rows.values())[:4]:
            self.assertEqual({h['attacker'] for h in r['hit_sides']},{UNIT,TARGET});self.assertNotIn('request',r)
            self.assertFalse(any(f['controls'] for f in r['world_frames']))

    def test_finalization_is_explicit_same_world_handoff(self):
        for r in self.rows.values():
            self.assertEqual(r['finalization']['before'],r['world_frames'][-1]['after']);self.assertEqual(r['finalization']['call']['entry'],0x473860)

    def test_result_selector_zero_does_not_claim_victory(self):
        for r in self.rows.values():self.assertEqual(result_contract(r)['selector'],0)

    def test_player_kill_and_enemy_kill_scores_are_different(self):
        a=result_contract(self.rows['enemy_dies_job1']);b=result_contract(self.rows['player_dies_job1'])
        self.assertEqual((a['score'],a['player_kills'],a['player_contribution'],a['player_deaths']),(20,1,20,0))
        self.assertEqual((b['score'],b['player_kills'],b['player_contribution'],b['player_deaths']),(0,0,0,1))

    def test_enemy_clear_condition_is_not_death_or_win_selector(self):
        r=self.rows['neutral_living_control'];self.assertEqual(result_contract(r)['unit_condition'],2)
        self.assertTrue(all(bytes.fromhex(r['final_state'][k])[15]==1 for k in ('record','target_record')))

    def test_removal_uses_faction_specific_timeout(self):
        for name,side,timeout in [('enemy_dies_job1',0,600),('player_dies_job1',1,900)]:
            e=next(e for e in self.rows[name]['contracts'] if e['entry']==0x46BA10);u=bytes.fromhex(e['after']['units'][side])
            self.assertEqual(struct.unpack_from('<h',u,0x4FE)[0],timeout);death_contract(e)

    def test_original_threshold_and_delay_boundaries(self):
        for r in list(self.rows.values())[:4]:
            removal=next(e for e in r['contracts'] if e['entry']==0x4799C0 and e['result']==1)
            side=r['input']['victim'];u=bytes.fromhex(removal['before']['units'][side]);self.assertGreater(struct.unpack_from('<h',u,0xA)[0],70)
            s=expand(r['world_frames'][-1]['after'],r['blobs']);self.assertEqual(bytes.fromhex(s['record' if side==0 else 'target_record'])[15],4)
            self.assertEqual(r['terminal_index'],len(r['world_frames'])-2)

    def test_max_counter_preserves_old_value_on_signed_wrap(self):
        b=bytearray(struct.pack('<h',32767));max_add(b,0,1,'h');self.assertEqual(struct.unpack('<h',b)[0],32767)

    def test_driver_guard_and_call_body_remain_frozen(self):
        self.assertIs(LethalMachine.call,parent.BilateralMachine.call);self.assertIs(LethalMachine.source_code.__code__,parent.BilateralMachine.source_code.__code__)
        self.assertIs(LethalMachine.base_call.__code__,parent.BilateralMachine.base_call.__code__)

    def test_both_guards_reject_unknown_and_assertion_PC(self):
        cc=next(a for a in sorted(ALLOWED) if parent.parent.CODE[a-0x400000]==0xCC)
        for reference in (False,True):
            m=LethalMachine(corpus()[0],reference)
            for at in (0x400000,cc):
                with self.assertRaises(ValueError):m.source_code(m.uc,at,1,None)

    def test_extra_input_rejected(self):
        c=deepcopy(corpus()[0]);c['injected']=1
        with self.assertRaises(ValueError):validate(c)

    def test_invalid_victim_rejected(self):
        c=deepcopy(corpus()[0]);c['victim']=2
        with self.assertRaises(ValueError):validate(c)

    def test_external_request_rejected(self):self.bad(lambda r:r.__setitem__('request',{}))
    def test_external_control_rejected(self):self.bad(lambda r:r['world_frames'][0]['controls'].append({}))
    def test_missing_slot_rejected(self):self.bad(lambda r:r['world_frames'][0]['scanned_slots'].pop())
    def test_wrong_unit_order_rejected(self):self.bad(lambda r:r['world_frames'][0]['unit_calls'].reverse())
    def test_wrong_world_root_rejected(self):self.bad(lambda r:r['world_frames'][0]['call'].__setitem__('entry',0x475700))
    def test_wrong_terminal_rejected(self):self.bad(lambda r:r.__setitem__('terminal_index',0))
    def test_missing_extra_world_rejected(self):self.bad(lambda r:r['world_frames'].pop())
    def test_missing_HP_store_rejected(self):self.bad(lambda r:r['both_hp_writes'].pop())
    def test_wrong_HP_PC_rejected(self):self.bad(lambda r:r['both_hp_writes'][0].__setitem__('pc',0x473860))
    def test_wrong_hit_identity_rejected(self):self.bad(lambda r:r['hit_sides'][0].__setitem__('victim',UNIT))
    def test_forged_random_body_rejected(self):self.bad(lambda r:next(e for e in r['contracts'] if e['entry']==0x467E00).__setitem__('result',123))
    def test_false_death_request_rejected(self):self.bad(lambda r:next(e for e in r['contracts'] if e['entry']==0x472770).__setitem__('result',1))
    def test_wrong_removal_caller_rejected(self):self.bad(lambda r:next(e for e in r['contracts'] if e['entry']==0x46BA10).__setitem__('caller',0x12100000))
    def test_wrong_command11_args_rejected(self):self.bad(lambda r:next(e for e in r['contracts'] if e['entry']==0x475370)['args'].__setitem__(1,2))
    def test_forged_ledger_record_rejected(self):self.bad(lambda r:next(e for e in r['contracts'] if e['entry']==0x4799C0)['after']['records'].__setitem__(0,'00'*256))
    def test_forged_faction_score_rejected(self):self.bad(lambda r:next(e for e in r['contracts'] if e['entry']==0x4799C0)['after'].__setitem__('death_stats','00'*48))
    def test_wrong_finalization_root_rejected(self):self.bad(lambda r:r['finalization']['call'].__setitem__('entry',0x475700))
    def test_finalization_world_rewrite_rejected(self):self.bad(lambda r:r['finalization']['after'].__setitem__('record','00'*256))
    def test_false_result_selector_rejected(self):
        def edit(r):
            s=expand(r['finalization']['after'],r['blobs']);b=bytearray.fromhex(s['result_data']);struct.pack_into('<h',b,0x50C,1);r['finalization']['after']['result_data']=b.hex()
        self.bad(edit)
    def test_wrong_player_deaths_output_rejected(self):
        def edit(r):
            s=expand(r['finalization']['after'],r['blobs']);b=bytearray.fromhex(s['result_data']);b[0x518+0xB0+0xAE]=0;r['finalization']['after']['result_data']=b.hex()
        self.bad(edit)
    def test_forged_page_rejected(self):self.bad(lambda r:r['blobs'].__setitem__(next(iter(r['blobs'])),'ff'))
    def test_game_stub_rejected(self):self.bad(lambda r:r.__setitem__('game_function_results_stubbed',True))


def add_case(name):
    def test(self):self.assertTrue(verify_case(self.rows[name],False)['independent_function_contracts'])
    setattr(LethalTests,'test_complete_case_'+name,test)


for c in corpus():add_case(c['name'])


if __name__=='__main__':unittest.main()
