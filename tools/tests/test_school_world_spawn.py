import gzip,json,unittest
from copy import deepcopy
from tools.school_world_spawn import *
from tools.school_world_life_codec import pack,unpack
from tools.school_world_life_verification import REPORTS,verify_case


class SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.states=[verify_case(c,'release') for c in json.loads(gzip.decompress(REPORTS['release'].read_bytes()))['cases']]

    def test_every_world_pool_reuse_and_predecessor_unlink(self):
        for initial in self.states:
            state=initial
            for tick in range(76,119):
                r=world_project(state,tick);units=r['units']['units'];friends=[u for u in units if u['index']<3];works=bytes.fromhex(r['units']['after'][0]['hex']);pool=bytes.fromhex(r['units']['after'][6]['hex'])
                self.assertEqual(r['prefix']['delay'],182-tick)
                self.assertEqual([p for u in friends for p in u['allocated_nodes']],[POOL+(2*u['index']+1)*NODE for u in friends] if tick==107 else [])
                self.assertEqual([p for u in friends for p in u['released_nodes']],[POOL+2*u['index']*NODE for u in friends] if tick==118 else [])
                if tick>=107:
                    for u in friends:
                        i=u['index'];root=works[i*STRIDE+0x48:i*STRIDE+0xA0];node=POOL+(2*i+1)*NODE;n=pool[(2*i+1)*NODE:(2*i+2)*NODE];spec=source_contract()['spawns'][str(u['job'])]
                        self.assertEqual(u32(root,32),node);self.assertEqual((n[0],n[2],n[8],u32(n,24)),(1,0,1,spec['layer']));self.assertEqual(u32(n,44),u32(root,44));self.assertEqual(n[0x48:0x54],root[0x48:0x54])
                        self.assertEqual(u32(n,32),POOL+2*i*NODE if tick<118 else 0)
                        if tick==107:self.assertEqual(len(u['linked_order']),1);self.assertEqual(get(n,14),spec['program']['duration']-1)
                state=r['next_state']
            self.assertEqual(unpack(pack(state)),state)

    def test_depth1_layer_retained_despite_source_sprite_layer(self):
        s=source_contract();pr=s['programs']['spawn:3'];node=bytearray(NODE);node[8]=1;put(node,24,0);setup(node,0,pr[0]);self.assertEqual(u32(node,24),0)
        node[8]=0;setup(node,0,pr[0]);self.assertEqual(u32(node,24),1)

    def test_main_opcode_loop_decrements_and_child_immediate_single_step(self):
        s=source_contract()
        for job in ('3','4','9'):
            main=schedule(s['programs']['main:'+job],106);pr=s['spawns'][job];self.assertEqual(get(main,14),3 if job=='9' else 5)
            child=schedule(s['programs']['spawn:'+job],1,layer=pr['layer'],depth=1);self.assertEqual(get(child,14),pr['program']['duration']-1);self.assertEqual(u32(child,24),pr['layer'])

    def test_modified_spawn_owner_flags_or_layer_refused(self):
        state=self.states[0]
        for tick in range(76,108):state=world_project(state,tick)['next_state']
        for at in (3,0x18,0x1C,0x2C):
            bad=deepcopy(state);r=bad['unit_before'][6];raw=bytearray.fromhex(r['hex']);raw[NODE+at]^=1;r['hex']=raw.hex()
            with self.assertRaises(ValueError):world_project(bad,108)

    def test_wrong_first_free_slot_is_not_silently_substituted(self):
        state=self.states[0]
        for tick in range(76,107):state=world_project(state,tick)['next_state']
        state=deepcopy(state);r=state['unit_before'][6];raw=bytearray.fromhex(r['hex']);raw[NODE]=1;r['hex']=raw.hex()
        with self.assertRaises(ValueError):world_project(state,107)

    def test_finite_tick_and_no_skipped_delay(self):
        for tick in (75,119,True,76.0,77):
            with self.assertRaises(ValueError):world_project(self.states[0],tick)


if __name__=='__main__':unittest.main()
