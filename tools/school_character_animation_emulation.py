"""Resume the actual fourth-texture parent through source animation and text2 prefix."""
from tools.school_character_image_live_emulation import *
from tools.school_character_animation_catalog import advance,third_prefix,state,NODE as ANODE,OBJECT as AOBJECT,NODE7,OBJECT7,NAME_TEXTURE
from tools.school_character_prefix_emulation import PREFIX_CODE
from tools.school_board_opening_emulation import ExitEmulator

EXTRA=((0x4CBF90,0x4CC0F0),(0x4CC3E0,0x4CC4E4),(0x4C9650,0x4C99E0),(0x4CD120,0x4CD1E0),(0x4077C0,0x407822))
ANIMATION_CODE=BOARD_CODE|SCRIPT_CODE|TEXT_CODE|PREFIX_CODE|frozenset(a for lo,hi in EXTRA for a in range(lo,hi))

class SchoolCharacterAnimationEmulator(SchoolCharacterImageLiveEmulator):
 def __init__(self):
  self.animation_loading=False;self.third_loading=False;super().__init__()
 def _write_hook(self,uc,access,address,size,value,context):
  if not self.animation_loading:return super()._write_hook(uc,access,address,size,value,context)
  if not any(a<=address and address+size<=b for a,b in self.animation_allowed):raise RuntimeError(f'animation finite write {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
 def _record(self,address,recv,ret,count,target):
  sp=self.uc.reg_read(UC_X86_REG_ESP);record={'va':hex(address),'receiver':recv,'args':[self.read(sp+4+i*4) for i in range(count)],'return_va':hex(ret),'return_value':0}
  expected=self.animation_expected[target]
  actual=self.animation_observed[target]
  if len(actual)>=len(expected) or record!=expected[len(actual)]:raise RuntimeError(f'animation exact {target} {len(actual)}: {record!r}; expected {expected[len(actual)] if len(actual)<len(expected) else None!r}')
  actual.append(record);self._stub_return(0,count*4)
 def _hook(self,uc,address,size,context):
  if not self.animation_loading:return super()._hook(uc,address,size,context)
  sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
  if self.third_loading:
   if address==0xE300000:
    font=uc.reg_read(UC_X86_REG_EBP);text=self.read(font);vm=self.read(text)
    if (self.read(font-4),self.read(text-4),self.read(vm-4),self.read(vm+4),ret)!=(AOBJECT,VM,VM,RETURN,0x4CAD09):raise RuntimeError('third original font frame ownership')
    self.third_pending={'api':'CreateFontA','va':hex(address),'import_slot':'0x5920a0','args':[self.read(sp+4+i*4) for i in range(14)],
     'face_hex':self.bounded_text(self.read(sp+56)).hex(),'return_va':hex(ret),'root_return_va':hex(RETURN),'frames':{'vm':vm,'text':text,'font':font,'sp':sp},'natural_stack_verified':True,'first_instruction_executed':False}
    uc.emu_stop();return
   if address in (0x4C4DC0,0x4C4B80,0x4C2120,0x4CABD0):
    count=3 if address in (0x4C4DC0,0x4C4B80) else 2
    self.third_calls.append({'va':hex(address),'receiver':recv,'args':[self.read(sp+4+i*4) for i in range(count)],'return_va':hex(ret)})
   if address==0x4CD6F7:
    array=self.read(sp+8);count=uc.reg_read(UC_X86_REG_EAX)&65535
    if count!=1:raise RuntimeError('third source single line')
    self.third_split={'count':count,'source_pointer':self.read(sp+4),'array_pointer':array,'lines':[{'pointer':self.read(array),'hex':self.bounded_text(self.read(array)).hex()}]}
  else:
   if address==0x4C4DC0 and getattr(self,'third_calls',None) is not None:
    self.third_calls.append({'va':hex(address),'receiver':recv,'args':[self.read(sp+4+i*4) for i in range(3)],'return_va':hex(ret)})
   if address in (0x4CD060,0x4CD120):
    p={'va':hex(address),'receiver':recv,'args':[self.read(sp+4)],'return_va':hex(ret),'return_value':None};self.animation_observed['predicates'].append(p)
    expected=self.animation_expected['predicates'];idx=len(self.animation_observed['predicates'])-1
    if idx>=len(expected) or {k:v for k,v in p.items() if k!='return_value'}!={k:v for k,v in expected[idx].items() if k!='return_value'}:raise RuntimeError('animation original readiness caller')
   if address in (0x4D0079,0x4D008E):self.animation_observed['predicates'][-1]['return_value']=uc.reg_read(UC_X86_REG_EAX)&255
   if address==0x4CB220:
    record={'receiver':recv,'args':[self.read(sp+4),self.read(sp+8)],'return_va':hex(ret)};self.animation_observed['text_updates'].append(record)
   if address==0x4CBF00:return self._record(address,recv,ret,9,'text_draws')
   primitive=None
   if address in (0x4CBDB0,0x410310,0x408F90,0x4D29E0,0x4C7770,0x4CBA60):primitive={0x4CBDB0:11,0x410310:7,0x408F90:2,0x4D29E0:16,0x4C7770:0,0x4CBA60:0}[address]
   elif address in (0x4CA1B0,0x4C99E0) and not self.read(recv,'H'):primitive=0
   elif address==0x4CD4D0 and not self.read(self.read(sp+4),'H'):primitive=2
   if primitive is not None:return self._record(address,recv,ret,primitive,'presentation')
  if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
  if address==RETURN:uc.emu_stop();return
  if address in ANIMATION_CODE:self.visited.add(address);self.animation_visited.add(address);return
  raise RuntimeError(f'animation undeclared instruction {address:#x}')
 def _root(self):
  sp=STACK+0xFF00;self.write(sp,RETURN);self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_ECX,VM)
 def animate(self,parent):
  if self.uc.reg_read(UC_X86_REG_EIP)!=0x4CC0D2 or self.bridge.closed or not self.live_loading:raise RuntimeError('actual image loader CPU/resource parent')
  before=self.script_regions();renderer=self.read(0x7A49FC);steps=[];self.animation_visited=set()
  self.animation_allowed=[(STACK,STACK+65536),(VM+28,VM+38),(VM+0x93E2,VM+0x93E3),(0x7A4E18,0x7A4E20),(NODE7+4,NODE7+6)]
  self.animation_allowed += [(ANODE+o,ANODE+o+2) for o in (2,4,6,16,18,20,34,36,38,40,42,56,0xD6)]
  self.animation_allowed += [(ANODE+o,ANODE+o+4) for o in (0xAC,0xBC,0xC4)]
  self.animation_allowed += [(OBJECT7+i*0x110+o,OBJECT7+i*0x110+o+2) for i in range(2) for o in (24,26,30,34)]
  retained=self.capture_scene_memory(self.animation_allowed[1:]);self.animation_loading=True
  try:
   for i in range(78):
    self.animation_expected=advance(self.script_regions(),i,renderer);self.animation_observed={k:[] for k in ('presentation','text_draws','text_updates','predicates')}
    if i:self._root()
    self.uc.emu_start(0x4CC0D2 if not i else 0x4CE8F0,RETURN,timeout=2_000_000,count=100000)
    actual_return={'va':self.uc.reg_read(UC_X86_REG_EIP),'sp':self.uc.reg_read(UC_X86_REG_ESP),'eax':self.uc.reg_read(UC_X86_REG_EAX)}
    expected=self.animation_expected
    if self.script_regions()!=expected['after']:
     differences=[]
     for a,b in zip(self.script_regions(),expected['after']):
      aa=bytes.fromhex(a['hex']);bb=bytes.fromhex(b['hex']);differences += [(hex(a['pointer']+j),x,y) for j,(x,y) in enumerate(zip(aa,bb)) if x!=y]
     raise RuntimeError(f'animation complete update {i} state differs {differences[:25]!r}')
    if any(self.animation_observed[k]!=expected[k] for k in self.animation_observed) or actual_return!=expected['natural_return']:raise RuntimeError(f'animation complete update {i} calls/return')
    steps.append({'index':i,'after':self.script_regions(),'before_state':expected['before_state'],'after_state':state(self.script_regions()),**deepcopy(self.animation_observed),'natural_return':actual_return})
   pixels=[self.bridge.readback(t['pointer']) for t in self.animation_textures]
   if pixels!=self.animation_pixels:raise RuntimeError('animation four actual textures retained')
   return {'before':before,'after':self.script_regions(),'renderer':renderer,'steps':steps,'actual_readbacks':pixels,'visited':sorted(self.animation_visited),
    'original_handler_returned':True,'original_animation_executed':True,'original_readiness_executed':True,'synthetic_readiness':False,'GPU_draw_or_present_executed':False,'world_update_loop_executed':False,**self.verify_scene_memory(retained)}
  finally:self.animation_loading=False
 def third(self,parent):
  before=self.script_regions();pointer=self.read(TACT+0x64);expected=third_prefix(before,pointer)
  self.animation_allowed += [(VM+0x34,VM+0x3C),(VM+0x1CC,VM+0x1CD),(VM+0x9250,VM+0x9254),(AOBJECT+24,AOBJECT+38)]
  retained=self.capture_scene_memory(self.animation_allowed[1:]);self.third_calls=[];self.third_split=None;self.third_pending=None;self.animation_loading=True
  try:
   self.animation_expected=expected['activation'];self.animation_observed={k:[] for k in ('presentation','text_draws','text_updates','predicates')}
   self._root();self.uc.emu_start(0x4CE8F0,RETURN,timeout=2_000_000,count=100000)
   actual_return={'va':self.uc.reg_read(UC_X86_REG_EIP),'sp':self.uc.reg_read(UC_X86_REG_ESP),'eax':self.uc.reg_read(UC_X86_REG_EAX)}
   activation={'after':self.script_regions(),**deepcopy(self.animation_observed),'natural_return':actual_return}
   if activation!=expected['activation']:raise RuntimeError('third complete activation/frame source')
   self.third_loading=True
   self._root();self.uc.emu_start(0x4CE8F0,RETURN,timeout=2_000_000,count=100000)
   if self.third_pending is None or self.script_regions()!=expected['after'] or self.third_calls!=expected['calls'] or self.third_split!=expected['split'] or self.third_pending!=expected['pending_font']:raise RuntimeError('third full prefix/source/stack '+repr(self.third_pending))
   pixels=[self.bridge.readback(t['pointer']) for t in self.animation_textures]
   if pixels!=self.animation_pixels:raise RuntimeError('third four actual textures retained')
   return {'before':before,'after':self.script_regions(),'activation':activation,'script_pointer':pointer,'third_text':expected['third_text'],'calls':self.third_calls,'split':self.third_split,'pending_font':self.third_pending,'actual_readbacks':pixels,
    'original_text_activation_executed':True,'original_lookup_split_executed':True,'font_API_executed':False,'third_texture_created':False,'GPU_draw_or_present_executed':False,'world_update_loop_executed':False,**self.verify_scene_memory(retained)}
  finally:self.animation_loading=False;self.third_loading=False
 def complete_second(self,first):
  result=super().complete_second(first);self.animation_textures=self.image_prior_textures+[result['image_live']['texture']];self.animation_pixels=self.image_prior_pixels+[result['image_live']['actual_readback']]
  result['character_animation']=self.animate(result['image_live']);result['third_text_prefix']=self.third(result['character_animation']);return result

def report(helper_path):
 helper,identity=build_image(helper_path);parents=(parent_evidence(),read_deployment(),read_opening(),read_entry(),read_preflight(),read_script_opening(),read_parent());cases=[]
 for index in range(3):
  e,text,case=restored_case(index,parents,SchoolCharacterAnimationEmulator)
  case['provenance']['helper_sha256']=identity['helper_sha256'];first=e.run_live_text(text,helper,bridge_type=ImageD3D8,continuation=e.complete_second)
  case.update(first.pop('continuation'));case['first_live_text']=first;cases.append(case)
  if hashlib.sha256(helper.read_bytes()).hexdigest()!=identity['helper_sha256']:raise ValueError('animation fixed helper identity')
  print('Native '+case['name']+': character fades/readiness and third-text font entry',flush=True)
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'bridge_build':identity,'cases':cases,**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use immutable evidence path')
 path.write_text(report_text(report(ROOT/'.venv-audit'/f'{path.stem}-bridge.exe')),encoding='utf-8',newline='\n')
