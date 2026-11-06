"""Bounded pure ABI/dirty-input regressions; never starts a native helper."""
from pathlib import Path
import struct
import unittest

from devtools.terminal_wait_registration_probe import NODE, validate_thread_request


class ThreadRequestTests(unittest.TestCase):
    def setUp(self):
        self.ptd = 0x50001020
        self.args = [0, 0, 0x56E110, self.ptd, 4, NODE+0x24]
        self.raw = bytearray(116)
        for offset, value in ((4, 0xFFFFFFFF), (0x14, 1), (0x48, 0x421F50),
                              (0x4C, NODE), (0x50, 0x761D68)):
            struct.pack_into('<I', self.raw, offset, value)

    def test_original_suspended_thread_request(self):
        validate_thread_request(self.args, NODE, self.ptd, self.raw)

    def test_each_wrong_parameter_rejected(self):
        for index in range(6):
            with self.subTest(index=index):
                changed = self.args.copy()
                changed[index] ^= 1
                with self.assertRaises(ValueError):
                    validate_thread_request(changed, NODE, self.ptd, self.raw)

    def test_every_PTD_byte_is_checked(self):
        for index in range(116):
            with self.subTest(offset=index):
                changed = bytearray(self.raw)
                changed[index] ^= 1
                with self.assertRaises(ValueError):
                    validate_thread_request(self.args, NODE, self.ptd, changed)

    def test_incomplete_or_extended_PTD_rejected(self):
        for changed in (self.raw[:-1], self.raw+b'\x00'):
            with self.assertRaises(ValueError):
                validate_thread_request(self.args, NODE, self.ptd, changed)


class OriginalConstructorRegression(unittest.TestCase):
    def test_original_base_constructor_preserves_uninitialized_thread_fields(self):
        # Execute only the 41-instruction original base constructor in plain RAM.
        # No platform API, source corpus, or native resource is involved.
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
        from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_ESP, UC_X86_REG_EIP
        import hashlib
        original = Path(__file__).resolve().parents[2]/'analysis/hermit_game.exe'
        raw = original.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),
                         '588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005')
        uc = Uc(UC_ARCH_X86, UC_MODE_32)
        uc.mem_map(0x422000, 4096)
        uc.mem_write(0x422290, raw[0x22290:0x222D0])
        uc.mem_map(NODE, 4096)
        uc.mem_write(NODE, b'\xA5'*128)
        uc.mem_map(0x21000000, 4096)
        uc.mem_map(0x32000000, 4096)
        uc.mem_write(0x21000F00, struct.pack('<I', 0x32000000))
        uc.reg_write(UC_X86_REG_ECX, NODE)
        uc.reg_write(UC_X86_REG_ESP, 0x21000F00)
        uc.emu_start(0x422290, 0x32000000, timeout=1000000, count=100)
        self.assertEqual(uc.reg_read(UC_X86_REG_EIP), 0x32000000)
        self.assertEqual(bytes(uc.mem_read(NODE, 4)), struct.pack('<I', 0x594A54))
        self.assertEqual(bytes(uc.mem_read(NODE+0x20, 8)), b'\xA5'*8)
        self.assertEqual(bytes(uc.mem_read(NODE+0x28, 1)), b'\x00')
        self.assertEqual(uc.reg_read(UC_X86_REG_ESP), 0x21000F04)


if __name__ == '__main__':
    unittest.main()
