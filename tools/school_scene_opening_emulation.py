"""Natural scene initialization return plus explicitly driven native opening.

Original opening code runs on actual initialized school state. Rectangle drawing
and scheduler/flush remain declared primitives; no world loop or VM is simulated.
"""
import argparse,hashlib,json,pickle,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EBP
from tools.school_deployment_tail_emulation import (
 SchoolDeploymentTailEmulator,CHECKPOINTS,parent_evidence,ROOT,SOURCE_SHA256,UNITCTRL,STACK,RETURN,ExitEmulator,AUTHORITY,report_text)
from tools.school_tactical_startup_emulation import TACT
from tools.tactics_exit_emulation import TASK

DEPLOYMENT=ROOT/'analysis/school-deployment-tail-v1-20261011.json'
DEPLOYMENT_SHA='82812542fc02b448d33bd3c743da973935949d37475f9676ba20b9c2b1e09132'
NATIVE=((0x4534A1,0x453527),(0x467AA0,0x467B57),(0x41F710,0x41F822),
 (0x456B20,0x456B58),(0x4077C0,0x407823),(0x451A16,0x451A18),(0x451A45,0x451A58),
 (0x453F10,0x453F77),(0x45413B,0x454290),(0x4547A8,0x4547C2),(0x415040,0x415069))
CODE=frozenset(a for lo,hi in NATIVE for a in range(lo,hi))
REGIONS=((TACT,0x190),(UNITCTRL+0x2E6F4,24),(TACT+0x108CC2,2),(0x7A417C,2),(0x7A4184,2))

def read_deployment():
 raw=DEPLOYMENT.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=DEPLOYMENT_SHA:raise ValueError('opening deployment parent identity')
 return json.loads(raw)

class SchoolSceneOpeningEmulator(SchoolDeploymentTailEmulator):
 def __init__(self):
  self.opening_loading=False;self.opening_phase=None
  super().__init__()

 def _write_hook(self,uc,access,address,size,value,context):
  if not self.opening_loading:return super()._write_hook(uc,access,address,size,value,context)
  if not any(a<=address and address+size<=b for a,b in self.opening_allowed):
   raise RuntimeError(f'opening finite guard {address:#x}/{size} at{uc.reg_read(UC_X86_REG_EIP):#x}')
  if not STACK<=address<STACK+65536:self.writes.append((address,size,value&((1<<(size*8))-1)))

 def _hook(self,uc,address,size,context):
  if not self.opening_loading:return super()._hook(uc,address,size,context)
  sp,recv=uc.reg_read(UC_X86_REG_ESP),uc.reg_read(UC_X86_REG_ECX)
  if address==0x467AA0:
   expected_return=RETURN if self.opening_phase=='declared_timer_probe' else 0x4534B5
   if self.opening_phase not in ('initialization','declared_timer_probe') or recv!=UNITCTRL or self.read(sp)!=expected_return or self.read(sp+4,'i')!=self.opening_inputs['timer_input']:
    raise RuntimeError('opening native timer caller')
  if address==0x41F710 and (self.opening_phase,recv,self.read(sp))!=('initialization',TASK+0x844,0x4534C6):raise RuntimeError('opening native no-op caller')
  if address==0x456B20 and (self.opening_phase,recv,self.read(sp))!=('initialization',TACT,0x4534CE):raise RuntimeError('opening native branch caller')
  if address==0x4077C0 and (recv,self.read(sp),self.read(sp+4))!=(TACT+0x68,0x453514,TASK):raise RuntimeError('opening native owner binding')
  if address in (0x422360,0x415420):
   expected={0x4534D8:(0x422360,TACT,[0]),0x4534ED:(0x422360,TACT,[0]),
    0x4534E3:(0x415420,TASK,[]),0x4534F8:(0x415420,TASK,[])}
   args=[self.read(sp+4)] if address==0x422360 else []
   if self.opening_phase!='initialization' or expected.get(self.read(sp))!=(address,recv,args):raise RuntimeError('opening scheduler/flush exact caller')
   self.opening_primitives.append({'va':hex(address),'receiver':recv,'args':args,'return_va':hex(self.read(sp))})
   self._stub_return(0,4 if args else 0);return
  if address==0x453F10:
   if self.opening_phase!='opening' or recv!=TACT or self.read(sp)!=RETURN or self.read(TACT+0x38) not in (0,3,4):raise RuntimeError('opening declared driver phase')
  if address==0x410310:
   args=[self.read(sp+4+i*4) for i in range(7)];x,y,width,height,kind,color,enabled=args
   if self.opening_phase!='opening' or recv!=TASK+0x1058 or self.read(sp) not in (0x4541DA,0x454217):raise RuntimeError('opening rectangle caller')
   if (x,width,height,kind,enabled)!=(0,1024,6,5,1) or y not in range(0,768,6) or color&0xFFFFFF:raise RuntimeError('opening rectangle shape')
   self.opening_rectangles.append({'return_va':hex(self.read(sp)),'args':args})
   self._stub_return(0,28);return
  if address==0x415040:
   if self.opening_phase!='opening' or recv!=TASK or (self.read(sp),self.read(sp+4))!=(0x454229,6):raise RuntimeError('opening original increment caller')
   self.opening_increments+=1
  if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
  if address==0x424F80:raise RuntimeError('opening unexpected source assertion')
  if address in CODE:self.visited.add(address);return
  raise RuntimeError(f'opening undeclared instruction {address:#x}')

 def regions(self):return [{'pointer':at,'bytes':count,'hex':bytes(self.uc.mem_read(at,count)).hex()} for at,count in REGIONS]

 def declared_timer_probe(self,value):
  if type(value)!=int or not -(1<<31)<=value<(1<<31):raise ValueError('opening signed32 timer input')
  if self.opening_loading:raise RuntimeError('opening nested probe refused')
  self.opening_inputs={'timer_input':value};self.opening_allowed=[(STACK,STACK+65536),(UNITCTRL+0x2E6F4,UNITCTRL+0x2E70C)]
  retained=self.capture_scene_memory(self.opening_allowed[1:]);prior=self._function_ranges
  self.opening_loading=True;self.opening_phase='declared_timer_probe';self._function_ranges=prior+NATIVE
  try:
   result=self.call(0x467AA0,[value&0xFFFFFFFF],receiver=UNITCTRL)
   return {'input':value,'hex':bytes(self.uc.mem_read(UNITCTRL+0x2E6F4,24)).hex(),'return_value':result,
    'driver':'declared_signed32_timer_probe',**self.verify_scene_memory(retained)}
  finally:self._function_ranges=prior;self.opening_loading=False;self.opening_phase=None

 def run_initialization_and_opening(self):
  if self.uc.reg_read(UC_X86_REG_EIP)!=0x4534A1:raise RuntimeError('opening requires natural deployment return')
  frame=self.uc.reg_read(UC_X86_REG_EBP);outer=self.read(frame)
  if (self.read(frame+4),self.read(outer+4),self.read(frame-4),self.read(0x7A49FC))!=(0x451A16,0x45170E,TACT,TASK):
   raise RuntimeError(f'opening original phase initializer frame {frame:#x}/{outer:#x}: '+str(tuple(hex(v) for v in (self.read(frame+4),self.read(outer+4),self.read(frame-4),self.read(0x7A49FC)))))
  if self.read(TACT+0x34)!=2 or self.read(TACT+0x43,'B'):raise RuntimeError('opening unsupported phase/active script')
  self.opening_inputs={'timer_input':self.read(0x7F44A8,'i'),'task_pointer':TASK,'phase':2,
   'driver':'declared_original_453f10_updates_on_actual_initialized_state','max_updates':215}
  before=self.regions();self.opening_primitives=[];self.opening_increments=0
  self.opening_allowed=[(STACK,STACK+65536),(UNITCTRL+0x2E6F4,UNITCTRL+0x2E70C),(TACT+0x38,TACT+0x3C),(TACT+0xB4,TACT+0xB8)]
  retained=self.capture_scene_memory(self.opening_allowed[1:]);null=bytes(self.uc.mem_read(0,4))
  self.opening_loading=True;self.opening_phase='initialization';self.clear_trace('tactical_startup')
  try:
   self.uc.emu_start(0x4534A1,0x45170E,timeout=5_000_000,count=100_000)
   if (self.uc.reg_read(UC_X86_REG_EIP),self.uc.reg_read(UC_X86_REG_EAX),self.uc.reg_read(UC_X86_REG_ESP))!=(0x45170E,0,outer+8):
    raise RuntimeError('opening initializer natural return/stack')
   if len(self.opening_primitives)!=4:raise RuntimeError('opening scheduler calls incomplete')
   initialization={'before':before,'after':self.regions(),'primitives':deepcopy(self.opening_primitives),
    'natural_returns':['0x451a16','0x45170e'],'return_value':0,'natural_stack_verified':True,**self.verify_scene_memory(retained)}
   self.opening_allowed=[(STACK,STACK+65536),(TACT+0x38,TACT+0x3C),(TACT+0x170,TACT+0x172),
    (TACT+0x108CC2,TACT+0x108CC4),(0x7A417C,0x7A417E),(0x7A4184,0x7A4186)]
   retained=self.capture_scene_memory(self.opening_allowed[1:]);before=self.regions();updates=[];self.opening_phase='opening'
   for index in range(215):
    phase=self.read(TACT+0x38);fade=self.read(0x7A417C,'h');self.opening_rectangles=[]
    previous_ranges=self._function_ranges
    try:
     self._function_ranges=previous_ranges+NATIVE
     value=self.call(0x453F10,receiver=TACT)
    finally:self._function_ranges=previous_ranges
    rectangles=deepcopy(self.opening_rectangles)
    stream=b''.join(struct.pack('<8I',int(r['return_va'],16),*r['args']) for r in rectangles)
    updates.append({'index':index,'before_phase':phase,'before_fade':fade,'phase':self.read(TACT+0x38),
     'fade':self.read(0x7A417C,'h'),'return_value':value,'rectangle_count':len(rectangles),
     'rectangle_arguments_sha256':hashlib.sha256(stream).hexdigest()})
    if self.read(TACT+0x38)==5:break
   if len(updates)!=215 or self.read(TACT+0x170,'B')!=1 or self.read(TACT+0x171,'B')!=0 or self.opening_increments!=214:
    raise RuntimeError('opening finite phase5 request boundary')
   if bytes(self.uc.mem_read(0,4))!=null:raise RuntimeError('opening null retention')
   return {'inputs':deepcopy(self.opening_inputs),'initialization':initialization,'opening':{'before':before,'after':self.regions(),
    'updates':updates,'native_increment_calls':self.opening_increments,'script_work_requested':True,
    'stop_phase':5,**self.verify_scene_memory(retained)},'scene_initialization_completed':True,
    'scene_vm_executed':False,'world_update_loop_executed':False,'live_rendering':False}
  finally:self.opening_loading=False;self.opening_phase=None

def restored_opening_case(index,parent,previous):
 name,sha=CHECKPOINTS[index];path=ROOT/f'.venv-audit/formation-actual-checkpoint-{index}.pkl';raw=path.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('opening trusted checkpoint identity')
 payload=pickle.loads(raw)
 if payload['source_sha']!=SOURCE_SHA256 or payload['evidence_kind']!='private_actual_cpu_after_full35_before_placement':raise ValueError('opening checkpoint provenance')
 e=SchoolSceneOpeningEmulator();e.__dict__.update({k:v for k,v in payload['state'].items() if not k.startswith('_audit_') and k!='uc'})
 for at,data in payload['memory']:e.uc.mem_write(at,data)
 e.uc.context_restore(payload['cpu'])
 if e.run_placement()!=parent['cases'][index]['formation_placement']:raise ValueError('opening full placement mismatch')
 if e.run_deployment_tail()!=previous['cases'][index]['deployment_tail']:raise ValueError('opening full deployment mismatch')
 return e,{'name':name,'provenance':{'checkpoint_sha256':sha,'parent_deployment_sha256':DEPLOYMENT_SHA,
  'complete_placement_equal':True,'complete_deployment_equal':True,'upstream_rerun':False}}

def report():
 parent=parent_evidence();previous=read_deployment();cases=[]
 for index in range(3):
  e,c=restored_opening_case(index,parent,previous);c['scene_opening']=e.run_initialization_and_opening();cases.append(c)
  print('Actual initialization and declared native opening '+c['name']+': phase5/request170',flush=True)
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,
  'inherited_refusals':deepcopy(previous['inherited_refusals']),
  'boundary':'Scene initializer returned; declared native opening reached script-work request. Work callbacks, event VM and live battle remain pending.',**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use a new immutable evidence path')
 path.write_text(report_text(report()),encoding='utf-8',newline='\n')
