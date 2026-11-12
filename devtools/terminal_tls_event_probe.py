"""Owned no-UI WOW64 event controls. Never opens a game or existing process.

The notified fixture supplies a cooperative OutputDebugString boundary. The
silent control deliberately lacks that boundary. Neither qualifies the game.
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

ROOT=Path(__file__).resolve().parents[1]
DEPS=('devtools/terminal_tls_event_probe.py','devtools/terminal_tls_event_fixture.cs',
      'tools/school_crt_init_capture.py','tools/school_startup_inputs.py')
REFERENCES=('https://learn.microsoft.com/en-us/windows/win32/debug/debugging-events',
            'https://learn.microsoft.com/en-us/windows/win32/api/debugapi/nf-debugapi-continuedebugevent')


def need(ok, message):
    if not ok:raise ValueError(message)


def identity(path):
    p=Path(path);raw=p.read_bytes()
    return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def native_case(exe, mode):
    # Frozen ABI declarations only. No attach/arm/SetThreadContext path is used.
    from tools import school_crt_init_capture as abi
    w=abi.win
    duplicate=w.bind('DuplicateHandle',W.BOOL,[W.HANDLE,W.HANDLE,W.HANDLE,C.POINTER(W.HANDLE),W.DWORD,W.BOOL,W.DWORD])
    current=w.bind('GetCurrentProcess',W.HANDLE,[])
    thread_id=w.bind('GetThreadId',W.DWORD,[W.HANDLE])
    thread_pid=w.bind('GetProcessIdOfThread',W.DWORD,[W.HANDLE])
    exit_thread=w.bind('GetExitCodeThread',W.BOOL,[W.HANDLE,C.POINTER(W.DWORD)])
    exit_process=w.bind('GetExitCodeProcess',W.BOOL,[W.HANDLE,C.POINTER(W.DWORD)])
    selector=w.bind('Wow64GetThreadSelectorEntry',W.BOOL,[W.HANDLE,W.DWORD,C.c_void_p])
    qpc_api=w.bind('QueryPerformanceCounter',W.BOOL,[C.POINTER(C.c_int64)])
    qpf_api=w.bind('QueryPerformanceFrequency',W.BOOL,[C.POINTER(C.c_int64)])
    class DebugString(C.Structure):
        _fields_=[('data',C.c_void_p),('unicode',W.WORD),('length',W.WORD)]
    job=w.jobnew(None,None);w.check(job,'owned Job')
    limits=C.create_string_buffer(144);struct.pack_into('<I',limits,16,0x2000)
    w.check(w.setjob(job,9,limits,len(limits)),'kill-on-close limit')
    pi=w.PI();si=w.SI();si.cb=C.sizeof(si);si.flags=1;si.show=0
    events=[];handles={};pending=None;created=False;assigned=False;process_exited=False
    start=time.perf_counter();deadline=start+15
    report=dict(mode=mode,events=events,threads=[],captures=[],event_attempts=[],error=None,
                observer_memory_writes=[],observer_context_writes=[],breakpoints_installed=False,
                current_process_attach=False,forced_termination=False,fixture_capture_passed=False,
                original_adaptation_eligible=False,accepted=False)
    config=None
    loader_breaks=set()
    frequency=C.c_int64();w.check(qpf_api(C.byref(frequency)),'QPC frequency')
    report['qpc_frequency']=frequency.value
    def read(p,n):
        need(0<n<=4096,'bounded remote read');data=w.memory(pi.process,p,n)
        need(data is not None,'complete remote read '+hex(p));return data
    def retain(h,tid):
        local=W.HANDLE();w.check(duplicate(current(),h,current(),C.byref(local),0,False,2),'retain debug-event thread')
        try:need(thread_pid(local)==pi.pid and thread_id(local)==tid,'same owned thread generation')
        except BaseException:w.close(local);raise
        need(tid not in handles,'no reused retained thread ID')
        handles[tid]=local
        report['threads'].append(dict(tid=tid,owner_pid=pi.pid,create_event=len(events)-1,
                                      duplicate_succeeded=True))
    def capture(tid,index,pointer,stage):
        h=handles[tid];need(w.wait(h,0)==258,'live retained thread at event')
        before=abi.context(h);fs=struct.unpack_from('<I',before,144)[0]
        desc=C.create_string_buffer(8);w.check(selector(h,fs,desc),'actual WOW64 FS descriptor')
        d=desc.raw;teb=struct.unpack_from('<H',d,2)[0]|d[4]<<16|d[7]<<24
        head=read(teb,64);need(struct.unpack_from('<II',head,32)==(pi.pid,tid),'actual current TEB owner')
        need(struct.unpack_from('<I',head,24)[0]==teb,'TEB self')
        expansion=read(teb+0xF94,4) if index>=64 else None
        slot=(int.from_bytes(expansion,'little')+(index-64)*4) if expansion else teb+0xE10+index*4
        raw=read(slot,4);value=int.from_bytes(raw,'little')
        payload=read(value,116) if value else b''
        after=abi.context(h);need(before==after,'read-only context remained byte-identical at synchronous event')
        need(w.wait(h,0)==258,'same thread remains live until event continuation')
        return dict(stage=stage,tid=tid,index=index,pointer=pointer,FS=fs,selector_hex=d.hex(),
            TEB=teb,TEB_head_hex=head.hex(),expansion_hex=expansion.hex() if expansion else None,
            slot=slot,slot_hex=raw.hex(),payload_hex=payload.hex(),context_before_hex=before.hex(),
            context_after_hex=after.hex(),live_wait_before=258,live_wait_after=258,event_index=len(events)-1)
    try:
        command=C.create_unicode_buffer('"'+str(exe)+'" '+mode)
        w.check(w.create(str(exe),command,None,None,False,0x08000006,None,str(exe.parent),C.byref(si),C.byref(pi)),
                'create owned no-window debug fixture suspended')
        created=True;report.update(pid=pi.pid,main_tid=pi.tid)
        w.check(w.assign(job,pi.process),'assign only owned fixture');assigned=True
        w.check(w.resume(pi.thread)!=0xFFFFFFFF,'resume initial owned thread')
        while not process_exited:
            need(time.perf_counter()<deadline and len(events)<256,'bounded event loop')
            ev=abi.EVENT()
            if not abi.wait_event(C.byref(ev),100):
                need(C.get_last_error()==121,'WaitForDebugEvent timed wait only');continue
            pending=ev
            need(ev.pid==pi.pid,'debug events restricted to created helper')
            ticks=C.c_int64();w.check(qpc_api(C.byref(ticks)),'event QPC')
            row=dict(code=ev.code,pid=ev.pid,tid=ev.tid,qpc=time.perf_counter_ns(),raw_qpc=ticks.value,continued=False)
            events.append(row);status=0x10002
            if ev.code==3:
                if ev.u.create.file:w.close(ev.u.create.file)
                retain(ev.u.create.thread,ev.tid)
            elif ev.code==2:retain(ev.u.thread.thread,ev.tid)
            elif ev.code==6:
                if ev.u.file:w.close(ev.u.file)
            elif ev.code==1:
                code=ev.u.exception.record.code;row['exception_code']=code
                # Only ordinary OS loader breakpoints are handled, never inserted ones.
                loader=code in (0x80000003,0x4000001F) and config is None and ev.tid==pi.tid and code not in loader_breaks
                if loader:loader_breaks.add(code)
                row['loader_initial_break']=loader
                status=0x10002 if loader else 0x80010001
            elif ev.code==8:
                info=DebugString.from_buffer_copy(bytes(ev.u)[:C.sizeof(DebugString)])
                need(info.length<=1024,'bounded debug string')
                raw=read(info.data,info.length*(2 if info.unicode else 1))
                text=raw.decode('utf-16-le' if info.unicode else 'ascii',errors='strict').rstrip('\0')
                row['text']=text
                if text.startswith('TLS1 '):
                    fields=text.split();stage=fields[1];values=list(map(int,fields[2:]))
                    need(len(values) in (6,10) and values[0]==pi.pid,'owned fixture event payload')
                    pid,tid,index,pointer,qpc,freq=values[:6]
                    need(0<=index<1088 and freq==frequency.value,'native TLS/QPC bounds')
                    if stage=='config':config=values;need(tid==ev.tid and pointer==0,'MAIN config')
                    elif stage in ('live','clear'):
                        need(config and index==config[2] and tid==ev.tid and tid!=pi.tid,'current worker notification')
                        report['captures'].append(capture(tid,index,pointer,stage))
                    elif stage=='done':report['done']=values
                    else:raise ValueError('unknown fixture stage')
            elif ev.code==4:
                row['exit_code']=int(ev.u.exit_code)
                worker=next(x for x in report['threads'] if x['tid']==ev.tid)
                worker['exit_event']=len(events)-1;worker['exit_code']=row['exit_code']
            elif ev.code==5:
                row['exit_code']=int(ev.u.exit_code);report['process_exit_code']=row['exit_code'];process_exited=True
            elif ev.code not in (7,):raise ValueError('unsupported debug event')
            if config and ev.tid!=pi.tid and ev.code in (1,2,6,7,8) and not row.get('text','').startswith('TLS1 '):
                attempt=dict(event_index=len(events)-1,tid=ev.tid,error=None)
                try:attempt['capture']=capture(ev.tid,config[2],0,'natural_event')
                except Exception as exc:attempt['error']=repr(exc)
                report['event_attempts'].append(attempt)
            w.check(abi.continue_event(ev.pid,ev.tid,status),'continue same owned debug event')
            row.update(continued=True,continue_status=status,continued_qpc=time.perf_counter_ns());pending=None
        need(w.wait(pi.process,2000)==0,'normal owned process signaled')
        code=W.DWORD();w.check(exit_process(pi.process,C.byref(code)),'owned process exit query')
        report['queried_process_exit']=code.value
        for worker in report['threads']:
            h=handles[worker['tid']];wait=w.wait(h,0);code=W.DWORD()
            w.check(exit_thread(h,C.byref(code)),'retained thread exit query')
            worker['final_wait']=wait;worker['queried_exit']=code.value
        need(report['process_exit_code']==report['queried_process_exit']==0,'normal helper exit0')
    except Exception as exc:report['error']=repr(exc)
    finally:
        if pending is not None:
            ok=bool(abi.continue_event(pending.pid,pending.tid,0x80010001 if pending.code==1 else 0x10002))
            report['pending_continued_on_cleanup']=ok
        if created and not process_exited:
            report['forced_termination']=True
            if assigned:w.terminate(job,9)
            else:w.terminate_parent(pi.process,9)
            # Drain pending exits so termination completes before handles are closed.
            until=time.perf_counter()+2
            while time.perf_counter()<until and w.wait(pi.process,0)!=0:
                ev=abi.EVENT()
                if abi.wait_event(C.byref(ev),50):
                    if ev.code==6 and ev.u.file:w.close(ev.u.file)
                    abi.continue_event(ev.pid,ev.tid,0x10002)
        report['job_members_after']=w.ids(job)
        report['process_signaled_after_cleanup']=not created or w.wait(pi.process,0)==0
        closes=[]
        for h in handles.values():closes.append(bool(w.close(h)))
        if created:closes.extend((bool(w.close(pi.thread)),bool(w.close(pi.process))))
        closes.append(bool(w.close(job)));report['all_owned_handles_closed']=all(closes)
        report['wall_seconds']=time.perf_counter()-start
    return report


def run(folder):
    from devtools.terminal_host_desktop import snapshot,differences
    folder=Path(folder).resolve()
    need(folder.is_relative_to(ROOT/'.venv-audit') and folder.drive.lower()=='f:' and not folder.exists(),
         'fresh F-drive owned probe folder')
    folder.mkdir();tmp=folder/'tmp';tmp.mkdir()
    initial=[identity(ROOT/p) for p in DEPS]
    result=dict(kind='owned_WOW64_TLS_event_controls',accepted=False,original_adaptation_eligible=False,
                original_game_started=False,implementations=initial,references=REFERENCES,cases=[])
    before=snapshot();result['desktop_before']=before
    old_temp={k:os.environ.get(k) for k in ('TEMP','TMP')}
    try:
        os.environ.update(TEMP=str(tmp),TMP=str(tmp))
        compiler=Path(os.environ.get('SystemRoot','C:/Windows'))/'Microsoft.NET/Framework/v4.0.30319/csc.exe'
        need(compiler.is_file(),'existing x86 C# compiler')
        exe=folder/'tls-event-fixture.exe'
        build=subprocess.run([str(compiler),'/nologo','/platform:x86','/target:winexe','/optimize+',
            '/out:'+str(exe),str(ROOT/DEPS[1])],capture_output=True,timeout=10,
            creationflags=0x08000000,env=dict(os.environ,TEMP=str(tmp),TMP=str(tmp)))
        result['build']=dict(returncode=build.returncode,stdout=build.stdout.decode(errors='replace'),
                             stderr=build.stderr.decode(errors='replace'))
        need(build.returncode==0 and exe.stat().st_size<65536,'bounded helper build')
        result['binary']=identity(exe)
        for mode in ('notified','silent'):
            case=native_case(exe,mode);result['cases'].append(case)
            if case['error']:break
    except Exception as exc:result['error']=repr(exc)
    finally:
        for key,value in old_temp.items():
            if value is None:os.environ.pop(key,None)
            else:os.environ[key]=value
        after=[snapshot()];time.sleep(1);after.append(snapshot())
        result['desktop_after']=after;result['desktop_checks']=[differences(before,a) for a in after]
        result['implementations_unchanged']=initial==[identity(ROOT/p) for p in DEPS]
        result['clock']=dict(perf_counter=vars(time.get_clock_info('perf_counter')))
        out=folder/'report.json';raw=(json.dumps(result,indent=2)+'\n').encode()
        need(len(raw)<512*1024,'bounded fixture evidence')
        with out.open('xb') as f:f.write(raw)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--execute',action='store_true')
    parser.add_argument('--folder',type=Path);args=parser.parse_args()
    if not args.execute:print(json.dumps(dict(plan_only=True,no_UI=True,game_access=False,cases=['notified','silent'])))
    else:
        need(args.folder is not None,'fresh folder required');r=run(args.folder)
        print(json.dumps(dict(error=r.get('error'),cases=[dict(mode=c['mode'],error=c['error'],
            captures=len(c['captures']),events=len(c['events']),seconds=c['wall_seconds']) for c in r['cases']],
            desktop_checks=r['desktop_checks'],original_adaptation_eligible=False)))
