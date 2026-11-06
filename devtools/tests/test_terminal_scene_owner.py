"""Reject cross-lifetime identities and unauthorized native roots before launch."""
import struct
import unittest
from types import SimpleNamespace
from devtools import terminal_scene_owner as owner


class OwnershipTests(unittest.TestCase):
    def test_selector(self):
        self.assertEqual(owner.parse_selector(bytes.fromhex('0000785634000012')),0x12345678)
        with self.assertRaises(ValueError):
            owner.parse_selector(bytes(7))

    def fixture(self):
        head,ptd = bytearray(64),bytearray(116)
        for offset,value in ((4,0x20000),(8,0x10000),(0x18,0x30000),(0x20,12),(0x24,34)):
            struct.pack_into('<I',head,offset,value)
        for offset,value in ((0,34),(0x48,0x421F50),(0x4C,0x40000)):
            struct.pack_into('<I',ptd,offset,value)
        return [0x30000,head,7,0x50000,ptd,12,34,0x40000]

    def test_current_tls(self):
        owner.validate_tls(*self.fixture())

    def test_cross_owner_and_missing_tls_rejected(self):
        for argument,replacement in ((0,1),(2,1088),(3,0),(5,13),(6,35),(7,1),(4,bytes(115))):
            values = self.fixture()
            values[argument] = replacement
            with self.subTest(argument=argument),self.assertRaises(ValueError):
                owner.validate_tls(*values)
        for offset in (0,0x48,0x4C):
            values = self.fixture()
            struct.pack_into('<I',values[4],offset,0)
            with self.subTest(ptd_offset=offset),self.assertRaises(ValueError):
                owner.validate_tls(*values)

    def test_only_three_original_roots_in_order(self):
        c = owner.Calls.__new__(owner.Calls)
        c.pid,c.main,c.owned = 12,0x70000,SimpleNamespace(members=lambda:[12])
        c.scene_construction_authorized=True
        protocol = ((0x4E1B60,0,()),(0x4DA860,0,(4,)),(0x439E30,0x70010,(16,)))
        for c.phase,expected in enumerate(protocol):
            c.validate(*expected)
            for other in protocol:
                if other != expected:
                    with self.assertRaises(ValueError):
                        c.validate(*other)
        c.phase=1
        with self.assertRaises(ValueError):
            c.validate(0x4DA860,0,(76,))
        c.owned=SimpleNamespace(members=lambda:[13])
        with self.assertRaises(ValueError):
            c.validate(*protocol[1])

    def test_no_root_without_handoff_preflight(self):
        c=owner.Calls.__new__(owner.Calls)
        c.pid,c.main,c.phase=12,0x70000,0
        c.owned=SimpleNamespace(members=lambda:[12])
        c.scene_construction_authorized=False
        with self.assertRaisesRegex(ValueError,'empty original scheduler'):
            c.validate(0x4E1B60,0,())


if __name__ == '__main__':
    unittest.main()
