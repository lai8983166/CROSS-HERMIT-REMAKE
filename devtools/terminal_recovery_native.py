"""Narrow native restoration backend with retained current process/Job identity."""
from __future__ import annotations
import ctypes as C
import ctypes.wintypes as W
import hashlib
from pathlib import Path
import struct
import types
from devtools import terminal_graphics_desktop as frozen
from devtools.terminal_graphics_recovery_observer_v2 import GuardedReadOnlyWindowsBackend
from devtools.terminal_graphics_recovery import created,ROOT,need
from devtools.terminal_oplock import Win

class RetainedOwner:
    def __init__(self, registration, controller_pid, controller_created):
        from devtools.terminal_recovery_admission import current_build
        need(registration['helper']==current_build()['helper'],'registration is exactly the admitted compiled helper')
        self.w=Win();self.process=None;self.job=None;self.owner=registration['owner'];self.close_results=[]
        k=self.w.k
        def bind(name,result,args):
            f=getattr(k,name);f.restype=result;f.argtypes=args;return f
        self.duplicate=bind('DuplicateHandle',W.BOOL,[W.HANDLE,W.HANDLE,W.HANDLE,C.POINTER(W.HANDLE),W.DWORD,W.BOOL,W.DWORD])
        self.current=bind('GetCurrentProcess',W.HANDLE,[])()
        self.query=bind('QueryInformationJobObject',W.BOOL,[W.HANDLE,C.c_int,C.c_void_p,W.DWORD,C.c_void_p])
        self.injob=bind('IsProcessInJob',W.BOOL,[W.HANDLE,W.HANDLE,C.POINTER(W.BOOL)])
        self.pathfn=bind('QueryFullProcessImageNameW',W.BOOL,[W.HANDLE,W.DWORD,W.LPWSTR,C.POINTER(W.DWORD)])
        parent=self.w.openp(0x1040,False,controller_pid);self.w.check(parent,'retain exact duplication source')
        try:
            need(created(self.w,parent)==controller_created,'same live registration controller')
            target=W.HANDLE();self.w.check(self.duplicate(parent,registration['job_handle'],self.current,C.byref(target),4,False,0),'duplicate query-only current owner Job')
            self.job=target.value
            self.process=self.w.openp(0x101010,False,self.owner['pid']);self.w.check(self.process,'retain actual native owner')
            need(created(self.w,self.process)==self.owner['process_created'] and self.w.wait(self.process,0)==258,'actual current owner lifetime still alive')
            same=W.BOOL();self.w.check(self.injob(self.process,self.job,C.byref(same)),'actual owner Job membership');need(same.value,'registration names actual owner Job')
            text=C.create_unicode_buffer(32768);size=W.DWORD(len(text));self.w.check(self.pathfn(self.process,0,text,C.byref(size)),'actual helper image path')
            path=Path(text.value).resolve();expected=registration['helper'];need(path==(ROOT/expected['path']).resolve() and path.is_relative_to(ROOT/'.venv-audit'),'fixed F current helper image')
            data=path.read_bytes();need(len(data)==expected['bytes'] and hashlib.sha256(data).hexdigest()==expected['sha256'],'exact current compiled helper bytes')
            raw=self.w.memory(self.process,self.owner['main_teb'],48)
            need(struct.unpack_from('<I',raw,24)[0]==self.owner['main_teb'] and struct.unpack_from('<II',raw,32)==(self.owner['pid'],self.owner['main_tid']),'actual live TEB PID/TID/self fields')
            self.helper=expected
        except BaseException:self.close();raise
        finally:self.w.check(self.w.close(parent),'close duplication source')
    def inspect(self,*,require_exit=True):
        raw=C.create_string_buffer(8+8*16);self.w.check(self.query(self.job,3,raw,len(raw),None),'retained actual Job members')
        assigned,count=struct.unpack_from('<II',raw.raw);need(assigned<=16 and count<=16 and assigned==count,'complete bounded actual Job membership')
        members=list(struct.unpack_from('<'+'Q'*count,raw.raw,8));wait=self.w.wait(self.process,0);code=W.DWORD()
        self.w.check(self.w.exit_process(self.process,C.byref(code)),'retained process actual exit code')
        if require_exit:need(wait==0 and code.value==0 and not members,'normal current process exit0 and actual empty Job before restoration')
        return dict(kind='retained-native-handles',owner=self.owner,process_wait=wait,process_exit=code.value,job_members=members,same_job=True)
    def close(self):
        for name in ('process','job'):
            value=getattr(self,name,None)
            if value:
                result=int(self.w.close(value));self.close_results.append(dict(kind=name,result=result));setattr(self,name,None)
                need(result==1,'retained '+name+' handle close')
        return self.close_results

class BoundWindowsBackend(GuardedReadOnlyWindowsBackend):
    evidence_kind='native'
    def __init__(self,journal):
        super().__init__();self.permit=None;self.journal=journal
        namespace=dict(vars(frozen),NATIVE_ADMISSION=True)
        self.primitive=types.FunctionType(frozen.WindowsBackend.write.__code__,namespace)
    def authorize(self,baseline,receipt,check_live):
        need(self.permit is None,'one active authenticated write scope')
        self.permit=(baseline,receipt,check_live)
    def disarm(self):self.permit=None
    def repair(self,*args,**kwargs):raise ValueError('legacy unrestricted repair is forbidden')
    def _gamma(self,device,value=None):
        if value is not None:
            need(self.permit is not None and device==self.permit[0]['target_device'],'authenticated exact gamma target')
            self.permit[2]()
        return frozen.WindowsBackend._gamma(self,device,value)
    def write(self,kind,value,*,device,baseline):
        need(self.permit is not None,'native writes require current authenticated releases')
        original,receipt,check=self.permit;check()
        need(device==original['target_device'] and baseline==original['state'],'exact original target and baseline')
        need(value==frozen._mutable(baseline,device)[kind],'only restore exact original values')
        need(kind in receipt['mutations'] or kind=='gamma','only authenticated mutation or gamma after mode restoration')
        self.journal('begin','write:'+kind)
        value=self.primitive(self,kind,value,device=device,baseline=baseline)
        self.journal('end','write:'+kind)
        return value
