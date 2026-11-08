"""Bounded foreground activation inside the qualified guest console only."""
from contextlib import contextmanager
import ctypes as C
from ctypes import wintypes as W
import time

_QUALIFICATION = None


def focus_owned_window(c, hwnd):
    from devtools.native_input_isolation import require_qualified_guest
    from tools.school_native_dialogue_input import owned_target_guard
    from tools.school_native_scene import original
    # The scope qualifies before launching the game. Do not synchronously start
    # CIM/PowerShell during the brief factory observation in members(). A guest
    # reboot necessarily ends this Python process and therefore this scope.
    qualification = _QUALIFICATION or require_qualified_guest()
    owned_target_guard(c, hwnd, False)
    getfg = original.ubind('GetForegroundWindow', W.HWND, [])
    setfg = original.ubind('SetForegroundWindow', W.BOOL, [W.HWND])
    attach = original.ubind('AttachThreadInput', W.BOOL, [W.DWORD, W.DWORD, W.BOOL])
    kernel = C.WinDLL('kernel32', use_last_error=True)
    kernel.GetCurrentThreadId.restype = W.DWORD
    kernel.GetCurrentProcessId.restype = W.DWORD
    kernel.WTSGetActiveConsoleSessionId.restype = W.DWORD
    kernel.ProcessIdToSessionId.argtypes = [W.DWORD, C.POINTER(W.DWORD)]
    kernel.ProcessIdToSessionId.restype = W.BOOL
    active = kernel.WTSGetActiveConsoleSessionId()
    current_tid = kernel.GetCurrentThreadId()
    before = getfg()
    receipt = dict(hwnd=hwnd, before=before, operations=[], guest_only=True,
                   current_tid=current_tid, console_session=active,
                   guest_uuid=qualification['current_guest_uuid'],
                   guest_boot_utc=qualification['current_guest_boot_utc'])
    def session(pid):
        value = W.DWORD()
        if not kernel.ProcessIdToSessionId(pid, C.byref(value)) or value.value != active or not active:
            raise ValueError('all activation participants must belong to the guest console session')
        return value.value
    own_pid = kernel.GetCurrentProcessId()
    receipt.update(own_pid=own_pid, own_session=session(own_pid),
                   target_pid=c.pid, target_session=session(c.pid))
    if before != hwnd:
        receipt['operations'].append(dict(name='SetForegroundWindow', result=bool(setfg(hwnd))))
    if getfg() != hwnd:
        foreground = getfg(); foreground_pid = W.DWORD()
        foreground_tid = original.ownerpid(foreground, C.byref(foreground_pid))
        if not foreground or not foreground_tid or foreground_tid == current_tid:
            raise ValueError('valid distinct current foreground guest queue required')
        attached_session = session(foreground_pid.value)
        owned_target_guard(c, hwnd, False)
        if getfg() != foreground:
            raise ValueError('guest foreground changed before attachment')
        receipt.update(attached_foreground=foreground, attached_tid=foreground_tid,
                       attached_pid=foreground_pid.value, attached_session=attached_session)
        attached = bool(attach(current_tid, foreground_tid, True))
        receipt['operations'].append(dict(name='AttachThreadInput', result=attached))
        if not attached:
            raise ValueError('guest queue attachment failed')
        try:
            owned_target_guard(c, hwnd, False)
            receipt['operations'].append(dict(name='SetForegroundWindow', result=bool(setfg(hwnd))))
        finally:
            detached = bool(attach(current_tid, foreground_tid, False))
            receipt['operations'].append(dict(name='DetachThreadInput', result=detached))
            if not detached:
                raise ValueError('guest queue detachment failed')
    # SetForegroundWindow may notify the other input queue asynchronously.
    # Wait for its actual foreground acknowledgement; never send another input.
    started = time.monotonic()
    while getfg() != hwnd and time.monotonic() - started < .30:
        time.sleep(.01)
    receipt['foreground_wait_seconds'] = time.monotonic() - started
    receipt['after'] = getfg()
    owned_target_guard(c, hwnd)
    return receipt


@contextmanager
def guest_focus_scope():
    # Scope only the focus API imported by the unchanged parent observer.
    # No frozen parent file is edited; the new implementation is recorded.
    from devtools.native_input_isolation import require_qualified_guest
    global _QUALIFICATION
    if _QUALIFICATION is not None:
        raise RuntimeError('nested guest focus scopes are not supported')
    qualification = require_qualified_guest()
    from tools import school_native_dialogue_input as inputs
    original = inputs.focus_owned_window
    _QUALIFICATION = qualification
    inputs.focus_owned_window = focus_owned_window
    try:
        yield
    finally:
        inputs.focus_owned_window = original
        _QUALIFICATION = None
