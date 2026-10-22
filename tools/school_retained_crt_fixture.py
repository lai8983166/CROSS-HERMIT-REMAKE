"""Separate declared-input original CRT function fixtures, NOT retained restoration."""
import gzip,hashlib,json,struct
from collections import Counter
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from tools import school_retained_crt as retained
from tools import school_retained_crt_platform as platform

base=retained.base;ROOT=base.ROOT;need=base.need;sha=base.sha;word=base.word
STACK=0x21000000;PATH=0x22000000;RETURN=0x32000000;HEAP=0x50001000
LEDGER=(0x80a430,0x80a434,0x80a438,0x80a43c,0x80a440)
SOURCE_SHA='588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'
FILE_SHA='a4443ca63b9889503e35170da0c8b976a799c25ec3f0bd1b0f80dc97c38a6164'
IMPORTS={0x592234:('EnterCriticalSection',4),0x592238:('LeaveCriticalSection',4),0x592144:('HeapAlloc',12),0x59218c:('HeapValidate',12),0x592258:('HeapFree',12),0x592190:('IsBadReadPtr',8),0x592244:('IsBadWritePtr',8),0x592214:('GetCurrentDirectoryA',8),0x5921ec:('CreateFileA',28),0x5921f0:('GetFileSize',8),0x5921e8:('ReadFile',20),0x592270:('CloseHandle',4)}

def text(g,p):
 b=bytearray()
 for i in range(260):
  v=g.read(p+i,1)[0]
  if not v:return bytes(b)
  b.append(v)
 raise ValueError('bounded source path')

def initialize(g,hello):
 g.u=Uc(UC_ARCH_X86,UC_MODE_32);g.image=base.SOURCE.read_bytes();need(sha(g.image)==SOURCE_SHA,'pinned original source')
 g.u.mem_map(base.BASE,(len(g.image)+4095)&~4095);g.u.mem_write(base.BASE,g.image)
 for p,n in [(0,4096),(STACK,65536),(PATH,4096),(RETURN,4096)]:g.u.mem_map(p,n)
 g.u.mem_write(0,struct.pack('<I',0xffffffff));g.u.mem_write(PATH,b'data\\adv\\bin\\sc004.bin\0')
 inputs=[]
 for p,v in [*( (p,0) for p in LEDGER),(0x7619c4,1)]:
  b=struct.pack('<I',v);old=g.read(p);g.u.mem_write(p,b);inputs.append(dict(pointer=p,before_hex=old.hex(),hex=b.hex(),role='explicit empty debug ledger test input'))
 b=bytes.fromhex(hello['critical_hex']);need(len(b)==24,'native critical section extent');old=g.read(0x80a4b0,24);g.u.mem_write(0x80a4b0,b);inputs.append(dict(pointer=0x80a4b0,before_hex=old.hex(),hex=b.hex(),role='owned native critical section bytes in separate fixture'))
 maps=[]
 for slot in IMPORTS:
  target=word(g.read(slot))
  if not any(a<=target<=b for a,b,_ in g.u.mem_regions()):p=target&~4095;g.u.mem_map(p,4096);maps.append(dict(pointer=p,bytes=4096))
 need(word(g.read(0x7619c0))==word(g.read(0x80ab2c))==1,'debug tracking on and heap mode1')
 return dict(kind='separate declared function-test inputs, never retained state',source_sha256=SOURCE_SHA,overlays=inputs,entry_maps=maps,empty_FS_exception_chain=True,fixture_path_hex=g.read(PATH,23).hex(),initial_memory=base.memory_rows(g.u),initial_cpu=base.architectural_cpu(g.u),heap_token_translation=dict(guest=word(g.read(0x80ab28)),native=hello['heap']),critical_translation=dict(guest=0x80a4b0,native=hello['critical']))

def ledger(g):return dict(zip(('first','total','last','current','high'),[word(g.read(p)) for p in LEDGER]),next_request=word(g.read(0x7619c4)),game_bytes=word(g.read(0x79fc74)))

class Guest:
 def __init__(self,live):
  self.live=live;self.declaration=initialize(self,live.hello);self.allocations={};self.history=[];self.next=HEAP;self.steps=[];self.api_calls=[]
 def read(self,p,n=4):return bytes(self.u.mem_read(p,n))
 def cpu(self):return {k:self.u.reg_read(v) for k,v in base.REGISTERS.items()}
 def owned(self,p,n=1):
  matches=[(a,r) for a,r in self.allocations.items() if a<=p and p+n<=a+r['bytes']];need(len(matches)==1,'source pointer within live owned allocation');return matches[0]
 def sync(self,p):
  r=self.allocations[p];b=self.read(p,r['bytes']);q=self.live.request('sync',pointer=r['native'],hex=b.hex());need(q['hex']==b.hex(),'actual entire source bytes mirrored before native use')
 def api(self,slot):
  name,pop=IMPORTS[slot];sp=self.cpu()['ESP'];ret=word(self.read(sp));args=[word(self.read(sp+4+i)) for i in range(0,pop,4)];start=len(self.live.trace);outputs=[];maps=[]
  def put(p,b):self.u.mem_write(p,b);outputs.append(dict(pointer=p,hex=b.hex()))
  if name in ('EnterCriticalSection','LeaveCriticalSection'):
   need(args==[0x80a4b0],'source lock9 pointer');r=self.live.request('enter' if name[0]=='E' else 'leave',critical=self.live.hello['critical']);value=0;put(args[0],bytes.fromhex(r['critical_hex']))
  elif name=='HeapAlloc':
   need(args[:2]==[self.declaration['heap_token_translation']['guest'],0],'logical source heap/flags, never native stale token');r=self.live.request('alloc',heap=self.live.hello['heap'],flags=0,bytes=args[2]);p=self.next;self.next+=0x200000;n=(r['bytes']+4095)&~4095;self.u.mem_map(p,n);maps.append(dict(pointer=p,bytes=n));put(p,bytes.fromhex(r['hex']));entry=dict(guest=p,native=r['pointer'],bytes=r['bytes'],freed=False);self.allocations[p]=entry;self.history.append(entry);value=p
  elif name in ('HeapValidate','HeapFree'):
   need(args[:2]==[self.declaration['heap_token_translation']['guest'],0],'source owned heap ABI');p,r=self.owned(args[2]);need(p==args[2],'raw native heap block');self.sync(p);r=self.live.request('validate' if name=='HeapValidate' else 'free',heap=self.live.hello['heap'],flags=0,pointer=r['native']);value=r['value']
   if name=='HeapFree':self.allocations[p]['freed']=True;del self.allocations[p]
  elif name in ('IsBadReadPtr','IsBadWritePtr'):
   p,r=self.owned(args[0],args[1]);self.sync(p);r=self.live.request('badread' if name=='IsBadReadPtr' else 'badwrite',pointer=r['native'],offset=args[0]-p,bytes=args[1]);value=r['value']
  elif name=='GetCurrentDirectoryA':
   need(args==[260,0x7a0ebc],'source directory ABI');r=self.live.request('directory',bytes=args[0]);value=r['value'];put(args[1],bytes.fromhex(r['hex']))
  elif name=='CreateFileA':
   raw=text(self,args[0]);need(raw==b'data\\adv\\bin\\sc004.bin','source SC004 path');r=self.live.request('open',path=raw.decode('ascii'),**dict(zip(('access','share','security','disposition','attributes','template'),args[1:])));value=r['handle']
  elif name=='GetFileSize':r=self.live.request('size',handle=args[0],high=args[1]);value=r['value']
  elif name=='ReadFile':
   p,r=self.owned(args[1],args[2]);self.sync(p);r=self.live.request('read',handle=args[0],pointer=r['native'],offset=args[1]-p,bytes=args[2],overlapped=args[4]);value=r['value'];put(p,bytes.fromhex(r['after_hex']));put(args[3],struct.pack('<I',r['read']))
  else:need(name=='CloseHandle','planned OS leaf only');r=self.live.request('file_close',handle=args[0]);value=r['value']
  a=dict(name=name,import_slot=slot,target=word(self.read(slot)),sp=sp,return_va=ret,args=args,pop=pop,value=value,new_mappings=maps,memory_outputs=outputs,wire_start=start,wire_end=len(self.live.trace),void_return_normalized=name in ('EnterCriticalSection','LeaveCriticalSection'));self.api_calls.append(a)
  self.u.reg_write(base.REGISTERS['EAX'],value);self.u.reg_write(base.REGISTERS['ESP'],sp+4+pop);self.u.reg_write(base.REGISTERS['EIP'],ret)
 def root(self,label,va,args=()):
  sp=STACK+0xf000;self.u.mem_write(sp,struct.pack('<'+'I'*(1+len(args)),RETURN,*args))
  for k,v in dict(EIP=va,ESP=sp,ECX=0,EFLAGS=0x202).items():self.u.reg_write(base.REGISTERS[k],v)
  before=self.cpu();counts=Counter();ih=hashlib.sha256();wh=hashlib.sha256();writes=0;self.api_calls=[];targets={word(self.read(slot)):slot for slot in IMPORTS}
  def code(u,at,n,_):
   if at==RETURN:u.emu_stop();return
   if at in targets:self.api(targets[at]);return
   need(base.BASE<=at<0x592000 and self.read(at,n)==self.image[at-base.BASE:at-base.BASE+n],'original source instruction only, unsupported boundary '+hex(at));counts[at]+=1;ih.update(struct.pack('<I',at)+self.read(at,n))
  def write(u,access,at,n,value,_):
   nonlocal writes
   need(not base.BASE<=at<0x592000,'no code patch');writes+=1;wh.update(struct.pack('<IIQ',at,n,value&0xffffffffffffffff))
  c=self.u.hook_add(UC_HOOK_CODE,code);w=self.u.hook_add(UC_HOOK_MEM_WRITE,write)
  try:self.u.emu_start(va,0,count=2000000,timeout=120000000)
  except Exception as exc:raise RuntimeError(label+' at '+hex(self.cpu()['EIP'])) from exc
  finally:self.u.hook_del(c);self.u.hook_del(w)
  need(self.cpu()['EIP']==RETURN and self.cpu()['ESP']==sp+4,'source natural cdecl return');result=dict(before_cpu=before,cpu=self.cpu(),boundary=RETURN,instruction_counts=[dict(va=a,count=n) for a,n in sorted(counts.items())],instruction_sha256=ih.hexdigest(),writes=writes,write_sha256=wh.hexdigest(),api_calls=self.api_calls)
  row=dict(label=label,root=dict(va=va,sp=sp,args=list(args),return_va=RETURN,receiver=0),result=result,ledger=ledger(self),full_memory=base.memory_rows(self.u),architectural_cpu=base.architectural_cpu(self.u));self.steps.append(row);print(label,sum(counts.values()),'original instructions;',len(self.api_calls),'actual OS leaves',flush=True);return result['cpu']['EAX']

def run(helper,build):
 live=platform.Live(helper);g=None
 try:
  g=Guest(live);g.root('reset_source_game_accounting',0x4288e0)
  first=g.root('allocate_source_262168',0x428a40,[262168]);first_state=dict(pointer=first,raw_hex=g.read(first-32,262208).hex())
  second=g.root('allocate_source_88_concurrently',0x428a40,[88]);both=[dict(pointer=p,raw_hex=g.read(p-32,n).hex()) for p,n in [(first,262208),(second,128)]]
  g.root('free_source_first_while_second_alive',0x428ad0,[first]);remaining=dict(pointer=second,raw_hex=g.read(second-32,128).hex())
  g.root('free_source_second',0x428ad0,[second]);data=g.root('source_complete_SC004_file_loader',0x42ae20,[PATH]);b=g.read(data,262168);need(sha(b)==FILE_SHA and b==(platform.INSTALLED/'DATA/ADV/BIN/SC004.BIN').read_bytes(),'complete original ReadFile bytes');p,r=g.owned(data,262168);g.sync(p);native=live.request('readback',pointer=r['native']);need(bytes.fromhex(native['hex'])==g.read(p,r['bytes']),'actual entire native readback equals source allocation');file_state=dict(pointer=data,raw_hex=g.read(p,r['bytes']).hex(),file_sha256=sha(b),native_readback_wire_index=len(live.trace)-1)
  g.root('free_source_file_buffer',0x428ad0,[data]);need(not g.allocations and ledger(g)==dict(first=0,last=0,total=524424,current=0,high=262256,next_request=4,game_bytes=0),'all source counters/list naturally balanced');live.close()
 except BaseException:
  if not live.closed:
   try:live.close()
   except BaseException:pass
  raise
 return dict(schema_version=1,fixture_inputs=g.declaration,helper_build=build,native_hello=live.hello,native_trace=live.trace,helper_exit_code=live.exit_code,helper_cleanup=live.cleanup,steps=g.steps,allocation_history=g.history,first_allocation=first_state,concurrent_allocations=both,remaining_allocation=remaining,file_allocation=file_state,original_source_executed=True,retained_heap_restored=False,retained_integration=False,R3_complete=False,new_window=False,new_GPU=False,new_OS_input=False,debug_tracking_enabled=True,heap_mode=1,other_heap_modes_tested=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--helper',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable report')
 helper,build=platform.build(ROOT/a.helper);r=run(helper,build);out.write_bytes(gzip.compress(json.dumps(r,separators=(',',':')).encode(),mtime=0));print('complete source CRT/file lifecycle, separate declared-input fixture',flush=True)
