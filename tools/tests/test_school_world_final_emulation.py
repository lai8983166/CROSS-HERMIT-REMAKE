import hashlib,json,unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from tools.school_world_final_verification import REPORTS,SHAS,PARENT,verify_case,load_verified_checkpoint
from tools.school_world_final import source_contract


class Checks:
    @classmethod
    def setUpClass(cls):cls.data=json.loads(REPORTS[cls.phase].read_bytes())

    def test_three_complete_source_original_phases(self):
        self.assertEqual(hashlib.sha256(REPORTS[self.phase].read_bytes()).hexdigest(),SHAS[self.phase]);self.assertEqual(self.data['source_contract'],source_contract())
        for c in self.data['cases']:self.assertTrue(verify_case(c,self.phase))
        self.assertEqual(self.data['second_46B470_body_completed'],self.phase=='return')
        for key in ('original_outer_task_frame_completed','original_opening_completed','persistent_write_authority'):self.assertIs(self.data[key],False)

    def test_full_main_and_suffix_owned_memory_corruption_refused(self):
        for key in ('after','tail_after'):
            for i in range(10):
                c=deepcopy(self.data['cases'][0]);r=c['actual'][key][i];r['hex']=r['hex'][:-2]+('01' if r['hex'][-2:]=='00' else '00')
                with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_wrong_original_call_stack_parent_and_outer_authority_refused(self):
        mutations=[lambda c:c['actual']['calls'].pop(),lambda c:c['parent_checkpoint'].update(sha256='0'*64),lambda c:c['actual'].update(original_opening_completed=True)]
        if self.phase=='units':mutations += [lambda c:c['actual']['tested_slots'].pop(),lambda c:c['actual']['pending'].update(sp=0)]
        else:mutations += [lambda c:c['actual']['driver_return'].update(sp=0),lambda c:c['actual']['effect_returns'].pop(),lambda c:c['actual'].update(original_outer_task_frame_completed=True)]
        for mutate in mutations:
            c=deepcopy(self.data['cases'][0]);mutate(c)
            with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_three_private_full_owned_retained_actual_continuations(self):
        for c in self.data['cases']:
            payload,cp=load_verified_checkpoint(c['name'],self.phase);self.assertEqual(hex(payload['pending_eip']),cp['pending_eip'])
        with self.assertRaises(ValueError):load_verified_checkpoint('../initial',self.phase)
        # A warm immutable-parent cache cannot authorize changed current files.
        original=Path.read_bytes
        def changed(path):return b'{}' if path==PARENT else original(path)
        with patch.object(Path,'read_bytes',changed),patch('tools.school_world_final_verification.pickle.loads') as unpickle:
            with self.assertRaises(ValueError):load_verified_checkpoint('initial',self.phase)
            unpickle.assert_not_called()


class UnitsTests(Checks,unittest.TestCase):phase='units'
class ReturnTests(Checks,unittest.TestCase):phase='return'


if __name__=='__main__':unittest.main()
