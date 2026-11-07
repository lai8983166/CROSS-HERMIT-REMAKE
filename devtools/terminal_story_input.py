"""Bounded confirmation of real original ADV opcode51 waits only.

Reuses the already authorized scan-code39 backend and original input checker.
Never drives unknown UI choices, school assignments or battle state fields.
"""
import struct
import threading
import time

from devtools import terminal_scene_owner as base
from devtools import terminal_scene_automation as keyboard

ADV=0x5C306C


def confirmation_key(row):
    tasks=row['tasks'];vm=bytes.fromhex(row['VM_hex'])
    if len(tasks)!=1 or tasks[0]['vtable']!=ADV or len(vm)!=128:return None
    frame=next((f for f in row['frames'] if f['tid']==tasks[0]['thread_id']),None)
    if not frame or not {0x421F8A,0x56E183}<={f['return_va'] for f in frame['chain']}:return None
    if not vm[4] or struct.unpack_from('<HH',vm,32)!=(1,51):return None
    return (tasks[0]['pointer'],base.word(vm,16),base.word(vm,28))


class StoryConfirm:
    def __init__(self,maximum):
        base.need(type(maximum) is int and 1<=maximum<=192,'bounded original story confirmations')
        self.maximum=maximum;self.actions=[];self.key=None;self.since=None;self.last_completed=None;self.budget_exhausted=False

    def observe(self,c,owned,row):
        key=confirmation_key(row);now=time.monotonic()
        if key is None:self.key=None;self.since=None;return
        if key!=self.key:self.key=key;self.since=now;return
        if now-self.since<1:return
        base.need(key!=self.last_completed,'do not retry a potentially delivered story confirmation')
        if len(self.actions)>=self.maximum:self.budget_exhausted=True;return
        record=dict(key=list(key),before_elapsed=owned.elapsed(),before_sample=row,error=None,
            samples=[],game_memory_written=False,full_instruction_causality_proved=False)
        self.actions.append(record);advanced=threading.Event();outcome={};thread=None
        try:
            original=base.SOURCE.read_bytes();record['input_code_identity']=[]
            for a,b in keyboard.INPUT_RANGES:
                actual=c.get(a,b-a);base.need(actual==original[a-0x400000:b-0x400000],'live original confirmation code')
                record['input_code_identity'].append(dict(pointer=a,bytes=b-a,sha256=base.sha(actual)))
            hwnd=base.original.findwindow(b'Cross Hermit',None)
            record['activation']=keyboard.focus_owned_window(c,hwnd)
            game=base.word(c.get(0x7A49FC,4))
            foreground=base.original.ubind('GetForegroundWindow',keyboard.W.HWND,[])
            def sample():
                s=dict(index=len(record['samples']),elapsed=owned.elapsed(),wall_time_ns=time.time_ns(),
                    foreground_hwnd=foreground() or 0,keyboard_hex=c.get(game+0x10B8,0xA00).hex(),
                    VM_hex=c.get(base.native.VM,128).hex(),mouse_hex=c.get(game+0x196C,0x58).hex())
                record['samples'].append(s);return s
            first=sample()
            base.need(not bytes.fromhex(first['keyboard_hex'])[0x4B9]&0x80,'confirmation key initially released')
            current=bytes.fromhex(first['VM_hex'])
            base.need(current[4] and struct.unpack_from('<HH',current,32)==(1,51)
                      and (base.word(current,16),base.word(current,28))==key[1:],
                      'same current active original script and confirmation wait')
            def send():
                try:outcome['receipt']=keyboard.bounded_confirm(c,hwnd,advanced)
                except BaseException as exc:outcome['error']=repr(exc)
            thread=threading.Thread(target=send,name='owned-story-confirm',daemon=False);thread.start()
            deadline=time.monotonic()+3;finished=None
            while time.monotonic()<deadline and len(record['samples'])<256:
                s=sample()
                if base.word(bytes.fromhex(s['VM_hex']),28)!=key[2]:advanced.set()
                if not thread.is_alive():
                    if finished is None:finished=time.monotonic()
                    if time.monotonic()-finished>=.1:break
                time.sleep(.005)
            thread.join(timeout=3);base.need(not thread.is_alive(),'bounded keyboard backend completed')
            record['backend']=outcome;base.need('receipt' in outcome,'keyboard backend returned receipt')
            record['transition']=keyboard.transition(record['samples'],outcome['receipt'],key[2],hwnd)
            self.last_completed=key;self.key=None;self.since=None
        except Exception as exc:record['error']=repr(exc);raise
        finally:
            if thread and thread.is_alive():thread.join(timeout=3)
            record['after_elapsed']=owned.elapsed()
