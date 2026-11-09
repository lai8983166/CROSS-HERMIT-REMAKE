"""PID-only heap ETW capability on an owned WOW64 helper; never original game.

The private extension encoding follows the pinned Microsoft TraceEvent source.
No WPT DLL, IFEO mutation, global kernel logger or external process is used.
Capture and offline decode are separate bounded guest-only operations.
"""
import argparse
import ctypes as C
import hashlib
import json
import os
from pathlib import Path
import queue
import struct
import subprocess
import threading
import time
import uuid
from devtools import terminal_wait_etw_probe as abi

ROOT=Path(__file__).resolve().parents[1]
ABI_SHA='60af4a1e487fff1e738808804be36cf7223b2843a365b123b49b1784087a31f6'
HEAP_GUID='222962ab-6180-4b88-a825-346b75f2a24a'
COMMIT='fd17789ba95a2e176b14d725721867c06d2377ed'
MICROSOFT_SOURCES={
 'src/TraceEvent/ETWKernelControl.cs':dict(bytes=26378,sha256='be6094f341112ca8b85dbb2174c37208b6b43ad7fee56eb8c5aa0b91b8cda79e'),
 'src/TraceEvent/Parsers/KernelTraceEventParser.cs':dict(bytes=565156,sha256='30ba785aa815ec546aa1ee4c1fb87f64af57066b0f852b1657a0bb2639a3f65c')}
MAX_ETL=4*1024*1024
MAX_SECONDS=30
need=abi.need
identity=abi.identity


def dependencies():
    need(identity(abi.__file__)['sha256']==ABI_SHA,'fixed previously audited ETW ABI module')
    return [identity(p)for p in (Path(__file__),Path(__file__).with_name('terminal_heap_etw_helper.cs'),Path(abi.__file__))]


def qualified():
    from devtools.native_input_isolation import require_qualified_guest
    return require_qualified_guest()


def new_output(path):
    path=Path(path).resolve()
    need(path.parent==ROOT/'analysis' and path.suffix=='.json' and not path.exists(),'new guest analysis output only')
    return path


def extension_bytes(pid):
    need(type(pid)is int and 0<pid<=0xffffffff,'one actual positive helper PID')
    # DWORD-count and extension-count, then PID item. No global PID zero.
    # Allocation and free stack IDs: event group 0x10 with opcodes 0x21/0x24.
    return struct.pack('<6I',6|(2<<16),2|(2<<16),pid,3|(3<<16),0x1021,0x1024)


def properties(name,path=None,pid=None):
    need(C.sizeof(abi.PROPERTIES)==120 and C.sizeof(abi.WNODE)==48 and C.sizeof(C.c_void_p)==8,'x64 controller layout')
    need(name.startswith('ChaomofaOwnedHeap-') and len(name)<96,'dedicated unique heap logger')
    buf=C.create_string_buffer(4096);p=abi.PROPERTIES.from_buffer(buf)
    p.Wnode.BufferSize=len(buf);p.Wnode.Guid[:]=uuid.UUID(HEAP_GUID).bytes_le
    p.Wnode.Flags=0x20000;p.Wnode.ClientContext=1
    p.LoggerNameOffset=120;name_bytes=(name+'\0').encode('utf-16-le')
    C.memmove(C.addressof(buf)+120,name_bytes,len(name_bytes))
    if path is not None:
        text=(str(path)+'\0').encode('utf-16-le');need(len(text)<=2048,'bounded ETL filename')
        p.LogFileNameOffset=120+len(name_bytes)
        C.memmove(C.addressof(buf)+p.LogFileNameOffset,text,len(text))
        offset=p.LogFileNameOffset+len(text);extra=extension_bytes(pid)
        need(offset+len(extra)<=len(buf) and offset<65536,'complete PID extension fits properties')
        C.memmove(C.addressof(buf)+offset,extra,len(extra));p.EnableFlags=0x80ff0000|offset
        p.BufferSize=64;p.MinimumBuffers=4;p.MaximumBuffers=8;p.MaximumFileSize=4;p.LogFileMode=1;p.FlushTimer=1
    return buf,p


class Session:
    def __init__(self,api,name,path,pid,clock=None):
        self.api=api;self.name=name;self.path=path;self.pid=pid;self.owned=False;self.handle=C.c_uint64()
        self.clock=clock
        self.record=dict(logger=name,pid=pid,owned=False,start_status=None,stop_status=None)
    def start(self):
        buf,p=properties(self.name,self.path,self.pid);self.record['requested_properties_hex']=bytes(buf).hex()
        if self.clock:self.record['start_begin_filetime']=self.clock()
        status=int(self.api.StartTraceW(C.byref(self.handle),self.name,C.byref(p)));self.record['start_status']=status
        if status==0:self.owned=True;self.record.update(owned=True,handle=self.handle.value)
        if self.clock:self.record['start_end_filetime']=self.clock()
        need(status==0 and self.handle.value!=0,'PID heap StartTraceW failed: '+str(status)+'; no existing logger touched')
    def stop(self):
        if not self.owned:return
        buf,p=properties(self.name)
        interval={}
        if self.clock:interval['begin_filetime']=self.clock()
        status=int(self.api.ControlTraceW(self.handle.value,self.name,C.byref(p),1))
        self.record.setdefault('stop_attempts',[]).append(status);self.record['stop_status']=status
        self.record['statistics']={k:int(getattr(p,k))for k in ('EventsLost','LogBuffersLost','RealTimeBuffersLost','BuffersWritten')}
        self.record['returned_stop_properties_hex']=bytes(p).hex()
        self.owned=status not in (0,234,4201)
        if self.clock:interval['end_filetime']=self.clock()
        self.record.setdefault('stop_intervals',[]).append(interval)


def check_helper(ready,live,closed):
    need(ready['stage']=='ready' and ready['wow64']is True and ready['pointer_size']==4,'actual WOW64 fixture')
    need(live['stage']=='live' and (live['pid'],live['tid'])==(ready['pid'],ready['tid']),'same fixture PID/TID')
    need(all(type(live[k])is int and 0<live[k]<=0xffffffff for k in ('heap','freed_address','live_address')),'actual WOW64 allocation pointers')
    need(live['freed_address']!=live['live_address'] and live['free_result']is True and live['live_not_freed']is True,'free and live counterexample distinct')
    need(live['freed_size']==152 and live['live_size']==296,'exact two allocation sizes')
    need(closed['stage']=='closed' and closed['live_free_result']is True and closed['heap_destroy_result']is True,'owned helper clean exit')
    times=[ready['filetime'],live['begin_filetime'],live['end_filetime'],closed['begin_filetime'],closed['end_filetime']]
    need(all(type(t)is int and t>0 for t in times) and times==sorted(times),'ordered actual helper FILETIME receipts')


def x86_helper_image(path):
    b=Path(path).read_bytes();need(0<len(b)<=1024*1024 and b[:2]==b'MZ','bounded actual compiled helper PE')
    offset=struct.unpack_from('<I',b,0x3c)[0]
    need(offset+26<=len(b) and b[offset:offset+4]==b'PE\0\0' and struct.unpack_from('<H',b,offset+4)[0]==0x14c
         and struct.unpack_from('<H',b,offset+24)[0]==0x10b,'actual compiled helper x86 PE32')
    return identity(path)


def cleanup_helper(proc,result):
    forced=False
    if proc.poll()is None:
        try:proc.stdin.write(b'cleanup\n');proc.stdin.flush();proc.wait(timeout=1)
        except Exception:
            forced=True
            try:proc.kill();proc.wait(timeout=2)
            except Exception as exc:result['errors'].append('owned helper emergency cleanup: '+repr(exc));result['status']='blocked'
    result['cleanup'].update(helper_forced=forced,helper_exit=proc.returncode)
    # A failed emergency cleanup must not hang on an open pipe or erase the report.
    if proc.poll()is not None:
        try:
            error=proc.stderr.read(8193)
            result['cleanup']['helper_stderr']=error[:8192].decode(errors='replace')
            if len(error)>8192:raise ValueError('helper stderr exceeds bound')
        except Exception as exc:result['errors'].append('stderr cleanup: '+repr(exc));result['status']='blocked'
        for stream in (proc.stdin,proc.stdout,proc.stderr):
            try:stream.close()
            except Exception as exc:result['errors'].append('pipe close: '+repr(exc));result['status']='blocked'
    else:
        result['errors'].append('owned helper remains alive; pipes not synchronously closed');result['status']='blocked'


def run(out):
    qualification=qualified() # Before compiler, helper, Windows API or hook.
    begun=time.monotonic();out=new_output(out);before=dependencies();folder=out.with_suffix('')
    need(not folder.exists(),'new artifact directory');folder.mkdir()
    result=dict(kind='owned_WOW64_PID_heap_ETW_capability',accepted=False,original_game=False,fullABI=False,PTDcleanup=False,
        qualification=qualification,implementations=before,helper={},trace=None,errors=[],cleanup={},bounds=dict(seconds=30,ETL_bytes=MAX_ETL),
        registry_modified=False,IFEO_modified=False,global_kernel_logger_used=False,process_memory_written=False,
        original_process_opened=False,heap_tracing_is_instrumentation=True,
        limitation='No observer remote memory writes. ETW configures the owned helper allocator and can perturb it; no zero-perturbation or original-game compatibility claim.',
        Microsoft_commit=COMMIT,Microsoft_sources=MICROSOFT_SOURCES)
    proc=None;session=None
    def remaining(cap=5):
        left=MAX_SECONDS-3-(time.monotonic()-begun);need(left>0,'capture deadline before cleanup reserve');return min(cap,left)
    try:
        compiler=Path(os.environ.get('SystemRoot','C:/Windows'))/'Microsoft.NET/Framework/v4.0.30319/csc.exe'
        need(compiler.is_file(),'built-in Framework x86 compiler unavailable; no installation fallback')
        exe=folder/'heap-fixture.exe';tmp=folder/'tmp';tmp.mkdir();env=dict(os.environ,TEMP=str(tmp),TMP=str(tmp))
        build=subprocess.run([str(compiler),'/nologo','/platform:x86','/target:exe','/out:'+str(exe),str(Path(__file__).with_name('terminal_heap_etw_helper.cs'))],
            capture_output=True,timeout=remaining(10),creationflags=0x08000000,env=env)
        need(len(build.stdout)+len(build.stderr)<=8192,'bounded compiler diagnostics')
        result['compiler']=identity(compiler);result['build']=dict(returncode=build.returncode,stdout=build.stdout.decode(errors='replace'),stderr=build.stderr.decode(errors='replace'))
        need(build.returncode==0 and exe.is_file(),'owned x86 helper build failed')
        result['helper_executable']=x86_helper_image(exe)
        proc=subprocess.Popen([str(exe)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=0x08000000,env=env)
        lines=queue.Queue(maxsize=4)
        def reader():
            for unused in range(4):
                b=proc.stdout.readline(8193)
                try:lines.put_nowait(b)
                except queue.Full:return
                if not b or len(b)>8192:return
        thread=threading.Thread(target=reader,daemon=True);thread.start()
        def read():
            b=lines.get(timeout=remaining());need(0<len(b)<=8192 and b.endswith(b'\n'),'complete bounded helper receipt');return json.loads(b)
        ready=read();result['helper']['ready']=ready
        need(ready['pid']==proc.pid and ready['stage']=='ready' and ready['pointer_size']==4 and ready['wow64']is True,'owned ready WOW64 process')
        kernel,api=abi.bind_windows()
        def filetime():
            ticks=C.c_uint64();kernel.GetSystemTimePreciseAsFileTime(C.byref(ticks));return ticks.value
        session=Session(api,'ChaomofaOwnedHeap-'+uuid.uuid4().hex,folder/'trace.etl',proc.pid,filetime)
        result['trace']=session.record;session.start()
        proc.stdin.write(b'allocate\n');proc.stdin.flush();live=read();result['helper']['live']=live
        need(time.monotonic()-begun<27 and proc.poll()is None,'helper stays live before stop')
        session.stop();need(session.record['stop_status']==0,'owned heap logger successful stop required')
        result['trace_stopped_before_live_cleanup']=True
        proc.stdin.write(b'cleanup\n');proc.stdin.flush();closed=read();result['helper']['closed']=closed
        proc.wait(timeout=remaining());result['helper_exit']=proc.returncode
        need(proc.returncode==0,'helper exited normally');check_helper(ready,live,closed)
        need(all(session.record['statistics'][k]==0 for k in ('EventsLost','LogBuffersLost','RealTimeBuffersLost')),'capture loss counters must be zero')
        need((folder/'trace.etl').is_file() and 0<(folder/'trace.etl').stat().st_size<=MAX_ETL,'bounded retained sequential ETL')
        result['status']='captured_decode_required'
    except Exception as exc:result['errors'].append(repr(exc));result['status']='blocked'
    finally:
        if session is not None and session.owned:
            try:session.stop()
            except Exception as exc:result['errors'].append('stop cleanup: '+repr(exc))
        result['cleanup']['logger_still_owned']=bool(session is not None and session.owned)
        if proc is not None:
            try:cleanup_helper(proc,result)
            except Exception as exc:result['errors'].append('owned helper cleanup observation: '+repr(exc));result['status']='blocked'
        try:
            if (folder/'trace.etl').is_file():result['ETL']=identity(folder/'trace.etl')
            result['implementations_after']=dependencies()
        except Exception as exc:result['errors'].append('final identity: '+repr(exc));result['status']='blocked'
        result['elapsed_seconds']=time.monotonic()-begun
        if result.get('implementations_after')!=before or result['elapsed_seconds']>30 or result['cleanup'].get('logger_still_owned') or result['cleanup'].get('helper_forced'):
            result['errors'].append('identity, duration or owned cleanup boundary failed');result['status']='blocked'
        write_report(out,result)
    return result


def write_report(path,result):
    # Qualification carries a large authenticated module body; keep its digest/reference.
    if 'qualification'in result:
        raw=json.dumps(result.pop('qualification'),sort_keys=True,separators=(',',':')).encode()
        result['qualification_receipt_sha256']=hashlib.sha256(raw).hexdigest()
    raw=(json.dumps(result,indent=2)+'\n').encode();need(len(raw)<=65536,'bounded compact report')
    with Path(path).open('xb')as f:f.write(raw)


def parse_heap(opcode,flags,version,payload):
    need(opcode in (33,36) and version==0,'known pinned heap alloc/free version zero only')
    need(flags&0x60 in (0x20,0x40),'unambiguous native event pointer width')
    width=4 if flags&0x20 else 8;count=3 if opcode==33 else 2
    need(len(payload)==width*count+4,'complete exact pinned heap payload length')
    fields=[int.from_bytes(payload[i*width:(i+1)*width],'little')for i in range(count)]
    return dict(heap=fields[0],address=fields[2]if opcode==33 else fields[1],size=fields[1]if opcode==33 else None,
                source=int.from_bytes(payload[-4:],'little'),pointer_size=width)


def analyze_matches(records,source):
    ready=source['helper']['ready'];live=source['helper']['live'];closed=source['helper']['closed'];check_helper(ready,live,closed)
    expected=[(33,live['freed_address'],152),(33,live['live_address'],296),(36,live['freed_address'],None)]
    need(len(records)==3,'exact two allocations and one free; live negative has no free')
    actual=[]
    for r in records:
        need(r['pid']==ready['pid'] and r['tid']==ready['tid'],'event actual helper owner')
        h=bytes.fromhex(r['header_hex']);p=bytes.fromhex(r['payload_hex'])
        need(len(h)==80 and str(uuid.UUID(bytes_le=h[24:40]))==HEAP_GUID,'exact original heap header')
        need(struct.unpack_from('<II',h,8)==(r['tid'],r['pid']) and struct.unpack_from('<q',h,16)[0]==r['filetime']
             and h[45]==r['opcode'],'actual raw event owner, timestamp and opcode')
        d=parse_heap(h[45],struct.unpack_from('<H',h,4)[0],h[42],p)
        need(d==r['data'] and d['heap']==live['heap'] and d['pointer_size']==4,'same actual WOW64 fixture heap and raw fields')
        need(live['begin_filetime']<=r['filetime']<=live['end_filetime'],'actual event inside helper operation envelope')
        actual.append((r['opcode'],d['address'],d['size']))
    need(actual==expected and [r['filetime']for r in records]==sorted(r['filetime']for r in records),'ordered distinct fixture alloc/free records')
    return dict(two_allocations_and_one_free_observed=True,kept_live_allocation_not_reported_freed=True,
                helper_HeapFree_BOOL=True,event_HeapFree_BOOL_present=False,caller_stack_verified=False,original_game=False,PTDcleanup=False)


def check_capture_source(source):
    need(source['kind']=='owned_WOW64_PID_heap_ETW_capability' and source['accepted']is False
         and source['original_game']is False and source['fullABI']is False and source['PTDcleanup']is False,'explicit capability scope')
    need(source['trace']['start_status']==source['trace']['stop_status']==0 and source['trace']['owned']is True,'actual owned start/stop success')
    raw=bytes.fromhex(source['trace']['requested_properties_hex']);need(len(raw)==4096,'complete requested properties including PID extension')
    p=abi.PROPERTIES.from_buffer_copy(raw);offset=p.EnableFlags&0xffff
    need(p.EnableFlags&0xffff0000==0x80ff0000 and 120<=offset<=len(raw)-24
         and raw[offset:offset+24]==extension_bytes(source['helper']['ready']['pid']),'exact single helper PID and stack extension')
    need(bytes(p.Wnode.Guid)==uuid.UUID(HEAP_GUID).bytes_le and p.Wnode.ClientContext==1 and p.LogFileMode==1
         and p.MaximumFileSize==4 and p.BufferSize==64 and p.MinimumBuffers==4 and p.MaximumBuffers==8,'bounded PID heap trace properties')
    stopped=abi.PROPERTIES.from_buffer_copy(bytes.fromhex(source['trace']['returned_stop_properties_hex']))
    need(all(getattr(stopped,k)==source['trace']['statistics'][k]==0 for k in ('EventsLost','LogBuffersLost','RealTimeBuffersLost')),'original stop bytes authenticate zero loss')
    need(source['trace']['pid']==source['helper']['ready']['pid'] and source['helper_exit']==0,'same capture helper lifetime')
    trace=source['trace'];need(len(trace['stop_intervals'])==1 and trace['stop_attempts']==[0],'one successful directly timed stop')
    stop=trace['stop_intervals'][0]
    timing=[source['helper']['ready']['filetime'],trace['start_begin_filetime'],trace['start_end_filetime'],
            source['helper']['live']['begin_filetime'],source['helper']['live']['end_filetime'],stop['begin_filetime'],stop['end_filetime'],
            source['helper']['closed']['begin_filetime'],source['helper']['closed']['end_filetime']]
    need(all(type(t)is int and t>0 for t in timing) and timing==sorted(timing),'actual precise StartTrace/StopTrace envelopes separate live allocation from cleanup')
    need(source['cleanup']['logger_still_owned']is False and source['elapsed_seconds']<=MAX_SECONDS
         and source['registry_modified']is False and source['IFEO_modified']is False
         and source['global_kernel_logger_used']is False and source['process_memory_written']is False,'bounded isolated capability only')


def decode(source_path,source_sha,etl_path,etl_sha,out):
    qualified();begun=time.monotonic();out=new_output(out);before=dependencies()
    source_path=Path(source_path);etl_path=Path(etl_path)
    need(identity(source_path)['sha256']==source_sha and source_path.stat().st_size<=65536,'fixed bounded capture source')
    source=json.loads(source_path.read_bytes());need(identity(etl_path)['sha256']==etl_sha and 0<etl_path.stat().st_size<=MAX_ETL,'fixed bounded ETL')
    need(source['ETL']['sha256']==etl_sha and source['status']=='captured_decode_required' and not source['errors'],'actual successful capture source')
    need(source['implementations']==before and source['implementations_after']==before,'same exact capture/decoder implementation')
    check_capture_source(source)
    check_helper(source['helper']['ready'],source['helper']['live'],source['helper']['closed'])
    need(source['trace_stopped_before_live_cleanup']is True and source['cleanup']['helper_forced']is False and source['cleanup']['helper_exit']==0,'cleanup and live negative bound')
    result=dict(kind='owned_WOW64_heap_ETW_decode',accepted=False,original_game=False,fullABI=False,PTDcleanup=False,
                source=identity(source_path),ETL=identity(etl_path),implementations=before,errors=[])
    try:
        _read(etl_path,source,result,begun+30)
        result['analysis']=analyze_matches(result['matching_records'],source);result['status']='owned_WOW64_heap_events_observed'
    except Exception as exc:result['errors'].append(repr(exc));result['status']='blocked'
    result['elapsed_seconds']=time.monotonic()-begun;result['implementations_after']=dependencies()
    if result['implementations_after']!=before or result['elapsed_seconds']>30:result['errors'].append('decoder identity/time boundary');result['status']='blocked'
    write_report(out,result);return result


def _read(path,source,result,deadline):
    result['ABI']=abi.decoder_layout();api=C.WinDLL('advapi32',use_last_error=True)
    api.OpenTraceW.argtypes=[C.POINTER(abi.LOGFILE)];api.OpenTraceW.restype=C.c_uint64
    api.ProcessTrace.argtypes=[C.POINTER(C.c_uint64),C.c_uint32,C.c_void_p,C.c_void_p];api.ProcessTrace.restype=C.c_uint32
    api.CloseTrace.argtypes=[C.c_uint64];api.CloseTrace.restype=C.c_uint32
    errors=[];buffers=[];matches=[];counts={};digest=hashlib.sha256();total=0;foreign=0
    live=source['helper']['live'];pid=source['helper']['ready']['pid'];samples={}
    def event(record):
        nonlocal total,foreign
        if errors:return
        try:
            need(time.monotonic()<deadline,'bounded offline decode deadline');total+=1;need(total<=100000,'bounded complete heap event count')
            e=record.contents;h=e.EventHeader
            need(e.UserDataLength<=65535 and (e.UserData or not e.UserDataLength),'bounded native payload pointer')
            payload=C.string_at(e.UserData,e.UserDataLength)if e.UserDataLength else b''
            digest.update(struct.pack('<I',len(payload))+bytes(h)+bytes(e.BufferContext)+payload)
            guid=str(uuid.UUID(bytes_le=bytes(h.ProviderId)));opcode=h.EventDescriptor.Opcode
            if guid!=HEAP_GUID:return
            key=str(opcode);counts[key]=counts.get(key,0)+1
            if h.ProcessId!=pid:foreign+=1;return
            if key not in samples and len(samples)<20:
                samples[key]=dict(header_hex=bytes(h).hex(),payload_prefix_hex=payload[:128].hex(),payload_bytes=len(payload),extended_data_count=e.ExtendedDataCount)
            if opcode not in (33,36):return
            data=parse_heap(opcode,h.Flags,h.EventDescriptor.Version,payload)
            if data['heap']!=live['heap']or data['address']not in (live['freed_address'],live['live_address']):return
            need(len(matches)<8,'bounded duplicate/counterexample detection')
            matches.append(dict(index=total,pid=h.ProcessId,tid=h.ThreadId,filetime=h.TimeStamp,opcode=opcode,data=data,
                                header_hex=bytes(h).hex(),payload_hex=payload.hex(),buffer_context_hex=bytes(e.BufferContext).hex(),extended_data_count=e.ExtendedDataCount))
        except Exception as exc:errors.append(repr(exc))
    def buffer(log):
        try:
            need(time.monotonic()<deadline and len(buffers)<80,'bounded decoder buffers/deadline');need(log.contents.EventsLost==0,'buffer events lost')
            buffers.append(int(log.contents.BuffersRead));return 0 if errors else 1
        except Exception as exc:errors.append(repr(exc));return 0
    event_cb=C.WINFUNCTYPE(None,C.POINTER(abi.EVENT_RECORD))(event)
    buffer_cb=C.WINFUNCTYPE(C.c_uint32,C.POINTER(abi.LOGFILE))(buffer)
    log=abi.LOGFILE();log.LogFileName=str(path);log.ProcessTraceMode=0x10000000
    log.EventRecordCallback=C.cast(event_cb,C.c_void_p).value;log.BufferCallback=C.cast(buffer_cb,C.c_void_p).value
    handle=int(api.OpenTraceW(C.byref(log)));need(handle!=0xffffffffffffffff,'OpenTraceW failed')
    try:
        header=log.LogfileHeader;result['ETL_header_raw_hex']=bytes(header).hex()
        need(header.EventsLost==header.BuffersLost==0,'zero original ETL header loss')
        need(header.BuffersWritten==source['trace']['statistics']['BuffersWritten'],'same complete stop/header buffer count')
        need(all(source['trace']['statistics'][k]==0 for k in ('EventsLost','LogBuffersLost','RealTimeBuffersLost')),'zero original stop loss')
        need(header.StartTime<=source['helper']['live']['begin_filetime']<=source['helper']['live']['end_filetime']<=header.EndTime,'ETL header covers helper operations')
        need(header.EndTime<=source['trace']['stop_intervals'][0]['end_filetime']<=source['helper']['closed']['begin_filetime'],
             'actual ETL end precedes retained allocation cleanup')
        handles=(C.c_uint64*1)(handle);status=int(api.ProcessTrace(handles,1,None,None))
        result.update(process_trace_status=status,callback_errors=errors,buffer_reads=buffers,total_records=total,heap_opcode_counts=counts,
                      foreign_heap_events=foreign,first_heap_schema_samples=list(samples.values()),matching_records=matches,complete_event_digest=digest.hexdigest(),
                      digest_coverage='length-prefix + converted EVENT_HEADER80 + BUFFER_CONTEXT4 + UserData; original full ETL retained')
        need(status==0 and not errors and buffers and buffers[-1]==header.BuffersWritten,'complete successful ETL consumption')
        need(foreign==0,'PID extension must not emit foreign heap events')
    finally:
        result['close_trace_status']=int(api.CloseTrace(handle));need(result['close_trace_status']==0,'owned offline reader closed')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True,type=Path);p.add_argument('--decode',action='store_true')
    for k in ('source','source-sha','etl','etl-sha'):p.add_argument('--'+k)
    a=p.parse_args()
    if a.decode:r=decode(a.source,a.source_sha,a.etl,a.etl_sha,a.out)
    else:r=run(a.out)
    print(json.dumps(dict(status=r['status'],errors=r['errors'],accepted=False)))
    return 2 if r['status']!='blocked' else 1


if __name__=='__main__':raise SystemExit(main())
