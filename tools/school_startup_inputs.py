"""Read fresh pre-publication globals in an owned original process tree; no game patch."""
import ctypes as C,ctypes.wintypes as W,json,time,struct,hashlib
from pathlib import Path
k=C.WinDLL('kernel32',use_last_error=True)
H=W.HANDLE;D=W.DWORD;P=C.c_void_p;S=C.c_size_t
class SI(C.Structure):
 _fields_=[('cb',D),('reserved',W.LPWSTR),('desktop',W.LPWSTR),('title',W.LPWSTR),('x',D),('y',D),('cx',D),('cy',D),('xChars',D),('yChars',D),('fill',D),('flags',D),('show',W.WORD),('reserved2',W.WORD),('reservedPtr',P),('stdin',H),('stdout',H),('stderr',H)]
class PI(C.Structure):_fields_=[('process',H),('thread',H),('pid',D),('tid',D)]
class TE(C.Structure):_fields_=[('size',D),('usage',D),('tid',D),('pid',D),('base',W.LONG),('delta',W.LONG),('flags',D)]
def bind(n,rest,args):
 f=getattr(k,n);f.restype=rest;f.argtypes=args;return f
jobnew=bind('CreateJobObjectW',H,[P,W.LPCWSTR]);setjob=bind('SetInformationJobObject',W.BOOL,[H,C.c_int,P,D]);assign=bind('AssignProcessToJobObject',W.BOOL,[H,H]);queryjob=bind('QueryInformationJobObject',W.BOOL,[H,C.c_int,P,D,P])
create=bind('CreateProcessW',W.BOOL,[W.LPCWSTR,W.LPWSTR,P,P,W.BOOL,D,P,W.LPCWSTR,C.POINTER(SI),C.POINTER(PI)])
resume=bind('ResumeThread',D,[H]);suspend=bind('SuspendThread',D,[H]);ctx=bind('Wow64GetThreadContext',W.BOOL,[H,P])
read=bind('ReadProcessMemory',W.BOOL,[H,P,P,S,C.POINTER(S)]);openp=bind('OpenProcess',H,[D,W.BOOL,D]);opent=bind('OpenThread',H,[D,W.BOOL,D]);close=bind('CloseHandle',W.BOOL,[H]);wait=bind('WaitForSingleObject',D,[H,D]);terminate=bind('TerminateJobObject',W.BOOL,[H,W.UINT]);terminate_parent=bind('TerminateProcess',W.BOOL,[H,W.UINT])
snapshot=bind('CreateToolhelp32Snapshot',H,[D,D]);first=bind('Thread32First',W.BOOL,[H,C.POINTER(TE)]);nextt=bind('Thread32Next',W.BOOL,[H,C.POINTER(TE)])
def check(v,name):
 if not v:raise OSError(C.get_last_error(),name)
def memory(h,at,n):
 b=C.create_string_buffer(n);got=S();return b.raw if read(h,at,b,n,C.byref(got)) and got.value==n else None
def ids(job):
 b=C.create_string_buffer(65536);check(queryjob(job,3,b,len(b),None),'job members');n=struct.unpack_from('<I',b.raw,4)[0];return list(struct.unpack_from('<'+'Q'*n,b.raw,8))
def threads(pid):
 h=snapshot(4,0);check(h,'thread snapshot');t=TE();t.size=C.sizeof(t);rr=[]
 try:
  ok=first(h,C.byref(t))
  while ok:
   if t.pid==pid:rr.append(t.tid)
   ok=nextt(h,C.byref(t))
 finally:close(h)
 return rr

from tools.school_window_events import ROOT
import argparse


def observe():
 raw=(ROOT/'analysis/hermit_game.exe').read_bytes();source=raw[0x9dd70:0x9ddd0]
 job=jobnew(None,None);check(job,'job');limits=C.create_string_buffer(144);struct.pack_into('<I',limits,16,0x2000);check(setjob(job,9,limits,len(limits)),'job limits')
 app=(ROOT/'CROSS HERMIT/CROSS HERMIT/CROSS HERMIT.EXE').resolve();si=SI();si.cb=C.sizeof(si);si.flags=1;si.show=0;pi=PI();owned={};samples=[];result=None;error=None;created=False;assigned=False
 try:
  if hashlib.sha256(app.read_bytes()).hexdigest()!='030dca584a3a0b20751a72609f7acc823e8d79d820cebf1fcde8be6a791a9df7':raise ValueError('original executable identity')
  check(create(str(app),None,None,None,False,0x08000004,None,str(app.parent),C.byref(si),C.byref(pi)),'create');created=True;check(assign(job,pi.process),'assign');assigned=True;resume(pi.thread);start=time.monotonic()
  while time.monotonic()-start<25:
   members=ids(job)
   for pid in members:
    if pid not in owned:
     h=openp(0x410|0x100000,False,pid)
     if h:owned[pid]=h
    h=owned.get(pid)
    if not h or memory(h,0x49dd70,len(source))!=source:continue
    held=[];frames=[]
    try:
     for tid in threads(pid):
      th=opent(0x4a,False,tid)
      if not th:continue
      if suspend(th)==0xffffffff:close(th);continue
      held.append(th);buf=C.create_string_buffer(736);at=(C.addressof(buf)+15)&~15;C.memset(at,0,716);C.c_uint32.from_address(at).value=0x1003f
      if not ctx(th,at):continue
      b=C.string_at(at,716);bp=struct.unpack_from('<I',b,180)[0];ip=struct.unpack_from('<I',b,184)[0];chain=[]
      for index in range(100):
       v=memory(h,bp,8)
       if v is None:break
       nb,ret=struct.unpack('<II',v);chain.append(dict(bp=bp,saved_bp=nb,return_va=ret))
       if not bp<nb<bp+0x100000:break
       bp=nb
      relevant=0x49dd70<=ip<0x49df85 or any(0x49dd70<=f['return_va']<=0x49df8a for f in chain)
      frames.append(dict(tid=tid,EIP=ip,EBP=struct.unpack_from('<I',b,180)[0],ESP=struct.unpack_from('<I',b,196)[0],chain=chain,relevant=relevant))
     values={hex(a):memory(h,a,4).hex() for a in (0x7a49fc,0x7a4a00,0x80a398)}
     sample=dict(pid=pid,elapsed=time.monotonic()-start,globals=values,frames=frames,winmain_hex=memory(h,0x49dd70,len(source)).hex(),job_members=members)
     sample['main_header_hex']=memory(h,int.from_bytes(bytes.fromhex(values['0x7a4a00']),'little'),16).hex();sample['published_hwnd_hex']=memory(h,0x7a0bb4,4).hex();samples.append(sample)
     if any(f['relevant'] for f in frames):result=sample;break
    finally:
     for th in reversed(held):resume(th);close(th)
   if result:break
   time.sleep(0.001)
  if result is None:raise RuntimeError('owned original pre-factory WinMain frame not observed')
 except Exception as e:error=repr(e)
 finally:
  terminated=bool(terminate(job,1))
  if created and not assigned:terminate_parent(pi.process,1)
  exits={str(pid):wait(h,5000)==0 for pid,h in owned.items()}
  for h in owned.values():close(h)
  if created:wait(pi.process,5000);close(pi.thread);close(pi.process)
  members_after=ids(job);close(job)
 return dict(app=str(app),original_sha256=hashlib.sha256(app.read_bytes()).hexdigest(),error=error,result=result,samples=samples,terminated_owned_job=terminated,owned_process_exit=exits,job_members_after_termination=members_after,original_code_modified=False,original_general_registers_modified=False)


def verify_observation(r):
 if r['error'] is not None or r['original_sha256']!='030dca584a3a0b20751a72609f7acc823e8d79d820cebf1fcde8be6a791a9df7':raise ValueError('actual owned original capture failed')
 s=r['result'];raw=(ROOT/'analysis/hermit_game.exe').read_bytes()
 if s['winmain_hex']!=raw[0x9dd70:0x9ddd0].hex() or not any(0x49df8a in [x['return_va'] for x in f['chain']] and 0x45060f in [x['return_va'] for x in f['chain']] for f in s['frames']):raise ValueError('real original WinMain/game-factory frame required')
 if s['globals']['0x7a49fc']!='00000000' or s['globals']['0x80a398']!='00000000':raise ValueError('fresh observed game/cache input differs')
 main=bytes.fromhex(s['main_header_hex']);hwnd=int.from_bytes(bytes.fromhex(s['published_hwnd_hex']),'little')
 if len(main)!=16 or struct.unpack_from('<I',main)[0]!=0x5986a0 or struct.unpack_from('<I',main,4)[0]!=hwnd or hwnd==0:raise ValueError('original constructed main and published window required')
 if not r['terminated_owned_job'] or not r['owned_process_exit'] or not all(r['owned_process_exit'].values()) or r['job_members_after_termination'] or r['original_code_modified'] or r['original_general_registers_modified']:raise ValueError('owned original observation lifetime/integrity')
 return {0x7a49fc:0,0x80a398:0}


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh observation file required')
 cases=[observe(),observe()];out.write_text(json.dumps(dict(sampler_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=cases),indent=2)+'\n',encoding='utf8',newline='\n')
 for c in cases:print('observed fresh inputs',verify_observation(c),'owned processes exited',c['owned_process_exit'])
