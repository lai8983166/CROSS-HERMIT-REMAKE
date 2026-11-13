"""Persistent recovery observer with an external, no-window Job supervisor.

The supervisor only uses kernel/process/file APIs. Desktop admission stays closed
until the native owner/receipt/display contract is qualified. Model faults execute
the same recover() orchestration in a separate real Windows process.
"""
from __future__ import annotations
import argparse
import ctypes as C
import ctypes.wintypes as W
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import time

from devtools.terminal_oplock import Win,need
from devtools.terminal_oplock_probe_v2 import Owned,SI,PI
from devtools import terminal_graphics_desktop as recovery

ROOT=Path(__file__).resolve().parents[1]
MAX_BYTES=262144
MAX_COMMANDS=8
MODES={'normal','block_baseline','block_recovery_read','block_gamma_write','exit_during_write'}

def implementation_pins():
    names=('devtools/terminal_graphics_recovery.py','devtools/terminal_graphics_recovery_observer.py','devtools/terminal_graphics_recovery_observer_v2.py','devtools/terminal_graphics_desktop.py','devtools/terminal_window_desktop.py','devtools/terminal_host_desktop.py','tools/school_native_dialogue_desktop.py','devtools/terminal_oplock.py','devtools/terminal_oplock_probe_v2.py','devtools/tests/test_terminal_graphics_desktop.py','devtools/tests/test_terminal_window_desktop.py')
    return [dict(path=n,bytes=(ROOT/n).stat().st_size,sha256=hashlib.sha256((ROOT/n).read_bytes()).hexdigest())for n in names]

def verify_implementations(cfg):
    need(cfg['implementation_pins']==implementation_pins(),'all declared observer/supervisor implementation bytes unchanged')

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def read(path):
    need(path.stat().st_size<=MAX_BYTES,'bounded recovery message')
    return json.loads(path.read_text(encoding='utf8'))

def publish(path,value):
    raw=(json.dumps(value,separators=(',',':'))+'\n').encode();need(len(raw)<=MAX_BYTES,'bounded recovery output')
    need(not path.exists(),'fresh immutable recovery record')
    temporary=path.with_suffix(path.suffix+'.pending')
    with temporary.open('xb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
    temporary.replace(path)

def folder_path(path):
    p=Path(path).resolve();need(p.is_relative_to(ROOT/'.venv-audit') and p.drive.lower()=='f:','F-owned recovery directory');return p

def created(w,handle):
    fn=w.k.GetProcessTimes;fn.argtypes=[W.HANDLE]+[C.POINTER(W.FILETIME)]*4;fn.restype=W.BOOL
    times=[W.FILETIME()for _ in range(4)];w.check(fn(handle,*[C.byref(x)for x in times]),'process lifetime')
    return times[0].dwLowDateTime|(times[0].dwHighDateTime<<32)

class WorkerJob(Owned):
    """Reuse frozen query/containment, with suspended fixed worker command."""
    def __init__(self,folder):
        self.w=Win();k=self.w.k
        def bind(n,r,a):
            f=getattr(k,n);f.restype=r;f.argtypes=a;return f
        self.jobnew=bind('CreateJobObjectW',W.HANDLE,[C.c_void_p,W.LPCWSTR])
        self.setjob=bind('SetInformationJobObject',W.BOOL,[W.HANDLE,C.c_int,C.c_void_p,W.DWORD])
        self.assign=bind('AssignProcessToJobObject',W.BOOL,[W.HANDLE,W.HANDLE])
        self.queryjob=bind('QueryInformationJobObject',W.BOOL,[W.HANDLE,C.c_int,C.c_void_p,W.DWORD,C.c_void_p])
        self.terminate=bind('TerminateJobObject',W.BOOL,[W.HANDLE,W.UINT])
        self.create=bind('CreateProcessW',W.BOOL,[W.LPCWSTR,W.LPWSTR,C.c_void_p,C.c_void_p,W.BOOL,W.DWORD,C.c_void_p,W.LPCWSTR,C.POINTER(SI),C.POINTER(PI)])
        self.job=None;self.pi=PI();self.started=False;self.assigned=False
        self.receipt=dict(parent_pid=None,forced=False,exits={},handles_closed=False,job_empty=False)
        try:
            need(C.sizeof(C.c_void_p)==8,'fixed 64-bit Job structure contract')
            self.job=self.jobnew(None,None);self.w.check(self.job,'recovery Job')
            limit=C.create_string_buffer(144);C.c_uint32.from_buffer(limit,16).value=0x2000
            self.w.check(self.setjob(self.job,9,limit,144),'kill-on-close recovery Job')
            args=[str(ROOT/'.venv-audit/Scripts/python.exe'),'-B','-X','utf8','-m','devtools.terminal_graphics_recovery','--worker',str(folder)]
            cmd=C.create_unicode_buffer(subprocess.list2cmdline(args));si=SI();si.cb=C.sizeof(si);si.flags=1;si.show=0
            env=dict(os.environ,TEMP=str(folder),TMP=str(folder));block=C.create_unicode_buffer('\0'.join(k+'='+v for k,v in sorted(env.items()))+'\0\0')
            self.w.check(self.create(args[0],cmd,None,None,False,0x08000404,block,str(ROOT),C.byref(si),C.byref(self.pi)),'suspended hidden recovery worker')
            self.started=True;self.receipt['parent_pid']=self.pi.pid
            self.w.check(self.assign(self.job,self.pi.process),'assign recovery before first instruction');self.assigned=True
            self.launch_created=created(self.w,self.pi.process)
            need(self.w.resume(self.pi.thread)==1,'one recovery resume')
        except BaseException:self.finish();raise

def supervisor(folder):
    folder=folder_path(folder);cfg=read(folder/'config.json');token=cfg['token'];w=Win();parent=None;job=None;job_ready=False;start=time.monotonic_ns()
    result=dict(kind='external_recovery_supervisor',supervisor_pid=os.getpid(),controller_pid=cfg['controller_pid'],started_ns=start,reason=None,commands=[],backend=cfg['backend'],native_desktop_calls=0 if cfg['backend']=='model' else None,native_observation_commands_completed=0,desktop_writes=0,desktop_restored=False)
    try:
        need(cfg['backend'] in ('model','native-readonly') and cfg['scenario'] in MODES,'native write recovery admission remains closed')
        need(cfg['backend']=='model' or cfg['scenario']=='normal','real observation has no model fault injection')
        need(1<=cfg['lifetime_seconds']<=120,'fixed total session bound')
        parent=w.openp(0x101000,False,cfg['controller_pid']);w.check(parent,'retain exact controller')
        need(created(w,parent)==cfg['controller_created'] and w.wait(parent,0)==258,'same live controller lifetime')
        need(hashlib.sha256(Path(__file__).read_bytes()).hexdigest()==cfg['implementation_sha256'],'frozen recovery implementation')
        verify_implementations(cfg)
        job=WorkerJob.__new__(WorkerJob);WorkerJob.__init__(job,folder);job_ready=True
        deadline=start+int(cfg['lifetime_seconds']*1e9);active=None;seq=0
        def complete(command):
            r=read(folder/f'response-{command["seq"]}.json')
            need(r['token']==token and r['seq']==command['seq'] and r['request_sha256']==command['request_sha256'],'current response identity')
            need(r['completed_ns']<=command['deadline_ns'],'response completed within externally armed deadline')
            command.update(completed_ns=r['completed_ns'],response_sha256=digest(r),ok=r['ok'])
            result['native_observation_commands_completed']+=int(cfg['backend']=='native-readonly' and command['op'] in ('baseline','readback') and r['ok'])
            if command['op']=='close':result['close_acknowledged']=r['ok'] is True and r.get('value')==dict(closed=True)
        while True:
            now=time.monotonic_ns()
            if w.wait(parent,0)==0:result['reason']='controller_exited';break
            if (folder/'cancel.json').exists():
                need(read(folder/'cancel.json')['token']==token,'same controller cancellation');result['reason']='controller_cancelled';break
            if now>=deadline:result['reason']='session_deadline';break
            if active:
                response=folder/f'response-{seq}.json'
                if response.exists():
                    complete(active);active=None
                elif now>=active['deadline_ns']:result['reason']='command_deadline';break
            else:
                path=folder/f'request-{seq+1}.json'
                if path.exists():
                    q=read(path);need(q['token']==token and q['seq']==seq+1<=MAX_COMMANDS,'strict command identity/order')
                    need(q['op'] in (('baseline','recover','close') if cfg['backend']=='model' else ('baseline','readback','close')),'fixed recovery operations; no native write command')
                    maximum=20000 if q['op']=='recover' else 5000
                    need(100<=q['timeout_ms']<=maximum and 0<=now-q['created_ns']<=2_000_000_000,'fresh bounded command')
                    seq+=1;active=dict(seq=seq,op=q['op'],request_sha256=digest(q),armed_ns=now,deadline_ns=min(deadline,q['created_ns']+q['timeout_ms']*1000000))
                    need(active['deadline_ns']>now,'command already expired before arm');result['commands'].append(active)
                    publish(folder/f'armed-{seq}.json',dict(token=token,**active))
            if job.wait(0)==0:
                if active and (folder/f'response-{seq}.json').exists():complete(active);active=None
                code=W.DWORD();w.check(w.exit_process(job.pi.process,C.byref(code)),'signalled root exit code')
                if result.get('close_acknowledged') and code.value==0:
                    # The launcher can be signalled while a signalled child is
                    # still listed by Job accounting. Wait only within the
                    # already armed close/session budget; do not relabel kills.
                    began=time.monotonic_ns();until=min(deadline,result['commands'][-1]['deadline_ns'],began+250_000_000)
                    first=None;members=None;queries=0;accepted=False;abort=None
                    while True:
                        if w.wait(parent,0)==0:abort='controller_exited';break
                        if (folder/'cancel.json').exists():abort='controller_cancelled';break
                        if time.monotonic_ns()>=until:abort='drain_deadline';break
                        members=job.ids();queries+=1
                        if first is None:first=members
                        if time.monotonic_ns()>=until:abort='drain_deadline';break
                        if not members:accepted=True;break
                        time.sleep(min(.005,max(0,(until-time.monotonic_ns())/1e9)))
                    result['natural_job_drain']=dict(initial_members=first,final_members=members,queries=queries,accepted=accepted,abort=abort,elapsed_ns=time.monotonic_ns()-began,maximum_ns=250_000_000,deadline_ns=until)
                result['reason']='worker_exited';break
            time.sleep(.005)
    except BaseException as exc:result.update(reason='supervisor_failure',failure=repr(exc))
    finally:
        if job and hasattr(job,'receipt'):
            result['cleanup']=job.finish() if job_ready else job.receipt
            result['launch_pid']=job.receipt['parent_pid'];result['assigned_before_resume']=job.assigned
        if parent:result['controller_handle_closed']=bool(w.close(parent))
        result['finished_ns']=time.monotonic_ns();result['elapsed_seconds']=(result['finished_ns']-start)/1e9
        c=result.get('cleanup',{});root_exit=c.get('exits',{}).get(str(result.get('launch_pid')),{})
        result['normal_close']=bool(result.get('reason')=='worker_exited' and result.get('close_acknowledged') and result.get('natural_job_drain',{}).get('accepted') and root_exit==dict(wait=0,code=0) and c.get('job_empty') and c.get('handles_closed') and not c.get('forced') and not c.get('errors') and result.get('controller_handle_closed'))
        publish(folder/'supervisor-result.json',result)
    return 0 if result['normal_close'] else 1

def worker(folder):
    from devtools.tests.test_terminal_graphics_desktop import ModelBackend,OWNER,DEVICE,receipt
    folder=folder_path(folder);cfg=read(folder/'config.json');need(cfg['backend'] in ('model','native-readonly'),'no native write desktop backend admitted');verify_implementations(cfg)
    journal=folder/'operations.jsonl';scenario=cfg['scenario'];stage='baseline';operation=0
    def block():
        # Real unbounded kernel wait in this owned worker, not a simulated timer.
        fn=C.WinDLL('kernel32').Sleep;fn.argtypes=[W.DWORD];fn.restype=None;fn(0xffffffff)
    class ObservedModel(ModelBackend):
        def note(self,phase,kind):
            nonlocal operation
            operation+=1;need(operation<=128,'bounded recovery operation journal')
            row=dict(seq=operation,phase=phase,operation=kind,pid=os.getpid(),at_ns=time.monotonic_ns())
            with journal.open('ab')as f:f.write((json.dumps(row)+'\n').encode());f.flush();os.fsync(f.fileno())
        def read(self,*a,**kw):
            self.note('begin','read')
            if scenario=='block_baseline' or (scenario=='block_recovery_read' and stage=='recover'):block()
            v=super().read(*a,**kw);self.note('end','read');return v
        def write(self,kind,*a,**kw):
            self.note('begin','write:'+kind)
            if kind=='gamma' and scenario=='block_gamma_write':block()
            if kind=='gamma' and scenario=='exit_during_write':os._exit(37)
            v=super().write(kind,*a,**kw);self.note('end','write:'+kind);return v
    if cfg['backend']=='native-readonly':
        from devtools.terminal_graphics_recovery_observer_v2 import GuardedReadOnlyWindowsBackend
        backend=GuardedReadOnlyWindowsBackend()
    else:backend=ObservedModel()
    baseline=None;seq=0
    while seq<MAX_COMMANDS:
        arm=folder/f'armed-{seq+1}.json'
        if not arm.exists():time.sleep(.005);continue
        q=read(folder/f'request-{seq+1}.json');a=read(arm);seq+=1
        need(a['token']==q['token']==cfg['token'] and a['seq']==q['seq']==seq and a['request_sha256']==digest(q),'supervisor arm bound to exact request')
        need(time.monotonic_ns()<a['deadline_ns'],'worker starts only before armed deadline')
        response=dict(seq=seq,token=cfg['token'],request_sha256=digest(q),worker_pid=os.getpid(),backend=cfg['backend'],native_desktop_calls=0,desktop_writes=0)
        try:
            if cfg['backend']=='native-readonly' and q['op'] in ('baseline','readback'):
                # Read errors remain actual failures; no model fallback exists.
                response['native_desktop_calls']=None
                ObservedModel.note(backend,'begin','native-read:'+q['op'])
                if q['op']=='baseline':
                    need(baseline is None,'one persistent native observation baseline');baseline=backend.first();value=baseline
                else:
                    need(baseline is not None,'same observer baseline required');value=backend.read(backend.device,foreground_identity=baseline['foreground_identity'])
                response['value']=dict(state=value,read_only=True,D3D_adapter_mapping_proven=False)
                ObservedModel.note(backend,'end','native-read:'+q['op'])
            elif q['op']=='baseline':
                need(baseline is None,'one observer baseline');baseline=recovery.capture_baseline(backend,DEVICE,OWNER);response['value']=baseline
            elif q['op']=='recover':
                need(cfg['backend']=='model','native observer forbids restore')
                need(baseline is not None,'persistent baseline precedes restoration');stage='recover'
                backend.state['monitors'][0]['mode']['width']=800
                response['value']=recovery.recover(baseline,receipt(baseline,backend),backend,budget=recovery.Budget(min(20,q['timeout_ms']/1000)))
            else:response['value']=dict(closed=True)
            response['ok']=True
        except BaseException as exc:response.update(ok=False,failure=repr(exc))
        response['completed_ns']=time.monotonic_ns();publish(folder/f'response-{seq}.json',response)
        if q['op']=='close':return 0
    return 38

class RecoverySession:
    """Controller never calls desktop APIs; one worker retains observer identity."""
    def __init__(self,folder,*,scenario='normal',lifetime_seconds=30,backend='model'):
        self.folder=folder_path(folder);need(not self.folder.exists(),'fresh recovery session');need(backend in ('model','native-readonly'),'native recovery admission is still closed');need(scenario in MODES and (backend=='model' or scenario=='normal'),'bounded declared scenario')
        self.folder.mkdir();self.token=secrets.token_hex(32);self.seq=0;self.finished=False;self.pending=None;w=Win();parent=w.openp(0x101000,False,os.getpid());w.check(parent,'current controller identity')
        try:creation=created(w,parent)
        finally:w.close(parent)
        publish(self.folder/'config.json',dict(token=self.token,backend=backend,scenario=scenario,lifetime_seconds=lifetime_seconds,controller_pid=os.getpid(),controller_created=creation,implementation_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),implementation_pins=implementation_pins()))
        args=[sys.executable,'-B','-X','utf8','-m','devtools.terminal_graphics_recovery','--supervisor',str(self.folder)]
        self.log=(self.folder/'supervisor.log').open('xb')
        self.process=subprocess.Popen(args,cwd=ROOT,env=dict(os.environ,TEMP=str(self.folder),TMP=str(self.folder)),stdin=subprocess.DEVNULL,stdout=self.log,stderr=self.log,creationflags=subprocess.CREATE_NO_WINDOW)
    def request(self,op,timeout_ms=5000):
        need(not self.finished and self.process.poll() is None and self.pending is None,'live serial external supervisor');self.seq+=1
        q=dict(seq=self.seq,token=self.token,op=op,timeout_ms=timeout_ms,created_ns=time.monotonic_ns());publish(self.folder/f'request-{self.seq}.json',q);self.pending=q;return q
    def collect(self,q):
        # A controller timeout is secondary. The independent supervisor owns the Job.
        deadline=time.monotonic()+q['timeout_ms']/1000+5
        while time.monotonic()<deadline:
            path=self.folder/f'response-{q["seq"]}.json'
            if path.exists():
                r=read(path);need(r['seq']==q['seq'] and r['token']==self.token and r['request_sha256']==digest(q),'controller response identity')
                arm=read(self.folder/f'armed-{q["seq"]}.json');need(r['completed_ns']<=arm['deadline_ns'],'late response rejected');self.pending=None;return r
            if (self.folder/'supervisor-result.json').exists() or self.process.poll() is not None:raise TimeoutError('recovery process stopped; restoration not confirmed')
            time.sleep(.005)
        raise TimeoutError('supervisor did not report within bounded containment reserve')
    def call(self,op,timeout_ms=5000):return self.collect(self.request(op,timeout_ms))
    def finish(self):
        if self.finished:return read(self.folder/'supervisor-result.json')
        try:
            if self.process.poll() is None and not (self.folder/'supervisor-result.json').exists():
                if self.pending:publish(self.folder/'cancel.json',dict(token=self.token))
                else:
                    try:self.call('close',1000)
                    except (TimeoutError,ValueError):pass
            try:self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill();self.process.wait(timeout=3)
                raise RuntimeError('supervisor failed to finish; kill-on-close containment is not restoration proof')
            return read(self.folder/'supervisor-result.json')
        finally:self.log.close();self.finished=True

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True);g.add_argument('--supervisor');g.add_argument('--worker');a=p.parse_args()
    raise SystemExit(supervisor(a.supervisor) if a.supervisor else worker(a.worker))
