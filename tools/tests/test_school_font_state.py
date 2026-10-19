import struct
import unittest
from tools.school_font_state import *


class SourceTests(unittest.TestCase):
    def test_original_GDI_ret4_and_all_state_argument_sources(self):
        c=source_contract();self.assertEqual(len(c['calls']),32);self.assertEqual(c['VB_args'],[8400,520,0,0]);self.assertEqual(len(c['imports']),3)
        self.assertEqual(c['states_stop'],'0x416101')

    def test_two_complete_exact_state_sequences(self):
        rows=plan(0x12345678);self.assertEqual(len(rows),60);self.assertEqual(rows[:30],rows[30:])
        self.assertEqual(rows[1],dict(method='texture',args=[0,0x12345678]));self.assertEqual(sum(r['method']=='render' for r in rows),28)
        self.assertEqual(sum(r['method']=='stage' for r in rows),26)

    def test_full_object_VB_and_tokens_preserve_glyphs_and_padding(self):
        before=bytes([0xCD])*1656;expected=bytearray(before)
        for at,value in ((96,0x12345678),(1648,11),(1652,12)):struct.pack_into('<I',expected,at,value)
        self.assertEqual(project(before,0x12345678,(11,12)),expected)

    def test_invalid_object_or_identity_refused(self):
        for f in (lambda:project(bytes(1655),1),lambda:project(bytes(1656),0),lambda:project(bytes(1656),1,(1,)),lambda:project(bytes(1656),1,(-1,2))):
            with self.assertRaises(ValueError):f()
