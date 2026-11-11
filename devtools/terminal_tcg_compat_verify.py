"""Offline exact-source verification of the bounded compatibility consumer."""
import argparse,hashlib,json
from pathlib import Path
from devtools.terminal_tcg_compat_context import pack,unpack,source_digest
from devtools.terminal_tcg_ram_event_verify import trajectory

def verify(source,sha):
    raw=(source/'report.json').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('report identity')
    r=json.loads(raw)
    if not r['bounded_case_passed'] or r['errors'] or not r['all_processes_exited']:raise ValueError('case failed')
    for row in r['files']:
        p=source/Path(row['path']).name;data=p.read_bytes()
        if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']:raise ValueError('raw identity '+p.name)
    envelopes={}
    for name in ('source_a','saved_a_after','target_a'):
        state=r[name]['states'][0];identity=source_digest(state)
        kw=dict(expected_cpu=0,expected_vcpus=2,expected_source_sha256=identity)
        envelope=pack(state,**kw)
        if unpack(envelope,**kw)!=state:raise ValueError('lossless reconstruction')
        envelopes[name]=envelope
    traces={role:trajectory(source/(role+'.trace'),r['expected']['a'],r['expected']['b'])for role in ('source','target')}
    checks=dict(r['checks'],envelopes_equal=len({source_digest(v)for v in envelopes.values()})==1,
        a_to_b_entries_equal=traces['source']['a_to_b']==traces['target']['a_to_b'])
    if not all(checks.values()):raise ValueError('independent check failed')
    return dict(accepted=False,windows_admitted=False,source_report_sha256=sha,
        bounded_compatibility_restore_passed=True,checks=checks,envelopes=envelopes,
        a_to_b_entry_count=len(traces['source']['a_to_b']),
        exit_suffix_equal=traces['source']['supervised_exit_suffix']==traces['target']['supervised_exit_suffix'],
        scope='Exact raw A context, same-command save, restored A/B and native high-state consumption; no Windows/game admission')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('sha256');p.add_argument('output',type=Path)
    a=p.parse_args();result=verify(a.source,a.sha256)
    with a.output.open('x')as f:json.dump(result,f,indent=2)
    print(result['bounded_compatibility_restore_passed'])
