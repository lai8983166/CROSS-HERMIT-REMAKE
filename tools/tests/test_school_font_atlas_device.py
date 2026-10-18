import json
import struct
import unittest
from tools.school_font_atlas_device import *


class DeviceTests(unittest.TestCase):
    def test_build_provenance_and_immutable_parent(self):
        r = json.loads((ROOT/'analysis/school-font-atlas-device-v1-20261018.json').read_text())
        self.assertEqual(r['build'], dict(source_sha256=sha(SOURCE.read_bytes()), helper_sha256=sha(HELPER.read_bytes()), compiler_sha256=sha(COMPILER.read_bytes()), machine=0x14C))
        with self.assertRaises(ValueError): build_one(SOURCE, HELPER)
        parent = json.loads((ROOT/'analysis/school-font-cache-platform-v1-20261018.json').read_text())
        self.assertEqual(sha((ROOT/'tools/school_font_cache_device.cs').read_bytes()), parent['builds']['device']['source_sha256'])

    def test_real_additional_texture_description_and_complete_cleanup(self):
        r = probe()
        atlas = r['atlas']
        self.assertEqual(atlas['hr'], 0)
        self.assertEqual(atlas['inspection'], dict(native_requested=False, method='GetLevelDesc', level=0,
            result=dict(hr=0, hex=struct.pack('<8I', 26, 1, 0, 1, 131072, 0, 256, 256).hex())))
        self.assertEqual(set(atlas['texture']['methods']), {'8', '56', '64', '68'})
        self.assertEqual(r['cleanup'], dict(atlas_texture_release_count=0, texture_surface_release_count=1,
            texture_release_count=0, extra_reference_release_counts=[3, 2, 1], device_release_count=0,
            factory_release_count=0, window_destroyed=True, all_owned_resources_released=True))

    def test_foreign_unordered_wrong_size_duplicate_and_closed_requests_refused(self):
        def run(bridge):
            with self.assertRaises(ValueError): create(bridge, 1)
            device = setup(bridge)
            with self.assertRaises(ValueError):
                bridge.request('atlas_create', pointer=device, width=128, height=256, levels=1, usage=0, format=26, pool=1)
            create(bridge, device)
            with self.assertRaises(ValueError): create(bridge, device)
            return bridge
        result = owned_run(run)
        self.assertTrue(result['cleanup']['all_owned_resources_released'])
        with self.assertRaises(ValueError): create(result['value'], 1)
