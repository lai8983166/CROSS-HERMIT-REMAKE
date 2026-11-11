"""Apply one scoped patch to an authenticated local TCG build and seal it."""
import argparse,hashlib,json,os,subprocess
from pathlib import Path
def ident(p):
 raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def main(a):
 root=Path(__file__).resolve().parents[1];work=root/'.venv-audit/native-worker';s=work/'tcg-build-v1/source';b=work/'tcg-build-v1/build'
 parent=json.loads(a.parent.read_bytes());a.output.mkdir(exist_ok=False)
 for row in parent['modified_source']:
  if ident(Path(row['path']))['sha256']!=row['sha256']:raise ValueError('parent source changed')
 base=json.loads((root/'analysis/terminal-wait-tcg-build-manifest-v4-20261110.json').read_bytes())
 for row in base['dynamic_dependencies']+base['compiler_components']:
  if ident(Path(row['path']))['sha256']!=row['sha256']:raise ValueError('compiler/library changed')
 subprocess.run(['git','apply','--check',str(a.patch.resolve())],cwd=s,check=True)
 subprocess.run(['git','apply',str(a.patch.resolve())],cwd=s,check=True)
 env=dict(os.environ,TMPDIR=str(work/'tcg-build-v1/tmp'),XDG_CACHE_HOME=str(work/'tcg-build-v1/cache'),PYTHONDONTWRITEBYTECODE='1')
 with (a.output/'build.log').open('wb')as log:
  subprocess.run(['nice','-n','10','ninja','-j2','qemu-system-x86_64'],cwd=b,env=env,stdout=log,stderr=log,timeout=180,check=True)
 runtime=a.output/'qemu-system-x86_64';runtime.write_bytes((b/'qemu-system-x86_64').read_bytes());runtime.chmod(0o755)
 paths=[Path(x['path'])for x in parent['modified_source']]
 for line in a.patch.read_text().splitlines():
  if line.startswith('+++ b/'):
   p=s/line[6:]
   if p not in paths:paths.append(p)
 delta=subprocess.check_output(['git','diff','--binary',base['base_commit'],'--',*[str(p.relative_to(s))for p in paths]],cwd=s)
 (a.output/'source.diff').write_bytes(delta)
 record=dict(parent_manifest=ident(a.parent),binary=ident(runtime),modified_source=[ident(p)for p in paths],
  source_delta=ident(a.output/'source.diff'),patch=ident(a.patch),accepted=False,compiler_and_libraries_rehashed_match_parent=True,
  build_config=[ident(b/n)for n in ('config-host.mak','config-host.h','meson-info/intro-buildoptions.json','compile_commands.json')])
 (a.output/'manifest.json').write_text(json.dumps(record,indent=2));print(json.dumps(record['binary']))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for name in ('parent','patch','output'):p.add_argument('--'+name,type=Path,required=True)
 main(p.parse_args())
