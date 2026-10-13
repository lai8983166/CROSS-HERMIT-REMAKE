"""Real original character-name raster with prior dialogue textures alive."""
from tools.school_character_prefix_emulation import *
from tools.school_character_name_catalog import (
 name_rules,expected_raster,pending_texture,RASTER as NAME_RASTER,TEXTURE as NAME_TEXTURE,PREFIX_SHA)

class SchoolCharacterNameEmulator(SchoolCharacterPrefixEmulator):
 def __init__(self):
  self.name_loading=False;super().__init__()

 def _write_hook(self,uc,access,address,size,value,context):
  if not self.name_loading:return super()._write_hook(uc,access,address,size,value,context)
  if not any(a<=address and address+size<=b for a,b in self.name_allowed):raise RuntimeError(f'name raster finite write {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')

 def _font_api(self,address,sp):
  if not self.name_loading or address!=FONT_API:return SchoolFontRasterEmulator._font_api(self,address,sp)
  args=[self.read(sp+4+i*4) for i in range(14)];ret=self.read(sp)
  if ret!=0x4CA7CB or args!=name_rules()['prefix']['font_args']:raise RuntimeError('name exact real font request')
  self.font_handle=self.platform.font(args[:-1],self.bounded_text(args[-1]))
  self.api_records.append({'name':'CreateFontA','slot':'0x5920a0','return_va':hex(ret),'args':args,'result':self.font_handle})
  self._stub_return(self.font_handle,56)

 def _hook(self,uc,address,size,context):
  if not self.name_loading:return super()._hook(uc,address,size,context)
  if address==0x56D810:
   sp=uc.reg_read(UC_X86_REG_ESP);frame=uc.reg_read(UC_X86_REG_EBP);target,source=self.read(sp+4),self.read(sp+8)
   if (self.read(sp),target,source)!=(0x4CA7F0,frame-0x108,name_rules()['prefix']['name']['pointer']):raise RuntimeError('name exact source copy')
   raw=self.bounded_text(source);self.local_text=target;self.text_raw=raw;self._raster_write(target,raw+b'\0')
   self.crt_records.append({'name':'bounded_source_copy','target':target,'source':source,'hex':raw.hex(),'return_va':'0x4ca7f0'})
   self._stub_return(target,0);return
  if 0x4CA7CB<=address<0x4CA82C:self.visited.add(address);return
  return SchoolFontRasterEmulator._hook(self,uc,address,size,context)

 def run_name_raster(self,prefix):
  if self.uc.reg_read(UC_X86_REG_EIP)!=FONT_API or self.name_loading or not self.live_loading or self.bridge.closed:raise RuntimeError('actual live name font required')
  sp=self.uc.reg_read(UC_X86_REG_ESP)
  if self.read(sp)!=0x4CA7CB or self.script_regions()!=prefix['after']:raise RuntimeError('actual name font parent')
  self.raster_parent=prefix;self.raster_address=NAME_RASTER;self.font_texture_address=NAME_TEXTURE
  self.graphics=self.read(0x7A49FC);self.device=self.read(self.graphics+0xB210)
  if self.device!=self.bridge.device['pointer'] or self.read(NAME_TEXTURE+0x2C) or self.read(NAME_TEXTURE+0x30):raise RuntimeError('name empty texture/live device')
  self.uc.mem_map(NAME_RASTER,RASTER_BYTES);bindings=[]
  for api,(slot,name,_,_) in API.items():
   bindings.append({'slot':hex(slot),'before':self.read(slot),'bound':api,'name':name});self.write(slot,api)
  self.name_allowed=[(STACK,STACK+65536),(CHARACTER_NODE+0x5C,CHARACTER_NODE+0x60),(NAME_TEXTURE+0x28,NAME_TEXTURE+0x44),
   (NAME_TEXTURE+0x4C,NAME_TEXTURE+0x50),(NAME_TEXTURE+0x64,NAME_TEXTURE+0x68),(NAME_RASTER,NAME_RASTER+RASTER_BYTES)]
  before=self.script_regions();retained=self.capture_scene_memory(self.name_allowed[1:])
  self.name_loading=True;self.raster_loading=True;self.api_records=[];self.crt_records=[];self.pending_texture=None
  self.measure_dc=self.raster_dc=self.bitmap=self.font_handle=self.old_measure_font=self.brush=0
  try:
   self.uc.ctl_remove_cache(FONT_API,FONT_API+1);self.uc.emu_start(FONT_API,RETURN,timeout=5_000_000,count=100000)
   if self.pending_texture is None:raise RuntimeError('name pending texture not reached')
   raw=self.platform.raster(self.bitmap);self._raster_write(NAME_RASTER,raw)
   derived=expected_raster(before,self.measured,self.graphics,self.font_handle)
   if self.script_regions()!=derived['after']:raise RuntimeError('name independent complete raster state')
   entry={'sp':self.uc.reg_read(UC_X86_REG_ESP),'ebp':self.uc.reg_read(UC_X86_REG_EBP),'return_va':self.read(self.uc.reg_read(UC_X86_REG_ESP))}
   if entry!=pending_texture(prefix):raise RuntimeError('name exact original texture stack '+repr(entry))
   pixels=[self.bridge.readback(t['pointer']) for t in self.resource_textures]
   if pixels!=self.resource_pixels:raise RuntimeError('name both old textures retained')
   return {'before':before,'after':self.script_regions(),'inputs':{'graphics_context':self.graphics,'device':self.device,'host_ansi_code_page':self.platform.acp,
    'platform':'real_host_GDI_offscreen_measurement_DC','parent_prefix_sha256':PREFIX_SHA,'import_bindings':bindings},
    'font_api':deepcopy(self.api_records),'crt':deepcopy(self.crt_records),'measured':self.measured,'selected_face':self.selected_face,'text_hex':self.text_raw.hex(),
    'raster':{'pointer':NAME_RASTER,'size':self.platform.bitmaps[self.bitmap]['size'],'hex':raw.hex(),'sha256':hashlib.sha256(raw).hexdigest()},
    'pending_texture':self.pending_texture,'entry':entry,'prior_actual_readbacks':pixels,'real_name_font_and_raster_executed':True,
    'name_texture_created':False,'image_load_executed':False,'GPU_draw_or_present_executed':False,**self.verify_scene_memory(retained)}
  finally:self.name_loading=False;self.raster_loading=False

 def complete_second(self,first):
  result=super().complete_second(first);result['name_raster']=self.run_name_raster(result['character_prefix']);return result

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use immutable evidence path')
 path.write_text(report_text(report(ROOT/'.venv-audit'/f'{path.stem}-bridge.exe',SchoolCharacterNameEmulator)),encoding='utf-8',newline='\n')
