"""Owned, bounded original title/workroom/school/battle UI continuation.

No game roots or game memory writes. All input guards and phase budgets are
frozen before launch. Native observations are not full instruction replay.
"""
import argparse
from contextlib import contextmanager
import ctypes as C
import ctypes.wintypes as W
import gzip
import json
from pathlib import Path
import struct
import threading
import time
import traceback
from types import SimpleNamespace

from devtools import terminal_menu_handoff as menu
from devtools import terminal_scene_owner as base
from devtools import terminal_startup_handoff as startup
from devtools import terminal_menu_startup as startup_gate
from devtools import terminal_story_input as story
from devtools import terminal_workroom_input as workroom
from devtools import terminal_school_input as school
from devtools import terminal_battle_input as battle
from devtools import terminal_battle_notice as notice
from devtools.terminal_scene_resources import clone
from devtools.terminal_story_catalog import Catalog
from devtools.native_input_isolation import require_qualified_guest
from devtools.isolated_guest_focus import guest_focus_scope, focus_owned_window as guest_focus
from devtools.terminal_input_window import observe as observe_input_window

ROOT=base.ROOT
need=base.need
word=base.word
RANGES=tuple(dict.fromkeys(menu.RANGES+workroom.INPUT_RANGES+school.INPUT_RANGES+battle.INPUT_RANGES+notice.INPUT_RANGES))
AUTHORIZATION=ROOT/'analysis/terminal-school-input-authorization-v2-20261109.json'
CONTROLLER=None
CATALOG=None


@contextmanager
def school_focus_scope():
    # The frozen story module holds this imported alias. Scope both references
    # to the same recorded guest implementation, restoring them on every exit.
    previous = story.keyboard.focus_owned_window
    with guest_focus_scope():
        story.keyboard.focus_owned_window = guest_focus
        try:
            yield
        finally:
            story.keyboard.focus_owned_window = previous


class OwnedAction:
    def __init__(self,name,ready,send,post_release_snapshots=False):
        self.name=name;self.ready=ready;self.send=send;self.attempted=False;self.receipt=None;self.start=None;self.since=None
        self.post_release_snapshots=post_release_snapshots

    def observe(self,c,owned,row):
        if self.attempted:return
        if not self.ready(row):self.start=None;self.since=None;return
        now=time.monotonic()
        if self.since is None:self.since=now;self.start=row;return
        if now-self.since<1:return
        self.attempted=True
        record=dict(stage=self.name,before_sample=row,ready_start_sample=self.start,ready_decision_sample=row,
                    before_elapsed=owned.elapsed(),input_samples=[],post_release_snapshots=[],error=None)
        self.receipt=record;thread=None;outcome={}
        try:
            hwnd=base.original.findwindow(b'Cross Hermit',None)
            record['activation']=story.keyboard.focus_owned_window(c,hwnd)
            game=word(c.get(0x7A49FC,4));foreground=base.original.ubind('GetForegroundWindow',W.HWND,[])
            def sample():
                result=dict(elapsed=owned.elapsed(),wall_time_ns=time.time_ns(),
                    foreground_hwnd=foreground()or 0,mouse_hex=c.get(game+0x196C,0x58).hex(),
                    MAIN_event_hex=c.get(c.main+0x2C,8).hex(),VM_hex=c.get(base.native.VM,128).hex())
                if self.name=='opening_notice':
                    pointer=row['tasks'][0]['pointer']
                    result['notice_state_hex']=c.get(pointer+0x190+0x30998,0x14).hex()
                    result['battle_head_tail_hex']=c.get(pointer+0x43,0x1D).hex()
                return result
            def send():
                try:outcome['action']=self.send(c,hwnd)
                except BaseException as exc:outcome['error']=repr(exc)
            record['input_samples'].append(sample())
            thread=threading.Thread(target=send,name='owned-'+self.name,daemon=False);thread.start()
            def after_finished():
                if self.post_release_snapshots and len(record['post_release_snapshots'])<128:
                    record['post_release_snapshots'].append(snapshot(c,owned))
            observe_input_window(thread,sample,record,after_finished=after_finished)
            thread.join(timeout=6);need(not thread.is_alive(),'bounded reviewed mouse action completed')
            record.update(outcome)
            need('action'in record and record['action']['error']is None and record['action']['released'],
                 'one reviewed mouse action submitted and released without retry')
        except Exception as exc:record['error']=repr(exc);raise
        finally:
            if thread and thread.is_alive():thread.join(timeout=6)
            record['after_elapsed']=owned.elapsed()


class BattleConfirm(story.StoryConfirm):
    # Exact original confirmation implementation, a separately declared owner.
    observe=clone(story.StoryConfirm.observe,
                  confirmation_key=clone(story.confirmation_key,ADV=battle.BATTLE))


class TitleSelection(menu.OneMenuSelection):
    def observe(self,c,owned,row):
        if self.done:
            if self.story:self.story.observe(c,owned,row)
            return
        tasks=row['tasks']
        ready=(len(tasks)==1 and tasks[0]['vtable']==startup.MENU
               and word(bytes.fromhex(tasks[0]['header_hex']),0x30)==1
               and word(bytes.fromhex(row['MAIN_event_hex']))==0)
        frame=next((f for f in row['frames'] if ready and f['tid']==tasks[0]['thread_id']),None)
        ready=bool(ready and frame and any(f['return_va']==0x45F065 for f in frame['chain']))
        now=time.monotonic()
        if not ready:self.since=None;self.ready_start=None;return
        if self.since is None:self.since=now;self.ready_start=row;return
        if now-self.since<1:return
        from devtools.terminal_owned_mouse import owned_main_menu_click
        from tools.school_native_dialogue_input import focus_owned_window
        hwnd=base.original.findwindow(b'Cross Hermit',None)
        self.done=True  # Never retry a potentially delivered click.
        self.receipt=dict(index=self.index,before_elapsed=owned.elapsed(),error=None,
            ready_start_sample=self.ready_start,ready_decision_sample=row)
        try:
            self.receipt['activation']=focus_owned_window(c,hwnd)
            game=word(c.get(0x7A49FC,4));outcome={}
            self.receipt['input_samples']=[]
            def observe_input():
                return dict(elapsed=owned.elapsed(),wall_time_ns=time.time_ns(),
                    mouse_hex=c.get(game+0x196C,0x58).hex(),MAIN_event_hex=c.get(c.main+0x2C,8).hex())
            def send():
                try:outcome['action']=owned_main_menu_click(c,hwnd,self.index,explicit_user_override=True)
                except BaseException as exc:outcome['error']=repr(exc)
            self.receipt['input_samples'].append(observe_input())
            worker=threading.Thread(target=send,name='owned-menu-input',daemon=False)
            worker.start()
            try:
                observe_input_window(worker,observe_input,self.receipt)
            finally:worker.join(timeout=6)
            need(not worker.is_alive(),'bounded mouse input finished and release attempted')
            self.receipt.update(outcome)
            need('action' in self.receipt,'mouse backend returned a complete receipt')
            need(self.receipt['action']['error'] is None and self.receipt['action']['released'],
                 'single bounded original menu click completed')
        except Exception as exc:
            self.receipt['error']=repr(exc);raise
        finally:self.receipt['after_elapsed']=owned.elapsed()


class SchoolController:
    def __init__(self,index,authorized,story_limit=192):
        need(index==0 and authorized is True and story_limit==192,'declared new-game school continuation')
        self.title=TitleSelection(0,True,0)
        self.story_phases=[story.StoryConfirm(192),story.StoryConfirm(192),BattleConfirm(64)]
        self.workroom=OwnedAction('workroom_exit',workroom.ready,
            lambda c,h:workroom.owned_workroom_exit(c,h,explicit_user_override=True))
        self.school=[OwnedAction(stage,lambda r,s=stage:school.ready(r,s),
            lambda c,h,s=stage:school.action(c,h,s,explicit_user_override=True))for stage in ('departure','confirmation')]
        self.battle=[OwnedAction(stage,lambda r,s=stage:battle.ready(r,s),
            lambda c,h,s=stage:battle.action(c,h,s,explicit_user_override=True),
            post_release_snapshots=(stage=='confirmation'))for stage in ('request','confirmation')]
        self.notice=OwnedAction('opening_notice',lambda r:notice.ready(r,'opening_notice'),
            lambda c,h:notice.action(c,h,'opening_notice',explicit_user_override=True))
        self.stop_reason=None;self.battle_seen=False

    def observe(self,c,owned,row):
        if not self.title.done:self.title.observe(c,owned,row);return
        kinds={t['vtable']for t in row['tasks']}
        if kinds=={workroom.WORKROOM}:
            self.workroom.observe(c,owned,row);return
        if school.GROUP in kinds:
            need(self.workroom.attempted,'school input follows the declared workroom exit')
            action=self.school[0]if not self.school[0].attempted else self.school[1]
            action.observe(c,owned,row);return
        phase=None
        if kinds=={story.ADV}:phase=1 if self.workroom.attempted else 0
        elif kinds=={battle.BATTLE}:
            need(all(a.attempted for a in self.school),'battle input follows both original school controls')
            self.battle_seen=True
            if not self.notice.attempted and notice.ready(row,'opening_notice'):
                self.notice.observe(c,owned,row);return
            if self.battle[0].attempted:self.battle[1].observe(c,owned,row);return
            if battle.ready(row,'request'):
                need(self.notice.attempted,'declared opening notice precedes retreat')
                self.battle[0].observe(c,owned,row);return
            head=bytes.fromhex(row['tasks'][0]['scene_head_hex'])
            if head[0x43] and head[0x59]:phase=2
        if phase is None:return
        key=clone(story.confirmation_key,ADV=battle.BATTLE)(row)if phase==2 else story.confirmation_key(row)
        if key is not None:
            need(row.get('program_code',{}).get('matched')is True,'current original script bytes match fixed asset catalog')
        self.story_phases[phase].observe(c,owned,row)
        if self.story_phases[phase].budget_exhausted:self.stop_reason='story_phase_budget_'+str(phase)

    def count(self):
        return int(self.title.done)+sum(len(s.actions)for s in self.story_phases)+sum(
            int(a.attempted)for a in [self.workroom,*self.school,self.notice,*self.battle])

    def reports(self):
        return dict(collector_input_actions=[self.title.receipt]if self.title.receipt else [],
            collector_input_actions_scope='title_menu_only',
            mouse_controller=dict(attempted=self.title.done,receipt=self.title.receipt,user_override_required=True,maximum_clicks=1),
            story_phases=[dict(name=name,maximum=s.maximum,actions=s.actions,budget_exhausted=s.budget_exhausted)
                          for name,s in zip(('opening_ADV','after_workroom_ADV','battle_dialogue'),self.story_phases)],
            workroom_inputs=[self.workroom.receipt]if self.workroom.receipt else [],
            school_inputs=[a.receipt for a in self.school if a.receipt],
            battle_inputs=[a.receipt for a in self.battle if a.receipt],
            notice_inputs=[self.notice.receipt]if self.notice.receipt else [],
            maximum_mouse_actions=7,maximum_story_actions=448)


def progress_signature(row,controller):
    waits={0x49FF57,0x4A7CEA,0x453CB5,0x453CD3,0x453CDD,0x451758,0x451796}
    return (tuple((t['pointer'],t['vtable'],t['thread_id'],t['header_hex'][96:128])for t in row['tasks']),
        row['MAIN_event_hex'],row['VM_hex'][32:76],controller.count(),
        tuple((f['tid'],tuple(x['return_va']for x in f['chain']if x['return_va']in waits))for f in row['frames']),
        tuple(n['control_hex']for n in row.get('school',{}).get('nodes',[])))


def snapshot(c,owned):
    with base.original.frozen(c.h,c.pid) as frames:
        manager,rows=startup.graph(c)
        game=word(c.get(0x7A49FC,4))
        row=dict(elapsed=owned.elapsed(),frames=frames,manager_hex=manager.hex(),
            registered_tasks=rows,MAIN_event_hex=c.get(c.main+0x2C,8).hex(),game=game,
            keyboard_hex=c.get(game+0x10B8,0xA00).hex(),mouse_hex=c.get(game+0x196C,0x58).hex(),
            scenario_hex=c.get(0x7F4488,80).hex(),VM_hex=c.get(base.native.VM,128).hex(),
            scene_global=word(c.get(0x7A4174,4)),group90_hex=c.get(game+0xB14,8).hex(),
            tasks=[])
        for node in rows:
            head=bytes.fromhex(node['head_hex']);pointer=node['pointer'];vt=word(head)
            task=dict(pointer=pointer,vtable=vt,vtable_hex=c.get(vt,8).hex(),
                      header_hex=c.get(pointer,64).hex(),thread_id=word(head,0x24))
            frame=next((f for f in frames if f['tid']==task['thread_id']),None)
            if frame and {0x421F8A,0x56E183}<={f['return_va'] for f in frame['chain']}:
                task['TLS']=base.capture_tls(c,frame,pointer)
                task['TLS']['index_memory']=dict(pointer=0x761BC0,hex=c.get(0x761BC0,4).hex())
                if task['TLS']['TLS_index']>=64:
                    p=task['TLS']['TEB']+0xF94
                    task['TLS']['expansion_memory']=dict(pointer=p,hex=c.get(p,4).hex())
            if vt==0x59A430:
                task['scene_head_hex']=c.get(pointer,0x200).hex()
                task['controller_task_backpointer']=word(c.get(pointer+0x190+0x117C38,4))
                task['battle_gates']=notice.capture(c,pointer)
                task['terminal_frames']=[dict(return_va=f['return_va'],pointer=f['bp']-0x80,hex=c.get(f['bp']-0x80,0x90).hex())
                    for f in (frame['chain'] if frame else []) if f['return_va']in(0x451ABC,0x451716,0x421F8A)]
            row['tasks'].append(task)
        row['workroom_flags']=[dict(pointer=p,hex=c.get(p,2).hex())for p in (0x7A4E62,0x7E11A0)]
        if any(t['vtable']in(school.GROUP,school.UI)for t in row['tasks']):row['school']=school.capture(c)
        vm=bytes.fromhex(row['VM_hex'])
        if vm[4] and any(t['vtable']in(story.ADV,battle.BATTLE)for t in row['tasks']):
            row['program_code']=c.catalog.observe(c.get,vm)
        return row


def continue_school(pid,owned,progress,duration):
    report=dict(pid=pid,error=None,samples=[],workers=[],host_game_calls=[],host_memory_writes=[],
        collector_input_actions=[],full_battle_exit_accepted=False,full_native_instruction_trace=False)
    c=None;handles={};started=time.monotonic()
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
        deadline=min(started+duration,time.monotonic()+1500);last_signature=None;last_saved=0
        last_progress=time.monotonic();menu_since=None
        stop=Path(str(progress).removesuffix('.progress.json')+'.stop.json')
        while time.monotonic()<deadline:
            row=snapshot(c,owned)
            for task in row['tasks']:
                head=bytes.fromhex(task['header_hex']);tid=word(head,0x24)
                if not word(head,0x20) or not tid:continue
                key=(task['pointer'],tid)
                if key not in handles:
                    handle=W.HANDLE()
                    base.original.check(base.parent.duplicate(h,word(head,0x20),base.parent.current_process(),
                        C.byref(handle),0,False,2),'retain current original worker')
                    try:
                        need(base.get_thread_pid(handle)==pid and base.get_thread_id(handle)==tid,'same worker owner')
                        event=base.event_identity(c,word(head,0x1C))
                    except BaseException:
                        base.original.close(handle);raise
                    handles[key]=handle
                    report['workers'].append(dict(pointer=key[0],thread_id=tid,vtable=task['vtable'],
                        original_handle=word(head,0x20),event=event,first_elapsed=row['elapsed']))
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
        for handle in handles.values():base.original.close(handle)
        if c:base.original.close(c.h)
    return report


def run(out,seconds):
    isolation=require_qualified_guest()
    paths=[Path(__file__),ROOT/'devtools/terminal_workroom_input.py',ROOT/'devtools/terminal_workroom_contract.py',
           ROOT/'devtools/terminal_school_input.py',ROOT/'devtools/terminal_school_preparation_contract.py',
           ROOT/'devtools/terminal_battle_input.py',ROOT/'devtools/terminal_scene_owner_contract.py',
           ROOT/'devtools/terminal_story_catalog.py',ROOT/'devtools/terminal_owned_mouse.py',
           ROOT/'devtools/native_input_isolation.py',ROOT/'devtools/isolated_vm_preflight.py',
           ROOT/'devtools/isolated_guest_focus.py',ROOT/'devtools/terminal_input_window.py',
           ROOT/'devtools/terminal_battle_notice.py',AUTHORIZATION]
    identities=[base.identity(p)for p in paths];catalog=Catalog()
    continuation=clone(continue_school,CATALOG=catalog)
    with school_focus_scope():
        result=clone(menu.run,continue_menu=continuation,OneMenuSelection=SchoolController)(out,seconds,0,True,192)
    need(identities==[base.identity(p)for p in paths],'complete new input/collector layer frozen during lifetime')
    result['parent_implementations']=result.pop('implementations')
    result.update(kind='original_workroom_school_continuation_observation',implementation_layers=identities,input_isolation=isolation,
        observation_plan=dict(maximum_seconds=seconds,maximum_mouse_actions=7,story_phase_budgets=[192,192,64],
            stable_unhandled_wait_seconds=60,retreat_is_separate_from_retained_neutral_timeout_cases=True),
        full_battle_exit_accepted=False,full_resource_lifetime_proved=False,wait_return_proved=False,
        result_consumption_proved=False)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--seconds',type=int,default=1800);args=parser.parse_args();out=args.out.resolve()
    need(out.is_relative_to(ROOT/'analysis')and not out.exists(),'new owned local observation output')
    need(900<=args.seconds<=1800,'bounded full continuation lifetime')
    result=run(out,args.seconds);raw=json.dumps(result,separators=(',',':')).encode()
    need(len(raw)<=192*1024*1024,'bounded raw evidence');packed=gzip.compress(raw,mtime=0)
    need(len(packed)<=24*1024*1024,'bounded compressed source')
    with out.open('xb')as stream:stream.write(packed)
    print(json.dumps(dict(report=base.identity(out),probe_error=(result.get('probe')or{}).get('error'),
                          lifecycle_error=result['lifecycle']['error'],stop_reason=(result.get('probe')or{}).get('stop_reason'))),flush=True)
    if (result.get('probe')or{}).get('error')or result['lifecycle']['error']:raise SystemExit(1)


if __name__=='__main__':main()

