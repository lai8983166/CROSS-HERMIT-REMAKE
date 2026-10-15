import gzip,hashlib,json,unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from tools.school_world_resume_verification import REPORTS,SHAS,PARENT,PREVIOUS,verify_case,load_verified_checkpoint
from tools.school_world_resume import source_contract,SOURCE,SCRIPT
from tools.school_world_life_codec import pack,unpack

class Checks:
    @classmethod
    def setUpClass(cls):cls.data=json.loads(gzip.decompress(REPORTS[cls.phase].read_bytes()))

    def test_all_original_cases_full_bytes_calls_and_cpu(self):
        self.assertEqual(hashlib.sha256(REPORTS[self.phase].read_bytes()).hexdigest(),SHAS[self.phase]);self.assertEqual(self.data['source_contract'],source_contract());self.assertEqual(len(self.data['cases']),3)
        self.assertEqual((self.data['schema_version'],self.data['encoding']),(2,'full-hex-zlib-v1'));self.assertEqual(self.data['phase'],self.phase)
        for c in self.data['cases']:self.assertTrue(verify_case(c,self.phase))
        for k in ('original_outer_task_frame_completed','original_opening_completed','preflight_body_executed','persistent_write_authority'):self.assertIs(self.data[k],False)
        self.assertIs(self.data['countdown_180_decrements_completed'],True)

    def test_every_owned_region_corruption_refused(self):
        a=unpack(self.data['cases'][0]['actual']);parts=[(None,'after')] if self.phase=='entry' else [('prefix','after'),('units','after'),('suffix','tail_after')]
        for part,key in parts:
            for i in range(len((a[part] if part else a)[key])):
                c=deepcopy(self.data['cases'][0]);actual=unpack(c['actual']);r=(actual[part] if part else actual)[key][i];r['hex']=r['hex'][:-2]+('01' if r['hex'][-2:]=='00' else '00');c['actual']=pack(actual)
                with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_calls_boundary_authority_and_provenance_refused(self):
        mutations=[lambda c:c['parent_checkpoint'].update(sha256='0'*64)]
        if self.phase in PREVIOUS:mutations.append(lambda c:c['prior_checkpoint'].update(sha256='0'*64))
        if self.phase=='entry':mutations += [lambda c:c['actual']['calls'].pop(),lambda c:c['actual']['pending'].update(first_instruction_executed=True),lambda c:c['actual']['pending'].update(args=[1,0]),lambda c:c['actual']['inputs'].update(busy=1),lambda c:c['actual']['inputs'].update(script_sha256='0'*64)]
        else:
            mutations += [lambda c:c['actual']['units']['calls'].pop(),lambda c:c['actual']['suffix']['driver_return'].update(sp=0),lambda c:c['actual']['prefix'].update(action=0 if self.phase=='zero' else 1)]
            if self.phase=='zero':mutations.append(lambda c:c['actual']['units']['mode_returns'][0].update(eax=1))
            else:mutations.append(lambda c:c['actual']['units']['units'][0].update(animation_frozen=False))
        for mutate in mutations:
            c=deepcopy(self.data['cases'][0]);mutate(c)
            with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_private_cpu_memory_and_fresh_sha_before_unpickle(self):
        for c in self.data['cases']:
            payload,cp=load_verified_checkpoint(c['name'],self.phase);self.assertEqual(hex(payload['pending_eip']),cp['pending_eip'])
        with self.assertRaises(ValueError):load_verified_checkpoint('../initial',self.phase)
        original=Path.read_bytes;identities=[SOURCE,SCRIPT,PARENT,REPORTS[self.phase]]
        if self.phase in PREVIOUS:identities.append(REPORTS[PREVIOUS[self.phase]])
        for identity in identities:
            def changed(path):return b'{}' if path==identity else original(path)
            with patch.object(Path,'read_bytes',changed),patch('tools.school_world_resume_verification.pickle.loads') as unpickle:
                with self.assertRaises(ValueError):load_verified_checkpoint('initial',self.phase)
                self.assertEqual(unpickle.call_count,0)

class ZeroTests(Checks,unittest.TestCase):phase='zero'

if __name__=='__main__':unittest.main()
