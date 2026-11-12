"""One-shot read-only RW oplock. No process attachment, input, or target writes.

Hash/identity checks must precede arm: a second data open would break our lock.
Closing the file releases/acknowledges the lock, including exceptional paths.
"""
import ctypes as C
import ctypes.wintypes as W
from pathlib import Path
import threading
import time

OPLOCK_LEVEL_CACHE_READ = 1
OPLOCK_LEVEL_CACHE_HANDLE = 2
OPLOCK_LEVEL_CACHE_WRITE = 4
RW_LEVEL = OPLOCK_LEVEL_CACHE_READ | OPLOCK_LEVEL_CACHE_WRITE
# Failed async owners stay pinned. The dedicated runner must end via ExitProcess
# (os._exit), after its other cleanup/reporting, rather than destroy these buffers.
PENDING_OWNERS = []


class Overlapped(C.Structure):
    _fields_ = [('internal', C.c_size_t), ('internal_high', C.c_size_t),
                ('offset', W.DWORD), ('offset_high', W.DWORD), ('event', W.HANDLE)]


class Input(C.Structure):
    _fields_ = [('version', W.WORD), ('length', W.WORD), ('level', W.DWORD), ('flags', W.DWORD)]


class Output(C.Structure):
    _fields_ = [('version', W.WORD), ('length', W.WORD), ('original_level', W.DWORD),
                ('new_level', W.DWORD), ('flags', W.DWORD), ('access', W.DWORD), ('share', W.WORD)]


def need(ok, text):
    if not ok:
        raise ValueError(text)


class Win:
    def __init__(self):
        self.k = C.WinDLL('kernel32', use_last_error=True)
        self.n = C.WinDLL('ntdll', use_last_error=True)
        def bind(lib, name, result, args):
            fn = getattr(lib, name); fn.restype = result; fn.argtypes = args
            return fn
        self.create_file = bind(self.k, 'CreateFileW', W.HANDLE, [W.LPCWSTR,W.DWORD,W.DWORD,C.c_void_p,W.DWORD,W.DWORD,W.HANDLE])
        self.event = bind(self.k, 'CreateEventW', W.HANDLE, [C.c_void_p,W.BOOL,W.BOOL,W.LPCWSTR])
        self.io = bind(self.k, 'DeviceIoControl', W.BOOL, [W.HANDLE,W.DWORD,C.c_void_p,W.DWORD,C.c_void_p,W.DWORD,C.c_void_p,C.POINTER(Overlapped)])
        self.wait = bind(self.k, 'WaitForSingleObject', W.DWORD, [W.HANDLE,W.DWORD])
        self.close = bind(self.k, 'CloseHandle', W.BOOL, [W.HANDLE])
        self.openp = bind(self.k, 'OpenProcess', W.HANDLE, [W.DWORD,W.BOOL,W.DWORD])
        self.opent = bind(self.k, 'OpenThread', W.HANDLE, [W.DWORD,W.BOOL,W.DWORD])
        self.thread_pid = bind(self.k, 'GetProcessIdOfThread', W.DWORD, [W.HANDLE])
        self.thread_id = bind(self.k, 'GetThreadId', W.DWORD, [W.HANDLE])
        self.exit_thread = bind(self.k, 'GetExitCodeThread', W.BOOL, [W.HANDLE,C.POINTER(W.DWORD)])
        self.exit_process = bind(self.k, 'GetExitCodeProcess', W.BOOL, [W.HANDLE,C.POINTER(W.DWORD)])
        self.suspend = bind(self.k, 'SuspendThread', W.DWORD, [W.HANDLE])
        self.resume = bind(self.k, 'ResumeThread', W.DWORD, [W.HANDLE])
        self.context = bind(self.k, 'Wow64GetThreadContext', W.BOOL, [W.HANDLE,C.c_void_p])
        self.selector = bind(self.k, 'Wow64GetThreadSelectorEntry', W.BOOL, [W.HANDLE,W.DWORD,C.c_void_p])
        self.read = bind(self.k, 'ReadProcessMemory', W.BOOL, [W.HANDLE,C.c_void_p,C.c_void_p,C.c_size_t,C.POINTER(C.c_size_t)])
        self.query = bind(self.n, 'NtQueryInformationProcess', W.LONG, [W.HANDLE,W.DWORD,C.c_void_p,W.DWORD,C.c_void_p])
        self.counter = bind(self.k, 'QueryPerformanceCounter', W.BOOL, [C.POINTER(C.c_int64)])
        self.frequency = bind(self.k, 'QueryPerformanceFrequency', W.BOOL, [C.POINTER(C.c_int64)])

    def qpc(self):
        value=C.c_int64();self.check(self.counter(C.byref(value)),'raw QPC');return value.value

    @staticmethod
    def check(ok, text):
        if not ok:
            raise OSError(C.get_last_error(), text)

    def memory(self, handle, address, size):
        need(0 < address < 0x100000000 and 0 < size <= 4096, 'bounded WOW64 read')
        buffer = C.create_string_buffer(size); got = C.c_size_t()
        self.check(self.read(handle,address,buffer,size,C.byref(got)), 'read current owner')
        need(got.value == size, 'complete owner read')
        return buffer.raw


class ReadOplock:
    """Local regular private file only. Retains async buffers until completion."""
    def __init__(self, path, max_seconds=15):
        self.path = Path(path).resolve()
        need(self.path.drive.upper() == 'F:' and self.path.is_file(), 'existing F-drive private file')
        need(0 < max_seconds <= 30, 'bounded lock lifetime')
        self.w = Win(); self.handle = None; self.event = None
        self.overlap = Overlapped(); self.output = Output()
        self.input = Input(1,C.sizeof(Input),RW_LEVEL,1)
        self.mutex = threading.Lock(); self.timer = None
        self.receipt = dict(path=str(self.path), access=0x80000000, share=7, flags=0x40000000,
                            requested_level=RW_LEVEL, arm_ns=None, break_ns=None, release_ns=None,
                            watchdog_release=False, file_closed=False, async_completed=False, event_closed=False)
        try:
            self.event = self.w.event(None,True,False,None); self.w.check(self.event,'oplock event')
            self.overlap.event = self.event
            self.handle = self.w.create_file(str(self.path),0x80000000,7,None,3,0x40000000,None)
            self.w.check(self.handle not in (None,0,C.c_void_p(-1).value), 'read-only private stream')
            ok = self.w.io(self.handle,0x90240,C.byref(self.input),C.sizeof(self.input),
                           C.byref(self.output),C.sizeof(self.output),None,C.byref(self.overlap))
            self.receipt['request_error'] = C.get_last_error()
            need(not ok and self.receipt['request_error']==997, 'RW oplock actually granted')
            self.receipt['arm_ns'] = time.perf_counter_ns()
            self.receipt['arm_qpc'] = self.w.qpc()
            self.timer = threading.Timer(max_seconds,self.release,kwargs={'watchdog':True})
            self.timer.daemon = True; self.timer.start()
        except BaseException:
            self.finish()
            raise

    def observe_break(self, timeout_ms):
        need(0 <= timeout_ms <= 15000, 'bounded break wait')
        status = self.w.wait(self.event,timeout_ms)
        need(status in (0,258), 'oplock event wait status')
        if status == 258:
            return False
        self.receipt.update(break_ns=time.perf_counter_ns(),break_qpc=self.w.qpc(), internal=int(self.overlap.internal),
                            output_hex=C.string_at(C.byref(self.output),C.sizeof(self.output)).hex())
        need(self.overlap.internal == 0 and self.output.version == 1 and self.output.length==C.sizeof(Output)
             and self.output.original_level==RW_LEVEL and self.output.flags & 1
             and not self.receipt['file_closed'], 'actual RW break requiring acknowledgment')
        return True

    def release(self, watchdog=False):
        with self.mutex:
            if self.handle and self.handle != C.c_void_p(-1).value:
                self.receipt['release_begin_qpc'] = self.w.qpc()
                self.w.check(self.w.close(self.handle),'release oplock file')
                self.handle = None
                self.receipt.update(file_closed=True,release_ns=time.perf_counter_ns(),watchdog_release=watchdog)

    def finish(self):
        # File close is the implicit ACK, NOT CancelIoEx. Keep buffers alive.
        try:
            self.release()
            if self.timer:
                self.timer.cancel()
            if self.event:
                if self.receipt['arm_ns'] is not None:
                    self.receipt['async_completed'] = self.w.wait(self.event,2000)==0
                    need(self.receipt['async_completed'],'closed oplock request completed before buffer retirement')
                self.w.check(self.w.close(self.event),'close oplock notification event')
                self.event = None; self.receipt['event_closed'] = True
        except BaseException:
            if self not in PENDING_OWNERS:
                PENDING_OWNERS.append(self)
            raise
        return dict(self.receipt)
