"""Original layer7 two-line terminal replacement in the retained native lifetime."""
import argparse,copy,gzip,hashlib,json,struct,time,types
from functools import lru_cache
from tools import terminal_followup_emulation as parent

ROOT,CODE,need,sha,terminal,MAIN,VM,STACK,RETURN,TASK,INPUT,MANAGER,KEYBOARD,overlay=(getattr(parent,n) for n in ('ROOT','CODE','need','sha','terminal','MAIN','VM','STACK','RETURN','TASK','INPUT','MANAGER','KEYBOARD','overlay'))
RANGES,ALLOWED,REFERENCE=parent.RANGES,parent.ALLOWED,parent.REFERENCE
EXTRA_RANGES=()
OBJECT=VM+0x430+7*0xAB8;NODE=VM+0x6F60+7*0xE0
TEXTURE=OBJECT+0x28;STRIDE=0x110
RASTERS=(0x3EA00000,0x3EB00000);QUERIES=parent.QUERIES
PROJECTION_DOMAINS=('overlay-replacement-0','overlay-replacement-1')
PROJECTION_STRIDE=0x100000;PREFIX_NEXT_MAX=0x65801000
REPLACEMENT_NEXT_MAX=PREFIX_NEXT_MAX+14*PROJECTION_STRIDE
GDI_GUEST_START=0x6A001000
PARENT_ACCEPTANCE='analysis/terminal-followup-acceptance-v1-20261027.json'
PARENT_ACCEPTANCE_SHA='86bb1ed313febc97a715bad7e530335e79a0ea7f527ac28e543274ad0d0ebc5f'
PARENT_SOURCE='analysis/terminal-followup-source-v1-20261027.json.gz'
PARENT_SOURCE_SHA='c46d21d7064224e29de0f25a539dac92f23eecf407c26c4f20df14cac2268779'
PARENT_PROOF='analysis/terminal-followup-proof-v1-20261027.json'
PARENT_PROOF_SHA='94f34f76e60c3eb3f10d9cfefda14c942c10dba4007b883981cf83fc117beb25'

@lru_cache(maxsize=1)
def fixed_parents():
 refs={k:parent.parent.file_ref(p,h) for k,p,h in (('acceptance',PARENT_ACCEPTANCE,PARENT_ACCEPTANCE_SHA),('source',PARENT_SOURCE,PARENT_SOURCE_SHA),('proof',PARENT_PROOF,PARENT_PROOF_SHA))}
 a=json.loads((ROOT/PARENT_ACCEPTANCE).read_text(encoding='utf8'))
 need(a['source_report']==refs['source'] and a['independent_proof']==refs['proof'] and a['tasks_complete']==3 and a['boundaries']['VM_PC_per_case']==[198,194] and a['boundaries']['VM_wait']==1,'accepted complete followup waiting boundary')
 return refs

def fixed_parent_times():return parent.fixed_parent_times()
def helper_contract():return parent.helper_contract()
def helpers(prefix='terminal-replacement'):return parent.helpers(prefix)

def branch(name):
 need(name in ('neutral_running','timeout_before_combat'),'one original terminal replacement branch')
 win=name=='neutral_running';start=198 if win else 194
 return dict(first_PC=start,configuration=4,layer=7,object=OBJECT,node=NODE,role=None,segment=2 if win else 11,text_indices=[3,4] if win else [5,6],text_PCs=[start+12,start+18],ready_PC=start+28,final_PC=start+32,scene_capture=76 if win else 77)

def projection_domain(index):
 need(type(index)is int and 0<=index<2,'one of two original replacement resource domains')
 return PROJECTION_DOMAINS[index]

class ReplacementProjection:
 """Route only new GPU IPC identities through one domain per creation.

 The original AddressSpace still performs all typed marshaling. Native payloads
 and the frozen prefix's identities are untouched, including retired mappings.
 """
 def __init__(self,machine):
  self.machine=machine;self.space=machine.space;self.prefix=copy.deepcopy(self.space.ledger());self.prefix_next=self.space.next
  need(all(r['domain']=='overlay' for r in self.prefix) and self.prefix_next<=PREFIX_NEXT_MAX,'bounded unchanged predecessor GPU projection')
 def result(self,domain,value,key=None):
  r=self.machine.nx_current
  need(domain=='overlay' and r is not None and r['kind']=='text','only current new replacement text GPU projection')
  index=r['record_index'];target=projection_domain(index)
  need(r['record']==TEXTURE+index*STRIDE and r['projection_domain']==target,'creation domain derives from original ordered record')
  result=self.space.result(target,value,key)
  rows=self.space.ledger();current=[x for x in rows if x['domain']==target]
  expected=6 if 'texture' in value else 7
  need(('texture' in value or 'bits' in value) and len(current)==expected,'six distinct interface identities and one whole-surface bits identity per new creation')
  need(rows[:len(self.prefix)]==self.prefix and self.space.next<=REPLACEMENT_NEXT_MAX<GDI_GUEST_START,'prefix identities preserved and new GPU mappings remain below GDI namespace')
  return result

def namespaced(fn):
 """Retain host bytecode/constants; route recorder names and new GPU IPC."""
 def rename(n):
  if fn.__name__=='gpu_api' and n=='space':return 'nx_space'
  return 'nx_'+n[3:] if n.startswith('fu_') else 'replacement_'+n[9:] if n.startswith('followup_') else n
 code=fn.__code__.replace(co_names=tuple(rename(n) for n in fn.__code__.co_names))
 return types.FunctionType(code,fn.__globals__,fn.__name__,fn.__defaults__,fn.__closure__)

class ReplacementMachine(parent.FollowupMachine):
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.replacement_active=self.replacement_ready=self.replacement_cleaning=False;self.replacement_stop=None
  for n in ('segments','frames','leaves','commands','writes','queries','bindings','gpu','calls','conversions','resources','observers','cleanup','replacements','copy_rows'):setattr(self,'nx_'+n,[])
  self.nx_live={};self.nx_count=self.nx_write_count=0;self.nx_ih=hashlib.sha256();self.nx_wh=hashlib.sha256();self.nx_current=self.nx_pending_release=None
 nx_mark=namespaced(parent.FollowupMachine.fu_mark)
 nx_capture=namespaced(parent.FollowupMachine.fu_capture)
 nx_prefix_counts=namespaced(parent.FollowupMachine.fu_prefix_counts)
 nx_observe=namespaced(parent.FollowupMachine.fu_observe)
 nx_prepare=namespaced(parent.FollowupMachine.fu_prepare)
 nx_gdi=namespaced(parent.FollowupMachine.fu_gdi)
 nx_segment=namespaced(parent.FollowupMachine.fu_segment)
 nx_frame=namespaced(parent.FollowupMachine.fu_frame)
 nx_resume_frame=namespaced(parent.FollowupMachine.fu_resume_frame)
 nx_font=namespaced(parent.FollowupMachine.fu_font)
 nx_finish_resource=namespaced(parent.FollowupMachine.fu_finish_resource)
 nx_actual_root=namespaced(parent.FollowupMachine.fu_actual_root)
 _nx_captured=namespaced(parent.FollowupMachine.fu_captured)
 _nx_gpu_api=namespaced(parent.FollowupMachine.gpu_api)
 _nx_api_crt=namespaced(parent.FollowupMachine.api_crt)
 def nx_captured(self,capture):
  row=self._nx_captured(capture);row['cycle']='replacement_confirmation';return row
 def nx_set_raster(self,address):
  need(address in RASTERS,'finite distinct replacement real DIB destinations');service=self.name_platform.service;fn=service.call_raster
  service.call_raster=types.MethodType(types.FunctionType(fn.__func__.__code__,dict(fn.__func__.__globals__,RASTER=address)),service)
 def api_crt(self,slot):
  if not self.replacement_ready:return super().api_crt(slot)
  return self._nx_api_crt(slot)
 def gpu_api(self,at):
  if not self.replacement_ready:return super().gpu_api(at)
  self._nx_gpu_api(at)
  call=self.nx_gpu[-1]
  if call['op']=='release':
   # The predecessor still owns its private generation ledger. Synchronize only
   # the same creation, never a later allocation reusing the pointer/record.
   for r in self.fu_resources:
    if r['generation']==call['generation']:
     need(r['alive'] and self.fu_live.get(r['texture']['pointer']) is r,'same live predecessor creation released once')
     r.update(alive=False,release_wire_index=call['wire_index'],released_phase='replacement_'+call['phase']);del self.fu_live[r['texture']['pointer']]
 def write_hook(self,uc,access,at,size,value,context):
  super().write_hook(uc,access,at,size,value,context)
  if self.replacement_active:
   if getattr(self,'nx_keyboard_fragment',False):need(KEYBOARD<=at and at+size<=KEYBOARD+0xA00 or STACK<=at and at+size<=STACK+0x20000,'finite original replacement keyboard writes')
   self.nx_write_count+=1;self.nx_wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
   if VM<=at<VM+0x9400 or KEYBOARD<=at<KEYBOARD+0xA00 or TASK<=at<TASK+0x190 or at==0:self.nx_writes.append(dict(pc=self.getreg('EIP'),address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))
 def code(self,uc,at,size,context):
  active=self.replacement_active
  if active:
   if at==self.replacement_stop:uc.emu_stop();return
   if self.nx_pending_release and at==self.nx_pending_release['caller'] and self.getreg('ESP')==self.nx_pending_release['return_ESP']:
    q=self.nx_pending_release;need(self.get(q['record']+44)==0 and not self.nx_resources[q['ledger_index']]['alive'],'original replacement destructor clears retired record');q['after']=self.nx_capture();q['GPU_APIs']=copy.deepcopy(self.nx_gpu[q.pop('GPU_start'):]);self.nx_replacements.append(q);self.nx_pending_release=None
   if at==0x403730:
    record=self.getreg('ECX');pointer=self.get(record+44);sp=self.getreg('ESP')
    if pointer in self.nx_live and self.get(sp)==0x4051AE:
     r=self.nx_live[pointer];current=self.nx_current
     need(current is not None and record==current['record'] and record in (TEXTURE,TEXTURE+STRIDE) and r['generation'] in self.nx_prefix_generations and r['label']=='text7_'+str(current['record_index']+1),'exact original layer7 old creation replacement')
     self.nx_pending_release=dict(entry=at,caller=self.get(sp),return_ESP=sp+4,record=record,generation=r['generation'],ledger_index=self.nx_resources.index(r),before=self.nx_capture(),GPU_start=len(self.nx_gpu))
   if at==0x4CE9C5:
    p=self.get(VM+16)+self.get(VM+28);op,n=struct.unpack('<HH',self.read(p,4));need(self.get(VM+28)<self.nx_branch['final_PC'],'next replacement successor stays unexecuted');self.nx_commands.append(dict(PC=self.get(VM+28),opcode=op,bytes=n,source_pointer=p))
   if at in overlay.parent.APIS and self.get(self.getreg('ESP'))==overlay.parent.APIS[at][2]:
    sp=self.getreg('ESP');ret=self.get(sp);first=len(self.task_APIs);super().code(uc,at,size,context);need(len(self.task_APIs)==first+1,'one actual replacement task leaf');r=self.task_APIs[-1];self.nx_leaves.append(dict(kind='TASK',call=dict(r,sp=sp,return_va=ret,pop=4,value=r['result'],memory_outputs=[],new_mappings=[])));return
   if at in self.gdi_targets:self.nx_gdi(at);return
   if at==0x405869:
    sp=self.getreg('ESP');args=[self.get(sp+j) for j in range(0,24,4)];self.nx_conversions.append(dict(entry=at,args=args,resource_label=self.nx_current['label'],record=self.nx_current['record'],rect=list(struct.unpack('<4I',self.read(args[4],16))),point=list(struct.unpack('<2I',self.read(args[5],8)))))
   if at in QUERIES:
    sp=self.getreg('ESP');self.nx_queries.append(dict(entry=at,CPU=self.cpu(),receiver=self.getreg('ECX'),stack_hex=self.read(sp,68).hex(),selected_layer=self.get(VM+0x1CC,'B'),nodes={str(i):self.read(VM+0x6F60+i*0xE0,0xE0).hex() for i in (4,5,7)},objects={str(i):self.read(VM+0x430+i*0xAB8,0xAB8).hex() for i in (4,5,7)}))
  super().code(uc,at,size,context)
  if active and at in ALLOWED:self.nx_count+=1;self.nx_ih.update(struct.pack('<I',at))
 def nx_text(self,index):
  b=self.nx_branch;pc=b['text_PCs'][index];record=TEXTURE+index*STRIDE
  need(self.get(VM+28)==pc and self.get(OBJECT+22,'H')==index,'ordered original replacement text count and PC')
  r=self.nx_prepare('text','replacement_text_'+str(index),record,RASTERS[index]);r.update(text_index=b['text_indices'][index],PC=pc,object=OBJECT,node=NODE,record_index=index,projection_domain=projection_domain(index))
  self.nx_frame('replacement_text_to_font',self.font_target);self.nx_font(r);self.nx_segment('replacement_text_pixels_handler_complete_task',0x403BD0);r['completion']=self.nx_capture()
  need(self.get(VM+28)==pc+6 and self.get(OBJECT+22,'H')==index+1,'original replacement append and complete task')
  self.nx_finish_resource(r);self.nx_resume_frame('replacement_text_complete',lambda:None)
 def admission(self):
  a=super().admission();self.nx_branch=branch(self.live_input['name']);self.nx_prefix=self.nx_prefix_counts();self.nx_before=self.nx_capture()
  need((self.get(VM+28),self.get(VM+32,'H'))==(self.nx_branch['first_PC'],1),'accepted complete followup waiting boundary')
  self.nx_resources=copy.deepcopy(self.fu_resources)
  self.nx_prefix_generations={r['generation'] for r in self.nx_resources}
  self.nx_live={r['texture']['pointer']:r for r in self.nx_resources if r['alive']};self.nx_resources_before=copy.deepcopy(self.nx_resources)
  need(len(self.nx_resources)==8 and len(self.nx_live)==(8 if self.live_input['name']=='neutral_running' else 7),'complete eight predecessor generations')
  self.nx_space=ReplacementProjection(self)
  # This is a forward interval marker only. It claims no old cleanup CPU/hash.
  end=len(self.fu_leaves);self.fu_cleanup.append(dict(label='forward_leaf_end_only',leaves=[end,end]))
  self.replacement_ready=self.replacement_active=self.active_overlay=True
  stream=parent.parent.parent.input_contract()['streams'][str(self.nx_branch['scene_capture'])];self.nx_captured(stream['captures'][0])
  for _ in range(2):
   self.nx_frame('held_parent_confirmation');need((self.get(VM+28),self.get(VM+32,'H'),self.get(KEYBOARD+0x4B9,'B'))==(self.nx_branch['first_PC'],1,0),'idle keeps followup confirmation')
  self.nx_captured(stream['captures'][1]);self.nx_frame('captured_press');need((self.get(VM+28),self.get(VM+32,'H'),self.get(KEYBOARD+0x4B9,'B'))==(self.nx_branch['first_PC'],0,128),'complete task consumes replacement press');confirmed=self.nx_capture();self.nx_captured(stream['captures'][2]);need(self.get(KEYBOARD+0x4B9,'B')==0,'original replacement release')
  self.nx_frame('select_layer7');need(self.get(VM+28)==self.nx_branch['first_PC']+8 and self.get(VM+0x1CC,'B')==7,'original config4 selects layer7')
  before=self.nx_capture();wire=len(self.gpu.trace);old=[self.get(TEXTURE+i*STRIDE+44) for i in range(3)];self.nx_frame('clear_layer7_text')
  need(self.get(VM+28)==self.nx_branch['text_PCs'][0] and self.get(OBJECT+22,'H')==0 and len(self.gpu.trace)==wire and [self.get(TEXTURE+i*STRIDE+44) for i in range(3)]==old,'original44 clears count while retaining every old texture')
  clear=dict(before=before,after=self.nx_capture(),GPU_wire_before=wire,GPU_wire_after=len(self.gpu.trace))
  for i in range(2):self.nx_text(i)
  for _ in range(100):
   self.nx_frame('text_readiness');need(self.get(VM+28)==self.nx_branch['ready_PC'],'only original50 before replacement confirmation')
   if self.get(VM+32,'H')==0:break
  else:raise ValueError('bounded original replacement readiness')
  ready=self.nx_capture();self.nx_frame('enter_new_confirmation');need((self.get(VM+28),self.get(VM+32,'H'))==(self.nx_branch['final_PC'],1),'natural replacement confirmation');confirmation=self.nx_capture()
  for _ in range(2):
   self.nx_frame('held_new_confirmation');need((self.get(VM+28),self.get(VM+32,'H'),self.get(KEYBOARD+0x4B9,'B'))==(self.nx_branch['final_PC'],1,0),'two complete tasks hold replacement confirmation')
  final=self.nx_capture();observations=self.nx_observe('final');self.replacement_active=self.active_overlay=False
  for r in self.nx_resources:r['alive_after_forward']=r['alive']
  need(len(self.nx_resources)==10 and len(self.nx_replacements)==(1 if self.live_input['name']=='neutral_running' else 2),'two new creations and actual same-record old generation replacements')
  self.nx_result=dict(prefix=self.nx_prefix,before=self.nx_before,branch=self.nx_branch,resources_before=self.nx_resources_before,resources=copy.deepcopy(self.nx_resources),bindings=self.nx_bindings,confirmed=confirmed,clear=clear,role=None,role_container=None,ready=ready,confirmation=confirmation,final=final,segments=self.nx_segments,frames=self.nx_frames,leaves=self.nx_leaves,commands=self.nx_commands,writes=self.nx_writes,queries=self.nx_queries,replacements=self.nx_replacements,GPU_APIs=self.nx_gpu,calls=self.nx_calls,conversions=self.nx_conversions,readbacks=observations,readback_observers=self.nx_observers,GDI_trace=copy.deepcopy(self.name_platform.trace[self.nx_prefix['GDI_trace']:]),GDI_handle_projection=self.name_platform.space.ledger(),accounting=self.get(0x765720),forward_wire_end=len(self.gpu.trace),CRT_forward_wire_end=len(self.live.trace))
  self.nx_result.update(GPU_projection_before=dict(next=self.nx_space.prefix_next,ledger=self.nx_space.prefix),GPU_projection=[r for r in self.space.ledger() if r['domain'] in PROJECTION_DOMAINS])
  return a
 def fu_actual_root(self,*args,**kwargs):
  if not self.replacement_ready:return super().fu_actual_root(*args,**kwargs)
  return self.nx_actual_root(*args,**kwargs)
 def resource_root(self,label,*args,**kwargs):
  if self.replacement_ready and label=='supplemental_original_group20_destructor' and self.live_input['name']=='neutral_running':self.nx_actual_root('supplemental_original_replacement_extra_line_destructor',0x403730,receiver=TEXTURE+STRIDE)
  return super().resource_root(label,*args,**kwargs)
 def run(self):
  row=super().run();need(not self.nx_live and len(self.nx_resources)==10 and all(not r['alive'] for r in self.nx_resources),'all ten actual creation generations originally released')
  row.update(terminal_replacement=self.nx_result,replacement_cleanup=self.nx_cleanup,replacement_resources_after_cleanup=copy.deepcopy(self.nx_resources));return row

def source_contract():
 return dict(parent=parent.source_contract(),fixed_predecessor=fixed_parents(),branches={n:branch(n) for n in ('neutral_running','timeout_before_combat')},keyboard=KEYBOARD,raw_device_offset=12,raw_device_bytes=256,new_capture_cycle=True,captured_inputs=parent.parent.parent.input_contract(),first_confirmation_released=True,next_confirmation_released=False,forward_roots=[0x40DB90,0x40DC80,0x425DE0,0x454CF0],new_VM_or_handler_roots=0,derived_input_host_writes=0,PC_or_wait_host_writes=0,new_OS_input=False,draw_or_Present=False,new_rasters=list(RASTERS),helper=helper_contract(),extra_code=[],GPU_projection=dict(prefix_domain='overlay',prefix_entries_unchanged=True,new_domains=list(PROJECTION_DOMAINS),domain_from_record_index=True,original_AddressSpace_algorithm=True,keys_per_new_generation=dict(texture=1,vtable=1,methods=4,bits=1,total=7),guest_stride=PROJECTION_STRIDE,prefix_next_max=PREFIX_NEXT_MAX,new_next_max=REPLACEMENT_NEXT_MAX,GDI_guest_start=GDI_GUEST_START))

def save_source(path,data):
 """Keep terminal.save's JSON bytes; change only new CLI gzip compression."""
 p=ROOT/path;need(not p.exists(),'fresh replacement source path');raw=(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n').encode()
 p.write_bytes(gzip.compress(raw,compresslevel=6,mtime=0) if p.suffix=='.gz' else raw)

def run_case(c,ch,gh,ticks=None):
 fixed=fixed_parent_times()[c['name']]
 if ticks is None:ticks=list(fixed)
 need(ticks==fixed,'exact frozen original clock stream');instances=[]
 class Attached(ReplacementMachine):
  def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);instances.append(self)
 class Diagnostics:
  @staticmethod
  def save(path,data):
   if instances:
    m=instances[0];data['replacement']=dict(active=m.replacement_active,segments=m.nx_segments,frames=m.nx_frames,leaves=m.nx_leaves,resources=m.nx_resources,bindings=m.nx_bindings,commands=m.nx_commands,queries=m.nx_queries,replacements=m.nx_replacements,CRT_trace=copy.deepcopy(m.live.trace),GPU_trace=copy.deepcopy(m.gpu.trace),GDI_trace=copy.deepcopy(m.name_platform.trace),readback_observers=m.nx_observers,memory=m.snapshot(),trace=m.mark(),local_trace=m.nx_mark())
   return terminal.save(path.replace('terminal-overlay-diagnostic-','terminal-replacement-diagnostic-').replace('.json.gz','-20261028.json.gz'),data)
 fn=types.FunctionType(overlay.run_case.__code__,dict(overlay.run_case.__globals__,OverlayMachine=Attached,terminal=Diagnostics),closure=overlay.run_case.__closure__)
 return fn(c,ch,gh,ticks)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case',type=int);p.add_argument('--helper-prefix',default='terminal-replacement');a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable replacement report');fixed_parents();fixed_parent_times();ch,gh,b=helpers(a.helper_prefix);rows=[]
 for c in (overlay.parent.corpus() if a.case is None else [overlay.parent.corpus()[a.case]]):rows.append(run_case(c,ch,gh));print('replacement source',c['name'],'new confirmation held',flush=True)
 save_source(a.out,dict(schema_version=1,source_contract=source_contract(),helper_build=b,cases=rows,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False))
