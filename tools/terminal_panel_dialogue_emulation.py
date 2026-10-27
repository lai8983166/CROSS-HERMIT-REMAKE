"""Original layer7 terminal dialogue group with current owned GDI/GPU resources."""
import argparse,copy,gc,gzip,hashlib,json,struct,types
from functools import lru_cache
import unicorn.x86_const as x86
from tools import terminal_confirmation_emulation as parent
from tools.school_font_raster_catalog import geometry

ROOT,CODE,need,sha,terminal,MAIN,VM,STACK,RETURN,TASK,INPUT,MANAGER=(getattr(parent,n) for n in ('ROOT','CODE','need','sha','terminal','MAIN','VM','STACK','RETURN','TASK','INPUT','MANAGER'))
OBJECT=parent.OBJECT;NODE=parent.NODE;TEXTURE=OBJECT+0x28;STRIDE=0x110
RASTER=0x3E200000;RASTER_STRIDE=0x100000
RANGES=parent.RANGES;ALLOWED=parent.ALLOWED;REFERENCE=parent.REFERENCE
PARENT_ACCEPTANCE='analysis/terminal-confirmation-acceptance-v1-20261026.json'
PARENT_ACCEPTANCE_SHA='3d2a114f3120d1eff89984dfa13cfd6a17ab7d8f513267026a9255f5f6754529'
PARENT_SOURCE='analysis/terminal-confirmation-source-v1-20261026.json.gz'
PARENT_SOURCE_SHA='b2a22addd13640b2a89f766b4703d2ede260d0279e7c4384124a36455e38a9c3'
PARENT_PROOF='analysis/terminal-confirmation-proof-v1-20261026.json'
PARENT_PROOF_SHA='559d652aa1131b39ee4d6d26a194c9cb52cd9f0c8e5f23e24840b30cc271e5ed'
QUERIES=(0x4C4B80,0x4CABD0,0x4077C0,0x403730,0x403BD0,0x4CB220,0x4CB5F0,0x4CD3B7,0x4CD350,0x4128F0,0x4CCFF7,0x4CD02D,0x4CD402,0x4CD432)

def file_ref(path,expected):
 p=ROOT/path;h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 need(h.hexdigest()==expected,'fixed accepted predecessor '+path)
 return dict(path=path,bytes=p.stat().st_size,sha256=expected)

@lru_cache(maxsize=1)
def fixed_parents():
 a=file_ref(PARENT_ACCEPTANCE,PARENT_ACCEPTANCE_SHA);p=file_ref(PARENT_PROOF,PARENT_PROOF_SHA);s=file_ref(PARENT_SOURCE,PARENT_SOURCE_SHA)
 accepted=json.loads((ROOT/PARENT_ACCEPTANCE).read_text(encoding='utf8'))
 need(accepted['source_report']==s and accepted['independent_proof']==p and accepted['tasks_complete']==3 and accepted['boundaries']['VM_PC']==142 and accepted['boundaries']['VM_wait']==0,'accepted original pending layer7 font')
 return dict(acceptance=a,source=s,proof=p)

@lru_cache(maxsize=1)
def fixed_parent_times():
 fixed_parents()
 with gzip.open(ROOT/PARENT_SOURCE,'rt',encoding='utf8') as f:data=json.load(f)
 result={r['input']['name']:[a['result'] for a in r['APIs'] if a['name']=='GetTickCount'] for r in data['cases']}
 need(set(result)=={'neutral_running','timeout_before_combat'} and all(v and all(type(x)is int for x in v) for v in result.values()),'two complete fixed parent clock streams')
 del data;gc.collect();return result

def branch(name):
 need(name in ('neutral_running','timeout_before_combat'),'one actual terminal branch')
 return dict(text_indices=[1] if name=='neutral_running' else [1,2,3],ready_PC=152 if name=='neutral_running' else 164,final_PC=156 if name=='neutral_running' else 168)

class PanelDialogueMachine(parent.ConfirmationMachine):
 """Extend the current owner before any predecessor supplemental teardown."""
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.panel_dialogue_active=False;self.panel_dialogue_cleaning=False;self.panel_dialogue_stop=None
  self.pd_segments=[];self.pd_frames=[];self.pd_leaves=[];self.pd_calls=[];self.pd_gpu=[];self.pd_conversions=[];self.pd_writes=[];self.pd_commands=[];self.pd_queries=[];self.pd_sentences=[];self.pd_textures={};self.pd_cleanup=[]
  self.pd_count=self.pd_write_count=0;self.pd_ih=hashlib.sha256();self.pd_wh=hashlib.sha256();self.pd_current=None
 def pd_mark(self):return dict(instructions=self.pd_count,writes=self.pd_write_count,code_sha256=self.pd_ih.hexdigest(),write_sha256=self.pd_wh.hexdigest())
 def pd_capture(self,full=True):
  memory=self.snapshot() if full else [dict(pointer=a,bytes=b-a+1,sha256=sha(self.read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()]
  return dict(memory=memory,CPU=self.cpu(),state=self.task_state(),queue=self.queue_state(),trace=self.mark(),local_trace=self.pd_mark())
 def pd_readbacks(self):
  return dict(GYBC=self.gpu.readback(self.texture_native),name=self.gpu.readback(self.name_native),portrait=self.gpu.readback(self.portrait_native),dialogue=self.gpu.readback(self.dialogue_native))
 def pd_gdi(self,target):
  need(self.pd_current is not None,'GDI only in current original text append')
  slot=self.gdi_targets[target];name,caller,pop=parent.parent.GDI[slot];sp=self.getreg('ESP');ret=self.get(sp);args=[self.get(sp+4+j) for j in range(0,pop,4)]
  need(caller is None or ret==caller,'exact original panel dialogue GDI caller '+name)
  row=self.name_platform.call(self,name,args,ret);row.update(import_slot=slot,target=target,sp=sp,return_va=ret,pop=pop,value=row['result'])
  if name=='CreateDIBSection':
   need(row['guest_bits']==self.pd_current['raster_address'] and row['mapped_bytes']<=RASTER_STRIDE,'one bounded distinct current DIB mapping')
   self.mutable.append((row['guest_bits'],row['guest_bits']+row['mapped_bytes']))
  self.pd_calls.append(row);self.pd_leaves.append(dict(kind='GDI',call=copy.deepcopy(row)));self.return_api(sp,row['result'],pop)
 def gpu_api(self,at):
  sp=self.getreg('ESP');slot=self.methods[at];arg0=self.get(sp+4)
  if not(self.panel_dialogue_active or self.panel_dialogue_cleaning) or slot!=80 and arg0 not in self.pd_textures:return super().gpu_api(at)
  pop={80:32,56:12,64:20,68:8,8:4}[slot];bp=self.getreg('EBP');ret=self.get(sp);args=[self.get(sp+4+j) for j in range(0,pop,4)];outputs=[];wire_index=len(self.gpu.trace)
  need(ret=={80:0x403C8A,64:0x40395E,68:0x4039D3,8:0x40378D}.get(slot,ret) and (slot!=56 or ret in (0x403CBE,0x403A44)),'original panel dialogue COM caller')
  def put(p,b):self.map_new(p,len(b));self.uc.mem_write(p,b);outputs.append(dict(pointer=p,hex=b.hex()))
  if slot==80:
   s=self.pd_current;need(s is not None and not self.panel_dialogue_cleaning and 'texture' not in s,'one texture per original new line')
   cfg=geometry(self.name_platform.service.measured);w,h=[1<<(v-1).bit_length() for v in cfg['texture_size']]
   need(args==[self.device_ptr,w,h,1,0,25,1,s['record']+44] and self.get(OBJECT+22,'H')==s['record_index'] and self.get(s['record']+44)==0,'exact current line index, record and CreateTexture ABI')
   native=self.gpu.create(w,h);result=self.space.result('overlay',native);t=result['texture'];s.update(texture=t,native_pointer=native['texture']['pointer'],geometry=cfg,alive=True);self.pd_textures[t['pointer']]=s
   self.map_identity(t);self.methods.update({p:int(k) for k,p in t['methods'].items()});put(args[-1],struct.pack('<I',t['pointer']));op='create'
  else:
   s=self.pd_textures[arg0];t=s['texture'];need(s['alive'] and self.get(s['record']+44)==t['pointer'],'current live same-record panel dialogue texture');native_pointer=s['native_pointer']
   if slot==56:
    need(args==[t['pointer'],0,bp-(52 if ret==0x403CBE else 36)],'original current line descriptor');op='describe';native=self.gpu.describe(native_pointer);result=copy.deepcopy(native);put(args[2],bytes.fromhex(result['hex']))
   elif slot==64:
    need(not self.panel_dialogue_cleaning and args==[t['pointer'],0,self.get(bp+8),0,2048] and 'lock' not in s,'original current line LockRect ABI');op='lock';native=self.gpu.lock(native_pointer);result=self.space.result('overlay',native);s['lock']=result;b=bytes.fromhex(result['hex']);put(result['bits'],b);self.mutable.append((result['bits'],result['bits']+len(b)));put(args[2],struct.pack('<II',result['pitch'],result['bits']))
   elif slot==68:
    need(not self.panel_dialogue_cleaning and args==[t['pointer'],0] and 'upload_hex' not in s,'original current line UnlockRect ABI');op='unlock';s['upload_hex']=self.read(s['lock']['bits'],len(bytes.fromhex(s['lock']['hex']))).hex();native=self.gpu.unlock(native_pointer,bytes.fromhex(s['upload_hex']));result=copy.deepcopy(native);s['readback_wire_index']=len(self.gpu.trace);s['readback']=self.gpu.readback(native_pointer);need(s['readback']['hex']==s['upload_hex'],'whole actual current line upload and readback')
   else:
    need(self.panel_dialogue_cleaning and args==[t['pointer']],'only supplemental original line Release');op='release';native=self.gpu.release(native_pointer);result=copy.deepcopy(native);s['alive']=False
  value=result['count'] if slot==8 else result['hr'];need(value==0,'actual current panel dialogue COM success')
  row=dict(record=s['record'],record_index=s['record_index'],wire_index=wire_index,slot=slot,target=at,sp=sp,return_va=ret,args=args,pop=pop,value=value,op=op,native_result=native,result=result,memory_outputs=outputs,actual_API_executed=True);self.pd_gpu.append(row)
  if self.panel_dialogue_active:self.pd_leaves.append(dict(kind='GPU',call=copy.deepcopy(row)))
  self.return_api(sp,value,pop)
 def write_hook(self,uc,access,at,size,value,context):
  super().write_hook(uc,access,at,size,value,context)
  if self.panel_dialogue_active:
   self.pd_write_count+=1;self.pd_wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
   if VM<=at<VM+0x9400 or parent.KEYBOARD<=at<parent.KEYBOARD+0xA00 or TASK<=at<TASK+0x190 or at==0:self.pd_writes.append(dict(pc=self.getreg('EIP'),address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))
 def code(self,uc,at,size,context):
  active=self.panel_dialogue_active
  if active:
   if at==self.panel_dialogue_stop:uc.emu_stop();return
   if at==0x4CE9C5:
    p=self.get(VM+16)+self.get(VM+28);op,n=struct.unpack('<HH',self.read(p,4));expected=self.pd_branch['text_indices'];pc=self.get(VM+28)
    need((op==17 and pc in [142+6*i for i in range(1,len(expected))]) or (op==50 and pc==self.pd_branch['ready_PC']-4) or (op==51 and pc==self.pd_branch['ready_PC']),'bounded current dialogue-group dispatch')
    self.pd_commands.append(dict(PC=pc,opcode=op,bytes=n,source_pointer=p))
   if at==0x405869:
    sp=self.getreg('ESP');args=[self.get(sp+j) for j in range(0,24,4)];self.pd_conversions.append(dict(entry=at,args=args,record=self.pd_current['record'],sentence_index=self.pd_current['record_index'],rect=list(struct.unpack('<4I',self.read(args[4],16))),point=list(struct.unpack('<2I',self.read(args[5],8)))))
   if at in parent.parent.parent.TASK_APIS and self.get(self.getreg('ESP'))==parent.parent.parent.TASK_APIS[at][2]:
    sp=self.getreg('ESP');ret=self.get(sp);first=len(self.task_APIs);super().code(uc,at,size,context);need(len(self.task_APIs)==first+1,'one actual current dialogue task query');r=self.task_APIs[-1];self.pd_leaves.append(dict(kind='TASK',call=dict(r,sp=sp,return_va=ret,pop=4,value=r['result'],memory_outputs=[],new_mappings=[])));return
   if at in self.gdi_targets:self.pd_gdi(at);return
   if at in QUERIES:
    sp=self.getreg('ESP');self.pd_queries.append(dict(entry=at,CPU=self.cpu(),receiver=self.getreg('ECX'),stack_hex=self.read(sp,68).hex(),object_hex=self.read(OBJECT,0xAB8).hex(),node_hex=self.read(NODE,0xE0).hex()))
  super().code(uc,at,size,context)
  if active and at in ALLOWED:self.pd_count+=1;self.pd_ih.update(struct.pack('<I',at))
 def pd_segment(self,label,entry,stop=RETURN,root=None):
  before=self.cpu();trace=self.mark();local=self.pd_mark();first=len(self.pd_leaves)
  if root:
   sp=STACK+0xF000;self.put(sp,RETURN)
   for j,a in enumerate(root['args']):self.put(sp+4+j*4,a)
   self.uc.reg_write(x86.UC_X86_REG_ESP,sp);self.uc.reg_write(x86.UC_X86_REG_ECX,root['receiver'])
  self.panel_dialogue_stop=stop;self.uc.ctl_remove_cache(entry,entry+1);self.uc.emu_start(entry,0,timeout=60_000_000,count=4_000_000);self.panel_dialogue_stop=None
  need(self.getreg('EIP')==stop,'natural original panel dialogue segment '+label)
  if stop==RETURN:need(self.getreg('ESP')==STACK+0xF004,'complete original task stack '+label)
  row=dict(label=label,kind='root' if root else 'continuation',entry=entry,stop=stop,root=root,before_CPU=before,CPU=self.cpu(),trace_before=trace,trace_after=self.mark(),local_before=local,local_after=self.pd_mark(),leaves=[first,len(self.pd_leaves)]);self.pd_segments.append(row);return row
 def pd_prepare_sentence(self,index):
  need(0<=index<len(self.pd_branch['text_indices']) and len(self.pd_sentences)==index and self.pd_current is None,'exact ordered finite dialogue sentence')
  record=TEXTURE+index*STRIDE;need(self.get(OBJECT+22,'H')==index and self.get(record+44)==0,'original unused layer7 line record before append')
  s=dict(text_index=self.pd_branch['text_indices'][index],PC=142+index*6,record_index=index,record=record,raster_address=RASTER+index*RASTER_STRIDE)
  self.pd_current=s;service=self.name_platform.service;fn=service.call_raster
  service.call_raster=types.MethodType(types.FunctionType(fn.__func__.__code__,dict(fn.__func__.__globals__,RASTER=s['raster_address'])),service)
  return s
 def pd_complete_sentence(self,s):
  need(self.pd_current is s and self.getreg('EIP')==self.font_target and self.get(VM+28)==s['PC'],'natural pending original current sentence font')
  s['font_boundary']=self.pd_capture();sp=self.getreg('ESP');s['pending_font']=dict(entry=self.font_target,caller=self.get(sp),args=[self.get(sp+4+j*4) for j in range(14)],CPU=self.cpu(),first_instruction_executed=False);need(s['pending_font']['caller']==0x4CAD09,'original current sentence font caller')
  first_calls=len(self.pd_calls);first_gpu=len(self.pd_gpu);first_conversions=len(self.pd_conversions);first_leaves=len(self.pd_leaves);first_gdi_trace=len(self.name_platform.trace);service=self.name_platform.service;first_stages=len(service.stages)
  self.pd_segment('original_line_'+str(s['text_index'])+'_font_raster',self.font_target,0x403BD0)
  s['raster']=dict(self.pd_capture(),measured=copy.deepcopy(service.measured),selected_face=service.face,ACP=service.gdi.acp,raster_hex=service.gdi.raster(service.bitmap).hex(),stages=copy.deepcopy(service.stages[first_stages:]),calls=copy.deepcopy(self.pd_calls[first_calls:]))
  self.pd_segment('original_line_'+str(s['text_index'])+'_pixels_handler_VM_complete_task',0x403BD0)
  need(self.get(VM+28)==s['PC']+6 and self.get(VM+32,'H')==0 and self.get(OBJECT+22,'H')==s['record_index']+1,'original append and complete VM/task return')
  s.update(completion=self.pd_capture(),calls=copy.deepcopy(self.pd_calls[first_calls:]),GPU_APIs=copy.deepcopy(self.pd_gpu[first_gpu:]),conversions=copy.deepcopy(self.pd_conversions[first_conversions:]),GDI_trace=copy.deepcopy(self.name_platform.trace[first_gdi_trace:]),leaves=[first_leaves,len(self.pd_leaves)],observer_wire_indices=list(range(len(self.gpu.trace),len(self.gpu.trace)+4)),readbacks_old4=self.pd_readbacks())
  need(s['alive'] and len(s['GPU_APIs'])==4,'exact four original COM leaves for new line, no premature release')
  self.pd_sentences.append(s);self.pd_current=None;return s
 def pd_frame(self,phase,sentence_index=None,resume=False):
  index=len(self.pd_frames);before=self.task_state();queue=self.queue_state();first=len(self.pd_segments)
  if not resume:
   for label,entry,recv in (('heads',0x40DB90,MANAGER),('arena',0x40DC80,MANAGER),('input',0x425DE0,INPUT)):
    self.pd_segment(label+'_'+str(index),entry,root=dict(receiver=recv,args=[]))
  if sentence_index is not None:
   s=self.pd_prepare_sentence(sentence_index)
   if not resume:self.pd_segment('task_to_line_'+str(s['text_index'])+'_font',0x454CF0,self.font_target,dict(receiver=TASK,args=[]))
   self.pd_complete_sentence(s)
  else:
   need(not resume,'resume only the already pending first sentence')
   self.pd_segment('task_'+str(index),0x454CF0,root=dict(receiver=TASK,args=[]))
  row=dict(index=index,phase=phase,kind='resume' if resume else 'root',before=before,after=self.task_state(),queue_before=queue,queue_after=self.queue_state(),segments=[first,len(self.pd_segments)],capture=self.pd_capture(False));self.pd_frames.append(row)
  print(self.live_input['name'],phase,index,self.get(VM+28),self.get(VM+32,'H'),flush=True);return row
 def admission(self):
  a=super().admission();self.pd_branch=branch(self.live_input['name']);self.pd_prefix=dict(CRT_APIs=len(self.crt_apis),resource_steps=len(self.resource_steps),task_APIs=len(self.task_APIs),extra_counts=copy.deepcopy(dict(self.extra_counts)),GPU_wire=len(self.gpu.trace),GDI_trace=len(self.name_platform.trace),GDI_stages=len(self.name_platform.service.stages),overlay_commands=len(self.overlay_commands))
  self.pd_before=self.pd_capture();need(self.getreg('EIP')==self.font_target and (self.get(VM+28),self.get(VM+32,'H'),self.get(VM+0x1CC,'B'),self.get(parent.KEYBOARD+0x4B9,'B'))==(142,0,7,0),'same original pending layer7 font with retained released input')
  need(self.get(OBJECT+22,'H')==0 and all(self.get(TEXTURE+i*STRIDE+44)==0 for i in range(3)),'empty original layer7 line records, no replacement')
  self.panel_dialogue_active=self.active_overlay=True
  self.pd_frame('resume_first_sentence',0,True)
  for i in range(1,len(self.pd_branch['text_indices'])):self.pd_frame('append_sentence',i)
  for _ in range(100):
   self.pd_frame('text_readiness');need(self.get(VM+28)==self.pd_branch['ready_PC'],'only original50 before confirmation')
   if self.get(VM+32,'H')==0:break
  else:raise ValueError('bounded natural layer7 text readiness')
  ready=self.pd_capture();self.pd_frame('enter_confirmation');need((self.get(VM+28),self.get(VM+32,'H'))==(self.pd_branch['final_PC'],1),'new original51 confirmation remains pending');confirmation=self.pd_capture()
  for _ in range(2):
   self.pd_frame('held_confirmation');need((self.get(VM+28),self.get(VM+32,'H'),self.get(parent.KEYBOARD+0x4B9,'B'))==(self.pd_branch['final_PC'],1,0),'two complete no-input tasks hold new original confirmation')
  final=self.pd_capture();self.panel_dialogue_active=self.active_overlay=False
  old_observer_wire_indices=list(range(len(self.gpu.trace),len(self.gpu.trace)+4));readbacks=self.pd_readbacks();new_readbacks=[];new_observer_wire_indices=[]
  for s in self.pd_sentences:
   new_observer_wire_indices.append(len(self.gpu.trace));b=self.gpu.readback(s['native_pointer']);need(b==s['readback'],'entire current new line surface retained through confirmation');new_readbacks.append(b)
  self.pd_result=dict(prefix=self.pd_prefix,before=self.pd_before,branch=self.pd_branch,sentences=copy.deepcopy(self.pd_sentences),ready=ready,confirmation=confirmation,final=final,segments=self.pd_segments,frames=self.pd_frames,leaves=self.pd_leaves,calls=self.pd_calls,GPU_APIs=copy.deepcopy(self.pd_gpu),conversions=self.pd_conversions,writes=self.pd_writes,commands=self.pd_commands,queries=self.pd_queries,readbacks_old4=readbacks,old_observer_wire_indices=old_observer_wire_indices,new_readbacks=new_readbacks,new_observer_wire_indices=new_observer_wire_indices,GDI_trace=copy.deepcopy(self.name_platform.trace[self.pd_prefix['GDI_trace']:]),GDI_handle_projection=self.name_platform.space.ledger(),accounting=self.get(0x765720),object=OBJECT,node=NODE)
  return a
 def resource_root(self,label,*args,**kwargs):
  if label=='supplemental_original_group20_destructor':
   self.panel_dialogue_cleaning=True
   try:
    for s in reversed(self.pd_sentences):
     first=len(self.pd_gpu);before=self.pd_capture();self.resource_root('supplemental_original_panel_dialogue_line_'+str(s['text_index'])+'_destructor',0x403730,receiver=s['record']);after=self.pd_capture();need(not s['alive'] and self.get(s['record']+44)==0,'original line descriptor/Release clears actual current texture')
     self.pd_cleanup.append(dict(text_index=s['text_index'],record=s['record'],before=before,after=after,GPU_APIs=copy.deepcopy(self.pd_gpu[first:]),record_hex=self.read(s['record'],0x68).hex(),accounting=self.get(0x765720)))
   finally:self.panel_dialogue_cleaning=False
  return super().resource_root(label,*args,**kwargs)
 def run(self):
  r=super().run();r.update(terminal_panel_dialogue=self.pd_result,panel_dialogue_cleanup=self.pd_cleanup);return r

def source_contract():
 return dict(parent=parent.source_contract(),fixed_predecessor=fixed_parents(),first_PC=142,first_wait=0,layer=7,object=OBJECT,first_texture_record=TEXTURE,record_stride=STRIDE,branches={n:branch(n) for n in ('neutral_running','timeout_before_combat')},raster=RASTER,raster_stride=RASTER_STRIDE,forward_roots=[0x40DB90,0x40DC80,0x425DE0,0x454CF0],first_continuation_new_roots=0,new_VM_or_handler_roots=0,derived_input_host_writes=0,PC_or_wait_host_writes=0,new_OS_input=False,draw_or_Present=False,next_confirmation_released=False,extra_code=[])

def helpers(prefix='terminal-panel-dialogue'):return parent.helpers(prefix)

def run_case(c,ch,gh,ticks=None):
 fixed=fixed_parent_times()[c['name']]
 if ticks is None:ticks=list(fixed)
 need(ticks==fixed,'exact accepted original terminal clock stream')
 class Diagnostics:
  @staticmethod
  def save(path,data):return terminal.save(path.replace('terminal-overlay-diagnostic-','terminal-panel-dialogue-diagnostic-').replace('.json.gz','-20261026.json.gz'),data)
 fn=types.FunctionType(parent.parent.parent.overlay.run_case.__code__,dict(parent.parent.parent.overlay.run_case.__globals__,OverlayMachine=PanelDialogueMachine,terminal=Diagnostics),closure=parent.parent.parent.overlay.run_case.__closure__)
 return fn(c,ch,gh,ticks)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case',type=int);p.add_argument('--helper-prefix',default='terminal-panel-dialogue');a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable layer7 dialogue report')
 fixed_parent_times();ch,gh,b=helpers(a.helper_prefix);rows=[]
 for c in (parent.parent.parent.overlay.parent.corpus() if a.case is None else [parent.parent.parent.overlay.parent.corpus()[a.case]]):
  rows.append(run_case(c,ch,gh));print('panel dialogue source',c['name'],'new confirmation held',flush=True)
 terminal.save(a.out,dict(schema_version=1,source_contract=source_contract(),helper_build=b,cases=rows,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False))
