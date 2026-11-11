"""Bounded host serial qualification: no WinRM and no host input injection."""
import base64,ctypes,datetime,hashlib,json,os,re,secrets,socket,subprocess,sys,time
from pathlib import Path
from devtools.isolated_windows_vm import WORKER,ROOT,environment,identity
from devtools.isolated_vm_preflight import observe_host
from devtools.isolated_vm_bounded_query_v3 import Job
from devtools.terminal_tcg_qualification_verify_v1 import verify,GUEST_UUID
SOURCE='490dd9ea43e5c0f73434bdba21d5ad1e8cee3587c829f6a27cdf7d332730839f'
EXE='a5aaf66a409ba15632bf7f6211552fa1f26335838957da5c7535ba74291caddc'

def child_ok(v,allow_graphics_failure=False):
 keys={'thread','pipe_write','stdin','process','pipe_read','job'}
 return (v['exit_code'] in ((0,1)if allow_graphics_failure else(0,)) and v['cleanup_ok']is True and v['error']is None and not v['timed_out'] and not v['output_limit_exceeded'] and v['job_assigned_before_resume']is True and not v['job_terminated'] and v['active_processes_after']==0 and set(v['handle_close'])==keys and all(x is True for x in v['handle_close'].values()))

def boot_utc(raw):
 text=raw.decode('utf-16-le')if b'\x00'in raw else raw.decode('ascii')
 m=re.search(r'LastBootUpTime=(\d{14})\.(\d{6})([+-])(\d{3})',text)
 if not m:raise ValueError('complete native boot identity')
 dt=datetime.datetime.strptime(m[1],'%Y%m%d%H%M%S')-datetime.timedelta(minutes=int(m[4])*(1 if m[3]=='+'else-1))
 return dt.strftime('%Y-%m-%dT%H:%M:%S')+'.'+m[2]+'0Z'

class Channel:
 def __init__(self,key,nonce,log):
  self.s=socket.create_connection(('127.0.0.1',15988),5);self.buf=b'';self.key=key;self.nonce=nonce;self.session='';self.seq=0;self.log=log
 def line(self,deadline):
  while b'\n'not in self.buf:
   remaining=deadline-time.monotonic()
   if remaining<=0:raise TimeoutError('serial response deadline')
   self.s.settimeout(remaining);part=self.s.recv(4096)
   if not part:raise EOFError('serial endpoint closed')
   self.buf+=part
   if len(self.buf)>100000:raise ValueError('serial reply budget')
  line,self.buf=self.buf.split(b'\n',1)
  if time.monotonic()>deadline:raise TimeoutError('late complete serial reply')
  return json.loads(line)
 def ready(self,seconds=360):
  end=time.monotonic()+seconds;count=0
  while time.monotonic()<end:
   self.s.settimeout(2);self.s.sendall(b'\n');count+=1
   try:
    r=self.line(min(end,time.monotonic()+5))
    if r.get('seq')==0 and r.get('ok')is False and isinstance(r.get('session'),str):return dict(blank_challenges=count,response=r)
    raise ValueError('unexpected readiness response')
   except socket.timeout:pass
  raise TimeoutError('guest serial agent readiness')
 def call(self,op,seconds=15,**fields):
  self.seq+=1;start=time.monotonic();request=dict(key=self.key,seq=self.seq,session=self.session,op=op,nonce=self.nonce,**fields)
  raw=json.dumps(request,separators=(',',':')).encode()+b'\n';self.s.settimeout(5);self.s.sendall(raw)
  while True:
   r=self.line(start+seconds)
   if r.get('seq')!=0:break
  record=dict(op=op,seq=self.seq,seconds=time.monotonic()-start,response=r)
  self.log.append(record)
  if hasattr(self,'logpath'):
   with self.logpath.open('a',encoding='utf8')as f:f.write(json.dumps(record)+chr(10))
  if r.get('seq')!=self.seq or r.get('ok')is not True:raise ValueError('serial operation failed: '+op)
  if op=='hello':self.session=r['session']
  elif r.get('session')!=self.session:raise ValueError('serial session changed')
  return r['value']

def worker(case):
 if sys.stdin.readline().strip()!='assigned':raise ValueError('host job gate')
 nonce=secrets.randbelow(0x20000000)+0x40000000;r=dict(accepted=False,nonce=nonce,operations=[],errors=[],host_input_actions=0);ch=None;hello=False
 try:
  seed=json.loads((WORKER/'tcg-serial-seed-v3/seed-verification.json').read_bytes())
  if seed['verified']is not True:raise ValueError('verified seed')
  code="[pscustomobject]@{uuid=(Get-CimInstance Win32_ComputerSystemProduct).UUID}|ConvertTo-Json -Compress"
  host=json.loads(subprocess.run(['powershell.exe','-NoProfile','-NonInteractive','-Command',code],capture_output=True,text=True,timeout=20,check=True,env=environment(),creationflags=subprocess.CREATE_NO_WINDOW).stdout)
  ch=Channel((WORKER/'tcg-serial-seed-v3/control-key.private').read_text().strip(),nonce,r['operations']);ch.logpath=case/'operations.jsonl';r['readiness']=ch.ready()
  (case/'readiness.json').write_text(json.dumps(r['readiness']))
  v=ch.call('hello',40);hello=True;i=v['identity'];expected=json.loads((WORKER/'tcg-serial-agent-build-v3/manifest.json').read_bytes())['executable']
  if not(v['autologon_cleared']is True and v['initialization_restored']is True and i['uuid']==str(GUEST_UUID) and i['manufacturer']=='QEMU' and i['computer_name']=='CHAOMOFA-WORKER' and i['session_id']==i['active_console_session_id']>0 and i['exe_sha256']==expected['sha256']):raise ValueError('serial guest identity')
  echo=ch.call('echo',40)
  if not child_ok(echo)or base64.b64decode(echo['output_base64'])!=('CMF-%08x\r\n'%nonce).encode():raise ValueError('complete echo and cleanup')
  r['command_return_and_cleanup']=True
  boot=ch.call('boot',40)
  if not child_ok(boot):raise ValueError('complete native boot query and cleanup')
  expected_boot=boot_utc(base64.b64decode(boot['output_base64']));r['expected_boot_utc']=expected_boot
  probe=WORKER/'tcg-qualification-build-v1/probe.exe';data=probe.read_bytes()
  if len(data)!=32768 or hashlib.sha256(data).hexdigest()!=EXE:raise ValueError('original probe identity')
  if ch.call('begin')['offset_after']!=0:raise ValueError('initial upload offset')
  for offset in range(0,len(data),2048):
   block=data[offset:offset+2048];v=ch.call('block',offset=offset,data=base64.b64encode(block).decode(),sha256=hashlib.sha256(block).hexdigest())
   if v['offset_after']!=offset+len(block)or v['prefix_sha256']!=hashlib.sha256(data[:offset+len(block)]).hexdigest():raise ValueError('uploaded prefix')
  sealed=ch.call('seal')
  if sealed!={'length':32768,'sha256':EXE}:raise ValueError('uploaded executable identity')
  r['small_block_deployment']=True
  actual={}
  def execute():
   actual['run']=ch.call('run',140)
   if not child_ok(actual['run'],True):raise ValueError('probe native lifetime/cleanup')
   v=ch.call('read',15);raw=base64.b64decode(v['data'],validate=True)
   if len(raw)!=v['length']or hashlib.sha256(raw).hexdigest()!=v['sha256']:raise ValueError('probe report transfer')
   (case/'guest-probe.json').write_bytes(raw);actual['guest']=json.loads(raw)
  h=observe_host(nonce,execute,seconds=175);r['host_observation']=h;r['native_run']=actual.get('run')
  if h['error']:raise ValueError(h['error'])
  envelope=dict(schema='terminal-tcg-qualification-v1',accepted=False,nonce=nonce,source_sha256=SOURCE,guest_executable=identity(probe),host=host,host_observation=h,guest=actual['guest'])
  (case/'qualification-envelope.json').write_text(json.dumps(envelope,indent=2))
  r['verification']=verify(envelope,expected_source_sha256=SOURCE,expected_executable_sha256=EXE,expected_boot_utc=expected_boot,expected_nonce=nonce)
 except Exception as e:r['errors'].append(type(e).__name__+': '+str(e))
 finally:
  if ch:
   if hello:
    try:
     r['bye']=ch.call('bye',15)
     if r['bye'].get('bootstrap_restored')is not True:r['errors'].append('owned bootstrap restoration failed')
    except Exception as e:r['errors'].append('bye: '+type(e).__name__)
   ch.s.close();r['host_socket_closed']=True
  (case/'serial-result.json').write_text(json.dumps(r,indent=2))
 print(json.dumps({k:v for k,v in r.items()if k not in ('operations','readiness','host_observation')}))

def main(case):
 case=case.resolve()
 if case.parent!=WORKER or(case/'host-control.json').exists():raise ValueError('fresh F worker case')
 job=Job();p=None;assigned=False;r=dict(accepted=False,deadline_seconds=700,errors=[]);start=time.monotonic()
 try:
  with(case/'client.stdout').open('xb')as out,(case/'client.stderr').open('xb')as err:
   p=subprocess.Popen([sys.executable,'-B','-X','utf8','-m','devtools.terminal_tcg_serial_client_v3','--worker',str(case)],stdin=subprocess.PIPE,stdout=out,stderr=err,env=environment(),creationflags=subprocess.CREATE_NO_WINDOW)
   job.assign(p);assigned=True;r['assigned_before_request']=True;p.stdin.write(b'assigned\n');p.stdin.close()
   try:r['exit_code']=p.wait(timeout=700)
   except subprocess.TimeoutExpired:r['errors'].append('host deadline');job.terminate();p.wait(timeout=5)
   if job.active():job.terminate()
   end=time.monotonic()+5
   while job.active()and time.monotonic()<end:time.sleep(.02)
   r['active_processes_after']=job.active()
 finally:
  if p and p.poll()is None:
   if assigned:job.terminate()
   else:p.kill()
   p.wait(timeout=5)
  job.close();r['job_closed']=True;r['seconds']=time.monotonic()-start
  (case/'host-control.json').write_text(json.dumps(r,indent=2));(case/'vm-stop').touch()
 print(json.dumps(r))
if __name__=='__main__':
 if len(sys.argv)==3 and sys.argv[1]=='--worker':worker(Path(sys.argv[2]))
 elif len(sys.argv)==2:main(Path(sys.argv[1]))
 else:raise SystemExit('fresh case path required')
