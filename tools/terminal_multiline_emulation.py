"""Original three-line and cross-layer terminal dialogue in current native owners."""
import argparse,copy,hashlib,json,struct,time,types
from functools import lru_cache
from tools import terminal_next_dialogue_emulation as parent

ROOT,CODE,need,sha,terminal,MAIN,VM,STACK,RETURN,TASK,INPUT,MANAGER,KEYBOARD,overlay=(getattr(parent,n) for n in ('ROOT','CODE','need','sha','terminal','MAIN','VM','STACK','RETURN','TASK','INPUT','MANAGER','KEYBOARD','overlay'))
RANGES,ALLOWED,REFERENCE=parent.RANGES,parent.ALLOWED,parent.REFERENCE
EXTRA_RANGES=();RASTERS=(0x3EE00000,0x3EF00000,0x3F000000);QUERIES=parent.QUERIES
PROJECTION_DOMAINS=tuple('overlay-multiline-'+str(i) for i in range(3))
PROJECTION_STRIDE=parent.PROJECTION_STRIDE;PREFIX_NEXT_MAX=parent.NEXT_DIALOGUE_NEXT_MAX
MULTILINE_NEXT_MAX=PREFIX_NEXT_MAX+21*PROJECTION_STRIDE;GDI_GUEST_START=parent.GDI_GUEST_START
PARENT_ACCEPTANCE='analysis/terminal-next-dialogue-acceptance-v1-20261028.json'
PARENT_ACCEPTANCE_SHA='0d849b99865609cceecbf5f8ad1081f90631156aabda15c69f520b04d9b8cac3'
PARENT_SOURCE='analysis/terminal-next-dialogue-source-v3-20261028.json.gz'
PARENT_SOURCE_SHA='c75bb96032732b4e38f56ebba2e33d9fbf4d7681532aca6a1b8cdc19ee8518ad'
PARENT_PROOF='analysis/terminal-next-dialogue-proof-v1-20261028.json'
PARENT_PROOF_SHA='fa786e29b8c332df1a6d42f75e89abe8bd83084f6ade7fe9466cd58d96c4e3a3'
followup=parent.parent.parent

def object_at(layer):return VM+0x430+layer*0xAB8
def node_at(layer):return VM+0x6F60+layer*0xE0
def record_at(layer,index=0):return object_at(layer)+0x28+index*0x110

@lru_cache(maxsize=1)
def fixed_parents():
 refs={k:followup.parent.file_ref(p,h) for k,p,h in (('acceptance',PARENT_ACCEPTANCE,PARENT_ACCEPTANCE_SHA),('source',PARENT_SOURCE,PARENT_SOURCE_SHA),('proof',PARENT_PROOF,PARENT_PROOF_SHA))}
 a=json.loads((ROOT/PARENT_ACCEPTANCE).read_text(encoding='utf8'))
 need(a['source_report']==refs['source'] and a['independent_proof']==refs['proof'] and a['tasks_complete']==3 and a['boundaries']['VM_PC_per_case']==[256,268] and a['boundaries']['VM_wait']==1,'accepted next-dialogue confirmation boundary');return refs

def fixed_parent_times():return parent.fixed_parent_times()
def helper_contract():return parent.helper_contract()
def helpers(prefix='terminal-multiline'):return parent.helpers(prefix)

@lru_cache(maxsize=1)
def fixed_parent_forward_summaries():
 raw=(ROOT/PARENT_PROOF).read_bytes();need(sha(raw)==PARENT_PROOF_SHA,'fixed compact multiline parent proof')
 return {c['name']:c['forward_summary']['full_cumulative'] for c in json.loads(raw)['cases']}

def validate_parent_prefix(machine):
 name=machine.live_input['name'];expected=fixed_parent_forward_summaries()[name];actual=machine.mark();need(actual==expected,'fixed complete next-dialogue prefix '+name+' expected='+repr(expected)+' actual='+repr(actual));print('multiline prefix preflight',name,actual,flush=True)
 return dict(case=name,fixed_proof_sha256=PARENT_PROOF_SHA,expected=expected,actual=actual)

def branch(name):
 need(name in ('neutral_running','timeout_before_combat'),'one original multiline branch');win=name=='neutral_running'
 lines=[dict(PC=p,text_index=t,layer=l,record_index=i) for p,t,l,i in ([(268,6,7,0),(274,7,7,1),(280,8,7,2)] if win else [(280,8,7,0),(298,9,5,0)])]
 return dict(first_PC=256 if win else 268,segment=2 if win else 11,role=None,lines=lines,ready_PC=290 if win else 308,final_PC=294 if win else 312,scene_capture=76 if win else 77,final_layer=7 if win else 5)

def projection_domain(index):
 need(type(index)is int and 0<=index<3,'one of three original multiline creation ordinals');return PROJECTION_DOMAINS[index]

class MultilineProjection:
 def __init__(self,machine):
  self.machine=machine;self.space=machine.space;self.prefix=copy.deepcopy(self.space.ledger());self.prefix_next=self.space.next
  allowed=('overlay',parent.FOLLOWUP_POINTER_DOMAIN,parent.FOLLOWUP_BITS_DOMAIN)+parent.parent.PROJECTION_DOMAINS+parent.PROJECTION_DOMAINS
  need(all(r['domain'] in allowed for r in self.prefix) and self.prefix_next<=PREFIX_NEXT_MAX,'complete bounded parent GPU identities');parent.followup_pointer_prefix(machine,self.prefix)
 def result(self,domain,value,key=None):
  r=self.machine.ml_current;need(domain=='overlay' and r is not None and r['kind']=='text','only current original multiline text creation');i=r['creation_index'];line=self.machine.ml_branch['lines'][i];target=projection_domain(i)
  need(r['record']==record_at(line['layer'],line['record_index']) and r['projection_domain']==target,'domain independently tied to current layer/count record')
  result=self.space.result(target,value,key);rows=self.space.ledger();current=[x for x in rows if x['domain']==target]
  need(('texture' in value or 'bits' in value) and len(current)==(6 if 'texture' in value else 7),'six interfaces and one complete surface identity')
  need(rows[:len(self.prefix)]==self.prefix and self.space.next<=MULTILINE_NEXT_MAX<GDI_GUEST_START,'old identities exact, new namespace below GDI');return result

def namespaced(fn):
 def rename(n):
  if fn.__name__=='gpu_api' and n=='space':return 'ml_space'
  return 'ml_'+n[3:] if n.startswith('fu_') else 'multiline_'+n[9:] if n.startswith('followup_') else n
 return types.FunctionType(fn.__code__.replace(co_names=tuple(rename(n) for n in fn.__code__.co_names)),fn.__globals__,fn.__name__,fn.__defaults__,fn.__closure__)

class MultilineMachine(parent.NextDialogueMachine):
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.multiline_active=self.multiline_ready=self.multiline_cleaning=False;self.multiline_stop=None
  for n in ('segments','frames','leaves','commands','writes','queries','bindings','gpu','calls','conversions','resources','observers','cleanup','replacements','clears'):setattr(self,'ml_'+n,[])
  self.ml_live={};self.ml_count=self.ml_write_count=0;self.ml_ih=hashlib.sha256();self.ml_wh=hashlib.sha256();self.ml_current=self.ml_pending_release=None
 ml_mark=namespaced(followup.FollowupMachine.fu_mark)
 ml_capture=namespaced(followup.FollowupMachine.fu_capture)
 ml_prefix_counts=namespaced(followup.FollowupMachine.fu_prefix_counts)
 ml_observe=namespaced(followup.FollowupMachine.fu_observe)
 ml_prepare=namespaced(followup.FollowupMachine.fu_prepare)
 ml_gdi=namespaced(followup.FollowupMachine.fu_gdi)
 ml_segment=namespaced(followup.FollowupMachine.fu_segment)
 ml_frame=namespaced(followup.FollowupMachine.fu_frame)
 ml_resume_frame=namespaced(followup.FollowupMachine.fu_resume_frame)
 ml_font=namespaced(followup.FollowupMachine.fu_font)
 ml_finish_resource=namespaced(followup.FollowupMachine.fu_finish_resource)
 ml_actual_root=namespaced(followup.FollowupMachine.fu_actual_root)
 _ml_captured=namespaced(followup.FollowupMachine.fu_captured)
 _ml_gpu_api=namespaced(followup.FollowupMachine.gpu_api)
 _ml_api_crt=namespaced(followup.FollowupMachine.api_crt)
 def ml_captured(self,capture):
  row=self._ml_captured(capture);row['cycle']='multiline_confirmation';return row
 def ml_set_raster(self,address):
  need(address in RASTERS,'finite separately mapped multiline DIB destinations');service=self.name_platform.service;fn=service.call_raster;service.call_raster=types.MethodType(types.FunctionType(fn.__func__.__code__,dict(fn.__func__.__globals__,RASTER=address)),service)
 def api_crt(self,slot):
  if not self.multiline_ready:return super().api_crt(slot)
  return self._ml_api_crt(slot)
 def gpu_api(self,at):
  if not self.multiline_ready:return super().gpu_api(at)
  self._ml_gpu_api(at);call=self.ml_gpu[-1]
  if call['op']=='release':
   for resources,live in ((self.nd_resources,self.nd_live),(self.nx_resources,self.nx_live),(self.fu_resources,self.fu_live)):
    for r in resources:
     if r['generation']==call['generation']:
      need(r['alive'] and r['record']==call['record'] and live.get(r['texture']['pointer']) is r,'same live predecessor generation released once');r.update(alive=False,release_wire_index=call['wire_index'],released_phase='multiline_'+call['phase']);del live[r['texture']['pointer']]
 def write_hook(self,uc,access,at,size,value,context):
  super().write_hook(uc,access,at,size,value,context)
  if self.multiline_active:
   if getattr(self,'ml_keyboard_fragment',False):need(KEYBOARD<=at and at+size<=KEYBOARD+0xA00 or STACK<=at and at+size<=STACK+0x20000,'finite original multiline keyboard writes')
   self.ml_write_count+=1;self.ml_wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
   if VM<=at<VM+0x9400 or KEYBOARD<=at<KEYBOARD+0xA00 or TASK<=at<TASK+0x190 or at==0:self.ml_writes.append(dict(pc=self.getreg('EIP'),address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))
 def code(self,uc,at,size,context):
  active=self.multiline_active
  if active:
   if at==self.multiline_stop:uc.emu_stop();return
   if self.ml_pending_release and at==self.ml_pending_release['caller'] and self.getreg('ESP')==self.ml_pending_release['return_ESP']:
    q=self.ml_pending_release;need(self.get(q['record']+44)==0 and not self.ml_resources[q['ledger_index']]['alive'],'original multiline destructor clears retired record');q['after']=self.ml_capture();q['GPU_APIs']=copy.deepcopy(self.ml_gpu[q.pop('GPU_start'):]);self.ml_replacements.append(q);self.ml_pending_release=None
   if at==0x403730:
    record=self.getreg('ECX');pointer=self.get(record+44);sp=self.getreg('ESP')
    if pointer in self.ml_live and self.get(sp)==0x4051AE:
     r=self.ml_live[pointer];current=self.ml_current;need(current is not None and record==current['record'] and r['generation'] in self.ml_prefix_generations,'original prior generation of exact current multiline record');self.ml_pending_release=dict(entry=at,caller=self.get(sp),return_ESP=sp+4,record=record,generation=r['generation'],ledger_index=self.ml_resources.index(r),before=self.ml_capture(),GPU_start=len(self.ml_gpu))
   if at==0x4CE9C5:
    p=self.get(VM+16)+self.get(VM+28);op,n=struct.unpack('<HH',self.read(p,4));need(self.get(VM+28)<self.ml_branch['final_PC'],'multiline successor unexecuted');self.ml_commands.append(dict(PC=self.get(VM+28),opcode=op,bytes=n,source_pointer=p))
   if at in overlay.parent.APIS and self.get(self.getreg('ESP'))==overlay.parent.APIS[at][2]:
    sp=self.getreg('ESP');ret=self.get(sp);first=len(self.task_APIs);super().code(uc,at,size,context);need(len(self.task_APIs)==first+1,'one actual multiline task leaf');r=self.task_APIs[-1];self.ml_leaves.append(dict(kind='TASK',call=dict(r,sp=sp,return_va=ret,pop=4,value=r['result'],memory_outputs=[],new_mappings=[])));return
   if at in self.gdi_targets:self.ml_gdi(at);return
   if at==0x405869:
    sp=self.getreg('ESP');args=[self.get(sp+j) for j in range(0,24,4)];self.ml_conversions.append(dict(entry=at,args=args,resource_label=self.ml_current['label'],record=self.ml_current['record'],rect=list(struct.unpack('<4I',self.read(args[4],16))),point=list(struct.unpack('<2I',self.read(args[5],8)))))
   if at in QUERIES:
    sp=self.getreg('ESP');self.ml_queries.append(dict(entry=at,CPU=self.cpu(),receiver=self.getreg('ECX'),stack_hex=self.read(sp,68).hex(),selected_layer=self.get(VM+0x1CC,'B'),nodes={str(i):self.read(node_at(i),0xE0).hex() for i in (4,5,7)},objects={str(i):self.read(object_at(i),0xAB8).hex() for i in (4,5,7)}))
  super().code(uc,at,size,context)
  if active and at in ALLOWED:self.ml_count+=1;self.ml_ih.update(struct.pack('<I',at))
 def ml_select_clear(self,configuration,layer,text_PC):
  self.ml_frame('select_layer'+str(layer));need(self.get(VM+28)==text_PC-4 and self.get(VM+0x1CC,'B')==layer,'original configuration selects multiline layer');before=self.ml_capture();wire=len(self.gpu.trace);old=[self.get(record_at(layer,i)+44) for i in range(3)];self.ml_frame('clear_layer'+str(layer))
  need(self.get(VM+28)==text_PC and self.get(object_at(layer)+22,'H')==0 and len(self.gpu.trace)==wire and [self.get(record_at(layer,i)+44) for i in range(3)]==old,'original44 clears count without releasing or changing old texture pointers');self.ml_clears.append(dict(configuration=configuration,layer=layer,before=before,after=self.ml_capture(),GPU_wire_before=wire,GPU_wire_after=len(self.gpu.trace)))
 def ml_text(self,index):
  line=self.ml_branch['lines'][index];pc,layer,i=line['PC'],line['layer'],line['record_index'];need(self.get(VM+28)==pc and self.get(object_at(layer)+22,'H')==i,'original current per-layer text count and PC')
  r=self.ml_prepare('text','multiline_text_'+str(index),record_at(layer,i),RASTERS[index]);r.update(line,creation_index=index,object=object_at(layer),node=node_at(layer),projection_domain=projection_domain(index))
  self.ml_frame('text_to_font',self.font_target);self.ml_font(r);self.ml_segment('multiline_text_pixels_handler_complete_task',0x403BD0);r['completion']=self.ml_capture();need(self.get(VM+28)==pc+6 and self.get(object_at(layer)+22,'H')==i+1,'original append and complete text task');self.ml_finish_resource(r);self.ml_resume_frame('multiline_text_complete',lambda:None)
 def admission(self):
  a=super().admission();self.ml_prefix_preflight=validate_parent_prefix(self);self.ml_branch=branch(self.live_input['name']);self.ml_prefix=self.ml_prefix_counts();self.ml_before=self.ml_capture();need((self.get(VM+28),self.get(VM+32,'H'))==(self.ml_branch['first_PC'],1),'accepted next-dialogue wait')
  self.ml_resources=copy.deepcopy(self.nd_resources);self.ml_prefix_generations={r['generation'] for r in self.ml_resources};self.ml_live={r['texture']['pointer']:r for r in self.ml_resources if r['alive']};self.ml_resources_before=copy.deepcopy(self.ml_resources);self.ml_space=MultilineProjection(self)
  need(len(self.ml_resources)==(11 if self.live_input['name']=='neutral_running' else 13) and len(self.ml_live)==(9 if self.live_input['name']=='neutral_running' else 10),'complete current parent generations')
  end=len(self.nd_leaves);self.nd_cleanup.append(dict(label='forward_leaf_end_only',leaves=[end,end]));self.multiline_ready=self.multiline_active=self.active_overlay=True
  stream=parent.parent.parent.parent.parent.input_contract()['streams'][str(self.ml_branch['scene_capture'])];self.ml_captured(stream['captures'][0])
  for _ in range(2):
   self.ml_frame('held_parent_confirmation');need((self.get(VM+28),self.get(VM+32,'H'),self.get(KEYBOARD+0x4B9,'B'))==(self.ml_branch['first_PC'],1,0),'idle holds parent confirmation')
  self.ml_captured(stream['captures'][1]);self.ml_frame('captured_press');need((self.get(VM+28),self.get(VM+32,'H'),self.get(KEYBOARD+0x4B9,'B'))==(self.ml_branch['first_PC'],0,128),'complete task consumes new captured press');confirmed=self.ml_capture();self.ml_captured(stream['captures'][2]);need(self.get(KEYBOARD+0x4B9,'B')==0,'original captured release')
  self.ml_select_clear(4,7,self.ml_branch['lines'][0]['PC'])
  for i,line in enumerate(self.ml_branch['lines']):
   if i and line['layer']!=self.ml_branch['lines'][i-1]['layer']:self.ml_select_clear(8,5,line['PC'])
   self.ml_text(i)
  for _ in range(300):
   self.ml_frame('text_readiness');need(self.get(VM+28)==self.ml_branch['ready_PC'],'only original50 before multiline confirmation')
   if self.get(VM+32,'H')==0:break
  else:raise ValueError('bounded original multiline readiness')
  ready=self.ml_capture();self.ml_frame('enter_new_confirmation');need((self.get(VM+28),self.get(VM+32,'H'))==(self.ml_branch['final_PC'],1),'natural multiline confirmation');confirmation=self.ml_capture()
  for _ in range(2):
   self.ml_frame('held_new_confirmation');need((self.get(VM+28),self.get(VM+32,'H'),self.get(KEYBOARD+0x4B9,'B'))==(self.ml_branch['final_PC'],1,0),'two complete no-input holds')
  final=self.ml_capture();observations=self.ml_observe('final');self.multiline_active=self.active_overlay=False
  for r in self.ml_resources:r['alive_after_forward']=r['alive']
  need(len(self.ml_replacements)==2 and len(self.ml_resources)==len(self.ml_resources_before)+len(self.ml_branch['lines']),'exact new creations and two prior-record replacements')
  self.ml_result=dict(prefix=self.ml_prefix,prefix_preflight=self.ml_prefix_preflight,before=self.ml_before,branch=self.ml_branch,resources_before=self.ml_resources_before,resources=copy.deepcopy(self.ml_resources),bindings=self.ml_bindings,confirmed=confirmed,clears=self.ml_clears,role=None,role_container=None,ready=ready,confirmation=confirmation,final=final,segments=self.ml_segments,frames=self.ml_frames,leaves=self.ml_leaves,commands=self.ml_commands,writes=self.ml_writes,queries=self.ml_queries,replacements=self.ml_replacements,GPU_APIs=self.ml_gpu,calls=self.ml_calls,conversions=self.ml_conversions,readbacks=observations,readback_observers=self.ml_observers,GDI_trace=copy.deepcopy(self.name_platform.trace[self.ml_prefix['GDI_trace']:]),GDI_handle_projection=self.name_platform.space.ledger(),accounting=self.get(0x765720),forward_wire_end=len(self.gpu.trace),CRT_forward_wire_end=len(self.live.trace),GPU_projection_before=dict(next=self.ml_space.prefix_next,ledger=self.ml_space.prefix),GPU_projection=[r for r in self.space.ledger() if r['domain'] in PROJECTION_DOMAINS]);return a
 def nd_actual_root(self,*args,**kwargs):
  if not self.multiline_ready:return super().nd_actual_root(*args,**kwargs)
  return self.ml_actual_root(*args,**kwargs)
 def resource_root(self,label,*args,**kwargs):
  if self.multiline_ready and label=='supplemental_original_group20_destructor' and self.live_input['name']=='neutral_running':self.ml_actual_root('supplemental_original_multiline_third_text_destructor',0x403730,receiver=record_at(7,2))
  return super().resource_root(label,*args,**kwargs)
 def run(self):
  row=super().run();need(not self.ml_live and all(not r['alive'] for r in self.ml_resources),'all current multiline generations originally released');row.update(terminal_multiline=self.ml_result,multiline_cleanup=self.ml_cleanup,multiline_resources_after_cleanup=copy.deepcopy(self.ml_resources));return row

def source_contract():
 return dict(parent=parent.source_contract(),fixed_predecessor=fixed_parents(),branches={n:branch(n) for n in ('neutral_running','timeout_before_combat')},keyboard=KEYBOARD,raw_device_bytes=256,new_capture_cycle=True,captured_inputs=parent.parent.parent.parent.parent.input_contract(),first_confirmation_released=True,next_confirmation_released=False,forward_roots=[0x40DB90,0x40DC80,0x425DE0,0x454CF0],new_VM_or_handler_roots=0,derived_input_host_writes=0,PC_or_wait_host_writes=0,new_OS_input=False,draw_or_Present=False,new_rasters=list(RASTERS),helper=helper_contract(),extra_code=[],GPU_projection=dict(prefix_entries_unchanged=True,new_domains=list(PROJECTION_DOMAINS),domain_from_creation_layer_count=True,original_AddressSpace_algorithm=True,keys_per_new_generation=7,prefix_next_max=PREFIX_NEXT_MAX,new_next_max=MULTILINE_NEXT_MAX,GDI_guest_start=GDI_GUEST_START))

save_source=parent.save_source
def run_case(c,ch,gh,ticks=None):
 fixed=fixed_parent_times()[c['name']];ticks=list(fixed) if ticks is None else ticks;need(ticks==fixed,'exact accepted original clock stream');instances=[]
 class Attached(MultilineMachine):
  def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);instances.append(self)
 class Diagnostics:
  @staticmethod
  def save(path,data):
   if instances:
    m=instances[0];data['multiline']=dict(active=m.multiline_active,segments=m.ml_segments,frames=m.ml_frames,leaves=m.ml_leaves,resources=m.ml_resources,bindings=m.ml_bindings,commands=m.ml_commands,replacements=m.ml_replacements,clears=m.ml_clears,CRT_trace=copy.deepcopy(m.live.trace),GPU_trace=copy.deepcopy(m.gpu.trace),GDI_trace=copy.deepcopy(m.name_platform.trace),memory=m.snapshot(),trace=m.mark(),local_trace=m.ml_mark())
   save_source(path.replace('terminal-overlay-diagnostic-','terminal-multiline-diagnostic-').replace('.json.gz','-20261029-'+str(time.time_ns())+'.json.gz'),data)
 fn=types.FunctionType(overlay.run_case.__code__,dict(overlay.run_case.__globals__,OverlayMachine=Attached,terminal=Diagnostics),closure=overlay.run_case.__closure__);return fn(c,ch,gh,ticks)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case',type=int);p.add_argument('--helper-prefix',default='terminal-multiline');a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable multiline source');fixed_parents();ch,gh,b=helpers(a.helper_prefix);rows=[]
 for c in (overlay.parent.corpus() if a.case is None else [overlay.parent.corpus()[a.case]]):rows.append(run_case(c,ch,gh));print('multiline source',c['name'],'new confirmation held',flush=True)
 save_source(a.out,dict(schema_version=1,source_contract=source_contract(),helper_build=b,cases=rows,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False))
