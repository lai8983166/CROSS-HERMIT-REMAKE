"""Read-only desktop baseline and restoration gate. Never launches a game."""
import ctypes as C
import ctypes.wintypes as W
import json
import hashlib
from pathlib import Path
import time


def snapshot():
    from tools.school_native_dialogue_desktop import desktop_status
    u = C.WinDLL('user32', use_last_error=True)
    def bind(name, result, args):
        f = getattr(u, name); f.restype = result; f.argtypes = args
        return f
    class Monitor(C.Structure):
        _fields_ = [('size', W.DWORD), ('screen', W.RECT), ('work', W.RECT),
                    ('flags', W.DWORD), ('device', W.WCHAR*32)]
    class Mode(C.Structure):
        _fields_ = [('device', W.WCHAR*32), ('spec', W.WORD), ('driver', W.WORD),
                    ('size', W.WORD), ('extra', W.WORD), ('fields', W.DWORD),
                    ('x', W.LONG), ('y', W.LONG), ('orientation', W.DWORD), ('fixed', W.DWORD),
                    ('color', W.SHORT), ('duplex', W.SHORT), ('yres', W.SHORT),
                    ('tt', W.SHORT), ('collate', W.SHORT), ('form', W.WCHAR*32),
                    ('dpi', W.WORD), ('bpp', W.DWORD), ('width', W.DWORD), ('height', W.DWORD),
                    ('flags', W.DWORD), ('frequency', W.DWORD), ('icm', W.DWORD),
                    ('intent', W.DWORD), ('media', W.DWORD), ('dither', W.DWORD),
                    ('reserved1', W.DWORD), ('reserved2', W.DWORD), ('panw', W.DWORD), ('panh', W.DWORD)]
    def rect(r): return [r.left, r.top, r.right, r.bottom]
    def checked(ok):
        if not ok: raise C.WinError(C.get_last_error())
    monitors = []; errors = []
    callback_type = C.WINFUNCTYPE(W.BOOL, W.HANDLE, W.HDC, C.POINTER(W.RECT), W.LPARAM)
    def collect(handle, dc, area, data):
        try:
            info = Monitor(); info.size = C.sizeof(info)
            checked(bind('GetMonitorInfoW', W.BOOL, [W.HANDLE, C.POINTER(Monitor)])(handle, C.byref(info)))
            mode = Mode(); mode.size = C.sizeof(mode)
            checked(bind('EnumDisplaySettingsW', W.BOOL, [W.LPCWSTR, W.DWORD, C.POINTER(Mode)])(
                info.device, 0xffffffff, C.byref(mode)))
            monitors.append(dict(device=info.device, screen=rect(info.screen), work=rect(info.work),
                primary=bool(info.flags & 1), mode={k:getattr(mode, k) for k in
                    ('width', 'height', 'bpp', 'frequency', 'x', 'y', 'orientation', 'fixed')}))
            return True
        except Exception as exc:
            errors.append(repr(exc)); return False
    callback = callback_type(collect)
    ok = bind('EnumDisplayMonitors', W.BOOL, [W.HDC, C.c_void_p, callback_type, W.LPARAM])(
        None, None, callback, 0)
    if errors: raise RuntimeError(errors[0])
    checked(ok)
    find = bind('FindWindowW', W.HWND, [W.LPCWSTR, W.LPCWSTR])
    visible = bind('IsWindowVisible', W.BOOL, [W.HWND])
    window_rect = bind('GetWindowRect', W.BOOL, [W.HWND, C.POINTER(W.RECT)])
    bars = []
    def bar_record(hwnd):
        r = W.RECT(); checked(window_rect(hwnd, C.byref(r)))
        pid = W.DWORD()
        bind('GetWindowThreadProcessId', W.DWORD, [W.HWND, C.POINTER(W.DWORD)])(hwnd, C.byref(pid))
        bars.append(dict(hwnd=hwnd, pid=pid.value, visible=bool(visible(hwnd)), rect=rect(r),
            hung=bool(bind('IsHungAppWindow', W.BOOL, [W.HWND])(hwnd))))
    primary = find('Shell_TrayWnd', None)
    if primary: bar_record(primary)
    next_window = bind('FindWindowExW', W.HWND, [W.HWND, W.HWND, W.LPCWSTR, W.LPCWSTR])
    previous = None
    while True:
        h = next_window(None, previous, 'Shell_SecondaryTrayWnd', None)
        if not h: break
        bar_record(h); previous = h
        if len(bars) > 16: raise ValueError('unexpected taskbar window count')
    class Appbar(C.Structure):
        _fields_ = [('size', W.DWORD), ('hwnd', W.HWND), ('callback', W.UINT),
                    ('edge', W.UINT), ('rect', W.RECT), ('param', W.LPARAM)]
    data = Appbar(); data.size = C.sizeof(data)
    shell = C.WinDLL('shell32'); fn = shell.SHAppBarMessage
    fn.argtypes = [W.DWORD, C.POINTER(Appbar)]; fn.restype = C.c_size_t
    state = fn(4, C.byref(data))
    metric = bind('GetSystemMetrics', C.c_int, [C.c_int])
    return dict(time_ns=time.time_ns(), monitors=sorted(monitors, key=lambda m:m['device']),
        taskbars=bars, appbar_state=state, auto_hide=bool(state & 1),
        metrics={str(i):metric(i) for i in (0, 1, 76, 77, 78, 79, 80)},
        input_desktop=desktop_status(), shell_window=bind('GetShellWindow', W.HWND, [])() or 0,
        game_window=find('Cross Hermit', None) or 0, desktop_state_written=False)


def health(state):
    issues = []
    if not state['monitors']: issues.append('no_monitors')
    if not state['shell_window']: issues.append('shell_missing')
    if not state['input_desktop']['ready']: issues.append('input_desktop_unavailable')
    if state['game_window']: issues.append('game_window_remaining')
    if not state['taskbars']: issues.append('taskbar_missing')
    for m in state['monitors']:
        l,t,r,b=m['screen']; wl,wt,wr,wb=m['work']
        if not (l <= wl < wr <= r and t <= wt < wb <= b):
            issues.append('invalid_work_area')
        if not state['auto_hide'] and m.get('primary') and m['work'] == m['screen']:
            issues.append('primary_taskbar_work_area_missing')
    for bar in state['taskbars']:
        l, t, r, b = bar['rect']
        if bar['hung']: issues.append('taskbar_unresponsive')
        if not state['auto_hide'] and (not bar['visible'] or min(r-l, b-t) <= 1):
            issues.append('taskbar_collapsed_or_hidden')
        if not any(l < m['screen'][2] and r > m['screen'][0]
                   and t < m['screen'][3] and b > m['screen'][1] for m in state['monitors']):
            issues.append('taskbar_offscreen')
    return sorted(set(issues))


def differences(before, after):
    issues = health(after)
    for key in ('monitors', 'metrics', 'appbar_state'):
        if before[key] != after[key]: issues.append(key+'_changed')
    geometry = lambda s: sorted((tuple(x['rect']), x['visible']) for x in s['taskbars'])
    if geometry(before) != geometry(after): issues.append('taskbar_geometry_changed')
    for key in ('input_desktop', 'observer_desktop'):
        if before['input_desktop'][key] != after['input_desktop'][key]:
            issues.append(key+'_changed')
    # PID/HWND may legitimately change if the shell restarts. Geometry and health
    # must still match. Foreground restoration is independently checked below.
    for key in ('foreground_hwnd', 'foreground_pid'):
        if before['input_desktop'][key] != after['input_desktop'][key]:
            issues.append(key+'_changed')
    return sorted(set(issues))


def guarded_run(action, receipt, *, read=snapshot, sleep=time.sleep):
    path = Path(receipt)
    if path.exists(): raise ValueError('fresh desktop receipt required')
    before = read()
    implementation = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    report = dict(before=before, after=[], restored=False, checks=[], action_error=None,
                  observer_sha256=implementation)
    result = None
    try:
        faults = health(before)
        if faults: raise RuntimeError('desktop baseline rejected: '+','.join(faults))
        result = action()
    except BaseException as exc:
        report['action_error'] = repr(exc)
        raise
    finally:
        try:
            for i in range(2):
                if i: sleep(1)
                after = read(); report['after'].append(after)
                report['checks'].append(differences(before, after))
            report['restored'] = not health(before) and all(not x for x in report['checks'])
            if hashlib.sha256(Path(__file__).read_bytes()).hexdigest() != implementation:
                report['restored'] = False
                raise RuntimeError('desktop observer changed during run')
        except BaseException as exc:
            report['audit_error'] = repr(exc)
        with path.open('x', encoding='utf8') as stream:
            json.dump(report, stream, ensure_ascii=False, indent=2)
    if not report['restored']:
        raise RuntimeError('desktop restoration not verified; see '+str(path))
    return result
