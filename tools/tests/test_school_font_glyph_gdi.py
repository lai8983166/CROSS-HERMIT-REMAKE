import json
import unittest
from tools.school_font_glyph_gdi import *


class GDITests(unittest.TestCase):
    def test_actual_immutable_build_and_parent(self):
        r=json.loads((ROOT/'analysis/school-font-glyph-gdi-v1-20261019.json').read_text())
        self.assertEqual(r['build'],dict(source_sha256=sha(SOURCE.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C))
        with self.assertRaises(ValueError):build_one(SOURCE,HELPER)
        p=json.loads((ROOT/'analysis/school-font-atlas-gdi-v2-20261018.json').read_text())
        self.assertEqual(p['build']['source_sha256'],sha((ROOT/'tools/school_font_atlas_gdi_v2.cs').read_bytes()))

    def test_real95_glyphs_complete_DIB_snapshot_and_cleanup(self):
        r=probe();self.assertEqual(len(r['glyphs']),95);self.assertTrue(r['cleanup']['all_owned_resources_released'])
        self.assertEqual(len(bytes.fromhex(r['after']['hex'])),262144)
        self.assertNotEqual(r['before']['hex'],r['after']['hex']);self.assertFalse(r['after']['native_requested'])
        self.assertEqual(r['after']['completed_glyphs'],95)

    def test_unordered_foreign_duplicate_and_wrong_character_refused(self):
        with GlyphGDI() as p:
            with self.assertRaises(ValueError):p.request('glyph_measure',pointer=1,character=32,before_hex='cc'*8)
            setup(p);calls=prepare(p);dc=calls[0]['result']['result'];bits=calls[1]['result']['bits']
            p.request('glyph_pixels',pointer=bits,stage='before')
            for pointer,ch in ((1,32),(dc,33)):
                with self.assertRaises(ValueError):p.request('glyph_measure',pointer=pointer,character=ch,before_hex='cc'*8)
            p.request('glyph_measure',pointer=dc,character=32,before_hex='cc'*8)
            with self.assertRaises(ValueError):p.request('glyph_measure',pointer=dc,character=32,before_hex='cc'*8)
            with self.assertRaises(ValueError):p.request('glyph_draw',pointer=dc,character=32,x=1,y=0)
        self.assertTrue(p.cleanup['all_owned_resources_released'])
