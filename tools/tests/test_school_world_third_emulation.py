import hashlib,json,unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from tools.school_world_third_verification import REPORTS,SHAS,INPUTS,verify_case,load_verified_checkpoint
from tools.school_world_third import source_contract


class Checks:
    @classmethod
    def setUpClass(cls):cls.data=json.loads(REPORTS[cls.phase].read_bytes())

    def test_three_complete_original_source_cases(self):
        self.assertEqual(hashlib.sha256(REPORTS[self.phase].read_bytes()).hexdigest(),SHAS[self.phase]);self.assertEqual(self.data['source_contract'],source_contract());self.assertEqual(len(self.data['cases']),3)
        for c in self.data['cases']:self.assertTrue(verify_case(c,self.phase))
        self.assertEqual(self.data['third_46B470_body_completed'],self.phase=='return')
        for k in ('original_outer_task_frame_completed','original_opening_completed','persistent_write_authority'):self.assertIs(self.data[k],False)

    def test_full_main_suffix_owned_memory_corruption_rejected(self):
        for key in ('after','tail_after'):
            for i in range(10):
                c=deepcopy(self.data['cases'][0]);r=c['actual'][key][i];r['hex']=r['hex'][:-2]+('01' if r['hex'][-2:]=='00' else '00')
                with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_call_stack_parent_order_and_authority_corruption_rejected(self):
        mutations=[lambda c:c['actual']['calls'].pop(),lambda c:c['actual']['calls'][0].update(sp=0),lambda c:c['parent_checkpoint'].update(sha256='0'*64)]
        if self.phase=='units':mutations += [lambda c:c['actual']['unit_entries'].pop(),lambda c:c['actual']['tested_slots'].pop(),lambda c:c['actual'].update(attached_node_free_executed=True)]
        else:mutations += [lambda c:c['actual']['driver_return'].update(sp=0),lambda c:c['actual']['effect_returns'].pop(),lambda c:c['actual'].update(original_outer_task_frame_completed=True)]
        for mutate in mutations:
            c=deepcopy(self.data['cases'][0]);mutate(c)
            with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_private_full_owned_retained_state_and_fresh_sha(self):
        for c in self.data['cases']:
            payload,cp=load_verified_checkpoint(c['name'],self.phase);self.assertEqual(hex(payload['pending_eip']),cp['pending_eip'])
        with self.assertRaises(ValueError):load_verified_checkpoint('../initial',self.phase)
        original=Path.read_bytes
        def changed(path):return b'{}' if path==INPUTS else original(path)
        with patch.object(Path,'read_bytes',changed),patch('tools.school_world_third_verification.pickle.loads') as unpickle:
            with self.assertRaises(ValueError):load_verified_checkpoint('initial',self.phase)
            self.assertEqual(unpickle.call_count,0)


class UnitsTests(Checks,unittest.TestCase):phase='units'
class ReturnTests(Checks,unittest.TestCase):phase='return'


if __name__=='__main__':unittest.main()
