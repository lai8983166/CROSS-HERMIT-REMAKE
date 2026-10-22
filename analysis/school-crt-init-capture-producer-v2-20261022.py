"""Owned original pre-CRT observations using hardware execution breakpoints.

Private desktop is never switched. No source memory/general registers are written.
Probe job termination is explicit, not original game shutdown.
"""
import argparse,ctypes as C,ctypes.wintypes as W,gzip,json,struct,time,hashlib
from tools import school_startup_inputs as win
from tools.school_retained_crt import FIELDS

ROOT=win.ROOT;k=win.k;H=win.H;D=win.D;P=win.P;S=win.S
APP=ROOT/'CROSS HERMIT/CROSS HERMIT/CROSS HERMIT.EXE'
SOURCE=ROOT/'analysis/hermit_game.exe'
SOURCE_SHA='588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'
ORIGINAL_SHA='030dca584a3a0b20751a72609f7acc823e8d79d820cebf1fcde8be6a791a9df7'
BREAKPOINTS=(0x5713c0,0x49dd70,0x57b9ea,0x576f60)
LABELS={0x5713c0:'before_original_CRT',0x49dd70:'before_original_WinMain',0x57b9ea:'original_HeapCreate_return',0x576f60:'before_original_lock_init'}

class CREATE(C.Structure):
 _fields_=[('file',H),('process',H),('thread',H),('base',P),('debug_offset',D),('debug_bytes',D),('tls',P),('start',P),('image',P),('unicode',W.WORD)]
class THREAD(C.Structure):_fields_=[('thread',H),('tls',P),('start',P)]
class EXCEPTION_RECORD(C.Structure):
 _fields_=[('code',D),('flags',D),('record',P),('address',P),('parameters',D),('information',S*15)]
class EXCEPTION(C.Structure):_fields_=[('record',EXCEPTION_RECORD),('first',D)]
class UNION(C.Union):_fields_=[('create',CREATE),('thread',THREAD),('exception',EXCEPTION),('file',H),('exit_code',D),('raw',C.c_byte*160)]
class EVENT(C.Structure):_fields_=[('code',D),('pid',D),('tid',D),('u',UNION)]

wait_event=win.bind('WaitForDebugEvent',W.BOOL,[C.POINTER(EVENT),D]);continue_event=win.bind('ContinueDebugEvent',W.BOOL,[D,D,D]);set_context=win.bind('Wow64SetThreadContext',W.BOOL,[H,P])
user=C.WinDLL('user32',use_last_error=True)
user.CreateDesktopW.restype=H;user.CreateDesktopW.argtypes=[W.LPCWSTR,W.LPCWSTR,P,D,D,P]
user.CloseDesktop.restype=W.BOOL;user.CloseDesktop.argtypes=[H]
mapped=win.bind('K32GetMappedFileNameW',D,[H,P,W.LPWSTR,D])

def sha(b):return hashlib.sha256(b).hexdigest()
def need(b,s):
 if not b:raise ValueError(s)
def required(h,p,n):
 need(0<=n<=0x300000,'bounded original read');b=win.memory(h,p,n);need(b is not None,'readable original bytes '+hex(p));return b
def word(b,o=0):return struct.unpack_from('<I',b,o)[0]
def context(h):
 b=C.create_string_buffer(736);at=(C.addressof(b)+15)&~15;C.c_uint32.from_address(at).value=0x1003f;win.check(win.ctx(h,at),'Wow64GetThreadContext');return C.string_at(at,716)
def arm(h,mask):
 before=context(h);b=bytearray(before);struct.pack_into('<I',b,0,0x10010)
 for o,v in zip((4,8,12,16,20,24),(*BREAKPOINTS,0,mask)):struct.pack_into('<I',b,o,v)
 buf=C.create_string_buffer(736);at=(C.addressof(buf)+15)&~15;C.memmove(at,bytes(b),716);win.check(set_context(h,at),'Wow64SetThreadContext debug registers only');after=context(h);need(before[28:]==after[28:],'general/FPU/segment state unchanged by debug register write')
 return dict(before_context_hex=before.hex(),requested_debug_context_hex=b.hex(),after_context_hex=after.hex(),general_state_unchanged=True)

def graph(h,values):
 rows=[];p=values['debug_first'];previous=0;seen=set();total=0
 while p:
  need(p not in seen and len(rows)<4096,'bounded acyclic debug graph');seen.add(p);header=required(h,p,32);prev,nxt,file,line,size,kind,request=struct.unpack('<7I',header[:28]);need(prev==previous and size<=0x200000 and total+size<=0x800000,'complete bounded original debug chain');raw=required(h,p,size+36);need(raw[28:32]==raw[-4:]==bytes([0xfd])*4,'original live allocation guards');name=b''
  if file:
   for i in range(512):
    v=required(h,file+i,1)
    if v==bytes(1):break
    name+=v
   else:raise ValueError('bounded original allocation source name')
  rows.append(dict(pointer=p,prev=prev,next=nxt,file=file,line=line,size=size,kind=kind,request=request,source_name_hex=name.hex(),raw_hex=raw.hex()));total+=size;previous=p;p=nxt
 need(previous==values['debug_last'] and total==values['current_bytes'],'entire original graph/current counter');return rows

def capture(h,pid,tid,c):
 ip=word(c,184);data=required(h,0x5ff000,0x20d000);code=required(h,0x401000,0x191000);values={n:word(data,p-0x5ff000) for n,p in FIELDS.items()};sp=word(c,196);stack=required(h,sp,256);slots=(0x59212c,0x59227c,0x592144,0x59218c,0x592258);imports=[]
 for slot in slots:
  p=word(required(h,slot,4));path=C.create_unicode_buffer(1024);n=mapped(h,p,path,len(path));imports.append(dict(slot=slot,target=p,mapped_path=path.value if n else None,entry_hex=required(h,p,16).hex()))
 return dict(label=LABELS[ip],pid=pid,tid=tid,EIP=ip,first_instruction_executed=False,full_context_hex=c.hex(),stack_pointer=sp,stack_hex=stack.hex(),source_text=dict(pointer=0x401000,bytes=len(code),sha256=sha(code),hex=code.hex()),original_data=dict(pointer=0x5ff000,bytes=len(data),sha256=sha(data),hex=data.hex()),globals=values,lock_table_hex=required(h,0x761df0,192).hex(),static_locks=[dict(pointer=p,hex=required(h,p,24).hex()) for p in (0x80a480,0x80a498,0x80a4b0,0x80a4c8)],debug_graph=graph(h,values),actual_import_targets=imports)

def observe():
 need(C.sizeof(P)==8 and C.sizeof(EVENT)==176 and EVENT.u.offset==16,'64-bit debugger ABI');need(sha(APP.read_bytes())==ORIGINAL_SHA and sha(SOURCE.read_bytes())==SOURCE_SHA,'pinned original executable/source')
 desktop_name='CodexCrtInit_'+str(time.time_ns());desktop=user.CreateDesktopW(desktop_name,None,None,0,0x1ff,None);win.check(desktop,'private desktop');job=win.jobnew(None,None);win.check(job,'owned job');limits=C.create_string_buffer(144);struct.pack_into('<I',limits,16,0x2000);win.check(win.setjob(job,9,limits,len(limits)),'kill-on-close job')
 pi=win.PI();si=win.SI();si.cb=C.sizeof(si);si.flags=1;si.show=0;si.desktop='winsta0'+chr(92)+desktop_name;created=False;assigned=False;pending=None;processes={};threads={};events=[];arms=[];captures=[];error=None;cleanup={};mask=0x55
 try:
  win.check(win.create(str(APP.resolve()),None,None,None,False,0x08000005,None,str(APP.parent.resolve()),C.byref(si),C.byref(pi)),'debug original on private desktop');created=True;win.check(win.assign(job,pi.process),'assign owned original');assigned=True;win.resume(pi.thread);deadline=time.monotonic()+35
  while time.monotonic()<deadline and len(events)<12000:
   e=EVENT()
   if not wait_event(C.byref(e),100):continue
   pending=(e.pid,e.tid);status=0x10002;row=dict(code=e.code,pid=e.pid,tid=e.tid)
   if e.code==3:
    processes[e.pid]=e.u.create.process;threads[(e.pid,e.tid)]=e.u.create.thread;row.update(image_base=e.u.create.base,start=e.u.create.start);arms.append(dict(pid=e.pid,tid=e.tid,event_index=len(events),**arm(e.u.create.thread,mask)))
    if e.u.create.file:win.close(e.u.create.file)
   elif e.code==2:threads[(e.pid,e.tid)]=e.u.thread.thread;arms.append(dict(pid=e.pid,tid=e.tid,event_index=len(events),**arm(e.u.thread.thread,mask)))
   elif e.code==6:
    if e.u.file:win.close(e.u.file)
   elif e.code==1:
    ex=e.u.exception;row.update(exception_code=ex.record.code,exception_address=ex.record.address,first_chance=ex.first);status=0x80010001
    if ex.record.code==0x80000003:
     status=0x10002;th=threads[(e.pid,e.tid)];c=context(th);row.update(EIP=word(c,184),DR6=word(c,20),DR7=word(c,24),source_prefix_hex=(win.memory(processes[e.pid],0x5713c0,16) or b'').hex());arms.append(dict(pid=e.pid,tid=e.tid,event_index=len(events),loader_breakpoint_rearm=True,**arm(th,mask)))
    elif ex.record.code==0x80000004:
     th=threads[(e.pid,e.tid)];c=context(th);ip=word(c,184);row.update(EIP=ip,DR6=word(c,20),DR7=word(c,24))
     if ip in BREAKPOINTS and word(c,20)&(1<<BREAKPOINTS.index(ip)):
      s=capture(processes[e.pid],e.pid,e.tid,c);s['event_index']=len(events);captures.append(s);print('captured',s['label'],'pid',e.pid,'blocks',len(s['debug_graph']),flush=True);status=0x10002
      newmask=word(c,24)&~(1<<(2*BREAKPOINTS.index(ip)));arms.append(dict(pid=e.pid,tid=e.tid,event_index=len(events),**arm(th,newmask)))
      if ip==0x49dd70:events.append(row);break
   elif e.code==4:threads.pop((e.pid,e.tid),None)
   elif e.code==5:row['exit_code']=e.u.exit_code;processes.pop(e.pid,None)
   row['continue_status']=status;events.append(row);win.check(continue_event(e.pid,e.tid,status),'ContinueDebugEvent');pending=None
  need([s['EIP'] for s in captures]==[0x5713c0,0x57b9ea,0x576f60,0x49dd70],'four natural original CRT boundaries before WinMain')
 except BaseException as exc:error=repr(exc)
 finally:
  members_before=win.ids(job);terminated=False
  if members_before:terminated=bool(win.terminate(job,0x435254))
  if created and not assigned:win.terminate_parent(pi.process,0x435254)
  if pending:continue_event(*pending,0x10002);pending=None
  deadline=time.monotonic()+10
  while processes and time.monotonic()<deadline:
   e=EVENT()
   if not wait_event(C.byref(e),100):continue
   if e.code==3:
    processes[e.pid]=e.u.create.process
    if e.u.create.file:win.close(e.u.create.file)
   if e.code==6 and e.u.file:win.close(e.u.file)
   if e.code==5:processes.pop(e.pid,None)
   events.append(dict(cleanup_event=True,code=e.code,pid=e.pid,tid=e.tid,exit_code=e.u.exit_code if e.code==5 else None));continue_event(e.pid,e.tid,0x10002)
  parent_signaled=bool(created and win.wait(pi.process,5000)==0)
  if created:win.close(pi.thread);win.close(pi.process)
  members_after=win.ids(job);win.close(job);desktop_closed=bool(user.CloseDesktop(desktop));cleanup=dict(explicit_probe_termination=terminated,members_before_probe_termination=members_before,members_after_cleanup=members_after,parent_signaled=parent_signaled,all_debug_process_exits_observed=not processes,private_desktop_closed=desktop_closed,original_game_normal_shutdown=False)
 return dict(schema_version=1,original_sha256=ORIGINAL_SHA,source_sha256=SOURCE_SHA,debugger_pointer_bytes=8,debug_event_bytes=C.sizeof(EVENT),desktop=dict(name=desktop_name,private=True,switched=False,input_sent=False),parent_pid=pi.pid,error=error,events=events,debug_register_instrumentation=arms,captures=captures,cleanup=cleanup,source_memory_written=False,general_registers_written=False,original_WinMain_executed=False,retained_heap_restored=False,R3_complete=False)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable evidence required')
 cases=[]
 for i in range(2):
  r=observe();cases.append(r)
  if r['error']:break
 out.write_bytes(gzip.compress(json.dumps(dict(schema_version=1,sampler_source_sha256=sha(__import__('pathlib').Path(__file__).read_bytes()),cases=cases),separators=(',',':')).encode(),mtime=0));need(len(cases)==2 and all(c['error']is None for c in cases),'two actual original CRT captures; see preserved failure evidence')
