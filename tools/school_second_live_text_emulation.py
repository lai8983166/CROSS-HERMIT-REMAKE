"""Complete the second original text with two simultaneously owned real textures."""
from tools.school_next_text_emulation import *
from tools.school_d3d8_multi_bridge import MultiD3D8,build as build_multi
from tools.school_font_raster_catalog import geometry,convert_surface
from tools.school_text_timing_catalog import expected_update,BYTES

SECOND_TEXTURE=TEXTURE+0x110
SECOND_RASTER=0x38000000
SECOND_MIRROR=0x39000000
NEXT_SHA='47e76776fc4eaddf701e99242bccd0968029093ce2faf6056cf3492f0614f69a'

class SchoolSecondLiveTextEmulator(SchoolNextTextEmulator):
 def __init__(self):
  self.second_loading=False;super().__init__()

 def _write_hook(self,uc,access,address,size,value,context):
  if self.raster_loading:return SchoolFontRasterEmulator._write_hook(self,uc,access,address,size,value,context)
  if not self.second_loading:return super()._write_hook(uc,access,address,size,value,context)
  if SECOND_MIRROR<=address<SECOND_MIRROR+MIRROR_BYTES and address+size>SECOND_MIRROR+getattr(self,'lock_bytes',0):raise RuntimeError('second real locked extent')
  if not any(a<=address and address+size<=b for a,b in self.live_allowed):raise RuntimeError(f'second finite write {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')

 def _hook(self,uc,address,size,context):
  if self.raster_loading:return SchoolFontRasterEmulator._hook(self,uc,address,size,context)
  if not self.second_loading:return super()._hook(uc,address,size,context)
  sp=uc.reg_read(UC_X86_REG_ESP)
  if address==0x4CB220:
   raw=bytes(uc.mem_read(OBJECT,BYTES));origin=[self.read(NODE+30,'H'),self.read(NODE+32,'H')]
   self.update_before=raw;self.update_expected=expected_update(raw,origin,OBJECT)
  if address==0x4CBF00:
   record={'va':hex(address),'receiver':uc.reg_read(UC_X86_REG_ECX),'args':[self.read(sp+4+i*4) for i in range(9)],'return_va':hex(self.read(sp)),'return_value':0}
   if len(self.text_draws)>=len(self.update_expected['draws']) or record!=self.update_expected['draws'][len(self.text_draws)]:raise RuntimeError('second exact declared text draw boundary')
   self.text_draws.append(record);self._stub_return(0,36);return
  return SchoolLiveTextEmulator._hook(self,uc,address,size,context)

 def complete_second(self,first):
  first_pointer=first['texture']['pointer'];preparation=self.run_next_text(first)
  self.raster_address=SECOND_RASTER;self.font_texture_address=SECOND_TEXTURE
  raster=self.run_font_raster(preparation,keep_resources=True,platform=self.platform,parent_sha=NEXT_SHA)
  self.native_old_bitmap=next(r['result'] for r in raster['font_api'] if r['name']=='SelectObject' and r['return_va']=='0x40541b')
  cleanup_bindings=[]
  for at,value in ((0x5920A4,0xE310000),(0x5920C4,0xE310010),(0x592060,0xE310020)):
   cleanup_bindings.append({'slot':at,'before':self.read(at),'bound':value});self.write(at,value)
  cfg=geometry(raster['measured']);self.live_texture_size=tuple(1<<(v-1).bit_length() for v in cfg['texture_size'])
  self.live_texture_address=SECOND_TEXTURE;self.live_mirror_address=SECOND_MIRROR
  self.uc.mem_map(SECOND_MIRROR,MIRROR_BYTES)
  self.live_allowed=[(STACK,STACK+65536),(SECOND_TEXTURE+0x28,SECOND_TEXTURE+0x46),(OBJECT+22,OBJECT+24),
   (VM+0x1C,VM+0x2C),(VM+0x93E2,VM+0x93E3),(NODE+4,NODE+6),(0x765720,0x765724),(SECOND_MIRROR,SECOND_MIRROR+MIRROR_BYTES)]
  self.live_allowed += [(OBJECT+i*0x110+o,OBJECT+i*0x110+o+2) for i in range(2) for o in (24,26,30,34)]
  before=self.script_regions();retained=self.capture_scene_memory(self.live_allowed[1:]);account=self.read(0x765720)
  entry={'sp':self.uc.reg_read(UC_X86_REG_ESP),'ebp':self.uc.reg_read(UC_X86_REG_EBP),'return_va':self.read(self.uc.reg_read(UC_X86_REG_ESP))}
  font_frame=preparation['pending_font']['frames']['font']
  if entry!={'sp':font_frame-0x2E0,'ebp':font_frame-0x1DC,'return_va':0x405779}:raise RuntimeError('second natural texture frame')
  self.remote_reads=[];self.com_records=[];self.cleanup_calls=[];self.conversion_calls=[];self.text_updates=[];self.text_draws=[]
  self.lock_before=self.lock_after=b'';self.lock_bytes=0;self.board_records=[];self.board_index=46
  self.second_loading=True
  try:
   self.uc.ctl_remove_cache(0x403BD0,0x403BD1)
   self.uc.emu_start(0x403BD0,RETURN,timeout=10_000_000,count=200000)
   if (self.uc.reg_read(UC_X86_REG_EIP),self.uc.reg_read(UC_X86_REG_ESP),self.read(VM+0x1C),self.read(OBJECT+22,'H'))!=(RETURN,STACK+0xFF04,244,2):raise RuntimeError('second natural VM return')
   pixels=self.bridge.readback(self.bridge.texture['pointer']);first_pixels=self.bridge.readback(first_pointer)
   if first_pixels!=first['actual_readback'] or bytes.fromhex(pixels['hex'])!=self.lock_after:raise RuntimeError('second real readback/first retention')
   conv=self.lock_before
   for call in self.conversion_calls:
    conv=convert_surface(bytes.fromhex(raster['raster']['hex']),raster['raster']['size'],call['rect'],conv,self.lock_pitch,call['point'])
   if conv!=self.lock_after:raise RuntimeError('second independent complete band pixel equality')
   if self.text_draws!=self.update_expected['draws'] or bytes(self.uc.mem_read(OBJECT,BYTES)).hex()!=self.update_expected['after_hex']:raise RuntimeError('second independent full timing equality')
   return {'preparation':preparation,'raster':raster,'cleanup_import_bindings':cleanup_bindings,'entry':entry,'before':before,'after':self.script_regions(),
    'remote_reads':self.remote_reads,'COM_calls':self.com_records,'conversion_calls':self.conversion_calls,'GDI_cleanup_calls':self.cleanup_calls,'text_updates':self.text_updates,
    'update_before_hex':self.update_before.hex(),'text_draws':self.text_draws,'presentation':self.board_records,
    'lock':{'mirror':SECOND_MIRROR,'host_bits':self.host_bits,'pitch':self.lock_pitch,'before_hex':self.lock_before.hex(),'after_hex':self.lock_after.hex()},
    'texture':self.bridge.texture,'actual_readback':pixels,'first_actual_readback':first_pixels,'first_resource_retained':True,
    'accounting_before':account,'accounting_after':self.read(0x765720),'natural_return':{'va':RETURN,'sp':self.uc.reg_read(UC_X86_REG_ESP),'eax':self.uc.reg_read(UC_X86_REG_EAX)},
    'original_texture_create_upload_executed':True,'text_record_completed':True,'text_handler_completed':True,'natural_VM_returned':True,
    'original_text_draw_body_executed':False,'GPU_draw_or_present_executed':False,'original_renderer_startup_executed':False,'dialogue_playback_completed':False,
    'waves_executed':False,'world_update_loop_executed':False,'full_task_wrapper_executed':False,**self.verify_scene_memory(retained)}
  finally:self.second_loading=False

def report(helper_path):
 helper,identity=build_multi(helper_path)
 parents=(parent_evidence(),read_deployment(),read_opening(),read_entry(),read_preflight(),read_script_opening(),read_parent());cases=[]
 for index in range(3):
  e,text,case=restored_case(index,parents,SchoolSecondLiveTextEmulator)
  if hashlib.sha256(helper.read_bytes()).hexdigest()!=identity['helper_sha256']:raise ValueError('second fixed helper identity')
  case['provenance']['helper_sha256']=identity['helper_sha256']
  first=e.run_live_text(text,helper,bridge_type=MultiD3D8,continuation=e.complete_second)
  case['second_live_text']=first.pop('continuation');case['first_live_text']=first
  if hashlib.sha256(helper.read_bytes()).hexdigest()!=identity['helper_sha256']:raise ValueError('second helper changed during execution')
  cases.append(case);print('Native '+case['name']+': two real textures, original PC244 and two-row update',flush=True)
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'bridge_build':identity,'cases':cases,'inherited_refusals':deepcopy(read_text_parent()['inherited_refusals']),**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use new immutable evidence path')
 path.write_text(report_text(report(ROOT/'.venv-audit'/f'{path.stem}-bridge.exe')),encoding='utf-8',newline='\n')
