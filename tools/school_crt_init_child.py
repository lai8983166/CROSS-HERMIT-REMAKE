"""Attach only to the freshly published owned child, leaving its parent untraced."""
import ctypes as C,gzip,json,time,types
from pathlib import Path
from tools import school_crt_init_capture as base

def observe(late=False):
 jobs=[];protocol=[]
 def jobnew(*args):
  h=base.win.jobnew(*args);jobs.append(h);return h
 def create(app,command,ps,ts,inherit,flags,env,cwd,si,pi):
  return base.win.create(app,command,ps,ts,inherit,0x08000004,env,cwd,si,pi)
 def resume(thread):
  result=base.win.resume(thread);deadline=time.monotonic()+8;parent=None
  while time.monotonic()<deadline:
   members=base.win.ids(jobs[-1])
   if parent is None and members:parent=members[0]
   children=[p for p in members if p!=parent]
   if children:
    child=children[0];prefix=None
    if late:
     h=base.win.openp(0x410,False,child);base.win.check(h,'watch owned child unpack boundary');expected=base.SOURCE.read_bytes()[0x1713c0:0x1713d0]
     try:
      while time.monotonic()<deadline:
       prefix=base.win.memory(h,0x5713c0,16)
       if prefix==expected:break
      base.need(prefix==expected,'original CRT prefix becomes available before attach')
     finally:base.win.close(h)
    ok=bool(base.attach(child));protocol.append(dict(parent_pid=parent,child_pid=child,attach_result=ok,error=0 if ok else C.get_last_error(),waited_for_original_CRT_prefix=late,observed_prefix_hex=None if prefix is None else prefix.hex()));base.need(ok,'direct attach owned newly published child');return result
   time.sleep(.001)
  raise ValueError('normal owned child publication deadline')
 proxy=types.SimpleNamespace(**dict(vars(base.win),jobnew=jobnew,create=create,resume=resume));run=types.FunctionType(base.observe.__code__,dict(base.observe.__globals__,win=proxy),'normal_parent_then_attach_child');r=run();r['normal_parent_child_attach']=protocol;return r

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--late',action='store_true');a=p.parse_args();out=base.ROOT/a.out
 if out.exists():p.error('fresh immutable evidence')
 cases=[]
 for i in range(2):
  c=observe(a.late);cases.append(c)
  if c['error']:break
 out.write_bytes(gzip.compress(json.dumps(dict(schema_version=3,sampler_source_sha256=base.sha(Path(__file__).read_bytes()),base_source_sha256=base.sha(Path(base.__file__).read_bytes()),cases=cases),separators=(',',':')).encode(),mtime=0));base.need(len(cases)==2 and all(c['error']is None for c in cases),'two direct child original initialization captures; see diagnostics')
