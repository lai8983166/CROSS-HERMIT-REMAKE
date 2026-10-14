import hashlib,json,unittest
from copy import deepcopy
from tools.school_student_tail import source_contract
from tools.school_student_tail_verification import REPORT,REPORT_SHA,verify_case,load_verified_checkpoint


class StudentTailNativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=json.loads(REPORT.read_bytes())

    def test_three_original_first_units_and_eighteen_restored_probes(self):
        self.assertEqual(hashlib.sha256(REPORT.read_bytes()).hexdigest(),REPORT_SHA)
        self.assertEqual(self.data['source_contract'],source_contract())
        self.assertEqual([r['name'] for r in self.data['cases']],['initial','student9_waiting','fifth_class'])
        for row in self.data['cases']:self.assertTrue(verify_case(row))
        self.assertIs(self.data['first_unit_completed'],True)
        for k in ('second_world_completed','original_opening_completed','persistent_write_authority'):self.assertIs(self.data[k],False)

    def test_every_owned_region_corruption_refused(self):
        for i in range(10):
            bad=deepcopy(self.data['cases'][0]);r=bad['actual_tail']['after'][i]
            r['hex']=r['hex'][:-2]+('00' if r['hex'][-2:]!='00' else '01')
            with self.assertRaises(ValueError):verify_case(bad)

    def test_wrong_natural_stack_parent_scan_probe_and_restoration_refused(self):
        original=self.data['cases'][0]
        mutations=[lambda b:b['actual_tail']['pending'].update(sp=0),
          lambda b:b['parent_checkpoint'].update(sha256='0'*64),
          lambda b:b['actual_tail']['effect_scans'].pop(),
          lambda b:b['actual_tail'].update(next_unit_executed=True),
          lambda b:b['declared_probes']['rows'][2]['declared'].update(hp_gap=2),
          lambda b:b['declared_probes']['rows'][2]['restoration'].update(cpu_after_sha256='0'*64),
          lambda b:b['actual_tail']['inputs'].update(map_all_bytes_verified=16)]
        for change in mutations:
            bad=deepcopy(original);change(bad)
            with self.assertRaises(ValueError):verify_case(bad)

    def test_all_private_checkpoints_match_restored_complete_state(self):
        for row in self.data['cases']:
            payload,cp=load_verified_checkpoint(row['name'])
            self.assertEqual(hex(payload['pending_eip']),cp['pending_eip']);self.assertFalse(cp['runtime_or_original_save'])
        with self.assertRaises(ValueError):load_verified_checkpoint('../initial')


if __name__=='__main__':unittest.main()
