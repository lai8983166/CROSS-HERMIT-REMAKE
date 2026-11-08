"""Authenticated, encrypted guest administration when Tools is not ready.

Only the dedicated VM's DHCP lease and SMBIOS UUID are accepted. This does not
change host WinRM/TrustedHosts or use its interactive desktop.
"""
import argparse
import ipaddress
import json
from pathlib import Path
import re
import uuid
from devtools.isolated_windows_vm import WORKER, VMX, validate_vmx


def run_script(script):
    import winrm
    fields = validate_vmx(VMX.read_text(encoding='utf8'))
    mac = fields['ethernet0.generatedAddress'].lower()
    if not re.fullmatch(r'(?:[0-9a-f]{2}:){5}[0-9a-f]{2}', mac):
        raise ValueError('actual dedicated VM MAC required')
    raw_uuid = bytes.fromhex(fields['uuid.bios'].replace('-', ' '))
    guest_uuid = str(uuid.UUID(bytes_le=raw_uuid))
    leases = Path('C:/ProgramData/VMware/vmnetdhcp.leases').read_text(encoding='utf8')
    addresses = [m.group(1) for m in re.finditer(r'lease\s+(\S+)\s*\{([^}]+)\}', leases)
                 if re.search(r'hardware ethernet\s+' + re.escape(mac) + r'\s*;', m.group(2), re.I)]
    if not addresses or not ipaddress.ip_address(addresses[-1]).is_private:
        raise ValueError('private lease of the actual dedicated MAC required')
    secret = json.loads((WORKER / 'credentials.private.json').read_bytes())['password']
    session = winrm.Session('http://' + addresses[-1] + ':5985/wsman',
        auth=('CHAOMOFA-WORKER\\Administrator', secret), transport='ntlm', message_encryption='always',
        operation_timeout_sec=20, read_timeout_sec=30)
    guard = "$ErrorActionPreference='Stop';$m=Get-CimInstance Win32_ComputerSystem;"
    guard += "if($env:COMPUTERNAME -ne 'CHAOMOFA-WORKER' -or $m.Manufacturer -notlike '*VMware*' -or "
    guard += "(Get-CimInstance Win32_ComputerSystemProduct).UUID -ne '" + guest_uuid + "'){throw 'Wrong dedicated guest'};"
    try:
        result = session.run_ps(guard + script)
    except Exception as exc:
        raise RuntimeError('dedicated guest administration transport failed: ' + type(exc).__name__) from None
    output = result.std_out.decode('utf8', errors='replace').replace(secret, '[redacted]')
    if result.status_code:
        raise RuntimeError('dedicated guest administration failed, exit ' + str(result.status_code))
    return output


STATUS = """[pscustomobject]@{computer=$env:COMPUTERNAME;uuid=(Get-CimInstance Win32_ComputerSystemProduct).UUID;
 cpu=$m.NumberOfLogicalProcessors;memory=$m.TotalPhysicalMemory;
 tools=@(Get-Service VMTools -ErrorAction SilentlyContinue|Select-Object Name,Status);
 explorer=@(Get-Process explorer -ErrorAction SilentlyContinue|Select-Object Id,SessionId);
 boot=(Get-CimInstance Win32_OperatingSystem).LastBootUpTime.ToUniversalTime().ToString('o')}|ConvertTo-Json -Depth 4 -Compress"""


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['status', 'restart-tools'])
    args = p.parse_args()
    script = STATUS if args.action == 'status' else "Restart-Service VMTools;" + STATUS
    print(run_script(script))
