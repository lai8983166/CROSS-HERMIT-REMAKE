"""Compare raw QPC and converted UTC against exact same-thread wait records.

No timestamp calibration, tolerance, source rewrite, or discarded middle record.
Successful individual waits retain the original one-switch-out requirement; this
diagnosis cannot establish continuous state/ABI or resource/PTD cleanup.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import struct
from devtools import terminal_battle_wait_verification_v4 as v

ROOT=Path(__file__).resolve().parents[1]
need=v.need


def packed(path,limit):
    need(Path(path).stat().st_size<=2*1024*1024,'bounded packed records')
    with gzip.open(path,'rb')as f:raw=f.read(limit+1)
    need(len(raw)<=limit,'bounded expanded records');return json.loads(raw)


def bind_raw(utc,raw):
    need(len(utc)==len(raw)>0,'same complete selected event count')
    prior=-1
    for left,right in zip(utc,raw):
        need(set(right)==(set(left)-{'ns'})|{'qpc_ticks'},'only timestamp coordinate differs')
        for key in set(left)-{'ns','record_header_hex'}:need(left[key]==right[key],'same original event field '+key)
        a=bytearray.fromhex(left['record_header_hex']);b=bytearray.fromhex(right['record_header_hex'])
        need(len(a)==len(b)==80,'two exact native EVENT_HEADERs')
        ticks=struct.unpack_from('<q',b,16)[0]
        need(type(right['qpc_ticks'])is int and ticks==right['qpc_ticks']and ticks>0 and ticks>=prior,'monotonic actual raw QPC')
        prior=ticks;a[16:24]=b'\0'*8;b[16:24]=b'\0'*8
        need(a==b,'raw and converted headers differ only by timestamp')


def bind_reader_artifact(source,source_id,report,artifact):
    for key,expected in (('source',source_id),('ETL',source['ETL'])):
        need(all(report[key][k]==expected[k]and artifact[key][k]==expected[k]
                 for k in ('bytes','sha256')),'reader and retained records bind exact '+key)
    need(artifact['subject']==source['subject'],'retained raw records identify same subject')
    rows=artifact['records']
    need(isinstance(rows,list)and type(report['retained_subject_records'])is int
         and type(report['total_records'])is int
         and 0<len(rows)<=v.etl.MAX_SELECTED and report['retained_subject_records']==len(rows)
         and len(rows)<=report['total_records']<=v.etl.EVENT_LIMIT,'complete reader subject count')


def interval_check(rows,pair,tid,lo,hi,key,margin=0):
    a,b=pair
    if not rows[a][key]+margin<lo<=hi<rows[b][key]-margin:return False
    switches=[i for i in range(a+1,b)if rows[i]['opcode']==36]
    intervals=[(x,y)for x,y in zip(switches,switches[1:])if rows[x]['data']['OldThreadId']==tid and rows[y]['data']['NewThreadId']==tid]
    return sum(rows[x][key]+margin<lo<=hi<rows[y][key]-margin for x,y in intervals)==1


def compare(source,utc,raw,pairs,proofs):
    bind_raw(utc,raw);out=[];tid=source['subject']['tid'];semantics={}
    need(len(source['window_snapshots'])==len(proofs)>0,'every original snapshot has one checked proof')
    for index,(snap,proof)in enumerate(zip(source['window_snapshots'],proofs)):
        timing=snap['timing_diagnostic'];reads=timing['clock_reads'];lo,hi=timing['data_interval_qpc']
        need(len(reads)==2 and all(type(r[k])is int and r[k]>0 for r in reads
             for k in ('qpc_before','qpc_after','UTC_ns')),'actual integer QPC and UTC readings')
        need(type(snap['snapshot_begin_ns'])is int and type(snap['snapshot_end_ns'])is int
             and snap['snapshot_begin_ns']<=snap['snapshot_end_ns'],'ordered integer UTC snapshot times')
        need(len(reads)==2 and [r['UTC_ns']for r in reads]==[snap['snapshot_begin_ns'],snap['snapshot_end_ns']], 'same original two UTC readings')
        need(lo==reads[0]['qpc_before']<=reads[0]['qpc_after']<=reads[1]['qpc_before']<=reads[1]['qpc_after']==hi,
             'actual QPC bracket covers both UTC readings and all original data reads')
        need(timing['includes_original_context_acquisition']is False,'context acquisition is separately disclosed')
        need(timing['context_acquired_while_same_handles_suspended']is True,'actual held context acquisition disclosed')
        need(type(lo)is int and type(hi)is int and 0<lo<=hi,'positive actual data interval')
        calls=timing['TLS_calls'];need(len(calls)==1,'one actual complete TLS observation')
        call=calls[0];selector=call['selector_query']
        need(all(type(x[k])is int and x[k]>0 for x in (call,selector)for k in ('qpc_begin','qpc_end'))
             and type(selector['result'])is int and 0<selector['result']<=0xffffffff,
             'actual integer TLS/selector timing and result')
        need(call['completed']is True and
             lo<=call['qpc_begin']<=selector['qpc_begin']<=selector['qpc_end']<=call['qpc_end']<=hi,
             'successful original TLS/selector timing lies inside captured data interval')
        candidates=[pair for pair in pairs if raw[pair[0]]['qpc_ticks']<lo<=hi<raw[pair[1]]['qpc_ticks']]
        item=dict(snapshot_index=index,QPC_data_interval=[lo,hi],UTC_data_interval=[snap['snapshot_begin_ns'],snap['snapshot_end_ns']],
            actual_Nt_context=proof['supported_Nt_context'],raw_QPC_strict_single_off_interval=False,converted_UTC_strict_single_off_interval=False)
        if proof['supported_Nt_context']and len(candidates)==1:
            pair=candidates[0];a,b=pair
            need(utc[a]['data']['SysCallAddress']==source['kernel_wait_export']['target']and utc[b]['data']['SysCallNtStatus']==0,'same actual NtWait with successful raw exit')
            semantic={k:proof.get(k)for k in ('wait_return_site','wait_frame_bp','caller_frame_bp','result_locals','tail_counter')}
            need(pair not in semantics or semantics[pair]==semantic,'same pending syscall keeps original frame and result identity')
            semantics[pair]=semantic
            item.update(global_syscall_pair=[utc[a]['index'],utc[b]['index']],
                raw_QPC_strict_single_off_interval=interval_check(raw,pair,tid,lo,hi,'qpc_ticks',1),
                converted_UTC_strict_single_off_interval=interval_check(utc,pair,tid,snap['snapshot_begin_ns'],snap['snapshot_end_ns'],'ns'))
        item['raw_QPC_switches_inside_data_interval']=[r['index']for r in raw if r['opcode']==36 and lo<=r['qpc_ticks']<=hi]
        # Allocator bytes already exist in the SHA-bound source. Keep timing
        # and an exact content reference, not hundreds of duplicate raw copies.
        item['TLS_observation_intervals']=[dict(
            {k:value for k,value in call.items()if k!='allocator_observation'},
            allocator_observation_sha256=hashlib.sha256(json.dumps(call.get('allocator_observation'),sort_keys=True,separators=(',',':')).encode()).hexdigest())
            for call in timing['TLS_calls']]
        out.append(item)
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('source','source-sha','utc-report','utc-sha','raw-report','raw-sha','out'):p.add_argument('--'+name,required=True)
    a=p.parse_args();out=Path(a.out);need(not out.exists(),'new clock comparison report')
    dependencies=[Path(__file__),Path(v.__file__),Path(v.v3.__file__),Path(v.v2.__file__),Path(v.v1.__file__),Path(v.original.__file__),Path(v.etw.__file__),Path(v.etl.__file__),Path(v.etl.parent.__file__)]
    implementations=[v.etw.identity(p)for p in dependencies]
    refs=[]
    for path,sha in ((a.source,a.source_sha),(a.utc_report,a.utc_sha),(a.raw_report,a.raw_sha)):
        row=v.etw.identity(Path(path));need(row['sha256']==sha and row['bytes']<=2*1024*1024,'explicit retained artifact SHA');refs.append(row)
    source=packed(a.source,8*1024*1024);ur=json.loads(Path(a.utc_report).read_text());rr=json.loads(Path(a.raw_report).read_text())
    sequences=[]
    for report,path in ((ur,a.utc_report),(rr,a.raw_report)):
        need(not report['callback_errors']and report['process_trace_status']==report['close_trace_status']==0,'complete successful native reader')
        need(report['implementations']==report['implementations_after'],'reader implementation unchanged during execution')
        need(all(report['source'][k]==refs[0][k]for k in ('bytes','sha256')),'same original source')
        records=Path(path).with_suffix('.records.json.gz');entry=v.etw.identity(records)
        need(all(report['selected_records'][k]==entry[k]for k in ('bytes','sha256')),'same complete retained records')
        data=packed(records,128*1024*1024)
        bind_reader_artifact(source,refs[0],report,data)
        refs.append(entry);sequences.append(data['records'])
    utc,raw=sequences
    need(ur['ETL_header']==rr['ETL_header']and ur['ETL_header_raw_hex']==rr['ETL_header_raw_hex']and ur['buffer_reads']==rr['buffer_reads']
         and ur['total_records']==rr['total_records'],'same entire original ETL and buffer coverage')
    need(type(source['snapshot_clock']['frequency'])is int and source['snapshot_clock']['frequency']>0
         and source['snapshot_clock']['clock_conversion_or_tolerance_applied']is False
         and source['clock_diagnostic_only']is True and source['long_capture_preflight_passed']is False,
         'explicit unconverted positive raw QPC diagnostic clock')
    need(rr['raw_timestamp_mode']is True and rr['ETL_header']['ReservedFlags']==1 and rr['ETL_header']['PerfFreq']==source['snapshot_clock']['frequency'],'same actual raw QPC clock frequency')
    requested=v.etw.PROPERTIES.from_buffer_copy(bytes.fromhex(source['trace']['requested_properties_hex']))
    need(requested.Wnode.ClientContext==1,'collector requested actual QPC timestamps')
    v.producer_identities(source);v.source_contract(source,ur['ETL'],True);v.verify_receipt(source,utc,ur)
    image=(ROOT/'analysis/hermit_game.exe').read_bytes();v.verify_code(source,image)
    directory=ROOT/'.venv-audit/native-worker/guest-system-dlls'
    def loader(entry):
        data=(directory/Path(entry['module_path']).name).read_bytes()
        need(hashlib.sha256(data).hexdigest()==entry['module_sha256'],'exact retained guest DLL');return data
    v.original.verify_kernel_export(source,(ROOT/'.venv-audit/native-worker/guest-ntoskrnl.exe').read_bytes())
    v.original.verify_api_exports(source,loader);v.original.verify_tls_implementation(source,loader)
    need(source['phase']=='startup_preflight','short timing capability only, never battle acceptance')
    pairs,ledger=v.v3.validate_records(utc,source['subject'],2)
    baseline=source['before'];v.snapshot_contract(source,baseline,baseline,image)
    proofs=[v.snapshot_contract(source,s,baseline,image)for s in source['window_snapshots']]
    compared=compare(source,utc,raw,pairs,proofs)
    successful={tuple(r['global_syscall_pair'])for r in compared if r['raw_QPC_strict_single_off_interval']}
    report=dict(kind='same_ETL_raw_clock_comparison',accepted=False,fullABI=False,fullstate=False,PTDcleanup=False,
        strict_battle_window_verified=False,long_capture_preflight_passed=False,source_rewritten=False,timestamp_offset_applied=False,
        references=refs,QPC_frequency=source['snapshot_clock']['frequency'],cross_CPU_ordering_guard_ticks=1,
        complete_events=ur['total_records'],selected_records=len(utc),source_snapshots=len(compared),
        distinct_individually_QPC_qualified_waits=len(successful),boundary_ledger=ledger,snapshots=compared,
        UTC_failed_QPC_passed=[r['snapshot_index']for r in compared if r['raw_QPC_strict_single_off_interval']and not r['converted_UTC_strict_single_off_interval']],
        QPC_crossing_snapshots=[r['snapshot_index']for r in compared if r['raw_QPC_switches_inside_data_interval']],
        limitation='Data-read intervals exclude prior context acquisition. No whole-window/full-instruction/resource acceptance. Old sources have no raw snapshot QPC and cannot be repaired by a guessed conversion.',
        primary_clock_reference='https://learn.microsoft.com/en-us/windows/win32/api/evntrace/ns-evntrace-event_trace_logfilew')
    report['implementations']=implementations;report['implementations_after']=[v.etw.identity(p)for p in dependencies]
    need(report['implementations']==report['implementations_after'],'clock comparison dependencies unchanged')
    raw_json=(json.dumps(report,indent=2)+'\n').encode();need(len(raw_json)<=512*1024,'bounded clock comparison')
    with out.open('xb')as f:f.write(raw_json)
    print(json.dumps({k:report[k]for k in ('source_snapshots','distinct_individually_QPC_qualified_waits','UTC_failed_QPC_passed','QPC_crossing_snapshots','accepted')}))
    return 2


if __name__=='__main__':raise SystemExit(main())
