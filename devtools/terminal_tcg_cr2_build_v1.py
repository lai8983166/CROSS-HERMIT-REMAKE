"""Build a sparse CR2 overlay without changing frozen source or build objects."""
import hashlib,json,os,shlex,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WORK=ROOT/'.venv-audit/native-worker'
SOURCE=WORK/'tcg-build-v1/source'; BUILD=WORK/'tcg-build-v1/build'
OUT=WORK/'tcg-cr2-build-v1'; OVER=OUT/'overlay'
def ident(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def main():
 OUT.mkdir(exist_ok=True); OVER.mkdir(exist_ok=True)
 parent=WORK/'tcg-checkpoint-build-v12/manifest.json'
 for row in json.loads(parent.read_text())['modified_source']:
  assert ident(Path(row['path']))['sha256']==row['sha256'],row['path']
 assert ident(Path(json.loads(parent.read_text())['binary']['path']))['sha256']==json.loads(parent.read_text())['binary']['sha256']
 changed={}
 base=json.loads((ROOT/'analysis/terminal-wait-tcg-build-manifest-v4-20261110.json').read_text())
 for row in base['compiler_components']+base['dynamic_dependencies']:
  assert ident(Path(row['path']))['sha256']==row['sha256'],row['path']
 def edit(name,old,new):
  text=changed.get(name,(SOURCE/name).read_text())
  assert text.count(old)==1,(name,old,text.count(old))
  changed[name]=text.replace(old,new)
 decl='\nvoid terminal_cr2_poison(const char *reason);\n'
 targetdecl=decl+'void terminal_cr2_write(CPUX86State *, uint64_t, int, int, int, int);\nvoid terminal_cr2_restored(CPUState *);\n'
 edit('target/i386/terminal-state.c','#include "system/tcg.h"','#include "system/tcg.h"\n'+targetdecl+'static TcgStateJson *terminal_cr2_command(int64_t, Error **);')
 edit('target/i386/terminal-state.c','    SegmentCache *seg;\n\n    if (!tcg_enabled() || runstate_is_running()) {','    SegmentCache *seg;\n\n    if (cpu_index == -2 || cpu_index == -3) {\n        return terminal_cr2_command(cpu_index, errp);\n    }\n    if (!tcg_enabled() || runstate_is_running()) {')
 changed['target/i386/terminal-state.c']+='\n'+(ROOT/'devtools/terminal_tcg_cr2_backend_v1.c').read_text()
 # Preserve PF assignment and restore ordering: prepare at assignment; finish only
 # after the existing cpu_restore_state call in cpu_loop_exit_restore.
 edit('target/i386/tcg/system/excp_helper.c','        env->cr[2] = err.cr2;','        terminal_cr2_write(env, err.cr2, err.exception_index, err.error_code, access_type, mmu_idx);\n        env->cr[2] = err.cr2;')
 edit('target/i386/tcg/system/misc_helper.c','        env->cr[reg] = t0;','        if (reg == 2) { terminal_cr2_write(env, t0, -1, -1, -1, -1); }\n        env->cr[reg] = t0;')
 edit('target/i386/tcg/emit.c.inc','        gen_helper_write_crN(tcg_env, tcg_constant_i32(op->n), v);','        if (op->n == 2) { gen_update_eip_cur(s); }\n        gen_helper_write_crN(tcg_env, tcg_constant_i32(op->n), v);')
 # translate.c copied so its local emit include resolves to the new overlay.
 changed['target/i386/tcg/translate.c']=(SOURCE/'target/i386/tcg/translate.c').read_text()
 edit('accel/tcg/cpu-exec-common.c','    cpu_loop_exit(cpu);\n}\n\nvoid cpu_loop_exit_atomic','    terminal_cr2_restored(cpu);\n    cpu_loop_exit(cpu);\n}\n\nvoid cpu_loop_exit_atomic')
 edit('accel/tcg/cpu-exec-common.c','#include "internal-common.h"','#include "internal-common.h"\nvoid terminal_cr2_restored(CPUState *);')
 edit('target/i386/tcg/system/svm_helper.c','    env->cr[2] = x86_ldq_phys(cs,','    terminal_cr2_poison("vmrun");\n    env->cr[2] = x86_ldq_phys(cs,')
 edit('target/i386/cpu.c','    memset(env, 0, offsetof(CPUX86State, end_reset_fields));','    terminal_cr2_poison("reset-init");\n    memset(env, 0, offsetof(CPUX86State, end_reset_fields));')
 for sig,reason in [('static int cpu_pre_save(void *opaque)','migration-save'),('static int cpu_post_load(void *opaque, int version_id)','migration-load')]:
  edit('target/i386/machine.c',sig+'\n{',sig+'\n{\n    terminal_cr2_poison("'+reason+'");')
 edit('target/i386/gdbstub.c','int x86_cpu_gdb_write_register(CPUState *cs, uint8_t *mem_buf, int n)\n{','int x86_cpu_gdb_write_register(CPUState *cs, uint8_t *mem_buf, int n)\n{\n    terminal_cr2_poison("gdb-register-write");')
 edit('gdbstub/gdbstub.c','static void handle_write_mem(GArray *params, void *user_ctx)\n{','static void handle_write_mem(GArray *params, void *user_ctx)\n{\n    terminal_cr2_poison("gdb-memory-write");')
 edit('migration/savevm.c','int qemu_loadvm_state(QEMUFile *f, Error **errp)\n{','int qemu_loadvm_state(QEMUFile *f, Error **errp)\n{\n    terminal_cr2_poison("migration-load");')
 for name in list(changed):
  if name.startswith('target/') and name not in ('target/i386/tcg/emit.c.inc','target/i386/terminal-state.c','target/i386/tcg/translate.c'):
   edit(name,'#include "cpu.h"','#include "cpu.h"\n'+targetdecl)
 for name in ('gdbstub/gdbstub.c','migration/savevm.c'):
  edit(name,'#include "qemu/osdep.h"','#include "qemu/osdep.h"\n'+decl)
 known={row['path'] for row in json.loads(parent.read_text())['modified_source']}
 for name in changed:
  if str(SOURCE/name) not in known:
   original=subprocess.check_output(['git','show',base['base_commit']+':'+name],cwd=SOURCE)
   assert original==(SOURCE/name).read_bytes(),name
 for name,content in changed.items():
  p=OVER/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
 # Source-local quoted includes must still resolve at their original directories.
 commands=json.loads((BUILD/'compile_commands.json').read_text()); replacements={}; receipts=[]
 env=dict(os.environ,TMPDIR=str(WORK/'tcg-build-v1/tmp'),XDG_CACHE_HOME=str(WORK/'tcg-build-v1/cache'),PYTHONDONTWRITEBYTECODE='1')
 with (OUT/'build.log').open('w') as log:
  for name in changed:
   if not name.endswith('.c'):continue
   rows=[r for r in commands if os.path.normpath(os.path.join(r['directory'],r['file']))==str(SOURCE/name)]
   assert len(rows)==1,(name,len(rows))
   row=rows[0];args=shlex.split(row['command']);oldout=row['output'];obj=OUT/'objects'/oldout;obj.parent.mkdir(parents=True,exist_ok=True)
   args[args.index('-o')+1]=str(obj);args[args.index('-c')+1]=str(OVER/name)
   for flag in ('-MF','-MQ'):
    if flag in args:args[args.index(flag)+1]=str(obj)+('.d' if flag=='-MF' else '')
   args[1:1]=['-iquote',str((SOURCE/name).parent)]
   subprocess.run(args,cwd=BUILD,env=env,stdout=log,stderr=log,check=True,timeout=180)
   replacements[oldout]=str(obj);receipts.append(dict(source=ident(SOURCE/name),overlay=ident(OVER/name),original_command=row['command'],command=shlex.join(args),object=ident(obj)))
  linkrows=json.loads(subprocess.check_output(['ninja','-t','compdb','-x','c_LINKER_RSP'],cwd=BUILD))
  link=next(r for r in linkrows if r['output']=='qemu-system-x86_64');args=shlex.split(link['command']);args=[replacements.get(a,a) for a in args];args[args.index('-o')+1]=str(OUT/'qemu-system-x86_64')
  subprocess.run(args,cwd=BUILD,env=env,stdout=log,stderr=log,check=True,timeout=180)
 link_inputs=[ident(BUILD/a) for a in shlex.split(link['command']) if not a.startswith('-') and (BUILD/a).is_file() and a!='qemu-system-x86_64']
 manifest=dict(compiler_and_libraries=[ident(Path(r['path'])) for r in base['compiler_components']+base['dynamic_dependencies']],link_inputs=link_inputs,build_config=[ident(BUILD/n) for n in ('config-host.mak','config-host.h','compile_commands.json','build.ninja')], parent_manifest=ident(parent),binary=ident(OUT/'qemu-system-x86_64'),overlay=[ident(OVER/n)for n in changed],compilation=receipts,original_link=link['command'],link=shlex.join(args),accepted=False)
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps(manifest['binary']))
if __name__=='__main__':main()
