import struct
import unittest
from devtools.terminal_story_input import confirmation_key,StoryConfirm,ADV


class StoryWaitTests(unittest.TestCase):
    def row(self):
        vm=bytearray(128);vm[4]=1;struct.pack_into('<I',vm,16,0x20000);struct.pack_into('<I',vm,28,100)
        struct.pack_into('<HH',vm,32,1,51)
        return dict(tasks=[dict(vtable=ADV,pointer=0x10000,thread_id=9)],VM_hex=vm.hex(),
            frames=[dict(tid=9,chain=[dict(return_va=0x421F8A),dict(return_va=0x56E183)])])
    def test_current_original_adv_confirm_only(self):
        self.assertEqual(confirmation_key(self.row()),(0x10000,0x20000,100))
    def test_other_task_and_thread_refused(self):
        r=self.row();r['tasks'][0]['vtable']=0x59A430;self.assertIsNone(confirmation_key(r))
        r=self.row();r['frames'][0]['tid']=10;self.assertIsNone(confirmation_key(r))
    def test_other_wait_or_inactive_vm_refused(self):
        for at,value in ((4,0),(32,0),(34,52)):
            r=self.row();vm=bytearray.fromhex(r['VM_hex']);vm[at]=value;r['VM_hex']=vm.hex()
            self.assertIsNone(confirmation_key(r))
    def test_budget_and_duplicate_ambiguity_refused(self):
        for n in (0,193,True):
            with self.assertRaises(ValueError):StoryConfirm(n)
        x=StoryConfirm(1);r=self.row();x.key=confirmation_key(r);x.since=0;x.last_completed=x.key
        with self.assertRaises(ValueError):x.observe(None,None,r)
        self.assertEqual(x.actions,[])
    def test_exhausted_budget_seals_without_another_input(self):
        x=StoryConfirm(1);r=self.row();x.key=confirmation_key(r);x.since=0;x.actions=[{'prior':True}]
        x.observe(None,None,r)
        self.assertTrue(x.budget_exhausted);self.assertEqual(x.actions,[{'prior':True}])


if __name__=='__main__':unittest.main()
