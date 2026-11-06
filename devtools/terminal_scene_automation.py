"""One bounded, previously authorized system-key handoff; never game-field writes.

The caller must invoke observe AFTER resuming the sampled original threads.
Reuses the frozen owned-window/desktop/foreground guards and release-on-error
backend. Tool delivery alone is insufficient: original input and VM must agree.
"""
import argparse
import ctypes as C
import gzip
import ctypes.wintypes as W
import hashlib
import json
from pathlib import Path
import struct
import threading
import time
from types import SimpleNamespace

from tools.school_native_dialogue import INPUT_RANGES
from tools.school_native_dialogue_input import focus_owned_window,owned_held_space
from tools import school_native_dialogue_input as input_backend
from devtools import terminal_scene_owner as base

ROOT=base.ROOT


def need(value,message):
    if not value:raise ValueError(message)


def word(raw,offset=0):return struct.unpack_from('<I',raw,offset)[0]


def transition(rows, receipt, wait_pc, hwnd):
    """Check recorded game state and backend timestamps, not SendInput alone."""
    need(1<=len(rows)<=256,'bounded actual input observations')
    need([r['index'] for r in rows]==list(range(len(rows))),'ordered input observations')
    need(all(a['wall_time_ns']<=b['wall_time_ns'] for a,b in zip(rows,rows[1:])),
         'monotonic input receipt order')
    pressed=[];released=[];advanced=[]
    for row in rows:
        keyboard=bytes.fromhex(row['keyboard_hex']);vm=bytes.fromhex(row['VM_hex'])
        need(len(keyboard)==0xA00 and len(vm)==128,'complete original keyboard and VM fields')
        need(row['foreground_hwnd']==hwnd,'same original foreground throughout input handoff')
        down=bool(keyboard[0x480+0x39]&0x80)
        if down:pressed.append(row['index'])
        elif pressed:released.append(row['index'])
        if word(vm,28)!=wait_pc:advanced.append(row['index'])
    need(receipt.get('input_returned') is True and receipt.get('released') is True
         and receipt.get('down_result')==1 and receipt.get('up_results')==[1],
         'guarded original backend press and release actually submitted')
    need(receipt['scan_code']==0x39 and receipt['hold_ms']==120,'exact previously authorized system input')
    need(receipt['down_wall_time_ns']<=receipt['up_wall_time_ns'],'input press/release time order')
    need(pressed and released and advanced,'actual original press, release and VM transition')
    need(advanced[0]>=pressed[0] and released[0]>pressed[0],'original input precedes observed advancement')
    need(rows[0]['wall_time_ns']<=receipt['down_wall_time_ns']
         and receipt['up_wall_time_ns']<=rows[-1]['wall_time_ns'],'input bracketed by retained samples')
    return dict(press_index=pressed[0],release_index=released[0],advanced_index=advanced[0],
                before_PC=wait_pc,after_PC=word(bytes.fromhex(rows[advanced[0]]['VM_hex']),28),
                transition_observed=True,full_instruction_causality_proved=False)


def bounded_confirm(c,hwnd,advanced):
    """Same guarded key; release at first observed progress or the120ms ceiling.

    The release condition is explicit test input, not a game-state write. A
    held level can otherwise acknowledge two short adjacent dialogue waits.
    """
    class Api:
        @staticmethod
        def submit(packet):
            send=base.original.ubind('SendInput',W.UINT,[W.UINT,C.POINTER(input_backend.INPUT),C.c_int])
            return send(1,C.byref(packet),C.sizeof(input_backend.INPUT))
    guard=lambda:input_backend.owned_target_guard(c,hwnd)
    receipt=input_backend.held_space(Api(),guard,120,sleep=advanced.wait)
    receipt.update(hold_policy='release_on_first_observed_VM_advance_or_120ms',
                   maximum_hold_ms=120,hold_ms_is_ceiling=True,
                   hwnd=hwnd,pid=c.pid,existing_process_memory_written=False)
    return receipt


class OneDialogueInput:
    def __init__(self):
        self.wait_pc=None;self.since=None;self.done=False;self.result=None

    def observe(self,c,owned,hwnd,sample):
        if self.done:return
        head=bytes.fromhex(sample.get('scene_head_hex',''))
        vm=bytes.fromhex(sample['VM_hex'])
        waiting=bool(head and head[0x43] and head[0x59] and vm[4]
                     and struct.unpack_from('<HH',vm,32)==(1,51))
        pc=word(vm,28);now=time.monotonic()
        if not waiting:self.since=None;return
        if self.since is None or pc!=self.wait_pc:
            self.wait_pc=pc;self.since=now;return
        if now-self.since<1:return
        self.done=True  # Never retry a possibly delivered key or change its semantics.
        self.result=dict(wait_PC=pc,samples=[],error=None,transition_observed=False,
                         suspension_during_input=False,game_memory_written=False)
        outcome={};thread=None;advanced_event=threading.Event()
        try:
            raw=base.SOURCE.read_bytes()
            self.result['input_code_identity']=[]
            for a,b in INPUT_RANGES:
                actual=c.get(a,b-a)
                need(actual==raw[a-0x400000:b-0x400000],'live original input implementation')
                self.result['input_code_identity'].append(dict(pointer=a,bytes=b-a,sha256=base.sha(actual)))
            game=word(c.get(0x7A49FC,4))
            self.result['game']=game
            self.result['activation']=focus_owned_window(c,hwnd)
            foreground=base.original.ubind('GetForegroundWindow',W.HWND,[])
            def snapshot():
                row=dict(index=len(self.result['samples']),wall_time_ns=time.time_ns(),
                         elapsed=owned.elapsed(),foreground_hwnd=foreground() or 0,
                         keyboard_hex=c.get(game+0x10B8,0xA00).hex(),
                         VM_hex=c.get(base.native.VM,128).hex(),
                         mouse_hex=c.get(game+0x196C,0x58).hex())
                self.result['samples'].append(row)
                return row
            initial=snapshot()
            need(word(bytes.fromhex(initial['VM_hex']),28)==pc
                 and not bytes.fromhex(initial['keyboard_hex'])[0x4B9]&0x80,
                 'same original stable confirmation, initially released')
            def send():
                try:outcome['receipt']=bounded_confirm(c,hwnd,advanced_event)
                except BaseException as exc:outcome['error']=repr(exc)
            thread=threading.Thread(target=send,name='owned-scancode39',daemon=False)
            thread.start()
            deadline=time.monotonic()+2
            while time.monotonic()<deadline and len(self.result['samples'])<256:
                row=snapshot()
                if word(bytes.fromhex(row['VM_hex']),28)!=pc:advanced_event.set()
                if outcome.get('receipt'):
                    try:
                        self.result.update(transition(self.result['samples'],outcome['receipt'],pc,hwnd))
                        break
                    except ValueError:
                        pass  # Only observe longer; never submit another key.
                if outcome.get('error'):break
                time.sleep(.005)
            thread.join(timeout=3)
            need(not thread.is_alive(),'bounded input backend finished and released')
            self.result['backend']=outcome
            need('receipt' in outcome,'input backend returned receipt')
            self.result.update(transition(self.result['samples'],outcome['receipt'],pc,hwnd))
        except BaseException as exc:
            self.result['error']=repr(exc)
            self.result['backend']=outcome
            raise
        finally:
            if thread and thread.is_alive():thread.join(timeout=3)


def implementation():
    paths=[Path(__file__),ROOT/'tools/school_native_dialogue_input.py',
           ROOT/'tools/school_native_dialogue_desktop.py',
           ROOT/'analysis/school-native-dialogue-authorization-v1-20261022.json']
    return [base.identity(p) for p in paths]


def run(output,duration):
    from devtools.terminal_scene_resources import build_run
    controller=OneDialogueInput()
    runtimes=[]
    class ForegroundOwnedRuntime(base.VisibleOwnedRuntime):
        def __init__(self):
            super().__init__();self.activation=[];self.focus_attempted=False;self.activating=False
            self.failure_context=[];runtimes.append(self)

        def members(self):
            members=super().members()
            if self.focus_attempted or self.activating:return members
            hwnd=base.original.findwindow(b'Cross Hermit',None)
            if not hwnd:return members
            visible=base.original.ubind('IsWindowVisible',W.BOOL,[W.HWND])
            if not visible(hwnd):return members
            pid=W.DWORD();base.original.ownerpid(hwnd,C.byref(pid))
            if pid.value not in members or pid.value not in self.handles:return members
            h=self.handles[pid.value]
            raw=base.original.memory(h,0x7A4A00,4)
            main=word(raw) if raw else 0
            if not main or base.original.getprop(hwnd,b'CPP_CLASS')!=main:return members
            c=SimpleNamespace(pid=pid.value,owned=self,h=h,
                              get=lambda p,n:base.original.required(h,p,n))
            self.activating=True;self.focus_attempted=True
            try:
                self.activation.append(dict(elapsed=self.elapsed(),**focus_owned_window(c,hwnd)))
            except BaseException as exc:
                self.activation.append(dict(elapsed=self.elapsed(),error=repr(exc)))
                # Foreground is still mandatory at the actual input boundary.
                # A failed optional early activation must not abort construction.
            finally:self.activating=False
            return members

        def finish(self):
            # Failure-only bounded contexts, before inherited exclusively-owned cleanup.
            for pid in super().members():
                h=self.handles.get(pid)
                if h and base.original.memory(h,0x49DD70,16)==base.SOURCE.read_bytes()[0x9DD70:0x9DD80]:
                    try:
                        with base.original.frozen(h,pid) as frames:
                            self.failure_context.append(dict(pid=pid,elapsed=self.elapsed(),frames=frames))
                    except Exception as exc:self.failure_context.append(dict(pid=pid,error=repr(exc)))
            return super().finish()

    def after_sample(c,owned,hwnd,sample):
        try:controller.observe(c,owned,hwnd,sample)
        except Exception as exc:
            # Preserve delivery failure, then let the next read-only snapshot
            # identify a renderer fault which may have stopped keyboard updates.
            return dict(input_error=repr(exc),no_retry=True,continue_failure_diagnostics=True)
    before=implementation()
    result=build_run(base,runtime_class=ForegroundOwnedRuntime,post_sample_hook=after_sample)(output,duration)
    after=implementation()
    need(before==after,'automation/backend implementations unchanged during current lifetime')
    result['automation']=dict(implementations=before,backend='owned scan-code39; release on advance,120ms ceiling',
        maximum_actions=1,action_attempted=controller.done,action=controller.result,
        human_operation_required=False,original_input_object_written=False,
        complete_battle_exit_accepted=False,
        startup_activation=[r for runtime in runtimes for r in runtime.activation],
        pending_cleanup_contexts=[r for runtime in runtimes for r in runtime.failure_context],
        prior_explicit_authorization=dict(thread='01a0f832-bf3c-7470-9974-b707b159226c',
            turn='01a15f55-b5da-7eb0-9e27-841d2e64fab5',
            record='analysis/school-native-dialogue-authorization-v1-20261022.json',
            verified_in_original_user_message=True))
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--seconds',type=int,default=60)
    args=p.parse_args();out=args.out.resolve()
    need(out.is_relative_to(ROOT/'analysis') and not out.exists(),'fresh immutable local output')
    need(15<=args.seconds<=120,'bounded automatic test 15..120 seconds')
    result=run(out,args.seconds)
    raw=json.dumps(result,separators=(',',':')).encode()
    need(len(raw)<=64*1024*1024,'bounded automatic diagnostic data')
    packed=gzip.compress(raw,mtime=0)
    need(len(packed)<=12*1024*1024,'bounded compressed automatic evidence')
    with out.open('xb') as stream:stream.write(packed)
    print(json.dumps(dict(report=base.identity(out),resource_status=result['resource_status'],
        action=(result['automation']['action'] or {}).get('transition_observed'),
        error=(result.get('probe') or {}).get('error'),lifecycle_error=result['lifecycle']['error'])),flush=True)
    if ((result.get('probe') or {}).get('error') or result['lifecycle']['error']
            or not (result['automation']['action'] or {}).get('transition_observed')
            or (result['automation']['action'] or {}).get('error')):
        raise SystemExit(1)


if __name__=='__main__':main()
