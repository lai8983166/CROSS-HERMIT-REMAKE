import hashlib
import unittest
from pathlib import Path

from devtools.terminal_tcg_build_identity import inspect
from devtools.terminal_tcg_fp_probe import decode, image

ROOT = Path(__file__).resolve().parents[2]
WORKER = ROOT / '.venv-audit/native-worker'


class TCGFPProbeTests(unittest.TestCase):
    def test_executed_image_is_reproducible(self):
        raw = (WORKER / 'tcg-fp-v1-20261110/guest.elf').read_bytes()
        self.assertEqual(image()[0], raw)

    def test_actual_nonzero_pointer_contrast(self):
        raw = (WORKER / 'tcg-fp-v1-20261110/guest.bin').read_bytes()
        r = decode(raw)
        expected = image()[1]
        for name in ('fip', 'fdp', 'fcs', 'fds'):
            self.assertEqual(r['env'][name], expected[name])
            self.assertEqual(r['fx'][name], 0)
        self.assertEqual(r['env']['fop'], 0)
        self.assertEqual(r['fx']['fop'], 0xa5a5)
        self.assertEqual(r['fx']['st0'], '00000000000000c00040')
        self.assertEqual(r['cpuid_7_0_ebx'] & ((1 << 6) | (1 << 13)), 0)

    def test_truncated_or_extended_frame_rejected(self):
        for count in (0, 543, 545):
            with self.assertRaises(ValueError):
                decode(bytes(count))

    def test_pinned_source_content(self):
        r = inspect(WORKER / 'tcg-source-identity-v1/source.git')
        self.assertTrue(r['source_objects_verified'])
        self.assertFalse(r['exact_build_provenance_complete'])
        self.assertFalse(r['binary_build_reproduced'])


if __name__ == '__main__':
    unittest.main()
