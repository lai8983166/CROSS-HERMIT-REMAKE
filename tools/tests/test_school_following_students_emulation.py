import hashlib,json,unittest
from copy import deepcopy
from tools.school_following_students_verification import REPORT,REPORT_SHA,verify_case,load_verified_checkpoint
from tools.school_following_students import source_contract


class FollowingStudentNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=json.loads(REPORT.read_bytes())

    def test_all_actual_friendly_returns_and_complete_source_calls(self):
        self.assertEqual(hashlib.sha256(REPORT.read_bytes()).hexdigest(),REPORT_SHA);self.assertEqual(self.data['source_contract'],source_contract())
        self.assertEqual([c['actual']['friendly_unit_updates_completed'] for c in self.data['cases']],[2,1,1])
        for c in self.data['cases']:self.assertTrue(verify_case(c))
        for k in ('world_completed','original_opening_completed','persistent_write_authority'):self.assertIs(self.data[k],False)

    def test_all_owned_memory_corruptions_refused(self):
        for i in range(10):
            c=deepcopy(self.data['cases'][0]);r=c['actual']['after'][i];r['hex']=r['hex'][:-2]+('01' if r['hex'][-2:]=='00' else '00')
            with self.assertRaises(ValueError):verify_case(c)

    def test_wrong_original_calls_loop_stack_scope_and_parent_refused(self):
        mutations=[lambda c:c['actual']['calls'][12]['args'].__setitem__(2,2109),lambda c:c['actual']['tested_slots'].pop(),
          lambda c:c['actual']['pending'].update(sp=0),lambda c:c['actual'].update(world_completed=True),
          lambda c:c['parent_checkpoint'].update(sha256='0'*64)]
        for mutate in mutations:
            c=deepcopy(self.data['cases'][0]);mutate(c)
            with self.assertRaises(ValueError):verify_case(c)

    def test_three_private_full_owned_and_retained_checkpoints(self):
        for c in self.data['cases']:
            payload,cp=load_verified_checkpoint(c['name']);self.assertEqual(hex(payload['pending_eip']),cp['pending_eip'])
        with self.assertRaises(ValueError):load_verified_checkpoint('../initial')


if __name__=='__main__':unittest.main()
