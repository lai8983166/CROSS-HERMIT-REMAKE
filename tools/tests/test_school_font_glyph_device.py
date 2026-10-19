import json
import struct
import unittest
from tools.school_font_glyph_device import *


class DeviceTests(unittest.TestCase):
    def test_actual_immutable_build_and_parent(self):
        r=json.loads((ROOT/'analysis/school-font-glyph-device-v1-20261019.json').read_text())
        self.assertEqual(r['build'],dict(source_sha256=sha(SOURCE.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C))
        with self.assertRaises(ValueError):build_one(SOURCE,HELPER)
        parent=json.loads((ROOT/'analysis/school-font-atlas-device-v1-20261018.json').read_text())
        self.assertEqual(parent['build']['source_sha256'],sha((ROOT/'tools/school_font_atlas_device.cs').read_bytes()))

    def test_real_lock_complete_buffer_transfer_readback_and_cleanup(self):
        r=probe();locked=r['locked'];readback=r['uploaded']['inspection']
        self.assertEqual(locked['locked_hex'],struct.pack('<2I',locked['pitch'],locked['bits']).hex())
        self.assertEqual(len(bytes.fromhex(locked['before_hex'])),locked['pitch']*256)
        self.assertEqual(readback['hex'],r['written_hex']);self.assertFalse(readback['native_requested'])
        self.assertEqual((readback['lock_hr'],readback['unlock_hr'],r['uploaded']['hr']),(0,0,0))
        self.assertEqual(r['cleanup']['atlas_texture_release_count'],0);self.assertTrue(r['cleanup']['all_owned_resources_released'])

    def test_unordered_foreign_duplicate_bad_payload_and_abandoned_lock_cleanup(self):
        def run(bridge):
            with self.assertRaises(ValueError):bridge.request('atlas_lock',pointer=1,level=0,rect=0,flags=0)
            device=setup(bridge);texture=create(bridge,device)['texture']['pointer']
            with self.assertRaises(ValueError):bridge.request('atlas_unlock',pointer=texture,level=0,bytes_hex='00')
            locked=bridge.request('atlas_lock',pointer=texture,level=0,rect=0,flags=0)
            with self.assertRaises(ValueError):bridge.request('atlas_lock',pointer=texture,level=0,rect=0,flags=0)
            with self.assertRaises(ValueError):bridge.request('atlas_unlock',pointer=texture,level=0,bytes_hex='00')
        r=owned_run(run);self.assertEqual(r['cleanup']['abandoned_atlas_unlock_hr'],0);self.assertTrue(r['cleanup']['all_owned_resources_released'])
