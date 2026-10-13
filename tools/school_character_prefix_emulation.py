"""Natural confirmed opcode30 to pending character name CreateFontA."""
from tools.school_dialogue_confirmation_emulation import *
from tools.school_character_prefix_catalog import expected_prefix, NODE as CHARACTER_NODE, OBJECT as CHARACTER_OBJECT, FONT_API

PREFIX_RANGES=((0x4C61C0,0x4C6322),(0x4CC600,0x4CC7A8),(0x4CC0F0,0x4CC1DE),(0x4CA770,0x4CA7CB),
 (0x4C9520,0x4C9560),(0x4CA060,0x4CA0B0),(0x4CA0B0,0x4CA0F0),(0x4CA130,0x4CA1B0),
 (0x4CA720,0x4CA770),(0x4CA960,0x4CA9B0),(0x4CA9B0,0x4CAA20),(0x4CAF10,0x4CAF50),(0x4CAFF0,0x4CB030))
PREFIX_CODE=frozenset(a for lo,hi in PREFIX_RANGES for a in range(lo,hi))

class SchoolCharacterPrefixEmulator(SchoolDialogueConfirmationEmulator):
 def __init__(self):
  self.character_loading=False;super().__init__()

 def _write_hook(self,uc,access,address,size,value,context):
  if not self.character_loading:return super()._write_hook(uc,access,address,size,value,context)
  if not any(a<=address and address+size<=b for a,b in self.character_allowed):raise RuntimeError(f'character finite write {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')

 def _hook(self,uc,address,size,context):
  if not self.character_loading:return super()._hook(uc,address,size,context)
  if address==FONT_API:
   sp=uc.reg_read(UC_X86_REG_ESP);name=uc.reg_read(UC_X86_REG_EBP);layer=self.read(name);handler=self.read(layer);vm=self.read(handler)
   pending={'va':address,'return_va':self.read(sp),'receiver':uc.reg_read(UC_X86_REG_ECX),'args':[self.read(sp+4+i*4) for i in range(14)],
    'frames':{'vm':vm,'handler':handler,'layer':layer,'name':name,'sp':sp},'name_argument':self.read(name+8),'first_instruction_executed':False}
   if pending!=self.character_expected['pending_font']:raise RuntimeError('character exact font stack differs '+repr(pending))
   self.pending_character=pending;uc.emu_stop();return
  if address in PREFIX_CODE:self.visited.add(address);self.character_visited.add(address);return
  return super()._hook(uc,address,size,context)

 def continue_character(self,parent):
  if not self.live_loading or self.bridge.closed or self.uc.reg_read(UC_X86_REG_EIP)!=0x4C61C0:raise RuntimeError('character actual live handler entry required')
  before=self.script_regions()
  if before!=parent['after']:raise RuntimeError('character actual confirmation bytes')
  self.character_expected=expected_prefix(before);self.pending_character=None;self.character_visited=set()
  self.character_allowed=[(STACK,STACK+65536),(VM+0x9250,VM+0x9260)]
  self.character_allowed += [(CHARACTER_NODE+o,CHARACTER_NODE+o+2) for o in self.character_expected['node_word_stores']]
  self.character_allowed += [(CHARACTER_OBJECT,CHARACTER_OBJECT+2),(CHARACTER_OBJECT+4,CHARACTER_OBJECT+5),(CHARACTER_OBJECT+6,CHARACTER_OBJECT+8),(CHARACTER_OBJECT+10,CHARACTER_OBJECT+11)]
  retained=self.capture_scene_memory(self.character_allowed[1:]);self.character_loading=True
  try:
   self.uc.emu_start(0x4C61C0,RETURN,timeout=2_000_000,count=100000)
   if self.pending_character is None or self.script_regions()!=self.character_expected['after']:raise RuntimeError('character complete independent prefix state')
   pixels=[self.bridge.readback(t['pointer']) for t in self.resource_textures]
   if pixels!=self.resource_pixels:raise RuntimeError('character retained real textures')
   return {'before':before,'after':self.script_regions(),'pending_font':self.pending_character,'actual_readbacks':pixels,
    'visited':sorted(self.character_visited),'resources_retained':True,'handler_prefix_executed':True,
    'name_font_executed':False,'image_load_executed':False,'animation_executed':False,'GPU_draw_or_present_executed':False,'world_update_loop_executed':False,
    **self.verify_scene_memory(retained)}
  finally:self.character_loading=False

 def complete_second(self,first):
  result=super().complete_second(first);result['character_prefix']=self.continue_character(result['confirmation']);return result

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use new immutable evidence path')
 path.write_text(report_text(report(ROOT/'.venv-audit'/f'{path.stem}-bridge.exe',SchoolCharacterPrefixEmulator)),encoding='utf-8',newline='\n')
