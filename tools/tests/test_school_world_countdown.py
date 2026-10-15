import json,unittest
from copy import deepcopy
from tools.school_world_countdown import *


class SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.cases=json.loads((ROOT/'analysis/school-world-countdown-inputs-20261015.json').read_bytes())['cases']

    def test_consecutive_source_worlds_and_original_opcode_loop(self):
        for c in self.cases:
            state=c['initial_state']
            for tick in (4,5,6):
                r=world_project(state,tick);self.assertEqual(r['prefix']['delay'],182-tick);self.assertEqual(r['units']['idle_root_indices'],[217,247,248]);self.assertEqual(r['units']['templates_activated'],0)
                pool=bytes.fromhex(r['units']['after'][6]['hex']);node=pool[:NODE]
                self.assertEqual(get(node,14),5 if tick==6 else 6-tick)
                if tick==6:self.assertEqual(u32(node,4),state['unit_inputs']['units'][0]['bindings'][1]['metadata_pointer']+source_contract()['following2063']['offset'])
                state=r['next_state']

    def test_finite_tick_and_no_skipped_delay(self):
        s=self.cases[0]['initial_state']
        for tick in (3,7,True):
            with self.assertRaises(ValueError):world_project(s,tick)
        b=deepcopy(s);raw=bytearray.fromhex(b['prefix_before'][1]['hex']);put(raw,28,0,'h');b['prefix_before'][1]['hex']=raw.hex()
        with self.assertRaises(ValueError):world_project(b,4)

    def test_captured_audio_guard_and_early_expiry_refused(self):
        for kind in ('audio','expiry'):
            s=deepcopy(self.cases[0]['initial_state'])
            if kind=='audio':s['unit_inputs']['audio_manager_hex']='00'*8+'01'+'00'*11
            else:
                r=s['unit_before'][6];p=bytearray.fromhex(r['hex']);put(p,14,1,'h');r['hex']=p.hex()
            with self.assertRaises(ValueError):world_project(s,4)

    def test_cleared_root_cannot_silently_rebind_or_activate(self):
        for at,value in ((217*STRIDE+0x48+4,1),(215*STRIDE+0x293,0)):
            s=deepcopy(self.cases[0]['initial_state']);r=s['unit_before'][0];raw=bytearray.fromhex(r['hex']);raw[at]=value;r['hex']=raw.hex()
            # Prefix owns work memory too: corrupt its corresponding copy.
            s['prefix_before'][12]['hex']=raw.hex()
            with self.assertRaises(ValueError):world_project(s,4)


if __name__=='__main__':unittest.main()
