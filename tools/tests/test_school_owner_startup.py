import struct
import unittest

from tools.school_owner_startup import source_contract, project_constructor, project_image, dword, SOURCE


class SourceTests(unittest.TestCase):
    def api(self):
        return {'GetDC': {'result': 0x1234},
                'QueryPerformanceCounter': {'result': 1, 'hex': struct.pack('<Q', 123456789).hex()},
                'QueryPerformanceFrequency': {'result': 1, 'hex': struct.pack('<Q', 10000000).hex()}}

    def test_original_imports_constructor_and_static_font_boundary(self):
        contract = source_contract()
        self.assertEqual([r['symbol'] for r in contract['imports']],
                         ['GetDC', 'QueryPerformanceCounter', 'QueryPerformanceFrequency', 'CreateFontA', 'GetObjectA'])
        self.assertIn('0x56dda0', [r['va'] for r in contract['functions']])
        self.assertEqual(contract['face_hex'], 'b2d3a9fac5e920')

    def test_full_constructor_zeros_old_fonts_sets_gate_and_preserves_padding(self):
        for fill in (0xA5, 0xCC):
            before = bytes([fill])*0xC000
            after = project_constructor(before, self.api())
            for offset in (0xB26C, 0xB270, 0x1090, 0x1094, 0xB20C, 0xB210):
                self.assertEqual(dword(after, offset), 0)
            self.assertEqual(struct.unpack_from('<4H', after, 0xB288), (0, 1, 0, 1))
            self.assertEqual(after[0xB1A4:0xB1A8], bytes([fill])*4)
            self.assertEqual(dword(after, 0xB208), 0x1234)
            self.assertEqual(dword(after, 0xB188), 10000000)

    def test_child_constructor_float_depends_on_declared_dirty_input(self):
        after = project_constructor(bytes([0xA5])*0xC000, self.api())
        for at in (0x8C88, 0x8F00):
            self.assertEqual(after[at+0x26C:at+0x270], struct.pack('<f', -1515870811))
            self.assertEqual(after[at+0x24C:at+0x250], b'\xa5'*4)

    def test_global_pool_and_timer_image_projection_is_bounded(self):
        expected = project_image(self.api())
        self.assertEqual(expected[0x365728:0x39172A], bytes(0x2C002))
        self.assertEqual(expected[:0x1FF530], SOURCE.read_bytes()[:0x1FF530])
        self.assertEqual(expected[0x399AE8:0x399AF0], struct.pack('<Q', 123456789))

    def test_bad_owner_length_refused(self):
        with self.assertRaises(ValueError):
            project_constructor(bytes(10), self.api())


if __name__ == '__main__':
    unittest.main()
