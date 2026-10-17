import json
import struct
import unittest
from tools.school_font_device_bridge import *
from tools.school_device_init_emulation import DeviceEmulator


class BridgeTests(unittest.TestCase):
    def test_fixed_new_build_and_immutable_parent(self):
        report = json.loads((ROOT/'analysis/school-font-startup-bridge-v1-20261018.json').read_text(encoding='utf-8'))
        for key, path in (('source_sha256', SOURCE), ('helper_sha256', HELPER), ('compiler_sha256', COMPILER)):
            self.assertEqual(report['build'][key], sha(path.read_bytes()))
        self.assertEqual(machine(HELPER), 0x14C)
        parent = json.loads((ROOT/'analysis/school-device-init-bridge-v1-20261017.json').read_text(encoding='utf-8'))['build']
        self.assertEqual(parent['source_sha256'], sha((ROOT/'tools/school_device_init_bridge.cs').read_bytes()))
        with self.assertRaises(ValueError):
            build()

    def test_live_cache_queries_and_balanced_reference_lifetime(self):
        r = probe()
        self.assertGreaterEqual(r['calls'][0]['result']['count'], 2)
        self.assertEqual(len(bytes.fromhex(r['calls'][1]['result']['hex'])), 212)
        actual = struct.unpack('<4I', bytes.fromhex(r['calls'][2]['result']['hex']))
        self.assertEqual(actual, (0, 1, r['hello']['window'], 68))
        self.assertEqual(r['cleanup']['extra_reference_release_counts'], [1])
        self.assertEqual(r['cleanup']['device_release_count'], 0)
        self.assertTrue(r['cleanup']['all_owned_resources_released'])

    def test_foreign_unordered_duplicate_and_closed_queries_refused(self):
        def run(bridge):
            engine = DeviceEmulator(bridge)
            engine.run()
            ptr = engine.objects['device']['pointer']
            for op, pointer in (('cache_addref', 1), ('cache_caps', ptr), ('cache_creation', ptr)):
                with self.assertRaises(ValueError):
                    bridge.request(op, pointer=pointer)
            bridge.request('cache_addref', pointer=ptr)
            with self.assertRaises(ValueError):
                bridge.request('cache_addref', pointer=ptr)
            return bridge, ptr
        result = owned_run(run)
        bridge, ptr = result['value']
        self.assertEqual(result['cleanup']['extra_reference_release_counts'], [1])
        self.assertTrue(result['cleanup']['all_owned_resources_released'])
        with self.assertRaises(ValueError):
            bridge.request('cache_caps', pointer=ptr)
