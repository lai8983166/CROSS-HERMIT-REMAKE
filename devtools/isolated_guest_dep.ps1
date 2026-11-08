param([ValidateSet('disable','restore')][string]$Action = 'disable')
$ErrorActionPreference = 'Stop'
$machine = Get-CimInstance Win32_ComputerSystem
if ($env:COMPUTERNAME -ne 'CHAOMOFA-WORKER' -or $machine.Manufacturer -notlike '*VMware*') { throw 'Dedicated guest only' }
$qualification = Get-Content -LiteralPath 'C:\ChaomofaWorker\isolation-qualified.json' -Raw | ConvertFrom-Json
$guestUuid = (Get-CimInstance Win32_ComputerSystemProduct).UUID
if ($guestUuid -ne $qualification.guest.machine.uuid) { throw 'Guest qualification UUID mismatch' }
$app = 'C:\ChaomofaWorker\project\.venv-audit\scene-callback-runtime\CROSS HERMIT\CROSS HERMIT\CROSS HERMIT.EXE'
$sha = (Get-FileHash -LiteralPath $app -Algorithm SHA256).Hash.ToLowerInvariant()
if ($sha -ne '030dca584a3a0b20751a72609f7acc823e8d79d820cebf1fcde8be6a791a9df7') { throw 'Original private EXE identity mismatch' }
if (@(Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -eq $app }).Count) { throw 'Game must be stopped' }
$systemBefore = Get-ProcessMitigation -System | ConvertTo-Json -Depth 8 -Compress
$policyBefore = (Get-CimInstance Win32_OperatingSystem).DataExecutionPrevention_SupportPolicy
$before = Get-ProcessMitigation -Name $app
if ($Action -eq 'disable') {
    if ($null -ne $before -and [string]$before.DEP.Enable -ne 'NOTSET') { throw 'Existing DEP override; refuse replacement' }
    Set-ProcessMitigation -Name $app -Disable DEP
} else {
    Set-ProcessMitigation -Name $app -Remove -Disable DEP
}
$after = Get-ProcessMitigation -Name $app
$systemAfter = Get-ProcessMitigation -System | ConvertTo-Json -Depth 8 -Compress
$policyAfter = (Get-CimInstance Win32_OperatingSystem).DataExecutionPrevention_SupportPolicy
if ($systemBefore -ne $systemAfter -or $policyBefore -ne $policyAfter) { throw 'Unexpected system policy change' }
if ($Action -eq 'disable' -and [string]$after.DEP.Enable -ne 'OFF') { throw 'DEP override was not registered' }
[pscustomobject]@{action=$Action;guest_uuid=$guestUuid;image_path=$app;image_sha256=$sha;
    before=$before;after=$after;system_before=($systemBefore|ConvertFrom-Json);system_after=($systemAfter|ConvertFrom-Json);
    system_dep_policy_before=$policyBefore;system_dep_policy_after=$policyAfter;
    host_configuration_changed=$false;accepted=$false}|ConvertTo-Json -Depth 12 -Compress
