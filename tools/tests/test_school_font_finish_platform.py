import json
import struct
import unittest
from tools.school_font_finish_platform import *


class GDITests(unittest.TestCase):
    def test_immutable_x86_GDI_and_preserved_parent(self):
        r=json.loads((ROOT/'analysis/school-font-finish-gdi-v1-20261019.json').read_text())
        self.assertEqual(r['build'],dict(source_sha256=sha(GDI_SOURCE.read_bytes()),helper_sha256=sha(GDI_HELPER.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C))
        with self.assertRaises(ValueError):build_one(GDI_SOURCE,GDI_HELPER)
        old=json.loads((ROOT/'analysis/school-font-second-glyph-gdi-v2-20261019.json').read_text())
        self.assertEqual(old['build']['source_sha256'],sha((ROOT/'tools/school_font_second_glyph_gdi_v2.cs').read_bytes()))

    def test_actual_second_native_delete_order_lifetime_and_independent_counters(self):
        r=gdi_probe();self.assertEqual([x['result']['result'] for x in r['deletion']],[1,1,1])
        self.assertEqual(r['deletion'][1]['result']['inspection'],dict(native_requested=False,method='GdiFlush/GetObjectA/GetObjectType(bitmap)',result=0,reported_type=7))
        for kind in ('fonts','dcs','bitmaps'):
            self.assertEqual(r['cleanup']['second_native_atlas_'+kind+'_released'],1)
            self.assertEqual(r['cleanup']['native_atlas_'+kind+'_released'],1)
            self.assertEqual(r['cleanup']['second_atlas_'+kind+'_released'],0)
        self.assertTrue(r['cleanup']['second_native_GDI_cleanup_executed']);self.assertTrue(r['cleanup']['all_owned_resources_released'])

    def test_early_foreign_wrong_order_and_partial_pending_bitmap_cleanup_refused(self):
        with FinishGDI() as p:
            with self.assertRaises(ValueError):p.request('second_font_delete_bitmap',pointer=1)
            ready=gdi_ready(p);second_raster(p,ready);prep=ready['second']
            with self.assertRaises(ValueError):p.request('second_font_delete_dc',pointer=prep[0]['result']['result'])
            with self.assertRaises(ValueError):p.request('second_font_delete_bitmap',pointer=1)
            p.request('second_font_delete_bitmap',pointer=prep[1]['result']['result'])
        self.assertTrue(p.cleanup['all_owned_resources_released']);self.assertTrue(p.cleanup['second_atlas_selection_restored'])
        self.assertFalse(p.cleanup['second_native_GDI_cleanup_executed'])
