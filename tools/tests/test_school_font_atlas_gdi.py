import json
import unittest
from tools.school_font_atlas_gdi import *
from tools.school_font_atlas import font_logfont


class GDITests(unittest.TestCase):
    def test_actual_build_and_immutable_parent(self):
        r = json.loads((ROOT/'analysis/school-font-atlas-gdi-v2-20261018.json').read_text())
        self.assertEqual(r['build'], dict(source_sha256=sha(SOURCE.read_bytes()), helper_sha256=sha(HELPER.read_bytes()), compiler_sha256=sha(COMPILER.read_bytes()), machine=0x14C))
        with self.assertRaises(ValueError): build_one(SOURCE, HELPER)
        parent = json.loads((ROOT/'analysis/school-font-cache-platform-v1-20261018.json').read_text())
        self.assertEqual(sha((ROOT/'tools/school_font_cache_gdi.cs').read_bytes()), parent['builds']['gdi']['source_sha256'])

    def test_real_atlas_GDI_font_inspection_setup_and_complete_cleanup(self):
        r = probe(); calls = r['calls']
        self.assertEqual(calls[3]['result']['result'], 16)
        self.assertEqual(calls[4]['result']['inspection'], dict(native_requested=False, method='GetObjectA', result=60, hex=font_logfont().hex()))
        self.assertEqual(r['cleanup'], dict(atlas_fonts_released=1, atlas_dcs_released=1, atlas_bitmaps_released=1,
            atlas_selection_restored=True, fonts_released=2, dcs_released=1, cache_bitmaps_released=1,
            cache_dcs_released=1, cache_selection_restored=True, all_owned_resources_released=True))

    def test_unordered_foreign_wrong_header_font_and_closed_requests_refused(self):
        with AtlasGDI() as platform:
            with self.assertRaises(ValueError): platform.request('atlas_dc')
            setup(platform)
            for op, args in (('atlas_map', dict(pointer=1, value=1)), ('atlas_font', dict(args=FONT_ARGS, face_hex='00'))):
                with self.assertRaises(ValueError): platform.request(op, **args)
            dc = platform.request('atlas_dc')['result']
            with self.assertRaises(ValueError): platform.request('atlas_dib', pointer=dc, header_hex='00'*40)
            platform.request('atlas_dib', pointer=dc, header_hex=bitmap_header().hex())
            platform.request('atlas_map', pointer=dc, value=1)
            with self.assertRaises(ValueError): platform.request('atlas_muldiv', args=[8, 96, 72])
            platform.request('atlas_muldiv', args=[12, 96, 72])
            with self.assertRaises(ValueError): platform.request('atlas_font', args=[-15]+FONT_ARGS[1:], face_hex='4669786564537973')
        self.assertTrue(platform.cleanup['all_owned_resources_released'])
        with self.assertRaises(ValueError): platform.request('atlas_dc')
