"""Independent bounded verifier of read-only startup/menu observations.

Imports verification primitives only, never the native collector. A qualified
handoff observation is partial evidence, not complete retirement/resource proof.
"""
from __future__ import annotations
import argparse
import math
import json
from pathlib import Path
import struct

from devtools import terminal_scene_owner_verification as owner
from devtools import terminal_startup_handoff_contract as contract

ROOT=owner.ROOT
need=owner.need
word=owner.u32
blob=owner.blob
STARTUP=0x5CAA48
MENU=0x59B060
PARENT='analysis/terminal-scene-preflight-v3-20261107.json.gz'
PARENT_SHA='3a028556e6e0141746df00573766332ee91ec34bb7a6c19ba4e182724ff4d7ff'
EXTRA_RANGES=((0x506150,0x5066A0),(0x50A007,0x50A1E8),
    (0x45E8D0,0x45EDB8),(0x4217C0,0x421BF0),(0x421F50,0x422090),
    (0x41F480,0x41F640),(0x45EFB0,0x45F0CB),(0x415480,0x415C00))
V2_RANGES=((0x5066A0,0x50673A),(0x525060,0x525084),(0x49E834,0x49E845))
V2_IAT=tuple(dict.fromkeys(owner.IAT+(0x592440,0x592284)))
IMPLEMENTATIONS=('devtools/terminal_startup_handoff.py',
                 'devtools/terminal_scene_owner.py','devtools/terminal_scene_resources.py')


def number(value,label):
    need(type(value) in (int,float) and math.isfinite(value) and value>=0,label)
    return value


def verify_graph(sample,main):
    manager=blob(sample['manager_hex'],0x120,'complete scheduler')
    rows=sample['registered_tasks']
    need(isinstance(rows,list) and len(rows)<=32,'bounded task graph')
    nodes={r['pointer']:r for r in rows}
    need(len(nodes)==len(rows),'unique task nodes')
    visited=[]
    for bucket in range(32):
        pointer=word(manager,bucket*8)
        while pointer:
            need(type(pointer) is int and 0x10000<=pointer<0x80000000
                 and pointer in nodes and pointer not in visited,'complete acyclic graph')
            row=nodes[pointer];head=blob(row['head_hex'],48,'task header')
            need(row['bucket']==bucket and word(head,8)==main+0x64,'same manager and bucket')
            visited.append(pointer);pointer=word(head,12)
    need(visited==list(nodes),'exact single-linked graph traversal')
    kinds={vt:[p for p,r in nodes.items() if word(bytes.fromhex(r['head_hex']))==vt]
           for vt in (STARTUP,MENU)}
    need(all(len(v)<=1 for v in kinds.values()),'unique startup/menu')
    need(not (kinds[STARTUP] and kinds[MENU]),'observed startup/menu overlap')
    need(sum(map(len,kinds.values()))==len(nodes),'no unrelated original tasks')
    return nodes,manager,kinds


def verify_tls(tls,frame,head,node,tid,pid,locals_row,version=1):
    context=blob(frame['context_hex'],716,'worker context')
    selector=blob(tls['selector_hex'],8,'FS descriptor')
    teb=struct.unpack_from('<H',selector,2)[0]|selector[4]<<16|selector[7]<<24
    need(tls['TEB']==teb and tls['FS']==word(context,144)
         and selector[5]&0x80 and selector[5]&0x10 and not selector[5]&8,'actual FS data descriptor')
    th=blob(tls['TEB_head_hex'],0x40,'TEB header');low,high=word(th,8),word(th,4)
    need(word(th,0x18)==teb and word(th,0x20)==pid and word(th,0x24)==tid
         and tls['owner_pid']==pid and tls['thread_id']==tid==frame['tid'],'same TEB/PID/TID')
    need(0<low<=frame['ESP']<high<=0x100000000,'TEB stack bounds')
    index=tls['TLS_index'];need(type(index) is int and 0<=index<1088,'bounded TLS index')
    if version==2:
        memory=tls.get('index_memory',{})
        need(memory.get('pointer')==0x761BC0
             and word(blob(memory.get('hex'),4,'CRT TLS index memory'))==index,
             'actual original CRT TLS index address/value')
    else:
        need('index_memory' not in tls and 'expansion_memory' not in tls,
             'v1 cannot silently carry unverified v2 TLS fields')
    if index<64:
        need(tls['expansion_pointer'] is None,'inline TLS slots')
        need('expansion_memory' not in tls,'inline TLS has no expansion memory claim')
        slot=teb+0xE10+index*4
    else:
        slot=owner.address(tls['expansion_pointer'],'TLS expansion')+(index-64)*4
        if version==2:
            memory=tls.get('expansion_memory',{})
            need(memory.get('pointer')==teb+0xF94
                 and word(blob(memory.get('hex'),4,'TLS expansion memory'))==tls['expansion_pointer'],
                 'actual TEB expansion pointer address/value')
    need(tls['slot']==slot and word(blob(tls['TLS_slot_hex'],4,'TLS raw slot'))==tls['PTD'],
         'TLS pointer arithmetic and actual PTD slot')
    owner.address(tls['PTD'],'PTD')
    ptd=blob(tls['PTD_hex'],116,'complete PTD')
    need((word(ptd),word(ptd,0x48),word(ptd,0x4C))==(tid,0x421F50,node),'PTD worker callback/node')
    callbacks=[r for r in frame['chain'] if r['return_va']==0x421F8A]
    wrappers=[r for r in frame['chain'] if r['return_va']==0x56E183]
    need(len(callbacks)==len(wrappers)==1,'one callback and CRT ancestor')
    cf,wf=callbacks[0],wrappers[0]
    need(low<=cf['bp']-0x80<cf['bp']+12<=high and cf['bp']<wf['bp']<wf['saved_bp']
         and low<=wf['bp']<wf['bp']+12<=high and wf['saved_bp']+12<=high,
         'original callback/worker/CRT stack ancestry')
    need(locals_row['pointer']==cf['bp']-0x80,'callback locals belong to TLS-bound frame')
    expected=dict(worker_argument=node,wrapper_argument=tls['PTD'],callback_this=node,
                  callback_argument=word(head,0x18),node_argument=word(head,0x18))
    need(tls['ancestry']==expected,'exact original call arguments')
    addresses=dict(worker_argument=wf['bp']+8,wrapper_argument=wf['saved_bp']+8,
        callback_this=cf['bp']-4,callback_argument=cf['bp']+8,node_argument=node+0x18)
    memory=tls['ancestry_memory'];need(set(memory)==set(addresses),'complete raw ancestry')
    for name,pointer in addresses.items():
        need(memory[name]['pointer']==pointer and word(blob(memory[name]['hex'],4,name))==expected[name],
             'actual raw original argument '+name)


def verify_event(event,pid,label):
    need(event['owner_pid']==pid and event['duplicate_succeeded'] is True and event['query_status']==0
         and event['type_name']=='Event' and event['wait_or_signal_called'] is False
         and type(event['remote_handle']) is int and 0<event['remote_handle']<0xFFFFFFFF,
         'same-owner original '+label+' event')


def verify_samples(probe,game,version=1):
    pid=owner.address(probe['pid'],'PID');main=owner.address(probe['main'],'MAIN')
    window=probe['window'];main_tid=owner.address(window['main_tid'],'MAIN TID')
    worker=probe['worker'];node=owner.address(worker['node'],'startup node')
    tid=owner.address(worker['thread_id'],'startup TID')
    need(tid!=main_tid and window['pid']==pid and window['hwnd'],'distinct owned MAIN/worker')
    owner.address(worker['remote_handle'],'worker handle')
    event=worker['node_event']
    verify_event(event,pid,'node')
    if version==2:
        need('manager_event' in worker,'v2 manager Event identity')
        verify_event(worker['manager_event'],pid,'manager')
        need(worker['manager_event']['remote_handle']!=event['remote_handle'],'distinct node/manager events')
    else:need('manager_event' not in worker,'v1 cannot silently carry unverified manager Event identity')
    samples=probe['samples'];need(1<=len(samples)<=1600,'bounded retained samples')
    need([r['index'] for r in samples]==list(range(len(samples))),'sample indices')
    elapsed=[number(r['elapsed'],'sample time') for r in samples]
    need(all(a<=b for a,b in zip(elapsed,elapsed[1:])),'monotonic sample times')
    tls_count=0;counter_before=None;limit_indices=[];startup_indices=[];menu_indices=[]
    exited_seen=False;menu_node=None;manager_event=None;tls_identity=None
    for i,row in enumerate(samples):
        nodes,manager,kinds=verify_graph(row,main)
        if version==2:
            need(word(manager,0x118)==worker['manager_event']['remote_handle'],
                 'manager Event identity bound to every raw manager snapshot')
        pending=blob(row['MAIN_event_hex'],8,'MAIN pending event')
        need(word(pending) in (0,1),'MAIN pending state')
        need(row['game']==game and row['timing_pointer']==game+0xB17C,'same game timing owner')
        blob(row['timing_hex'],0x7C,'frame timing');blob(row['mouse_hex'],0x58,'mouse input')
        blob(row['group10_hex'],8,'group10');blob(row['group90_hex'],8,'group90')
        exited=row['startup_thread_exited'];need(type(exited) is bool,'worker exit sample flag')
        need(not exited_seen or exited,'no worker resurrection');exited_seen|=exited
        frames=row['frames'];need(1<=len(frames)<=2 and len({f['tid'] for f in frames})==len(frames),
                                 'bounded unique contexts')
        need(any(f['tid']==main_tid for f in frames),'MAIN context in every sample')
        for frame in frames:
            need(frame['tid'] in (main_tid,tid),'actual original thread context')
            owner.verify_frame(frame)
        wf=next((f for f in frames if f['tid']==tid),None)
        need(not exited or wf is None,'no suspended context for terminated worker')
        if kinds[STARTUP]:
            startup_indices.append(i)
            need(kinds[STARTUP]==[node] and row['startup_node']==node,'same startup lifetime')
            head=blob(row['startup_head_hex'],64,'startup header')
            need(head[:48].hex()==nodes[node]['head_hex'] and head[0x28]==1,'exact startup prefix/autodelete')
            if word(head,0x20):
                need((word(head,0x20),word(head,0x24),word(head,0x1C))==
                     (worker['remote_handle'],tid,event['remote_handle']),'same worker/event fields')
            current_event=word(manager,0x118)
            if manager_event is None:manager_event=current_event
            need(current_event==manager_event and 0<current_event<0xFFFFFFFF,'same live manager event field')
            if 'callback_locals' in row:
                local=row['callback_locals'];data=blob(local['hex'],128,'callback locals')
                need(wf is not None,'callback locals require actual worker frame')
                matches=[f for f in wf['chain'] if f['return_va']==0x421F8A]
                need(len(matches)==1 and local['pointer']==matches[0]['bp']-0x80,'callback locals frame address')
                need(local['this']==word(data,0x7C)==node and local['counter']==word(data,0x74),
                     'raw callback this and counter')
                counter=local['counter']
                # Debug-filled uninitialized locals before50649E are not progress.
                if counter!=0xCCCCCCCC:
                    need(counter<=0x3F4D,'bounded unmodified startup counter')
                    if counter_before is not None:need(counter>=counter_before,'startup counter cannot decrease')
                    counter_before=counter
                    if head[0x30]==100 and counter>=0x3F4C:limit_indices.append(i)
                if 'TLS' in row:
                    verify_tls(row['TLS'],wf,head,node,tid,pid,local,version);tls_count+=1
                    observed_identity=tuple(row['TLS'][k] for k in ('TEB','FS','TLS_index','slot','PTD'))+(local['pointer'],)
                    if tls_identity is None:tls_identity=observed_identity
                    need(observed_identity==tls_identity,'same callback/TEB/TLS/PTD lifetime across samples')
            else:need('TLS' not in row,'no TLS claim without callback locals')
        else:
            need(not any(k in row for k in ('startup_head_hex','startup_node','callback_locals','TLS')),
                 'no stale deleted startup dereference')
        if kinds[MENU]:
            current=kinds[MENU][0]
            need(row['menu_node']==current and (menu_node is None or menu_node==current),'same menu lifetime')
            menu_node=current
            if exited and word(pending)==0:menu_indices.append(i)
        else:need('menu_node' not in row,'no invented menu pointer')
    need(startup_indices and tls_count,'actual original startup and full TLS observations')
    need(probe['natural_animation_limit_observed'] is bool(limit_indices),'threshold claim derived from retained raw samples')
    complete=False
    if probe.get('worker_exit') is not None:
        ex=probe['worker_exit']
        need(ex['thread_id']==tid and ex['wait_status']==0 and ex['before_WM_CLOSE'] is True
             and ex['natural_return_full_trace_proved'] is False and exited_seen,'retained worker signaled before cleanup')
        t=number(ex['elapsed'],'worker exit observation time')
        need(samples[0]['elapsed']<=t<=samples[-1]['elapsed']+1,'worker exit inside probe')
        normal=type(ex['exit_code']) is int and ex['exit_code']==0
        # Check a contiguous retained suffix. Sparse samples cannot exclude an
        # unsampled transient overlap; the proof records that limit explicitly.
        suffix=[]
        for index in reversed(range(len(samples))):
            if index not in menu_indices:break
            suffix.append(index)
        complete=bool(normal and limit_indices and suffix
            and max(limit_indices)<min(suffix)
            and samples[max(suffix)]['elapsed']-samples[min(suffix)]['elapsed']>=1)
    else:need(not exited_seen,'exit samples require queried exit result')
    need(probe['native_handoff_observed'] is complete,'handoff claim must match normal exit and retained stable menu')
    if complete:need(probe['stop_reason']=='startup_thread_exited_and_menu_alone','handoff stop reason')
    else:need(probe['stop_reason']=='bounded_deadline','partial observation deadline')
    return dict(samples=len(samples),TLS_samples=tls_count,animation_limit_samples=limit_indices,
                native_handoff_observed=complete,worker_exit_code=probe.get('worker_exit',{}).get('exit_code'))


def verify_report(report,raw):
    contract.authenticate(raw)
    need(report['schema_version']==1 and report['kind']=='native_startup_natural_handoff_observation','startup report schema')
    owner.false_fields(report,('accepted','old_terminal_cases_replayed','independent_full_replay',
        'full_native_instruction_or_API_trace','R3_complete','R4_complete','R5_complete','R6_complete',
        'original_scene_roots_called','human_operation_required','full_resource_lifetime_proved','full_battle_exit_accepted'))
    p=report['probe'];life=report['lifecycle'];ready=life['ready'];lifetime=life['lifetime']
    need(p['error'] is None and life['error'] is None,'successful bounded read-only observation')
    owner.false_fields(p,('full_native_instruction_trace','normal_PTD_cleanup_proved','full_battle_exit_accepted'))
    need(p['host_original_calls']==p['host_memory_writes']==p['host_input_actions']==[],
         'no original calls, host memory writes or input')
    need(p['process_access']==0x100450,'query/read/duplicate/synchronize-only process rights')
    need(Path(p['process_image']).resolve()==(ROOT/owner.APP).resolve(),'exact private executable path')
    need(ready['pid']==p['pid'] and ready['main']['pointer']==p['main'],'same original process/MAIN')
    need((ready['window']['pid'],ready['window']['tid'],ready['window']['hwnd'])==
         (p['pid'],p['window']['main_tid'],p['window']['hwnd']),'same original window')
    expected=owner.source_rows(raw)+[dict(pointer=a,bytes=b-a,sha256=owner.sha(raw[a-0x400000:b-0x400000]))
                                   for a,b in EXTRA_RANGES]
    expected_v2=expected+[dict(pointer=a,bytes=b-a,sha256=owner.sha(raw[a-0x400000:b-0x400000]))
                         for a,b in V2_RANGES]
    code=p['source_before']['code']
    need(p['source_before']==p['source_after'] and code in (expected,expected_v2),
         'complete declared live original ranges unchanged')
    version=2 if code==expected_v2 else 1
    iat=p['source_before']['IAT']
    need([r['slot'] for r in iat]==list(V2_IAT if version==2 else owner.IAT)
         and all(word(blob(r['hex'],4,'IAT target'))>=0x10000 for r in iat),'complete non-null live IAT')
    owner.verify_tls_implementation(p['TLS_implementation'])
    need(lifetime['forced_termination'] is False and lifetime['members_after_cleanup']==[]
         and any(p['pid'] in r['pids'] for r in lifetime['membership']),'owned Job drained without forced termination')
    members={pid for row in lifetime['membership'] for pid in row['pids']}
    exits=lifetime['exits']
    need({str(pid) for pid in members}==set(exits) and lifetime['parent_pid'] in members
         and all(e['signaled'] is True and type(e['code']) is int and 0<=e['code']<=0xFFFFFFFF
                 for e in exits.values()),'complete owned process exit statuses')
    need(lifetime['child_status_is_not_WinMain_return'] is True,
         'protected child status must not be called a WinMain return')
    need(life['close_request']['pid']==p['pid'] and life['close_request']['message']==16
         and life['close_request']['posted'] is True,'owned WM_CLOSE after probe')
    # close_request.elapsed is recorded before the injected read-only probe,
    # so it must not be mistaken for the actual later PostMessage timestamp.
    result=verify_samples(p,ready['game']['pointer'],version)
    # Compute coverage rather than equating a version label with proof.
    merged=[]
    for start,end in sorted((r['pointer'],r['pointer']+r['bytes']) for r in code):
        if merged and start<=merged[-1][1]:merged[-1]=(merged[-1][0],max(end,merged[-1][1]))
        else:merged.append((start,end))
    covered=all(any(a<=start and end<=b for a,b in merged) for start,end in contract.RANGES)
    result.update(status='partial_handoff_observation' if result['native_handoff_observed'] else 'partial_bounded_observation',
        observed_source_contract_version=version,
        accepted=False,full_native_instruction_trace=False,normal_PTD_cleanup_proved=False,
        full_resource_lifetime_proved=False,full_battle_exit_accepted=False,
        formal_terminal_boundary_advanced=False,observed_graph_overlap=False,
        cleanup_process_exits=exits,WinMain_normal_return_proved=False,
        continuously_proved_no_overlap=False,all_static_contract_ranges_live_authenticated=covered,
        TLS_index_raw_identity_verified=version==2,manager_event_object_identity_verified=version==2,
        limitations=[
            'Only retained snapshots are independently checked; no complete instruction/API or continuous graph trace.',
            'Normal worker exit0 plus graph handoff does not independently observe every destructor/PTD free/TLS clear.',
            'No-input collector excludes its own submitted input; sparse mouse samples do not exclude all external input.',
            'Startup worker exit0 before WM_CLOSE is distinct from protected process status after cleanup; no normal WinMain return is proved.',
        ])
    if not covered:
        result['limitations'].append('Original startup dispatch506713..50673A and stage initialization525080 were not in this collector live range list.')
    return result


def verify_file(path,digest):
    report=owner.read_report(path,digest)
    raw=(ROOT/'analysis/hermit_game.exe').read_bytes()
    need(report['original']==dict(path='analysis/hermit_game.exe',bytes=len(raw),sha256=contract.SOURCE_SHA),
         'recorded original identity')
    expected=[]
    for relative in IMPLEMENTATIONS:
        file=ROOT/relative
        expected.append(dict(path=relative,bytes=file.stat().st_size,sha256=owner.sha(file.read_bytes())))
    need(report['implementations']==expected and report['observer']==expected[1],
         'explicit exact collector/base/adapter identities')
    need(owner.sha((ROOT/owner.APP).read_bytes())==
         '030dca584a3a0b20751a72609f7acc823e8d79d820cebf1fcde8be6a791a9df7',
         'current private original executable identity')
    parent=owner.read_report(ROOT/PARENT,PARENT_SHA)
    runtime=report['runtime'];pr=parent['runtime']
    reference=runtime['immutable_files_reference']
    need(reference==dict(path=PARENT,sha256=PARENT_SHA,rows=len(pr['immutable_files']),freshly_hashed_this_lifetime=True),
         'fixed original asset inventory reference')
    need({k:v for k,v in runtime.items() if k!='immutable_files_reference'}==
         {k:v for k,v in pr.items() if k!='immutable_files'},'exact runtime inventory metadata')
    restored=report['mutable_private_runtime_files']
    expected_paths={str(Path(pr['private_root'])/r['path']).replace('\\','/'):r['private_sha256']
                    for r in pr['private_writable_files']}
    need(len(restored)==len(expected_paths) and {r['path'] for r in restored}==set(expected_paths),
         'complete private mutable restore set')
    need(all(r['restored_exact'] is True and r['sha256']==expected_paths[r['path']] for r in restored),
         'private mutable files restored to exact source')
    row=report['probe']['TLS_implementation'];dll=Path(row['module_path'])
    need(dll.resolve()==Path('C:/Windows/SysWOW64/kernelbase.dll').resolve(),'actual x86 OS TLS module')
    module=dll.read_bytes();need(owner.sha(module)==row['module_sha256'],'OS TLS module identity')
    import pefile
    pe=pefile.PE(data=module)
    export=next(x for x in pe.DIRECTORY_ENTRY_EXPORT.symbols if x.name==b'TlsGetValue')
    need(pe.FILE_HEADER.Machine==0x14C and export.forwarder is None and export.address==row['RVA']
         and pe.get_data(export.address,64).hex()==row['code_hex'],'actual OS TLS export bytes')
    result=verify_report(report,raw)
    result.update(source_report=dict(path=str(Path(path).resolve()),bytes=Path(path).stat().st_size,sha256=digest),
                  verifier_sha256=owner.sha(Path(__file__).read_bytes()),
                  native_dependency_attestation_complete=False)
    result['current_verification_dependencies']=[dict(path=p,bytes=(ROOT/p).stat().st_size,
        sha256=owner.sha((ROOT/p).read_bytes())) for p in
        ('devtools/terminal_scene_owner_verification.py','devtools/terminal_startup_handoff_contract.py')]
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report',required=True);parser.add_argument('--sha256',required=True)
    parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    result=verify_file(args.report,args.sha256)
    with args.out.open('x',encoding='utf8') as stream:json.dump(result,stream,ensure_ascii=False,indent=2)
    print(json.dumps(dict(status=result['status'],accepted=False)))


if __name__=='__main__':main()
