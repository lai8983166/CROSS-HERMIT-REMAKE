import json
import unittest
from tools.school_startup_return_platform import *
from tools.school_startup_return import capture_code


class PlatformTests(unittest.TestCase):
    def test_immutable_x86_new_device_and_unchanged_parent(self):
        r=json.loads((ROOT/'analysis/school-startup-return-device-v1-20261019.json').read_text())
        self.assertEqual(r['build'],dict(source_sha256=sha(DEVICE_SOURCE.read_bytes()),helper_sha256=sha(DEVICE_HELPER.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C))
        with self.assertRaises(ValueError):build_one(DEVICE_SOURCE,DEVICE_HELPER)
        old=json.loads((ROOT/'analysis/school-font-finish-device-v1-20261019.json').read_text())
        self.assertEqual(old['build']['source_sha256'],sha((ROOT/'tools/school_font_finish_device.cs').read_bytes()))
        self.assertEqual(old['build']['helper_sha256'],sha((ROOT/'.venv-audit/school-font-finish-device-v1.exe').read_bytes()))

    def test_actual_void_call_owned_capture_input_and_complete_external_restoration(self):
        r=probe();g=r['gamma'];identity=r['prepare']['device'];cleanup=r['cleanup']
        self.assertEqual(g['native_return_type'],'void');self.assertFalse(g['eax_is_status']);self.assertNotIn('hr',g)
        self.assertEqual(g['method_pointer'],identity['methods']['72'])
        self.assertEqual(g['forwarder_hex'],capture_code(g['method_pointer']).hex());self.assertTrue(g['forwarder_freed'])
        self.assertEqual(g['input_after_hex'],gamma_bytes().hex());self.assertFalse(g['inspection']['native_requested'])
        for key in ('device_before_hex','device_after_hex','desktop_before_hex','desktop_after_hex'):
            self.assertEqual(len(bytes.fromhex(g['inspection'][key])),1536)
        self.assertEqual(cleanup['gamma_native_calls'],1)
        for key in ('gamma_device_restored','gamma_desktop_restored','gamma_DCs_balanced','all_owned_resources_released'):
            self.assertTrue(cleanup[key])
        self.assertEqual(cleanup['gamma_DCs_acquired'],cleanup['gamma_DCs_released'])
        self.assertEqual(cleanup['gamma_DCs_acquired'],5 if cleanup['gamma_desktop_restore_write_required'] else 4)

    def test_foreign_early_wrong_payload_flags_and_duplicate_requests_refused(self):
        def run(b):
            with self.assertRaises(ValueError):b.request('gamma_prepare',pointer=1)
            with self.assertRaises(ValueError):b.request('gamma_set',pointer=1,flags=1,hex=gamma_bytes().hex())
            ready=ready_gamma(b);p=ready['device']
            with self.assertRaises(ValueError):b.request('gamma_set',pointer=p,flags=1,hex=gamma_bytes().hex())
            b.request('gamma_prepare',pointer=p)
            with self.assertRaises(ValueError):b.request('gamma_prepare',pointer=p)
            for flags,raw in ((0,gamma_bytes()),(1,bytes(1536)),(1,bytes(1535))):
                with self.assertRaises(ValueError):b.request('gamma_set',pointer=p,flags=flags,hex=raw.hex())
            b.request('gamma_set',pointer=p,flags=1,hex=gamma_bytes().hex())
            with self.assertRaises(ValueError):b.request('gamma_set',pointer=p,flags=1,hex=gamma_bytes().hex())
        r=owned_run(run);self.assertTrue(r['cleanup']['all_owned_resources_released']);self.assertEqual(r['cleanup']['gamma_native_calls'],1)

    def test_admission_only_partial_cleanup_has_no_gamma_call_or_desktop_change(self):
        def run(b):
            ready=ready_gamma(b);return b.request('gamma_prepare',pointer=ready['device'])
        r=owned_run(run);self.assertNotIn('gamma_native_calls',r['cleanup']);self.assertNotIn('gamma_DCs_acquired',r['cleanup'])
        self.assertTrue(r['cleanup']['all_owned_resources_released'])
