"""Original terminal first dialogue with current owned GDI and fourth GPU texture."""
import argparse,copy,hashlib,struct,time,types
from unicorn.x86_const import UC_X86_REG_ESP,UC_X86_REG_ECX
from tools import terminal_portrait_emulation as parent
from tools import terminal_name_emulation as name
from tools.school_text_preparation_emulation import NATIVE as TEXT_NATIVE
from tools.school_dialogue_wait_emulation import WAIT_RANGES
from tools.school_font_raster_catalog import geometry

ROOT,CODE,need,sha,terminal,MAIN,VM,STACK,RETURN,TASK,INPUT,MANAGER=(getattr(parent,n) for n in ('ROOT','CODE','need','sha','terminal','MAIN','VM','STACK','RETURN','TASK','INPUT','MANAGER'))
OBJECT=VM+0x430+5*0xAB8;TEXTURE=OBJECT+0x28;RASTER=0x3E100000
GDI=dict(name.GDI);GDI[0x5920A0]=('CreateFontA',0x4CAD09,56)
EXTRA_RANGES=TEXT_NATIVE+WAIT_RANGES+((0x4CAD09,0x4CADD3),)
RANGES=parent.RANGES+EXTRA_RANGES;ALLOWED=frozenset(a for lo,hi in RANGES for a in range(lo,hi))
REFERENCE=types.FunctionType(parent.REFERENCE.__code__,dict(parent.REFERENCE.__globals__,RANGES=RANGES))

class DialogueMachine(parent.PortraitMachine):
 source_code=types.FunctionType(parent.PortraitMachine.source_code.__code__,dict(parent.PortraitMachine.source_code.__globals__,ALLOWED=ALLOWED,REFERENCE=REFERENCE))
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.dialogue_active=False;self.dialogue_cleaning=False;self.dialogue_segments=[];self.dialogue_frames=[];self.dialogue_leaves=[];self.dialogue_calls=[];self.dialogue_gpu=[];self.dialogue_conversions=[];self.dialogue_writes=[];self.dialogue_commands=[];self.dialogue_queries=[];self.dialogue_count=self.dialogue_write_count=0;self.dialogue_ih=hashlib.sha256();self.dialogue_wh=hashlib.sha256();self.dialogue_stop=None
 def dialogue_mark(self):return dict(instructions=self.dialogue_count,writes=self.dialogue_write_count,code_sha256=self.dialogue_ih.hexdigest(),write_sha256=self.dialogue_wh.hexdigest())
 def dialogue_capture(self):return dict(memory=self.snapshot(),CPU=self.cpu(),state=self.task_state(),queue=self.queue_state(),trace=self.mark(),local_trace=self.dialogue_mark())
 def dialogue_gdi(self,target):
  slot=self.gdi_targets[target];nm,caller,pop=GDI[slot];sp=self.getreg('ESP');ret=self.get(sp);args=[self.get(sp+4+j) for j in range(0,pop,4)]
  need(caller is None or ret==caller,'exact original dialogue GDI caller '+nm)
  row=self.name_platform.call(self,nm,args,ret);row.update(import_slot=slot,target=target,sp=sp,return_va=ret,pop=pop,value=row['result'])
  if nm=='CreateDIBSection':self.mutable.append((RASTER,RASTER+row['mapped_bytes']))
  self.dialogue_calls.append(row);self.dialogue_leaves.append(dict(kind='GDI',call=copy.deepcopy(row)));self.return_api(sp,row['result'],pop)
 def gpu_api(self,at):
  sp=self.getreg('ESP');slot=self.methods[at];arg0=self.get(sp+4)
  if not(self.dialogue_active or self.dialogue_cleaning) or slot!=80 and arg0!=getattr(self,'dialogue_texture',{}).get('pointer'):return super().gpu_api(at)
  pop={80:32,56:12,64:20,68:8,8:4}[slot];bp=self.getreg('EBP');ret=self.get(sp);args=[self.get(sp+4+j) for j in range(0,pop,4)];outputs=[]
  need(ret=={80:0x403C8A,64:0x40395E,68:0x4039D3,8:0x40378D}.get(slot,ret) and (slot!=56 or ret in (0x403CBE,0x403A44)),'original dialogue COM caller')
  def put(p,b):self.map_new(p,len(b));self.uc.mem_write(p,b);outputs.append(dict(pointer=p,hex=b.hex()))
  if slot==80:
   cfg=geometry(self.name_platform.service.measured);w,h=[1<<(v-1).bit_length() for v in cfg['texture_size']]
   need(args==[self.device_ptr,w,h,1,0,25,1,TEXTURE+44] and not hasattr(self,'dialogue_texture'),'one source fourth texture ABI');native=self.gpu.create(w,h);result=self.space.result('overlay',native);self.dialogue_texture=result['texture'];t=self.dialogue_texture;self.dialogue_native=native['texture']['pointer'];self.map_identity(t);self.methods.update({p:int(k) for k,p in t['methods'].items()});put(args[-1],struct.pack('<I',t['pointer']));op='create'
  else:
   t=self.dialogue_texture;need(arg0==t['pointer'],'same current dialogue texture')
   if slot==56:need(args==[t['pointer'],0,bp-(52 if ret==0x403CBE else 36)],'original dialogue descriptor');op='describe';native=self.gpu.describe(self.dialogue_native);result=copy.deepcopy(native);put(args[2],bytes.fromhex(result['hex']))
   elif slot==64:
    need(args==[t['pointer'],0,self.get(bp+8),0,2048],'original dialogue lock');op='lock';native=self.gpu.lock(self.dialogue_native);result=self.space.result('overlay',native);self.dialogue_lock=result;b=bytes.fromhex(result['hex']);put(result['bits'],b);self.mutable.append((result['bits'],result['bits']+len(b)));put(args[2],struct.pack('<II',result['pitch'],result['bits']))
   elif slot==68:
    need(args==[t['pointer'],0],'original dialogue unlock');op='unlock';self.dialogue_upload=self.read(self.dialogue_lock['bits'],len(bytes.fromhex(self.dialogue_lock['hex'])));native=self.gpu.unlock(self.dialogue_native,self.dialogue_upload);result=copy.deepcopy(native);self.dialogue_readback=self.gpu.readback(self.dialogue_native);need(self.dialogue_readback['hex']==self.dialogue_upload.hex(),'entire fourth current GPU readback')
   else:need(args==[t['pointer']],'original dialogue Release');op='release';native=self.gpu.release(self.dialogue_native);result=copy.deepcopy(native)
  value=result['count'] if slot==8 else result['hr'];need(value==0,'actual dialogue COM success');row=dict(slot=slot,target=at,sp=sp,return_va=ret,args=args,pop=pop,value=value,op=op,native_result=native,result=result,memory_outputs=outputs,actual_API_executed=True);self.dialogue_gpu.append(row)
  if self.dialogue_active:self.dialogue_leaves.append(dict(kind='GPU',call=copy.deepcopy(row)))
  self.return_api(sp,value,pop)
 def write_hook(self,uc,access,at,size,value,context):
  super().write_hook(uc,access,at,size,value,context)
  if self.dialogue_active:
   self.dialogue_write_count+=1;self.dialogue_wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
   if VM<=at<VM+0x9400 or at==0:self.dialogue_writes.append(dict(pc=self.getreg('EIP'),address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))
 def code(self,uc,at,size,context):
  active=self.dialogue_active
  if active:
   if at==self.dialogue_stop:uc.emu_stop();return
   if at==0x4CE9C5:
    p=self.get(VM+16)+self.get(VM+28);op,n=struct.unpack('<HH',self.read(p,4));need(op!=27,'next opcode27 must remain unexecuted');self.dialogue_commands.append(dict(PC=self.get(VM+28),opcode=op,bytes=n,source_pointer=p))
   if at==0x405869:
    sp=self.getreg('ESP');a=[self.get(sp+j) for j in range(0,24,4)];self.dialogue_conversions.append(dict(entry=at,args=a,rect=list(struct.unpack('<4I',self.read(a[4],16))),point=list(struct.unpack('<2I',self.read(a[5],8)))))
   if at in parent.TASK_APIS and self.get(self.getreg('ESP'))==parent.TASK_APIS[at][2]:
    sp=self.getreg('ESP');ret=self.get(sp);before=len(self.task_APIs);super().code(uc,at,size,context);need(len(self.task_APIs)==before+1,'one actual dialogue task query');r=self.task_APIs[-1];self.dialogue_leaves.append(dict(kind='TASK',call=dict(r,sp=sp,return_va=ret,pop=4,value=r['result'],memory_outputs=[],new_mappings=[])));return
   if at in self.gdi_targets:self.dialogue_gdi(at);return
   if at in (0x4CB5F0,0x4CD3B7,0x4D5EC0,0x4CD402,0x4128F0,0x4CD432,0x4CCFF7,0x4CCB30,0x4CD02D):
    sp=self.getreg('ESP');self.dialogue_queries.append(dict(entry=at,CPU=self.cpu(),receiver=self.getreg('ECX'),stack_hex=self.read(sp,28).hex(),object_hex=self.read(OBJECT,0xAB8).hex()))
  super().code(uc,at,size,context)
  if active and at in ALLOWED:self.dialogue_count+=1;self.dialogue_ih.update(struct.pack('<I',at))
 def dialogue_segment(self,label,entry,stop=RETURN,root=None):
  before=self.cpu();trace=self.mark();local=self.dialogue_mark();first=len(self.dialogue_leaves)
  if root:
   sp=STACK+0xF000;self.put(sp,RETURN)
   for j,a in enumerate(root['args']):self.put(sp+4+j*4,a)
   self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_ECX,root['receiver'])
  self.dialogue_stop=stop;self.uc.ctl_remove_cache(entry,entry+1);self.uc.emu_start(entry,RETURN,timeout=60_000_000,count=4_000_000);self.dialogue_stop=None
  need(self.getreg('EIP')==stop,'natural original dialogue segment '+label)
  if root and stop==RETURN:need(self.getreg('ESP')==STACK+0xF004,'complete original dialogue root stack '+label)
  row=dict(label=label,entry=entry,stop=stop,root=root,before_CPU=before,CPU=self.cpu(),trace_before=trace,trace_after=self.mark(),local_before=local,local_after=self.dialogue_mark(),leaves=[first,len(self.dialogue_leaves)]);self.dialogue_segments.append(row);return row
 def dialogue_frame(self,index,phase,first=False):
  before=self.task_state();queue_before=self.queue_state();start=len(self.dialogue_segments)
  for label,va,recv in (('heads',0x40DB90,MANAGER),('arena',0x40DC80,MANAGER),('input',0x425DE0,INPUT)):
   self.dialogue_segment(label+'_'+str(index),va,root=dict(receiver=recv,args=[]))
  if first:
   self.dialogue_segment('task_to_original_font',0x454CF0,self.font_target,dict(receiver=TASK,args=[]));sp=self.getreg('ESP');self.dialogue_font_boundary=self.dialogue_capture();self.dialogue_pending_font=dict(entry=self.font_target,caller=self.get(sp),args=[self.get(sp+4+j*4) for j in range(14)],CPU=self.cpu(),first_instruction_executed=False)
   self.dialogue_segment('original_font_and_raster',self.font_target,0x403BD0);s=self.name_platform.service;self.dialogue_raster=dict(self.dialogue_capture(),measured=copy.deepcopy(s.measured),selected_face=s.face,ACP=s.gdi.acp,raster_hex=s.gdi.raster(s.bitmap).hex(),stages=copy.deepcopy(s.stages[self.dialogue_prefix['GDI_stages']:]),calls=copy.deepcopy(self.dialogue_calls))
   self.dialogue_segment('original_pixels_handler_VM_complete_task',0x403BD0);need(self.getreg('ESP')==STACK+0xF004,'first whole task naturally returned');self.dialogue_completion=self.dialogue_capture()
  else:self.dialogue_segment('task_'+str(index),0x454CF0,root=dict(receiver=TASK,args=[]))
  row=dict(index=index,phase=phase,before=before,after=self.task_state(),queue_before=queue_before,queue_after=self.queue_state(),segments=[start,len(self.dialogue_segments)],capture=self.dialogue_capture());self.dialogue_frames.append(row);return row
 def admission(self):
  a=super().admission();self.dialogue_prefix=dict(CRT_APIs=len(self.crt_apis),resource_steps=len(self.resource_steps),task_APIs=len(self.task_APIs),extra_counts=copy.deepcopy(dict(self.extra_counts)),GPU_wire=len(self.gpu.trace),GDI_trace=len(self.name_platform.trace),GDI_stages=len(self.name_platform.service.stages),overlay_commands=len(self.overlay_commands));self.dialogue_before=self.dialogue_capture();self.dialogue_active=self.active_overlay=True
  # Preserve the accepted name/portrait prefix byte for byte. Only this new
  # DIB uses a fresh mapping in the same live native measurement-DC owner.
  s=self.name_platform.service;fn=s.call_raster
  s.call_raster=types.MethodType(types.FunctionType(fn.__func__.__code__,dict(fn.__func__.__globals__,RASTER=RASTER)),s)
  self.dialogue_frame(0,'select_text_config');need(self.get(VM+28)==104 and self.get(VM+32,'H')==0,'original43 whole task PC104')
  self.dialogue_frame(1,'first_sentence',True);need(self.get(VM+28)==110 and self.get(VM+32,'H')==0,'first sentence whole task PC110')
  for i in range(2,100):
   self.dialogue_frame(i,'text_readiness');need(self.get(VM+28)==114,'only original50 during readiness')
   if self.get(VM+32,'H')==0:break
  else:raise ValueError('bounded first dialogue readiness')
  self.dialogue_ready=self.dialogue_capture();self.dialogue_frame(i+1,'enter_confirmation');need(self.get(VM+28)==118 and self.get(VM+32,'H')==1,'original51 confirmation wait');self.dialogue_confirmation=self.dialogue_capture()
  for j in range(2):
   self.dialogue_frame(i+2+j,'held_confirmation');need(self.get(VM+28)==118 and self.get(VM+32,'H')==1,'no-input original confirmation remains held')
  self.dialogue_final=self.dialogue_capture();self.dialogue_active=self.active_overlay=False
  self.dialogue_result=dict(prefix=self.dialogue_prefix,before=self.dialogue_before,font_boundary=self.dialogue_font_boundary,pending_font=self.dialogue_pending_font,raster=self.dialogue_raster,completion=self.dialogue_completion,ready=self.dialogue_ready,confirmation=self.dialogue_confirmation,final=self.dialogue_final,segments=self.dialogue_segments,frames=self.dialogue_frames,leaves=self.dialogue_leaves,calls=self.dialogue_calls,GPU_APIs=copy.deepcopy(self.dialogue_gpu),conversions=self.dialogue_conversions,writes=self.dialogue_writes,commands=self.dialogue_commands,queries=self.dialogue_queries,texture=self.dialogue_texture,texture_record=TEXTURE,lock=self.dialogue_lock,upload_hex=self.dialogue_upload.hex(),readback=self.dialogue_readback,GYBC_readback=self.gpu.readback(self.texture_native),name_readback=self.gpu.readback(self.name_native),portrait_readback=self.gpu.readback(self.portrait_native),GDI_trace=copy.deepcopy(self.name_platform.trace[self.dialogue_prefix['GDI_trace']:]),GDI_handle_projection=self.name_platform.space.ledger(),accounting=self.get(0x765720),geometry=geometry(self.dialogue_raster['measured']))
  return a
 def resource_root(self,label,*args,**kwargs):
  if label=='supplemental_original_group20_destructor':
   self.dialogue_cleaning=True;first=len(self.dialogue_gpu);before=self.cpu()
   try:self.resource_root('supplemental_original_dialogue_texture_destructor',0x403730,receiver=TEXTURE)
   finally:self.dialogue_cleaning=False
   self.dialogue_cleanup=dict(GPU_APIs=copy.deepcopy(self.dialogue_gpu[first:]),texture_bytes=self.get(0x765720),record_hex=self.read(TEXTURE,0x68).hex(),before_CPU=before,CPU=self.cpu())
  return super().resource_root(label,*args,**kwargs)
 def run(self):
  r=super().run();r.update(terminal_dialogue=self.dialogue_result,dialogue_cleanup=self.dialogue_cleanup);return r

def source_contract():return dict(parent=parent.source_contract(),forward_roots=[0x40DB90,0x40DC80,0x425DE0,0x454CF0],new_VM_or_handler_roots=0,first_PC=96,ready_PC=114,final_PC=118,final_wait=1,hold_tasks=2,next_opcode27_executed=False,original_API_IAT_rebindings=0,system_input=False,draw_or_Present=False,raster=RASTER,texture_record=TEXTURE,extra_code=[dict(start=a,end=b,sha256=sha(CODE[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES])
def helpers(prefix='terminal-dialogue'):return parent.helpers(prefix)
def run_case(c,ch,gh,ticks=None):
 # Same native owner lifetime and failure teardown as the accepted predecessor.
 class Diagnostics:
  @staticmethod
  def save(path,data):return terminal.save(path.replace('terminal-overlay-diagnostic-','terminal-dialogue-diagnostic-') .replace('.json.gz','-20261026.json.gz'),data)
 fn=types.FunctionType(parent.overlay.run_case.__code__,dict(parent.overlay.run_case.__globals__,OverlayMachine=DialogueMachine,terminal=Diagnostics),closure=parent.overlay.run_case.__closure__);return fn(c,ch,gh,ticks)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case',type=int);a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable dialogue report');ch,gh,b=helpers();rows=[]
 for c in (parent.overlay.parent.corpus() if a.case is None else [parent.overlay.parent.corpus()[a.case]]):
  r=run_case(c,ch,gh);rows.append(r);print('dialogue source',c['name'],'PC118 held',len(r['terminal_dialogue']['frames']),flush=True)
 terminal.save(a.out,dict(schema_version=1,source_contract=source_contract(),helper_build=b,cases=rows,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False))
