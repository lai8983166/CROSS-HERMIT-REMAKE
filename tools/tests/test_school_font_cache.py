import struct
import unittest
from tools.school_font_cache import *


class SourceTests(unittest.TestCase):
    def test_original_calls_imports_and_complete_native_returns(self):
        self.assertEqual(len(source_contract()['imports']), 7)
        raw, md = SOURCE.read_bytes(), Cs(CS_ARCH_X86, CS_MODE_32)
        for start, end in RANGES.items():
            body = list(md.disasm(raw[start-BASE:end-BASE], start))
            self.assertEqual(body[-1].address+body[-1].size, end)
            self.assertEqual(body[-1].mnemonic, 'ret')

    def test_sprite_flags_follow_both_original_source_predicates(self):
        caps, creation = bytearray(212), bytearray(16)
        self.assertEqual(struct.unpack('<8I', sprite(bytes(32), 1, caps, creation)), (0x5D1180, 1, 1, 0, 0, 0, 0, 0))
        caps[44], caps[48], creation[12] = 16, 32, 16
        self.assertEqual(struct.unpack('<8I', sprite(bytes(32), 1, caps, creation))[-2:], (1, 1))
        caps[48], creation[12], caps[33] = 0, 0, 2
        self.assertEqual(struct.unpack('<8I', sprite(bytes(32), 1, caps, creation))[-2:], (0, 1))

    def test_header_negation_and_complete_cache_gdi_projection(self):
        self.assertEqual(len(bitmap_header()), 40)
        self.assertEqual(struct.unpack_from('<i', bitmap_header(True), 8)[0], -256)
        after = cache_after_gdi(b'\xcd'*176, 1, 2, 3, 4)
        self.assertEqual(after[0x70:0x98], bitmap_header())
        self.assertEqual(after[0xA8:0xAC], b'\xcd'*4)
        self.assertEqual(dword(after, 12), SPRITE)
        self.assertEqual(dword(after, 0xA0), 4)

    def test_font_complete_copies_all60_bytes_and_cache_device(self):
        logfont = bytes(range(60))
        after = font_complete(123, 456, logfont)
        self.assertEqual(len(after), 80)
        self.assertEqual(after[12:72], logfont)
        self.assertEqual(struct.unpack_from('<2I', after, 72), (CACHE, 123))

    def test_incomplete_buffers_and_foreign_null_handles_refused(self):
        for fn, args in ((sprite, (bytes(31), 1, bytes(212), bytes(16))),
                         (cache_before_gdi, (bytes(175),)), (font_complete, (1, 2, bytes(59))),
                         (cache_after_gdi, (bytes(176), 1, 2, 0, 4))):
            with self.assertRaises(ValueError):
                fn(*args)
