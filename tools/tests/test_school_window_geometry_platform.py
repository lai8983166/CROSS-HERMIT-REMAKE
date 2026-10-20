import json
import unittest
from tools.school_window_geometry_platform import *
from tools.school_window_geometry import CLIENT_RECT,STYLE
from tools.tests.test_school_main_window_platform import constructor,TITLE_HEX


def gate(p):
    constructor(p);p.request('copy_title',before_hex='cd'*256,source_hex=TITLE_HEX)
    return p.request('find_window',class_hex=TITLE_HEX,window_name=0)['result']==0


class PlatformTests(unittest.TestCase):
    def test_actual_geometry_full_guarded_buffers_and_no_window(self):
        with GeometryPlatform() as p:
            absent=gate(p)
            if absent:
                r=p.request('set_rect',before_hex='a5'*16,args=[0,0,1024,768])
                self.assertNotEqual(r['result'],0);self.assertEqual(r['hex'],CLIENT_RECT.hex());self.assertTrue(r['guards_unchanged'])
                r=p.request('adjust_window_rect',before_hex=r['hex'],style=STYLE,menu=0)
                self.assertNotEqual(r['result'],0);self.assertEqual(r['hex'],CLIENT_RECT.hex());self.assertTrue(r['guards_unchanged'])
            else:
                with self.assertRaises(ValueError):p.request('set_rect',before_hex='a5'*16,args=[0,0,1024,768])
            self.assertFalse(p.hello['window_created'])
        self.assertEqual(p.cleanup['set_rect_calls'],int(absent));self.assertEqual(p.cleanup['adjust_window_rect_calls'],int(absent))
        self.assertTrue(p.cleanup['all_owned_resources_released'])

    def test_refuses_early_malformed_changed_style_and_duplicate_calls(self):
        with GeometryPlatform() as p:
            with self.assertRaises(ValueError):p.request('set_rect',before_hex='cd'*16,args=[0,0,1024,768])
            with self.assertRaises(ValueError):p.request('adjust_window_rect',before_hex=CLIENT_RECT.hex(),style=STYLE,menu=0)
            absent=gate(p)
            if absent:
                for args in (dict(before_hex='cd'*15,args=[0,0,1024,768]),dict(before_hex='cd'*16,args=[0,0,800,600])):
                    with self.assertRaises(ValueError):p.request('set_rect',**args)
                r=p.request('set_rect',before_hex='cd'*16,args=[0,0,1024,768])
                for style,menu in ((0,0),(STYLE,1)):
                    with self.assertRaises(ValueError):p.request('adjust_window_rect',before_hex=r['hex'],style=style,menu=menu)
                with self.assertRaises(ValueError):p.request('adjust_window_rect',before_hex='cd'*16,style=STYLE,menu=0)
                p.request('adjust_window_rect',before_hex=r['hex'],style=STYLE,menu=0)
                with self.assertRaises(ValueError):p.request('set_rect',before_hex='cd'*16,args=[0,0,1024,768])
                with self.assertRaises(ValueError):p.request('adjust_window_rect',before_hex=r['hex'],style=STYLE,menu=0)
        self.assertTrue(p.cleanup['all_owned_resources_released'])

    def test_partial_cleanup_and_actual_geometry_counters(self):
        for stage in (0,1,2,3):
            with GeometryPlatform() as p:
                absent=gate(p) if stage else False
                if stage>=2 and absent:r=p.request('set_rect',before_hex='cc'*16,args=[0,0,1024,768])
                if stage==3 and absent:p.request('adjust_window_rect',before_hex=r['hex'],style=STYLE,menu=0)
            self.assertEqual(p.cleanup['critical_sections_deleted'],2 if stage else 0)
            self.assertEqual(p.cleanup['event_handles_closed'],1 if stage else 0)
            self.assertEqual(p.cleanup['user32_module_refs_released'],1)
            self.assertEqual(p.cleanup['set_rect_calls'],int(stage>=2 and absent))
            self.assertEqual(p.cleanup['adjust_window_rect_calls'],int(stage==3 and absent))
            self.assertTrue(p.cleanup['all_owned_resources_released'])

    def test_immutable_x86_build_and_actual_system_modules(self):
        r=json.loads((ROOT/'analysis/school-window-geometry-platform-v1-20261020.json').read_text(encoding='utf8'))
        self.assertEqual(r['build'],dict(source_sha256=sha(SOURCE.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),machine=0x14C))
        with GeometryPlatform() as p:self.assertEqual(p.provenance,r['system_modules'])


if __name__=='__main__':unittest.main()
