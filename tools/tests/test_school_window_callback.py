import unittest
from tools.school_window_callback import *


class SourceTests(unittest.TestCase):
    def test_original_imports_complete_callback_functions_and_global_factory_order(self):
        r=source_contract();self.assertEqual(len(r['imports']),5)
        self.assertTrue(r['global_dependency']['publication_after_window_creation'])
        self.assertFalse(r['global_dependency']['global_modified'] or r['global_dependency']['heap_resolved'])
        for a,b in RANGES.items():
            code=list(Cs(CS_ARCH_X86,CS_MODE_32).disasm(SOURCE.read_bytes()[a-BASE:b-BASE],a))
            self.assertEqual(code[-1].mnemonic,'ret');self.assertEqual(code[-1].address+code[-1].size,b)

    def test_callback_frame_is_declared_and_only_creation_lparam_is_translated(self):
        for msg in (36,129):
            p=dict(hwnd=123,message=msg,wParam=0,lParam=0x12345678);b,args=callback_stack(p)
            self.assertEqual(dword(b,TOP-STACK),RETURN);self.assertEqual(args[-1],SHADOW if msg==129 else p['lParam'])
            self.assertEqual(len(b),65536);self.assertEqual(callback_cpu()['EIP'],ENTRY)


if __name__=='__main__':unittest.main()
