import struct
import unittest
from tools.school_font_finish import *


class SourceTests(unittest.TestCase):
    def test_original_second_state_and_full_loop_SEH_caller_source(self):
        c=source_contract();self.assertEqual(c['native_return'],'0x4134e3')
        self.assertEqual(c['loop_index_after'],2);self.assertEqual(c['captured_prior_SEH'],0)
        self.assertEqual(len(c['exit_trace']),23);self.assertEqual(c['VB_args'],[8400,520,0,0])

    def test_second_two_exact30_call_blocks(self):
        rows=plan(0x12345678);self.assertEqual(len(rows),60);self.assertEqual(rows[:30],rows[30:])
        self.assertEqual(rows[1],dict(method='texture',args=[0,0x12345678]))

    def test_full_second_object_projection_preserves_UVs_and_padding(self):
        before=bytes([0xCD])*1656;expected=bytearray(before)
        for at,value in ((96,0x12345678),(1648,3),(1652,4)):struct.pack_into('<I',expected,at,value)
        self.assertEqual(project(before,0x12345678,(3,4)),expected)

    def test_invalid_full_object_or_resources_refused(self):
        for f in (lambda:project(bytes(1655),1),lambda:project(bytes(1656),0),lambda:project(bytes(1656),1,(1,)),lambda:project(bytes(1656),1,(-1,2))):
            with self.assertRaises(ValueError):f()
