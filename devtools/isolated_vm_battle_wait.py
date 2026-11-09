"""Single-scheduler host transport for bounded original battle wait evidence."""
import argparse
import gzip
import json
from pathlib import Path,PureWindowsPath
import re
from devtools.isolated_windows_vm import ROOT,WORKER,VMX,vmrun,identity
from devtools.isolated_vm_guest_admin import run_script


def preflight_gate(proof,source,current,window_identity):
    if (proof.get('long_capture_preflight_passed')is not True or proof.get('errors')
            or source.get('phase')!='startup_preflight' or source.get('error')is not None
            or proof.get('accepted')is not False):
        raise ValueError('explicit successful bounded preflight capability required; never formal acceptance')
    owner=source['input_isolation']
    if (current['uuid'].lower()!=owner['current_guest_uuid'].lower()
            or current['boot']!=owner['current_guest_boot_utc']
            or (current['cpu'],current['memory'])!=(owner['current_guest_resources']['logical_processors'],
                owner['current_guest_resources']['memory_bytes'])):
        raise ValueError('preflight capability must belong to this exact current guest boot/resources')
    entries=[x for x in source['window_implementations']if PureWindowsPath(x['path']).name=='terminal_battle_wait_window_v2.py']
    if len(entries)!=1 or any(entries[0][k]!=window_identity[k]for k in ('bytes','sha256')):
        raise ValueError('current window collector differs from the native short preflight')
    preparation=source['preparation'];trigger=source['prepared_trigger'];rehearsal=source['trigger_concurrency_preflight']
    window=rehearsal['input_window']
    if not (preparation['begin_ns']<=preparation['end_ns']<=rehearsal['observation_begin_ns']<=trigger['begin_ns']
            <=source['capture_interval']['begin_ns']<=trigger['end_ns']<=rehearsal['observation_end_ns']
            and rehearsal['input_submitted']is False and rehearsal['original_deadline_seconds']==11
            and window['complete']is True and window['maximum_seconds']==11 and 0<window['elapsed_seconds']<11
            and rehearsal['trigger_error']is None and preparation['outside_input_window']is True
            and preparation['ETW_started']is False and preparation['thread_duplicate_created']is False
            and trigger['original_ETW_start_tail_unchanged']is True
            and trigger['live_bytes_rechecked']is True and trigger['fresh_owner_snapshot']is True):
        raise ValueError('actual prepared trigger concurrency must pass the unchanged input deadline')


def authenticate_producers(source,proof):
    names={'terminal_battle_wait_window.py','terminal_battle_wait_window_v2.py','terminal_original_wait_etw.py',
           'terminal_wait_etw_probe.py','terminal_input_window.py'}
    producers=source['window_implementations']
    if (proof.get('window_implementations')!=producers or len(producers)!=len(names)
            or {PureWindowsPath(row['path']).name for row in producers}!=names):
        raise ValueError('exact independently bound complete prepared preflight producer set')
    for row in producers:
        actual=identity(ROOT/'devtools'/PureWindowsPath(row['path']).name)
        if any(actual[k]!=row[k]for k in ('bytes','sha256')):
            raise ValueError('preflight production dependency changed; short native preflight required')


def authenticate_preflight(path,sha):
    from devtools.isolated_vm_guest_admin import STATUS
    if not path or not re.fullmatch('[0-9a-f]{64}',sha or ''):raise ValueError('explicit proof and SHA required before long capture')
    path=Path(path).resolve();got=identity(path)
    if got['sha256']!=sha or got['bytes']>1024*1024:raise ValueError('bounded exact preflight proof')
    proof=json.loads(path.read_text(encoding='utf8'))
    allowed={'terminal_battle_wait_verification.py','terminal_battle_wait_etl.py',
             'terminal_battle_wait_verification_v2.py',
             'terminal_original_wait_etw_verification.py','terminal_wait_etw_probe.py',
             'terminal_school_handoff_verification.py'}
    implementations=proof.get('implementations',[])
    if proof.get('implementations_after')!=implementations or len(implementations)!=len(allowed):
        raise ValueError('complete unchanged independent preflight verifier identities')
    if {PureWindowsPath(x['path']).name for x in implementations}!=allowed:
        raise ValueError('exact preflight verification dependency set')
    for row in implementations:
        current=identity(ROOT/'devtools'/PureWindowsPath(row['path']).name)
        if any(current[k]!=row[k]for k in ('bytes','sha256')):
            raise ValueError('preflight verifier changed; re-decode the retained source first')
    sourcepath=WORKER/PureWindowsPath(proof['source']['path']).name
    etlpath=WORKER/sourcepath.name.removesuffix('.json.gz')/'trace.etl'
    for p,row in ((sourcepath,proof['source']),(etlpath,proof['ETL'])):
        actual=identity(p)
        if any(actual[k]!=row[k]for k in ('bytes','sha256')):raise ValueError('preflight original source/ETL changed')
    with gzip.open(sourcepath,'rb')as f:raw=f.read(8*1024*1024+1)
    if len(raw)>8*1024*1024:raise ValueError('bounded preflight source')
    source=json.loads(raw);current=json.loads(run_script(STATUS))
    authenticate_producers(source,proof)
    preflight_gate(proof,source,current,identity(ROOT/'devtools/terminal_battle_wait_window_v2.py'))
    return dict(proof=got,source=identity(sourcepath),ETL=identity(etlpath),current_guest=current,
                bounded_capture_capability_only=True,formal_acceptance=False)


def authenticate_retention(path,sha,current):
    if not path or not re.fullmatch('[0-9a-f]{64}',sha or ''):raise ValueError('explicit retention preflight and SHA required')
    path=Path(path).resolve();got=identity(path)
    if got['sha256']!=sha or got['bytes']>2*1024*1024:raise ValueError('bounded exact retention preflight')
    with gzip.open(path,'rb')as f:raw=f.read(8*1024*1024+1)
    if len(raw)>8*1024*1024:raise ValueError('bounded expanded retention preflight')
    source=json.loads(raw);probe=source.get('probe')or{};owner=source['input_isolation']
    if (probe.get('retention_capability_passed')is not True or probe.get('error')
            or source['lifecycle'].get('error') or source.get('accepted')is not False
            or len(probe.get('samples',[]))!=8 or not probe.get('workers')
            or probe.get('observer_retention_cleanup',{}).get('closed_observer_handles')!=len(probe['workers'])):
        raise ValueError('actual bounded retention capability required')
    if (current['uuid'].lower()!=owner['current_guest_uuid'].lower() or current['boot']!=owner['current_guest_boot_utc']
            or (current['cpu'],current['memory'])!=(owner['current_guest_resources']['logical_processors'],owner['current_guest_resources']['memory_bytes'])):
        raise ValueError('retention preflight must belong to same current guest boot/resources')
    names={'terminal_worker_retention.py','terminal_worker_retention_v2.py','terminal_worker_retention_v3.py','terminal_worker_retention_preflight.py','terminal_factory_focus.py',
           'terminal_original_wait_etw.py','terminal_school_handoff.py'}
    rows=source['retention_implementations']
    if len(rows)!=len(names) or {PureWindowsPath(x['path']).name for x in rows}!=names:raise ValueError('exact retention implementations')
    for row in rows:
        actual=identity(ROOT/'devtools'/PureWindowsPath(row['path']).name)
        if any(actual[k]!=row[k]for k in ('bytes','sha256')):raise ValueError('retention implementation changed; short preflight required')
    return dict(source=got,retention_capability_only=True,formal_acceptance=False)


def capture(label,phase='startup_preflight',preflight_proof=None,preflight_sha=None,retention_proof=None,retention_sha=None):
    if not re.fullmatch('[a-z0-9-]+',label):raise ValueError('simple fresh label')
    if phase not in ('startup_preflight','retention_preflight','battle_retreat'):raise ValueError('declared phase only')
    stem='terminal-battle-wait-window-'+label
    out=WORKER/(stem+'.json.gz');receipt=WORKER/(stem+'.run.json')
    driver=WORKER/(stem+'-driver.py');log=WORKER/(stem+'.log')
    if any(p.exists()for p in (out,receipt,driver,log,WORKER/stem)):raise ValueError('fresh immutable run required')
    idle="$p=@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'CROSS HERMIT.EXE' -or $_.Name -like 'python*'});if($p.Count){throw 'guest busy'};'idle'"
    if run_script(idle).strip()!='idle':raise ValueError('guest busy before deployment')
    qualification=authenticate_preflight(preflight_proof,preflight_sha)if phase=='battle_retreat'else None
    retention=authenticate_retention(retention_proof,retention_sha,qualification['current_guest'])if qualification else None
    guest=PureWindowsPath('C:/ChaomofaWorker/project');remote=guest/'analysis'/out.name
    remote_driver=PureWindowsPath('C:/ChaomofaWorker')/driver.name;remote_log=remote_driver.parent/log.name
    modules=[ROOT/'devtools'/name for name in ('terminal_battle_wait_window.py','terminal_battle_wait_window_v2.py','terminal_original_wait_etw.py','terminal_wait_etw_probe.py')]
    if phase in ('battle_retreat','retention_preflight'):modules.extend(ROOT/'devtools'/n for n in
        ('terminal_worker_retention.py','terminal_worker_retention_v2.py','terminal_worker_retention_v3.py','terminal_factory_focus.py'))
    if phase=='battle_retreat':modules.append(ROOT/'devtools/terminal_battle_wait_capture.py')
    if phase=='retention_preflight':modules.append(ROOT/'devtools/terminal_worker_retention_preflight.py')
    before=[identity(p)for p in modules]+[identity(Path(__file__))]
    module={'battle_retreat':'devtools.terminal_battle_wait_capture','startup_preflight':'devtools.terminal_battle_wait_window_v2',
            'retention_preflight':'devtools.terminal_worker_retention_preflight'}[phase]
    args=[module,'--out',str(remote)]+([]if phase=='retention_preflight'else['--phase',phase])
    script=('import os,sys,runpy,traceback\nos.chdir('+repr(str(guest))+');sys.path.insert(0,'+repr(str(guest))+')\n'
        'sys.argv='+repr(args)+'\n'
        'with open('+repr(str(remote_log))+',"x",encoding="utf8")as f:\n'
        ' sys.stdout=sys.stderr=f\n'
        ' try:runpy.run_module(sys.argv[0],run_name="__main__")\n'
        ' except BaseException:traceback.print_exc();raise\n')
    with driver.open('x',encoding='utf8')as f:f.write(script)
    result=dict(phase=phase,accepted=False,new_native_lifetime=True,host_input_actions=0,
        sources=before,driver=identity(driver),preflight=qualification,retention_preflight=retention,errors=[])
    try:
        for p in modules:vmrun(['CopyFileFromHostToGuest',VMX,p,guest/'devtools'/p.name],guest=True)
        vmrun(['CopyFileFromHostToGuest',VMX,driver,remote_driver],guest=True)
        vmrun(['runProgramInGuest',VMX,'-activeWindow','-interactive',
            PureWindowsPath('C:/ChaomofaWorker/Python/pythonw.exe'),'-B',remote_driver],
            guest=True,timeout=2400 if phase=='battle_retreat'else 240)
    except Exception as exc:result['errors'].append(str(exc))
    finally:
        for src,dst in ((remote,out),(remote_log,log)):
            try:vmrun(['CopyFileFromGuestToHost',VMX,src,dst],guest=True)
            except Exception as exc:result['errors'].append('retrieve: '+str(exc))
        try:
            if not out.exists()or out.stat().st_size>2*1024*1024:raise ValueError('bounded source required')
            with gzip.open(out,'rb')as f:raw=f.read(8*1024*1024+1)
            if len(raw)>8*1024*1024:raise ValueError('expanded source limit')
            source=json.loads(raw);result['source_report']=identity(out)
            result['observed']=dict(error=source.get('error'),lifecycle_error=source.get('lifecycle',{}).get('error'),
                school_probe_error=source.get('school_probe_error'),
                snapshots=len(source.get('window_snapshots',[])),subject=source.get('subject'),stop_reason=source.get('stop_reason'))
            if phase=='retention_preflight':
                probe=source.get('probe')or{}
                result['observed'].update(error=probe.get('error')or(None if probe.get('retention_capability_passed')else 'retention capability missing'),
                    retention_capability_passed=probe.get('retention_capability_passed'),snapshots=len(probe.get('samples',[])))
            if source.get('ETL'):
                row=source['ETL'];expected=guest/'analysis'/stem/'trace.etl'
                if PureWindowsPath(row['path'])!=expected or not 0<row['bytes']<64*1024*1024:raise ValueError('exact bounded window ETL')
                folder=WORKER/stem;folder.mkdir();local=folder/'trace.etl'
                vmrun(['CopyFileFromGuestToHost',VMX,expected,local],guest=True)
                got=identity(local)
                if any(got[k]!=row[k]for k in ('bytes','sha256')):raise ValueError('ETL transfer identity')
                result['ETL']=got
            if source.get('school_source_reference'):
                row=source['school_source_reference'];expected=guest/'analysis'/(stem+'.school.json.gz')
                if PureWindowsPath(row['path'])!=expected or not 0<row['bytes']<=24*1024*1024:
                    raise ValueError('exact bounded original school history')
                local=WORKER/expected.name
                if local.exists():raise ValueError('school recovery file already exists')
                vmrun(['CopyFileFromGuestToHost',VMX,expected,local],guest=True)
                got=identity(local)
                if any(got[k]!=row[k]for k in ('bytes','sha256')):raise ValueError('original input history transfer identity')
                result['school_source']=got
        except Exception as exc:result['errors'].append('source validation: '+str(exc))
        result['sources_unchanged']=before==[identity(p)for p in modules]+[identity(Path(__file__))]
        with receipt.open('x',encoding='utf8')as f:json.dump(result,f,indent=2)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--label',required=True)
    p.add_argument('--phase',choices=['startup_preflight','retention_preflight','battle_retreat'],default='startup_preflight')
    p.add_argument('--preflight-proof',type=Path);p.add_argument('--preflight-sha')
    p.add_argument('--retention-proof',type=Path);p.add_argument('--retention-sha')
    a=p.parse_args();r=capture(a.label,a.phase,a.preflight_proof,a.preflight_sha,a.retention_proof,a.retention_sha)
    print(json.dumps({k:v for k,v in r.items()if k not in ('sources','driver')},indent=2))
    observed=r.get('observed',{})
    raise SystemExit(1 if r['errors']or not r['sources_unchanged']or not observed or observed.get('error')or observed.get('school_probe_error')or observed.get('lifecycle_error')else 0)
