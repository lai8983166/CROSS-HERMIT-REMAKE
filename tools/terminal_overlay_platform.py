"""Bounded current native CRT and 512x512 D3D8 overlay services."""
from pathlib import Path
import subprocess
from tools import school_crt_init_platform as crt
from tools import school_d3d8_image_bridge as gpu
from tools.school_d3d8_bridge import LiveD3D8
ROOT=crt.ROOT

def build(source,name):
 path=ROOT/('.venv-audit/'+name+'.exe');path.parent.mkdir(exist_ok=True)
 p=subprocess.run([str(crt.old.COMPILER),'/nologo','/platform:x86','/r:System.Web.Extensions.dll','/out:'+str(path),str(source)],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW,timeout=30)
 if p.returncode:raise RuntimeError((p.stdout+p.stderr).decode('cp936',errors='replace'))
 if crt.old.machine(path)!=0x14c:raise ValueError('x86 native service')
 return path,dict(source=str(source.relative_to(ROOT)),source_sha256=crt.old.sha(source.read_bytes()),helper_sha256=crt.old.sha(path.read_bytes()),machine=0x14c)

class OverlayGPU(LiveD3D8):
 def __init__(self,helper):
  super().__init__(helper)
  if self.hello.get('image_size')!=[512,512]:self.close();raise ValueError('current bounded overlay helper')
