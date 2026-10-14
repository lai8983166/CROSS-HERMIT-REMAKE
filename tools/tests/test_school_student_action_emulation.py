import hashlib,json,unittest
from copy import deepcopy
from tools.school_student_action_verification import REPORTS,PHASE_SHAS,verify_case,load_verified_checkpoint
from tools.school_student_action import source_contract


class Checks:
    @classmethod
    def setUpClass(cls):cls.data=json.loads(REPORTS[cls.phase].read_bytes())

    def test_three_actual_full_source_native_phases(self):
        self.assertEqual(hashlib.sha256(REPORTS[self.phase].read_bytes()).hexdigest(),PHASE_SHAS[self.phase]);self.assertEqual(self.data['source_contract'],source_contract())
        self.assertEqual([r['name'] for r in self.data['cases']],['initial','student9_waiting','fifth_class'])
        for row in self.data['cases']:self.assertTrue(verify_case(row,self.phase))
        for k in ('full_unit_or_world_completed','original_opening_completed','persistent_write_authority'):self.assertIs(self.data[k],False)

    def test_entire_work_pool_control_task_and_pointer_corruption_refuse(self):
        original=self.data['cases'][0]
        for i in range(5):
            bad=deepcopy(original);r=bad['actual']['after'][i];r['hex']=r['hex'][:-2]+('00' if r['hex'][-2:]!='00' else '01')
            with self.assertRaises(ValueError):verify_case(bad,self.phase)

    def test_wrong_source_metadata_boundary_scope_and_parent_refuse(self):
        original=self.data['cases'][0]
        bad=deepcopy(original);bad['actual']['inputs']['metadata_bindings'][0]['metadata_sha256']='0'*64
        with self.assertRaises(ValueError):verify_case(bad,self.phase)
        bad=deepcopy(original);bad['actual']['pending']['sp']+=4
        with self.assertRaises(ValueError):verify_case(bad,self.phase)
        bad=deepcopy(original);bad['actual']['full_unit_or_world_completed']=True
        with self.assertRaises(ValueError):verify_case(bad,self.phase)
        bad=deepcopy(original);bad['parent_checkpoint']['sha256']='0'*64
        with self.assertRaises(ValueError):verify_case(bad,self.phase)

    def test_precise_original_call_or_verified_private_state(self):
        if self.phase=='binding':
            bad=deepcopy(self.data['cases'][0]);bad['actual']['calls']=[r for r in bad['actual']['calls'] if r['va']!='0x465040']
            with self.assertRaises(ValueError):verify_case(bad,self.phase)
        else:
            for row in self.data['cases']:
                payload,cp=load_verified_checkpoint(row['name'],self.phase);self.assertEqual(hex(payload['pending_eip']),cp['pending_eip']);self.assertFalse(cp['runtime_or_original_save'])
            with self.assertRaises(ValueError):load_verified_checkpoint('../initial',self.phase)


class BindingTests(Checks,unittest.TestCase):phase='binding'
class InitializerTests(Checks,unittest.TestCase):phase='initializer'
class AnimationTests(Checks,unittest.TestCase):phase='animation'


if __name__=='__main__':unittest.main()
