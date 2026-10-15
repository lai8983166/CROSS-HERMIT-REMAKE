import json,struct,unittest
from copy import deepcopy
from tools.school_world_final import *


class WorldFinalSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.cases=json.loads((ROOT/'analysis/school-world-final-inputs-20261015.json').read_bytes())['cases']

    def test_four_source_archives_and_ten_complete_unit_projections(self):
        s=source_contract();self.assertEqual([s['jobs'][str(k)]['main']['duration'] for k in (383,393,387,4)],[8,1,1,40])
        for c in self.cases:
            before=deepcopy(c['before']);r=units_project(c['inputs'],before);self.assertEqual(c['before'],before)
            self.assertEqual([u['frame_wait'] for u in r['units']],[7]*7+[0,0,39]);self.assertEqual([u['main_return'] for u in r['units']],[0]*7+[1,1,0])
            self.assertEqual([u['index'] for u in r['units'] if u['vision_args'] is not None],[248]);self.assertEqual(r['after'][9]['hex'],'00000000')
            for i in (1,5,6,7,8):self.assertEqual(r['after'][i],before[i])

    def test_wrong_source_metadata_opening_queue_and_phase_refuse(self):
        c=self.cases[0]
        for off in (0x293,0x292,0x518,0x510,0x48+0x20,0x48+0x34):
            b=deepcopy(c['before']);w=bytearray.fromhex(b[0]['hex']);w[240*STRIDE+off]=1;b[0]['hex']=w.hex()
            with self.assertRaises(ValueError):units_project(c['inputs'],b)
        x=deepcopy(c['inputs']);x['units'][0]['binding']['metadata_sha256']='0'*64
        with self.assertRaises(ValueError):units_project(x,c['before'])
        x=deepcopy(c['inputs']);x['map_all_bytes_verified']=16
        with self.assertRaises(ValueError):units_project(x,c['before'])

    def test_actual_enabled_suffix_full_idle_effects_and_preserved_action(self):
        for c in self.cases:
            b=deepcopy(c['tail_before']);out=suffix_project(c['tail_inputs'],b);self.assertEqual(c['tail_before'],b)
            self.assertEqual(bytes.fromhex(out[5]['hex'])[4],1);self.assertEqual(out[5],b[5]);self.assertEqual(out[3]['hex'],idle_effects(bytes.fromhex(b[3]['hex'])).hex())
            for i in (4,6,7,8,9):self.assertEqual(out[i],b[i])

    def test_enabled_suffix_refuses_wrong_action_nonempty_queue_and_secondary(self):
        c=self.cases[0]
        for i,off,value in ((5,4,0),(5,24,0),(6,8,1),(4,0,1)):
            b=deepcopy(c['tail_before']);v=bytearray.fromhex(b[i]['hex']);v[off]=value;b[i]['hex']=v.hex()
            with self.assertRaises(ValueError):suffix_project(c['tail_inputs'],b)


if __name__=='__main__':unittest.main()
