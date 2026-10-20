"""Read-only original startup/teardown observation in an exclusively owned Job.

No debugger attachment, instruction/register replacement, imported return stub, or
write to the original process. Native execution is not an emulator checkpoint.
"""
import argparse
from contextlib import contextmanager
from tools.school_startup_inputs import *

user=C.WinDLL('user32',use_last_error=True)
def ubind(name,result,args):
 f=getattr(user,name);f.restype=result;f.argtypes=args;return f
ownerpid=ubind('GetWindowThreadProcessId',D,[H,C.POINTER(D)])
getprop=ubind('GetPropA',P,[H,W.LPCSTR])
iswindow=ubind('IsWindow',W.BOOL,[H])
post=ubind('PostMessageW',W.BOOL,[H,W.UINT,W.WPARAM,W.LPARAM])
findwindow=ubind('FindWindowA',H,[W.LPCSTR,W.LPCSTR])
getexit=bind('GetExitCodeProcess',W.BOOL,[H,C.POINTER(D)])
mapped=bind('K32GetMappedFileNameW',D,[H,P,W.LPWSTR,D])
SOURCE=ROOT/'analysis/hermit_game.exe'
SOURCE_SHA='588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'
ORIGINAL_SHA='030dca584a3a0b20751a72609f7acc823e8d79d820cebf1fcde8be6a791a9df7'
GLOBAL_ADDRESSES=(0x7a49fc,0x7a4a00,0x80a398,0x7a0bb4)
# Finite original bodies, including callers and the native destruction routes.
RANGES=((0x49dd70,0x49e14a),(0x450350,0x45056c),(0x450570,0x45072b),
 (0x450730,0x4507c0),(0x413450,0x41355b),(0x413560,0x4136d0),
 (0x40d970,0x40d9ba),(0x4248e0,0x424978),(0x424980,0x424a89),
 (0x450d30,0x45104c),(0x49e150,0x49e1a0),(0x44fe60,0x44ffa0),
 (0x412dd0,0x412e30),(0x413190,0x413444),(0x416140,0x416255),
 (0x415f50,0x416133),(0x4010d0,0x40180d),(0x401810,0x401d20),
 (0x40dab0,0x40dc80),(0x5714d2,0x5714f2))

class OwnedOriginal:
 def __init__(self):
  self.job=jobnew(None,None);check(self.job,'CreateJobObjectW')
  self.pi=PI();self.created=False;self.assigned=False;self.handles={};self.history=[]
  self.forced=False;self.started=time.monotonic()
  limits=C.create_string_buffer(144);struct.pack_into('<I',limits,16,0x2000)
  check(setjob(self.job,9,limits,len(limits)),'kill-on-close Job limit')
 def start(self):
  app=(ROOT/'CROSS HERMIT/CROSS HERMIT/CROSS HERMIT.EXE').resolve()
  if hashlib.sha256(app.read_bytes()).hexdigest()!=ORIGINAL_SHA:raise ValueError('original identity')
  si=SI();si.cb=C.sizeof(si);si.flags=1;si.show=0
  check(create(str(app),None,None,None,False,0x08000004,None,str(app.parent),C.byref(si),C.byref(self.pi)),'original create')
  self.created=True;check(assign(self.job,self.pi.process),'original assign');self.assigned=True
  if resume(self.pi.thread)==0xffffffff:raise OSError(C.get_last_error(),'original resume')
 def members(self):
  members=ids(self.job)
  if not self.history or self.history[-1]['pids']!=members:self.history.append(dict(elapsed=self.elapsed(),pids=members))
  for pid in members:
   if pid not in self.handles:
    h=openp(0x410|0x100000,False,pid)
    if h:self.handles[pid]=h
  return members
 def elapsed(self):return time.monotonic()-self.started
 def finish(self):
  before=self.members()
  if before:self.forced=True;check(terminate(self.job,1),'owned emergency termination')
  if self.created and not self.assigned:terminate_parent(self.pi.process,1);self.forced=True
  exits={}
  for pid,h in self.handles.items():
   signaled=wait(h,5000)==0;v=D();check(getexit(h,C.byref(v)),'process exit code')
   exits[str(pid)]=dict(signaled=signaled,code=v.value);close(h)
  if self.created:wait(self.pi.process,5000);close(self.pi.thread);close(self.pi.process)
  after=ids(self.job);close(self.job)
  return dict(parent_pid=self.pi.pid,membership=self.history,members_before_cleanup=before,
   forced_termination=self.forced,exits=exits,members_after_cleanup=after,
   child_status_is_not_WinMain_return=True)

@contextmanager
def frozen(h,pid,thread_ids=None):
 held=[];frames=[]
 try:
  for tid in threads(pid) if thread_ids is None else thread_ids:
   th=opent(0x4a,False,tid)
   if not th:continue
   if suspend(th)==0xffffffff:close(th);continue
   held.append(th);buf=C.create_string_buffer(736);at=(C.addressof(buf)+15)&~15
   C.memset(at,0,716);C.c_uint32.from_address(at).value=0x1003f
   if not ctx(th,at):continue
   b=C.string_at(at,716);bp=struct.unpack_from('<I',b,180)[0];chain=[]
   for _ in range(100):
    v=memory(h,bp,8)
    if v is None:break
    nb,ret=struct.unpack('<II',v);chain.append(dict(bp=bp,saved_bp=nb,return_va=ret))
    if not bp<nb<bp+0x100000:break
    bp=nb
   # Full actual context is evidence, not a register input for any emulator.
   frames.append(dict(tid=tid,context_hex=b.hex(),EIP=struct.unpack_from('<I',b,184)[0],
    EBP=struct.unpack_from('<I',b,180)[0],ESP=struct.unpack_from('<I',b,196)[0],chain=chain))
  yield frames
 finally:
  for th in reversed(held):resume(th);close(th)

def required(h,at,n):
 v=memory(h,at,n)
 if v is None:raise ValueError('unreadable actual object '+hex(at))
 return v

def globals_at(h):
 values=[memory(h,at,4) for at in GLOBAL_ADDRESSES]
 return None if any(v is None for v in values) else dict(zip((hex(a) for a in GLOBAL_ADDRESSES),(int.from_bytes(v,'little') for v in values)))

def source_at(h,raw):
 rows=[]
 for a,b in RANGES:
  actual=required(h,a,b-a);expected=raw[a-0x400000:b-0x400000]
  if actual!=expected:raise ValueError('live original code differs '+hex(a))
  rows.append(dict(va=a,bytes=b-a,sha256=hashlib.sha256(actual).hexdigest()))
 return rows

def capture(h,pid,frames,g,elapsed,raw,objects=False):
 s=dict(pid=pid,elapsed=elapsed,globals=g,frames=frames,source=source_at(h,raw))
 # 5714E6 is the original CRT return address of WinMain. The immediately
 # preceding frame's saved EBP is WinMain's actual EBP, even inside libraries.
 bp=None
 for f in frames:
  for row in f['chain']:
   if row['return_va']==0x5714e6:bp=row['bp'];break
  if bp:break
 if bp:
  s['winmain_frame']=dict(bp=bp,locals_hex=required(h,bp-0x9c,0x9c).hex(),args_hex=required(h,bp+8,16).hex(),
   stack_start=bp-0xac,stack_hex=required(h,bp-0xac,0xd0).hex())
 for f in frames:
  for row in f['chain']:
   if row['return_va']==0x5714f2:
    caller=row['saved_bp']
    s['crt_exit']=dict(callee_bp=row['bp'],caller_bp=caller,
     WinMain_result_hex=required(h,caller-0x60,4).hex(),exit_argument_hex=required(h,row['bp']+8,4).hex())
 if objects:
  main=g['0x7a4a00'];game=g['0x7a49fc'];cache=g['0x80a398']
  s['main']=dict(pointer=main,hex=required(h,main,0x1110).hex())
  owner=required(h,game,0xba20);s['game']=dict(pointer=game,hex=owner.hex())
  s['cache']=dict(pointer=cache,hex=required(h,cache,176).hex())
  cb=bytes.fromhex(s['cache']['hex']);sprite=struct.unpack_from('<I',cb,12)[0]
  s['cache_sprite']=dict(pointer=sprite,hex=required(h,sprite,32).hex())
  bits=struct.unpack_from('<I',cb,0xa0)[0];bitmap=required(h,bits,256*256*4)
  s['cache_bitmap']=dict(pointer=bits,bytes=len(bitmap),sha256=hashlib.sha256(bitmap).hexdigest())
  def word(off):return struct.unpack_from('<I',owner,off)[0]
  s['fonts']=[dict(offset=off,pointer=word(off),hex=required(h,word(off),0x678 if off!=0xb270 else 80).hex()) for off in (0x1090,0x1094,0xb270)]
  s['queues']=[]
  for off,n in ((0x1068,word(0x1060)*8),(0x106c,word(0x1064))):
   if not 0<n<=0x100000:raise ValueError('source queue capacity')
   data=required(h,word(off),n)
   s['queues'].append(dict(offset=off,pointer=word(off),bytes=n,sha256=hashlib.sha256(data).hexdigest(),head_hex=data[:32].hex(),tail_hex=data[-32:].hex()))
  s['interfaces']=[]
  for off in (0xb20c,0xb210,0x1aa0,0x1aa4,0x1aa8):
   ptr=word(off);head=required(h,ptr,16);vt=int.from_bytes(head[:4],'little');table=required(h,vt,64)
   method=int.from_bytes(table[:4],'little');name=C.create_unicode_buffer(2048)
   check(mapped(h,method,name,len(name)),'actual interface method mapping')
   s['interfaces'].append(dict(offset=off,pointer=ptr,head_hex=head.hex(),vtable=vt,vtable_hex=table.hex(),
    first_method_hex=required(h,method,16).hex(),method_module=name.value))
  hwnd=g['0x7a0bb4'];wpid=D();tid=ownerpid(hwnd,C.byref(wpid))
  s['window']=dict(hwnd=hwnd,tid=tid,pid=wpid.value,is_window=bool(iswindow(hwnd)),property=getprop(hwnd,b'CPP_CLASS') or 0,
   find_window=findwindow(b'Cross Hermit',None) or 0)
 return s

def observe(duplicate=True):
 raw=SOURCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA:raise ValueError('source identity')
 o=OwnedOriginal();result=dict(error=None,factory=None,ready=None,shutdown=[],duplicate=None,close_request=None)
 try:
  # A foreign game window changes the original duplicate gate. Read-only refusal
  # protects it: this observer never posts a message to a preexisting window.
  if findwindow(b'Cross Hermit',None):raise RuntimeError('preexisting original window; no foreign window touched')
  o.start();deadline=time.monotonic()+25
  while time.monotonic()<deadline and result['ready'] is None:
   for pid in o.members():
    h=o.handles.get(pid)
    if not h or memory(h,0x49dd70,96)!=raw[0x9dd70:0x9ddd0]:continue
    g=globals_at(h)
    if not g or not g['0x7a4a00'] or not g['0x7a0bb4']:continue
    with frozen(h,pid) as frames:
     g=globals_at(h)
     factory=any(0x49df8a in [r['return_va'] for r in f['chain']] and 0x45060f in [r['return_va'] for r in f['chain']] for f in frames)
     loop=any(0x49dfd1<=f['EIP']<0x49e092 or any(0x49dfd1<=r['return_va']<0x49e092 for r in f['chain']) for f in frames)
     if result['factory'] is None and factory:result['factory']=capture(h,pid,frames,g,o.elapsed(),raw)
     if loop and g['0x7a49fc'] and g['0x80a398']:
      result['ready']=capture(h,pid,frames,g,o.elapsed(),raw,objects=True)
   time.sleep(.002)
  if result['factory'] is None or result['ready'] is None:raise RuntimeError('fresh factory and initialized WinMain loop not both observed')
  s=result['ready'];hwnd=s['globals']['0x7a0bb4'];pid=s['pid'];h=o.handles[pid]
  if duplicate:
   d=OwnedOriginal();dr=dict(before_window=hwnd,error=None,observations=[])
   try:
    if findwindow(b'Cross Hermit',None)!=hwnd:raise ValueError('owned original duplicate prerequisite')
    d.start();deadline=time.monotonic()+8
    while time.monotonic()<deadline:
     members=d.members()
     if not members:break
     for dp in members:
      dh=d.handles.get(dp);gg=globals_at(dh) if dh else None
      if gg and gg['0x7a4a00']:
       dr['observations'].append(dict(pid=dp,elapsed=d.elapsed(),globals=gg))
     time.sleep(.001)
    dr.update(after_window=findwindow(b'Cross Hermit',None) or 0,elapsed=d.elapsed())
   except Exception as e:dr['error']=repr(e)
   finally:dr['lifetime']=d.finish()
   result['duplicate']=dr
  # Recheck both property and Job membership immediately before sending. These
  # are the only writes to the environment: a normal message to our own HWND.
  wp=D();ownerpid(hwnd,C.byref(wp));members=o.members();prop=getprop(hwnd,b'CPP_CLASS') or 0
  if wp.value!=pid or pid not in members or prop!=s['main']['pointer']:raise ValueError('close ownership changed')
  result['close_request']=dict(hwnd=hwnd,pid=pid,job_members=members,property=prop,message=16,wParam=0,lParam=0,
   elapsed=o.elapsed(),posted=bool(post(hwnd,16,0,0)))
  if not result['close_request']['posted']:raise OSError(C.get_last_error(),'owned WM_CLOSE')
  deadline=time.monotonic()+15;last=None
  while time.monotonic()<deadline:
   if not o.members():break
   g=globals_at(h)
   if g is not None:
    # Capture full contexts on changes or on the WinMain cleanup chain. Sampling
    # is not a claim to have logged every native API or every destructor call.
    with frozen(h,pid,[s['window']['tid']]) as frames:
     g=globals_at(h)
     relevant=any(any(0x49e092<=r['return_va']<0x49e14a for r in f['chain']) or 0x49e092<=f['EIP']<0x49e14a for f in frames)
     signature=tuple(g.values()) if g else None
     if g and (signature!=last or relevant and len(result['shutdown'])<32):
      result['shutdown'].append(capture(h,pid,frames,g,o.elapsed(),raw));last=signature
   time.sleep(.001)
  result['window_after']=dict(is_window=bool(iswindow(hwnd)),property=getprop(hwnd,b'CPP_CLASS') or 0)
 except Exception as e:result['error']=repr(e)
 finally:result['lifetime']=o.finish()
 result.update(original_code_written=False,original_registers_written=False,original_IAT_written=False,
  native_execution=True,retained_VM_advanced=False,resumable_checkpoint=False)
 return result

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--cases',type=int,default=2);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable evidence path required')
 cases=[]
 for i in range(a.cases):
  r=observe();cases.append(r)
  print('case',i,'error',r['error'],'ready',r['ready'] is not None,'teardown samples',len(r['shutdown']),'exits',r['lifetime']['exits'],flush=True)
 out.write_text(json.dumps(dict(schema_version=1,source_image_sha256=SOURCE_SHA,original_sha256=ORIGINAL_SHA,
  observer_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases),indent=2)+'\n',encoding='utf8',newline='\n')
 if any(c['error'] is not None for c in cases):raise SystemExit(1)
