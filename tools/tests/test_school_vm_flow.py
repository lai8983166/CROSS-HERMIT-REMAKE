import struct,unittest
from copy import deepcopy
from tools.tests import test_school_vm_draw as fixtures
from tools.school_vm_flow import *

class SourceTests(unittest.TestCase):
    def seed(self):
        old,b=fixtures.SourceTests().seed()
        from tools.school_vm_draw import project as parent
        for phase in ('cleanup','vm','task'):b=parent(phase,old,b)['after']
        for r in b:
            d=bytearray.fromhex(r['hex'])
            if r['pointer']==TACT:struct.pack_into('<I',d,0x48,1)
            elif r['pointer']==WORK:d[:]=b'\x01\x01\x01'
            elif r['pointer']==INPUT:d[0x630]=255
            r['hex']=d.hex()
        b.extend([dict(pointer=GLOBAL,bytes=160,hex=bytes(160).hex()),dict(pointer=SLOTS,bytes=12,hex='0000ffff0100ffff0200ffff')])
        x=dict(old,driver='explicit_original_reset_and_selected_task_calls_after_verified_return',ime_target=0x76182A80,strlen_target=0xE320050)
        return x,b

    def test_exact_source_dispatch_ABI_and_fade_integer(self):
        s=source_contract();self.assertEqual(len(s['commands']),9);self.assertEqual(s['fade']['step'],648);self.assertEqual(s['fade']['accumulator_after60'],38880);r={int(x['va'],16):x for x in s['functions']};self.assertEqual(r[0x56CD4A]['args'],1);self.assertEqual(r[0x56CEC0]['args'],3);self.assertEqual(r[0x56CFCC]['frame'],16);self.assertEqual(r[0x4E29E0]['args'],4)

    def test_actual_branch_full71_steps_and_delayed_release(self):
        x,b=self.seed();count=commands=0;ends=[];saved=deepcopy(b)
        for phase in PHASES:
            for kind in KINDS[phase]:
                a=project_step(kind,x,b);b=a['after'];count+=1;commands+=a['command'] is not None;self.assertEqual(a['task_phase'],2);self.assertFalse(a['GPU_executed'])
            ends.append((a['PC'],a['wait'],a['fade_remaining'],a['fade_accumulator']))
        self.assertEqual((count,commands),(71,9));self.assertEqual(ends[:5],[(44,0,0,0),(56,0,0,0),(88,0,0,0),(112,0,0,0),(176,0,0,0)]);self.assertEqual(ends[-2:],[(184,4,59,648),(184,0,0,38880)]);self.assertEqual(data(b)[SLOTS].hex(),'0000ffff0100010002000100');self.assertEqual(data(saved)[VM][0x3C],1)

    def test_nonzero_global_bits_and_word_preserve_other_bytes(self):
        x,b=self.seed()
        for kind in ('branch','assign'):b=project_step(kind,x,b)['after']
        r=next(r for r in b if r['pointer']==GLOBAL);r['hex']='ff'*160;a=project_step('bit',x,b);v=data(a['after'])[GLOBAL];self.assertEqual(v[0x78:0x7C],bytes.fromhex('ffffff7f'));self.assertEqual(v[:0x78],b'\xff'*0x78)
        a=project_step('word',x,a['after']);v=data(a['after'])[GLOBAL];self.assertEqual(v[0x28:0x2A],bytes(2));self.assertEqual(v[0x2A:0x78],b'\xff'*(0x78-0x2A))

    def test_original_call_bytes_all_kinds_and_cdecl_operands(self):
        x,b=self.seed();raw=SOURCE.read_bytes()
        self.assertEqual(raw[0x42626D-BASE:0x426271-BASE].hex(),'6a406a00')
        for at in (0x42612D,0x4261AD):self.assertEqual(raw[at-BASE:at-BASE+7].hex(),'68000100006a00')
        for at,offset in ((0x426274,0x63C),(0x426137,0x528),(0x4261B7,0x428)):
            self.assertEqual(raw[at-BASE],0x05);self.assertEqual(struct.unpack_from('<I',raw,at-BASE+1)[0],offset)
        self.assertEqual(raw[0x425C90-BASE:0x425C93-BASE].hex(),'8b4808')
        for phase in PHASES:
            for kind in KINDS[phase]:
                a=project_step(kind,x,b);calls=call_protocol(kind,x,b,a['fade_completed'])
                for va,ret,recv,args in calls:
                    if ret==RETURN:continue
                    self.assertEqual(raw[ret-BASE-5],0xE8);self.assertEqual(ret+struct.unpack_from('<i',raw,ret-BASE-4)[0],va)
                b=a['after']

    def test_invalid_input_render_phase_branch_or_incomplete_state_refused(self):
        x,b=self.seed()
        for ptr,offset in ((TASK+0xB28E,0),(WORK+0x2434,0),(TACT,0x44),(INPUT,0x630),(INPUT,8),(VM,0x3C),(VM,0x20),(VM,0x92E1),(VM,0x6F62)):
            bad=deepcopy(b);r=next(r for r in bad if r['pointer']==ptr);d=bytearray.fromhex(r['hex']);d[offset]^=1;r['hex']=d.hex()
            with self.assertRaises(ValueError):project_step('branch',x,bad)
        with self.assertRaises(ValueError):project_step('branch',x,b[:-1])
        bad=dict(x,driver='live_OS_frame')
        with self.assertRaises(ValueError):project_step('branch',bad,b)

if __name__=='__main__':unittest.main()
