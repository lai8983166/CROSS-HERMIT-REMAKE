"""Original native scheduler lifecycle in isolated buffers of an exclusively owned game."""
import ctypes as C,ctypes.wintypes as W,hashlib,json,struct,time,types
from pathlib import Path
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools import school_startup_lifetime as original

ROOT=original.ROOT;SOURCE=original.SOURCE;SOURCE_SHA=original.SOURCE_SHA
METHODS={0x421540:0,0x421660:0,0x422290:0,0x4216c0:3,0x4217c0:0,0x4215f0:0,0x4222d0:0,0x422560:1,0x4225a0:1}
RANGES=((0x421540,0x421be3),(0x421bf0,0x422289),(0x422290,0x422354),(0x422560,0x42260a),(0x42b2d0,0x42b2ef),(0x56e050,0x56e1e0),(0x56e1e0,0x56e230),(0x4539b0,0x453cfc),(0x594a54,0x594a5c))
IAT=(0x592228,0x59222c,0x592230,0x592234,0x592238,0x592260,0x592264,0x592268,0x59226c,0x592270,0x592274,0x59227c,0x592280)

def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,msg):
 if not v:raise ValueError(msg)
def word(b,at=0):return struct.unpack_from('<I',b,at)[0]

def call_thunk():
 # Remote LPTHREAD_START_ROUTINE: only the private parameter block is written.
 b=bytearray.fromhex('558bec5356578b75088966208b5e0885db');jz=len(b);b+=b'\x74\0';loop=len(b)
 b+=bytes.fromhex('4bff749e0c85db');jnz=len(b);b+=b'\x75\0';end=len(b)
 b[jz+1]=end-(jz+2);b[jnz+1]=(loop-(jnz+2))&255
 b+=bytes.fromhex('8b4e04ff1689461c896624c7462843414c4c31c05f5e5b5dc20400')
 return bytes(b)

def source_contract():
 raw=SOURCE.read_bytes();need(sha(raw)==SOURCE_SHA,'source identity');md=Cs(CS_ARCH_X86,CS_MODE_32)
 checks={0x4217ef:('cmp','dword ptr [ebp - 8], 0x20'),0x42182a:('call','0x421850'),0x421ed3:('call','0x56e050'),0x421eca:('push','0x421f50'),0x421f88:('call','dword ptr [eax]'),0x422021:('call','0x56e1e0'),0x4217b6:('ret','0xc'),0x421be0:('ret','4'),0x4222b0:('mov','dword ptr [eax], 0x594a54'),0x421c23:('je','0x421c51')}
 rows=[]
 for at,want in checks.items():
  i=next(md.disasm(raw[at-0x400000:at-0x400000+16],at));need((i.mnemonic,i.op_str)==want,'source operand '+hex(at));rows.append(dict(va=at,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
 need(list(struct.unpack_from('<2I',raw,0x594a54-0x400000))==[0x422330,0x422300],'original base task vtable')
 return dict(source_sha256=SOURCE_SHA,ranges=[dict(va=a,bytes=b-a,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in RANGES],instructions=rows,base_task_vtable=0x594a54,base_callback=0x422330,worker=0x421f50,runtime_beginthreadex=0x56e050,runtime_endthreadex=0x56e1e0,original_IAT_slots=list(IAT),call_thunk_hex=call_thunk().hex(),source_callbacks_replaced=False,retained_scene_or_world_execution=False)

alloc=original.bind('VirtualAllocEx',C.c_void_p,[W.HANDLE,C.c_void_p,C.c_size_t,W.DWORD,W.DWORD])
free=original.bind('VirtualFreeEx',W.BOOL,[W.HANDLE,C.c_void_p,C.c_size_t,W.DWORD])
write=original.bind('WriteProcessMemory',W.BOOL,[W.HANDLE,C.c_void_p,C.c_void_p,C.c_size_t,C.POINTER(C.c_size_t)])
protect=original.bind('VirtualProtectEx',W.BOOL,[W.HANDLE,C.c_void_p,C.c_size_t,W.DWORD,C.POINTER(W.DWORD)])
flush=original.bind('FlushInstructionCache',W.BOOL,[W.HANDLE,C.c_void_p,C.c_size_t])
remote=original.bind('CreateRemoteThread',W.HANDLE,[W.HANDLE,C.c_void_p,C.c_size_t,C.c_void_p,C.c_void_p,W.DWORD,C.POINTER(W.DWORD)])
exit_thread=original.bind('GetExitCodeThread',W.BOOL,[W.HANDLE,C.POINTER(W.DWORD)])
duplicate=original.bind('DuplicateHandle',W.BOOL,[W.HANDLE,W.HANDLE,W.HANDLE,C.POINTER(W.HANDLE),W.DWORD,W.BOOL,W.DWORD])
current_process=original.bind('GetCurrentProcess',W.HANDLE,[])

class NativeCalls:
 def __init__(self,pid,owned):
  need(pid in owned.members(),'only owned Job process');self.pid=pid;self.owned=owned;self.h=original.openp(0x1fffff,False,pid);original.check(self.h,'own process write/query handle')
  self.blocks=[];self.calls=[];self.writes=[];self.kernel_close=None;self.active=None;self.allowed_closes=set()
  self.data=self.reserve(0x10000);self.code=self.reserve(4096)
  self.put(self.code,call_thunk());old=W.DWORD();original.check(protect(self.h,self.code,4096,0x20,C.byref(old)),'private thunk RX');original.check(flush(self.h,self.code,len(call_thunk())),'private instruction cache')
  self.kernel_close=word(self.get(0x592270,4))
 def reserve(self,n):
  p=alloc(self.h,None,n,0x3000,4);need(p and p+n<=0x100000000 and all(not a<=p<a+s for a,s in self.blocks),'fresh private x86 allocation');self.blocks.append((p,n));return p
 def get(self,p,n):return original.required(self.h,p,n)
 def put(self,p,b):
  need(any(a<=p and p+len(b)<=a+n for a,n in self.blocks),'write only new private allocation')
  got=C.c_size_t();buffer=C.create_string_buffer(b);original.check(write(self.h,p,buffer,len(b),C.byref(got)) and got.value==len(b),'owned private write')
  self.writes.append(dict(pointer=p,bytes=len(b),sha256=sha(b)))
 def call(self,va,receiver,args=(),label='source'):
  need(self.pid in self.owned.members() and self.active is None,'exclusive live owned call')
  need((va in METHODS and len(args)==METHODS[va]) or (va==self.kernel_close and receiver==0 and len(args)==1 and label=='supplemental_CloseHandle'),'bounded source entry/ABI')
  need(va==self.kernel_close or self.data<=receiver<self.data+0x10000,'private source receiver')
  manager=self.data+0x1000;nodes={self.data+0x2000+i*0x1000 for i in range(8)}
  if va==self.kernel_close:need(args[0] in self.allowed_closes,'only observed exited owned worker handle may be closed')
  elif va in (0x421540,0x421660,0x4217c0,0x4215f0):need(receiver==manager,'exact private manager')
  elif va==0x4216c0:need(receiver==manager and args[0] in nodes and 0<=args[1]<32 and 0<=args[2]<=0xffffffff,'private node and bounded original bucket')
  else:need(receiver in nodes and (not args or args==(2,)),'exact private node/disabled flag')
  block=struct.pack('<11I',va,receiver,len(args),*(list(args)+[0]*(3-len(args))),0,0xcccccccc,0xcccccccc,0xcccccccc,0)
  self.put(self.data,block);tid=W.DWORD();th=remote(self.h,None,0,self.code,self.data,0,C.byref(tid));original.check(th,'owned call entry thread');self.active=th
  try:
   status=original.wait(th,10000);need(status==0,'native source call must actually finish');code=W.DWORD();original.check(exit_thread(th,C.byref(code)),'native call thread exit');after=self.get(self.data,44)
   need(code.value==0 and word(after,40)==0x4c4c4143 and word(after,32)==word(after,36),'native source call completion and exact ESP cleanup')
   row=dict(label=label,va=va,receiver=receiver,args=list(args),thread_id=tid.value,wait_status=status,thread_exit_code=code.value,parameter_before_hex=block.hex(),parameter_after_hex=after.hex(),eax=word(after,28));self.calls.append(row)
   if va==self.kernel_close:self.allowed_closes.remove(args[0])
   return row
  finally:
   if original.wait(th,0)==0:original.close(th);self.active=None
 def state(self,manager,nodes):return dict(manager_hex=self.get(manager,0x200).hex(),nodes=[dict(pointer=p,hex=self.get(p,0x80).hex()) for p in nodes])
 def close(self):
  if self.active is not None:
   original.close(self.active);original.close(self.h)
   return [dict(pointer=p,bytes=n,released=False,reason='deferred to owned Job teardown; running source call memory is never freed') for p,n in self.blocks]
  rows=[]
  for p,n in reversed(self.blocks):rows.append(dict(pointer=p,bytes=n,released=bool(free(self.h,p,0,0x8000))))
  original.close(self.h);need(all(r['released'] for r in rows),'all private buffers freed');return rows

def live_identity(c):
 raw=SOURCE.read_bytes();rows=[]
 for a,b in RANGES:
  data=c.get(a,b-a);need(data==raw[a-0x400000:b-0x400000],'unchanged actual original code '+hex(a));rows.append(dict(pointer=a,bytes=b-a,sha256=sha(data)))
 return dict(code=rows,IAT=[dict(slot=p,hex=c.get(p,4).hex()) for p in IAT])

def closed_event(c,handle,label):
 local=W.HANDLE();C.set_last_error(0)
 ok=bool(duplicate(c.h,handle,current_process(),C.byref(local),0,False,2));error=C.get_last_error()
 if ok:original.close(local)
 need(not ok and error==6,'original event handle must actually be invalid after source cleanup')
 return dict(label=label,handle=handle,duplicate_succeeded=ok,error=error)

def retained_empty_graph():
 from tools.school_vm_graphics_verification import load_verified_checkpoint,read_memory
 payload,cp=load_verified_checkpoint('initial','rectangle')
 main=word(read_memory(payload,0x7a4a00,4));manager=main+0x64;contents=read_memory(payload,manager,0x11c)
 need(main==0x1080000 and contents==bytes(0x11c),'pinned empty retained scheduler graph')
 return dict(checkpoint=cp,main_global=main,manager=manager,manager_hex=contents.hex(),nodes=[],retained_VM_advanced=False)

def native_probe(pid,owned,fill=0xa5,buckets=(0,0,31),disabled=1):
 c=NativeCalls(pid,owned);manager=c.data+0x1000;nodes=[c.data+0x2000+i*0x1000 for i in range(len(buckets))]
 r=dict(fill=fill,buckets=list(buckets),disabled=disabled,manager=manager,nodes=nodes,private_allocations=[dict(pointer=p,bytes=n) for p,n in c.blocks],source_before=live_identity(c),stages=[],worker_threads=[],closed_events=[])
 def stage(label):r['stages'].append(dict(label=label,**c.state(manager,nodes)))
 try:
  c.put(manager,bytes([fill])*0x200)
  for p in nodes:c.put(p,bytes([fill])*0x80)
  stage('declared_fresh_buffers');c.call(0x421540,manager);c.call(0x421660,manager);stage('original_manager_initialized')
  for i,p in enumerate(nodes):c.call(0x422290,p);c.call(0x4216c0,manager,(p,buckets[i],0x12340000+i));stage('registered_'+str(i))
  if disabled is not None:c.call(0x422560,nodes[disabled],(2,));stage('original_disabled_flag')
  c.call(0x4217c0,manager);stage('first_original_dispatch')
  completed=[i for i in range(len(nodes)) if i!=disabled]
  for i in completed:r['closed_events'].append(closed_event(c,word(c.get(nodes[i]+0x1c,4)),'first_node_'+str(i)))
  for i in completed:
   p=nodes[i];handle=word(c.get(p+0x20,4));local=W.HANDLE();original.check(duplicate(c.h,handle,current_process(),C.byref(local),0,False,2),'own worker thread duplicate')
   try:
    status=original.wait(local,5000);code=W.DWORD();original.check(exit_thread(local,C.byref(code)),'original CRT worker exit');need(status==0 and code.value==0,'original worker actually ended')
    r['worker_threads'].append(dict(index=i,handle=handle,thread_id=word(c.get(p+0x24,4)),wait_status=status,exit_code=code.value))
   finally:original.close(local)
   c.allowed_closes.add(handle);need(c.call(c.kernel_close,0,(handle,),label='supplemental_CloseHandle')['eax']==1,'supplemental leaked original thread handle close')
  if disabled is not None:
   c.call(0x4225a0,nodes[disabled],(2,));stage('original_reenabled_flag');c.call(0x4217c0,manager);stage('second_original_dispatch')
   p=nodes[disabled];handle=word(c.get(p+0x20,4));local=W.HANDLE();original.check(duplicate(c.h,handle,current_process(),C.byref(local),0,False,2),'own final worker duplicate')
   r['closed_events'].append(closed_event(c,word(c.get(p+0x1c,4)),'second_node_'+str(disabled)))
   try:
    status=original.wait(local,5000);code=W.DWORD();original.check(exit_thread(local,C.byref(code)),'final worker exit');need(status==0 and code.value==0,'final source worker actually ended')
    r['worker_threads'].append(dict(index=disabled,handle=handle,thread_id=word(c.get(p+0x24,4)),wait_status=status,exit_code=code.value))
   finally:original.close(local)
   c.allowed_closes.add(handle);need(c.call(c.kernel_close,0,(handle,),label='supplemental_CloseHandle')['eax']==1,'last supplemental thread close')
  c.call(0x4215f0,manager)
  r['closed_events'].append(closed_event(c,word(c.get(manager+0x118,4)),'manager_after_destructor'))
  for p in nodes:c.call(0x4222d0,p)
  stage('original_destructors_returned');r['source_after']=live_identity(c);need(r['source_before']==r['source_after'],'all original code/IAT unchanged')
 finally:
  r['calls']=c.calls;r['private_writes']=c.writes;r['private_frees']=c.close()
 return r

def observe_case(fill,buckets,disabled):
 owners=[];probe=[]
 def own():
  o=original.OwnedOriginal();owners.append(o);return o
 def post(hwnd,msg,w,l):
  need(msg==16 and len(owners)==1 and not probe,'only own original close boundary')
  pid=W.DWORD();original.ownerpid(hwnd,C.byref(pid));need(pid.value in owners[0].members(),'native probe belongs to owned Job')
  probe.append(native_probe(pid.value,owners[0],fill,buckets,disabled));return original.post(hwnd,msg,w,l)
 observe=types.FunctionType(original.observe.__code__,dict(original.observe.__globals__,OwnedOriginal=own,post=post),'observe_scheduler_case',original.observe.__defaults__)
 lifecycle=observe(False)
 return dict(fill=fill,buckets=list(buckets),disabled=disabled,native_scheduler_probe=probe[0] if probe else None,original_lifecycle=lifecycle,private_process_buffers_written=True,original_code_or_IAT_written=False,original_general_registers_replaced=False,retained_scene_execution=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--cases',type=int,default=3);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable report path required')
 cases=[]
 for i,(fill,buckets,disabled) in enumerate([(0,(0,),None),(0xa5,(0,0,31),1),(0xcc,(31,5,5),0)][:a.cases]):
  case=observe_case(fill,buckets,disabled);cases.append(case);print('native scheduler',i,'error',case['original_lifecycle']['error'],'probe',case['native_scheduler_probe']is not None,flush=True)
  if case['original_lifecycle']['error']:break
 result=dict(schema_version=1,source_contract=source_contract(),cases=cases,R3_complete=False,retained_VM_or_world_advanced=False)
 out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
 if any(c['original_lifecycle']['error'] for c in cases):raise SystemExit(1)
