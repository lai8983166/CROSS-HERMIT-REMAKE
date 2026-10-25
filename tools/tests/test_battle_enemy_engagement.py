"""Autonomous enemy decisions, repeated world combat and evidence rejection."""
from copy import deepcopy
import gzip
import json
import struct
import unittest
from tools.battle_enemy_engagement import corpus,validate,expand
from tools.battle_enemy_engagement_emulation import ROOT,CTRL,UNIT,TARGET,REGIONS,EnemyMachine,ALLOWED,CODE,sha,source_contract
from tools.battle_enemy_engagement_verification import load_case,verify_case

REPORT='analysis/battle-enemy-engagement-source-v1-20261025.json'
REPORT_SHA='2c0c0f317d8318128a9511f3d99dbfbba41950abe81376ab9ea71f1c79f90520'


class EnemyEngagementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw=(ROOT/REPORT).read_bytes()
        if sha(raw)!=REPORT_SHA:raise ValueError('fixed original enemy engagement corpus')
        cls.data=json.loads(raw);cls.rows={r['name']:load_case(r) for r in cls.data['case_reports']}

    def bad(self,edit,name='enemy_job1',replay=False):
        r=deepcopy(self.rows[name]);edit(r)
        with self.assertRaises(ValueError):verify_case(r,replay)

    def frames(self,name='enemy_job1'):return self.rows[name]['world_frames']

    def test_contract_and_all_inputs(self):
        self.assertEqual(self.data['source_contract'],source_contract());self.assertEqual([r['input'] for r in self.rows.values()],corpus());self.assertEqual(len(REGIONS),37)

    def test_enemy_starts_idle_without_selected_target_or_skill(self):
        for r in self.rows.values():
            s=r['bind_after'];u=bytes.fromhex(s['unit'])
            self.assertEqual((bytes.fromhex(s['record'])[0xA4],bytes.fromhex(s['target_record'])[0xA4]),(4,0))
            self.assertEqual(u[0x290:0x294],bytes((2,0,0,0)))
            self.assertEqual(struct.unpack_from('<h',u,0x4EE)[0],-1);self.assertEqual(struct.unpack_from('<h',u,0x4F2)[0],-1)
            self.assertNotIn('request',r);self.assertFalse(any(f['controls'] for f in r['world_frames']))

    def test_four_jobs_finish_two_rounds_and_next_original_replan(self):
        for j,n in ((1,162),(2,162),(3,138),(4,138)):
            r=self.rows['enemy_job'+str(j)];self.assertEqual(len(r['world_frames']),n);self.assertEqual(r['completed_rounds'],2);self.assertEqual(len(r['hit']),2)
            before=bytes.fromhex(r['world_frames'][-2]['after']['unit']);after=bytes.fromhex(r['world_frames'][-1]['after']['unit'])
            self.assertEqual((before[0x290],before[0x293],before[0x292]),(6,24,0));self.assertEqual(after[0x292],15)
            self.assertEqual(struct.unpack_from('<h',after,0x4EE)[0],-1);self.assertEqual(struct.unpack_from('<h',after,0x4F2)[0],-1)

    def test_idle_decision_guard_attack_replan_callers_are_original(self):
        requests=[(f['index'],c['caller'],c['args'][1]) for f in self.frames() for c in f['ai_calls'] if c['entry']==0x475270]
        self.assertEqual(requests,[(39,0x4763AA,15),(40,0x47654C,19),(41,0x4778E2,6),(100,0x4786C5,15),(101,0x47654C,19),(102,0x4778E2,6),(161,0x4786C5,15)])
        self.assertEqual([f['index'] for f in self.frames() if any(c['entry']==0x48AAE0 for c in f['nested_calls'])],[62,123])

    def test_neutral_relation_and_disabled_search_stay_on_guard(self):
        for name in ('neutral_relation','search_disabled'):
            r=self.rows[name];self.assertEqual(len(r['world_frames']),96);self.assertEqual(r['hit'],[]);self.assertEqual(r['hp_writes'],[])
            self.assertEqual([c['args'][1] for f in self.frames(name) for c in f['ai_calls'] if c['entry']==0x475270],[15,19])
            self.assertEqual(bytes.fromhex(r['final_state']['unit'])[0x290],19)

    def test_player_HP_is_applied_twice_with_world_regeneration(self):
        r=self.rows['enemy_job1'];writes=r['hp_writes'];self.assertEqual([w['value'] for w in writes],[v for _ in range(2) for v in range(961,1001)])
        self.assertEqual(struct.unpack_from('<h',bytes.fromhex(r['final_state']['target_record']),0x16)[0],1000)
        self.assertEqual([h['draws'] for h in r['hit']],[40,42])

    def test_player_popup_and_voice_randoms_follow_changed_faction(self):
        f=self.frames()[62];after=f['unit_calls'][1]['after'];pool=bytes.fromhex(expand(after,self.rows['enemy_job1']['blobs'])['popup_pool'])
        self.assertEqual(pool[1],0);self.assertEqual(after['CRT_seed'],415139642)
        self.assertEqual(len(self.rows['enemy_job1']['platform']['trace']),18)

    def test_all_250_slots_and_ordered_whole_unit_children_retained(self):
        r=self.rows['enemy_job1'];s=expand(r['world_frames'][-1]['after'],r['blobs']);b=bytes.fromhex(s['all_unit_slots'])
        self.assertEqual(len(b),250*0x520);self.assertEqual(b[:0x520].hex(),s['unit']);self.assertEqual(b[0x520:0xA40].hex(),s['target']);self.assertEqual(b[0xA40:],bytes(248*0x520))
        for f in self.frames():
            self.assertEqual(f['scanned_slots'],[UNIT+j*0x520 for j in range(250)])
            self.assertEqual([c['caller'] for c in f['nested_calls'] if c['entry']==0x475700],[0x46B7E1,0x46B7E1])

    def test_fast_and_frozen_guards_match_full_enemy_execution(self):
        p=ROOT/'analysis/battle-enemy-engagement-reference-v1-20261025.json.gz';other=json.loads(gzip.decompress(p.read_bytes()))['cases'][0]
        a,b=deepcopy(self.rows['enemy_job3']),other;a.pop('platform');b.pop('platform');self.assertEqual(a,b)

    def test_both_guards_reject_unknown_PC_and_original_assertion(self):
        cc=next(at for at in sorted(ALLOWED) if CODE[at-0x400000]==0xCC)
        for reference in (False,True):
            m=EnemyMachine(corpus()[0],reference_guard=reference)
            for at in (0x400000,cc):
                with self.assertRaises(ValueError):m.source_code(m.uc,at,1,None)
            self.assertEqual(m.instructions,0)

    def test_external_attack_request_rejected(self):self.bad(lambda r:r.__setitem__('request',{}))
    def test_external_stop_request_rejected(self):self.bad(lambda r:r['world_frames'][99]['controls'].append({}))
    def test_missing_idle_timeout_request_rejected(self):self.bad(lambda r:r['world_frames'][39]['ai_calls'].pop(2))
    def test_forged_enemy_AI_caller_rejected(self):self.bad(lambda r:next(c for c in r['world_frames'][41]['ai_calls'] if c['entry']==0x475270).__setitem__('caller',0x12100000))
    def test_forged_selected_unit_rejected(self):self.bad(lambda r:next(c for c in r['world_frames'][41]['ai_calls'] if c['entry']==0x47C580)['args'].__setitem__(1,UNIT))
    def test_missing_second_attack_rejected(self):self.bad(lambda r:r['hit'].pop())
    def test_missing_replan_frame_rejected(self):self.bad(lambda r:r['world_frames'].pop())
    def test_wrong_completed_rounds_rejected(self):self.bad(lambda r:r.__setitem__('completed_rounds',1))
    def test_wrong_terminal_rejected(self):self.bad(lambda r:r.__setitem__('terminal_index',0))
    def test_missing_slot_rejected(self):self.bad(lambda r:r['world_frames'][0]['scanned_slots'].pop())
    def test_wrong_unit_order_rejected(self):self.bad(lambda r:r['world_frames'][0]['unit_calls'].reverse())
    def test_wrong_world_root_rejected(self):self.bad(lambda r:r['world_frames'][0]['call'].__setitem__('entry',0x475700))
    def test_standalone_HP_caller_rejected(self):self.bad(lambda r:next(c for c in r['world_frames'][0]['nested_calls'] if c['entry']==0x493450).__setitem__('caller',0x12100000))
    def test_forged_player_HP_rejected(self):self.bad(lambda r:r['world_frames'][62]['after'].__setitem__('target_record','00'*256))
    def test_missing_HP_write_rejected(self):self.bad(lambda r:r['hp_writes'].pop())
    def test_wrong_HP_PC_rejected(self):self.bad(lambda r:r['hp_writes'][0].__setitem__('pc',0x46B470))
    def test_missing_page_rejected(self):self.bad(lambda r:r['blobs'].pop(r['world_frames'][0]['before']['all_unit_slots']['pages'][0]))
    def test_corrupt_page_rejected(self):self.bad(lambda r:r['blobs'].__setitem__(next(iter(r['blobs'])),'00'))
    def test_wrong_page_order_rejected(self):self.bad(lambda r:r['world_frames'][0]['before']['all_unit_slots']['pages'].reverse())
    def test_missing_owned_region_rejected(self):self.bad(lambda r:r['final'].pop())
    def test_missing_TLS_leaf_rejected(self):self.bad(lambda r:r['platform']['trace'].pop())
    def test_foreign_TLS_thread_rejected(self):self.bad(lambda r:r['platform']['cleanup'].__setitem__('thread',0))
    def test_wrong_initial_relation_rejected(self):
        def edit(r):
            at=CTRL+0x115AAC+4*16;region=next(q for q in r['initial'] if q['pointer']<=at<q['pointer']+q['bytes']);b=bytearray.fromhex(region['hex']);b[at-region['pointer']]=0;region['hex']=b.hex()
        self.bad(edit)
    def test_unbounded_frames_rejected(self):
        c=deepcopy(corpus()[0]);c['budget']=385
        with self.assertRaises(ValueError):validate(c)
    def test_host_result_field_rejected(self):
        c=deepcopy(corpus()[0]);c['chosen_target']=1
        with self.assertRaises(ValueError):validate(c)
    def test_x87_change_rejected_by_fresh_original_execution(self):
        self.bad(lambda r:r['world_frames'][0]['stages'][0]['CPU']['FP0'].__setitem__(0,1),name='search_disabled',replay=True)


for c in corpus():
    def check(self,name=c['name']):verify_case(self.rows[name],False)
    setattr(EnemyEngagementTests,'test_case_'+c['name'],check)

if __name__=='__main__':unittest.main()
