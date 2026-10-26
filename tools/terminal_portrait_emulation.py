"""Same-current-resource original SC001/SC002 loading and terminal role readiness."""
import argparse,copy,hashlib,struct,types
from unicorn.x86_const import UC_X86_REG_ESP,UC_X86_REG_ECX
from tools import terminal_name_emulation as parent
from tools import terminal_overlay_emulation as overlay
from tools.school_retained_name_corpus import source_names
from tools.school_retained_portrait_file_catalog import parse

ROOT,CODE,need,sha,terminal,MAIN,VM,STACK,RETURN,NODE,TEXTURE=(getattr(parent,n) for n in ('ROOT','CODE','need','sha','terminal','MAIN','VM','STACK','RETURN','NODE','TEXTURE'))
TASK,INPUT,MANAGER=(getattr(overlay,n) for n in ('TASK','INPUT','MANAGER'))
EXTRA_RANGES=((0x4CDE10,0x4CDF10),(0x416740,0x416790),(0x4CC28B,0x4CC3C3),(0x4CC3E0,0x4CC600),(0x4C9610,0x4C99E0),(0x4CAA20,0x4CAA66),(0x4CB220,0x4CBF90),(0x4CD4D0,0x4CD7B0),(0x4CA860,0x4CA958),(0x4CD850,0x4CD8CE),(0x410310,0x4103E3),(0x408F90,0x409132),(0x4CC810,0x4CC8CC),(0x4CADE0,0x4CAF10),(0x4CD060,0x4CD1E0))
RANGES=parent.RANGES+EXTRA_RANGES;ALLOWED=frozenset(a for lo,hi in RANGES for a in range(lo,hi))
REFERENCE=types.FunctionType(parent.REFERENCE.__code__,dict(parent.REFERENCE.__globals__,RANGES=RANGES))
TASK_APIS=overlay.parent.APIS

class PortraitMachine(parent.NameMachine):
 source_code=types.FunctionType(parent.NameMachine.source_code.__code__,dict(parent.NameMachine.source_code.__globals__,ALLOWED=ALLOWED,REFERENCE=REFERENCE))
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.portrait_active=False;self.portrait_cleaning=False;self.portrait_gpu=[];self.portrait_leaves=[];self.portrait_copies=[];self.portrait_segments=[];self.portrait_writes=[];self.portrait_frames=[];self.portrait_count=self.portrait_write_count=0;self.portrait_ih=hashlib.sha256();self.portrait_wh=hashlib.sha256();self.stop_at=None
  role=2 if self.live_input['name']=='neutral_running' else 1;catalog,_=source_names();self.role=role;self.role_source=catalog['roles'][str(role)];self.portrait_path='data\\adv\\bin\\'+self.role_source['filename'];self.asset=(ROOT/self.role_source['image_path']).read_bytes();need(sha(self.asset)==self.role_source['image_sha256'],'fixed source portrait');self.container=parse(self.asset)
 def local_mark(self):return dict(instructions=self.portrait_count,writes=self.portrait_write_count,code_sha256=self.portrait_ih.hexdigest(),write_sha256=self.portrait_wh.hexdigest())
 def api_crt(self,slot):
  original=self.crt.api
  if self.portrait_active and slot==0x5921EC:
   fn=overlay.CrtGuest.api;self.crt.api=types.MethodType(types.FunctionType(fn.__code__,dict(fn.__globals__,RESOURCE_NAME=self.portrait_path),closure=fn.__closure__),self.crt)
  try:super().api_crt(slot)
  finally:self.crt.api=original
  if self.portrait_active:self.portrait_leaves.append(dict(kind='CRT',call=copy.deepcopy(self.crt_apis[-1])))
 def gpu_api(self,at):
  sp=self.getreg('ESP');slot=self.methods[at];arg0=self.get(sp+4)
  if not(self.portrait_active or self.portrait_cleaning) or slot!=80 and arg0!=getattr(self,'portrait_texture',{}).get('pointer'):return super().gpu_api(at)
  pop={80:32,56:12,64:20,68:8,8:4}[slot];bp=self.getreg('EBP');ret=self.get(sp);args=[self.get(sp+4+j) for j in range(0,pop,4)];outputs=[]
  need(ret=={80:0x403C8A,64:0x40395E,68:0x4039D3,8:0x40378D}.get(slot,ret) and (slot!=56 or ret in (0x403CBE,0x403A44)),'original portrait COM caller')
  def put(p,b):self.map_new(p,len(b));self.uc.mem_write(p,b);outputs.append(dict(pointer=p,hex=b.hex()))
  if slot==80:
   need(args==[self.device_ptr,256,512,1,0,25,1,self.portrait_record+44] and not hasattr(self,'portrait_texture'),'one source portrait texture ABI');native=self.gpu.create(256,512);result=self.space.result('overlay',native);self.portrait_texture=result['texture'];t=self.portrait_texture;self.portrait_native=native['texture']['pointer'];self.map_identity(t);self.methods.update({p:int(k) for k,p in t['methods'].items()});put(args[-1],struct.pack('<I',t['pointer']));op='create'
  else:
   t=self.portrait_texture;need(arg0==t['pointer'],'same current portrait texture')
   if slot==56:need(args==[t['pointer'],0,bp-(52 if ret==0x403CBE else 36)],'original portrait descriptor');op='describe';native=self.gpu.describe(self.portrait_native);result=copy.deepcopy(native);put(args[2],bytes.fromhex(result['hex']))
   elif slot==64:
    need(args==[t['pointer'],0,self.get(bp+8),0,2048],'original portrait lock');op='lock';native=self.gpu.lock(self.portrait_native);result=self.space.result('overlay',native);self.portrait_lock=result;b=bytes.fromhex(result['hex']);put(result['bits'],b);self.mutable.append((result['bits'],result['bits']+len(b)));put(args[2],struct.pack('<II',result['pitch'],result['bits']))
   elif slot==68:
    need(args==[t['pointer'],0],'original portrait unlock');op='unlock';self.portrait_upload=self.read(self.portrait_lock['bits'],len(bytes.fromhex(self.portrait_lock['hex'])));native=self.gpu.unlock(self.portrait_native,self.portrait_upload);result=copy.deepcopy(native);self.portrait_readback=self.gpu.readback(self.portrait_native);need(self.portrait_readback['hex']==self.portrait_upload.hex(),'entire current portrait GPU readback')
   else:need(args==[t['pointer']],'original portrait Release');op='release';native=self.gpu.release(self.portrait_native);result=copy.deepcopy(native)
  value=result['count'] if slot==8 else result['hr'];need(value==0,'actual portrait COM success');row=dict(slot=slot,target=at,sp=sp,return_va=ret,args=args,pop=pop,value=value,op=op,native_result=native,result=result,memory_outputs=outputs,actual_API_executed=True);self.portrait_gpu.append(row)
  if self.portrait_active:self.portrait_leaves.append(dict(kind='GPU',call=copy.deepcopy(row)))
  self.return_api(sp,value,pop)
 def write_hook(self,uc,access,at,size,value,context):
  super().write_hook(uc,access,at,size,value,context)
  if self.portrait_active:
   self.portrait_write_count+=1;self.portrait_wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
   if VM<=at<VM+0x9400 or at==0:self.portrait_writes.append(dict(pc=self.getreg('EIP'),address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))
 def code(self,uc,at,size,context):
  active=self.portrait_active
  if active:
   if at==self.stop_at:uc.emu_stop();return
   if at==0x56D4D0 and self.get(self.getreg('ESP'))==0x40483F:
    sp=self.getreg('ESP');args=[self.get(sp+4+j) for j in (0,4,8)];row=len(self.portrait_copies);need(row<512 and args==[self.portrait_lock['bits']+row*self.portrait_lock['pitch'],self.portrait_file+24+row*512,512],'each original portrait row memcpy');self.portrait_copies.append(dict(row=row,args=args,caller=0x40483F))
   if at in TASK_APIS:
    sp=self.getreg('ESP');target=at;ret=self.get(sp);args=[self.get(sp+4)];before=len(self.task_APIs);super().code(uc,at,size,context);need(len(self.task_APIs)==before+1,'one actual task query');r=self.task_APIs[-1];self.portrait_leaves.append(dict(kind='TASK',call=dict(r,sp=sp,return_va=ret,pop=4,value=r['result'],memory_outputs=[],new_mappings=[])));return
  super().code(uc,at,size,context)
  if active and at in ALLOWED:self.portrait_count+=1;self.portrait_ih.update(struct.pack('<I',at))
 def capture(self):return dict(memory=self.snapshot(),CPU=self.cpu(),state=self.task_state(),queue=self.queue_state(),trace=self.mark(),local_trace=self.local_mark())
 def segment(self,label,entry,stop=RETURN,root=None):
  before=self.cpu();trace=self.mark();local=self.local_mark();first=len(self.portrait_leaves)
  if root:
   sp=STACK+0xF000;self.put(sp,RETURN)
   for j,a in enumerate(root['args']):self.put(sp+4+j*4,a)
   self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_ECX,root['receiver'])
  self.stop_at=stop;self.uc.ctl_remove_cache(entry,entry+1);self.uc.emu_start(entry,RETURN,timeout=60_000_000,count=4_000_000);self.stop_at=None
  need(self.getreg('EIP')==stop,'natural original segment '+label)
  if root:need(self.getreg('ESP')==STACK+0xF004,'complete original root stack '+label)
  row=dict(label=label,entry=entry,stop=stop,root=root,before_CPU=before,CPU=self.cpu(),trace_before=trace,trace_after=self.mark(),local_before=local,local_after=self.local_mark(),leaves=[first,len(self.portrait_leaves)]);self.portrait_segments.append(row);return row
 def frame(self,index):
  before=self.task_state();queue_before=self.queue_state();first=len(self.portrait_segments)
  for label,va,receiver in (('heads',0x40DB90,MANAGER),('arena',0x40DC80,MANAGER),('input',0x425DE0,INPUT),('task',0x454CF0,TASK)):self.segment(label+'_'+str(index),va,root=dict(receiver=receiver,args=[]))
  return dict(index=index,before=before,after=self.task_state(),queue_before=queue_before,queue_after=self.queue_state(),segments=[first,len(self.portrait_segments)])
 def admission(self):
  a=super().admission();self.portrait_prefix=dict(CRT_APIs=len(self.crt_apis),resource_steps=len(self.resource_steps),task_APIs=len(self.task_APIs),extra_counts=copy.deepcopy(dict(self.extra_counts)),GPU_wire=len(self.gpu.trace),allocations=copy.deepcopy(self.crt.allocations),history=copy.deepcopy(self.crt.history));self.portrait_before=self.capture();self.portrait_active=True;self.active_overlay=True
  self.segment('original_portrait_file_and_constructor',0x4CDE10,0x403BD0);self.portrait_record=self.get(MAIN+0x844+32*8);file_api=next(x['call'] for x in self.portrait_leaves if x['kind']=='CRT' and x['call']['name']=='ReadFile');self.portrait_file=file_api['args'][1];need(self.read(self.portrait_file,len(self.asset))==self.asset,'entire source original portrait file');native=[]
  for p,r in self.crt.allocations.items():
   if p<=self.portrait_file<p+r['bytes'] or p<=self.portrait_record<p+r['bytes']:
    self.crt.sync(p);reply=self.live.request('readback',pointer=r['native']);need(reply['hex']==self.read(p,r['bytes']).hex(),'whole actual native file/vector readback');native.append(dict(guest=p,bytes=r['bytes'],wire_index=len(self.live.trace)-1,result=reply))
  self.portrait_constructed=dict(self.capture(),file_pointer=self.portrait_file,file_hex=self.read(self.portrait_file,len(self.asset)).hex(),record=self.portrait_record,record_hex=self.read(self.portrait_record,84).hex(),bank_hex=self.read(MAIN+0x844+32*8,8).hex(),native_allocation_readbacks=native,allocations=copy.deepcopy(self.crt.allocations))
  self.segment('original_portrait_pixels_and_IMAGE_return',0x403BD0,0x4CC0D2);self.portrait_image_return=self.capture();need(len(self.portrait_copies)==512,'all512 original rows copied')
  self.segment('original_role_VM_and_task_return',0x4CC0D2);self.portrait_complete=self.capture()
  for i in range(200):
   need(self.get(VM+28)==96,'only role instruction advances PC to96')
   if self.get(VM+0x20,'H')==0:break
   self.portrait_frames.append(self.frame(i))
   if i%20==0:print(self.live_input['name'],'portrait wait',i,self.get(VM+28),self.get(VM+0x20,'H'),flush=True)
  else:raise ValueError('bounded natural role readiness required')
  self.portrait_final=self.capture();self.portrait_active=self.active_overlay=False
  self.portrait_result=dict(prefix=self.portrait_prefix,before=self.portrait_before,constructed=self.portrait_constructed,image_return=self.portrait_image_return,completion=self.portrait_complete,final=self.portrait_final,segments=self.portrait_segments,frames=self.portrait_frames,leaves=self.portrait_leaves,writes=self.portrait_writes,copy_rows=self.portrait_copies,texture=self.portrait_texture,lock=self.portrait_lock,upload_hex=self.portrait_upload.hex(),readback=self.portrait_readback,GPU_APIs=copy.deepcopy(self.portrait_gpu),GYBC_readback=self.gpu.readback(self.texture_native),name_readback=self.gpu.readback(self.name_native),allocation_history=copy.deepcopy(self.crt.history),live_allocations=copy.deepcopy(self.crt.allocations),role=self.role,path=self.portrait_path,source=self.role_source,container=self.container)
  return a
 def resource_root(self,label,*args,**kwargs):
  if label=='supplemental_original_group20_destructor':
   self.portrait_cleaning=True;first=len(self.portrait_gpu)
   try:self.resource_root('supplemental_original_portrait_container_destructor',0x41F4E0,[32],MAIN+0x844)
   finally:self.portrait_cleaning=False
   self.portrait_cleanup=dict(GPU_APIs=copy.deepcopy(self.portrait_gpu[first:]),texture_bytes=self.get(0x765720),game_bytes=self.get(0x79FC74),bank_hex=self.read(MAIN+0x844+32*8,8).hex(),old_CRT_cleanup_start=len(self.crt_apis))
  return super().resource_root(label,*args,**kwargs)
 def run(self):
  r=super().run();r.update(terminal_portrait=self.portrait_result,portrait_cleanup=self.portrait_cleanup);return r

def source_contract():
 return dict(parent=parent.source_contract(),roles=[2,1],portrait_group=32,texture_size=[256,512],actual_current_file_CRT_and_GPU=True,new_forward_VM_or_role_handler_roots=0,complete_task_entry=0x454CF0,next_PC=96,next_instruction_executed=False,extra_code=[dict(start=a,end=b,sha256=sha(CODE[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES])
def helpers(prefix='terminal-portrait'):
 a,aa=overlay.platform.build(ROOT/'tools/terminal_portrait_crt_platform.cs',prefix+'-crt');b,bb=overlay.platform.build(ROOT/'tools/terminal_portrait_d3d8_platform.cs',prefix+'-gpu');return a,b,dict(CRT=aa,GPU=bb)
def run_case(c,ch,gh,ticks=None):
 class Diagnostics:
  @staticmethod
  def save(path,data):return terminal.save(path.replace('terminal-overlay-diagnostic-','terminal-portrait-diagnostic-'),data)
 fn=types.FunctionType(overlay.run_case.__code__,dict(overlay.run_case.__globals__,OverlayMachine=PortraitMachine,terminal=Diagnostics),closure=overlay.run_case.__closure__);return fn(c,ch,gh,ticks)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case',type=int);a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable portrait report');ch,gh,b=helpers();rows=[]
 for c in (overlay.parent.corpus() if a.case is None else [overlay.parent.corpus()[a.case]]):
  r=run_case(c,ch,gh);rows.append(r);print('portrait source',c['name'],'PC96 ready, frames',len(r['terminal_portrait']['frames']),flush=True)
 terminal.save(a.out,dict(schema_version=1,source_contract=source_contract(),helper_build=b,cases=rows,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False))
