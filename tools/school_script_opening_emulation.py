"""Actual selected school VM and native fade to the first board-on request."""
import argparse,hashlib,json,pickle,struct
from copy import deepcopy
from collections import Counter
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EBP
from tools.school_script_preflight_emulation import SchoolScriptPreflightEmulator,read_entry,read_opening,read_deployment,parent_evidence,CHECKPOINTS,ROOT,SOURCE_SHA256,UNITCTRL,STACK,RETURN,ExitEmulator,AUTHORITY,report_text,TACT,TASK,VM,WORK,CONTROL
from tools.school_deployment_tail_emulation import SchoolDeploymentTailEmulator

PARENT=ROOT/'analysis/school-script-preflight-v1-20261011.json'
PARENT_SHA='b3de8be5e282c4d2e00c2acca5722f7536746aa62c8aff1d6f58d32988ce7c42'
NATIVE=((0x4CE8F0,0x4D03B7),(0x42D460,0x42D512),(0x42D960,0x42D9E4),(0x42E9E0,0x42EBB4),
 (0x42F910,0x42F9FC),(0x42FAF0,0x42FBDC),(0x42FC60,0x42FCCA),(0x496DC0,0x496DE7),
 (0x497210,0x4972A7),(0x4972B0,0x497349),(0x4977A0,0x4977C6),(0x4978C0,0x497980),
 (0x497AA0,0x497C43),(0x499560,0x499752),(0x4C1E20,0x4C1EA4),(0x4C1EB0,0x4C1F29),
 (0x4C1F40,0x4C1FAD),(0x4C2060,0x4C2106),(0x4C23F0,0x4C24F3),(0x4C2670,0x4C2723),
 (0x4C3F40,0x4C3FF9),(0x4C5430,0x4C54BC),(0x4C5500,0x4C5586),(0x4C76B0,0x4C7756),
 (0x4C7AB0,0x4C7B17),(0x4CCB90,0x4CCE1C),(0x4E29E0,0x4E2C1F),(0x56CFCC,0x56CFF3))
CODE=frozenset(a for lo,hi in NATIVE for a in range(lo,hi))
REGIONS=((TACT,400),(CONTROL,18),(WORK,0x24A0),(VM,0x9400),(0x809348,0xA0),(0x7A4E18,8),(TASK+0x196C,2),(TASK+0x1970,2))
PRESENTATION={0x4D29E0:(16,0x4D024F),0x4CA1B0:(0,0x4D028E),0x4C99E0:(0,0x4D02AB),
 0x4CD4D0:(2,0x4D02E7),0x4C7770:(0,0x4D0354),0x4CBA60:(0,0x4D0391)}

def read_parent():
 raw=PARENT.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=PARENT_SHA:raise ValueError('script opening parent identity')
 return json.loads(raw)

def trace_bytes(records):return b''.join((json.dumps(r,sort_keys=True,separators=(',',':'))+'\n').encode() for r in records)

class SchoolScriptOpeningEmulator(SchoolScriptPreflightEmulator):
 def __init__(self):
  self.script_opening_loading=False
  super().__init__()

 def _write_hook(self,uc,access,address,size,value,context):
  if self.deployment_loading:return SchoolDeploymentTailEmulator._write_hook(self,uc,access,address,size,value,context)
  if not self.script_opening_loading:return super()._write_hook(uc,access,address,size,value,context)
  if not any(a<=address and address+size<=b for a,b in self.script_opening_allowed):
   raise RuntimeError(f'script opening finite guard {address:#x}/{size} at{uc.reg_read(UC_X86_REG_EIP):#x}')

 def _hook(self,uc,address,size,context):
  if self.deployment_loading:return SchoolDeploymentTailEmulator._hook(self,uc,address,size,context)
  if not self.script_opening_loading:return super()._hook(uc,address,size,context)
  sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
  if address==0x4CE8F0:
   if (recv,ret)!=(VM,RETURN) or self.read(VM+4,'B')!=1 or self.read(VM+0x92E1,'B'):raise RuntimeError('normal VM declared caller/state')
   if self.read(VM+0x20,'H')==0:
    at=self.read(VM+0x10)+self.read(VM+0x1C);offset=at-self.script_opening_inputs['script_pointer']
    if not 452<=offset<=660:raise RuntimeError('normal VM source bounds')
    op,advance=struct.unpack('<2H',uc.mem_read(at,4))
    if op not in (167,8,5,165,163,113,136,117,56,20,12,27) or advance<4 or offset+advance>676:raise RuntimeError('normal VM opcode bounds')
    self.script_opening_commands.append({'update':self.script_opening_index,'offset':offset,'opcode':op,'advance':advance})
  if address==0x497AA0 and (recv,ret)!=(WORK,RETURN):raise RuntimeError('native fade declared caller')
  if address in PRESENTATION:
   count,expected_ret=PRESENTATION[address];args=[self.read(sp+4+i*4) for i in range(count)]
   if ret!=expected_ret:raise RuntimeError('normal presentation caller')
   if address==0x4D29E0:
    x,y=self.script_opening_inputs['overlay_origin']
    if recv!=VM+0x94E8 or args!=[20,0,1,51,(TASK&0xFFFF0000)|x,(VM&0xFFFF0000)|y,424,24,20,30,100,100,255,128,128,128]:raise RuntimeError('normal overlay inputs')
   elif address in (0x4CA1B0,0x4C99E0):
    if recv not in [VM+0x6F60+i*0xE0 for i in range(10)] or self.read(recv,'H'):raise RuntimeError('normal active layer refused')
   elif address==0x4CD4D0:
    pairs=[[VM+0x6F60+i*0xE0,VM+0x430+i*0xAB8] for i in range(10)]
    if recv!=VM or args not in pairs or self.read(args[0],'H'):raise RuntimeError('normal active object refused')
   elif address==0x4C7770:
    if recv!=VM+0x9248 or self.read(recv,'H'):raise RuntimeError('normal active presentation fade refused')
   elif recv not in [VM+0x228+i*0x1A for i in range(20)] or self.read(recv,'B'):raise RuntimeError('normal active resource refused')
   self.script_opening_presentation.append({'va':hex(address),'receiver':recv,'args':args,'return_va':hex(ret),'return_value':0})
   self._stub_return(0,count*4);return
  if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
  if address in CODE:self.visited.add(address);return
  raise RuntimeError(f'normal opening undeclared instruction {address:#x}')

 def script_regions(self):return [{'pointer':a,'bytes':n,'hex':bytes(self.uc.mem_read(a,n)).hex()} for a,n in REGIONS]
 def script_state(self):
  return {'pc':self.read(VM+0x1C),'wait':self.read(VM+0x20,'H'),'wait_opcode':self.read(VM+0x26,'H'),
   'wait_count':self.read(VM+0x28,'H'),'wait_limit':self.read(VM+0x2A,'H'),'work_wait':self.read(VM+0x92E0,'B'),
   'variable0':self.read(VM+0x3C),'fade_value':self.read(WORK+0x2490,'i'),'fade_delta':self.read(WORK+0x2494,'i'),
   'fade_active':self.read(WORK+0x2499,'B'),'fade_status':self.read(WORK+0x249A,'B'),'fade_remaining':self.read(WORK+0x249C,'i')}

 def run_script_opening(self):
  if self.script_opening_loading:raise RuntimeError('normal opening nested driver refused')
  if (self.read(VM+4,'B'),self.read(VM+5,'B'),self.read(VM+0x1C),self.read(VM+0x20,'H'),self.read(VM+0x92E0,'B'),self.read(VM+0x92E1,'B'))!=(1,1,0,0,0,0):raise RuntimeError('normal opening requires selected native VM')
  if self.read(CONTROL+12,'B')!=7 or self.read(TACT+0x38)!=5 or self.read(TACT+0x43,'B')!=1 or self.read(TACT+0x171,'B') or self.read(0x7A49F8)!=WORK or self.read(0x7A49FC)!=TASK:raise RuntimeError('normal opening unsupported parent')
  self.script_opening_inputs={'script_pointer':self.read(TACT+0x64),'overlay_origin':[self.read(TASK+0x196C,'H'),self.read(TASK+0x1970,'H')],
   'completed_updates':107,'driver':'declared_original_vm_then_fade_calls','pending_handler':'0x4c5ea0'}
  before=self.script_regions();self.script_opening_allowed=[(STACK,STACK+65536),(VM,VM+0x9400),(WORK+0x1D,WORK+0x20),(WORK+0x21,WORK+0x24),
   (WORK+0x2490,WORK+0x24A0),(0x809370,0x809372),(0x8093C0,0x8093C4),(0x7A4E18,0x7A4E20)]
  retained=self.capture_scene_memory(self.script_opening_allowed[1:]);null=bytes(self.uc.mem_read(0,4));prior=self._function_ranges
  self.script_opening_commands=[];self.script_opening_presentation=[];frames=[];updates=[];self.script_opening_loading=True;self._function_ranges=prior+NATIVE
  try:
   for index in range(107):
    self.script_opening_index=index;previous=self.script_state();first=len(self.script_opening_presentation)
    value=self.call(0x4CE8F0,receiver=VM);fade=self.call(0x497AA0,receiver=WORK)
    if value!=1:raise RuntimeError('normal opening unexpectedly ended')
    records=self.script_opening_presentation[first:]
    if len(records)!=52:raise RuntimeError('normal opening presentation count')
    frames.append({'update':index,'calls':len(records),'sha256':hashlib.sha256(trace_bytes(records)).hexdigest()})
    updates.append({'index':index,'before':previous,'after':self.script_state(),'vm_return':value,'fade_return':fade})
   self.script_opening_index=107;sp=STACK+0xFF00;self.write(sp,RETURN);self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_ECX,VM)
   self.uc.emu_start(0x4CE8F0,0x4C5EA0,timeout=1_000_000,count=100000)
   pending_sp=self.uc.reg_read(UC_X86_REG_ESP);frame=self.uc.reg_read(UC_X86_REG_EBP)
   args=[self.read(pending_sp+4+i*4) for i in range(3)]
   if (self.uc.reg_read(UC_X86_REG_EIP),self.uc.reg_read(UC_X86_REG_ECX),self.read(pending_sp),args,self.read(frame-4))!=(0x4C5EA0,VM,0x4CED48,[0,self.script_opening_inputs['script_pointer']+660,1],VM):raise RuntimeError('normal board natural pending stack')
   if self.read(VM+0x1C)!=208 or self.read(VM+0x20,'H') or self.read(VM+0x92E0,'B') or self.read(WORK+0x2499,'B') or self.read(WORK+0x249C,'i'):raise RuntimeError('normal opening fade/wait not completed')
   if bytes(self.uc.mem_read(0,4))!=null:raise RuntimeError('normal opening null retention')
   return {'inputs':deepcopy(self.script_opening_inputs),'before':before,'after':self.script_regions(),'updates':updates,
    'commands':deepcopy(self.script_opening_commands),'presentation_frames':frames,
    'presentation_calls':len(self.script_opening_presentation),'presentation_sha256':hashlib.sha256(trace_bytes(self.script_opening_presentation)).hexdigest(),
    'presentation_first_update':deepcopy(self.script_opening_presentation[:52]),
    'pending_call':{'va':'0x4c5ea0','receiver':VM,'args':args,'return_va':'0x4ced48','root_return_va':hex(RETURN),
     'natural_stack_verified':True,'first_instruction_executed':False},'normal_vm_executed':True,'native_fade_executed':True,
    'synthetic_completion_callback':False,'full_task_wrapper_executed':False,'world_update_loop_executed':False,
    'dialogue_executed':False,'waves_executed':False,'live_rendering':False,'live_audio':False,**self.verify_scene_memory(retained)}
  finally:self._function_ranges=prior;self.script_opening_loading=False

def restored_script_case(index,parents):
 name,sha=CHECKPOINTS[index];raw=(ROOT/f'.venv-audit/formation-actual-checkpoint-{index}.pkl').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('normal opening checkpoint identity')
 payload=pickle.loads(raw)
 if payload['source_sha']!=SOURCE_SHA256 or payload['evidence_kind']!='private_actual_cpu_after_full35_before_placement':raise ValueError('normal opening checkpoint provenance')
 e=SchoolScriptOpeningEmulator();e.__dict__.update({k:v for k,v in payload['state'].items() if not k.startswith('_audit_') and k!='uc'})
 for at,data in payload['memory']:e.uc.mem_write(at,data)
 e.uc.context_restore(payload['cpu'])
 original_start=e.uc.emu_start
 def bounded_parent_start(begin,end,timeout=0,count=0):
  # Keep the frozen deployment instruction bound; only this diagnostic driver
  # allows more wall time for its inherited Python memory guards.
  if (begin,timeout,count)==(0x468A49,30_000_000,4_000_000):timeout=120_000_000
  return original_start(begin,end,timeout=timeout,count=count)
 e.uc.emu_start=bounded_parent_start
 try:
  for fn,key,parent in zip((e.run_placement,e.run_deployment_tail,e.run_initialization_and_opening,e.run_entry_control,e.run_script_preflight),
   ('formation_placement','deployment_tail','scene_opening','entry_control','script_preflight'),parents):
   if fn()!=parent['cases'][index][key]:raise ValueError('normal opening complete parent mismatch')
   print('Parent '+name+'/'+key+': complete frozen equality',flush=True)
 finally:e.uc.emu_start=original_start
 return e,{'name':name,'provenance':{'checkpoint_sha256':sha,'parent_preflight_sha256':PARENT_SHA,'complete_parent_stages_equal':True,
  'deployment_timeout_us':120000000,'deployment_instruction_limit':4000000,'upstream_rerun':False}}

def report():
 parents=(parent_evidence(),read_deployment(),read_opening(),read_entry(),read_parent());cases=[]
 for index in range(3):
  e,c=restored_script_case(index,parents);c['script_opening']=e.run_script_opening();cases.append(c)
  print('Actual normal opening '+c['name']+':107 updates, native fade released, natural board entry',flush=True)
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,'inherited_refusals':deepcopy(parents[-1]['inherited_refusals']),
  'boundary':'Declared normal VM/fade completed; first board handler pending, full task/world/audio/dialogue/waves/rendering remain boundaries.',**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use a new immutable evidence path')
 path.write_text(report_text(report()),encoding='utf-8',newline='\n')
