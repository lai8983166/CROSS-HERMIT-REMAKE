"""Reconcile existing battle-window gaps with the same retained input source.

Supplemental frames are actual observed endpoints, not successful wait pairs:
they lack precise capture brackets and the complete Nt argument stack. No UTC
offset is guessed, no rejected snapshot is discarded, and no source is rewritten.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import struct
from devtools import terminal_battle_wait_verification_v4 as verify

ROOT=Path(__file__).resolve().parents[1]
WORKER=ROOT/'.venv-audit/native-worker'
PARENTS={
 'window':('terminal-battle-wait-window-battle-v6-20261109.json.gz','9874fb2e589aafb1b3190c9a2a5aac7c7ee0e0a3179923cd10d463bee3fd680e'),
 'school':('terminal-battle-wait-window-battle-v6-20261109.school.json.gz','271fb1e0a7e58c956c3d7eaa565c3490d17219a0ad60753d9d0243abe97d0ff7'),
 'records':('terminal-battle-wait-decode-battle-v8-20261109.records.json.gz','cdf4001adf1759d5487b1fc003b621e28041b0d1549e76ef8026a9182053ae4c'),
 'strict':('terminal-battle-wait-decode-battle-v8-20261109.json','1315a2d66c30d49d20af4f240a1625564b1209a310f98fff57e42e38fe0a504c'),
}
need=verify.need


def identity(path):
    raw=Path(path).read_bytes()
    return dict(path=str(Path(path).resolve()),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def execution_paths():
    return [Path(__file__),Path(verify.__file__),Path(verify.v3.__file__),Path(verify.v2.__file__),
            Path(verify.v1.__file__),Path(verify.etl.__file__),Path(verify.etl.parent.__file__),
            Path(verify.original.__file__),Path(verify.etw.__file__),
            ROOT/'devtools/terminal_school_handoff_verification.py']


def terminal_memory(task):
    """Existing raw regions only. Missing API bytes are never synthesized."""
    regions=task['terminal_frames'];need(0<len(regions)<=100,'bounded saved terminal regions')
    memory={}
    for row in regions:
        pointer=row['pointer'];raw=bytes.fromhex(row['hex'])
        need(type(pointer)is int and 0<pointer<0x100000000-len(raw) and len(raw)==0x90,
             'complete bounded original terminal region')
        for address,value in enumerate(raw,pointer):
            need(address not in memory or memory[address]==value,'overlapping original stack bytes agree')
            memory[address]=value
    return memory


def raw_frame(memory,frame,required=False):
    bp=frame['bp'];addresses=range(bp,bp+8)
    available=all(a in memory for a in addresses)
    need(available or not required,'actual wait caller frame must have saved raw bytes')
    if not available:return None
    raw=bytes(memory[a]for a in addresses)
    need(struct.unpack('<II',raw)==(frame['saved_bp'],frame['return_va']),
         'raw wait/API saved frame matches decoded original chain')
    return dict(pointer=bp,hex=raw.hex())


def read_bound(path,sha,limit=1024*1024,expanded=192*1024*1024):
    packed=path.read_bytes();need(0<len(packed)<=limit and hashlib.sha256(packed).hexdigest()==sha,'exact fixed parent artifact')
    if path.suffix=='.gz':
        with gzip.open(path,'rb')as f:raw=f.read(expanded+1)
        need(len(raw)<=expanded,'bounded complete parent expansion')
    else:raw=packed
    return json.loads(raw),dict(path=path.relative_to(ROOT).as_posix(),bytes=len(packed),sha256=sha)


def endpoint(row,subject,baseline):
    candidates=[t for t in row['tasks']if t['pointer']==subject['node']and t['thread_id']==subject['tid']]
    need(len(candidates)==1,'one same original battle task')
    task=candidates[0];frames=[f for f in row['frames']if f['tid']==subject['tid']];need(len(frames)==1,'same original worker frame')
    frame=frames[0];ctx=bytes.fromhex(frame['context_hex']);need(len(ctx)==716,'complete original WOW64 context')
    need(struct.unpack_from('<I',ctx)[0]==0x1003f,'actual complete WOW64 context flags')
    need((frame['EIP'],frame['EBP'],frame['ESP'])==struct.unpack_from('<I',ctx,184)+struct.unpack_from('<I',ctx,180)+struct.unpack_from('<I',ctx,196),'raw EIP/EBP/ESP')
    head=bytes.fromhex(task['header_hex']);need(len(head)==64 and head==bytes.fromhex(task['scene_head_hex'])[:64],'same raw scene header')
    need(struct.unpack_from('<I',head)[0]==0x59a430 and struct.unpack_from('<I',head,0x24)[0]==subject['tid'],'original scene vtable/TID')
    verify.original.verify_current_tls(task['TLS'],ctx,baseline['current_TLS'],subject['node'],subject['pid'],subject['tid'])
    chain=frame['chain'];need(0<len(chain)<=100 and chain[0]['bp']==frame['EBP'],'raw frame-chain start')
    for f in chain:
        need(all(type(f[k])is int and 0<=f[k]<0x100000000 for k in ('bp','saved_bp','return_va')),
             'bounded original frame words')
    for a,b in zip(chain,chain[1:]):need(a['saved_bp']==b['bp'] and a['bp']<b['bp']<a['bp']+0x100000,'ordered original chain')
    waits=[x for x in chain if x['return_va']in verify.WAIT_SITES];need(len(waits)==1,'one original battle wait caller')
    api=[x for x in chain if x['return_va']==0x42240d]
    need(len(api)==1 and api[0]['saved_bp']==waits[0]['bp']
         and chain.index(api[0])+1==chain.index(waits[0]),'same original Win32 and game wait frames')
    memory=terminal_memory(task)
    wait_raw=raw_frame(memory,waits[0],True)
    api_raw=raw_frame(memory,api[0])
    # All original ancestor links covered by the retained memory must agree too.
    for f in chain:raw_frame(memory,f)
    locals_={};raw_rows=[]
    for ret,name,off in ((0x451abc,'inner_result',8),(0x451716,'dispatcher_result',8),(0x421f8a,'callback_result',12)):
        matches=[f for f in chain if f['return_va']==ret]
        if not matches:continue
        need(len(matches)==1,'unique result ancestor');f=matches[0]
        regions=[x for x in task['terminal_frames']if x['return_va']==ret]
        need(len(regions)==1 and regions[0]['pointer']==f['bp']-0x80,'original terminal raw region')
        r=regions[0];raw=bytes.fromhex(r['hex']);need(len(raw)==0x90,'full original local region')
        need(struct.unpack_from('<III',raw,0x7c)==(subject['node'],f['saved_bp'],ret),'raw receiver and saved original frame links')
        locals_[name]=struct.unpack_from('<I',raw,0x80-off)[0]
        if ret==0x421f8a:locals_['tail_counter']=struct.unpack_from('<I',raw,0x78)[0]
        raw_rows.append(dict(return_va=ret,pointer=r['pointer'],sha256=hashlib.sha256(raw).hexdigest()))
    site=waits[0]['return_va']
    if site==0x451758:need(0<=locals_['tail_counter']<10 and locals_['callback_result']!=0,'actual tail local and consumed callback result')
    return dict(elapsed=row['elapsed'],site=hex(site),locals=locals_,raw_local_regions=raw_rows,
        raw_wait_frame=wait_raw,decoded_API_to_wait_adjacency_checked=True,
        raw_API_frame=api_raw,api_link_raw_proved=api_raw is not None,
        actual_original_endpoint_observed=True,ETW_wait_return_proved=False,
        precise_capture_interval_available=False,complete_Nt_argument_stack_available=False)


def audit_result():
    source={};references={}
    for key,(name,sha)in PARENTS.items():source[key],references[key]=read_bound(WORKER/name,sha,24*1024*1024)
    window=source['window'];school=source['school'];rows=source['records']['records'];receipt=source['strict']
    proof,proof_id=read_bound(ROOT/'analysis/terminal-battle-wait-full-prefix-proof-v6-20261109.json','e2259a701effe4fd325f05eb997e163df65f8c592f7b1ce0faf9ffb3f74988d1')
    references['independent_full_prefix_proof']=proof_id
    need(receipt['errors']==["ValueError('actual complete snapshot strictly inside one target switch-out interval')"],'strict original failure preserved')
    verify.reported_end_boundary(window,rows,receipt)
    end=next(b['ns']for b in receipt['subject_thread_bindings']if b['opcode']==2)
    pairs,ledger=verify.validate_lifetime_records(rows,window['subject'],2,end)
    crossings=[]
    for index in (213,239,383,419):
        snap=window['window_snapshots'][index];lo,hi=snap['snapshot_begin_ns'],snap['snapshot_end_ns']
        match=[(a,b)for a,b in pairs if rows[a]['ns']<lo<=hi<rows[b]['ns']]
        need(len(match)==1,'one complete surrounding raw syscall')
        a,b=match[0];need(rows[a]['data']['SysCallAddress']==window['kernel_wait_export']['target']and rows[b]['data']['SysCallNtStatus']==0,'actual enclosing successful NtWait')
        near=[r for r in rows[a+1:b]if r['opcode']==36 and lo<=r['ns']<=hi]
        need(near,'actual crossing, not an assumed time correction')
        crossings.append(dict(snapshot_index=index,source_interval_ns=[lo,hi],enclosing_call_global_indices=[rows[a]['index'],rows[b]['index']],
            crossed_switches=[dict(global_index=r['index'],offset_from_snapshot_end_ns=r['ns']-hi,CPU=r['cpu'],data=r['data'],payload_hex=r['payload_hex'])for r in near],
            raw_QPC_snapshot_timestamps_available=False,cause_proved=False,strict_snapshot_accepted=False))
    record=school['probe']['battle_inputs'][1]
    canonical=json.dumps(record,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
    need(len(canonical)==window['input_receipt']['canonical']['bytes']and hashlib.sha256(canonical).hexdigest()==window['input_receipt']['canonical']['sha256'],'same exact original input record')
    supplemental=[endpoint(r,window['subject'],window['before'])for r in record['post_release_snapshots']]
    recovered_zero=[i for i,r in enumerate(supplemental)if r['site']=='0x451758'and r['locals'].get('tail_counter')==0]
    recovered_result=[i for i,r in enumerate(supplemental)if r['site']=='0x453cb5'and r['locals'].get('inner_result')==1]
    need(recovered_zero==[2]and recovered_result==[0],'actual existing missing endpoint locations')
    result=dict(kind='same_lifetime_gap_reconciliation',accepted=False,fullstate=False,fullABI=False,PTDcleanup=False,
        strict_full_window_verified=False,continuous_result_consumption_proved=False,new_native_capture=False,
        references=references,crossings=crossings,supplemental_original_endpoints=supplemental,
        recovered_tail_zero_rows=recovered_zero,recovered_nonzero_result_rows=recovered_result,
        added_successful_wait_pairs=0,
        timing_limit='Existing snapshot UTC and converted ETW UTC are different readings; no saved raw snapshot QPC. No offset/tolerance can be justified from this source.',
        supplemental_limit='The same native input source supplies actual missing result/tail endpoints, but no complete precise interval or Nt argument stack for a new successful wait pair.')
    return result


def audit(out):
    paths=execution_paths();before=[identity(p)for p in paths]
    result=audit_result()
    after=[identity(p)for p in paths]
    need(before==after,'gap-audit execution dependencies unchanged')
    result.update(execution_implementations=before,execution_implementations_after=after)
    raw=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode();need(len(raw)<128*1024,'small gap-only report')
    with Path(out).open('xb')as f:f.write(raw)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=audit(a.out)
    print(json.dumps(dict(recovered_tail_zero_rows=r['recovered_tail_zero_rows'],recovered_nonzero_result_rows=r['recovered_nonzero_result_rows'],accepted=False)))
    raise SystemExit(2)
