"""Opt-in, bounded PrintWindow candidate; never a graphics qualification claim.

No UI work happens at import. The caller must own the game's live Job and have
fresh desktop/capture authorization. Frozen observers are deliberately unchanged.
PrintWindow may block or return blank legacy-D3D content: one attempt only.
"""
import argparse
import ctypes as C
import ctypes.wintypes as W
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / '.venv-audit/scene-callback-runtime/CROSS HERMIT/CROSS HERMIT/CROSS HERMIT.EXE'
MAX_PIXELS = 2048 * 1536


def image_shape(width, height):
    if (type(width) is not int or type(height) is not int
            or width < 64 or height < 64 or width * height > MAX_PIXELS):
        raise ValueError('bounded nonempty game client size required')
    return width * height * 4


def pixels_to_png(width, height, pixels):
    from PIL import Image
    import io
    if len(pixels) != image_shape(width, height):
        raise ValueError('incomplete pixel buffer')
    frame = Image.frombytes('RGB', (width, height), pixels, 'raw', 'BGRX')
    if all(lo == hi for lo, hi in frame.getextrema()):
        raise ValueError('uniform/untouched image; capture not usable')
    out = io.BytesIO()
    frame.save(out, format='PNG')
    return out.getvalue()


def capture_owned(c, hwnd, output, *, explicit_capture_override=False, timeout=5):
    """Read a verified own window in a disposable, hidden capture process."""
    if explicit_capture_override is not True:
        raise PermissionError('separate native screenshot override required')
    if not 0 < timeout <= 5:
        raise ValueError('capture timeout must be at most five seconds')
    from tools.school_native_dialogue_input import owned_target_guard
    owned_target_guard(c, hwnd)
    path = Path(output).resolve()
    if not path.is_relative_to(ROOT / 'analysis') or path.exists() or path.suffix != '.png':
        raise ValueError('fresh PNG in analysis required')
    command = [sys.executable, '-B', '-X', 'utf8', '-m', 'devtools.terminal_host_capture',
               '--worker', '--pid', str(c.pid), '--hwnd', str(hwnd), '--main', str(c.main)]
    started = time.monotonic()
    # Worker has no subprocesses or persistent writes. run kills and waits for
    # this exact child on timeout; never terminates the game or a foreign PID.
    result = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=timeout,
                            creationflags=subprocess.CREATE_NO_WINDOW)
    owned_target_guard(c, hwnd)
    if result.returncode:
        raise RuntimeError('capture worker failed: ' + result.stderr.decode('utf8', 'replace')[-1500:])
    from PIL import Image
    import io
    with Image.open(io.BytesIO(result.stdout)) as picture:
        image_shape(*picture.size)
        if picture.format != 'PNG':
            raise ValueError('worker did not return PNG')
        picture.verify()
    with path.open('xb') as stream:
        stream.write(result.stdout)
    return dict(path=path.relative_to(ROOT).as_posix(), bytes=len(result.stdout),
                sha256=hashlib.sha256(result.stdout).hexdigest(), elapsed=time.monotonic()-started,
                pid=c.pid, hwnd=hwnd, backend='PrintWindow/PW_CLIENTONLY',
                visually_reviewed=False, graphics_qualified=False, input_sent=False)


def worker(pid, hwnd, main):
    from devtools import terminal_scene_owner as base
    from tools.school_native_dialogue_desktop import require_unlocked
    original = base.original
    require_unlocked()
    process = original.openp(0x1000, False, pid)
    original.check(process, 'query capture target identity')
    dc = bitmap = old = screen = None
    gdi = C.WinDLL('gdi32', use_last_error=True)
    def bind(name, result, args):
        fn = getattr(gdi, name); fn.restype = result; fn.argtypes = args
        return fn
    delete_dc = bind('DeleteDC', W.BOOL, [W.HDC])
    delete_object = bind('DeleteObject', W.BOOL, [W.HANDLE])
    select = bind('SelectObject', W.HANDLE, [W.HDC, W.HANDLE])
    def identity():
        owner = W.DWORD()
        original.ownerpid(hwnd, C.byref(owner))
        path = C.create_unicode_buffer(32768); count = W.DWORD(len(path))
        original.check(base.native.image_name(process, 0, path, C.byref(count)), 'capture image identity')
        if (owner.value != pid or Path(path.value).resolve() != APP.resolve()
                or original.getprop(hwnd, b'CPP_CLASS') != main
                or original.ubind('GetForegroundWindow', W.HWND, [])() != hwnd):
            raise ValueError('capture target identity/foreground changed')
        return True
    try:
        identity()
        rect = W.RECT()
        original.check(original.ubind('GetClientRect', W.BOOL, [W.HWND, C.POINTER(W.RECT)])(
            hwnd, C.byref(rect)), 'game client bounds')
        width, height = rect.right-rect.left, rect.bottom-rect.top
        size = image_shape(width, height)
        class Header(C.Structure):
            _fields_ = [('size', W.DWORD), ('width', W.LONG), ('height', W.LONG),
                        ('planes', W.WORD), ('bits', W.WORD), ('compression', W.DWORD),
                        ('image_size', W.DWORD), ('x', W.LONG), ('y', W.LONG),
                        ('used', W.DWORD), ('important', W.DWORD)]
        header = Header(C.sizeof(Header), width, -height, 1, 32, 0, size, 0, 0, 0, 0)
        screen = original.ubind('GetDC', W.HDC, [W.HWND])(hwnd)
        original.check(screen, 'own window DC')
        dc = bind('CreateCompatibleDC', W.HDC, [W.HDC])(screen)
        original.check(dc, 'capture memory DC')
        bits = C.c_void_p()
        bitmap = bind('CreateDIBSection', W.HANDLE,
                      [W.HDC, C.c_void_p, W.UINT, C.POINTER(C.c_void_p), W.HANDLE, W.DWORD])(
                          screen, C.byref(header), 0, C.byref(bits), None, 0)
        original.check(bitmap and bits.value, 'bounded capture bitmap')
        old = select(dc, bitmap)
        original.check(old and old != C.c_void_p(-1).value, 'select capture bitmap')
        C.memset(bits, 0xA5, size)
        identity()
        original.check(original.ubind('PrintWindow', W.BOOL, [W.HWND, W.HDC, W.UINT])(
            hwnd, dc, 1), 'PrintWindow client content')
        original.check(bind('GdiFlush', W.BOOL, [])(), 'flush capture bitmap')
        identity()
        png = pixels_to_png(width, height, C.string_at(bits, size))
        sys.stdout.buffer.write(png)
    finally:
        if old and old != C.c_void_p(-1).value and dc: select(dc, old)
        if bitmap: delete_object(bitmap)
        if dc: delete_dc(dc)
        if screen: original.ubind('ReleaseDC', C.c_int, [W.HWND, W.HDC])(hwnd, screen)
        original.close(process)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker', action='store_true', required=True)
    for name in ('pid', 'hwnd', 'main'): parser.add_argument('--'+name, type=int, required=True)
    args = parser.parse_args()
    worker(args.pid, args.hwnd, args.main)
