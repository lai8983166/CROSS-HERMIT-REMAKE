import json
import unittest
from tools.school_font_state_gdi import *


class GDITests(unittest.TestCase):
    def test_actual_immutable_build_and_parent(self):
        r=json.loads((ROOT/'analysis/school-font-state-gdi-v5-20261019.json').read_text())
        self.assertEqual(r['build'],dict(source_sha256=sha(SOURCE.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C))
        with self.assertRaises(ValueError):build_one(SOURCE,HELPER)
        parent=json.loads((ROOT/'analysis/school-font-glyph-gdi-v1-20261019.json').read_text())
        self.assertEqual(parent['build']['source_sha256'],sha((ROOT/'tools/school_font_glyph_gdi.cs').read_bytes()))

    def test_actual_original_delete_order_deferred_bitmap_and_native_cleanup(self):
        r=probe();self.assertEqual([c['result']['result'] for c in r['deletion']],[1,1,1])
        self.assertEqual(r['deletion'][1]['result']['inspection'],dict(native_requested=False,method='GdiFlush/GetObjectA/GetObjectType(bitmap)',result=0,reported_type=7))
        self.assertTrue(r['cleanup']['native_cleanup_completed']);self.assertTrue(r['cleanup']['all_owned_resources_released'])
        for kind in ('fonts','dcs','bitmaps'):
            self.assertEqual(r['cleanup']['native_atlas_'+kind+'_released'],1);self.assertEqual(r['cleanup']['atlas_'+kind+'_released'],0)

    def test_wrong_order_foreign_and_pending_bitmap_fallback_cleanup(self):
        with StateGDI() as p:
            with self.assertRaises(ValueError):p.request('font_delete_bitmap',pointer=1)
            setup(p);r=raster(p)
            with self.assertRaises(ValueError):p.request('font_delete_dc',pointer=r['preparation'][0]['result']['result'])
            with self.assertRaises(ValueError):p.request('font_delete_bitmap',pointer=1)
            p.request('font_delete_bitmap',pointer=r['preparation'][1]['result']['result'])
        self.assertTrue(p.cleanup['all_owned_resources_released']);self.assertFalse(p.cleanup['native_cleanup_completed'])
