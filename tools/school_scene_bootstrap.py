"""Native derived scene construction and explicit isolated cooperative probes."""
import ctypes as C,ctypes.wintypes as W,gzip,json,struct,types
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools import school_scheduler_lifetime as parent

ROOT=parent.ROOT;SOURCE=parent.SOURCE;SOURCE_SHA=parent.SOURCE_SHA
SIZE=0x1194f0
RANGES=parent.RANGES+((0x451080,0x45199b),(0x4519c0,0x451b10),(0x439ef0,0x43a060),(0x422090,0x422289),(0x422360,0x422560),(0x59a430,0x59a438))
IAT=parent.IAT+(0x5920a0,0x592068,0x5920c4)
METHODS={**parent.METHODS,0x451170:0,0x451470:0,0x421d50:1,0x422360:1}
need=parent.need;word=parent.word;sha=parent.sha

def source_contract():
 raw=SOURCE.read_bytes();need(sha(raw)==SOURCE_SHA,'source SHA');md=Cs(CS_ARCH_X86,CS_MODE_32)
 checks={0x4510ad:('push','0x1194f0'),0x4510cd:('call','0x451170'),0x4510ee:('mov','dword ptr [0x7a4174], ecx'),0x4510fa:('mov','byte ptr [edx + 0x28], 1'),0x451148:('call','0x4216c0'),0x4511a5:('call','0x439ef0'),0x45121c:('mov','dword ptr [ecx], 0x59a430'),0x4516d0:('call','0x422360'),0x451711:('call','0x451a60'),0x451ab7:('call','0x4539b0'),0x4539ec:('call','0x454cf0'),0x453a0c:('call','0x46b470'),0x42238c:('mov','dword ptr [edx + 0x14], eax'),0x422407:('call','dword ptr [0x59226c]'),0x42241c:('call','0x4225a0'),0x4218a9:('mov','dword ptr [edx + 0x14], ecx')}
 rows=[]
 for at,want in checks.items():
  i=next(md.disasm(raw[at-0x400000:at-0x400000+16],at));need((i.mnemonic,i.op_str)==want,'scene source '+hex(at));rows.append(dict(va=at,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
 need(struct.unpack_from('<2I',raw,0x59a430-0x400000)==(0x451670,0x451630),'scene virtual callback/destructor')
 return dict(source_sha256=SOURCE_SHA,object_bytes=SIZE,vtable=0x59a430,thread_callback=0x451670,state_dispatch=0x451a60,world_loop=0x4539b0,ranges=[dict(pointer=a,bytes=b-a,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in RANGES],instructions=rows,IAT_slots=list(IAT),original_scene_callback_executed=False,original_factory_invoked=False,scope='private derived object and isolated yield roots; not retained scene execution')

class SceneCalls(parent.NativeCalls):
 def reserve(self,n):return super().reserve(0x200000 if n==0x10000 else n)
 def validate(self,va,receiver,args):
  need(self.pid in self.owned.members(),'owned Job only')
  if va==getattr(self,'font_query',None):
   need(receiver==0 and args==(self.font,60,self.data+0x400),'observed own font/private LOGFONT only');return
  need(va in METHODS and len(args)==METHODS[va],'scene entry/ABI whitelist')
  manager=self.data+0x1000;node=self.data+0x2000
  if va in (0x421540,0x421660,0x4217c0,0x4215f0):need(receiver==manager,'exact private manager')
  elif va==0x4216c0:need(receiver==manager and args==(node,0,0),'exact private source scene registration')
  elif va==0x421d50:need(receiver==manager and args==(node,),'exact private unlink')
  else:
   need(receiver==node,'exact private node')
   if va==0x422560:need(args in ((1,),(2,)),'only source active/disabled masks')
   if va==0x4225a0:need(args==(-1&0xffffffff,),'only full flag cleanup')
   if va==0x422360:need(args==(2,),'declared bounded delay2')
 def start(self,va,receiver,args=(),slot=0):
  self.validate(va,receiver,args);need(slot in (0,0x100) and slot not in self.pending,'exclusive private parameter slot')
  if self.pending:need(0 in self.pending and self.pending[0][1]['va']==0x422360 and slot==0x100 and va==0x4217c0,'only delay tick may overlap isolated yield')
  else:need(slot==0,'ordinary calls use primary slot')
  b=struct.pack('<11I',va,receiver,len(args),*(list(args)+[0]*(3-len(args))),0,0xcccccccc,0xcccccccc,0xcccccccc,0);self.put(self.data+slot,b)
  tid=W.DWORD();th=parent.remote(self.h,None,0,self.code,self.data+slot,0,C.byref(tid));parent.original.check(th,'owned scene source call')
  row=dict(va=va,receiver=receiver,args=list(args),slot=slot,sequence=self.sequence,thread_id=tid.value,parameter_before_hex=b.hex());self.sequence+=1;self.pending[slot]=(th,row);return th
 def finish(self,slot=0):
  th,row=self.pending[slot];status=parent.original.wait(th,10000);need(status==0,'actual scene call exit');code=W.DWORD();parent.original.check(parent.exit_thread(th,C.byref(code)),'scene thread exit')
  b=self.get(self.data+slot,44);need(code.value==0 and word(b,40)==0x4c4c4143 and word(b,32)==word(b,36),'native scene source ESP/exit')
  row.update(wait_status=status,exit_code=code.value,parameter_after_hex=b.hex(),eax=word(b,28));self.calls.append(row);parent.original.close(th);del self.pending[slot];return row
 def call(self,va,receiver,args=(),slot=0):self.start(va,receiver,args,slot);return self.finish(slot)
 def close(self):
  if self.pending:
   for th,row in self.pending.values():parent.original.close(th)
   parent.original.close(self.h);return [dict(pointer=p,bytes=n,released=False,reason='deferred to owned Job teardown; source call remains active') for p,n in self.blocks]
  return super().close()
 def __init__(self,*args):self.pending={};self.sequence=0;super().__init__(*args)

def font_state(c,label):
 before=b'\xa5'*76;c.put(c.data+0x400,before);row=c.call(c.font_query,0,(c.font,60,c.data+0x400));after=c.get(c.data+0x400,76)
 return dict(label=label,handle=c.font,bytes_returned=row['eax'],before_hex=before.hex(),after_hex=after.hex())

def identity(c):
 raw=SOURCE.read_bytes();code=[]
 for a,b in RANGES:
  value=c.get(a,b-a);need(value==raw[a-0x400000:b-0x400000],'live scene source identity');code.append(dict(pointer=a,bytes=b-a,sha256=sha(value)))
 return dict(code=code,IAT=[dict(slot=p,hex=c.get(p,4).hex()) for p in IAT])

def object_probe(pid,owned,fill):
 c=SceneCalls(pid,owned);manager=c.data+0x1000;node=c.data+0x2000;r=dict(kind='derived_object',fill=fill,manager=manager,node=node,allocations=[dict(pointer=a,bytes=n) for a,n in c.blocks],source_before=identity(c),stages=[])
 def stage(label):r['stages'].append(dict(label=label,manager_hex=c.get(manager,512).hex(),node_hex=c.get(node,SIZE+32).hex()))
 try:
  c.put(manager,bytes([fill])*512);c.put(node,bytes([fill])*(SIZE+32));stage('declared_fresh_buffers')
  c.call(0x421540,manager);c.call(0x421660,manager);c.call(0x451170,node);stage('original_scene_constructed')
  need(word(c.get(node,4))==0x59a430,'actual derived scene vtable');font=word(c.get(node+0x117f24,4));need(font,'real scene font handle')
  r['source_font_handle']=font
  c.font=font;c.font_query=word(c.get(0x592068,4));r['font_states']=[font_state(c,'source_constructor_font')]
  c.call(0x4216c0,manager,(node,0,0));stage('original_registered')
  c.call(0x422560,node,(2,));stage('original_disabled');c.call(0x4217c0,manager);stage('original_disabled_scan')
  c.call(0x421d50,manager,(node,));stage('original_unlinked');c.call(0x451470,node);stage('original_scene_destructed');r['font_states'].append(font_state(c,'after_source_destructor'));c.call(0x4215f0,manager);stage('original_manager_destructed')
  need(r['font_states'][0]['bytes_returned']==60 and r['font_states'][1]['bytes_returned']==0,'actual font lifetime')
  r['source_after']=identity(c);need(r['source_before']==r['source_after'],'unchanged original scene code/IAT')
 finally:r.update(calls=c.calls,writes=c.writes,frees=c.close())
 return r

new_event=parent.original.bind('CreateEventW',W.HANDLE,[C.c_void_p,W.BOOL,W.BOOL,W.LPCWSTR])
set_event=parent.original.bind('SetEvent',W.BOOL,[W.HANDLE])

def yield_probe(pid,owned):
 c=SceneCalls(pid,owned);manager=c.data+0x1000;node=c.data+0x2000;r=dict(kind='isolated_yield',manager=manager,node=node,allocations=[dict(pointer=a,bytes=n) for a,n in c.blocks],source_before=identity(c),stages=[],event_seed_owner='experiment actual CreateEvent/DuplicateHandle; not source callback-created',original_CRT_callback=False,experimental_release=True)
 locals=[]
 def stage(label):r['stages'].append(dict(label=label,manager_hex=c.get(manager,512).hex(),node_hex=c.get(node,128).hex()))
 def status(th):
  code=W.DWORD();parent.original.check(parent.exit_thread(th,C.byref(code)),'actual isolated yield thread status')
  with parent.original.frozen(c.h,pid,[c.pending[0][1]['thread_id']]) as frames:
   need(len(frames)==1,'actual isolated yield thread context');frame=frames[0];frame['stack_start']=frame['ESP'];frame['stack_hex']=c.get(frame['ESP'],128).hex()
  return dict(wait_status=parent.original.wait(th,0),exit_code=code.value,frame=frame)
 try:
  c.put(manager,bytes(512));c.put(node,bytes(128));c.call(0x421540,manager);c.call(0x421660,manager);c.call(0x422290,node);c.call(0x4216c0,manager,(node,0,0));stage('source_base_registered')
  event=new_event(None,False,False,None);parent.original.check(event,'actual owned node event');locals.append(event);target=W.HANDLE();parent.original.check(parent.duplicate(parent.current_process(),event,c.h,C.byref(target),0,False,2),'declared actual node event duplicate');r['node_event']=target.value;c.put(node+0x1c,struct.pack('<I',target.value))
  manager_event=word(c.get(manager+0x118,4));local_manager=W.HANDLE();parent.original.check(parent.duplicate(c.h,manager_event,parent.current_process(),C.byref(local_manager),0,False,2),'own source manager event duplicate');locals.append(local_manager)
  c.call(0x422560,node,(1,));stage('declared_owned_event_and_source_active')
  th=c.start(0x422360,node,(2,));need(parent.original.wait(local_manager,5000)==0,'original yield actually signals source manager event');r['blocked_before_ticks']=status(th);stage('original_yield_blocked')
  r['tick_statuses']=[]
  for i in range(2):c.call(0x4217c0,manager,slot=0x100);r['tick_statuses'].append(status(th));stage('original_delay_tick_'+str(i+1))
  parent.original.check(set_event(event),'explicit experimental release of actual shared node event');r['release_SetEvent_result']=True;c.finish();r['returned_thread']=dict(wait_status=0,exit_code=c.calls[-1]['exit_code']);stage('original_yield_returned')
  c.call(0x4225a0,node,(0xffffffff,));c.call(0x421d50,manager,(node,));c.call(0x4222d0,node);stage('source_base_unlinked_destructed')
  duplicate_closed=W.HANDLE();parent.original.check(parent.duplicate(c.h,target,parent.current_process(),C.byref(duplicate_closed),0,False,3),'supplemental owned event remote handle close');parent.original.close(duplicate_closed);r['node_event_after_supplemental_close']=parent.closed_event(c,target.value,'isolated_node_after_owner_close')
  c.call(0x4215f0,manager);r['manager_event_after_source_destructor']=parent.closed_event(c,manager_event,'manager_after_source_destructor');stage('source_manager_destructed');r['source_after']=identity(c);need(r['source_before']==r['source_after'],'unchanged yield source/IAT')
 finally:
  for h in locals:parent.original.close(h)
  r.update(calls=c.calls,writes=c.writes,frees=c.close())
 return r

def observe(probe):
 owners=[];results=[]
 def own():o=parent.original.OwnedOriginal();owners.append(o);return o
 def post(hwnd,msg,w,l):
  need(msg==16 and len(owners)==1 and not results,'only original owned close boundary');pid=W.DWORD();parent.original.ownerpid(hwnd,C.byref(pid));need(pid.value in owners[0].members(),'owned scene probe HWND')
  results.append(probe(pid.value,owners[0]));return parent.original.post(hwnd,msg,w,l)
 fn=types.FunctionType(parent.original.observe.__code__,dict(parent.original.observe.__globals__,OwnedOriginal=own,post=post),'observe_scene_bootstrap',parent.original.observe.__defaults__)
 lifecycle=fn(False);return dict(probe=results[0] if results else None,lifecycle=lifecycle,private_buffers_written=True,source_code_or_IAT_replaced=False,retained_scene_advanced=False)

def save(path,r):
 path=ROOT/path;need(not path.exists(),'fresh immutable scene report');path.write_bytes(gzip.compress(json.dumps(r,separators=(',',':')).encode(),mtime=0))

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--fill',type=lambda x:int(x,0),choices=[0,165,204],default=0);p.add_argument('--yield-probe',action='store_true');a=p.parse_args();contract=source_contract();case=observe(yield_probe if a.yield_probe else lambda pid,owned:object_probe(pid,owned,a.fill));save(a.out,dict(schema_version=1,source_contract=contract,case=case,R3_complete=False));print('scene bootstrap',a.fill,'yield',a.yield_probe,'error',case['lifecycle']['error'],'probe',case['probe'] is not None)
 if case['lifecycle']['error']:raise SystemExit(1)
