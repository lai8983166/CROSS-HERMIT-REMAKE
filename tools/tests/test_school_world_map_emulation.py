import unittest,json,hashlib
from copy import deepcopy
from tools.school_world_map_emulation import ROOT,PARENT,PARENT_SHA
from tools.school_world_map import source_contract
from tools.school_world_map_verification import verify_case


class WorldMapNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=json.loads((ROOT/'analysis/school-world-map-native-v4-20261014.json').read_text(encoding='utf-8'))
        cls.parent=json.loads(PARENT.read_bytes())

    def test_three_actual_suffixes_native_clear_and_fifty_one_restored_probes(self):
        self.assertEqual(self.report['source_contract'],source_contract())
        self.assertEqual(self.report['parent_sha256'],PARENT_SHA);self.assertEqual(hashlib.sha256(PARENT.read_bytes()).hexdigest(),PARENT_SHA)
        self.assertEqual([c['name'] for c in self.report['cases']],['initial','student9_waiting','fifth_class'])
        for key in ('world_tick_completed','original_opening_completed','persistent_write_authority'):self.assertIs(self.report[key],False)
        for case,parent in zip(self.report['cases'],self.parent['cases']):self.assertTrue(verify_case(case,parent))

    def test_wrong_complete_map_buffer_clock_stack_or_claim_refuse(self):
        original=self.report['cases'][0];parent=self.parent['cases'][0]
        for index in range(6):
            bad=deepcopy(original);r=bad['actual_map_suffix']['after'][index];data=bytearray.fromhex(r['hex']);data[-1]^=1;r['hex']=data.hex()
            with self.assertRaises(ValueError):verify_case(bad,parent)
        for field,value in [('clock_after_hex','00'*24),('original_memset_body_executed',False),('full_world_tick_executed',True),('live_input_captured',True),('retained_ranges_unchanged',False)]:
            bad=deepcopy(original);bad['actual_map_suffix'][field]=value
            with self.assertRaises(ValueError):verify_case(bad,parent)
        bad=deepcopy(original);bad['actual_map_suffix']['pending']['return_va']='0x0'
        with self.assertRaises(ValueError):verify_case(bad,parent)

    def test_wrong_declared_clock_mouse_or_restore_refuse(self):
        original=self.report['cases'][0];parent=self.parent['cases'][0]
        bad=deepcopy(original);bad['declared_probes']['clock'][2]['return_eax']=1
        with self.assertRaises(ValueError):verify_case(bad,parent)
        bad=deepcopy(original);bad['declared_probes']['mouse'][4]['outputs']['pixel']=[31,570]
        with self.assertRaises(ValueError):verify_case(bad,parent)
        for field in ('cpu_after_sha256','stack_after_sha256'):
            bad=deepcopy(original);bad['declared_probes']['mouse'][0]['restoration'][field]='0'*64
            with self.assertRaises(ValueError):verify_case(bad,parent)


if __name__=='__main__':unittest.main()
