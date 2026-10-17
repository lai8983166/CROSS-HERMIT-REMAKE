import json
import unittest
from copy import deepcopy

from tools.school_owner_startup import ROOT
from tools.school_owner_startup_verification import verify_report


class ConstructorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT/'analysis/school-owner-startup-constructor-v1-20261017.json').read_text(encoding='utf-8'))

    def test_full_source_projection_native_ABI_and_two_dirty_inputs(self):
        self.assertEqual(verify_report(self.report)['source_calls_each'], 42)

    def test_owner_source_clock_SEH_array_and_live_result_corruptions_refused(self):
        changes = [lambda c: c['constructor']['state']['owner'].update(sha256='0'*64),
                   lambda c: c['constructor']['state'].update(image_sha256='0'*64),
                   lambda c: c['constructor']['state'].update(SEH=4),
                   lambda c: c['constructor']['native']['entries'][19]['args'].__setitem__(2, 1),
                   lambda c: c['constructor']['native']['entries'][20].update(sp=1),
                   lambda c: c['constructor']['platform_calls'][0]['args'].__setitem__(0, 1),
                   lambda c: c['constructor']['platform_calls'][1]['result'].update(hex='00'*8),
                   lambda c: c['platform_trace'][0]['reply'].update(id=0)]
        for change in changes:
            bad = deepcopy(self.report)
            change(bad['cases'][0])
            with self.assertRaises(ValueError):
                verify_report(bad)


class DeviceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT/'analysis/school-owner-startup-device-v1-20261017.json').read_text(encoding='utf-8'))

    def test_real_device_prefix_on_both_original_constructed_owners(self):
        self.assertEqual(verify_report(self.report)['cases'], 2)

    def test_device_owner_state_live_requests_and_font_boundary_refused(self):
        changes = [lambda c: c['device']['native']['platform_calls'][2]['args'].__setitem__(4, 36),
                   lambda c: c['device']['state']['owner'].update(sha256='0'*64),
                   lambda c: c['device']['native']['cpu'].update(ESP=0),
                   lambda c: c['device']['pending'].update(first_instruction_executed=True),
                   lambda c: c['device_trace'][0]['reply'].update(id=0)]
        for change in changes:
            bad = deepcopy(self.report)
            change(bad['cases'][0])
            with self.assertRaises(ValueError):
                verify_report(bad)

    def test_full_owner_constructor_does_not_claim_VM_or_font_execution(self):
        bad = deepcopy(self.report)
        bad['retained_VM_advanced'] = True
        with self.assertRaises(ValueError):
            verify_report(bad)
        bad = deepcopy(self.report)
        bad['cases'][0]['constructor']['native']['visited'].append(0x415F50)
        with self.assertRaises(ValueError):
            verify_report(bad)

    def test_actual_interface_maps_and_cleanup_are_verified(self):
        for change in (lambda c: c['constructor']['state']['foreign_maps'][0].update(sha256='0'*64),
                       lambda c: c['platform_cleanup'].update(dcs_released=0)):
            bad = deepcopy(self.report)
            change(bad['cases'][0])
            with self.assertRaises(ValueError):
                verify_report(bad)


if __name__ == '__main__':
    unittest.main()
