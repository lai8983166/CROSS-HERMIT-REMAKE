"""Independent bounded original battle wait/result endpoint verification.

ETW returns and sampled caller frames are not a continuous instruction/state
trace. Every full ABI/state/resource/replay acceptance flag remains false.
"""
import argparse
import ctypes as C
import gzip
import hashlib
import json
from pathlib import Path
import struct
import time
import types
import uuid
from devtools import terminal_original_wait_etw_verification as original
from devtools import terminal_battle_wait_etl as etl

ROOT=Path(__file__).resolve().parents[1]
ORIGINAL_SHA='3291ca9c213d67a333b0914b175bd80ff59fcbc598bad3b2c7ff8254f912e769'
INPUT_VERIFIER_SHA='1d269d8496159b40d873db4b2e18459b4ee18159f22e4bab6b694cd7c5cf8288'
IMAGE_SHA='588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'
CODE_RANGES=((0x422360,0x422434),(0x422560,0x4225DA),(0x56CE80,0x56CE98),
             (0x4539B0,0x453CFC),(0x451A60,0x451B0F),(0x451670,0x4519A3),
             (0x496410,0x49644C),(0x4967B0,0x4968A9),(0x50A007,0x50A1E8))
WAIT_SITES=(0x453CB5,0x453CD3,0x453CDD,0x451758,0x451796)
MAX_SNAPSHOTS=768
need=original.need
blob=original.blob
word=original.word
etw=etl.frozen


def clone(function,**changes):
    return types.FunctionType(function.__code__,dict(function.__globals__,**changes),
                              function.__name__,function.__defaults__,function.__closure__)


def memory_at(regions,address,size):
    need(0<size<=716 and 0<len(regions)<=256,'bounded stack reads')
    hits=[]
    for row in regions:
        raw=bytes.fromhex(row['hex']);start=row['pointer']
        need(0<len(raw)<=716 and 0x10000<=start<0x80000000,'bounded original stack range')
        if start<=address and address+size<=start+len(raw):hits.append(raw[address-start:address-start+size])
    need(hits and all(x==hits[0] for x in hits),'complete consistent original stack bytes')
    return hits[0]


def source_contract(source,identity,diagnostic_only=False):
    need(source['kind']=='battle_wait_result_window' and source['phase'] in ('startup_preflight','battle_retreat'),
         'explicit original wait window phase')
    need(source['error'] is None and source['trace_limits']==etl.LIMITS and source['ETL_limit']==etl.ETL_LIMIT,
         'successful source with exact declared budgets')
    need(all(source['ETL'][k]==identity[k] for k in ('bytes','sha256')) and 0<identity['bytes']<etl.ETL_LIMIT,
         'same full bounded original ETL')
    subject=source['subject']
    need(all(type(subject[k])is int and 0<subject[k]<0x80000000 for k in ('pid','tid','main_tid','node','main'))
         and subject['tid']!=subject['main_tid'],'actual distinct worker and scheduler')
    t=source['trace'];need(t['start_status']==t['stop_status']==0 and t['stopped'] is True,'actual acquired/stopped ETW')
    req=etw.PROPERTIES.from_buffer_copy(blob(t['requested_properties_hex'],120,'requested trace properties'))
    need(req.EnableFlags==source['trace_flags']==0x92 and req.MaximumFileSize==64 and req.LogFileMode==1
         and req.BufferSize==64 and req.MinimumBuffers==4 and req.MaximumBuffers==8,
         'exact declared 64 MiB sequential system trace')
    st=etw.PROPERTIES.from_buffer_copy(blob(t['returned_stop_properties_hex'],120,'stopped trace properties'))
    keys=('EventsLost','LogBuffersLost','RealTimeBuffersLost','BuffersWritten','NumberOfBuffers')
    need(all(int(getattr(st,k))==t['statistics'][k] for k in keys),'raw StopTrace statistics')
    need(st.EventsLost==st.LogBuffersLost==st.RealTimeBuffersLost==0 and 0<st.BuffersWritten<=etl.MAX_BUFFERS,
         'zero reported loss and bounded nonempty ETL')
    need(source['observer_thread_duplicate_closed'] is True,'observer duplicate handle closed')
    need(source['host_game_calls']==source['host_memory_writes']==source['host_input_actions']==[],
         'window observer invokes no game function, field write or input')
    need(all(source[k] is False for k in ('source_memory_written','general_registers_written',
         'debug_registers_written','debug_object_modified','debugger_reply_substituted')),'read-only observation')
    need(source['mutable_private_runtime_files'] and all(x['restored_exact'] is True
         for x in source['mutable_private_runtime_files']),'private mutable runtime bytes restored exactly')
    interval=source['capture_interval'];before=source['before']
    need(before['snapshot_end_ns']<=interval['begin_ns']<interval['end_ns'],'real before snapshot precedes trace interval')
    rows=source['window_snapshots'];need(0<len(rows)<=MAX_SNAPSHOTS and source['maximum_snapshots']==MAX_SNAPSHOTS,
         'bounded complete window snapshot collection')
    end=interval['begin_ns']
    for row in rows:
        need(end<=row['snapshot_begin_ns']<=row['snapshot_end_ns']<=interval['end_ns'],'ordered exact captured intervals')
        end=row['snapshot_end_ns']
    return original.verify_lifecycle(source,require_crt=not diagnostic_only)


def verify_code(source,image):
    need(hashlib.sha256(image).hexdigest()==IMAGE_SHA,'fixed unpacked original executable')
    need(len(source['original_code'])==len(CODE_RANGES),'complete declared window code ranges')
    for row,(lo,hi) in zip(source['original_code'],CODE_RANGES):
        need(row['pointer']==lo and bytes.fromhex(row['hex'])==image[lo-0x400000:hi-0x400000],
             'actual original wait/result/recording instructions')


def validate_records(rows, subject, cpu_count):
    """Authenticate raw fields and CPU transitions before considering pairs."""
    need(0 < len(rows) <= etl.MAX_SELECTED, 'bounded complete selected sequence')
    pid, tid = subject['pid'], subject['tid']
    active_cpu = None; prior_index = -1; prior_ns = -1
    calls = []; pending = None; boundary_exits = []; final_pending = None
    for pos, row in enumerate(rows):
        h = blob(row['record_header_hex'], 80, 'EVENT_HEADER')
        bc = blob(row['buffer_context_hex'], 4, 'BUFFER_CONTEXT')
        raw = bytes.fromhex(row['payload_hex'])
        need(len(raw) <= 512, 'bounded complete selected payload')
        need(etw.filetime_ns(struct.unpack_from('<q', h, 16)[0]) == row['ns'], 'raw record timestamp')
        need(h[45] == row['opcode'] and str(uuid.UUID(bytes_le=h[24:40])) == row['guid'], 'raw event identity')
        need(struct.unpack_from('<II', h, 8) == (row['tid'], row['pid']), 'raw owner IDs')
        flags = struct.unpack_from('<H', h, 4)[0]
        cpu = struct.unpack_from('<H', bc)[0] if flags & 0x200 else bc[0]
        need(cpu == row['cpu'] and 0 <= cpu < cpu_count and type(row['index']) is int and row['index'] > prior_index
             and row['ns'] >= prior_ns, 'complete monotonic raw CPU sequence')
        prior_index, prior_ns = row['index'], row['ns']; op = row['opcode']
        if op == 36:
            need(row['guid'] == etw.THREAD_GUID and len(raw) >= 8, 'raw CSwitch class/payload')
            new, old = struct.unpack_from('<II', raw)
            need((new, old) == (row['data']['NewThreadId'], row['data']['OldThreadId'])
                 and row['decoder_cpu_tid_before'] == old, 'full-reader CPU attribution agrees with CSwitch bytes')
            need(tid in (new, old) and new != old, 'actual target CPU transition')
            if old == tid:
                need(active_cpu == cpu, 'target switched off its actual CPU')
                active_cpu = None
            if new == tid:
                need(active_cpu is None, 'target not simultaneously running on another CPU')
                active_cpu = cpu
        else:
            need(row['guid'] == etw.PERF_GUID and op in (51, 52) and active_cpu == cpu
                 and row['decoder_cpu_tid_before'] == tid, 'syscall attributed by full CPU flow')
            need(row['tid'] in (tid, 0xffffffff) and row['pid'] in (pid, 0xffffffff), 'no conflicting raw owner')
            if op == 51:
                need(len(raw) == (8 if flags & 0x40 else 4)
                     and int.from_bytes(raw, 'little') == row['data']['SysCallAddress'], 'raw syscall address')
                need(pending is None, 'overlapping target syscalls; no inferred nesting or discarded entry')
                pending = pos
            else:
                need(len(raw) == 4 and int.from_bytes(raw, 'little') == row['data']['SysCallNtStatus'], 'raw NTSTATUS')
                if pending is None:
                    need(not calls and not boundary_exits, 'unmatched syscall exit inside retained sequence')
                    boundary_exits.append(pos)  # Only the trace's initial partial call; never a candidate.
                else:
                    calls.append((pending, pos)); pending = None
    if pending is not None:
        final_pending = pending  # Trace may stop during a later wait; this is never selected.
    return calls, dict(initial_unpaired_exits=boundary_exits, final_unpaired_entry=final_pending,
                       closed_calls=len(calls), full_global_pairing=not boundary_exits and final_pending is None)


def snapshot_contract(source,snap,baseline,image):
    """One actual live snapshot. No invented after state or copied timestamp."""
    sub=source['subject'];node=sub['node'];pid=sub['pid'];tid=sub['tid']
    frame=snap['frame'];context=blob(frame['context_hex'],716,'worker WOW64 context')
    need(snap['node_pointer']==node and snap['manager_pointer']==sub['main']+0x64,'current task and scheduler')
    head=blob(snap['node_hex'],64,'live node');manager=blob(snap['manager_hex'],0x120,'live manager')
    need(word(head,8)==snap['manager_pointer'] and word(head,0x24)==tid and word(head,0x1c) and word(head,0x20),
         'actual node thread/event/backpointer')
    need(word(head)==(0x59a430 if source['phase']=='battle_retreat' else 0x5caa48),'actual original scene type')
    need(snap['source_memory_written'] is False and snap['debug_registers_written'] is False,'read-only snapshot')
    for role,expected_tid in (('frame',tid),('scheduler_frame',sub['main_tid'])):
        f=snap[role];raw=blob(f['context_hex'],716,'actual current context')
        need(f['tid']==expected_tid and f['owner_verified_before_suspend'] is True
             and type(f['previous_suspend_count'])is int and f['previous_suspend_count']>=0,'same-handle owner before suspension')
        need((f['EIP'],f['ESP'],f['EBP'])==(word(raw,184),word(raw,196),word(raw,180)),'raw current registers')
    original.verify_current_tls(snap['current_TLS'],context,baseline['current_TLS'],node,pid,tid)
    for offset in (0,8,0x18,0x1c,0x20,0x24):
        need(word(head,offset)==word(bytes.fromhex(baseline['node_hex']),offset),'same actual task lifetime')
    need(word(manager,0x118)==word(bytes.fromhex(baseline['manager_hex']),0x118)!=0,'same actual scheduler event')
    chain=frame['chain'];regions=snap['stack_regions']
    need(0<len(chain)<=100 and chain[0]['bp']==frame['EBP'],'actual frame-chain start')
    for i,row in enumerate(chain):
        need(struct.unpack('<II',memory_at(regions,row['bp'],8))==(row['saved_bp'],row['return_va']),'raw original frame links')
        if i+1<len(chain):need(row['saved_bp']==chain[i+1]['bp'] and row['bp']<row['saved_bp']<row['bp']+0x100000,'continuous actual frame chain')
    def unique(va,required=True):
        candidates=[x for x in chain if x['return_va']==va]
        need(len(candidates)==1 if required else len(candidates)<=1,'unique raw ancestor '+hex(va))
        return candidates[0] if candidates else None
    api=unique(0x42240d);callback=unique(0x421f8a);worker=unique(0x56e183)
    need(struct.unpack('<IIII',memory_at(regions,api['bp'],16))==
         (api['saved_bp'],0x42240d,word(head,0x1c),0xffffffff),'actual original Win32 wait parameters')
    wait_bp=api['saved_bp'];wait_rows=[x for x in chain if x['bp']==wait_bp]
    need(len(wait_rows)==1,'actual 422360 frame follows Win32 caller')
    wait=wait_rows[0];site=wait['return_va'];call=image[site-5-0x400000:site-0x400000]
    need(len(call)==5 and call[0]==0xe8 and site+struct.unpack_from('<i',call,1)[0]==0x422360,'actual original immediate wait callsite')
    need(any(lo<=site-5<site<=hi for lo,hi in CODE_RANGES),'live captured caller code range')
    need(struct.unpack('<II',memory_at(regions,wait_bp-8,8))==(snap['manager_pointer'],node)
         and word(memory_at(regions,wait_bp+8,4))==0 and word(head,4)&0x10000,'original wait locals, zero delay and set flag')
    tls=snap['current_TLS'];ptrs=dict(worker_argument=worker['bp']+8,wrapper_argument=worker['saved_bp']+8,
        callback_this=callback['bp']-4,callback_argument=callback['bp']+8,node_argument=node+0x18)
    vals={}
    for key,pointer in ptrs.items():
        r=tls['ancestry_memory'][key];need(r['pointer']==pointer,'actual original CRT ancestry address')
        vals[key]=word(blob(r['hex'],4,'actual original ancestor argument'));need(vals[key]==tls['ancestry'][key],'raw ancestry value')
    need(vals['worker_argument']==vals['callback_this']==node and vals['wrapper_argument']==tls['PTD']
         and vals['callback_argument']==vals['node_argument']==word(head,0x18),'same current CRT callback lifetime')
    registered=snap['registered_nodes'];seen=set();found=False
    for bucket in range(32):
        pointer=word(manager,bucket*8)
        while pointer:
            need(pointer not in seen and len(seen)<32,'acyclic current scheduler graph');seen.add(pointer)
            candidates=[x for x in registered if x['pointer']==pointer]
            need(len(candidates)==1 and candidates[0]['bucket']==bucket,'complete current registration graph')
            raw=blob(candidates[0]['head_hex'],48,'registered node')
            need(word(raw,8)==snap['manager_pointer'],'registered manager backpointer')
            if pointer==node:need(raw==head[:48],'same live registered node');found=True
            pointer=word(raw,12)
    need(found and len(seen)==len(registered),'actual node remains registered')
    result=dict(wait_return_site=site,wait_frame_bp=wait_bp,caller_frame_bp=wait['saved_bp'],
        snapshot_interval=[snap['snapshot_begin_ns'],snap['snapshot_end_ns']],result_locals={},
        Nt_context=None,supported_Nt_context=False)
    entry=next(x for x in source['API_exports'] if x['name']=='NtWaitForSingleObject')
    if frame['EIP']==entry['target']+12:
        # The shared API PE check runs once before snapshots. Only actual raw
        # stack/context interpretation is repeated, not PE file work per sample.
        result['Nt_context']=clone(original.verify_Nt_wait_stack,memory_at=memory_at)(
            dict(source,owner_snapshots={'observed_wait':snap}),entry,bytes.fromhex(entry['entry_hex']))
        result['supported_Nt_context']=True
    else:
        result['unsupported_reason']='Raw waiting caller exists but current EIP is not the authenticated NtWait return PC; no ETW pair assigned.'
    if source['phase']=='battle_retreat':
        need(site in WAIT_SITES,'known original battle wait callsite')
        scene=blob(snap['scene_head_hex'],0x200,'live battle scene')
        need(scene[:64]==head,'same battle scene/header')
        back=snap['controller_backpointer'];gate=snap['recording_gate']
        need(back['pointer']==node+0x190+0x117c38 and word(blob(back['hex'],4,'controller scene backpointer'))==node,'controller actual scene owner')
        need(gate['pointer']==node+0x190+0x117c3c,'actual recording gate address')
        gate_raw=blob(gate['hex'],1,'actual recording gate')
        result.update(retreat_flag=head[0x31],recording_gate_signed=struct.unpack('<b',gate_raw)[0],recording_effects_verified=False)
        for va,name,offset in ((0x451abc,'inner_result',8),(0x451716,'dispatcher_result',8),(0x421f8a,'callback_result',12)):
            f=unique(va,False)
            if f:
                need(word(memory_at(regions,f['bp']-4,4))==node,'actual original scene receiver')
                result['result_locals'][name]=word(memory_at(regions,f['bp']-offset,4))
        if site in (0x453cb5,0x453cd3,0x453cdd):
            need(unique(0x451abc)['bp']==wait['saved_bp'],'scene-loop is actual wait caller')
            if site!=0x453cb5:need(result['result_locals']['inner_result']!=0,'actual post-result scene local remains nonzero')
        else:
            need(callback['bp']==wait['saved_bp'] and result['result_locals']['callback_result']!=0,'callback actually consumed nonzero result')
            count=word(memory_at(regions,callback['bp']-8,4));result['tail_counter']=count
            need(0<=count<10 if site==0x451758 else count==10,'actual original tail loop count')
    return result


def verify_receipt(source,rows,receipt):
    need(receipt['process_trace_status']==receipt['close_trace_status']==0 and receipt['callback_errors']==[],
         'complete offline native decode and owned reader close')
    need(receipt['retained_subject_records']==len(rows) and 0<len(rows)<=etl.MAX_SELECTED
         and len(rows)<=receipt['total_records']<=etl.EVENT_LIMIT,'complete bounded target sequence')
    header=receipt['ETL_header'];etl.validate_log_header(header,source)
    actual=etw.LOG_HEADER.from_buffer_copy(blob(receipt['ETL_header_raw_hex'],280,'ETL header'))
    need(all(int(getattr(actual,k))==value for k,value in header.items()),'raw ETL header scalars')
    need(receipt['buffer_reads']==list(range(1,header['BuffersWritten']+1)),'all original ETL buffers consumed in order')
    first=blob(receipt['first_record']['header_hex'],80,'first native record')
    need(struct.unpack_from('<q',first,16)[0]==receipt['first_record']['FILETIME']==header['StartTime'],
         'exact original first FILETIME without clock calibration')
    bindings=receipt['subject_thread_bindings'];need(0<len(bindings)<=16,'actual subject thread lifetime bindings')
    sub=source['subject'];begin=min(x['snapshot_begin_ns'] for x in source['window_snapshots'])
    end=max(x['snapshot_end_ns'] for x in source['window_snapshots']);birth=False
    for row in bindings:
        h=blob(row['header_hex'],80,'actual lifetime header');raw=bytes.fromhex(row['payload_hex'])
        need(row['opcode'] in (1,2,3,4) and h[45]==row['opcode']
             and str(uuid.UUID(bytes_le=h[24:40]))==etw.THREAD_GUID,'raw thread lifetime class')
        need(len(raw)>=8 and struct.unpack_from('<II',raw)==(row['pid'],row['tid'])==(sub['pid'],sub['tid']),
             'raw ETL subject PID/TID binding')
        need(etw.filetime_ns(struct.unpack_from('<q',h,16)[0])==row['ns'],'raw lifetime timestamp')
        need(row['schema']['provider_guid']==etw.SYSTEM_GUID and row['schema']['event_guid']==etw.THREAD_GUID,
             'actual lifetime TDH schema')
        if row['opcode'] in (1,3):need(row['ns']<=begin,'initial binding precedes observed waits');birth=True
        else:need(row['ns']>=end,'lifetime does not end before actual owner samples')
    need(birth,'actual initial PID/TID binding')


def pair_snapshots(source,rows,proofs):
    pairs,ledger=validate_records(rows,source['subject'],source['input_isolation']['current_guest_resources']['logical_processors'])
    groups={};boundaries=[];unsupported=[]
    for index,proof in enumerate(proofs):
        if not proof['supported_Nt_context']:
            unsupported.append(dict(snapshot_index=index,reason=proof['unsupported_reason']));continue
        lo,hi=proof['snapshot_interval']
        found=[(a,b) for a,b in pairs if rows[a]['ns']<lo<=hi<rows[b]['ns']]
        if not found:
            initial=ledger['initial_unpaired_exits'];final=ledger['final_unpaired_entry']
            boundary=('initial_partial' if initial and hi<rows[initial[0]]['ns'] else
                      'final_partial' if final is not None and rows[final]['ns']<lo else None)
            need(boundary is not None,'sampled Nt wait has no complete unique ETW pair or explicit trace-boundary explanation')
            boundaries.append(dict(snapshot_index=index,reason=boundary,wait_return_site=proof['wait_return_site']));continue
        need(len(found)==1,'one original syscall contains the entire actual paused snapshot')
        a,b=found[0]
        need(rows[a]['data']['SysCallAddress']==source['kernel_wait_export']['target']
             and rows[b]['data']['SysCallNtStatus']==0,'actual successful kernel NtWaitForSingleObject')
        switches=rows[a+1:b];need(all(x['opcode']==36 for x in switches),'no discarded inside-wait syscall event')
        off=[]
        for left,right in zip(switches,switches[1:]):
            if left['data']['OldThreadId']==source['subject']['tid'] and right['data']['NewThreadId']==source['subject']['tid']:
                if left['ns']<lo<=hi<right['ns']:off.append([left['index'],right['index']])
        need(len(off)==1,'actual complete snapshot strictly inside one target switch-out interval')
        semantic={k:proof.get(k) for k in ('wait_return_site','wait_frame_bp','caller_frame_bp','result_locals','tail_counter')}
        if (a,b) not in groups:
            groups[(a,b)]=dict(selected_indices=[a,b],global_indices=[rows[a]['index'],rows[b]['index']],
                interval_ns=[rows[a]['ns'],rows[b]['ns']],NTSTATUS=0,syscall_address=rows[a]['data']['SysCallAddress'],
                semantic=semantic,snapshot_indices=[],switched_out_intervals=[],recording_gate_samples=[])
        group=groups[(a,b)]
        need(group['semantic']==semantic,'same pending syscall cannot change original frame/result identity between samples')
        group['snapshot_indices'].append(index);group['switched_out_intervals'].append(off[0])
        if 'recording_gate_signed' in proof:group['recording_gate_samples'].append(proof['recording_gate_signed'])
    ordered=[groups[key] for key in sorted(groups)]
    need(len(ordered)>=3 if source['phase']=='startup_preflight' else bool(ordered),
         'at least three distinct successful preflight waits or one actual battle wait required')
    return ordered,ledger,boundaries,unsupported


def endpoint_coverage(groups):
    """Report observed points, never infer unobserved waits from source branches."""
    sites={site:[] for site in WAIT_SITES};tail={};callback=[]
    for i,g in enumerate(groups):
        sem=g['semantic'];site=sem['wait_return_site'];values=sem['result_locals']
        if site in sites:sites[site].append(i)
        if site==0x451758:
            count=sem['tail_counter'];need(count not in tail,'same original tail count cannot identify two different successful waits')
            tail[count]=i
        if site in (0x451758,0x451796) and values.get('callback_result')==1:callback.append(i)
    terminal=[i for i in sites[0x453cb5] if groups[i]['semantic']['result_locals'].get('inner_result',0)!=0]
    triples=[(a,b,c) for a in terminal for b in sites[0x453cd3] for c in sites[0x453cdd] if a<b<c]
    ten=sorted(tail)==list(range(10)) and [tail[k] for k in range(10)]==sorted(tail.values())
    return dict(observed_sites={hex(k):v for k,v in sites.items()},post_result_three_wait_endpoints_observed=bool(triples),
        callback_nonzero_consumption_endpoint_observed=bool(callback),
        ten_distinct_tail_waits_observed=ten,observed_tail_counters=sorted(tail),
        completion_gate_wait_observed=bool(sites[0x451796]),recording_call_execution_verified=False,
        recording_file_effects_verified=False,continuous_instruction_result_consumption_verified=False)


def input_verifier():
    from devtools import terminal_school_handoff_verification as school
    need(hashlib.sha256(Path(school.__file__).read_bytes()).hexdigest()==INPUT_VERIFIER_SHA,
         'unchanged independent input/qualification verifier')
    return school


def verify_input_reference(source,school_path,image):
    if source['phase']=='startup_preflight':return dict(input_required=False,input_transition_claimed=False)
    school=input_verifier();expected=source['school_source_reference'];path=Path(school_path)
    actual=etw.identity(path);need(all(actual[k]==expected[k] for k in ('bytes','sha256')),'exact once-retained full school source')
    need(0<actual['bytes']<=24*1024*1024,'bounded compressed school history')
    with gzip.open(path,'rb') as f:raw=f.read(192*1024*1024+1)
    need(len(raw)<=192*1024*1024,'bounded expanded school history')
    report=json.loads(raw);reference=source['input_receipt'];index=reference['object_path']
    need(index[:2]==['probe','battle_inputs'] and len(index)==3 and type(index[2])is int and index[2]>=0,
         'exact original battle action object path')
    need(all(reference['source'][k]==actual[k] for k in ('bytes','sha256')),'same referenced input source')
    record=report['probe']['battle_inputs'][index[2]]
    raw_record=json.dumps(record,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
    canonical=reference['canonical']
    need(len(raw_record)==canonical['bytes'] and hashlib.sha256(raw_record).hexdigest()==canonical['sha256'],
         'exact original action canonical bytes')
    need(canonical['encoding']=='UTF-8 JSON sort_keys=True,separators=(comma,colon),ensure_ascii=False', 'explicit canonical encoding')
    need(record['stage']=='confirmation' and record['error'] is None and reference['error'] is None,
         'one successful original retreat confirmation')
    action=record['action'];down=action['down_wall_time_ns'];up=action['up_wall_time_ns']
    need((reference['down_wall_time_ns'],reference['up_wall_time_ns'])==(down,up)
         and reference['released'] is action['released'] is True,'actual original mouse release receipt')
    need(source['start_trigger']=='second_left_button_down_query' and source['start_trigger_ns']<=source['capture_interval']['begin_ns']<=down<up,
         'original final-query trace begins before actual down/up')
    probe=report['probe'];ready=report['lifecycle']['ready'];sub=source['subject']
    need(probe['pid']==sub['pid'] and probe['main']==sub['main'] and source['lifecycle']==report['lifecycle'],
         'same original whole-school lifetime')
    isolation=school.verify_input_isolation(report['input_isolation'])
    viewed,focus=school.guest_focus_view(report,isolation,sub['pid'],ready['window']['hwnd'])
    probe=viewed['probe'];receipt=probe['battle_inputs'][index[2]]
    workers={(w['pointer'],w['thread_id']):w for w in probe['workers']}
    result=school.verify_mouse_action(receipt,'retreat_confirmation',probe,image,ready['game']['pointer'],
        ready['window']['hwnd'],workers,check_disk=False)
    need(result['input_edges_observed'] is True and (result['node'],result['thread_id'])==(sub['node'],sub['tid']),
         'same battle original press/held/release edge proven')
    return dict(input_required=True,source=actual,canonical=canonical,object_path=index,
        actual_input_edges_verified=True,down_ns=down,up_ns=up,
        native_result_inferred_from_input=False,full_school_history_independently_replayed=False)


def verify(source,rows,receipt,image,kernel_image,module_loader,diagnostic_only=False,school_path=None):
    lifecycle=source_contract(source,receipt['ETL'],diagnostic_only)
    verify_code(source,image);verify_receipt(source,rows,receipt)
    qualification=input_verifier().verify_input_isolation(source['input_isolation'])
    kernel=original.verify_kernel_export(source,kernel_image)
    api=original.verify_api_exports(source,module_loader);tls=original.verify_tls_implementation(source,module_loader)
    baseline=source['before'];before=snapshot_contract(source,baseline,baseline,image)
    for name,handle in (('node_event',word(bytes.fromhex(baseline['node_hex']),0x1c)),
                        ('manager_event',word(bytes.fromhex(baseline['manager_hex']),0x118))):
        event=source['event_owners'][name]
        need(event['owner_pid']==source['subject']['pid'] and event['remote_handle']==handle and event['duplicate_succeeded'] is True
             and event['query_status']==0 and event['type_name']=='Event' and event['wait_or_signal_called'] is False,'actual same-owner Event queries')
    proofs=[snapshot_contract(source,x,baseline,image) for x in source['window_snapshots']]
    groups,ledger,boundaries,unsupported=pair_snapshots(source,rows,proofs)
    inputs=verify_input_reference(source,school_path,image)
    worker_exit=source.get('worker_exit')
    if worker_exit:
        need(worker_exit['code']==worker_exit['wait_status']==0 and worker_exit['before_WM_CLOSE'] is True
             and worker_exit['duplicate_handle_query_only'] is True and worker_exit['PTDcleanup'] is False,
             'separate actual original worker exit query receipt')
        need(worker_exit['observed_ns']>=max(x['snapshot_end_ns'] for x in source['window_snapshots']),
             'worker exit after all live owner snapshots')
    return dict(scope='bounded original wait and sampled result endpoints; not continuous instruction/state proof',
        phase=source['phase'],accepted=False,fullABI=False,fullstate=False,PTDcleanup=False,
        full_instruction_trace=False,full_resource_lifetime_proved=False,independent_full_replay=False,
        two_fresh_full_native_cases_verified=False,result_consumption_proved=False,
        diagnostic_only=diagnostic_only,source_cleanup=lifecycle,qualification=qualification,
        kernel=kernel,API_exports=api,TLS_implementation=tls,input_reference=inputs,
        snapshots_checked=len(proofs),distinct_successful_waits=len(groups),waits=groups,
        boundary_ledger=ledger,unpaired_boundary_snapshots=boundaries,unsupported_Nt_snapshots=unsupported,
        first_Nt_context=next(p['Nt_context'] for p in proofs if p['supported_Nt_context']),
        result_endpoints=endpoint_coverage(groups),worker_exit_query=worker_exit,
        limits=['ETW and sparse snapshots do not establish a continuous original instruction stream or complete CPU/RAM/ABI.',
                'Each counted wait has its own complete pair and actual original owner/Nt stack snapshot; duplicate samples count once.',
                'Unpaired trace boundaries are explicit and never promoted to successful waits; no intermediate overlap is ignored.',
                'Recording gate samples do not establish 4967B0 execution or exact replay file side effects.',
                'Actual worker exit or menu observation is not PTD/TLS/event/thread-handle cleanup proof.'])


def producer_identities(source):
    rows=source['window_implementations'];need(3<=len(rows)<=16,'bounded actual window implementation list')
    seen=set()
    for row in rows:
        name=Path(row['path']).name;need(name not in seen,'unique actual producer module');seen.add(name)
        actual=etw.identity(ROOT/'devtools'/name)
        need(all(actual[k]==row[k] for k in ('bytes','sha256')),'current code matches actual window producer '+name)
    need({'terminal_battle_wait_window.py','terminal_original_wait_etw.py','terminal_wait_etw_probe.py'}<=seen,
         'actual window and frozen native/ETW layers recorded')
    return rows


def decode_source(source_path,source_sha,etl_path,etl_sha,out,diagnostic_only=False,school_path=None):
    begun=time.monotonic();qualification=etw.qualify()
    source_path=Path(source_path).resolve();etl_path=Path(etl_path).resolve();out=Path(out).resolve()
    records_path=out.with_suffix('.records.json.gz')
    need(out.parent==ROOT/'analysis' and out.suffix=='.json' and not out.exists() and not records_path.exists(),
         'fresh bounded guest offline outputs')
    paths=[Path(__file__),Path(etl.__file__),Path(original.__file__),Path(etw.__file__),
           ROOT/'devtools/terminal_school_handoff_verification.py']
    identities=[etw.identity(p) for p in paths]
    result=dict(kind='battle_wait_result_window_decode',status='blocked',phase=None,accepted=False,
        long_capture_preflight_passed=False,diagnostic_only=diagnostic_only,new_native_capture=False,
        fullABI=False,fullstate=False,PTDcleanup=False,full_instruction_trace=False,
        full_resource_lifetime_proved=False,result_consumption_proved=False,
        qualification=qualification,implementations=identities,trace_limits=etl.LIMITS,errors=[])
    selected=[]
    try:
        need(identities[2]['sha256']==ORIGINAL_SHA and identities[3]['sha256']==etl.FROZEN_READER_SHA
             and identities[4]['sha256']==INPUT_VERIFIER_SHA,'exact frozen verification dependencies')
        need(0<source_path.stat().st_size<=etl.SOURCE_GZIP_LIMIT and 0<etl_path.stat().st_size<etl.ETL_LIMIT,
             'bounded original source and full ETL files')
        result['source']=etw.identity(source_path);result['ETL']=etw.identity(etl_path)
        need(result['source']['sha256']==source_sha and result['ETL']['sha256']==etl_sha,'explicit original source/ETL SHA')
        with gzip.open(source_path,'rb') as f:raw=f.read(etl.SOURCE_EXPANDED_LIMIT+1)
        need(len(raw)<=etl.SOURCE_EXPANDED_LIMIT,'bounded complete expanded window source')
        source=json.loads(raw);result['phase']=source['phase']
        result['source_cleanup']=source_contract(source,result['ETL'],diagnostic_only)
        result['window_implementations']=producer_identities(source)
        def consume(rows):
            selected.extend(rows)
            return dict(scope='raw selected original target records; no inferred result or helper fixture')
        etl.decode_etl(etl_path,source,result,begun+etl.DECODE_SECONDS,consume)
        artifact=dict(schema_version=1,source=result['source'],ETL=result['ETL'],subject=source['subject'],
            phase=source['phase'],scope=result['retained_sequence_scope'],records=selected)
        packed=gzip.compress(json.dumps(artifact,separators=(',',':')).encode(),mtime=0)
        need(len(packed)<=etl.SELECTED_GZIP_LIMIT,'all selected records within 512 KiB gzip cap; never truncate')
        with records_path.open('xb') as f:f.write(packed)
        result['selected_records']=etw.identity(records_path)
        if source['phase']=='battle_retreat' and school_path is None:
            school_path=Path(source['school_source_reference']['path'])
        result['analysis']=verify(source,selected,result,(ROOT/'analysis/hermit_game.exe').read_bytes(),
            Path(source['kernel_wait_export']['module']['path']).read_bytes(),
            lambda row:Path(row['module_path']).read_bytes(),diagnostic_only,school_path)
        need(etw.identity(source_path)==result['source'] and etw.identity(etl_path)==result['ETL'],'raw source files remained unchanged')
        need(producer_identities(source)==result['window_implementations'],'window implementation identity remained unchanged')
        current=all(source['input_isolation'][k]==qualification[k] for k in
                    ('current_guest_uuid','current_guest_boot_utc','current_guest_resources'))
        result['same_current_guest_boot_and_resources']=current
        result['long_capture_preflight_passed']=(source['phase']=='startup_preflight'
            and result['analysis']['distinct_successful_waits']>=3 and current)
        result['status']=('diagnostic_wait_window_observed_cleanup_unproven' if diagnostic_only
            and not result['source_cleanup']['strict_source_cleanup_verified'] else
            'diagnostic_wait_window_observed' if diagnostic_only else 'wait_window_observed')
    except Exception as exc:
        result['errors'].append(repr(exc));result['long_capture_preflight_passed']=False
    finally:
        result['elapsed_seconds']=time.monotonic()-begun
        result['implementations_after']=[etw.identity(p) for p in paths]
        if result['implementations_after']!=identities:
            result['errors'].append('decoder or dependency implementation changed');result['status']='blocked'
        if result['elapsed_seconds']>etl.DECODE_SECONDS:
            result['errors'].append('bounded offline decode deadline exceeded');result['status']='blocked'
        if result['errors']:result['long_capture_preflight_passed']=False
        raw=json.dumps(result,ensure_ascii=False,indent=2).encode()
        need(len(raw)<=512*1024,'bounded 512 KiB result summary; full raw records stored separately')
        with out.open('xb') as f:f.write(raw+b'\n')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True);p.add_argument('--source-sha',required=True)
    p.add_argument('--etl',type=Path,required=True);p.add_argument('--etl-sha',required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--diagnostic-only',action='store_true')
    p.add_argument('--school-source',type=Path)
    a=p.parse_args();r=decode_source(a.source,a.source_sha,a.etl,a.etl_sha,a.out,a.diagnostic_only,a.school_source)
    print(json.dumps(dict(status=r['status'],errors=r['errors'],accepted=False,
        long_capture_preflight_passed=r['long_capture_preflight_passed'])))
    raise SystemExit(0 if r['status']=='wait_window_observed' else 2 if r['status'].startswith('diagnostic_') else 1)
