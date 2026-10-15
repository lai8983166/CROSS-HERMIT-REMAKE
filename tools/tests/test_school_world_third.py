import json,unittest,struct
from copy import deepcopy
from tools.school_world_third import *


class SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.cases=json.loads((ROOT/'analysis/school-world-third-inputs-20261015.json').read_bytes())['cases']

    def test_all_remaining_units_and_actual_clear_projection(self):
        for c in self.cases:
            r=project(c['inputs'],c['before']);self.assertEqual(r['cleared_root_indices'],[217,247,248]);self.assertEqual(sum(u['inactive'] for u in r['units']),24)
            self.assertEqual(r['after'][1],c['before'][1]);self.assertEqual(r['after'][0]['hex'][:STRIDE*2],c['before'][0]['hex'][:STRIDE*2]);self.assertEqual(r['after'][-1]['hex'],'00000000')

    def test_refuse_skipped_wait_phase_activation_or_end_flag(self):
        c=self.cases[0]
        for kind in ('delay','phase','activation','end'):
            b=deepcopy(c['before']);w=bytearray.fromhex(b[0]['hex']);ctrl=bytearray.fromhex(b[7]['hex']);records=bytearray.fromhex(b[1]['hex'])
            if kind=='delay':put(ctrl,28,0,'h')
            elif kind=='phase':w[215*STRIDE+0x293]=0
            elif kind=='activation':records[u32(w,215*STRIDE+0x258)-b[1]['pointer']+15]=1
            else:w[217*STRIDE+0x48+11]=0
            b[0]['hex']=w.hex();b[1]['hex']=records.hex();b[7]['hex']=ctrl.hex()
            with self.assertRaises(ValueError):project(c['inputs'],b)

    def test_unproved_attached_expiry_or_cycle_rejected(self):
        c=self.cases[0];w=bytes.fromhex(c['before'][0]['hex']);p=u32(w,STRIDE+0x48+32)-POOL
        for kind in ('expiry','cycle'):
            b=deepcopy(c['before']);pool=bytearray.fromhex(b[6]['hex'])
            if kind=='expiry':put(pool,p+14,1,'h')
            else:put(pool,p+32,POOL+p)
            b[6]['hex']=pool.hex()
            with self.assertRaises(ValueError):project(c['inputs'],b)

    def test_enabled_suffix_and_upcoming_audio_source_only(self):
        for c in self.cases:
            after=suffix_project(c['tail_inputs'],c['tail_before']);self.assertEqual(after[5],c['tail_before'][5]);self.assertNotEqual(after[3],c['tail_before'][3])
        audio=source_contract()['upcoming2063'];self.assertEqual((audio['opcode'],audio['sound']),(2,59));self.assertIs(audio['native_executed'],False)


if __name__=='__main__':unittest.main()
