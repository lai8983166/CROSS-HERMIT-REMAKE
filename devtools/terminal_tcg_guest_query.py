"""Authenticated status and owned WOW64 probe through a QEMU loopback forward."""
import json,sys
from devtools.isolated_vm_bounded_query_v3 import _supervise,runtime_paths
from devtools.isolated_windows_vm import WORKER

UUID='626d1a20-6383-4cd3-85d5-6c9831d6f941'
PORT=15985

def _worker():
    request=json.loads(sys.stdin.readline())
    try:
        import winrm
        secret=json.loads((WORKER/'credentials.private.json').read_bytes())['password']
        session=winrm.Session(f'http://127.0.0.1:{PORT}/wsman',
            auth=('CHAOMOFA-WORKER\\Administrator',secret),transport='ntlm',message_encryption='always',
            operation_timeout_sec=5,read_timeout_sec=7)
        guard="$ErrorActionPreference='Stop';$m=Get-CimInstance Win32_ComputerSystem;$p=Get-CimInstance Win32_ComputerSystemProduct;"
        guard+="if($env:COMPUTERNAME -ne 'CHAOMOFA-WORKER' -or $m.Manufacturer -ne 'QEMU' -or $p.UUID -ne '"+UUID+"'){throw 'Wrong isolated guest'};"
        status="[pscustomobject]@{computer=$env:COMPUTERNAME;manufacturer=$m.Manufacturer;uuid=$p.UUID;cpu=$m.NumberOfLogicalProcessors;memory=$m.TotalPhysicalMemory;boot=(Get-CimInstance Win32_OperatingSystem).LastBootUpTime.ToUniversalTime().ToString('o');explorer=@(Get-Process explorer -ErrorAction SilentlyContinue|Select-Object Id,SessionId);services=@(Get-Service WinRM|Select-Object Name,Status)}|ConvertTo-Json -Depth 4 -Compress"
        if request['action']=='status':script=guard+status
        elif request['action']=='wow64':
            script=guard+"$child=& ($env:windir+'\\SysWOW64\\WindowsPowerShell\\v1.0\\powershell.exe') -NoProfile -NonInteractive -Command '[pscustomobject]@{pointer_bytes=[IntPtr]::Size;process64=[Environment]::Is64BitProcess;os64=[Environment]::Is64BitOperatingSystem;pid=$PID;image=(Get-Process -Id $PID).Path}|ConvertTo-Json -Compress';if($LASTEXITCODE -ne 0){throw 'WOW64 child failed'};$result=$child|ConvertFrom-Json;if(Get-Process -Id $result.pid -ErrorAction SilentlyContinue){throw 'child PID still alive'};$result|Add-Member child_exited $true;$result|Add-Member uuid $p.UUID;$result|ConvertTo-Json -Compress"
        else:raise ValueError('read-only action required')
        value=session.run_ps(script)
        if value.status_code:raise RuntimeError('guest query failed')
        output=value.std_out.decode('utf8').replace(secret,'[redacted]')
        result=dict(ok=True,value=json.loads(output),remote_completion='observed')
    except Exception as exc:result=dict(ok=False,error_type=type(exc).__name__,remote_completion='unknown')
    print(json.dumps(result),flush=True)

def query(action):
    if action not in ('status','wow64'):raise ValueError('action')
    bootstrap='import sys;sys.path[:0]='+repr(runtime_paths())+';from devtools.terminal_tcg_guest_query import _worker;_worker()'
    return _supervise(dict(action=action),18,bootstrap)

if __name__=='__main__':print(json.dumps(query(sys.argv[1])))
