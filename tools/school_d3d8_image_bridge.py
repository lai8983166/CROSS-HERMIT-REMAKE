"""Separate real multi-texture bridge; the earlier single-texture helper stays immutable."""
from tools.school_d3d8_bridge import LiveD3D8,ROOT,COMPILER,machine,sha
from pathlib import Path
import subprocess

SOURCE=ROOT/'tools/school_d3d8_image_bridge.cs'

def build(path=ROOT/'.venv-audit/school-d3d8-image-bridge.exe'):
 path=Path(path).resolve();path.parent.mkdir(parents=True,exist_ok=True)
 p=subprocess.run([str(COMPILER),'/nologo','/platform:x86','/r:System.Web.Extensions.dll','/out:'+str(path),str(SOURCE)],capture_output=True,timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
 if p.returncode:raise RuntimeError((p.stdout+p.stderr).decode('cp936',errors='replace'))
 if machine(path)!=0x14C:raise RuntimeError('multi bridge x86 ABI')
 return path,{'source_sha256':sha(SOURCE.read_bytes()),'compiler_sha256':sha(COMPILER.read_bytes()),'helper_sha256':sha(path.read_bytes()),'machine':0x14C}

class ImageD3D8(LiveD3D8):
 def __init__(self,helper):
  super().__init__(helper);self.textures={}
  if self.hello.get('max_textures')!=10 or self.hello.get('max_creates')!=32:
   self.close();raise ValueError('image bridge resource limits')
  if self.hello.get('image_size')!=[256,512]:
   self.close();raise ValueError('exact scene image extension')

 def create(self,*args,**kwargs):
  r=super().create(*args,**kwargs);self.textures[r['texture']['pointer']]=r['texture'];return r

 def release(self,pointer):
  r=super().release(pointer);self.textures.pop(pointer,None)
  if self.texture is not None and self.texture['pointer']==pointer:self.texture=None
  return r
