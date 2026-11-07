"""Native menu continuation after the original startup retires.

Snapshots never call game roots or write game memory. Input defaults to separate
Computer Use; an optional one-click backend requires explicit user authorization.
A stop file only stops observation/owned cleanup.
"""
import argparse
import ctypes as C
import ctypes.wintypes as W
import gzip
import json
from pathlib import Path
import time
import traceback
import threading
from types import SimpleNamespace

from devtools import terminal_scene_owner as base
from devtools import terminal_startup_handoff as startup
from devtools import terminal_menu_startup as startup_gate
from devtools.terminal_scene_resources import clone

ROOT=base.ROOT
need=base.need
word=base.word
RANGES=startup.RANGES+((0x45E8D0,0x45F9A0),(0x49F4E0,0x49F720),
    (0x4B8FF0,0x4B9300),(0x4D9F30,0x4DA550),(0x60CEB0,0x60CEE0),
    (0x4D1820,0x4D1B37),(0x4CE210,0x4CE560))
CONTROLLER=None


class OneMenuSelection:
    def __init__(self,index,authorized,story_limit=0):
        need(authorized is True,'separate explicit mouse override required')
        need(type(index) is int and index in (0,1),'reviewed main-menu selection')
        self.index=index;self.done=False;self.since=None;self.receipt=None;self.story=None;self.ready_start=None
        if story_limit:
            from devtools.terminal_story_input import StoryConfirm
            self.story=StoryConfirm(story_limit)

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
        from devtools.terminal_menu_input import owned_main_menu_click
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
                self.receipt['input_samples'].append(dict(elapsed=owned.elapsed(),wall_time_ns=time.time_ns(),
                    mouse_hex=c.get(game+0x196C,0x58).hex(),MAIN_event_hex=c.get(c.main+0x2C,8).hex()))
            def send():
                try:outcome['action']=owned_main_menu_click(c,hwnd,self.index,explicit_user_override=True)
                except BaseException as exc:outcome['error']=repr(exc)
            observe_input();worker=threading.Thread(target=send,name='owned-menu-input',daemon=False)
            worker.start();deadline=time.monotonic()+5;finished_at=None
            try:
                while time.monotonic()<deadline and len(self.receipt['input_samples'])<1024:
                    observe_input()
                    if not worker.is_alive():
                        if finished_at is None:finished_at=time.monotonic()
                        if time.monotonic()-finished_at>=.1:break
                    time.sleep(.005)
            finally:worker.join(timeout=6)
            need(not worker.is_alive(),'bounded mouse input finished and release attempted')
            observe_input();self.receipt.update(outcome)
            need('action' in self.receipt,'mouse backend returned a complete receipt')
            need(self.receipt['action']['error'] is None and self.receipt['action']['released'],
                 'single bounded original menu click completed')
        except Exception as exc:
            self.receipt['error']=repr(exc);raise
        finally:self.receipt['after_elapsed']=owned.elapsed()


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
            row['tasks'].append(task)
        return row


def continue_menu(pid,owned,progress,duration):
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
        c.main=word(c.get(0x7A4A00,4));report['main']=c.main
        identity=clone(base.source_identity,RANGES=RANGES,IAT=startup.IAT)
        report['source_before']=identity(c)
        report['TLS_implementation']=base.tls_contract(c)
        report['manager_event']=base.event_identity(c,word(c.get(c.main+0x17C,4)))
        deadline=min(started+duration,time.monotonic()+600);last_signature=None;last_saved=0
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
            signature=(tuple((t['pointer'],t['vtable']) for t in row['tasks']),
                row['MAIN_event_hex'],row['VM_hex'][56:72],row['mouse_hex'][96:104])
            now=time.monotonic()
            if signature!=last_signature or now-last_saved>=1:
                need(len(report['samples'])<2000,'bounded menu snapshot retention')
                row['index']=len(report['samples']);report['samples'].append(row)
                last_saved=now;last_signature=signature
                progress.write_text(json.dumps(dict(status='observing_menu_continuation',pid=pid,
                    elapsed=owned.elapsed(),samples=len(report['samples']),
                    tasks=[dict(pointer=t['pointer'],vtable=hex(t['vtable'])) for t in row['tasks']],
                    VM_PC=word(bytes.fromhex(row['VM_hex']),28),
                    mouse_hex=row['mouse_hex'],host_game_calls=0,
                    collector_input_actions=(int(CONTROLLER is not None and CONTROLLER.done)
                        +(len(CONTROLLER.story.actions) if CONTROLLER and CONTROLLER.story else 0)))),encoding='utf8')
            if stop.exists():
                raw=stop.read_bytes();need(len(raw)<=1024 and json.loads(raw)=={'stop':True},'explicit observation stop only')
                report['stop_reason']='controller_finished_observation';break
            if CONTROLLER is not None:
                CONTROLLER.observe(c,owned,row)
                if CONTROLLER.story and CONTROLLER.story.budget_exhausted:
                    report['story_budget_wait_sample']=row
                    report['stop_reason']='story_confirmation_budget';break
            time.sleep(.05)
        report.setdefault('stop_reason','bounded_menu_deadline')
        report['source_after']=identity(c)
        need(report['source_before']==report['source_after'],'original menu code unchanged')
    except Exception as exc:
        report.update(error=repr(exc),traceback=traceback.format_exc(limit=8))
    finally:
        if CONTROLLER is not None:
            report['mouse_controller']=dict(attempted=CONTROLLER.done,receipt=CONTROLLER.receipt,
                user_override_required=True,maximum_clicks=1)
            if CONTROLLER.receipt is not None:
                report['collector_input_actions'].append(CONTROLLER.receipt)
            if CONTROLLER.story is not None:
                report['collector_input_actions_scope']='mouse_menu_only'
                report['collector_story_input_actions']=CONTROLLER.story.actions
                report['maximum_story_confirmations']=CONTROLLER.story.maximum
        for handle in handles.values():base.original.close(handle)
        if c:base.original.close(c.h)
    return report


def run(out,seconds,menu_selection=None,explicit_user_override=False,story_limit=0):
    paths=[Path(__file__),Path(startup.__file__),Path(base.__file__),ROOT/'devtools/terminal_scene_resources.py']
    paths.append(Path(startup_gate.__file__))
    controller=None
    if menu_selection is not None:
        controller=OneMenuSelection(menu_selection,explicit_user_override,story_limit)
        paths.extend((ROOT/'devtools/terminal_menu_input.py',ROOT/'tools/school_native_dialogue_input.py',
                      ROOT/'tools/school_native_dialogue_desktop.py'))
        if story_limit:
            paths.extend((ROOT/'devtools/terminal_story_input.py',ROOT/'devtools/terminal_scene_automation.py',
                          ROOT/'tools/school_native_dialogue.py',ROOT/'analysis/school-native-dialogue-authorization-v1-20261022.json'))
    else:need(not story_limit,'story input requires the authorized current menu flow')
    identities=[base.identity(p) for p in paths]
    activations=[]
    class FocusedRuntime(base.VisibleOwnedRuntime):
        def __init__(self):
            super().__init__();self.focus_attempted=False;self.activating=False
        def members(self):
            members=super().members()
            if self.focus_attempted or self.activating:return members
            hwnd=base.original.findwindow(b'Cross Hermit',None)
            if not hwnd or not base.original.ubind('IsWindowVisible',W.BOOL,[W.HWND])(hwnd):return members
            pid=W.DWORD();base.original.ownerpid(hwnd,C.byref(pid))
            if pid.value not in members or pid.value not in self.handles:return members
            h=self.handles[pid.value];raw=base.original.memory(h,0x7A4A00,4)
            main=word(raw) if raw else 0
            if not main or base.original.getprop(hwnd,b'CPP_CLASS')!=main:return members
            self.focus_attempted=True;self.activating=True
            try:
                from tools.school_native_dialogue_input import focus_owned_window
                c=SimpleNamespace(pid=pid.value,owned=self,h=h,get=lambda p,n:base.original.required(h,p,n))
                activations.append(dict(elapsed=self.elapsed(),**focus_owned_window(c,hwnd)))
            except Exception as exc:activations.append(dict(elapsed=self.elapsed(),error=repr(exc)))
            finally:self.activating=False
            return members
    result=clone(base.run,run_probe=clone(continue_menu,CONTROLLER=controller),
                 VisibleOwnedRuntime=FocusedRuntime if controller else base.VisibleOwnedRuntime)(out,seconds)
    result['startup_activation']=activations
    need(identities==[base.identity(p) for p in paths],'observation implementation unchanged throughout native run')
    need(base.sha(startup.PARENT.read_bytes())==startup.PARENT_SHA,'fixed immutable asset parent')
    parent=json.loads(gzip.decompress(startup.PARENT.read_bytes()))
    inventory=result['runtime'].pop('immutable_files')
    need(inventory==parent['runtime']['immutable_files'],'freshly hashed native assets match fixed parent')
    result['runtime']['immutable_files_reference']=dict(path=startup.PARENT.relative_to(ROOT).as_posix(),
        sha256=startup.PARENT_SHA,rows=len(inventory),freshly_hashed_this_lifetime=True)
    result.update(kind='original_menu_continuation_observation',implementations=identities,
        human_operation_required=False,host_game_roots_called=False,full_battle_exit_accepted=False)
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--seconds',type=int,default=720)
    parser.add_argument('--menu-selection',type=int,choices=(0,1))
    parser.add_argument('--allow-owned-mouse',action='store_true',help='requires prior explicit user override of JS-only skill')
    parser.add_argument('--story-confirmations',type=int,default=0,help='bounded original ADV confirms using prior scan-code39 authorization')
    args=parser.parse_args();out=args.out.resolve()
    need(out.is_relative_to(ROOT/'analysis') and not out.exists(),'fresh bounded local output')
    need(300<=args.seconds<=900,'bounded native observation')
    result=run(out,args.seconds,args.menu_selection,args.allow_owned_mouse,args.story_confirmations)
    raw=json.dumps(result,separators=(',',':')).encode()
    need(len(raw)<=64*1024*1024,'bounded raw evidence');packed=gzip.compress(raw,mtime=0)
    need(len(packed)<=6*1024*1024,'bounded compressed evidence')
    with out.open('xb') as stream:stream.write(packed)
    print(json.dumps(dict(report=base.identity(out),probe_error=(result.get('probe') or {}).get('error'),
                          lifecycle_error=result['lifecycle']['error'])),flush=True)
    if (result.get('probe') or {}).get('error') or result['lifecycle']['error']:raise SystemExit(1)


if __name__=='__main__':main()
