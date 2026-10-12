"""Natural consecutive text prefix while the first real texture stays alive."""
import argparse, hashlib, struct
import json
from copy import deepcopy
from unicorn import x86_const as X86
from tools.school_live_text_emulation import *
from tools.school_text_preparation_catalog import source_catalog as text_rules
from tools.school_live_text_catalog import expected as first_expected

ROW=OBJECT+0x110
FIELDS=(24,26,28,30,32,34,36)
NEXT_RANGES=((0x4CB5F0,0x4CB698),)
NEXT_CODE=frozenset(a for lo,hi in NEXT_RANGES for a in range(lo,hi))
CPU_REGISTERS=('EAX','EBX','ECX','EDX','ESI','EDI','ESP','EBP','EIP','EFLAGS',
 'CS','DS','ES','FS','GS','SS','CR0','CR2','CR3','CR4','DR0','DR1','DR2','DR3','DR6','DR7',
 'FPCW','FPSW','FPTAG','FIP','FCS','FDP','FDS','FOP','MXCSR')+tuple(f'FP{i}' for i in range(8))+tuple(f'XMM{i}' for i in range(8))

def architectural_state(context):
 # UcContext's opaque bytes also contain emulator bookkeeping. Read actual
 # architectural state through the same API for saved and restored contexts.
 return {name:context.reg_read(getattr(X86,'UC_X86_REG_'+name)) for name in CPU_REGISTERS}

class SchoolNextTextEmulator(SchoolLiveTextEmulator):
 def __init__(self):
  self.next_loading=False;self.predicate_loading=False;super().__init__()

 def _write_hook(self,uc,access,address,size,value,context):
  if self.predicate_loading:
   if not (STACK<=address and address+size<=STACK+65536):raise RuntimeError('actual predicate stack-only writes')
   return
  if not self.next_loading:return super()._write_hook(uc,access,address,size,value,context)
  if not any(a<=address and address+size<=b for a,b in self.next_allowed):
   raise RuntimeError(f'next text finite guard {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')

 def _hook(self,uc,address,size,context):
  if self.predicate_loading:
   if address==RETURN:uc.emu_stop();return
   if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
   if address in NEXT_CODE:self.visited.add(address);return
   raise RuntimeError(f'actual predicate unsupported instruction {address:#x}')
  if not self.next_loading:return super()._hook(uc,address,size,context)
  sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
  if address==0x4CE8F0:
   if (recv,ret,self.read(VM+0x1C),self.read(VM+0x20,'H'))!=(VM,RETURN,238,0):raise RuntimeError('next actual VM root')
  if address==0x4C4B80:
   args=[self.read(sp+4+i*4) for i in range(3)]
   if (recv,ret,args)!=(VM,0x4CEC2B,[0,self.next_inputs['script_pointer']+690,0]):raise RuntimeError('next natural opcode17 caller')
   self.next_calls.append({'va':hex(address),'receiver':recv,'args':args,'return_va':hex(ret)})
  if address==0x4C2120:
   args=[self.read(sp+4+i*4) for i in range(2)]
   if (recv,ret,args)!=(VM,0x4C4BCC,[self.next_inputs['script_pointer']+948,1]):raise RuntimeError('next natural text lookup')
   self.next_calls.append({'va':hex(address),'receiver':recv,'args':args,'return_va':hex(ret)})
  if address==0x4CD6F7:
   array=self.read(sp+8);count=uc.reg_read(UC_X86_REG_EAX)&65535
   if count!=1:raise RuntimeError('next source single line required')
   self.next_split={'count':count,'source_pointer':self.read(sp+4),'array_pointer':array,
    'lines':[{'pointer':self.read(array),'hex':self.bounded_text(self.read(array)).hex()}]}
  if address==0x4CABD0:
   args=[self.read(sp+4+i*4) for i in range(2)]
   if (recv,ret,self.read(OBJECT+22,'H'))!=(OBJECT,0x4C4D04,1):raise RuntimeError('next original append record')
   self.next_calls.append({'va':hex(address),'receiver':recv,'args':args,'return_va':hex(ret)})
  if address==0xE300000:
   if ret!=0x4CAD09:raise RuntimeError('second font boundary caller')
   uc.emu_stop();return
  if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
  if address in TEXT_CODE or address in SCRIPT_CODE:self.visited.add(address);return
  raise RuntimeError(f'next text unsupported original instruction {address:#x}')

 def observe_first_readiness(self):
  if self.bridge.closed or self.bridge.texture['pointer']!=self.read(TEXTURE+0x2C):raise RuntimeError('first actual live texture required')
  before=self.script_regions();stack=bytes(self.uc.mem_read(STACK,65536));cpu=self.uc.context_save();registers=architectural_state(cpu)
  self.predicate_loading=True
  try:
   sp=STACK+0x1000;self.write(sp,RETURN);self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_ECX,OBJECT)
   self.uc.emu_start(0x4CB5F0,RETURN,timeout=1_000_000,count=100000)
   if (self.uc.reg_read(UC_X86_REG_EIP),self.uc.reg_read(UC_X86_REG_ESP))!=(RETURN,sp+4):raise RuntimeError('actual readiness predicate return')
   ready=self.uc.reg_read(UC_X86_REG_EAX)&255
   if ready!=0 or self.script_regions()!=before:raise RuntimeError('first readiness unexpectedly changes actual program')
  finally:
   self.uc.mem_write(STACK,stack);self.uc.context_restore(cpu);self.predicate_loading=False
  if bytes(self.uc.mem_read(STACK,65536))!=stack or architectural_state(self.uc.context_save())!=registers:raise RuntimeError('predicate original CPU/stack not restored')
  return {'va':'0x4cb5f0','receiver':OBJECT,'return_value':ready,'actual_record':True,
   'driver':'declared predicate only; complete CPU context and original stack restored',
   'stack_sha256':hashlib.sha256(stack).hexdigest(),'CPU_registers_sha256':hashlib.sha256(json.dumps(registers,sort_keys=True).encode()).hexdigest(),
   'CPU_register_count':len(registers),
   'program_regions_unchanged':True,'CPU_and_stack_restored':True,
   'original_VM_called_predicate':False}

 def run_next_text(self,first):
  if self.next_loading or not self.live_loading or self.bridge.closed:raise RuntimeError('next owned live resource continuation required')
  if (self.uc.reg_read(UC_X86_REG_EIP),self.uc.reg_read(UC_X86_REG_ESP),self.read(VM+0x1C),self.read(OBJECT+22,'H'))!=(RETURN,STACK+0xFF04,238,1):raise RuntimeError('next actual first return required')
  expected=first_expected(first)
  if expected['after']!=first['after'] or expected['pixel_hex']!=first['actual_readback']['hex']:raise RuntimeError('complete independent first parent')
  readiness=self.observe_first_readiness();pointer=self.read(TACT+0x64)
  if struct.unpack('<3H',self.uc.mem_read(self.read(VM+0x10)+238,6))!=(17,6,1):raise RuntimeError('next source command identity')
  self.next_inputs={'script_pointer':pointer,'driver':'next declared original VM update without first-fade delay','font_api':self.read(0x5920A0)}
  if self.next_inputs['font_api']!=0xE300000:raise RuntimeError('next inherited font binding')
  before=self.script_regions()
  self.next_allowed=[(STACK,STACK+65536),(VM+0x1C,VM+0x2C),(VM+0x93E2,VM+0x93E3),(0x7A4E18,0x7A4E20)]+[(ROW+o,ROW+o+2) for o in FIELDS]
  retained=self.capture_scene_memory(self.next_allowed[1:]);self.next_calls=[];self.next_split=None;self.next_loading=True
  try:
   sp=STACK+0xFF00;self.write(sp,RETURN);self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_ECX,VM)
   self.uc.emu_start(0x4CE8F0,0xE300000,timeout=2_000_000,count=100000)
   sp=self.uc.reg_read(UC_X86_REG_ESP);font=self.uc.reg_read(UC_X86_REG_EBP);text=self.read(font);vm=self.read(text)
   if (self.uc.reg_read(UC_X86_REG_EIP),self.read(sp),self.read(font-4),self.read(text-4),self.read(vm-4),self.read(vm+4))!=(0xE300000,0x4CAD09,OBJECT,VM,VM,RETURN):raise RuntimeError('next natural font frame chain')
   args=[self.read(sp+4+i*4) for i in range(14)]
   if args!=text_rules()['first_font_arguments'] or self.next_split is None:raise RuntimeError('next source font args/split')
   entry=text_rules()['entries'][1];pixels=self.bridge.readback(self.bridge.texture['pointer'])
   if pixels!=first['actual_readback']:raise RuntimeError('first live texture not retained')
   if self.bridge.process.poll() is not None:raise RuntimeError('first texture owner exited during continuation')
   return {'inputs':deepcopy(self.next_inputs),'before':before,'after':self.script_regions(),'first_readiness':readiness,
    'second_text':{'index':1,'pointer':pointer+entry['offset'],'hex':self.bounded_text(pointer+entry['offset']).hex()},
    'calls':deepcopy(self.next_calls),'split':deepcopy(self.next_split),
    'pending_font':{'api':'CreateFontA','va':'0xe300000','import_slot':'0x5920a0','args':args,'face_hex':self.bounded_text(args[-1]).hex(),
     'return_va':'0x4cad09','root_return_va':hex(RETURN),'frames':{'vm':vm,'text':text,'font':font,'sp':sp},
     'natural_stack_verified':True,'first_instruction_executed':False},
    'first_actual_readback':pixels,'first_owner_alive_at_boundary':True,'first_resource_retained':True,
    'second_font_executed':False,'second_texture_created':False,'second_handler_completed':False,
    'first_fade_completed':False,'GPU_draw_or_present_executed':False,'world_update_loop_executed':False,'waves_executed':False,
    **self.verify_scene_memory(retained)}
  finally:self.next_loading=False

def report(helper_path):
 helper,identity=build(helper_path)
 parents=(parent_evidence(),read_deployment(),read_opening(),read_entry(),read_preflight(),read_script_opening(),read_parent());cases=[]
 for index in range(3):
  e,text,case=restored_case(index,parents,SchoolNextTextEmulator)
  if hashlib.sha256(helper.read_bytes()).hexdigest()!=identity['helper_sha256']:raise ValueError('next fixed helper changed before execution')
  case['provenance']['helper_sha256']=identity['helper_sha256']
  first=e.run_live_text(text,helper,continuation=e.run_next_text)
  if hashlib.sha256(helper.read_bytes()).hexdigest()!=identity['helper_sha256']:raise ValueError('next fixed helper changed after execution')
  case['next_text']=first.pop('continuation');case['first_live_text']=first;cases.append(case)
  print('Native '+case['name']+': live first resource retained, readiness false, second original font pending',flush=True)
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'bridge_build':identity,'cases':cases,
  'inherited_refusals':deepcopy(read_text_parent()['inherited_refusals']),**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use new immutable evidence path')
 path.write_text(report_text(report(ROOT/'.venv-audit'/f'{path.stem}-bridge.exe')),encoding='utf-8',newline='\n')
