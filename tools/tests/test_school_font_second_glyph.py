import struct
import unittest
from copy import deepcopy
from tools.school_font_second_glyph import *


class SourceTests(unittest.TestCase):
    def test_source_exact_characters_accesses_and_mapping_authority(self):
        c=source_contract();self.assertEqual(c['characters'],list(range(32,127)))
        self.assertEqual(c['shared_glyph_source']['pixel_count'],65536)
        self.assertTrue(c['retirement_preserves_CPU']);self.assertTrue(c['first_texture_actual_readback_after_second_upload'])

    def test_dynamic_second_full_UV_object_preserves_padding(self):
        measures=[(4+(n%5),11+(n%2)) for n in range(95)]
        rows,end=layout(measures);expected=bytearray([0xCD]*1656)
        for n,r in enumerate(rows):struct.pack_into('<4f',expected,112+n*16,r['x']/256,r['y']/256,(r['x']+r['width'])/256,(r['y']+r['height'])/256)
        self.assertEqual(glyph_object(bytes([0xCD])*1656,measures),expected)
        self.assertGreater(end[1],0)

    def test_pixel_conversion_all_alpha_values_and_pitch_padding(self):
        dib=bytearray(262144)
        for n in range(65536):dib[n*4]=n%256
        before=bytes([0xA5])*(520*256);after=pixels(dib,before,520)
        for y in range(256):
            self.assertEqual(after[y*520+512:(y+1)*520],bytes([0xA5])*8)
            for x in range(256):self.assertEqual(struct.unpack_from('<H',after,y*520+x*2)[0],0 if x<16 else ((x>>4)<<12)|0xFFF)

    def test_exact_retired_DIB_region_preserves_live_texture_and_refuses_overlap(self):
        regions=[dict(name='DIB',pointer=0x30001000,base=0x30000000,bytes=270336,data_bytes=262144,buffer={'sha256':'retained'}),
                 dict(name='texture',pointer=0x31001000,base=0x31000000,bytes=139264,data_bytes=131072,buffer={'sha256':'live'})]
        active,retired=retire_regions(regions)
        self.assertEqual(active,[regions[1]]);self.assertEqual(retired[0]['region'],regions[0])
        self.assertFalse(retired[0]['native_game_call_executed']);self.assertFalse(retired[0]['host_release_performed_by_retirement'])
        for change in (lambda r:r.reverse(),lambda r:r[0].update(bytes=1),lambda r:r[1].update(pointer=0x30001000,base=0x30000000)):
            bad=deepcopy(regions);change(bad)
            with self.assertRaises(ValueError):retire_regions(bad)
