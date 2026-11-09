import copy
from pathlib import Path
import struct
import unittest
from devtools import terminal_wait_native_verification as v


def fixture():
    # Declared synthetic ABI observations, never a native acceptance source.
    node,manager,tid,pid,ptd=0x100000,0x110000,200,100,0x120000
    head=bytearray(64)
    for off,value in ((8,manager),(0x1C,44),(0x20,48),(0x24,tid)):
        struct.pack_into('<I',head,off,value)
    m=bytearray(0x120);struct.pack_into('<I',m,0x118,52)
    p=bytearray(116)
    for off,value in ((0,tid),(0x48,0x421F50),(0x4C,node)):struct.pack_into('<I',p,off,value)
    teb=0x200000;teb_head=bytearray(64)
    for off,value in ((4,0x400000),(8,0x200000),(0x18,teb),(0x20,pid),(0x24,tid)):struct.pack_into('<I',teb_head,off,value)
    tls=dict(thread_id=tid,owner_pid=pid,PTD=ptd,PTD_hex=p.hex(),FS=0x53,TEB=teb,
        selector_hex=struct.pack('<HHBBBB',0xFFF,0,0x20,0xF3,0x40,0).hex(),TEB_head_hex=teb_head.hex(),
        TLS_index=5,slot=teb+0xE10+20,TLS_slot_hex=struct.pack('<I',ptd).hex(),expansion_pointer=None)
    def event(handle):return dict(owner_pid=pid,remote_handle=handle,type_name='Event',duplicate_succeeded=True,query_status=0,wait_or_signal_called=False)
    owner=dict(node=node,thread_id=tid,head_hex=head[:48].hex(),TLS=tls,
               node_event=event(44),manager_event=event(52))
    relay=dict(child_pid=pid,parent_pid=99,child_tid=tid,error=None,scope_completed=True,hits=[],protocol=[],
        source_memory_written=False,general_registers_written=False,debugger_reply_substituted=False,
        accepted=False,full_instruction_trace=False,parent_api=dict(target=0x70001000),
        cleanup=dict(errors=[],parent_detached=True,child_debug_registers_restored=True))
    args={0x4223A8:(manager+0x100,),0x4223BE:(44,),0x4223D7:(52,),0x4223EF:(manager+0x100,),0x422407:(44,0xFFFFFFFF)}
    for i,ip in enumerate((*v.SITES,0x453CB5)):
        c=bytearray(716);s=bytearray(128);n=bytearray(head)
        sp=0x300000 if i==0 else 0x300008 if i==12 else 0x2FFF00
        eax=0 if ip==0x42240D else 1
        for before,after,slot,argc,success in v.CALLS:
            if ip==after:sp+=argc*4
        for off,value in ((20,1),(144,0x53),(156,10),(160,11),(164,12),(172,node),(176,eax),(180,0x301000),(184,ip),(196,sp)):
            struct.pack_into('<I',c,off,value)
        struct.pack_into('<I',s,0,0x453CB5)
        for j,a in enumerate(args.get(ip,())):struct.pack_into('<I',s,j*4,a)
        if i==9:struct.pack_into('<I',n,4,0x10000)
        d=dict(stack_pointer=sp,stack_hex=s.hex(),node_pointer=node,node_hex=n.hex(),manager_pointer=manager,
               manager_hex=m.hex(),PTD_pointer=ptd,PTD_hex=p.hex(),current_TLS=copy.deepcopy(tls))
        relay['hits'].append(dict(index=i,target=ip,elapsed=i/100,context_hex=c.hex(),data=d))
        pc=bytearray(716);struct.pack_into('<I',pc,184,0x70001000)
        relay['protocol'].append(dict(hit_index=i,parent_context_hex=pc.hex(),parent_stack_hex=struct.pack('<4I',1,2,3,0x10002).hex(),
            client_id_hex=struct.pack('<2I',pid,tid).hex(),original_continue_status=0x10002))
    raw=(Path(__file__).resolve().parents[2]/'analysis/hermit_game.exe').read_bytes()
    code=[dict(pointer=lo,hex=raw[lo-0x400000:hi-0x400000].hex())for lo,hi in
        ((0x422360,0x422434),(0x422560,0x4225DA),(0x56CE80,0x56CE98))]
    return dict(error=None,code=code,owner=owner,relay=relay,IAT=[dict(slot=c[2],target=0x70001000+i*32)for i,c in enumerate(v.CALLS)])


class WaitBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.raw=(Path(__file__).resolve().parents[2]/'analysis/hermit_game.exe').read_bytes()
    def test_scope_remains_bounded(self):
        result=v.verify(fixture(),self.raw)
        self.assertTrue(result['native_wait_callsite_sequence_verified'])
        for field in ('accepted','full_instruction_trace','full_state_replay','producer_module_provenance_verified','full_resource_lifetime_proved'):
            self.assertFalse(result[field])
    def test_unsuccessful_wait_or_event_rejected(self):
        for index,value in ((10,0xFFFFFFFF),(10,258),(4,0),(6,0)):
            p=fixture();c=bytearray.fromhex(p['relay']['hits'][index]['context_hex']);struct.pack_into('<I',c,176,value)
            p['relay']['hits'][index]['context_hex']=c.hex()
            with self.subTest(index=index,value=value),self.assertRaises(ValueError):v.verify(p,self.raw)
    def test_wrong_owner_argument_and_abi_rejected(self):
        for index,field,offset in ((0,'context_hex',172),(10,'context_hex',196),(12,'context_hex',156)):
            p=fixture();raw=bytearray.fromhex(p['relay']['hits'][index][field]);raw[offset]^=1;p['relay']['hits'][index][field]=raw.hex()
            with self.subTest(index=index),self.assertRaises(ValueError):v.verify(p,self.raw)
        p=fixture();d=p['relay']['hits'][9]['data'];s=bytearray.fromhex(d['stack_hex']);s[0]^=1;d['stack_hex']=s.hex()
        with self.assertRaisesRegex(ValueError,'arguments'):v.verify(p,self.raw)
    def test_missing_edge_wrong_reply_or_dirty_cleanup_rejected(self):
        p=fixture();p['relay']['hits'].pop(3)
        with self.assertRaises(ValueError):v.verify(p,self.raw)
        p=fixture();p['relay']['protocol'][2]['original_continue_status']=0x80010001
        with self.assertRaises(ValueError):v.verify(p,self.raw)
        p=fixture();p['relay']['cleanup']['parent_detached']=False
        with self.assertRaises(ValueError):v.verify(p,self.raw)
    def test_original_source_tamper_rejected(self):
        raw=bytearray(self.raw);raw[0x22407]^=1
        with self.assertRaisesRegex(ValueError,'original image'):v.verify(fixture(),raw)
    def test_live_code_and_current_TLS_slot_tamper_rejected(self):
        p=fixture();p['code'][0]['hex']='90'+p['code'][0]['hex'][2:]
        with self.assertRaisesRegex(ValueError,'live original'):v.verify(p,self.raw)
        p=fixture();p['relay']['hits'][4]['data']['current_TLS']['TLS_slot_hex']='00000000'
        with self.assertRaisesRegex(ValueError,'current TLS slot'):v.verify(p,self.raw)
        p=fixture();p['relay']['hits'][4]['data']['current_TLS']['FS']=0
        with self.assertRaisesRegex(ValueError,'current FS'):v.verify(p,self.raw)
    def test_actual_failure_cannot_pass_successful_wait_verification(self):
        import gzip,json
        from devtools.terminal_wait_observer_gate import FAILURE,ROOT
        report=json.loads(gzip.decompress((ROOT/FAILURE).read_bytes()))
        with self.assertRaisesRegex(ValueError,'successful bounded'):v.verify(report['probe'],self.raw)
        for record in report['probe']['relay']['instrumentation']:v.verify_debug_write(record)
        altered=copy.deepcopy(report['probe']['relay']['instrumentation'][0])
        raw=bytearray.fromhex(altered['after_context_hex']);raw[176]^=1;altered['after_context_hex']=raw.hex()
        with self.assertRaisesRegex(ValueError,'unchanged general'):v.verify_debug_write(altered)


if __name__=='__main__':unittest.main()
