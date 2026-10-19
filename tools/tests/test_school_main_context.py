import unittest
from tools.school_main_context import *


class SourceTests(unittest.TestCase):
    def test_original_source_and_imports(self):
        s=source_contract()
        self.assertEqual(s['allocation_bytes'],4368)
        self.assertEqual(len(s['imports']),6)
        self.assertEqual(next(r['dll'] for r in s['imports'] if r['symbol']=='PathAddBackslashA'),'SHLWAPI.dll')
        self.assertEqual(s['stops']['publication'],'0x49de15')

    def test_zero_length_memset_is_not_a_directory_clear(self):
        s=source_contract()
        self.assertEqual(s['directory_memset_args'],[DIRECTORY,525,0])
        self.assertEqual(s['directory_memset_clears_bytes'],0)
        self.assertGreater(functions()[0x56CEC0],0x56CF13)

    def test_explicit_mid_frame_and_retained_boundary(self):
        s=source_contract()
        self.assertTrue(s['declared_mid_WinMain_frame'])
        self.assertFalse(s['WinMain_prelude_executed'])
        self.assertEqual(len(s['inherited_missing_heaps']),2)
        self.assertEqual(SP,BP-0xA8)
        for fill in (0xA5,0xCC):
            raw=initial_owner(fill)
            self.assertEqual(raw[:SIZE],b'\xcd'*SIZE)
            self.assertEqual(raw[SIZE:],bytes([fill])*(BACKING-SIZE))
        with self.assertRaises(ValueError):initial_owner(0)


if __name__=='__main__':unittest.main()
