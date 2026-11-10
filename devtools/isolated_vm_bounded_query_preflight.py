"""One fresh headless boot; deadline/identity checks only, never game acceptance."""
import argparse
import json
import time
from devtools.isolated_windows_vm import WORKER,VMX,validate_vmx,vmrun,identity
from devtools.isolated_vm_bounded_query import query


def run(label):
    import re
    if not re.fullmatch('bounded-query-v[0-9]+-20261110',label):raise ValueError('fresh owned preflight label')
    d=WORKER/label;d.mkdir(exist_ok=False)
    validate_vmx(VMX.read_text());r=dict(accepted=False,fullstate=False,original_game_starts=0,host_input_actions=0,errors=[])
    if str(VMX).lower()in vmrun(['list']).lower():raise ValueError('existing VM must remain undisturbed')
    r['vmx_before']=identity(VMX);r['vmdk_before_bytes']=sum(p.stat().st_size for p in WORKER.glob('worker*.vmdk'))
    t=time.monotonic()
    try:
        r['start']=vmrun(['start',VMX,'nogui'],timeout=20)
        r['boot_queries']=[]
        for attempt in range(4):
            time.sleep(5)
            q=query('status',seconds=12);r['boot_queries'].append(q)
            (d/'progress.json').write_text(json.dumps(r,indent=2))
            if q.get('response',{}).get('ok'):
                r['before']=json.loads(q['response']['value']);break
        else:raise ValueError('bounded boot readiness refused')
        if r['before']['cpu']!=2 or r['before']['uuid']!='E6D84D56-0960-FA47-1543-6C62C21D5DC7':raise ValueError('actual guest identity')
        r['completed_query']=query('sleep_echo',1,seconds=12)
        if r['completed_query'].get('response',{}).get('value','').strip()!='bounded-query-finished':raise ValueError('normal guarded query')
        r['deadline_query']=query('sleep_echo',8,seconds=2)
        q=r['deadline_query']
        if not q.get('timed_out')or q.get('host_job_active_after')!=0 or q['elapsed_seconds']>6 or q['remote_completion']!='unknown':raise ValueError('host deadline and honest remote state')
        # A timeout does not authorize new work. Only read-only status follows.
        r['after_query']=query('status',seconds=12)
        if not r['after_query'].get('response',{}).get('ok'):raise ValueError('guest response after host deadline')
        r['after']=json.loads(r['after_query']['response']['value'])
        if r['before']['boot']!=r['after']['boot']or r['before']['uuid']!=r['after']['uuid']:raise ValueError('same guest lifetime')
        r['host_deadline_preflight_passed']=True
    except Exception as e:r['errors'].append(repr(e))
    finally:
        try:
            r['stop']=vmrun(['stop',VMX,'soft'],timeout=30)
            r['running_after']=vmrun(['list']);r['snapshots']=vmrun(['listSnapshots',VMX])
            if str(VMX).lower()in r['running_after'].lower():raise ValueError('owned guest still running')
            r['vmem_files']=[str(p)for p in WORKER.glob('*.vmem')]
            validate_vmx(VMX.read_text());r['vmx_after']=identity(VMX)
            r['vmdk_after_bytes']=sum(p.stat().st_size for p in WORKER.glob('worker*.vmdk'))
        except Exception as e:r['errors'].append('cleanup: '+repr(e))
        r['elapsed_seconds']=time.monotonic()-t
        r['code']=[identity(p)for p in (WORKER.parents[1]/'devtools').glob('isolated_vm_bounded_query*.py')]
        (d/'report.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
    return bool(r['errors'])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--label',required=True);raise SystemExit(run(p.parse_args().label))
