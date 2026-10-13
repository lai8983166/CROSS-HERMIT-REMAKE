"""Actual layer5 text2 font/texture return and no-skip original readiness."""
from tools.school_character_animation_emulation import *
from tools.school_third_live_text_catalog import (
 TEXTURE as THIRD_TEXTURE,RASTER as THIRD_RASTER,MIRROR as THIRD_MIRROR,
 raster_state,complete_state,advance_wait,presentation,PREFIX_SHA)
from tools.school_dialogue_wait_emulation import WAIT_CODE

THIRD_CODE=ANIMATION_CODE|LIVE_CODE|RASTER_CODE|WAIT_CODE

class SchoolThirdLiveTextEmulator(SchoolCharacterAnimationEmulator):
 def __init__(self):
  self.third_live_loading=False;self.third_waiting=False;self.third_raster_loading=False;super().__init__()
 def _write_hook(self,uc,access,address,size,value,context):
  if self.third_raster_loading:return SchoolFontRasterEmulator._write_hook(self,uc,access,address,size,value,context)
  if not self.third_live_loading:return super()._write_hook(uc,access,address,size,value,context)
  if THIRD_MIRROR<=address<THIRD_MIRROR+MIRROR_BYTES and address+size>THIRD_MIRROR+self.lock_bytes:raise RuntimeError('third exact actual lock extent')
  if not any(a<=address and address+size<=b for a,b in self.third_allowed):raise RuntimeError(f'third finite write {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
 def _hook(self,uc,address,size,context):
  if self.third_raster_loading:return SchoolFontRasterEmulator._hook(self,uc,address,size,context)
  if not self.third_live_loading:return super()._hook(uc,address,size,context)
  sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
  if self.third_waiting:
   if address==0x4C5260:self.third_handlers.append({'va':hex(address),'receiver':recv,'args':[self.read(sp+4+i*4) for i in range(3)],'return_va':hex(ret)})
   if address==0x4CB5F0:
    if (ret,recv)!=(0x4CD3B7,VM+0x430+len(self.third_predicates)*0xAB8) or len(self.third_predicates)>=10:raise RuntimeError('third all-object source readiness caller')
    self.third_predicates.append({'receiver':recv,'return_value':None})
   if address==0x4CD3B7:self.third_predicates[-1]['return_value']=uc.reg_read(UC_X86_REG_EAX)&255
   if address in (0x4D5EC0,0x4128F0):
    if address==0x4D5EC0:
     args=[self.read(sp+4+i*4) for i in range(5)];r={'kind':'mouse','va':hex(address),'receiver':recv,'args':args,'return_va':hex(ret),'output':args[0]}
    else:r={'kind':'keyboard','va':hex(address),'receiver':recv,'args':[self.read(sp+4),self.read(sp+8)],'return_va':hex(ret)}
    idx=len(self.third_inputs);wanted=self.third_expected['input_calls']
    if idx>=len(wanted) or any(r[k]!=wanted[idx][k] for k in r):raise RuntimeError('third exact original input query caller')
    self.third_inputs.append(r)
   if address in (0x4CD402,0x4CD432):
    r=self.third_inputs[-1];r['return_eax']=uc.reg_read(UC_X86_REG_EAX)
    if r['kind']=='mouse':r['output_hex']=bytes(uc.mem_read(r['output'],14)).hex()
  if address==0x4D29E0 and not self.third_waiting:
   self.third_expected=complete_state(self.third_before,self.device,self.bridge.texture['pointer'])
   self.animation_expected={**self.third_expected,'presentation':presentation(self.third_prefix_parent)}
  if address==0x4CB220:
   self.animation_observed['text_updates'].append({'receiver':recv,'args':[self.read(sp+4),self.read(sp+8)],'return_va':hex(ret)})
   self.third_objects.append({'receiver':recv,'before_hex':bytes(uc.mem_read(recv,0xAB8)).hex(),'after_hex':None})
  if address==0x4CD541:
   obj=self.third_objects[-1];obj['after_hex']=bytes(uc.mem_read(obj['receiver'],0xAB8)).hex()
  if address==0x4CBF00:return self._record(address,recv,ret,9,'text_draws')
  primitive=None
  if address in (0x4CBDB0,0x410310,0x408F90,0x4D29E0,0x4C7770,0x4CBA60):primitive={0x4CBDB0:11,0x410310:7,0x408F90:2,0x4D29E0:16,0x4C7770:0,0x4CBA60:0}[address]
  elif address in (0x4CA1B0,0x4C99E0) and not self.read(recv,'H'):primitive=0
  elif address==0x4CD4D0 and not self.read(self.read(sp+4),'H'):primitive=2
  if primitive is not None:return self._record(address,recv,ret,primitive,'presentation')
  if address in (0x403C81,0x403CB8,0x403958,0x4039CD,0x403C87,0x403CBB,0x40395B,0x4039D0,0x403910,0x405869,0xE310000,0xE310010,0xE310020):return SchoolLiveTextEmulator._hook(self,uc,address,size,context)
  if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
  if address==RETURN:uc.emu_stop();return
  if address in THIRD_CODE:self.visited.add(address);self.third_visited.add(address);return
  raise RuntimeError(f'third undeclared instruction {address:#x}')
 def upload_third(self,prefix):
  if not self.live_loading or self.bridge.closed or self.uc.reg_read(UC_X86_REG_EIP)!=0xE300000 or self.script_regions()!=prefix['after']:raise RuntimeError('actual third font parent')
  self.raster_address=THIRD_RASTER;self.font_texture_address=THIRD_TEXTURE
  self.third_raster_loading=True
  try:raster=self.run_font_raster(prefix,keep_resources=True,platform=self.platform,parent_sha=PREFIX_SHA)
  finally:self.third_raster_loading=False
  expected=raster_state(raster['before'],raster['measured'],self.graphics)
  if raster['after']!=expected['after']:raise RuntimeError('third full source raster state')
  raster['prior_actual_readbacks']=[self.bridge.readback(t['pointer']) for t in self.animation_textures]
  if raster['prior_actual_readbacks']!=self.animation_pixels:raise RuntimeError('third raster retains four actual resources')
  self.native_old_bitmap=next(r['result'] for r in raster['font_api'] if r['return_va']=='0x40541b');bindings=[]
  for at,value in ((0x5920A4,0xE310000),(0x5920C4,0xE310010),(0x592060,0xE310020)):
   bindings.append({'slot':at,'before':self.read(at),'bound':value});self.write(at,value)
  self.live_texture_size=tuple(1<<(v-1).bit_length() for v in expected['texture_size']);self.live_texture_address=THIRD_TEXTURE;self.live_mirror_address=THIRD_MIRROR;self.uc.mem_map(THIRD_MIRROR,MIRROR_BYTES)
  self.third_allowed=[(STACK,STACK+65536),(THIRD_TEXTURE+0x28,THIRD_TEXTURE+0x46),(AOBJECT+22,AOBJECT+38),(VM+0x1C,VM+0x2C),(VM+0x93E2,VM+0x93E3),(0x7A4E18,0x7A4E20),(0x765720,0x765724),(THIRD_MIRROR,THIRD_MIRROR+MIRROR_BYTES),(ANODE+4,ANODE+6),(NODE7+4,NODE7+6)]
  self.third_allowed += [(OBJECT7+i*0x110+o,OBJECT7+i*0x110+o+2) for i in range(2) for o in (24,26,30,34)]
  self.third_allowed += [(ANODE+o,ANODE+o+n) for o,n in ((0xAC,4),(0xBC,4),(0xC4,4),(0xD6,2))]
  before=self.script_regions();self.third_before=before;self.third_prefix_parent=prefix;retained=self.capture_scene_memory(self.third_allowed[1:]);account=self.read(0x765720)
  entry={'sp':self.uc.reg_read(UC_X86_REG_ESP),'ebp':self.uc.reg_read(UC_X86_REG_EBP),'return_va':self.read(self.uc.reg_read(UC_X86_REG_ESP))};f=prefix['pending_font']['frames']['font']
  if entry!={'sp':f-0x2E0,'ebp':f-0x1DC,'return_va':0x405779}:raise RuntimeError('third natural texture stack')
  self.remote_reads=[];self.com_records=[];self.cleanup_calls=[];self.conversion_calls=[];self.lock_before=self.lock_after=b'';self.lock_bytes=0
  self.animation_observed={k:[] for k in ('presentation','text_draws','text_updates','predicates')};self.third_objects=[];self.third_visited=set();self.third_live_loading=True
  try:
   self.uc.ctl_remove_cache(0x403BD0,0x403BD1);self.uc.emu_start(0x403BD0,RETURN,timeout=30_000_000,count=2000000)
   natural={'va':self.uc.reg_read(UC_X86_REG_EIP),'sp':self.uc.reg_read(UC_X86_REG_ESP),'eax':self.uc.reg_read(UC_X86_REG_EAX)}
   if natural!={'va':RETURN,'sp':STACK+0xFF04,'eax':1}:raise RuntimeError('third upload did not naturally return; '+repr({'CPU':natural,'measured':raster['measured'],'raster_size':expected['raster_size'],'conversion_calls':len(self.conversion_calls),'COM_calls':len(self.com_records)}))
   texture=deepcopy(self.bridge.texture);pixels=self.bridge.readback(texture['pointer']);prior=[self.bridge.readback(t['pointer']) for t in self.animation_textures]
   e=complete_state(before,self.device,texture['pointer'])
   if self.script_regions()!=e['after'] or natural!=e['natural_return'] or any(self.animation_observed[k]!=self.animation_expected[k] for k in self.animation_observed if k!='predicates') or self.third_objects!=e['objects']:raise RuntimeError('third complete original texture/handler/update source')
   out=self.lock_before
   for b in bands(expected):out=convert_surface(bytes.fromhex(raster['raster']['hex']),expected['raster_size'],b['rect'],out,self.lock_pitch,b['point'])
   if pixels['hex']!=out.hex() or self.lock_after!=out or prior!=self.animation_pixels:raise RuntimeError('third all original converted pixels/four prior readbacks')
   return {'before':before,'after':self.script_regions(),'raster':raster,'entry':entry,'cleanup_import_bindings':bindings,'texture':texture,'actual_readback':pixels,'prior_actual_readbacks':prior,
    'remote_reads':self.remote_reads,'COM_calls':self.com_records,'conversion_calls':self.conversion_calls,'GDI_cleanup_calls':self.cleanup_calls,
    'lock':{'mirror':THIRD_MIRROR,'host_bits':self.host_bits,'pitch':self.lock_pitch,'before_hex':self.lock_before.hex(),'after_hex':self.lock_after.hex()},
    'accounting_before':account,'accounting_after':self.read(0x765720),'presentation':self.animation_observed['presentation'],'text_draws':self.animation_observed['text_draws'],'text_updates':self.animation_observed['text_updates'],'objects':self.third_objects,'natural_return':natural,'visited':sorted(self.third_visited),
    'original_third_font_texture_handler_executed':True,'GPU_draw_or_present_executed':False,'world_update_loop_executed':False,'dialogue_playback_completed':False,**self.verify_scene_memory(retained)}
  finally:self.third_live_loading=False
 def wait_third(self,live,prefix):
  if self.uc.reg_read(UC_X86_REG_EIP)!=RETURN or self.script_regions()!=live['after']:raise RuntimeError('actual third handler return')
  before_inputs=[self.read(TASK+o) for o in (0x198C,0x1990,0x19A0)]
  if before_inputs!=[0,1,0] or self.read(TASK+0x10B8+0x480+57,'B') or [self.read(TASK+o,'H') for o in (0x196C,0x1970)]!=[0,0]:raise RuntimeError('captured prior pulse and no keyboard/position binding')
  self.write(TASK+0x1990,0);before=self.script_regions();retained=self.capture_scene_memory(self.third_allowed[1:]);steps=[];self.third_waiting=True;self.third_live_loading=True
  try:
   for index in range(80):
    expected=advance_wait(self.script_regions(),index,prefix);self.third_expected=expected;self.animation_expected=expected;self.animation_observed={k:[] for k in ('presentation','text_draws','text_updates','predicates')};self.third_objects=[];self.third_predicates=[];self.third_inputs=[];self.third_handlers=[]
    self._root();self.uc.emu_start(0x4CE8F0,RETURN,timeout=2_000_000,count=100000)
    natural={'va':self.uc.reg_read(UC_X86_REG_EIP),'sp':self.uc.reg_read(UC_X86_REG_ESP),'eax':self.uc.reg_read(UC_X86_REG_EAX)}
    step={'index':index,'after':self.script_regions(),'presentation':self.animation_observed['presentation'],'text_draws':self.animation_observed['text_draws'],'text_updates':self.animation_observed['text_updates'],'objects':self.third_objects,'predicates':self.third_predicates,'input_calls':self.third_inputs,'handlers':self.third_handlers,'natural_return':natural}
    if step!=expected:raise RuntimeError('third complete natural wait '+str(index))
    steps.append(step)
    if self.read(VM+0x20,'H')==0:break
   else:raise RuntimeError('third natural readiness limit')
   textures=self.animation_textures+[live['texture']];pixels=[self.bridge.readback(t['pointer']) for t in textures]
   if pixels!=self.animation_pixels+[live['actual_readback']]:raise RuntimeError('third all five retained pixels')
   return {'before':before,'after':self.script_regions(),'input_binding':{'before_mouse_words':before_inputs,'after_mouse_words':[self.read(TASK+o) for o in (0x198C,0x1990,0x19A0)],'write_address':TASK+0x1990,'kind':'explicit isolated reset of prior confirmation pulse; no live input capture','space_key':0,'mouse_position':[0,0]},'steps':steps,'actual_readbacks':pixels,'original_fade_readiness_executed':True,'text_skip_executed':False,'confirmation_started':False,'GPU_draw_or_present_executed':False,'world_update_loop_executed':False,**self.verify_scene_memory(retained)}
  finally:self.third_waiting=False;self.third_live_loading=False
 def complete_second(self,first):
  result=super().complete_second(first);result['third_live_text']=self.upload_third(result['third_text_prefix']);result['third_text_wait']=self.wait_third(result['third_live_text'],result['third_text_prefix']);return result

def report(helper_path):
 helper,identity=build_image(helper_path);parents=(parent_evidence(),read_deployment(),read_opening(),read_entry(),read_preflight(),read_script_opening(),read_parent());cases=[]
 for index in range(3):
  e,text,c=restored_case(index,parents,SchoolThirdLiveTextEmulator);c['provenance']['helper_sha256']=identity['helper_sha256'];first=e.run_live_text(text,helper,bridge_type=ImageD3D8,continuation=e.complete_second)
  c.update(first.pop('continuation'));c['first_live_text']=first;cases.append(c)
  if hashlib.sha256(helper.read_bytes()).hexdigest()!=identity['helper_sha256']:raise ValueError('third fixed helper identity')
  print('Native '+c['name']+': fifth actual texture, third natural readiness released',flush=True)
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'bridge_build':identity,'cases':cases,**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use immutable evidence path')
 path.write_text(report_text(report(ROOT/'.venv-audit'/f'{path.stem}-bridge.exe')),encoding='utf-8',newline='\n')
