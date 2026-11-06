import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from tools import terminal_unit_frontends_proof as proof


class SourceAuthenticationTests(unittest.TestCase):
    def setUp(self):
        temporary=tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root=Path(temporary.name)
        self.prefix=self.root/'analysis/source-fixture'
        self.prefix.parent.mkdir()
        root_patch=patch.object(proof.corpus,'ROOT',self.root)
        root_patch.start();self.addCleanup(root_patch.stop)
        base_patch=patch.object(proof.corpus,'fixed_base',return_value=({},{}))
        base_patch.start();self.addCleanup(base_patch.stop)
        def identity(path):
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(b'bounded authentic fixture')
            return proof.corpus.identity(path)
        implementation={}
        for name in ('corpus','emulation','delta','trace','records','images','minimap'):
            path=self.root/'tools'/('terminal_unit_frontends_'+name+'.py')
            row=identity(path);implementation[row['path']]=row
        artifacts=[identity(Path(str(self.prefix)+suffix)) for suffix in ('.chunks.zip','.delta.jsonl.gz')]
        helpers={}
        for kind,suffix,name in (('CRT','crt','terminal_unit_frontends_crt_platform.cs'),
                                ('GPU','gpu','terminal_unit_frontends_d3d8_platform.cs')):
            src=identity(self.root/'tools'/name)
            binary=identity(self.root/'.venv-audit'/('source-fixture-0-'+suffix+'.exe'))
            helpers[kind]=dict(source=src['path'],source_sha256=src['sha256'],
                               helper_sha256=binary['sha256'],machine=0x14C)
        self.data=dict(source_execution_complete=True,implementation_unchanged=True,
            implementation_start=implementation,implementation_end=copy.deepcopy(implementation),
            artifacts=artifacts,fixed_base={},helper_build=helpers,
            case=proof.source.previous.overlay.parent.corpus()[0])

    def check(self,data):
        Path(str(self.prefix)+'.process.json').write_text(json.dumps(data),encoding='utf8')
        return proof.authenticate_source(self.prefix)

    def test_actual_source_pair_and_both_retained_helpers_are_authenticated(self):
        data,_=self.check(self.data)
        self.assertEqual(set(data['authenticated_helpers']),{'CRT','GPU'})

    def test_empty_duplicate_and_foreign_artifact_lists_are_rejected(self):
        for kind in ('empty','duplicate','foreign'):
            data=copy.deepcopy(self.data)
            if kind=='empty':data['artifacts']=[]
            elif kind=='duplicate':data['artifacts'][1]=data['artifacts'][0]
            else:data['artifacts'][0]['path']='analysis/another.chunks.zip'
            with self.subTest(kind=kind),self.assertRaises(ValueError):self.check(data)

    def test_helper_source_and_binary_sha_tampering_is_rejected(self):
        for field in ('source_sha256','helper_sha256'):
            data=copy.deepcopy(self.data)
            data['helper_build']['CRT'][field]='0'*64
            with self.subTest(field=field),self.assertRaises(ValueError):self.check(data)

    def test_missing_principal_source_and_changed_end_identity_are_rejected(self):
        for kind in ('missing','changed'):
            data=copy.deepcopy(self.data)
            key='tools/terminal_unit_frontends_trace.py'
            if kind=='missing':del data['implementation_start'][key]
            else:data['implementation_end'][key]['sha256']='0'*64
            with self.subTest(kind=kind),self.assertRaises(ValueError):self.check(data)

    def checkpoint_fixture(self):
        data,process=self.check(self.data)
        checker=dict(data['implementation_start'])
        for name in ('proof','verification','retries','platform_verification','inputs_verification',
                     'other_platform_verification','projection_verification'):
            path=self.root/'tools'/('terminal_unit_frontends_'+name+'.py')
            path.write_bytes(b'unchanged independent checker')
            checker[path.relative_to(self.root).as_posix()]=proof.corpus.identity(path)
        state=dict(transactions=[{}],final_trace={'instructions':1},final_memory_digest={'bytes':4096})
        source_proof=dict(transactions=1,final_trace=state['final_trace'],final_memory=state['final_memory_digest'],
            complete_CPU_and_mapped_memory_compared_at_every_transaction=True,
            all_cumulative_original_digests_reproduced=True,canonical_trace_matches_source=True,
            original_wait_reached=True,wait_body_executed=False,outer_result_consumed=False,
            complete_battle_exit=False)
        old=dict(case_index=0,implementation_unchanged=True,source_process=process,
                 source_artifacts=data['artifacts'],source_helpers=data['authenticated_helpers'],
                 implementation_start=checker,implementation_end=copy.deepcopy(checker),
                 source_proof=source_proof)
        return data,process,dict(unit_frontends=dict(execution=state)),old

    def resume(self,data,process,row,old,archive=None,wrong_sha=False):
        path=self.root/'analysis/completed-source-proof.json'
        path.write_text(json.dumps(old),encoding='utf8')
        sha=proof.corpus.identity(path)['sha256']
        return proof.resume_source_proof(path,'0'*64 if wrong_sha else sha,data,process,row,0,archive)

    def test_completed_source_replay_can_resume_only_with_exact_binding_and_final_state(self):
        data,process,row,old=self.checkpoint_fixture()
        result,identity=self.resume(data,process,row,old)
        self.assertEqual(result,old['source_proof'])
        self.assertFalse(identity['source_replay_reexecuted'])
        for kind in ('SHA','source','artifacts','complete'):
            bad=copy.deepcopy(old)
            if kind=='source':bad['source_process']['sha256']='0'*64
            elif kind=='artifacts':bad['source_artifacts']=[]
            elif kind=='complete':bad['source_proof']['original_wait_reached']=False
            with self.subTest(kind=kind),self.assertRaises(ValueError):
                self.resume(data,process,row,bad,wrong_sha=kind=='SHA')

    def test_changed_verification_module_cannot_reuse_a_source_proof(self):
        data,process,row,old=self.checkpoint_fixture()
        (self.root/'tools/terminal_unit_frontends_trace.py').write_bytes(b'changed checker')
        with self.assertRaises(ValueError):self.resume(data,process,row,old)

    def test_changed_orchestrator_requires_its_exact_historical_bytes(self):
        data,process,row,old=self.checkpoint_fixture()
        path=self.root/'tools/terminal_unit_frontends_proof.py'
        path.write_bytes(b'old orchestration')
        saved=proof.corpus.identity(path)
        old['implementation_start'][saved['path']]=saved
        old['implementation_end'][saved['path']]=saved
        archive=self.root/'analysis/old-orchestrator.json'
        archive.write_text(json.dumps(dict(**saved,source_utf8='old orchestration')),encoding='utf8')
        path.write_bytes(b'new orchestration')
        with self.assertRaises(ValueError):self.resume(data,process,row,old)
        result,identity=self.resume(data,process,row,old,archive)
        self.assertEqual(result,old['source_proof'])
        self.assertIsNotNone(identity['historical_orchestrator'])
        altered=json.loads(archive.read_text(encoding='utf8'));altered['source_utf8']='wrong'
        archive.write_text(json.dumps(altered),encoding='utf8')
        with self.assertRaises(ValueError):self.resume(data,process,row,old,archive)
