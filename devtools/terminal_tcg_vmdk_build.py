"""Enable local VMDK reader in the authenticated runtime; no dependency install."""
import json,os,subprocess
from pathlib import Path
from devtools.terminal_tcg_incremental_build import ident

def main():
    root=Path(__file__).resolve().parents[1];work=root/'.venv-audit/native-worker'
    source=work/'tcg-build-v1/source';build=work/'tcg-build-v1/build'
    parent_path=work/'tcg-checkpoint-build-v11b/manifest.json';parent=json.loads(parent_path.read_bytes())
    out=work/'tcg-checkpoint-build-v12';out.mkdir(exist_ok=False)
    for row in parent['modified_source']+parent['build_config']:
        if ident(Path(row['path']))['sha256']!=row['sha256']:raise ValueError('parent identity changed')
    base=json.loads((root/'analysis/terminal-wait-tcg-build-manifest-v4-20261110.json').read_bytes())
    for row in base['dynamic_dependencies']+base['compiler_components']:
        if ident(Path(row['path']))['sha256']!=row['sha256']:raise ValueError('dependency identity changed')
    subprocess.run(['git','diff','--exit-code',base['base_commit'],'--','block/vmdk.c','block/meson.build'],cwd=source,check=True)
    env=dict(os.environ,TMPDIR=str(work/'tcg-build-v1/tmp'),XDG_CACHE_HOME=str(work/'tcg-build-v1/cache'),PYTHONDONTWRITEBYTECODE='1')
    with (out/'build.log').open('xb')as log:
        subprocess.run([str(build/'pyvenv/bin/meson'),'configure','-Dvmdk=enabled',str(build)],env=env,stdout=log,stderr=log,timeout=30,check=True)
        subprocess.run(['nice','-n','10','ninja','-j2','qemu-system-x86_64'],cwd=build,env=env,stdout=log,stderr=log,timeout=180,check=True)
    binary=out/'qemu-system-x86_64';binary.write_bytes((build/'qemu-system-x86_64').read_bytes());binary.chmod(0o755)
    r=dict(parent_manifest=ident(parent_path),binary=ident(binary),modified_source=parent['modified_source'],
        source_delta=parent['source_delta'],config_change='vmdk auto (auto_features disabled) -> enabled',
        unchanged_base_source=[ident(source/n)for n in ('block/vmdk.c','block/meson.build')],
        compiler_and_libraries_rehashed_match_parent=True,accepted=False,
        build_config=[ident(build/n)for n in ('config-host.mak','config-host.h','meson-info/intro-buildoptions.json','compile_commands.json')])
    (out/'manifest.json').write_text(json.dumps(r,indent=2));print(json.dumps(r['binary']))

if __name__=='__main__':main()
