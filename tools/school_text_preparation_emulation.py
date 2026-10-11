"""Natural text activation and first original text preparation to font entry."""
import argparse, hashlib, json, pickle
from copy import deepcopy
from tools.school_board_opening_emulation import (
 SchoolBoardOpeningEmulator, SchoolDeploymentTailEmulator, ROOT, SOURCE_SHA256,
 CHECKPOINTS, parent_evidence, read_deployment, read_opening, read_entry, read_preflight,
 read_parent as read_script_opening, AUTHORITY, report_text, trace_bytes, REGIONS,
 VM, WORK, TACT, TASK, CONTROL, STACK, RETURN, NODE, OBJECT,
 UC_X86_REG_EIP, UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_ESP, UC_X86_REG_EBP)

PARENT=ROOT/'analysis/school-board-opening-v1-20261012.json'
PARENT_SHA='de8fec0fa15b30f61bd737cdbf9ae59963d53073d181c6430f086d16a958f40e'
NATIVE=((0x4C4DC0,0x4C4EB0),(0x4C4B80,0x4C4D77),(0x4C2120,0x4C218C),
 (0x4CD5B0,0x4CD6FA),(0x4CABD0,0x4CAD09),(0x4CAFA0,0x4CAFEB),
 (0x4CB080,0x4CB0CE),(0x4CB180,0x4CB220))
CODE=frozenset(a for lo,hi in NATIVE for a in range(lo,hi))
OWNED=((VM+0x1C,6),(VM+0x22,4),(VM+0x34,8),(VM+0x1CC,1),(VM+0x9250,4),
 (VM+0x93E2,1),(NODE+4,2),(0x7A4E18,8),(OBJECT+0x18,16))

def read_parent():
 raw=PARENT.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=PARENT_SHA:raise ValueError('text parent identity')
 return json.loads(raw)

class SchoolTextPreparationEmulator(SchoolBoardOpeningEmulator):
 def __init__(self):
  self.text_loading=False
  super().__init__()

 def _write_hook(self,uc,access,address,size,value,context):
  if self.deployment_loading:return SchoolDeploymentTailEmulator._write_hook(self,uc,access,address,size,value,context)
  if not self.text_loading:return super()._write_hook(uc,access,address,size,value,context)
  if not any(a<=address and address+size<=b for a,b in self.text_allowed):raise RuntimeError(f'text finite guard {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')

 def _hook(self,uc,address,size,context):
  if self.deployment_loading:return SchoolDeploymentTailEmulator._hook(self,uc,address,size,context)
  if not self.text_loading:return super()._hook(uc,address,size,context)
  sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
  if address in (0x4C4DC0,0x4C4B80):
   expected=(0x4CEF42,676) if address==0x4C4DC0 else (0x4CEC2B,684)
   args=[self.read(sp+4+i*4) for i in range(3)]
   if (recv,ret,args)!=(VM,expected[0],[0,self.text_inputs['script_pointer']+expected[1],0]):raise RuntimeError('text natural handler caller')
   self.text_calls.append({'va':hex(address),'receiver':recv,'args':args,'return_va':hex(ret)})
  if address==0x4C2120:
   args=[self.read(sp+4+i*4) for i in range(2)]
   if (recv,ret,args)!=(VM,0x4C4BCC,[self.text_inputs['script_pointer']+948,0]):raise RuntimeError('text lookup caller')
   self.text_calls.append({'va':hex(address),'receiver':recv,'args':args,'return_va':hex(ret)})
  if address==0x4CD6F7:
   array=self.read(sp+8);count=uc.reg_read(UC_X86_REG_EAX)&65535
   if count!=1:raise RuntimeError('text first line count')
   self.text_split={'count':count,'source_pointer':self.read(sp+4),'array_pointer':array,
    'lines':[{'pointer':self.read(array+i*4),'hex':self.bounded_text(self.read(array+i*4)).hex()} for i in range(count)]}
  if address==0x4CABD0:
   args=[self.read(sp+4+i*4) for i in range(2)]
   if (recv,ret)!=(OBJECT,0x4C4D04) or self.read(OBJECT+22,'H'):raise RuntimeError('text first record caller')
   self.text_calls.append({'va':hex(address),'receiver':recv,'args':args,'return_va':hex(ret)})
  if address in CODE:self.visited.add(address);return
  return super()._hook(uc,address,size,context)

 def bounded_text(self,pointer):
  raw=bytes(self.uc.mem_read(pointer,255))
  if 0 not in raw:raise RuntimeError('text bounded null terminator')
  return raw[:raw.index(0)]

 def run_text_preparation(self):
  if self.text_loading:raise RuntimeError('text nested driver')
  sp=self.uc.reg_read(UC_X86_REG_ESP);frame=self.uc.reg_read(UC_X86_REG_EBP);pointer=self.read(TACT+0x64)
  if self.uc.reg_read(UC_X86_REG_EIP)!=0x4C4DC0 or self.uc.reg_read(UC_X86_REG_ECX)!=VM or not STACK<=sp<=STACK+65520 or not STACK+4<=frame<STACK+65536:raise RuntimeError('text actual pending CPU required')
  if (self.read(sp),self.read(frame-4),[self.read(sp+4+i*4) for i in range(3)])!=(0x4CEF42,VM,[0,pointer+676,0]):raise RuntimeError('text actual pending stack')
  if (self.read(VM+0x1C),self.read(VM+0x20,'H'),self.read(NODE+2,'H'),self.read(OBJECT+22,'H'),self.read(CONTROL+12,'B'),self.read(TACT+0x38))!=(224,0,2,0,7,5):raise RuntimeError('text actual board state')
  font_api=self.read(0x5920A0)
  if font_api!=0xE300000:raise RuntimeError('text inherited font API binding')
  self.text_inputs={'script_pointer':pointer,'overlay_origin':[self.read(TASK+o,'H') for o in (0x196C,0x1970)],
   'completed_updates':1,'driver':'natural_text_activation_then_original_vm_to_font_entry','font_api':font_api}
  before=self.script_regions();self.text_allowed=[(STACK,STACK+65536)]+[(a,a+n) for a,n in OWNED]
  retained=self.capture_scene_memory(self.text_allowed[1:]);null=bytes(self.uc.mem_read(0,4))
  self.text_loading=True;self.board_loading=True;self.board_index=46;self.board_inputs={'overlay_origin':self.text_inputs['overlay_origin']}
  self.board_records=[];self.text_calls=[];self.text_split=None
  try:
   self.uc.emu_start(0x4C4DC0,RETURN,timeout=1_000_000,count=100000)
   if (self.uc.reg_read(UC_X86_REG_EIP),self.uc.reg_read(UC_X86_REG_ESP),self.uc.reg_read(UC_X86_REG_EAX))!=(RETURN,STACK+0xFF04,1):raise RuntimeError('text activation natural VM return')
   if len(self.board_records)!=54:raise RuntimeError('text activation stable board presentation count')
   activated={'pc':self.read(VM+0x1C),'wait':self.read(VM+0x20,'H'),'target':self.read(VM+0x1CC,'B'),
    'origin':[self.read(VM+o,'H') for o in (0x34,0x36)],'layer_pointer':self.read(VM+0x38)}
   sp=STACK+0xFF00;self.write(sp,RETURN);self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_ECX,VM)
   self.uc.emu_start(0x4CE8F0,font_api,timeout=1_000_000,count=100000)
   sp=self.uc.reg_read(UC_X86_REG_ESP);font_frame=self.uc.reg_read(UC_X86_REG_EBP);text_frame=self.read(font_frame);vm_frame=self.read(text_frame)
   args=[self.read(sp+4+i*4) for i in range(14)]
   if (self.uc.reg_read(UC_X86_REG_EIP),self.read(sp),self.read(font_frame-4),self.read(text_frame-4),self.read(vm_frame-4))!=(font_api,0x4CAD09,OBJECT,VM,VM):raise RuntimeError('text natural font frame chain')
   if self.read(vm_frame+4)!=RETURN or self.text_split is None:raise RuntimeError('text natural root/split')
   if bytes(self.uc.mem_read(0,4))!=null:raise RuntimeError('text null retention')
   first=self.bounded_text(pointer+992)
   return {'inputs':deepcopy(self.text_inputs),'before':before,'after':self.script_regions(),'activated':activated,
    'first_text':{'index':0,'pointer':pointer+992,'hex':first.hex(),'decoded_big5':first.decode('cp950')},
    'split':deepcopy(self.text_split),'calls':deepcopy(self.text_calls),
    'presentation_calls':len(self.board_records),'presentation_sha256':hashlib.sha256(trace_bytes(self.board_records)).hexdigest(),
    'presentation':deepcopy(self.board_records),
    'pending_font':{'api':'CreateFontA','va':hex(font_api),'import_slot':'0x5920a0','args':args,
     'face_hex':self.bounded_text(args[-1]).hex(),'return_va':'0x4cad09','root_return_va':hex(RETURN),
     'frames':{'vm':vm_frame,'text':text_frame,'font':font_frame,'sp':sp},
     'natural_stack_verified':True,'first_instruction_executed':False},
    'text_activation_executed':True,'text_lookup_executed':True,'line_split_executed':True,'initial_text_record_prepared':True,
    'font_api_executed':False,'text_handler_completed':False,'synthetic_font_handle':False,'text_layout_completed':False,
    'text_readiness_executed':False,'dialogue_playback_completed':False,'waves_executed':False,
    'full_task_wrapper_executed':False,'world_update_loop_executed':False,'live_rendering':False,'live_audio':False,
    **self.verify_scene_memory(retained)}
  finally:self.text_loading=False;self.board_loading=False

def restored_text_case(index,parents):
 name,sha=CHECKPOINTS[index];raw=(ROOT/f'.venv-audit/formation-actual-checkpoint-{index}.pkl').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('text checkpoint identity')
 payload=pickle.loads(raw)
 if payload['source_sha']!=SOURCE_SHA256 or payload['evidence_kind']!='private_actual_cpu_after_full35_before_placement':raise ValueError('text checkpoint provenance')
 e=SchoolTextPreparationEmulator();e.__dict__.update({k:v for k,v in payload['state'].items() if k!='uc' and not k.startswith('_audit_')})
 for at,data in payload['memory']:e.uc.mem_write(at,data)
 e.uc.context_restore(payload['cpu']);original=e.uc.emu_start
 def bounded_start(begin,end,timeout=0,count=0):
  if (begin,timeout,count)==(0x468A49,30_000_000,4_000_000):timeout=120_000_000
  return original(begin,end,timeout=timeout,count=count)
 e.uc.emu_start=bounded_start
 try:
  for fn,key,parent in zip((e.run_placement,e.run_deployment_tail,e.run_initialization_and_opening,e.run_entry_control,e.run_script_preflight,e.run_script_opening,e.run_board_opening),
   ('formation_placement','deployment_tail','scene_opening','entry_control','script_preflight','script_opening','board_opening'),parents):
   if fn()!=parent['cases'][index][key]:raise ValueError('text complete parent mismatch')
   print('Parent '+name+'/'+key+': complete frozen equality',flush=True)
 finally:e.uc.emu_start=original
 return e,{'name':name,'provenance':{'checkpoint_sha256':sha,'parent_board_sha256':PARENT_SHA,'complete_parent_stages_equal':True,
  'deployment_timeout_us':120000000,'deployment_instruction_limit':4000000,'upstream_rerun':False}}

def report():
 parents=(parent_evidence(),read_deployment(),read_opening(),read_entry(),read_preflight(),read_script_opening(),read_parent());cases=[]
 for index in range(3):
  e,c=restored_text_case(index,parents);c['text_preparation']=e.run_text_preparation();cases.append(c)
  print('Actual text '+c['name']+':activation returned, first text prepared, natural font API entry',flush=True)
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,'inherited_refusals':deepcopy(parents[-1]['inherited_refusals']),
  'boundary':'Original text activation/first lookup/split/record prefix completed; font API pending; font/layout/readiness/task/world/audio/waves remain boundaries.',**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use a new immutable evidence path')
 path.write_text(report_text(report()),encoding='utf-8',newline='\n')
