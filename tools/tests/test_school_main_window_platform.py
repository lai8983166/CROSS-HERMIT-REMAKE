import json
import unittest
from tools.school_main_window_platform import *
from tools.tests.test_school_main_context_platform import prefix

TITLE_HEX=b'Cross Hermit\0'.hex()


def constructor(platform):
    prefix(platform)
    d=platform.request('GetCurrentDirectoryA',before_hex='cd'*525)
    d=platform.request('PathAddBackslashA',before_hex=d['hex'])
    text=bytes.fromhex(d['hex']).split(b'\0',1)[0]+b'\0'
    for i in range(7):r=platform.request('lstrcpyA',before_hex='cd'*260,source_hex=text.hex())
    platform.request('lstrcatA',before_hex=r['hex'],source_hex=b'SaveData\\\0'.hex())


class PlatformTests(unittest.TestCase):
    def test_complete_title_copy_and_actual_borrowed_window_query(self):
        with MainWindowPlatform() as p:
            constructor(p)
            r=p.request('copy_title',before_hex='a5'*256,source_hex=TITLE_HEX)
            value=bytes.fromhex(TITLE_HEX)
            self.assertEqual(bytes.fromhex(r['hex']),value+b'\xa5'*(256-len(value)))
            r=p.request('find_window',class_hex=TITLE_HEX,window_name=0)
            self.assertIs(type(r['result']),int)
            self.assertTrue(0<=r['result']<=0xFFFFFFFF)
            self.assertTrue(r['class_unchanged'] and r['guards_unchanged'])
            self.assertFalse(r['window_owned'] or r['window_manipulated'])
        self.assertEqual(p.cleanup,dict(critical_sections_deleted=2,event_handles_closed=1,user32_module_refs_released=1,all_owned_resources_released=True))

    def test_refuses_early_wrong_foreign_and_duplicate_requests(self):
        with MainWindowPlatform() as p:
            with self.assertRaises(ValueError):p.request('copy_title',before_hex='a5'*256,source_hex=TITLE_HEX)
            with self.assertRaises(ValueError):p.request('find_window',class_hex=TITLE_HEX,window_name=0)
            constructor(p)
            for args in (dict(before_hex='a5'*255,source_hex=TITLE_HEX),dict(before_hex='a5'*256,source_hex='00')):
                with self.assertRaises(ValueError):p.request('copy_title',**args)
            p.request('copy_title',before_hex='a5'*256,source_hex=TITLE_HEX)
            with self.assertRaises(ValueError):p.request('find_window',class_hex=TITLE_HEX,window_name=1)
            with self.assertRaises(ValueError):p.request('find_window',class_hex=b'Other\0'.hex(),window_name=0)
            p.request('find_window',class_hex=TITLE_HEX,window_name=0)
            with self.assertRaises(ValueError):p.request('find_window',class_hex=TITLE_HEX,window_name=0)
            with self.assertRaises(ValueError):p.request('copy_title',before_hex='a5'*256,source_hex=TITLE_HEX)
        self.assertTrue(p.cleanup['all_owned_resources_released'])

    def test_partial_cleanup_releases_owned_module_and_constructor_resources(self):
        for stage in (0,1,2):
            with MainWindowPlatform() as p:
                if stage:constructor(p)
                if stage==2:p.request('copy_title',before_hex='cc'*256,source_hex=TITLE_HEX)
            self.assertEqual(p.cleanup['critical_sections_deleted'],2 if stage else 0)
            self.assertEqual(p.cleanup['event_handles_closed'],1 if stage else 0)
            self.assertEqual(p.cleanup['user32_module_refs_released'],1)
            self.assertTrue(p.cleanup['all_owned_resources_released'])

    def test_immutable_x86_source_binary_and_three_actual_system_modules(self):
        r=json.loads((ROOT/'analysis/school-main-window-platform-v1-20261020.json').read_text(encoding='utf8'))
        self.assertEqual(r['build'],dict(source_sha256=sha(SOURCE.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),helper_sha256=sha(HELPER.read_bytes()),machine=0x14C))
        with MainWindowPlatform() as p:
            self.assertEqual(p.hello,r['hello']);self.assertEqual(p.provenance,r['system_modules'])
            self.assertEqual(len(p.provenance),3)
            self.assertFalse(p.hello['window_created'])


if __name__=='__main__':unittest.main()
