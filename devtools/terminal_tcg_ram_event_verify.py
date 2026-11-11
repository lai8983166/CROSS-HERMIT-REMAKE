"""Verify the declared stopped A-to-B boundary from retained raw evidence.

The asynchronous isa-debug-exit teardown after B is recorded separately;
not normalized into instruction-retirement equivalence.
"""
import argparse,hashlib,json,re
from pathlib import Path
from devtools.terminal_tcg_canonical57 import from_tcg


def trajectory(path,a,b):
    rows=[]
    for line in path.read_text().splitlines():
        m=re.match(r'Trace (\d+): .* \[([0-9a-f]+)/([0-9a-f]+)/([0-9a-f]+)/([0-9a-f]+)\]',line)
        if m:rows.append([int(m[1]),*[int(m[i],16)for i in (2,3,4)]])
    start=next(i for i,r in enumerate(rows)if r[2]==a)
    end=next(i for i in range(start,len(rows))if rows[i][2]==b)
    return dict(a_to_b=rows[start:end],supervised_exit_suffix=rows[end:])


def verify(source,expected_sha):
    report=source/'report.json';raw=report.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=expected_sha:raise ValueError('report identity')
    r=json.loads(raw)
    for row in r['files']:
        p=source/Path(row['path']).name
        data=p.read_bytes()
        if len(data)!=row['bytes']or hashlib.sha256(data).hexdigest()!=row['sha256']:raise ValueError('raw evidence changed '+p.name)
    checks={k:v for k,v in r['checks'].items()if k!='continued_trajectory'}
    if r['errors']or not r['all_processes_exited']:raise ValueError('capture failure')
    for point in ('a','b'):
        left=r['source_'+point];right=r['target_'+point]
        checks['full_observation_'+point]=left==right
        checks['canonical57_'+point]=from_tcg(left['states'][0],expected_cpu=0,expected_vcpus=2)['registers']==from_tcg(right['states'][0],expected_cpu=0,expected_vcpus=2)['registers']
    t={role:trajectory(source/(role+'.trace'),r['expected']['a'],r['expected']['b'])for role in ('source','target')}
    checks['a_to_b_trace_entries']=t['source']['a_to_b']==t['target']['a_to_b']
    if not all(checks.values()):raise ValueError({k:v for k,v in checks.items()if not v})
    return dict(accepted=False,windows_admitted=False,bounded_a_to_b_passed=True,checks=checks,
        source_report_sha256=expected_sha,trajectory=t,
        exit_suffix_equal=t['source']['supervised_exit_suffix']==t['target']['supervised_exit_suffix'],
        scope='Two stopped boundaries A/B, complete exported observations and RAMBlock bytes, raw event logs and natural result output. Asynchronous debug-exit suffix is not a replay acceptance claim.')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('sha256');p.add_argument('output',type=Path)
    a=p.parse_args();r=verify(a.source,a.sha256)
    with a.output.open('x')as f:json.dump(r,f,indent=2)
    print(json.dumps({k:v for k,v in r.items()if k not in ('trajectory','checks')},indent=2))
