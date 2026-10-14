import json
import unittest
from copy import deepcopy
from tools.school_world_mode_emulation import ROOT,PARENT,PARENT_SHA
from tools.school_world_mode import source_contract
from tools.school_world_mode_verification import verify_case
import hashlib


class WorldModeNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((ROOT/'analysis/school-world-mode-native-v6-20261014.json').read_text(encoding='utf-8'))
        cls.parent=json.loads(PARENT.read_bytes())

    def test_three_actual_nested_prefixes_and_twenty_one_restored_probes(self):
        self.assertEqual(self.report['source_contract'],source_contract())
        self.assertEqual(self.report['parent_sha256'],hashlib.sha256(PARENT.read_bytes()).hexdigest())
        self.assertEqual(self.report['parent_sha256'],PARENT_SHA)
        self.assertEqual([c['name'] for c in self.report['cases']],['initial','student9_waiting','fifth_class'])
        for key in ('world_tick_completed','original_opening_completed','persistent_write_authority'):
            self.assertIs(self.report[key],False)
        for case,parent in zip(self.report['cases'],self.parent['cases']):self.assertTrue(verify_case(case,parent))

    def test_wrong_full_regions_stack_or_scope_refuse(self):
        original=self.report['cases'][0];parent=self.parent['cases'][0]
        for field in ['control','map_flags','task_flags']:
            bad=deepcopy(original);row=next(r for r in bad['actual_world_prefix']['after'] if r['name']==field)
            data=bytearray.fromhex(row['hex']);data[-1]^=1;row['hex']=data.hex()
            with self.assertRaises(ValueError):verify_case(bad,parent)
        for field,value in [('full_world_tick_executed',True),('mode_store_bodies_stubbed',True),('opening_completion',1),('retained_ranges_unchanged',False)]:
            bad=deepcopy(original);bad['actual_world_prefix'][field]=value
            with self.assertRaises(ValueError):verify_case(bad,parent)
        bad=deepcopy(original);bad['actual_world_prefix']['pending']['return_va']='0x0'
        with self.assertRaises(ValueError):verify_case(bad,parent)

    def test_wrong_probe_before_after_leaf_calls_or_restoration_refuse(self):
        original=self.report['cases'][0];parent=self.parent['cases'][0]
        for kind in ['before','after']:
            bad=deepcopy(original);bad['declared_mode_probes'][2][kind][1]['hex']='00000000' if kind=='before' else '01010101'
            with self.assertRaises(ValueError):verify_case(bad,parent)
        for field in ['cpu_after_sha256','stack_after_sha256']:
            bad=deepcopy(original);bad['declared_mode_probes'][2]['restoration'][field]='0'*64
            with self.assertRaises(ValueError):verify_case(bad,parent)
        bad=deepcopy(original);bad['declared_mode_probes'][2]['calls'][2]['args']=[0]
        with self.assertRaises(ValueError):verify_case(bad,parent)


if __name__=='__main__':unittest.main()
