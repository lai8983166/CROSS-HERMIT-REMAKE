"""Last original terminal dialogue group with retained native texture ownership."""
import argparse,copy,hashlib,json,struct,time,types
from functools import lru_cache
from tools import terminal_multiline_emulation as parent
from tools import terminal_last_dialogue_gdi as lifetime_gdi

ROOT,CODE,need,sha,terminal,MAIN,VM,STACK,RETURN,TASK,INPUT,MANAGER,KEYBOARD,overlay=(getattr(parent,n) for n in ('ROOT','CODE','need','sha','terminal','MAIN','VM','STACK','RETURN','TASK','INPUT','MANAGER','KEYBOARD','overlay'))
RANGES,ALLOWED,REFERENCE=parent.RANGES,parent.ALLOWED,parent.REFERENCE
EXTRA_RANGES=();RASTERS=(0x3F100000,0x3F200000,0x3F300000);QUERIES=parent.QUERIES
PROJECTION_DOMAINS=tuple('overlay-last-dialogue-'+str(i) for i in range(3))
PROJECTION_STRIDE=parent.PROJECTION_STRIDE;PREFIX_NEXT_MAX=parent.MULTILINE_NEXT_MAX
GPU_GUEST_START=0x48001000;LAST_DIALOGUE_NEXT_MAX=GPU_GUEST_START+21*PROJECTION_STRIDE;GDI_GUEST_START=parent.GDI_GUEST_START
PARENT_ACCEPTANCE='analysis/terminal-multiline-acceptance-v1-20261029.json'
PARENT_ACCEPTANCE_SHA='ef160a3bbbccf4816f4741fc6bef7aa6687683639a95ed2c55224ea5ab9cc555'
PARENT_SOURCE='analysis/terminal-multiline-source-v1-20261029.json.gz'
PARENT_SOURCE_SHA='b14ad5cf6b3bfceb9f6d291a1f33f0ff0036c301900b306065b8c1e7420ba1e1'
PARENT_PROOF='analysis/terminal-multiline-proof-v1-20261029.json'
PARENT_PROOF_SHA='40dacc03e9c4ea0542eceb8b11c999521f9bcc408d0debabb3a474319993b6c2'
followup=parent.followup

def object_at(layer):return VM+0x430+layer*0xAB8
def node_at(layer):return VM+0x6F60+layer*0xE0
def record_at(layer,index=0):return object_at(layer)+0x28+index*0x110

@lru_cache(maxsize=1)
def fixed_parents():
 refs={k:followup.parent.file_ref(p,h) for k,p,h in (('acceptance',PARENT_ACCEPTANCE,PARENT_ACCEPTANCE_SHA),('source',PARENT_SOURCE,PARENT_SOURCE_SHA),('proof',PARENT_PROOF,PARENT_PROOF_SHA))}
 a=json.loads((ROOT/PARENT_ACCEPTANCE).read_text(encoding='utf8'))
 need(a['source_report']==refs['source'] and a['independent_proof']==refs['proof'] and a['tasks_complete']==3 and a['boundaries']['VM_PC_per_case']==[294,312] and a['boundaries']['VM_wait']==1,'accepted next-dialogue confirmation boundary');return refs

def fixed_parent_times():return parent.fixed_parent_times()
def experimental_helper_contract():
 old=ROOT/'tools/terminal_followup_d3d8_platform.cs';new=ROOT/'tools/terminal_last_dialogue_d3d8_platform.cs';a=old.read_bytes();b=new.read_bytes();need(a.count(b'resources.Count>=10')==a.count(b'max_textures=10')==1,'exact two original capacity declarations');expected=a.replace(b'resources.Count>=10',b'resources.Count>=11').replace(b'max_textures=10',b'max_textures=11');need(a!=expected and b==expected,'only actual live texture capacity10 to11 changes; all ABI/protection/32-create limits frozen')
 return dict(previous=parent.helper_contract(),original=dict(path=old.relative_to(ROOT).as_posix(),sha256=sha(a)),current=dict(path=new.relative_to(ROOT).as_posix(),sha256=sha(b)),only_live_capacity_changed=True,max_textures=11,max_creates=32,duplicate_live_address_still_rejected=True,ABI_and_all_other_guards_unchanged=True)
def helper_contract():return parent.helper_contract()
def helpers(prefix='terminal-last-dialogue'):return parent.helpers(prefix)

@lru_cache(maxsize=1)
def fixed_parent_forward_summaries():
 raw=(ROOT/PARENT_PROOF).read_bytes();need(sha(raw)==PARENT_PROOF_SHA,'fixed compact last_dialogue parent proof')
 return {c['name']:c['forward_summary']['full_cumulative'] for c in json.loads(raw)['cases']}

def validate_parent_prefix(machine):
 projection=getattr(machine,'ld_gdi_projection',None)
 if projection is not None:need(len(projection.calls)==len(projection.plan),'complete planned original GDI parent prefix')
 name=machine.live_input['name'];expected=fixed_parent_forward_summaries()[name];actual=machine.mark();need(actual==expected,'fixed complete next-dialogue prefix '+name+' expected='+repr(expected)+' actual='+repr(actual));print('last_dialogue prefix preflight',name,actual,flush=True)
 return dict(case=name,fixed_proof_sha256=PARENT_PROOF_SHA,expected=expected,actual=actual)

def branch(name):
 need(name in ('neutral_running','timeout_before_combat'),'one original last-dialogue branch');win=name=='neutral_running'
 lines=[dict(PC=p,text_index=t,layer=l,record_index=i) for p,t,l,i in ([(306,9,4,0)] if win else [(324,10,7,0),(330,11,7,1),(336,12,7,2)])]
 return dict(first_PC=294 if win else 312,segment=2 if win else 11,role=None,lines=lines,ready_PC=316 if win else 346,final_PC=320 if win else 350,scene_capture=76 if win else 77,final_layer=4 if win else 7)

def projection_domain(index):
 need(type(index)is int and 0<=index<3,'one of three original last_dialogue creation ordinals');return PROJECTION_DOMAINS[index]

class LastDialogueProjection:
 def __init__(self,machine):
  self.machine=machine;self.space=machine.space;self.prefix=copy.deepcopy(self.space.ledger());self.prefix_next=self.space.next
  allowed=('overlay','overlay-followup-text-pointer','overlay-followup-text-bits','overlay-replacement-0','overlay-replacement-1','overlay-next-dialogue-name','overlay-next-dialogue-portrait','overlay-next-dialogue-text')+parent.PROJECTION_DOMAINS
  need(all(v['domain'] in allowed for v in self.prefix) and self.prefix_next<=PREFIX_NEXT_MAX,'entire accepted parent projection');parent.parent.followup_pointer_prefix(machine,self.prefix)
  regions=list(machine.uc.mem_regions());need(all(b<GPU_GUEST_START or LAST_DIALOGUE_NEXT_MAX<=a for a,b,_ in regions),'entire new GPU address span disjoint from every current guest mapping');need(LAST_DIALOGUE_NEXT_MAX<=0x50000000<GDI_GUEST_START,'new GPU domain below CRT heap and GDI');need(all(not(GPU_GUEST_START<=v['guest']<LAST_DIALOGUE_NEXT_MAX) for v in self.prefix),'new identities never overlap retired or live parent identities')
  self.space.next=GPU_GUEST_START;self.namespace=dict(prefix_next=self.prefix_next,new_start=GPU_GUEST_START,new_end=LAST_DIALOGUE_NEXT_MAX,all_before_mappings_disjoint=True,before_mapping_count=len(regions),parent_ledger_unchanged=True,original_AddressSpace_guest_code_unchanged=True)

 def result(self,domain,value,key=None):
  r=self.machine.ld_current;need(domain=='overlay' and r is not None and r['kind']=='text','only current original last_dialogue text creation');i=r['creation_index'];line=self.machine.ld_branch['lines'][i];target=projection_domain(i)
  need(r['record']==record_at(line['layer'],line['record_index']) and r['projection_domain']==target,'domain independently tied to current layer/count record')
  result=self.space.result(target,value,key);rows=self.space.ledger();current=[x for x in rows if x['domain']==target]
  need(('texture' in value or 'bits' in value) and len(current)==(6 if 'texture' in value else 7),'six interfaces and one complete surface identity')
  need(rows[:len(self.prefix)]==self.prefix and self.space.next<=LAST_DIALOGUE_NEXT_MAX<GDI_GUEST_START,'old identities exact, new namespace below GDI');return result

def namespaced(fn):
 def rename(n):
  if fn.__name__=='gpu_api' and n=='space':return 'ld_space'
  return 'ld_'+n[3:] if n.startswith('fu_') else 'last_dialogue_'+n[9:] if n.startswith('followup_') else n
 return types.FunctionType(fn.__code__.replace(co_names=tuple(rename(n) for n in fn.__code__.co_names)),fn.__globals__,fn.__name__,fn.__defaults__,fn.__closure__)

class LastDialogueMachine(parent.MultilineMachine):
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.last_dialogue_active=self.last_dialogue_ready=self.last_dialogue_cleaning=False;self.last_dialogue_stop=None
  self.ld_gdi_projection=lifetime_gdi.install(self,ROOT)
  for n in ('segments','frames','leaves','commands','writes','queries','bindings','gpu','calls','conversions','resources','observers','cleanup','replacements','clears'):setattr(self,'ld_'+n,[])
  self.ld_live={};self.ld_count=self.ld_write_count=0;self.ld_ih=hashlib.sha256();self.ld_wh=hashlib.sha256();self.ld_current=self.ld_pending_release=None
 ld_mark=namespaced(followup.FollowupMachine.fu_mark)
 ld_capture=namespaced(followup.FollowupMachine.fu_capture)
 ld_prefix_counts=namespaced(followup.FollowupMachine.fu_prefix_counts)
 ld_observe=namespaced(followup.FollowupMachine.fu_observe)
 ld_prepare=namespaced(followup.FollowupMachine.fu_prepare)
 ld_gdi=namespaced(followup.FollowupMachine.fu_gdi)
 ld_segment=namespaced(followup.FollowupMachine.fu_segment)
 ld_frame=namespaced(followup.FollowupMachine.fu_frame)
 ld_resume_frame=namespaced(followup.FollowupMachine.fu_resume_frame)
 ld_font=namespaced(followup.FollowupMachine.fu_font)
 ld_finish_resource=namespaced(followup.FollowupMachine.fu_finish_resource)
 ld_actual_root=namespaced(followup.FollowupMachine.fu_actual_root)
 _ld_captured=namespaced(followup.FollowupMachine.fu_captured)
 _ld_gpu_api=namespaced(followup.FollowupMachine.gpu_api)
 _ld_api_crt=namespaced(followup.FollowupMachine.api_crt)
 def ld_captured(self,capture):
  row=self._ld_captured(capture);row['cycle']='last_dialogue_confirmation';return row
 def ld_set_raster(self,address):
  need(address in RASTERS,'finite separately mapped last_dialogue DIB destinations');service=self.name_platform.service;fn=service.call_raster;service.call_raster=types.MethodType(types.FunctionType(fn.__func__.__code__,dict(fn.__func__.__globals__,RASTER=address)),service)
 def api_crt(self,slot):
  if not self.last_dialogue_ready:return super().api_crt(slot)
  return self._ld_api_crt(slot)
 def gpu_api(self,at):
  if not self.last_dialogue_ready:return super().gpu_api(at)
  self._ld_gpu_api(at);call=self.ld_gpu[-1]
  if call['op']=='release':
   for resources,live in ((self.ml_resources,self.ml_live),(self.nd_resources,self.nd_live),(self.nx_resources,self.nx_live),(self.fu_resources,self.fu_live)):
    for r in resources:
     if r['generation']==call['generation']:
      need(r['alive'] and r['record']==call['record'] and live.get(r['texture']['pointer']) is r,'same live predecessor generation released once');r.update(alive=False,release_wire_index=call['wire_index'],released_phase='last_dialogue_'+call['phase']);del live[r['texture']['pointer']]
 def write_hook(self,uc,access,at,size,value,context):
  super().write_hook(uc,access,at,size,value,context)
  if self.last_dialogue_active:
   if getattr(self,'ld_keyboard_fragment',False):need(KEYBOARD<=at and at+size<=KEYBOARD+0xA00 or STACK<=at and at+size<=STACK+0x20000,'finite original last_dialogue keyboard writes')
   self.ld_write_count+=1;self.ld_wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
   if VM<=at<VM+0x9400 or KEYBOARD<=at<KEYBOARD+0xA00 or TASK<=at<TASK+0x190 or at==0:self.ld_writes.append(dict(pc=self.getreg('EIP'),address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))
 def code(self,uc,at,size,context):
  active=self.last_dialogue_active
  if active:
   if at==self.last_dialogue_stop:uc.emu_stop();return
   if self.ld_pending_release and at==self.ld_pending_release['caller'] and self.getreg('ESP')==self.ld_pending_release['return_ESP']:
    q=self.ld_pending_release;need(self.get(q['record']+44)==0 and not self.ld_resources[q['ledger_index']]['alive'],'original last_dialogue destructor clears retired record');q['after']=self.ld_capture();q['GPU_APIs']=copy.deepcopy(self.ld_gpu[q.pop('GPU_start'):]);self.ld_replacements.append(q);self.ld_pending_release=None
   if at==0x403730:
    record=self.getreg('ECX');pointer=self.get(record+44);sp=self.getreg('ESP')
    if pointer in self.ld_live and self.get(sp)==0x4051AE:
     r=self.ld_live[pointer];current=self.ld_current;need(current is not None and record==current['record'] and r['generation'] in self.ld_prefix_generations,'original prior generation of exact current last_dialogue record');self.ld_pending_release=dict(entry=at,caller=self.get(sp),return_ESP=sp+4,record=record,generation=r['generation'],ledger_index=self.ld_resources.index(r),before=self.ld_capture(),GPU_start=len(self.ld_gpu))
   if at==0x4CE9C5:
    p=self.get(VM+16)+self.get(VM+28);op,n=struct.unpack('<HH',self.read(p,4));need(self.get(VM+28)<self.ld_branch['final_PC'],'last_dialogue successor unexecuted');self.ld_commands.append(dict(PC=self.get(VM+28),opcode=op,bytes=n,source_pointer=p))
   if at in overlay.parent.APIS and self.get(self.getreg('ESP'))==overlay.parent.APIS[at][2]:
    sp=self.getreg('ESP');ret=self.get(sp);first=len(self.task_APIs);super().code(uc,at,size,context);need(len(self.task_APIs)==first+1,'one actual last_dialogue task leaf');r=self.task_APIs[-1];self.ld_leaves.append(dict(kind='TASK',call=dict(r,sp=sp,return_va=ret,pop=4,value=r['result'],memory_outputs=[],new_mappings=[])));return
   if at in self.gdi_targets:self.ld_gdi(at);return
   if at==0x405869:
    sp=self.getreg('ESP');args=[self.get(sp+j) for j in range(0,24,4)];self.ld_conversions.append(dict(entry=at,args=args,resource_label=self.ld_current['label'],record=self.ld_current['record'],rect=list(struct.unpack('<4I',self.read(args[4],16))),point=list(struct.unpack('<2I',self.read(args[5],8)))))
   if at in QUERIES:
    sp=self.getreg('ESP');self.ld_queries.append(dict(entry=at,CPU=self.cpu(),receiver=self.getreg('ECX'),stack_hex=self.read(sp,68).hex(),selected_layer=self.get(VM+0x1CC,'B'),nodes={str(i):self.read(node_at(i),0xE0).hex() for i in (4,5,7)},objects={str(i):self.read(object_at(i),0xAB8).hex() for i in (4,5,7)}))
  super().code(uc,at,size,context)
  if active and at in ALLOWED:self.ld_count+=1;self.ld_ih.update(struct.pack('<I',at))
 def ld_select_clear(self,configuration,layer,text_PC):
  self.ld_frame('select_layer'+str(layer));need(self.get(VM+28)==text_PC-4 and self.get(VM+0x1CC,'B')==layer,'original configuration selects last_dialogue layer');before=self.ld_capture();wire=len(self.gpu.trace);old=[self.get(record_at(layer,i)+44) for i in range(3)];self.ld_frame('clear_layer'+str(layer))
  need(self.get(VM+28)==text_PC and self.get(object_at(layer)+22,'H')==0 and len(self.gpu.trace)==wire and [self.get(record_at(layer,i)+44) for i in range(3)]==old,'original44 clears count without releasing or changing old texture pointers');self.ld_clears.append(dict(configuration=configuration,layer=layer,before=before,after=self.ld_capture(),GPU_wire_before=wire,GPU_wire_after=len(self.gpu.trace)))
 def ld_text(self,index):
  line=self.ld_branch['lines'][index];pc,layer,i=line['PC'],line['layer'],line['record_index'];need(self.get(VM+28)==pc and self.get(object_at(layer)+22,'H')==i,'original current per-layer text count and PC')
  r=self.ld_prepare('text','last_dialogue_text_'+str(index),record_at(layer,i),RASTERS[index]);r.update(line,creation_index=index,object=object_at(layer),node=node_at(layer),projection_domain=projection_domain(index))
  self.ld_frame('text_to_font',self.font_target);self.ld_font(r);self.ld_segment('last_dialogue_text_pixels_handler_complete_task',0x403BD0);r['completion']=self.ld_capture();need(self.get(VM+28)==pc+6 and self.get(object_at(layer)+22,'H')==i+1,'original append and complete text task');self.ld_finish_resource(r);self.ld_resume_frame('last_dialogue_text_complete',lambda:None)
 def admission(self):
  a=super().admission();self.ld_prefix_preflight=validate_parent_prefix(self);self.ld_branch=branch(self.live_input['name']);self.ld_prefix=self.ld_prefix_counts();self.ld_before=self.ld_capture();need((self.get(VM+28),self.get(VM+32,'H'))==(self.ld_branch['first_PC'],1),'accepted next-dialogue wait')
  self.ld_resources=copy.deepcopy(self.ml_resources);self.ld_prefix_generations={r['generation'] for r in self.ld_resources};self.ld_live={r['texture']['pointer']:r for r in self.ld_resources if r['alive']};self.ld_resources_before=copy.deepcopy(self.ld_resources);self.ld_space=LastDialogueProjection(self)
  need(len(self.ld_resources)==(14 if self.live_input['name']=='neutral_running' else 15) and len(self.ld_live)==10,'complete current parent generations')
  end=len(self.ml_leaves);self.ml_cleanup.append(dict(label='forward_leaf_end_only',leaves=[end,end]));self.last_dialogue_ready=self.last_dialogue_active=self.active_overlay=True
  stream=followup.parent.parent.input_contract()['streams'][str(self.ld_branch['scene_capture'])];self.ld_captured(stream['captures'][0])
  for _ in range(2):
   self.ld_frame('held_parent_confirmation');need((self.get(VM+28),self.get(VM+32,'H'),self.get(KEYBOARD+0x4B9,'B'))==(self.ld_branch['first_PC'],1,0),'idle holds parent confirmation')
  self.ld_captured(stream['captures'][1]);self.ld_frame('captured_press');need((self.get(VM+28),self.get(VM+32,'H'),self.get(KEYBOARD+0x4B9,'B'))==(self.ld_branch['first_PC'],0,128),'complete task consumes new captured press');confirmed=self.ld_capture();self.ld_captured(stream['captures'][2]);need(self.get(KEYBOARD+0x4B9,'B')==0,'original captured release')
  self.ld_select_clear(7 if self.live_input['name']=='neutral_running' else 4,self.ld_branch['final_layer'],self.ld_branch['lines'][0]['PC'])
  for i,line in enumerate(self.ld_branch['lines']):
   self.ld_text(i)
  for _ in range(300):
   self.ld_frame('text_readiness');need(self.get(VM+28)==self.ld_branch['ready_PC'],'only original50 before last_dialogue confirmation')
   if self.get(VM+32,'H')==0:break
  else:raise ValueError('bounded original last_dialogue readiness')
  ready=self.ld_capture();self.ld_frame('enter_new_confirmation');need((self.get(VM+28),self.get(VM+32,'H'))==(self.ld_branch['final_PC'],1),'natural last_dialogue confirmation');confirmation=self.ld_capture()
  for _ in range(2):
   self.ld_frame('held_new_confirmation');need((self.get(VM+28),self.get(VM+32,'H'),self.get(KEYBOARD+0x4B9,'B'))==(self.ld_branch['final_PC'],1,0),'two complete no-input holds')
  final=self.ld_capture();observations=self.ld_observe('final');self.last_dialogue_active=self.active_overlay=False
  for r in self.ld_resources:r['alive_after_forward']=r['alive']
  need(len(self.ld_replacements)==(1 if self.live_input['name']=='neutral_running' else 3) and len(self.ld_resources)==len(self.ld_resources_before)+len(self.ld_branch['lines']),'exact new creations and all retained prior-record replacements')
  self.ld_result=dict(prefix=self.ld_prefix,prefix_preflight=self.ld_prefix_preflight,before=self.ld_before,branch=self.ld_branch,resources_before=self.ld_resources_before,resources=copy.deepcopy(self.ld_resources),bindings=self.ld_bindings,confirmed=confirmed,clears=self.ld_clears,role=None,role_container=None,ready=ready,confirmation=confirmation,final=final,segments=self.ld_segments,frames=self.ld_frames,leaves=self.ld_leaves,commands=self.ld_commands,writes=self.ld_writes,queries=self.ld_queries,replacements=self.ld_replacements,GPU_APIs=self.ld_gpu,calls=self.ld_calls,conversions=self.ld_conversions,readbacks=observations,readback_observers=self.ld_observers,GDI_trace=copy.deepcopy(self.name_platform.trace[self.ld_prefix['GDI_trace']:]),GDI_handle_projection=self.name_platform.space.ledger(),accounting=self.get(0x765720),forward_wire_end=len(self.gpu.trace),CRT_forward_wire_end=len(self.live.trace),GPU_namespace=self.ld_space.namespace,GPU_projection_before=dict(next=self.ld_space.prefix_next,ledger=self.ld_space.prefix),GPU_projection=[r for r in self.space.ledger() if r['domain'] in PROJECTION_DOMAINS]);return a
 def ml_actual_root(self,*args,**kwargs):
  if not self.last_dialogue_ready:return super().ml_actual_root(*args,**kwargs)
  return self.ld_actual_root(*args,**kwargs)
 def resource_root(self,label,*args,**kwargs):
  return super().resource_root(label,*args,**kwargs)
 def run(self):
  row=super().run();need(not self.ld_live and all(not r['alive'] for r in self.ld_resources),'all current last_dialogue generations originally released');row.update(terminal_last_dialogue=self.ld_result,last_dialogue_cleanup=self.ld_cleanup,last_dialogue_resources_after_cleanup=copy.deepcopy(self.ld_resources),last_dialogue_GDI_lifetimes=self.ld_gdi_projection.report());return row

def source_contract():
 return dict(parent=parent.source_contract(),fixed_predecessor=fixed_parents(),branches={n:branch(n) for n in ('neutral_running','timeout_before_combat')},keyboard=KEYBOARD,raw_device_bytes=256,new_capture_cycle=True,captured_inputs=followup.parent.parent.input_contract(),first_confirmation_released=True,next_confirmation_released=False,forward_roots=[0x40DB90,0x40DC80,0x425DE0,0x454CF0],new_VM_or_handler_roots=0,derived_input_host_writes=0,PC_or_wait_host_writes=0,new_OS_input=False,draw_or_Present=False,new_rasters=list(RASTERS),helper=helper_contract(),experimental_capacity11_not_used_by_original_cases=True,extra_code=[],GDI_projection=dict(plan=lifetime_gdi.plan_reference(ROOT),opaque_handles_only=True,actual_API_payloads_unchanged=True,new_owned_lifetime_always_fresh_after_prefix=True,full_call_lifetimes='last_dialogue_GDI_lifetimes',ledger_semantics='latest lifetime per guest slot'),GPU_projection=dict(prefix_entries_unchanged=True,new_domains=list(PROJECTION_DOMAINS),domain_from_creation_layer_count=True,original_AddressSpace_algorithm=True,keys_per_new_generation=7,prefix_next_max=PREFIX_NEXT_MAX,new_start=GPU_GUEST_START,new_next_max=LAST_DIALOGUE_NEXT_MAX,disjoint_complete_before_mapping_span_required=True,GDI_guest_start=GDI_GUEST_START))

save_source=parent.save_source
def capacity_probe(out):
 need(not(ROOT/out).exists(),'fresh immutable capacity probe');contract=experimental_helper_contract();path,build=overlay.platform.build(ROOT/'tools/terminal_last_dialogue_d3d8_platform.cs','terminal-last-dialogue-capacity-gpu');gpu=overlay.platform.OverlayGPU(path);live=[];rejected=False
 try:
  need(gpu.hello['max_textures']==11 and gpu.hello['max_creates']==32 and gpu.hello['window_visible'] is False,'actual headless x86 capacity11 hello')
  for _ in range(11):live.append(gpu.create(1,1)['texture']['pointer'])
  need(len(set(live))==11,'eleven simultaneously live real textures')
  try:gpu.create(1,1)
  except ValueError as error:need('bounded multi texture capacity' in str(error),'twelfth texture refused by exact capacity guard');rejected=True
  need(rejected and gpu.trace[-1]['reply']['ok'] is False,'actual twelfth request rejected without owner death')
  for p in reversed(live):need(gpu.release(p)['count']==0,'actual capacity-probe final texture release')
  live.clear();cleanup=gpu.close();need(gpu.process.returncode==0 and cleanup['all_owned_resources_released'] and not cleanup['texture_releases'],'normal close without fallback texture releases')
  result=dict(schema_version=1,helper=contract,helper_build=build,actual_hello=gpu.hello,trace=gpu.trace,successful_simultaneous_creates=11,twelfth_create_refused=True,all_eleven_explicit_releases_zero=True,cleanup=cleanup,exit_code=gpu.process.returncode,normal_exit=True,original_VM_or_game_roots=0,isolated_platform_capacity_probe=True,new_OS_input=False)
  terminal.save(out,result);return result
 finally:
  if not gpu.closed:
   for p in reversed(live):gpu.release(p)
   gpu.close()

def run_case(c,ch,gh,ticks=None):
 fixed=fixed_parent_times()[c['name']];ticks=list(fixed) if ticks is None else ticks;need(ticks==fixed,'exact accepted original clock stream');instances=[]
 class Attached(LastDialogueMachine):
  def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);instances.append(self)
 class Diagnostics:
  @staticmethod
  def save(path,data):
   if instances:
    m=instances[0];data['last_dialogue']=dict(active=m.last_dialogue_active,segments=m.ld_segments,frames=m.ld_frames,leaves=m.ld_leaves,resources=m.ld_resources,bindings=m.ld_bindings,commands=m.ld_commands,replacements=m.ld_replacements,clears=m.ld_clears,CRT_trace=copy.deepcopy(m.live.trace),GPU_trace=copy.deepcopy(m.gpu.trace),GDI_trace=copy.deepcopy(m.name_platform.trace),GDI_lifetimes=m.ld_gdi_projection.report(),memory=m.snapshot(),trace=m.mark(),local_trace=m.ld_mark())
   save_source(path.replace('terminal-overlay-diagnostic-','terminal-last-dialogue-diagnostic-').replace('.json.gz','-20261029-'+str(time.time_ns())+'.json.gz'),data)
 fn=types.FunctionType(overlay.run_case.__code__,dict(overlay.run_case.__globals__,OverlayMachine=Attached,terminal=Diagnostics),closure=overlay.run_case.__closure__);return fn(c,ch,gh,ticks)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out');p.add_argument('--capacity-out');p.add_argument('--case',type=int);p.add_argument('--helper-prefix',default='terminal-last-dialogue');a=p.parse_args();need(bool(a.out)!=bool(a.capacity_out),'one original source output or isolated capacity output')
 if a.capacity_out:capacity_probe(a.capacity_out)
 else:
  need(not(ROOT/a.out).exists(),'fresh immutable last-dialogue source');fixed_parents();ch,gh,b=helpers(a.helper_prefix);rows=[]
  for c in (overlay.parent.corpus() if a.case is None else [overlay.parent.corpus()[a.case]]):rows.append(run_case(c,ch,gh));print('last_dialogue source',c['name'],'new confirmation held',flush=True)
  save_source(a.out,dict(schema_version=1,source_contract=source_contract(),helper_build=b,cases=rows,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False))
