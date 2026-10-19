import unittest
from tools.school_main_window import *


class SourceTests(unittest.TestCase):
    def test_original_functions_import_and_both_source_branches(self):
        s=source_contract()
        self.assertEqual(s['import_identity']['symbol'],'FindWindowA')
        self.assertEqual(s['task_slots'],dict(offset=100,count=32,stride=8,zero_bytes=256))
        self.assertEqual(s['no_duplicate_pending']['args'],[0,0,1024,768,0x90000000,1])
        self.assertFalse(s['instance_is_live_module'])
        self.assertFalse(s['query_result_fabricated'])

    def test_exact_task_zeroing_preserves_adjacent_critical_section(self):
        before=bytes([0xCD])*parent.BACKING
        for duplicate in (False,True):
            after=project_owner(before,'tasks',duplicate)
            self.assertEqual(after[:0x64],before[:0x64])
            self.assertEqual(after[0x64:0x164],bytes(256))
            self.assertEqual(after[0x164:],before[0x164:])

    def test_branch_projection_preserves_unexecuted_exit_and_sets_window_parameters(self):
        before=bytes([0xCD])*parent.BACKING
        duplicate=project_owner(before,'branch',True);normal=project_owner(before,'branch',False)
        self.assertEqual(duplicate[0x5C:0x64],b'\xcd'*8)
        self.assertEqual(dword(normal,0x5C),105);self.assertEqual(dword(normal,0x60),103)
        self.assertEqual(dword(normal,0x1108),0)
        self.assertEqual(duplicate[0x164:],before[0x164:])


if __name__=='__main__':unittest.main()
