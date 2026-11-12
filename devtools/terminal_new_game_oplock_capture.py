"""One file-system event gates live NEW_GAME; never owns its debugger port.

Menu readiness and long-lived ADV reuse the frozen observer. NEW_GAME itself is
sampled once, only after an acknowledged RW break on the private CH001 stream.
"""
import ctypes as C
import hashlib
from pathlib import Path
import struct
import time
from devtools import terminal_new_game_capture as old
from devtools.terminal_oplock import ReadOplock, Win, need, PENDING_OWNERS
from devtools.terminal_oplock_probe import process_info

CONTROLLER=None
ROOT=Path(__file__).resolve().parents[1]
RELATIVE='DATA/ADV/DAT/CH001.YBC'


def identity(path):
    raw=Path(path).read_bytes()
    return dict(path=str(Path(path).resolve()),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


class Session:
    def __init__(self,c):
        from tools.school_native_scene import APP,INSTALLED
        self.path=(APP.parent/RELATIVE).resolve();self.c=c;self.lock=None;self.pending=True
        self.data=dict(mode='private_CH001_RW_oplock',error=None,game_memory_writes=False,
                       debugger_attach=False,accepted=False)
        need(self.path.is_relative_to(ROOT/'.venv-audit') and not self.path.samefile(INSTALLED/RELATIVE),
             'separate existing private CH001 file')
        self.data['file_before']=identity(self.path)
        original=identity(INSTALLED/RELATIVE)
        need((original['bytes'],original['sha256'])==(self.data['file_before']['bytes'],self.data['file_before']['sha256']),
             'unmodified original CH001 content')
        self.data['ntdll_disk']=identity('C:/Windows/SysWOW64/ntdll.dll')
        self.expected_wrapper=(ROOT/'analysis/hermit_game.exe').read_bytes()[0x2ABC0:0x2AC50]
        self.w=Win();freq=C.c_int64();self.w.check(self.w.frequency(C.byref(freq)),'native QPC frequency')
        self.data['qpc_frequency']=freq.value
        self.data['owner_before']=self.owner()
        # All file opens/hashes above precede the lock. No other read of this
        # stream is allowed until close has completed the async request.
        self.lock=ReadOplock(self.path,15)

    def owner(self):
        info=process_info(self.w,self.c.h)
        need(info['pid']==self.c.pid and info['parent_pid']==self.c.owned.pi.pid
             and info['debug_port']==C.c_size_t(-1).value
             and {self.c.pid,self.c.owned.pi.pid}<=set(self.c.owned.members()),
             'same owned original parent and existing child debug port')
        return info

    def frame(self,c,frame,handle):
        ancestry={x['return_va'] for x in frame['chain']}
        if 0x49F53E not in ancestry:return
        need({0x42ABF3,0x421F8A,0x56E183}<=ancestry,'original NEW_GAME file-open/CRT ancestry')
        eip=frame['EIP'];code=c.get(eip-12,32)
        need(code[:1]==b'\xb8' and code[5:6]==b'\xba' and code[10:15]==b'\xff\xd2\xc2\x2c\x00',
             'qualified WOW64 NtCreateFile saved-return layout')
        descriptor=C.create_string_buffer(8);fs=old.word(bytes.fromhex(frame['context_hex']),144)
        self.w.check(self.w.selector(handle,fs,descriptor),'actual blocked worker FS')
        d=descriptor.raw;teb=struct.unpack_from('<H',d,2)[0]|d[4]<<16|d[7]<<24
        head=c.get(teb,48);stackbase,stacklimit=struct.unpack_from('<2I',head,4)
        need(old.word(head,24)==teb and struct.unpack_from('<2I',head,32)==(c.pid,frame['tid'])
             and stacklimit<=frame['ESP']<stackbase,'actual blocked worker stack bounds')
        stack=c.get(frame['ESP'],min(4096,stackbase-frame['ESP']));args=struct.unpack_from('<11I',stack,4)
        need(args[1]==0x80100080 and args[5:9]==(1,1,1,0x60) and args[4]==args[9]==args[10]==0,
             'same original readonly synchronous existing-file arguments')
        oa=c.get(args[2],24);need(old.word(oa)==24 and old.word(oa,4)==0,'absolute original file attributes')
        us=c.get(old.word(oa,8),8);length,maximum,p=struct.unpack('<HHI',us)
        need(0<length<=maximum<=2048 and length%2==0,'bounded current file name')
        raw=c.get(p,length);name=raw.decode('utf-16le')
        need(name.casefold()==('\\??\\'+str(self.path)).casefold(),'actual gated CH001 system call')
        namebuffer=C.create_unicode_buffer(32768)
        from devtools.terminal_menu_handoff import base
        size=base.original.mapped(c.h,eip,namebuffer,len(namebuffer))
        need(size and namebuffer.value.casefold().endswith('\\windows\\syswow64\\ntdll.dll'),
             'actual system-call mapping')
        live=c.get(0x42ABC0,0x90)
        need(live==self.expected_wrapper,'original CreateFileA wrapper bytes')
        frame['oplock_file_open']=dict(stack_hex=stack.hex(),nt_create_file=eip-12,nt_code_hex=code.hex(),
            args=list(args),object_attributes_hex=oa.hex(),unicode_string_hex=us.hex(),name_hex=raw.hex(),
            mapped_file=namebuffer.value,wrapper_hex=live.hex(),captured_qpc=self.w.qpc(),
            TEB=teb,TEB_hex=head.hex(),descriptor_hex=d.hex())

    def collect(self,capture):
        need(self.pending and self.lock is not None,'one outstanding private file event')
        try:
            need(self.lock.observe_break(6000),'bounded CH001 RW break')
            need(not self.lock.receipt['file_closed'] and not self.lock.receipt['watchdog_release'],
                 'file gate still held before snapshot')
            self.data['snapshot_begin_qpc']=self.w.qpc()
            row=old.Capture.snapshot(capture)
            self.data['snapshot_end_qpc']=self.w.qpc()
            need(not self.lock.receipt['file_closed'] and not self.lock.receipt['watchdog_release'],
                 'file gate held throughout snapshot')
            tasks=[t for t in row['tasks'] if t['vtable']==old.NEW_GAME]
            need(len(tasks)==1 and 'TLS' in tasks[0],'one actual live NEW_GAME TLS lifetime')
            task=tasks[0];frame=next(f for f in row['frames'] if f['tid']==task['thread_id'])
            need('oplock_file_open' in frame,'file event binds to original NEW_GAME worker')
            self.data['owner_during']=self.owner()
            need(self.data['owner_during']==self.data['owner_before'],'original debug ownership unchanged')
            self.data.update(sample_elapsed=row['elapsed'],thread_id=task['thread_id'],node=task['pointer'],
                             captured_qpc=frame['oplock_file_open']['captured_qpc'])
            self.lock.release();self.pending=False
            handle=capture.handles[(task['pointer'],task['thread_id'])]
            need(self.w.wait(handle,4000)==0,'original NEW_GAME natural exit after release')
            code=capture.api.status(handle);need(code==0,'original NEW_GAME retained exit0')
            worker=next(w for w in capture.workers if (w['pointer'],w['thread_id'])==(task['pointer'],task['thread_id']))
            worker['exit']=dict(code=code,wait_status=0,elapsed=capture.owned.elapsed(),before_WM_CLOSE=True)
            self.data['exit']=dict(worker['exit'],qpc=self.w.qpc())
            self.data['owner_after']=self.owner()
            need(self.data['owner_after']==self.data['owner_before'],'debug ownership after natural worker exit')
            return row
        except BaseException as exc:
            self.data['error']=repr(exc);raise
        finally:
            # One event only. A wrong file caller fails instead of retrying.
            self.lock.release();self.pending=False

    def finish(self):
        if self.lock:
            self.data['oplock']=self.lock.finish()
            need(not self.lock.receipt['watchdog_release'],'watchdog containment is not successful capture')
        need(not any(p.path==self.path for p in PENDING_OWNERS),'no pending async owner before identity')
        self.data['file_after']=identity(self.path)
        need(self.data['file_after']==self.data['file_before'],'private CH001 bytes unchanged')


def continue_menu(pid,owned,progress,duration):
    from devtools.terminal_scene_resources import clone
    controller=CONTROLLER
    class EventAPI(old.NativeAPI):
        def frame(self,c,h,tid):
            row=super().frame(c,h,tid)
            if controller.oplock is not None and controller.oplock.pending:
                controller.oplock.frame(c,row,h)
            return row
    class EventCapture(old.Capture):
        def __init__(self,c,owned,main_tid,api):
            super().__init__(c,owned,main_tid,api,clock=time.perf_counter)
        def snapshot(self):
            if controller.oplock is not None and controller.oplock.pending:
                return controller.oplock.collect(self)
            return super().snapshot()
        def close(self):
            try:
                if controller.oplock is not None:controller.oplock.finish()
            finally:super().close()
        def receipt(self):
            r=super().receipt()
            r['pause_clock']='perf_counter'
            r['oplock']=controller.oplock.data if controller.oplock is not None else None
            return r
    return clone(old.continue_menu,CONTROLLER=controller,Capture=EventCapture,NativeAPI=EventAPI)(pid,owned,progress,duration)
