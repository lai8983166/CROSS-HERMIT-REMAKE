"""Safely coalesce current-turn overlay ancestors; never modify their bytes."""
import argparse,json,shutil,subprocess,time
from pathlib import Path
from devtools.terminal_tcg_roundtrip_probe import identity

def compact(root):
    w=(root/'.venv-audit/native-worker').resolve();source=w/'tcg-windows-control-v6/disk.qcow2'
    report=json.loads((source.parent/'report.json').read_bytes())
    if not report['all_processes_exited']or report['errors']:raise ValueError('VM must be stopped')
    if identity(source)['sha256']!=report['overlay']['sha256']:raise ValueError('final source identity')
    parents=[w/f'tcg-windows-control-{v}/disk.qcow2'for v in ('v2','v4','v5','v6')]
    before=[identity(p)for p in parents];base=w/'tcg-windows-compat-v2/disk.qcow2';base_before=identity(base)
    out=w/'tcg-windows-current-v1';out.mkdir(exist_ok=False);target=out/'disk.qcow2'
    if not target.resolve().is_relative_to(w):raise ValueError('output scope')
    shutil.copyfile(source,target);image=w/'qemu-worker/runtime/qemu-img.exe';start=time.monotonic()
    commands=[[str(image),'rebase','-f','qcow2','-b','../tcg-windows-compat-v2/disk.qcow2','-B','qcow2',str(target)],
              [str(image),'compare','-f','qcow2','-F','qcow2',str(source),str(target)]]
    r=dict(accepted=False,source_before=before,base_before=base_before,commands=commands,errors=[])
    try:
        for i,command in enumerate(commands):
            with (out/f'command-{i}.log').open('xb')as log:
                subprocess.run(command,cwd=out,stdout=log,stderr=log,timeout=180,check=True)
        r['virtual_contents_equal']=True
    except Exception as exc:r['errors'].append(type(exc).__name__+': '+str(exc))
    r.update(seconds=time.monotonic()-start,source_unchanged=[identity(p)for p in parents]==before,
        historical_base_unchanged=identity(base)==base_before,target=identity(target))
    r['passed']=r.get('virtual_contents_equal',False)and r['source_unchanged']and r['historical_base_unchanged']and not r['errors']
    (out/'report.json').write_text(json.dumps(r,indent=2));print(json.dumps({k:r.get(k)for k in ('passed','seconds','errors','target')}))

if __name__=='__main__':compact(Path(__file__).resolve().parents[1])
