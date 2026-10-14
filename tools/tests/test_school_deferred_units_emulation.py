import hashlib,json,unittest
from copy import deepcopy
from tools.school_deferred_units import project,source_contract,STRIDE
from tools.school_deferred_units_verification import REPORT,REPORT_SHA,verify_case,load_verified_checkpoint


class DeferredUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=json.loads(REPORT.read_bytes())

    def test_three_source_projected_inactive_original_early_returns(self):
        self.assertEqual(hashlib.sha256(REPORT.read_bytes()).hexdigest(),REPORT_SHA);self.assertEqual(self.data['source_contract'],source_contract())
        for c in self.data['cases']:
            self.assertTrue(verify_case(c));self.assertEqual(project(c['actual']['before'])['templates_activated'],0)
        for k in ('world_completed','original_opening_completed','persistent_write_authority'):self.assertIs(self.data[k],False)

    def test_full_memory_and_wrong_inactive_predicate_phase_refused(self):
        for i in range(10):
            c=deepcopy(self.data['cases'][0]);r=c['actual']['after'][i];r['hex']=r['hex'][:-2]+('01' if r['hex'][-2:]=='00' else '00')
            with self.assertRaises(ValueError):verify_case(c)
        for off,value in ((0x293,1),(0x2A7,0),(0x292,1)):
            before=deepcopy(self.data['cases'][0]['actual']['before']);w=bytearray.fromhex(before[0]['hex']);w[215*STRIDE+off]=value;before[0]['hex']=w.hex()
            with self.assertRaises(ValueError):project(before)

    def test_wrong_return_loop_activation_parent_or_skipped_animation_refused(self):
        mutations=[lambda c:c['actual']['returns'][0].update(eax=0),lambda c:c['actual']['tested_slots'].pop(),
          lambda c:c['actual'].update(templates_activated=1),lambda c:c['parent_checkpoint'].update(sha256='0'*64),
          lambda c:c['actual']['visited'].append(0x40A100),lambda c:c['actual']['pending'].update(sp=0)]
        for mutate in mutations:
            c=deepcopy(self.data['cases'][0]);mutate(c)
            with self.assertRaises(ValueError):verify_case(c)

    def test_three_verified_complete_scene_entry_private_checkpoints(self):
        for c in self.data['cases']:
            payload,cp=load_verified_checkpoint(c['name']);self.assertEqual(hex(payload['pending_eip']),cp['pending_eip'])
        with self.assertRaises(ValueError):load_verified_checkpoint('../initial')


if __name__=='__main__':unittest.main()
