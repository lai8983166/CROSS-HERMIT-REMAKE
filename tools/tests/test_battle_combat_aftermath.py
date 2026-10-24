"""Whole original unit follow-up state and tampered evidence rejection."""
from copy import deepcopy
import gzip
import json
import struct
import unittest
from tools.battle_combat_aftermath import corpus,validate
from tools.battle_combat_aftermath_emulation import ROOT,UNIT,TARGET,RECORD,REGIONS,source_contract,sha
from tools.battle_combat_aftermath_verification import verify_case

REPORT='analysis/battle-combat-aftermath-source-v1-20261024.json.gz'
REPORT_SHA='727a2c3c0c77f831f9de86e59863256449a044a39cd1bad9b0823ea07f07be33'


class AftermathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw=(ROOT/REPORT).read_bytes()
        if sha(raw)!=REPORT_SHA:raise ValueError('fixed original whole-unit aftermath evidence')
        cls.data=json.loads(gzip.decompress(raw));cls.rows={r['input']['name']:r for r in cls.data['cases']}

    def bad(self,edit,name='lethal',replay=False):
        r=deepcopy(self.rows[name]);edit(r)
        with self.assertRaises(ValueError):verify_case(r,replay)

    def test_original_contract_and_all_declared_cases(self):
        self.assertEqual(self.data['source_contract'],source_contract());self.assertEqual([r['input'] for r in self.data['cases']],corpus())
        self.assertEqual((len(self.rows),len(REGIONS)),(23,35))

    def test_actual_unit_update_writes_attack_completion(self):
        r=self.rows['ordinary'];steps=[s for s in r['consume']['aftermath'] if s['unit']==UNIT]
        self.assertEqual(len(steps),37)
        # The phase22 command sees the preceding update's completion flag.
        self.assertEqual(bytes.fromhex(steps[30]['after']['unit'])[4],1)
        self.assertEqual(bytes.fromhex(steps[30]['after']['unit'])[0x293],22)
        self.assertEqual(bytes.fromhex(steps[31]['after']['unit'])[0x293],23)
        self.assertEqual(bytes.fromhex(steps[-1]['after']['unit'])[0x293],24)
        self.assertTrue(any(w['pc']==0x46B80F and w['address']==UNIT+4 for w in r['lifecycle_writes']))

    def test_two_reactions_restore_original_saved_command(self):
        for n,command,updates in (('stagger',8,62),('heavy_stagger',9,92)):
            steps=[s for s in self.rows[n]['consume']['aftermath'] if s['unit']==TARGET]
            self.assertEqual(len(steps),updates);self.assertEqual(bytes.fromhex(steps[0]['after']['target'])[0x290],command)
            last=bytes.fromhex(steps[-1]['after']['target']);self.assertEqual(last[0x290:0x294],bytes((2,0,2,0)));self.assertEqual(last[0x2A6],0)

    def test_heavy_reaction_moves_and_updates_occupancy(self):
        r=self.rows['heavy_stagger'];before=bytes.fromhex(r['consume']['hp']['after']['target']);after=bytes.fromhex(r['final_state']['target'])
        # Phase0 starts the action and increments the source timer to1, so the
        # displacement table's index0 is never applied in this full update flow.
        self.assertEqual(struct.unpack_from('<i',after,0x2EC)[0]-struct.unpack_from('<i',before,0x2EC)[0],82*65536)
        occ=bytes.fromhex(r['final_state']['occupancy']);self.assertEqual(occ[(5*64+30)*2+1],0);self.assertEqual(occ[(5*64+33)*2+1],1)

    def test_death_is_requested_after_first_unit_update(self):
        r=self.rows['lethal'];hp=r['consume']['hp']['after'];self.assertEqual(struct.unpack_from('<h',bytes.fromhex(hp['target_record']),0x16)[0],0)
        self.assertEqual(bytes.fromhex(hp['target'])[0x292],0)
        steps=[s for s in r['consume']['aftermath'] if s['unit']==TARGET]
        self.assertEqual(bytes.fromhex(steps[0]['after']['target'])[0x292],13)
        self.assertEqual(bytes.fromhex(steps[1]['after']['target'])[0x290],13)
        self.assertEqual(steps[-1]['call']['result'],1)

    def test_death_removes_combat_occupancy_but_keeps_used_slot(self):
        r=self.rows['lethal'];u=bytes.fromhex(r['final_state']['target']);rec=bytes.fromhex(r['final_state']['target_record'])
        self.assertEqual((u[0],u[0x290],rec[15]),(1,11,3));self.assertEqual(u[0x4E9:0x4EB],b'\xff\xff')
        self.assertEqual(bytes.fromhex(r['final_state']['occupancy'])[(5*64+30)*2+1],0)

    def test_survival_threshold_does_not_enter_death_command(self):
        r=self.rows['threshold_survival'];self.assertEqual(struct.unpack_from('<h',bytes.fromhex(r['consume']['hp']['after']['target_record']),0x16)[0],1)
        self.assertEqual(bytes.fromhex(r['final_state']['target_record'])[15],1)
        self.assertFalse(any(0x4799C0 in s['entries'] for s in r['consume']['aftermath']))

    def test_signed_statistics_skip_overflow_and_accept_last_increment(self):
        for n,which,off,fmt,expected in (
            ('kill_short_saturated','record',0xAA,'h',32767),('kill_short_last_increment','record',0xAA,'h',32767),
            ('points_short_saturated','record',0xAC,'h',32760),('points_short_last_increment','record',0xAC,'h',32767),
            ('death_byte_saturated','target_record',0xAE,'b',127),('death_byte_last_increment','target_record',0xAE,'b',127),
            ('score_short_saturated','world_stats',0x800,'h',32760)):
            self.assertEqual(struct.unpack_from('<'+fmt,bytes.fromhex(self.rows[n]['final_state'][which]),off)[0],expected)

    def test_region_short_counter_wraps_instead_of_saturating(self):
        r=self.rows['region_short_wrap'];self.assertEqual(struct.unpack_from('<h',bytes.fromhex(r['final_state']['world_stats']),0)[0],-32732)

    def test_zero_regeneration_interval_is_observable(self):
        self.assertEqual(struct.unpack_from('<h',bytes.fromhex(self.rows['ordinary']['final_state']['target_record']),0x16)[0],62)
        self.assertEqual(struct.unpack_from('<h',bytes.fromhex(self.rows['heavy_stagger']['final_state']['target_record']),0x16)[0],100)
        self.assertEqual(struct.unpack_from('<h',bytes.fromhex(self.rows['lethal']['final_state']['target_record']),0x16)[0],0)

    def test_voice_random_draw_executes_before_empty_sound_device_gate(self):
        r=self.rows['ordinary'];self.assertEqual(len(r['platform']['trace']),9);self.assertEqual(r['entries']['0x570fe0'],3)

    def test_visibility_uses_real_nonbinary_mask_maxima(self):
        v=bytes.fromhex(self.rows['ordinary']['final_state']['visible']);self.assertTrue({95,143,223,255}.issubset(set(v)))
        self.assertEqual(v,bytes.fromhex(self.rows['ordinary']['final_state']['seen']))

    def test_missing_full_unit_update_rejected(self):self.bad(lambda r:r['consume']['aftermath'].pop())
    def test_wrong_update_order_rejected(self):self.bad(lambda r:r['consume']['aftermath'][0].__setitem__('unit',TARGET))
    def test_forged_unit_root_rejected(self):self.bad(lambda r:r['consume']['aftermath'][0]['call'].__setitem__('entry',0x475700))
    def test_forged_completion_flag_rejected(self):self.bad(lambda r:r['consume']['aftermath'][0]['after'].__setitem__('unit','00'*0x520))
    def test_forged_death_statistic_rejected(self):self.bad(lambda r:r['consume']['aftermath'][3]['after'].__setitem__('record','00'*256))
    def test_forged_occupancy_rejected(self):self.bad(lambda r:r['final_state'].__setitem__('occupancy','00'*0x3000))
    def test_forged_visibility_rejected(self):self.bad(lambda r:r['final_state'].__setitem__('visible','00'*0x2000))
    def test_missing_actual_lifecycle_store_rejected(self):self.bad(lambda r:r['lifecycle_writes'].pop())
    def test_forged_HP_store_PC_rejected(self):self.bad(lambda r:r['hp_writes'][0].__setitem__('pc',0x46B760))
    def test_missing_actual_TLS_leaf_rejected(self):self.bad(lambda r:r['platform']['trace'].pop())
    def test_foreign_cleanup_thread_rejected(self):self.bad(lambda r:r['platform']['cleanup'].__setitem__('thread',0))
    def test_missing_owner_region_rejected(self):self.bad(lambda r:r['final'].pop())
    def test_host_result_input_rejected(self):
        c=deepcopy(corpus()[0]);c['dead']=True
        with self.assertRaises(ValueError):validate(c)

    def test_x87_tamper_rejected_by_fresh_source(self):
        self.bad(lambda r:r['consume']['aftermath'][0]['call']['cpu_after']['FP0'].__setitem__(0,1),name='ordinary',replay=True)


for c in corpus():
    def check(self,name=c['name']):verify_case(self.rows[name],False)
    setattr(AftermathTests,'test_case_'+c['name'],check)

if __name__=='__main__':unittest.main()
