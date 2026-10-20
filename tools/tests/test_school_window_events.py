import unittest
from tools.school_window_events import *


class SourceTests(unittest.TestCase):
    def test_original_size_switch_and_default_routes_are_pinned(self):
        r=source_contract();self.assertEqual(r['admitted_messages'],[129,131,1,5,3,24,70])
        self.assertEqual(r['WINDOWPOS']['bytes'],28);self.assertFalse(r['captured_game_global_modified'])

    def test_size_is_unsigned_move_signed_and_show_reason_scalar(self):
        self.assertEqual(scalar(5,0,1024+(768<<16)),dict(width=1024,height=768,size_state=0))
        self.assertEqual(scalar(3,0,0xFFFF0001),dict(x=1,y=-1))
        self.assertEqual(scalar(24,1,0),dict(shown=True,reason=0))
        for msg,w,l in ((70,0,1),(5,-1,0),(3,0,0x100000000)):
            with self.assertRaises(ValueError):scalar(msg,w,l)

    def test_windowpos_exact_x86_layout_and_owned_handle(self):
        b=struct.pack('<II4iI',123,0,-1,16,1024,768,0x43)
        self.assertEqual(windowpos(b,123)['x'],-1)
        for data,h in ((b[:-1],123),(b,124)):
            with self.assertRaises(ValueError):windowpos(data,h)


if __name__=='__main__':unittest.main()
