"""Bounded startup observation without posting a competing scene event.

Used to discover a real native handoff before enabling the scene probe. No
original functions are called and no input is injected by this observer.
"""
import argparse
import ctypes as C
import ctypes.wintypes as W
import gzip
import json
from pathlib import Path
import time

from devtools import terminal_scene_owner as base
from devtools.terminal_scene_resources import clone, make_sampler, RESOURCE_RANGES


def probe(pid,owned,progress,duration):
    result=dict(pid=pid,samples=[],error=None,original_functions_called=False)
    c=None
    try:
        c=base.Calls(pid,owned,4)
        hwnd=base.original.findwindow(b'Cross Hermit',None);wp=W.DWORD()
        main_tid=base.original.ownerpid(hwnd,C.byref(wp))
        base.need(wp.value==pid,'same exclusively owned window')
        result.update(main=c.main,window=dict(hwnd=hwnd,pid=pid,main_tid=main_tid))
        identity=clone(base.source_identity,RANGES=base.RANGES+RESOURCE_RANGES)
        sampler=make_sampler(base.bounded_sample,base.original,{},identity)
        result['source_before']=identity(c)
        deadline=time.monotonic()+duration;last=None;saved=0
        while time.monotonic()<deadline:
            s=sampler(c,owned,hwnd,main_tid,None,None,False)
            sig=[(r['pointer'],r['head_hex'][:8]) for r in s['registered_tasks']]
            if sig!=last or time.monotonic()-saved>.5:
                s['index']=len(result['samples']);result['samples'].append(s)
                last=sig;saved=time.monotonic()
                progress.write_text(json.dumps(dict(status='startup_observation',pid=pid,hwnd=hwnd,
                    elapsed=owned.elapsed(),tasks=sig,scene_event_posted=False)),encoding='utf8')
            time.sleep(.02)
        result['source_after']=identity(c)
        base.need(result['source_before']==result['source_after'],'unchanged original code')
    except Exception as exc:result['error']=repr(exc)
    finally:
        if c:
            result['calls']=c.calls;result['private_writes']=c.writes
            result['private_frees']=c.close()
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--seconds',type=int,default=90);args=p.parse_args();out=args.out.resolve()
    base.need(out.is_relative_to(base.ROOT/'analysis') and not out.exists(),'fresh bounded output')
    base.need(15<=args.seconds<=120,'bounded startup observation')
    before=base.identity(Path(__file__))
    result=clone(base.run,run_probe=probe)(out,args.seconds)
    base.need(before==base.identity(Path(__file__)),'startup collector unchanged')
    result.update(kind='native_startup_handoff_diagnostic',startup_observer=before,
                  original_scene_event_posted=False,full_battle_exit_accepted=False)
    raw=json.dumps(result,separators=(',',':')).encode();base.need(len(raw)<16*1024*1024,'bounded report')
    packed=gzip.compress(raw,mtime=0)
    with out.open('xb') as stream:stream.write(packed)
    print(json.dumps(dict(report=base.identity(out),error=(result.get('probe') or {}).get('error'),
                         lifecycle_error=result['lifecycle']['error'])),flush=True)
    if not result.get('probe') or result['probe']['error'] or result['lifecycle']['error']:raise SystemExit(1)


if __name__=='__main__':main()
