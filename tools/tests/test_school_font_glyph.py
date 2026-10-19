import struct
import unittest
from tools.school_font_glyph import *


class SourceTests(unittest.TestCase):
    def test_original_95_calls_and_16bit_conversion_source(self):
        c=source_contract();self.assertEqual(len(c['characters']),95);self.assertEqual(c['pixel_count'],65536)
        self.assertEqual(c['imports'][1]['symbol'],'ExtTextOutA');self.assertEqual(c['upload_stop'],'0x4017b6')

    def test_exact_wrap_threshold_UV_stores_and_untouched_padding(self):
        dims=[(127,8),(127,8)]+[(1,8)]*93
        rows,end=layout(dims);self.assertEqual((rows[1]['x'],rows[1]['y']),(128,0));self.assertEqual((rows[2]['x'],rows[2]['y']),(0,9))
        before=bytes([0xCD])*1656;expected=bytearray(before)
        for n,r in enumerate(rows):struct.pack_into('<4f',expected,112+n*16,r['x']/256,r['y']/256,(r['x']+r['width'])/256,(r['y']+r['height'])/256)
        self.assertEqual(glyph_object(before,dims),expected);self.assertEqual(expected[1632:],before[1632:])

    def test_all_blue_values_zero_alpha_and_pitch_padding(self):
        dib=bytearray(262144)
        for y in range(256):
            for x in range(256):dib[(y*256+x)*4:(y*256+x)*4+4]=bytes((x,255-x,17,123))
        after=pixels(bytes(dib),bytes([0xA5])*(768*256),768)
        for y in (0,255):
            for x in range(256):self.assertEqual(struct.unpack_from('<H',after,y*768+x*2)[0],0 if x<16 else ((x//16)<<12)|4095)
            self.assertEqual(after[y*768+512:(y+1)*768],bytes([0xA5])*256)

    def test_incomplete_dimensions_buffers_and_pitch_refused(self):
        for f in (lambda:layout([(8,16)]*94),lambda:layout([(0,16)]*95),lambda:glyph_object(bytes(1655),[(8,16)]*95),lambda:pixels(bytes(262143),bytes(131072),512),lambda:pixels(bytes(262144),bytes(131072),511)):
            with self.assertRaises(ValueError):f()
