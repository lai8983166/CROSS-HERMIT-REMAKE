import gzip,hashlib,json,unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from tools.school_world_script_verification import REPORTS,SHAS,PARENT,PREVIOUS,verify_case,load_verified_checkpoint
from tools.school_world_script import SOURCE,SCRIPT,source_contract
from tools.school_world_script_inputs import INPUTS
from tools.school_world_life_codec import pack,unpack

class Checks:
    @classmethod
    def setUpClass(cls):cls.data=json.loads(gzip.decompress(REPORTS[cls.phase].read_bytes()))

    def test_all_source_native_cases_full_calls_bytes_and_CPU(self):
        self.assertEqual(hashlib.sha256(REPORTS[self.phase].read_bytes()).hexdigest(),SHAS[self.phase]);self.assertEqual(self.data['source_contract'],source_contract());self.assertEqual(len(self.data['cases']),3)
        for c in self.data['cases']:self.assertTrue(verify_case(c,self.phase))
        for k in ('original_outer_task_frame_completed','playback_vm_executed','persistent_write_authority'):self.assertIs(self.data[k],False)

    def test_every_owned_byte_region_corruption_refused(self):
        a=unpack(self.data['cases'][0]['actual']);parts=[(None,'after')] if self.phase in ('preflight','binding') else [('prefix','after'),('units','after'),('suffix','tail_after')]
        for part,key in parts:
            for i in range(len((a[part] if part else a)[key])):
                c=deepcopy(self.data['cases'][0]);x=unpack(c['actual']);r=(x[part] if part else x)[key][i];r['hex']=r['hex'][:-2]+('01' if r['hex'][-2:]=='00' else '00');c['actual']=pack(x)
                with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_natural_calls_return_authority_and_provenance_refused(self):
        mutations=[lambda c:c['parent_checkpoint'].update(sha256='0'*64)]
        if self.phase in PREVIOUS:mutations.append(lambda c:c['prior_checkpoint'].update(sha256='0'*64))
        if self.phase in ('preflight','binding'):
            mutations += [lambda c:c['actual']['calls'].pop(),lambda c:c['actual']['calls'][0].update(sp=0),lambda c:c['actual']['pending'].update(eax=9),lambda c:c['actual'].update(owned_bodies_stubbed=True)]
            if self.phase=='preflight':mutations += [lambda c:c['actual']['commands'][0].update(opcode=0),lambda c:c['actual']['adapters'][0].update(result=0)]
            else:mutations.append(lambda c:c['actual']['binding_observation'].update(args=[0]*7))
        else:mutations += [lambda c:c['actual']['units']['calls'].pop(),lambda c:c['actual']['suffix']['driver_return'].update(sp=0)]
        for mutate in mutations:
            c=deepcopy(self.data['cases'][0]);mutate(c)
            with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_private_cpu_full_memory_and_fresh_identity_before_unpickle(self):
        for c in self.data['cases']:
            payload,cp=load_verified_checkpoint(c['name'],self.phase);self.assertEqual(hex(payload['pending_eip']),cp['pending_eip'])
        with self.assertRaises(ValueError):load_verified_checkpoint('../initial',self.phase)
        original=Path.read_bytes
        for identity in (SOURCE,SCRIPT,INPUTS,PARENT,REPORTS[self.phase]):
            def changed(path):return b'{}' if path==identity else original(path)
            with patch.object(Path,'read_bytes',changed),patch('tools.school_world_script_verification.pickle.loads') as unpickle:
                with self.assertRaises(ValueError):load_verified_checkpoint('initial',self.phase)
                self.assertEqual(unpickle.call_count,0)

class PreflightTests(Checks,unittest.TestCase):phase='preflight'
class BindingTests(Checks,unittest.TestCase):phase='binding'

if __name__=='__main__':unittest.main()
