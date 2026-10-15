import hashlib,json,struct,unittest
from copy import deepcopy
from tools.school_scene_templates import project,source_contract,STRIDE
from tools.school_scene_templates_verification import REPORT,REPORT_SHA,verify_case,load_verified_checkpoint


class SceneTemplatesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=json.loads(REPORT.read_bytes())

    def test_three_original22_unit_loops_full_source_and_no_activation(self):
        self.assertEqual(hashlib.sha256(REPORT.read_bytes()).hexdigest(),REPORT_SHA);self.assertEqual(self.data['source_contract'],source_contract())
        for c in self.data['cases']:
            self.assertTrue(verify_case(c));self.assertEqual(len(c['actual']['returns']),44);self.assertEqual(len(c['actual']['calls']),198)
        self.assertEqual(self.data['templates_activated'],0)
        for k in ('world_completed','persistent_write_authority'):self.assertIs(self.data[k],False)

    def test_all_owned_corruptions_and_active_or_wrong_phase_refused(self):
        for i in range(10):
            c=deepcopy(self.data['cases'][0]);r=c['actual']['after'][i];r['hex']=r['hex'][:-2]+('01' if r['hex'][-2:]=='00' else '00')
            with self.assertRaises(ValueError):verify_case(c)
        b=deepcopy(self.data['cases'][0]['actual']['before']);w=bytearray.fromhex(b[0]['hex']);w[239*STRIDE+0x293]=1;b[0]['hex']=w.hex()
        with self.assertRaises(ValueError):project(b)
        b=deepcopy(self.data['cases'][0]['actual']['before']);w=bytes.fromhex(b[0]['hex']);rp=struct.unpack_from('<I',w,218*STRIDE+0x258)[0]
        records=bytearray.fromhex(b[1]['hex']);records[rp-b[1]['pointer']+15]=1;b[1]['hex']=records.hex()
        with self.assertRaises(ValueError):project(b)

    def test_missing_call_return_test_or_false_activation_and_scope_refused(self):
        for mutate in (lambda c:c['actual']['calls'].pop(),lambda c:c['actual']['returns'].pop(),lambda c:c['actual']['tested_slots'].pop(),
          lambda c:c['actual'].update(templates_activated=1),lambda c:c['actual'].update(next_unit_executed=True),lambda c:c['actual']['pending'].update(sp=0)):
            c=deepcopy(self.data['cases'][0]);mutate(c)
            with self.assertRaises(ValueError):verify_case(c)

    def test_three_full_private_continuations_before240(self):
        for c in self.data['cases']:
            payload,cp=load_verified_checkpoint(c['name']);self.assertEqual(hex(payload['pending_eip']),cp['pending_eip'])
        with self.assertRaises(ValueError):load_verified_checkpoint('../initial')


if __name__=='__main__':unittest.main()
