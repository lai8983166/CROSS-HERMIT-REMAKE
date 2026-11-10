"""Four bounded own-fixture kernel returns through the installed SDK KD client.

Development evidence only: the kernel trap is not complete user postreturn state.
No game launch, user breakpoint, code patch, or host desktop input.
"""
import concurrent.futures as cf
import json
from pathlib import Path, PureWindowsPath
import re
import subprocess
import time
from devtools.isolated_windows_vm import WORKER, VMX, environment, identity
from devtools.isolated_vm_kd import PIPE, validate_kd_vmx, run_guest
from devtools.isolated_vm_guest_admin import STATUS


def need(value, message):
    if not value:
        raise ValueError(message)


def main():
    d = WORKER/'kd-worker'
    out, log = d/'cli-wait-v1.json', d/'cli-wait-v1.log'
    need(not out.exists() and not log.exists(), 'fresh bounded output')
    validate_kd_vmx(VMX.read_text(encoding='utf8'))
    folder = WORKER/'vm-wait-fixture-v1-20261110'
    guest = PureWindowsPath('C:/ChaomofaWorker/kd-cli-wait-v1-20261110')
    q = str(guest)
    r = dict(accepted=False, fullstate=False, fullABI=False, original_game_started=False,
             host_input_actions=0, errors=[])
    exe = Path('C:/Program Files (x86)/Windows Kits/10/Debuggers/x64/kd.exe')
    pool = cf.ThreadPoolExecutor(max_workers=1)
    p = launch = None
    t = time.monotonic()
    try:
        r['guest_before'] = json.loads(run_guest(STATUS))
        need(r['guest_before']['boot'] == '2026-11-10T01:00:17.5000000Z', 'reviewed current boot')
        run_guest("if(@(Get-Process 'CROSS HERMIT',python,pythonw,helper,fixture -ErrorAction SilentlyContinue).Count){throw 'busy'};if(Test-Path -LiteralPath '"+q+"'){throw 'fresh'};New-Item -ItemType Directory -Path '"+q+"'|Out-Null;'ready'")
        for name in ('fixture.bin','fixture.exe','manifest.json','terminal_vm_wait_fixture.cs'):
            vmrun_copy = __import__('devtools.isolated_windows_vm',fromlist=['vmrun']).vmrun
            vmrun_copy(['CopyFileFromHostToGuest',VMX,folder/name,guest/name],guest=True)
        run_guest(';'.join("[IO.File]::WriteAllText('"+q+'\\ack-'+str(i)+"','continue')"for i in range(4))+";'acks ready'")
        command = "$p=Start-Process -FilePath '"+q+"\\fixture.exe' -ArgumentList @('--owned-vmm-fixture','"+q+"') -WindowStyle Hidden -PassThru;if(!$p.WaitForExit(150000)){throw 'bounded fixture lifespan'};[pscustomobject]@{exit_code=$p.ExitCode;result=if(Test-Path -LiteralPath '"+q+"\\result.json'){Get-Content -LiteralPath '"+q+"\\result.json' -Raw|ConvertFrom-Json}else{$null}}|ConvertTo-Json -Depth 10 -Compress"
        launch = pool.submit(run_guest,command)
        ready_command="$end=[DateTime]::UtcNow.AddSeconds(10);while(!(Test-Path -LiteralPath '"+q+"\\ready.json')){if([DateTime]::UtcNow -gt $end){throw 'ready deadline'};Start-Sleep -Milliseconds 50};Get-Content -LiteralPath '"+q+"\\ready.json' -Raw"
        ready=json.loads(run_guest(ready_command));r['ready']=ready
        need(ready['source_sha256']==identity(folder/'terminal_vm_wait_fixture.cs')['sha256'],'fixture source identity')
        r['modules']=json.loads(run_guest("@((Get-Process -Id "+str(ready['pid'])+").Modules|Where-Object {$_.ModuleName -ieq 'wow64cpu.dll'}|ForEach-Object {[pscustomobject]@{name=$_.ModuleName;path=$_.FileName;base=$_.BaseAddress.ToInt64();size=$_.ModuleMemorySize;sha256=(Get-FileHash -LiteralPath $_.FileName -Algorithm SHA256).Hash}})|ConvertTo-Json -Compress"))
        module=r['modules'][0]if isinstance(r['modules'],list)else r['modules']
        need(module['sha256'].lower()=='6d3e9d039c22b58c577435ef0209d43668ef2003e284be9980e4ad1289045a66','actual loaded WOW64 CPU module')
        r['kernel_sha256']=run_guest('(Get-FileHash C:\\Windows\\System32\\ntoskrnl.exe -Algorithm SHA256).Hash').strip().lower()
        need(r['kernel_sha256']=='5669b9b8bfcf20f08b7d1d65dc2deccbf836279c0e3f66722d72ad33ee7f672a','reviewed kernel bytes')
        count=ready['data']+0x200
        body='.echo OWNED_WAIT_BEGIN;r;? @$tpid;? @$tid;dq @rsp L20;dq @rbp-0x80 L32;dq %x L1;u poi(@rbp+0xe8)-2 L8;.echo OWNED_WAIT_END;.if (dwo(%x) == 3) { bc *;bl;.echo OWNED_FOUR_COMPLETE;gc } .else { gc }'%(count,count)
        condition='.if (@$tpid == 0x%x) { .if (@$tid == 0x%x) { .if (poi(@rbp-0x48) == 0x%x) { %s } .else { gc } } .else { gc } } .else { gc }'%(ready['pid'],ready['tid'],ready['event_handle'],body)
        command='bc *;ba e 1 fffff806208fcc6a "'+condition+'";.echo OWNED_CLI_ARMED;g'
        r['command']=command;r['client']=identity(exe)
        env=environment();env['_NT_SYMBOL_PATH']=str(WORKER/'symbols');env['_NT_ALT_SYMBOL_PATH']=''
        with log.open('xb')as f:
            p=subprocess.Popen([str(exe),'-k','com:pipe,port='+PIPE+',resets=0,reconnect','-bonc','-noshell','-sins','-y',str(WORKER/'symbols'),'-c',command],stdin=subprocess.PIPE,stdout=f,stderr=subprocess.STDOUT,env=env,cwd=WORKER,creationflags=subprocess.CREATE_NO_WINDOW)
            r['client_pid']=p.pid
            deadline=time.monotonic()+15
            while time.monotonic()<deadline:
                if re.search(r'^OWNED_CLI_ARMED\r?$',log.read_text(errors='replace'),re.M):break
                need(p.poll()is None,'client alive before arm');time.sleep(.1)
            else:raise ValueError('bounded arm deadline')
            r['go']=run_guest("[IO.File]::WriteAllText('"+q+"\\go','continue');'go written'")
            r['completion']=json.loads(launch.result(timeout=20))
            r['guest_after']=json.loads(run_guest(STATUS))
            data=log.read_text(errors='replace')
            need(re.search(r'^OWNED_FOUR_COMPLETE\r?$',data,re.M),'all four native markers and breakpoint removal')
            result=r['completion']['result']
            need(r['completion']['exit_code']==0 and result['error']is None and result['returns']==[0,0,0,258],'native four return results')
            need(not result['cleanup_errors']and result['handles_closed']and result['buffers_released']and result['watchdog_disarmed'],'native own-resource cleanup')
            p.terminate();p.wait(timeout=5);r['client_stopped_after_guest_resumed']=True
    except Exception as exc:r['errors'].append(repr(exc))
    finally:
        if p and p.poll()is None:p.terminate();p.wait(timeout=5);r['emergency_client_stop']=True
        pool.shutdown(wait=True)
        r['elapsed_seconds']=time.monotonic()-t
        if log.exists():r['log']=identity(log)
        with out.open('x',encoding='utf8')as f:json.dump(r,f,indent=2)
    print(json.dumps(dict(path=str(out),errors=r['errors'],elapsed_seconds=r['elapsed_seconds'],accepted=False)))
    return bool(r['errors'])


if __name__=='__main__':raise SystemExit(main())
