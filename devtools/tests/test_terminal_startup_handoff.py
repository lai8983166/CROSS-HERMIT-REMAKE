import struct
import unittest
from types import SimpleNamespace
from devtools import terminal_startup_handoff as probe


class GraphTests(unittest.TestCase):
    def fixture(self):
        main=0x10000;node=0x20000;manager=bytearray(0x120);head=bytearray(48)
        struct.pack_into('<I',manager,0,node)
        for at,value in ((0,probe.STARTUP),(8,main+0x64)):
            struct.pack_into('<I',head,at,value)
        data={main+0x64:manager,node:head}
        return SimpleNamespace(main=main,get=lambda p,n:bytes(data[p][:n])),data

    def test_classify_original_single_owner(self):
        c,data=self.fixture();manager,rows=probe.graph(c)
        self.assertEqual(len(probe.classify(rows)['startup']),1)
        self.assertEqual(probe.classify(rows)['menu'],[])

    def test_cycle_and_wrong_manager_refused(self):
        for at,value in ((12,0x20000),(8,0x10000)):
            c,data=self.fixture();struct.pack_into('<I',data[0x20000],at,value)
            with self.subTest(at=at),self.assertRaises(ValueError):probe.graph(c)

    def test_no_tail_pointer_assumption(self):
        c,data=self.fixture();struct.pack_into('<I',data[c.main+0x64],4,0xAABBCCDD)
        _,rows=probe.graph(c)
        self.assertEqual(len(rows),1)


if __name__=='__main__':unittest.main()
