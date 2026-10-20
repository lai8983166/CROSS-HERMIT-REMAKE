import unittest
from tools.school_window_module import *


class SourceTests(unittest.TestCase):
    def test_deterministic_code_free_resource_module(self):
        raw=build_bytes();self.assertEqual(raw,RESOURCE_DLL.read_bytes())
        p=inspect_module(raw);self.assertEqual((p['entry_point'],p['executable_sections'],p['bytes']),(0,0,3072))
        self.assertEqual([r['id'] for r in p['resource_entries']],[5,157])

    def test_every_resource_byte_matches_original(self):
        pe=pefile.PE(data=build_bytes())
        for t in pe.DIRECTORY_ENTRY_RESOURCE.entries:
            for n in t.directory.entries:
                for lang in n.directory.entries:
                    d=lang.data.struct
                    self.assertEqual(pe.get_data(d.OffsetToData,d.Size),resource_bytes()[(t.id,n.id,lang.id)])

    def test_refuses_modified_module_or_resources(self):
        for at in (0x98+16,len(build_bytes())-1,0x200+160):
            b=bytearray(build_bytes());b[at]^=1
            with self.subTest(at=at),self.assertRaises(ValueError):inspect_module(bytes(b))

    def test_original_resource_calls_and_fresh_input_scope(self):
        s=source_contract();self.assertEqual(s['icon_id'],157)
        self.assertEqual(s['cursor_args'],[0,32512]);self.assertEqual(s['stock_brush_id'],4)
        self.assertEqual(s['stops']['class_ready'],'0x45047d')
        self.assertFalse(s['class_registration_executed'])


if __name__=='__main__':unittest.main()
