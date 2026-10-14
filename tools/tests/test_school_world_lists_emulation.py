import unittest,json,hashlib
from copy import deepcopy
from tools.school_world_lists_verification import REPORT,REPORT_SHA,verify_case,load_verified_checkpoint
from tools.school_world_lists import source_contract


class WorldListsNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(REPORT.read_bytes())

    def test_three_actual_250_slot_loops_source_masks_and_probes(self):
        self.assertEqual(hashlib.sha256(REPORT.read_bytes()).hexdigest(),REPORT_SHA)
        self.assertEqual(self.data['source_contract'],source_contract())
        self.assertEqual([c['name'] for c in self.data['cases']],['initial','student9_waiting','fifth_class'])
        for case in self.data['cases']:self.assertTrue(verify_case(case))
        self.assertEqual([c['actual_list_suffix']['occupied_slots'] for c in self.data['cases']],[38,37,37])
        self.assertEqual([c['actual_list_suffix']['display_state1_slots'] for c in self.data['cases']],[14,13,13])
        for k in ('world_tick_completed','original_opening_completed','persistent_write_authority'):self.assertIs(self.data[k],False)

    def test_wrong_full_buffers_predicate_counts_or_scope_refuse(self):
        original=self.data['cases'][0]
        for i in range(5):
            bad=deepcopy(original);r=bad['actual_list_suffix']['after'][i];b=bytearray.fromhex(r['hex']);b[-1]^=1;r['hex']=b.hex()
            with self.assertRaises(ValueError):verify_case(bad)
        for k,v in [('occupied_slots',1),('full_world_tick_executed',True),('predicates_stubbed',True),('retained_ranges_unchanged',False)]:
            bad=deepcopy(original);bad['actual_list_suffix'][k]=v
            with self.assertRaises(ValueError):verify_case(bad)
        bad=deepcopy(original);bad['actual_list_suffix']['pending']['return_va']='0x0'
        with self.assertRaises(ValueError):verify_case(bad)

    def test_wrong_sorting_masks_or_restoration_refuse(self):
        original=self.data['cases'][0]
        bad=deepcopy(original);bad['actual_list_suffix']['mask_bindings'][0]['sha256']='0'*64
        with self.assertRaises(ValueError):verify_case(bad)
        bad=deepcopy(original);bad['declared_probes']['sorting'][0]['display_indices'].reverse()
        with self.assertRaises(ValueError):verify_case(bad)
        bad=deepcopy(original);bad['declared_probes']['final_restoration']['cpu_after_sha256']='0'*64
        with self.assertRaises(ValueError):verify_case(bad)

    def test_three_private_checkpoint_hashes_full_bytes_and_exact_pending_stack(self):
        for name in ('initial','student9_waiting','fifth_class'):
            payload,cp=load_verified_checkpoint(name)
            self.assertEqual(payload['pending_eip'],0x48CD90);self.assertFalse(cp['runtime_or_original_save'])
        with self.assertRaises(ValueError):load_verified_checkpoint('untrusted')


if __name__=='__main__':unittest.main()
