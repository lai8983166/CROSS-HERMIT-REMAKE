"""Natural first-line font/GDI raster to pending original texture creation."""
import argparse,ctypes as C,hashlib,json,struct
from copy import deepcopy
from tools.school_text_preparation_emulation import *
from tools.school_gdi_platform import WindowsGDI

TEXT_REPORT=ROOT/'analysis/school-text-preparation-v1-20261012.json'
TEXT_SHA='fca8be507e3fa52273cf14db51f325c2fa70395e31b4a8b855a664112e50856a'
RASTER=0x10100000
RASTER_BYTES=0x100000
TEXTURE=OBJECT+0x28
NATIVE_RASTER=((0x4CAD09,0x4CAD7C),(0x4077C0,0x407823),(0x4142B0,0x4142DD),
 (0x408E30,0x408E93),(0x405160,0x405779),(0x403730,0x4037EF))
RASTER_CODE=frozenset(a for lo,hi in NATIVE_RASTER for a in range(lo,hi))
# Import binding, exact source caller, and stdcall byte cleanup.
IMPORTS={0x5920A0:('CreateFontA',0x4CAD09,56),0x5922C4:('lstrlenA',None,4),
 0x5920A4:('SelectObject',None,8),0x5920BC:('GetTextExtentPoint32A',0x405246,16),
 0x592094:('CreateCompatibleDC',0x405373,4),0x592098:('CreateDIBSection',0x4053CC,24),
 0x59209C:('SetMapMode',0x40545D,8),0x592084:('GetStockObject',0x405471,4),
 0x592088:('PatBlt',0x4054AC,24),0x59208C:('SetBkMode',0x405508,8),
 0x5920B4:('SetBkColor',0x405520,8),0x5920B8:('SetTextAlign',0x405535,8),
 0x5920B0:('SetTextColor',None,8),0x592090:('TextOutA',None,20)}
API={0xE300000 if slot==0x5920A0 else 0xE300100+16*i:(slot,*value) for i,(slot,value) in enumerate(IMPORTS.items())}

def read_text_parent():
 raw=TEXT_REPORT.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=TEXT_SHA:raise ValueError('font pinned text identity')
 return json.loads(raw)

class SchoolFontRasterEmulator(SchoolTextPreparationEmulator):
 def __init__(self):
  self.raster_loading=False
  super().__init__()

 def _write_hook(self,uc,access,address,size,value,context):
  if not self.raster_loading:return super()._write_hook(uc,access,address,size,value,context)
  if not any(a<=address and address+size<=b for a,b in self.raster_allowed):raise RuntimeError(f'raster finite guard {address:#x}/{size}')

 def _raster_write(self,address,raw):
  self._write_hook(self.uc,0,address,len(raw),0,None);self.uc.mem_write(address,raw)

 def _font_api(self,address,sp):
  slot,name,caller,pop=API[address];ret=self.read(sp);args=[self.read(sp+4+i*4) for i in range(pop//4)]
  if caller is not None and ret!=caller:raise RuntimeError('raster exact import caller')
  g=self.platform;extra={}
  if name=='CreateFontA':
   if args!=self.raster_parent['pending_font']['args']:raise RuntimeError('raster font input')
   result=g.font(args[:-1],self.bounded_text(args[-1]));self.font_handle=result
  elif name=='lstrlenA':
   if ret not in (0x4051BA,0x405230,0x405676,0x4056C7) or args!=[self.local_text]:raise RuntimeError('raster string length caller/source')
   result=len(self.bounded_text(args[0]))
  elif name=='SelectObject':
   expected={0x4051EA:[self.measure_dc,self.font_handle],0x40528A:[self.measure_dc,self.old_measure_font],
    0x40541B:[self.raster_dc,self.bitmap],0x405485:[self.raster_dc,self.brush],0x4054C6:[self.raster_dc,self.font_handle]}
   if ret not in expected or args!=expected[ret]:raise RuntimeError('raster exact object selection')
   result=g.select(*args)
   if ret==0x4051EA:self.old_measure_font=result
  elif name=='GetTextExtentPoint32A':
   frame=self.uc.reg_read(UC_X86_REG_EBP)
   if args!=[self.measure_dc,self.local_text,len(self.text_raw),frame-0x54]:raise RuntimeError('raster text extent inputs')
   size,face=g.measure(self.measure_dc,self.text_raw);self.measured=size;self.selected_face=face
   self._raster_write(args[3],struct.pack('<2i',*size));result=1;extra={'measured':size,'selected_face':face}
  elif name=='CreateCompatibleDC':
   if args!=[0]:raise RuntimeError('raster private DC input')
   result=g.dc();self.raster_dc=result
  elif name=='CreateDIBSection':
   frame=self.uc.reg_read(UC_X86_REG_EBP)
   if args!=[self.raster_dc,frame-0x38,0,frame-0x3C,0,0]:raise RuntimeError('raster DIB input')
   header=bytes(self.uc.mem_read(args[1],40));result=g.dib(self.raster_dc,header);self.bitmap=result
   self._raster_write(args[3],struct.pack('<I',RASTER));extra={'header_hex':header.hex(),'virtual_bits_pointer':RASTER}
  elif name=='GetStockObject':
   if args!=[4]:raise RuntimeError('raster source brush')
   result=g.handle(g.g.GetStockObject(4));self.brush=result
  elif name=='PatBlt':
   w,h=g.bitmaps[self.bitmap]['size']
   if args!=[self.raster_dc,0,0,w,h,0xF00021]:raise RuntimeError('raster exact bitmap clear')
   result=int(g.g.PatBlt(*args))
   if result!=1:raise RuntimeError('real GDI clear failed')
  elif name in ('SetMapMode','SetBkMode','SetBkColor','SetTextAlign','SetTextColor'):
   expected={'SetMapMode':[self.raster_dc,1],'SetBkMode':[self.raster_dc,1],
    'SetBkColor':[self.raster_dc,0],'SetTextAlign':[self.raster_dc,0]}
   if name=='SetTextColor':
    if ret not in (0x405663,0x4056B4):raise RuntimeError('raster text color caller')
    want=[self.raster_dc,0x80808 if ret==0x405663 else 0xFFFFFF]
   else:want=expected[name]
   if args!=want:raise RuntimeError('raster state inputs')
   result=int(getattr(g.g,name)(*args))
   if name in ('SetMapMode','SetBkMode') and not result or name in ('SetBkColor','SetTextAlign','SetTextColor') and result==0xFFFFFFFF:raise RuntimeError('real GDI state call failed')
  elif name=='TextOutA':
   pad=max(1,min(3,self.measured[1]//10));point=[2*pad,2*pad] if ret==0x40569C else [pad,pad]
   if ret not in (0x40569C,0x4056E7) or args!=[self.raster_dc,*point,self.local_text,len(self.text_raw)]:raise RuntimeError('raster exact text drawing')
   result=int(g.g.TextOutA(args[0],args[1],args[2],self.text_raw,args[4]))
   if result!=1:raise RuntimeError('real GDI text drawing failed')
  else:raise RuntimeError('raster unsupported host API')
  self.api_records.append({'name':name,'slot':hex(slot),'return_va':hex(ret),'args':args,'result':result,**extra})
  self._stub_return(result,pop)

 def _hook(self,uc,address,size,context):
  if not self.raster_loading:return super()._hook(uc,address,size,context)
  sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
  if address in API:return self._font_api(address,sp)
  if address==0x56D810:
   target,source=self.read(sp+4),self.read(sp+8);frame=uc.reg_read(UC_X86_REG_EBP)
   if ret!=0x4CAD23 or (target,source)!=(frame-0x110,self.raster_parent['split']['lines'][0]['pointer']):raise RuntimeError('raster exact text copy')
   raw=self.bounded_text(source);self.local_text=target;self.text_raw=raw
   self._raster_write(target,raw+b'\0');self.crt_records.append({'name':'bounded_source_copy','target':target,'source':source,'hex':raw.hex(),'return_va':hex(ret)})
   self._stub_return(len(raw),0);return
  if address==0x56CEC0:
   frame=uc.reg_read(UC_X86_REG_EBP);args=[self.read(sp+i) for i in (4,8,12)]
   if (ret,args)!=(0x40533D,[frame-0x38,0,40]):raise RuntimeError('raster exact DIB zero')
   self._raster_write(args[0],bytes(40));self._stub_return(args[0],0);return
  if address==0x414440:
   if ret!=0x4051D7 or recv!=self.graphics:raise RuntimeError('raster measurement context acquisition')
   self.measure_dc=self.platform.dc();self._stub_return(self.measure_dc,0);return
  if address==0x403BD0:
   if (ret,recv,[self.read(sp+4),self.read(sp+8)])!=(0x405779,TEXTURE,[self.device,0]):raise RuntimeError('raster pending original texture caller')
   self.pending_texture={'va':hex(address),'receiver':recv,'args':[self.device,0],'return_va':hex(ret),'first_instruction_executed':False,'natural_stack_verified':True}
   uc.emu_stop();return
  if address in RASTER_CODE:self.visited.add(address);return
  if address==0x56CE80:return super()._hook(uc,address,size,context)
  raise RuntimeError(f'raster unsupported original instruction {address:#x}')

 def run_font_raster(self,parent):
  if self.raster_loading or self.uc.reg_read(UC_X86_REG_EIP)!=0xE300000:raise RuntimeError('actual pending font CPU required')
  sp=self.uc.reg_read(UC_X86_REG_ESP)
  if self.read(sp)!=0x4CAD09 or [self.read(sp+4+i*4) for i in range(14)]!=parent['pending_font']['args']:raise RuntimeError('actual pending font stack required')
  self.raster_parent=parent;self.graphics=self.read(0x7A49FC);self.device=self.read(self.graphics+0xB210)
  if self.read(TEXTURE+0x2C) or self.read(TEXTURE+0x30) or not self.graphics:raise RuntimeError('raster empty source texture/context required')
  self.uc.mem_map(RASTER,RASTER_BYTES)
  bindings=[]
  for api,(slot,name,_,_) in API.items():
   bindings.append({'slot':hex(slot),'before':self.read(slot),'bound':api,'name':name});self.write(slot,api)
  self.raster_allowed=[(STACK,STACK+65536),(TEXTURE+0x28,TEXTURE+0x44),(TEXTURE+0x4C,TEXTURE+0x50),(TEXTURE+0x64,TEXTURE+0x68),(RASTER,RASTER+RASTER_BYTES)]
  before=self.script_regions();retained=self.capture_scene_memory(self.raster_allowed[1:]);null=bytes(self.uc.mem_read(0,4))
  self.raster_loading=True;self.api_records=[];self.crt_records=[];self.pending_texture=None
  self.measure_dc=self.raster_dc=self.bitmap=self.font_handle=self.old_measure_font=self.brush=0
  self.platform=WindowsGDI();result=None
  try:
   # The previous run ended at this exact address. Invalidate Unicorn's cached
   # exit translation so the natural CPU frame can now execute its API hook.
   self.uc.ctl_remove_cache(0xE300000,0xE300001)
   self.uc.emu_start(0xE300000,RETURN,timeout=5_000_000,count=100000)
   if self.pending_texture is None:raise RuntimeError(f'natural texture boundary not reached: EIP={self.uc.reg_read(UC_X86_REG_EIP):#x}, APIs={self.api_records}')
   raw=self.platform.raster(self.bitmap);self._raster_write(RASTER,raw)
   if bytes(self.uc.mem_read(0,4))!=null:raise RuntimeError('raster null retention')
   result={'inputs':{'graphics_context':self.graphics,'device':self.device,'import_bindings':bindings,'host_ansi_code_page':self.platform.acp,
    'platform':'real_host_GDI_offscreen_measurement_DC','parent_text_sha256':TEXT_SHA},'before':before,'after':self.script_regions(),
    'font_api':self.api_records,'crt':self.crt_records,'measured':self.measured,'selected_face':self.selected_face,
    'text_hex':self.text_raw.hex(),'raster':{'pointer':RASTER,'size':self.platform.bitmaps[self.bitmap]['size'],'hex':raw.hex(),'sha256':hashlib.sha256(raw).hexdigest()},
    'pending_texture':self.pending_texture,'font_api_executed':True,'original_raster_geometry_executed':True,'real_offscreen_GDI_drawing':True,
    'original_gpu_executed':False,'texture_creation_executed':False,'text_record_completed':False,'text_readiness_executed':False,
    'natural_VM_returned':False,'dialogue_playback_completed':False,'waves_executed':False,'full_task_wrapper_executed':False,'world_update_loop_executed':False,
    **self.verify_scene_memory(retained)}
  finally:
   cleanup=self.platform.close();self.raster_loading=False
   if result is not None:result['platform_cleanup']=cleanup
  return result

def report():
 parents=(parent_evidence(),read_deployment(),read_opening(),read_entry(),read_preflight(),read_script_opening(),read_parent());text=read_text_parent();cases=[]
 for i in range(3):
  name,sha=CHECKPOINTS[i];raw=(ROOT/f'.venv-audit/formation-actual-checkpoint-{i}.pkl').read_bytes()
  if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('raster actual checkpoint identity')
  payload=pickle.loads(raw)
  if payload['source_sha']!=SOURCE_SHA256 or payload['evidence_kind']!='private_actual_cpu_after_full35_before_placement':raise ValueError('raster actual checkpoint provenance')
  e=SchoolFontRasterEmulator();e.__dict__.update({k:v for k,v in payload['state'].items() if k!='uc' and not k.startswith('_audit_')})
  for at,data in payload['memory']:e.uc.mem_write(at,data)
  e.uc.context_restore(payload['cpu']);original=e.uc.emu_start
  def bounded_start(begin,end,timeout=0,count=0):
   if (begin,timeout,count)==(0x468A49,30_000_000,4_000_000):timeout=120_000_000
   return original(begin,end,timeout=timeout,count=count)
  e.uc.emu_start=bounded_start
  try:
   for fn,key,parent in zip((e.run_placement,e.run_deployment_tail,e.run_initialization_and_opening,e.run_entry_control,e.run_script_preflight,e.run_script_opening,e.run_board_opening),
    ('formation_placement','deployment_tail','scene_opening','entry_control','script_preflight','script_opening','board_opening'),parents):
    if fn()!=parent['cases'][i][key]:raise ValueError('raster complete parent mismatch')
    print('Parent '+name+'/'+key+': complete frozen equality',flush=True)
  finally:e.uc.emu_start=original
  c={'name':name,'provenance':{'checkpoint_sha256':sha,'parent_board_sha256':PARENT_SHA,'complete_parent_stages_equal':True,
   'deployment_timeout_us':120000000,'deployment_instruction_limit':4000000,'upstream_rerun':False}}
  p=e.run_text_preparation()
  if p!=text['cases'][i]['text_preparation']:raise ValueError('font complete text parent mismatch')
  c['provenance']['parent_text_sha256']=TEXT_SHA;c['provenance']['complete_parent_stages']=8
  c['font_raster']=e.run_font_raster(p);cases.append(c)
  print('Native font/raster '+c['name']+': real GDI, pending texture creation',flush=True)
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,'inherited_refusals':deepcopy(text['inherited_refusals']),
  'boundary':'Real host ANSI GDI/offscreen raster; original texture creation/GPU/text completion/readiness/VM/dialogue/world/waves remain pending.',**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use new immutable path')
 path.write_text(report_text(report()),encoding='utf-8',newline='\n')
