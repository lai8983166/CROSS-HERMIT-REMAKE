"""Retain real worker owners inside the same verified suspended observation.

Registered graph nodes can precede native thread construction. Such raw nodes
remain in the source; absence of callback ancestry is not resource acceptance.
"""
from contextlib import ExitStack, contextmanager
import ctypes as C
import ctypes.wintypes as W
import time

from devtools import terminal_school_handoff as school
from devtools import terminal_original_wait_etw as original_wait
from devtools.terminal_scene_resources import clone

base=school.base
need=base.need
word=base.word


class Proxy:
    def __init__(self, target, **overrides):
        self.target=target;self.overrides=overrides
    def __getattr__(self, key):
        return self.overrides[key] if key in self.overrides else getattr(self.target,key)


@contextmanager
def owned_cohort(c, main_tid, backend=base):
    """Same-handle identity before every suspend; restore only our increments."""
    with ExitStack() as stack:
        frames=list(stack.enter_context(original_wait.owned_frames(c,[main_tid],backend)))
        tids=backend.original.threads(c.pid)
        need(main_tid in tids and len(tids)==len(set(tids)) and len(tids)<=256,
             'bounded unique current game cohort includes main')
        for tid in tids:
            if tid!=main_tid:
                frames.extend(stack.enter_context(original_wait.owned_frames(c,[tid],backend)))
        need(set(backend.original.threads(c.pid))==set(tids),'no thread appeared during cohort suspension')
        yield frames


class WorkerRetention:
    def __init__(self,c,main_tid,backend=base,cohort=owned_cohort,snapshot=school.snapshot):
        self.c=c;self.main_tid=main_tid;self.backend=backend;self.cohort=cohort;self.snapshot=snapshot
        self.handles={};self.workers=[];self.failure=None;self.closed=[]

    def retain(self,row):
        """Called only within capture's held cohort; preserve the first failing row."""
        c=self.c;b=self.backend;receipt=row['worker_retention'];call=None
        try:
            for task in row['tasks']:
                head=bytes.fromhex(task['header_hex']);tid=word(head,0x24)
                need(tid==task['thread_id'],'raw header worker ID')
                key=(task['pointer'],tid);remote=word(head,0x20);event=word(head,0x1C)
                frame=next((f for f in row['frames'] if f['tid']==tid),None)
                ancestors={x['return_va'] for x in frame['chain']} if frame else set()
                proof=dict(pointer=key[0],thread_id=tid,remote_handle=remote,event=event,
                    observed_context_present=frame is not None,status=None)
                receipt['tasks'].append(proof)
                if key in self.handles:
                    previous=next(w for w in self.workers if (w['pointer'],w['thread_id'])==key)
                    need((previous['original_handle'],previous['event']['remote_handle'],previous['vtable'])==
                         (remote,event,task['vtable']),'retained live graph owner remains exact')
                    proof['status']='already_retained';continue
                callback={0x421F8A,0x56E183}
                if not callback<=ancestors:
                    need(not callback&ancestors and 'TLS' not in task,
                         'partial original callback ancestry must not become pending')
                    proof['status']='pending_callback_ancestry'
                    continue
                need(remote and tid and 'TLS' in task,'original callback requires actual native handle and TLS')
                handle=W.HANDLE()
                call=dict(api='DuplicateHandle',pid=c.pid,pointer=key[0],thread_id=tid,
                          remote_handle=remote,event=event,options=2,desired_access=0,inherit=False)
                b.original.check(b.parent.duplicate(c.h,remote,b.parent.current_process(),
                    C.byref(handle),0,False,2),'retain same suspended original worker')
                try:
                    need(b.get_thread_pid(handle)==c.pid and b.get_thread_id(handle)==tid,
                         'duplicate belongs to exact original worker')
                    call=dict(api='event_identity',pid=c.pid,pointer=key[0],thread_id=tid,remote_handle=event)
                    identity=b.event_identity(c,event)
                except BaseException:
                    b.original.check(b.original.close(handle),'close failed observer retention');raise
                self.handles[key]=handle
                self.workers.append(dict(pointer=key[0],thread_id=tid,vtable=task['vtable'],
                    original_handle=remote,event=identity,first_elapsed=row['elapsed']))
                proof['status']='retained'
        except BaseException as exc:
            if self.failure is None:self.failure=dict(error=repr(exc),call=call,row=row)
            raise

    def capture(self,owned):
        begin=time.perf_counter_ns()
        with self.cohort(self.c,self.main_tid,self.backend) as frames:
            @contextmanager
            def held(h,pid):
                need(h==self.c.h and pid==self.c.pid,'same already suspended owner')
                yield frames
            proxy=Proxy(self.backend,original=Proxy(self.backend.original,frozen=held))
            row=clone(self.snapshot,base=proxy)(self.c,owned)
            row['worker_retention']=dict(version=1,pid=self.c.pid,main_tid=self.main_tid,
                capture_begin_perf_ns=begin,cohort_tids=[f['tid'] for f in frames],
                retained_while_suspended=True,tasks=[])
            self.retain(row)
            row['worker_retention']['capture_end_perf_ns']=time.perf_counter_ns()
        return row

    def close(self):
        failures=[]
        for key,handle in self.handles.items():
            if key in self.closed:continue
            if self.backend.original.close(handle):self.closed.append(key)
            else:failures.append(key)
        need(not failures,'observer duplicate close failure')
        return dict(closed_observer_handles=len(self.closed),original_resource_cleanup_proved=False)


# The continuation preserves the frozen controller, phase budgets and exit gates.
# Only snapshot/retention ownership changes; the original file stays immutable.
from pathlib import Path
from types import SimpleNamespace
import json
import traceback
startup_gate=school.startup_gate
startup=school.startup
battle=school.battle
progress_signature=school.progress_signature
RANGES=school.RANGES
CATALOG=None
CONTROLLER=None


def continue_school(pid,owned,progress,duration):
    report=dict(pid=pid,error=None,samples=[],workers=[],host_game_calls=[],host_memory_writes=[],
        collector_input_actions=[],full_battle_exit_accepted=False,full_native_instruction_trace=False)
    c=None;tracker=None;handles={};started=time.monotonic()
    try:
        # Reuse the immutable observer as a current native phase, never its old handles.
        report['startup']=startup_gate.probe(pid,owned,progress,min(duration-30,720))
        need(report['startup']['error'] is None and report['startup']['native_handoff_observed'],
             'current native startup must retire before menu continuation')
        h=base.original.openp(0x100450,False,pid)
        base.original.check(h,'read-only current menu owner')
        c=SimpleNamespace(h=h,pid=pid,owned=owned,get=lambda p,n:base.original.required(h,p,n))
        c.main=word(c.get(0x7A4A00,4));c.catalog=CATALOG;report['main']=c.main
        identity=clone(base.source_identity,RANGES=RANGES,IAT=startup.IAT)
        report['source_before']=identity(c)
        report['TLS_implementation']=base.tls_contract(c)
        report['manager_event']=base.event_identity(c,word(c.get(c.main+0x17C,4)))
        tracker=WorkerRetention(c,report['startup']['window']['main_tid'])
        handles=tracker.handles;report['workers']=tracker.workers
        deadline=min(started+duration,time.monotonic()+1500);last_signature=None;last_saved=0
        last_progress=time.monotonic();menu_since=None
        stop=Path(str(progress).removesuffix('.progress.json')+'.stop.json')
        while time.monotonic()<deadline:
            row=tracker.capture(owned)
            for worker in report['workers']:
                if 'exit' in worker:continue
                handle=handles[(worker['pointer'],worker['thread_id'])]
                status=base.original.wait(handle,0)
                need(status in (0,258),'successful zero-time worker status query')
                if status==0:
                    code=W.DWORD();base.original.check(base.parent.exit_thread(handle,C.byref(code)),'original worker exit')
                    worker['exit']=dict(code=code.value,wait_status=status,elapsed=owned.elapsed(),before_WM_CLOSE=True)
                    need(code.value==0,'abnormal original worker termination')
            signature=progress_signature(row,CONTROLLER)
            now=time.monotonic()
            if signature!=last_signature:last_progress=now
            if signature!=last_signature or now-last_saved>=1:
                need(len(report['samples'])<5000,'bounded menu snapshot retention')
                row['index']=len(report['samples']);report['samples'].append(row)
                last_saved=now;last_signature=signature
                progress.write_text(json.dumps(dict(status='observing_school_battle_continuation',pid=pid,
                    elapsed=owned.elapsed(),samples=len(report['samples']),
                    tasks=[dict(pointer=t['pointer'],vtable=hex(t['vtable'])) for t in row['tasks']],
                    VM_PC=word(bytes.fromhex(row['VM_hex']),28),
                    mouse_hex=row['mouse_hex'],host_game_calls=0,
                    collector_input_actions=CONTROLLER.count(),
                    phase_story_counts=[len(s.actions)for s in CONTROLLER.story_phases],
                    pending_control=next((a.name for a in [CONTROLLER.workroom,*CONTROLLER.school,*CONTROLLER.battle]if not a.attempted),None))),encoding='utf8')
            if stop.exists():
                raw=stop.read_bytes();need(len(raw)<=1024 and json.loads(raw)=={'stop':True},'explicit observation stop only')
                report['stop_reason']='controller_finished_observation';break
            CONTROLLER.observe(c,owned,row)
            if CONTROLLER.stop_reason:
                report['stop_reason']=CONTROLLER.stop_reason;report['dependency_sample']=row;break
            battle_workers=[w for w in report['workers']if w['vtable']==battle.BATTLE]
            if (CONTROLLER.battle_seen and battle_workers and all(w.get('exit',{}).get('code')==0 for w in battle_workers)
                    and len(row['tasks'])==1 and row['tasks'][0]['vtable']==startup.MENU):
                if menu_since is None:menu_since=now
                if now-menu_since>=2:
                    report['stop_reason']='battle_worker_exit_and_menu_observed';break
            else:menu_since=None
            if CONTROLLER.title.done and now-last_progress>=60:
                report['stop_reason']='stable_unhandled_native_wait';report['dependency_sample']=row;break
            time.sleep(.005 if CONTROLLER.battle[1].attempted else .05)
        report.setdefault('stop_reason','bounded_school_battle_deadline')
        report['source_after']=identity(c)
        need(report['source_before']==report['source_after'],'original menu code unchanged')
    except Exception as exc:
        report.update(error=repr(exc),traceback=traceback.format_exc(limit=8))
    finally:
        if CONTROLLER is not None:report.update(CONTROLLER.reports())
        if tracker:
            if tracker.failure:report['worker_retention_failure']=tracker.failure
            try:report['observer_retention_cleanup']=tracker.close()
            except Exception as exc:report['error']=report.get('error')or repr(exc)
        if c:base.original.close(c.h)
    return report

