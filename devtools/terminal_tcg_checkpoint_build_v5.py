"""Identity-guarded additive observer build in the existing F-backed tree."""
import hashlib,json,subprocess,os
from pathlib import Path
R=Path(__file__).resolve().parents[1];W=R/'.venv-audit/native-worker'
S=W/'tcg-build-v1/source';B=W/'tcg-build-v1/build';O=W/'tcg-checkpoint-build-v5'
O.mkdir(exist_ok=False)
prior=json.loads((R/'analysis/terminal-wait-tcg-build-manifest-v4-20261110.json').read_bytes())
for row in prior['modified_source']:
 p=Path(row['path'])
 if hashlib.sha256(p.read_bytes()).hexdigest()!=row['sha256']:raise ValueError('parent changed '+str(p))
source=S/'target/i386/terminal-state.c';schema=S/'qapi/misc-i386.json'
source.write_bytes(source.read_bytes()+b'\n'+(R/'devtools/terminal_tcg_checkpoint_observer.c').read_bytes())
schema.write_text(schema.read_text()+'''\n##
# @x-query-tcg-checkpoint:
#
# Observe stopped RAM hashes and event fields.  No restore or acceptance.
#
# Returns: Project diagnostic JSON.
#
# Since: 11.1
##
{ 'command': 'x-query-tcg-checkpoint', 'returns': 'TcgStateJson' }
''')
env=dict(os.environ,TMPDIR=str(W/'tcg-build-v1/tmp'),XDG_CACHE_HOME=str(W/'tcg-build-v1/cache'),PYTHONDONTWRITEBYTECODE='1')
with (O/'build.log').open('wb')as log:
 subprocess.run(['nice','-n','10','ninja','-j2','qemu-system-x86_64'],cwd=B,env=env,stdout=log,stderr=log,timeout=180,check=True)
runtime=O/'qemu-system-x86_64';runtime.write_bytes((B/'qemu-system-x86_64').read_bytes());runtime.chmod(0o755)
def ident(p):
 raw=p.read_bytes();return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
delta=subprocess.check_output(['git','diff','--binary',prior['base_commit'],'--',*[str(Path(x['path']).relative_to(S))for x in prior['modified_source']]],cwd=S)
(O/'source.diff').write_bytes(delta)
record=dict(parent_manifest=ident(R/'analysis/terminal-wait-tcg-build-manifest-v4-20261110.json'),
 binary=ident(runtime),modified_source=[ident(Path(x['path']))for x in prior['modified_source']],
 source_delta=ident(O/'source.diff'),new_observer=ident(R/'devtools/terminal_tcg_checkpoint_observer.c'),
 build_config=[ident(B/n)for n in ('config-host.mak','config-host.h','meson-info/intro-buildoptions.json','compile_commands.json')],
 accepted=False,compiler_and_libraries='Parent manifest unchanged; additive observer only')
(O/'manifest.json').write_text(json.dumps(record,indent=2));print(json.dumps(record['binary']))
