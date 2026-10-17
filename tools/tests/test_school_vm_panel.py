import struct,unittest
from copy import deepcopy
from tools.tests import test_school_vm_flow as fixtures
from tools.school_vm_panel import *

class SourceTests(unittest.TestCase):
    def seed(self):
        x,b=fixtures.SourceTests().seed()
        from tools.school_vm_flow import PHASES as phases,KINDS as kinds,project_step as parent
        for phase in phases:
            for kind in kinds[phase]:b=parent(kind,x,b)['after']
        next(r for r in b if r['pointer']==VM)['hex']=self.mode_one(next(r for r in b if r['pointer']==VM)['hex'])
        return x,b

    def mode_one(self,hexstr):
        v=bytearray.fromhex(hexstr);v[0x9228]=1;v[0x1CC]=255;return v.hex()

    def test_original_source_dispatch_and_timer_rule(self):
        s=source_contract();self.assertEqual(len(s['functions']),71);self.assertEqual(s['timer']['polls'],31);self.assertEqual(s['timer']['final_count'],31)
        raw=SOURCE.read_bytes()
        for op,target in ((12,0x4CFFB9),(56,0x4D012A)):
            kind=raw[0x4D06AB-BASE+op-12];self.assertEqual(struct.unpack_from('<I',raw,0x4D066F-BASE+kind*4)[0],target)

    def test_full_display_mode_and31_poll_trace_to_original_entry(self):
        x,b=self.seed();ends=[];old=data(b)[VM][0x1CC];count=0
        for phase in PHASES:
            for kind in KINDS[phase]:a=project_step(kind,x,b);b=a['after'];count+=1
            ends.append((a['PC'],a['wait'],a['timer_count']))
        self.assertEqual(count,36);self.assertEqual(ends,[(192,1,0),(192,0,0),(200,0,0),(208,1,0),(208,0,31),(208,0,31)]);self.assertEqual(data(b)[VM][0x9228],0);self.assertEqual(data(b)[VM][0x1CC],old);self.assertEqual(a['pending']['args'],[0,x['script_pointer']+660,1]);self.assertFalse(a['pending']['first_instruction_executed']);self.assertIsNone(a['VM_return'])

    def test_timer30_still_waits_after30_polls(self):
        x,b=self.seed()
        for kind in ('display','release','text_mode','timer_start'):b=project_step(kind,x,b)['after']
        for i in range(31):
            a=project_step('timer_poll',x,b);b=a['after'];self.assertEqual(a['old_timer_count'],i);self.assertEqual(a['timer_count'],i+1);self.assertEqual(a['wait'],0 if i==30 else 1);self.assertEqual(data(b)[VM][0x1CD],0 if i==30 else 1)

    def test_original_call_bytes_full_timer_args_and_pending_stack(self):
        x,b=self.seed();raw=SOURCE.read_bytes()
        for phase in PHASES:
            for kind in KINDS[phase]:
                a=project_step(kind,x,b)
                for va,ret,recv,args in call_protocol(kind,x,b):
                    if ret==RETURN:continue
                    self.assertEqual(raw[ret-BASE-5],0xE8);self.assertEqual(ret+struct.unpack_from('<i',raw,ret-BASE-4)[0],va)
                if kind=='timer_start':self.assertEqual(call_protocol(kind,x,b)[19][3],[0,12,0,30,0])
                b=a['after']
        self.assertEqual(a['CPU']['ESP'],layout()['vm']-144)

    def test_invalid_input_render_phase_mode_or_timer_refused(self):
        x,b=self.seed()
        for ptr,offset in ((TASK+0xB28E,0),(INPUT,0x630),(VM,0x1C),(VM,0x3C),(VM,0x1CC),(VM,0x92E0),(VM,0x9248)):
            bad=deepcopy(b);r=next(r for r in bad if r['pointer']==ptr);v=bytearray.fromhex(r['hex']);v[offset]^=1;r['hex']=v.hex()
            with self.assertRaises(ValueError):project_step('display',x,bad)
        for kind in ('display','release','text_mode','timer_start'):b=project_step(kind,x,b)['after']
        r=next(r for r in b if r['pointer']==VM);v=bytearray.fromhex(r['hex']);struct.pack_into('<H',v,0x28,31);r['hex']=v.hex()
        with self.assertRaises(ValueError):project_step('timer_poll',x,b)

if __name__=='__main__':unittest.main()
