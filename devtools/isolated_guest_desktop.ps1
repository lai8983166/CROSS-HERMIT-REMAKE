$ErrorActionPreference = 'Stop'
$machine = Get-CimInstance Win32_ComputerSystem
if ($env:COMPUTERNAME -ne 'CHAOMOFA-WORKER' -or $machine.Manufacturer -notlike '*VMware*' -or $machine.Model -notlike '*Virtual*' -or $machine.NumberOfLogicalProcessors -ne 2) {
    throw 'Only the dedicated two-CPU VMware guest may be configured'
}
# The fresh server dashboard steals focus while its first-login prompt opens.
$policy = 'HKLM:\Software\Policies\Microsoft\Windows\Server\ServerManager'
New-Item -Path $policy -Force | Out-Null
New-ItemProperty -Path $policy -Name DoNotOpenAtLogon -PropertyType DWord -Value 1 -Force | Out-Null
$dashboard = @(Get-Process ServerManager -ErrorAction SilentlyContinue)
foreach ($process in $dashboard) {
    if ($process.Path -ne "$env:SystemRoot\System32\ServerManager.exe") { throw 'Unexpected dashboard executable' }
    Stop-Process -Id $process.Id
}
# Keep the crash/event logs; suppress only the server's post-crash question UI.
$reliability = 'HKLM:\Software\Policies\Microsoft\Windows NT\Reliability'
New-Item -Path $reliability -Force | Out-Null
New-ItemProperty -Path $reliability -Name ShutdownReasonOn -PropertyType DWord -Value 0 -Force | Out-Null
$trackers = @(Get-Process shutdown -ErrorAction SilentlyContinue)
foreach ($process in $trackers) {
    if ($process.Path -ne "$env:SystemRoot\System32\shutdown.exe") { throw 'Unexpected event tracker executable' }
    Stop-Process -Id $process.Id
}
& powercfg.exe /change monitor-timeout-ac 0
if ($LASTEXITCODE -ne 0) { throw 'Guest monitor timeout configuration failed' }
& powercfg.exe /change standby-timeout-ac 0
if ($LASTEXITCODE -ne 0) { throw 'Guest standby timeout configuration failed' }
[pscustomobject]@{
    computer = $env:COMPUTERNAME
    uuid = (Get-CimInstance Win32_ComputerSystemProduct).UUID
    dashboard_autostart_disabled = ((Get-ItemProperty -Path $policy).DoNotOpenAtLogon -eq 1)
    stopped_dashboard_pids = @($dashboard | ForEach-Object Id)
    stopped_event_tracker_pids = @($trackers | ForEach-Object Id)
    host_configuration_changed = $false
} | ConvertTo-Json -Compress | Set-Content -Encoding UTF8 'C:\ChaomofaWorker\desktop-configuration.json'
