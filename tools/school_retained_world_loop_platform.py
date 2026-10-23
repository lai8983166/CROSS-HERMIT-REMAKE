"""Headless API owner; heap/locks exist only after original initialization calls."""
import subprocess
from pathlib import Path
from tools import school_retained_crt_platform as old
ROOT=old.ROOT;SOURCE=ROOT/'tools/school_retained_world_loop_platform.cs'

def build(path):
 path=Path(path).resolve()
 if path.exists():raise ValueError('fresh helper output')
 p=subprocess.run([str(old.COMPILER),'/nologo','/platform:x86','/r:System.Web.Extensions.dll','/out:'+str(path),str(SOURCE)],capture_output=True,timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
 if p.returncode:raise RuntimeError((p.stdout+p.stderr).decode('cp936',errors='replace'))
 if old.machine(path)!=0x14c:raise ValueError('x86 helper ABI')
 return path,dict(source_sha256=old.sha(SOURCE.read_bytes()),compiler_sha256=old.sha(old.COMPILER.read_bytes()),helper_sha256=old.sha(path.read_bytes()),helper_path=str(path),machine=0x14c)

BASE_SOURCE_SHA='cb25ac0088513f488baaf240d9b67bcd5966a700a94795e37d9525e193e5647b'
Live=old.Live
