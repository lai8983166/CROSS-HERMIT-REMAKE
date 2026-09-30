"""Guard the independent UnitCtrl exit path against a false 112→exit inference."""
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
IMAGE_BASE = 0x400000


class BattleParallelExitEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.exe = (ROOT / 'analysis/hermit_game.exe').read_bytes()

    @classmethod
    def at(cls, va, size):
        offset = va - IMAGE_BASE
        return cls.exe[offset:offset + size]

    def assert_call(self, va, target):
        data = self.at(va, 5)
        self.assertEqual(data[0], 0xe8)
        self.assertEqual(va + 5 + struct.unpack_from('<i', data, 1)[0], target)

    def test_parallel_controller_is_called_during_tactics_loop(self):
        self.assert_call(0x451a11, 0x452fc0)
        self.assert_call(0x4539ec, 0x454cf0)
        self.assert_call(0x453a0c, 0x46b470)
        self.assert_call(0x4530a2, 0x499c90)
        self.assert_call(0x4530e5, 0x499c90)
        self.assertEqual(self.at(0x499d04, 4), bytes.fromhex('c6420a01'))
        self.assertEqual(self.at(0x46b4b5, 11), bytes.fromhex(
            '0fbe82488b100085c07408'))
        self.assert_call(0x46b4c3, 0x499da0)

    def test_phase_six_does_not_set_tactics_exit_flag(self):
        # 4549D0 writes argument [ebp+14h] to TacticsTask+4Ch.
        self.assertEqual(self.at(0x454a7a, 3), bytes.fromhex('89424c'))
        for call_va, fourth_push_va in [
            (0x49a0ef, 0x49a0de),
            (0x49a10d, 0x49a0fc),
            (0x49a141, 0x49a130),
        ]:
            with self.subTest(call=hex(call_va)):
                self.assert_call(call_va, 0x4549d0)
                self.assertEqual(self.at(fourth_push_va, 2), bytes.fromhex('6a00'))


if __name__ == '__main__':
    unittest.main()
