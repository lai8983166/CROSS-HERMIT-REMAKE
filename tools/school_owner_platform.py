"""Bounded real32-bit screen-DC/timer/font helper with explicit resource lifetime."""
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from tools.school_d3d8_bridge import LiveD3D8, ROOT, COMPILER, machine, sha

SOURCE = ROOT/'tools/school_owner_platform.cs'
HELPER = ROOT/'.venv-audit/school-owner-platform-v2.exe'


def build():
    if HELPER.exists():
        raise ValueError('immutable fresh owner helper required')
    result = subprocess.run([str(COMPILER), '/nologo', '/platform:x86',
                             '/r:System.Web.Extensions.dll', '/out:'+str(HELPER), str(SOURCE)],
                            capture_output=True, timeout=30, creationflags=subprocess.CREATE_NO_WINDOW)
    if result.returncode:
        raise RuntimeError((result.stdout+result.stderr).decode('cp936', errors='replace'))
    return dict(source_sha256=sha(SOURCE.read_bytes()), compiler_sha256=sha(COMPILER.read_bytes()),
                helper_sha256=sha(HELPER.read_bytes()), machine=machine(HELPER))


class OwnerPlatform(LiveD3D8):
    def __init__(self):
        if machine(HELPER) != 0x14C:
            raise ValueError('real x86 owner helper required')
        self.process = subprocess.Popen([str(HELPER)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, text=True, encoding='utf-8',
                                       creationflags=subprocess.CREATE_NO_WINDOW)
        self.reader = ThreadPoolExecutor(max_workers=1)
        self.sequence, self.closed, self.trace, self.cleanup = 0, False, [], None
        try:
            reply = self._read()
            if reply.get('ok') is not True or reply.get('id') != 0:
                raise RuntimeError(reply)
            self.hello = reply['hello']
            if self.hello['pointer_bytes'] != 4:
                raise ValueError('owner helper pointer ABI')
        except BaseException:
            self._terminate()
            raise
