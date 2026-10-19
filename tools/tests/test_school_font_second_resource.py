import struct
import unittest
from tools.school_font_second_resource import *


class SourceTests(unittest.TestCase):
    def test_original_second_tables_and_font_flag_arithmetic(self):
        c=source_contract()
        self.assertEqual(c['muldiv_args'],[8,96,72])
        self.assertEqual(c['font_args'],[-11,0,0,0,400,0,0,0,1,0,0,4,2])
        self.assertEqual(c['face_hex'],'b2d3a9fac5e920')
        self.assertEqual(c['GDI_stop'],'0x401491')

    def test_full_raw_ANSI_LOGFONT_and_top_down_bitmap(self):
        expected=struct.pack('<5i',-11,0,0,0,400)+bytes([0,0,0,1,0,0,4,2])+FACE+bytes(25)
        self.assertEqual(font_logfont(),expected)
        self.assertEqual(len(expected),60)
        self.assertEqual(bitmap_header(),struct.pack('<IiiHH6I',40,256,-256,1,32,0,0,0,0,0,0))

    def test_full_second_texture_projection_preserves_all_padding(self):
        before=bytes([0xCD])*1656;expected=bytearray(before)
        struct.pack_into('<I',expected,0x5C,0x12345678)
        self.assertEqual(texture_object(before,0x12345678),expected)
        self.assertEqual(source_contract()['texture_output'],SECOND+0x5C)

    def test_invalid_full_object_or_texture_identity_refused(self):
        for before,pointer in ((bytes(1655),1),(bytes(1656),0),(bytes(1656),0x100000000)):
            with self.assertRaises(ValueError):texture_object(before,pointer)
