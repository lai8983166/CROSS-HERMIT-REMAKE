import struct,unittest
from copy import deepcopy
from tools.tests import test_school_vm_present as fixtures
from tools.school_vm_draw import *

class SourceTests(unittest.TestCase):
    def seed(self):
        x,b=fixtures.SourceTests().seed();t=next(r for r in b if r['pointer']==TACT);d=bytearray.fromhex(t['hex']);struct.pack_into('<I',d,0x60,WORK);t['hex']=d.hex()
        from tools.school_vm_present import project as parent
        b=parent('command',x,b)['after'];b=parent('packet',x,b)['after'];b=parent('draw',x,b)['after']
        return x,b+[dict(pointer=a,bytes=n,hex=bytes(n).hex()) for a,n in REGIONS[len(PARENT_REGIONS):]]

    def test_source_gate_and_three_return_projections(self):
        x,b=self.seed();old=deepcopy(b)
        for phase in PHASES:
            a=project(phase,x,b);self.assertEqual(a['CPU'],cpu_expected(phase));self.assertFalse(a['GPU_executed']);self.assertEqual(a['script_PC'],8);b=a['after']
        self.assertEqual(old[0],b[0]);self.assertEqual(a['task_return'],0);self.assertEqual(a['VM_return'],1);self.assertEqual(a['task_phase'],2)

    def test_source_original_call_bytes_and_finite_ABI(self):
        s=source_contract();self.assertEqual(s['maintenance']['native_calls'],51);self.assertEqual([len(call_protocol(p)) for p in PHASES],[9,51,3]);raw=SOURCE.read_bytes()
        for phase in PHASES:
            for va,ret,recv,args in call_protocol(phase):self.assertEqual(ret+struct.unpack_from('<i',raw,ret-BASE-4)[0],va);self.assertEqual(raw[ret-BASE-5],0xE8)
        r={int(x['va'],16):x for x in s['functions']};self.assertEqual(r[0x407710]['frame'],96);self.assertEqual(r[0x407AD0]['args'],2);self.assertEqual(r[0x4CD4D0]['args'],2)

    def test_active_render_menu_or_maintenance_refused(self):
        x,b=self.seed()
        for ptr,offset in ((TASK+0xB28E,0),(WORK+0x2434,0),(WORK+0x2490,9),(WORK+0x2490,0x18),(VM,0x6F62),(VM,0x6F64),(VM,0x6F82),(VM,0x6F90),(VM,0x9248),(VM,0x1CF),(VM,0x228)):
            bad=deepcopy(b);r=next(r for r in bad if r['pointer']==ptr);v=bytearray.fromhex(r['hex']);v[offset]=1;r['hex']=v.hex()
            with self.assertRaises(ValueError):project('cleanup',x,bad)
        with self.assertRaises(ValueError):project('cleanup',x,b[:-1])

    def test_full_cleanup_packet_and_SEH_projection(self):
        x,b=self.seed();a=project('cleanup',x,b);p=bytes.fromhex(a['packet']['hex']);self.assertEqual(len(p),128);self.assertEqual(int.from_bytes(p[0x4C:0x50],'little'),TASK);self.assertEqual(p[0x2C:0x34],bytes(8));self.assertEqual(next(r['hex'] for r in a['after'] if r['pointer']==0),'00000000');self.assertEqual(a['CPU']['EAX'],0xCCCCCCCC);self.assertEqual(a['draw_return'],1)

if __name__=='__main__':unittest.main()
