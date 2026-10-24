"""Source hit/EFCT/HP, real TLS and corrupt evidence rejection."""
from copy import deepcopy
import gzip
import json
import struct
import unittest
from tools.battle_hit_damage import corpus,case,validate
from tools.battle_hit_damage_emulation import ROOT,UNIT,TARGET,RECORD,FXDATA,TLS,DAMAGE,DamageMachine,source_contract,sha
from tools.battle_hit_damage_verification import verify_case
from tools.battle_hit_damage_platform import NativeTLS

REPORT='analysis/battle-hit-damage-source-v1-20261024.json.gz'
REPORT_SHA='64f02e3ba446c86f27ea20c7fb7bbcdba1b3c870b3fd2b320a8d23b26a7f4a81'


class DamageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw=(ROOT/REPORT).read_bytes()
        if sha(raw)!=REPORT_SHA:raise ValueError('immutable original hit/HP corpus')
        cls.data=json.loads(gzip.decompress(raw));cls.rows={r['input']['name']:r for r in cls.data['cases']}

    def value(self,n):return verify_case(self.rows[n],False)
    def bad(self,edit,name='ordinary',replay=False):
        r=deepcopy(self.rows[name]);edit(r)
        with self.assertRaises(ValueError):verify_case(r,replay)

    def test_fixed_sources_and_all_cases(self):
        self.assertEqual(self.data['source_contract'],source_contract());self.assertEqual([r['input'] for r in self.data['cases']],corpus());self.assertEqual(len(self.rows),34)
    def test_ordinary_four_jobs_reach_actual_HP(self):
        for n in ('ordinary','ordinary_job2','ordinary_job3','ordinary_job4'):
            r=self.value(n);self.assertEqual((r['raw_hit'],r['damage32'],r['delta16'],r['hp_after']),(1,39,-39,61));self.assertTrue(r['HP_written'])
    def test_all_five_hit_classes(self):self.assertEqual([self.value(n)['raw_hit'] for n in ('miss_roll95','ordinary','stagger','heavy_stagger','block_armor')],[0,1,2,3,4])
    def test_zero_evasion_is_not_automatic_critical_or_roll95_miss(self):
        for n in ('zero_evasion_normal','zero_evasion_roll95_hit'):self.assertEqual((self.value(n)['raw_hit'],self.value(n)['hp_after']),(1,61))
    def test_roll94_95_and_forced_roll4(self):
        self.assertEqual(self.value('roll94_hit')['raw_hit'],1);self.assertEqual(self.value('roll95_high_accuracy_miss')['raw_hit'],0)
        self.assertEqual(self.value('forced_roll4_low_accuracy')['raw_hit'],3);self.assertEqual(self.value('roll5_normal')['raw_hit'],1)
    def test_zero_damage_normal_blocks_critical_still_staggers(self):
        self.assertFalse(self.value('block_armor')['HP_written']);r=self.value('critical_exact_zero');self.assertTrue(r['HP_written']);self.assertEqual((r['raw_hit'],r['damage32'],r['hp_after']),(3,0,100))
    def test_critical_negative_damage_minimum_one(self):self.assertEqual((self.value('critical_negative_minimum')['damage32'],self.value('critical_negative_minimum')['hp_after']),(1,99))
    def test_mental_thresholds_are_strict(self):
        self.assertEqual(self.value('mental_equal')['raw_hit'],1);self.assertEqual(self.value('mental_triple_equal')['raw_hit'],2)
    def test_attacking_target_changes_reaction_not_damage(self):
        r=self.value('attacking_target');self.assertEqual((r['raw_hit'],r['event_hit'],r['hp_after'],r['reaction_request']),(3,1,61,0))
    def test_short_packet_wrap_can_heal(self):
        r=self.value('short_wrap_heals');self.assertGreater(r['damage32'],65535);self.assertGreater(r['delta16'],0);self.assertGreater(r['hp_after'],r['hp_before'])
    def test_short_delta_minus32768(self):self.assertEqual(self.value('short_delta_overflow')['delta16'],-32768)
    def test_HP_zero_is_not_declared_death(self):
        for n in ('lethal','exact_hp_zero'):
            r=self.rows[n];self.assertEqual(self.value(n)['hp_after'],0);self.assertEqual(bytes.fromhex(r['final_state']['target'])[0x290],2);self.assertEqual(bytes.fromhex(r['final_state']['target_record'])[15],1)
    def test_unsigned_survival_threshold(self):
        for n in ('threshold_survival','threshold_below_hp'):self.assertEqual(self.value(n)['hp_after'],1)
        for n in ('threshold_unmet','threshold_unsigned_high'):self.assertEqual(self.value(n)['hp_after'],0)
    def test_HP_clamps_declared_capacity(self):self.assertEqual(self.value('hp_above_capacity')['hp_after'],50)
    def test_original_battle_RNG_varies_without_supplied_rolls(self):
        self.assertEqual(self.value('power_spread')['battle_draws'],3);self.assertEqual(self.value('ordinary')['battle_draws'],2);self.assertEqual(self.value('miss_roll95')['battle_draws'],1)
    def test_original_CRT_and_real_TLS_leaves(self):
        r=self.value('ordinary');self.assertEqual((r['CRT_draws'],r['actual_API_leaves']),(2,6));self.assertTrue(self.rows['ordinary']['platform']['cleanup']['actual_free'])
    def test_real_TLS_rejects_foreign_guest_slot_and_releases(self):
        p=NativeTLS(TLS)
        try:
            with self.assertRaises(ValueError):p.leaf('TlsGetValue',[999])
        finally:self.assertTrue(p.close()['actual_free'])
    def test_original_damage_pool_exhaustion_rejected_and_TLS_closed(self):
        m=DamageMachine(case('exhausted'))
        for i in range(512):m.put(DAMAGE+i*8,128,'B')
        with self.assertRaisesRegex(ValueError,'undeclared original instruction'):m.run()
        self.assertTrue(m.native.closed)
    def test_wrong_final_HP_rejected(self):self.bad(lambda r:r['consume']['hp']['after'].__setitem__('target_record','00'*256))
    def test_wrong_hit_class_rejected(self):self.bad(lambda r:r['consume']['hit'][0].__setitem__('kind',3))
    def test_wrong_battle_seed_rejected(self):self.bad(lambda r:r['consume']['hit'][0].__setitem__('seed',0))
    def test_wrong_damage_queue_rejected(self):self.bad(lambda r:r['consume']['damage']['after'].__setitem__('damage_pool','00'*4096))
    def test_forged_HP_write_PC_rejected(self):self.bad(lambda r:r['hp_writes'][0].__setitem__('pc',0x48AC90))
    def test_effect_root_injected_rejected(self):self.bad(lambda r:r['consume']['damage']['call'].__setitem__('entry',0x4919F0))
    def test_broken_continuous_CPU_rejected(self):self.bad(lambda r:r['consume']['continuation']['cpu_before'].__setitem__('EIP',0x48AC90))
    def test_fake_TLS_result_rejected(self):self.bad(lambda r:r['platform']['trace'][1].__setitem__('value',TLS+4))
    def test_cross_thread_TLS_cleanup_rejected(self):self.bad(lambda r:r['platform']['cleanup'].__setitem__('thread',0))
    def test_missing_real_API_leaf_rejected(self):self.bad(lambda r:r['platform']['trace'].pop())
    def test_readonly_EFCT_corruption_rejected(self):
        def edit(r):
            p=next(x for x in r['final'] if x['pointer']==FXDATA);b=bytearray.fromhex(p['hex']);b[40]^=1;p['hex']=b.hex()
        self.bad(edit)
    def test_extraneous_owner_region_rejected(self):self.bad(lambda r:r['final'].pop())
    def test_CRT_seed_tamper_rejected(self):self.bad(lambda r:r['consume']['damage']['after'].__setitem__('CRT_seed',0))
    def test_host_supplied_damage_input_rejected(self):
        c=case('bad');c['damage_result']=39
        with self.assertRaises(ValueError):validate(c)
    def test_unknown_death_body_rejected(self):
        m=DamageMachine(case('death_boundary'))
        with self.assertRaisesRegex(ValueError,'undeclared original instruction'):m.code(m.uc,0x472770,1,None)
    def test_fresh_ordinary_all_memory_CPU_and_trace(self):verify_case(self.rows['ordinary'],True)
    def test_fresh_wrap_healing_all_memory_CPU_and_trace(self):verify_case(self.rows['short_wrap_heals'],True)
    def test_x87_trace_tamper_rejected_by_fresh_execution(self):self.bad(lambda r:r['consume']['continuation']['cpu_after']['FP0'].__setitem__(0,1),replay=True)


for c in corpus():
    def check(self,name=c['name']):verify_case(self.rows[name],False)
    setattr(DamageTests,'test_case_'+c['name'],check)

if __name__=='__main__':unittest.main()
