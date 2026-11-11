"""Sparse immutable context-filter overlay above the frozen CR2-v4 runtime."""
import hashlib,json,os,shlex,subprocess
from pathlib import Path
from devtools.terminal_tcg_cr2_build_v4 import identity,check,require,helper_symbol
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'.venv-audit/native-worker'
SOURCE=WORK/'tcg-build-v1/source'; BUILD=WORK/'tcg-build-v1/build'
OUT=WORK/'tcg-context-build-v1'
def main():
    require(not OUT.exists(), 'new output required')
    p4=WORK/'tcg-cr2-build-v4/manifest.json'; v4=json.loads(p4.read_bytes())
    check(v4['parent_manifest']); v3=json.loads(Path(v4['parent_manifest']['path']).read_bytes())
    for row in v3['compiler_and_libraries']+v3['link_inputs']+v3['build_config']+v3['overlay']+[v3['binary'],v4['binary'],v4['object'],v4['new_header']]: check(row)
    for row in v3['compilation']: check(row['object'])
    require(helper_symbol(Path(v4['object']['path']))['flags_byte_x86_64_offset28']==0,'CR2 write helper flags')
    state=next(r for r in v3['compilation'] if r['overlay']['path'].endswith('/terminal-state.c'))
    text=Path(state['overlay']['path']).read_text()
    def replace(text,old,new):
        require(text.count(old)==1,'exact substitution '+old);return text.replace(old,new)
    text=replace(text,'static TcgStateJson *terminal_cr2_command(int64_t, Error **);','static TcgStateJson *terminal_cr2_command(int64_t, Error **);\nstatic TcgStateJson *terminal_context_command(int64_t, Error **);\nvoid terminal_context_poison(const char *);')
    text=replace(text,'    if (cpu_index == -2 || cpu_index == -3) {','    if (cpu_index >= -7 && cpu_index <= -4) {\n        return terminal_context_command(cpu_index, errp);\n    }\n    if (cpu_index == -2 || cpu_index == -3) {')
    text=replace(text,'void terminal_cr2_poison(const char *reason)\n{','void terminal_cr2_poison(const char *reason)\n{\n    terminal_context_poison(reason);')
    text+='\n'+(ROOT/'devtools/terminal_tcg_context_backend_v1.c').read_text()
    cpu=(SOURCE/'accel/tcg/cpu-exec.c').read_text()
    cpu=replace(cpu,'static bool check_for_breakpoints_slow(', 'extern bool terminal_context_match(CPUState *, uint64_t);\n\nstatic bool check_for_breakpoints_slow(')
    cpu=replace(cpu,'                match_bp = true;','                match_bp = terminal_context_match(cpu, pc);\n                if (!match_bp) { match_page = true; }')
    changed={'target/i386/terminal-state.c':text,'accel/tcg/cpu-exec.c':cpu}
    commands=json.loads((BUILD/'compile_commands.json').read_text()); replacements={}; receipts=[]
    OUT.mkdir()
    env=dict(os.environ,TMPDIR=str(WORK/'tcg-build-v1/tmp'),XDG_CACHE_HOME=str(WORK/'tcg-build-v1/cache'),PYTHONDONTWRITEBYTECODE='1')
    with (OUT/'build.log').open('xb') as log:
        for name,content in changed.items():
            dst=OUT/'overlay'/name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(content)
            rows=[r for r in commands if os.path.normpath(os.path.join(r['directory'],r['file']))==str(SOURCE/name) and not r['output'].startswith('libuser.a.p/')]
            require(len(rows)==1,'unique compile command'); row=rows[0]; args=shlex.split(row['command']); obj=OUT/(Path(name).name+'.o')
            args[1:1]=['-iquote',str((SOURCE/name).parent)]
            for flag,value in [('-o',str(obj)),('-c',str(dst)),('-MF',str(obj)+'.d'),('-MQ',str(obj))]:
                if flag in args:args[args.index(flag)+1]=value
            subprocess.run(args,cwd=BUILD,env=env,stdout=log,stderr=log,check=True,timeout=180)
            old=state['object']['path'] if name.endswith('terminal-state.c') else row['output']
            replacements[old]=str(obj)
            receipts.append(dict(source=identity(SOURCE/name),overlay=identity(dst),object=identity(obj),command=shlex.join(args)))
        link=shlex.split(v4['link_command'])
        for old in replacements:require(link.count(old)==1,'unique link replacement '+old)
        link=[replacements.get(x,x) for x in link];binary=OUT/'qemu-system-x86_64';link[link.index('-o')+1]=str(binary)
        subprocess.run(link,cwd=BUILD,env=env,stdout=log,stderr=log,check=True,timeout=180)
    record=dict(accepted=False,parent_manifest=identity(p4),binary=identity(binary),compilation=receipts,link_command=shlex.join(link),cr2_helper_flags=0,backend=identity(ROOT/'devtools/terminal_tcg_context_backend_v1.c'),builder=identity(Path(__file__)),frozen_parent_rehashed=True)
    (OUT/'manifest.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record['binary']))
if __name__=='__main__':main()
