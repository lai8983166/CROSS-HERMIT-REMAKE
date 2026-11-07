"""Current startup retirement gate, independent of its animation/input trigger.

The existing animation-only observer remains frozen. This gate records the
trigger evidence separately and never upgrades sampled retirement to a complete
resource or instruction-trace proof.
"""
import ctypes as C
import ctypes.wintypes as W
import time
import traceback
from types import SimpleNamespace

from devtools import terminal_scene_owner as base
from devtools import terminal_startup_handoff as startup
from devtools.terminal_scene_resources import clone


def retired_menu(report,row):
    ex=report.get('worker_exit',{})
    if not (report.get('worker') and ex.get('wait_status')==0 and ex.get('exit_code')==0
            and ex.get('before_WM_CLOSE') is True and row.get('startup_thread_exited') is True):return False
    kinds=startup.classify(row['registered_tasks'])
    return bool(not kinds['startup'] and len(row['registered_tasks'])==1 and len(kinds['menu'])==1
                and base.word(bytes.fromhex(row['MAIN_event_hex']))==0)


def probe(pid,owned,progress,duration):
    import json
    report=dict(pid=pid,samples=[],error=None,host_original_calls=[],host_memory_writes=[],host_input_actions=[],
        gate_contract='original_startup_retired_v1',native_handoff_observed=False,
        natural_animation_limit_observed=False,original_mouse_press_sampled=False,
        retirement_trigger_proved=False,full_native_instruction_trace=False,normal_PTD_cleanup_proved=False,
        full_battle_exit_accepted=False)
    c=None;worker=None;node=tid=None
    try:
        base.need(pid in owned.members(),'owned private process')
        h=base.original.openp(0x100450,False,pid);base.original.check(h,'read-only current startup owner')
        c=SimpleNamespace(pid=pid,h=h,owned=owned,get=lambda p,n:base.original.required(h,p,n))
        c.main=base.word(c.get(0x7A4A00,4))
        base.need(c.main and base.word(c.get(c.main,4))==0x5986A0,'actual original MAIN')
        image=C.create_unicode_buffer(32768);size=W.DWORD(len(image))
        base.original.check(base.native.image_name(h,0,image,C.byref(size)),'actual private image')
        from pathlib import Path
        base.need(Path(image.value).resolve()==base.native.APP.resolve(),'exact original private image')
        hwnd=base.original.findwindow(b'Cross Hermit',None);wp=W.DWORD()
        main_tid=base.original.ownerpid(hwnd,C.byref(wp));base.need(wp.value==pid,'same own HWND')
        identity=clone(base.source_identity,RANGES=startup.RANGES,IAT=startup.IAT)
        report.update(main=c.main,process_image=image.value,process_access=0x100450,
            window=dict(hwnd=hwnd,pid=pid,main_tid=main_tid),source_before=identity(c),
            TLS_implementation=base.tls_contract(c))
        deadline=time.monotonic()+duration;last_saved=0;last_signature=None;menu_since=None
        while time.monotonic()<deadline:
            status=base.original.wait(worker,0) if worker else 258
            base.need(status in (0,258),'successful original thread status query')
            exited=status==0
            row=startup.sample(c,owned,main_tid,None if exited else tid,node)
            kinds=startup.classify(row['registered_tasks'])
            if not worker and kinds['startup']:
                head=bytes.fromhex(kinds['startup'][0]['head_hex'])
                if base.word(head,0x20) and base.word(head,0x24):
                    node=kinds['startup'][0]['pointer'];tid=base.word(head,0x24);worker=W.HANDLE()
                    base.original.check(base.parent.duplicate(h,base.word(head,0x20),base.parent.current_process(),
                        C.byref(worker),0,False,2),'retain current original startup thread')
                    base.need(base.get_thread_pid(worker)==pid and base.get_thread_id(worker)==tid,'same startup worker owner')
                    report['worker']=dict(node=node,thread_id=tid,remote_handle=base.word(head,0x20),
                        node_event=base.event_identity(c,base.word(head,0x1C)),
                        manager_event=base.event_identity(c,base.word(c.get(c.main+0x17C,4))))
            if exited and 'worker_exit' not in report:
                code=W.DWORD();base.original.check(base.parent.exit_thread(worker,C.byref(code)),'startup exit status')
                report['worker_exit']=dict(thread_id=tid,exit_code=code.value,wait_status=0,before_WM_CLOSE=True,
                    elapsed=owned.elapsed(),natural_return_full_trace_proved=False)
                base.need(code.value==0,'abnormal original startup exit')
            row['startup_thread_exited']=exited
            threshold=('startup_head_hex' in row and bytes.fromhex(row['startup_head_hex'])[0x30]==100
                       and row.get('callback_locals',{}).get('counter',0)>=16204)
            press=bool(kinds['startup'] and base.word(bytes.fromhex(row['mouse_hex']),0x24)&1)
            now=time.monotonic()
            signature=(tuple((r['pointer'],r['head_hex'][:8]) for r in row['registered_tasks']),
                       row['MAIN_event_hex'],exited,threshold,press)
            if signature!=last_signature or now-last_saved>=1:
                base.need(len(report['samples'])<1600,'bounded startup gate samples')
                row['index']=len(report['samples']);report['samples'].append(row)
                if threshold:report['natural_animation_limit_observed']=True
                if press:report['original_mouse_press_sampled']=True
                last_signature=signature;last_saved=now
                progress.write_text(json.dumps(dict(status='observing_original_startup_retirement',pid=pid,
                    elapsed=owned.elapsed(),counter=row.get('callback_locals',{}).get('counter'),
                    startup_registered=bool(kinds['startup']),menu_registered=bool(kinds['menu']),
                    worker_exited=exited,samples=len(report['samples']))),encoding='utf8')
            if retired_menu(report,row):
                if menu_since is None:menu_since=row['elapsed']
                if row['elapsed']-menu_since>=1:
                    if report['samples'][-1] is not row:
                        base.need(len(report['samples'])<1600,'bounded final startup sample')
                        row['index']=len(report['samples']);report['samples'].append(row)
                    report.update(native_handoff_observed=True,stop_reason='original_startup_exit0_and_menu_alone')
                    break
            else:menu_since=None
            time.sleep(.05)
        report.setdefault('stop_reason','bounded_deadline')
        report['source_after']=identity(c)
        base.need(report['source_before']==report['source_after'],'original startup source unchanged')
    except Exception as exc:report.update(error=repr(exc),error_traceback=traceback.format_exc(limit=6))
    finally:
        if worker:base.original.close(worker)
        if c:base.original.close(c.h)
    return report
