import hashlib,json,unittest
from copy import deepcopy
from tools.school_scene_first_verification import REPORTS,SHAS,verify_case,load_verified_checkpoint
from tools.school_scene_first import source_contract


class Checks:
    @classmethod
    def setUpClass(cls):cls.data=json.loads(REPORTS[cls.phase].read_bytes())

    def test_three_full_source_original_phases(self):
        self.assertEqual(hashlib.sha256(REPORTS[self.phase].read_bytes()).hexdigest(),SHAS[self.phase]);self.assertEqual(self.data['source_contract'],source_contract())
        for c in self.data['cases']:self.assertTrue(verify_case(c,self.phase))
        self.assertEqual(self.data['unit_completed'],self.phase=='complete')
        for k in ('world_completed','original_opening_completed','persistent_write_authority'):self.assertIs(self.data[k],False)

    def test_every_owned_region_corruption_refused(self):
        for i in range(10):
            c=deepcopy(self.data['cases'][0]);r=c['actual']['after'][i];r['hex']=r['hex'][:-2]+('01' if r['hex'][-2:]=='00' else '00')
            with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_wrong_source_relation_call_stack_scope_and_parent_refused(self):
        mutations=[lambda c:c['actual']['inputs']['main_binding'].update(metadata_sha256='0'*64),lambda c:c['actual']['inputs'].update(relation_matrix_hex='00'*256),
          lambda c:c['actual']['calls'][0]['args'].__setitem__(0,0),lambda c:c['actual']['pending'].update(sp=0),
          lambda c:c['actual'].update(animation_release_executed=True),lambda c:c['parent_checkpoint'].update(sha256='0'*64)]
        for mutate in mutations:
            c=deepcopy(self.data['cases'][0]);mutate(c)
            with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_three_private_full_owned_retained_and_source_bindings(self):
        for c in self.data['cases']:
            payload,cp=load_verified_checkpoint(c['name'],self.phase);self.assertEqual(hex(payload['pending_eip']),cp['pending_eip'])
        with self.assertRaises(ValueError):load_verified_checkpoint('../initial',self.phase)


class InitializerTests(Checks,unittest.TestCase):phase='initializer'
class CompleteTests(Checks,unittest.TestCase):phase='complete'


if __name__=='__main__':unittest.main()
