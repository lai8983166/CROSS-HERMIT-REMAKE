"""Guarded dedicated-guest transport for the owned WOW64 heap capability."""
import argparse
import json
from pathlib import Path,PureWindowsPath
import re
from devtools.isolated_windows_vm import ROOT,WORKER,VMX,identity,vmrun
from devtools.isolated_vm_guest_admin import run_script
from devtools.isolated_vm_original_wait_decode import checked_artifact,transferred,restore_guest_artifact


def run(label,source_label=None):
    if not re.fullmatch('[a-z0-9-]+',label)or(source_label is not None and not re.fullmatch('[a-z0-9-]+',source_label)):
        raise ValueError('explicit simple fresh labels')
    stem='terminal-heap-'+label;out=WORKER/(stem+'.json');log=WORKER/(stem+'.log')
    driver=WORKER/(stem+'-driver.py');receipt=WORKER/(stem+'.run.json')
    if any(p.exists()for p in (out,log,driver,receipt,WORKER/stem)):raise ValueError('fresh heap capability output')
    idle="$p=@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'CROSS HERMIT.EXE' -or $_.Name -like 'python*' -or $_.Name -eq 'heap-fixture.exe'});if($p.Count){throw 'guest busy'};'idle'"
    if run_script(idle).strip()!='idle':raise ValueError('guest busy before any deployment')
    guest=PureWindowsPath('C:/ChaomofaWorker/project');remote=guest/'analysis'/out.name
    remote_driver=PureWindowsPath('C:/ChaomofaWorker')/driver.name;remote_log=remote_driver.parent/log.name
    modules=[ROOT/'devtools'/n for n in ('terminal_heap_etw_probe.py','terminal_heap_etw_probe_v2.py','terminal_heap_etw_helper.cs','terminal_wait_etw_probe.py')]
    paths=modules+[Path(__file__)];before=[identity(p)for p in paths];inputs=[]
    args=['devtools.terminal_heap_etw_probe_v2','--out',str(remote)]
    if source_label is not None:
        source=WORKER/('terminal-heap-'+source_label+'.json');source_data=json.loads(source.read_bytes())
        etl=source.with_suffix('')/'trace.etl';sid=identity(source);eid=identity(etl)
        if sid['bytes']>65536 or eid['bytes']>4*1024*1024:raise ValueError('bounded retained helper source')
        guest_etl=guest/'analysis'/source.stem/'trace.etl'
        checked_artifact(source_data['ETL'],guest_etl,4*1024*1024);transferred(source_data['ETL'],etl)
        inputs=[restore_guest_artifact(source,guest/'analysis'/source.name,sid),restore_guest_artifact(etl,guest_etl,eid)]
        args+=['--decode','--source',str(guest/'analysis'/source.name),'--source-sha',sid['sha256'],
               '--etl',str(guest_etl),'--etl-sha',eid['sha256']]
    script=('import os,sys,runpy,traceback\nos.chdir('+repr(str(guest))+');sys.path.insert(0,'+repr(str(guest))+')\n'
        'sys.argv='+repr(args)+'\nwith open('+repr(str(remote_log))+',"x",encoding="utf8")as f:\n'
        ' sys.stdout=sys.stderr=f\n try:runpy.run_module(sys.argv[0],run_name="__main__")\n'
        ' except SystemExit as exc:\n  print("diagnostic_exit",exc.code)\n  if exc.code!=2:raise\n'
        ' except BaseException:traceback.print_exc();raise\n')
    with driver.open('x',encoding='utf8')as f:f.write(script)
    result=dict(accepted=False,host_input_actions=0,original_game=False,source_label=source_label,
        implementations=before,driver=identity(driver),inputs=inputs,errors=[],expected_diagnostic_exit=2)
    try:
        for p in modules:vmrun(['CopyFileFromHostToGuest',VMX,p,guest/'devtools'/p.name],guest=True)
        vmrun(['CopyFileFromHostToGuest',VMX,driver,remote_driver],guest=True)
        vmrun(['runProgramInGuest',VMX,'-interactive',PureWindowsPath('C:/ChaomofaWorker/Python/pythonw.exe'),'-B',remote_driver],guest=True,timeout=90)
    except Exception as exc:result['errors'].append(str(exc))
    finally:
        for remote_path,local in ((remote,out),(remote_log,log)):
            try:vmrun(['CopyFileFromGuestToHost',VMX,remote_path,local],guest=True)
            except Exception as exc:result['errors'].append('retrieve: '+str(exc))
        try:
            if not out.is_file()or out.stat().st_size>65536:raise ValueError('bounded helper report required')
            data=json.loads(out.read_bytes());result['report']=identity(out)
            result['observed']={k:data.get(k)for k in ('status','errors','elapsed_seconds','accepted','PTDcleanup')}
            if source_label is None:
                folder=WORKER/stem;folder.mkdir()
                for key,name,limit in (('ETL','trace.etl',4*1024*1024),('helper_executable','heap-fixture.exe',1024*1024)):
                    if key not in data:continue
                    expected=remote.with_suffix('')/name;checked_artifact(data[key],expected,limit)
                    vmrun(['CopyFileFromGuestToHost',VMX,expected,folder/name],guest=True)
                    result[key]=transferred(data[key],folder/name)
        except Exception as exc:result['errors'].append('validation: '+str(exc))
        result['implementations_unchanged']=before==[identity(p)for p in paths]
        with receipt.open('x',encoding='utf8')as f:json.dump(result,f,indent=2)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--label',required=True);p.add_argument('--source-label');a=p.parse_args()
    r=run(a.label,a.source_label);print(json.dumps({k:v for k,v in r.items()if k not in ('implementations','inputs')},indent=2))
    raise SystemExit(1 if r['errors']or r.get('observed',{}).get('errors')or not r['implementations_unchanged']else 0)
