"""Owned persistent real x86 Direct3D8 objects and bounded synchronized texture buffers."""
import hashlib,json,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tools.school_d3d8_platform import ROOT,COMPILER,machine,sha

SOURCE=ROOT/'tools/school_d3d8_bridge.cs'
def build(path=ROOT/'.venv-audit/school-d3d8-bridge.exe'):
 path=Path(path).resolve();path.parent.mkdir(parents=True,exist_ok=True)
 p=subprocess.run([str(COMPILER),'/nologo','/platform:x86','/r:System.Web.Extensions.dll','/out:'+str(path),str(SOURCE)],capture_output=True,timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
 if p.returncode:raise RuntimeError((p.stdout+p.stderr).decode('cp936',errors='replace'))
 if machine(path)!=0x14C:raise RuntimeError('bridge x86 ABI')
 return path,{'source_sha256':sha(SOURCE.read_bytes()),'compiler_sha256':sha(COMPILER.read_bytes()),'helper_sha256':sha(path.read_bytes()),'machine':0x14C}

class LiveD3D8:
 def __init__(self,helper):
  if machine(helper)!=0x14C:raise ValueError('real x86 helper required')
  self.process=subprocess.Popen([str(helper)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)
  self.reader=ThreadPoolExecutor(max_workers=1);self.sequence=0;self.closed=False;self.trace=[];self.cleanup=None
  try:
   r=self._read()
   if r.get('ok') is not True or r.get('id')!=0:raise RuntimeError(r)
   self.hello=r['hello']
   if self.hello['pointer_bytes']!=4 or self.hello['window_visible'] or machine(self.hello['runtime_path'])!=0x14C or sha(Path(self.hello['runtime_path']).read_bytes())!=self.hello['runtime_sha256']:raise RuntimeError('actual live platform provenance')
   self.device=self.hello['device'];self.texture=None
  except BaseException:
   self._terminate();raise

 def _read(self):
  line=self.reader.submit(self.process.stdout.readline).result(timeout=30)
  if not line or len(line)>3*1024*1024:raise RuntimeError('bounded live bridge response')
  return json.loads(line)

 def request(self,op,**args):
  if self.closed:raise ValueError('live bridge closed')
  r={'id':self.sequence+1,'op':op,**args};line=json.dumps(r,separators=(',',':'))
  if len(line)>3*1024*1024:raise ValueError('bounded bridge request')
  self.sequence+=1
  try:
   self.process.stdin.write(line+'\n');self.process.stdin.flush();reply=self._read()
  except BaseException:
   self._terminate();raise
  self.trace.append({'request':r,'reply':reply})
  if reply.get('id')!=self.sequence:raise RuntimeError('live bridge sequence')
  if reply.get('ok') is not True:raise ValueError(reply.get('error','real bridge refused'))
  return reply['result']

 def create(self,w,h,levels=1,usage=0,format=25,pool=1):
  r=self.request('create',width=w,height=h,levels=levels,usage=usage,format=format,pool=pool);self.texture=r['texture'];return r

 def describe(self,pointer):return self.request('describe',pointer=pointer)
 def lock(self,pointer,flags=0x800):return self.request('lock',pointer=pointer,flags=flags)
 def unlock(self,pointer,raw):
  if not isinstance(raw,bytes) or len(raw)>1024*1024:raise ValueError('bounded actual texture buffer')
  return self.request('unlock',pointer=pointer,hex=raw.hex())
 def readback(self,pointer):return self.request('readback',pointer=pointer)
 def release(self,pointer):return self.request('release',pointer=pointer)

 def _terminate(self):
  if self.process.poll() is None:self.process.kill()
  self.process.wait(timeout=10);self.closed=True
  for s in (self.process.stdin,self.process.stdout,self.process.stderr):s.close()
  self.reader.shutdown(wait=True)

 def close(self):
  if self.closed:return self.cleanup
  try:
   self.cleanup=self.request('close');self.process.stdin.close();code=self.process.wait(timeout=10)
   if code or not self.cleanup['all_owned_resources_released']:raise RuntimeError('live bridge cleanup')
  finally:self._terminate()
  return self.cleanup

 def __enter__(self):return self
 def __exit__(self,*args):self.close()
