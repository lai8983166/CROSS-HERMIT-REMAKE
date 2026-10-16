import struct,unittest
from copy import deepcopy
from tools.school_vm_present import *

class SourceTests(unittest.TestCase):
    def seed(self):
        b=[dict(pointer=a,bytes=n,hex=bytes(n).hex()) for a,n in REGIONS];d={r['pointer']:bytearray.fromhex(r['hex']) for r in b};p=0xE741BD0;t=d[TACT];t[0x43]=1;t[0x44]=2;t[0x59]=1;struct.pack_into('<I',t,0x64,p);v=d[VM];v[4:6]=b'\x01\x01';struct.pack_into('<I',v,0x10,p+452);d[WORK][0]=1;struct.pack_into('<II',d[BANK],0,0xE741B74,1)
        for r in b:r['hex']=d[r['pointer']].hex()
        return dict(script_pointer=p,script_sha256=SCRIPT_SHA,driver='continuous_original_task_VM',texture_record=dict(pointer=0xE741B74,bytes=84,hex=bytes(84).hex())),b

    def test_source_opcode_and_complete_byte_projection(self):
        x,b=self.seed();saved=deepcopy(b);a=project('command',x,b);v=bytes.fromhex(next(r['hex'] for r in a['after'] if r['pointer']==VM));self.assertEqual(struct.unpack_from('<IHHH',v,0x1C),(8,0,167,8));self.assertEqual(struct.unpack_from('<I',v,0x3C)[0],1);self.assertEqual(b,saved);self.assertEqual(a['pending']['args'][:4],[20,0,1,51]);self.assertFalse(a['VM_returned'])

    def test_full_native_packet_padding_SEH_and_bound_resource(self):
        x,b=self.seed();a=project('command',x,b);a=project('packet',x,a['after']);p=bytes.fromhex(a['packet']['hex']);self.assertEqual(len(p),128);self.assertEqual(p[0x46:0x48],b'\xcc\xcc');self.assertEqual(p[0x5A:0x5C],b'\xcc\xcc');self.assertEqual(struct.unpack_from('<I',p,0x4C)[0],TASK);self.assertEqual(struct.unpack_from('<H',p,0x58)[0],0x40)
        z=project('draw',x,a['after']);self.assertEqual(z['resource_lookup_return'],x['texture_record']['pointer']);self.assertEqual(z['pending']['va'],'0x407ad0');self.assertFalse(z['assertion_executed']);self.assertEqual(z['packet']['hex'],packet_project(0xC0,x['texture_record']));self.assertEqual(bytes.fromhex(next(r['hex'] for r in z['after'] if r['pointer']==0)),struct.pack('<I',layout()['seh']))

    def test_original_dispatch_source_ABI_and_exact_calls(self):
        s=source_contract();self.assertEqual(len(s['functions']),18);self.assertEqual(s['resource_request'],dict(group=20,index=0,layer=51,captured_count=1));r=SOURCE.read_bytes();self.assertEqual(layout()['packet'],BASE_SP-572)
        for phase in PHASES:
            for ret in call_protocol(phase):self.assertEqual(r[ret-BASE-5],0xE8)
        frames={int(x['va'],16):x['frame'] for x in s['functions']};self.assertEqual((frames[0x4D2CA0],frames[0x4075E0]),(224,96))

    def test_wrong_script_vm_phase_SEH_or_resource_count_refused(self):
        x,b=self.seed()
        for pointer,offset in ((VM,4),(VM,0x10),(VM,0x1C),(VM,0x20),(VM,0x92E1),(TACT,0x44),(BANK,4),(0,0)):
            bad=deepcopy(b);r=next(r for r in bad if r['pointer']==pointer);v=bytearray.fromhex(r['hex']);v[offset]^=1;r['hex']=v.hex()
            with self.assertRaises(ValueError):project('command',x,bad)
        bad=dict(x);bad['driver']='synthetic'
        with self.assertRaises(ValueError):project('command',bad,b)
        with self.assertRaises(ValueError):project('command',x,b[:-1])

if __name__=='__main__':unittest.main()
