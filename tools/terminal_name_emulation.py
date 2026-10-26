"""Original terminal role2/1 name GDI and current GPU upload to portrait entry."""
import argparse,copy,ctypes,hashlib,struct,types
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_ESP,UC_X86_REG_EIP
from tools import terminal_after_fade_emulation as parent
from tools import school_retained_third_dialogue as dialogue
from tools.school_font_raster_emulation import NATIVE_RASTER
from tools.school_character_name_texture_emulation import NAME_SUFFIX
from tools.school_font_raster_catalog import geometry
from tools.school_retained_rendering import AddressSpace

ROOT,CODE,need,sha,terminal,MAIN,VM,STACK,RETURN=(getattr(parent,n) for n in ('ROOT','CODE','need','sha','terminal','MAIN','VM','STACK','RETURN'))
NODE=VM+0x6F60+5*0xE0;TEXTURE=NODE+0x60;RASTER=dialogue.RASTER
GDI=dict(dialogue.GDI);GDI[0x5920A0]=('CreateFontA',0x4CA7CB,56)
EXTRA_RANGES=NATIVE_RASTER+NAME_SUFFIX+((0x405779,0x405BDB),(0x4D1BF0,0x4D1C70),(0x414440,0x4144A7),(0x56D810,0x56DA10),(0x575940,0x575C70),(0x56CDA0,0x56CEC0))
RANGES=parent.RANGES+EXTRA_RANGES;ALLOWED=frozenset(a for lo,hi in RANGES for a in range(lo,hi))
REFERENCE=types.FunctionType(parent.REFERENCE.__code__,dict(parent.REFERENCE.__globals__,RANGES=RANGES))

class NativeGDI:
 """Typed handle translation; native resources live only in the current host."""
 def __init__(self):
  self.service=dialogue.Offscreen(1);self.space=AddressSpace();self.space.next=0x6A001000
  self.measure=self.space.guest('GDI',self.service.actual);self.service.logical=self.service.actual
  self.trace=[]
 def logical(self,p):return self.space.guest('GDI',p)
 def native(self,p):
  need(p in self.space.guest_to_native,'declared owned/stock GDI identity');return self.space.native('GDI',p)
 def call(self,g,name,args,ret):
  native=list(args)
  if name not in ('CreateFontA','lstrlenA','CreateCompatibleDC','GetStockObject'):native[0]=self.native(args[0])
  if name=='SelectObject':native[1]=self.native(args[1])
  row=self.service.call(g,name,native,ret);observed=copy.deepcopy(row);value=row['result']
  if name in ('CreateFontA','CreateCompatibleDC','CreateDIBSection','GetStockObject','SelectObject'):value=self.logical(value)
  row.update(args=list(args),result=value,actual_API_executed=True)
  row.pop('dc_translated_args',None);row.pop('native_bits',None)
  self.trace.append(dict(name=name,args=list(args),native_args=native,logical_result=value,native_result=observed))
  return row
 def close(self):return self.service.close()

class NameMachine(parent.FadeMachine):
 source_code=types.FunctionType(parent.FadeMachine.source_code.__code__,dict(parent.FadeMachine.source_code.__globals__,ALLOWED=ALLOWED,REFERENCE=REFERENCE))
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.name_active=False;self.name_cleaning=False;self.name_calls=[];self.name_gpu=[];self.conversions=[];self.name_pending=None;self.name_textures={}
  self.name_leaves=[];self.name_instructions=0;self.name_write_count=0;self.name_code_hash=hashlib.sha256();self.name_write_hash=hashlib.sha256()
  self.name_platform=NativeGDI();self.put(MAIN+0xB208,self.name_platform.measure)
  self.gdi_targets={self.get(slot):slot for slot in GDI}
  # Unicorn translates a basic block before invoking its first code hook. Map
  # the following zero page too; no native target instruction is executed.
  for target in self.gdi_targets:self.map_new(target,4096)
  self.mutable.append((0x7A4D4C,0x7A4D4C+260))
  self.u=self.uc;self.constructor_done=True
 def put(self,p,value,fmt='I'):
  if getattr(self,'constructor_done',False):need(STACK<=p and p+struct.calcsize('<'+fmt)<=STACK+0x20000,'runtime host setup limited to original root stack')
  return super().put(p,value,fmt)
 def read(self,p,n=4):return bytes(self.uc.mem_read(p,n))
 def return_api(self,sp,value,pop):
  for r,v in ((UC_X86_REG_EAX,value&0xFFFFFFFF),(UC_X86_REG_ESP,sp+4+pop),(UC_X86_REG_EIP,self.get(sp))):self.uc.reg_write(r,v)
 def gdi_api(self,target):
  slot=self.gdi_targets[target];name,caller,pop=GDI[slot];sp=self.getreg('ESP');ret=self.get(sp);args=[self.get(sp+4+j) for j in range(0,pop,4)]
  need(caller is None or caller==ret,'exact original name GDI caller '+name)
  row=self.name_platform.call(self,name,args,ret);row.update(import_slot=slot,target=target,sp=sp,return_va=ret,pop=pop)
  if name=='CreateDIBSection':self.mutable.append((RASTER,RASTER+row['mapped_bytes']))
  self.name_leaves.append(dict(kind='GDI',index=len(self.name_calls)));self.name_calls.append(row);self.return_api(sp,row['result'],pop)
 def gpu_api(self,at):
  sp=self.getreg('ESP');args0=self.get(sp+4);slot=self.methods[at]
  if not(self.name_active or self.name_cleaning) or slot!=80 and args0 not in self.name_textures:return super().gpu_api(at)
  pop={80:32,56:12,64:20,68:8,8:4}[slot];bp=self.getreg('EBP');ret=self.get(sp);args=[self.get(sp+4+j) for j in range(0,pop,4)];outputs=[]
  need(ret=={80:0x403C8A,64:0x40395E,68:0x4039D3,8:0x40378D}.get(slot,ret) and (slot!=56 or ret in (0x403CBE,0x403A44)),'original name COM caller')
  def put(p,b):self.map_new(p,len(b));self.uc.mem_write(p,b);outputs.append(dict(pointer=p,hex=b.hex()))
  if slot==80:
   cfg=geometry(self.name_platform.service.measured);w,h=[1<<(v-1).bit_length() for v in cfg['texture_size']]
   need(args==[self.device_ptr,w,h,1,0,25,1,TEXTURE+44] and not self.name_textures,'exact sole name texture CreateTexture')
   native=self.gpu.create(w,h);result=self.space.result('overlay',native);self.name_texture=result['texture'];t=self.name_texture;self.name_native=native['texture']['pointer'];self.name_textures[t['pointer']]=t;self.map_identity(t);self.methods.update({p:int(k) for k,p in t['methods'].items()});put(args[-1],struct.pack('<I',t['pointer']));op='create'
  else:
   t=self.name_textures[args0];need(args0==self.name_texture['pointer'],'same current name texture');native_pointer=self.name_native
   if slot==56:
    need(args==[t['pointer'],0,bp-(52 if ret==0x403CBE else 36)],'original name descriptor ABI');op='describe';native=self.gpu.describe(native_pointer);result=copy.deepcopy(native);put(args[-1],bytes.fromhex(result['hex']))
   elif slot==64:
    need(args==[t['pointer'],0,self.get(bp+8),0,2048],'original name LockRect ABI');op='lock';native=self.gpu.lock(native_pointer);result=self.space.result('overlay',native);self.name_lock=result;raw=bytes.fromhex(result['hex']);put(result['bits'],raw);self.mutable.append((result['bits'],result['bits']+len(raw)));put(args[2],struct.pack('<II',result['pitch'],result['bits']))
   elif slot==68:
    need(args==[t['pointer'],0],'original name UnlockRect ABI');op='unlock';self.name_upload=self.read(self.name_lock['bits'],len(bytes.fromhex(self.name_lock['hex'])));native=self.gpu.unlock(native_pointer,self.name_upload);result=copy.deepcopy(native);self.name_readback=self.gpu.readback(native_pointer);need(self.name_readback['hex']==self.name_upload.hex(),'actual entire current name readback')
   else:need(args==[t['pointer']],'original name Release ABI');op='release';native=self.gpu.release(native_pointer);result=copy.deepcopy(native)
  value=result['count'] if slot==8 else result['hr'];need(value==0,'actual name COM success')
  self.name_leaves.append(dict(kind='GPU',index=len(self.name_gpu)));self.name_gpu.append(dict(slot=slot,target=at,sp=sp,return_va=ret,args=args,pop=pop,value=value,op=op,native_result=native,result=result,memory_outputs=outputs,actual_API_executed=True));self.return_api(sp,value,pop)
 def name_mark(self):return dict(instructions=self.name_instructions,writes=self.name_write_count,code_sha256=self.name_code_hash.hexdigest(),write_sha256=self.name_write_hash.hexdigest())
 def write_hook(self,uc,access,at,size,value,context):
  super().write_hook(uc,access,at,size,value,context)
  if self.name_active:self.name_write_count+=1;self.name_write_hash.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
 def code(self,uc,at,size,context):
  if self.name_active:
   if at==0x4CDE10:
    sp=self.getreg('ESP');self.name_pending=dict(entry=at,CPU=self.cpu(),receiver=self.getreg('ECX'),args=[self.get(sp+4),self.get(sp+8)],caller=self.get(sp),stack=self.read(STACK,0x20000).hex(),SEH=self.read(0,4).hex(),first_instruction_executed=False);uc.emu_stop();return
   if at==0x405869:
    sp=self.getreg('ESP');a=[self.get(sp+j) for j in range(0,24,4)];self.conversions.append(dict(entry=at,args=a,rect=list(struct.unpack('<4I',self.read(a[4],16))),point=list(struct.unpack('<2I',self.read(a[5],8)))))
   if at==0x403BD0 and not hasattr(self,'raster_boundary'):
    service=self.name_platform.service;raw=service.gdi.raster(service.bitmap)
    self.raster_boundary=dict(memory=self.snapshot(),CPU=self.cpu(),state=self.task_state(),trace=self.mark(),local_trace=self.name_mark(),raster_hex=raw.hex(),measured=service.measured,selected_face=service.face,ACP=service.gdi.acp,stages=copy.deepcopy(service.stages),calls=copy.deepcopy(self.name_calls))
   if at in self.gdi_targets:self.gdi_api(at);return
  super().code(uc,at,size,context)
  if self.name_active and at in ALLOWED:self.name_instructions+=1;self.name_code_hash.update(struct.pack('<I',at))
 def admission(self):
  a=super().admission();self.name_before=dict(memory=self.snapshot(),CPU=self.cpu(),state=self.task_state(),trace=self.mark(),GPU_wire=len(self.gpu.trace));self.name_active=True
  self.uc.ctl_remove_cache(self.font_target,self.font_target+1)
  try:self.uc.emu_start(self.font_target,RETURN,timeout=60_000_000,count=4_000_000)
  finally:self.name_active=False
  need(self.name_pending is not None,'natural original portrait loading entry')
  self.name_result=dict(before=self.name_before,raster=self.raster_boundary,pending=self.name_pending,memory=self.snapshot(),CPU=self.cpu(),state=self.task_state(),trace=self.mark(),local_trace=self.name_mark(),calls=copy.deepcopy(self.name_calls),GPU_APIs=copy.deepcopy(self.name_gpu),leaves=copy.deepcopy(self.name_leaves),conversions=self.conversions,texture=self.name_texture,lock=self.name_lock,upload_hex=self.name_upload.hex(),readback=self.name_readback,GYBC_readback=self.gpu.readback(self.texture_native),path=self.string(self.name_pending['args'][0]).decode('ascii'),accounting=self.get(0x765720),GDI_handle_projection=self.name_platform.space.ledger(),GDI_trace=copy.deepcopy(self.name_platform.trace),GPU_wire_end=len(self.gpu.trace))
  return a
 def resource_root(self,label,*args,**kwargs):
  if label=='supplemental_original_group20_destructor':
   self.name_cleaning=True
   try:
    mark=len(self.name_gpu);self.resource_root('supplemental_original_name_texture_destructor',0x403730,receiver=TEXTURE)
    self.name_cleanup=dict(GPU_APIs=copy.deepcopy(self.name_gpu[mark:]),texture_bytes=self.get(0x765720),GDI=self.name_platform.close())
   finally:self.name_cleaning=False
  return super().resource_root(label,*args,**kwargs)
 def run(self):
  try:r=super().run();r['terminal_name']=self.name_result;r['name_cleanup']=self.name_cleanup;return r
  finally:self.name_platform.close()

def source_contract():
 return dict(parent=parent.source_contract(),role_indices=[2,1],layer=5,measure_DC_field=MAIN+0xB208,measure_DC_before_first_original_instruction=True,actual_owned_GDI_and_GPU=True,original_IAT_rebindings=0,new_forward_game_roots=0,next_entry=0x4CDE10,extra_code=[dict(start=a,end=b,sha256=sha(CODE[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES])

def helpers(prefix='terminal-name'):
 a,aa=parent.parent.platform.build(ROOT/'tools/terminal_overlay_crt_platform.cs',prefix+'-crt');b,bb=parent.parent.platform.build(ROOT/'tools/terminal_overlay_d3d8_platform.cs',prefix+'-gpu');return a,b,dict(CRT=aa,GPU=bb)

def run_case(c,ch,gh,ticks=None):
 class Diagnostics:
  @staticmethod
  def save(path,data):return terminal.save(path.replace('terminal-overlay-diagnostic-','terminal-name-diagnostic-'),data)
 fn=types.FunctionType(parent.parent.run_case.__code__,dict(parent.parent.run_case.__globals__,OverlayMachine=NameMachine,terminal=Diagnostics),closure=parent.parent.run_case.__closure__)
 return fn(c,ch,gh,ticks)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case',type=int);a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable name report');ch,gh,b=helpers();rows=[]
 for c in (parent.parent.parent.corpus() if a.case is None else [parent.parent.parent.corpus()[a.case]]):
  r=run_case(c,ch,gh);rows.append(r);print('name source',c['name'],r['terminal_name']['path'],r['terminal_name']['raster']['measured'],flush=True)
 terminal.save(a.out,dict(schema_version=1,source_contract=source_contract(),helper_build=b,cases=rows,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False))
