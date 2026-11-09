"""Run/retrieve one short original wait observation in the dedicated guest."""
import argparse
import gzip
import json
from pathlib import PureWindowsPath, Path
import re
from devtools.isolated_windows_vm import ROOT, WORKER, VMX, vmrun, identity
from devtools.isolated_vm_guest_admin import run_script


def capture(label):
    if not re.fullmatch('[a-z0-9-]+',label):
        raise ValueError('simple unique label')
    stem = 'terminal-original-wait-'+label
    out = WORKER/(stem+'.json.gz'); receipt = WORKER/(stem+'.run.json')
    if out.exists() or receipt.exists():
        raise ValueError('immutable fresh observation required')
    guard = "$p=@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'CROSS HERMIT.EXE' -or $_.Name -like 'python*'});if($p.Count){throw 'guest busy'};'idle'"
    if run_script(guard).strip() != 'idle':
        raise ValueError('guest not idle before deploying sources')
    guest = PureWindowsPath('C:/ChaomofaWorker/project')
    remote = guest/'analysis'/out.name
    log = PureWindowsPath('C:/ChaomofaWorker')/(stem+'.log')
    names = ('terminal_original_wait_etw.py','terminal_wait_etw_probe.py',
             'isolated_guest_focus.py','isolated_guest_dep_observer.py','native_input_isolation.py')
    sources = [ROOT/'devtools'/n for n in names]
    before = [identity(p) for p in sources]+[identity(Path(__file__))]
    driver = WORKER/(stem+'-driver.py'); remote_driver = log.parent/driver.name
    script = ('import os,sys,runpy,traceback\nos.chdir('+repr(str(guest))+');sys.path.insert(0,'+repr(str(guest))+')\n'
        'sys.argv='+repr(['devtools.terminal_original_wait_etw','--out',str(remote)])+'\n'
        'with open('+repr(str(log))+',"x",encoding="utf8")as f:\n'
        ' sys.stdout=sys.stderr=f\n'
        ' try:runpy.run_module("devtools.terminal_original_wait_etw",run_name="__main__")\n'
        ' except BaseException:traceback.print_exc();raise\n')
    with driver.open('x',encoding='utf8') as f:f.write(script)
    result = dict(accepted=False,sources=before,driver=identity(driver),errors=[],host_input_actions=0)
    try:
        for p in sources:
            vmrun(['CopyFileFromHostToGuest',VMX,p,guest/'devtools'/p.name],guest=True)
        vmrun(['CopyFileFromHostToGuest',VMX,driver,remote_driver],guest=True)
        vmrun(['runProgramInGuest',VMX,'-activeWindow','-interactive',
               PureWindowsPath('C:/ChaomofaWorker/Python/pythonw.exe'),'-B',remote_driver],guest=True,timeout=240)
    except Exception as exc:
        result['errors'].append(str(exc))
    finally:
        for source,target in ((remote,out),(log,WORKER/log.name)):
            try:vmrun(['CopyFileFromGuestToHost',VMX,source,target],guest=True)
            except Exception as exc:result['errors'].append('retrieve: '+str(exc))
        try:
            if out.exists():
                report = json.loads(gzip.decompress(out.read_bytes()))
                result['source_report'] = identity(out)
                result['observed'] = dict(error=report.get('error'),lifecycle_error=report['lifecycle']['error'],
                    forced_cleanup=report['lifecycle']['lifetime']['forced_termination'],subject=report.get('subject'))
                if report.get('ETL'):
                    row = report['ETL']; gp = PureWindowsPath(row['path'])
                    if gp != guest/'analysis'/stem/'trace.etl' or not 0 < row['bytes'] <= 4*1024*1024:
                        raise ValueError('bounded exact guest ETL only')
                    folder = WORKER/stem; folder.mkdir()
                    local = folder/'trace.etl'
                    vmrun(['CopyFileFromGuestToHost',VMX,gp,local],guest=True)
                    got = identity(local)
                    if any(got[k] != row[k] for k in ('bytes','sha256')):
                        raise ValueError('transferred ETL identity')
                    result['ETL'] = got
        except Exception as exc:
            result['errors'].append('source/artifact validation: '+str(exc))
        result['sources_unchanged'] = before == [identity(p) for p in sources]+[identity(Path(__file__))]
        with receipt.open('x',encoding='utf8') as f:json.dump(result,f,indent=2)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--label',required=True)
    args=p.parse_args();r=capture(args.label)
    print(json.dumps({k:v for k,v in r.items() if k not in ('sources','driver')},indent=2))
    raise SystemExit(1 if r['errors'] or not r['sources_unchanged'] else 0)
