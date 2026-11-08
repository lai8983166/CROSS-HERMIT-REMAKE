"""Check that a real guest qualification refresh preserves its probe foreground."""
import argparse
import ctypes as C
from ctypes import wintypes as W
import json
import time
from pathlib import Path
from devtools.native_input_isolation import require_qualified_guest, current_machine


def run():
    qualification = require_qualified_guest()
    user = C.WinDLL('user32', use_last_error=True)
    user.CreateWindowExW.argtypes = [W.DWORD,W.LPCWSTR,W.LPCWSTR,W.DWORD,C.c_int,C.c_int,C.c_int,C.c_int,
                                    W.HWND,W.HMENU,W.HINSTANCE,W.LPVOID]
    user.CreateWindowExW.restype = W.HWND
    user.SetForegroundWindow.argtypes = [W.HWND]; user.SetForegroundWindow.restype = W.BOOL
    user.GetForegroundWindow.restype = W.HWND
    user.GetWindowThreadProcessId.argtypes = [W.HWND,C.POINTER(W.DWORD)]
    user.GetWindowThreadProcessId.restype = W.DWORD
    user.AttachThreadInput.argtypes=[W.DWORD,W.DWORD,W.BOOL]
    user.AttachThreadInput.restype=W.BOOL
    user.DestroyWindow.argtypes = [W.HWND]; user.DestroyWindow.restype = W.BOOL
    hwnd = user.CreateWindowExW(0,'STATIC','Guest query foreground probe',0x10CF0000,
                                50,50,400,120,None,None,None,None)
    if not hwnd: raise OSError('guest probe window creation failed')
    report = dict(qualification=qualification,host_input_actions=0,keyboard_mouse_actions=0,accepted=False)
    try:
        report['set_foreground'] = bool(user.SetForegroundWindow(hwnd))
        if user.GetForegroundWindow() != hwnd:
            kernel=C.WinDLL('kernel32',use_last_error=True)
            kernel.GetCurrentThreadId.restype=W.DWORD
            kernel.WTSGetActiveConsoleSessionId.restype=W.DWORD
            kernel.ProcessIdToSessionId.argtypes=[W.DWORD,C.POINTER(W.DWORD)]
            kernel.ProcessIdToSessionId.restype=W.BOOL
            pid=W.DWORD(); session=W.DWORD()
            tid=user.GetWindowThreadProcessId(user.GetForegroundWindow(),C.byref(pid))
            own=kernel.GetCurrentThreadId(); active=kernel.WTSGetActiveConsoleSessionId()
            if not tid or not active or not kernel.ProcessIdToSessionId(pid,C.byref(session)) or session.value!=active:
                raise ValueError('only same guest console foreground queue')
            report['attachment']=dict(own_tid=own,foreground_tid=tid,foreground_pid=pid.value,session=session.value)
            if not user.AttachThreadInput(own,tid,True):raise OSError('guest probe attach failed')
            try:report['attached_set_foreground']=bool(user.SetForegroundWindow(hwnd))
            finally:
                report['detached']=bool(user.AttachThreadInput(own,tid,False))
                if not report['detached']:raise OSError('guest probe detach failed')
            time.sleep(.3)
        report['before'] = user.GetForegroundWindow()
        if report['before'] != hwnd: raise ValueError('probe must already be actual guest foreground')
        report['queried_machine'] = current_machine()
        report['after'] = user.GetForegroundWindow()
        report['foreground_preserved'] = report['before'] == report['after'] == hwnd
        if not report['foreground_preserved']: raise ValueError('qualification query changed guest foreground')
    except Exception as exc:
        report['error']=repr(exc)
    finally:
        report['probe_window_destroyed'] = bool(user.DestroyWindow(hwnd))
    return report


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args(); output=args.out.resolve()
    if not output.is_relative_to(Path('C:/ChaomofaWorker')) or output.exists():
        raise ValueError('new dedicated guest report required')
    result=run()
    with output.open('x',encoding='utf8') as stream:json.dump(result,stream,indent=2)
    if result.get('error') or not result['probe_window_destroyed']: raise SystemExit(1)
