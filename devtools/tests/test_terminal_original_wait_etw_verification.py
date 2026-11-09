"""Bounded pure tests: no ETW, Windows API, VM, input or game process."""
import copy
import ctypes as C
import hashlib
from pathlib import Path
import struct
import unittest
from unittest import mock
import uuid

from devtools import terminal_original_wait_etw_verification as v


def event(index, ns, op, cpu, data, before):
    h=bytearray(80);struct.pack_into('<H',h,4,0x40)
    struct.pack_into('<II',h,8,0xffffffff,0xffffffff)
    struct.pack_into('<q',h,16,116444736000000000+ns//100)
    guid=v.etw.THREAD_GUID if op==36 else v.etw.PERF_GUID
    h[24:40]=uuid.UUID(guid).bytes_le;h[45]=op
    payload=(struct.pack('<II',data['NewThreadId'],data['OldThreadId']) if op==36 else
             struct.pack('<Q',data['SysCallAddress']) if op==51 else struct.pack('<I',data['SysCallNtStatus']))
    return dict(index=index,ns=ns,opcode=op,cpu=cpu,guid=guid,tid=0xffffffff,pid=0xffffffff,
                data=data,decoder_cpu_tid_before=before,record_header_hex=h.hex(),
                buffer_context_hex=bytes((cpu,0,0,0)).hex(),payload_hex=payload.hex())


def sample():
    tid=77;pid=42;node=0x300000;main=0x400000;manager=main+0x64;ptd=0x200000;teb=0x500000
    context=bytearray(716)
    for offset,value in ((144,0x53),(184,0x77001000),(180,0x100100),(196,0x100000)):
        struct.pack_into('<I',context,offset,value)
    chain=[dict(bp=0x100100,saved_bp=0x100200,return_va=0x42240D),
           dict(bp=0x100200,saved_bp=0x100300,return_va=0x421F8A),
           dict(bp=0x100300,saved_bp=0x100400,return_va=0x56E183)]
    regions=[dict(pointer=x['bp'],hex=struct.pack('<II',x['saved_bp'],x['return_va']).hex()) for x in chain]
    regions += [dict(pointer=0x100100,hex=struct.pack('<IIII',0x100200,0x42240D,90,0xffffffff).hex()),
                dict(pointer=0x1001f8,hex=struct.pack('<II',manager,node).hex())]
    head=bytearray(64)
    for offset,value in ((0,0x5CAA48),(4,0x10000),(8,manager),(0x18,19),(0x1c,90),(0x20,94),(0x24,tid)):
        struct.pack_into('<I',head,offset,value)
    manager_raw=bytearray(0x120);struct.pack_into('<I',manager_raw,0,node);struct.pack_into('<I',manager_raw,0x118,98)
    teb_raw=bytearray(64)
    for offset,value in ((4,0x110000),(8,0x100000),(0x18,teb),(0x20,pid),(0x24,tid)):
        struct.pack_into('<I',teb_raw,offset,value)
    ptd_raw=bytearray(116)
    for offset,value in ((0,tid),(0x48,0x421F50),(0x4c,node)):struct.pack_into('<I',ptd_raw,offset,value)
    selector=bytearray(8);struct.pack_into('<H',selector,2,teb&65535);selector[4]=(teb>>16)&255;selector[7]=teb>>24
    pointers=dict(worker_argument=0x100308,wrapper_argument=0x100408,callback_this=0x1001fc,
                  callback_argument=0x100208,node_argument=node+0x18)
    values=dict(worker_argument=node,wrapper_argument=ptd,callback_this=node,callback_argument=19,node_argument=19)
    tls=dict(owner_pid=pid,thread_id=tid,FS=0x53,selector_hex=selector.hex(),TEB=teb,TEB_head_hex=teb_raw.hex(),
        TLS_index=2,expansion_pointer=None,slot=teb+0xe18,TLS_slot_hex=struct.pack('<I',ptd).hex(),PTD=ptd,
        PTD_hex=ptd_raw.hex(),ancestry=values,
        ancestry_memory={k:dict(pointer=p,hex=struct.pack('<I',values[k]).hex()) for k,p in pointers.items()})
    snap=dict(node_pointer=node,node_hex=head.hex(),manager_pointer=manager,manager_hex=manager_raw.hex(),
        frame=dict(tid=tid,EIP=0x77001000,ESP=0x100000,EBP=0x100100,context_hex=context.hex(),chain=chain),
        scheduler_frame=dict(tid=41),current_TLS=tls,stack_regions=regions,
        registered_nodes=[dict(pointer=node,bucket=0,head_hex=head[:48].hex())],
        source_memory_written=False,debug_registers_written=False)
    snapshots={}
    for key,lo,hi in (('before',1000,2000),('observed_wait',10000,11000),('after',30000,31000)):
        snapshots[key]=dict(copy.deepcopy(snap),snapshot_begin_ns=lo,snapshot_end_ns=hi)
    image=(v.ROOT/'analysis/hermit_game.exe').read_bytes()
    props=v.etw.PROPERTIES();props.BuffersWritten=2;props.NumberOfBuffers=4
    requested=v.etw.PROPERTIES();requested.EnableFlags=0x92;requested.MaximumFileSize=4
    requested.LogFileMode=1;requested.BufferSize=64;requested.MaximumBuffers=8
    source=dict(kind='original_worker_ETW_wait',error=None,trace_flags=0x92,
        lifecycle=dict(error=None,lifetime=dict(parent_pid=40,forced_termination=False,members_after_cleanup=[],members_before_cleanup=[],
            membership=[dict(pids=[40,42]),dict(pids=[])],child_status_is_not_WinMain_return=True,
            exits={'40':dict(signaled=True,code=0),'42':dict(signaled=True,code=0xc0000354)}),
            window_after=dict(is_window=False,property=0),close_request=dict(posted=True,pid=42,job_members=[40,42],message=16,wParam=0,lParam=0),
            shutdown=[dict(globals={'0x7a49fc':0,'0x7a4a00':0,'0x80a398':0},
                crt_exit=dict(WinMain_result_hex='00000000',exit_argument_hex='00000000',callee_bp=100,caller_bp=200),
                frames=[dict(chain=[dict(bp=100,saved_bp=200,return_va=0x5714f2)])])]),
        mutable_private_runtime_files=[dict(restored_exact=True)],
        subject=dict(pid=pid,tid=tid,node=node,main=main,main_tid=41),owner_snapshots=snapshots,
        input_isolation=dict(current_guest_resources=dict(logical_processors=2)),
        capture_interval=dict(begin_ns=3000,end_ns=25000),kernel_wait_export=dict(target=0xfffff8020e4fcc00),
        trace=dict(start_status=0,stop_status=0,stopped=True,returned_stop_properties_hex=bytes(props).hex(),
            requested_properties_hex=bytes(requested).hex(),
            statistics=dict(EventsLost=0,LogBuffersLost=0,RealTimeBuffersLost=0,BuffersWritten=2,NumberOfBuffers=4)),
        ETL=dict(bytes=4096,sha256='a'*64),source_memory_written=False,general_registers_written=False,
        debug_registers_written=False,debug_object_modified=False,debugger_reply_substituted=False,
        host_game_calls=[],host_memory_writes=[],host_input_actions=[],
        event_owners={k:dict(owner_pid=pid,remote_handle=h,duplicate_succeeded=True,query_status=0,
                           type_name='Event',wait_or_signal_called=False) for k,h in (('node_event',90),('manager_event',98))},
        original_code=[dict(pointer=a,hex=image[a-0x400000:b-0x400000].hex()) for a,b in
            ((0x422360,0x422434),(0x422560,0x4225da),(0x56ce80,0x56ce98))])
    rows=[event(1,5000,36,0,dict(NewThreadId=tid,OldThreadId=9),9),
          event(2,8000,51,0,dict(SysCallAddress=source['kernel_wait_export']['target']),tid),
          event(3,9000,36,0,dict(NewThreadId=9,OldThreadId=tid),tid),
          event(4,12000,36,1,dict(NewThreadId=tid,OldThreadId=10),10),
          event(5,13000,52,1,dict(SysCallNtStatus=0),tid),
          event(6,20000,36,1,dict(NewThreadId=10,OldThreadId=tid),tid)]
    return source,rows,image


class StrictRecords(unittest.TestCase):
    def test_one_closed_raw_wait_and_owner(self):
        s,rows,image=sample();v.check_source(s,s['ETL'])
        result=v.analyze_original_events(rows,s)
        self.assertEqual(result['global_indices'],[2,5]);self.assertEqual(result['NTSTATUS'],0)
        self.assertFalse(result['accepted']);self.assertFalse(result['fullABI'])
        self.assertTrue(v.verify_owners(s,image)['current_TLS_verified'])

    def test_each_raw_field_is_bound(self):
        for field,value in (('ns',8100),('cpu',1),('tid',77),('guid',v.etw.THREAD_GUID),
                            ('payload_hex','00'*8),('decoder_cpu_tid_before',88)):
            with self.subTest(field=field):
                s,rows,_=sample();rows[1][field]=value
                with self.assertRaises(ValueError):v.analyze_original_events(rows,s)

    def test_nested_entry_fails_not_lifo(self):
        s,rows,_=sample();rows.insert(2,event(3,8500,51,0,dict(SysCallAddress=123),77))
        with self.assertRaisesRegex(ValueError,'overlapping'):v.analyze_original_events(rows,s)

    def test_missing_switch_or_exit_fails(self):
        for index in (2,3,4):
            s,rows,_=sample();del rows[index]
            with self.assertRaises(ValueError):v.analyze_original_events(rows,s)

    def test_failure_status_and_wrong_export_fail(self):
        s,rows,_=sample();rows[4]=event(5,13000,52,1,dict(SysCallNtStatus=258),77)
        with self.assertRaisesRegex(ValueError,'successful'):v.analyze_original_events(rows,s)
        s,rows,_=sample();s['kernel_wait_export']['target']+=8
        with self.assertRaisesRegex(ValueError,'export address'):v.analyze_original_events(rows,s)

    def test_snapshot_must_be_entirely_switched_out(self):
        s,rows,_=sample();s['owner_snapshots']['observed_wait']['snapshot_begin_ns']=8500
        with self.assertRaisesRegex(ValueError,'switched-out'):v.analyze_original_events(rows,s)

    def test_explicit_partial_boundary_is_never_selected(self):
        s,rows,_=sample();rows.insert(1,event(2,6000,52,0,dict(SysCallNtStatus=0),77))
        for i,row in enumerate(rows):row['index']=i+1
        result=v.analyze_original_events(rows,s)
        self.assertEqual(result['boundary_ledger']['initial_unpaired_exits'],[1])
        self.assertFalse(result['boundary_ledger']['full_global_pairing'])
        rows.insert(2,event(3,7000,52,0,dict(SysCallNtStatus=0),77))
        with self.assertRaisesRegex(ValueError,'unmatched'):v.analyze_original_events(rows,s)

    def test_two_cpu_attribution_rejected(self):
        s,rows,_=sample();rows.insert(2,event(3,8500,36,1,dict(NewThreadId=77,OldThreadId=10),10))
        with self.assertRaisesRegex(ValueError,'another CPU'):v.analyze_original_events(rows,s)


class OwnerTampering(unittest.TestCase):
    def test_tls_slot_and_node_lifetime_change(self):
        s,_,image=sample();s['owner_snapshots']['after']['current_TLS']['TLS_slot_hex']='00003000'
        with self.assertRaisesRegex(ValueError,'TLS slot'):v.verify_owners(s,image)
        s,_,image=sample();h=bytearray.fromhex(s['owner_snapshots']['after']['node_hex']);struct.pack_into('<I',h,0x1c,91)
        s['owner_snapshots']['after']['node_hex']=h.hex()
        with self.assertRaises(ValueError):v.verify_owners(s,image)

    def test_stack_parameter_and_frame_link_tamper(self):
        for idx in (0,3,4):
            s,_,image=sample();region=s['owner_snapshots']['observed_wait']['stack_regions'][idx]
            raw=bytearray.fromhex(region['hex']);raw[-1]^=1;region['hex']=raw.hex()
            with self.assertRaises(ValueError):v.verify_owners(s,image)

    def test_no_manager_or_ancestry_substitution(self):
        s,_,image=sample();s['owner_snapshots']['observed_wait']['registered_nodes']=[]
        with self.assertRaises(ValueError):v.verify_owners(s,image)
        s,_,image=sample();s['owner_snapshots']['observed_wait']['current_TLS']['ancestry_memory']['worker_argument']['pointer']+=4
        with self.assertRaises(ValueError):v.verify_owners(s,image)

    def test_source_kind_loss_and_hidden_write_rejected(self):
        for mutation in (lambda s:s.update(kind='owned_ETW_capability_fixture'),
                         lambda s:s.update(debug_registers_written=True),
                         lambda s:s['trace']['statistics'].update(EventsLost=1),
                         lambda s:s.update(helper=dict(pid=42,tid=77)),
                         lambda s:s['lifecycle']['lifetime'].update(forced_termination=True),
                         lambda s:s['mutable_private_runtime_files'][0].update(restored_exact=False),
                         lambda s:s.update(trace_flags=0x97),
                         lambda s:s['lifecycle']['lifetime']['exits']['42'].update(code=1)):
            s,_,_=sample();mutation(s)
            with self.assertRaises(ValueError):v.check_source(s,s['ETL'])

    def test_frozen_reader_identity_unchanged(self):
        self.assertEqual(hashlib.sha256(Path(v.etw.__file__).read_bytes()).hexdigest(),v.READER_SHA)

    def test_current_event_query_and_manager_event(self):
        s,_,image=sample();s['event_owners']['node_event']['remote_handle']=98
        with self.assertRaisesRegex(ValueError,'Event query'):v.verify_owners(s,image)
        s,_,image=sample();raw=bytearray.fromhex(s['owner_snapshots']['after']['manager_hex'])
        struct.pack_into('<I',raw,0x118,102);s['owner_snapshots']['after']['manager_hex']=raw.hex()
        with self.assertRaisesRegex(ValueError,'manager event'):v.verify_owners(s,image)

    def test_protection_status_never_substitutes_for_source_CRT(self):
        s,_,_=sample();self.assertTrue(v.verify_lifecycle(s)['source_CRT_zero_result_observed'])
        s['lifecycle']['shutdown'][0]['crt_exit']['WinMain_result_hex']='01000000'
        with self.assertRaisesRegex(ValueError,'zero return'):v.verify_lifecycle(s)
        s,_,_=sample();s['lifecycle']['shutdown']=[]
        with self.assertRaisesRegex(ValueError,'CRT zero result'):v.verify_lifecycle(s)


def receipt(rows):
    h=v.etw.LOG_HEADER();h.StartTime=116444736000000000+20;h.EndTime=116444736000000000+260
    h.NumberOfProcessors=2;h.PointerSize=8;h.PerfFreq=10_000_000;h.BuffersWritten=2;h.LogFileMode=1
    header={k:int(getattr(h,k)) for k in ('StartTime','EndTime','BootTime','PerfFreq','NumberOfProcessors',
        'PointerSize','EventsLost','BuffersLost','BuffersWritten','ReservedFlags','LogFileMode')}
    first=bytearray.fromhex(rows[0]['record_header_hex']);struct.pack_into('<q',first,16,h.StartTime)
    binding=bytearray(first);binding[45]=3;struct.pack_into('<q',binding,16,h.StartTime+20)
    return dict(process_trace_status=0,close_trace_status=0,callback_errors=[],retained_subject_records=len(rows),
        ETL_header=header,ETL_header_raw_hex=bytes(h).hex(),first_record=dict(FILETIME=h.StartTime,header_hex=first.hex()),
        buffer_reads=[1,2],subject_thread_bindings=[dict(opcode=3,pid=42,tid=77,ns=4000,header_hex=binding.hex(),
            payload_hex=struct.pack('<II',42,77).hex(),schema=dict(event_guid=v.etw.THREAD_GUID,provider_guid=v.etw.SYSTEM_GUID))])


class DecoderReceipts(unittest.TestCase):
    def test_original_header_and_binding(self):
        s,rows,_=sample();v.verify_decode_receipt(s,rows,receipt(rows))

    def test_header_loss_and_buffer_tampering(self):
        for mutation in (lambda r:r['ETL_header'].update(StartTime=r['ETL_header']['StartTime']+1),
                         lambda r:r['ETL_header'].update(EventsLost=1),
                         lambda r:r.update(buffer_reads=[1]),
                         lambda r:r.update(retained_subject_records=5),
                         lambda r:r.update(callback_errors=['aborted'])):
            s,rows,_=sample();r=receipt(rows);mutation(r)
            with self.assertRaises(ValueError):v.verify_decode_receipt(s,rows,r)

    def test_wrong_thread_and_lifetime_time(self):
        for mutation in (lambda b:b.update(pid=43),lambda b:b.update(ns=4100),
                         lambda b:b.update(payload_hex=struct.pack('<II',43,77).hex())):
            s,rows,_=sample();r=receipt(rows);mutation(r['subject_thread_bindings'][0])
            with self.assertRaises(ValueError):v.verify_decode_receipt(s,rows,r)

    def test_guest_qualification_precedes_output_and_native_decoder(self):
        with (mock.patch.object(v.etw,'qualify',side_effect=ValueError('not qualified')),
              mock.patch.object(v.etw,'_decode_etl') as reader):
            with self.assertRaisesRegex(ValueError,'not qualified'):
                v.decode_source(Path('unused'),'',Path('unused'),'','unused')
            reader.assert_not_called()


def nt_context_sample():
    source,_,_=sample();snap=source['owner_snapshots']['observed_wait'];frame=snap['frame']
    entry=dict(name='NtWaitForSingleObject',target=0x77893bf0,RVA=0x73bf0,base=0x77820000,
               module_sha256=hashlib.sha256(b'original guest bytes').hexdigest())
    code=bytes.fromhex('b804000d00ba10678b77ffd2c20c00')+bytes(49)
    entry['entry_hex']=code.hex();source['API_exports']=[entry]
    raw=bytearray.fromhex(frame['context_hex']);struct.pack_into('<I',raw,184,entry['target']+12)
    struct.pack_into('<I',raw,176,1);frame['context_hex']=raw.hex();frame['EIP']=entry['target']+12
    snap['stack_regions'].append(dict(pointer=frame['ESP'],hex=struct.pack('<IIII',0x76378229,90,0,0).hex()))
    return source,entry,code


class ActualNtWaitContext(unittest.TestCase):
    def test_raw_stub_and_three_parameters_do_not_infer_return(self):
        source,entry,code=nt_context_sample();r=v.verify_Nt_wait_stack(source,entry,code)
        self.assertEqual((r['EventHandle'],r['Alertable'],r['Timeout']),(90,0,0))
        self.assertEqual(r['snapshot_EAX'],1);self.assertFalse(r['snapshot_EAX_is_syscall_result'])
        self.assertFalse(r['caller_callsite_instruction_verified']);self.assertFalse(r['fullABI'])

    def test_stub_opcodes_and_cleanup_count_are_bound(self):
        for offset in (0,5,10,11,12,13,14):
            with self.subTest(offset=offset):
                source,entry,code=nt_context_sample();raw=bytearray(code);raw[offset]^=1
                with self.assertRaisesRegex(ValueError,'stub'):v.verify_Nt_wait_stack(source,entry,bytes(raw))

    def test_actual_EIP_must_be_post_call_ret_instruction(self):
        for offset in (0,10,13):
            source,entry,code=nt_context_sample();frame=source['owner_snapshots']['observed_wait']['frame']
            raw=bytearray.fromhex(frame['context_hex']);struct.pack_into('<I',raw,184,entry['target']+offset)
            frame['context_hex']=raw.hex();frame['EIP']=entry['target']+offset
            with self.assertRaisesRegex(ValueError,'exact NtWait'):v.verify_Nt_wait_stack(source,entry,code)

    def test_each_native_parameter_is_actual_not_inferred(self):
        for offset in (4,8,12):
            source,entry,code=nt_context_sample();region=source['owner_snapshots']['observed_wait']['stack_regions'][-1]
            raw=bytearray.fromhex(region['hex']);struct.pack_into('<I',raw,offset,91 if offset==4 else 1);region['hex']=raw.hex()
            with self.assertRaisesRegex(ValueError,'NT wait arguments'):v.verify_Nt_wait_stack(source,entry,code)

    def test_wrong_guest_module_rejected_before_PE_interpretation(self):
        source,entry,code=nt_context_sample()
        with self.assertRaisesRegex(ValueError,'guest DLL bytes'):
            v.verify_Nt_wait_context(source,lambda row:b'substituted guest bytes')


def missing_crt_sample():
    source,_,_=sample();raw=bytearray(0xd0);bp=0x100200;struct.pack_into('<I',raw,0xb0,0x5714e6)
    source['lifecycle']['shutdown']=[dict(elapsed=6.4,globals={'0x7a49fc':0,'0x7a4a00':0,'0x80a398':0},
        frames=[dict(chain=[dict(bp=bp,saved_bp=bp+0x100,return_va=0x5714e6),
                            dict(bp=bp-0x100,saved_bp=bp,return_va=0x49e120)])],
        winmain_frame=dict(bp=bp,stack_start=bp-0xac,stack_hex=raw.hex(),
                           locals_hex=raw[0x10:0xac].hex(),args_hex=raw[0xb4:0xc4].hex()))]
    return source


class ExplicitCleanupDiagnostic(unittest.TestCase):
    def test_default_remains_strict_and_diagnostic_does_not_claim_CRT(self):
        source=missing_crt_sample()
        with self.assertRaisesRegex(ValueError,'CRT zero result'):v.check_source(source,source['ETL'])
        result=v.check_source(source,source['ETL'],diagnostic_only=True)
        self.assertTrue(result['diagnostic_only']);self.assertFalse(result['source_CRT_zero_result_observed'])
        self.assertFalse(result['strict_source_cleanup_verified']);self.assertFalse(result['PTDcleanup'])
        self.assertFalse(result['pre_CRT_cleanup_witness']['sampled_return_local_is_CRT_return'])

    def test_diagnostic_does_not_allow_forced_or_failed_cleanup(self):
        for mutation in (lambda s:s['lifecycle']['lifetime'].update(forced_termination=True),
                         lambda s:s['lifecycle']['lifetime']['exits']['42'].update(code=1),
                         lambda s:s['lifecycle'].update(window_after=dict(is_window=True,property=0)),
                         lambda s:s['mutable_private_runtime_files'][0].update(restored_exact=False)):
            source=missing_crt_sample();mutation(source)
            with self.assertRaises(ValueError):v.check_source(source,source['ETL'],diagnostic_only=True)

    def test_diagnostic_requires_real_pre_CRT_endpoint(self):
        for mutation in (lambda x:x['globals'].update({'0x7a4a00':123}),
                         lambda x:x['frames'][0]['chain'][1].update(return_va=0x49e131),
                         lambda x:x['frames'][0]['chain'][0].update(return_va=0x5714e5),
                         lambda x:x['winmain_frame'].update(stack_start=1)):
            source=missing_crt_sample();mutation(source['lifecycle']['shutdown'][0])
            with self.assertRaises(ValueError):v.check_source(source,source['ETL'],diagnostic_only=True)

    def test_contradictory_or_incomplete_CRT_receipt_not_diagnostic(self):
        source=missing_crt_sample();source['lifecycle']['shutdown'][0]['crt_exit']=dict(WinMain_result_hex='01000000',exit_argument_hex='01000000')
        with self.assertRaises(ValueError):v.check_source(source,source['ETL'],diagnostic_only=True)
        source=missing_crt_sample();source['lifecycle']['shutdown'][0]['frames'][0]['chain'].append(dict(bp=2,saved_bp=3,return_va=0x5714f2))
        with self.assertRaisesRegex(ValueError,'absent CRT-exit frame'):v.check_source(source,source['ETL'],diagnostic_only=True)

    def test_sampled_return_local_cannot_be_substituted(self):
        source=missing_crt_sample();f=source['lifecycle']['shutdown'][0]['winmain_frame']
        raw=bytearray.fromhex(f['stack_hex']);struct.pack_into('<I',raw,0xa8,1)
        f.update(stack_hex=raw.hex(),locals_hex=raw[0x10:0xac].hex())
        with self.assertRaisesRegex(ValueError,'return local is zero'):v.check_source(source,source['ETL'],diagnostic_only=True)

    def test_source_ETL_and_loss_guards_not_bypassed(self):
        source=missing_crt_sample();wrong=dict(source['ETL'],sha256='b'*64)
        with self.assertRaises(ValueError):v.check_source(source,wrong,diagnostic_only=True)
        source['trace']['statistics']['EventsLost']=1
        with self.assertRaises(ValueError):v.check_source(source,source['ETL'],diagnostic_only=True)


if __name__=='__main__':unittest.main()
