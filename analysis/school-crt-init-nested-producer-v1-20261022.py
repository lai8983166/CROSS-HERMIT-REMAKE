"""Observe the original protection parent's child-debug protocol, without patches."""
import ctypes as C,ctypes.wintypes as W,gzip,json,struct,time,types
from pathlib import Path
import pefile
from tools import school_crt_init_capture as b

win=b.win;ROOT=b.ROOT;need=b.need;word=b.word;sha=b.sha
class MODULE(C.Structure):
 _fields_=[('size',win.D),('module_id',win.D),('pid',win.D),('global_usage',win.D),('process_usage',win.D),('base',win.P),('bytes',win.D),('module',win.H),('name',W.WCHAR*256),('path',W.WCHAR*260)]
module_first=win.bind('Module32FirstW',W.BOOL,[win.H,C.POINTER(MODULE)]);module_next=win.bind('Module32NextW',W.BOOL,[win.H,C.POINTER(MODULE)])

def resolve(pid,module,symbol):
 h=win.snapshot(0x18,pid);win.check(h,'module inventory');m=MODULE();m.size=C.sizeof(m);rows={}
 try:
  ok=module_first(h,C.byref(m))
  while ok:rows[m.name.lower()]=dict(base=m.base,path=m.path,bytes=m.bytes);ok=module_next(h,C.byref(m))
 finally:win.close(h)
 def lookup(module,symbol):
  r=rows[module.lower()];p=pefile.PE(r['path']);need(p.FILE_HEADER.Machine==0x14c,'actual x86 debugger parent module');s=next(s for s in p.DIRECTORY_ENTRY_EXPORT.symbols if s.name==symbol.encode())
  if s.forwarder:
   name,symbol=s.forwarder.decode().rsplit('.',1);return lookup(name+'.dll',symbol)
  return dict(module=module,symbol=symbol,base=r['base'],module_path=r['path'],module_sha256=sha(Path(r['path']).read_bytes()),RVA=s.address,target=r['base']+s.address)
 return lookup(module,symbol)

def instrument(th,targets,mask):
 arm=types.FunctionType(b.arm.__code__,dict(b.arm.__globals__,BREAKPOINTS=targets),'declared_hardware_targets');return dict(targets=list(targets),mask=mask,**arm(th,mask))

def observe():
 need(sha(b.APP.read_bytes())==b.ORIGINAL_SHA and sha(b.SOURCE.read_bytes())==b.SOURCE_SHA,'pinned original source')
 name='CodexCrtNested_'+str(time.time_ns());desktop=b.user.CreateDesktopW(name,None,None,0,0x1ff,None);win.check(desktop,'private desktop');job=win.jobnew(None,None);win.check(job,'owned Job');limits=C.create_string_buffer(144);struct.pack_into('<I',limits,16,0x2000);win.check(win.setjob(job,9,limits,len(limits)),'Job limits');pi=win.PI();si=win.SI();si.cb=C.sizeof(si);si.flags=1;si.show=0;si.desktop='winsta0'+chr(92)+name
 created=assigned=False;parent_debug=False;pending=None;debug_processes={};debug_threads={};child_handles={};events=[];arms=[];captures=[];protocol=[];error=None;child_pid=None;native_api=None;child_mask=0x55;cleanup={}
 try:
  win.check(win.create(str(b.APP.resolve()),None,None,None,False,0x08000004,None,str(b.APP.parent.resolve()),C.byref(si),C.byref(pi)),'normal protected original on private desktop');created=True;win.check(win.assign(job,pi.process),'assign');assigned=True;win.resume(pi.thread);deadline=time.monotonic()+8
  while time.monotonic()<deadline:
   children=[p for p in win.ids(job) if p!=pi.pid]
   if children:child_pid=children[0];break
   time.sleep(.001)
  need(child_pid is not None,'normal protection parent creates owned child')
  win.check(b.attach(pi.pid),'attach original protection parent after child publication');parent_debug=True;h=win.openp(0x410|0x100000,False,child_pid);win.check(h,'read owned original child');child_handles[child_pid]=h
  for tid in win.threads(child_pid):
   th=win.opent(0x5a,False,tid);win.check(th,'instrument owned child thread');win.check(win.suspend(th)!=0xffffffff,'suspend child for debug registers')
   try:arms.append(dict(role='child',pid=child_pid,tid=tid,**instrument(th,b.BREAKPOINTS,child_mask)))
   finally:win.resume(th);win.close(th)
  native_api=resolve(pi.pid,'kernel32.dll','ContinueDebugEvent');entry=native_api['target'];deadline=time.monotonic()+40
  while time.monotonic()<deadline and len(events)<20000:
   e=b.EVENT()
   if not b.wait_event(C.byref(e),100):continue
   pending=(e.pid,e.tid);status=0x10002;row=dict(code=e.code,pid=e.pid,tid=e.tid)
   if e.code==3:
    debug_processes[e.pid]=e.u.create.process;debug_threads[(e.pid,e.tid)]=e.u.create.thread
    if e.u.create.file:win.close(e.u.create.file)
   elif e.code==2:debug_threads[(e.pid,e.tid)]=e.u.thread.thread
   elif e.code==6:
    if e.u.file:win.close(e.u.file)
   elif e.code==1:
    ex=e.u.exception;row.update(exception_code=ex.record.code,exception_address=ex.record.address,first_chance=ex.first);status=0x80010001;th=debug_threads[(e.pid,e.tid)]
    if ex.record.code in (0x80000003,0x4000001f):
     status=0x10002;arms.append(dict(role='parent',pid=e.pid,tid=e.tid,**instrument(th,(entry,0,0,0),1)))
    elif ex.record.code in (0x80000004,0x4000001e):
     c=b.context(th);ip=word(c,184);row.update(EIP=ip,DR6=word(c,20));status=0x10002
     if ip==entry:
      sp=word(c,196);raw=b.required(debug_processes[e.pid],sp,16);ret,cp,ct,cs=struct.unpack('<4I',raw);need(cp==child_pid,'original parent only continues owned child');thc=win.opent(0x5a,False,ct);win.check(thc,'read child event context')
      try:
       cc=b.context(thc);cip=word(cc,184);rec=dict(parent_pid=e.pid,parent_tid=e.tid,parent_EIP=ip,parent_stack_hex=raw.hex(),child_pid=cp,child_tid=ct,continue_status=cs,child_context_hex=cc.hex(),child_CRT_prefix_hex=(win.memory(h,0x5713c0,16) or b'').hex());protocol.append(rec)
       if cip in b.BREAKPOINTS and word(cc,20)&(1<<b.BREAKPOINTS.index(cip)):
        s=b.capture(h,cp,ct,cc);s['parent_protocol_index']=len(protocol)-1;captures.append(s);print('nested capture',s['label'],'blocks',len(s['debug_graph']),'parent status',hex(cs),flush=True);child_mask &= ~(1<<(2*b.BREAKPOINTS.index(cip)));arms.append(dict(role='child',pid=cp,tid=ct,**instrument(thc,b.BREAKPOINTS,child_mask)))
        if cip==0x49dd70:events.append(row);break
        need(cs==0x10002,'original parent naturally handles hardware breakpoint; no debugger reply rewrite')
      finally:win.close(thc)
      arms.append(dict(role='parent',pid=e.pid,tid=e.tid,**instrument(th,(entry,ret,0,0),4)))
     else:
      need(word(c,8)==ip and word(c,20)&2,'natural original parent ContinueDebugEvent return');arms.append(dict(role='parent',pid=e.pid,tid=e.tid,**instrument(th,(entry,0,0,0),1)))
   elif e.code==4:debug_threads.pop((e.pid,e.tid),None)
   elif e.code==5:row['exit_code']=e.u.exit_code;debug_processes.pop(e.pid,None)
   row['continue_status']=status;events.append(row);win.check(b.continue_event(e.pid,e.tid,status),'continue owned parent event');pending=None
  cleanup['last_source_prefix_hex']=(win.memory(h,0x5713c0,16) or b'').hex();need([s['EIP'] for s in captures]==[0x5713c0,0x57b9ea,0x576f60,0x49dd70],'four original child CRT boundaries under original parent protocol')
 except BaseException as exc:error=repr(exc)
 finally:
  members_before=win.ids(job);terminated=bool(win.terminate(job,0x435254)) if members_before else False
  if created and not assigned:win.terminate_parent(pi.process,0x435254)
  if pending:b.continue_event(*pending,0x10002)
  deadline=time.monotonic()+10
  while debug_processes and time.monotonic()<deadline:
   e=b.EVENT()
   if not b.wait_event(C.byref(e),100):continue
   if e.code==3:
    debug_processes[e.pid]=e.u.create.process
    if e.u.create.file:win.close(e.u.create.file)
   if e.code==6 and e.u.file:win.close(e.u.file)
   if e.code==5:debug_processes.pop(e.pid,None)
   events.append(dict(cleanup_event=True,code=e.code,pid=e.pid,tid=e.tid));b.continue_event(e.pid,e.tid,0x10002)
  signaled=bool(created and win.wait(pi.process,5000)==0)
  for h in child_handles.values():win.wait(h,5000);win.close(h)
  if created:win.close(pi.thread);win.close(pi.process)
  after=win.ids(job);win.close(job);desktop_closed=bool(b.user.CloseDesktop(desktop));cleanup.update(explicit_probe_termination=terminated,members_before_probe_termination=members_before,members_after_cleanup=after,parent_signaled=signaled,all_debug_process_exits_observed=not debug_processes,private_desktop_closed=desktop_closed,original_game_normal_shutdown=False)
 return dict(schema_version=2,original_sha256=b.ORIGINAL_SHA,source_sha256=b.SOURCE_SHA,desktop=dict(name=name,private=True,switched=False,input_sent=False),parent_pid=pi.pid,child_pid=child_pid,parent_debug_attached_after_child=parent_debug,ContinueDebugEvent_export=native_api,events=events,debug_register_instrumentation=arms,original_parent_protocol=protocol,captures=captures,error=error,cleanup=cleanup,source_memory_written=False,general_registers_written=False,debugger_reply_substituted=False,original_WinMain_executed=False if captures and captures[-1]['EIP']==0x49dd70 else None,retained_heap_restored=False,R3_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable output')
 cases=[]
 for i in range(2):
  c=observe();cases.append(c)
  if c['error']:break
 out.write_bytes(gzip.compress(json.dumps(dict(schema_version=2,sampler_source_sha256=sha(Path(__file__).read_bytes()),base_source_sha256=sha(Path(b.__file__).read_bytes()),cases=cases),separators=(',',':')).encode(),mtime=0));need(len(cases)==2 and all(c['error']is None for c in cases),'two original initialization captures; see preserved diagnostics')
