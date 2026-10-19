import json
import unittest
from tools.school_font_second_glyph_platform import *


class GDITests(unittest.TestCase):
    def test_immutable_x86_GDI_and_parent(self):
        r=json.loads((ROOT/'analysis/school-font-second-glyph-gdi-v2-20261019.json').read_text())
        self.assertEqual(r['build'],dict(source_sha256=sha(GDI_SOURCE.read_bytes()),helper_sha256=sha(GDI_HELPER.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C))
        with self.assertRaises(ValueError):build_one(GDI_SOURCE,GDI_HELPER)
        old=json.loads((ROOT/'analysis/school-font-second-resource-gdi-v1-20261019.json').read_text())
        self.assertEqual(old['build']['source_sha256'],sha((ROOT/'tools/school_font_second_resource_gdi.cs').read_bytes()))

    def test_actual95_second_glyphs_dynamic_metrics_and_separate_cleanup(self):
        r=gdi_probe();s=r['second'];self.assertEqual(len(s['calls']),190)
        self.assertEqual(s['after']['completed_glyphs'],95);self.assertNotEqual(s['before']['hex'],s['after']['hex'])
        self.assertEqual(len(bytes.fromhex(s['after']['hex'])),262144)
        from tools.school_font_second_ink import ink_rectangles
        import struct
        measures=[struct.unpack('<2I',bytes.fromhex(r['result']['hex'])) for r in s['calls'] if r['op']=='second_glyph_measure']
        rows,end=layout(measures);bounds=ink_rectangles(rows,s['after']['ink_inspection'])
        self.assertEqual(bounds,ink_rectangles(rows,s['before']['ink_inspection']))
        self.assertEqual((bounds[87]['A'],bounds[87]['B'],bounds[87]['C']),(0,7,-1))
        self.assertTrue(r['cleanup']['all_owned_resources_released']);self.assertEqual(r['cleanup']['native_atlas_bitmaps_released'],1)
        self.assertEqual(r['cleanup']['second_atlas_bitmaps_released'],1)

    def test_early_foreign_wrong_character_draw_and_partial_cleanup_refused(self):
        with SecondGlyphGDI() as p:
            with self.assertRaises(ValueError):p.request('second_glyph_pixels',pointer=1,stage='before')
            r=gdi_ready(p);dc=r['second'][0]['result']['result'];bits=r['second'][1]['result']['bits']
            p.request('second_glyph_pixels',pointer=bits,stage='before')
            with self.assertRaises(ValueError):p.request('second_glyph_measure',pointer=dc,character=33,before_hex='cc'*8)
            p.request('second_glyph_measure',pointer=dc,character=32,before_hex='cc'*8)
            with self.assertRaises(ValueError):p.request('second_glyph_draw',pointer=dc,character=32,x=1,y=0)
            with self.assertRaises(ValueError):p.request('second_glyph_pixels',pointer=bits,stage='after')
        self.assertTrue(p.cleanup['all_owned_resources_released']);self.assertTrue(p.cleanup['second_atlas_selection_restored'])


class DeviceTests(unittest.TestCase):
    def test_immutable_x86_device_and_parent(self):
        r=json.loads((ROOT/'analysis/school-font-second-glyph-device-v1-20261019.json').read_text())
        self.assertEqual(r['build'],dict(source_sha256=sha(DEVICE_SOURCE.read_bytes()),helper_sha256=sha(DEVICE_HELPER.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C))
        with self.assertRaises(ValueError):build_one(DEVICE_SOURCE,DEVICE_HELPER)
        old=json.loads((ROOT/'analysis/school-font-second-resource-device-v2-20261019.json').read_text())
        self.assertEqual(old['build']['source_sha256'],sha((ROOT/'tools/school_font_second_resource_device_v2.cs').read_bytes()))

    def test_actual_second_upload_full_readback_first_resources_and_cleanup(self):
        r=device_probe();self.assertEqual(r['unlocked']['inspection']['hex'],r['uploaded_hex'])
        first=r['unlocked']['retained_first_texture_inspection']
        self.assertFalse(first['native_requested']);self.assertEqual(first['pointer'],r['first']['texture'])
        self.assertEqual(len(bytes.fromhex(first['hex'])),first['pitch']*256)
        self.assertEqual(r['cleanup']['second_atlas_texture_release_count'],0)
        self.assertEqual(r['cleanup']['font_state_block_delete_results'],[0,0]);self.assertTrue(r['cleanup']['all_owned_resources_released'])

    def test_foreign_early_duplicate_bad_buffer_and_partial_lock_cleanup_refused(self):
        def run(b):
            with self.assertRaises(ValueError):b.request('second_atlas_lock',pointer=1,level=0,rect=0,flags=0)
            first,second=device_ready(b);pointer=second['texture']['pointer']
            with self.assertRaises(ValueError):b.request('second_atlas_unlock',pointer=pointer,level=0,bytes_hex='')
            locked=b.request('second_atlas_lock',pointer=pointer,level=0,rect=0,flags=0)
            with self.assertRaises(ValueError):b.request('second_atlas_lock',pointer=pointer,level=0,rect=0,flags=0)
            with self.assertRaises(ValueError):b.request('second_atlas_unlock',pointer=pointer,level=0,bytes_hex='00')
        r=owned_run(run);self.assertEqual(r['cleanup']['abandoned_second_atlas_unlock_hr'],0);self.assertTrue(r['cleanup']['all_owned_resources_released'])
