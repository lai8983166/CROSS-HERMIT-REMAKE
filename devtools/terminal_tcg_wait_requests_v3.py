"""Prepare immutable native-fixture control requests; no guest execution."""
import argparse,base64,hashlib,json
from pathlib import Path

def prepare(case,fixture):
    guest='C:/ChaomofaWorker/'+case.name
    lines=["$d='"+guest+"';if(Test-Path -LiteralPath $d){throw 'fresh fixture directory required'};New-Item -ItemType Directory -Path $d|Out-Null;"]
    files=[]
    for name in ('fixture.exe','fixture.bin','manifest.json','terminal_tcg_wait_fixture_v3.cs'):
        data=(fixture/name).read_bytes();sha=hashlib.sha256(data).hexdigest();files.append(dict(name=name,bytes=len(data),sha256=sha))
        lines.append("[IO.File]::WriteAllBytes(($d+'/"+name+"'),[Convert]::FromBase64String('"+base64.b64encode(data).decode()+"'));if((Get-FileHash -Algorithm SHA256 -LiteralPath ($d+'/"+name+"')).Hash -ne '"+sha+"'){throw 'fixture hash'};")
    lines.append("[pscustomobject]@{prepared=$true;uuid=$p.UUID;directory=$d}|ConvertTo-Json -Compress")
    (case/'prepare.ps1').write_text(''.join(lines),encoding='utf8')
    launch="$d='"+guest+"';if(Test-Path ($d+'/ready.json')){throw 'already started'};0..3|ForEach-Object{[IO.File]::WriteAllText(($d+'/ack-'+$_),'preapproved observer continuation')};"
    launch+="$cmd='\"'+$d+'/fixture.exe\" --owned-vmm-fixture \"'+$d+'\"';$spawn=Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine=$cmd;CurrentDirectory=$d};if($spawn.ReturnValue -ne 0){throw 'create failed'};"
    launch+="$r=[pscustomobject]@{launched=$true;pid=$spawn.ProcessId;uuid=$p.UUID};$j=$r|ConvertTo-Json -Compress;[IO.File]::WriteAllText(($d+'/launch-receipt.json'),$j);$j"
    (case/'launch.ps1').write_text(launch,encoding='utf8')
    (case/'go.ps1').write_text("$d='"+guest+"';if(Test-Path ($d+'/go')){throw 'go already issued'};[IO.File]::WriteAllText(($d+'/go'),'go');[pscustomobject]@{go=$true;uuid=$p.UUID}|ConvertTo-Json -Compress",encoding='utf8')
    result="$d='"+guest+"';if(!(Test-Path ($d+'/result.json'))){[pscustomobject]@{ready=$false}|ConvertTo-Json -Compress}else{$r=Get-Content -Raw ($d+'/result.json')|ConvertFrom-Json;$r|Add-Member process_exited (-not [bool](Get-Process -Id $r.ready.pid -ErrorAction SilentlyContinue));$r|ConvertTo-Json -Depth 12 -Compress}"
    (case/'result.ps1').write_text(result,encoding='utf8')
    (case/'read-ready.ps1').write_text("$d='"+guest+"';if(Test-Path ($d+'/ready.json')){[IO.File]::ReadAllText($d+'/ready.json')}elseif(Test-Path ($d+'/result.json')){[IO.File]::ReadAllText($d+'/result.json')}else{[pscustomobject]@{ready=$false;files=@(Get-ChildItem $d|Select-Object -ExpandProperty Name)}|ConvertTo-Json -Compress}",encoding='utf8')
    (case/'fixture-inputs.json').write_text(json.dumps(dict(guest_directory=guest,files=files,ack_policy='All four observer continuation gates preapproved; real waits and event signaling remain unchanged'),indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('case',type=Path);p.add_argument('fixture',type=Path);a=p.parse_args();prepare(a.case,a.fixture)
