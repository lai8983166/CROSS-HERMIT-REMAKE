import gzip,hashlib,json,unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from tools.school_task_cycle import SOURCE,PHASES,source_contract
from tools.school_task_cycle_verification import REPORTS,SHAS,PARENT,verify_case,load_verified_checkpoint
from tools.school_world_life_codec import pack,unpack

class Checks:
    @classmethod
    def setUpClass(cls):cls.data=json.loads(gzip.decompress(REPORTS[cls.phase].read_bytes()))

    def test_three_cases_full_source_calls_bytes_CPU_and_scope(self):
        self.assertEqual(hashlib.sha256(REPORTS[self.phase].read_bytes()).hexdigest(),SHAS[self.phase]);self.assertEqual(self.data['source_contract'],source_contract());self.assertEqual(len(self.data['cases']),3)
        for c in self.data['cases']:self.assertTrue(verify_case(c,self.phase))
        for k in ('normal_VM_executed','live_input_sampled','full_outer_frame_executed','persistent_write_authority'):self.assertIs(self.data[k],False)

    def test_every_owned_region_corruption_refused(self):
        c=self.data['cases'][0];a=unpack(c['actual'])
        for i in range(len(a['after'])):
            bad=deepcopy(c);x=unpack(bad['actual']);r=x['after'][i];r['hex']=r['hex'][:-2]+('01' if r['hex'][-2:]=='00' else '00');bad['actual']=pack(x)
            with self.assertRaises(ValueError):verify_case(bad,self.phase)

    def test_calls_adapter_driver_authority_CPU_and_parent_mutations_refused(self):
        mutations=[lambda c:c['prior_checkpoint'].update(sha256='0'*64),lambda c:c['continuation_checkpoint'].update(path='../bad.pkl')]
        changes=[lambda a:a['calls'].pop(),lambda a:a['calls'][1].update(sp=0),lambda a:a['calls'][0].update(receiver=0),lambda a:a['adapters'][0].update(result=1),lambda a:a['adapters'][0].update(args=[1]),lambda a:a['CPU'].update(EAX=9),lambda a:a.update(owned_bodies_stubbed=True),lambda a:a.update(normal_VM_executed=True),lambda a:a.update(live_input_sampled=True),lambda a:a['imports'].update(ime_target=1),lambda a:a.update(retained_bytes=0),lambda a:a['retained_ranges'].pop(),lambda a:a['retained_ranges'][0].update(sha256='0'*64)]
        if self.phase=='vm_entry':changes.append(lambda a:a['pending'].update(first_instruction_executed=True))
        for mutate in mutations:
            c=deepcopy(self.data['cases'][0]);mutate(c)
            with self.assertRaises(ValueError):verify_case(c,self.phase)
        for mutate in changes:
            c=deepcopy(self.data['cases'][0]);a=unpack(c['actual']);mutate(a);c['actual']=pack(a)
            with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_private_CPU_memory_and_fresh_identity_before_unpickle(self):
        for c in self.data['cases']:
            payload,cp=load_verified_checkpoint(c['name'],self.phase);self.assertEqual(hex(payload['pending_eip']),cp['pending_eip'])
        with self.assertRaises(ValueError):load_verified_checkpoint('../initial',self.phase)
        original=Path.read_bytes
        for identity in (SOURCE,PARENT,REPORTS[self.phase]):
            def changed(path):return b'{}' if path==identity else original(path)
            with patch.object(Path,'read_bytes',changed),patch('tools.school_task_cycle_verification.pickle.loads') as unpickle:
                with self.assertRaises(ValueError):load_verified_checkpoint('initial',self.phase)
                self.assertEqual(unpickle.call_count,0)

class Reset1Tests(Checks,unittest.TestCase):phase='reset1'
class Phase2Tests(Checks,unittest.TestCase):phase='phase2'
class Reset2Tests(Checks,unittest.TestCase):phase='reset2'
class VMEntryTests(Checks,unittest.TestCase):phase='vm_entry'

if __name__=='__main__':unittest.main()
