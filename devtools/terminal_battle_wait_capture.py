"""One legal school-to-battle source with a bounded separate wait-window source."""
import argparse
import ctypes as C
import ctypes.wintypes as W
import gzip
import hashlib
import json
from pathlib import Path
import time

from devtools.terminal_scene_resources import clone
from devtools import terminal_battle_wait_window_v2 as window

ROOT=Path(__file__).resolve().parents[1]
need=window.need


def canonical_identity(value):
    raw=json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
    return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
                encoding='UTF-8 JSON sort_keys=True,separators=(comma,colon),ensure_ascii=False')


def write_gzip(path,value,raw_limit,packed_limit):
    raw=json.dumps(value,separators=(',',':')).encode()
    need(len(raw)<=raw_limit,'bounded complete expanded source')
    packed=gzip.compress(raw,mtime=0);need(len(packed)<=packed_limit,'bounded complete compressed source')
    with path.open('xb')as f:f.write(packed)


def precise_submit_api(api,kernel,records):
    original=api.submit
    def submit(packet):
        need(len(records)<16,'bounded actual input submissions')
        row=dict(type=int(packet.type),flags=int(packet.data.mi.dwFlags),
            packet_hex=C.string_at(C.byref(packet),C.sizeof(packet)).hex(),
            begin_ns=window.original.utc_now_ns(kernel),result=None,error=None)
        records.append(row)
        try:
            row['result']=original(packet)
            return row['result']
        except Exception as exc:
            row['error']=repr(exc);raise
        finally:row['end_ns']=window.original.utc_now_ns(kernel)
    api.submit=submit
    return api


def run(out,seconds=1800):
    from devtools.native_input_isolation import require_qualified_guest
    qualification=require_qualified_guest()
    from devtools import terminal_school_handoff as school,terminal_battle_input as battle
    from devtools import terminal_scene_owner as base
    from devtools.terminal_worker_retention_v3 import continue_school
    from devtools.terminal_worker_retention import Proxy
    from devtools import terminal_factory_focus
    from devtools.terminal_input_window import observe as input_observe
    from devtools.isolated_guest_dep_observer import DepObserver
    out=Path(out).resolve();school_out=out.with_name(out.name.removesuffix('.json.gz')+'.school.json.gz')
    need(out.parent==ROOT/'analysis'and out.name.endswith('.json.gz')and not out.exists()
         and not school_out.exists()and 900<=seconds<=1800,'fresh bounded guest sources')
    paths=[Path(__file__),ROOT/'devtools/terminal_battle_wait_window.py',
        ROOT/'devtools/terminal_battle_wait_window_v2.py',
        ROOT/'devtools/terminal_original_wait_etw.py',ROOT/'devtools/terminal_wait_etw_probe.py',
        ROOT/'devtools/terminal_school_handoff.py',ROOT/'devtools/terminal_input_window.py',
        ROOT/'devtools/terminal_battle_input.py',ROOT/'devtools/terminal_owned_mouse.py',
        ROOT/'devtools/terminal_worker_retention.py',ROOT/'devtools/terminal_worker_retention_v2.py',
        ROOT/'devtools/terminal_worker_retention_v3.py',ROOT/'devtools/terminal_factory_focus.py']
    before=[window.identity(p)for p in paths];windows=[]

    class Confirmation(school.OwnedAction):
        def observe(self,c,owned,row):
            if (self.attempted or not self.ready(row) or self.since is None
                    or time.monotonic()-self.since<1):
                return super().observe(c,owned,row)
            need(not windows,'exactly one confirmation window; never retry a click')
            task=row['tasks'][0];hwnd=base.original.findwindow(b'Cross Hermit',None);pid=W.DWORD()
            main_tid=base.original.ownerpid(hwnd,C.byref(pid));need(pid.value==c.pid,'current original HWND owner')
            observer=window.WaitWindow(c,task['pointer'],task['thread_id'],main_tid,
                out.parent/out.name.removesuffix('.json.gz'),'battle_retreat',qualification)
            windows.append(observer)
            observer.prepare()
            observer.result['precise_input_submissions']=[]
            def start():
                observer.result['start_trigger']='second_left_button_down_query'
                observer.result['start_trigger_ns']=window.original.utc_now_ns(observer.kernel)
                observer.begin()
            def make_api(c,hwnd,game):
                api=precise_submit_api(battle.make_api(c,hwnd,game),observer.kernel,
                    observer.result['precise_input_submissions'])
                return window.wrap_click_api(api,start)
            action=clone(battle.action,make_api=make_api)
            self.send=lambda c,h:action(c,h,'confirmation',explicit_user_override=True)
            def observe_inputs(worker,capture,record,**kwargs):
                def sample():
                    value=capture();observer.poll();return value
                observer.result['input_observation_begin_ns']=window.original.utc_now_ns(observer.kernel)
                try:return input_observe(worker,sample,record,**kwargs)
                finally:observer.result['input_observation_end_ns']=window.original.utc_now_ns(observer.kernel)
            try:
                with observer.synchronized_input_snapshots():
                    clone(school.OwnedAction.observe,observe_input_window=observe_inputs)(self,c,owned,row)
                    need(observer.active,'trace started before the real confirmation down')
                    observer.drain()
            except Exception as exc:
                observer.result['error']=repr(exc);raise
            finally:observer.finish()

    class Controller(school.SchoolController):
        def __init__(self,*args):
            super().__init__(*args)
            old=self.battle[1]
            self.battle[1]=Confirmation(old.name,old.ready,old.send,post_release_snapshots=True)

    with DepObserver()as dep,terminal_factory_focus.scope()as factory:
        menu=Proxy(school.menu,run=factory.menu_run)
        report=clone(school.run,menu=menu,SchoolController=Controller,continue_school=continue_school)(school_out,seconds)
    report['factory_focus_observation']=factory.receipts
    need(before==[window.identity(p)for p in paths],'whole actual collector/adapter source identity')
    report['window_observer_implementations']=before
    report['worker_retention_version']=3
    report['worker_retention_implementation']=window.identity(ROOT/'devtools/terminal_worker_retention_v3.py')
    report['worker_retention_parent_implementation']=window.identity(ROOT/'devtools/terminal_worker_retention_v2.py')
    report['worker_retention_grandparent_implementation']=window.identity(ROOT/'devtools/terminal_worker_retention.py')
    report['collector_globals_adapted']=True
    report['frozen_school_source_bytes_modified']=False
    report['actual_process_dep_observations']=dep.rows;report['dep_observer_error']=dep.error
    # Full legal-input history is kept once and SHA-referenced by the small window.
    write_gzip(school_out,report,192*1024*1024,24*1024*1024)
    result=windows[0].result if windows else dict(kind='battle_wait_result_window',phase='battle_retreat',
        error='legal confirmation never reached; no trace or click fabricated',accepted=False)
    result['school_source_reference']=window.identity(school_out)
    result['window_implementations']=before
    for key in ('lifecycle','mutable_private_runtime_files','input_isolation'):
        result[key]=report[key]
    result['school_probe_error']=(report.get('probe')or{}).get('error')
    result['school_stop_reason']=(report.get('probe')or{}).get('stop_reason')
    actions=(report.get('probe')or{}).get('battle_inputs',[])
    confirmations=[(i,x)for i,x in enumerate(actions)if x['stage']=='confirmation']
    if len(confirmations)==1:
        index,record=confirmations[0]
        result['input_receipt']=dict(source=window.identity(school_out),
            object_path=['probe','battle_inputs',index],canonical=canonical_identity(record),
            down_wall_time_ns=record.get('action',{}).get('down_wall_time_ns'),
            up_wall_time_ns=record.get('action',{}).get('up_wall_time_ns'),
            released=record.get('action',{}).get('released'),error=record.get('error'))
    write_gzip(out,result,8*1024*1024,2*1024*1024)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--seconds',type=int,default=1800);p.add_argument('--phase',choices=['battle_retreat'],default='battle_retreat')
    a=p.parse_args();r=run(a.out,a.seconds)
    print(json.dumps(dict(error=r.get('error'),school_probe_error=r.get('school_probe_error'),
        stop_reason=r.get('stop_reason'),school_stop_reason=r.get('school_stop_reason'),
        snapshots=len(r.get('window_snapshots',[])),ETL=r.get('ETL'),accepted=False)))
    raise SystemExit(1 if r.get('error')or r.get('school_probe_error')or r.get('lifecycle',{}).get('error')else 0)
