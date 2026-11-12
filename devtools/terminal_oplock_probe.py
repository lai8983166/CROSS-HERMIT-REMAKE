"""Bounded native RW-oplock qualification in owned no-window x86 processes.

The C# parent alone owns/continues its child debugger. This observer only holds a
read oplock and reads the blocked worker. No game/attachment/input entry exists.
"""
import argparse
import ctypes as C
import ctypes.wintypes as W
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import time

from devtools.terminal_oplock import ReadOplock, Win, need, PENDING_OWNERS

ROOT=Path(__file__).resolve().parents[1]
DEPS=('devtools/terminal_oplock.py','devtools/terminal_oplock_probe.py','devtools/terminal_oplock_fixture.cs',
      'devtools/terminal_host_desktop.py','tools/school_native_dialogue_desktop.py')
PAYLOAD=bytes((i*17+3)&255 for i in range(64))


def identity(path):
    p=Path(path);raw=p.read_bytes()
    return dict(path=str(p),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def load(path):
    p=Path(path);need(p.stat().st_size<256*1024,'bounded helper report')
    return json.loads(p.read_text(encoding='utf-8-sig'))


class SI(C.Structure):
    _fields_=[('cb',W.DWORD),('reserved',W.LPWSTR),('desktop',W.LPWSTR),('title',W.LPWSTR),
        ('x',W.DWORD),('y',W.DWORD),('w',W.DWORD),('h',W.DWORD),('xc',W.DWORD),('yc',W.DWORD),
        ('fill',W.DWORD),('flags',W.DWORD),('show',W.WORD),('cb2',W.WORD),('reserved2',C.c_void_p),
        ('input',W.HANDLE),('output',W.HANDLE),('error',W.HANDLE)]


class PI(C.Structure):
    _fields_=[('process',W.HANDLE),('thread',W.HANDLE),('pid',W.DWORD),('tid',W.DWORD)]


class Owned:
    def __init__(self,exe,folder):
        self.w=Win();k=self.w.k
        def bind(name,result,args):
            f=getattr(k,name);f.restype=result;f.argtypes=args;return f
        self.jobnew=bind('CreateJobObjectW',W.HANDLE,[C.c_void_p,W.LPCWSTR])
        self.setjob=bind('SetInformationJobObject',W.BOOL,[W.HANDLE,C.c_int,C.c_void_p,W.DWORD])
        self.assign=bind('AssignProcessToJobObject',W.BOOL,[W.HANDLE,W.HANDLE])
        self.queryjob=bind('QueryInformationJobObject',W.BOOL,[W.HANDLE,C.c_int,C.c_void_p,W.DWORD,C.c_void_p])
        self.terminate=bind('TerminateJobObject',W.BOOL,[W.HANDLE,W.UINT])
        self.create=bind('CreateProcessW',W.BOOL,[W.LPCWSTR,W.LPWSTR,C.c_void_p,C.c_void_p,W.BOOL,W.DWORD,C.c_void_p,W.LPCWSTR,C.POINTER(SI),C.POINTER(PI)])
        self.job=None;self.pi=PI();self.started=False;self.assigned=False
        self.receipt=dict(parent_pid=None,forced=False,exits={},handles_closed=False,job_empty=False)
        try:
            self.job=self.jobnew(None,None);self.w.check(self.job,'fixture Job')
            limit=C.create_string_buffer(144);struct.pack_into('<I',limit,16,0x2000)
            self.w.check(self.setjob(self.job,9,limit,144),'kill-on-close fixture Job')
            si=SI();si.cb=C.sizeof(si);si.flags=1;si.show=0
            cmd=C.create_unicode_buffer('"'+str(exe)+'" parent "'+str(folder)+'"')
            # No shell and no visible window; inherit F-drive temp environment.
            env=dict(os.environ,TEMP=str(folder),TMP=str(folder))
            envblock=C.create_unicode_buffer('\0'.join(k+'='+v for k,v in sorted(env.items()))+'\0\0')
            self.w.check(self.create(str(exe),cmd,None,None,False,0x08000404,envblock,str(folder),C.byref(si),C.byref(self.pi)),'owned no-window parent')
            self.started=True;self.receipt['parent_pid']=self.pi.pid
            self.w.check(self.assign(self.job,self.pi.process),'assign before resume');self.assigned=True
            need(self.w.resume(self.pi.thread)==1,'resume suspended owned parent once')
        except BaseException:
            self.finish();raise

    def ids(self):
        b=C.create_string_buffer(8+8*16);self.w.check(self.queryjob(self.job,3,b,len(b),None),'fixture Job members')
        assigned,count=struct.unpack_from('<2I',b.raw)
        need(count<=16 and assigned<=16,'bounded own Job members')
        return list(struct.unpack_from('<'+'Q'*count,b.raw,8))

    def wait(self,ms):
        return self.w.wait(self.pi.process,ms)

    def finish(self):
        errors=[];members=None;retained=[]
        try:
            try:members=self.ids() if self.job else []
            except BaseException as exc:errors.append('member query: '+repr(exc))
            for pid in members or []:
                h=self.w.openp(0x101000,False,pid)
                if h:retained.append((pid,h))
                else:errors.append('retain member '+str(pid))
            if members or members is None or (self.started and self.w.wait(self.pi.process,0)!=0):
                self.receipt['forced']=True
                if self.job:
                    try:self.w.check(self.terminate(self.job,94),'contain fixture Job')
                    except BaseException as exc:errors.append(repr(exc))
                if self.started and not self.assigned:
                    fn=self.w.k.TerminateProcess;fn.argtypes=[W.HANDLE,W.UINT];fn.restype=W.BOOL
                    try:self.w.check(fn(self.pi.process,94),'contain unassigned suspended parent')
                    except BaseException as exc:errors.append(repr(exc))
                deadline=time.perf_counter()+3
                for pid,h in retained:
                    status=self.w.wait(h,max(0,int((deadline-time.perf_counter())*1000)))
                    self.receipt['exits'][str(pid)]=dict(wait=status)
                    if status!=0:errors.append('member did not exit '+str(pid))
                if self.started:self.w.wait(self.pi.process,max(0,int((deadline-time.perf_counter())*1000)))
            if self.started:
                code=W.DWORD();self.w.check(self.w.exit_process(self.pi.process,C.byref(code)),'parent exit query')
                self.receipt['exits'][str(self.pi.pid)]=dict(wait=self.w.wait(self.pi.process,0),code=code.value)
            if self.job:self.receipt['job_empty']=not self.ids()
        except BaseException as exc:errors.append(repr(exc))
        finally:
            for pid,h in retained:
                if not self.w.close(h):errors.append('close retained member '+str(pid))
            for field in ('thread','process'):
                h=getattr(self.pi,field)
                if h:
                    if not self.w.close(h):errors.append('CloseHandle '+field)
                    else:setattr(self.pi,field,None)
            if self.job:
                if not self.w.close(self.job):errors.append('CloseHandle job')
                else:self.job=None
            self.receipt['handles_closed']=not (self.pi.thread or self.pi.process or self.job)
            self.receipt['errors']=errors
        return dict(self.receipt)


def process_info(w,h):
    port=C.c_size_t();basic=C.create_string_buffer(48)
    need(w.query(h,7,C.byref(port),C.sizeof(port),None)==0,'read existing debug port')
    need(w.query(h,0,basic,48,None)==0,'read current parent relationship')
    return dict(debug_port=port.value,pid=struct.unpack_from('<Q',basic.raw,32)[0],
                parent_pid=struct.unpack_from('<Q',basic.raw,40)[0],basic_hex=basic.raw.hex())


def capture(w,ph,th,meta):
    tid=meta['tid'];pid=meta['pid'];index=meta['index']
    need(w.thread_pid(th)==pid and w.thread_id(th)==tid and w.wait(th,0)==258,'current live worker identity')
    start=time.perf_counter_ns();previous=w.suspend(th)
    need(previous!=0xffffffff,'suspend actual blocked worker')
    out=dict(suspend_previous=previous)
    try:
        def context():
            b=C.create_string_buffer(716);struct.pack_into('<I',b,0,0x1003f)
            w.check(w.context(th,b),'full WOW64 context');return b.raw
        before=context();fs=struct.unpack_from('<I',before,144)[0]
        desc=C.create_string_buffer(8);w.check(w.selector(th,fs,desc),'actual FS descriptor')
        d=desc.raw;teb=struct.unpack_from('<H',d,2)[0]|d[4]<<16|d[7]<<24
        head=w.memory(ph,teb,48)
        need(struct.unpack_from('<I',head,24)[0]==teb and struct.unpack_from('<2I',head,32)==(pid,tid),'actual TEB owner')
        need(0<=index<64,'fixture fixed TLS slot')
        slot=teb+0xe10+4*index;slotraw=w.memory(ph,slot,4);pointer=struct.unpack('<I',slotraw)[0]
        need(pointer==meta['pointer'] and pointer,'actual initialized TLS pointer')
        payload=w.memory(ph,pointer,116)
        need(struct.unpack_from('<6I',payload)==(0x544c5350,pid,tid,index,0x1234abcd,pointer),'actual TLS body owner')
        esp=struct.unpack_from('<I',before,196)[0]
        stackbase,stacklimit=struct.unpack_from('<2I',head,4)
        need(stacklimit<=esp<stackbase,'actual TEB stack bounds')
        stack=w.memory(ph,esp,min(4096,stackbase-esp))
        eip=struct.unpack_from('<I',before,184)[0];code=w.memory(ph,eip,32)
        nt_create=meta['nt_create_file'];nt_code=w.memory(ph,nt_create,32)
        # Capture potential original syscall argument frames without changing
        # registers/stack. Offline review must bind one to this exact file.
        frames=[]
        for offset in range(0,len(stack)-52,4):
            ret=struct.unpack_from('<I',stack,offset)[0]
            if nt_create<ret<nt_create+32:
                # CALL transition adds its own return above NtCreateFile's
                # caller return. Keep both layouts as raw candidates; neither
                # is accepted without original instruction/argument review.
                for skip in (4,8):
                    frame=dict(offset=offset,argument_skip=skip,return_address=ret)
                    try:
                        args=struct.unpack_from('<11I',stack,offset+skip);frame['args']=list(args)
                        oa=w.memory(ph,args[2],24);nameptr=struct.unpack_from('<I',oa,8)[0]
                        us=w.memory(ph,nameptr,8);length,maximum,ptr=struct.unpack('<HHI',us)
                        need(0<length<=maximum<=2048 and length%2==0,'bounded original file name')
                        frame.update(object_attributes_hex=oa.hex(),unicode_string_hex=us.hex(),name_hex=w.memory(ph,ptr,length).hex())
                    except (OSError,ValueError) as exc:frame['error']=repr(exc)
                    frames.append(frame)
        after=context();need(before==after,'unchanged context while read-only capture stopped')
        out.update(context_hex=before.hex(),context_after_hex=after.hex(),FS=fs,descriptor_hex=d.hex(),
                   TEB=teb,TEB_hex=head.hex(),slot=slot,slot_hex=slotraw.hex(),payload_hex=payload.hex(),
                   captured_ns=time.perf_counter_ns(),captured_qpc=w.qpc(),process=process_info(w,ph),
                   stack_address=esp,stack_hex=stack.hex(),EIP=eip,code_hex=code.hex(),
                   nt_create_file=nt_create,nt_create_code_hex=nt_code.hex(),syscall_frames=frames)
    finally:
        out['resume_previous']=w.resume(th)
        need(out['resume_previous']!=0xffffffff,'resume own suspend increment')
        out['suspend_ns']=time.perf_counter_ns()-start
    need(out['suspend_ns']<250_000_000 and previous==0 and out['resume_previous']==1,'bounded capture, no foreign suspend')
    return out


def run_case(exe,folder,gated):
    folder.mkdir();payload=folder/'payload.bin';payload.write_bytes(PAYLOAD)
    result=dict(gated=gated,input=identity(payload),error=None,accepted=False)
    lock=owner=None;ph=th=None;w=Win()
    try:
        if gated:lock=ReadOplock(payload,15)
        owner=Owned(exe,folder)
        if gated:
            need(lock.observe_break(10000),'one event-triggered read-open break')
            meta=load(folder/'worker.json');parent=load(folder/'parent.json')
            need(meta['pid']==parent['child_pid'] and parent['parent_pid']==owner.pi.pid,'original debugger parent binding')
            need(set(owner.ids())=={owner.pi.pid,meta['pid']},'only declared debugger parent and child')
            ph=w.openp(0x100410,False,meta['pid']);w.check(ph,'read child without debug attachment')
            th=w.opent(0x10004a,False,meta['tid']);w.check(th,'retain actual worker')
            result['capture']=capture(w,ph,th,meta)
            need(result['capture']['process']['parent_pid']==owner.pi.pid,'preserve debugger parent')
            need(result['capture']['process']['debug_port']==C.c_size_t(-1).value,'child remains debugged by original parent')
            result['return_file_before_release']=(folder/'child.json').exists()
            need(not result['return_file_before_release'],'ordinary worker not completed before release')
            result['before_release_ns']=time.perf_counter_ns()
            need(not lock.receipt['file_closed'],'lock held throughout capture')
            lock.release()
            need(w.wait(th,4000)==0,'original worker exits after close-ACK')
            code=W.DWORD();w.check(w.exit_thread(th,C.byref(code)),'retained worker exit query')
            result['worker_exit']=dict(code=code.value,wait=0,qpc_ns=time.perf_counter_ns())
            need(code.value==0,'retained worker exit0')
        need(owner.wait(8000)==0,'bounded normal debugger parent completion')
        result['child']=load(folder/'child.json');result['debugger']=load(folder/'debugger.json')
        result['meta']=load(folder/'worker.json');result['parent']=load(folder/'parent.json')
        child=result['child']['result']
        need(child['error'] is None and child['cleared'] and child['freed'] and result['child']['tls_freed'],'real helper cleanup')
        need(child['data_hex']==PAYLOAD.hex() and result['debugger']['error'] is None and
             result['debugger']['exit_code']==0 and not result['debugger']['forced'] and
             not result['debugger']['cleanup'],'unaltered successful IO and original debugger completion')
        if gated:
            need(child['before']<=lock.receipt['break_qpc']<=result['capture']['captured_qpc']<
                 lock.receipt['release_begin_qpc']<=child['after'],'same-QPC ordinary open held through capture')
            need(any(e['code']==4 and e['tid']==child['tid'] and e['value']==0
                     for e in result['debugger']['events']),'original debugger actual worker exit0 event')
    except BaseException as exc:result['error']=repr(exc)
    finally:
        if lock:
            try:result['oplock']=lock.finish()
            except BaseException as exc:result['oplock_cleanup_error']=repr(exc)
        result['read_handle_cleanup_errors']=[]
        for h in (th,ph):
            if h and not w.close(h):
                result['read_handle_cleanup_errors'].append(C.get_last_error())
        if owner:result['owner']=owner.finish()
        safe_read=(not lock or (lock.receipt['file_closed'] and lock.receipt['async_completed'])) and not any(
            pending.path==payload.resolve() for pending in PENDING_OWNERS)
        if safe_read:result['input_after']=identity(payload)
        else:result['input_after_skipped']='oplock cleanup incomplete; never open own locked stream'
    return result


def execute(folder):
    need(folder.resolve().is_relative_to(ROOT/'.venv-audit') and not folder.exists(),'fresh F project fixture directory')
    folder.mkdir();tmp=folder/'tmp';tmp.mkdir()
    report=dict(kind='owned_original_debugger_RW_oplock_preflight',accepted=False,
                implementations=[identity(ROOT/p) for p in DEPS],cases=[],error=None,
                game_started=False,observer_debug_attachment=False,game_or_thread_memory_writes=False)
    from devtools.terminal_host_desktop import snapshot,differences,health
    report['desktop_before']=snapshot()
    try:
        need(not health(report['desktop_before']),'healthy desktop baseline')
        compiler=Path('C:/Windows/Microsoft.NET/Framework/v4.0.30319/csc.exe')
        exe=folder/'oplock-fixture.exe';report['compiler']=identity(compiler)
        cp=subprocess.run([str(compiler),'/nologo','/target:winexe','/platform:x86','/optimize+',
            '/r:System.Web.Extensions.dll','/out:'+str(exe),str(ROOT/'devtools/terminal_oplock_fixture.cs')],
            cwd=folder,env=dict(os.environ,TEMP=str(tmp),TMP=str(tmp)),capture_output=True,timeout=20,
            creationflags=0x08000000)
        report['build']=dict(code=cp.returncode,stdout=cp.stdout.decode(errors='replace'),stderr=cp.stderr.decode(errors='replace'))
        need(cp.returncode==0,'bounded x86 fixture build');report['binary']=identity(exe)
        for name,gated in (('baseline',False),('oplocked',True)):
            case=run_case(exe,folder/name,gated);report['cases'].append(case)
            need(case['error'] is None and not case.get('oplock_cleanup_error') and
                 not case['read_handle_cleanup_errors'] and case['owner']['job_empty'] and
                 case['owner']['handles_closed'] and not case['owner']['errors'] and not case['owner']['forced'] and
                 case['input']==case.get('input_after') and not case.get('oplock',{}).get('watchdog_release'),
                 'normal representative case before proceeding')
    except BaseException as exc:report['error']=repr(exc)
    finally:
        report['desktop_after']=[snapshot()];time.sleep(1);report['desktop_after'].append(snapshot())
        report['desktop_checks']=[differences(report['desktop_before'],s) for s in report['desktop_after']]
        report['implementations_unchanged']=report['implementations']==[identity(ROOT/p) for p in DEPS]
        if report['desktop_checks']!=[[],[]] or not report['implementations_unchanged']:
            report['error']=report['error'] or 'desktop or frozen implementation verification failed'
        with (folder/'report.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--execute',action='store_true')
    parser.add_argument('--folder',type=Path,required=True);a=parser.parse_args()
    if not a.execute:print(json.dumps(dict(plan='baseline then RW-oplock owned debugger/child; no game, UI or target writes',maximum_seconds=60)))
    else:
        try:
            r=execute(a.folder.resolve());print(json.dumps(dict(error=r['error'],cases=[dict(gated=c['gated'],error=c['error']) for c in r['cases']],desktop_checks=r['desktop_checks'])))
        finally:
            if PENDING_OWNERS:
                # Even a reporting exception must not retire pending buffers.
                import sys
                try:sys.stdout.flush();sys.stderr.flush()
                finally:os._exit(6)
        need(r['error'] is None,'see preserved bounded preflight result')
