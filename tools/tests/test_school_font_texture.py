import struct
import unittest
from tools.school_font_texture import *


class SourceTests(unittest.TestCase):
    def test_complete_original_table_debug_target_and_calls(self):
        contract = source_contract()
        self.assertEqual(len(contract['formats']), 43)
        self.assertEqual([r['fields'][0] for r in contract['formats'][:2]], [20, 21])
        self.assertEqual(contract['inherited_debug_target'], DEBUG_TARGET)

    def caps(self, flags=0x4000, aspect=0):
        caps = bytearray(212)
        for offset, value in {60: flags, 88: 1024, 92: 512, 104: aspect}.items():
            struct.pack_into('<I', caps, offset, value)
        return caps

    def test_source_size_limits_aspect_and_power_of_two(self):
        self.assertEqual(requirements(2000, 600, 1, self.caps())['width'], 1024)
        self.assertEqual(requirements(3, 5, 1, self.caps(0x4002)), dict(width=4, height=8, levels=1, format=21))
        self.assertEqual(requirements(64, 16, 1, self.caps(0x4020)), dict(width=16, height=16, levels=1, format=21))

    def test_source_mipmap_paths(self):
        self.assertEqual(requirements(64, 16, 0, self.caps())['levels'], 7)
        self.assertEqual(requirements(64, 16, 30, self.caps())['levels'], 7)
        self.assertEqual(requirements(63, 16, 0, self.caps(0x4100))['levels'], 1)
        self.assertEqual(requirements(64, 16, 0, self.caps(0))['levels'], 1)

    def test_only_actual_texture_surface_slots_change(self):
        before = b'\xcd'*176
        result = bytearray(texture_cache(before, 123, 456))
        self.assertEqual(dword(result, 16), 123)
        self.assertEqual(dword(result, 48), 456)
        result[16:20] = before[16:20]
        result[48:52] = before[48:52]
        self.assertEqual(result, before)

    def test_incomplete_or_unowned_inputs_refused(self):
        for fn, args in ((requirements, (1, 1, 1, bytes(211))),
                         (texture_cache, (bytes(175), 1, 2)), (texture_cache, (bytes(176), 0, 2))):
            with self.assertRaises(ValueError):
                fn(*args)
