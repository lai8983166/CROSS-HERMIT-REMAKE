import struct
import unittest
from tools.school_font_slots import *


class SourceTests(unittest.TestCase):
    def test_original_tables_calls_and_native_copy_ranges(self):
        c = source_contract()
        self.assertEqual([s['size'] for s in c['slots']], [12, 8])
        self.assertEqual(c['allocation_bytes'], 1656)
        self.assertEqual(c['texture_parameters']['format'], 26)
        self.assertIn('0x56ce01', [r['va'] for r in c['functions']])

    def test_complete_constructor_retains_all_nonfield_bytes(self):
        for fill in (0xA5, 0xCD):
            for index, (name, size, flags) in enumerate(((b'FixedSys\0', 12, 1), (bytes.fromhex('b2d3a9fac5e92000'), 8, 0))):
                expected = bytearray([fill]*1656)
                expected[:len(name)] = name
                for at, value in ((80, size), (84, flags), (88, 0), (92, 0), (96, 0), (1648, 0), (1652, 0)):
                    struct.pack_into('<I', expected, at, value)
                self.assertEqual(constructor(bytes([fill])*1656, index), expected)

    def test_atlas_size_thresholds_and_unsigned_maxwidth_clamp(self):
        for size, dim in ((0, 256), (20, 256), (21, 512), (40, 512), (41, 1024), (0xFFFFFFFF, 1024)):
            for maximum in (128, 256, 8192):
                before = bytearray(constructor(b'\xcd'*SIZE))
                struct.pack_into('<I', before, 80, size)
                expected = bytearray(before)
                for at, value in ((88, 0x12345678), (100, min(dim, maximum)), (104, min(dim, maximum))):
                    struct.pack_into('<I', expected, at, value)
                struct.pack_into('<f', expected, 108, min(maximum/dim, 1))
                self.assertEqual(atlas(bytes(before), 0x12345678, maximum), expected)

    def test_invalid_full_objects_indices_or_live_inputs_refused(self):
        for call in (lambda: constructor(bytes(1655)), lambda: constructor(bytes(1656), 2),
                     lambda: atlas(bytes(1655), 1, 256), lambda: atlas(bytes(1656), 0, 256),
                     lambda: atlas(bytes(1656), 1, 0)):
            with self.assertRaises(ValueError): call()
