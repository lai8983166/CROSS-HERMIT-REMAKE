"""Bounded baseline restoration for an explicitly authorized owned-window run.

Importing does nothing to the desktop. No screenshot, input injection, process
restart, registry setting, or forced focus attachment is used. Repairs require
proof that the test Job is empty and that no newer user input has arrived.
"""
from __future__ import annotations
import ctypes as C
import ctypes.wintypes as W
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

from devtools import terminal_host_desktop as previous


class Mode(C.Structure):
    _fields_ = [('device', W.WCHAR*32), ('spec', W.WORD), ('driver', W.WORD),
                ('size', W.WORD), ('extra', W.WORD), ('fields', W.DWORD),
                ('x', W.LONG), ('y', W.LONG), ('orientation', W.DWORD), ('fixed', W.DWORD),
                ('color', W.SHORT), ('duplex', W.SHORT), ('yres', W.SHORT), ('tt', W.SHORT),
                ('collate', W.SHORT), ('form', W.WCHAR*32), ('dpi', W.WORD), ('bpp', W.DWORD),
                ('width', W.DWORD), ('height', W.DWORD), ('flags', W.DWORD), ('frequency', W.DWORD),
                ('icm', W.DWORD), ('intent', W.DWORD), ('media', W.DWORD), ('dither', W.DWORD),
                ('reserved1', W.DWORD), ('reserved2', W.DWORD), ('panw', W.DWORD), ('panh', W.DWORD)]


def need(value, message):
    if not value:
        raise ValueError(message)


class Desktop:
    def __init__(self):
        self.u = C.WinDLL('user32', use_last_error=True)
        self.k = C.WinDLL('kernel32', use_last_error=True)

    def fn(self, lib, name, result, args):
        f = getattr(lib, name)
        f.restype, f.argtypes = result, args
        return f

    def checked(self, result):
        if not result:
            raise C.WinError(C.get_last_error())
        return result

    def last_input(self):
        class LastInput(C.Structure):
            _fields_ = [('size', W.UINT), ('tick', W.DWORD)]
        value = LastInput(C.sizeof(LastInput), 0)
        self.checked(self.fn(self.u, 'GetLastInputInfo', W.BOOL, [C.POINTER(LastInput)])(C.byref(value)))
        return value.tick

    def identity(self, hwnd):
        need(hwnd, 'nonzero saved window')
        pid = W.DWORD()
        tid = self.fn(self.u, 'GetWindowThreadProcessId', W.DWORD, [W.HWND, C.POINTER(W.DWORD)])(hwnd, C.byref(pid))
        self.checked(tid)
        cls = C.create_unicode_buffer(256)
        self.checked(self.fn(self.u, 'GetClassNameW', C.c_int, [W.HWND, W.LPWSTR, C.c_int])(hwnd, cls, len(cls)))
        handle = self.fn(self.k, 'OpenProcess', W.HANDLE, [W.DWORD, W.BOOL, W.DWORD])(0x1000, False, pid.value)
        self.checked(handle)
        values = [W.FILETIME() for _ in range(4)]
        try:
            self.checked(self.fn(self.k, 'GetProcessTimes', W.BOOL, [W.HANDLE] + [C.POINTER(W.FILETIME)]*4)(handle, *[C.byref(v) for v in values]))
        finally:
            self.checked(self.fn(self.k, 'CloseHandle', W.BOOL, [W.HANDLE])(handle))
        return dict(hwnd=hwnd, pid=pid.value, tid=tid, window_class=cls.value,
                    process_created=values[0].dwLowDateTime | values[0].dwHighDateTime << 32)

    def read(self):
        out = previous.snapshot()
        out['last_input_tick'] = self.last_input()
        out['foreground_identity'] = self.identity(out['input_desktop']['foreground_hwnd'])
        out['taskbar_identities'] = [self.identity(b['hwnd']) for b in out['taskbars']]
        out['mode_bytes'] = {}
        need(len(out['monitors']) <= 16, 'bounded monitor count')
        for monitor in out['monitors']:
            mode = Mode()
            mode.size = C.sizeof(mode)
            self.checked(self.fn(self.u, 'EnumDisplaySettingsW', W.BOOL, [W.LPCWSTR, W.DWORD, C.POINTER(Mode)])(
                monitor['device'], 0xffffffff, C.byref(mode)))
            need(not mode.extra, 'no unrecorded display driver private bytes')
            out['mode_bytes'][monitor['device']] = bytes(mode).hex()
        work = W.RECT()
        self.checked(self.fn(self.u, 'SystemParametersInfoW', W.BOOL, [W.UINT, W.UINT, C.c_void_p, W.UINT])(
            0x30, 0, C.byref(work), 0))
        out['system_work_area'] = [work.left, work.top, work.right, work.bottom]
        return out

    def repair(self, before, after):
        actions = []
        self.recovery_actions = actions
        def guard():
            need(self.last_input() == before['last_input_tick'], 'new user input: no desktop writes')
            current = previous.snapshot()
            need(current['input_desktop']['ready'] and
                 current['input_desktop']['input_desktop'] == before['input_desktop']['input_desktop'] and
                 current['input_desktop']['observer_desktop'] == before['input_desktop']['observer_desktop'],
                 'same unlocked desktop for restoration')
            need(not current['game_window'] and current['shell_window'] == before['shell_window'],
                 'owned test window gone and original shell retained')
            need(current['appbar_state'] == before['appbar_state'], 'taskbar user policy changed: refuse overwrite')
            return current
        current = guard()
        need({m['device'] for m in current['monitors']} == {m['device'] for m in before['monitors']}, 'same monitor topology')
        for monitor in before['monitors']:
            now = next(m for m in current['monitors'] if m['device'] == monitor['device'])
            if now['mode'] == monitor['mode']:
                continue
            guard()
            mode = Mode.from_buffer_copy(bytes.fromhex(before['mode_bytes'][monitor['device']]))
            need(mode.size == C.sizeof(Mode) and mode.extra == 0, 'complete saved DEVMODE')
            result = self.fn(self.u, 'ChangeDisplaySettingsExW', W.LONG,
                             [W.LPCWSTR, C.POINTER(Mode), W.HWND, W.DWORD, C.c_void_p])(
                                 monitor['device'], C.byref(mode), None, 0, None)
            actions.append(dict(api='ChangeDisplaySettingsExW', device=monitor['device'], result=result, registry_written=False))
            need(result == 0, 'saved display mode restoration succeeded')
        current = guard()
        for bar, token in zip(before['taskbars'], before['taskbar_identities']):
            observed = next((b for b in current['taskbars'] if b['hwnd'] == bar['hwnd']), None)
            need(observed is not None and self.identity(bar['hwnd']) == token and not observed['hung'], 'same responsive taskbar owner')
            if (observed['rect'], observed['visible']) == (bar['rect'], bar['visible']):
                continue
            need(not before['auto_hide'], 'auto-hide geometry is controlled by shell policy')
            guard()
            left, top, right, bottom = bar['rect']
            flags = 0x0004 | 0x0010 | (0x0040 if bar['visible'] else 0x0080)
            result = self.fn(self.u, 'SetWindowPos', W.BOOL,
                             [W.HWND, W.HWND, C.c_int, C.c_int, C.c_int, C.c_int, W.UINT])(
                                 bar['hwnd'], None, left, top, right-left, bottom-top, flags)
            actions.append(dict(api='SetWindowPos', hwnd=bar['hwnd'], result=int(result), no_activate=True, no_zorder=True))
            self.checked(result)
        guard()
        work = W.RECT()
        spi = self.fn(self.u, 'SystemParametersInfoW', W.BOOL, [W.UINT, W.UINT, C.c_void_p, W.UINT])
        self.checked(spi(0x30, 0, C.byref(work), 0))
        if [work.left, work.top, work.right, work.bottom] != before['system_work_area']:
            guard()
            work = W.RECT(*before['system_work_area'])
            result = spi(0x2f, 0, C.byref(work), 0)
            actions.append(dict(api='SystemParametersInfoW/SPI_SETWORKAREA', result=int(result), registry_written=False))
            self.checked(result)
        current = guard()
        if current['input_desktop']['foreground_hwnd'] != before['foreground_identity']['hwnd']:
            need(self.identity(before['foreground_identity']['hwnd']) == before['foreground_identity'], 'original foreground window and process lifetime')
            result = self.fn(self.u, 'SetForegroundWindow', W.BOOL, [W.HWND])(before['foreground_identity']['hwnd'])
            actions.append(dict(api='SetForegroundWindow', hwnd=before['foreground_identity']['hwnd'], result=int(result), forced=False))
        return actions


def differences(before, after):
    issues = previous.differences(before, after)
    if before['system_work_area'] != after['system_work_area']:
        issues.append('system_work_area_changed')
    if before['foreground_identity'] != after['foreground_identity']:
        issues.append('foreground_lifetime_changed')
    return sorted(set(issues))


class BoundedDesktop:
    """Each OS query/repair gets a separate no-console child and a 5s limit."""
    def __init__(self, folder, deadline):
        self.folder, self.deadline = Path(folder).resolve(), deadline
        root = Path(__file__).resolve().parents[1]
        need(self.folder.is_relative_to(root / '.venv-audit') and self.folder.drive.lower() == 'f:', 'F workspace desktop IO only')
        self.process_receipts = []

    def command(self, mode, payload=None):
        remaining = self.deadline - time.monotonic()
        need(remaining > 0, 'desktop recovery total deadline')
        arguments = [sys.executable, '-B', '-X', 'utf8', '-m', 'devtools.terminal_window_desktop', mode]
        temporary = None
        if payload is not None:
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf8', suffix='.json', prefix='desktop-input-', dir=self.folder, delete=False) as stream:
                json.dump(payload, stream)
                temporary = Path(stream.name).resolve()
            need(temporary.parent == self.folder, 'owned desktop temporary input')
            arguments.append(str(temporary))
        record = dict(mode=mode, timeout_seconds=min(5, remaining), completed=False)
        self.process_receipts.append(record)
        started = time.monotonic()
        try:
            completed = subprocess.run(arguments, cwd=Path(__file__).resolve().parents[1],
                env=dict(os.environ, TEMP=str(self.folder), TMP=str(self.folder)),
                capture_output=True, timeout=record['timeout_seconds'], creationflags=subprocess.CREATE_NO_WINDOW)
            record.update(completed=True, returncode=completed.returncode, seconds=time.monotonic()-started)
            need(len(completed.stdout) <= 128*1024 and len(completed.stderr) <= 8192, 'bounded desktop subprocess result')
            body = json.loads(completed.stdout)
            if completed.returncode:
                record['failure'] = body
                raise RuntimeError('bounded desktop operation failed: ' + str(body))
            return body
        except subprocess.TimeoutExpired:
            record.update(timed_out=True, seconds=time.monotonic()-started)
            raise
        finally:
            if temporary:
                temporary.unlink()

    def read(self):
        return self.command('--read')

    def repair(self, before, after):
        return self.command('--repair', dict(before=before, after=after))['actions']


def guarded_run(action, receipt, *, backend=None, sleep=time.sleep):
    """Call only after a fresh explicit desktop authorization has been checked."""
    backend = backend or Desktop()
    path = Path(receipt)
    need(not path.exists(), 'fresh desktop recovery receipt')
    before = backend.read()
    report = dict(before=before, after=[], recovery_actions=[], checks=[], restored=False,
                  action_started=False, action_error=None, automatic_recovery_attempted=False)
    result = None
    try:
        need(not previous.health(before), 'healthy original desktop required')
        report['action_started'] = True
        result = action()
    except BaseException as exc:
        report['action_error'] = repr(exc)
    finally:
        try:
            after = backend.read()
            report['after_action'] = after
            if report['action_started'] and differences(before, after):
                need(isinstance(result, dict) and result.get('cleanup', {}).get('job_empty'), 'test Job empty before any host restoration')
                need(before['last_input_tick'] == after['last_input_tick'], 'user resumed input: do not overwrite current desktop')
                report['automatic_recovery_attempted'] = True
                report['recovery_actions'] = backend.repair(before, after)
            for index in range(2):
                if index:
                    sleep(.5)
                after = backend.read()
                report['after'].append(after)
                report['checks'].append(differences(before, after))
            report['restored'] = not previous.health(before) and all(not x for x in report['checks'])
        except BaseException as exc:
            report['recovery_error'] = repr(exc)
        report['bounded_desktop_processes'] = getattr(backend, 'process_receipts', [])
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf8', newline='\n')
    need(not report['action_error'] and report['restored'], 'owned-window action or desktop recovery failed; see ' + str(path))
    return result


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--read', action='store_true')
    group.add_argument('--repair')
    args = parser.parse_args()
    desktop = Desktop()
    try:
        if args.read:
            output = desktop.read()
        else:
            source = Path(args.repair).resolve()
            need(source.is_relative_to(Path(__file__).resolve().parents[1] / '.venv-audit') and source.stat().st_size < 128*1024, 'bounded F repair input')
            data = json.loads(source.read_text(encoding='utf8'))
            output = dict(actions=desktop.repair(data['before'], data['after']))
        print(json.dumps(output))
    except BaseException as exc:
        print(json.dumps(dict(error=repr(exc), actions=getattr(desktop, 'recovery_actions', []))))
        raise SystemExit(1)
