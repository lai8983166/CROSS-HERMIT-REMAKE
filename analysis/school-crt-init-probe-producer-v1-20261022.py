"""One native child boundary per owned probe, observed before protector handling."""
import ctypes as C,gzip,json,struct,time
from pathlib import Path
from tools import school_crt_init_capture as b
from tools.school_crt_init_nested import resolve,instrument
win=b.win;ROOT=b.ROOT;need=b.need;word=b.word;sha=b.sha

def observe(target):
 need(target in b.BREAKPOINTS and sha(b.APP.read_bytes())==b.ORIGINAL_SHA,'owned original target/source');name='CodexCrtProbe_'+str(time.time_ns());desktop=b.user.CreateDesktopW(name,None,None,0,0x1ff,None);win.check(desktop,'private desktop');job=win.jobnew(None,None);win.check(job,'Job');limits=C.create_string_buffer(144);struct.pack_into('<I',limits,16,0x2000);win.check(win.setjob(job,9,limits,len(limits)),'Job limits');pi=win.PI();si=win.SI();si.cb=C.sizeof(si);si.flags=1;si.show=0;si.desktop='winsta0'+chr(92)+name
 created=assigned=False;pending=None;processes={};threads={};child_h=None;events=[];arms=[];waits=[];continues=[];captures=[];error=None;child=None;exports=None;frames={};targets={};masks={}
 try:
  win.check(win.create(str(b.APP.resolve()),None,None,None,False,0x08000004,None,str(b.APP.parent.resolve()),C.byref(si),C.byref(pi)),'normal original start');created=True;win.check(win.assign(job,pi.process),'assign');assigned=True;win.resume(pi.thread);deadline=time.monotonic()+8
  while time.monotonic()<deadline:
   children=[p for p in win.ids(job) if p!=pi.pid]
   if children:child=children[0];break
   time.sleep(.001)
  need(child is not None,'original child publication');win.check(b.attach(pi.pid),'attach published protection parent');child_h=win.openp(0x410|0x100000,False,child);win.check(child_h,'owned child read');exports={n:resolve(pi.pid,'ntdll.dll',n) for n in ('NtDebugContinue','NtWaitForDebugEvent')};cont,wait=[exports[n]['target'] for n in ('NtDebugContinue','NtWaitForDebugEvent')];deadline=time.monotonic()+50
  def arm_parent(th,key,new_targets=None,mask=0x11):
   if new_targets is not None:targets[key]=new_targets
   masks[key]=mask;arms.append(dict(role='parent',pid=key[0],tid=key[1],**instrument(th,targets[key],mask)))
  while time.monotonic()<deadline and len(events)<24000:
   e=b.EVENT()
   if not b.wait_event(C.byref(e),100):continue
   pending=(e.pid,e.tid);key=pending;status=0x10002;row=dict(code=e.code,pid=e.pid,tid=e.tid)
   if e.code==3:
    processes[e.pid]=e.u.create.process;threads[key]=e.u.create.thread;arm_parent(threads[key],key,(cont,0,wait,0))
    if e.u.create.file:win.close(e.u.create.file)
   elif e.code==2:threads[key]=e.u.thread.thread;arm_parent(threads[key],key,(cont,0,wait,0))
   elif e.code==6:
    if e.u.file:win.close(e.u.file)
   elif e.code==1:
    ex=e.u.exception;row.update(exception_code=ex.record.code,exception_address=ex.record.address);status=0x80010001;th=threads[key]
    if ex.record.code in (0x80000003,0x4000001f):status=0x10002;arm_parent(th,key,(cont,0,wait,0))
    elif ex.record.code in (0x80000004,0x4000001e):
     c=b.context(th);ip=word(c,184);sp=word(c,196);ts=list(targets[key]);mask=masks[key];row.update(EIP=ip,DR6=word(c,20));status=0x10002
     if ip==cont:
      raw=b.required(processes[e.pid],sp,16);ret,obj,client,cs=struct.unpack('<4I',raw);cp,ct=struct.unpack('<2I',b.required(processes[e.pid],client,8));need(cp==child,'owned child continuation');thc=win.opent(0x5a,False,ct);win.check(thc,'child context')
      try:
       cc=b.context(thc);prefix=win.memory(child_h,0x5713c0,16);continues.append(dict(parent_pid=e.pid,parent_tid=e.tid,parent_context_hex=c.hex(),parent_stack_hex=raw.hex(),client_id_hex=struct.pack('<2I',cp,ct).hex(),child_context_hex=cc.hex(),CRT_prefix_hex=(prefix or b'').hex()))
       if prefix==b.SOURCE.read_bytes()[0x1713c0:0x1713d0] and word(cc,24)==0:
        arms.append(dict(role='child',pid=cp,tid=ct,before_continue_index=len(continues)-1,**instrument(thc,(target,0,0,0),1)))
      finally:win.close(thc)
      ts[1]=ret;arm_parent(th,key,tuple(ts),(mask&~1)|4)
     elif ip==wait:
      raw=b.required(processes[e.pid],sp,20);ret,obj,alert,timeout,output=struct.unpack('<5I',raw);frames[key]=dict(parent_context_hex=c.hex(),parent_stack_hex=raw.hex(),output=output);ts[3]=ret;arm_parent(th,key,tuple(ts),(mask&~0x10)|0x40)
     elif ip==ts[1] and word(c,20)&2:arm_parent(th,key,tuple(ts),(mask&~4)|1)
     elif ip==ts[3] and word(c,20)&8:
      f=frames.pop(key);raw=b.required(processes[e.pid],f['output'],96);state,cp,ct=struct.unpack_from('<3I',raw);record=dict(parent_pid=e.pid,parent_tid=e.tid,entry=f,parent_return_context_hex=c.hex(),state_hex=raw.hex(),state=state,child_pid=cp,child_tid=ct);waits.append(record)
      if word(c,176)==0 and cp==child and state in (6,7,8):
       thc=win.opent(0x5a,False,ct);win.check(thc,'stopped original child')
       try:
        cc=b.context(thc);record['child_context_hex']=cc.hex()
        if word(cc,184)==target and word(cc,20)&1:
         s=b.capture(child_h,cp,ct,cc);s['parent_wait_index']=len(waits)-1;captures.append(s);events.append(row);print('captured original',s['label'],'blocks',len(s['debug_graph']),flush=True);break
       finally:win.close(thc)
      arm_parent(th,key,tuple(ts),(mask&~0x40)|0x10)
     else:raise ValueError('only declared parent API entry/return breakpoints')
   elif e.code==4:threads.pop(key,None)
   elif e.code==5:processes.pop(e.pid,None)
   row['continue_status']=status;events.append(row);win.check(b.continue_event(e.pid,e.tid,status),'continue parent debugger event');pending=None
  need(len(captures)==1 and captures[0]['EIP']==target,'one natural original boundary before protector handling')
 except BaseException as exc:error=repr(exc)
 finally:
  members_before=win.ids(job);terminated=bool(win.terminate(job,0x435254)) if members_before else False
  if created and not assigned:win.terminate_parent(pi.process,0x435254)
  if pending:b.continue_event(*pending,0x10002)
  deadline=time.monotonic()+10
  while processes and time.monotonic()<deadline:
   e=b.EVENT()
   if not b.wait_event(C.byref(e),100):continue
   if e.code==3:
    processes[e.pid]=e.u.create.process
    if e.u.create.file:win.close(e.u.create.file)
   if e.code==6 and e.u.file:win.close(e.u.file)
   if e.code==5:processes.pop(e.pid,None)
   events.append(dict(cleanup_event=True,code=e.code,pid=e.pid,tid=e.tid));b.continue_event(e.pid,e.tid,0x10002)
  signaled=bool(created and win.wait(pi.process,5000)==0)
  if child_h:win.wait(child_h,5000);win.close(child_h)
  if created:win.close(pi.thread);win.close(pi.process)
  after=win.ids(job);win.close(job);closed=bool(b.user.CloseDesktop(desktop))
 return dict(schema_version=4,target=target,parent_pid=pi.pid,child_pid=child,original_sha256=b.ORIGINAL_SHA,source_sha256=b.SOURCE_SHA,desktop=dict(name=name,private=True,switched=False,input_sent=False),parent_exports=exports,events=events,debug_register_instrumentation=arms,parent_waits=waits,parent_continues=continues,captures=captures,error=error,cleanup=dict(explicit_probe_termination=terminated,members_before_probe_termination=members_before,members_after_cleanup=after,parent_signaled=signaled,all_debug_process_exits_observed=not processes,private_desktop_closed=closed,original_game_normal_shutdown=False),source_memory_written=False,general_registers_written=False,debugger_reply_substituted=False,retained_heap_restored=False,R3_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable evidence')
 cases=[]
 for i in range(2):
  for target in b.BREAKPOINTS:
   c=observe(target);c['round']=i;cases.append(c)
   if c['error']:break
  if cases[-1]['error']:break
 r=dict(schema_version=4,sampler_source_sha256=sha(Path(__file__).read_bytes()),base_source_sha256=sha(Path(b.__file__).read_bytes()),cases=cases);out.write_bytes(gzip.compress(json.dumps(r,separators=(',',':')).encode(),mtime=0));need(len(cases)==8 and all(c['error']is None for c in cases),'eight original source boundary probes; see preserved diagnostics')
