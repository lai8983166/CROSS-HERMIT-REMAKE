"""Seal final pinned source delta, actual build options and runtime dependencies."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

PIN='e470268ff446ec56728215a987ed166d5ed8fb64'

def identity(path):
    raw=path.read_bytes()
    return dict(path=str(path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())

def main(a):
    source=a.work/'source';build=a.work/'build';exe=build/'qemu-system-x86_64'
    def cmd(*args):return subprocess.check_output(args,cwd=source,timeout=30,text=True)
    if cmd('git','rev-parse','HEAD').strip()!=PIN:raise ValueError('wrong base')
    names=cmd('git','diff','--name-only',PIN).splitlines()
    names+=['target/i386/terminal-state.c']
    delta=cmd('git','diff','--binary',PIN).encode()
    delta_path=a.work/'logs/final-source.diff'
    with delta_path.open('xb')as f:f.write(delta)
    libraries=[]
    ldd=cmd('ldd',str(exe))
    for line in ldd.splitlines():
        match=re.search(r'(?:=>\s*)?(/[^\s]+)',line)
        if match:
            p=Path(match.group(1)).resolve()
            if p.is_file()and str(p)not in[p['path']for p in libraries]:libraries.append(identity(p))
    dependencies=[]
    for name in ('keycodemapdb','berkeley-softfloat-3','berkeley-testfloat-3'):
        p=source/'subprojects'/name
        revision=subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD'],text=True).strip()
        changes=subprocess.check_output(['git','-C',str(p),'status','--porcelain'],text=True).splitlines()
        dependencies.append(dict(name=name,commit=revision,overlay_status=changes))
    toolchain=[]
    for name in ('cc1','cc1plus','collect2','ld','as'):
        value=cmd('gcc','-print-prog-name='+name).strip()
        if not value.startswith('/'):
            value=cmd('which',value).strip()
        toolchain.append(dict(role=name,**identity(Path(value).resolve())))
    record=dict(schema='tcg-project-build-v1',base_commit=PIN,exact_local_build_identity=True,
                publisher_binary_reproduction=False,full57=False,windows_admitted=False,
                host='Existing Ubuntu WSL2 registered at F:/WSL_Linux; no host package/config install',
                binary=identity(exe),version=cmd(str(exe),'--version'),source_delta=identity(delta_path),
                modified_source=[identity(source/p)for p in names],dependencies=dependencies,
                build_configuration=[identity(p)for p in (build/'config-host.mak',build/'config-host.h',
                    build/'meson-info/intro-buildoptions.json',build/'compile_commands.json',a.work/'logs/toolchain.txt')],
                dynamic_dependencies=libraries,compiler_components=toolchain,ldd=ldd,
                limitations=['Traceable local source/configuration/toolchain/binary chain; no claim of byte-identical rebuild.',
                             'Subset architecture probes do not imply complete CPU, machine or resource restore.'])
    with a.output.open('x')as f:json.dump(record,f,indent=2)
    print(json.dumps(dict(binary=record['binary'],modified_source=len(names),dependencies=len(libraries)),indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('work',type=Path);p.add_argument('output',type=Path)
    main(p.parse_args())
