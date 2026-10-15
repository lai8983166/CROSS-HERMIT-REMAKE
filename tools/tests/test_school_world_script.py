import unittest
from copy import deepcopy
from tools.school_world_script import *
from tools.school_world_script_inputs import checked_parent

class SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.parents=[checked_parent(n) for n in ('initial','student9_waiting','fifth_class')]

    def test_complete_preflight_binding_and_two_paused_worlds(self):
        for parent,state,seed in self.parents:
            p=preflight_project(seed['inputs'],seed['before']);b=binding_project(seed['inputs'],p['after'])
            self.assertEqual([c['opcode'] for c in p['commands']],[167,8,166,11,19]);self.assertEqual(p['commands'][-1]['offset'],944)
            d=script_data(b['after']);self.assertEqual((d[TACT][0x43],d[TACT][0x59],d[CONTROL][12],d[VM][4],d[VM][5]),(1,1,6,1,1));self.assertEqual(u32(d[VM],0x1C),0)
            state=merge_script_state(state,b['after']);frozen=next(r['hex'] for r in state['unit_before'] if r['name']=='works')
            for tick in (184,185):
                r=world_project(state,tick);self.assertEqual(r['prefix']['controller_state'],7);self.assertEqual(r['prefix']['action'],0);self.assertEqual(r['units']['after'][0]['hex'],frozen);state=r['next_state']
            self.assertEqual(get(bytes.fromhex(state['tail_before'][3]['hex']),10),185)

    def test_source_native_cleanup_bodies_are_pinned(self):
        s=source_contract();self.assertEqual(len(s['native_helpers']),6);self.assertEqual(s['source_script_sha256'],SCRIPT_SHA)
        self.assertEqual([x['va'] for x in s['native_helpers'][:4]],['0x42b2d0','0x41e500','0x41d790','0x40d120'])

    def test_wrong_driver_live_audio_or_incomplete_regions_refused(self):
        seed=self.parents[0][2]
        for key,value in (('driver','synthetic'),('script_sha256','0'*64),('selector',1)):
            bad=deepcopy(seed['inputs']);bad[key]=value
            with self.assertRaises(ValueError):preflight_project(bad,seed['before'])
        for index in (-1,-2):
            bad=deepcopy(seed['before']);raw=bytearray.fromhex(bad[index]['hex']);raw[8]=1;bad[index]['hex']=raw.hex()
            with self.assertRaises(ValueError):preflight_project(seed['inputs'],bad)
        with self.assertRaises(ValueError):preflight_project(seed['inputs'],seed['before'][:-1])

    def test_binding_requires_real_preflight_result_and_paused_status(self):
        seed=self.parents[0][2]
        with self.assertRaises(ValueError):binding_project(seed['inputs'],seed['before'])
        p=preflight_project(seed['inputs'],seed['before']);b=binding_project(seed['inputs'],p['after']);state=merge_script_state(self.parents[0][1],b['after'])
        for tick in (183,186,True,184.0,185):
            with self.assertRaises(ValueError):world_project(state,tick)
        for at in (0x44,0x59):
            bad=deepcopy(state);r=bad['prefix_before'][0];raw=bytearray.fromhex(r['hex']);raw[at]^=1;r['hex']=raw.hex()
            with self.assertRaises(ValueError):world_project(bad,184)

if __name__=='__main__':unittest.main()

class CallSourceTests(unittest.TestCase):
    def test_selected_call_protocols_are_direct_source_instructions(self):
        raw=SOURCE.read_bytes()
        for phase,count in (('preflight',48),('binding',16)):
            returns=call_protocol(phase);self.assertEqual(len(returns),count)
            for ret in returns:self.assertEqual(raw[ret-BASE-5],0xE8)
