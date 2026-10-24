"""World scheduling, global resets and rejection of altered source evidence."""
from copy import deepcopy
import gzip
import json
import struct
import unittest
from tools.battle_world_update import corpus,validate
from tools.battle_world_update_emulation import ROOT,CTRL,UNIT,TARGET,REGIONS,sha,source_contract
from tools.battle_world_update_verification import verify_case

REPORT='analysis/battle-world-update-source-v2-20261024.json.gz'
REPORT_SHA='5f2fe150e8a74f42bd948a5bc878bb01de7afc3808e70ff2afa84f28a020cb95'


class WorldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw=(ROOT/REPORT).read_bytes()
        if sha(raw)!=REPORT_SHA:raise ValueError('fixed original whole world evidence')
        cls.data=json.loads(gzip.decompress(raw));cls.rows={r['input']['name']:r for r in cls.data['cases']}

    def bad(self,edit,name='ordinary',replay=False):
        r=deepcopy(self.rows[name]);edit(r)
        with self.assertRaises(ValueError):verify_case(r,replay)

    def frames(self,name='ordinary'):return self.rows[name]['consume']['world_frames']

    def test_original_contract(self):
        self.assertEqual(self.data['source_contract'],source_contract());self.assertEqual([r['input'] for r in self.data['cases']],corpus())
        self.assertEqual((len(self.rows),len(REGIONS)),(11,37))

    def test_all_250_scanned_but_only_two_used_units_called(self):
        for f in self.frames():
            self.assertEqual(f['scanned_slots'],[UNIT+i*0x520 for i in range(250)])
            self.assertEqual([(s['unit'],s['index'],s['caller']) for s in f['unit_calls']],[(UNIT,0,0x46B584),(TARGET,1,0x46B584)])
            self.assertEqual([s['result'] for s in f['unit_calls']],[5,5])

    def test_per_frame_statistics_reset_and_last_unit_clear(self):
        for f in self.frames():
            pre,units,post=[s['state'] for s in f['stages']]
            self.assertEqual(bytes.fromhex(pre['world_stats'])[:0x800],bytes(0x800))
            self.assertEqual(struct.unpack_from('<h',bytes.fromhex(units['world_stats']),0)[0],1)
            self.assertEqual(struct.unpack_from('<h',bytes.fromhex(units['world_stats']),16)[0],1)
            self.assertEqual((pre['last_updated'],units['last_updated'],post['last_updated']),(0,TARGET,0))

    def test_double_visibility_buffer_swap_and_clear(self):
        frames=self.frames()
        for i,f in enumerate(frames):
            pre,post=f['stages'][0]['state'],f['after']
            current,back=struct.unpack('<II',bytes.fromhex(pre['world_fields']['0x11003e0c']))
            self.assertEqual((current,back),((0x12744000,0x12740000) if i%2==0 else (0x12740000,0x12744000)))
            key='visible_other' if i%2==0 else 'visible'
            self.assertEqual(bytes.fromhex(pre[key])[:6144],bytes(6144))
            self.assertTrue({95,143,223,255}.issubset(set(bytes.fromhex(post[key]))))
            self.assertTrue(any(bytes.fromhex(post['seen'])))

    def test_world_lists_rebuilt_and_all_unused_slots_stay_empty(self):
        for f in self.frames():
            b=bytes.fromhex(f['stages'][0]['state']['world_fields']['0x110dc30c'])
            self.assertEqual(struct.unpack_from('<3I',b,0),(2,UNIT,TARGET))
            self.assertEqual(struct.unpack_from('<2I',b,0xdd0c4-0xdc30c),(1,TARGET))
            self.assertEqual(struct.unpack_from('<2I',b,0xdd4b0-0xdc30c),(1,UNIT))
            self.assertEqual(bytes.fromhex(f['after']['all_unit_slots'])[2*0x520:],bytes(248*0x520))

    def test_ten_empty_preview_animations_tick_in_post_update(self):
        for i,f in enumerate(self.frames()):
            b=bytes.fromhex(f['after']['world_fields']['0x1110c680'])
            for j in range(10):self.assertEqual((b[j*0x520+4],struct.unpack_from('<h',b,j*0x520+10)[0]),(1,i+1))

    def test_enemy_idle_threshold_draws_each_later_frame(self):
        frames=self.frames();self.assertEqual([f['after']['battle_draws'] for f in frames],[2,3,4])
        self.assertEqual([struct.unpack_from('<h',bytes.fromhex(f['after']['target_record']),0x16)[0] for f in frames],[62,63,64])

    def test_HP_zero_death_request_then_command_then_persistent_score(self):
        frames=self.frames('lethal')
        self.assertEqual(bytes.fromhex(frames[0]['after']['target'])[0x292],13)
        self.assertEqual(bytes.fromhex(frames[1]['after']['target'])[0x290],13)
        self.assertEqual([struct.unpack_from('<h',bytes.fromhex(f['after']['world_stats']),0x800)[0] for f in frames],[0,20,20])
        self.assertEqual(bytes.fromhex(frames[-1]['after']['target_record'])[15],1)

    def test_total_gate_skips_all_250_predicates_and_pre_post_work(self):
        for f in self.frames('world_gate_off'):
            self.assertEqual(f['entries'],[0x46B470]);self.assertEqual(f['scanned_slots'],[]);self.assertEqual(f['unit_calls'],[])
            self.assertEqual(f['before'],f['after'])

    def test_missing_frame_rejected(self):self.bad(lambda r:r['consume']['world_frames'].pop())
    def test_missing_slot_rejected(self):self.bad(lambda r:r['consume']['world_frames'][0]['scanned_slots'].pop())
    def test_duplicate_slot_rejected(self):self.bad(lambda r:r['consume']['world_frames'][0]['scanned_slots'].__setitem__(249,UNIT))
    def test_unit_order_rejected(self):self.bad(lambda r:r['consume']['world_frames'][0]['unit_calls'].reverse())
    def test_forged_world_root_rejected(self):self.bad(lambda r:r['consume']['world_frames'][0]['call'].__setitem__('entry',0x46B760))
    def test_forged_natural_caller_rejected(self):self.bad(lambda r:r['consume']['world_frames'][0]['unit_calls'][0].__setitem__('caller',0x12100000))
    def test_forged_nested_return_stack_rejected(self):self.bad(lambda r:r['consume']['world_frames'][0]['unit_calls'][0]['cpu_after'].__setitem__('ESP',0))
    def test_missing_pre_helper_rejected(self):self.bad(lambda r:r['consume']['world_frames'][0]['entries'].pop(3))
    def test_stage_order_rejected(self):self.bad(lambda r:r['consume']['world_frames'][0]['stages'].reverse())
    def test_region_reset_rejected(self):self.bad(lambda r:r['consume']['world_frames'][1]['stages'][0]['state'].__setitem__('world_stats',r['consume']['world_frames'][0]['after']['world_stats']))
    def test_unused_slot_corruption_rejected(self):self.bad(lambda r:r['consume']['world_frames'][0]['after'].__setitem__('all_unit_slots','01'+r['consume']['world_frames'][0]['after']['all_unit_slots'][2:-2]+'01'))
    def test_visible_buffer_corruption_rejected(self):self.bad(lambda r:r['final_state'].__setitem__('visible_other','00'*0x2000))
    def test_missing_owned_region_rejected(self):self.bad(lambda r:r['final'].pop())
    def test_native_cleanup_thread_rejected(self):self.bad(lambda r:r['platform']['cleanup'].__setitem__('thread',0))
    def test_missing_native_leaf_rejected(self):self.bad(lambda r:r['platform']['trace'].pop())
    def test_host_result_input_rejected(self):
        c=deepcopy(corpus()[0]);c['result']=0
        with self.assertRaises(ValueError):validate(c)
    def test_unbounded_frame_budget_rejected(self):
        c=deepcopy(corpus()[0]);c['frames']=5
        with self.assertRaises(ValueError):validate(c)
    def test_x87_stage_tamper_rejected_by_fresh_source(self):
        self.bad(lambda r:r['consume']['world_frames'][0]['stages'][0]['CPU']['FP0'].__setitem__(0,1),replay=True)


for c in corpus():
    def check(self,name=c['name']):verify_case(self.rows[name],False)
    setattr(WorldTests,'test_case_'+c['name'],check)

if __name__=='__main__':unittest.main()
