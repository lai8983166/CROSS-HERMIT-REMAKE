"""Independent original registration/dispatch replay and current synchronization owners."""
import copy,gzip,json,os,struct,types
from functools import lru_cache
from unicorn import UcError
from tools import school_retained_scheduler as work
from tools import school_retained_fog_verification as previous

ROOT=work.ROOT;base=work.base;need=work.need;sha=work.sha;word=work.word;canonical=work.canonical
_step=work.previous.previous.previous.adapt(previous.previous.Replay.loop_step,[("elif p['kind']=='new_texture_dependency':", "elif p['kind']=='original_scheduler_thread_platform_dependency':\n   slot=p['import_slot'];need(slot in (0x59221c,0x59226c) and word(self.read(slot))==at and p['name']==work.SLOTS[slot][0],'exact original thread/wait dependency');expected.update(import_slot=slot,name=p['name'])\n  elif p['kind']=='new_texture_dependency':")],work=types.SimpleNamespace(**dict(vars(work.previous.previous),SLOTS=work.SLOTS)))

class Replay(previous.Replay):
 loop_code=work.previous.previous.previous.adapt(previous.previous.previous.Replay.source_step,[("if at==a['boundary']:","if at==a['boundary'] and not s['fault']:"),("'actual_opening_CRT','actual_role9_CRT','recorded_task_platform'","'actual_opening_CRT','actual_role9_CRT','recorded_task_platform','actual_world_static_lock','actual_fog_GPU','actual_scheduler_platform'"),("count=2000000,timeout=120000000","count=8000000,timeout=240000000"),("finally:self.u.hook_del(ch);self.u.hook_del(wr)","except UcError as exc:need(s['fault'] is not None and str(exc)==s['unicorn_error'],'exact independently observed original scheduler fault')\n finally:self.u.hook_del(ch);self.u.hook_del(wr)")],UcError=UcError,work=work.opening)
 def loop_step(self,s):
  if s['label']=='supplemental_original_fog_texture_destructor' and not hasattr(self,'scheduler_proof'):verify_scheduler(self)
  return _step(self,s)
 def api(self,a):
  if a.get('kind')!='actual_scheduler_platform':return super().api(a)
  slot=a['import_slot'];need(slot in work.SLOTS,'declared scheduler IAT');name,pop=work.SLOTS[slot];sp=self.cpu()['ESP'];ret=word(self.read(sp));args=[word(self.read(sp+4+i)) for i in range(0,pop,4)];need(a['name']==name and a['args']==args and a['sp']==sp and a['pop']==pop and a['return_va']==ret and a['target']==a['va']==word(self.read(slot)) and a['new_mappings']==[],'entire original scheduler API/caller/stack');e=self.case['scheduler'];i=self.scheduler_wire;need(a['native_wire_index']==i and i<len(e['native_trace']),'exact scheduler native cursor');wire=e['native_trace'][i];native=wire['reply']['result'];need(wire['request']==dict(id=i+1,op=a['native_op'],**a['native_request']) and wire['reply']['id']==i+1 and wire['reply']['ok']is True and a['native_result']==native,'actual same-owner scheduler native request/reply');self.scheduler_wire+=1;out=[];value=0
  if name in ('InitializeCriticalSection','DeleteCriticalSection','EnterCriticalSection','LeaveCriticalSection'):
   need(args==[work.MANAGER+256],'same current source manager lock');op={'InitializeCriticalSection':'initialize','DeleteCriticalSection':'delete','EnterCriticalSection':'enter','LeaveCriticalSection':'leave'}[name];q=dict(guest=args[0]);need(a['native_op']==op and a['native_request']==q,'exact native manager lock operation')
   if op=='initialize':need(not self.scheduler_lock_live and len(bytes.fromhex(native['hex']))==24 and ret==0x42156e,'original constructor initializes fresh actual x86 lock');self.scheduler_lock_live=True
   else:need(self.scheduler_lock_live,'original live initialized manager lock')
   if op=='delete':need(self.scheduler_depth==0 and ret==0x421626 and native==dict(value=1),'original unlocked manager lock destructor');self.scheduler_lock_live=False
   else:
    if op in ('enter','leave'):self.scheduler_depth+=1 if op=='enter' else -1;need(0<=self.scheduler_depth<=4 and native['depth']==self.scheduler_depth,'bounded original lock depth')
    out=[dict(pointer=args[0],hex=native['hex'])]
  elif name=='CreateEventA':
   need(args==[0,0,0,0] and ret in (0x421585,0x42194d) and a['native_op']=='create_event' and a['native_request']=={} and native['handle'] and len(self.scheduler_events)<2,'original automatic nonsignaled manager/node event creation');value=0x65010000+16*len(self.scheduler_events);need(native['handle'] not in self.scheduler_events.values(),'separate live current native event owners');self.scheduler_events[value]=native['handle']
  else:
   need(name in ('CloseHandle','SetEvent','ResetEvent') and args[0] in self.scheduler_events and args[0] not in self.scheduler_closed_events,'only a live current own event operation');op={'CloseHandle':'close_event','SetEvent':'set','ResetEvent':'reset'}[name];need(a['native_op']==op and a['native_request']==dict(handle=self.scheduler_events[args[0]]) and native==dict(value=1),'original operation uses exact actual source event');value=1
   if name=='CloseHandle':self.scheduler_closed_events.add(args[0])
  need(a['value']==value and a['memory_outputs']==out,'every scheduler leaf value and entire actual opaque output');self.apply_outputs(a);self.api_return(value,pop,ret,sp)

prepare=types.FunctionType(previous.prepare.__code__,dict(previous.prepare.__globals__,Replay=Replay),'independent_parent_into_scheduler_replay')

def protocol(c):
 previous.protocol(c);e=c['scheduler'];need(e['contract']==work.contracts(),'all accepted scheduler/parent/platform identities');need(e['native_build']['source_sha256']==work.contracts()['platform_source_sha256'] and e['native_build']['machine']==0x14c,'actual own x86 synchronization source');need(e['native_exit']==0 and e['native_cleanup']==dict(all_owned_resources_released=True,events=0,criticals=0,forced_cleanup=False,window_created=False,thread_created=False),'normal source event/manager release without fallback or counterfeit worker');need(e['declaration']==[dict(pointer=work.MANAGER,bytes=4096,fill=165),dict(pointer=work.STACK-0xf000,bytes=65536,fill=0)],'only fresh declared manager and separate root stack');need(e['retained_stack_pointer']==work.previous.STACK-0x1000 and len(bytes.fromhex(e['retained_stack_hex']))==8192,'entire source ordinary-loop stack retained')
 expected=[('original_manager_constructor',0x421540,work.MANAGER,[]),('original_manager_empty_lists',0x421660,work.MANAGER,[]),('original_retained_task_registration',0x4216c0,work.MANAGER,[work.TACT,0,0]),('original_first_scheduler_scan',0x4217c0,work.MANAGER,[])];need(len(e['steps'])==4,'complete source registration to first scan')
 for s,(label,va,recv,args) in zip(e['steps'],expected):need(s['label']==label and s['root']==dict(va=va,receiver=recv,args=args,sp=work.STACK,return_va=work.RETURN) and s['requested_boundary']==work.RETURN,'only declared original registration/scan roots')
 need(all(s['pending'] is s['fault'] is None for s in e['steps'][:3]) and e['frontier']==(e['steps'][-1]['pending'] or e['steps'][-1]['fault']),'natural original registration then exact first dispatch dependency');need(e['frontier'] is not None and e['frontier'].get('kind')=='original_scheduler_thread_platform_dependency' and e['frontier'].get('import_slot')==0x59221c and e['frontier'].get('name')=='CreateThread' and e['frontier']['return_va']==0x56e0c4,'actual next original CRT CreateThread boundary; not a synthetic successful wait');need(e['entry_memory']==c['fog_texture']['business_memory'] and canonical(e['entry_CPU'])==canonical(c['fog_texture']['business_architectural_cpu']),'continuous current source wait before any new declared roots')

@lru_cache(maxsize=1)
def proof_helper():
 p=ROOT/('.venv-audit/scheduler-independent-'+str(os.getpid())+'.exe');return work.platform.build(p)

def fresh_platform(e):
 helper,build=proof_helper();live=work.platform.Live(helper);handles={};observations=[]
 try:
  for row in e['native_trace']:
   q=dict(row['request']);q.pop('id');op=q.pop('op')
   if op=='close':continue
   if 'handle' in q:need(q['handle'] in handles,'fresh independent event ownership');q['handle']=handles[q['handle']]
   result=live.request(op,**q)
   if op=='create_event':handles[row['reply']['result']['handle']]=result['handle'];obs=live.request('wait',handle=result['handle'],milliseconds=0);need(obs==dict(value=258),'fresh automatic event starts actually nonsignaled');observations.append(obs)
   elif op not in ('initialize','enter','leave'):need(result==row['reply']['result'],'fresh native logical synchronization result')
  cleanup=live.close();need(cleanup==e['native_cleanup'] and live.exit_code==0,'fresh independent normal synchronization teardown')
 finally:
  if not live.closed:live._terminate()
 return dict(build=build,hello=live.hello,trace=live.trace,actual_initial_event_observations=observations,cleanup=cleanup,exit_code=live.exit_code)

def verify_scheduler(r):
 c=r.case;e=c['scheduler'];need(base.memory_rows(r.u)==e['entry_memory'] and canonical(base.architectural_cpu(r.u))==canonical(e['entry_CPU']) and r.cpu()['EIP']==0x422360 and r.read(e['retained_stack_pointer'],8192).hex()==e['retained_stack_hex'],'whole independent natural wait context and original stack before registration');context=r.u.context_save();r.scheduler_events={};r.scheduler_closed_events=set();r.scheduler_lock_live=False;r.scheduler_depth=r.scheduler_wire=0;before=set(r.blocks)
 for d in e['declaration']:
  p=d['pointer'];n=d['bytes'];need(all(not(a<p+n and p<=b) for a,b,_ in r.u.mem_regions()),'new independent declared manager/root stack');r.u.mem_map(p,n);r.u.mem_write(p,bytes([d['fill']])*n)
 need(work.state(r)==e['declared_state'],'whole declared storage and unchanged source game state');count=writes=0
 for s in e['steps']:count+=r.loop_step(s);writes+=s['result']['writes'];need(work.state(r)==s['scheduler_state'],'all source manager/task/CRT bytes at every original root')
 need(work.state(r)==e['business_final'] and base.memory_rows(r.u)==e['business_memory'] and canonical(base.architectural_cpu(r.u))==canonical(e['business_CPU']),'entire original first dispatch terminal state');need(sorted(set(r.blocks)-before)==e['new_allocations'] and r.scheduler_events=={int(k):v for k,v in e['events'].items()},'exact source new CRT block/event ownership');need(word(r.read(work.TACT+8))==work.MANAGER and word(r.read(work.MANAGER))==work.TACT and word(r.read(work.TACT+0x1c)) in r.scheduler_events,'original registration/list/node event writes');sp=r.cpu()['ESP'];args=[word(r.read(sp+4+i)) for i in range(0,24,4)];need(len(e['new_allocations'])==1 and args==[0,0,0x56e110,e['new_allocations'][0]+32,4,work.TACT+36] and word(r.read(sp))==0x56e0c4,'entire original CRT suspended CreateThread ABI and actual thread data pointer');ptd=r.read(args[3],116);expected=bytearray(116)
 for off,value in ((4,0xffffffff),(20,1),(72,0x421f50),(76,work.TACT),(80,0x761d68)):struct.pack_into('<I',expected,off,value)
 need(ptd==bytes(expected),'all original calloc/initialization thread bytes and exact source callback chain');thread=dict(CreateThread_arguments=args,CRT_wrapper=0x56e110,worker=0x421f50,scene_callback=0x451670,data_pointer=args[3],data_hex=ptd.hex(),thread_created=False);cleanup=iter(e['cleanup'])
 for p in e['new_allocations']:
  s=next(cleanup);need(s['label']=='supplemental_original_thread_data_free' and s['root']==dict(va=0x56f3b0,receiver=0,args=[p+32,2],sp=work.STACK,return_va=work.RETURN),'explicit source thread-block error cleanup');r.loop_step(s)
 s=next(cleanup);need(s['label']=='supplemental_original_task_unlink' and s['root']==dict(va=0x421d50,receiver=work.MANAGER,args=[work.TACT],sp=work.STACK,return_va=work.RETURN),'original supplemental task unregister');r.loop_step(s);close=e['supplemental_node_event_close']
 if close:
  h=word(r.read(work.TACT+0x1c));need(close['guest_handle']==h and h in r.scheduler_events and h not in r.scheduler_closed_events and close['native_handle']==r.scheduler_events[h] and close['wire_index']==r.scheduler_wire,'supplemental close only of observed own source node event');wire=e['native_trace'][r.scheduler_wire];need(wire['request']==dict(id=r.scheduler_wire+1,op='close_event',handle=r.scheduler_events[h]) and wire['reply']==dict(id=r.scheduler_wire+1,ok=True,result=dict(value=1)) and close['result']==dict(value=1),'actual source supplemental node close receipt');r.scheduler_wire+=1;r.scheduler_closed_events.add(h)
 s=next(cleanup);need(s['label']=='supplemental_original_manager_destructor' and s['root']==dict(va=0x4215f0,receiver=work.MANAGER,args=[],sp=work.STACK,return_va=work.RETURN),'original supplemental manager teardown');r.loop_step(s);need(next(cleanup,None)is None and work.state(r)==e['after_cleanup'] and set(r.blocks)==before and set(r.scheduler_events)==r.scheduler_closed_events and not r.scheduler_lock_live and r.scheduler_depth==0,'all and only source new current resources released');need(r.read(e['retained_stack_pointer'],8192).hex()==e['retained_stack_hex'],'full original wait stack untouched by independent root stack');r.u.context_restore(context);need(canonical(base.architectural_cpu(r.u))==canonical(e['restored_CPU'])==canonical(e['entry_CPU']) and base.memory_rows(r.u)==e['restored_memory'],'complete retained ordinary-loop context restored without replaying wait');wire=e['native_trace'][r.scheduler_wire];need(wire['request']==dict(id=r.scheduler_wire+1,op='close') and wire['reply']==dict(id=r.scheduler_wire+1,ok=True,result=e['native_cleanup']) and r.scheduler_wire+1==len(e['native_trace']),'entire source native synchronization trace consumed');fresh=fresh_platform(e);r.scheduler_proof=dict(original_instructions=count,original_writes=writes,declared_original_roots=4,original_registration_verified=True,first_scan_started=True,first_scan_returned=False,thread_creation=thread,source_node_event_created=True,full_CPU_memory_queue_and_stack=True,ordinary_loop_context_preserved=True,exact_dependency=e['frontier'],new_CRT_allocations=len(e['new_allocations']),current_native_event_count=len(r.scheduler_events),independent_fresh_platform=fresh,normal_source_cleanup=True,cooperative_yield_executed=False,original_CRT_worker_created=False,original_MAIN_scheduler_connected=False,R3_complete=False,R6_complete=False)

def verify_case(c,boundary_observer=None):
 protocol(c);instances=[]
 def observe(r):
  instances.append(r)
  if boundary_observer is not None:boundary_observer(r)
 call=types.FunctionType(previous.verify_case.__code__,dict(previous.verify_case.__globals__,prepare=prepare),'whole_parent_fog_into_original_scheduler');result=call(c,observe);need(len(instances)==1 and hasattr(instances[0],'scheduler_proof'),'one independently completed scheduler scope');return dict(result,scheduler=instances[0].scheduler_proof)

def verify_group(args):
 import contextlib
 rows,prefix=args;proofs=[]
 with open(ROOT/(prefix+'-'+rows[0]['name']+'.log'),'x',encoding='utf8',buffering=1) as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
  previous.isolated_worker_builds()
  for row in rows:
   b=base.pinned(row['path'],row['sha256']);need(len(b)==row['bytes'],'entire compressed source length');c=json.loads(gzip.decompress(b));need((c['name'],c['scene_capture'])==(row['name'],row['scene_capture']),'same source case identity');proof=verify_case(c);path=prefix+'-'+row['name']+'-'+str(row['scene_capture'])+'.json';out=ROOT/path;need(not out.exists(),'fresh immutable whole-case independent proof');out.write_text(json.dumps(dict(schema_version=1,source_case=row,verification_source_sha256=sha((ROOT/'tools/school_retained_scheduler_verification.py').read_bytes()),proof=proof),indent=2)+chr(10),encoding='utf8',newline=chr(10));raw=out.read_bytes();proofs.append(dict(proof,source_case=row,independent_case_proof=dict(path=path,sha256=sha(raw),bytes=len(raw))));print('complete independent original registration/dispatch',row['name'],row['scene_capture'],flush=True)
 return proofs

def verify_matrix(matrix,prefix,existing_initial_proof=None,jobs=3):
 need(matrix['contract']==work.contracts() and matrix['schema_version']==1,'all source scheduler matrix identities');rows=matrix['case_reports'];need([(r['name'],r['scene_capture']) for r in rows]==[(n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],'all six original registered task cases');need(1<=jobs<=3,'bounded independent workers');proofs=[];todo=rows
 for key in ('new_OS_input','actual_D3D_draw_or_Present','original_outer_scheduler','historical_heap_restored','R3_complete','R6_complete'):need(matrix[key] is False,'honest scheduler scope '+key)
 if existing_initial_proof:
  b=(ROOT/existing_initial_proof).read_bytes();p=json.loads(b);need(p['source_case']==rows[0] and p['verification_source_sha256']==sha((ROOT/'tools/school_retained_scheduler_verification.py').read_bytes()) and p['proof']['scheduler']['normal_source_cleanup'] and p['proof']['scheduler']['full_CPU_memory_queue_and_stack'],'only exact complete source/code/ownership initial proof reused');proofs.append(dict(p['proof'],source_case=rows[0],independent_case_proof=dict(path=existing_initial_proof,sha256=sha(b),bytes=len(b))));todo=rows[1:]
 groups=[([r for r in todo if r['name']==n],prefix) for n in ('initial','student9_waiting','fifth_class')];groups=[g for g in groups if g[0]]
 if jobs==1:
  for group in groups:proofs.extend(verify_group(group))
 else:
  from concurrent.futures import ProcessPoolExecutor
  with ProcessPoolExecutor(max_workers=jobs) as pool:
   for group in pool.map(verify_group,groups):proofs.extend(group)
 need(len(proofs)==6,'all complete independent cases');return dict(schema_version=1,cases=proofs,six_original_scheduler_dispatches_verified=True,whole_parent_replayed_each=True,reused_complete_initial_independent_proof=existing_initial_proof,cooperative_yield_executed=False,original_CRT_worker_created=False,original_MAIN_scheduler_connected=False,new_OS_input=False,interactive_desktop_required=False,R3_complete=False,R6_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('matrix');p.add_argument('--out',required=True);p.add_argument('--existing-initial-proof');p.add_argument('--jobs',type=int,default=3);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable whole-case proof')
 raw=(ROOT/a.matrix).read_bytes();r=verify_matrix(json.loads(raw),'analysis/'+out.stem+'-cases',a.existing_initial_proof,a.jobs);r['source_matrix_sha256']=sha(raw);r['verification_source_sha256']=sha((ROOT/'tools/school_retained_scheduler_verification.py').read_bytes());out.write_text(json.dumps(r,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('six whole original registration/dispatch cases verified',flush=True)
