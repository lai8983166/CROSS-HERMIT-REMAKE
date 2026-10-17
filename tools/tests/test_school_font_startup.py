import struct
import unittest
from tools.school_font_startup import *


class SourceTests(unittest.TestCase):
    def test_source_and_missing_original_cache_are_bound(self):
        self.assertEqual(source_contract()['inherited_head'], 0x4D61D08)
        self.assertFalse(source_contract()['checkpoint']['cache_head_target_mapped'])

    def test_font_constructor_retains_unwritten_bytes(self):
        for fill in (0xCD, 0xA5):
            before = bytes([fill])*80
            after = font_constructor(before)
            self.assertEqual(struct.unpack_from('<3I', after), (0x5D1154, 1, 0))
            self.assertEqual(after[12:72], before[12:72])
            self.assertEqual(after[72:], bytes(8))

    def test_cache_constructor_and_device_prefix_preserve_padding(self):
        before = b'\xcd'*176
        result = cache_constructor(before)
        self.assertEqual(result[0x50:0x60], before[0x50:0x60])
        self.assertEqual(result[0x70:0x98], before[0x70:0x98])
        caps = bytearray(212)
        struct.pack_into('<I', caps, 12, 0x20000000)
        after = cache_prefix(before, 0x1234, caps)
        self.assertEqual(dword(after, 4), 0x1234)
        self.assertEqual(after[0x70:0x98], before[0x70:0x98])
        self.assertEqual(dword(after, 0x50), 0x20000000)

    def test_source_texture_usage_pool_paths(self):
        for flags, usage, pool in ((0, 0, 1), (0x20000000, 512, 0)):
            caps = bytearray(212)
            struct.pack_into('<I', caps, 12, flags)
            self.assertEqual(texture_arguments(123, caps), [123, CACHE+88, CACHE+92, 0, usage, CACHE+84, pool])

    def test_incomplete_object_and_caps_refused(self):
        for fn, args in ((font_constructor, (bytes(79),)), (cache_constructor, (bytes(175),)),
                         (cache_prefix, (bytes(176), 1, bytes(211))), (texture_arguments, (1, bytes(211)))):
            with self.assertRaises(ValueError):
                fn(*args)
