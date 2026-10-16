import struct,unittest
from copy import deepcopy
from tools.school_task_cycle import *

class SourceTests(unittest.TestCase):
    def seed(self):
        b=[dict(pointer=a,bytes=n,hex=bytes(n).hex()) for a,n in REGIONS];t=bytearray(400);t[0x43]=t[0x59]=1;t[0x44]=1;struct.pack_into('<I',t,0x48,1);b[0]['hex']=t.hex();k=bytearray(0x680);k[0x630]=255;b[1]['hex']=k.hex();return b

    def test_signed_reset_task_phases_and_full_retention_projection(self):
        b=self.seed();saved=deepcopy(b)
        for p in PHASES:
            a=project(p,b);after=a['after'];self.assertEqual(a['input_flag'],0 if p.startswith('reset') else 255);self.assertFalse(a['normal_VM_executed']);self.assertFalse(a['live_input_sampled']);self.assertEqual(after[4:],b[4:]);b=after
        self.assertEqual(a['task_phase'],2);self.assertIsNone(a['task_return']);self.assertEqual(saved,self.seed())

    def test_original_descriptor_signed_branches_and_vm_callsite(self):
        s=source_contract();self.assertEqual(s['import_identity']['symbol'],'ImmGetOpenStatus');self.assertTrue(s['platform_response']['declared_response']);self.assertFalse(s['platform_response']['live_OS_observed']);raw=SOURCE.read_bytes()
        for p in PHASES:
            for ret in call_protocol(p)[1:]:self.assertEqual(raw[ret-BASE-5],0xE8)
        self.assertEqual(call_protocol('vm_entry')[-1],0x454D90)

    def test_unsupported_context_flags_phase_effects_or_truncation_refused(self):
        b=self.seed()
        for index,offset in ((0,0x43),(0,0x44),(0,0x59),(1,8),(1,0x630),(1,0x528),(3,9),(3,0x18)):
            bad=deepcopy(b);raw=bytearray.fromhex(bad[index]['hex']);raw[offset]^=1;bad[index]['hex']=raw.hex()
            with self.assertRaises(ValueError):project('reset1',bad)
        with self.assertRaises(ValueError):project('reset1',b[:-1])
        with self.assertRaises(ValueError):project('unknown',b)

if __name__=='__main__':unittest.main()
