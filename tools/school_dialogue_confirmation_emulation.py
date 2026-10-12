"""Declared mouse confirmation on held original gate, then next handler boundary."""
from tools.school_dialogue_wait_emulation import *
from tools.school_dialogue_confirmation_catalog import expected_boundary

class SchoolDialogueConfirmationEmulator(SchoolDialogueWaitEmulator):
 def __init__(self):
  self.next_boundary_loading=False;super().__init__()

 def _write_hook(self,uc,access,address,size,value,context):
  if not self.next_boundary_loading:return super()._write_hook(uc,access,address,size,value,context)
  if not any(a<=address and address+size<=b for a,b in self.boundary_allowed):raise RuntimeError('next-handler prefix finite write')

 def _hook(self,uc,address,size,context):
  if self.next_boundary_loading and address==0x4C61C0:
   sp=uc.reg_read(UC_X86_REG_ESP)
   record={'va':hex(address),'receiver':uc.reg_read(UC_X86_REG_ECX),'args':[self.read(sp+4+i*4) for i in range(3)],
    'return_va':hex(self.read(sp)),'root_return_va':hex(RETURN),'frames':{'vm':uc.reg_read(UC_X86_REG_EBP),'sp':sp},'natural_stack_verified':True,'first_instruction_executed':False}
   if record!=self.boundary_expected['pending_call']:raise RuntimeError('next original handler exact natural stack')
   self.pending_boundary=record;uc.emu_stop();return
  return super()._hook(uc,address,size,context)

 def run_confirmation(self,waits,mouse_buttons=1):
  if type(mouse_buttons)is not int or mouse_buttons!=1:raise ValueError('declared single mouse-button confirmation required')
  if not self.live_loading or self.bridge.closed or self.uc.reg_read(UC_X86_REG_EIP)!=RETURN or (self.read(VM+0x1C),self.read(VM+0x20,'H'),self.read(VM+0x22,'H'))!=(252,1,51) or self.read(TASK+0x1990)!=0:raise RuntimeError('actual held zero-input confirmation required')
  before=self.script_regions();binding={'slot':TASK+0x1990,'before':0,'bound':mouse_buttons,'origin':'declared isolated mouse-button input; no live input capture','live_game_input_modified':False}
  self.wait_allowed += [(TASK+0x1990,TASK+0x1994)];retained=self.capture_scene_memory(self.wait_allowed[1:])
  self.wait_loading=True;self.second_loading=True
  try:
   self._live_write(binding['slot'],struct.pack('<I',mouse_buttons))
   step=self.one_wait_update(len(waits['steps']),{'mouse_buttons':mouse_buttons,'space_key':0})
   if (self.read(VM+0x1C),self.read(VM+0x20,'H'))!=(252,0):raise RuntimeError('original confirmation did not release wait')
   self.boundary_expected=expected_boundary(step['after']);self.pending_boundary=None
   self.boundary_allowed=[(STACK,STACK+65536),(VM+0x1C,VM+0x26),(VM+0x93E2,VM+0x93E3),(0x7A4E18,0x7A4E20)]
   prefix_retained=self.capture_scene_memory(self.boundary_allowed[1:]);self.next_boundary_loading=True
   sp=STACK+0xFF00;self.write(sp,RETURN);self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_ECX,VM)
   self.uc.emu_start(0x4CE8F0,RETURN,timeout=2_000_000,count=100000)
   if self.pending_boundary is None or self.script_regions()!=self.boundary_expected['after']:raise RuntimeError('next original handler complete prefix')
   pixels=[self.bridge.readback(t['pointer']) for t in self.resource_textures]
   if pixels!=self.resource_pixels:raise RuntimeError('confirmation both real textures retained')
   return {'binding':binding,'before':before,'confirmation_step':step,'after':self.script_regions(),'pending_call':self.pending_boundary,
    'actual_readbacks':pixels,'resources_retained':True,'confirmation_handler_completed':True,'original_input_query_bodies_executed':True,
    'live_input_capture_executed':False,'next_handler_executed':False,'GPU_draw_or_present_executed':False,'world_update_loop_executed':False,'waves_executed':False,
    'prefix_retention':self.verify_scene_memory(prefix_retained),**self.verify_scene_memory(retained)}
  finally:self.wait_loading=False;self.second_loading=False;self.next_boundary_loading=False

 def complete_second(self,first):
  result=super().complete_second(first);result['confirmation']=self.run_confirmation(result['waits']);return result

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use new immutable evidence path')
 path.write_text(report_text(report(ROOT/'.venv-audit'/f'{path.stem}-bridge.exe',SchoolDialogueConfirmationEmulator)),encoding='utf-8',newline='\n')
