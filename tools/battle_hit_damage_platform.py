"""Actual current-thread Win32 TLS leaves, with an explicit guest token role."""
import ctypes
from ctypes import wintypes
from tools.battle_pathfinding_emulation import need


class NativeTLS:
    def __init__(self,token,guest_index=51):
        self.kernel=ctypes.WinDLL('kernel32',use_last_error=True);k=self.kernel
        for name,args,result in [('TlsAlloc',[],wintypes.DWORD),('TlsFree',[wintypes.DWORD],wintypes.BOOL),
                                 ('TlsSetValue',[wintypes.DWORD,ctypes.c_void_p],wintypes.BOOL),('TlsGetValue',[wintypes.DWORD],ctypes.c_void_p),
                                 ('GetLastError',[],wintypes.DWORD),('SetLastError',[wintypes.DWORD],None),('GetCurrentThreadId',[],wintypes.DWORD)]:
            f=getattr(k,name);f.argtypes=args;f.restype=result
        self.owner=k.GetCurrentThreadId();self.token=token;self.guest_index=guest_index;self.last_error=0x1234;self.trace=[];self.closed=False
        saved=ctypes.get_last_error()
        try:
            self.index=k.TlsAlloc();need(self.index!=0xFFFFFFFF,'actual TlsAlloc')
            need(k.TlsSetValue(self.index,token)!=0,'actual TlsSetValue current owned slot')
            need(k.TlsGetValue(self.index)==token,'actual TLS token readback')
        finally:ctypes.set_last_error(saved)
        self.creation=dict(thread=self.owner,native_index=self.index,guest_index=guest_index,guest_token=token,actual_set_and_readback=True,pointer_is_guest_token_not_native_dereference=True)

    def leaf(self,name,args):
        need(not self.closed and self.kernel.GetCurrentThreadId()==self.owner,'current owned TLS thread')
        saved=ctypes.get_last_error();before=self.last_error
        try:
            # ctypes swaps its saved LastError into the actual OS thread for
            # each call and restores the caller's OS error afterward.
            ctypes.set_last_error(before)
            if name=='GetLastError':
                need(args==[],'GetLastError ABI');value=self.kernel.GetLastError()
            elif name=='TlsGetValue':
                need(args==[self.guest_index],'owned guest TLS slot role');value=self.kernel.TlsGetValue(self.index)
                need(value==self.token,'actual current TLS result must be guest context token')
            elif name=='SetLastError':
                need(len(args)==1,'SetLastError ABI');self.kernel.SetLastError(args[0]);value=0
            else:raise ValueError('undeclared actual TLS API')
            self.last_error=ctypes.get_last_error()
            receipt=dict(name=name,guest_args=args,value=value,error_before=before,error_after=self.last_error,
                         actual_native_index=self.index if name=='TlsGetValue' else None,actual_API_executed=True,
                         void_EAX_normalized=name=='SetLastError')
            self.trace.append(receipt);return value
        finally:ctypes.set_last_error(saved)

    def close(self):
        need(not self.closed and self.kernel.GetCurrentThreadId()==self.owner,'single same-thread TLS release')
        saved=ctypes.get_last_error()
        try:
            need(self.kernel.TlsSetValue(self.index,None)!=0,'clear actual owned TLS token')
            need(not self.kernel.TlsGetValue(self.index),'cleared actual TLS token')
            need(self.kernel.TlsFree(self.index)!=0,'actual TlsFree')
            value=self.kernel.TlsGetValue(self.index);error=ctypes.get_last_error();need(not value,'freed slot no guest token')
            self.closed=True;return dict(actual_clear=True,actual_free=True,freed_readback=value or 0,freed_readback_error=error,
                                         thread=self.owner,native_index=self.index,forced_cleanup=False)
        finally:ctypes.set_last_error(saved)
