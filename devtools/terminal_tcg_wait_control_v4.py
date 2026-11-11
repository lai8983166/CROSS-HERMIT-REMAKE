"""Bounded authenticated owned wait-fixture requests and output continuation."""
import base64,argparse,hashlib,json,os,re,sys,time
from pathlib import Path
from devtools.isolated_windows_vm import WORKER
from devtools.isolated_vm_bounded_query_v3 import _supervise,runtime_paths

def _worker():
    req=json.loads(sys.stdin.readline());events=[]
    try:
        if not re.fullmatch(r'tcg-wait-native-v\d+',req['case']):raise ValueError('case')
        case=WORKER/req['case']
        if not(case/'vm-ready.json').exists()or(case/'vm-stop').exists()or(case/'report.json').exists():raise ValueError('current VM required')
        import winrm
        secret=json.loads((WORKER/'credentials.private.json').read_bytes())['password']
        session=winrm.Session('http://127.0.0.1:15985/wsman',auth=('CHAOMOFA-WORKER\\Administrator',secret),
            transport='ntlm',message_encryption='always',operation_timeout_sec=20,read_timeout_sec=30)
        from devtools.terminal_winrm_output import receive
        session.protocol.get_command_output=lambda shell,command:receive(session.protocol,case,shell,command)
        if req['mode']=='run':
            if not re.fullmatch('[a-z0-9-]+\\.ps1',req['name']):raise ValueError('script name')
            path=case/req['name'];raw=path.read_bytes()
            if hashlib.sha256(raw).hexdigest()!=req['sha256']:raise ValueError('script identity')
            phase=case/('phase-'+path.stem+'-'+str(os.getpid())+'.json')
            def wrap(name,original):
                def call(*args,**kwargs):
                    row=dict(method=name,start=time.monotonic());events.append(row);phase.write_text(json.dumps(events))
                    value=original(*args,**kwargs);row['end']=time.monotonic()
                    if name in ('open_shell','run_command'):row['owned_id']=value
                    phase.write_text(json.dumps(events));return value
                return call
            for name in ('open_shell','run_command','send_command_input','get_command_output','cleanup_command','close_shell'):
                setattr(session.protocol,name,wrap(name,getattr(session.protocol,name)))
            guard="$ErrorActionPreference='Stop';$m=Get-CimInstance Win32_ComputerSystem;$p=Get-CimInstance Win32_ComputerSystemProduct;if($env:COMPUTERNAME -ne 'CHAOMOFA-WORKER' -or $m.Manufacturer -ne 'QEMU' -or $p.UUID -ne '626d1a20-6383-4cd3-85d5-6c9831d6f941'){throw 'Wrong guest'};"
            shell=session.protocol.open_shell();boot="$s=[Console]::In.ReadToEnd();Invoke-Expression ([Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($s)))";command=session.protocol.run_command(shell,'powershell.exe',['-NoLogo','-NoProfile','-NonInteractive','-EncodedCommand',base64.b64encode(boot.encode('utf-16-le')).decode()]);session.protocol.send_command_input(shell,command,base64.b64encode(guard.encode()+raw),end=True);out,err,code=session.protocol.get_command_output(shell,command);session.protocol.cleanup_command(shell,command);session.protocol.close_shell(shell)
        elif req['mode']=='resume':
            if not re.fullmatch(r'phase-[a-z0-9-]+-\d+\.json',req['name']):raise ValueError('phase name')
            raw=(case/req['name']).read_bytes()
            if hashlib.sha256(raw).hexdigest()!=req['sha256']:raise ValueError('phase identity')
            rows=json.loads(raw)
            if [x['method']for x in rows] not in (['open_shell','run_command','send_command_input'],['open_shell','run_command','send_command_input','get_command_output']) or 'end' in rows[-1]:raise ValueError('pending command required')
            ids=[rows[i]['owned_id']for i in (0,1)]
            if any(not re.fullmatch('[A-Fa-f0-9-]{36}',s)for s in ids):raise ValueError('owned ids')
            out,err,code=session.protocol.get_command_output(*ids)
            session.protocol.cleanup_command(*ids);session.protocol.close_shell(ids[0])
        else:raise ValueError('mode')
        if code:
            result=dict(ok=False,status_code=code,diagnostic=err.decode('utf8',errors='replace').replace(secret,'[redacted]')[:4096],remote_completion='observed')
        else:result=dict(ok=True,value=json.loads(out.decode('utf8')),remote_completion='observed',command_and_shell_closed=True)
    except Exception as exc:result=dict(ok=False,error_type=type(exc).__name__,diagnostic=str(exc).replace(secret,'[redacted]')[:2048] if 'secret' in locals() else '',remote_completion='unknown')
    print(json.dumps(result),flush=True)

def request(case,name,mode):
    path=case/name;payload=dict(case=case.name,name=name,mode=mode,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    bootstrap='import sys;sys.path[:0]='+repr(runtime_paths())+';from devtools.terminal_tcg_wait_control_v4 import _worker;_worker()'
    return _supervise(payload,55,bootstrap)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('case',type=Path);p.add_argument('name');p.add_argument('--resume',action='store_true')
    a=p.parse_args();print(json.dumps(request(a.case,a.name,'resume'if a.resume else'run')))
