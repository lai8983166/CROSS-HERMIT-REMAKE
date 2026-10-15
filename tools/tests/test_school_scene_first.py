import json,struct,unittest
from copy import deepcopy
from tools.school_scene_first import *


class SceneFirstSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.cases=json.loads((ROOT/'analysis/school-scene-first-inputs-20261015.json').read_bytes())['cases']

    def test_source_metadata_terminal_bit_and_second_dispatch(self):
        s=source_contract();self.assertEqual(s['main']['duration'],1);self.assertEqual(bytes.fromhex(s['main']['frame_hex'])[0],0x80)
        self.assertEqual(s['main']['metadata_bytes'],3212);self.assertEqual(s['category_mask'],1);self.assertEqual(s['pose_lookup_hex'],'0201')

    def test_initializer_and_terminal_complete_preserve_whole_other_regions(self):
        for c in self.cases:
            old=deepcopy(c['before']);init=project(c['inputs'],old,'initializer');complete=project(c['inputs'],old,'complete')
            self.assertEqual(c['before'],old)
            for phase,result in (('initializer',init),('complete',complete)):
                w=bytes.fromhex(result['after'][0]['hex'])[INDEX*STRIDE:(INDEX+1)*STRIDE]
                self.assertEqual(list(w[6:8]),[1,1]);self.assertEqual(w[0x293],1);self.assertEqual(struct.unpack_from('<h',w,0x48+0xC)[0],1)
                for i in (1,3,4,5,6,7,8):self.assertEqual(result['after'][i],old[i])
                self.assertEqual(result['unit_completed'],phase=='complete')
            wi=bytes.fromhex(init['after'][0]['hex']);wc=bytes.fromhex(complete['after'][0]['hex']);at=INDEX*STRIDE+0x48
            self.assertEqual(wi[at+4:at+8],wc[at+4:at+8]);self.assertEqual(wc[at+0xB],1);self.assertEqual(wc[at+0xE:at+0x10],b'\0\0')
            self.assertEqual(complete['main_animation_return'],1);self.assertIsNone(complete['vision_args']);self.assertEqual(complete['next_slot'],218)

    def test_source_faction_zero_relation_controls_vision(self):
        c=self.cases[0];actual=project(c['inputs'],c['before'],'complete');self.assertIsNone(actual['vision_args'])
        hypothetical=deepcopy(c['inputs']);rel=bytearray.fromhex(hypothetical['relation_matrix_hex']);rel[6]=0;hypothetical['relation_matrix_hex']=rel.hex()
        result=project(hypothetical,c['before'],'complete');self.assertEqual(result['vision_args'],[59,12,6]);self.assertNotEqual(result['after'][3]['hex'],c['before'][3]['hex'])

    def test_wrong_queues_phase_metadata_map_lengths_and_opening_refuse(self):
        c=self.cases[0]
        for off in (0x293,0x292,0x510,0x518,0x48+0x20,0x48+0x34,0x48+0x48):
            b=deepcopy(c['before']);w=bytearray.fromhex(b[0]['hex']);w[INDEX*STRIDE+off]=1;b[0]['hex']=w.hex()
            with self.assertRaises(ValueError):project(c['inputs'],b,'complete')
        x=deepcopy(c['inputs']);x['main_binding']['metadata_sha256']='0'*64
        with self.assertRaises(ValueError):project(x,c['before'],'complete')
        x=deepcopy(c['inputs']);x['map_all_bytes_verified']=16
        with self.assertRaises(ValueError):project(x,c['before'],'complete')
        b=deepcopy(c['before']);ctrl=bytearray.fromhex(b[7]['hex']);ctrl[24]=0;b[7]['hex']=ctrl.hex()
        with self.assertRaises(ValueError):project(c['inputs'],b,'complete')


if __name__=='__main__':unittest.main()
