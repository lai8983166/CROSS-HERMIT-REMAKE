"""Independent interpretation of the bounded original wait hardware observations.

API boundary observations are not an instruction trace or complete state replay.
Source/collector/module authentication must precede use as provenance evidence.
"""
import struct
from pathlib import Path

SITES=(0x422360,0x4223A8,0x4223AE,0x4223BE,0x4223C4,0x4223D7,
       0x4223DD,0x4223EF,0x4223F5,0x422407,0x42240D,0x422431)
CALLS=((0x4223A8,0x4223AE,0x592234,1,None),
       (0x4223BE,0x4223C4,0x592228,1,'nonzero'),
       (0x4223D7,0x4223DD,0x59222C,1,'nonzero'),
       (0x4223EF,0x4223F5,0x592238,1,None),
       (0x422407,0x42240D,0x59226C,2,'zero'))


def need(value,message):
    if not value:raise ValueError(message)


def blob(text,size,label):
    value=bytes.fromhex(text)
    need(len(value)==size,'complete '+label)
    return value


def word(raw,offset=0):
    return struct.unpack_from('<I',raw,offset)[0]


def verify_current_tls(tls,context,owner,node,pid,tid):
    need(tls['owner_pid']==pid and tls['thread_id']==tid and tls['FS']==word(context,144),'current FS/owner')
    selector=blob(tls['selector_hex'],8,'actual selector')
    teb=struct.unpack_from('<H',selector,2)[0]|selector[4]<<16|selector[7]<<24
    need(teb==tls['TEB']==owner['TEB'],'current TEB from actual FS selector')
    h=blob(tls['TEB_head_hex'],64,'TEB head')
    need((word(h,0x18),word(h,0x20),word(h,0x24))==(teb,pid,tid),'TEB self and current PID/TID')
    need(word(h,8)<=word(context,196)<word(h,4),'current worker stack bounds')
    index=tls['TLS_index'];need(type(index)is int and 0<=index<1088 and index==owner['TLS_index'],'current CRT TLS index')
    slot=teb+0xE10+index*4 if index<64 else tls['expansion_pointer']+(index-64)*4
    if index>=64:need(tls['expansion_pointer']==owner['expansion_pointer'] and tls['expansion_pointer']!=0,'same current TLS expansion')
    need(slot==tls['slot']==owner['slot'] and word(blob(tls['TLS_slot_hex'],4,'current TLS slot'))==tls['PTD']==owner['PTD'],
         'read current TLS slot, not old PTD pointer alone')
    p=blob(tls['PTD_hex'],116,'current PTD')
    need((word(p),word(p,0x48),word(p,0x4C))==(tid,0x421F50,node),'current original PTD callback')


def verify_debug_write(record):
    before=blob(record['before_context_hex'],716,'pre-instrumentation context')
    wanted=blob(record['requested_debug_context_hex'],716,'requested debug-only context')
    after=blob(record['after_context_hex'],716,'post-instrumentation context')
    need(word(wanted)==0x10010 and before[28:]==wanted[28:],'only request debug-register writes')
    need(before[28:192]==after[28:192] and before[196:]==after[196:]
         and word(before,192)^word(after,192)in(0,2),'unchanged general/FPU/SIMD/segment state')
    need(tuple(word(wanted,i)for i in (4,8,12,16))==tuple(record['targets'])
         and word(wanted,24)==record['mask'] and word(wanted,20)==0,'declared debug instrumentation request')
    need(after[4:20]==wanted[4:20] and word(after,24)&~0x400==word(wanted,24)&~0x400,
         'debug targets/control actually installed')


def verify_failed_source(source,module_directory):
    """Authenticate the single retained failure without upgrading it to a proof."""
    import gzip,hashlib,json,zipfile
    import pefile
    from devtools import terminal_wait_observer_gate as gate
    root=Path(__file__).resolve().parents[1]
    packed=Path(source).read_bytes()
    need(hashlib.sha256(packed).hexdigest()==gate.FAILURE_SHA,'fixed bounded failure source')
    report=json.loads(gzip.decompress(packed));probe=report['probe'];r=probe['relay']
    raw=(root/'analysis/hermit_game.exe').read_bytes()
    need(hashlib.sha256(raw).hexdigest()=='588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005','fixed original image')
    need(gate.witness()['native_wait_relay_supported'] is False,'known incompatible witness')
    for row,(lo,hi)in zip(probe['code'],((0x422360,0x422434),(0x422560,0x4225DA),(0x56CE80,0x56CE98))):
        need(row['pointer']==lo and bytes.fromhex(row['hex'])==raw[lo-0x400000:hi-0x400000],'actual original failure code')
    need(len(probe['code'])==3,'all actual failure code ranges')
    # Pin executed layers via the exact immutable incremental capsules, never
    # re-sign an old source using the disabled current implementation.
    capsules={'devtools/terminal_debug_relay.py':'analysis/terminal-wait-relay-implementation-v5-20261109.zip',
              'devtools/terminal_wait_native_probe.py':'analysis/terminal-wait-relay-implementation-v4-20261109.zip'}
    need({p['path']for p in report['observer_implementations']}==set(capsules),'executed observer identity set')
    for row in report['observer_implementations']:
        with zipfile.ZipFile(root/capsules[row['path']])as archive:data=archive.read(row['path'])
        need(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'executed frozen observer bytes')
    expected=('EnterCriticalSection','ResetEvent','SetEvent','LeaveCriticalSection','WaitForSingleObject')
    need([r['name']for r in probe['API_exports']]==list(expected),'all five original OS exports')
    modules=[]
    for call,iat,entry in zip(CALLS,probe['IAT'],probe['API_exports']):
        # Only caller-supplied F-drive copies. Never use a same-named host DLL.
        path=Path(module_directory)/entry['module']
        data=path.read_bytes();need(hashlib.sha256(data).hexdigest()==entry['module_sha256'],'actual guest OS module SHA')
        pe=pefile.PE(data=data);need(pe.FILE_HEADER.Machine==0x14C,'guest x86 module')
        symbol=next(s for s in pe.DIRECTORY_ENTRY_EXPORT.symbols if s.name==entry['symbol'].encode())
        need(not symbol.forwarder and symbol.address==entry['RVA'],'actual final resolved OS export')
        need(iat['slot']==entry['slot']==call[2] and iat['target']==entry['target']==entry['base']+entry['RVA'],
             'original IAT equals current relocated final export')
        image=pe.get_memory_mapped_image(ImageBase=entry['base'])
        need(blob(entry['entry_hex'],32,'actual API entry')==blob(entry['relocated_disk_entry_hex'],32,'relocated entry')==
             image[entry['RVA']:entry['RVA']+32],'live API bytes and PE relocations')
        if not any(m['sha256']==entry['module_sha256']for m in modules):
            modules.append(dict(path=str(path),bytes=len(data),sha256=entry['module_sha256']))
    need(len(r['hits'])==len(r['original_child_replies'])==1 and r['hits'][0]['target']==0x422360,'only wait-entry stop observed')
    hit=r['hits'][0];reply=r['original_child_replies'][0];owner=probe['owner']
    need(hit['context_hex']==reply['child_context_hex'],'same child stop before original continuation')
    c=blob(hit['context_hex'],716,'actual child entry context')
    verify_current_tls(hit['data']['current_TLS'],c,owner['TLS'],owner['node'],r['child_pid'],r['child_tid'])
    need(word(c,184)==0x422360 and word(c,20)&1 and word(c,172)==owner['node'],'actual hardware wait-entry/receiver')
    need(reply['original_continue_status']==word(blob(reply['parent_stack_hex'],16,'parent stack'),12)==0x80010001,
         'original parent forwards exception, no success rewrite')
    for record in r['instrumentation']:verify_debug_write(record)
    need(r['debugger_reply_substituted'] is False and r['source_memory_written'] is False
         and r['general_registers_written'] is False,'no source/general/reply mutation claimed')
    life=report['lifecycle']['lifetime']
    need(r['parent_exit_during_scope']==0x4000001E and life['forced_termination'] is True
         and life['members_after_cleanup']==[],'failure and actual emergency cleanup separated')
    need(all(x['restored_exact']for x in report['mutable_private_runtime_files']),'private mutable originals restored')
    from devtools.isolated_vm_preflight import verify as verify_qualification
    isolation=report['input_isolation'];qualification=verify_qualification(json.loads(isolation['source_utf8']))
    return dict(accepted=False,kind='authenticated_incompatible_observer_failure',source=dict(path=str(source),
        bytes=len(packed),sha256=gate.FAILURE_SHA),guest_modules=modules,qualification=qualification,
        original_wait_entry_TLS_verified=True,original_OS_API_export_entries_verified=5,
        debug_only_write_receipts_verified=len(r['instrumentation']),original_parent_reply=0x80010001,
        parent_exit_during_scope=0x4000001E,child_pre_cleanup_exit_not_proved=True,
        cleanup_errors=r['cleanup']['errors'],forced_Job_cleanup=True,Job_members_after=[],
        wait_return_proved=False,result_consumption_proved=False,full_resource_lifetime_proved=False,
        original_debug_behavior_equivalence_proved=False,independent_full_replay=False,
        next_required='Non-injected-trap observation preflight; do not retry this mechanism or start two long cases.')


def verify(probe,raw):
    import hashlib
    need(hashlib.sha256(raw).hexdigest()=='588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005',
         'fixed original image')
    need(probe['error'] is None,'successful bounded native wait observation')
    ranges=((0x422360,0x422434),(0x422560,0x4225DA),(0x56CE80,0x56CE98))
    need(len(probe['code'])==len(ranges),'all observed original code ranges')
    for row,(lo,hi)in zip(probe['code'],ranges):
        need(row['pointer']==lo and blob(row['hex'],hi-lo,'live original code')==raw[lo-0x400000:hi-0x400000],
             'live original wait code equals fixed image')
    r=probe['relay'];owner=probe['owner'];node=owner['node'];tid=owner['thread_id']
    need(r['error'] is None and r['scope_completed'] is True,'complete relay scope')
    need(not r['cleanup']['errors'] and r['cleanup']['parent_detached'] is True
         and r['cleanup']['child_debug_registers_restored'] is True,'debug resources restored')
    for k in ('source_memory_written','general_registers_written','debugger_reply_substituted','accepted','full_instruction_trace'):
        need(r[k] is False,'no undeclared relay behavior '+k)
    need(r['child_tid']==tid and owner['TLS']['thread_id']==tid
         and owner['TLS']['owner_pid']==r['child_pid'] and r['child_pid']!=r['parent_pid'],'same current native owner')
    head=blob(owner['head_hex'],48,'original node header')
    manager=word(head,8);event=word(head,0x1C);ptd=owner['TLS']['PTD']
    need(word(head,0x24)==tid and event not in (0,0xFFFFFFFF),'current node thread and event')
    for key,handle in (('node_event',event),('manager_event',owner['manager_event']['remote_handle'])):
        e=owner[key]
        need(e['owner_pid']==r['child_pid'] and e['remote_handle']==handle and e['type_name']=='Event'
             and e['duplicate_succeeded'] is True and e['query_status']==0
             and e['wait_or_signal_called'] is False,'actual non-consuming event query '+key)
    hits=r['hits'];need(len(hits)==13 and [h['index']for h in hits]==list(range(13)), 'complete ordered wait boundaries')
    need([h['target']for h in hits[:12]]==list(SITES),'exact original wait sites')
    contexts=[blob(h['context_hex'],716,'WOW64 context')for h in hits]
    data=[h['data']for h in hits]
    stack=[blob(d['stack_hex'],128,'boundary stack')for d in data]
    caller=word(stack[0]);need(hits[-1]['target']==caller,'natural original caller')
    need(0x401005<=caller<0x591000 and raw[caller-5-0x400000]==0xE8
         and caller+struct.unpack_from('<i',raw,caller-4-0x400000)[0]==0x422360,
         'caller really invokes original wait')
    need(word(contexts[0],172)==node,'original thiscall receiver')
    need(all(a['elapsed']<=b['elapsed']for a,b in zip(hits,hits[1:])),'monotonic hardware observations')
    for h,c,d,s in zip(hits,contexts,data,stack):
        need(word(c,184)==h['target'] and word(c,20)&1,'actual selected hardware stop')
        need(d['stack_pointer']==word(c,196),'actual native ESP')
        n=blob(d['node_hex'],64,'node');m=blob(d['manager_hex'],0x120,'manager')
        need(d['node_pointer']==node and d['manager_pointer']==manager and word(n,8)==manager
             and word(n,0x24)==tid and word(n,0x1C)==event,'continuous current node identity')
        need(word(m,0x118)==owner['manager_event']['remote_handle'],'same scheduler event lifetime')
        p=blob(d['PTD_hex'],116,'PTD')
        need(d['PTD_pointer']==ptd and word(p)==tid and word(p,0x48)==0x421F50 and word(p,0x4C)==node,
             'same full current PTD owner')
        verify_current_tls(d['current_TLS'],c,owner['TLS'],node,r['child_pid'],tid)
    protocol=r['protocol'];need(len(protocol)==len(hits),'parent protocol for every stop')
    for i,p in enumerate(protocol):
        pc=blob(p['parent_context_hex'],716,'parent context');ps=blob(p['parent_stack_hex'],16,'parent API stack')
        need(p['hit_index']==i and tuple(struct.unpack('<2I',blob(p['client_id_hex'],8,'client id')))==(r['child_pid'],tid)
             and p['original_continue_status']==word(ps,12)==0x10002
             and word(pc,184)==r['parent_api']['target'],'original parent reply and owned client')
    rows={h['target']:(c,d,s)for h,c,d,s in zip(hits,contexts,data,stack)}
    expected_args={0x4223A8:(manager+0x100,),0x4223BE:(event,),
        0x4223D7:(owner['manager_event']['remote_handle'],),0x4223EF:(manager+0x100,),
        0x422407:(event,0xFFFFFFFF)}
    need([x['slot']for x in probe['IAT']]==[c[2]for c in CALLS]
         and all(x['target']not in (0,0xFFFFFFFF)for x in probe['IAT']),'complete non-null original API slots')
    api_results=[]
    for before,after,slot,argc,success in CALLS:
        bc,bd,bs=rows[before];ac,ad,ass=rows[after]
        need(raw[before-0x400000:before-0x400000+6]==b'\xff\x15'+struct.pack('<I',slot), 'original indirect CALL encoding')
        need(tuple(word(bs,i*4)for i in range(argc))==expected_args[before],'actual API arguments')
        need(word(ac,196)==word(bc,196)+argc*4,'original stdcall stack cleanup')
        need(all(word(bc,i)==word(ac,i)for i in (156,160,164,180)),'callee-saved original API ABI')
        value=word(ac,176)
        if success=='zero':need(value==0,'wait must return WAIT_OBJECT_0, never failure or timeout')
        if success=='nonzero':need(value!=0,'ResetEvent/SetEvent must succeed')
        api_results.append(dict(call=before,return_site=after,EAX=value))
    need(word(contexts[-1],196)==word(contexts[0],196)+8
         and all(word(contexts[-1],i)==word(contexts[0],i)for i in (156,160,164,180)), 'natural ret4 and preserved caller ABI')
    need(word(bytes.fromhex(data[9]['node_hex']),4)&0x10000
         and not(word(bytes.fromhex(data[-1]['node_hex']),4)&0x10000),'original wait flag armed and cleared')
    return dict(accepted=False,native_wait_callsite_sequence_verified=True,observed_boundaries=len(hits),
        API_results=api_results,full_instruction_trace=False,full_state_replay=False,
        producer_module_provenance_verified=False,full_resource_lifetime_proved=False)
