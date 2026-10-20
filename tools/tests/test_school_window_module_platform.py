import json
import unittest
from tools.school_window_module_platform import *
from tools.school_window_module import geometry
from tools.tests.test_school_window_geometry_platform import gate


def ready(p):
    if not gate(p):raise RuntimeError('actual duplicate gate prevents resource test')
    r=p.request('set_rect',before_hex='cd'*16,args=[0,0,1024,768])
    p.request('adjust_window_rect',before_hex=r['hex'],style=geometry.STYLE,menu=0)


class PlatformTests(unittest.TestCase):
    def test_actual_module_resources_and_four_native_shared_resource_calls(self):
        with ModulePlatform() as p:
            ready(p)
            a=p.request('load_icon',module=p.module,id_value=157)
            b=p.request('load_icon',module=p.module,id_value=157)
            c=p.request('load_cursor',module=0,id_value=32512)
            d=p.request('stock_brush',id_value=4)
            for r in (a,b,c,d):self.assertGreater(r['result'],0)
            self.assertTrue(a['shared'] and b['shared'] and c['shared'] and d['stock'])
            self.assertFalse(a['destroy_permitted'] or c['destroy_permitted'] or d['delete_permitted'])
        self.assertEqual(p.cleanup['icon_load_calls'],2)
        self.assertEqual(p.cleanup['resource_module_refs_released'],1)
        self.assertEqual(p.cleanup['gdi32_module_refs_released'],1)
        self.assertTrue(p.cleanup['all_owned_resources_released'])

    def test_refuses_early_foreign_wrong_or_duplicate_requests(self):
        with ModulePlatform() as p:
            with self.assertRaises(ValueError):p.request('load_icon',module=p.module,id_value=157)
            ready(p)
            for module,id_value in ((0,157),(p.module,1)):
                with self.assertRaises(ValueError):p.request('load_icon',module=module,id_value=id_value)
            with self.assertRaises(ValueError):p.request('load_cursor',module=0,id_value=32512)
            for i in range(2):p.request('load_icon',module=p.module,id_value=157)
            with self.assertRaises(ValueError):p.request('load_icon',module=p.module,id_value=157)
            with self.assertRaises(ValueError):p.request('load_cursor',module=p.module,id_value=32512)
            p.request('load_cursor',module=0,id_value=32512)
            with self.assertRaises(ValueError):p.request('stock_brush',id_value=0)
            p.request('stock_brush',id_value=4)
            with self.assertRaises(ValueError):p.request('stock_brush',id_value=4)

    def test_partial_cleanup_releases_only_owned_modules_and_resources(self):
        for count in (0,1,2):
            with ModulePlatform() as p:
                if count:
                    ready(p)
                    for i in range(count):p.request('load_icon',module=p.module,id_value=157)
            self.assertEqual(p.cleanup['icon_load_calls'],count)
            self.assertEqual(p.cleanup['shared_icons_destroyed'],0)
            self.assertFalse(p.cleanup['shared_cursor_destroyed'] or p.cleanup['stock_brush_deleted'])
            self.assertEqual(p.cleanup['resource_module_refs_released'],1)
            self.assertTrue(p.cleanup['all_owned_resources_released'])

    def test_actual_code_free_module_and_immutable_helper_build(self):
        r=json.loads((ROOT/'analysis/school-window-module-platform-v1-20261020.json').read_text(encoding='utf8'))
        self.assertEqual(r['build'],dict(source_sha256=sha(SOURCE.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),machine=0x14C))
        with ModulePlatform() as p:
            self.assertEqual(p.provenance,r['system_modules'])
            self.assertEqual(p.hello['resource_module']['entry_point'],0)
            self.assertEqual(p.hello['resource_module']['resources'],r['hello']['resource_module']['resources'])
            self.assertEqual(len(p.provenance),4)


if __name__=='__main__':unittest.main()
