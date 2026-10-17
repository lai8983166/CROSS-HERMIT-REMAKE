import struct
import unittest

from tools.school_device_init import (
    ATTEMPTS, BASE, SOURCE, FORMATS, presentation, source_contract,
)


class SourceTests(unittest.TestCase):
    def test_preserved_original_import_descriptor_and_functions(self):
        source = source_contract()
        self.assertEqual(source['import_identity']['symbol'], 'Direct3DCreate8')
        self.assertEqual(source['import_identity']['sdk'], 220)
        self.assertEqual(len(source['functions']), 14)
        self.assertEqual(source['preferred_formats'], list(FORMATS))

    def test_original_direct_E8_calls_are_bound(self):
        raw = SOURCE.read_bytes()
        for row in source_contract()['instructions']:
            if row['mnemonic'] == 'call' and row['operands'].startswith('0x'):
                va = int(row['va'], 16)
                self.assertEqual(raw[va-BASE], 0xE8)
                self.assertEqual(va+5+struct.unpack_from('<i', raw, va-BASE+1)[0],
                                 int(row['operands'], 16))

    def test_windowed_original_presentation_has_all52_bytes(self):
        raw = presentation(1024, 768, 22, 0x12345678)
        self.assertEqual(len(raw), 52)
        self.assertEqual(struct.unpack('<13I', raw),
                         (1024, 768, 22, 1, 0, 1, 0x12345678, 1, 0, 0, 0, 0, 0))

    def test_original_four_fallback_pairs_and_software_bit(self):
        self.assertEqual(ATTEMPTS, ((1, 64), (1, 32), (2, 64), (2, 32)))
        self.assertEqual([flags | 4 for _, flags in ATTEMPTS], [68, 36, 68, 36])


if __name__ == '__main__':
    unittest.main()
