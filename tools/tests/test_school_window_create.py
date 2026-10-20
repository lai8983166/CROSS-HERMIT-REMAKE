import unittest
from tools.school_window_create import *


class SourceTests(unittest.TestCase):
    def test_original_bound_branch_and_message1_zero_return_are_source_pinned(self):
        r=source_contract();self.assertEqual(r['admitted_messages'],[129,131,1])
        self.assertEqual(r['create_contract']['source_switch_target'],'0x450ed3')
        self.assertFalse(r['create_contract']['default_procedure_called'] or r['captured_game_global_modified'])

    def test_rect_input_output_requires_exact_observed_form_and_positive_extent(self):
        self.assertEqual(rectangle(struct.pack('<4i',16,16,1040,784),0),[16,16,1040,784])
        for b,w in ((bytes(16),1),(bytes(52),1),(bytes(15),0),(struct.pack('<4i',5,5,1,1),0)):
            with self.subTest(w=w,bytes=len(b)),self.assertRaises(ValueError):rectangle(b,w)


if __name__=='__main__':unittest.main()
