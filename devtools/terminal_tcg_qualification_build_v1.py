"""Build, never execute, the fixed x86 QEMU-only probe; all output/temp on F."""
import json,subprocess
from pathlib import Path
from devtools.isolated_windows_vm import ROOT,WORKER,environment,identity

def main():
 out=WORKER/'tcg-qualification-build-v1';out.mkdir(exist_ok=False)
 source=ROOT/'devtools/terminal_tcg_qualification_probe_v1.cs'
 compiler=Path('C:/Windows/Microsoft.NET/Framework/v4.0.30319/csc.exe')
 before=identity(source);exe=out/'probe.exe'
 flags=['/nologo','/platform:x86','/target:winexe','/r:System.Management.dll','/r:System.Web.Extensions.dll']
 p=subprocess.run([str(compiler),*flags,'/out:'+str(exe),str(source)],env=environment(),capture_output=True,timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
 (out/'build.log').write_bytes(p.stdout+p.stderr)
 if p.returncode or identity(source)!=before:raise ValueError('build failed or source changed')
 r=dict(accepted=False,source=before,compiler=identity(compiler),flags=flags,executable=identity(exe),host_executed=False)
 (out/'manifest.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
if __name__=='__main__':main()
