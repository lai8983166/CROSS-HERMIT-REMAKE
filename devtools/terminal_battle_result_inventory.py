"""Distinguish saved wait-return sites from actual consumer instruction PCs.

Only the fixed retained battle lifetime is inspected. Endpoints do not supply
unrecorded execution between them, and pending NtWait EAX is never a return.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import struct
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
WORKER=ROOT/'.venv-audit/native-worker'
WINDOW=('terminal-battle-wait-window-battle-v6-20261109.json.gz','9874fb2e589aafb1b3190c9a2a5aac7c7ee0e0a3179923cd10d463bee3fd680e')
SCHOOL=('terminal-battle-wait-window-battle-v6-20261109.school.json.gz','271fb1e0a7e58c956c3d7eaa565c3490d17219a0ad60753d9d0243abe97d0ff7')
CONSUMERS=((0x453cb5,0x453cfc),(0x4967b0,0x4968a9))


def need(ok,msg):
    if not ok:raise ValueError(msg)


def load(name,sha):
    p=WORKER/name;b=p.read_bytes();need(len(b)<=24*1024*1024 and hashlib.sha256(b).hexdigest()==sha,'fixed complete retained native source')
    with gzip.open(p,'rb')as f:raw=f.read(192*1024*1024+1)
    need(len(raw)<=192*1024*1024,'bounded complete source expansion')
    return json.loads(raw),dict(path=str(p),bytes=len(b),sha256=sha)


def classify(frame):
    raw=bytes.fromhex(frame['context_hex']);need(len(raw)==716 and struct.unpack_from('<I',raw)[0]==0x1003f,'complete original context')
    eip=struct.unpack_from('<I',raw,184)[0];need(eip==frame['EIP'],'raw actual instruction PC')
    return dict(actual_EIP=eip,actual_consumer_PC=any(a<=eip<b for a,b in CONSUMERS),
        saved_consumer_return_sites=[f['return_va']for f in frame['chain']if any(a<=f['return_va']<b for a,b in CONSUMERS)],
        context_sha256=hashlib.sha256(raw).hexdigest())


def scene_frames(value,subject,path=()):
    if isinstance(value,dict):
        if isinstance(value.get('tasks'),list)and isinstance(value.get('frames'),list):
            tasks=[t for t in value['tasks']if t.get('pointer')==subject['node']and t.get('thread_id')==subject['tid']]
            if tasks:
                need(len(tasks)==1,'one actual retained battle scene');task=tasks[0]
                head=bytes.fromhex(task['header_hex']);need(len(head)==64 and struct.unpack_from('<I',head,0x24)[0]==subject['tid'],'raw scene thread identity')
                need(struct.unpack_from('<I',head)[0]==0x59a430,'same original battle scene vtable')
                frames=[f for f in value['frames']if f['tid']==subject['tid']]
                need(len(frames)==1,'same original captured worker');tls=task['TLS']
                need((tls['owner_pid'],tls['thread_id'])==(subject['pid'],subject['tid']),'same actual TLS owner')
                yield dict(source_path=list(path),elapsed=value.get('elapsed'),**classify(frames[0]))
        for k,v in value.items():yield from scene_frames(v,subject,path+(k,))
    elif isinstance(value,list):
        for i,v in enumerate(value):yield from scene_frames(v,subject,path+(i,))


def run(out):
    window,wid=load(*WINDOW);school,sid=load(*SCHOOL)
    rows=list(scene_frames(school['probe'],window['subject'],('probe',)))
    need(rows,'actual retained scene contexts exist')
    windows=[dict(snapshot_index=i,**classify(x['frame']))for i,x in enumerate(window['window_snapshots'])]
    hits=[r for r in rows if r['actual_consumer_PC']];wait_hits=[r for r in rows if r['saved_consumer_return_sites']]
    need(len(hits)<=16,'bounded unique direct consumer-PC evidence; no truncation')
    nt=next(x['target']+12 for x in window['API_exports']if x['name']=='NtWaitForSingleObject')
    gates=Counter(x['recording_gate']['hex']for x in window['window_snapshots'])
    report=dict(kind='retained_same_battle_result_consumption_coverage_inventory',references=[wid,sid],accepted=False,
        original_subject=window['subject'],actual_scene_contexts=len(rows),direct_consumer_PC_contexts=hits,
        actual_EIP_counts={hex(k):v for k,v in Counter(r['actual_EIP']for r in rows).items()},
        contexts_with_saved_consumer_return_sites=len(wait_hits),first_saved_return_witness=wait_hits[0]if wait_hits else None,
        wait_window_contexts=len(windows),wait_window_current_Nt_return_PC_contexts=sum(r['actual_EIP']==nt for r in windows),
        wait_window_direct_consumer_PC_contexts=sum(r['actual_consumer_PC']for r in windows),
        original_recording_gate_byte_counts=dict(gates),
        result_endpoint_audit='analysis/terminal-battle-wait-gap-audit-v2-20261109.json',
        continuous_result_consumption_proved=False,fullABI=False,fullstate=False,PTDcleanup=False,new_native_capture=False,
        limitations=['A saved 453CB5/453CD3/453CDD stack return site is not current EIP in the consumer.',
            'Pending NtWait user context EAX is not the later syscall return; no result/register is patched.',
            'Observed recording gate bytes select a candidate original branch, not evidence that its instructions executed.',
            'Snapshots and recovered endpoint locals do not supply the intervening instruction/write/ABI trace.'],
        next_required_observation='Authenticate complete live caller/return context and original consumer code/data across the completed wait; retain actual instruction/write/leaf outcomes. Existing discarded or absent records cannot be reconstructed from stack return sites.',
        implementation=dict(path=str(Path(__file__)),sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
    raw=(json.dumps(report,indent=2)+'\n').encode();need(len(raw)<=65536,'bounded coverage inventory')
    with Path(out).open('xb')as f:f.write(raw)
    print(json.dumps({k:report[k]for k in ('actual_scene_contexts','wait_window_contexts','wait_window_current_Nt_return_PC_contexts','wait_window_direct_consumer_PC_contexts','contexts_with_saved_consumer_return_sites')}));return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();run(a.out);raise SystemExit(2)
