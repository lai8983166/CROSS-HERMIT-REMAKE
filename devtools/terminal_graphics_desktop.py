"""GAME parent recovery: implementation present, native admission deliberately closed.

There is no launcher or CLI. Import and all offline models perform no desktop IO.
WindowsBackend reuses the frozen window observer, but cannot be instantiated while
NATIVE_ADMISSION is false. Native qualification additionally needs the external
bounded helper/Job supervisor; Budget below cannot interrupt a blocked driver API.
"""
from __future__ import annotations

import copy
import ctypes as C
import ctypes.wintypes as W
import hashlib
import json
import time

from devtools import terminal_window_desktop as frozen

NATIVE_ADMISSION = False
SCHEMA = 'terminal-graphics-release-v1'
GAMMA_BYTES = 1536
MAX_RECOVERY_SECONDS = 20
need = frozen.need


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=True).encode('ascii')).hexdigest()


def ramp(value):
    need(isinstance(value, str) and len(value) == 2 * GAMMA_BYTES, 'complete original 1536-byte gamma')
    raw = bytes.fromhex(value)
    need(len(raw) == GAMMA_BYTES, 'gamma byte length')
    return raw


class Budget:
    def __init__(self, seconds=10, *, clock=time.monotonic, max_operations=40):
        need(0 < seconds <= MAX_RECOVERY_SECONDS, 'bounded recovery time')
        need(1 <= max_operations <= 64, 'bounded recovery operation count')
        self.clock, self.deadline = clock, clock() + seconds
        self.remaining = max_operations

    def check(self):
        need(self.clock() < self.deadline, 'recovery deadline exceeded')
        need(self.remaining > 0, 'recovery operation budget exhausted')
        self.remaining -= 1


def capture_baseline(backend, target_device, owner):
    """Call before any D3D factory/device, then register token with GFX_BASELINE.

    The owner must already be identified, but need not have created its window.
    Model snapshots remain explicitly model observations and cannot admit native.
    """
    need(set(owner) == {'run_id', 'pid', 'process_created', 'main_tid', 'main_teb'}, 'complete owner lifetime')
    need(all(owner.values()), 'nonzero owner lifetime')
    state = backend.read(target_device)
    need(not frozen.previous.health(state), 'healthy desktop before device creation')
    need(target_device in state['display_identities'], 'target display present')
    need(state['graphics']['device'] == target_device, 'gamma target display')
    ramp(state['graphics']['gamma_hex'])
    need(state['input_observer']['last_input_tick'] == state['last_input_tick'], 'same LastInput observation')
    need(state['cursor']['flags'] in (0, 1), 'cursor suppression is not qualified')
    value = dict(schema='terminal-graphics-baseline-v1', evidence_kind=backend.evidence_kind,
                 owner=copy.deepcopy(owner), target_device=target_device, state=state)
    value['baseline_token'] = digest(value)
    return value


def validate_release_receipt(receipt, baseline, *, evidence_kind):
    """Validate a runner's ordered aggregation, never synthesize native success.

    Source refs identify immutable raw wire/Job observations. Native authentication
    and complete ledger reconstruction belong to the independent runner audit;
    this shape/order check alone is expressly insufficient for native admission.
    """
    core = {key: val for key, val in baseline.items() if key != 'baseline_token'}
    need(digest(core) == baseline['baseline_token'], 'baseline token changed')
    need(receipt['schema'] == SCHEMA, 'release receipt schema')
    need(receipt['evidence_kind'] == baseline['evidence_kind'] == evidence_kind, 'model/native evidence separation')
    if evidence_kind == 'native':
        need(NATIVE_ADMISSION, 'native graphics recovery not admitted')
    need(receipt['owner'] == baseline['owner'], 'same MAIN/process lifetime')
    need(receipt['baseline_token'] == baseline['baseline_token'], 'native registered baseline token')
    need(receipt['window_identity']['hwnd'] and receipt['window_identity']['generation'], 'owned window lifetime')
    events = receipt['events']
    need(6 <= len(events) <= 32, 'bounded actual release events')
    need(all(e['observed'] is True and e['source_ref'] and e['baseline_token'] == baseline['baseline_token']
             for e in events), 'actual source-linked release observations')
    need(all(a['seq'] < b['seq'] for a, b in zip(events, events[1:])), 'strict release event order')
    kinds = [e['kind'] for e in events]
    required = ('input_unacquire', 'input_release', 'graphics_gamma_restore',
                'graphics_release', 'window_destroy', 'job_empty')
    need(all(kinds.count(kind) == 1 for kind in required), 'one complete cleanup summary per phase')
    selected = {kind: events[kinds.index(kind)] for kind in required}
    need([selected[k]['seq'] for k in required] == sorted(selected[k]['seq'] for k in required),
         'input release before graphics/window/Job teardown')
    for kind in ('input_unacquire', 'input_release', 'graphics_gamma_restore', 'graphics_release'):
        need(selected[kind]['window_alive'] is True, 'input/device cleanup while original window alive')
        need(selected[kind]['main_tid'] == baseline['owner']['main_tid'] and
             selected[kind]['main_teb'] == baseline['owner']['main_teb'], 'cleanup same MAIN TID/TEB')
        need(selected[kind]['window_identity'] == receipt['window_identity'], 'cleanup same owned window lifetime')
    inp = selected['input_unacquire']
    need(inp['hresults'] and all(x in (0, 1) for x in inp['hresults']), 'actual DirectInput Unacquire success/S_FALSE')
    need(selected['input_release']['remaining_refs'] == 0 and selected['input_release']['objects'] >= 1,
         'all input objects released')
    gamma = selected['graphics_gamma_restore']
    need(gamma['device_alive'] is True and gamma['saved_hex'] == gamma['readback_hex'], 'device gamma actual readback')
    ramp(gamma['saved_hex'])
    gfx = selected['graphics_release']
    need(gfx['remaining_refs'] == 0 and gfx['live_resources'] == 0 and gfx['locked_resources'] == 0,
         'all graphics references/locks released')
    need(selected['window_destroy']['is_window'] is False and selected['window_destroy']['destroy_result'] == 1,
         'actual owned window destroyed')
    need(selected['window_destroy']['window_identity'] == receipt['window_identity'], 'destroyed original owned window')
    need(selected['job_empty']['active_processes'] == 0, 'actual Job empty before any parent restoration')
    cursor = receipt['owner_cursor_receipt']
    need(cursor['source_ref'] and cursor['main_tid'] == baseline['owner']['main_tid'] and
         cursor['main_teb'] == baseline['owner']['main_teb'] and cursor['net_showcursor_delta'] == 0 and
         cursor['flags'] == baseline['state']['cursor']['flags'] and
         cursor['handle'] == baseline['state']['cursor']['handle'],
         'owner cursor visibility count balanced before thread exit')
    need(set(receipt['mutation_sources']) == set(receipt['mutations']), 'source for every attributed mutation')
    for source in receipt['mutation_sources'].values():
        need(source['source_ref'] and source['owner'] == baseline['owner'] and
             source['baseline_token'] == baseline['baseline_token'], 'mutation source bound to owner/baseline')
    return selected


def _mode(state, device):
    return next(m['mode'] for m in state['monitors'] if m['device'] == device)


def _mutable(state, device):
    return dict(mode=_mode(state, device), gamma=state['graphics']['gamma_hex'],
                cursor_clip=state['cursor']['clip'], cursor_position=state['cursor']['position'],
                taskbars=state['taskbars'], work_area=state['system_work_area'],
                foreground=state['foreground_identity'])


def _context(before, state, device):
    need(state['input_desktop']['ready'] and not state['game_window'], 'same unlocked desktop, no live game window')
    need(state['shell_window'] == before['shell_window'] and not any(x['hung'] for x in state['taskbars']),
         'same responsive shell before restoration')
    need(state['original_foreground_identity'] == before['foreground_identity'],
         'original foreground lifetime changed: no overwrite')
    for key in ('input_desktop', 'observer_desktop'):
        need(state['input_desktop'][key] == before['input_desktop'][key], 'input desktop identity changed')
    need(state['input_observer'] == before['input_observer'], 'new user input or observer lifetime changed')
    need(state['last_input_tick'] == before['last_input_tick'], 'new user input')
    need(0 <= state['tick64'] - before['tick64'] < 120_000, 'bounded LastInput identity age')
    for key in ('display_identities', 'shell_identity', 'taskbar_identities', 'appbar_state'):
        need(state[key] == before[key], key + ' changed: no overwrite')
    need(state['graphics']['device'] == device, 'gamma display changed')
    need(state['cursor']['flags'] == before['cursor']['flags'] and
         state['cursor']['handle'] == before['cursor']['handle'],
         'cursor shape/visibility not restored by original owner')
    need({m['device'] for m in state['monitors']} == {m['device'] for m in before['monitors']}, 'monitor topology changed')
    for monitor in before['monitors']:
        if monitor['device'] != device:
            need(_mode(state, monitor['device']) == monitor['mode'], 'unowned display mode changed')


def recover(baseline, receipt, backend, *, budget=None, sleep=time.sleep):
    """Restore only attributed values; preserve a bounded failure receipt.

    Mode restoration may reset gamma. Thus gamma is read after mode readback,
    restored from the original bytes (never a linear substitute), and read again.
    A successful BOOL is recorded but never sufficient. No retry loop is used.
    """
    report = dict(schema='terminal-graphics-recovery-v1', evidence_kind=backend.evidence_kind,
                  baseline_token=baseline['baseline_token'], native_admission=False,
                  restored=False, actions=[], observations=[], checks=[], error=None,
                  unrestored=['not_observed'])
    budget = budget or Budget()
    before, device = baseline['state'], baseline['target_device']
    try:
        validate_release_receipt(receipt, baseline, evidence_kind=backend.evidence_kind)
        def read():
            budget.check()
            state = backend.read(device, foreground_identity=before['foreground_identity'])
            report['observations'].append(dict(state_sha256=digest(state), tick64=state['tick64'],
                mode=_mode(state, device), gamma_hex=state['graphics']['gamma_hex'],
                cursor=copy.deepcopy(state['cursor']), last_input_tick=state['last_input_tick']))
            report['unrestored'] = [key for key, value in _mutable(state, device).items()
                                    if value != _mutable(before, device)[key]]
            _context(before, state, device)
            return state
        state = read()
        original, expected = _mutable(before, device), _mutable(state, device)
        mutations = receipt['mutations']
        need(set(mutations) <= set(original), 'no unapproved mutation field')
        for key, value in expected.items():
            need(value == original[key] or (key in mutations and value == mutations[key]),
                 key + ': current state not attributable to this run')

        def write(kind, value):
            nonlocal state, expected
            state = read()
            need(_mutable(state, device) == expected, 'state changed since attribution: no overwrite')
            budget.check()
            action = dict(kind=kind, attempted=True, actual_return=None)
            report['actions'].append(action)
            result = backend.write(kind, value, device=device, baseline=before)
            action['actual_return'] = result
            state = read()
            actual = _mutable(state, device)
            need(actual[kind] == value, kind + ': actual readback mismatch')
            if kind == 'mode':
                # A display change may reset gamma. Refuse other new differences
                # rather than assume unrelated shell/cursor changes are ours.
                need(actual['foreground'] == expected['foreground'], 'mode changed foreground lifetime')
                need(actual['cursor_position'] == expected['cursor_position'], 'mode changed cursor position: refuse guess')
                for key in ('cursor_clip', 'taskbars', 'work_area'):
                    need(actual[key] in (expected[key], original[key]), key + ': unowned side effect of mode change')
            else:
                for key in actual:
                    need(key == kind or actual[key] == expected[key], key + ': concurrent state change')
            expected = actual

        if expected['mode'] != original['mode']:
            write('mode', original['mode'])
        need(_mode(state, device) == original['mode'], 'mode readback precedes final gamma')
        if expected['gamma'] != original['gamma']:
            write('gamma', original['gamma'])
        # Clip first: SetCursorPos is otherwise clamped to the test's old clip.
        for kind in ('cursor_clip', 'cursor_position', 'taskbars', 'work_area', 'foreground'):
            if expected[kind] != original[kind]:
                write(kind, original[kind])
        for index in range(2):
            if index:
                budget.check()
                sleep(.5)
            state = read()
            issues = frozen.differences(before, state)
            for key, value in _mutable(state, device).items():
                if value != original[key]:
                    issues.append(key + '_changed')
            report['checks'].append(sorted(set(issues)))
        report['restored'] = all(not check for check in report['checks'])
        need(report['restored'], 'two stable actual readbacks required')
    except Exception as exc:
        report['error'] = str(exc)
        report['restored'] = False
    return report


class WindowsBackend(frozen.Desktop):
    """Concrete unexecuted Win32 implementation, with a closed qualification gate.

    No ShowCursor/SetCursor calls here: visibility is a per-owner-thread count,
    and a saved opaque HCURSOR is not a license to change another owner's shape.
    No input injection, Explorer restart, forced focus, or registry writes.
    """
    evidence_kind = 'native'

    def __init__(self, *, armed=False):
        need(NATIVE_ADMISSION and armed, 'native recovery closed: no qualified bounded launch contract')
        super().__init__()
        self.g = C.WinDLL('gdi32', use_last_error=True)

    def _display_identity(self, device):
        class DisplayDevice(C.Structure):
            _fields_ = [('size', W.DWORD), ('name', W.WCHAR * 32), ('description', W.WCHAR * 128),
                        ('flags', W.DWORD), ('device_id', W.WCHAR * 128), ('key', W.WCHAR * 128)]
        fn = self.fn(self.u, 'EnumDisplayDevicesW', W.BOOL,
                     [W.LPCWSTR, W.DWORD, C.POINTER(DisplayDevice), W.DWORD])
        def enumeration(parent):
            found = []
            for index in range(17):
                item = DisplayDevice()
                item.size = C.sizeof(item)
                if not fn(parent, index, C.byref(item), 1):
                    break
                need(index < 16, 'bounded display identity count')
                found.append({key: getattr(item, key) for key in ('name', 'description', 'flags', 'device_id', 'key')})
            return found
        adapter = next((x for x in enumeration(None) if x['name'] == device), None)
        need(adapter is not None, 'target adapter identity')
        monitors = enumeration(device)
        need(monitors, 'target monitor hardware identity')
        return dict(adapter=adapter, monitors=monitors)

    def _gamma(self, device, value=None):
        raw = (C.c_ubyte * GAMMA_BYTES)()
        if value is not None:
            raw[:] = ramp(value)
        dc = self.fn(self.g, 'CreateDCW', W.HDC,
                     [W.LPCWSTR, W.LPCWSTR, W.LPCWSTR, C.c_void_p])('DISPLAY', device, None, None)
        self.checked(dc)
        try:
            name = 'GetDeviceGammaRamp' if value is None else 'SetDeviceGammaRamp'
            result = self.fn(self.g, name, W.BOOL, [W.HDC, C.c_void_p])(dc, C.byref(raw))
            self.checked(result)
            return bytes(raw).hex() if value is None else int(result)
        finally:
            self.checked(self.fn(self.g, 'DeleteDC', W.BOOL, [W.HDC])(dc))

    def read(self, device, *, foreground_identity=None):
        start = self.last_input()
        out = super().read()
        out['display_identities'] = {m['device']: self._display_identity(m['device']) for m in out['monitors']}
        out['shell_identity'] = self.identity(out['shell_window'])
        out['original_foreground_identity'] = self.identity(foreground_identity['hwnd']) if foreground_identity else copy.deepcopy(out['foreground_identity'])
        class CursorInfo(C.Structure):
            _fields_ = [('size', W.DWORD), ('flags', W.DWORD), ('handle', W.HANDLE), ('point', W.POINT)]
        cursor = CursorInfo()
        cursor.size = C.sizeof(cursor)
        self.checked(self.fn(self.u, 'GetCursorInfo', W.BOOL, [C.POINTER(CursorInfo)])(C.byref(cursor)))
        clip = W.RECT()
        self.checked(self.fn(self.u, 'GetClipCursor', W.BOOL, [C.POINTER(W.RECT)])(C.byref(clip)))
        out['cursor'] = dict(flags=cursor.flags, handle=cursor.handle or 0,
                             position=[cursor.point.x, cursor.point.y], clip=[clip.left, clip.top, clip.right, clip.bottom])
        out['graphics'] = dict(device=device, gamma_hex=self._gamma(device))
        pid = self.fn(self.k, 'GetCurrentProcessId', W.DWORD, [])()
        process = self.fn(self.k, 'GetCurrentProcess', W.HANDLE, [])()
        times = [W.FILETIME() for _ in range(4)]
        self.checked(self.fn(self.k, 'GetProcessTimes', W.BOOL,
                            [W.HANDLE] + [C.POINTER(W.FILETIME)] * 4)(process, *[C.byref(x) for x in times]))
        session = W.DWORD()
        self.checked(self.fn(self.k, 'ProcessIdToSessionId', W.BOOL, [W.DWORD, C.POINTER(W.DWORD)])(pid, C.byref(session)))
        out['tick64'] = self.fn(self.k, 'GetTickCount64', C.c_ulonglong, [])()
        finish = self.last_input()
        need(start == out['last_input_tick'] == finish, 'user input during desktop observation')
        out['input_observer'] = dict(pid=pid, process_created=times[0].dwLowDateTime | times[0].dwHighDateTime << 32,
                                     session_id=session.value, last_input_tick=finish)
        return out

    def write(self, kind, value, *, device, baseline):
        # Only recover() may call these primitives after receipt/context guards.
        need(NATIVE_ADMISSION, 'native restoration remains closed')
        if kind == 'mode':
            mode = frozen.Mode.from_buffer_copy(bytes.fromhex(baseline['mode_bytes'][device]))
            need(mode.size == C.sizeof(mode) and mode.extra == 0, 'complete original DEVMODE')
            result = self.fn(self.u, 'ChangeDisplaySettingsExW', W.LONG,
                             [W.LPCWSTR, C.POINTER(frozen.Mode), W.HWND, W.DWORD, C.c_void_p])(
                                 device, C.byref(mode), None, 0, None)
            need(result == 0, 'display mode API failed')
            return int(result)
        if kind == 'gamma':
            return self._gamma(device, value)
        if kind == 'cursor_clip':
            rect = W.RECT(*value)
            return int(self.checked(self.fn(self.u, 'ClipCursor', W.BOOL, [C.POINTER(W.RECT)])(C.byref(rect))))
        if kind == 'cursor_position':
            return int(self.checked(self.fn(self.u, 'SetCursorPos', W.BOOL, [C.c_int, C.c_int])(*value)))
        if kind == 'taskbars':
            need(not baseline['auto_hide'], 'do not override automatic shell policy')
            results = []
            for bar in value:
                need(self.last_input() == baseline['last_input_tick'], 'new user input during taskbar repair')
                token = next(x for x in baseline['taskbar_identities'] if x['hwnd'] == bar['hwnd'])
                need(self.identity(bar['hwnd']) == token and self.identity(baseline['shell_window']) == baseline['shell_identity'],
                     'taskbar/shell lifetime changed during repair')
                l, t, r, b = bar['rect']
                flags = 0x0004 | 0x0010 | (0x0040 if bar['visible'] else 0x0080)
                results.append(int(self.checked(self.fn(self.u, 'SetWindowPos', W.BOOL,
                    [W.HWND, W.HWND, C.c_int, C.c_int, C.c_int, C.c_int, W.UINT])(
                    bar['hwnd'], None, l, t, r-l, b-t, flags))))
            return results
        if kind == 'work_area':
            rect = W.RECT(*value)
            return int(self.checked(self.fn(self.u, 'SystemParametersInfoW', W.BOOL,
                [W.UINT, W.UINT, C.c_void_p, W.UINT])(0x2f, 0, C.byref(rect), 0)))
        if kind == 'foreground':
            need(self.identity(value['hwnd']) == value, 'original foreground lifetime changed')
            return int(self.fn(self.u, 'SetForegroundWindow', W.BOOL, [W.HWND])(value['hwnd']))
        raise ValueError('unapproved desktop write ' + kind)
