"""Post-build immutable provenance audit; never recompiles or overwrites runtime."""
import hashlib,json,subprocess,shlex
from pathlib import Path
from devtools.terminal_tcg_cr2_build_v4 import identity,check,require
ROOT=Path(__file__).resolve().parents[1];WORK=ROOT/'.venv-audit/native-worker';BUILD=WORK/'tcg-build-v1/build';SRC=WORK/'tcg-build-v1/source';OUT=WORK/'tcg-context-build-v1'
def main():
    manifest=json.loads((OUT/'manifest.json').read_bytes()); v12=json.loads((WORK/'tcg-checkpoint-build-v12/manifest.json').read_bytes());known={r['path']:r for r in v12['modified_source']}
    v3=json.loads((WORK/'tcg-cr2-build-v3/manifest.json').read_bytes());v4=json.loads((WORK/'tcg-cr2-build-v4/manifest.json').read_bytes())
    base='e470268ff446ec56728215a987ed166d5ed8fb64';deps={};checks=[]
    for r in manifest['compilation']:
        check(r['source']);check(r['overlay']);check(r['object']); dp=Path(r['object']['path']+'.d')
        for word in shlex.split(dp.read_text().replace(chr(92)+chr(10),' ').split(':',1)[1]):
            p=(BUILD/word).resolve();row=identity(p)
            if str(p).startswith(str(SRC)+'/'):
                if str(p) in known:check(known[str(p)]);row['provenance']='frozen-v12-modified'
                else:
                    raw=subprocess.check_output(['git','show',base+':'+str(p.relative_to(SRC))],cwd=SRC)
                    require(hashlib.sha256(raw).hexdigest()==row['sha256'],'base source changed '+str(p));row['provenance']='fixed-base-git'
            elif str(p).startswith(str(OUT)+'/overlay/'):
                row['provenance']='this-build-overlay'
            else:row['provenance']='recorded-current-build-or-system-dependency'
            deps[str(p)]=row
        checks.append(identity(dp))
    original=SRC/'accel/tcg/cpu-exec.c';raw=subprocess.check_output(['git','show',base+':accel/tcg/cpu-exec.c'],cwd=SRC)
    require(raw==original.read_bytes(),'original cpu-exec source differs from base')
    for r in v3['compiler_and_libraries']+v3['link_inputs']+v3['build_config']+v3['overlay']+[v3['binary'],v4['binary'],v4['object'],v4['new_header']]:check(r)
    for r in v3['compilation']:check(r['object'])
    check(manifest['binary']);check(manifest['backend']);check(manifest['builder'])
    record=dict(audit_passed=True,manifest=identity(OUT/'manifest.json'),fixed_base=base,cpu_exec_original=identity(original),actual_dependency_files=checks,dependencies=list(deps.values()),limitation='System/generated include bytes are recorded now, not retroactively authenticated against an unavailable pre-build header manifest.',synchronization='Commands require every CPU stopped, synchronously handled on QMP main loop under BQL. Realtime timer callback is also main-loop/BQL serialized. Match and poison accesses use ctx_lock while CPUs execute. No command runs while CPUs execute.',parent_inputs_rehashed=True)
    p=OUT/'dependency-audit-v1.json';require(not p.exists(),'new audit only');p.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(dict(audit_passed=True,dependencies=len(deps),report=identity(p))))
if __name__=='__main__':main()
