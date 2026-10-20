import unittest
from tools.school_window_geometry import *


class SourceTests(unittest.TestCase):
    def test_source_exact_api_stack_and_unexecuted_icon_call(self):
        s=source_contract()
        self.assertEqual([i['symbol'] for i in s['imports']],['SetRect','AdjustWindowRect'])
        self.assertEqual(s['stops']['class'],'0x450416')
        self.assertEqual(FRAME_SP,ENTRY_SP-148)
        self.assertFalse(s['LoadIconA_executed'])

    def test_only_original_class_fields_initialized(self):
        r=partial_class()
        self.assertEqual(len(r),48)
        self.assertEqual([dword(r,i*4) for i in (0,1,2,3,4,5,10)],[48,0,0x424980,0,0,window.HINSTANCE,window.TITLE])
        for i in (6,7,8,9,11):self.assertEqual(dword(r,i*4),0xCCCCCCCC)

    def test_full_owner_only_client_rectangle_changes(self):
        before=b'\xcd'*parent.BACKING;after=project_owner(before)
        self.assertEqual(after[:CLIENT_OFFSET],before[:CLIENT_OFFSET])
        self.assertEqual(after[CLIENT_OFFSET:CLIENT_OFFSET+16],CLIENT_RECT)
        self.assertEqual(after[CLIENT_OFFSET+16:],before[CLIENT_OFFSET+16:])

    def test_original_icon157_matches_captured_source_resource(self):
        r=resource_contract()
        self.assertEqual(r['modules'][0]['icons'],r['modules'][1]['icons'])
        self.assertEqual((r['group_id'],r['image_id'],r['language'],r['width'],r['height'],r['bits_per_pixel']),(157,5,1041,32,32,8))
        self.assertFalse(r['module_loaded'] or r['icon_loaded'])


if __name__=='__main__':unittest.main()
