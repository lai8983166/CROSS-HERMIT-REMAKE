"""Independent bounded verification of recorded scene-owner observations.

No collector imports or native API calls. This checks retained observations and
replays only the original scenario-selection cdecl root. It never certifies a
complete native trace, WAIT_OBJECT_0, normal PTD destruction or battle acceptance.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA = '588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'
APP = '.venv-audit/scene-callback-runtime/CROSS HERMIT/CROSS HERMIT/CROSS HERMIT.EXE'
MAX_RAW = 32 * 1024 * 1024
RANGES = (
 (0x421540,0x421BE3),(0x421BF0,0x422289),(0x422290,0x422354),(0x422560,0x42260A),
 (0x42B2D0,0x42B2EF),(0x56E050,0x56E1E0),(0x56E1E0,0x56E230),(0x4539B0,0x453CFC),(0x594A54,0x594A5C),
 (0x451080,0x45199B),(0x4519C0,0x451B10),(0x439EF0,0x43A060),(0x422090,0x422289),
 (0x422360,0x422560),(0x59A430,0x59A438),
 (0x4E1B60,0x4E1C63),(0x49E930,0x49F570),(0x4DA860,0x4DAB50),(0x439E30,0x439EF0),
 (0x49DFD1,0x49E834),(0x451B10,0x4539B0),(0x4CE8F0,0x4D03B7),(0x46B470,0x46B663),
 (0x422360,0x422434),(0x422560,0x42260A),(0x56E050,0x56E225),(0x5753B0,0x57555B),
 (0x458580,0x458929),(0x453D00,0x453E5D),(0x451670,0x4519A3),(0x4967B0,0x4968A9),
 (0x45E8D0,0x45EA50),(0x60CB18,0x60CB28))
IAT = (0x592228,0x59222C,0x592230,0x592234,0x592238,0x592260,0x592264,0x592268,
       0x59226C,0x592270,0x592274,0x59227C,0x592280,0x5920A0,0x592068,0x5920C4,
       0x59221C,0x5921A8,0x5921AC,0x5921A4)
# Independent declaration: do not import the collector to validate its ranges.
RESOURCE_RANGES=((0x40E210,0x40E29A),(0x40E330,0x40EA80),
    (0x407AD0,0x408127),(0x40DB90,0x40DEB5),(0x40DF20,0x40E000),
    (0x403620,0x4037EF),(0x403BD0,0x403D44),(0x407710,0x4077B6),
    (0x428A40,0x428B59),(0x56F420,0x56F805))
THUNK = bytes.fromhex('558bec5356578b75088966208b5e0885db74094bff749e0c85db75f78b4e04ff1689461c896624c7462843414c4c31c05f5e5b5dc20400')
CDECL = THUNK.replace(bytes.fromhex('8b4e04ff16'),bytes.fromhex('8b4e04ff1683c404'))


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def u32(data, offset=0):
    return struct.unpack_from('<I',data,offset)[0]


def blob(value, size, label):
    need(isinstance(value,str) and len(value)==size*2, 'complete '+label)
    try:
        data=bytes.fromhex(value)
    except ValueError as exc:
        raise ValueError('hex '+label) from exc
    need(len(data)==size,'complete '+label)
    return data


def address(value, label):
    need(type(value) is int and 0<value<0x100000000,'x86 '+label)
    return value


def false_fields(obj, fields):
    for field in fields:
        need(obj.get(field) is False,'scope must remain false: '+field)


def source_rows(raw):
    need(len(raw)==5980160 and sha(raw)==SOURCE_SHA,'original source identity')
    return [dict(pointer=a,bytes=b-a,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in RANGES]


def scenario_replay(raw, before):
    """Execute authenticated original code and exact cdecl bridge, no API stubs."""
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
    from unicorn.x86_const import UC_X86_REG_ESP, UC_X86_REG_EFLAGS, UC_X86_REG_EIP
    need(len(before)==80,'scenario before extent')
    need(sha(raw)==SOURCE_SHA,'scenario original source identity')
    uc=Uc(UC_ARCH_X86,UC_MODE_32)
    uc.mem_map(0x400000,(len(raw)+4095)&~4095)
    uc.mem_write(0x400000,raw)
    uc.mem_write(0x7F4488,before)
    for at,size in ((0x31000000,65536),(0x32000000,4096),(0x33000000,4096),(0x34000000,4096)):
        uc.mem_map(at,size)
    uc.mem_write(0x32000000,CDECL)
    uc.mem_write(0x33000000,struct.pack('<11I',0x4DA860,0,1,4,0,0,0,0,0,0,0))
    uc.mem_write(0x3100FF00,struct.pack('<2I',0x34000000,0x33000000))
    uc.reg_write(UC_X86_REG_ESP,0x3100FF00)
    uc.reg_write(UC_X86_REG_EFLAGS,0x202)
    count=[0]
    def step(*_): count[0]+=1
    uc.hook_add(UC_HOOK_CODE,step)
    uc.emu_start(0x32000000,0x34000000,count=50000)
    block=bytes(uc.mem_read(0x33000000,44))
    need(uc.reg_read(UC_X86_REG_EIP)==0x34000000 and uc.reg_read(UC_X86_REG_ESP)==0x3100FF08
         and u32(block,32)==u32(block,36) and u32(block,40)==0x4C4C4143,'original cdecl natural return/ESP')
    return bytes(uc.mem_read(0x7F4488,80)),count[0]


def verify_calls(probe):
    frees=probe['private_frees']
    need(len(frees)==3 and all(x.get('released') is True for x in frees),'private bridge normal cleanup')
    allocations=list(reversed(frees))
    need([x['bytes'] for x in allocations]==[0x200000,4096,4096],'exact bridge allocation sizes')
    protected=((0x400000,5980160),(probe['main'],0x1110),(probe['worker']['node'],0x1194F0))
    for i,a in enumerate(allocations):
        address(a['pointer'],'private allocation')
        need(a['pointer']+a['bytes']<=0x100000000,'allocation end')
        for pointer,size in protected:
            need(a['pointer']+a['bytes']<=pointer or pointer+size<=a['pointer'],'bridge cannot alias original code/MAIN/scene')
        for b in allocations[i+1:]:
            need(a['pointer']+a['bytes']<=b['pointer'] or b['pointer']+b['bytes']<=a['pointer'],'non-overlapping bridge allocations')
    data,std,cdecl=[x['pointer'] for x in allocations]
    expected=[dict(pointer=std,bytes=len(THUNK),sha256=sha(THUNK)),dict(pointer=cdecl,bytes=len(CDECL),sha256=sha(CDECL))]
    calls=probe['calls']
    protocol=[(0x4E1B60,0,[]),(0x4DA860,0,[4]),(0x439E30,probe['main']+0x10,[16])]
    need(len(calls)==3 and [(c['va'],c['receiver'],c['args']) for c in calls]==protocol,'three exact original roots')
    for i,call in enumerate(calls):
        before=struct.pack('<11I',call['va'],call['receiver'],len(call['args']),
            *(call['args']+[0]*(3-len(call['args']))),0,0xCCCCCCCC,0xCCCCCCCC,0xCCCCCCCC,0)
        after=blob(call['parameter_after_hex'],44,'bridge output')
        need(call['sequence']==i and call['slot']==0 and call['parameter_before_hex']==before.hex()
            and after[:28]==before[:28] and u32(after,28)==call['eax']
            and u32(after,32)==u32(after,36)!=0 and u32(after,40)==0x4C4C4143
            and call['wait_status']==call['exit_code']==0,'native bridge parameters/ESP/completion')
        address(call['thread_id'],'bridge thread ID')
        expected.append(dict(pointer=data,bytes=44,sha256=sha(before)))
    need(probe['host_private_writes']==expected,'all host writes are exact private bridge bytes')


def verify_frame(frame):
    context=blob(frame['context_hex'],716,'WOW64_CONTEXT')
    need(u32(context)==0x1003F,'complete WOW64 context flags')
    need([frame[x] for x in ('EBP','EIP','ESP')]==[u32(context,x) for x in (180,184,196)],'context scalars')
    address(frame['tid'],'frame thread')
    chain=frame['chain']
    need(len(chain)<=100,'bounded frame chain')
    if chain: need(chain[0]['bp']==frame['EBP'],'chain context root')
    for row in chain:
        address(row['bp'],'frame BP')
        need(all(type(row[k]) is int and 0<=row[k]<0x100000000 for k in ('saved_bp','return_va')),'frame words')
    for a,b in zip(chain,chain[1:]):
        need(a['saved_bp']==b['bp'] and a['bp']<b['bp']<a['bp']+0x100000,'frame link/order')
    return context


def verify_graph(sample, main):
    manager=blob(sample['manager_hex'],0x120,'manager')
    rows=sample['registered_tasks']
    need(len(rows)<=128,'graph bound')
    mapping={r['pointer']:r for r in rows}
    need(len(mapping)==len(rows),'unique graph nodes')
    visited=[]
    for bucket in range(32):
        pointer=u32(manager,bucket*8)
        while pointer:
            need(pointer in mapping and pointer not in visited,'complete acyclic graph')
            row=mapping[pointer]
            address(pointer,'task pointer')
            head=blob(row['head_hex'],48,'registered task')
            need(row['bucket']==bucket and u32(head,8)==main+0x64,'task bucket/manager owner')
            visited.append(pointer)
            pointer=u32(head,12)
    need(visited==[r['pointer'] for r in rows],'exact graph traversal')
    need(sample['scene_registered'] is (sample['scene_global'] in mapping),'scene registration assertion')
    return mapping,manager


def verify_tls(sample, frame, worker, pid):
    tls=sample['TLS'];node=worker['node'];tid=worker['thread_id']
    context=blob(frame['context_hex'],716,'worker context')
    descriptor=blob(tls['selector_hex'],8,'FS descriptor')
    teb=struct.unpack_from('<H',descriptor,2)[0]|descriptor[4]<<16|descriptor[7]<<24
    need(teb==tls['TEB'] and tls['FS']==u32(context,144),'actual FS selector/base')
    need(descriptor[5]&0x80 and descriptor[5]&0x10 and not descriptor[5]&8,'present data FS descriptor')
    head=blob(tls['TEB_head_hex'],0x40,'TEB head')
    low,high=u32(head,8),u32(head,4)
    need(u32(head,0x18)==teb and u32(head,0x20)==pid and u32(head,0x24)==tid
         and tls['owner_pid']==pid and tls['thread_id']==tid and frame['tid']==tid,'TEB/TLS same owner')
    need(low<=frame['ESP']<high,'worker current stack bounds')
    index=tls['TLS_index']
    need(type(index) is int and 0<=index<1088,'TLS index bound')
    if index<64:
        need(tls['expansion_pointer'] is None,'fixed TLS has no expansion')
        slot=teb+0xE10+4*index
    else:
        slot=address(tls['expansion_pointer'],'TLS expansion')+4*(index-64)
    need(tls['slot']==slot,'TLS slot arithmetic')
    address(tls['PTD'],'PTD pointer')
    need(u32(blob(tls['TLS_slot_hex'],4,'TLS slot raw pointer'))==tls['PTD'],'actual TLS slot points to PTD')
    ptd=blob(tls['PTD_hex'],116,'full PTD')
    need((u32(ptd),u32(ptd,0x48),u32(ptd,0x4C))==(tid,0x421F50,node),'PTD worker/node identity')
    chain=frame['chain']
    wrappers=[r for r in chain if r['return_va']==0x56E183]
    callbacks=[r for r in chain if r['return_va']==0x421F8A]
    need(len(wrappers)==len(callbacks)==1,'one actual CRT/callback ancestor')
    wf,cf=wrappers[0],callbacks[0]
    need(low<=cf['bp']-4<cf['bp']+12<=high and low<=wf['bp']<wf['bp']+12<=high
         and low<=wf['saved_bp']<wf['saved_bp']+12<=high and cf['bp']<wf['bp']<wf['saved_bp'],
         'callback/worker/wrapper frame bounds and order')
    ancestry=tls['ancestry']
    scene=blob(sample['scene_head_hex'],512,'scene head')
    need(ancestry==dict(worker_argument=node,wrapper_argument=tls['PTD'],callback_this=node,
        callback_argument=u32(scene,0x18),node_argument=u32(scene,0x18)),'retained original ancestor arguments')
    expected_addresses=dict(worker_argument=wf['bp']+8,wrapper_argument=wf['saved_bp']+8,
                            callback_this=cf['bp']-4,callback_argument=cf['bp']+8,node_argument=node+0x18)
    memory=tls['ancestry_memory']
    need(set(memory)==set(expected_addresses),'all original argument memory retained')
    for name,pointer in expected_addresses.items():
        need(memory[name]['pointer']==pointer and u32(blob(memory[name]['hex'],4,'ancestor '+name))==ancestry[name],
             'raw original ancestor address/value '+name)
    need(sample['worker_stack_pointer']==frame['ESP'],'retained worker stack start')
    blob(sample['worker_stack_hex'],min(128,high-frame['ESP']),'retained worker stack window')


def verify_tls_implementation(row):
    from capstone import Cs,CS_ARCH_X86,CS_MODE_32
    code=blob(row['code_hex'],64,'TLS implementation')
    need(row['module'].lower()=='kernelbase.dll' and row['symbol']=='TlsGetValue'
         and row['target']==row['base']+row['RVA'],'TLS module/export location')
    instructions=[[i.mnemonic,i.op_str] for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(code,row['target'])]
    need(row['instructions']==instructions,'TLS implementation instruction bytes')
    # Bind actual addressing operations and bounds, not arbitrary operand substrings.
    for encoding in ('648b0d18000000','83f840','8b8481100e0000','3d40040000','8b89940f0000'):
        need(bytes.fromhex(encoding) in code,'authenticated TLS addressing contract')
    need(row['fixed_slots_offset']==0xE10 and row['expansion_pointer_offset']==0xF94,'TLS layout assertions')


def verify_report(report, raw):
    expected_source=source_rows(raw)
    need(report['schema_version']==1 and report['kind'] in (
        'actual_same_owner_scene_and_retreat_observation',
        'actual_same_owner_scene_resource_observation'),'report schema')
    if report['kind']=='actual_same_owner_scene_resource_observation':
        expected_source += [dict(pointer=a,bytes=b-a,sha256=sha(raw[a-0x400000:b-0x400000]))
                            for a,b in RESOURCE_RANGES]
        false_fields(report,('full_resource_lifetime_proved','full_battle_exit_accepted'))
        need(report['resource_status']=='partial','resource failure cannot pass owner observation')
    false_fields(report,('accepted','old_terminal_cases_replayed','full_native_instruction_or_API_trace',
                        'independent_full_replay','R3_complete','R4_complete','R5_complete','R6_complete'))
    p=report['probe'];need(p is not None and p['error'] is None and not p.get('cleanup_error'),'successful bounded owner observation')
    need(p['scenario']==4 and p['original_scene_constructor_and_factory'] is True,'original scenario4 owner observation')
    false_fields(p,('source_code_IAT_or_general_registers_written','old_terminal_fixture_loaded','full_instruction_trace',
                    'wait_API_return_status_sampled','full_battle_exit_accepted'))
    pid=address(p['pid'],'PID');main=address(p['main'],'MAIN')
    need('source_after' in p,'missing final live source identity')
    need(p['source_before']==p['source_after'] and p['source_before']['code']==expected_source,'complete unchanged original source ranges')
    iat=p['source_before']['IAT']
    need([r['slot'] for r in iat]==list(IAT) and all(u32(blob(r['hex'],4,'IAT slot')) for r in iat),'complete live IAT identity')
    verify_tls_implementation(p['TLS_implementation'])
    verify_calls(p)
    selected,count=scenario_replay(raw,blob(p['scenario_before_hex'],80,'before scenario'))
    need(p['scenario_selected_hex']==selected.hex(),'original scenario4 cdecl replay output')
    window=p['window'];need(window['pid']==pid and window['hwnd'] and window['main_tid'],'window owner')
    life=report['lifecycle'];ready=life['ready'];lifetime=life['lifetime']
    need(ready['pid']==pid and ready['main']['pointer']==main,'startup/scene same MAIN owner')
    need((ready['window']['pid'],ready['window']['tid'],ready['window']['hwnd'])==
         (pid,window['main_tid'],window['hwnd']),'startup and sampled HWND/thread ownership')
    need(not lifetime['members_after_cleanup'],'owned process tree cleanup')
    need(any(pid in x['pids'] for x in lifetime['membership']),'process in owned lifetime')
    need(all(x['restored_exact'] is True for x in report['mutable_private_runtime_files']),'private mutable files restored')
    worker=p['worker'];node=address(worker['node'],'scene node');tid=address(worker['thread_id'],'worker ID')
    address(worker['remote_handle'],'worker handle')
    for kind in ('node_event','manager_event'):
        event=worker[kind]
        need(event['owner_pid']==pid and event['duplicate_succeeded'] is True and event['query_status']==0
             and event['type_name']=='Event' and event['wait_or_signal_called'] is False,'same-owner non-consuming Event observation')
        need(event['remote_handle'] not in (0,0xFFFFFFFF),'valid recorded Event handle')
    initial=p['derived_object_initial'];body=blob(initial['hex'],0x1194F0,'initial derived scene')
    need(initial['pointer']==node and initial['bytes']==len(body) and u32(body)==0x59A430
         and u32(body,8)==main+0x64 and (u32(body,0x20),u32(body,0x24))==(worker['remote_handle'],tid),'original full derived object owner')
    samples=p['samples'];need(1<=len(samples)<=1751,'bounded samples')
    need([s['index'] for s in samples]==list(range(len(samples))),'sample sequence')
    need(all(a['elapsed']<=b['elapsed'] for a,b in zip(samples,samples[1:])),'sample monotonic order')
    tls_count=0;retreat=False;tail=False;successors=[];published=set();observed_returns=set()
    for sample in samples:
        blob(sample['MAIN_event_hex'],8,'MAIN event');blob(sample['scenario_hex'],80,'scenario snapshot')
        blob(sample['VM_hex'],128,'VM');blob(sample['game_exit_flag_hex'],4,'exit flag')
        need(type(sample['worker_exited']) is bool,'worker exit sample flag')
        frames=sample['frames'];need(len(frames)<=2 and len({f['tid'] for f in frames})==len(frames),'unique bounded sampled threads')
        for f in frames:
            need(f['tid'] in (window['main_tid'],tid),'only actual MAIN/worker context')
            verify_frame(f)
        mapping,manager=verify_graph(sample,main)
        current=sample['scene_global']
        if current: published.add(current)
        if 'scene_head_hex' in sample:
            need(current==node and node in mapping and not sample['worker_exited'],'live registered scene snapshot')
            head=blob(sample['scene_head_hex'],512,'scene head')
            need(head[:48].hex()==mapping[node]['head_hex'] and u32(head)==0x59A430
                 and u32(head,8)==main+0x64 and u32(head,0x18)==0 and head[0x28]==1,'derived scene exact registered prefix')
            need(sample['controller_task_backpointer']==node,'controller backpointer')
            if u32(head,4)&1:
                need((u32(head,0x20),u32(head,0x24),u32(head,0x1C))==
                     (worker['remote_handle'],tid,worker['node_event']['remote_handle']),'same active worker/node event')
            need(u32(manager,0x118)==worker['manager_event']['remote_handle'],'same actual manager event')
            inp=sample['input'];blob(inp['keyboard_edges_hex'],256,'keyboard edges')
            blob(inp['mouse_hex'],0x58,'complete mouse gate fields')
            need(inp['mouse_pointer']==inp['game']+0x196C,'original mouse window')
            retreat|=head[0x31]==1
        else:
            need('TLS' not in sample,'no TLS without live scene')
        wf=next((f for f in frames if f['tid']==tid),None)
        returns=[r['return_va'] for r in wf['chain']] if wf else []
        tail|=0x451758 in returns or 0x451796 in returns
        if 'TLS' in sample:
            need(wf is not None,'TLS actual sampled thread')
            verify_tls(sample,wf,worker,pid);tls_count+=1
            observed_returns.update(set(returns)&{0x42240D,0x4516D5,0x453CB5,0x453CD3,0x453CDD,
                                                 0x451758,0x451796,0x451ABC,0x451716,0x421F8A,0x56E183})
        successor=mapping.get(sample['successor_global'])
        if (successor and u32(bytes.fromhex(successor['head_hex']))==0x59B060 and not sample['scene_registered']
                and u32(bytes.fromhex(sample['MAIN_event_hex']))==0 and sample['worker_exited']):
            successors.append(successor)
    need(tls_count and published=={node},'observed complete same-owner TLS and single scene lifetime')
    if 'worker_exit' in p:
        exit_row=p['worker_exit']
        need(exit_row['thread_id']==tid and exit_row['wait_status']==0 and exit_row['before_WM_CLOSE'] is True
             and exit_row['retreat_flag_observed'] is retreat and exit_row['tail_wait_observed'] is tail,'worker exit agrees with retained observations')
    if p['native_retreat_observed'] is True:
        need('worker_exit' in p and p['worker_exit']['exit_code']==0 and retreat and tail
             and p.get('successor') in successors,'retreat observation endpoints')
    else:
        need(p['native_retreat_observed'] is False,'boolean retreat scope')
    return dict(schema_version=1,status='retreat_observed' if p['native_retreat_observed'] else 'partial',
        accepted=False,scenario=4,samples=len(samples),TLS_observations=tls_count,
        source_scenario_replay_instructions=count,same_owner_observation_verified=True,
        observed_worker_return_sites=[hex(x) for x in sorted(observed_returns)],
        native_retreat_observed=p['native_retreat_observed'],
        lifecycle_error=life.get('error'),forced_job_cleanup=lifetime.get('forced_termination'),
        full_memory_or_permissions_verified=False,full_native_instruction_or_API_trace=False,
        wait_API_success_proved=False,normal_PTD_cleanup_proved=False,
        callback_natural_return_directly_observed=False,full_battle_exit_accepted=False,
        old_terminal_cases_replayed=False,independent_full_replay=False,
        limitation='Validates recorded bounded samples and independent scenario-root replay; no full native execution replay or API-return trace. Frame return sites are active-call observations, not proof of successful OS wait return.')


def read_report(path, expected_sha):
    path=Path(path)
    need(path.stat().st_size<=8*1024*1024,'compressed report budget')
    packed=path.read_bytes();need(sha(packed)==expected_sha,'explicit report SHA identity')
    with gzip.open(path,'rb') as stream:
        data=stream.read(MAX_RAW+1)
    need(len(data)<=MAX_RAW,'decompressed report budget')
    return json.loads(data)


def verify_file(path, expected_sha):
    report=read_report(path,expected_sha)
    raw=(ROOT/'analysis/hermit_game.exe').read_bytes()
    observer=ROOT/'devtools/terminal_scene_owner.py'
    need(report['observer']==dict(path='devtools/terminal_scene_owner.py',bytes=observer.stat().st_size,
         sha256=sha(observer.read_bytes())),'collector immutable identity')
    need(report['original']==dict(path='analysis/hermit_game.exe',bytes=len(raw),sha256=SOURCE_SHA),'original receipt identity')
    need(Path(report['probe']['process_image']).resolve()==(ROOT/APP).resolve(),'private executable path')
    need(sha((ROOT/APP).read_bytes())=='030dca584a3a0b20751a72609f7acc823e8d79d820cebf1fcde8be6a791a9df7','private original executable identity')
    row=report['probe']['TLS_implementation'];dll=Path(row['module_path'])
    need(dll.resolve()==Path('C:/Windows/SysWOW64/kernelbase.dll').resolve(),'actual x86 OS module path')
    module=dll.read_bytes();need(sha(module)==row['module_sha256'],'OS module identity')
    import pefile
    pe=pefile.PE(data=module)
    export=next(x for x in pe.DIRECTORY_ENTRY_EXPORT.symbols if x.name==b'TlsGetValue')
    need(pe.FILE_HEADER.Machine==0x14C and export.forwarder is None and export.address==row['RVA']
         and pe.get_data(export.address,64).hex()==row['code_hex'],'actual OS export bytes')
    result=verify_report(report,raw)
    result['source_report']=dict(path=str(Path(path).resolve()),bytes=Path(path).stat().st_size,sha256=expected_sha)
    result['verifier_sha256']=sha(Path(__file__).read_bytes())
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--report',required=True);p.add_argument('--sha256',required=True);p.add_argument('--out',required=True)
    args=p.parse_args();out=Path(args.out)
    need(not out.exists(),'immutable verification output')
    result=verify_file(args.report,args.sha256)
    data=(json.dumps(result,indent=2)+'\n').encode()
    with out.open('xb') as stream: stream.write(data)
    print(json.dumps(result))


if __name__=='__main__':
    main()
