"""Owned live startup bridge, without the earlier bridge's pre-created device."""
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from tools.school_d3d8_bridge import LiveD3D8, ROOT, COMPILER, machine, sha

SOURCE = ROOT/'tools/school_device_init_bridge.cs'


def build(path=ROOT/'.venv-audit/school-device-init-bridge.exe'):
    path = Path(path).resolve()
    result = subprocess.run([str(COMPILER), '/nologo', '/platform:x86',
                             '/r:System.Web.Extensions.dll', '/out:'+str(path), str(SOURCE)],
                            capture_output=True, timeout=30,
                            creationflags=subprocess.CREATE_NO_WINDOW)
    if result.returncode:
        raise RuntimeError((result.stdout+result.stderr).decode('cp936', errors='replace'))
    if machine(path) != 0x14C:
        raise ValueError('required x86 bridge')
    return path, dict(source_sha256=sha(SOURCE.read_bytes()),
                      compiler_sha256=sha(COMPILER.read_bytes()),
                      helper_sha256=sha(path.read_bytes()), machine=0x14C)


class DeviceBridge(LiveD3D8):
    def __init__(self, helper, width, height):
        if machine(helper) != 0x14C or not (64 <= width <= 1280 and 64 <= height <= 800):
            raise ValueError('bounded x86 device startup required')
        self.process = subprocess.Popen([str(helper), str(width), str(height)],
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, text=True, encoding='utf-8',
                                       creationflags=subprocess.CREATE_NO_WINDOW)
        self.reader = ThreadPoolExecutor(max_workers=1)
        self.sequence = 0
        self.closed = False
        self.trace = []
        self.cleanup = None
        try:
            reply = self._read()
            if reply.get('ok') is not True or reply.get('id') != 0:
                raise RuntimeError(reply)
            self.hello = reply['hello']
            if (self.hello['pointer_bytes'] != 4 or self.hello['window_visible']
                    or (self.hello['width'], self.hello['height']) != (width, height)
                    or not self.hello['window']):
                raise ValueError('real owned hidden window required')
        except BaseException:
            self._terminate()
            raise
