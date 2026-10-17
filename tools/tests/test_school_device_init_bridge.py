import json
import struct
import unittest

from tools.school_device_init import ROOT, presentation
from tools.school_device_init_bridge import DeviceBridge, machine, sha

HELPER = ROOT/'.venv-audit/school-device-init-bridge.exe'


class BridgeTests(unittest.TestCase):
    def test_real_factory_device_caps_surface_and_viewport_cleanup(self):
        with DeviceBridge(HELPER, 640, 480) as bridge:
            factory = bridge.request('factory', sdk=220)['factory']
            mode = bridge.request('display_mode', pointer=factory['pointer'])
            fmt = struct.unpack('<4I', bytes.fromhex(mode['hex']))[3]
            result = bridge.request('create_device', pointer=factory['pointer'],
                                    type=1, flags=68,
                                    presentation_hex=presentation(640, 480, fmt, bridge.hello['window']).hex())
            self.assertEqual(result['hr'], 0)
            device = result['device']['pointer']
            self.assertEqual(len(bytes.fromhex(bridge.request('caps', pointer=device)['hex'])), 212)
            surface = bridge.request('backbuffer', pointer=device)['surface']['pointer']
            desc = bytes.fromhex(bridge.request('describe_surface', pointer=surface)['hex'])
            self.assertEqual(struct.unpack_from('<2I', desc, 24), (640, 480))
            bridge.request('release_surface', pointer=surface)
            with self.assertRaisesRegex(ValueError, 'foreign or expired'):
                bridge.request('describe_surface', pointer=surface)
            self.assertEqual(bridge.request('viewport', pointer=device,
                             hex=struct.pack('<6I', 0, 0, 640, 480, 0, 0x3F800000).hex())['hr'], 0)
        self.assertTrue(bridge.cleanup['all_owned_resources_released'])
        self.assertEqual(bridge.cleanup['device_release_count'], 0)
        self.assertEqual(bridge.cleanup['factory_release_count'], 0)
        self.assertTrue(bridge.cleanup['window_destroyed'])

    def test_foreign_fullscreen_and_duplicate_factory_refused(self):
        with DeviceBridge(HELPER, 640, 480) as bridge:
            factory = bridge.request('factory', sdk=220)['factory']['pointer']
            with self.assertRaisesRegex(ValueError, 'foreign or expired'):
                bridge.request('display_mode', pointer=1)
            with self.assertRaises(ValueError):
                bridge.request('factory', sdk=220)
            mode = bridge.request('display_mode', pointer=factory)
            fmt = struct.unpack('<4I', bytes.fromhex(mode['hex']))[3]
            pp = bytearray(presentation(640, 480, fmt, bridge.hello['window']))
            struct.pack_into('<I', pp, 28, 0)
            with self.assertRaisesRegex(ValueError, 'windowed presentation'):
                bridge.request('create_device', pointer=factory, type=1,
                               flags=68, presentation_hex=pp.hex())
            with self.assertRaisesRegex(ValueError, 'unsupported'):
                bridge.request('present')

    def test_bad_dimensions_and_post_cleanup_requests_refused(self):
        with self.assertRaises(ValueError):
            DeviceBridge(HELPER, 0, 480)
        with DeviceBridge(HELPER, 640, 480) as bridge:
            pass
        with self.assertRaisesRegex(ValueError, 'closed'):
            bridge.request('factory', sdk=220)

    def test_archived_bridge_provenance(self):
        report = json.loads((ROOT/'analysis/school-device-init-bridge-v1-20261017.json').read_text(encoding='utf-8'))
        self.assertEqual(machine(HELPER), 0x14C)
        self.assertEqual(sha(HELPER.read_bytes()), report['build']['helper_sha256'])
        self.assertEqual(sha((ROOT/'tools/school_device_init_bridge.cs').read_bytes()), report['build']['source_sha256'])
        self.assertTrue(report['cleanup']['all_owned_resources_released'])


if __name__ == '__main__':
    unittest.main()
