"""Read actual DEP policy of the exact private guest image; never modifies it."""
import ctypes as C
from ctypes import wintypes as W
import hashlib
from pathlib import Path
import threading
import time


class DepObserver:
    def __init__(self):
        self.stop = threading.Event()
        self.rows = []
        self.error = None
        self.thread = threading.Thread(target=self.observe, daemon=True)

    def observe(self):
        try:
            from devtools.native_input_isolation import require_qualified_guest
            require_qualified_guest()
            image = Path('C:/ChaomofaWorker/project/.venv-audit/scene-callback-runtime/CROSS HERMIT/CROSS HERMIT/CROSS HERMIT.EXE')
            sha = hashlib.sha256(image.read_bytes()).hexdigest()
            if sha != '030dca584a3a0b20751a72609f7acc823e8d79d820cebf1fcde8be6a791a9df7':
                raise ValueError('original private image identity')
            kernel = C.WinDLL('kernel32', use_last_error=True)
            psapi = C.WinDLL('psapi', use_last_error=True)
            psapi.EnumProcesses.argtypes = [C.POINTER(W.DWORD), W.DWORD, C.POINTER(W.DWORD)]
            psapi.EnumProcesses.restype = W.BOOL
            kernel.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
            kernel.OpenProcess.restype = W.HANDLE
            kernel.CloseHandle.argtypes = [W.HANDLE]
            kernel.CloseHandle.restype = W.BOOL
            kernel.QueryFullProcessImageNameW.argtypes = [W.HANDLE, W.DWORD, W.LPWSTR, C.POINTER(W.DWORD)]
            kernel.QueryFullProcessImageNameW.restype = W.BOOL
            kernel.GetProcessDEPPolicy.argtypes = [W.HANDLE, C.POINTER(W.DWORD), C.POINTER(W.BOOL)]
            kernel.GetProcessDEPPolicy.restype = W.BOOL
            seen = set()
            started = time.monotonic()
            while not self.stop.is_set() and time.monotonic() - started < 240:
                ids = (W.DWORD * 4096)(); used = W.DWORD()
                if not psapi.EnumProcesses(ids, C.sizeof(ids), C.byref(used)) or used.value >= C.sizeof(ids):
                    raise OSError('bounded process enumeration failed')
                for pid in ids[:used.value // C.sizeof(W.DWORD)]:
                    if pid in seen:
                        continue
                    handle = kernel.OpenProcess(0x400, False, pid)
                    if not handle:
                        continue
                    try:
                        path = C.create_unicode_buffer(32768); size = W.DWORD(len(path))
                        if kernel.QueryFullProcessImageNameW(handle, 0, path, C.byref(size)) and path.value.lower() == str(image).lower():
                            flags = W.DWORD(); permanent = W.BOOL()
                            ok = bool(kernel.GetProcessDEPPolicy(handle, C.byref(flags), C.byref(permanent)))
                            self.rows.append(dict(pid=pid, image_path=path.value, image_sha256=sha,
                                elapsed=round(time.monotonic()-started, 6), query_ok=ok,
                                flags=flags.value, permanent=bool(permanent.value), error=0 if ok else C.get_last_error()))
                            seen.add(pid)
                    finally:
                        if not kernel.CloseHandle(handle):
                            raise OSError('process observer handle cleanup failed')
                if len(self.rows) > 16:
                    raise ValueError('bounded original process observations')
                self.stop.wait(.25)
        except Exception as exc:
            self.error = str(exc)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *args):
        self.stop.set()
        self.thread.join(25)
        if self.thread.is_alive():
            self.error = 'process observer failed to stop'
