"""Original retained opening to ordinary-loop/world/yield or real dependency frontier."""
import copy,gzip,hashlib,json,struct,types
from collections import Counter
from functools import lru_cache
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_INVALID,UcError
from tools import school_retained_opening as previous
from tools import school_retained_world_loop_platform as platform

ROOT=previous.ROOT;base=previous.base;need=previous.need;sha=previous.sha;word=previous.word;canonical=previous.canonical
STACK=previous.STACK;RETURN=previous.RETURN;VM=previous.VM;TACT=previous.task.TACT;CONTROL=TACT+0x190
ACCEPTANCE='analysis/school-retained-opening-acceptance-v1-20261023.json'
ACCEPTANCE_SHA='70549e1455aebf1c7415576d98ad5cc03d4dee287b5f267be4d114f680df4035'

@lru_cache(maxsize=1)
def contracts():
 need(sha(previous.previous.crt.platform.SOURCE.read_bytes())==platform.BASE_SOURCE_SHA,'frozen original platform source');a=json.loads(base.pinned(ACCEPTANCE,ACCEPTANCE_SHA));need((a['final_PC'],a['final_wait'],a['final_opcode'],a['tasks_complete'])==(492,0,19,3),'accepted complete original opening terminal');return dict(platform_source_sha256=sha(platform.SOURCE.read_bytes()),platform_base_sha256=platform.BASE_SOURCE_SHA,parent_acceptance=ACCEPTANCE,parent_acceptance_sha256=ACCEPTANCE_SHA,previous=previous.contracts(),loop_root=0x4539b0,loop_receiver=TACT,task_call=0x4539ec,control_call=0x4539fb,world_call=0x453a0c,world_entry=0x46b470,world_return=0x453a11,yield_call=0x453cb0,yield_entry=0x422360,scope='one declared original ordinary-loop root; continuous original callees, natural world/yield or exact real dependency; no scheduler return substitute')

def state(g):
 return dict(opening=previous.state(g),scene_header_hex=g.read(TACT,0x190).hex(),world_gate_hex=g.read(CONTROL+0x108b20,80).hex(),task_phase=g.read(TACT+0x44,1)[0],task_flags_hex=g.read(TACT+0x44,32).hex(),scene_mode=word(g.read(TACT+0x38)),world_enabled=struct.unpack('<h',g.read(CONTROL+0x108b32,2))[0],global_scene=word(g.read(0x7a4174)),renderer=word(g.read(0x7a49fc)),input=word(g.read(0x7a4a00)))

def chain(g):
 rows=[];bp=g.cpu()['EBP'];seen=set()
 for i in range(16):
  if bp in seen or not any(a<=bp and bp+7<=b for a,b,_ in g.u.mem_regions()):break
  seen.add(bp);raw=g.read(bp,8);prior,ret=struct.unpack('<2I',raw);rows.append(dict(bp=bp,previous_bp=prior,return_va=ret));bp=prior
 return rows

class Guest(previous.Guest):
 continue_opening=previous.adapt(previous.Guest.continue_opening,[("cleanup=[]\n  for r in self.opening_textures:","self.loop_record=self.continue_loop()\n  cleanup=[]\n  for r in self.opening_textures:")])
 def new_api(self,slot):
  sp=self.cpu()['ESP'];arg=word(self.read(sp+4));name,pop=previous.dialogue.IMPORTS[slot]
  if name not in ('EnterCriticalSection','LeaveCriticalSection') or arg!=0x80a4c8:return super().new_api(slot)
  ret=word(self.read(sp));need(pop==4 and ret=={'EnterCriticalSection':0x5770d3,'LeaveCriticalSection':0x5770f4}[name] and arg in self.criticals,'original lock13 ABI and current initialized owner');start=len(self.live.trace);op='enter_static' if name[0]=='E' else 'leave_static';r=self.live.request(op,guest=arg,pointer=self.criticals[arg]);raw=bytes.fromhex(r['critical_hex']);need(len(raw)==24,'entire current native lock13 bytes');self.u.mem_write(arg,raw);self.memory_evidence.mark(arg,24);self.api_calls.append(dict(kind='actual_world_static_lock',name=name,import_slot=slot,target=word(self.read(slot)),sp=sp,return_va=ret,args=[arg],pop=pop,value=0,new_mappings=[],memory_outputs=[dict(pointer=arg,hex=raw.hex())],wire_start=start,wire_end=len(self.live.trace),void_return_normalized=True,lock_index=13,depth=r['depth']))
  self.u.reg_write(base.REGISTERS['EAX'],0);self.u.reg_write(base.REGISTERS['ESP'],sp+8);self.u.reg_write(base.REGISTERS['EIP'],ret)
 def loop_step(self,label,stop,root=None):
  if root:
   self.u.mem_write(root['sp'],struct.pack('<'+'I'*(len(root['args'])+1),root['return_va'],*root['args']))
   for k,v in dict(EIP=root['va'],ESP=root['sp'],ECX=root['receiver'],EFLAGS=0x202).items():self.u.reg_write(base.REGISTERS[k],v)
  before=self.cpu();ih=hashlib.sha256();wh=hashlib.sha256();counts=Counter();writes=0;calls=[];display=[];conversions=[];self.api_calls=[];pending=None;fault=None;error=None;maps=[];targets={word(self.read(s)):s for s in previous.dialogue.IMPORTS};iat={s:self.read(s) for s in previous.dialogue.IMPORTS}
  for at in targets:
   if not any(a<=at<=b for a,b,_ in self.u.mem_regions()):p=at&~4095;self.u.mem_map(p,4096);maps.append(dict(pointer=p,bytes=4096))
  self.memory_evidence.refresh()
  if root:self.memory_evidence.mark(root['sp'],4*(len(root['args'])+1))
  def frontier(kind,at,**extra):
   nonlocal pending
   sp=self.cpu()['ESP'];pending=dict(kind=kind,va=at,cpu=self.cpu(),receiver=self.cpu()['ECX'],sp=sp,stack_hex=self.read(sp,64).hex(),return_va=word(self.read(sp)),frames=chain(self),first_instruction_executed=False,**extra);self.u.emu_stop()
  def code(u,at,n,_):
   if at==stop:u.emu_stop();return
   if at==0x428ad0:
    p=word(self.read(self.cpu()['ESP']+4))
    if p and p not in {a+32 for a in self.allocations}:frontier('unowned_CRT_free',at,pointer=p);return
   if at in targets:
    slot=targets[at];ret=word(self.read(self.cpu()['ESP']))
    if slot in previous.dialogue.GDI and not(slot==previous.task.LENGTH_SLOT and ret==0x425a7e):frontier('new_GDI_dependency',at,import_slot=slot);return
    self.new_api(slot);return
   if at==self.device_method:frontier('new_texture_dependency',at);return
   if at in self.third_methods:self.new_gpu(at);return
   if not base.BASE<=at<0x592000:frontier('uncovered_platform_or_interface',at);return
   need(self.read(at,n)==self.image[at-base.BASE:at-base.BASE+n],'every immutable original loop instruction');counts[at]+=1;ih.update(struct.pack('<I',at)+self.read(at,n))
   if at in (0x4539b0,0x454cf0,0x453f10,0x46b470,0x432100,0x457aa0,0x422360,0x4ce8f0,0x454c80):
    sp=self.cpu()['ESP'];calls.append(dict(va=at,receiver=self.cpu()['ECX'],sp=sp,return_va=word(self.read(sp)),frames=chain(self)))
   if at in previous.dialogue.DISPLAY:display.append(dict(va=at,receiver=self.cpu()['ECX'],return_va=word(self.read(self.cpu()['ESP']))))
   if at==0x405869:
    sp=self.cpu()['ESP'];args=[word(self.read(sp+j)) for j in range(0,24,4)];conversions.append(dict(va=at,args=args,lock_hex=self.read(args[1],8).hex(),rect=list(struct.unpack('<4I',self.read(args[4],16))),point=list(struct.unpack('<2I',self.read(args[5],8)))))
  def write(u,access,at,n,value,_):
   nonlocal writes
   need(not base.BASE<=at<0x592000,'no original code writes');writes+=1;wh.update(struct.pack('<IIQ',at,n,value&0xffffffffffffffff))
   if any(a<=at and at+n<=b for a,b in self.memory_evidence.regions):self.memory_evidence.mark(at,n)
  def invalid(u,access,at,n,value,_):
   nonlocal fault
   fault=dict(access=access,address=at,bytes=n,value=value,cpu=self.cpu(),frames=chain(self),instruction_completed=False);return False
  ch=self.u.hook_add(UC_HOOK_CODE,code);wr=self.u.hook_add(UC_HOOK_MEM_WRITE,write);bad=self.u.hook_add(UC_HOOK_MEM_INVALID,invalid)
  try:self.u.ctl_remove_cache(before['EIP'],before['EIP']+1);self.u.emu_start(before['EIP'],0,count=8000000,timeout=240000000)
  except UcError as exc:
   need(fault is not None,'only an observed real unmapped access may stop original loop');error=str(exc)
  finally:self.u.hook_del(ch);self.u.hook_del(wr);self.u.hook_del(bad)
  need(iat=={s:self.read(s) for s in previous.dialogue.IMPORTS},'unchanged original IAT');row=dict(label=label,root=root,result=dict(before_cpu=before,cpu=self.cpu(),boundary=self.cpu()['EIP'],instruction_counts=[dict(va=p,count=n) for p,n in sorted(counts.items())],instruction_sha256=ih.hexdigest(),writes=writes,write_sha256=wh.hexdigest(),api_calls=copy.deepcopy(self.api_calls)),entry_mappings=maps,display_calls=display,conversions=conversions,full_memory=self.memory_evidence.snapshot(),architectural_cpu=base.architectural_cpu(self.u),ledger=previous.previous.crt.old.ledger(self),state=previous.dialogue.text_state(self),queue=previous.task.queue(self),loop_state=state(self),calls=calls,pending=pending,fault=fault,unicorn_error=error,requested_boundary=stop);self.loop_attempts.append(row);print('loop segment',label,hex(self.cpu()['EIP']),sum(counts.values()),pending and pending['kind'],fault,flush=True);need(self.cpu()['EIP']==stop or pending is not None or fault is not None,'bounded actual loop frontier');return row
 def continue_loop(self):
  self.loop_attempts=[];before=state(self);entry_cpu=base.architectural_cpu(self.u);entry_memory=base.memory_rows(self.u);owners=dict(opening_closed=self.opening_gpu.closed,role9_closed=self.role_gpu.closed,fourth_closed=self.fourth_gpu.closed,opening_textures=copy.deepcopy(self.opening_textures),role9_textures=copy.deepcopy(self.role_textures),allocations=copy.deepcopy(self.allocations));need(not any(owners[k] for k in ('opening_closed','role9_closed','fourth_closed')),'all current source resource owners still live');steps=[]
  for va,recv in ((0x425de0,previous.task.INPUT),(0x40db90,previous.task.MANAGER),(0x40dc80,previous.task.MANAGER)):
   steps.append(self.loop_step('loop_request_or_queue_'+hex(va),RETURN,dict(va=va,receiver=recv,args=[],sp=STACK,return_va=RETURN)))
  for label,stop,root in [('original_loop_to_world',0x46b470,dict(va=0x4539b0,receiver=TACT,args=[],sp=STACK,return_va=RETURN)),('continuous_original_world_return',0x453a11,None),('continuous_original_loop_to_yield',0x422360,None)]:
   s=self.loop_step(label,stop,root);steps.append(s)
   if s['pending'] or s['fault']:break
  final=state(self);memory=base.memory_rows(self.u);need(memory==steps[-1]['full_memory'],'fresh complete loop boundary rehash');return dict(contract=contracts(),before=before,entry_architectural_cpu=entry_cpu,entry_memory=entry_memory,owners=owners,steps=steps,final=final,final_memory=memory,final_architectural_cpu=base.architectural_cpu(self.u),frontier=copy.deepcopy(steps[-1]['pending'] or steps[-1]['fault']),new_declared_loop_roots=1,new_VM_or_world_roots=0,host_game_control_writes=0,new_OS_input=False,original_outer_scheduler=False,cooperative_yield_executed=False)

def run_case(helper,build,gpu,gpubuild,role_gpu,rolebuild,opening_gpu,openingbuild,name,scene):
 instances=[]
 class Attached(Guest):
  def __init__(self,*a,**kw):super().__init__(*a,**kw);instances.append(self)
 call=previous.adapt(previous.run_case,[("analysis/school-retained-opening-failed-","analysis/school-retained-world-loop-failed-"),("fonts=getattr(g,", "world_loop_attempts=getattr(g,'loop_attempts',[]),fonts=getattr(g,")],Guest=Attached);c=call(helper,build,gpu,gpubuild,role_gpu,rolebuild,opening_gpu,openingbuild,name,scene);c['world_loop']=instances[0].loop_record;return c

def matrix_header(rows):
 return dict(schema_version=1,contract=contracts(),case_reports=rows,new_VM_roots=0,game_function_substitutions=0,IAT_rebindings=0,new_OS_input=False,new_GPU=True,new_hidden_windows=True,actual_D3D_draw_or_Present=False,original_outer_scheduler=False,historical_heap_restored=False,R3_complete=False,R6_complete=False)

def produce_group(args):
 name,prefix,existing=args;rows=[];helper=build=gpu=gb=rgpu=rb=ogpu=ob=None
 for scene in (76,77):
  if name=='initial' and scene==76 and existing:
   path=existing
   with gzip.open(ROOT/path,'rt',encoding='utf8') as f:c=json.load(f)
   need((c['name'],c['scene_capture'])==(name,scene) and c['world_loop']['contract']==contracts(),'existing exact source case')
  else:
   if helper is None:
    tag=prefix+'-'+name;helper,build=platform.build(ROOT/('.venv-audit/'+tag+'-crt.exe'));gpu,gb=previous.previous.previous.build_gpu(ROOT/('.venv-audit/'+tag+'-fourth.exe'));rgpu,rb=previous.previous.previous.build_gpu(ROOT/('.venv-audit/'+tag+'-role9.exe'));ogpu,ob=previous.previous.previous.build_gpu(ROOT/('.venv-audit/'+tag+'-glyph.exe'))
   path='analysis/'+prefix+'-'+name+'-'+str(scene)+'.json.gz';need(not (ROOT/path).exists(),'fresh source case');c=run_case(helper,build,gpu,gb,rgpu,rb,ogpu,ob,name,scene);previous.write_report(path,c)
  raw=(ROOT/path).read_bytes();rows.append(dict(name=name,scene_capture=scene,path=path,sha256=sha(raw),bytes=len(raw)));del c;print('source ordinary loop case saved',name,scene,flush=True)
 return rows

if __name__=='__main__':
 import argparse
 from concurrent.futures import ProcessPoolExecutor
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--existing-initial76');p.add_argument('--jobs',type=int,default=1);a=p.parse_args();out=ROOT/a.out
 if out.exists() or not 1<=a.jobs<=3:p.error('fresh immutable matrix; 1..3 independent source workers')
 args=[(name,out.stem,a.existing_initial76) for name in ('initial','student9_waiting','fifth_class')];rows=[]
 if a.jobs==1:
  for group in args:rows.extend(produce_group(group))
 else:
  with ProcessPoolExecutor(max_workers=a.jobs) as executor:
   for group in executor.map(produce_group,args):rows.extend(group)
 result=matrix_header(rows);result['source_processes']=a.jobs;out.write_text(json.dumps(result,indent=2)+chr(10),encoding='utf8',newline=chr(10))
