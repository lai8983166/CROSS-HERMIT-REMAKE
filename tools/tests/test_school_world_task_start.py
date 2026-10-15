import unittest
from copy import deepcopy
from tools.school_world_task_start import *

class TaskSourceTests(unittest.TestCase):
    def seed(self):
        inputs=dict(main_owner=MAIN,input_pointer=INPUT,strlen_slot=0x5922C4,strlen_target=0xE320050,text_pointer=INPUT+0x528,work_pointer=WORK,driver='declared_next_454CF0_after_original_world185')
        rows=[dict(pointer=a,bytes=n,hex=bytes(n).hex()) for a,n in TASK_REGIONS];task=bytearray(400);task[0x43]=1;task[0x59]=1;struct.pack_into('<I',task,0x48,1);rows[0]['hex']=task.hex();return inputs,rows

    def test_original_first_setup_source_and_full_buffers(self):
        x,b=self.seed();raw=bytearray.fromhex(b[1]['hex']);raw[0x428:0x528]=bytes([33])*256;raw[0x529:0x628]=bytes([44])*255;raw[0x63C:0x67C]=bytes([55])*64;raw[0x634:0x638]=bytes([66])*4;b[1]['hex']=raw.hex()
        a=project(x,b);after=bytes.fromhex(a['after'][1]['hex']);self.assertEqual(after[0x428:0x628],bytes(512));self.assertEqual(after[0x63C:0x67C],bytes(64));self.assertEqual(after[0x630],255);self.assertEqual(bytes.fromhex(a['after'][0]['hex'])[0x44],1)
        self.assertEqual((a['task_return'],a['strlen_result'],a['input_sampled'],a['VM_playback_executed']),(0,0,False,False))
        self.assertEqual(a['after'][3],b[3]);self.assertEqual(len(call_protocol()),14)

    def test_source_order_native_guards_and_import_identity(self):
        s=source_contract();self.assertEqual(len(s['functions']),10);self.assertEqual(s['platform_adapter']['name'],'lstrlenA');self.assertEqual(s['platform_adapter']['callee_pop_bytes'],4)
        raw=SOURCE.read_bytes()
        for ret in call_protocol()[1:]:self.assertEqual(raw[ret-BASE-5],0xE8)

    def test_active_text_or_effects_wrong_phase_or_input_owner_refused(self):
        x,b=self.seed()
        for index,offset in ((0,0x43),(0,0x44),(0,0x59),(1,0x528),(1,0x630),(3,9),(3,0x18)):
            bad=deepcopy(b);raw=bytearray.fromhex(bad[index]['hex']);raw[offset]^=1;bad[index]['hex']=raw.hex()
            with self.assertRaises(ValueError):project(x,bad)
        for key in ('main_owner','input_pointer','strlen_slot','text_pointer','work_pointer'):
            bad=dict(x);bad[key]+=4
            with self.assertRaises(ValueError):project(bad,b)
        with self.assertRaises(ValueError):project(x,b[:-1])

if __name__=='__main__':unittest.main()
