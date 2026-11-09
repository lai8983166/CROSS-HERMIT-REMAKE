"""Short original startup capability test for suspended worker retention."""
import argparse
import ctypes as C
import ctypes.wintypes as W
import gzip
import json
from pathlib import Path
from types import SimpleNamespace
import time
import traceback

from devtools import terminal_worker_retention_v3 as retention
from devtools import terminal_battle_wait_window as window
from devtools import terminal_factory_focus
from devtools.terminal_scene_resources import clone


def run(out):
    from devtools.native_input_isolation import require_qualified_guest
    qualification=require_qualified_guest()
    from devtools import terminal_menu_handoff as menu
    from devtools.isolated_guest_focus import guest_focus_scope
    from devtools.isolated_guest_dep_observer import DepObserver
    base=retention.base;need=base.need;out=Path(out).resolve()
    need(out.parent==window.ROOT/'analysis' and not out.exists(),'fresh bounded guest source')
    paths=[Path(__file__),Path(retention.__file__),Path(window.original.__file__),
           window.ROOT/'devtools/terminal_school_handoff.py',Path(retention.parent.__file__),
           Path(retention.parent.parent.__file__),Path(terminal_factory_focus.__file__)]
    before=[window.identity(p) for p in paths]
    def observe(pid,owned,progress,duration):
        h=None;tracker=None;r=dict(error=None,samples=[],accepted=False)
        try:
            h=base.original.openp(0x100450,False,pid);base.original.check(h,'read original owner')
            c=SimpleNamespace(pid=pid,h=h,owned=owned,get=lambda p,n:base.original.required(h,p,n))
            c.main=base.word(c.get(0x7A4A00,4))
            hwnd=base.original.findwindow(b'Cross Hermit',None);owner=W.DWORD()
            main_tid=base.original.ownerpid(hwnd,C.byref(owner));need(owner.value==pid,'current original window owner')
            kernel,_=__import__('devtools.terminal_wait_etw_probe',fromlist=['bind_windows']).bind_windows()
            ready={};window.original.await_startup(c,main_tid,ready,kernel)
            r['startup_readiness']=ready
            tracker=retention.WorkerRetention(c,main_tid)
            for _ in range(8):r['samples'].append(tracker.capture(owned));time.sleep(.01)
            r['workers']=tracker.workers
            need(tracker.workers and all(x['worker_retention']['retained_while_suspended'] for x in r['samples']),
                 'actual startup worker retained during bounded suspended observations')
            r['retention_capability_passed']=True
        except Exception as exc:r.update(error=repr(exc),traceback=traceback.format_exc(limit=8))
        finally:
            if tracker:
                if tracker.failure:r['worker_retention_failure']=tracker.failure
                try:r['observer_retention_cleanup']=tracker.close()
                except Exception as exc:r['error']=r.get('error')or repr(exc)
            if h:base.original.close(h)
        return r
    with guest_focus_scope(),DepObserver() as dep,terminal_factory_focus.scope()as factory:
        # Exercise the same focused runtime as the full collector. The custom
        # observe callback only reads eight startup samples: no controller input.
        result=clone(factory.menu_run,continue_menu=observe,OneMenuSelection=lambda *args:object())(out,30,0,True,192)
    result['factory_focus_observation']=factory.receipts
    activations=result.get('startup_activation',[])
    if len(activations)!=1 or 'error'in activations[0]or activations[0].get('guest_only')is not True:
        probe=result.get('probe')
        if probe is not None:
            probe['error']=probe.get('error')or 'actual qualified startup activation was not successfully observed'
            probe['retention_capability_passed']=False
    need(before==[window.identity(p) for p in paths],'retention collector unchanged during native probe')
    result.update(kind='worker_retention_startup_preflight',retention_implementations=before,
        input_isolation=qualification,actual_process_dep_observations=dep.rows,dep_observer_error=dep.error,
        accepted=False,full_resource_lifetime_proved=False,PTDcleanup=False)
    raw=json.dumps(result,separators=(',',':')).encode();need(len(raw)<=8*1024*1024,'bounded retention preflight')
    with out.open('xb') as f:f.write(gzip.compress(raw,mtime=0))
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True)
    r=run(p.parse_args().out);probe=r.get('probe')or{}
    print(json.dumps(dict(error=probe.get('error'),lifecycle_error=r['lifecycle'].get('error'),
        retention_capability_passed=probe.get('retention_capability_passed'),accepted=False)))
    raise SystemExit(0 if probe.get('retention_capability_passed') and not probe.get('error') and not r['lifecycle'].get('error') else 1)
