import struct
import unittest

from tools.school_renderer_init import (
    ARENA_BYTES, LAYER_COUNT, SOURCE, BASE, bind, clip, constructor,
    dword, initialize_queues, rectangle_packet, source_contract,
)


class SourceTests(unittest.TestCase):
    def test_source_identity_calls_tables_and_outer_order(self):
        contract = source_contract()
        self.assertEqual(contract['queue']['layer_bytes'], 32768)
        self.assertEqual(len(contract['functions']), 17)
        raw = SOURCE.read_bytes()
        for row in contract['instructions']:
            if row['mnemonic'] == 'call':
                va = int(row['va'], 16)
                self.assertEqual(raw[va-BASE], 0xE8)
                target = va + 5 + struct.unpack_from('<i', raw, va-BASE+1)[0]
                self.assertEqual(target, int(row['operands'], 16))

    def test_constructor_preserves_unspecified_fields(self):
        original = bytes([0xA5])*96
        after = constructor(original)
        self.assertEqual(dword(after, 0x18), 1)
        self.assertEqual(dword(after, 0x20), 1)
        for offset in (8, 12, 0x28, 0x2C, 0x38, 0x3C):
            self.assertEqual(after[offset:offset+4], original[offset:offset+4])
        bound = bind(after, 0x2000000, 0x12345678)
        self.assertEqual(struct.unpack_from('<2I', bound), (0x2000000, 0x12345678))
        self.assertEqual(bound[8:], after[8:])

    def test_queue_defaults_and_retained_fields(self):
        before = bind(constructor(bytes([0xA5])*96), 0x2000000, 0)
        after = initialize_queues(before, 0x3000000, 0x3010000)
        self.assertEqual(struct.unpack_from('<4I', after, 8),
                         (LAYER_COUNT, ARENA_BYTES, 0x3000000, 0x3010000))
        self.assertEqual(dword(after, 0x30), 0x3010000)
        self.assertEqual(dword(after, 0x1C), 0)
        self.assertEqual(after[0x38:0x40], bytes([0xA5])*8)

    def test_clip_is_rejection_with_strict_comparison_and_signed_abs(self):
        self.assertEqual(clip((274, 580, 473, 154), (1024, 768)), 0)
        self.assertEqual(clip((1297, 0, 273, 1), (1024, 768)), 0)
        self.assertEqual(clip((1298, 0, 273, 1), (1024, 768)), 1)
        self.assertEqual(clip((-1298, 0, 273, 1), (1024, 768)), 1)
        self.assertEqual(clip((0, -770, 1, 1), (1024, 768)), 1)
        self.assertEqual(clip((0x80000000, 0, 0, 0), (1024, 768)), 0)
        self.assertEqual(clip((0, 0, 0x7FFFFFFF, 0), (1024, 768)), 1)

    def test_rectangle_layout_keeps_padding_and_truncates_operands(self):
        packet = rectangle_packet(bytes([0xCD])*24, (-1, 580, 473, 154),
                                  0x10043, 0x223438, 0x101, 0x3010000)
        self.assertEqual(struct.unpack_from('<2I', packet), (0x3010000, 4))
        self.assertEqual(packet[8:10], b'\x01\xcd')
        self.assertEqual(struct.unpack_from('<5H', packet, 10),
                         (65535, 580, 473, 154, 67))
        self.assertEqual(dword(packet, 20), 0x223438)

    def test_invalid_projection_shapes_refused(self):
        for raw in (b'', bytes(95), bytes(97)):
            with self.assertRaises(ValueError):
                constructor(raw)
        with self.assertRaises(ValueError):
            bind(bytes(96), 0, 0)
        with self.assertRaises(ValueError):
            rectangle_packet(bytes(23), (0, 0, 1, 1), 0, 0, 1, 0)


if __name__ == '__main__':
    unittest.main()
