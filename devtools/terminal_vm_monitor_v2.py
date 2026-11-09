"""Bind an elevated VMware listener to this boot's owned VM log and OS PID.

Windows denies this session the elevated process command line. Authenticate the
current loopback owner PID/name/creation time against the fresh dedicated log,
its exact config path and vmrun inventory; do not accept a port alone.
"""
import datetime,json,re,socket,subprocess,time
from devtools import terminal_vm_monitor as parent
from devtools.isolated_windows_vm import WORKER,VMX,VMWARE,environment,identity,validate_vmx,vmrun
need=parent.need


def endpoint():
    fields=validate_vmx(VMX.read_text(encoding='utf8'))
    need(fields.get('debugStub.listen.guest64')=='TRUE' and fields.get('debugStub.listen.guest64.remote')=='FALSE'
         and fields.get('debugStub.hideBreakpoints')=='TRUE','hidden hardware localhost configuration')
    running=vmrun(['list']);need(str(VMX).lower()in running.lower(),'dedicated VM is currently running')
    log=WORKER/'vmware.log'
    with log.open('rb')as f:prefix=f.read(128*1024)
    text=prefix.decode('utf8',errors='strict')
    match=re.match(r'(\S+)\| vmx\| I005: Log for VMware Workstation pid=(\d+) version=([^\s]+)',text)
    need(match,'this boot actual VMware log header')
    pid=int(match[2]);started=datetime.datetime.fromisoformat(match[1])
    need('Config file: '+str(VMX)in text,'actual log config is the dedicated VMX')
    need('Command line: "'+str(VMWARE/'x64/vmware-vmx.exe')+'"' in text,'actual logged installed VMware executable')
    need('Created new IPv4 socket listener for (127.0.0.1:8864)'in text,'actual logged loopback endpoint')
    script=("$ErrorActionPreference='Stop';$rows=@(Get-NetTCPConnection -State Listen -LocalPort 8864);"
        "if(!$rows.Count){throw 'missing listener'};$p=Get-CimInstance Win32_Process -Filter 'ProcessId="+str(pid)+"';"
        "if($p.Name -ne 'vmware-vmx.exe'){throw 'wrong listener process'};foreach($r in $rows){"
        "if($r.OwningProcess -ne "+str(pid)+" -or $r.LocalAddress -notin @('127.0.0.1','::1')){throw 'wrong endpoint'}};"
        "[pscustomobject]@{pid=$p.ProcessId;name=$p.Name;created_utc=$p.CreationDate.ToUniversalTime().ToString('o');"
        "command_line_query_available=([bool]$p.CommandLine);endpoints=@($rows|Select-Object LocalAddress,LocalPort,OwningProcess)}|ConvertTo-Json -Depth 4 -Compress")
    p=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',script],env=environment(),capture_output=True,text=True,timeout=20)
    need(p.returncode==0,'actual OS listener PID/name/creation identity')
    got=json.loads(p.stdout);created=datetime.datetime.fromisoformat(got['created_utc'][:26]+'+00:00')
    delta=(started-created).total_seconds();need(0<=delta<30,'fresh log belongs to same actual process creation')
    got.update(vm_config_path=str(VMX),log_header=match[0],creation_to_log_seconds=delta,
               executable_file=identity(VMWARE/'x64/vmware-vmx.exe'),port_identity_method='current OS listener PID/name/creation + same boot owned VMware log config/executable + vmrun inventory')
    return got


class Monitor(parent.Monitor):
    def __init__(self):
        self.owner=endpoint();self.rows=[];self.sock=None;self.stopped=False;self.breakpoints=set()
        self.sock=socket.create_connection(('127.0.0.1',8864),timeout=3);self.sock.settimeout(3)
