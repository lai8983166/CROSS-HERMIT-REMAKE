"""Bounded read-only wait window attached to the original legal retreat input.

New observer only; frozen school/input/ETW modules are not edited. ETW and
snapshots cannot establish full instruction/state or resource-lifetime replay.
"""
import argparse
from contextlib import contextmanager
import ctypes as C
import ctypes.wintypes as W
import gzip
import hashlib
import json
from pathlib import Path
import struct
import threading
import time
from types import SimpleNamespace

from devtools import terminal_original_wait_etw as original
from devtools.terminal_scene_resources import clone

ROOT=Path(__file__).resolve().parents[1]
ETL_LIMIT=64*1024*1024
MAX_SECONDS=3.0
MAX_SNAPSHOTS=768
CODE_RANGES=((0x422360,0x422434),(0x422560,0x4225DA),(0x56CE80,0x56CE98),
             (0x4539B0,0x453CFC),(0x451A60,0x451B0F),(0x451670,0x4519A3),
             (0x496410,0x49644C),(0x4967B0,0x4968A9),(0x50A007,0x50A1E8))
TRACE_LIMITS=dict(maximum_file_mib=64,buffer_kib=64,minimum_buffers=4,maximum_buffers=8,
    max_events=2000000,max_buffers=1024,max_selected_records=16384,
    max_selected_gzip_bytes=524288,decode_seconds=180)
ANCESTORS=(0x453CB5,0x453CD3,0x453CDD,0x451ABC,0x451716,0x451758,0x451796,0x421F8A)
need=original.need
identity=original.identity
word=lambda raw,off=0:struct.unpack_from('<I',raw,off)[0]


def properties(path=None):
    buf,p=original.trace_properties(path)
    if path is not None:p.MaximumFileSize=64
    return buf,p


def extended_stack(c,frame):
    rows=original.stack_regions(c,frame)
    for link in frame['chain']:
        if link['return_va'] in ANCESTORS:
            for bp in (link['bp'],link['saved_bp']):
                rows.append(dict(pointer=bp-0x90,hex=c.get(bp-0x90,0xA0).hex()))
    return rows


def wrap_click_api(api,start):
    """Start just before the final original guard, without changing input values."""
    old=api.left_button_down;calls=0
    def query():
        nonlocal calls
        calls+=1
        need(calls<=2,'frozen click protocol has exactly two left-button queries')
        if calls==2:start()
        return old()
    api.left_button_down=query
    return api


class WaitWindow:
    def __init__(self,c,node,tid,main_tid,folder,phase,qualification):
        from devtools.native_input_isolation import require_qualified_guest
        require_qualified_guest()
        from devtools import terminal_wait_etw_probe as etw
        self.c=c;self.node=node;self.tid=tid;self.main_tid=main_tid;self.phase=phase
        self.lock=threading.RLock();self.active=False;self.finished=False;self.session=None;self.thread_handle=None
        self.kernel,self.advapi=etw.bind_windows();self.folder=Path(folder)
        need(not self.folder.exists(),'fresh window artifact directory')
        self.folder.mkdir();self.etl=self.folder/'trace.etl'
        self.result=dict(kind='battle_wait_result_window',phase=phase,error=None,
            subject=dict(pid=c.pid,tid=tid,main_tid=main_tid,main=c.main,node=node),
            input_isolation=qualification,trace_flags=0x92,ETL_limit=ETL_LIMIT,trace_limits=dict(TRACE_LIMITS),
            maximum_seconds=MAX_SECONDS,maximum_snapshots=MAX_SNAPSHOTS,
            window_snapshots=[],non_wait_samples=[],sample_attempts=0,non_wait_count=0,
            host_game_calls=[],host_memory_writes=[],host_input_actions=[],
            source_memory_written=False,general_registers_written=False,debug_registers_written=False,
            debug_object_modified=False,debugger_reply_substituted=False,
            accepted=False,full_instruction_trace=False,full_resource_lifetime_proved=False,
            full_battle_exit_accepted=False,wait_return_proved=False,result_consumption_proved=False)

    @contextmanager
    def synchronized_input_snapshots(self):
        from devtools import terminal_scene_owner as base
        previous=base.original.frozen
        @contextmanager
        def locked(*args,**kwargs):
            with self.lock:
                with previous(*args,**kwargs)as frames:yield frames
        base.original.frozen=locked
        try:yield
        finally:
            need(base.original.frozen is locked,'scoped observer wrapper not replaced')
            base.original.frozen=previous

    def snapshot(self):
        from devtools import terminal_scene_owner as base,terminal_startup_handoff as startup
        c=self.c
        with self.lock, original.owned_frames(c,[self.main_tid,self.tid])as frames:
            begin=original.utc_now_ns(self.kernel)
            frame=next(x for x in frames if x['tid']==self.tid)
            self.result['sample_attempts']+=1
            returns={x['return_va']for x in frame['chain']}
            if not {0x42240D,0x421F8A,0x56E183}<=returns:
                self.result['non_wait_count']+=1
                if len(self.result['non_wait_samples'])<16:
                    self.result['non_wait_samples'].append(dict(snapshot_begin_ns=begin,
                        snapshot_end_ns=original.utc_now_ns(self.kernel),frame=frame))
                return None
            manager,nodes=startup.graph(c)
            need(any(x['pointer']==self.node for x in nodes),'actual waiting node remains registered')
            head=c.get(self.node,64)
            need(word(head,8)==c.main+0x64 and word(head,0x24)==self.tid,'same live scene/worker')
            row=dict(snapshot_begin_ns=begin,node_pointer=self.node,node_hex=head.hex(),
                manager_pointer=c.main+0x64,manager_hex=manager.hex(),registered_nodes=nodes,
                frame=frame,scheduler_frame=next(x for x in frames if x['tid']==self.main_tid),
                current_TLS=base.capture_tls(c,frame,self.node),stack_regions=extended_stack(c,frame),
                source_memory_written=False,debug_registers_written=False)
            if self.phase=='battle_retreat':
                row.update(scene_head_hex=c.get(self.node,0x200).hex(),
                    controller_backpointer=dict(pointer=self.node+0x190+0x117C38,
                        hex=c.get(self.node+0x190+0x117C38,4).hex()),
                    recording_gate=dict(pointer=self.node+0x190+0x117C3C,
                        hex=c.get(self.node+0x190+0x117C3C,1).hex()))
            row['snapshot_end_ns']=original.utc_now_ns(self.kernel)
            return row

    def begin(self):
        from devtools import terminal_scene_owner as base, terminal_wait_etw_probe as etw
        from tools.school_crt_init_nested import resolve
        import pefile
        with self.lock:
            need(not self.active and not self.finished,'one original input-triggered trace only')
            c=self.c;r=self.result
            r['kernel_wait_export']=original.kernel_wait_identity()
            raw=base.SOURCE.read_bytes();need(base.sha(raw)==base.SOURCE_SHA,'fixed original image')
            r['original_code']=[]
            for lo,hi in CODE_RANGES:
                value=c.get(lo,hi-lo);need(value==raw[lo-0x400000:hi-0x400000],'actual unchanged original window code')
                r['original_code'].append(dict(pointer=lo,hex=value.hex()))
            r['API_exports']=[]
            for module,name,slot in (('kernel32.dll','WaitForSingleObject',0x59226C),('ntdll.dll','NtWaitForSingleObject',None)):
                entry=resolve(c.pid,module,name)
                mapped=pefile.PE(entry['module_path']).get_memory_mapped_image(ImageBase=entry['base'])
                value=c.get(entry['target'],64);need(value==mapped[entry['RVA']:entry['RVA']+64],'actual relocated wait export')
                iat=c.get(slot,4)if slot else None
                need(iat is None or word(iat)==entry['target'],'actual original wait IAT')
                r['API_exports'].append(dict(name=name,slot=slot,IAT_hex=iat.hex()if iat else None,entry_hex=value.hex(),**entry))
            r['TLS_implementation']=base.tls_contract(c)
            r['before']=self.snapshot();need(r['before']is not None,'actual original wait before trace')
            head=bytes.fromhex(r['before']['node_hex'])
            r['event_owners']=dict(node_event=base.event_identity(c,word(head,0x1C)),
                manager_event=base.event_identity(c,word(bytes.fromhex(r['before']['manager_hex']),0x118)))
            handle=W.HANDLE()
            base.original.check(base.parent.duplicate(c.h,word(head,0x20),base.parent.current_process(),
                C.byref(handle),0,False,2),'retain exact original worker for exit observation')
            self.thread_handle=handle
            need(base.get_thread_pid(handle)==c.pid and base.get_thread_id(handle)==self.tid,'retained worker identity')
            class WindowSession(etw.Session):
                start=clone(etw.Session.start,properties=properties)
            self.session=WindowSession(self.advapi,self.etl);self.session.start()
            r['capture_interval']=dict(begin_ns=original.utc_now_ns(self.kernel))
            self.started=time.monotonic();self.active=True

    def thread_exit(self):
        from devtools import terminal_scene_owner as base
        status=base.original.wait(self.thread_handle,0)
        need(status in (0,258),'valid current original thread status query')
        if status==0:
            code=W.DWORD();base.original.check(base.parent.exit_thread(self.thread_handle,C.byref(code)),'original worker exit status')
            self.result['worker_exit']=dict(code=code.value,wait_status=status,
                observed_ns=original.utc_now_ns(self.kernel),before_WM_CLOSE=True,
                duplicate_handle_query_only=True,PTDcleanup=False)
            need(code.value==0,'original worker exited abnormally')
            return True
        return False

    def poll(self):
        with self.lock:
            if not self.active or self.finished:return
            if time.monotonic()-self.started>=MAX_SECONDS:
                self.result['stop_reason']='bounded_window_deadline';self.finish();return
            if self.thread_exit():
                self.result['stop_reason']='original_worker_exit_observed';self.finish();return
            try:row=self.snapshot()
            except Exception as exc:
                if self.thread_exit():
                    self.result['sampling_exit_race']=repr(exc)
                    self.result['stop_reason']='worker_exit_during_read_only_sample';self.finish();return
                raise
            if row is not None:
                need(len(self.result['window_snapshots'])<MAX_SNAPSHOTS,'complete window sample budget; no truncation')
                self.result['window_snapshots'].append(row)

    def drain(self,seconds=MAX_SECONDS):
        until=time.monotonic()+seconds
        while self.active and not self.finished and time.monotonic()<until:
            self.poll();time.sleep(.001)
        if not self.finished:
            self.result.setdefault('stop_reason','bounded_preflight_window'if self.phase=='startup_preflight'else'bounded_window_drain')
            self.finish()

    def finish(self):
        from devtools import terminal_scene_owner as base
        with self.lock:
            if self.finished:return
            self.finished=True
            if self.active:self.result['capture_interval']['end_ns']=original.utc_now_ns(self.kernel)
            if self.session is not None:
                self.result['trace']=self.session.stop()
                if self.session.owned:self.result['trace']=self.session.stop()
                if self.session.owned or self.result['trace'].get('stop_status')!=0:
                    self.result['error']='owned window ETW stop failed'
            if self.thread_handle:
                self.result['observer_thread_duplicate_closed']=bool(base.original.close(self.thread_handle))
                self.thread_handle=None
                if not self.result['observer_thread_duplicate_closed']:self.result['error']='observer thread duplicate close failed'
            if self.etl.exists():
                self.result['ETL']=identity(self.etl)
                if not 0<self.result['ETL']['bytes']<ETL_LIMIT:self.result['error']='bounded complete window ETL exceeded'


def startup_probe(out,qualification):
    from devtools import terminal_menu_handoff as menu,terminal_scene_owner as base
    from devtools.isolated_guest_focus import guest_focus_scope
    from devtools.isolated_guest_dep_observer import DepObserver
    def observe(pid,owned,progress,duration):
        h=None;window=None
        try:
            h=base.original.openp(0x100450,False,pid);base.original.check(h,'read/query original owner')
            c=SimpleNamespace(pid=pid,h=h,owned=owned,get=lambda p,n:base.original.required(h,p,n))
            c.main=word(c.get(0x7A4A00,4));hwnd=base.original.findwindow(b'Cross Hermit',None);owner=W.DWORD()
            main_tid=base.original.ownerpid(hwnd,C.byref(owner));need(owner.value==pid,'current main window owner')
            kernel,_=__import__('devtools.terminal_wait_etw_probe',fromlist=['bind_windows']).bind_windows()
            ready={};node,tid=original.await_startup(c,main_tid,ready,kernel)
            window=WaitWindow(c,node,tid,main_tid,out.parent/out.name.removesuffix('.json.gz'),'startup_preflight',qualification)
            window.result['startup_readiness']=ready;window.begin();window.drain(.150)
        except Exception as exc:
            if window:window.result['error']=repr(exc)
            else:return dict(error=repr(exc))
        finally:
            if window:window.finish()
            if h:base.original.close(h)
        return window.result
    with guest_focus_scope(),DepObserver()as dep:
        result=clone(menu.run,continue_menu=observe)(out,30,None,False,0)
    obs=result.pop('probe')or dict(error='window callback not reached')
    result.update(obs,actual_process_dep_observations=dep.rows,dep_observer_error=dep.error)
    return result


def run(out,phase):
    from devtools.native_input_isolation import require_qualified_guest
    qualification=require_qualified_guest()
    out=Path(out).resolve()
    need(out.parent==ROOT/'analysis'and out.name.endswith('.json.gz')and not out.exists(),'fresh guest window output')
    need(phase=='startup_preflight','battle adapter must be separately reviewed before use')
    paths=[Path(__file__),ROOT/'devtools/terminal_original_wait_etw.py',ROOT/'devtools/terminal_wait_etw_probe.py']
    before=[identity(p)for p in paths]
    result=startup_probe(out,qualification)
    need(before==[identity(p)for p in paths],'executed window implementation unchanged')
    result['window_implementations']=before
    raw=json.dumps(result,separators=(',',':')).encode();need(len(raw)<=8*1024*1024,'bounded expanded window source')
    packed=gzip.compress(raw,mtime=0);need(len(packed)<=2*1024*1024,'bounded compressed window source')
    with out.open('xb')as f:f.write(packed)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--phase',choices=['startup_preflight'],default='startup_preflight')
    a=p.parse_args();r=run(a.out,a.phase)
    print(json.dumps(dict(error=r.get('error'),snapshots=len(r.get('window_snapshots',[])),ETL=r.get('ETL'),accepted=False)))
    raise SystemExit(1 if r.get('error')or r.get('lifecycle',{}).get('error')else 0)
