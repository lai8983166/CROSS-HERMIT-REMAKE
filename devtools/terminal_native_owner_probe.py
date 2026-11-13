"""One-shot, 30s, no-UI original base-worker/platform-owner preflight.

This is a declared cold function fixture, not a scene or native-image replay.
Original guest instructions execute in Unicorn; actual OS leaves execute on
the two permanently bound threads of one x86 helper. No game input exists.
"""
from __future__ import annotations
import argparse
import ctypes as C
import ctypes.wintypes as W
import gzip
import hashlib
import json
import os
from pathlib import Path
import queue
import struct
import sys
import threading
import time

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn import x86_const as X
from tools import school_crt_init_fixture as cold
from tools.terminal_unit_frontends_trace import MemoryDigest
from devtools.terminal_wait_registration_probe import full_cpu, validate_thread_request
from devtools.terminal_oplock_probe_v2 import Owned, SI, PI
from devtools.terminal_oplock import Win

ROOT = Path(__file__).resolve().parents[1]
MANAGER, NODE, WORK_STACK = 0x65001000, 0x65002000, 0x65300000
GDT, MAIN_TEB, WORK_TEB = 0x65400000, 0x65401000, 0x65402000
RETURN = cold.old.RETURN
ARGC = dict(HeapCreate=3, HeapAlloc=3, HeapFree=3, HeapValidate=3, HeapDestroy=1,
    InitializeCriticalSection=1, EnterCriticalSection=1, LeaveCriticalSection=1,
    DeleteCriticalSection=1, CreateEventA=4, ResetEvent=1, SetEvent=1, CloseHandle=1,
    WaitForSingleObject=2, CreateThread=6, ResumeThread=1, GetExitCodeThread=2,
    TlsAlloc=0, TlsFree=1, TlsGetValue=1, TlsSetValue=2, GetCurrentThreadId=0,
    GetLastError=0, SetLastError=1, ExitThread=1, IsBadReadPtr=2, IsBadWritePtr=2,
    GetVersionExA=1, GetCurrentDirectoryA=2, GetTickCount=0, Sleep=1)


def need(v, why):
    if not v: raise ValueError(why)


def sha(b): return hashlib.sha256(b).hexdigest()


def identity(p):
    p = Path(p); b = p.read_bytes()
    return dict(path=p.relative_to(ROOT).as_posix(), bytes=len(b), sha256=sha(b))


def build_gate(helper):
    import pefile
    record=helper.parent/'static-report.json'
    data=json.loads(record.read_text(encoding='utf-8'))
    need(data['source']==identity(ROOT/'devtools/terminal_native_owner.cpp'),'reviewed current native source')
    need(identity(helper) in data['artifacts'],'reviewed exact executable build')
    pe=pefile.PE(str(helper))
    need(pe.FILE_HEADER.Machine==0x14c and pe.OPTIONAL_HEADER.Subsystem==2,'x86 no-console executable')
    need({i.dll.lower() for i in pe.DIRECTORY_ENTRY_IMPORT}=={b'kernel32.dll'},'no GUI/input imports')
    return dict(report=identity(record),helper=identity(helper),source=data['source'],machine=0x14c,subsystem=2)


def implementation_pins():
    paths={Path(__file__).resolve(),ROOT/'analysis/hermit_real_iat.json'}
    for module in list(sys.modules.values()):
        name=getattr(module,'__file__',None)
        if name:
            p=Path(name).resolve()
            if p.suffix=='.py' and (p.is_relative_to(ROOT/'tools') or p.is_relative_to(ROOT/'devtools')):paths.add(p)
    return [identity(p) for p in sorted(paths)]


class SA(C.Structure):
    _fields_ = [('length', W.DWORD), ('descriptor', C.c_void_p), ('inherit', W.BOOL)]


class Owner(Owned):
    """Suspended creation, Job assignment before resume, independent deadline."""
    def __init__(self, exe, folder):
        self.w = Win(); k = self.w.k
        def bind(n, r, a):
            f = getattr(k, n); f.restype = r; f.argtypes = a; return f
        self.jobnew = bind('CreateJobObjectW', W.HANDLE, [C.c_void_p,W.LPCWSTR])
        self.setjob = bind('SetInformationJobObject',W.BOOL,[W.HANDLE,C.c_int,C.c_void_p,W.DWORD])
        self.assign = bind('AssignProcessToJobObject',W.BOOL,[W.HANDLE,W.HANDLE])
        self.queryjob = bind('QueryInformationJobObject',W.BOOL,[W.HANDLE,C.c_int,C.c_void_p,W.DWORD,C.c_void_p])
        self.terminate = bind('TerminateJobObject',W.BOOL,[W.HANDLE,W.UINT])
        self.create = bind('CreateProcessW',W.BOOL,[W.LPCWSTR,W.LPWSTR,C.c_void_p,C.c_void_p,W.BOOL,W.DWORD,C.c_void_p,W.LPCWSTR,C.POINTER(SI),C.POINTER(PI)])
        pipe = bind('CreatePipe',W.BOOL,[C.POINTER(W.HANDLE),C.POINTER(W.HANDLE),C.POINTER(SA),W.DWORD])
        flags = bind('SetHandleInformation',W.BOOL,[W.HANDLE,W.DWORD,W.DWORD])
        self.writefile = bind('WriteFile',W.BOOL,[W.HANDLE,C.c_void_p,W.DWORD,C.POINTER(W.DWORD),C.c_void_p])
        self.readfile = bind('ReadFile',W.BOOL,[W.HANDLE,C.c_void_p,W.DWORD,C.POINTER(W.DWORD),C.c_void_p])
        self.job = None; self.pi = PI(); self.started = self.assigned = False
        self.receipt = dict(parent_pid=None,forced=False,exits={},handles_closed=False,job_empty=False)
        self.pipes = []; self.timer = None; self.expired = False; self.finished=False; self.resumed=False
        self.trace = []; self.events = []; self.responses = {}; self.q = queue.Queue()
        self.requests={}; self.seq = 0; self.start = time.monotonic(); self.deadline = self.start + 30
        try:
            self.job = self.jobnew(None,None); self.w.check(self.job,'owner Job')
            limit = C.create_string_buffer(144); struct.pack_into('<I',limit,16,0x2000)
            self.w.check(self.setjob(self.job,9,limit,144),'kill on close')
            sa = SA(C.sizeof(SA),None,True)
            childin,parentin,parentout,childout = (W.HANDLE() for _ in range(4))
            for r,w in ((childin,parentin),(parentout,childout)):
                self.w.check(pipe(C.byref(r),C.byref(w),C.byref(sa),0),'owner pipe')
                self.pipes.extend([r.value,w.value])
            for h in (parentin,parentout): self.w.check(flags(h,1,0),'private parent pipe')
            self.input,self.output = parentin.value,parentout.value
            si = SI(); si.cb=C.sizeof(si); si.flags=0x101; si.show=0
            si.input=childin; si.output=childout; si.error=childout
            env=dict(os.environ,TEMP=str(folder),TMP=str(folder))
            block=C.create_unicode_buffer('\0'.join(k+'='+v for k,v in sorted(env.items()))+'\0\0')
            cmd=C.create_unicode_buffer('"'+str(exe)+'"')
            self.w.check(self.create(str(exe),cmd,None,None,True,0x08000404,block,str(folder),C.byref(si),C.byref(self.pi)),'no-window suspended owner')
            self.started=True; self.receipt['parent_pid']=self.pi.pid
            self.w.check(self.assign(self.job,self.pi.process),'assign before resume'); self.assigned=True
            for h in (childin.value,childout.value):
                self.w.close(h); self.pipes.remove(h)
            def expire():
                self.expired=True
                if self.job: self.terminate(self.job,95)
            self.timer=threading.Timer(max(0,self.deadline-time.monotonic()),expire)
            self.timer.daemon=True; self.timer.start()
            need(self.w.resume(self.pi.thread)==1,'one resume')
            self.resumed=True
            self.reader=threading.Thread(target=self._read,daemon=True); self.reader.start()
            while not any(e['event']=='READY' for e in self.events): self.poll(True)
            self.hello=next(e for e in self.events if e['event']=='READY')
            need(self.hello['pid']==self.pi.pid and self.hello['pointer_bits']==32,'same fresh x86 owner')
        except BaseException:
            self.finish(); raise

    def _read(self):
        pending=b''; total=0
        while True:
            b=C.create_string_buffer(4096); got=W.DWORD()
            if not self.readfile(self.output,b,4096,C.byref(got),None) or not got.value:
                self.q.put(None); return
            pending += b.raw[:got.value]; total += got.value
            if total > 16*1024*1024: self.q.put(ValueError('wire budget')); return
            while b'\n' in pending:
                line,pending=pending.split(b'\n',1); self.q.put(line.decode('ascii'))

    def send(self,lane,op,*args):
        self.check(); self.seq += 1
        line=' '.join(map(str,(self.seq,lane,op,*args)))+'\n'; raw=line.encode('ascii')
        wrote=W.DWORD(); self.w.check(self.writefile(self.input,raw,len(raw),C.byref(wrote),None),'owner request')
        need(wrote.value==len(raw),'whole owner request')
        self.trace.append(dict(direction='request',id=self.seq,lane=lane,op=op,args=list(args)))
        self.requests[self.seq]=(lane,op)
        return self.seq

    def check(self): need(not self.expired and time.monotonic()<self.deadline,'30 second hard deadline')

    def poll(self,block=False):
        self.check()
        try: line=self.q.get(timeout=min(.05,max(.001,self.deadline-time.monotonic())) if block else 0)
        except queue.Empty: return
        need(line is not None,'owner pipe ended before expected shutdown')
        if isinstance(line,Exception): raise line
        p=line.split(); row={}
        if p[0]=='R':
            row=dict(zip(('id','lane','tid','last_error','ok','result'),map(int,p[1:7])))
            extra=p[7:]
        else:
            need(p[0]=='E','owner message type'); row=dict(event=p[1]); extra=p[2:]
        for x in extra:
            k,v=x.split('=',1); row[k]=int(v) if v.isdecimal() and k!='hex' and not k.endswith('_hex') else v
        self.trace.append(dict(direction='response',**row))
        if p[0]=='R':
            need(row['id'] in self.requests and self.requests.pop(row['id'])[0]==row['lane'],'unique reply request/lane association')
            event=next(e for e in self.events if e['event']==('READY' if row['lane']==0 else 'WORKER_START'))
            tid,teb=(event['main_tid'],event['main_teb']) if row['lane']==0 else (event['worker_tid'],event['teb'])
            need((row['tid'],row['teb'])==(tid,teb),'fixed actual TID/TEB per lane')
            need(row['ok']==1,'native rejection: '+str(row)); self.responses[row['id']]=row
        else: self.events.append(row)

    def call(self,op,*args):
        i=self.send(0,op,*args)
        while i not in self.responses: self.poll(True)
        return self.responses.pop(i)

    def finish(self):
        if self.finished:return
        self.finished=True
        if self.timer: self.timer.cancel()
        super().finish()
        for h in self.pipes:
            if not self.w.close(h):self.receipt['errors'].append('close pipe handle')
        self.pipes=[]
        self.receipt['deadline_fired']=self.expired
        self.receipt['wall_seconds']=time.monotonic()-self.start


def descriptor(base):
    limit=0xfffff
    return struct.pack('<HHBBBB',limit&65535,base&65535,(base>>16)&255,0x93,0xcf,(base>>24)&255)


class Engine:
    def __init__(self):
        # Authenticate and construct guest memory before launching the native owner.
        self.declaration=cold.initialize(self,0)
        self.allocations={}; self.heap=0; self.locks={}; self.events=set(); self.next=0x50001000
        self.records=[]; self.roots=[]; self.ctx={}; self.pending={}; self.done={0:True,1:True}
        self.generators={}; self.lane=0; self.worker_ptd=None; self.worker_handle=None; self.worker_tid=None
        self.thread_ptd={0:0,1:0}
        self.count=0; self.ih=hashlib.sha256(); self.wh=hashlib.sha256(); self.sites={}
        for p,n in ((MANAGER,4096),(NODE,4096),(WORK_STACK,65536),(GDT,12288)):
            self.u.mem_map(p,n)
        self.u.mem_write(MANAGER,b'\xa5'*4096); self.u.mem_write(NODE,b'\xa5'*4096)
        self.u.mem_write(GDT,bytes(8)+descriptor(0)+descriptor(0)+descriptor(MAIN_TEB)+descriptor(WORK_TEB))
        self.u.reg_write(X.UC_X86_REG_GDTR,(0,GDT,39,0))
        for k in ('DS','ES','SS'): self.u.reg_write(getattr(X,'UC_X86_REG_'+k),16)
        self.u.reg_write(X.UC_X86_REG_FS,24)
        for p in (MAIN_TEB,WORK_TEB): self.u.mem_write(p,struct.pack('<I',0xffffffff))
        self.ctx[0]=self.u.context_save(); self.clean_worker=self.u.context_save()
        names=json.loads((ROOT/'analysis/hermit_real_iat.json').read_text())
        self.slots={int(k):(v.split('!')[-1],ARGC[v.split('!')[-1]]) for k,v in names.items() if v.split('!')[-1] in ARGC}
        self.slots.update({s:(n,pop//4) for s,(n,pop) in cold.IMPORTS.items() if n in ARGC})
        self.slots[0x59221c]=('CreateThread',6)
        self.slots[0x5921a4]=('ExitThread',1)  # ordinal import, original _endthreadex leaf
        self.slots[0x592264]=('Sleep',1)  # ordinal import in original completion loop
        self.targets={self.word(slot):slot for slot in self.slots}
        need(len(self.targets)==len(self.slots),'unique immutable import targets')
        for target in self.targets:
            if not any(a<=target<=b for a,b,_ in self.u.mem_regions()): self.u.mem_map(target&-4096,4096)
        self.md=MemoryDigest(self.u)
        self.u.hook_add(UC_HOOK_CODE,self.code)
        self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)
        self.declaration['thread_projection']=dict(native_entry='WorkerDispatcher',guest_entry=0x56e110,
            shared_guest_memory=True,main_FS=MAIN_TEB,worker_FS=WORK_TEB,
            native_TEB_imported=False,synthetic_declared_guest_thread_ABI=True)

    def read(self,p,n=4): return bytes(self.u.mem_read(p,n))
    def word(self,p): return struct.unpack('<I',self.read(p))[0]
    def put(self,p,b): self.u.mem_write(p,b); self.md.write(p,len(b))
    def reg(self,k,v=None):
        r=getattr(X,'UC_X86_REG_'+k)
        if v is None: return self.u.reg_read(r)
        self.u.reg_write(r,v)
    def state(self): return dict(cpu=full_cpu(self.u),memory=self.md.capture(),instructions=self.count,instruction_sha256=self.ih.hexdigest(),write_sha256=self.wh.hexdigest())
    def code(self,u,pc,n,_):
        if pc==RETURN or pc in self.targets: u.emu_stop(); return
        need(0x400000<=pc<0x592000 and self.read(pc,n)==self.image[pc-0x400000:pc-0x400000+n],'original instruction '+hex(pc))
        self.count+=1; need(self.count<=300000,'300000 instruction case budget')
        if self.count%2048==0:self.owner.check()
        raw=self.read(pc,n); self.ih.update(struct.pack('<BI',self.lane,pc)+raw)
        self.sites[pc]=[n,self.sites.get(pc,[n,0])[1]+1]
    def write(self,u,access,p,n,v,_):
        need(not (p<0x5ff000 and p+n>0x400000),'no original code, IAT or constant changes')
        self.wh.update(struct.pack('<BIII',self.lane,self.reg('EIP'),p,n)+self.read(p,n)+(v&((1<<(8*n))-1)).to_bytes(n,'little'))
        self.md.write(p,n)
    def owned(self,p,n=1):
        rows=[(g,r) for g,r in self.allocations.items() if g<=p and p+n<=g+r['bytes']]
        need(len(rows)==1,'current source allocation '+hex(p)); return rows[0]
    def native(self,p):
        if not p:return 0
        g,r=self.owned(p); return r['native']+p-g
    def guest(self,p):
        if not p:return 0
        for g,r in self.allocations.items():
            if r['native']<=p<r['native']+r['bytes']:return g+p-r['native']
        raise ValueError('unmapped native TLS pointer')
    def sync(self,p):
        g,r=self.owned(p)
        q=yield ('MEM_WRITE',r['native'],self.read(g,r['bytes']).hex())
        need(q['result']==r['bytes'],'whole PTD/raw allocation mirror')

    def api(self,slot):
        name,argc=self.slots[slot]; sp=self.reg('ESP'); ret=self.word(sp)
        a=[self.word(sp+4+4*i) for i in range(argc)]
        rec=dict(lane=self.lane,name=name,slot=slot,target=self.word(slot),args=a,sp=sp,ret=ret,before=self.state(),wire_start=len(self.owner.trace))
        self.records.append(rec); value=0
        ptd=self.thread_ptd[self.lane]
        if ptd and any(g<=ptd<g+r['bytes'] for g,r in self.allocations.items()):
            yield from self.sync(ptd)
            observed=yield('MEM_READ',self.native(ptd),116)
            need(observed['hex']==self.read(ptd,116).hex(),'current thread complete PTD mirror at leaf')
            rec['current_native_PTD']=dict(guest=ptd,native=self.native(ptd),hex=observed['hex'])
        if name=='HeapCreate':
            q=yield (name,*a); self.heap=q['result']; need(self.heap,'real heap'); value=cold.HEAP_TOKEN
        elif name=='HeapAlloc':
            need(a[0]==cold.HEAP_TOKEN,'heap projection'); q=yield(name,self.heap,*a[1:]); native=q['result']; need(native,'native allocation')
            q=yield('MEM_READ',native,a[2]); p=self.next; self.next+=0x200000
            self.u.mem_map(p,(a[2]+4095)&-4096); self.md.topology(); self.put(p,bytes.fromhex(q['hex']))
            self.allocations[p]=dict(native=native,bytes=a[2]); value=p
        elif name in ('HeapFree','HeapValidate'):
            need(a[0]==cold.HEAP_TOKEN,'heap projection'); native=0
            if a[2]:
                g,r=self.owned(a[2]); need(g==a[2],'whole raw allocation'); yield from self.sync(g); native=r['native']
            q=yield(name,self.heap,a[1],native); value=q['result']; need(value==1,'real '+name)
            if name=='HeapFree': del self.allocations[a[2]]
        elif name=='HeapDestroy':
            need(a==[cold.HEAP_TOKEN] and not self.allocations,'empty original heap'); q=yield(name,self.heap); value=q['result']; need(value==1,'heap teardown'); self.heap=0
        elif name in ('InitializeCriticalSection','DeleteCriticalSection','EnterCriticalSection','LeaveCriticalSection'):
            if name=='InitializeCriticalSection':
                need(a[0] not in self.locks,'fresh original lock'); q=yield('MEM_ALLOC',24); self.locks[a[0]]=q['result']; need(q['result'],'lock storage')
            p=self.locks[a[0]]; q=yield(name,p)
            if 'hex' in q:self.put(a[0],bytes.fromhex(q['hex']))
            if name=='DeleteCriticalSection':
                q=yield('MEM_FREE',p); need(q['result']==1,'lock storage free'); del self.locks[a[0]]
        elif name in ('IsBadReadPtr','IsBadWritePtr'):
            self.owned(a[0],a[1]); yield from self.sync(a[0]); q=yield(name,self.native(a[0]),a[1]); value=q['result']
        elif name in ('GetVersionExA','GetCurrentDirectoryA'):
            p,n=(a[0],148) if name=='GetVersionExA' else (a[1],a[0])
            q=yield('MEM_ALLOC',n); tmp=q['result']; need(tmp,'API output storage')
            yield ('MEM_WRITE',tmp,self.read(p,n).hex())
            q=yield ((name,tmp) if name=='GetVersionExA' else (name,n,tmp)); value=q['result']
            q=yield('MEM_READ',tmp,n); self.put(p,bytes.fromhex(q['hex']))
            q=yield('MEM_FREE',tmp); need(q['result']==1,'API storage free')
        elif name=='CreateThread':
            validate_thread_request(a,NODE,a[3],self.read(a[3],116)); yield from self.sync(a[3])
            self.worker_ptd=a[3]; q=yield(name,*a[:3],self.native(a[3]),*a[4:])
            need(q['result'] and q['ptd_hex']==self.read(a[3],116).hex(),'actual same-owner PTD mirror')
            value=q['result']; self.worker_handle=value; self.worker_tid=q['worker_tid']; self.put(a[5],struct.pack('<I',q['worker_tid']))
            rec['entry_projection']=dict(guest=0x56e110,native=q['native_entry'],guest_ptd=a[3],native_ptd=self.native(a[3]))
        elif name=='TlsSetValue':
            if a[1]:yield from self.sync(a[1])
            q=yield(name,a[0],self.native(a[1])); value=q['result']; need(value==1,'actual TLS install/clear')
            leaf_error=q['last_error']
            check=yield('TlsGetValue',a[0]); need(check['result']==self.native(a[1]),'same native thread TLS readback')
            rec['TLS_readback']=check
            restored=yield('SetLastError',leaf_error)
            need(restored['last_error']==leaf_error,'readback must preserve original leaf LastError')
            self.thread_ptd[self.lane]=a[1]
        elif name=='TlsGetValue':
            q=yield(name,*a); value=self.guest(q['result'])
        elif name=='GetExitCodeThread':
            q=yield(name,a[0]); value=q['result']; need(value==1,'thread exit query'); self.put(a[1],struct.pack('<I',q['exit_code']))
        else:
            q=yield(name,*a); value=q['result']
            if name=='CreateEventA': need(value,'fresh event'); self.events.add(value)
            elif name=='CloseHandle': need(value==1,'handle close'); self.events.discard(a[0])
            elif name in ('SetEvent','ResetEvent','TlsFree'): need(value==1,'real '+name)
            elif name=='TlsAlloc': need(value!=0xffffffff,'actual TLS slot')
            elif name=='ResumeThread': need(value==1,'actual worker resume once')
            elif name=='WaitForSingleObject': need(value==0,'successful actual wait')
            elif name=='ExitThread':
                need(self.lane==1 and a==[0] and q['exit_requested']==1,'original worker exits0')
                rec['native_exit_request']=q; rec['after']=self.state(); self.done[1]=True; return
        self.reg('EAX',value); self.reg('ESP',sp+4+argc*4); self.reg('EIP',ret)
        rec.update(value=value,after=self.state(),wire_end=len(self.owner.trace))

    def start_worker(self):
        starts=[e for e in self.owner.events if e['event']=='WORKER_START']
        if not starts or 1 in self.ctx:return
        need(len(starts)==1 and starts[0]['worker_tid']==self.worker_tid and starts[0]['guest_entry']==0x56e110 and starts[0]['guest_param']==self.native(self.worker_ptd),'actual worker entrance projection')
        self.u.context_restore(self.clean_worker); self.reg('FS',32)
        sp=WORK_STACK+0xf000; self.put(sp,struct.pack('<II',RETURN,self.worker_ptd))
        for k,v in dict(EIP=0x56e110,ESP=sp,EFLAGS=0x202).items():self.reg(k,v)
        self.ctx[1]=self.u.context_save(); self.done[1]=False
        self.roots.append(dict(label='native-created-worker-entry',entry=0x56e110,args=[self.worker_ptd],lane=1,before=self.state()))

    def drive(self):
        while not all(self.done.values()) or self.pending:
            self.owner.poll(False); self.start_worker(); progress=False
            for lane in (0,1):
                if lane not in self.ctx or self.done[lane]:continue
                self.lane=lane; self.u.context_restore(self.ctx[lane])
                if lane in self.pending:
                    i=self.pending[lane]
                    if i not in self.owner.responses:continue
                    q=self.owner.responses.pop(i); del self.pending[lane]
                    gen=self.generators[lane]
                    try: req=gen.send(q)
                    except StopIteration: del self.generators[lane]
                    else:self.pending[lane]=self.owner.send(lane,*req)
                else:
                    self.u.emu_start(self.reg('EIP'),0,count=300000,timeout=500000)
                    pc=self.reg('EIP')
                    if pc==RETURN:
                        need(lane==0,'worker cannot fake return past ExitThread'); self.done[lane]=True
                    else:
                        need(pc in self.targets,'unreached leaf or time slice exhausted '+hex(pc))
                        gen=self.api(self.targets[pc]); self.generators[lane]=gen
                        self.pending[lane]=self.owner.send(lane,*next(gen))
                self.ctx[lane]=self.u.context_save(); progress=True
            if not progress:self.owner.poll(True)
        self.lane=0; self.u.context_restore(self.ctx[0])

    def root(self,label,pc,args=(),receiver=0,callee=False):
        need(self.done[0] and not self.pending,'quiescent new root')
        self.u.context_restore(self.ctx[0]); sp=cold.old.STACK+0xf000
        self.put(sp,struct.pack('<'+'I'*(len(args)+1),RETURN,*args))
        for k,v in dict(EIP=pc,ESP=sp,ECX=receiver,EFLAGS=0x202).items():self.reg(k,v)
        row=dict(label=label,lane=0,entry=pc,args=list(args),receiver=receiver,callee=callee,before=self.state()); self.roots.append(row)
        self.ctx[0]=self.u.context_save(); self.done[0]=False; self.drive()
        need(self.reg('ESP')==sp+4+(4*len(args) if callee else 0),'natural original root ABI')
        row['after']=self.state(); return self.reg('EAX')


def execute(g,owner):
    g.owner=owner
    g.root('original_heap_init',0x57b9d0,(1,))
    need(g.root('original_TLS_and_lock_init',0x5752d0)==1,'original main TLS initialized')
    g.root('original_manager_constructor',0x421540,receiver=MANAGER,callee=True)
    g.root('original_empty_manager_buckets',0x421660,receiver=MANAGER,callee=True)
    g.root('original_base_node_constructor',0x422290,receiver=NODE,callee=True)
    need(g.word(NODE)==0x594a54 and g.word(g.word(NODE))==0x422330,'original base constructor publishes original callback')
    g.root('original_register_base_node',0x4216c0,(NODE,0,0),MANAGER,True)
    g.root('original_scan_and_complete_worker',0x4217c0,receiver=MANAGER,callee=True)
    need(g.done[1] and 0x421f88 in g.sites and 0x422330 in g.sites and 0x422021 in g.sites,'original wrapper callback and _endthreadex reached')
    q=owner.call('WaitForSingleObject',g.worker_handle,1000); need(q['result']==0,'actual worker termination')
    q=owner.call('GetExitCodeThread',g.worker_handle); need(q['result']==1 and q['exit_code']==0,'actual worker exit0')
    need(owner.call('CloseHandle',g.worker_handle)['result']==1,'supplemental worker handle close')
    g.root('original_base_node_destructor',0x4222d0,receiver=NODE,callee=True)
    g.root('original_manager_destructor',0x4215f0,receiver=MANAGER,callee=True)
    g.root('original_main_PTD_free_and_TLS_clear',0x575450,(0,))
    g.root('original_TLS_and_lock_teardown',0x575360)
    g.root('original_heap_teardown',0x57ba60)
    need(not g.heap and not g.allocations and not g.events and not g.locks,'original resources emptied')
    status=owner.call('STATUS'); need(owner.call('Shutdown')['result']==1,'normal owner shutdown')
    need(owner.wait(min(1000,max(0,int((owner.deadline-time.monotonic())*1000))))==0,'whole native process normal return')
    return status


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--prepare',action='store_true'); ap.add_argument('--execute',action='store_true')
    ap.add_argument('--out',required=True); ap.add_argument('--helper',required=True)
    a=ap.parse_args(); need(a.prepare != a.execute,'choose prepare or one execute')
    out=(ROOT/a.out).resolve(); helper=(ROOT/a.helper).resolve()
    need(out.is_relative_to(ROOT) and helper.is_relative_to(ROOT),'F workspace only')
    need(not out.exists(),'fresh immutable report'); folder=helper.parent; need(folder.exists(),'existing F evidence directory')
    gate=build_gate(helper)
    g=Engine()
    report=dict(schema_version=1,kind='same_owner_original_base_worker_preflight',accepted=False,
        formal_acceptance=False,scene_first_yield=False,first_result_consumption=False,complete_battle_exit=False,
        independent_full_replay=False,guest_native_pointer_projection=True,physical_native_context_import=False,
        helper=identity(helper),implementation=identity(Path(__file__)),original=identity(cold.base.SOURCE),
        declaration=g.declaration,initial=g.state(),build_gate=gate,implementation_pins=implementation_pins(),native_executed=False,desktop_used=False,
        screenshot=False,budget_seconds=30,roots=g.roots,API_calls=g.records)
    if a.prepare:
        report['offline_preparation_only']=True
    else:
        # This marker survives all failures. A retry requires a separate explicit decision.
        marker=folder/'native-attempt.once'
        with marker.open('x',encoding='ascii') as f:f.write(json.dumps(dict(helper=identity(helper),utc=time.time())))
        owner=None
        try:
            owner=Owner.__new__(Owner)
            Owner.__init__(owner,helper,folder); report['native_executed']=True
            report['status']=execute(g,owner); report['accepted']=True
        except BaseException as e:
            report['failure']=repr(e); report['failure_guest']=dict(lane=g.lane,state=g.state(),pending=g.pending)
        finally:
            if owner:
                owner.finish(); report.update(native_trace=owner.trace,events=owner.events,cleanup=owner.receipt)
                report['native_executed']=owner.resumed
                report['native_process_created']=owner.started
                exited=owner.receipt['exits'].get(str(owner.receipt['parent_pid']),{})
                if owner.receipt['forced'] or owner.receipt['deadline_fired'] or not owner.receipt['job_empty'] or owner.receipt['errors'] or not owner.receipt['handles_closed'] or exited.get('wait')!=0 or exited.get('code')!=0:
                    report['accepted']=False
            report['instruction_sites']=[dict(pc=p,hex=g.image[p-0x400000:p-0x400000+n].hex(),count=c) for p,(n,c) in sorted(g.sites.items())]
            report['final']=g.state()
    raw=json.dumps(report,separators=(',',':')).encode(); data=gzip.compress(raw,mtime=0)
    need(len(data)<=16*1024*1024,'16MiB evidence limit'); out.write_bytes(data)
    print(json.dumps(dict(out=str(out),bytes=len(data),native_executed=report['native_executed'],accepted=report['accepted'],failure=report.get('failure'))))
    return 0 if a.prepare or report['accepted'] else 1


if __name__=='__main__': raise SystemExit(main())
