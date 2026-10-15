import gzip,hashlib,json,unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from tools.school_world_frames_verification import REPORTS,SHAS,PARENT_INPUTS,verify_case,load_verified_checkpoint
from tools.school_world_frames import source_contract


class Checks:
    @classmethod
    def setUpClass(cls):cls.data=json.loads(gzip.decompress(REPORTS[cls.phase].read_bytes()))

    def test_three_complete_consecutive_source_native_cases(self):
        self.assertEqual(hashlib.sha256(REPORTS[self.phase].read_bytes()).hexdigest(),SHAS[self.phase]);self.assertEqual(self.data['source_contract'],source_contract());self.assertEqual(len(self.data['cases']),3)
        for c in self.data['cases']:self.assertTrue(verify_case(c,self.phase))
        for k in ('original_outer_task_frame_completed','original_opening_completed','audio_backend_executed','persistent_write_authority'):self.assertIs(self.data[k],False)

    def test_complete_phase_owned_bytes_corruption_rejected(self):
        for part,key in (('prefix','after'),('units','after'),('suffix','tail_after')):
            for i in range(len(self.data['cases'][0]['worlds'][0][part][key])):
                c=deepcopy(self.data['cases'][0]);r=c['worlds'][0][part][key][i];r['hex']=r['hex'][:-2]+('01' if r['hex'][-2:]=='00' else '00')
                with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_skipped_world_call_parent_stack_or_backend_authority_rejected(self):
        mutations=[lambda c:c['worlds'][0]['units']['calls'].pop(),lambda c:c['worlds'][0]['suffix']['driver_return'].update(sp=0),lambda c:c['parent_checkpoint'].update(sha256='0'*64),lambda c:c['worlds'][0]['units'].update(audio_backend_executed=True)]
        if self.phase=='early':mutations.append(lambda c:c['worlds'].pop(0))
        else:mutations.extend([lambda c:c['early_checkpoint'].update(sha256='0'*64),lambda c:c['worlds'].pop(0)])
        for mutate in mutations:
            c=deepcopy(self.data['cases'][0]);mutate(c)
            with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_private_complete_cpu_owned_retained_and_fresh_sha(self):
        for c in self.data['cases']:
            payload,cp=load_verified_checkpoint(c['name'],self.phase);self.assertEqual(hex(payload['pending_eip']),cp['pending_eip'])
        with self.assertRaises(ValueError):load_verified_checkpoint('../initial',self.phase)
        original=Path.read_bytes
        def changed(path):return b'{}' if path==PARENT_INPUTS else original(path)
        with patch.object(Path,'read_bytes',changed),patch('tools.school_world_frames_verification.pickle.loads') as unpickle:
            with self.assertRaises(ValueError):load_verified_checkpoint('initial',self.phase)
            self.assertEqual(unpickle.call_count,0)


class EarlyTests(Checks,unittest.TestCase):phase='early'
class LateTests(Checks,unittest.TestCase):phase='late'


if __name__=='__main__':unittest.main()
