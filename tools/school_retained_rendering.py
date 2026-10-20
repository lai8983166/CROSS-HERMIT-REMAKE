"""Source-initialized renderer reconstruction for retained logical VM checkpoints.

Initialization has declared fresh globals and runs before checkpoint logical-state
rehydration. Existing checkpoint files and expired platform handles are not edited.
"""
import hashlib,json,struct,sys
from contextlib import contextmanager
from tools.school_startup_return_emulation import ReturnEmulator,CALLER_PHASES,FONT_PHASES,PHASES,prefix
from tools.school_startup_return_platform import ReturnDevice,FinishGDI
from tools.school_renderer_init_emulation import REGISTERS,buffer_evidence
from tools.school_vm_graphics import TASK,ROOT,SOURCE,SOURCE_SHA256,BASE
from unicorn import UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EAX,UC_X86_REG_ECX
from collections import Counter
from tools.school_device_init_bridge import DeviceBridge

OLD_OWNER=0x20000000
FRESH_GLOBALS={0x7a49fc:0,0x80a398:0}

class RenderingDevice(DeviceBridge):
 def __init__(self,width=1024,height=768,version=2):
  super().__init__(ROOT/f'.venv-audit/school-retained-render-device-v{version}.exe',width,height)
 def _read(self):
  line=self.reader.submit(self.process.stdout.readline).result(timeout=30)
  if not line or len(line)>16*1024*1024:raise RuntimeError('bounded complete framebuffer response')
  return json.loads(line)

class AddressSpace:
 """Typed IPC pointer marshaling; native resources stay in their owning helper."""
 def __init__(self):self.native_to_guest={};self.guest_to_native={};self.next=0x40001000
 def guest(self,domain,pointer):
  if not pointer:return 0
  key=(domain,pointer)
  if key not in self.native_to_guest:
   if self.next>=0x70000000:raise ValueError('bounded interface address space exhausted')
   self.native_to_guest[key]=self.next;self.guest_to_native[self.next]=key;self.next+=0x100000
  return self.native_to_guest[key]
 def native(self,domain,pointer):
  if pointer not in self.guest_to_native:return pointer
  actual_domain,native=self.guest_to_native[pointer]
  if actual_domain!=domain:raise ValueError('cross-helper native pointer refused')
  return native
 def result(self,domain,value,key=None):
  if isinstance(value,dict):
   out={k:({slot:self.guest(domain,p) for slot,p in v.items()} if k=='methods' else self.result(domain,v,k)) for k,v in value.items()}
   if 'locked_hex' in out:
    b=bytearray.fromhex(out['locked_hex']);struct.pack_into('<I',b,4,out['bits']);out['locked_hex']=b.hex()
   return out
  if isinstance(value,list):return [self.result(domain,v) for v in value]
  if type(value)is int and key in ('pointer','vtable','bits','method_pointer'):return self.guest(domain,value)
  return value
 def ledger(self):return [dict(domain=d,native=p,guest=g) for (d,p),g in self.native_to_guest.items()]

class MappedPlatform:
 def __init__(self,platform,space,domain):
  self.platform,self.space,self.domain=platform,space,domain;self.trace=[];self.hello=platform.hello
 def request(self,op,**request):
  actual=dict(request)
  for key in ('pointer','object'):
   if key in actual:actual[key]=self.space.native(self.domain,actual[key])
  if op.endswith('_state') and actual.get('method')=='texture':
   actual['args']=list(actual['args']);actual['args'][1]=self.space.native(self.domain,actual['args'][1])
  if op=='render_call' and actual['slot'] in (61,83):
   actual['args']=list(actual['args']);actual['args'][1]=self.space.native(self.domain,actual['args'][1])
  result=self.platform.request(op,**actual);mapped=self.space.result(self.domain,result)
  self.trace.append(dict(op=op,request=request,result=mapped,native_request=actual,native_result=result))
  return mapped

@contextmanager
def owner_configuration():
 """Only Python bridge address configuration changes; original code/IAT retain identity."""
 changes=[]
 for name,mod in list(sys.modules.items()):
  if not name.startswith('tools.school_') or mod is None:continue
  for key,old,new in (('OWNER',OLD_OWNER,TASK),('MANAGER',OLD_OWNER+0x1058,TASK+0x1058)):
   if type(getattr(mod,key,None)) is int and getattr(mod,key)==old:
    changes.append((mod,key,old,new));setattr(mod,key,new)
 try:yield [dict(module=m.__name__,key=k,before=o,after=n) for m,k,o,n in changes]
 finally:
  for mod,key,old,new in reversed(changes):setattr(mod,key,old)

class RetainedStartup(ReturnEmulator):
 def __init__(self,bridge,platform,fill):
  self.continuing=False
  super().__init__(bridge,platform,fill)
  self.initial_loaded_image=self.initial_image(self.image)
  self.image=self.initial_loaded_image;self.uc.mem_write(BASE,self.image)
  self.initialization_declaration=dict(before_first_original_instruction=True,owner=TASK,globals={hex(a):self.read(a) for a in FRESH_GLOBALS},
   source_image_sha256=SOURCE_SHA256,loaded_image_sha256=hashlib.sha256(self.image).hexdigest(),original_code_modified=False,
   provenance='analysis/school-startup-inputs-v2-20261020.json',retained_checkpoint_not_loaded_yet=True)
  native_start=self.uc.emu_start
  flags=dict(ReturnEmulator=('return_running',),CallerEmulator=('caller_running',),FinishEmulator=('finish_running',),
   SecondGlyphEmulator=('second_glyph_running','second_pixel_running'),SecondResourceEmulator=('resource_running',),
   SecondEmulator=('second_running',),StateEmulator=('state_running',),PixelEmulator=('pixel_running',),
   GlyphEmulator=('glyph_running',),AtlasEmulator=('atlas_running',),SlotEmulator=('slot_running',),
   CacheEmulator=('cache_running',),TextureEmulator=('texture_running',),FontEmulator=('factory_running',))
  self.original_code_handlers=[(c,c.__dict__['_code']) for c in ReturnEmulator.__mro__ if '_code' in c.__dict__]
  def start(*args,**kwargs):
   self.fast_code_handler=next((fn for cls,fn in self.original_code_handlers if any(getattr(self,k,False) for k in flags.get(cls.__name__,()))),self.original_code_handlers[-2][1])
   return native_start(*args,**kwargs)
  self.uc.emu_start=start
 def initial_image(self,image):
  data=bytearray(image);original=SOURCE.read_bytes()
  for at,v in FRESH_GLOBALS.items():
   old=struct.unpack_from('<I',original,at-BASE)[0];actual=struct.unpack_from('<I',data,at-BASE)[0]
   # Later original cache publication is preserved; only inherited snapshot
   # values in an expected fresh image are adapted to declared loader inputs.
   if actual==old:struct.pack_into('<I',data,at-BASE,v)
  return bytes(data)
 def call(self,va,args=(),receiver=None):
  return super().call(va,args,receiver=TASK if receiver is None else receiver)
 def check(self,owner,image,seh):
  return super().check(owner,self.initial_image(image),seh)
 def construct(self):
  result=super().construct();self.constructed_image=self.initial_image(self.constructed_image);return result
 def _code(self,uc,at,size,user):
  if self.continuing:return self.continuation_code(uc,at,size)
  return self.fast_code_handler(self,uc,at,size,user)
 def _write(self,uc,access,at,size,value,user):
  if not self.continuing:return super()._write(uc,access,at,size,value,user)
  if BASE<=at<0x592000:raise ValueError('continuation attempted original code write')
  self.vm_write_hash.update(struct.pack('<IIQ',at,size,value&0xffffffffffffffff));self.vm_write_count+=1
 def _slot_read(self,uc,access,at,size,value,user):
  if not self.continuing:return super()._slot_read(uc,access,at,size,value,user)
 def map_missing(self,at,n):
  cursor=at&~4095;end=(at+n+4095)&~4095
  for a,b,_ in sorted(self.uc.mem_regions()):
   if b<cursor:continue
   if a>=end:break
   if cursor<a:self.uc.mem_map(cursor,min(a,end)-cursor)
   cursor=max(cursor,b+1)
   if cursor>=end:return
  if cursor<end:self.uc.mem_map(cursor,end-cursor)
 def rehydrate(self,payload,checkpoint):
  # Source-created renderer fields, font/cache globals and constructor-owned
  # tables survive logical-state rehydration. No owner/gate scalar is invented.
  regions=[('original_manager_fonts',TASK+0x1058,0x60),('original_renderer',TASK+0xb180,0x8a0),
   ('original_constructor_table',0x765728,0x2c002),('original_timer',0x799ae0,16),
   ('original_constructor_scalar',0x5ff530,4),('original_CRT_counter',0x79fc74,4),('original_cache_head',0x80a398,4)]
  overlays=[dict(name=name,pointer=a,bytes=n,hex=bytes(self.uc.mem_read(a,n)).hex()) for name,a,n in regions]
  proofs=[]
  for start,raw in payload['memory']:
   expected=bytearray(raw)
   for row in overlays:
    a=max(start,row['pointer']);b=min(start+len(raw),row['pointer']+row['bytes'])
    if a<b:expected[a-start:b-start]=bytes.fromhex(row['hex'])[a-row['pointer']:b-row['pointer']]
   self.map_missing(start,len(raw));self.uc.mem_write(start,bytes(expected))
   actual=bytes(self.uc.mem_read(start,len(raw)))
   if actual!=expected:raise ValueError('retained logical-state reconstruction mismatch')
   proofs.append(dict(pointer=start,bytes=len(raw),parent_sha256=hashlib.sha256(raw).hexdigest(),reconstructed_sha256=hashlib.sha256(actual).hexdigest()))
  self.uc.context_restore(payload['cpu'])
  from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
  from tools.school_world_mode_emulation import architectural_cpu
  reference=Uc(UC_ARCH_X86,UC_MODE_32);reference.context_restore(payload['cpu'])
  architectural_expected=architectural_cpu(reference);architectural_actual=architectural_cpu(self.uc)
  if architectural_actual!=architectural_expected:raise ValueError('full typed original CPU context was not restored')
  actual={k:self.uc.reg_read(r) for k,r in REGISTERS.items()};old={k:payload['cpu'].reg_read(r) for k,r in REGISTERS.items()}
  if actual!=old or actual['EIP']!=0x40e2a0 or self.read(TASK+0x1058)!=TASK:raise ValueError('retained original CPU/stack or source-created ownership lost')
  self.reconstruction=dict(checkpoint=checkpoint,cpu_before=old,cpu_after=actual,overlays=overlays,full_parent_maps=proofs,
   logical_rehydration=True,original_checkpoint_modified=False,in_place_unmodified_checkpoint_resume=False,
   owner_and_gate_written_by_original_initialization=True,source_derived_owner=self.read(TASK+0x1058),source_derived_gate=self.read(TASK+0xb28e)&65535,
   architectural_restore_recheck=dict(expected=architectural_expected,actual=architectural_actual,not_the_initial_snapshot=False))
  return self.reconstruction
 def prepare_rendering(self):
  ptr=self.objects['device']['pointer'];r=self.bridge.request('render_prepare',pointer=ptr)
  self.render_methods={}
  for key in ('device','first_buffer','second_buffer'):
   identity=r[key];self._identity('render_'+key,identity)
   for offset,target in identity['methods'].items():self.render_methods.setdefault(target,[]).append((key,int(offset)//4,identity['pointer']))
  return r
 def continuation_code(self,uc,at,size):
  if at in self.vm_stops:self.vm_boundary=at;uc.emu_stop();return
  sp=self.read_register('ESP')
  if hasattr(self,'text_imports') and at in self.text_imports:
   name,pop=self.text_imports[at];args=[self.read(sp+4+i*4) for i in range(pop//4)]
   result,row=self.text_gdi.invoke(self,name,args)
   self.vm_apis.append(dict(va=at,key='textGDI',sp=sp,return_va=self.read(sp),call=row))
   return self.platform_return(sp,result,pop)
  if at in self.render_methods:
   candidates=[x for x in self.render_methods[at] if x[2]==self.read(sp+4)]
   if len(candidates)!=1:raise ValueError('ambiguous native interface receiver')
   key,slot,ptr=candidates[0]
   if key=='text_texture' or key=='device' and slot==20:return self.text_api(at,sp,key,slot,ptr)
   return self.render_api(at,sp,key,slot,ptr)
  if at==0x424f80 or not BASE<=at<0x592000:
   self.vm_pending=dict(va=at,cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()},stack_hex=bytes(uc.mem_read(sp,48)).hex());uc.emu_stop();return
  actual=bytes(uc.mem_read(at,size));expected=self.original_code[at-BASE:at-BASE+size]
  if actual!=expected:raise ValueError('continuation source instruction bytes changed '+hex(at))
  self.vm_instructions[at]+=1;self.vm_instruction_hash.update(struct.pack('<I',at)+actual)
 def read_register(self,name):return self.uc.reg_read(REGISTERS[name])
 def platform_return(self,sp,result,pop):
  self.uc.reg_write(UC_X86_REG_EAX,result&0xffffffff);self.uc.reg_write(UC_X86_REG_ESP,sp+4+pop);self.uc.reg_write(UC_X86_REG_EIP,self.read(sp))
 def bind_text(self,gdi):
  from tools.school_font_raster_emulation import IMPORTS
  self.text_gdi=gdi;self.text_imports={}
  for slot,(name,caller,pop) in IMPORTS.items():self.text_imports[self.read(slot)]=(name,pop)
  for slot,name,pop in [(0x5920c4,'DeleteObject',4),(0x592060,'DeleteDC',4)]:self.text_imports[self.read(slot)]=(name,pop)
  # Device's CreateTexture is an actual original vtable entry. Its metadata
  # was already observed in startup; query its real identity for dispatch.
  identity=self.objects['device'];target=self.read(self.read(identity['pointer'])+20*4)
  self.render_methods.setdefault(target,[]).append(('device',20,identity['pointer']))
 def text_api(self,at,sp,key,slot,pointer):
  count=8 if key=='device' else {2:1,14:3,16:5,17:2}[slot]
  args=[self.read(sp+4+i*4) for i in range(count)];extra={}
  if key=='device':
   _,w,h,levels,usage,fmt,pool,out=args
   op='text_create';request=dict(pointer=pointer,width=w,height=h,levels=levels,usage=usage,format=fmt,pool=pool)
  elif slot==14:op='text_desc';request=dict(pointer=pointer)
  elif slot==16:op='text_lock';request=dict(pointer=pointer,level=args[1],rect=args[3],flags=args[4])
  elif slot==17:
   lock=self.text_locks[pointer];op='text_unlock';request=dict(pointer=pointer,level=args[1],hex=bytes(self.uc.mem_read(lock['bits'],lock['bytes'])).hex())
  else:op='text_release';request=dict(pointer=pointer)
  result=self.bridge.request(op,**request)
  if key=='device' and result['hr']>=0:
   identity=result['texture'];self._identity('text_'+str(identity['pointer']),identity)
   for offset,target in identity['methods'].items():self.render_methods.setdefault(target,[]).append(('text_texture',int(offset)//4,identity['pointer']))
   self.uc.mem_write(out,struct.pack('<I',identity['pointer']))
  elif slot==14 and result['hr']>=0:self.uc.mem_write(args[2],bytes.fromhex(result['hex']))
  elif slot==16 and result['hr']>=0:
   if not hasattr(self,'text_locks'):self.text_locks={}
   data=bytes.fromhex(result['before_hex']);result['bytes']=len(data);self.text_locks[pointer]=result
   self.map_missing(result['bits'],len(data));self.uc.mem_write(result['bits'],data);self.uc.mem_write(args[2],bytes.fromhex(result['locked_hex']))
  self.vm_apis.append(dict(va=at,key=key,slot=slot,sp=sp,return_va=self.read(sp),args=args,op=op,request=request,result=result))
  self.platform_return(sp,result['hr'] if 'hr' in result else result['count'],len(args)*4)
 def render_api(self,at,sp,key,slot,pointer):
  counts={3:0,15:4,34:0,35:0,36:6,37:2,40:1,50:2,54:1,55:1,61:2,63:3,70:3,72:4,76:1,83:3,88:1}
  count=counts[slot] if key=='device' else 4 if slot==11 else 0
  args=[self.read(sp+4+i*4) for i in range(count+1)]
  if args[0]!=pointer:raise ValueError('source native interface receiver mismatch')
  buffers=[]
  if key=='device':
   if slot==72:
    vertices={1:args[2],2:args[2]*2,3:args[2]+1,4:args[2]*3,5:args[2]+2,6:args[2]+2}[args[1]]
    buffers=[dict(index=2,hex=bytes(self.uc.mem_read(args[3],vertices*args[4])).hex())]
   if slot==36 and args[1]:buffers=[dict(index=1,hex=bytes(self.uc.mem_read(args[2],args[1]*16)).hex())]
   if slot==37:buffers=[dict(index=1,hex=bytes(self.uc.mem_read(args[2],64)).hex())]
   if slot==40:buffers=[dict(index=0,hex=bytes(self.uc.mem_read(args[1],24)).hex())]
   request=dict(pointer=pointer,slot=slot,args=args[1:],buffers=buffers);op='render_call'
  elif slot==11:
   request=dict(pointer=pointer,offset=args[1],size=args[2],flags=args[4]);op='render_vb_lock'
  else:
   request=dict(pointer=pointer,hex=bytes(self.uc.mem_read(self.vm_lock['bits'],self.vm_lock['bytes'])).hex());op='render_vb_unlock'
  r=self.bridge.request(op,**request)
  if key!='device' and slot==11 and r['hr']>=0:
   self.vm_lock=r;bits=r['bits'];data=bytes.fromhex(r['before_hex']);self.map_missing((bits&~4095)-4096,len(data)+12288);self.uc.mem_write(bits,data);self.uc.mem_write(args[3],struct.pack('<I',bits))
  self.vm_apis.append(dict(va=at,key=key,slot=slot,sp=sp,return_va=self.read(sp),args=args,op=op,request=request,result=r))
  self.uc.reg_write(UC_X86_REG_EAX,r['hr']&0xffffffff);self.uc.reg_write(UC_X86_REG_ESP,sp+4+len(args)*4);self.uc.reg_write(UC_X86_REG_EIP,self.read(sp))
 def continue_vm(self,stop):
  self.vm_stops={stop};self.vm_pending=None;self.vm_boundary=None;self.vm_instructions=Counter();self.vm_apis=[]
  self.vm_write_hash=hashlib.sha256();self.vm_write_count=0;self.vm_instruction_hash=hashlib.sha256();self.original_code=SOURCE.read_bytes();before={k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
  self.continuing=True
  try:self.uc.emu_start(before['EIP'],0,count=2000000,timeout=120_000_000)
  finally:self.continuing=False
  return dict(before_cpu=before,cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()},boundary=self.vm_boundary,pending=self.vm_pending,
   instruction_counts=[dict(va=a,count=n) for a,n in sorted(self.vm_instructions.items())],instruction_sha256=self.vm_instruction_hash.hexdigest(),
   writes=self.vm_write_count,write_sha256=self.vm_write_hash.hexdigest(),api_calls=self.vm_apis)

def initialize(e,bridge,platform,fill=0xa5):
 c=prefix(e,bridge,platform,fill)
 c['glyph_raster']=e.resume_glyphs(c['GDI_preparation']);c['pixel_upload']=e.resume_pixels(c['glyph_raster'])
 for phase in ('cleanup','vertex','states'):c['font_'+phase]=e.resume_state(phase,c['pixel_upload'] if phase=='cleanup' else c['font_'+('cleanup' if phase=='vertex' else 'vertex')])
 previous=c['font_states']
 for phase in ('loop','constructor','atlas'):c['second_'+phase]=e.resume_second(phase,previous);previous=c['second_'+phase]
 for phase in ('texture','gdi'):c['second_'+phase]=e.resume_resource(phase,previous);previous=c['second_'+phase]
 c['DIB_retirement']=e.retire_first_DIB(previous,c['font_cleanup']);c['second_raster']=e.second_raster(c['DIB_retirement']);c['second_upload']=e.second_upload(c['second_raster']);previous=c['second_upload']
 for phase in FONT_PHASES:c['finish_'+phase]=e.finish(phase,previous);previous=c['finish_'+phase]
 for phase in CALLER_PHASES:c['caller_'+phase]=e.resume_caller(phase,previous);previous=c['caller_'+phase]
 c['gamma_admission']=e.prepare_gamma(previous);previous=c['gamma_admission']
 for phase in PHASES:c['startup_'+phase]=e.resume_return(phase,previous);previous=c['startup_'+phase]
 return c

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh evidence path required')
 result=None
 with owner_configuration() as configuration:
  with ReturnDevice(1024,768) as bridge:
   with FinishGDI() as platform:
    space=AddressSpace();db=MappedPlatform(bridge,space,'device');gp=MappedPlatform(platform,space,'GDI')
    e=RetainedStartup(db,gp,0xa5);c=initialize(e,db,gp)
    result=dict(owner_configuration=configuration,initialization_declaration=e.initialization_declaration,startup=c,platform_trace=gp.trace,device_proxy_trace=db.trace,address_translation=space.ledger(),
     final_owner=buffer_evidence(bytes(e.uc.mem_read(TASK,0xc000))),final_cpu={k:e.uc.reg_read(v) for k,v in REGISTERS.items()})
   result['platform_cleanup']=platform.cleanup
  result.update(device_trace=bridge.trace,device_cleanup=bridge.cleanup)
 out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
 print('original startup initialized retained-address game owner and all renderer resources',flush=True)
