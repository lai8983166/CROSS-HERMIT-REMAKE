import json
import unittest
from tools.school_font_second_glyph_platform import *


class GDITests(unittest.TestCase):
    def test_immutable_x86_GDI_and_parent(self):
        r=json.loads((ROOT/'analysis/school-font-second-glyph-gdi-v1-20261019.json').read_text())
        self.assertEqual(r['build'],dict(source_sha256=sha(GDI_SOURCE.read_bytes()),helper_sha256=sha(GDI_HELPER.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C))
        with self.assertRaises(ValueError):build_one(GDI_SOURCE,GDI_HELPER)
        old=json.loads((ROOT/'analysis/school-font-second-resource-gdi-v1-20261019.json').read_text())
        self.assertEqual(old['build']['source_sha256'],sha((ROOT/'tools/school_font_second_resource_gdi.cs').read_bytes()))

    def test_actual95_second_glyphs_dynamic_metrics_and_separate_cleanup(self):
        r=gdi_probe();s=r['second'];self.assertEqual(len(s['calls']),190)
        self.assertEqual(s['after']['completed_glyphs'],95);self.assertNotEqual(s['before']['hex'],s['after']['hex'])
        self.assertEqual(len(bytes.fromhex(s['after']['hex'])),262144)
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
