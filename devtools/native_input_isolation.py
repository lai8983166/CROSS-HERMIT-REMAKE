"""Fail closed before native game launch outside a qualified dedicated guest."""
import hashlib
import json
from pathlib import Path
import subprocess

QUALIFICATION=Path('C:/ChaomofaWorker/isolation-qualified.json')


def current_machine():
    # Re-query at every gate: neither a cached resource configuration nor a prior
    # boot qualification authorizes the currently running guest.
    script="$guestSystem=Get-CimInstance Win32_ComputerSystem; $guestOS=Get-CimInstance Win32_OperatingSystem; [pscustomobject]@{computer_name=$env:COMPUTERNAME;manufacturer=$guestSystem.Manufacturer;uuid=(Get-CimInstance Win32_ComputerSystemProduct).UUID;logical_processors=[int]$guestSystem.NumberOfLogicalProcessors;memory_bytes=[uint64]$guestSystem.TotalPhysicalMemory;boot_utc=$guestOS.LastBootUpTime.ToUniversalTime().ToString('o',[Globalization.CultureInfo]::InvariantCulture)}|ConvertTo-Json -Compress"
    result=subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',script],
        capture_output=True,text=True,timeout=20,check=True,
        creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    return json.loads(result.stdout)


def validate_machine(machine):
    if machine.get('computer_name')!='CHAOMOFA-WORKER' or 'VMware'not in machine.get('manufacturer',''):
        raise RuntimeError('Native input requires the qualified dedicated Windows VM; shared host desktop is disabled')
    if not isinstance(machine.get('uuid'),str) or len(machine['uuid'])!=36:
        raise RuntimeError('Current guest machine identity unavailable')
    if (type(machine.get('logical_processors'))is not int or machine['logical_processors']!=2 or
            type(machine.get('memory_bytes'))is not int or not 3*1024**3<=machine['memory_bytes']<=4*1024**3):
        raise RuntimeError('Current guest must retain the qualified two CPU / four GiB resource bound')
    from devtools.isolated_vm_preflight import validate_boot_utc
    try:validate_boot_utc(machine.get('boot_utc'))
    except ValueError:raise RuntimeError('Current guest boot UTC identity unavailable')from None


def require_qualified_guest():
    machine=current_machine();validate_machine(machine)
    if not QUALIFICATION.is_file()or QUALIFICATION.stat().st_size>128*1024:
        raise RuntimeError('Input isolation and D3D8 preflight must pass before native game launch')
    raw=QUALIFICATION.read_bytes();report=json.loads(raw)
    from devtools.isolated_vm_preflight import verify
    verification=verify(report)
    qualified=report['guest']['machine']
    if qualified['uuid'].lower()!=machine['uuid'].lower():
        raise RuntimeError('Preflight belongs to a different guest')
    if qualified['boot_utc']!=machine['boot_utc']:
        raise RuntimeError('Preflight belongs to a different guest boot; repeat qualification')
    if any(qualified[key]!=machine[key]for key in ('logical_processors','memory_bytes')):
        raise RuntimeError('Current guest resources differ from qualified resources')
    return dict(path=str(QUALIFICATION),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
                current_guest_uuid=machine['uuid'],current_guest_boot_utc=machine['boot_utc'],
                current_guest_resources={key:machine[key]for key in ('logical_processors','memory_bytes')},
                verification=verification,source_utf8=raw.decode('utf8'))
