"""Minimal DbgEng client for this project's guest-only virtual serial channel.

No local kernel attach, UI, software breakpoints, memory/register writes, or
host boot edits. Vtable indices are taken from the installed Microsoft SDK's
IDebugClient/IDebugControl declarations; source header identity is recorded.
"""
import ctypes as C
import os
from pathlib import Path
import re
import time
import threading
import uuid
from devtools.isolated_windows_vm import WORKER,VMX,environment,identity
from devtools.isolated_vm_kd import PIPE,validate_kd_vmx

SDK=Path('C:/Program Files (x86)/Windows Kits/10/Debuggers')
CLIENT='27fe5639-8407-4f47-8364-ee118fb08ac8'
CONTROL='5182e668-105e-416e-ad92-24ef800424ba'
OUTPUT='4bf58045-d654-4c40-b0af-683090f356dc'
UNKNOWN='00000000-0000-0000-c000-000000000046'
H=C.c_long;U=C.c_ulong;P=C.c_void_p


def guid(value):return (C.c_ubyte*16).from_buffer_copy(uuid.UUID(value).bytes_le)


def need(value,message):
    if not value:raise ValueError(message)


def method(pointer,index,result,*args):
    table=C.cast(pointer,C.POINTER(C.POINTER(P))).contents
    return C.WINFUNCTYPE(result,P,*args)(table[index])


class Engine:
    def __init__(self):
        validate_kd_vmx(VMX.read_text(encoding='utf8'))
        header=SDK/'inc/dbgeng.h';text=header.read_text()
        expected={'IDebugClient':{'AttachKernel':3,'EndSession':26,'SetOutputCallbacks':34,'FlushCallbacks':47},
                  'IDebugControl':{'GetInterrupt':3,'SetInterrupt':4,'GetExecutionStatus':49,'SetExecutionStatus':50,'Execute':66,'WaitForEvent':93}}
        for interface,indices in expected.items():
            body=text.split('DECLARE_INTERFACE_('+interface+', IUnknown)',1)[1].split('};',1)[0]
            names=re.findall(r'STDMETHOD(?:V)?(?:_\([^,]+,\s*|\()([A-Za-z0-9_]+)\)',body)
            need(all(names[i]==n for n,i in indices.items()),'installed SDK interface layout')
        os.environ.update({k:v for k,v in environment().items()if k in('TEMP','TMP')})
        os.environ['_NT_SYMBOL_PATH']=str(WORKER/'symbols');os.environ['_NT_ALT_SYMBOL_PATH']=''
        self.dll_directory=os.add_dll_directory(str(SDK/'x64'))
        self.dll=C.WinDLL(str(SDK/'x64/dbgeng.dll'))
        self.client=P();self.control=P();self.output=[];self.output_bytes=0;self.overflow=False;self.calls=[];self.attached=False
        self.identities=dict(header=identity(header),engine=identity(SDK/'x64/dbgeng.dll'))
        create=self.dll.DebugCreate;create.argtypes=[P,C.POINTER(P)];create.restype=H
        self.check(create(C.byref(guid(CLIENT)),C.byref(self.client)),'DebugCreate')
        self.check(method(self.client,0,H,P,C.POINTER(P))(self.client,C.byref(guid(CONTROL)),C.byref(self.control)),'IDebugControl')
        query_type=C.WINFUNCTYPE(H,P,P,C.POINTER(P));ref_type=C.WINFUNCTYPE(U,P);output_type=C.WINFUNCTYPE(H,P,U,C.c_char_p)
        class Object(C.Structure):_fields_=[('vtable',C.POINTER(P))]
        def query(this,requested,result):
            if C.string_at(requested,16)in(uuid.UUID(OUTPUT).bytes_le,uuid.UUID(UNKNOWN).bytes_le):result[0]=this;return 0
            result[0]=None;return -2147467262
        def output(this,mask,text):
            data=text or b''
            if self.output_bytes+len(data)<=1024*1024:
                self.output.append(dict(monotonic=time.monotonic(),mask=int(mask),text=data.decode('utf8',errors='replace')));self.output_bytes+=len(data)
            else:self.overflow=True
            return 0
        self.callbacks=(query_type(query),ref_type(lambda this:2),ref_type(lambda this:1),output_type(output))
        self.vtable=(P*4)(*[C.cast(fn,P).value for fn in self.callbacks]);self.object=Object(self.vtable)
        self.check(method(self.client,34,H,P)(self.client,C.byref(self.object)),'SetOutputCallbacks')

    def check(self,result,operation):
        if result<0:raise RuntimeError(operation+' HRESULT=%08x'%(result&0xffffffff))
        return result

    def attach(self):
        options=('com:pipe,port='+PIPE+',resets=0,reconnect').encode()
        self.check(method(self.client,3,H,U,C.c_char_p)(self.client,0,options),'AttachKernel owned guest pipe');self.attached=True

    def wait(self,milliseconds=1000):
        need(0<=milliseconds<=30000,'bounded engine wait')
        timer=threading.Timer(milliseconds/1000,lambda: method(self.control,4,H,U)(self.control,2))
        timer.start()
        try:result=method(self.control,93,H,U,U)(self.control,0,0xffffffff)
        finally:timer.cancel();timer.join()
        self.calls.append(dict(operation='WaitForEvent',milliseconds=milliseconds,result=result,monotonic=time.monotonic()))
        self.check(result,'WaitForEvent');return result==0

    def interrupt(self):self.check(method(self.control,4,H,U)(self.control,0),'SetInterrupt guest only')

    def status(self):
        value=U();self.check(method(self.control,49,H,C.POINTER(U))(self.control,C.byref(value)),'GetExecutionStatus');return value.value

    def go(self):
        self.check(method(self.control,50,H,U)(self.control,1),'SetExecutionStatus GO')

    def execute(self,command):
        # This module is a bounded development observer, not arbitrary command I/O.
        need(command in ('vertarget','r','rF','rX','r cr0,cr2,cr3,cr4','r dr0,dr1,dr2,dr3,dr6,dr7','bc *','bl','lm m nt','dt nt!_KTRAP_FRAME','dt nt!_KTHREAD','dt nt!_ETHREAD Cid','dt nt!_EPROCESS UniqueProcessId DebugPort','? @$tpid','? @$tid','? @$thread','? @$proc')
             or re.fullmatch(r'\.echo [A-Za-z0-9_ -]{1,80}',command)
             or re.fullmatch(r'(?:db|dq|u) [0-9a-f`]+ L[0-9a-f]{1,3}',command)
             or re.fullmatch(r'ba e 1 ffff[0-9a-f`]+',command)
             or re.fullmatch(r'ba e 1 ffff[0-9a-f`]+ "\.if \(@\$tpid == 0x[0-9a-f]+\) \{ \.if \(@\$tid == 0x[0-9a-f]+\) \{ \.if \(poi\(@rbp-0x48\) == 0x[0-9a-f]+\) \{ \.echo OWNED_WAIT_RETURN \} \.else \{ gc \} \} \.else \{ gc \} \} \.else \{ gc \}"',command)
             or re.fullmatch(r'ba e 1 ffff[0-9a-f`]+ "\.if \(@\$tpid == 0x[0-9a-f]+ && @\$tid == 0x[0-9a-f]+\) \{ \.echo OWNED_WAIT_RETURN \} \.else \{ gc \}"',command),
             'read-only diagnostics or explicitly owned kernel hardware breakpoint')
        start=len(self.output);self.check(method(self.control,66,H,U,C.c_char_p,U)(self.control,0,command.encode(),0),'Execute '+command)
        self.calls.append(dict(operation='Execute',command=command,monotonic=time.monotonic()))
        need(not self.overflow,'bounded debugger output');return ''.join(x['text']for x in self.output[start:])

    def close(self):
        if self.client:
            if self.attached:
                if self.status()==6:
                    self.execute('bc *')
                    self.go()
                try:self.wait(1000)
                except RuntimeError as exc:
                    if 'HRESULT=8000000a' not in str(exc):raise
                self.check(method(self.client,26,H,U)(self.client,2),'EndSession active detach')
            method(self.client,34,H,P)(self.client,None)
        if self.control:method(self.control,2,U)(self.control);self.control=None
        if self.client:method(self.client,2,U)(self.client);self.client=None
        self.dll_directory.close()
