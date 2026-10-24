"""World-driven melee completion, lossless state evidence and tamper rejection."""
from copy import deepcopy
import gzip
import json
import struct
import unittest
from tools.battle_world_combat import corpus,validate,expand
from tools.battle_world_combat_emulation import ROOT,UNIT,TARGET,REGIONS,CombatMachine,ALLOWED,CODE,sha,source_contract
from tools.battle_world_combat_verification import load_case,verify_case

REPORT='analysis/battle-world-combat-source-v1-20261025.json'
REPORT_SHA='81b2d2c1d8811a760fa3d76d38dec297a0e07bf0dc9c75fa139c2ec2dada39e6'


class WorldCombatTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw=(ROOT/REPORT).read_bytes()
        if sha(raw)!=REPORT_SHA:raise ValueError('fixed complete original world combat corpus')
        cls.data=json.loads(raw);cls.rows={r['name']:load_case(r) for r in cls.data['case_reports']}

    def bad(self,edit,name='ordinary',replay=False):
        r=deepcopy(self.rows[name]);edit(r)
        with self.assertRaises(ValueError):verify_case(r,replay)

    def frames(self,name='ordinary'):return self.rows[name]['world_frames']

    def test_contract_and_all_inputs(self):
        self.assertEqual(self.data['source_contract'],source_contract());self.assertEqual([r['input'] for r in self.rows.values()],corpus());self.assertEqual(len(REGIONS),37)

    def test_four_jobs_complete_through_world_updates(self):
        for name,n in [('ordinary',60),('ordinary_job2',60),('ordinary_job3',48),('ordinary_job4',48)]:
            r=self.rows[name];self.assertEqual(len(r['world_frames']),n);self.assertEqual(r['terminal_index'],n-2)
            self.assertEqual(bytes.fromhex(r['final_state']['unit'])[0x290],5);self.assertEqual(len(r['hit']),1)

    def test_only_original_world_callers_drive_commands_events_HP(self):
        for f in self.frames():
            self.assertEqual(len(f['scanned_slots']),250)
            for entry,caller in ((0x475700,0x46B7E1),(0x482A30,0x46B86D),(0x4918D0,0x46B87D),(0x493450,0x46B889)):
                self.assertEqual([c['caller'] for c in f['nested_calls'] if c['entry']==entry],[caller,caller])
        hits=[f['index'] for f in self.frames() if any(c['entry']==0x48AAE0 for c in f['nested_calls'])];self.assertEqual(hits,[20])

    def test_actor_stop_is_explicit_original_request_then_world_consumption(self):
        frames=self.frames();controls=[(i,c) for i,f in enumerate(frames) for c in f['controls']];self.assertEqual(len(controls),1)
        i,c=controls[0];self.assertEqual(i,57);self.assertEqual(c['call']['args'],[UNIT,5])
        self.assertEqual(bytes.fromhex(c['before']['unit'])[0x293],24);self.assertEqual(bytes.fromhex(c['after']['unit'])[0x292],5)
        self.assertEqual(bytes.fromhex(frames[i+1]['after']['unit'])[0x290:0x294],bytes((5,6,0,0)))

    def test_light_and_heavy_reactions_restore_then_consume_passive_command(self):
        for name,n,command in [('stagger',85,8),('heavy_stagger',115,9)]:
            frames=self.frames(name);self.assertEqual(len(frames),n)
            self.assertTrue(any(bytes.fromhex(f['after']['target'])[0x290]==command for f in frames))
            restored=[f for f in frames if bytes.fromhex(f['after']['target'])[0x292]==5];self.assertEqual(len(restored),1)
            self.assertEqual(bytes.fromhex(frames[-1]['after']['target'])[0x290:0x294],bytes((5,5,0,0)))

    def test_heavy_knockback_updates_real_occupancy(self):
        r=self.rows['heavy_stagger'];u=bytes.fromhex(r['final_state']['target']);self.assertEqual(struct.unpack_from('<i',u,0x2EC)[0],1058*65536)
        occ=bytes.fromhex(expand(r['final_state'],r['blobs'])['occupancy']);self.assertEqual((occ[(5*64+30)*2+1],occ[(5*64+33)*2+1]),(0,1))

    def test_death_extra_world_frame_advances_record_three_to_four(self):
        r=self.rows['lethal'];frames=r['world_frames'];self.assertEqual(len(frames),125)
        self.assertEqual([bytes.fromhex(f['after']['target_record'])[15] for f in frames[-2:]],[3,4])
        self.assertEqual(bytes.fromhex(frames[-1]['after']['target'])[0],1)
        self.assertEqual(frames[-1]['unit_calls'][1]['result'],1)
        self.assertEqual(struct.unpack_from('<I',bytes.fromhex(expand(frames[-1]['stages'][0]['state'],r['blobs'])['world_fields']['0x110dc30c']),0xdccd8-0xdc30c)[0],1)

    def test_current_HP_before_hit_includes_twenty_world_regenerations(self):
        for name,after in [('lethal',0),('threshold_survival',2)]:
            f=self.frames(name)[20];self.assertEqual(struct.unpack_from('<h',bytes.fromhex(f['before']['target_record']),0x16)[0],30)
            self.assertEqual(struct.unpack_from('<h',bytes.fromhex(f['after']['target_record']),0x16)[0],after)
        self.assertEqual(struct.unpack_from('<h',bytes.fromhex(self.rows['threshold_survival']['final_state']['target_record']),0x16)[0],41)

    def test_miss_and_block_are_actual_world_effect_results(self):
        self.assertEqual(self.rows['miss_roll95']['hit'][0]['kind'],0);self.assertEqual(self.rows['block_armor']['hit'][0]['kind'],4)
        for name in ('miss_roll95','block_armor'):self.assertEqual(self.rows[name]['hp_writes'],[])

    def test_lossless_pages_retain_all_250_slots(self):
        r=self.rows['ordinary'];s=expand(r['world_frames'][-1]['after'],r['blobs']);b=bytes.fromhex(s['all_unit_slots'])
        self.assertEqual(len(b),250*0x520);self.assertEqual(b[:0x520].hex(),s['unit']);self.assertEqual(b[0x520:2*0x520].hex(),s['target']);self.assertEqual(b[2*0x520:],bytes(248*0x520))

    def test_fast_and_frozen_guards_match_full_original_execution(self):
        p=ROOT/'analysis/battle-world-combat-reference-v1-20261025.json.gz';other=json.loads(gzip.decompress(p.read_bytes()))['cases'][0]
        a,b=deepcopy(self.rows['ordinary']),other;a.pop('platform');b.pop('platform');self.assertEqual(a,b)

    def test_both_guards_reject_unknown_original_PC_and_CC_padding(self):
        cc=next(at for at in sorted(ALLOWED) if CODE[at-0x400000]==0xCC)
        for reference in (False,True):
            m=CombatMachine(corpus()[0],reference_guard=reference)
            for at in (0x400000,cc):
                with self.assertRaises(ValueError):m.source_code(m.uc,at,1,None)
            self.assertEqual(m.instructions,0)

    def test_missing_frame_rejected(self):self.bad(lambda r:r['world_frames'].pop())
    def test_missing_slot_rejected(self):self.bad(lambda r:r['world_frames'][0]['scanned_slots'].pop())
    def test_wrong_unit_order_rejected(self):self.bad(lambda r:r['world_frames'][0]['unit_calls'].reverse())
    def test_standalone_HP_caller_rejected(self):self.bad(lambda r:next(c for c in r['world_frames'][0]['nested_calls'] if c['entry']==0x493450).__setitem__('caller',0x12100000))
    def test_missing_child_animation_call_rejected(self):self.bad(lambda r:r['world_frames'][0]['nested_calls'].pop(2))
    def test_wrong_world_root_rejected(self):self.bad(lambda r:r['world_frames'][0]['call'].__setitem__('entry',0x475700))
    def test_missing_control_request_rejected(self):self.bad(lambda r:r['world_frames'][57]['controls'].clear())
    def test_wrong_control_command_rejected(self):self.bad(lambda r:r['world_frames'][57]['controls'][0]['call']['args'].__setitem__(1,11))
    def test_wrong_terminal_index_rejected(self):self.bad(lambda r:r.__setitem__('terminal_index',0))
    def test_forged_page_bytes_rejected(self):self.bad(lambda r:r['blobs'].__setitem__(next(iter(r['blobs'])),'00'))
    def test_missing_referenced_page_rejected(self):self.bad(lambda r:r['blobs'].pop(r['world_frames'][0]['before']['all_unit_slots']['pages'][0]))
    def test_wrong_page_order_rejected(self):self.bad(lambda r:r['world_frames'][0]['before']['all_unit_slots']['pages'].reverse())
    def test_truncated_paged_extent_rejected(self):self.bad(lambda r:r['world_frames'][0]['before']['all_unit_slots'].__setitem__('bytes',1))
    def test_forged_full_unit_rejected(self):self.bad(lambda r:r['world_frames'][0]['unit_calls'][0]['after'].__setitem__('unit','00'*0x520))
    def test_missing_HP_store_rejected(self):self.bad(lambda r:r['hp_writes'].pop())
    def test_wrong_HP_store_PC_rejected(self):self.bad(lambda r:r['hp_writes'][0].__setitem__('pc',0x46B470))
    def test_missing_owned_region_rejected(self):self.bad(lambda r:r['final'].pop())
    def test_missing_real_TLS_leaf_rejected(self):self.bad(lambda r:r['platform']['trace'].pop())
    def test_foreign_TLS_cleanup_thread_rejected(self):self.bad(lambda r:r['platform']['cleanup'].__setitem__('thread',0))
    def test_host_result_input_rejected(self):
        c=deepcopy(corpus()[0]);c['HP']=0
        with self.assertRaises(ValueError):validate(c)
    def test_unbounded_input_rejected(self):
        c=deepcopy(corpus()[0]);c['budget']=193
        with self.assertRaises(ValueError):validate(c)
    def test_x87_tamper_rejected_by_fresh_original_world(self):
        self.bad(lambda r:r['world_frames'][0]['stages'][0]['CPU']['FP0'].__setitem__(0,1),name='ordinary_job3',replay=True)


for c in corpus():
    def check(self,name=c['name']):verify_case(self.rows[name],False)
    setattr(WorldCombatTests,'test_case_'+c['name'],check)

if __name__=='__main__':unittest.main()
