"""Strictly check full context acquisition separately from sampled data waits."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import struct
from devtools import terminal_battle_wait_clock_review as clock

need=clock.need


def ordered(a,b,message):
    need(type(a)is int and type(b)is int and 0<a<=b,message)


def validate_attempt(record,subject,frame_pair=None,data_interval=None):
    need(record['complete']is True and 'error'not in record,'complete actual acquisition and cleanup')
    tids=[subject['main_tid'],subject['tid']];threads=record['threads'];ops=record['operations']
    need(len(threads)==2 and [x['tid']for x in threads]==tids,'same two original owners')
    handles=[x['handle']for x in threads]
    need(all(type(h)is int and h>0 for h in handles)and handles[0]!=handles[1],'distinct retained handles')
    expected=[('suspend',handles[0]),('suspend',handles[1]),('resume',handles[1]),('resume',handles[0]),('close',handles[1]),('close',handles[0])]
    need([(x['action'],x['handle'])for x in ops]==expected,'only own increments restored and handles closed in reverse order')
    for x in ops:
        ordered(x['qpc_begin'],x['qpc_end'],'actual operation timing')
        need(type(x['result'])is int and 0<=x['result']<=0xffffffff,'actual integer DWORD operation result')
    for index,t in enumerate(threads):
        reads=t['contexts'];need(len(reads)==2 and [x['phase']for x in reads]==['before','after'],'two actual full context calls')
        need(t['owner_verified_before_suspend']is True and type(t['previous_suspend_count'])is int and 0<=t['previous_suspend_count']<0xffffffff,'authenticated held owner')
        need(ops[index]['result']==t['previous_suspend_count']and ops[3-index]['result']==t['previous_suspend_count']+1
             and ops[5-index]['result']!=0,'actual successful own resume and close outcomes')
        for read in reads:
            ordered(read['qpc_begin'],read['qpc_end'],'context query timing')
            need(type(read['result'])is int and read['result']!=0,'actual successful context query')
            raw=bytes.fromhex(read['raw_hex']);need(len(raw)==716 and struct.unpack_from('<I',raw)[0]==0x1003f,'all original WOW64 context groups')
        same=reads[0]['raw_hex']==reads[1]['raw_hex']
        need(t['all_716_bytes_equal']is same,'recomputed complete raw comparison; no register mask')
        if frame_pair is not None:
            f=frame_pair[index]
            need(f['tid']==t['tid']and f['context_hex']==reads[0]['raw_hex']and f['previous_suspend_count']==t['previous_suspend_count'],
                 'sample frame is the actual first context from that same handle')
    main,worker=threads;mb,ma=main['contexts'];wb,wa=worker['contexts']
    sequence=[record['qpc_begin'],ops[0]['qpc_begin'],ops[0]['qpc_end'],mb['qpc_begin'],mb['qpc_end'],
        ops[1]['qpc_begin'],ops[1]['qpc_end'],wb['qpc_begin'],wb['qpc_end'],record['data_scope_begin_qpc'],
        record['settling']['qpc_begin'],record['settling']['qpc_end'],record['data_scope_end_qpc'],
        ma['qpc_begin'],ma['qpc_end'],wa['qpc_begin'],wa['qpc_end']]
    for op in ops[2:]:sequence.extend([op['qpc_begin'],op['qpc_end']])
    sequence.append(record['qpc_end'])
    for a,b in zip(sequence,sequence[1:]):ordered(a,b,'actual entire held protocol order')
    if data_interval is not None:
        ordered(record['settling']['qpc_end'],data_interval[0],'settling precedes complete data reads')
        ordered(data_interval[0],data_interval[1],'complete data interval')
        ordered(data_interval[1],record['data_scope_end_qpc'],'data ends before context reread')
    need(record['settling']['original_threads_still_suspended']is True and record['settling']['descheduling_assumed']is False,
         'settling does not stand in for actual scheduler evidence')
    return dict(full_worker_context_data_interval=[wb['qpc_begin'],wa['qpc_end']],
                both_full_context_data_interval=[mb['qpc_begin'],wa['qpc_end']],
                all_716_bytes_equal=all(t['all_716_bytes_equal']for t in threads))


def inspect(source,records,comparison):
    attempts=source['context_attempts'];need(len(attempts)==source['sample_attempts']>0,'all actual context attempts retained')
    need([x['index']for x in attempts]==list(range(len(attempts))),'complete attempt indices')
    summaries=[validate_attempt(x,source['subject'])for x in attempts]
    before=source['before'];validate_attempt(attempts[before['context_attempt_index']],source['subject'],
        [before['scheduler_frame'],before['frame']],before['timing_diagnostic']['data_interval_qpc'])
    positions={r['index']:i for i,r in enumerate(records)};need(len(positions)==len(records),'unique complete global event indices')
    need(len(source['window_snapshots'])==len(comparison['snapshots']),'same exact finite snapshot count')
    checks=[];used=[before['context_attempt_index']]
    for index,(snap,old)in enumerate(zip(source['window_snapshots'],comparison['snapshots'])):
        need(old['snapshot_index']==index and old['QPC_data_interval']==snap['timing_diagnostic']['data_interval_qpc'],'same checked data interval')
        key=snap['context_attempt_index'];used.append(key);need(type(key)is int and 0<=key<len(attempts),'actual attempt index')
        check=validate_attempt(attempts[key],source['subject'],[snap['scheduler_frame'],snap['frame']],old['QPC_data_interval'])
        lo,hi=check['full_worker_context_data_interval'];pair=old.get('global_syscall_pair');strict=False
        if pair:
            local=tuple(positions[x]for x in pair)
            strict=clock.interval_check(records,local,source['subject']['tid'],lo,hi,'qpc_ticks',1)
        checks.append(dict(snapshot_index=index,context_attempt_index=key,**check,
            data_only_strict=old['raw_QPC_strict_single_off_interval'],
            full_worker_context_data_strict_single_off_interval=strict,
            switches_in_complete_worker_interval=[r['index']for r in records if r['opcode']==36 and lo<=r['qpc_ticks']<=hi]))
    used.extend(x['context_attempt_index']for x in source['non_wait_samples'])
    need(len(used)==len(set(used))and all(type(i)is int and 0<=i<len(attempts)for i in used),'no context attempt reused for a different snapshot')
    need(len(attempts)-len(used)==source.get('unretained_non_wait_timing_samples',0),'all otherwise unretained nonwait attempts still counted')
    return dict(attempts=len(attempts),all_raw_context_pairs_equal=sum(x['all_716_bytes_equal']for x in summaries),snapshots=checks)


def load(path,sha,packed=False):
    path=Path(path);raw=path.read_bytes();need(0<len(raw)<=2*1024*1024 and hashlib.sha256(raw).hexdigest()==sha,'explicit bounded retained artifact')
    if packed:
        with gzip.open(path,'rb')as f:raw=f.read(128*1024*1024+1)
        need(len(raw)<=128*1024*1024,'bounded full expansion')
    return json.loads(raw),dict(path=str(path.resolve()),bytes=path.stat().st_size,sha256=sha)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('source','source-sha','clock-report','clock-sha','raw-records','raw-sha','out'):p.add_argument('--'+name,required=True)
    a=p.parse_args();out=Path(a.out);need(not out.exists(),'new complete-context review')
    paths=[Path(__file__),Path(clock.__file__),Path(clock.v.__file__),Path(clock.v.original.__file__)]
    impl=[clock.v.etw.identity(x)for x in paths]
    source,sid=load(a.source,a.source_sha,True);comparison,cid=load(a.clock_report,a.clock_sha);data,rid=load(a.raw_records,a.raw_sha,True)
    need(all(comparison['references'][0][k]==sid[k]and comparison['references'][4][k]==rid[k]for k in ('bytes','sha256')),'same independently checked source and raw records')
    need(data['subject']==source['subject']and all(data['source'][k]==sid[k]for k in ('bytes','sha256')),'same retained raw event owner and source')
    need(comparison['accepted']is False and comparison['long_capture_preflight_passed']is False and source['full_context_observation_diagnostic_only']is True,'diagnostic only, never production qualification')
    need(comparison['implementations']==comparison['implementations_after'],'clock verifier unchanged during run')
    for item in comparison['implementations']:
        path=Path(item['path']);actual=clock.v.etw.identity(path)
        need(all(actual[k]==item[k]for k in ('bytes','sha256')),'current exact clock verification dependency')
    clock.v.producer_identities(source)
    result=inspect(source,data['records'],comparison)
    result.update(kind='full_WOW64_context_acquisition_diagnostic',references=[sid,cid,rid],
        accepted=False,fullABI=False,fullstate=False,continuous_result_consumption_proved=False,PTDcleanup=False,
        long_capture_preflight_passed=False,all_original_ETL_records_retained=True,
        full_context_single_off_intervals=sum(x['full_worker_context_data_strict_single_off_interval']for x in result['snapshots']),
        coherent_worker_context_intervals=sum(x['full_worker_context_data_strict_single_off_interval']and x['all_716_bytes_equal']for x in result['snapshots']),
        joint_scheduler_worker_off_CPU_proved=False,
        limitation='Equal full 716-byte before/after contexts and finite single-off intervals are not continuous instruction/state/ABI or cleanup proof.',
        implementations=impl,implementations_after=[clock.v.etw.identity(x)for x in paths])
    need(result['implementations']==result['implementations_after'],'context review dependencies unchanged')
    raw=(json.dumps(result,indent=2)+'\n').encode();need(len(raw)<=256*1024,'bounded context comparison')
    with out.open('xb')as f:f.write(raw)
    print(json.dumps({k:result[k]for k in ('attempts','all_raw_context_pairs_equal','full_context_single_off_intervals','accepted')}));return 2


if __name__=='__main__':raise SystemExit(main())
