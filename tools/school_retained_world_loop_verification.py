"""Independent original opening and natural ordinary-loop/world continuation."""
import copy,gzip,json,struct,types
from functools import lru_cache
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_INVALID,UcError
from tools import school_retained_world_loop as work
from tools import school_retained_opening_verification as previous

ROOT=work.ROOT;base=work.base;need=work.need;sha=work.sha;word=work.word;canonical=work.canonical
CALLS=(0x4539b0,0x454cf0,0x453f10,0x46b470,0x432100,0x457aa0,0x422360,0x4ce8f0,0x454c80)

# Private validation graph: same frozen checks, actual extension helper source identity.
# No source report is rewritten and no frozen module globals are mutated.
_protocol_modules={};_protocol_functions={}
def protocol_function(fn):
 if id(fn) in _protocol_functions:return _protocol_functions[id(fn)]
 ns=dict(fn.__globals__)
 for k in ('previous','fourth_proxy'):
  m=ns.get(k)
  if hasattr(m,'protocol') and hasattr(m,'verify_case'):ns[k]=protocol_module(m)
 if fn.__name__!='protocol' and isinstance(ns.get('protocol'),types.FunctionType):ns['protocol']=protocol_function(ns['protocol'])
 if isinstance(ns.get('parent_protocol'),types.FunctionType):ns['parent_protocol']=protocol_function(ns['parent_protocol'])
 if fn.__module__=='tools.school_retained_character_task_verification' and fn.__name__=='protocol':
  result=work.previous.adapt(fn,[("sha(work.parent.old.init.platform.SOURCE.read_bytes())","sha(world_platform.SOURCE.read_bytes())")],world_platform=work.platform)
  ns=dict(result.__globals__,**{k:ns[k] for k in ('previous',) if k in ns});result=types.FunctionType(result.__code__,ns,fn.__name__,fn.__defaults__,fn.__closure__)
 else:result=types.FunctionType(fn.__code__,ns,fn.__name__,fn.__defaults__,fn.__closure__)
 _protocol_functions[id(fn)]=result;return result

def protocol_module(m):
 if id(m) in _protocol_modules:return _protocol_modules[id(m)]
 proxy=types.SimpleNamespace(**vars(m));_protocol_modules[id(m)]=proxy
 for k in ('previous','fourth_proxy'):
  ancestor=getattr(m,k,None)
  if hasattr(ancestor,'protocol') and hasattr(ancestor,'verify_case'):setattr(proxy,k,protocol_module(ancestor))
 for k in ('protocol','parent_protocol','verify_case','prepare'):
  fn=getattr(m,k,None)
  if isinstance(fn,types.FunctionType):setattr(proxy,k,protocol_function(fn))
 return proxy

parent=protocol_module(previous)

class Replay(previous.Replay):
 loop_code=work.previous.adapt(previous.Replay.source_step,[("if at==a['boundary']:","if at==a['boundary'] and not s['fault']:"),("'actual_opening_CRT','actual_role9_CRT','recorded_task_platform'","'actual_opening_CRT','actual_role9_CRT','recorded_task_platform','actual_world_static_lock'"),("count=2000000,timeout=120000000","count=8000000,timeout=240000000"),("finally:self.u.hook_del(ch);self.u.hook_del(wr)","except UcError as exc:need(s['fault'] is not None and str(exc)==s['unicorn_error'],'only the exact observed original memory fault')\n finally:self.u.hook_del(ch);self.u.hook_del(wr)")],UcError=UcError)
 def api(self,a):
  if a.get('kind')!='actual_world_static_lock':return super().api(a)
  sp=self.cpu()['ESP'];slot=a['import_slot'];need(slot in work.previous.dialogue.IMPORTS,'original static lock IAT');name,pop=work.previous.dialogue.IMPORTS[slot];ret=word(self.read(sp));arg=word(self.read(sp+4));need(name in ('EnterCriticalSection','LeaveCriticalSection') and pop==4 and arg==0x80a4c8 and arg in self.criticals and ret=={'EnterCriticalSection':0x5770d3,'LeaveCriticalSection':0x5770f4}[name],'original generic CRT lock13 caller and initialized current ownership');need(a['name']==name and a['sp']==sp and a['return_va']==ret and a['target']==a['va']==word(self.read(slot)) and a['args']==[arg] and a['pop']==4 and a['value']==0 and a['wire_start']==self.wire and a['lock_index']==13 and a['void_return_normalized']is True,'entire original lock13 ABI and native cursor');op='enter_static' if name[0]=='E' else 'leave_static';self.world_lock_depth=getattr(self,'world_lock_depth',0)+(1 if name[0]=='E' else -1);need(0<=self.world_lock_depth<=4,'bounded balanced lock13 depth');r=self.consume(op,guest=arg,pointer=self.criticals[arg]);raw=bytes.fromhex(r['critical_hex']);need(len(raw)==24 and a['depth']==r['depth']==self.world_lock_depth and a['wire_end']==self.wire and a['new_mappings']==[] and a['memory_outputs']==[dict(pointer=arg,hex=raw.hex())],'entire actual source static lock operation and bytes');self.u.mem_write(arg,raw);self.api_return(0,4,ret,sp)
 def loop_step(self,s):
  calls=[];fault=None
  def observe(u,at,n,_):
   if at==s['result']['boundary'] and not s['fault']:return
   if at in CALLS:
    sp=self.cpu()['ESP'];calls.append(dict(va=at,receiver=self.cpu()['ECX'],sp=sp,return_va=word(self.read(sp)),frames=work.chain(self)))
  def invalid(u,access,at,n,value,_):
   nonlocal fault
   fault=dict(access=access,address=at,bytes=n,value=value,cpu=self.cpu(),frames=work.chain(self),instruction_completed=False);return False
  ch=self.u.hook_add(UC_HOOK_CODE,observe);bad=self.u.hook_add(UC_HOOK_MEM_INVALID,invalid)
  try:n=self.loop_code(s)
  finally:self.u.hook_del(ch);self.u.hook_del(bad)
  need(calls==s['calls'] and fault==s['fault'] and work.state(self)==s['loop_state'],'all natural loop calls/frames, real faults and entire task/scene/world state')
  if s['pending']:
   p=s['pending'];at=self.cpu()['EIP'];sp=self.cpu()['ESP'];expected=dict(kind=p['kind'],va=at,cpu=self.cpu(),receiver=self.cpu()['ECX'],sp=sp,stack_hex=self.read(sp,64).hex(),return_va=word(self.read(sp)),frames=work.chain(self),first_instruction_executed=False)
   if p['kind']=='unowned_CRT_free':
    pointer=word(self.read(sp+4));need(at==0x428ad0 and pointer and pointer not in {a+32 for a in self.blocks},'actual original free argument has no current owner');expected['pointer']=pointer
   elif p['kind']=='new_GDI_dependency':
    slot=p['import_slot'];need(slot in work.previous.dialogue.GDI and word(self.read(slot))==at and not(slot==work.previous.task.LENGTH_SLOT and word(self.read(sp))==0x425a7e),'actual new unsupported original GDI ABI');expected['import_slot']=slot
   elif p['kind']=='new_texture_dependency':need(at==self.device_method,'actual new source CreateTexture entry')
   else:need(p['kind']=='uncovered_platform_or_interface' and not base.BASE<=at<0x592000,'real uncovered external interface')
   need(p==expected and at!=s['requested_boundary'],'all exact source dependency identity; no substitute or earlier artificial boundary')
  else:need(fault is not None or self.cpu()['EIP']==s['requested_boundary'],'only natural source target or independently reproduced fault')
  return n

prepare=types.FunctionType(previous.prepare.__code__,dict(parent.prepare.__globals__,Replay=Replay),'independently_replay_parent_into_world_capable_checker')

def protocol(c):
 parent.protocol(c);e=c['world_loop'];need(e['contract']==work.contracts(),'all opening and original loop source identities');need(e['new_declared_loop_roots']==1 and e['new_VM_or_world_roots']==e['host_game_control_writes']==0,'one exact loop root and no VM/world/control substitutes');need(e['new_OS_input']is e['original_outer_scheduler']is e['cooperative_yield_executed']is False,'honest original-loop root and pre-yield authority');need(4<=len(e['steps'])<=6,'bounded ordinary frame/source dependency progression');need([s['label'] for s in e['steps']]==['loop_request_or_queue_0x425de0','loop_request_or_queue_0x40db90','loop_request_or_queue_0x40dc80','original_loop_to_world','continuous_original_world_return','continuous_original_loop_to_yield'][:len(e['steps'])],'exact original loop/world/yield segment order')
 for s,va,recv in zip(e['steps'][:4],(0x425de0,0x40db90,0x40dc80,0x4539b0),(work.previous.task.INPUT,work.previous.task.MANAGER,work.previous.task.MANAGER,work.TACT)):
  need(s['root']==dict(va=va,receiver=recv,args=[],sp=work.STACK,return_va=work.RETURN),'only declared original request/resets/ordinary-loop roots')
 for s in e['steps'][4:]:need(s['root']is None,'world and tail resume along their original stack')
 need([s['requested_boundary'] for s in e['steps']]==[work.RETURN]*3+[0x46b470,0x453a11,0x422360][:len(e['steps'])-3],'natural declared world entry/return/yield observation points');need(e['frontier']==(e['steps'][-1]['pending'] or e['steps'][-1]['fault']),'exact terminal dependency or natural yield');need(all('full_memory' in s and 'architectural_cpu' in s and 'queue' in s for s in e['steps']),'complete provenance in every new interval')

def verify_loop(r):
 c=r.case;e=c['world_loop'];need(work.state(r)==e['before'] and base.memory_rows(r.u)==e['entry_memory']==c['opening']['final_memory'] and canonical(base.architectural_cpu(r.u))==canonical(e['entry_architectural_cpu'])==canonical(c['opening']['final_architectural_cpu']),'continuous independently replayed opening terminal before all supplemental cleanup');o=e['owners'];need(all(o[k]is False for k in ('opening_closed','role9_closed','fourth_closed')) and o['opening_textures']==c['opening']['textures'] and o['role9_textures']==c['role9']['textures'],'all current source texture owners remain live at loop entry');need(canonical(o['allocations'])==canonical(r.blocks),'all and only original current vector ownership at loop entry');count=writes=0
 for i,s in enumerate(e['steps']):
  if i==4:need(r.cpu()['EIP']==0x46b470 and r.cpu()['ECX']==work.CONTROL and word(r.read(r.cpu()['ESP']))==0x453a11 and r.cpu()['EBP']==work.STACK-4,'natural original world call, receiver and full outer loop frame')
  if i==5:need(r.cpu()['EIP']==0x453a11 and r.cpu()['ESP']==work.STACK-92 and r.cpu()['EBP']==work.STACK-4,'natural complete original world return')
  count+=r.loop_step(s);writes+=s['result']['writes']
 need(work.state(r)==e['final'] and base.memory_rows(r.u)==e['final_memory']==e['steps'][-1]['full_memory'] and canonical(base.architectural_cpu(r.u))==canonical(e['final_architectural_cpu']),'fresh entire source loop frontier state and CPU');world_returned=len(e['steps'])>=5 and e['steps'][4]['result']['boundary']==0x453a11 and not e['steps'][4]['fault'];reached_yield=len(e['steps'])==6 and r.cpu()['EIP']==0x422360 and e['frontier']is None
 if reached_yield:need(r.cpu()['ECX']==work.TACT and word(r.read(r.cpu()['ESP']))==0x453cb5 and word(r.read(r.cpu()['ESP']+4))==0,'natural first cooperative wait ABI, original body not executed')
 visits={a['va']:a['count'] for s in e['steps'] for a in s['result']['instruction_counts']};r.loop_proof=dict(name=c['name'],scene_capture=c['scene_capture'],actual_lock13_operations=sum(a.get('kind')=='actual_world_static_lock' for s in e['steps'] for a in s['result']['api_calls']),balanced_lock13=getattr(r,'world_lock_depth',0)==0,new_original_instructions=count,new_original_writes=writes,source_intervals=len(e['steps']),one_declared_loop_root=True,new_VM_or_world_roots=0,all_calls_CPU_memory_and_queue_verified=True,natural_world_return=world_returned,world_enabled_at_entry=e['steps'][3]['loop_state']['world_enabled'],world_function_entries=visits.get(0x46b470,0),world_unit_entries=visits.get(0x46b760,0),natural_pre_yield_boundary=reached_yield,cooperative_yield_executed=False,exact_dependency=copy.deepcopy(e['frontier']),final_task_phase=e['final']['task_phase'],final_scene_mode=e['final']['scene_mode'],final_PC=e['final']['opening']['PC'],final_mappings=len(e['final_memory']),original_outer_scheduler=False,actual_D3D_draw_or_Present=False,interactive_desktop_required=False,R3_complete=False,R6_complete=False)

def verify_case(c,boundary_observer=None):
 if not globals().get('_native_builds_ready'):isolated_worker_builds()
 protocol(c);proof=[]
 def observe(r):
  if boundary_observer is not None:boundary_observer(r)
  verify_loop(r);proof.append(r.loop_proof)
  cleanup=c['world_loop']['supplemental_lock_cleanup'];held=getattr(r,'world_lock_depth',0)
  need(len(cleanup)==held and held in (0,1),'all and only the fault-held lock needs explicit original cleanup')
  for s in cleanup:
   need(c['world_loop']['steps'][-1]['fault'] is not None and s['label']=='supplemental_original_lock13_release_after_fault' and s['root']==dict(va=0x5770e0,receiver=0,args=[13],sp=work.STACK,return_va=work.RETURN) and s['requested_boundary']==work.RETURN and s['fault'] is s['pending'] is None,'separate declared original lock13 cleanup after actual fault; never business progress');r.loop_step(s)
  need(getattr(r,'world_lock_depth',0)==0,'balanced actual lock13 before original resource teardown');proof[-1]['supplemental_original_lock_release_instructions']=[sum(x['count'] for x in s['result']['instruction_counts']) for s in cleanup];proof[-1]['normal_source_lock13_cleanup']=True
 call=work.previous.adapt(parent.verify_case,[("glyph_cleanup=[]","verify_original_loop(r);glyph_cleanup=[]")],prepare=prepare,verify_original_loop=observe);opening_proof=call(c);need(len(proof)==1,'one complete independently verified ordinary-loop scope');return dict(name=c['name'],scene_capture=c['scene_capture'],opening=opening_proof,world_loop=proof[0])

def verify_case_report(row):
 path=ROOT/row['path'];raw=base.pinned(row['path'],row['sha256']);need(len(raw)==row['bytes'],'whole compressed case byte length')
 with gzip.open(path,'rt',encoding='utf8') as f:c=json.load(f)
 need((c['name'],c['scene_capture'])==(row['name'],row['scene_capture']),'case source identity');p=verify_case(c);p['source_case']=row;print('independent ordinary loop/world verified',row['name'],row['scene_capture'],flush=True);return p

def isolated_worker_builds():
 # Only native helper build destinations differ. Original instruction/API replay
 # and every accepted historical validator file remain unchanged.
 import os
 def builder(label):return lru_cache(maxsize=1)(lambda:work.previous.previous.previous.build_gpu(ROOT/('.venv-audit/world-loop-proof-'+str(os.getpid())+'-'+label+'.exe')))
 previous.previous.proof_helper=builder('role9');previous.previous.previous.proof_helper=builder('fourth');previous.proof_helper=builder('opening')
 globals()['_native_builds_ready']=True

def verify_matrix(matrix,case_observer=None,jobs=1):
 need(matrix['schema_version']==1 and matrix['contract']==work.contracts() and matrix['new_VM_roots']==matrix['game_function_substitutions']==matrix['IAT_rebindings']==0,'all complete opening matrix source pins and no substitutes')
 for k in ('new_OS_input','actual_D3D_draw_or_Present','original_outer_scheduler','historical_heap_restored','R3_complete','R6_complete'):need(matrix[k]is False,'honest matrix scope '+k)
 need(matrix['new_GPU']is matrix['new_hidden_windows']is True,'actual independently owned hidden native resource domains');rows=matrix['case_reports'];need([(c['name'],c['scene_capture']) for c in rows]==[(n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],'all six immutable source opening case bindings');proofs=[]
 need(isinstance(jobs,int) and 1<=jobs<=3,'bounded independent verification processes')
 if jobs==1:
  for row in rows:
   p=verify_case_report(row);proofs.append(p)
   if case_observer is not None:case_observer(p)
 else:
  from concurrent.futures import ProcessPoolExecutor
  with ProcessPoolExecutor(max_workers=jobs,initializer=isolated_worker_builds) as executor:
   for p in executor.map(verify_case_report,rows,chunksize=2):
    proofs.append(p)
    if case_observer is not None:case_observer(p)
 return dict(schema_version=1,cases=proofs,six_original_loop_continuations_verified=True,independent_processes=jobs,native_build_destinations_isolated=jobs>1,interactive_desktop_required=False,new_OS_input=False,actual_D3D_draw_or_Present=False,R3_complete=False,R6_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('matrix');p.add_argument('--out',required=True);p.add_argument('--jobs',type=int,default=1);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable proof')
 raw=(ROOT/a.matrix).read_bytes();result=verify_matrix(json.loads(raw),jobs=a.jobs);result['source_matrix_sha256']=sha(raw);result['verification_source_sha256']=sha((ROOT/'tools/school_retained_world_loop_verification.py').read_bytes());out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n');print('six whole original opening proofs saved',flush=True)
