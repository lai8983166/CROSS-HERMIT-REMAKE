"""Offline bounded battle-window ETL decode; existing native inputs only."""
import argparse
import gzip
import json
from pathlib import Path,PureWindowsPath
import re
from devtools.isolated_windows_vm import ROOT,WORKER,VMX,vmrun,identity
from devtools.isolated_vm_guest_admin import run_script
from devtools.isolated_vm_original_wait_decode import restore_guest_artifact,transferred,checked_artifact


def decode(label,source_label,diagnostic_only=False,verification_version=1):
    if verification_version not in (1,2,3,4):raise ValueError('explicit bounded verifier version')
    if not all(re.fullmatch('[a-z0-9-]+',x)for x in (label,source_label)):raise ValueError('simple unique labels')
    stem='terminal-battle-wait-decode-'+label;source_stem='terminal-battle-wait-window-'+source_label
    out=WORKER/(stem+'.json');receipt=WORKER/(stem+'.run.json');records=WORKER/(stem+'.records.json.gz')
    driver=WORKER/(stem+'-driver.py');log=WORKER/(stem+'.log')
    if any(p.exists()for p in (out,receipt,records,driver,log)):raise ValueError('fresh immutable offline outputs')
    source=WORKER/(source_stem+'.json.gz');etl=WORKER/source_stem/'trace.etl'
    sid,eid=identity(source),identity(etl)
    if sid['bytes']>2*1024*1024 or not 0<eid['bytes']<64*1024*1024:raise ValueError('bounded existing native source/ETL')
    with gzip.open(source,'rb')as f:raw=f.read(8*1024*1024+1)
    if len(raw)>8*1024*1024:raise ValueError('bounded expanded source')
    data=json.loads(raw);guest=PureWindowsPath('C:/ChaomofaWorker/project')
    checked_artifact(data['ETL'],guest/'analysis'/source_stem/'trace.etl',64*1024*1024)
    transferred(data['ETL'],etl)
    idle="$p=@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'CROSS HERMIT.EXE' -or $_.Name -like 'python*'});if($p.Count){throw 'guest busy'};'idle'"
    if run_script(idle).strip()!='idle':raise ValueError('guest busy before offline deployment')
    inputs=[restore_guest_artifact(source,guest/'analysis'/source.name,sid),
            restore_guest_artifact(etl,guest/'analysis'/source_stem/'trace.etl',eid)]
    if data.get('school_source_reference'):
        row=data['school_source_reference'];expected=guest/'analysis'/(source_stem+'.school.json.gz')
        checked_artifact(row,expected,24*1024*1024)
        path=WORKER/expected.name;transferred(row,path)
        inputs.append(restore_guest_artifact(path,expected,row))
    modules=[ROOT/'devtools'/n for n in ('terminal_battle_wait_verification.py','terminal_battle_wait_etl.py',
        'terminal_original_wait_etw_verification.py','terminal_wait_native_verification.py')]
    if verification_version>=2:modules.append(ROOT/'devtools/terminal_battle_wait_verification_v2.py')
    if verification_version>=3:modules.extend(ROOT/'devtools'/name for name in
        ('terminal_battle_wait_etl_v2.py','terminal_battle_wait_verification_v3.py'))
    if verification_version==4:modules.append(ROOT/'devtools/terminal_battle_wait_verification_v4.py')
    before=[identity(p)for p in modules]
    module='devtools.terminal_battle_wait_verification'+('_v'+str(verification_version)if verification_version>=2 else '')
    args=[module,'--source',str(guest/'analysis'/source.name),
        '--source-sha',sid['sha256'],'--etl',str(guest/'analysis'/source_stem/'trace.etl'),'--etl-sha',eid['sha256'],
        '--out',str(guest/'analysis'/out.name)]+(['--diagnostic-only']if diagnostic_only else [])
    remote_driver=PureWindowsPath('C:/ChaomofaWorker')/driver.name;remote_log=remote_driver.parent/log.name
    script=('import os,sys,runpy,traceback\nos.chdir('+repr(str(guest))+');sys.path.insert(0,'+repr(str(guest))+')\n'
        'sys.argv='+repr(args)+'\nwith open('+repr(str(remote_log))+',"x",encoding="utf8")as f:\n'
        ' sys.stdout=sys.stderr=f\n try:runpy.run_module(sys.argv[0],run_name="__main__")\n'
        ' except BaseException:traceback.print_exc();raise\n')
    with driver.open('x',encoding='utf8')as f:f.write(script)
    result=dict(source=sid,ETL=eid,implementations=before,driver=identity(driver),guest_inputs=inputs,
        diagnostic_only=diagnostic_only,verification_version=verification_version,
        accepted=False,new_native_capture=False,host_input_actions=0,errors=[])
    try:
        for p in modules:vmrun(['CopyFileFromHostToGuest',VMX,p,guest/'devtools'/p.name],guest=True)
        vmrun(['CopyFileFromHostToGuest',VMX,driver,remote_driver],guest=True)
        vmrun(['runProgramInGuest',VMX,'-activeWindow','-interactive',
            PureWindowsPath('C:/ChaomofaWorker/Python/pythonw.exe'),'-B',remote_driver],guest=True,timeout=240)
    except Exception as exc:result['errors'].append(str(exc))
    finally:
        for src,dst in ((guest/'analysis'/out.name,out),(remote_log,log)):
            try:vmrun(['CopyFileFromGuestToHost',VMX,src,dst],guest=True)
            except Exception as exc:result['errors'].append('retrieve: '+str(exc))
        try:
            if not out.exists()or out.stat().st_size>1024*1024:raise ValueError('bounded decoder report required')
            report=json.loads(out.read_text(encoding='utf8'));result['report']=identity(out)
            result['result']={k:report.get(k)for k in ('status','phase','errors','elapsed_seconds',
                'total_records','retained_subject_records','process_trace_status','close_trace_status','long_capture_preflight_passed')}
            if report.get('selected_records'):
                row=report['selected_records'];expected=guest/'analysis'/records.name
                checked_artifact(row,expected,2*1024*1024 if verification_version>=3 else 512*1024)
                vmrun(['CopyFileFromGuestToHost',VMX,expected,records],guest=True)
                result['selected_records']=transferred(row,records)
        except Exception as exc:result['errors'].append('decode validation: '+str(exc))
        result['implementations_unchanged']=before==[identity(p)for p in modules]
        result['inputs_unchanged']=(sid,eid)==(identity(source),identity(etl))
        with receipt.open('x',encoding='utf8')as f:json.dump(result,f,indent=2)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--label',required=True);p.add_argument('--source-label',required=True)
    p.add_argument('--diagnostic-only',action='store_true');p.add_argument('--verification-version',type=int,choices=(1,2,3,4),default=1)
    a=p.parse_args()
    r=decode(a.label,a.source_label,a.diagnostic_only,a.verification_version)
    print(json.dumps({k:v for k,v in r.items()if k not in ('implementations','driver','guest_inputs')},indent=2))
    raise SystemExit(1 if r['errors']or r.get('result',{}).get('errors')or not r['implementations_unchanged']or not r['inputs_unchanged']else 0)
