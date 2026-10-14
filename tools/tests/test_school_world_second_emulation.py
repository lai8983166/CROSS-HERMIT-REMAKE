import hashlib,json,unittest
from copy import deepcopy
from tools.school_world_second_verification import REPORT,REPORT_SHA,verify_case,load_verified_checkpoint
from tools.school_world_second import source_contract


class NativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=json.loads(REPORT.read_bytes())

    def test_three_actual_next_world_original_controller_and_student_dispatch(self):
        self.assertEqual(hashlib.sha256(REPORT.read_bytes()).hexdigest(),REPORT_SHA)
        self.assertEqual(self.data['source_contract'],source_contract())
        self.assertEqual([r['name'] for r in self.data['cases']],['initial','student9_waiting','fifth_class'])
        for row in self.data['cases']:self.assertTrue(verify_case(row))
        for k in ('second_world_body_completed','original_opening_completed','persistent_write_authority'):self.assertIs(self.data[k],False)

    def test_complete_owned_buffers_and_wrong_action_delay_refuse(self):
        original=self.data['cases'][0]
        for i in range(19):
            bad=deepcopy(original);r=bad['actual_second_prefix']['after'][i];r['hex']=r['hex'][:-2]+('00' if r['hex'][-2:]!='00' else '01')
            with self.assertRaises(ValueError):verify_case(bad)
        bad=deepcopy(original);bad['actual_second_prefix']['delay']=0
        with self.assertRaises(ValueError):verify_case(bad)

    def test_wrong_driver_inner_stack_false_completion_or_parent_refuse(self):
        original=self.data['cases'][0]
        bad=deepcopy(original);bad['actual_second_prefix']['calls'][3]['sp']+=4
        with self.assertRaises(ValueError):verify_case(bad)
        bad=deepcopy(original);bad['actual_second_prefix']['pending']['return_va']='0x475a6a'
        with self.assertRaises(ValueError):verify_case(bad)
        bad=deepcopy(original);bad['actual_second_prefix']['180_enabled_world_updates_executed']=True
        with self.assertRaises(ValueError):verify_case(bad)
        bad=deepcopy(original);bad['parent_checkpoint']['sha256']='0'*64
        with self.assertRaises(ValueError):verify_case(bad)

    def test_private_checkpoint_preunpickle_identity_and_complete_state(self):
        for row in self.data['cases']:
            payload,cp=load_verified_checkpoint(row['name']);self.assertEqual(payload['pending_eip'],0x475D60);self.assertFalse(cp['runtime_or_original_save'])
        with self.assertRaises(ValueError):load_verified_checkpoint('../initial')


if __name__=='__main__':unittest.main()
