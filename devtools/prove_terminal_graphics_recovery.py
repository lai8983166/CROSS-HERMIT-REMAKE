"""Bounded real process watchdog tests; all desktop values are explicit models."""
from __future__ import annotations
import argparse,hashlib,json,os,subprocess,sys,time
from pathlib import Path
from devtools.terminal_graphics_recovery import RecoverySession,ROOT,folder_path,read,need,publish

def identity(path):
    b=path.read_bytes();return dict(path=path.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())

def check_containment(report):
    c=report['cleanup'];need(report['assigned_before_resume'] and c['job_empty'] and c['handles_closed'] and not c['errors'] and report['controller_handle_closed'],'observed suspended assignment, exact Job empty and handles closed')
    need(all(x['wait']==0 and x.get('code')!=259 for x in c['exits'].values()),'actual retained process exits')
    need(report['native_desktop_calls']==0 and report['desktop_restored'] is False,'no OS desktop recovery success claim')

def existing_case(folder,scenario):
    cfg=read(folder/'config.json');need(cfg['implementation_sha256']==identity(ROOT/'devtools/terminal_graphics_recovery.py')['sha256'] and cfg['backend']=='model' and cfg['scenario']==scenario,'unchanged collector/input semantics for explicit evidence reuse')
    r=read(folder/'supervisor-result.json');check_containment(r)
    for cmd in r['commands']:
        from devtools.terminal_graphics_recovery import digest
        q=read(folder/f'request-{cmd["seq"]}.json');arm=read(folder/f'armed-{cmd["seq"]}.json')
        need(q['token']==arm['token']==cfg['token'] and digest(q)==arm['request_sha256']==cmd['request_sha256'],'reused exact request/arm source')
        response=folder/f'response-{cmd["seq"]}.json'
        if response.exists():
            v=read(response);need(v['request_sha256']==digest(q) and v['token']==cfg['token'] and v['seq']==q['seq'] and v['completed_ns']<=arm['deadline_ns'],'reused complete timely response')
    if scenario=='normal':
        a=read(folder/'response-1.json');b=read(folder/'response-2.json');need(a['ok'] and b['ok'] and b['value']['restored'] and a['worker_pid']==b['worker_pid'] and r['normal_close'],'reused persistent observer and normal cleanup')
        return dict(case='normal_persistent_observer',passed=True,reused_completed_case=True,worker_pid=a['worker_pid'],model_recovery_checks=b['value']['checks'],supervisor=r)
    expected='worker_exited' if scenario=='exit_during_write' else 'command_deadline';need(r['reason']==expected and not r['normal_close'],'reused failure remains failure')
    journal=[json.loads(x)for x in (folder/'operations.jsonl').read_text().splitlines()];need(journal[-1]['phase']=='begin','reused last interrupted operation')
    if scenario=='exit_during_write':need(any(x.get('code')==37 for x in r['cleanup']['exits'].values()),'reused actual exit37')
    else:need(r['cleanup']['forced'] and 0<=r['finished_ns']-r['commands'][-1]['deadline_ns']<1_000_000_000,'reused external hard deadline')
    return dict(case=scenario,passed=True,reused_completed_case=True,controller_held_seconds=2,actual_native_wait=scenario!='exit_during_write',last_operation=journal[-1],supervisor=r)

def prove(folder,resume=False):
    folder=folder_path(folder);need(resume or not folder.exists(),'fresh bounded watchdog evidence')
    if not folder.exists():folder.mkdir()
    cases=[]
    if (folder/'normal').exists():cases.append(existing_case(folder/'normal','normal'))
    else:
        s=RecoverySession(folder/'normal')
        try:
            a=s.call('baseline');b=s.call('recover');need(a['ok'] and b['ok'] and b['value']['restored'],'same process successful frozen recovery model')
            need(a['worker_pid']==b['worker_pid'],'one observer process across baseline and restoration')
        finally:r=s.finish()
        check_containment(r);need(r['normal_close'] and s.process.returncode==0 and r['reason']=='worker_exited' and not r['cleanup']['forced'] and all(x['code']==0 for x in r['cleanup']['exits'].values()),'normal observer exits naturally')
        cases.append(dict(case='normal_persistent_observer',passed=True,worker_pid=a['worker_pid'],model_recovery_checks=b['value']['checks'],supervisor=r))
    for scenario in ('block_baseline','block_recovery_read','block_gamma_write','exit_during_write'):
        if (folder/scenario).exists():cases.append(existing_case(folder/scenario,scenario));continue
        s=RecoverySession(folder/scenario,scenario=scenario);command=None;observed=None
        try:
            if scenario!='block_baseline':s.call('baseline')
            command=s.request('baseline' if scenario=='block_baseline' else 'recover',1000)
            # Deliberately stop supervising in this controller. The separate
            # process must finish containment before the controller wakes.
            time.sleep(2)
            observed=read(s.folder/'supervisor-result.json')
            try:s.collect(command)
            except TimeoutError:pass
            else:raise AssertionError('blocked or exited worker returned restoration success')
        finally:r=s.finish()
        check_containment(r)
        need(not r['normal_close'] and s.process.returncode!=0,'worker failure never becomes supervisor exit0')
        expected='worker_exited' if scenario=='exit_during_write' else 'command_deadline'
        need(r['reason']==expected and observed==r,'independent supervisor reached expected failure before controller resumed')
        journal=[json.loads(x)for x in (s.folder/'operations.jsonl').read_text().splitlines()]
        need(journal and journal[-1]['phase']=='begin','last begun observation/write preserved on abrupt exit')
        if scenario=='exit_during_write':need(any(x.get('code')==37 for x in r['cleanup']['exits'].values()),'real worker exit37 observed')
        else:
            arm=r['commands'][-1];need(0<=r['finished_ns']-arm['deadline_ns']<1_000_000_000,'external hard deadline plus observed containment under1s')
            need(r['cleanup']['forced'],'blocked kernel wait was contained')
        cases.append(dict(case=scenario,passed=True,controller_held_seconds=2,actual_native_wait=scenario!='exit_during_write',last_operation=journal[-1],supervisor=r))
    s=RecoverySession(folder/'session_deadline',lifetime_seconds=1)
    try:
        s.call('baseline');time.sleep(1.4);r=s.finish()
    finally:
        if not s.finished:s.finish()
    check_containment(r);need(r['reason']=='session_deadline','idle persistent observer bounded too');cases.append(dict(case='session_deadline',passed=True,supervisor=r))
    orphan=folder/'controller_exited'
    p=subprocess.Popen([sys.executable,'-B','-X','utf8','-m','devtools.prove_terminal_graphics_recovery','--orphan',str(orphan)],cwd=ROOT,env=dict(os.environ,TEMP=str(folder),TMP=str(folder)),stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=subprocess.CREATE_NO_WINDOW)
    need(p.wait(timeout=8)==42,'owned controller exited without cleanup')
    until=time.monotonic()+4
    while not (orphan/'supervisor-result.json').exists() and time.monotonic()<until:time.sleep(.02)
    r=read(orphan/'supervisor-result.json');check_containment(r);need(r['reason']=='controller_exited','retained controller handle death triggers containment');cases.append(dict(case='controller_exited',passed=True,supervisor=r))
    native_rejected=False
    try:RecoverySession(folder/'forbidden-native',backend='native')
    except ValueError as exc:native_rejected='native recovery admission' in str(exc)
    need(native_rejected and not (folder/'forbidden-native').exists(),'native admission fails before creating process or directory')
    files=[identity(p)for p in sorted(folder.rglob('*')) if p.is_file()];need(sum(x['bytes']for x in files)<1024*1024,'all watchdog case evidence within1MiB')
    return dict(kind='external_recovery_watchdog_preflight',accepted=True,native_desktop_calls=0,native_game_runs=0,model_desktop_only=True,real_kernel_process_tests=True,native_admission=False,formal_acceptance=False,formal_progress='2/8',implementation=[identity(ROOT/p)for p in ('devtools/terminal_graphics_recovery.py','devtools/prove_terminal_graphics_recovery.py','devtools/terminal_graphics_desktop.py','devtools/terminal_oplock.py','devtools/terminal_oplock_probe_v2.py')],cases=cases,native_gate_rejected_before_launch=True,evidence=files,evidence_bytes=sum(x['bytes']for x in files),limits=dict(command_ms={'baseline':5000,'recover':20000,'close':5000},session_seconds=120,containment_reserve_seconds=3,message_bytes=262144,commands=8),limitations=['The hung calls are real kernel Sleep(INFINITE) in owned processes, not an actual stuck display driver.','External process termination bounds the worker lifetime; an OS or driver that refuses process termination remains a reported containment failure.','A timeout preserves the last begun read/write and never asserts that desktop changes were cancelled or restored.','The same worker runs baseline and final reads; model state is symbolic and no Windows graphics/input/shell API was invoked.','Native entry remains closed until authentic owner/release/mutation evidence, actual adapter mapping and a qualified bounded GAME runner are connected.'])

def orphan(folder):
    s=RecoverySession(folder,scenario='block_gamma_write');s.call('baseline');s.request('recover',5000);until=time.monotonic()+4
    while time.monotonic()<until:
        p=s.folder/'operations.jsonl'
        if p.exists() and 'write:gamma' in p.read_text():os._exit(42)
        time.sleep(.01)
    s.finish();return 43

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--folder');p.add_argument('--out');p.add_argument('--orphan');p.add_argument('--resume',action='store_true');a=p.parse_args()
    if a.orphan:raise SystemExit(orphan(a.orphan))
    need(a.folder and a.out,'bounded folder and fresh report required');r=prove(a.folder,a.resume);out=(ROOT/a.out).resolve();need(out.is_relative_to(ROOT/'analysis'),'F small report');publish(out,r);print(json.dumps(dict(report=identity(out),cases=len(r['cases']),local_evidence_bytes=r['evidence_bytes'])))
