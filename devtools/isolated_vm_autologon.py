"""Arm one dedicated-guest automatic logon, then clear its transient setting.

The installation's finite autologon allowance can expire. This uses the existing
F-drive private guest credential over the UUID-checked encrypted admin channel;
neither the credential nor the command containing it is printed or persisted.
No host registry, interactive desktop, or other guest is touched.
"""
import argparse
import json
from devtools.isolated_windows_vm import WORKER
from devtools.isolated_vm_guest_admin import run_script

GUARD=r"""$busy=@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'CROSS HERMIT.EXE' -or $_.Name -like 'python*'});if($busy.Count){throw 'guest busy'};
$key='HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon';$r=Get-ItemProperty -LiteralPath $key;
$desktop=@(Get-Process explorer -ErrorAction SilentlyContinue);"""


def configure(action):
    if action not in ('arm-once','clear'):raise ValueError('explicit dedicated guest action')
    if action=='arm-once':
        password=json.loads((WORKER/'credentials.private.json').read_bytes())['password']
        if not isinstance(password,str)or len(password)<16:raise ValueError('existing private guest credential required')
        literal="'"+password.replace("'","''")+"'"
        script=GUARD+"if($desktop.Count -or $r.AutoAdminLogon -ne '0' -or $r.DefaultPassword){throw 'only expired idle guest configuration may be armed'};"
        script+="New-ItemProperty -LiteralPath $key -Name DefaultUserName -Value 'Administrator' -PropertyType String -Force|Out-Null;"
        script+="New-ItemProperty -LiteralPath $key -Name DefaultDomainName -Value 'CHAOMOFA-WORKER' -PropertyType String -Force|Out-Null;"
        script+="New-ItemProperty -LiteralPath $key -Name DefaultPassword -Value "+literal+" -PropertyType String -Force|Out-Null;"
        script+="New-ItemProperty -LiteralPath $key -Name AutoLogonCount -Value 1 -PropertyType DWord -Force|Out-Null;"
        script+="New-ItemProperty -LiteralPath $key -Name AutoAdminLogon -Value '1' -PropertyType String -Force|Out-Null;"
    else:
        script=GUARD+"if($desktop.Count -ne 1 -or $desktop[0].SessionId -eq 0){throw 'one actual guest desktop required before clearing transient logon'};"
        script+="New-ItemProperty -LiteralPath $key -Name AutoAdminLogon -Value '0' -PropertyType String -Force|Out-Null;"
        script+="Remove-ItemProperty -LiteralPath $key -Name DefaultPassword,AutoLogonCount -ErrorAction SilentlyContinue;"
    script+="$r=Get-ItemProperty -LiteralPath $key;[pscustomobject]@{computer=$env:COMPUTERNAME;AutoAdminLogon=$r.AutoAdminLogon;AutoLogonCount=$r.AutoLogonCount;password_configured=([bool]$r.DefaultPassword);desktop_sessions=@($desktop|ForEach-Object SessionId)}|ConvertTo-Json -Compress"
    result=json.loads(run_script(script))
    if action=='arm-once' and not(result['AutoAdminLogon']=='1'and result['AutoLogonCount']==1 and result['password_configured']):raise ValueError('one-logon configuration did not verify')
    if action=='clear'and not(result['AutoAdminLogon']=='0'and not result['password_configured']and result['AutoLogonCount']is None):raise ValueError('transient guest credential was not cleared')
    return dict(action=action,guest=result,host_configuration_changed=False,host_input_actions=0)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['arm-once','clear']);a=p.parse_args()
    print(json.dumps(configure(a.action)))
