"""Original entry control on actual initialized school memory, to VM preflight.

Updates are declared diagnostic calls, not a world scheduler. Stop before the
first4551C0 instruction, preserving its natural stack and the existing VM.
"""
import argparse,hashlib,json,pickle,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EBP
from tools.school_scene_opening_emulation import SchoolSceneOpeningEmulator,read_deployment,DEPLOYMENT_SHA
from tools.school_deployment_tail_emulation import CHECKPOINTS,parent_evidence,ROOT,SOURCE_SHA256,UNITCTRL,STACK,RETURN,ExitEmulator,AUTHORITY,report_text
from tools.school_tactical_startup_emulation import TACT
from tools.tactics_exit_emulation import TASK

MAPCTRL=UNITCTRL+0x3D68;CONTROL=UNITCTRL+0x108B3E;VM=0x7D7C28
OPENING=ROOT/'analysis/school-scene-opening-v1-20261011.json'
OPENING_SHA='90b4896db16f17e321bd9ea362a92e75fd8b0fb0f1a19dccd8614c7c69aebd31'
NATIVE=((0x499DA0,0x499E6B),(0x499ECE,0x499ED3),(0x49A02F,0x49A114),(0x49A2B3,0x49A2CF),
 (0x43B400,0x43B524),(0x415070,0x415099),(0x456B20,0x456B58),
 (0x453F10,0x453F4A),(0x454290,0x4542B9),(0x4547A8,0x4547C2))
CODE=frozenset(a for lo,hi in NATIVE for a in range(lo,hi))
REGIONS=((TACT,400),(UNITCTRL+0x108B30,50),(MAPCTRL+0x265A6,4))

def read_opening():
 raw=OPENING.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=OPENING_SHA:raise ValueError('entry opening parent identity')
 return json.loads(raw)

class SchoolEntryControlEmulator(SchoolSceneOpeningEmulator):
 def __init__(self):
  self.entry_loading=False
  super().__init__()

 def _write_hook(self,uc,access,address,size,value,context):
  if not self.entry_loading:return super()._write_hook(uc,access,address,size,value,context)
  if not any(a<=address and address+size<=b for a,b in self.entry_allowed):
   raise RuntimeError(f'entry finite guard {address:#x}/{size} at{uc.reg_read(UC_X86_REG_EIP):#x}')

 def _hook(self,uc,address,size,context):
  if not self.entry_loading:return super()._hook(uc,address,size,context)
  sp,recv=uc.reg_read(UC_X86_REG_ESP),uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
  if address==0x499DA0 and (recv!=UNITCTRL or ret!=RETURN or self.read(CONTROL+12,'B') not in (0,4,5,6)):
   raise RuntimeError('entry declared controller caller/state')
  if address==0x453F10 and (recv!=TACT or ret!=RETURN or self.read(TACT+0x38)!=5 or self.read(TACT+0x171,'B')):
   raise RuntimeError('entry original waiting caller/state')
  if address==0x43B400:
   expected=[self.entry_inputs['origin'][0]*32+16,self.entry_inputs['origin'][1]*16+8]
   if (recv,ret)!=(MAPCTRL,0x499E3D) or [self.read(sp+4,'i'),self.read(sp+8,'i')]!=expected:raise RuntimeError('entry camera caller')
   self.entry_calls.append({'va':hex(address),'receiver':recv,'args':expected,'return_va':hex(ret)})
  if address==0x43B460 and (recv,ret,self.read(sp+4,'i'),self.read(sp+8,'i'))!=(MAPCTRL,0x43B444,-208,-21):raise RuntimeError('entry camera offset caller')
  if address==0x415070:
   if (recv,ret,self.read(sp+4))!=(TASK,0x49A068,180):raise RuntimeError('entry native delay caller')
   self.entry_calls.append({'va':hex(address),'receiver':recv,'args':[180],'return_va':hex(ret)})
  if address==0x456B20 and (recv,ret)!=(TACT,0x49A0BE):raise RuntimeError('entry native mode caller')
  if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
  if address in CODE:self.visited.add(address);return
  raise RuntimeError(f'entry undeclared instruction {address:#x}')

 def entry_regions(self):return [{'pointer':at,'bytes':n,'hex':bytes(self.uc.mem_read(at,n)).hex()} for at,n in REGIONS]
 def entry_state(self):return {'state':self.read(CONTROL+12,'B'),'delay':self.read(CONTROL+14,'h'),
  'request':self.read(TACT+0x170,'B'),'completion':self.read(TACT+0x171,'B'),
  'busy':self.read(UNITCTRL+0x108B34,'B'),'task_phase':self.read(TACT+0x38)}

 def run_entry_control(self):
  if self.entry_loading:raise RuntimeError('entry nested driver refused')
  if self.entry_state()!={'state':0,'delay':0,'request':1,'completion':0,'busy':0,'task_phase':5}:
   raise RuntimeError('entry requires actual completed opening request')
  if self.read(CONTROL,'B') or self.read(CONTROL+10,'B')!=1 or self.read(TACT+0x43,'B') or self.read(0x7F4491,'B') or self.read(UNITCTRL+0x117C38)!=TACT:
   raise RuntimeError('entry unsupported interactive/script/mode/owner')
  header=self.read(MAPCTRL+0x2659C);dimensions=[self.read(header+4,'h'),self.read(header+6,'h')]
  origin=[self.read(CONTROL+2,'h'),self.read(CONTROL+4,'h')]
  if (origin,dimensions)!=([9,16],[64,96]):raise RuntimeError('entry unsupported actual camera input')
  self.entry_inputs={'origin':origin,'dimensions':dimensions,'mode':0,'driver':'declared_499da0_and_phase5_wait_calls','completed_updates':183}
  before=self.entry_regions();vm_before=hashlib.sha256(bytes(self.uc.mem_read(VM,0x9400))).hexdigest()
  self.entry_allowed=[(STACK,STACK+65536),(CONTROL+12,CONTROL+13),(CONTROL+14,CONTROL+16),
   (TACT+0x170,TACT+0x171),(UNITCTRL+0x108B34,UNITCTRL+0x108B35),(MAPCTRL+0x265A6,MAPCTRL+0x265AA)]
  retained=self.capture_scene_memory(self.entry_allowed[1:]);null=bytes(self.uc.mem_read(0,4));prior=self._function_ranges
  self.entry_calls=[];self.entry_loading=True;self._function_ranges=prior+NATIVE;updates=[]
  try:
   for index in range(183):
    state=self.entry_state();value=self.call(0x499DA0,receiver=UNITCTRL)
    waiting=self.call(0x453F10,receiver=TACT)
    updates.append({'index':index,'before':state,'after':self.entry_state(),'return_value':value,'waiting_return':waiting})
   if self.entry_state()!={'state':6,'delay':0,'request':0,'completion':0,'busy':0,'task_phase':5}:raise RuntimeError('entry controller incomplete')
   sp=STACK+0xFF00;self.uc.mem_write(sp,struct.pack('<I',RETURN));self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_ECX,UNITCTRL)
   self.uc.emu_start(0x499DA0,0x4551C0,timeout=1_000_000,count=10000)
   pending_sp=self.uc.reg_read(UC_X86_REG_ESP);frame=self.uc.reg_read(UC_X86_REG_EBP)
   if (self.uc.reg_read(UC_X86_REG_EIP),self.uc.reg_read(UC_X86_REG_ECX),self.read(pending_sp),self.read(pending_sp+4),self.read(pending_sp+8),self.read(frame-4))!=(0x4551C0,TACT,0x49A0D4,0,1,UNITCTRL):
    raise RuntimeError('entry natural pending preflight call')
   if bytes(self.uc.mem_read(0,4))!=null:raise RuntimeError('entry null retention')
   vm_after=hashlib.sha256(bytes(self.uc.mem_read(VM,0x9400))).hexdigest()
   if vm_before!=vm_after:raise RuntimeError('entry VM changed before preflight')
   return {'inputs':deepcopy(self.entry_inputs),'before':before,'after':self.entry_regions(),'updates':updates,
    'calls':deepcopy(self.entry_calls),'pending_call':{'va':'0x4551c0','receiver':TACT,'args':[0,1],
     'return_va':'0x49a0d4','root_return_va':hex(RETURN),'natural_stack_verified':True,'first_instruction_executed':False},
    'vm_before_sha256':vm_before,'vm_after_sha256':vm_after,'request_consumed':True,'completion_reported':False,
    'world_update_loop_executed':False,'preflight_executed':False,'scene_vm_executed':False,'live_rendering':False,
    **self.verify_scene_memory(retained)}
  finally:self._function_ranges=prior;self.entry_loading=False

def restored_entry_case(index,parent,previous,opening):
 name,sha=CHECKPOINTS[index];raw=(ROOT/f'.venv-audit/formation-actual-checkpoint-{index}.pkl').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('entry trusted checkpoint identity')
 payload=pickle.loads(raw)
 if payload['source_sha']!=SOURCE_SHA256 or payload['evidence_kind']!='private_actual_cpu_after_full35_before_placement':raise ValueError('entry checkpoint provenance')
 e=SchoolEntryControlEmulator();e.__dict__.update({k:v for k,v in payload['state'].items() if not k.startswith('_audit_') and k!='uc'})
 for at,data in payload['memory']:e.uc.mem_write(at,data)
 e.uc.context_restore(payload['cpu'])
 if e.run_placement()!=parent['cases'][index]['formation_placement']:raise ValueError('entry full placement mismatch')
 if e.run_deployment_tail()!=previous['cases'][index]['deployment_tail']:raise ValueError('entry full deployment mismatch')
 if e.run_initialization_and_opening()!=opening['cases'][index]['scene_opening']:raise ValueError('entry full opening mismatch')
 return e,{'name':name,'provenance':{'checkpoint_sha256':sha,'parent_opening_sha256':OPENING_SHA,
  'complete_placement_equal':True,'complete_deployment_equal':True,'complete_opening_equal':True,'upstream_rerun':False}}

def report():
 parent=parent_evidence();previous=read_deployment();opening=read_opening();cases=[]
 for index in range(3):
  e,c=restored_entry_case(index,parent,previous,opening);c['entry_control']=e.run_entry_control();cases.append(c)
  print('Actual entry control '+c['name']+': request consumed, pending original4551C0(0,1)',flush=True)
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,'inherited_refusals':deepcopy(opening['inherited_refusals']),
  'boundary':'Declared original entry control consumed170, waited180 and reached natural preflight entry; no preflight or VM instruction executed.',**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use a new immutable evidence path')
 path.write_text(report_text(report()),encoding='utf-8',newline='\n')
