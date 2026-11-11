"""Reuse authenticated RAM/event captures with architectural57 v2; no VM run."""
import argparse,hashlib,json
from pathlib import Path
from devtools.terminal_tcg_canonical57_v2 import from_tcg,Canonical57Error
from devtools.terminal_tcg_ram_event_verify import verify


def run(work,output):
    result=dict(accepted=False,windows_admitted=False,native_runs=0,cases=[],tamper_refusals={})
    for name in ('tcg-ram-event-v2-before-call','tcg-ram-event-v3-rf-return','tcg-ram-event-v3-pending-irq'):
        directory=work/name;report=directory/'report.json';sha=hashlib.sha256(report.read_bytes()).hexdigest()
        prior=verify(directory,sha);r=json.loads(report.read_bytes())
        projected={k:from_tcg(r[k]['states'][0],expected_cpu=0,expected_vcpus=2)for k in ('source_a','source_b','target_a','target_b')}
        matches=all(projected['source_'+p]['registers']==projected['target_'+p]['registers']for p in ('a','b'))
        if not matches:raise ValueError('v2 projection difference')
        result['cases'].append(dict(name=name,report_sha256=sha,endpoint_proof=prior,canonical57=projected,v2_matches=True))
        try:verify(directory,'0'*64)
        except ValueError:result['tamper_refusals'][name+'-report-sha']=True
        else:raise ValueError('bad report identity accepted')
    compat=work/'tcg-compatibility-v8b/report.json';raw=json.loads(compat.read_bytes())['state']
    try:from_tcg(raw,expected_cpu=0,expected_vcpus=2)
    except Canonical57Error as e:result['actual_compatibility_refusal']=dict(reason=str(e),report_sha256=hashlib.sha256(compat.read_bytes()).hexdigest())
    else:raise ValueError('unsupported compatibility state silently accepted')
    result['all_bounded_checks_passed']=True
    with output.open('x')as f:json.dump(result,f,indent=2)
    print(json.dumps(dict(cases=len(result['cases']),all_bounded_checks_passed=True,compatibility_rejected=result['actual_compatibility_refusal']['reason'])))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('work',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();run(a.work,a.output)
