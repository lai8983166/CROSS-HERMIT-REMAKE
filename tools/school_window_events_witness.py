"""Read-only phase witnesses bound to complete independently verified raw events."""
import argparse
import hashlib
import json
from tools.school_window_events import ROOT
from tools.school_window_events_verification import verify_report
from tools.school_window_module_validation import digest


def witness(path,phase):
    raw=(ROOT/path).read_bytes();r=json.loads(raw);before=digest(r);proof=verify_report(r)
    if phase not in ('scalars','position'):raise ValueError('declared phase required')
    selected=range(3,6) if phase=='scalars' else (6,)
    cases=[]
    for c,p in zip(r['cases'],proof['case_proofs']):
        nodes=[c['callbacks'][i] for i in selected]
        cases.append(dict(fill=c['fill'],callbacks=[p['callbacks'][i] for i in selected],raw_nodes_sha256=digest(nodes),
            scalar_inputs=[n['setup']['packet'] for n in nodes] if phase=='scalars' else None,
            pending_message=p['pending_message'],pending_WINDOWPOS_flags=p['pending_WINDOWPOS_flags']))
    if digest(r)!=before:raise ValueError('witness mutated raw evidence')
    return dict(phase=phase,trajectory=dict(path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),
        independent_complete_replay=proof,cases=cases,raw_evidence_modified=False,retained_VM_advanced=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('phase',choices=('scalars','position'));p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    if out.exists():p.error('fresh immutable phase witness required')
    out.write_text(json.dumps(witness('analysis/school-window-events-trajectory-v1-20261020.json',a.phase),indent=2)+'\n',encoding='utf8',newline='\n')
