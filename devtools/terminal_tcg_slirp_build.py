"""Enable existing libslirp with version-matched headers extracted only on F."""
import hashlib,json,os,subprocess
from pathlib import Path
from devtools.terminal_tcg_incremental_build import ident

def main():
    root=Path(__file__).resolve().parents[1];w=root/'.venv-audit/native-worker'
    b=w/'tcg-build-v1/build';s=w/'tcg-build-v1/source';d=w/'tcg-slirp-deps-v1'
    parent_path=w/'tcg-checkpoint-build-v12/manifest.json';parent=json.loads(parent_path.read_bytes())
    out=w/'tcg-checkpoint-build-v13';out.mkdir(exist_ok=False)
    for row in parent['modified_source']+parent['build_config']:
        if ident(Path(row['path']))['sha256']!=row['sha256']:raise ValueError('parent changed')
    base=json.loads((root/'analysis/terminal-wait-tcg-build-manifest-v4-20261110.json').read_bytes())
    for row in base['dynamic_dependencies']+base['compiler_components']:
        if ident(Path(row['path']))['sha256']!=row['sha256']:raise ValueError('dependency changed')
    package=d/'libslirp-dev_4.7.0-1ubuntu3.1_amd64.deb'
    metadata=subprocess.check_output(['apt-cache','show','libslirp-dev=4.7.0-1ubuntu3.1'],text=True)
    digest=next(x.split(': ',1)[1]for x in metadata.splitlines()if x.startswith('SHA256:'))
    if ident(package)['sha256']!=digest:raise ValueError('package hash differs from apt metadata')
    (out/'package-metadata.txt').write_text(metadata)
    pc=d/'slirp.pc'
    pc.write_text('Name: slirp\nDescription: installed libslirp with F-extracted matching headers\nVersion: 4.7.0\nRequires: glib-2.0\nLibs: -l:libslirp.so.0\nCflags: -I'+str(d/'extracted/usr/include/slirp')+'\n')
    env=dict(os.environ,PKG_CONFIG_PATH=str(d),TMPDIR=str(w/'tcg-build-v1/tmp'),XDG_CACHE_HOME=str(w/'tcg-build-v1/cache'),PYTHONDONTWRITEBYTECODE='1')
    with (out/'build.log').open('xb')as log:
        subprocess.run([str(b/'pyvenv/bin/meson'),'configure','-Dslirp=enabled',str(b)],env=env,stdout=log,stderr=log,timeout=30,check=True)
        subprocess.run(['nice','-n','10','ninja','-j2','qemu-system-x86_64'],cwd=b,env=env,stdout=log,stderr=log,timeout=180,check=True)
    binary=out/'qemu-system-x86_64';binary.write_bytes((b/'qemu-system-x86_64').read_bytes());binary.chmod(0o755)
    r=dict(parent_manifest=ident(parent_path),binary=ident(binary),modified_source=parent['modified_source'],
        source_delta=parent['source_delta'],config_change='slirp enabled; no host package installation',
        added_dependency=ident(Path('/usr/lib/x86_64-linux-gnu/libslirp.so.0').resolve()),
        package=ident(package),headers=[ident(p)for p in (d/'extracted/usr/include/slirp').glob('*.h')],
        pkg_config=ident(pc),compiler_and_parent_libraries_rehashed=True,accepted=False,
        build_config=[ident(b/n)for n in ('config-host.mak','config-host.h','meson-info/intro-buildoptions.json','compile_commands.json')])
    (out/'manifest.json').write_text(json.dumps(r,indent=2));print(json.dumps(r['binary']))

if __name__=='__main__':main()
