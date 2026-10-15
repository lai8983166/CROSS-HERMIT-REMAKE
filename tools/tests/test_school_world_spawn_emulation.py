import gzip,hashlib,json,unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch
from tools.school_world_spawn_verification import REPORTS,SHAS,PARENT,PARENT_INPUTS,PHASES,PREVIOUS,verify_case,load_verified_checkpoint
from tools.school_world_spawn import source_contract
from tools.school_world_life_codec import pack,unpack,MARKER


class Checks:
    @classmethod
    def setUpClass(cls):cls.data=json.loads(gzip.decompress(REPORTS[cls.phase].read_bytes()))

    def test_all_source_native_worlds_full_bytes_calls_and_natural_returns(self):
        self.assertEqual(hashlib.sha256(REPORTS[self.phase].read_bytes()).hexdigest(),SHAS[self.phase]);self.assertEqual(self.data['source_contract'],source_contract());self.assertEqual(len(self.data['cases']),3)
        self.assertEqual((self.data['schema_version'],self.data['encoding']),(2,'full-hex-zlib-v1'))
        for c in self.data['cases']:self.assertTrue(verify_case(c,self.phase))
        for key in ('original_outer_task_frame_completed','original_opening_completed','audio_backend_executed','persistent_write_authority'):self.assertIs(self.data[key],False)

    def test_each_complete_owned_region_corruption_refused(self):
        for part,key in (('prefix','after'),('units','after'),('suffix','tail_after')):
            for i in range(len(self.data['cases'][0]['worlds'][0][part][key])):
                c=deepcopy(self.data['cases'][0]);w=unpack(c['worlds'][0]);r=w[part][key][i];r['hex']=r['hex'][:-2]+('01' if r['hex'][-2:]=='00' else '00');c['worlds'][0]=pack(w)
                with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_skipped_world_call_lifecycle_or_provenance_refused(self):
        mutations=[lambda c:c['worlds'].pop(0),lambda c:c['worlds'][0]['units']['calls'].pop(),lambda c:c['worlds'][-1]['suffix']['driver_return'].update(sp=0),lambda c:c['parent_checkpoint'].update(sha256='0'*64),lambda c:c['worlds'][0]['units'].update(attached_node_free_executed=True)]
        if self.phase in PREVIOUS:mutations.append(lambda c:c['prior_checkpoint'].update(sha256='0'*64))
        if self.phase=='spawn':
            mutations += [lambda c:c['worlds'][0]['units']['spawn_returns'][0].update(eax=0),lambda c:c['worlds'][0]['units']['spawn_returns'][1].update(eax=1),lambda c:next(a for a in c['worlds'][0]['units']['calls'] if a['va']=='0x56cec0').update(args=[0,0,88])]
        if self.phase=='tail':mutations.append(lambda c:next(a for a in c['worlds'][-1]['units']['calls'] if a['va']=='0x40b6a0').update(args=[0]))
        for mutate in mutations:
            c=deepcopy(self.data['cases'][0]);mutate(c)
            with self.assertRaises(ValueError):verify_case(c,self.phase)

    def test_complete_private_cpu_memory_and_fresh_report_before_unpickle(self):
        for c in self.data['cases']:
            payload,cp=load_verified_checkpoint(c['name'],self.phase);self.assertEqual(hex(payload['pending_eip']),cp['pending_eip'])
        with self.assertRaises(ValueError):load_verified_checkpoint('../initial',self.phase)
        original=Path.read_bytes;identities=[PARENT,PARENT_INPUTS,REPORTS[self.phase]]
        if self.phase in PREVIOUS:identities.append(REPORTS[PREVIOUS[self.phase]])
        for identity in identities:
            def changed(path):return b'{}' if path==identity else original(path)
            with patch.object(Path,'read_bytes',changed),patch('tools.school_world_spawn_verification.pickle.loads') as unpickle:
                with self.assertRaises(ValueError):load_verified_checkpoint('initial',self.phase)
                self.assertEqual(unpickle.call_count,0)


class FramesTests(Checks,unittest.TestCase):phase='frames'
class SpawnTests(Checks,unittest.TestCase):phase='spawn'
class TailTests(Checks,unittest.TestCase):phase='tail'


if __name__=='__main__':unittest.main()
