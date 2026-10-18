import json
import unittest
from tools.school_font_cache_platform import *


class PlatformTests(unittest.TestCase):
    def test_both_builds_and_immutable_parent_sources(self):
        r = json.loads((ROOT/'analysis/school-font-cache-platform-v1-20261018.json').read_text(encoding='utf-8'))
        for key, source, helper in (('device', DEVICE_SOURCE, DEVICE_HELPER), ('gdi', GDI_SOURCE, GDI_HELPER)):
            self.assertEqual(r['builds'][key], dict(source_sha256=sha(source.read_bytes()), helper_sha256=sha(helper.read_bytes()),
                             compiler_sha256=sha(COMPILER.read_bytes()), machine=0x14C))
            with self.assertRaises(ValueError):
                build_one(source, helper)
        parents = [('analysis/school-font-texture-bridge-v1-20261018.json', 'tools/school_font_texture_bridge.cs', 'build'),
                   ('analysis/school-owner-startup-platform-v2-20261017.json', 'tools/school_owner_platform.cs', 'build')]
        for report, source, key in parents:
            self.assertEqual(json.loads((ROOT/report).read_text())[key]['source_sha256'], sha((ROOT/source).read_bytes()))

    def test_live_owned_cache_GDI_and_indirect_font_cleanup(self):
        r = gdi_probe()
        self.assertGreater(r['bitmap']['bits'], 0)
        self.assertEqual(r['indirect']['inspection'], dict(native_requested=False, method='GetObjectA', result=60, hex=r['logfont']['hex']))
        self.assertEqual(r['cleanup'], dict(fonts_released=2, dcs_released=1, cache_bitmaps_released=1,
                         cache_dcs_released=1, cache_selection_restored=True, all_owned_resources_released=True))

    def test_live_device_sprite_and_font_references_balance(self):
        r = device_probe()
        self.assertEqual(r['calls'][0]['result']['count'], 4)
        self.assertEqual(r['calls'][3]['result']['count'], 5)
        self.assertEqual(len(bytes.fromhex(r['calls'][1]['result']['hex'])), 212)
        self.assertEqual(len(bytes.fromhex(r['calls'][2]['result']['hex'])), 16)
        self.assertEqual(r['cleanup']['extra_reference_release_counts'], [3, 2, 1])
        self.assertTrue(r['cleanup']['all_owned_resources_released'])

    def test_foreign_or_unordered_GDI_and_closed_requests_refused(self):
        with CachePlatform() as platform:
            for op, args in [('CreateCompatibleDC', {}), ('SetBkMode', dict(pointer=1, value=2)),
                             ('CreateDIBSection', dict(pointer=1, header_hex='00'*40)),
                             ('CreateFontIndirectA', dict(logfont_hex='00'*60))]:
                with self.assertRaises(ValueError):
                    platform.request(op, **args)
        self.assertTrue(platform.cleanup['all_owned_resources_released'])
        with self.assertRaises(ValueError):
            platform.request('GetDC')

    def test_unordered_or_duplicate_device_references_refused(self):
        from tools.school_font_texture_bridge import setup
        def run(bridge):
            device, _ = setup(bridge)
            for op in ('sprite_addref', 'font_addref', 'sprite_caps'):
                with self.assertRaises(ValueError):
                    bridge.request(op, pointer=device)
            tex = bridge.request('texture_create', pointer=device, width=64, height=16, levels=1, usage=512, format=21, pool=0)
            bridge.request('texture_surface', pointer=tex['texture']['pointer'], level=0)
            bridge.request('sprite_addref', pointer=device)
            with self.assertRaises(ValueError):
                bridge.request('sprite_addref', pointer=device)
        r = owned_run(run)
        self.assertEqual(r['cleanup']['extra_reference_release_counts'], [2, 1])
        self.assertTrue(r['cleanup']['all_owned_resources_released'])
