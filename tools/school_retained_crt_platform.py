"""Owned headless Win32 CRT test service; never opens a game window."""
import json,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tools.school_d3d8_bridge import ROOT,COMPILER,machine,sha

SOURCE=ROOT/'tools/school_retained_crt_platform.cs'
INSTALLED=ROOT/'CROSS HERMIT/CROSS HERMIT'

def build(path):
 path=Path(path).resolve()
 if path.exists():raise ValueError('fresh helper path required')
 p=subprocess.run([str(COMPILER),'/nologo','/platform:x86','/r:System.Web.Extensions.dll','/out:'+str(path),str(SOURCE)],capture_output=True,timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
 if p.returncode:raise RuntimeError((p.stdout+p.stderr).decode('cp936',errors='replace'))
 if machine(path)!=0x14c:raise ValueError('x86 helper ABI')
 return path,dict(source_sha256=sha(SOURCE.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),helper_sha256=sha(path.read_bytes()),machine=0x14c,helper_path=str(path))

class Live:
 def __init__(self,helper):
  if machine(helper)!=0x14c:raise ValueError('x86 helper ABI')
  self.process=subprocess.Popen([str(helper)],cwd=str(INSTALLED),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,encoding='utf8',creationflags=subprocess.CREATE_NO_WINDOW)
  self.reader=ThreadPoolExecutor(max_workers=1);self.trace=[];self.closed=False;self.cleanup=None
  try:
   r=self._read()
   if r.get('id')!=0 or r.get('ok')is not True:raise ValueError('native startup')
   self.hello=r['hello']
   if self.hello['pointer_bytes']!=4 or self.hello['window_created'] or self.hello['GPU_created'] or Path(self.hello['directory']).resolve()!=INSTALLED.resolve():raise ValueError('owned headless service provenance')
  except BaseException:self._terminate();raise
 def _read(self):
  line=self.reader.submit(self.process.stdout.readline).result(timeout=30)
  if not line or len(line)>3000000:raise ValueError('bounded response')
  return json.loads(line)
 def request(self,op,**args):
  if self.closed:raise ValueError('service closed')
  q=dict(id=len(self.trace)+1,op=op,**args);line=json.dumps(q,separators=(',',':'))
  if len(line)>3000000:raise ValueError('bounded request')
  try:self.process.stdin.write(line+'\n');self.process.stdin.flush();r=self._read()
  except BaseException:self._terminate();raise
  self.trace.append(dict(request=q,reply=r))
  if r.get('id')!=q['id'] or r.get('ok')is not True:raise ValueError(r)
  return r['result']
 def close(self):
  if self.closed:return self.cleanup
  try:
   self.cleanup=self.request('close');self.process.stdin.close();self.exit_code=self.process.wait(timeout=10)
   if self.exit_code or not self.cleanup['all_owned_resources_released']:raise ValueError('normal cleanup required')
  finally:self._terminate()
  return self.cleanup
 def _terminate(self):
  if self.process.poll()is None:self.process.kill()
  self.process.wait(timeout=10);self.closed=True
  for s in (self.process.stdin,self.process.stdout,self.process.stderr):s.close()
  self.reader.shutdown(wait=True)
