import hashlib,json,unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from tools.school_world_next_verification import REPORTS,SHAS,INPUTS,verify_case,load_verified_checkpoint
from tools.school_world_next import source_contract


class Checks:
    @classmethod
    def setUpClass(cls):cls.data=json.loads(REPORTS[cls.phase].read_bytes())

    def test_three_complete_source_native_cases(self):
        self.assertEqual(hashlib.sha256(REPORTS[self.phase].read_bytes()).hexdigest(),SHAS[self.phase]);self.assertEqual(self.data['source_contract'],source_contract())
        self.assertEqual(len(self.data['cases']),3)
        for c in self.data['cases']:self.assertTrue(verify_case(c,self.phase))
        for k in ('third_world_completed','original_opening_completed','persistent_write_authority'):self.assertIs(self.data[k],False)

    def test_complete_owned_memory_corruption_rejected(self):
        for i in range(len(self.data['cases'][0]['actual']['after'])):
            c=deepcopy(self.data['cases'][0]);r=c['actual']['after'][i];r['hex']=r['hex'][:-2]+('01' if r['hex'][-2:]=='00' else '00')
            with self.assertRaises(ValueError):verify_case(c,self.phase)
        if self.phase=='unit':
            c=deepcopy(self.data['cases'][0]);r=c['full_after'][1];r['hex']=r['hex'][:-2]+('01' if r['hex'][-2:]=='00' else '00')
            with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_call_stack_parent_scope_or_restoration_corruption_rejected(self):
        mutations=[lambda c:c['actual']['calls'].pop(),lambda c:c['actual']['calls'][0].update(sp=0),lambda c:c['parent_checkpoint'].update(sha256='0'*64)]
        if self.phase=='prefix':mutations += [lambda c:c['actual'].update(third_world_completed=True),lambda c:c['clearing_probes']['rows'][0]['restoration'].update(complete_owned_input_restored=False)]
        else:mutations += [lambda c:c['actual_tail']['pending'].update(sp=0),lambda c:c['actual'].update(allocation_executed=True)]
        for mutate in mutations:
            c=deepcopy(self.data['cases'][0]);mutate(c)
            with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_private_full_state_and_current_sha_before_unpickle(self):
        for c in self.data['cases']:
            payload,cp=load_verified_checkpoint(c['name'],self.phase);self.assertEqual(hex(payload['pending_eip']),cp['pending_eip'])
        with self.assertRaises(ValueError):load_verified_checkpoint('../initial',self.phase)
        original=Path.read_bytes
        def changed(path):return b'{}' if path==INPUTS else original(path)
        with patch.object(Path,'read_bytes',changed),patch('tools.school_world_next_verification.pickle.loads') as unpickle:
            with self.assertRaises(ValueError):load_verified_checkpoint('initial',self.phase)
            self.assertEqual(unpickle.call_count,0)


class PrefixTests(Checks,unittest.TestCase):phase='prefix'
class UnitTests(Checks,unittest.TestCase):phase='unit'


if __name__=='__main__':unittest.main()
