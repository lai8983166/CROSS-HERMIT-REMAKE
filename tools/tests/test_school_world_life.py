import gzip,json,unittest,zlib
from copy import deepcopy
from tools.school_world_life import *
from tools.school_world_life_codec import pack,unpack,MARKER,LIMIT
from tools.school_world_frames_verification import REPORTS,verify_case


class SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.states=[verify_case(c,'late') for c in json.loads(gzip.decompress(REPORTS['late'].read_bytes()))['cases']]

    def test_every_source_world_and_actual_boundaries(self):
        for initial in self.states:
            state=initial
            for tick in range(16,76):
                r=world_project(state,tick);active=r['units']['units'];last=next(u for u in active if u['index']==249);scene=next(u for u in active if u['index']==240)
                self.assertEqual(r['prefix']['delay'],182-tick)
                if tick==41:self.assertEqual((last['main_return'],last['main_wait'],last['root_idle']),(1,0,False))
                if tick==42:self.assertEqual(last['animation_steps'][0]['events'],[dict(kind='clear',depth=0)])
                if tick==65:self.assertEqual(scene['main_wait'],7);self.assertEqual(scene['animation_steps'][0]['events'][1],dict(kind='repeat',repeat=127,target_offset=666))
                released=[p for u in active for p in u.get('released_nodes',[])]
                self.assertEqual(len(released),len([u for u in active if u['index']<3]) if tick==74 else 0)
                state=r['next_state']
            pool=bytes.fromhex(state['unit_before'][6]['hex']);self.assertEqual([pool[i*NODE] for i in range(6)],[1,0,1,0,1 if len(initial['unit_inputs']['units'])==38 else 0,0])

    def test_source_repeat_counter_and_child_end_policy(self):
        s=source_contract();aw=schedule(s['programs']['main:383'],64);self.assertEqual((u32(aw,4),get(aw,14),get(aw,16)),(666,7,127))
        pr=s['programs']['attached:2103'];ended=schedule(pr,73);self.assertEqual((u32(ended,4),ended[11],get(ended,14)),(11398,1,0));self.assertEqual(u32(schedule(pr,74),4),0)

    def test_wrong_pc_timer_end_flag_and_skipped_call_refused(self):
        for at in (4,11,14,16):
            state=deepcopy(self.states[0]);row=state['unit_before'][6];raw=bytearray.fromhex(row['hex']);raw[at]^=1;row['hex']=raw.hex()
            with self.assertRaises(ValueError):world_project(state,16)
        for tick in (15,76,True,16.0,17):
            with self.assertRaises(ValueError):world_project(self.states[0],tick)

    def test_exact_lossless_all_owned_region_roundtrip(self):
        state=self.states[0];encoded=pack(state);self.assertEqual(unpack(encoded),state)
        self.assertLess(len(json.dumps(encoded)),len(json.dumps(state))//2)

    def test_compressed_region_malformed_truncated_trailing_and_size_refused(self):
        valid={MARKER:zlib.compress(b'abc').hex(),'bytes':3}
        self.assertEqual(unpack(valid),'616263')
        for bad in ({**valid,'bytes':2},{**valid,'bytes':True},{**valid,'bytes':LIMIT+1},{**valid,'extra':1},{**valid,MARKER:'zz'},{**valid,MARKER:valid[MARKER][:-2]},{**valid,MARKER:valid[MARKER]+'00'}):
            with self.assertRaises(ValueError):unpack(bad)

    def test_unexecuted_spawn_and_finite_repeat_refused(self):
        aw=bytearray(NODE);put(aw,4,100)
        for op in (1,3):
            with self.assertRaises(ValueError):step_animation(aw,0,[dict(offset=100,opcode=op,frame_hex=(bytes([op])+bytes(9)).hex())])


if __name__=='__main__':unittest.main()
