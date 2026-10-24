"""Real melee animation, independent events and preserved effect frontier."""
from copy import deepcopy
import gzip
import json
import unittest
from tools.battle_attack_animation import corpus,case,validate,resource
from tools.battle_attack_animation_emulation import ROOT,UNIT,DATA,PAGE,POOL,EVENTS,EVENT_CTRL,AnimationMachine,source_contract,sha
from tools.battle_attack_animation_verification import verify_case

REPORT='analysis/battle-attack-animation-source-v2-20261024.json.gz'
REPORT_SHA='b9f81791619557a37a7f5058ed133d63f5d9a559179c7e115451f49c3dcd1d54'


class AnimationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw=(ROOT/REPORT).read_bytes()
        if sha(raw)!=REPORT_SHA:raise ValueError('immutable real animation corpus')
        cls.data=json.loads(gzip.decompress(raw));cls.rows={r['input']['name']:r for r in cls.data['cases']}

    def bad(self,edit,name='job1_E',replay=False):
        r=deepcopy(self.rows[name]);edit(r)
        with self.assertRaises(ValueError):verify_case(r,replay)

    def test_source_assets_and_exact_corpus(self):
        self.assertEqual(self.data['source_contract'],source_contract());self.assertEqual([r['input'] for r in self.data['cases']],corpus());self.assertEqual(len(self.rows),41)
    def test_four_distinct_real_metadata_sources(self):
        self.assertEqual(len({resource(j)['identity']['sha256'] for j in range(1,5)}),4)
        self.assertEqual([len(resource(j)['raw']) for j in range(1,5)],[12284,13688,17180,17108])
    def test_event_precedes_animation_end(self):
        for j,event,end in ((1,16,48),(2,16,48),(3,12,36),(4,12,36)):
            full=verify_case(self.rows['job'+str(j)+'_E'],False);early=verify_case(self.rows['job'+str(j)+'_first_event'],False)
            self.assertEqual((full['first_event_tick'],full['animation_roots']),(event,end));self.assertFalse(early['animation_ended'])
    def test_full_binding_uses_original_initializers(self):
        self.assertEqual(self.rows['job1_E']['entries']['0x467020'],1);self.assertEqual(self.rows['job1_E']['entries']['0x409ef0'],7)
    def test_sound_code_runs_closed_device_gate(self):
        for j in range(1,5):
            r=self.rows['job'+str(j)+'_E'];self.assertEqual(r['entries']['0x40b990'],1);self.assertEqual(r['entries']['0x40d390'],1)
    def test_command12_consumption_returns_and_reclaims(self):
        for n in ('target_command12_at_consume','actor_command12_at_consume'):
            v=verify_case(self.rows[n],False);self.assertTrue(v['inactive_consumer_returned']);self.assertFalse(v['effect_frontier'])
    def test_cancel_reclaims_live_child(self):
        r=self.rows['cancel_with_live_child'];self.assertNotEqual(r['ticks'][-1]['after']['children'][:2],'00');self.assertEqual(r['final_state']['children'][:2],'00')
    def test_fresh_full_source_frontier_reproduction(self):verify_case(self.rows['job1_first_event'],True)
    def test_wrong_frame_counter_rejected(self):self.bad(lambda r:r['ticks'][0].__setitem__('after',r['ticks'][0]['before']))
    def test_missing_original_tick_rejected(self):self.bad(lambda r:r['ticks'].pop())
    def test_fabricated_consumer_return_rejected(self):self.bad(lambda r:r['consume'].__setitem__('returned',True))
    def test_effect_argument_corruption_rejected(self):self.bad(lambda r:r['consume'].__setitem__('stack_hex','00'*len(bytes.fromhex(r['consume']['stack_hex']))))
    def test_wrong_effect_PC_rejected(self):self.bad(lambda r:r['consume']['cpu_after'].__setitem__('EIP',0x48AAE1))
    def test_wrong_original_caller_rejected(self):self.bad(lambda r:r['steps'][0]['call'].__setitem__('entry',0x477980))
    def test_forged_event_payload_rejected(self):self.bad(lambda r:r['ticks'][15]['after'].__setitem__('events','00'*0x2000))
    def test_unused_child_slot_corruption_rejected(self):
        def edit(r):
            page=next(x for x in r['final'] if x['pointer']==PAGE);b=bytearray.fromhex(page['hex']);b[POOL-PAGE+100*88]=1;page['hex']=b.hex()
        self.bad(edit)
    def test_readonly_metadata_corruption_rejected(self):
        def edit(r):
            data=next(x for x in r['final'] if x['pointer']==DATA);b=bytearray.fromhex(data['hex']);b[100]^=1;data['hex']=b.hex()
        self.bad(edit)
    def test_child_pool_digest_corruption_rejected(self):self.bad(lambda r:r['ticks'][0]['after'].__setitem__('children_sha256','0'*64))
    def test_early_boundary_mislabeled_end_rejected(self):self.bad(lambda r:r['input'].__setitem__('consume','boundary'),name='job1_first_event')
    def test_host_flag_field_input_rejected(self):
        c=case('bad');c['animation_done']=1
        with self.assertRaises(ValueError):validate(c)
    def test_unknown_effect_body_rejected(self):
        m=AnimationMachine(case('boundary'))
        with self.assertRaisesRegex(ValueError,'undeclared original instruction'):m.code(m.uc,0x48AAE0,1,None)
    def test_original_metadata_write_rejected(self):
        m=AnimationMachine(case('write_boundary'))
        with self.assertRaisesRegex(ValueError,'forbidden original write'):m.write_hook(m.uc,0,DATA,1,0,None)
    def test_exhausted_event_pool_refuses_original_assertion(self):
        m=AnimationMachine(case('exhausted'))
        # Explicit negative fixture before the first original root executes.
        m.put(EVENT_CTRL+0x1C,0)
        with self.assertRaisesRegex(ValueError,'undeclared original instruction'):m.run()
    def test_trace_corruption_rejected_by_source_replay(self):self.bad(lambda r:r.__setitem__('write_trace_sha256','0'*64),replay=True)
    def test_x87_frontier_corruption_rejected_by_source_replay(self):self.bad(lambda r:r['consume']['cpu_after']['FP0'].__setitem__(0,1),replay=True)


for c in corpus():
    def check(self,name=c['name']):verify_case(self.rows[name],False)
    setattr(AnimationTests,'test_case_'+c['name'],check)

if __name__=='__main__':unittest.main()
