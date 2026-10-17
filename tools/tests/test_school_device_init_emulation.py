import json
import unittest
from copy import deepcopy

from tools.school_device_init import ROOT
from tools.school_device_init_bridge import DeviceBridge
from tools.school_device_init_emulation import DeviceEmulator, OWNER
from tools.school_device_init_verification import verify_report, verify_case


class NativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((ROOT/'analysis/school-device-init-native-v1-20261017.json').read_text(encoding='utf-8'))

    def test_two_archived_cases_match_source_full_owner_live_ABI_and_cleanup(self):
        result = verify_report(self.report)
        self.assertEqual([r['full_owner_bytes'] for r in result], [49152, 49152])
        self.assertEqual([r['selected_format'] for r in result], [24, 24])

    def test_fresh_native_startup_with_fresh_real_owned_interfaces(self):
        helper = ROOT/'.venv-audit/school-device-init-bridge.exe'
        with DeviceBridge(helper, 640, 480) as bridge:
            case = DeviceEmulator(bridge).run()
        case.update(bridge_trace=bridge.trace, cleanup=bridge.cleanup)
        self.assertEqual(verify_case(case)['dimensions'], [640, 480])

    def test_source_live_pointer_request_and_native_stack_corruptions_refused(self):
        changes = [lambda c: c['root_args'].__setitem__(1, 0),
                   lambda c: c['actual']['entries'][4].update(receiver=OWNER+4),
                   lambda c: c['actual']['entries'][4].update(sp=1),
                   lambda c: c['actual']['platform_calls'][2]['args'].__setitem__(4, 36),
                   lambda c: c['actual']['platform_calls'][4].update(result=0xFFFFFFFF),
                   lambda c: c['actual']['live_results'][2]['request'].update(presentation_hex='00'*52),
                   lambda c: c['bridge_trace'][0]['reply'].update(id=0),
                   lambda c: c['actual']['returns'][-1].update(eax=1)]
        for change in changes:
            bad = deepcopy(self.report['cases'][0])
            change(bad)
            with self.assertRaises(ValueError):
                verify_case(bad)

    def test_original_image_owner_foreign_maps_and_full_buffers_refused(self):
        changes = [lambda c: c['after_owner'].update(sha256='0'*64),
                   lambda c: c['foreign_maps'][0].update(sha256='0'*64),
                   lambda c: c.update(original_IAT_target=1),
                   lambda c: c.update(original_IAT_unchanged=False),
                   lambda c: c['actual']['live_results'][3]['result'].update(hex='00'*211)]
        for change in changes:
            bad = deepcopy(self.report['cases'][0])
            change(bad)
            with self.assertRaises(ValueError):
                verify_case(bad)

    def test_pending_font_and_resource_lifetime_completion_claims_refused(self):
        changes = [lambda c: c.update(owner_bound=True),
                   lambda c: c.update(retained_VM_advanced=True),
                   lambda c: c.update(live_pointers_resumable_after_cleanup=True),
                   lambda c: c['pending_font'].update(first_instruction_executed=True),
                   lambda c: c['actual']['visited'].append(0x415F50),
                   lambda c: c['cleanup'].update(device_release_count=1),
                   lambda c: c['actual']['cpu'].update(ESP=0)]
        for change in changes:
            bad = deepcopy(self.report['cases'][0])
            change(bad)
            with self.assertRaises(ValueError):
                verify_case(bad)

    def test_bridge_build_and_global_authority_corruptions_refused(self):
        for key in ('retained_VM_advanced', 'original_helpers_stubbed', 'drawing_or_Present'):
            bad = deepcopy(self.report)
            bad[key] = True
            with self.assertRaises(ValueError):
                verify_report(bad)
        bad = deepcopy(self.report)
        bad['bridge_build']['source_sha256'] = '0'*64
        with self.assertRaises(ValueError):
            verify_report(bad)


if __name__ == '__main__':
    unittest.main()
