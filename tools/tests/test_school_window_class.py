import struct
import unittest
from tools.school_window_class import *


class SourceTests(unittest.TestCase):
    def test_original_contract_matches_immutable_source_and_declares_dependency_scope(self):
        r=source_contract();self.assertEqual(r['instructions'],validate_source(SOURCE.read_bytes()))
        self.assertEqual(r['registration']['callback'],'0x424980')
        self.assertEqual(r['callback_dependency']['first_virtual'],'0x450d30')
        self.assertFalse(r['callback_dependency']['executed'] or r['window_created'] or r['retained_VM_advanced'])

    def test_refuses_corrupted_registration_callback_property_or_vtable(self):
        for at in (ENTRY,0x4249F6,0x594AB4,0x5986A0):
            b=bytearray(SOURCE.read_bytes());b[at-BASE]^=1
            with self.subTest(at=hex(at)),self.assertRaises(ValueError):validate_source(b)

    def test_class_and_creation_parameters_keep_guest_callback_and_actual_input(self):
        b=class_bytes(0x1230000,[11,12],13,14)
        self.assertEqual(struct.unpack('<12I',b),(48,0,CALLBACK,0,0,0x1230000,11,13,14,0,window.TITLE,12))
        self.assertEqual(creation_args(0x1230000),[0,window.TITLE,window.TITLE,0x90000000,16,16,1024,768,0,0,0x1230000,parent.OWNER])


if __name__=='__main__':unittest.main()
