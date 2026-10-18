import struct
import unittest
from tools.school_font_atlas import *


class SourceTests(unittest.TestCase):
    def test_original_imports_native_arithmetic_and_boundary(self):
        c = source_contract()
        self.assertEqual(c['imports'][3]['symbol'], 'MulDiv')
        self.assertEqual(c['imports'][-1]['symbol'], 'GetTextExtentPoint32A')
        self.assertEqual(c['GDI_stop'], '0x401491')
        self.assertFalse(c['glyph_measurement_executed'])

    def test_complete_top_down_bitmap_header(self):
        self.assertEqual(bitmap_header(), bytes.fromhex('280000000001000000ffffff01002000')+bytes(24))

    def test_complete_original_fixedsys_LOGFONT(self):
        expected = bytearray(60)
        struct.pack_into('<i', expected, 0, -16); struct.pack_into('<i', expected, 16, 700)
        expected[23], expected[26], expected[27] = 1, 4, 2
        expected[28:36] = b'FixedSys'
        self.assertEqual(font_logfont(), expected)

    def test_full_object_texture_store_preserves_padding_and_refuses_bad_input(self):
        before = bytes([0xCD])*1656
        expected = bytearray(before); struct.pack_into('<I', expected, 92, 0x12345678)
        self.assertEqual(texture_object(before, 0x12345678), expected)
        for data, pointer in ((bytes(1655), 1), (before, 0), (before, 0x100000000)):
            with self.assertRaises(ValueError): texture_object(data, pointer)
