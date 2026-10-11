"""Natural first school board handler, active layer animation and readiness."""
import argparse, hashlib, json, pickle
from copy import deepcopy
from tools.school_script_opening_emulation import (
 SchoolScriptOpeningEmulator, SchoolDeploymentTailEmulator, NATIVE as PARENT_NATIVE,
 REGIONS, ROOT, SOURCE_SHA256, CHECKPOINTS, parent_evidence, read_deployment,
 read_opening, read_entry, read_parent as read_preflight, AUTHORITY, report_text,
 trace_bytes, VM, WORK, TACT, TASK, CONTROL, STACK, RETURN, ExitEmulator,
 UC_X86_REG_EIP, UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_ESP, UC_X86_REG_EBP)

PARENT=ROOT/'analysis/school-script-opening-v1-20261012.json'
PARENT_SHA='b76eaae2a083ea1f71ea525778aac9e6e0ea978941e149705c6057773362521f'
NATIVE=PARENT_NATIVE+((0x4C5EA0,0x4C5FBE),(0x4C9520,0x4C954C),(0x4C9610,0x4C9641),
 (0x4C99E0,0x4CA03F),(0x4CA060,0x4CA1A6),(0x4CA1B0,0x4CA712),
 (0x4CA860,0x4CA958),(0x4CA960,0x4CAA1D),(0x4CAF10,0x4CAF45),
 (0x4CAFF0,0x4CB026),(0x4CB220,0x4CB5D8),(0x4CC0F0,0x4CC3C3),
 (0x4CC600,0x4CC7A6),(0x4CC7D0,0x4CC8CA),(0x4CD060,0x4CD11E),
 (0x4CD4D0,0x4CD564),(0x4CD850,0x4CD8CC))
CODE=frozenset(a for lo,hi in NATIVE for a in range(lo,hi))
NODE=VM+0x6F60+7*0xE0
OBJECT=VM+0x430+7*0xAB8
OWNED=((VM+0x1C,6),(VM+0x22,4),(VM+0x9250,12),(VM+0x93E2,1),
 (0x7A4E18,8),(OBJECT,2),(OBJECT+4,1),(OBJECT+6,2),(OBJECT+10,1))+tuple(
 (NODE+offset,2) for offset in (0,2,4,6,8,12,14,16,18,20,22,24,26,28,30,32,34,36,38,48,64,66,76))

def read_parent():
 raw=PARENT.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=PARENT_SHA:raise ValueError('board parent identity')
 return json.loads(raw)

class SchoolBoardOpeningEmulator(SchoolScriptOpeningEmulator):
 def __init__(self):
  self.board_loading=False
  super().__init__()

 def _write_hook(self,uc,access,address,size,value,context):
  if self.deployment_loading:return SchoolDeploymentTailEmulator._write_hook(self,uc,access,address,size,value,context)
  if not self.board_loading:return super()._write_hook(uc,access,address,size,value,context)
  if not any(a<=address and address+size<=b for a,b in self.board_allowed):
   raise RuntimeError(f'board finite guard {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')

 def _hook(self,uc,address,size,context):
  if self.deployment_loading:return SchoolDeploymentTailEmulator._hook(self,uc,address,size,context)
  if not self.board_loading:return super()._hook(uc,address,size,context)
  sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
  if address==0x4CE8F0 and (recv,ret)!=(VM,RETURN):raise RuntimeError('board VM declared caller')
  if address==0x4C5EA0:
   args=[self.read(sp+4+i*4) for i in range(3)]
   if (recv,ret,args)!=(VM,0x4CED48,[0,self.board_inputs['script_pointer']+660,1]):raise RuntimeError('board natural handler caller')
  if address in (0x4CA1B0,0x4C99E0):
   if recv not in [VM+0x6F60+i*0xE0 for i in range(10)]:raise RuntimeError('board layer receiver')
   if self.read(recv,'H') and (recv!=NODE or self.read(recv+2,'H') not in (2,3) or self.read(recv+0x22,'H')!=1):raise RuntimeError('board unsupported active layer')
  if address==0x4CB220 and (recv!=OBJECT or self.read(recv+0x16,'H')):raise RuntimeError('board nonempty text object refused')
  if address==0x4CD060 and (recv,ret,self.read(sp+4))!=(VM,0x4D00D1,0):raise RuntimeError('board readiness caller')
  if address==0x4CD11D:
   self.board_readiness.append({'update':self.board_index,'return_value':uc.reg_read(UC_X86_REG_EAX)&255})
  primitive=None
  if address==0x4D29E0:primitive=(16,0x4D024F,VM+0x94E8)
  elif address in (0x4CA1B0,0x4C99E0) and not self.read(recv,'H'):primitive=(0,0x4D028E if address==0x4CA1B0 else 0x4D02AB,recv)
  elif address==0x4CD4D0 and not self.read(self.read(sp+4),'H'):primitive=(2,0x4D02E7,VM)
  elif address==0x4C7770:primitive=(0,0x4D0354,VM+0x9248)
  elif address==0x4CBA60:primitive=(0,0x4D0391,recv)
  elif address==0x4CBDB0:primitive=(11,0x4CA6FC,VM)
  elif address==0x410310:primitive=(7,0x4CA409 if self.board_index<46 else 0x4CA319,TASK+0x1058)
  if primitive:
   count,expected_ret,expected_recv=primitive;args=[self.read(sp+4+i*4) for i in range(count)]
   if (recv,ret)!=(expected_recv,expected_ret):raise RuntimeError('board exact presentation caller')
   if address==0x4D29E0:
    x,y=self.board_inputs['overlay_origin']
    if args!=[20,0,1,51,(TASK&0xFFFF0000)|x,(VM&0xFFFF0000)|y,424,24,20,30,100,100,255,128,128,128]:raise RuntimeError('board overlay inputs')
   elif address==0x4CD4D0:
    if args not in [[VM+0x6F60+i*0xE0,VM+0x430+i*0xAB8] for i in range(10)]:raise RuntimeError('board inactive object inputs')
   elif address==0x4C7770 and self.read(recv,'H'):raise RuntimeError('board active fade refused')
   elif address==0x4CBA60 and (recv not in [VM+0x228+i*0x1A for i in range(20)] or self.read(recv,'B')):raise RuntimeError('board active resource refused')
   elif address==0x4CBDB0 and (args[3]!=0xFFFFFFFF or args[4]!=66 or args[9:]!=[20,0] or args[2]&65535>255):raise RuntimeError('board terminal sprite shape')
   elif address==0x410310 and (args[:4]!=[274,580,473,154] or args[4]!=(67 if self.board_index<46 else 0xFFFF0043) or args[6]!=1 or args[5]&0xFFFFFF!=0x223438):raise RuntimeError('board terminal rectangle shape')
   self.board_records.append({'va':hex(address),'receiver':recv,'args':args,'return_va':hex(ret),'return_value':0})
   self._stub_return(0,count*4);return
  if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
  if address in CODE:self.visited.add(address);return
  raise RuntimeError(f'board undeclared instruction {address:#x}')

 def board_state(self):
  return {'pc':self.read(VM+0x1C),'wait':self.read(VM+0x20,'H'),'opcode':self.read(VM+0x22,'H'),
   'layer_active':self.read(NODE,'H'),'layer_mode':self.read(NODE+2,'H'),'previous_mode':self.read(NODE+4,'H'),
   'animation_count':self.read(NODE+6,'H'),'animation_limit':self.read(NODE+16,'H'),
   'background_mode':self.read(NODE+34,'H'),'text_count':self.read(OBJECT+22,'H'),
   'instruction_count':self.read(0x7A4E18),'waiting_count':self.read(0x7A4E1C)}

 def run_board_opening(self):
  if self.board_loading:raise RuntimeError('board nested driver')
  sp=self.uc.reg_read(UC_X86_REG_ESP);frame=self.uc.reg_read(UC_X86_REG_EBP);pointer=self.read(TACT+0x64)
  if self.uc.reg_read(UC_X86_REG_EIP)!=0x4C5EA0 or self.uc.reg_read(UC_X86_REG_ECX)!=VM or not STACK<=sp<=STACK+65520 or not STACK+4<=frame<STACK+65536:raise RuntimeError('board actual pending CPU required')
  if (self.uc.reg_read(UC_X86_REG_EIP),self.uc.reg_read(UC_X86_REG_ECX),self.read(sp),self.read(frame-4),
   [self.read(sp+4+i*4) for i in range(3)])!=(0x4C5EA0,VM,0x4CED48,VM,[0,pointer+660,1]):raise RuntimeError('board actual pending stack required')
  if (self.read(VM+0x1C),self.read(VM+0x20,'H'),self.read(VM+4,'B'),self.read(CONTROL+12,'B'),self.read(TACT+0x38))!=(208,0,1,7,5):raise RuntimeError('board parent state')
  if any(self.read(VM+0x6F60+i*0xE0,'H') for i in range(10)) or self.read(OBJECT+22,'H'):raise RuntimeError('board parent active/nonempty presentation')
  self.board_inputs={'script_pointer':pointer,'overlay_origin':[self.read(TASK+o,'H') for o in (0x196C,0x1970)],
   'completed_updates':47,'driver':'natural_board_resume_then_declared_original_vm_calls','pending_handler':'0x4c4dc0'}
  before=self.script_regions();self.board_allowed=[(STACK,STACK+65536)]+[(a,a+n) for a,n in OWNED]
  retained=self.capture_scene_memory(self.board_allowed[1:]);null=bytes(self.uc.mem_read(0,4))
  self.board_records=[];self.board_readiness=[];updates=[];frames=[];self.board_loading=True
  try:
   for index in range(47):
    self.board_index=index;previous=self.board_state();first=len(self.board_records)
    if index:
     sp=STACK+0xFF00;self.write(sp,RETURN);self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_ECX,VM)
    self.uc.emu_start(0x4C5EA0 if index==0 else 0x4CE8F0,RETURN,timeout=1_000_000,count=100000)
    if (self.uc.reg_read(UC_X86_REG_EIP),self.uc.reg_read(UC_X86_REG_ESP),self.uc.reg_read(UC_X86_REG_EAX))!=(RETURN,STACK+0xFF04,1):raise RuntimeError('board natural VM return')
    records=self.board_records[first:]
    if len(records)!=54:raise RuntimeError('board presentation count')
    frames.append({'update':index,'calls':54,'sha256':hashlib.sha256(trace_bytes(records)).hexdigest()})
    updates.append({'index':index,'before':previous,'after':self.board_state(),'vm_return':1})
   self.board_index=47;sp=STACK+0xFF00;self.write(sp,RETURN);self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_ECX,VM)
   self.uc.emu_start(0x4CE8F0,0x4C4DC0,timeout=1_000_000,count=100000)
   sp=self.uc.reg_read(UC_X86_REG_ESP);args=[self.read(sp+4+i*4) for i in range(3)]
   if (self.uc.reg_read(UC_X86_REG_EIP),self.uc.reg_read(UC_X86_REG_ECX),self.read(sp),args)!=(0x4C4DC0,VM,0x4CEF42,[0,pointer+676,0]):raise RuntimeError('board natural text-active stack')
   if bytes(self.uc.mem_read(0,4))!=null:raise RuntimeError('board null retention')
   if self.board_state()['wait'] or self.board_state()['layer_mode']!=2:raise RuntimeError('board readiness not naturally completed')
   return {'inputs':deepcopy(self.board_inputs),'before':before,'after':self.script_regions(),'updates':updates,
    'readiness':deepcopy(self.board_readiness),'presentation_frames':frames,'presentation_calls':len(self.board_records),
    'presentation_sha256':hashlib.sha256(trace_bytes(self.board_records)).hexdigest(),
    'presentation_first_update':deepcopy(self.board_records[:54]),
    'pending_call':{'va':'0x4c4dc0','receiver':VM,'args':args,'return_va':'0x4cef42','root_return_va':hex(RETURN),
     'natural_stack_verified':True,'first_instruction_executed':False},
    'board_handler_executed':True,'active_layer_updates_executed':True,'readiness_predicate_executed':True,
    'synthetic_readiness':False,'text_activation_executed':False,'dialogue_executed':False,'waves_executed':False,
    'full_task_wrapper_executed':False,'world_update_loop_executed':False,'live_rendering':False,'live_audio':False,
    **self.verify_scene_memory(retained)}
  finally:self.board_loading=False

def restored_board_case(index,parents):
 name,sha=CHECKPOINTS[index];raw=(ROOT/f'.venv-audit/formation-actual-checkpoint-{index}.pkl').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('board checkpoint identity')
 payload=pickle.loads(raw)
 if payload['source_sha']!=SOURCE_SHA256 or payload['evidence_kind']!='private_actual_cpu_after_full35_before_placement':raise ValueError('board checkpoint provenance')
 e=SchoolBoardOpeningEmulator();e.__dict__.update({k:v for k,v in payload['state'].items() if k!='uc' and not k.startswith('_audit_')})
 for at,data in payload['memory']:e.uc.mem_write(at,data)
 e.uc.context_restore(payload['cpu']);original=e.uc.emu_start
 def bounded_start(begin,end,timeout=0,count=0):
  if (begin,timeout,count)==(0x468A49,30_000_000,4_000_000):timeout=120_000_000
  return original(begin,end,timeout=timeout,count=count)
 e.uc.emu_start=bounded_start
 try:
  for fn,key,parent in zip((e.run_placement,e.run_deployment_tail,e.run_initialization_and_opening,e.run_entry_control,e.run_script_preflight,e.run_script_opening),
   ('formation_placement','deployment_tail','scene_opening','entry_control','script_preflight','script_opening'),parents):
   if fn()!=parent['cases'][index][key]:raise ValueError('board complete parent mismatch')
   print('Parent '+name+'/'+key+': complete frozen equality',flush=True)
 finally:e.uc.emu_start=original
 return e,{'name':name,'provenance':{'checkpoint_sha256':sha,'parent_opening_sha256':PARENT_SHA,'complete_parent_stages_equal':True,
  'deployment_timeout_us':120000000,'deployment_instruction_limit':4000000,'upstream_rerun':False}}

def report():
 parents=(parent_evidence(),read_deployment(),read_opening(),read_entry(),read_preflight(),read_parent());cases=[]
 for index in range(3):
  e,c=restored_board_case(index,parents);c['board_opening']=e.run_board_opening();cases.append(c)
  print('Actual board '+c['name']+':47 updates, native readiness released, natural text-active entry',flush=True)
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,'inherited_refusals':deepcopy(parents[-1]['inherited_refusals']),
  'boundary':'Native first board and readiness completed; text-active pending; full task/world/audio/text/waves/rendering remain boundaries.',**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use a new immutable evidence path')
 path.write_text(report_text(report()),encoding='utf-8',newline='\n')
