"""Original name texture upload/cleanup to natural image-loading call."""
from tools.school_character_name_emulation import *
from tools.school_character_name_catalog import (
 MIRROR as NAME_MIRROR,PATH,expected_complete,pending_image)
from tools.school_second_live_text_catalog import bands

NAME_SUFFIX=((0x4CA82C,0x4CA855),(0x4CC1DE,0x4CC28B),(0x4CBF90,0x4CC0E9),(0x4CD7B0,0x4CD850),
 (0x4CA9B0,0x4CAA20))
NAME_SUFFIX_CODE=frozenset(a for lo,hi in NAME_SUFFIX for a in range(lo,hi))

class SchoolCharacterNameTextureEmulator(SchoolCharacterNameEmulator):
 def __init__(self):
  self.name_texture_loading=False;super().__init__()

 def _write_hook(self,uc,access,address,size,value,context):
  if not self.name_texture_loading:return super()._write_hook(uc,access,address,size,value,context)
  if NAME_MIRROR<=address<NAME_MIRROR+MIRROR_BYTES and address+size>NAME_MIRROR+getattr(self,'lock_bytes',0):raise RuntimeError('name actual lock extent')
  if not any(a<=address and address+size<=b for a,b in self.name_texture_allowed):raise RuntimeError(f'name texture finite write {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')

 def _hook(self,uc,address,size,context):
  if not self.name_texture_loading:return super()._hook(uc,address,size,context)
  sp=uc.reg_read(UC_X86_REG_ESP)
  if address==0x4CDE10:
   resource=uc.reg_read(UC_X86_REG_EBP);layer=self.read(resource);handler=self.read(layer);vm=self.read(handler)
   pending={'va':address,'receiver':uc.reg_read(UC_X86_REG_ECX),'args':[self.read(sp+4),self.read(sp+8)],'return_va':self.read(sp),
    'frames':{'resource':resource,'layer':layer,'handler':handler,'vm':vm,'sp':sp},'first_instruction_executed':False}
   if pending!=pending_image(self.name_prefix):raise RuntimeError('name exact image entry stack '+repr(pending))
   self.pending_name_image=pending;uc.emu_stop();return
  if address==0x56CDA0:
   target,source=self.read(sp+4),self.read(sp+8)
   if (self.read(sp),target,source)!=(0x4CD83A,PATH,0x5BFD60):raise RuntimeError('name exact bounded path concat '+hex(self.read(sp)))
   before=self.bounded_text(target);tail=self.bounded_text(source);raw=before+tail
   if raw!=name_rules()['image_path'].encode('ascii'):raise RuntimeError('name source image path')
   self._live_write(target,raw+b'\0');self.path_calls.append({'name':'bounded_source_concat','target':target,'source':source,'before_hex':before.hex(),'after_hex':raw.hex(),'return_va':hex(self.read(sp))})
   self._stub_return(target,0);return
  if address in NAME_SUFFIX_CODE:self.visited.add(address);self.name_texture_visited.add(address);return
  return SchoolLiveTextEmulator._hook(self,uc,address,size,context)

 def complete_name_texture(self,prefix,raster):
  if self.uc.reg_read(UC_X86_REG_EIP)!=0x403BD0 or self.bridge.closed or not self.live_loading:raise RuntimeError('actual live name texture entry required')
  self.name_prefix=prefix;self.pending_name_image=None;self.name_texture_visited=set();self.path_calls=[]
  self.native_old_bitmap=next(r['result'] for r in raster['font_api'] if r['name']=='SelectObject' and r['return_va']=='0x40541b')
  bindings=[]
  for at,value in ((0x5920A4,0xE310000),(0x5920C4,0xE310010),(0x592060,0xE310020)):
   bindings.append({'slot':at,'before':self.read(at),'bound':value});self.write(at,value)
  cfg=geometry(raster['measured']);self.live_texture_size=tuple(1<<(v-1).bit_length() for v in cfg['texture_size'])
  self.live_texture_address=NAME_TEXTURE;self.live_mirror_address=NAME_MIRROR;self.uc.mem_map(NAME_MIRROR,MIRROR_BYTES)
  self.name_texture_allowed=[(STACK,STACK+65536),(NAME_TEXTURE+0x28,NAME_TEXTURE+0x46),
   (0x765720,0x765724),(NAME_MIRROR,NAME_MIRROR+MIRROR_BYTES),(PATH,PATH+len(name_rules()['image_path'])+1)]
  self.name_texture_allowed += [(CHARACTER_NODE+o,CHARACTER_NODE+o+2) for o in (0x2C,0x2E,0x30,0x34)]
  self.name_texture_allowed += [(CHARACTER_NODE+0x44,CHARACTER_NODE+0x48)]
  before=self.script_regions();account=self.read(0x765720);retained=self.capture_scene_memory(self.name_texture_allowed[1:])
  self.remote_reads=[];self.com_records=[];self.cleanup_calls=[];self.conversion_calls=[];self.lock_before=self.lock_after=b'';self.lock_bytes=0
  self.name_texture_loading=True
  try:
   self.uc.ctl_remove_cache(0x403BD0,0x403BD1);self.uc.emu_start(0x403BD0,RETURN,timeout=10_000_000,count=200000)
   if self.pending_name_image is None:raise RuntimeError('natural image entry not reached')
   texture=self.bridge.texture;pixels=self.bridge.readback(texture['pointer']);prior=[self.bridge.readback(t['pointer']) for t in self.resource_textures]
   if prior!=self.resource_pixels or pixels['hex']!=self.lock_after.hex():raise RuntimeError('name all real textures retained')
   expected=expected_complete(raster,texture['pointer'],self.device,account)
   if self.script_regions()!=expected['after'] or self.read(0x765720)!=expected['accounting_after']:
    actual=memory_regions(self.script_regions());predicted=memory_regions(expected['after']);diff=[(hex(a+i),x,y) for a in actual for i,(x,y) in enumerate(zip(actual[a],predicted[a])) if x!=y]
    raise RuntimeError('name independent suffix differences '+repr(diff[:32])+' accounting '+repr((self.read(0x765720),expected['accounting_after'])))
   path=self.bounded_text(PATH).decode('ascii')
   if path!=expected['path']:raise RuntimeError('name complete original resource path')
   out=self.lock_before
   for b in bands(cfg):out=convert_surface(bytes.fromhex(raster['raster']['hex']),cfg['raster_size'],b['rect'],out,self.lock_pitch,b['point'])
   if out!=self.lock_after:raise RuntimeError('name original complete conversion differs')
   return {'before':before,'after':self.script_regions(),'texture':deepcopy(texture),'actual_readback':pixels,'prior_actual_readbacks':prior,'pending_image':self.pending_name_image,
    'path':path,'path_calls':self.path_calls,'visited':sorted(self.name_texture_visited),'cleanup_import_bindings':bindings,
    'remote_reads':self.remote_reads,'COM_calls':self.com_records,'conversion_calls':self.conversion_calls,'GDI_cleanup_calls':self.cleanup_calls,
    'lock':{'mirror':NAME_MIRROR,'host_bits':self.host_bits,'pitch':self.lock_pitch,'before_hex':self.lock_before.hex(),'after_hex':self.lock_after.hex()},
    'accounting_before':account,'accounting_after':self.read(0x765720),'original_name_texture_upload_executed':True,'original_name_font_cleanup_executed':True,
    'name_handler_completed':True,'image_loader_executed':False,'layer_handler_completed':False,'GPU_draw_or_present_executed':False,'world_update_loop_executed':False,**self.verify_scene_memory(retained)}
  finally:self.name_texture_loading=False

 def complete_second(self,first):
  result=super().complete_second(first);result['name_texture']=self.complete_name_texture(result['character_prefix'],result['name_raster']);return result

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use immutable evidence path')
 path.write_text(report_text(report(ROOT/'.venv-audit'/f'{path.stem}-bridge.exe',SchoolCharacterNameTextureEmulator)),encoding='utf-8',newline='\n')
