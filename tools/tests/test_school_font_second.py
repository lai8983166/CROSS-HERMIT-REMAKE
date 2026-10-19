import struct
import unittest
from tools.school_font_second import *


class SourceTests(unittest.TestCase):
    def test_source_loop_tables_and_unexecuted_return(self):
        c = source_contract()
        self.assertEqual(c['loop_trace'], [hex(a) for a in LOOP_TRACE])
        self.assertEqual(c['slot_source']['slots'][1], dict(index=1, face_pointer=0x592C9C,
            face_hex='b2d3a9fac5e920', size=8, flags=0))
        self.assertEqual(c['owner_offset'], 0x1094)
        self.assertFalse(c['return_source']['executed'])
        self.assertEqual(c['total_declared_allocation_counter_delta'], 3600)

    def test_second_full_object_face_fields_and_padding(self):
        before = bytes([0xCD])*1656
        expected = bytearray(before)
        expected[:8] = bytes.fromhex('b2d3a9fac5e92000')
        for at, value in ((0x50,8),(0x54,0),(0x58,0),(0x5C,0),(0x60,0),(0x670,0),(0x674,0)):
            struct.pack_into('<I', expected, at, value)
        self.assertEqual(constructor(before), expected)

    def test_second_atlas_full_projection_caps_clamp_and_scale(self):
        initial = constructor(bytes([0xCD])*1656)
        for maximum, dimension, scale in ((4096,256,1.0),(128,128,0.5)):
            expected = bytearray(initial)
            for at, value in ((0x58,0x12345678),(0x64,dimension),(0x68,dimension)):
                struct.pack_into('<I', expected, at, value)
            struct.pack_into('<f', expected, 0x6C, scale)
            self.assertEqual(atlas(initial,0x12345678,maximum), expected)

    def test_bad_buffer_caps_or_device_refused(self):
        for f in (lambda:constructor(bytes(1655)),lambda:atlas(bytes(1656),0,256),
                  lambda:atlas(bytes(1656),1,0),lambda:atlas(bytes(1655),1,256)):
            with self.assertRaises(ValueError): f()
