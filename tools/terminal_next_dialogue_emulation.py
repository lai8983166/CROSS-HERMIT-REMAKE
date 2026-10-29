"""Original next layer4 dialogue and timeout role2 in the retained native lifetime."""
import argparse,copy,gzip,hashlib,json,struct,time,types
from functools import lru_cache
from tools import terminal_replacement_emulation as parent

ROOT,CODE,need,sha,terminal,MAIN,VM,STACK,RETURN,TASK,INPUT,MANAGER,KEYBOARD,overlay=(getattr(parent,n) for n in ('ROOT','CODE','need','sha','terminal','MAIN','VM','STACK','RETURN','TASK','INPUT','MANAGER','KEYBOARD','overlay'))
RANGES,ALLOWED,REFERENCE=parent.RANGES,parent.ALLOWED,parent.REFERENCE
EXTRA_RANGES=()
OBJECT=VM+0x430+4*0xAB8;NODE=VM+0x6F60+4*0xE0
TEXTURE=OBJECT+0x28;NAME_RECORD=NODE+0x60
RASTERS=(0x3EC00000,0x3ED00000);QUERIES=parent.QUERIES
PROJECTION_DOMAINS=('overlay-next-dialogue-name','overlay-next-dialogue-portrait','overlay-next-dialogue-text')
FOLLOWUP_POINTER_DOMAIN='overlay-followup-text-pointer'
FOLLOWUP_BITS_DOMAIN='overlay-followup-text-bits'
PROJECTION_STRIDE=parent.PROJECTION_STRIDE;PREFIX_NEXT_MAX=parent.REPLACEMENT_NEXT_MAX
NEXT_DIALOGUE_NEXT_MAX=PREFIX_NEXT_MAX+21*PROJECTION_STRIDE
GDI_GUEST_START=parent.GDI_GUEST_START
PARENT_ACCEPTANCE='analysis/terminal-replacement-acceptance-v1-20261028.json'
PARENT_ACCEPTANCE_SHA='c08c51bbcf42e9b47b806ec6c846da8e55492838752c57374a0bfe7969b11df5'
PARENT_SOURCE='analysis/terminal-replacement-source-v2-20261028.json.gz'
PARENT_SOURCE_SHA='5da2c1cb00c57102113e5310ec71a623f86ff31946d5350b81b508913c1c0abd'
PARENT_PROOF='analysis/terminal-replacement-proof-v2-20261028.json'
PARENT_PROOF_SHA='d336834093a4706efd11d68004acf58abb6e21ea649de051aecf641062899980'

@lru_cache(maxsize=1)
def fixed_parents():
 refs={k:parent.parent.parent.file_ref(p,h) for k,p,h in (('acceptance',PARENT_ACCEPTANCE,PARENT_ACCEPTANCE_SHA),('source',PARENT_SOURCE,PARENT_SOURCE_SHA),('proof',PARENT_PROOF,PARENT_PROOF_SHA))}
 a=json.loads((ROOT/PARENT_ACCEPTANCE).read_text(encoding='utf8'))
 need(a['source_report']==refs['source'] and a['independent_proof']==refs['proof'] and a['tasks_complete']==3 and a['boundaries']['VM_PC_per_case']==[230,226] and a['boundaries']['VM_wait']==1,'accepted complete layer7 replacement waiting boundary')
 return refs

def fixed_parent_times():return parent.fixed_parent_times()
def helper_contract():return parent.helper_contract()
def helpers(prefix='terminal-next-dialogue'):return parent.helpers(prefix)

@lru_cache(maxsize=1)
def fixed_parent_forward_summaries():
 raw=(ROOT/PARENT_PROOF).read_bytes();need(sha(raw)==PARENT_PROOF_SHA,'fixed replacement proof before prefix preflight')
 return {c['name']:c['forward_summary']['full_cumulative'] for c in json.loads(raw)['cases']}

def validate_parent_prefix(machine):
 name=machine.live_input['name'];expected=fixed_parent_forward_summaries()[name];actual=machine.mark()
 need(actual==expected,'fixed replacement forward prefix '+name+' expected='+repr(expected)+' actual='+repr(actual))
 print('next dialogue prefix preflight',name,actual,flush=True)
 return dict(case=name,fixed_proof_sha256=PARENT_PROOF_SHA,expected=expected,actual=actual)

def branch(name):
 need(name in ('neutral_running','timeout_before_combat'),'one original next dialogue branch');win=name=='neutral_running'
 return dict(first_PC=230 if win else 226,configuration=7,layer=4,object=OBJECT,node=NODE,role=None if win else 2,segment=2 if win else 11,text_index=5 if win else 7,text_PC=242 if win else 254,ready_PC=252 if win else 264,final_PC=256 if win else 268,scene_capture=76 if win else 77)

def projection_domain(kind):
 need(type(kind)is str and kind in ('name','portrait','text'),'one of three original next dialogue resource domains')
 return PROJECTION_DOMAINS[('name','portrait','text').index(kind)]

class FollowupPointerProjection:
 """Bind only the timeout's already-original FU text pointer by its lifetime.

 The accepted prefix allocated one new identity at this point. A native driver
 can reissue a retired interface address; the dedicated key preserves that
 allocation ordinal while all shared COM methods and surface bytes stay raw.
 """
 def __init__(self,machine):
  self.machine=machine;self.space=machine.space;self.original=self.space.result;self.bound=self.bits_bound=None
 def bind_bits(self,value,r):
  m=self.machine
  need(r['record']==parent.parent.OLD_TEXT_RECORD and r['label']=='followup_text' and r['alive'] and not r.get('lock') and not m.replacement_ready and not m.next_dialogue_ready and self.bound is not None and self.bound['native']==r['native_pointer'],'only first original timeout FU text LockRect')
  old=[q for q in m.fu_resources if q['label']=='text5'];need(len(old)==1,'one actual retired original text5 surface');old=old[0]
  need(old['kind']=='text' and old['record']==r['record'] and not old['alive'] and type(old['release_wire_index'])is int and old['release_wire_index']<r['create_wire_index'],'same-record prior text5 creation actually retired before new creation')
  release=m.gpu.trace[old['release_wire_index']];create=m.gpu.trace[r['create_wire_index']]
  need(release['request']['op']=='release' and release['request']['pointer']==old['native_pointer'] and release['reply']['result']['count']==0,'actual successful native release of retired text5')
  need(create['request']['op']=='create' and [create['request']['width'],create['request']['height']]==r['size']==old['size']==[128,32] and create['reply']['result']['texture']['pointer']==r['native_pointer'],'actual old and new identical original 128x32 surfaces')
  need(value['pitch']==old['lock']['pitch']==256 and len(bytes.fromhex(value['hex']))==len(bytes.fromhex(old['lock']['hex']))==8192 and type(value['bits'])is int and value['bits']>0,'actual equal whole 8192-byte native spans without payload normalization')
  guest=old['lock']['bits'];matches=[q for q in self.space.ledger() if q['guest']==guest]
  need(len(matches)==1 and matches[0]['domain']=='overlay' and self.space.guest_to_native.get(guest)==('overlay',matches[0]['native']),'one original retired overlay surface mapping')
  for q in m.fu_resources:
   if q['alive'] and q.get('lock'):
    start=q['lock']['bits'];end=start+len(bytes.fromhex(q['lock']['hex']))
    need(end<=guest or start>=guest+8192,'no alive original resource occupies retired guest surface span')
  key=(FOLLOWUP_BITS_DOMAIN,value['bits']);need(self.bits_bound is None and key not in self.space.native_to_guest,'one declared FU bits alias binding')
  self.space.native_to_guest[key]=guest;self.space.guest_to_native[guest]=key
  self.bits_bound=dict(domain=FOLLOWUP_BITS_DOMAIN,native=value['bits'],guest=guest,retired_surface_identity=dict(native=matches[0]['native']),retired_generation=old['generation'],record=r['record'],pitch=256,bytes=8192,size=[128,32],retired_release_wire_index=old['release_wire_index'],current_create_wire_index=r['create_wire_index'])
 def result(self,domain,value,key=None):
  m=self.machine;r=m.fu_current
  active=m.followup_active and m.live_input['name']=='timeout_before_combat' and r is not None and r['kind']=='text'
  if domain=='overlay' and key=='texture' and active:
   need(r['record']==parent.parent.OLD_TEXT_RECORD and r['label']=='followup_text' and not r.get('texture') and not m.replacement_ready and not m.next_dialogue_ready,'only original timeout FU layer5 text creation')
   need(self.bound is None and list(value)==['pointer','vtable','methods'] and type(value['pointer'])is int and value['pointer']>0,'one exact original FU text interface pointer')
   pointer=self.space.guest(FOLLOWUP_POINTER_DOMAIN,value['pointer']);self.bound=dict(domain=FOLLOWUP_POINTER_DOMAIN,native=value['pointer'],guest=pointer)
   rest={k:v for k,v in value.items() if k!='pointer'}
   return dict(pointer=pointer,**self.original(domain,rest,key))
  if domain=='overlay' and active and key is None and isinstance(value,dict) and 'bits' in value:self.bind_bits(value,r)
  if domain=='overlay' and active and key=='bits':
   need(self.bits_bound is not None and value==self.bits_bound['native'],'FU bits scalar belongs to the exact validated native lock')
   return self.bits_bound['guest']
  return self.original(domain,value,key)

def followup_pointer_prefix(machine,ledger):
 rows=[r for r in ledger if r['domain']==FOLLOWUP_POINTER_DOMAIN]
 bits=[r for r in ledger if r['domain']==FOLLOWUP_BITS_DOMAIN]
 expected=machine.live_input['name']=='timeout_before_combat'
 need(len(rows)==len(bits)==int(expected),'exact one timeout FU pointer/bits domain and none for victory')
 if expected:
  resource=next(r for r in machine.fu_resources if r['label']=='followup_text')
  need(rows==[dict(domain=FOLLOWUP_POINTER_DOMAIN,native=resource['native_pointer'],guest=resource['texture']['pointer'])],'FU pointer bridge belongs to the actual original creation')
  lock=next(c['native_result'] for c in resource['GPU_APIs'] if c['op']=='lock');guest=resource['lock']['bits'];old=next(r for r in machine.fu_resources if r['label']=='text5')
  need(bits==[dict(domain=FOLLOWUP_BITS_DOMAIN,native=lock['bits'],guest=guest)] and guest==old['lock']['bits'] and not old['alive'],'FU bits alias belongs only to its actually retired original surface')
  duplicates={g:[r for r in ledger if r['guest']==g] for g in {r['guest'] for r in ledger} if sum(r['guest']==g for r in ledger)>1}
  need(set(duplicates)=={guest} and len(duplicates[guest])==2 and {r['domain'] for r in duplicates[guest]}=={'overlay',FOLLOWUP_BITS_DOMAIN},'only the declared retired-surface alias may overlap guest identities')

class ReplacementProjection(parent.ReplacementProjection):
 """Retain the parent mapper, admitting exactly the audited FU pointer key."""
 def __init__(self,machine):
  self.machine=machine;self.space=machine.space;self.prefix=copy.deepcopy(self.space.ledger());self.prefix_next=self.space.next
  need(all(r['domain'] in ('overlay',FOLLOWUP_POINTER_DOMAIN,FOLLOWUP_BITS_DOMAIN) for r in self.prefix) and self.prefix_next<=parent.PREFIX_NEXT_MAX,'bounded unchanged predecessor GPU projection plus exact FU pointer and retired surface alias')
  followup_pointer_prefix(machine,self.prefix)

class NextDialogueProjection:
 """Keep both accepted domains; assign each new original creation its own key."""
 def __init__(self,machine):
  self.machine=machine;self.space=machine.space;self.prefix=copy.deepcopy(self.space.ledger());self.prefix_next=self.space.next
  need(all(r['domain'] in ('overlay',FOLLOWUP_POINTER_DOMAIN,FOLLOWUP_BITS_DOMAIN)+parent.PROJECTION_DOMAINS for r in self.prefix) and self.prefix_next<=PREFIX_NEXT_MAX,'bounded unchanged predecessor GPU projection')
  followup_pointer_prefix(machine,self.prefix)
 def result(self,domain,value,key=None):
  r=self.machine.nd_current
  need(domain=='overlay' and r is not None,'only current next dialogue GPU projection')
  target=projection_domain(r['kind']);record=NAME_RECORD if r['kind']=='name' else TEXTURE if r['kind']=='text' else self.machine.get(MAIN+0x844+30*8)
  need(r['record']==record and r['projection_domain']==target,'creation domain derives from original resource kind and record')
  result=self.space.result(target,value,key);rows=self.space.ledger();current=[x for x in rows if x['domain']==target]
  need(('texture' in value or 'bits' in value) and len(current)==(6 if 'texture' in value else 7),'six distinct interfaces and one whole-surface identity per new creation')
  need(rows[:len(self.prefix)]==self.prefix and self.space.next<=NEXT_DIALOGUE_NEXT_MAX<GDI_GUEST_START,'prefix identities preserved and new GPU mappings below GDI namespace')
  return result

def namespaced(fn):
 """Retain the original recorder code; route only new phase names and IPC."""
 def rename(n):
  if fn.__name__=='gpu_api' and n=='space':return 'nd_space'
  return 'nd_'+n[3:] if n.startswith('fu_') else 'next_dialogue_'+n[9:] if n.startswith('followup_') else n
 return types.FunctionType(fn.__code__.replace(co_names=tuple(rename(n) for n in fn.__code__.co_names)),fn.__globals__,fn.__name__,fn.__defaults__,fn.__closure__)

class NextDialogueMachine(parent.ReplacementMachine):
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.next_dialogue_active=self.next_dialogue_ready=self.next_dialogue_cleaning=False;self.next_dialogue_stop=None
  for n in ('segments','frames','leaves','commands','writes','queries','bindings','gpu','calls','conversions','resources','observers','cleanup','replacements','copy_rows'):setattr(self,'nd_'+n,[])
  self.nd_live={};self.nd_count=self.nd_write_count=0;self.nd_ih=hashlib.sha256();self.nd_wh=hashlib.sha256();self.nd_current=self.nd_pending_release=None
 _nd_parent_admission=types.FunctionType(parent.ReplacementMachine.admission.__code__,dict(parent.ReplacementMachine.admission.__globals__,ReplacementProjection=ReplacementProjection),closure=parent.ReplacementMachine.admission.__closure__)
 nd_mark=namespaced(parent.parent.FollowupMachine.fu_mark)
 nd_capture=namespaced(parent.parent.FollowupMachine.fu_capture)
 nd_prefix_counts=namespaced(parent.parent.FollowupMachine.fu_prefix_counts)
 nd_observe=namespaced(parent.parent.FollowupMachine.fu_observe)
 _nd_prepare=namespaced(parent.parent.FollowupMachine.fu_prepare)
 nd_gdi=namespaced(parent.parent.FollowupMachine.fu_gdi)
 nd_segment=namespaced(parent.parent.FollowupMachine.fu_segment)
 nd_frame=namespaced(parent.parent.FollowupMachine.fu_frame)
 nd_resume_frame=namespaced(parent.parent.FollowupMachine.fu_resume_frame)
 nd_font=namespaced(parent.parent.FollowupMachine.fu_font)
 nd_finish_resource=namespaced(parent.parent.FollowupMachine.fu_finish_resource)
 nd_actual_root=namespaced(parent.parent.FollowupMachine.fu_actual_root)
 _nd_captured=namespaced(parent.parent.FollowupMachine.fu_captured)
 _nd_gpu_api=namespaced(parent.parent.FollowupMachine.gpu_api)
 _nd_api_crt=namespaced(parent.parent.FollowupMachine.api_crt)
 def nd_prepare(self,*args,**kwargs):
  r=self._nd_prepare(*args,**kwargs);r['projection_domain']=projection_domain(r['kind']);return r
 def nd_captured(self,capture):
  row=self._nd_captured(capture);row['cycle']='next_dialogue_confirmation';return row
 def nd_set_raster(self,address):
  need(address in RASTERS,'finite distinct next dialogue real DIB destinations');service=self.name_platform.service;fn=service.call_raster
  service.call_raster=types.MethodType(types.FunctionType(fn.__func__.__code__,dict(fn.__func__.__globals__,RASTER=address)),service)
 def api_crt(self,slot):
  if not self.next_dialogue_ready:return super().api_crt(slot)
  return self._nd_api_crt(slot)
 def gpu_api(self,at):
  if not self.next_dialogue_ready:return super().gpu_api(at)
  self._nd_gpu_api(at);call=self.nd_gpu[-1]
  if call['op']=='release':
   for resources,live in ((self.nx_resources,self.nx_live),(self.fu_resources,self.fu_live)):
    for r in resources:
     if r['generation']==call['generation']:
      need(r['alive'] and r['record']==call['record'] and live.get(r['texture']['pointer']) is r,'exact same live predecessor generation released once')
      r.update(alive=False,release_wire_index=call['wire_index'],released_phase='next_dialogue_'+call['phase']);del live[r['texture']['pointer']]
 def write_hook(self,uc,access,at,size,value,context):
  super().write_hook(uc,access,at,size,value,context)
  if self.next_dialogue_active:
   if getattr(self,'nd_keyboard_fragment',False):need(KEYBOARD<=at and at+size<=KEYBOARD+0xA00 or STACK<=at and at+size<=STACK+0x20000,'finite original next dialogue keyboard writes')
   self.nd_write_count+=1;self.nd_wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
   if VM<=at<VM+0x9400 or KEYBOARD<=at<KEYBOARD+0xA00 or TASK<=at<TASK+0x190 or at==0:self.nd_writes.append(dict(pc=self.getreg('EIP'),address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))
 def code(self,uc,at,size,context):
  active=self.next_dialogue_active
  if active:
   if at==self.next_dialogue_stop:uc.emu_stop();return
   if self.nd_pending_release and at==self.nd_pending_release['caller'] and self.getreg('ESP')==self.nd_pending_release['return_ESP']:
    q=self.nd_pending_release;need(self.get(q['record']+44)==0 and not self.nd_resources[q['ledger_index']]['alive'],'original next dialogue destructor clears retired record');q['after']=self.nd_capture();q['GPU_APIs']=copy.deepcopy(self.nd_gpu[q.pop('GPU_start'):]);self.nd_replacements.append(q);self.nd_pending_release=None
   if at==0x403730:
    record=self.getreg('ECX');pointer=self.get(record+44);sp=self.getreg('ESP')
    if pointer in self.nd_live and self.get(sp)==0x4051AE:
     r=self.nd_live[pointer];need(self.nd_branch['role'] is None and record==TEXTURE and r['label']=='followup_text' and r['generation'] in self.nd_prefix_generations,'exact original old layer4 text generation replacement')
     self.nd_pending_release=dict(entry=at,caller=self.get(sp),return_ESP=sp+4,record=record,generation=r['generation'],ledger_index=self.nd_resources.index(r),before=self.nd_capture(),GPU_start=len(self.nd_gpu))
   if at==0x4CE9C5:
    p=self.get(VM+16)+self.get(VM+28);op,n=struct.unpack('<HH',self.read(p,4));need(self.get(VM+28)<self.nd_branch['final_PC'],'next dialogue successor remains unexecuted');self.nd_commands.append(dict(PC=self.get(VM+28),opcode=op,bytes=n,source_pointer=p))
   if at in overlay.parent.APIS and self.get(self.getreg('ESP'))==overlay.parent.APIS[at][2]:
    sp=self.getreg('ESP');ret=self.get(sp);first=len(self.task_APIs);super().code(uc,at,size,context);need(len(self.task_APIs)==first+1,'one actual next dialogue task leaf');r=self.task_APIs[-1];self.nd_leaves.append(dict(kind='TASK',call=dict(r,sp=sp,return_va=ret,pop=4,value=r['result'],memory_outputs=[],new_mappings=[])));return
   if at in self.gdi_targets:self.nd_gdi(at);return
   if at==0x405869:
    sp=self.getreg('ESP');args=[self.get(sp+j) for j in range(0,24,4)];self.nd_conversions.append(dict(entry=at,args=args,resource_label=self.nd_current['label'],record=self.nd_current['record'],rect=list(struct.unpack('<4I',self.read(args[4],16))),point=list(struct.unpack('<2I',self.read(args[5],8)))))
   if at==0x56D4D0 and self.get(self.getreg('ESP'))==0x40483F:
    sp=self.getreg('ESP');args=[self.get(sp+4+j) for j in (0,4,8)];i=len(self.nd_copy_rows);r=self.nd_current;need(r is not None and r['kind']=='portrait' and i<512 and args==[r['lock']['bits']+i*r['lock']['pitch'],self.nd_file_pointer+24+i*512,512],'all original new SC002 memcpy row arguments');self.nd_copy_rows.append(dict(row=i,args=args,caller=0x40483F))
   if at in QUERIES:
    sp=self.getreg('ESP');self.nd_queries.append(dict(entry=at,CPU=self.cpu(),receiver=self.getreg('ECX'),stack_hex=self.read(sp,68).hex(),selected_layer=self.get(VM+0x1CC,'B'),nodes={str(i):self.read(VM+0x6F60+i*0xE0,0xE0).hex() for i in (4,5,7)},objects={str(i):self.read(VM+0x430+i*0xAB8,0xAB8).hex() for i in (4,5,7)}))
  super().code(uc,at,size,context)
  if active and at in ALLOWED:self.nd_count+=1;self.nd_ih.update(struct.pack('<I',at))
 def nd_role(self):
  r=self.nd_prepare('name','next_dialogue_name4',NAME_RECORD,RASTERS[0]);self.nd_frame('role30_to_name_font',self.font_target);self.nd_font(r);self.nd_segment('new_name_texture_to_IMAGE',0x403BD0,0x4CDE10);r['completion']=self.nd_capture();sp=self.getreg('ESP');args=[self.get(sp+4),self.get(sp+8)];side=self.get(NODE+0x32,'B')
  pending=dict(entry=0x4CDE10,receiver=self.getreg('ECX'),caller=self.get(sp),args=args,CPU=self.cpu(),first_instruction_executed=False,node_hex=self.read(NODE,0xE0).hex(),group_words=[self.get(NODE+0x40,'H'),self.get(NODE+0x42,'H')],side_byte=side,side_pointer=NODE+0x32,side_getter=0x4CA9B0,path=self.string(args[0]).decode('ascii'))
  need(pending['receiver']==VM and pending['caller']==0x4CC0D2 and pending['group_words']==[30,31] and side==0 and args[1]==30 and pending['path']==self.nd_role_path,'actual original role2 side0 layer4 IMAGE slot30 and SC002 path');self.nd_image_group=args[1];self.nd_role_record=dict(role=2,configuration=7,node=NODE,name_record=NAME_RECORD,pending_image=pending,source=self.nd_role_source,name_resource_label=r['label']);self.nd_finish_resource(r)
  q=self.nd_prepare('portrait','portrait30',0);q['first_gpu']=len(self.nd_gpu);q['first_leaf']=len(self.nd_leaves);self.nd_segment('new_SC002_file_and_constructor',0x4CDE10,0x403BD0);q['record']=self.get(MAIN+0x844+30*8);read_api=next(x['call'] for x in self.nd_leaves[q['first_leaf']:] if x['kind']=='CRT' and x['call']['name']=='ReadFile');self.nd_file_pointer=read_api['args'][1];need(self.read(self.nd_file_pointer,len(self.nd_asset))==self.nd_asset,'complete actual original SC002 file')
  native=[]
  for p,b in self.crt.allocations.items():
   if p<=self.nd_file_pointer<p+b['bytes'] or p<=q['record']<p+b['bytes']:
    self.crt.sync(p);reply=self.live.request('readback',pointer=b['native']);need(reply['hex']==self.read(p,b['bytes']).hex(),'actual entire new SC002/vector native buffer');native.append(dict(guest=p,bytes=b['bytes'],wire_index=len(self.live.trace)-1,result=reply))
  q['constructed']=dict(self.nd_capture(),file_pointer=self.nd_file_pointer,file_hex=self.nd_asset.hex(),record=q['record'],record_hex=self.read(q['record'],84).hex(),bank_hex=self.read(MAIN+0x844+30*8,8).hex(),native_allocation_readbacks=native,allocations=copy.deepcopy(self.crt.allocations));self.nd_segment('new_SC002_pixels_free_IMAGE_return',0x403BD0,0x4CC0D2);q['image_return']=self.nd_capture();q['copy_rows']=copy.deepcopy(self.nd_copy_rows);need(len(q['copy_rows'])==512,'all new SC002 rows originally copied');self.nd_segment('new_role_handler_complete_task',0x4CC0D2);q['completion']=self.nd_capture();self.nd_finish_resource(q);self.nd_resume_frame('role30_complete',lambda:None)
  need(self.get(VM+28)==246,'original role30 advances full twenty-byte command')
  readiness_frames=0
  for _ in range(200):
   if self.get(VM+32,'H')==0:break
   self.nd_frame('role_readiness');readiness_frames+=1;need(self.get(VM+28)==246,'only original role2 readiness before246')
  else:raise ValueError('bounded new layer4 original role2 readiness')
  need(readiness_frames==77,'all seventy-seven original role2 readiness tasks');self.nd_role_record.update(ready=self.nd_capture(),readiness_frames=readiness_frames);self.nd_frame('select_layer4');need(self.get(VM+28)==254 and self.get(VM+0x1CC,'B')==4,'original config7 selects layer4')
 def nd_text(self):
  b=self.nd_branch;r=self.nd_prepare('text','next_dialogue_text',TEXTURE,RASTERS[1]);r.update(text_index=b['text_index'],PC=b['text_PC'],object=OBJECT,node=NODE,record_index=0)
  need(self.get(OBJECT+22,'H')==0 and self.get(VM+28)==b['text_PC'],'original cleared or new layer4 text count and PC');self.nd_frame('text_to_font',self.font_target);self.nd_font(r);self.nd_segment('next_dialogue_text_pixels_handler_complete_task',0x403BD0);r['completion']=self.nd_capture();need(self.get(VM+28)==b['text_PC']+6 and self.get(OBJECT+22,'H')==1,'original full next dialogue text task and count');self.nd_finish_resource(r);self.nd_resume_frame('next_dialogue_text_complete',lambda:None)
 def admission(self):
  self.nd_followup_pointer_projection=FollowupPointerProjection(self);self.space.result=self.nd_followup_pointer_projection.result
  a=self._nd_parent_admission();self.nd_prefix_preflight=validate_parent_prefix(self);self.nd_branch=branch(self.live_input['name']);self.nd_prefix=self.nd_prefix_counts();self.nd_before=self.nd_capture();need((self.get(VM+28),self.get(VM+32,'H'))==(self.nd_branch['first_PC'],1),'accepted complete replacement waiting boundary')
  self.nd_resources=copy.deepcopy(self.nx_resources);self.nd_prefix_generations={r['generation'] for r in self.nd_resources};self.nd_live={r['texture']['pointer']:r for r in self.nd_resources if r['alive']};self.nd_resources_before=copy.deepcopy(self.nd_resources)
  need(len(self.nd_resources)==10 and len(self.nd_live)==(9 if self.nd_branch['role'] is None else 7),'complete ten predecessor creation generations');self.nd_space=NextDialogueProjection(self)
  end=len(self.nx_leaves);self.nx_cleanup.append(dict(label='forward_leaf_end_only',leaves=[end,end]));self.next_dialogue_ready=self.next_dialogue_active=self.active_overlay=True
  if self.nd_branch['role'] is not None:
   catalog,_=parent.parent.source_names();self.nd_role_source=catalog['roles']['2'];self.nd_role_path='data\\adv\\bin\\'+self.nd_role_source['filename'];self.nd_asset=(ROOT/self.nd_role_source['image_path']).read_bytes();need(sha(self.nd_asset)==self.nd_role_source['image_sha256'],'fixed actual SC002');self.nd_role_container=parent.parent.parse(self.nd_asset)
  stream=parent.parent.parent.parent.input_contract()['streams'][str(self.nd_branch['scene_capture'])];self.nd_captured(stream['captures'][0])
  for _ in range(2):
   self.nd_frame('held_parent_confirmation');need((self.get(VM+28),self.get(VM+32,'H'),self.get(KEYBOARD+0x4B9,'B'))==(self.nd_branch['first_PC'],1,0),'idle keeps replacement confirmation')
  self.nd_captured(stream['captures'][1]);self.nd_frame('captured_press');need((self.get(VM+28),self.get(VM+32,'H'),self.get(KEYBOARD+0x4B9,'B'))==(self.nd_branch['first_PC'],0,128),'complete task consumes next dialogue press');confirmed=self.nd_capture();self.nd_captured(stream['captures'][2]);need(self.get(KEYBOARD+0x4B9,'B')==0,'original next dialogue release')
  clear=None
  if self.nd_branch['role'] is not None:self.nd_role()
  else:
   self.nd_frame('select_layer4');need(self.get(VM+28)==238 and self.get(VM+0x1CC,'B')==4,'original config7 selects layer4');before=self.nd_capture();wire=len(self.gpu.trace);old=self.get(TEXTURE+44);self.nd_frame('clear_layer4_text');need(self.get(VM+28)==242 and self.get(OBJECT+22,'H')==0 and len(self.gpu.trace)==wire and self.get(TEXTURE+44)==old,'original44 clears count and retains old layer4 texture');clear=dict(before=before,after=self.nd_capture(),GPU_wire_before=wire,GPU_wire_after=len(self.gpu.trace))
  self.nd_text()
  for _ in range(100):
   self.nd_frame('text_readiness');need(self.get(VM+28)==self.nd_branch['ready_PC'],'only original50 before next dialogue confirmation')
   if self.get(VM+32,'H')==0:break
  else:raise ValueError('bounded original next dialogue readiness')
  ready=self.nd_capture();self.nd_frame('enter_new_confirmation');need((self.get(VM+28),self.get(VM+32,'H'))==(self.nd_branch['final_PC'],1),'natural next dialogue confirmation');confirmation=self.nd_capture()
  for _ in range(2):
   self.nd_frame('held_new_confirmation');need((self.get(VM+28),self.get(VM+32,'H'),self.get(KEYBOARD+0x4B9,'B'))==(self.nd_branch['final_PC'],1,0),'two complete tasks hold next dialogue confirmation')
  final=self.nd_capture();observations=self.nd_observe('final');self.next_dialogue_active=self.active_overlay=False
  for r in self.nd_resources:r['alive_after_forward']=r['alive']
  need(len(self.nd_resources)==(11 if self.nd_branch['role'] is None else 13) and len(self.nd_replacements)==(1 if self.nd_branch['role'] is None else 0),'exact new resource creations and original old layer4 replacement')
  self.nd_result=dict(prefix=self.nd_prefix,prefix_preflight=self.nd_prefix_preflight,historical_surface_alias=copy.deepcopy(self.nd_followup_pointer_projection.bits_bound),before=self.nd_before,branch=self.nd_branch,resources_before=self.nd_resources_before,resources=copy.deepcopy(self.nd_resources),bindings=self.nd_bindings,confirmed=confirmed,clear=clear,role=copy.deepcopy(getattr(self,'nd_role_record',None)),role_container=getattr(self,'nd_role_container',None),ready=ready,confirmation=confirmation,final=final,segments=self.nd_segments,frames=self.nd_frames,leaves=self.nd_leaves,commands=self.nd_commands,writes=self.nd_writes,queries=self.nd_queries,replacements=self.nd_replacements,GPU_APIs=self.nd_gpu,calls=self.nd_calls,conversions=self.nd_conversions,readbacks=observations,readback_observers=self.nd_observers,GDI_trace=copy.deepcopy(self.name_platform.trace[self.nd_prefix['GDI_trace']:]),GDI_handle_projection=self.name_platform.space.ledger(),accounting=self.get(0x765720),forward_wire_end=len(self.gpu.trace),CRT_forward_wire_end=len(self.live.trace),GPU_projection_before=dict(next=self.nd_space.prefix_next,ledger=self.nd_space.prefix),GPU_projection=[r for r in self.space.ledger() if r['domain'] in PROJECTION_DOMAINS])
  return a
 def fu_actual_root(self,*args,**kwargs):
  if not self.next_dialogue_ready:return super().fu_actual_root(*args,**kwargs)
  return self.nd_actual_root(*args,**kwargs)
 def nx_actual_root(self,*args,**kwargs):
  if not self.next_dialogue_ready:return super().nx_actual_root(*args,**kwargs)
  return self.nd_actual_root(*args,**kwargs)
 def resource_root(self,label,*args,**kwargs):
  if self.next_dialogue_ready and label=='supplemental_original_group20_destructor' and self.nd_branch['role'] is not None:
   self.nd_actual_root('supplemental_original_next_dialogue_text_destructor',0x403730,receiver=TEXTURE)
   self.nd_actual_root('supplemental_original_next_dialogue_portrait_container_destructor',0x41F4E0,[30],MAIN+0x844)
   self.nd_actual_root('supplemental_original_next_dialogue_name_destructor',0x403730,receiver=NAME_RECORD)
  return super().resource_root(label,*args,**kwargs)
 def run(self):
  row=super().run();need(not self.nd_live and all(not r['alive'] for r in self.nd_resources),'all next dialogue generations actually originally released')
  row.update(terminal_next_dialogue=self.nd_result,next_dialogue_cleanup=self.nd_cleanup,next_dialogue_resources_after_cleanup=copy.deepcopy(self.nd_resources));return row

def source_contract():
 return dict(parent=parent.source_contract(),fixed_predecessor=fixed_parents(),branches={n:branch(n) for n in ('neutral_running','timeout_before_combat')},keyboard=KEYBOARD,raw_device_offset=12,raw_device_bytes=256,new_capture_cycle=True,captured_inputs=parent.parent.parent.parent.input_contract(),first_confirmation_released=True,next_confirmation_released=False,forward_roots=[0x40DB90,0x40DC80,0x425DE0,0x454CF0],new_VM_or_handler_roots=0,derived_input_host_writes=0,PC_or_wait_host_writes=0,new_OS_input=False,draw_or_Present=False,new_rasters=list(RASTERS),helper=helper_contract(),extra_code=[],GPU_projection=dict(prefix_domains=['overlay',FOLLOWUP_POINTER_DOMAIN,FOLLOWUP_BITS_DOMAIN]+list(parent.PROJECTION_DOMAINS),prefix_entries_unchanged_after_declared_historical_bridge=True,new_domains=list(PROJECTION_DOMAINS),domain_from_resource_kind_and_record=True,original_AddressSpace_algorithm_for_new_generations=True,keys_per_new_generation=dict(texture=1,vtable=1,methods=4,bits=1,total=7),guest_stride=PROJECTION_STRIDE,prefix_next_max=PREFIX_NEXT_MAX,new_next_max=NEXT_DIALOGUE_NEXT_MAX,GDI_guest_start=GDI_GUEST_START),historical_pointer_bridge=dict(branch='timeout_before_combat',phase='followup',kind='text',label='followup_text',record=parent.parent.OLD_TEXT_RECORD,domain=FOLLOWUP_POINTER_DOMAIN,identities=1,only_texture_pointer=True,shared_vtable_methods_domain='overlay',original_AddressSpace_guest_algorithm=True,native_payload_unchanged=True,fixed_parent_guest_memory_CPU_trace_unchanged=True),historical_surface_alias=dict(branch='timeout_before_combat',phase='followup',kind='text',label='followup_text',retired_label='text5',record=parent.parent.OLD_TEXT_RECORD,domain=FOLLOWUP_BITS_DOMAIN,old_domain='overlay',size=[128,32],pitch=256,bytes=8192,identities=1,explicit_retired_guest_span_reuse=True,original_guest_new_allocation_algorithm=False,guest_next_increment=0,actual_original_release_required=True,no_other_live_span=True,only_declared_guest_identity_overlap=True,native_payload_unchanged=True),prefix_preflight=dict(fixed_proof=PARENT_PROOF,fixed_proof_sha256=PARENT_PROOF_SHA,full_cumulative=True,before_next_dialogue=True))

def save_source(path,data):
 p=ROOT/path;need(not p.exists(),'fresh next dialogue source path');encoder=json.JSONEncoder(ensure_ascii=False,separators=(',',':'))
 with p.open('xb') as output:
  if p.suffix=='.gz':
   with gzip.GzipFile(fileobj=output,mode='wb',filename='',mtime=0,compresslevel=6) as compressed:
    for block in encoder.iterencode(data):compressed.write(block.encode('utf8'))
    compressed.write(b'\n')
  else:
   for block in encoder.iterencode(data):output.write(block.encode('utf8'))
   output.write(b'\n')

def run_case(c,ch,gh,ticks=None):
 fixed=fixed_parent_times()[c['name']]
 if ticks is None:ticks=list(fixed)
 need(ticks==fixed,'exact frozen original clock stream');instances=[]
 class Attached(NextDialogueMachine):
  def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);instances.append(self)
 class Diagnostics:
  @staticmethod
  def save(path,data):
   if instances:
    m=instances[0];data['next_dialogue']=dict(active=m.next_dialogue_active,segments=m.nd_segments,frames=m.nd_frames,leaves=m.nd_leaves,resources=m.nd_resources,bindings=m.nd_bindings,commands=m.nd_commands,queries=m.nd_queries,replacements=m.nd_replacements,CRT_trace=copy.deepcopy(m.live.trace),GPU_trace=copy.deepcopy(m.gpu.trace),GDI_trace=copy.deepcopy(m.name_platform.trace),readback_observers=m.nd_observers,memory=m.snapshot(),trace=m.mark(),local_trace=m.nd_mark())
   path=path.replace('terminal-overlay-diagnostic-','terminal-next-dialogue-diagnostic-').replace('.json.gz','-20261028-'+str(time.time_ns())+'.json.gz')
   save_source(path,data)
 fn=types.FunctionType(overlay.run_case.__code__,dict(overlay.run_case.__globals__,OverlayMachine=Attached,terminal=Diagnostics),closure=overlay.run_case.__closure__)
 return fn(c,ch,gh,ticks)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case',type=int);p.add_argument('--helper-prefix',default='terminal-next-dialogue');a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable next dialogue report');fixed_parents();fixed_parent_times();ch,gh,b=helpers(a.helper_prefix);rows=[]
 for c in (overlay.parent.corpus() if a.case is None else [overlay.parent.corpus()[a.case]]):rows.append(run_case(c,ch,gh));print('next dialogue source',c['name'],'new confirmation held',flush=True)
 save_source(a.out,dict(schema_version=1,source_contract=source_contract(),helper_build=b,cases=rows,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False))
