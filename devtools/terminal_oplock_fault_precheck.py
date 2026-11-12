"""Three bounded owned-file fault cases; no game, UI or target writes."""
import argparse
import json
from pathlib import Path
import time
from unittest.mock import patch
from devtools import terminal_oplock_probe_v2 as probe
from devtools.terminal_oplock import ReadOplock, PENDING_OWNERS, need
from devtools.terminal_host_desktop import snapshot, differences, health


def execute(folder,exe):
    folder=folder.resolve();exe=exe.resolve()
    need(folder.is_relative_to(probe.ROOT/'.venv-audit') and not folder.exists(),'fresh local fault evidence')
    need(exe.is_relative_to(probe.ROOT/'.venv-audit'),'existing owned helper only')
    folder.mkdir();r=dict(kind='RW_oplock_fault_precheck',error=None,cases=[],game_started=False,accepted=False,
        sources=[probe.identity(probe.ROOT/p) for p in probe.DEPS]+[probe.identity(__file__)],binary=probe.identity(exe))
    r['before']=snapshot()
    try:
        need(not health(r['before']),'healthy desktop before no-UI cases')
        for name,watchdog in (('no_opener_cancel',False),('watchdog_close',True)):
            p=folder/(name+'.bin');p.write_bytes(probe.PAYLOAD);row=dict(name=name,before=probe.identity(p))
            lock=ReadOplock(p,.2 if watchdog else 2)
            try:
                if watchdog:need(lock.w.wait(lock.event,1000)==0,'watchdog completed request')
                else:need(not lock.observe_break(50),'no fabricated event without opener')
            finally:row['oplock']=lock.finish()
            need(row['oplock']['file_closed'] and row['oplock']['async_completed'] and row['oplock']['event_closed']
                 and row['oplock']['watchdog_release'] is watchdog,'fault file/event cleanup')
            row['after']=probe.identity(p);need(row['before']==row['after'],'fault payload unchanged');r['cases'].append(row)
        def failed_observer(*args):raise RuntimeError('injected owned observer failure after real break')
        with patch.object(probe,'capture',failed_observer):
            case=probe.run_case(exe,folder/'capture_failure',True)
        r['cases'].append(dict(name='capture_failure',result=case))
        need('injected owned observer failure' in case['error'] and not case.get('oplock_cleanup_error')
             and not case['read_handle_cleanup_errors'] and case['owner']['job_empty']
             and case['owner']['handles_closed'] and not case['owner']['errors']
             and all(e['wait']==0 for e in case['owner']['exits'].values())
             and case['input']==case['input_after'],'injected observation failure fully contained')
    except BaseException as exc:r['error']=repr(exc)
    finally:
        r['after']=[snapshot()];time.sleep(1);r['after'].append(snapshot())
        r['desktop_checks']=[differences(r['before'],s) for s in r['after']]
        if PENDING_OWNERS:r['error']=r['error'] or 'pending async owners require process containment'
        r['sources_unchanged']=r['sources']==[probe.identity(probe.ROOT/p) for p in probe.DEPS]+[probe.identity(__file__)]
        if r['desktop_checks']!=[[],[]] or not r['sources_unchanged']:r['error']=r['error'] or 'desktop/source mismatch'
        with (folder/'report.json').open('x',encoding='utf-8') as f:json.dump(r,f,indent=2)
    return r


if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--folder',type=Path,required=True);a.add_argument('--exe',type=Path,required=True);args=a.parse_args()
    try:
        r=execute(args.folder,args.exe);print(json.dumps(dict(error=r['error'],desktop_checks=r['desktop_checks'])))
        need(r['error'] is None,'fault qualification rejected')
    finally:
        if PENDING_OWNERS:
            import os,sys
            try:sys.stdout.flush();sys.stderr.flush()
            finally:os._exit(6)
