"""Original attack admission/chase/launch plus corrupt-evidence rejection."""
from copy import deepcopy
import gzip
import json
import unittest
from tools.battle_attack_launch import corpus,charge_corpus,case,validate
from tools.battle_attack_launch_emulation import ROOT,UNIT,RECORD,AttackMachine,source_contract,sha
from tools.battle_attack_launch_verification import verify_case,verify_charge

REPORT='analysis/battle-attack-launch-source-v5-20261024.json.gz'
REPORT_SHA='df2b38f5ecd46cbdcbbba10b1e32216230281a1548db0b03aa2cc4a3ffc309de'


class AttackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw=(ROOT/REPORT).read_bytes()
        if sha(raw)!=REPORT_SHA:raise ValueError('immutable original attack corpus')
        cls.data=json.loads(gzip.decompress(raw));cls.rows={r['input']['name']:r for r in cls.data['cases']};cls.charges={r['input']['name']:r for r in cls.data['charge_cases']}

    def bad(self,edit,name='ordinary',replay=False):
        row=deepcopy(self.rows[name]);edit(row)
        with self.assertRaises(ValueError):verify_case(row,replay)

    def test_source_identity_and_exact_corpora(self):
        self.assertEqual(self.data['source_contract'],source_contract());self.assertEqual([r['input'] for r in self.data['cases']],corpus())
        self.assertEqual([r['input'] for r in self.data['charge_cases']],charge_corpus())

    def test_natural_selection_continues_same_object(self):
        r=self.rows['natural_selection_to_release'];v=verify_case(r,False)
        self.assertEqual([s['call']['entry'] for s in r['steps']],[0x475700]*11)
        self.assertEqual(r['entries']['0x47c580'],1);self.assertEqual(v['release_roots'],[7])

    def test_chase_really_changes_coordinates(self):
        for n in ('chase_east','chase_south','range_zero'):self.assertGreater(verify_case(self.rows[n],False)['moves'],0)

    def test_timer_signed_wrap_and_slow(self):
        expected={'ordinary':5,'zero_windup':2,'one_windup':3,'negative_windup':3,'slow_status7':6,'windup_short_wrap':3}
        for n,i in expected.items():self.assertEqual(verify_case(self.rows[n],False)['release_roots'],[i])

    def test_no_animation_completion_or_damage(self):
        r=self.rows['ordinary'];self.assertEqual(r['steps'][-1]['after_hex'],r['steps'][-3]['before_hex'])
        self.assertEqual(bytes.fromhex(r['steps'][-1]['after_hex'])[4],0)
        self.assertEqual(bytes.fromhex(r['steps'][0]['record_before'])[0x16:0x18],bytes.fromhex(r['steps'][-1]['record_after'])[0x16:0x18])

    def test_mp_fallback_and_abort_requests(self):
        self.assertEqual(verify_case(self.rows['mp_fallback'],False)['mp'],0)
        for n in ('dead_target','unselectable_target','both_unaffordable','excluded_actor'):self.assertEqual(verify_case(self.rows[n],False)['pending'],15)
        self.assertEqual(verify_case(self.rows['target_state1'],False)['pending'],2)

    def test_wrong_phase_rejected(self):self.bad(lambda r:r['steps'][1].__setitem__('after_hex',r['steps'][0]['after_hex']))
    def test_wrong_mp_rejected(self):self.bad(lambda r:r['steps'][-1].__setitem__('record_after','00'*256))
    def test_wrong_action_rejected(self):self.bad(lambda r:r['action_events'][1]['args'].__setitem__(1,99))
    def test_inserted_child_root_rejected(self):self.bad(lambda r:r['steps'][0]['call'].__setitem__('entry',0x477980))
    def test_missing_wait_rejected(self):self.bad(lambda r:r['steps'].pop())
    def test_false_stop_rejected(self):self.bad(lambda r:r.__setitem__('stop','animation_complete'))
    def test_readonly_candidate_corruption_rejected(self):
        def edit(r):
            rec=next(x for x in r['final'] if x['pointer']==RECORD);b=bytearray.fromhex(rec['hex']);b[0x116]^=1;rec['hex']=b.hex()
        self.bad(edit)
    def test_readonly_map_corruption_rejected(self):self.bad(lambda r:r['final'][3].__setitem__('hex','00'*r['final'][3]['bytes']))
    def test_foreign_root_abi_rejected(self):self.bad(lambda r:r['steps'][0]['call'].__setitem__('ESP_after',0))
    def test_trace_corruption_rejected_by_fresh_execution(self):self.bad(lambda r:r.__setitem__('code_trace_sha256','0'*64),replay=True)
    def test_paid_charge_fabrication_rejected(self):
        r=deepcopy(self.charges['paid_short']);r['charge']=self.charges['paid_exact']['charge']
        with self.assertRaises(ValueError):verify_charge(r,False)
    def test_unknown_input_field_rejected(self):
        c=case('bad');c['host_animation_complete']=True
        with self.assertRaises(ValueError):validate(c)
    def test_unknown_original_dependency_rejected(self):
        m=AttackMachine(case('boundary'))
        with self.assertRaisesRegex(ValueError,'undeclared original instruction'):m.code(m.uc,0x40A100,1,None)
    def test_original_code_write_rejected(self):
        m=AttackMachine(case('write_boundary'))
        with self.assertRaisesRegex(ValueError,'forbidden original write'):m.write_hook(m.uc,0,0x477980,1,0,None)
    def test_direct_child_root_rejected(self):
        m=AttackMachine(case('root_boundary'))
        with self.assertRaises(ValueError):m.call(0x477980,(UNIT,))


def add_cases():
    for c in corpus():
        def check(self,name=c['name']):verify_case(self.rows[name],False)
        setattr(AttackTests,'test_case_'+c['name'],check)
    for c in charge_corpus():
        def check(self,name=c['name']):verify_charge(self.charges[name],False)
        setattr(AttackTests,'test_helper_'+c['name'],check)


add_cases()
if __name__=='__main__':unittest.main()
