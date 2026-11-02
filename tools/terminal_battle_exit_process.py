"""Freeze, supervise and preserve one complete exit-prefix source/proof process."""
import argparse,datetime,hashlib,json,os,runpy,shutil,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
BACKUP=ROOT.parent/'chaomofa-local-evidence'/'20261102-terminal-battle-exit-prefix'

def ref(path):
 p=Path(path);p=p if p.is_absolute() else ROOT/p;h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1048576),b''):h.update(block)
 return dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=h.hexdigest())

def save(path,data,exclusive=True):
 with Path(path).open('x' if exclusive else 'w',encoding='utf8',newline=chr(10)) as f:json.dump(data,f,ensure_ascii=False,separators=(',',':'));f.write(chr(10))

def modules():
 return sorted({Path(m.__file__).resolve().relative_to(ROOT).as_posix() for n,m in sys.modules.copy().items() if n.startswith('tools.') and getattr(m,'__file__',None) and Path(m.__file__).resolve().is_relative_to(ROOT)})

def prepare(mode):
 # This historical dependency loads lazily during the selected corpus.  Load it
 # before freezing imports so late execution cannot silently expand the inputs.
 from tools import school_native_dialogue_handoff_verification
 if mode=='source':
  from tools import terminal_battle_exit_emulation as implementation
 else:
  from tools import terminal_battle_exit_verification as implementation
 return implementation

def backup(paths,output):
 BACKUP.mkdir(parents=True,exist_ok=True);entries=[]
 for p in sorted(set(paths)):
  p=Path(p);identity=ref(p);name=p.parent.name+'-'+p.name if p.name.startswith('case-') and p.suffix=='.json' else p.name;dest=BACKUP/name
  if not dest.exists():shutil.copyfile(p,dest)
  h=hashlib.sha256();equal=True
  with p.open('rb') as a,dest.open('rb') as b:
   while True:
    x=a.read(1048576);y=b.read(1048576);h.update(y);equal=equal and x==y
    if not x and not y:break
  assert equal and h.hexdigest()==identity['sha256'] and dest.stat().st_size==identity['bytes'],str(dest)
  entries.append(dict(**identity,backup_path=dest.as_posix(),backup_bytes=dest.stat().st_size,backup_sha256=h.hexdigest(),byte_equal=True))
 save(output,dict(schema_version=1,entries=entries,all_byte_equal=True))

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=('source','proof'));p.add_argument('--version',required=True);p.add_argument('--report');p.add_argument('--child',action='store_true');a=p.parse_args()
 assert a.version.isalnum(),'simple immutable run version'
 base='terminal-battle-exit-prefix-'+a.mode+'-';suffix=a.version+'-20261102';target=ROOT/'analysis'/(base+suffix+('.json.gz' if a.mode=='source' else '.json'));imports=ROOT/'analysis'/(base+'imports-'+suffix+'.json');implementation=prepare(a.mode)
 module='tools.terminal_battle_exit_'+('emulation' if a.mode=='source' else 'verification')
 args=[module,'--out',target.relative_to(ROOT).as_posix()]
 if a.mode=='proof':
  assert a.report and (ROOT/a.report).is_file();args+=['--report',a.report]
 if a.child:
  start={p:ref(p) for p in modules()};sys.argv=args
  try:runpy.run_module(module,run_name='__main__')
  finally:
   end={p:ref(p) for p in modules()};save(imports,dict(start=start,end=end,actual_imports_unchanged=start==end));assert start==end,'actual tools imports changed or expanded'
  return
 log=ROOT/'analysis'/(base+'run-'+suffix+'.log');begun=ROOT/'analysis'/(base+'process-start-'+suffix+'.json');receipt=ROOT/'analysis'/(base+'process-review-'+suffix+'.json');state=ROOT/'.venv-audit'/(base+suffix+'-state.json');catalog=ROOT/'analysis'/(base+'local-evidence-'+suffix+'.json')
 for path in (target,imports,log,begun,receipt,catalog):assert not path.exists(),str(path)
 paths=modules()+['tools/terminal_battle_exit_process.py','tools/terminal_battle_exit_crt_platform.cs','tools/terminal_battle_exit_d3d8_platform.cs']
 frozen={p:ref(p) for p in sorted(set(paths))};snapshots=[]
 for name in ('emulation.py','crt_platform.cs','d3d8_platform.cs','process.py','budget.py')+(('verification.py',) if a.mode=='proof' else ()):
  path=ROOT/'tools'/('terminal_battle_exit_'+name);dest=ROOT/'.venv-audit'/(base+suffix+'-input-'+name);assert not dest.exists();shutil.copyfile(path,dest);snapshots.append(dest)
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',PYTHONPATH=str(ROOT)+os.pathsep+str(ROOT/'.venv-audit/Lib/site-packages'));env.pop('__PYVENV_LAUNCHER__',None)
 command=[sys._base_executable,'-X','utf8','-u',str(Path(__file__)),a.mode,'--version',a.version,'--child']
 if a.report:command+=['--report',a.report]
 started=time.monotonic()
 with log.open('xb') as out:
  child=subprocess.Popen(command,cwd=ROOT,env=env,stdin=subprocess.DEVNULL,stdout=out,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
  record=dict(mode=a.mode,pid=child.pid,command=command,HEAD=subprocess.check_output(['C:/Program Files/Git/cmd/git.exe','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),implementation_start=frozen,source_snapshots=[ref(s) for s in snapshots],started_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat());save(begun,record);save(state,dict(status='running',**record),False);code=child.wait()
 result=dict(mode=a.mode,pid=child.pid,exit_code=code,normal_exit=code==0,duration_seconds=round(time.monotonic()-started,2),raw_log=ref(log),start_record=ref(begun),implementation_end={p:ref(p) for p in frozen},finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat());result['implementation_unchanged']=result['implementation_end']==frozen
 helper_prefix=target.name.removesuffix('.gz').removesuffix('.json');helper_binaries=[ROOT/'.venv-audit'/(helper_prefix+'-'+kind+'.exe') for kind in ('crt','gpu')];result['helper_binaries']=[ref(path) for path in helper_binaries if path.is_file()]
 for key,path in [('report',target),('actual_imports',imports)]:
  if path.exists():result[key]=ref(path)
 save(receipt,result);save(state,dict(status='backing_up',**result),False)
 paths=[p for p in (target,imports,log,begun,receipt,*snapshots) if p.exists()]
 paths+=[path for path in helper_binaries if path.is_file()]
 paths+=list((ROOT/'analysis').glob('terminal-battle-exit-diagnostic-*.json.gz'))
 if a.mode=='source' and code!=0:
  for directory in (ROOT/'.venv-audit').glob('bex-cases-'+target.name.replace('.json.gz','')+'-*'):
   paths+=list(directory.glob('case-*.json'))
 backup(paths,catalog);save(state,dict(status='complete' if code==0 and result['implementation_unchanged'] else 'failed',evidence_catalog=ref(catalog),**result),False)
 if code:raise SystemExit(code)
 assert result['implementation_unchanged'],'frozen implementation changed'

if __name__=='__main__':main()
