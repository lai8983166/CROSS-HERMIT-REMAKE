"""Original retained task registration, current events and first scheduler dispatch."""
import copy,gzip,json,struct,types
from functools import lru_cache
from tools import school_retained_fog as previous
from tools import school_retained_scheduler_platform as platform

ROOT=previous.ROOT;base=previous.base;need=previous.need;sha=previous.sha;word=previous.word;canonical=previous.canonical
TACT=previous.TACT;RETURN=previous.RETURN;MANAGER=0x65001000;STACK=0x6530f000
ACCEPTANCE='analysis/school-retained-fog-acceptance-v1-20261023.json'
ACCEPTANCE_SHA='2b485ec36aec7e33a73f369abf67613ca8e65ccd4437fc50823da8cf5a708897'
SLOTS={0x59227c:('InitializeCriticalSection',4),0x592280:('DeleteCriticalSection',4),0x592274:('CreateEventA',16),0x592234:('EnterCriticalSection',4),0x592238:('LeaveCriticalSection',4),0x592228:('ResetEvent',4),0x59222c:('SetEvent',4),0x592270:('CloseHandle',4),0x59226c:('WaitForSingleObject',8),0x59221c:('CreateThread',24)}
dialogue=types.SimpleNamespace(**dict(vars(previous.previous.previous.dialogue),IMPORTS={**previous.previous.previous.dialogue.IMPORTS,**SLOTS}))
opening=types.SimpleNamespace(**dict(vars(previous.previous.previous),dialogue=dialogue))
_loop=previous.previous.previous.adapt(previous.previous.Guest.loop_step,[("if at==self.device_method:frontier(","if at==self.device_method and not getattr(self,'fog_creating',False):frontier("),("if at in self.third_methods:self.new_gpu(at);return","if at==self.device_method or at in self.third_methods:self.new_gpu(at);return"),("if at in targets:\n", "if at in targets and getattr(self,'scheduler_active',False) and targets[at] in (0x59221c,0x59226c):frontier('original_scheduler_thread_platform_dependency',at,import_slot=targets[at],name=SLOTS[targets[at]][0]);return\n  if at in targets:\n")],previous=opening,SLOTS=SLOTS)

@lru_cache(maxsize=1)
def contracts():
 a=json.loads(base.pinned(ACCEPTANCE,ACCEPTANCE_SHA));need(a['tasks_complete']==3 and a['natural_first_wait_entry']['va']==0x422360,'accepted natural original wait entry');return dict(parent_acceptance=ACCEPTANCE,parent_acceptance_sha256=ACCEPTANCE_SHA,previous=previous.contracts(),manager=MANAGER,stack=STACK,platform_source_sha256=sha(platform.SOURCE.read_bytes()),roots=[0x421540,0x421660,0x4216c0,0x4217c0],original_thread_callback=0x451670,scope='fresh declared logical manager/current native synchronization; source registration/first dispatch to legal thread/wait or exact real dependency; not original MAIN/CRT worker lifetime')

def state(g):
 return dict(parent=previous.fog_state(g),task_header_hex=g.read(TACT,0x190).hex(),manager_hex=g.read(MANAGER,512).hex(),accounting=word(g.read(0x79fc74)),allocations=copy.deepcopy(g.allocations if hasattr(g,'allocations') else g.blocks))

class Guest(previous.Guest):
 def loop_step(self,label,stop,root=None):
  if label=='supplemental_original_fog_texture_destructor' and not hasattr(self,'scheduler_record'):self.continue_scheduler()
  return _loop(self,label,stop,root)
 def new_api(self,slot):
  if not getattr(self,'scheduler_active',False) or slot not in SLOTS:return super().new_api(slot)
  name,pop=SLOTS[slot];sp=self.cpu()['ESP'];ret=word(self.read(sp));args=[word(self.read(sp+4+i)) for i in range(0,pop,4)];out=[];value=0;wire=len(self.scheduler_live.trace)
  def put(p,b):self.u.mem_write(p,b);self.memory_evidence.mark(p,len(b));out.append(dict(pointer=p,hex=b.hex()))
  if name in ('InitializeCriticalSection','DeleteCriticalSection','EnterCriticalSection','LeaveCriticalSection'):
   if args!=[MANAGER+0x100]:return super().new_api(slot)
   op={'InitializeCriticalSection':'initialize','DeleteCriticalSection':'delete','EnterCriticalSection':'enter','LeaveCriticalSection':'leave'}[name];q=dict(guest=args[0]);result=self.scheduler_live.request(op,**q)
   if op!='delete':put(args[0],bytes.fromhex(result['hex']))
  elif name=='CreateEventA':
   need(args==[0,0,0,0] and ret in (0x421585,0x42194d),'original manager/node automatic nonsignaled event ABI');op='create_event';q={};result=self.scheduler_live.request(op);value=0x65010000+len(self.scheduler_events)*16;self.scheduler_events[value]=result['handle']
  elif name in ('CloseHandle','SetEvent','ResetEvent'):
   if args[0] not in self.scheduler_events:return super().new_api(slot)
   need(args[0] not in self.scheduler_closed_events,'current live event owner');op={'CloseHandle':'close_event','SetEvent':'set','ResetEvent':'reset'}[name];q=dict(handle=self.scheduler_events[args[0]]);result=self.scheduler_live.request(op,**q);value=result['value']
   if name=='CloseHandle':self.scheduler_closed_events.add(args[0])
  else:raise ValueError('uncovered original scheduler platform operation')
  self.api_calls.append(dict(kind='actual_scheduler_platform',name=name,import_slot=slot,target=word(self.read(slot)),sp=sp,return_va=ret,args=args,pop=pop,value=value,new_mappings=[],memory_outputs=out,native_wire_index=wire,native_op=op,native_request=q,native_result=result));self.u.reg_write(base.REGISTERS['EAX'],value);self.u.reg_write(base.REGISTERS['ESP'],sp+4+pop);self.u.reg_write(base.REGISTERS['EIP'],ret)
 def continue_scheduler(self):
  contracts();need(self.cpu()['EIP']==0x422360 and self.read(TACT+8,4)==bytes(4),'natural retained wait before original registration');context=self.u.context_save();cpu=base.architectural_cpu(self.u);old_stack=self.read(previous.STACK-0x1000,0x2000);entry_memory=base.memory_rows(self.u);self.scheduler_live=platform.Live(self.scheduler_helper);self.scheduler_events={};self.scheduler_closed_events=set();self.scheduler_active=True;e=dict(contract=contracts(),entry_CPU=cpu,entry_memory=entry_memory,retained_stack_pointer=previous.STACK-0x1000,retained_stack_hex=old_stack.hex(),native_build=self.scheduler_build,native_hello=self.scheduler_live.hello,steps=[],cleanup=[],declaration=[]);self.scheduler_record=e;before_allocations=set(self.allocations)
  def root(label,va,receiver,args=()):return self.loop_step(label,RETURN,dict(va=va,receiver=receiver,args=list(args),sp=STACK,return_va=RETURN))
  try:
   for p,n,fill in ((MANAGER,4096,0xa5),(STACK-0xf000,65536,0)):
    need(all(not(a<p+n and p<=b) for a,b,_ in self.u.mem_regions()),'fresh independent scheduler harness storage');raw=bytes([fill])*n;self.u.mem_map(p,n);self.u.mem_write(p,raw);e['declaration'].append(dict(pointer=p,bytes=n,fill=fill))
   self.memory_evidence.refresh();e['declared_state']=state(self)
   for label,va,receiver,args in [('original_manager_constructor',0x421540,MANAGER,()),('original_manager_empty_lists',0x421660,MANAGER,()),('original_retained_task_registration',0x4216c0,MANAGER,(TACT,0,0)),('original_first_scheduler_scan',0x4217c0,MANAGER,())]:
    s=root(label,va,receiver,args);s['scheduler_state']=state(self);e['steps'].append(s)
    if s['pending'] or s['fault']:break
   e['business_final']=state(self);e['business_memory']=base.memory_rows(self.u);e['business_CPU']=base.architectural_cpu(self.u);e['frontier']=copy.deepcopy(e['steps'][-1]['pending'] or e['steps'][-1]['fault']);e['new_allocations']=sorted(set(self.allocations)-before_allocations);e['events']=copy.deepcopy(self.scheduler_events)
   for p in e['new_allocations']:e['cleanup'].append(root('supplemental_original_thread_data_free',0x56f3b0,0,(p+32,2)))
   e['cleanup'].append(root('supplemental_original_task_unlink',0x421d50,MANAGER,(TACT,)))
   node_event=word(self.read(TACT+0x1c));e['supplemental_node_event_close']=None
   if node_event in self.scheduler_events and node_event not in self.scheduler_closed_events:
    start=len(self.scheduler_live.trace);result=self.scheduler_live.request('close_event',handle=self.scheduler_events[node_event]);self.scheduler_closed_events.add(node_event);e['supplemental_node_event_close']=dict(guest_handle=node_event,native_handle=self.scheduler_events[node_event],wire_index=start,result=result,origin='owner supplement; original CRT worker never established')
   e['cleanup'].append(root('supplemental_original_manager_destructor',0x4215f0,MANAGER));e['after_cleanup']=state(self);need(set(self.allocations)==before_allocations and set(self.scheduler_events)==self.scheduler_closed_events,'all new own allocations/events normally released');need(self.read(previous.STACK-0x1000,0x2000)==old_stack,'untouched original ordinary-loop frame');self.u.context_restore(context);need(canonical(base.architectural_cpu(self.u))==canonical(cpu),'full original ordinary-loop CPU restored after declared independent roots');e['restored_CPU']=base.architectural_cpu(self.u);e['restored_memory']=base.memory_rows(self.u)
  finally:
   e['native_cleanup']=self.scheduler_live.close();e['native_exit']=self.scheduler_live.exit_code;e['native_trace']=copy.deepcopy(self.scheduler_live.trace);self.scheduler_active=False

def run_case(helper,build,gpu,gb,role,rb,opening_gpu,ob,name,scene,fog,fb,scheduler,sb):
 instances=[]
 class Attached(Guest):
  def __init__(self,*a,**kw):super().__init__(*a,**kw);self.scheduler_helper=scheduler;self.scheduler_build=sb;instances.append(self)
 call=types.FunctionType(previous.run_case.__code__,dict(previous.run_case.__globals__,Guest=Attached),'source_fog_into_original_registration')
 try:c=call(helper,build,gpu,gb,role,rb,opening_gpu,ob,name,scene,fog,fb)
 except BaseException as exc:
  if instances:
   g=instances[0];p=ROOT/('analysis/school-retained-scheduler-failed-'+scheduler.stem+'-'+name+'-'+str(scene)+'-20261024.json.gz');need(not p.exists(),'preserve immutable source failure');p.write_bytes(gzip.compress(json.dumps(dict(error=repr(exc),accepted=False,scheduler=getattr(g,'scheduler_record',None),CPU=g.cpu()),separators=(',',':')).encode(),mtime=0))
  raise
 c['scheduler']=instances[0].scheduler_record;return c

def build_group(prefix,name):
 tag=prefix+'-'+name;h,hb=previous.previous.platform.build(ROOT/('.venv-audit/'+tag+'-crt.exe'));g,gb=previous.build_gpu(ROOT/('.venv-audit/'+tag+'-fourth.exe'));r,rb=previous.build_gpu(ROOT/('.venv-audit/'+tag+'-role9.exe'));o,ob=previous.build_gpu(ROOT/('.venv-audit/'+tag+'-opening.exe'));f,fb=previous.build_gpu(ROOT/('.venv-audit/'+tag+'-fog.exe'));s,sb=platform.build(ROOT/('.venv-audit/'+tag+'-scheduler.exe'));return h,hb,g,gb,r,rb,o,ob,f,fb,s,sb

def produce_one(built,name,scene):
 h,hb,g,gb,r,rb,o,ob,f,fb,s,sb=built;return run_case(h,hb,g,gb,r,rb,o,ob,name,scene,f,fb,s,sb)

def produce_group(args):
 import contextlib
 name,prefix,existing=args;built=None;rows=[]
 with open(ROOT/('analysis/'+prefix+'-'+name+'.log'),'x',encoding='utf8',buffering=1) as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
  for scene in (76,77):
   if name=='initial' and scene==76 and existing:
    path=existing
    with gzip.open(ROOT/path,'rt',encoding='utf8') as f:c=json.load(f)
    need(c['scheduler']['contract']==contracts() and (c['name'],c['scene_capture'])==(name,scene),'exact completed first source case')
   else:
    if built is None:built=build_group(prefix,name)
    path='analysis/'+prefix+'-'+name+'-'+str(scene)+'.json.gz';need(not (ROOT/path).exists(),'fresh immutable scheduler case');c=produce_one(built,name,scene);previous.previous.previous.write_report(path,c)
   b=(ROOT/path).read_bytes();rows.append(dict(name=name,scene_capture=scene,path=path,sha256=sha(b),bytes=len(b)));print('complete source scheduler case',name,scene,flush=True);del c
 return rows

if __name__=='__main__':
 import argparse
 from concurrent.futures import ProcessPoolExecutor
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--existing-initial76');p.add_argument('--jobs',type=int,default=3);a=p.parse_args();out=ROOT/a.out
 if out.exists() or not 1<=a.jobs<=3:p.error('fresh immutable matrix and bounded 1..3 workers')
 groups=[(n,out.stem,a.existing_initial76) for n in ('initial','student9_waiting','fifth_class')];rows=[]
 if a.jobs==1:
  for group in groups:rows.extend(produce_group(group))
 else:
  with ProcessPoolExecutor(max_workers=a.jobs) as pool:
   for group in pool.map(produce_group,groups):rows.extend(group)
 matrix=previous.matrix_header(rows);matrix['contract']=contracts();matrix['source_processes']=a.jobs;out.write_text(json.dumps(matrix,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('SIX_SOURCE_SCHEDULER_CASES_COMPLETE',flush=True)
