"""Synthetic tamper regressions; no native process, UI, GPU or old case sources."""
import copy
import gzip
import json
from pathlib import Path
import struct
import tempfile
import unittest

from devtools import terminal_scene_owner_verification as v


def put(data, offset, value):
    struct.pack_into('<I',data,offset,value)


def change_hex(row, field, offset, value):
    data=bytearray.fromhex(row[field]);put(data,offset,value);row[field]=data.hex()


class OwnerVerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw=(v.ROOT/'analysis/hermit_game.exe').read_bytes()
        before=bytes(80);selected,_=v.scenario_replay(cls.raw,before)
        pid,tid,main,node=1111,2222,0x1000000,0x1100000
        head=bytearray(512)
        for at,value in ((0,0x59A430),(4,1),(8,main+0x64),(0x1C,0x84),(0x20,0x80),(0x24,tid)):
            put(head,at,value)
        head[0x28]=1
        body=head+bytearray(0x1194F0-len(head))
        manager=bytearray(0x120);put(manager,0,node);put(manager,0x118,0x88)
        context=bytearray(716)
        for at,value in ((0,0x1003F),(144,0x53),(180,0x20F000),(184,0x77000000),(196,0x20EF00)):
            put(context,at,value)
        frame=dict(tid=tid,context_hex=context.hex(),EBP=0x20F000,EIP=0x77000000,ESP=0x20EF00,
            chain=[dict(bp=0x20F000,saved_bp=0x20F100,return_va=0x453CB5),
                   dict(bp=0x20F100,saved_bp=0x20F200,return_va=0x421F8A),
                   dict(bp=0x20F200,saved_bp=0x20F300,return_va=0x56E183),
                   dict(bp=0x20F300,saved_bp=0x20F400,return_va=0x77112233)])
        teb=bytearray(0x40)
        for at,value in ((4,0x210000),(8,0x200000),(0x18,0x7FFDE000),(0x20,pid),(0x24,tid)):
            put(teb,at,value)
        ptd=bytearray(116)
        for at,value in ((0,tid),(0x48,0x421F50),(0x4C,node)):
            put(ptd,at,value)
        tls=dict(owner_pid=pid,thread_id=tid,FS=0x53,selector_hex='ffff00e0fdf3cf7f',
            TEB=0x7FFDE000,TEB_head_hex=teb.hex(),TLS_index=3,expansion_pointer=None,
            slot=0x7FFDE000+0xE10+12,TLS_slot_hex=struct.pack('<I',0x40001000).hex(),PTD=0x40001000,PTD_hex=ptd.hex(),
            ancestry=dict(worker_argument=node,wrapper_argument=0x40001000,callback_this=node,
                          callback_argument=0,node_argument=0))
        tls['ancestry_memory']={k:dict(pointer=a,hex=struct.pack('<I',tls['ancestry'][k]).hex())
            for k,a in dict(worker_argument=0x20F208,wrapper_argument=0x20F308,
                           callback_this=0x20F0FC,callback_argument=0x20F108,node_argument=node+0x18).items()}
        sample=dict(index=0,elapsed=1,scene_global=node,frames=[frame],MAIN_event_hex=bytes(8).hex(),
            manager_hex=manager.hex(),scenario_hex=selected.hex(),VM_hex=bytes(128).hex(),
            game_exit_flag_hex=bytes(4).hex(),registered_tasks=[dict(pointer=node,bucket=0,head_hex=head[:48].hex())],
            successor_global=0,scene_registered=True,worker_exited=False,scene_head_hex=head.hex(),
            controller_task_backpointer=node,TLS=tls,worker_stack_pointer=frame['ESP'],worker_stack_hex=bytes(128).hex(),
            input=dict(game=0x1200000,keyboard_edges_hex=bytes(256).hex(),mouse_pointer=0x120196C,mouse_hex=bytes(0x58).hex()))
        def event(handle):
            return dict(remote_handle=handle,owner_pid=pid,duplicate_succeeded=True,query_status=0,
                        type_name='Event',wait_or_signal_called=False)
        source=dict(code=v.source_rows(cls.raw),IAT=[dict(slot=s,hex=struct.pack('<I',0x77000000+i*16).hex()) for i,s in enumerate(v.IAT)])
        import pefile
        dll=Path('C:/Windows/SysWOW64/kernelbase.dll');osraw=dll.read_bytes();pe=pefile.PE(data=osraw)
        exp=next(x for x in pe.DIRECTORY_ENTRY_EXPORT.symbols if x.name==b'TlsGetValue')
        base=0x75000000;code=pe.get_data(exp.address,64)
        from capstone import Cs,CS_ARCH_X86,CS_MODE_32
        impl=dict(module='kernelbase.dll',symbol='TlsGetValue',base=base,module_path=str(dll),
            module_sha256=v.sha(osraw),RVA=exp.address,target=base+exp.address,code_hex=code.hex(),
            instructions=[[i.mnemonic,i.op_str] for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(code,base+exp.address)],
            fixed_slots_offset=0xE10,expansion_pointer_offset=0xF94)
        calls=[];data,std,cdecl=0x30000000,0x30200000,0x30210000
        writes=[dict(pointer=std,bytes=len(v.THUNK),sha256=v.sha(v.THUNK)),dict(pointer=cdecl,bytes=len(v.CDECL),sha256=v.sha(v.CDECL))]
        for i,(va,receiver,args) in enumerate(((0x4E1B60,0,[]),(0x4DA860,0,[4]),(0x439E30,main+0x10,[16]))):
            b=struct.pack('<11I',va,receiver,len(args),*(args+[0]*(3-len(args))),0,0xCCCCCCCC,0xCCCCCCCC,0xCCCCCCCC,0)
            a=bytearray(b)
            for at,value in ((28,0),(32,0x22F000),(36,0x22F000),(40,0x4C4C4143)): put(a,at,value)
            calls.append(dict(va=va,receiver=receiver,args=args,slot=0,sequence=i,thread_id=3000+i,
                parameter_before_hex=b.hex(),parameter_after_hex=a.hex(),eax=0,wait_status=0,exit_code=0))
            writes.append(dict(pointer=data,bytes=44,sha256=v.sha(b)))
        probe=dict(scenario=4,pid=pid,main=main,error=None,source_before=source,source_after=copy.deepcopy(source),
            original_scene_constructor_and_factory=True,source_code_IAT_or_general_registers_written=False,
            old_terminal_fixture_loaded=False,full_instruction_trace=False,wait_API_return_status_sampled=False,
            full_battle_exit_accepted=False,native_retreat_observed=False,TLS_implementation=impl,calls=calls,
            host_private_writes=writes,private_frees=[dict(pointer=a,bytes=n,released=True) for a,n in ((cdecl,4096),(std,4096),(data,0x200000))],
            scenario_before_hex=before.hex(),scenario_selected_hex=selected.hex(),
            window=dict(hwnd=123,pid=pid,main_tid=1112),worker=dict(node=node,thread_id=tid,remote_handle=0x80,
                manager_event=event(0x88),node_event=event(0x84)),
            derived_object_initial=dict(pointer=node,bytes=len(body),hex=body.hex()),samples=[sample])
        cls.template=dict(schema_version=1,accepted=False,kind='actual_same_owner_scene_and_retreat_observation',
            old_terminal_cases_replayed=False,full_native_instruction_or_API_trace=False,independent_full_replay=False,
            R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False,probe=probe,
            lifecycle=dict(error=None,ready=dict(pid=pid,main=dict(pointer=main),window=dict(pid=pid,tid=1112,hwnd=123)),
                lifetime=dict(members_after_cleanup=[],membership=[dict(pids=[pid])],forced_termination=False)),
            mutable_private_runtime_files=[dict(restored_exact=True)])

    def setUp(self):
        self.report=copy.deepcopy(self.template)
        self.probe=self.report['probe'];self.sample=self.probe['samples'][0]

    def verify(self):
        return v.verify_report(self.report,self.raw)

    def rejects(self):
        with self.assertRaises(ValueError): self.verify()

    def test_partial_keeps_stronger_claims_false(self):
        r=self.verify()
        self.assertEqual(r['status'],'partial')
        for k in ('accepted','full_battle_exit_accepted','wait_API_success_proved','normal_PTD_cleanup_proved','independent_full_replay'):
            self.assertIs(r[k],False)

    def test_source_authentication(self):
        changed=bytearray(self.raw);changed[0x11670]^=1
        with self.assertRaisesRegex(ValueError,'source identity'): v.verify_report(self.report,bytes(changed))

    def test_source_range_omission(self):
        self.probe['source_before']['code'].pop();self.probe['source_after']=copy.deepcopy(self.probe['source_before']);self.rejects()

    def test_iat_after_change(self):
        self.probe['source_after']['IAT'][0]['hex']='12345678';self.rejects()

    def test_missing_final_source_identity(self):
        del self.probe['source_after'];self.rejects()

    def test_scenario_output_tamper(self):
        change_hex(self.probe,'scenario_selected_hex',0,77);self.rejects()

    def test_extra_business_call(self):
        self.probe['calls'][2]['va']=0x453D00;self.rejects()

    def test_cdecl_esp_mismatch(self):
        change_hex(self.probe['calls'][1],'parameter_after_hex',36,0x22EFFC);self.rejects()

    def test_host_write_outside_bridge(self):
        self.probe['host_private_writes'].append(dict(pointer=0x7A4174,bytes=4,sha256=v.sha(bytes(4))));self.rejects()

    def test_private_allocation_overlap(self):
        self.probe['private_frees'][0]['pointer']=self.probe['private_frees'][1]['pointer'];self.rejects()

    def test_private_cleanup_failure(self):
        self.probe['private_frees'][0]['released']=False;self.rejects()

    def test_bridge_coherently_relocated_over_original_scene(self):
        old=self.probe['private_frees'][-1]['pointer'];new=self.probe['worker']['node']
        self.probe['private_frees'][-1]['pointer']=new
        for write in self.probe['host_private_writes']:
            if write['pointer']==old:write['pointer']=new
        self.rejects()

    def test_foreign_main_thread(self):
        self.probe['window']['main_tid']+=1;self.rejects()

    def test_foreign_event_owner(self):
        self.probe['worker']['node_event']['owner_pid']+=1;self.rejects()

    def test_consuming_event_query(self):
        self.probe['worker']['manager_event']['wait_or_signal_called']=True;self.rejects()

    def test_wrong_event_type(self):
        self.probe['worker']['node_event']['type_name']='Thread';self.rejects()

    def test_incomplete_context(self):
        self.sample['frames'][0]['context_hex']=self.sample['frames'][0]['context_hex'][:-2];self.rejects()

    def test_context_scalar_tamper(self):
        self.sample['frames'][0]['ESP']+=4;self.rejects()

    def test_broken_stack_chain(self):
        self.sample['frames'][0]['chain'][0]['saved_bp']+=4;self.rejects()

    def test_foreign_ptd_worker(self):
        change_hex(self.sample['TLS'],'PTD_hex',0,3333);self.rejects()

    def test_foreign_ptd_node(self):
        change_hex(self.sample['TLS'],'PTD_hex',0x4C,0x1101000);self.rejects()

    def test_incomplete_ptd(self):
        self.sample['TLS']['PTD_hex']=self.sample['TLS']['PTD_hex'][:-2];self.rejects()

    def test_wrong_teb_self(self):
        change_hex(self.sample['TLS'],'TEB_head_hex',0x18,0x7FFDF000);self.rejects()

    def test_wrong_selector_base(self):
        self.sample['TLS']['selector_hex']='ffff00e0fcf3cf7f';self.rejects()

    def test_wrong_tls_slot(self):
        self.sample['TLS']['slot']+=4;self.rejects()

    def test_raw_tls_pointer_tamper(self):
        self.sample['TLS']['TLS_slot_hex']='00000000';self.rejects()

    def test_raw_ancestor_address_tamper(self):
        self.sample['TLS']['ancestry_memory']['wrapper_argument']['pointer']+=4;self.rejects()

    def test_raw_ancestor_value_tamper(self):
        self.sample['TLS']['ancestry_memory']['callback_this']['hex']='00000000';self.rejects()

    def test_missing_raw_ancestor(self):
        del self.sample['TLS']['ancestry_memory']['worker_argument'];self.rejects()

    def test_wrapper_parameter_not_ptd(self):
        self.sample['TLS']['ancestry']['wrapper_argument']+=4;self.rejects()

    def test_wrong_callback_this(self):
        self.sample['TLS']['ancestry']['callback_this']+=4;self.rejects()

    def test_missing_original_crt_frame(self):
        self.sample['frames'][0]['chain'][2]['return_va']=0x56E184;self.rejects()

    def test_graph_cycle(self):
        change_hex(self.sample['registered_tasks'][0],'head_hex',12,self.probe['worker']['node']);self.rejects()

    def test_hidden_untraversed_node(self):
        r=copy.deepcopy(self.sample['registered_tasks'][0]);r['pointer']+=0x1000
        self.sample['registered_tasks'].append(r);self.rejects()

    def test_stale_global_cannot_supply_tls(self):
        self.sample['scene_registered']=False;self.rejects()

    def test_mouse_missing_confirmation_bit(self):
        self.sample['input']['mouse_hex']=bytes(16).hex();self.rejects()

    def test_full_acceptance_inflation(self):
        self.report['accepted']=True;self.rejects()

    def test_wait_success_inflation(self):
        self.probe['wait_API_return_status_sampled']=True;self.rejects()

    def test_retreat_claim_without_endpoints(self):
        self.probe['native_retreat_observed']=True;self.rejects()

    def test_retreat_observed_remains_not_full_acceptance(self):
        head=bytearray.fromhex(self.sample['scene_head_hex']);head[0x31]=1;self.sample['scene_head_hex']=head.hex()
        self.sample['frames'][0]['chain'][0]['return_va']=0x451758
        terminal=copy.deepcopy(self.sample);terminal['index']=1;terminal['elapsed']=2
        terminal['frames']=[];terminal['worker_exited']=True;terminal['scene_registered']=False
        for key in ('TLS','scene_head_hex','input','worker_stack_pointer','worker_stack_hex','controller_task_backpointer'):
            terminal.pop(key,None)
        successor=bytearray(48);put(successor,0,0x59B060);put(successor,8,self.probe['main']+0x64)
        pointer=0x1300000;terminal['successor_global']=pointer
        terminal['registered_tasks']=[dict(pointer=pointer,bucket=0,head_hex=successor.hex())]
        change_hex(terminal,'manager_hex',0,pointer)
        self.probe['samples'].append(terminal)
        self.probe['worker_exit']=dict(thread_id=2222,exit_code=0,wait_status=0,before_WM_CLOSE=True,
            retreat_flag_observed=True,tail_wait_observed=True)
        self.probe['successor']=copy.deepcopy(terminal['registered_tasks'][0]);self.probe['native_retreat_observed']=True
        result=self.verify();self.assertEqual(result['status'],'retreat_observed');self.assertIs(result['full_battle_exit_accepted'],False)
        self.probe['successor']['pointer']+=4;self.rejects()

    def test_report_hash_rejects_tamper(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'sample.gz';data=gzip.compress(b'{}',mtime=0);path.write_bytes(data)
            self.assertEqual(v.read_report(path,v.sha(data)),{})
            with self.assertRaisesRegex(ValueError,'SHA'):v.read_report(path,'0'*64)

    def test_decompression_bound(self):
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'sample.gz';data=gzip.compress(b'x'*(v.MAX_RAW+1),mtime=0);path.write_bytes(data)
            with self.assertRaisesRegex(ValueError,'decompressed report budget'):v.read_report(path,v.sha(data))


if __name__=='__main__':
    unittest.main()
