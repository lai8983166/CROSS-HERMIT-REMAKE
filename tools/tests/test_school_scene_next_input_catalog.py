import json,struct,unittest
from tools.school_scene_next_input_catalog import (
 source_catalog,native_fixture,expected_second,expected_lookup,expected_sequence,expected_progress,ROOT)
from tools.school_scene_unit_work_catalog import expected_prefix

class SceneNextInputSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.rules,cls.fixture=source_catalog(),native_fixture()

    def test_actual_complete_record_prefix_and_progress_against_source(self):
        for c in self.fixture['cases'][:3]:
            r,p=c['second_scene_record'],c['second_scene_work']
            x=expected_second(p,r['record_hex'],self.rules)
            self.assertEqual(x['record']['record_hex'],r['record_hex'])
            self.assertEqual(p['before_record_hex'],r['record_hex'])
            for key in ('work_hex','record_hex','cache_hex','controller_hex','counter','cache_slot'):
                self.assertEqual(x['prefix'][key],p[key],key)
            self.assertEqual(x['prefix']['resource_args'],p['resource_request']['args'])
            progress=c['scene_progress'];self.assertEqual(expected_progress(progress['before_hex'],1,self.rules)['after_hex'],progress['after_hex'])

    def test_all35_source_keys_queries_declared_insertions_and_boundary_semantics(self):
        d=self.fixture['declared_cache_diagnostic'];x=expected_sequence(d['seed_cache_hex'],self.rules)
        for key in ('hits','misses','final_declared_cache_hex'):self.assertEqual(x[key],d[key])
        for actual,e in zip(d['queries'],x['queries']):
            for key in ('ordinal','group','palette','return_pointer','cache_after_hex','declared_insertion','driver_cache_after_hex'):
                self.assertEqual(actual[key],e[key],(actual['ordinal'],key))
        for q in d['boundary_probes']:
            e=expected_lookup(q['cache_hex'],q['group'],q['palette'],rules=self.rules)
            for key in ('return_pointer','cache_after_hex','cache_unchanged'):self.assertEqual(e[key],q[key])
        # First-match scan must continue through unused rows; occupied values
        # are any nonzero byte and both query fields are sign-extended.
        cache=bytearray(4096);struct.pack_into('<BBHI',cache,511*8,2,128,32768,1)
        self.assertEqual(expected_lookup(cache.hex(),-32768,-128,rules=self.rules)['slot'],511)
        self.assertIsNone(expected_lookup(cache.hex(),32768,128,rules=self.rules)['slot'])

    def test_bad_cache_scalars_record_and_prefix_inputs_rejected(self):
        for value in (None,'zz','00'*4095):
            with self.assertRaises(ValueError):expected_lookup(value,4,5,rules=self.rules)
            with self.assertRaises(ValueError):expected_sequence(value,self.rules)
        for value in (True,'4',2**31,-2**31-1):
            with self.assertRaises(ValueError):expected_lookup('00'*4096,value,5,rules=self.rules)
        for value in (0,True,3,0xFFFFFFFF):
            with self.assertRaises(ValueError):expected_lookup('00'*4096,4,5,receiver=value,rules=self.rules)
        c=self.fixture['cases'][0];p=c['second_scene_work']
        with self.assertRaises(ValueError):expected_second(p,'00'*176,self.rules)
        for value in (True,-1,256):
            with self.assertRaises(ValueError):expected_prefix(p['before_record_hex'],1,p['cache_before_hex'],value,
                p['renderer'],p['allocation']['pointer'],p['classification_selector'],p['relation_hex'],self.rules['prefix'])

    def test_rules_and_frozen_exports_separate_and_exact(self):
        self.assertEqual(self.rules,json.loads((ROOT/'prototype/data/school_scene_next_input_rules.json').read_text('utf-8')))
        fixture=json.loads((ROOT/'prototype/data/school_scene_next_input_evidence.json').read_text('utf-8'))
        self.assertEqual(self.fixture,fixture);self.assertNotIn('cases',self.rules);self.assertNotIn('prefix',fixture)

if __name__=='__main__':unittest.main()
