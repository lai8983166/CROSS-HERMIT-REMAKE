"""Finish the additive observer build after correcting QAPI doc line length."""
import hashlib,json,os,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1];W=R/'.venv-audit/native-worker'
S=W/'tcg-build-v1/source';B=W/'tcg-build-v1/build';O=W/'tcg-checkpoint-build-v5'
p=S/'qapi/misc-i386.json';raw=p.read_text()
old='# Observe stopped RAM hashes and event fields.  No restore or acceptance.'
if raw.count(old)!=1:raise ValueError('unexpected QAPI schema')
p.write_text(raw.replace(old,'# Observe stopped RAM hashes and event fields.\n# No restore or acceptance.'))
env=dict(os.environ,TMPDIR=str(W/'tcg-build-v1/tmp'),XDG_CACHE_HOME=str(W/'tcg-build-v1/cache'),PYTHONDONTWRITEBYTECODE='1')
with (O/'build-v2.log').open('wb')as log:
 subprocess.run(['nice','-n','10','ninja','-j2','qemu-system-x86_64'],cwd=B,env=env,stdout=log,stderr=log,timeout=180,check=True)
runtime=O/'qemu-system-x86_64';runtime.write_bytes((B/'qemu-system-x86_64').read_bytes());runtime.chmod(0o755)
def ident(p):
 raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
parent=R/'analysis/terminal-wait-tcg-build-manifest-v4-20261110.json';prior=json.loads(parent.read_bytes())
for row in prior['dynamic_dependencies']+prior['compiler_components']:
 if ident(Path(row['path']))['sha256']!=row['sha256']:raise ValueError('compiler/library changed')
delta=subprocess.check_output(['git','diff','--binary',prior['base_commit'],'--',*[str(Path(x['path']).relative_to(S))for x in prior['modified_source']]],cwd=S)
(O/'source.diff').write_bytes(delta)
record=dict(parent_manifest=ident(parent),binary=ident(runtime),
 modified_source=[ident(Path(x['path']))for x in prior['modified_source']],source_delta=ident(O/'source.diff'),
 new_observer=ident(R/'devtools/terminal_tcg_checkpoint_observer.c'),
 build_config=[ident(B/n)for n in ('config-host.mak','config-host.h','meson-info/intro-buildoptions.json','compile_commands.json')],
 accepted=False,compiler_and_libraries_rehashed_match_parent=True)
(O/'manifest.json').write_text(json.dumps(record,indent=2));print(json.dumps(record['binary']))
