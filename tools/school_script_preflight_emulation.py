"""Natural script preflight VM and selected binding on actual school CPU."""
import argparse,hashlib,json,pickle,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EBP
from tools.school_entry_control_emulation import SchoolEntryControlEmulator,read_opening,read_deployment,parent_evidence,CHECKPOINTS,ROOT,SOURCE_SHA256,UNITCTRL,STACK,RETURN,ExitEmulator,AUTHORITY,report_text,TACT,TASK,VM,CONTROL

ENTRY=ROOT/'analysis/school-entry-control-v1-20261011.json'
ENTRY_SHA='8d6640db841aaa25905022a711fc1f0aa9f1c6700a89b3c6dffdec78b794e8b8'
SCRIPT_SOURCE=ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/SCRIPT/T0005.BIN'
SCRIPT_SHA='44ca546b5ea90ec23a4bc7d8dffeac6547a44bfd035383c91983f7c13ae72a52'
WORK=0xE200000
NATIVE=((0x4551C0,0x455301),(0x455060,0x455160),(0x4214F0,0x421538),
 (0x497720,0x497794),(0x496D80,0x496DB6),(0x496DC0,0x496DE7),(0x496DF0,0x496E27),(0x496E30,0x496E65),
 (0x4CE460,0x4CE4A6),(0x4CE4B0,0x4CE55B),(0x4CE090,0x4CE144),(0x4CD8D0,0x4CDBE0),
 (0x4CE560,0x4CE6E0),(0x4CD700,0x4CD75B),(0x4CE030,0x4CE05E),(0x4CE060,0x4CE08E),
 (0x4CE8F0,0x4D03B9),(0x42FC60,0x42FCCA),(0x42FBE0,0x42FC60),
 (0x4C1F40,0x4C1FC0),(0x4C1EB0,0x4C1F40),(0x4C2060,0x4C2120),(0x4C23F0,0x4C2500),(0x4C2610,0x4C2670),
 (0x4CE800,0x4CE86A),(0x4D0790,0x4D0854),(0x4549D0,0x454AB0),
 (0x49A0D4,0x49A114),(0x49A146,0x49A159),(0x49A2B3,0x49A2CF))
CODE=frozenset(a for lo,hi in NATIVE for a in range(lo,hi))
SPARSE=tuple((VM+0x446+i*0xAB8,2) for i in range(14,56))
REGIONS=((TACT,400),(CONTROL,18),(WORK,3),(VM,0x9400),(0x7A4E18,8))+SPARSE

def read_entry():
 raw=ENTRY.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=ENTRY_SHA:raise ValueError('preflight parent identity')
 return json.loads(raw)

class SchoolScriptPreflightEmulator(SchoolEntryControlEmulator):
 def __init__(self):
  self.preflight_loading=False
  super().__init__()

 def _write_hook(self,uc,access,address,size,value,context):
  if not self.preflight_loading:return super()._write_hook(uc,access,address,size,value,context)
  if not any(a<=address and address+size<=b for a,b in self.preflight_allowed):
   raise RuntimeError(f'preflight finite guard {address:#x}/{size} at{uc.reg_read(UC_X86_REG_EIP):#x}')

 def _primitive(self,va,receiver,args,ret,result,pop):
  self.preflight_primitives.append({'va':hex(va),'receiver':receiver,'args':args,'return_va':hex(ret),'return_value':result&0xFFFFFFFF})
  self._stub_return(result,pop)

 def _hook(self,uc,address,size,context):
  if not self.preflight_loading:return super()._hook(uc,address,size,context)
  sp,recv=uc.reg_read(UC_X86_REG_ESP),uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
  if address==0x4551C0 and (recv,ret,self.read(sp+4),self.read(sp+8))!=(TACT,0x49A0D4,0,1):raise RuntimeError('preflight natural entry')
  if address==0x455060:
   expected={0x4551F2:1,0x455208:2,0x454A03:1,0x454A19:2}
   if recv!=TACT or self.read(sp+4)!=0 or expected.get(ret)!=self.read(sp+8):raise RuntimeError('preflight nested lookup caller')
  if address==0x4CE8F0:
   if recv!=VM or ret!=0x4552AA or not self.read(VM+0x92E1,'B') or self.read(VM+0x20,'H') or not self.read(VM+4,'B'):raise RuntimeError('preflight VM update caller/state')
   at=self.read(VM+0x10)+self.read(VM+0x1C);offset=at-self.preflight_inputs['script_pointer']
   if not 0<=offset<=len(self.preflight_script)-4:raise RuntimeError('preflight script bounds')
   opcode,advance=struct.unpack('<HH',self.uc.mem_read(at,4))
   if opcode not in (167,8,166,11,19) or advance<4 or offset+advance>len(self.preflight_script) or len(self.preflight_commands)>=5:raise RuntimeError('preflight unsupported opcode')
   self.preflight_commands.append({'offset':offset,'opcode':opcode,'advance':advance})
  if address==0x4549D0:
   args=[self.read(sp+4+i*4) for i in range(7)]
   if (recv,ret,args)!=(TACT,0x49A0F4,[0,0,1,0,1,1,0]):raise RuntimeError('preflight actual selected binding')
   self.preflight_bindings.append({'va':hex(address),'receiver':recv,'args':args,'return_va':hex(ret)})
  if address==self.preflight_inputs['strcmp_import']:
   args=[self.read(sp+4),self.read(sp+8)]
   if ret!=0x45521C or args!=[self.preflight_inputs['script_pointer']+432,0x59A60C]:raise RuntimeError('preflight exact string compare')
   for i in range(256):
    left,right=self.read(args[0]+i,'B'),self.read(args[1]+i,'B')
    if left!=right or not left:break
   else:raise RuntimeError('preflight unterminated string')
   self._primitive(address,recv,args,ret,left-right,8);return
  if address==self.preflight_inputs['tick_import']:
   if ret!=0x45528D:raise RuntimeError('preflight unused tick caller')
   self._primitive(address,recv,[],ret,0,0);return
  if address==0x42B2D0:
   arg=self.read(sp+4)
   if (ret,arg) not in ((0x4CE822,0x5C2FF0),(0x4CE856,0x5C2FD8)):raise RuntimeError('preflight debug caller')
   self._primitive(address,recv,[arg],ret,0,0);return
  if address==0x41E500:
   if (ret,recv)!=(0x4CE84C,TASK+0x8F00):raise RuntimeError('preflight audio-end caller')
   self._primitive(address,recv,[],ret,0,0);return
  if address==0x40D120:
   if (ret,recv,self.read(sp+4))!=(0x4D083F,TASK+0x1A98,2):raise RuntimeError('preflight audio-stop caller')
   self._primitive(address,recv,[2],ret,0,4);return
  if address==0x56CEC0:
   args=[self.read(sp+4+i*4) for i in range(3)]
   if (ret,args)!=(0x454A68,[TACT+0x44,0,28]):raise RuntimeError('preflight exact task clear')
   self.uc.mem_write(TACT+0x44,bytes(28));self._primitive(address,recv,args,ret,TACT+0x44,0);return
  if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
  if address in CODE:self.visited.add(address);return
  raise RuntimeError(f'preflight undeclared instruction {address:#x}')

 def preflight_regions(self):return [{'pointer':at,'bytes':n,'hex':bytes(self.uc.mem_read(at,n)).hex()} for at,n in REGIONS]

 def run_script_preflight(self):
  if self.preflight_loading:raise RuntimeError('preflight nested driver refused')
  sp=self.uc.reg_read(UC_X86_REG_ESP)
  if (self.uc.reg_read(UC_X86_REG_EIP),self.uc.reg_read(UC_X86_REG_ECX),self.read(sp),self.read(sp+4),self.read(sp+8))!=(0x4551C0,TACT,0x49A0D4,0,1):raise RuntimeError('preflight requires natural pending call')
  if self.entry_state()!={'state':6,'delay':0,'request':0,'completion':0,'busy':0,'task_phase':5} or self.read(0x7A49F8)!=WORK or self.read(VM+5,'B')==2:raise RuntimeError('preflight unsupported actual state/ownership')
  script=SCRIPT_SOURCE.read_bytes();pointer=self.read(TACT+0x64)
  if hashlib.sha256(script).hexdigest()!=SCRIPT_SHA or bytes(self.uc.mem_read(pointer,len(script)))!=script:raise ValueError('preflight actual script identity')
  self.preflight_script=script;self.preflight_inputs={'script_pointer':pointer,'script_sha256':SCRIPT_SHA,'selector':0,'sub':1,
   'strcmp_import':self.read(0x592278),'tick_import':self.read(0x592210),'main_owner':self.read(0x7A4A00),
   'tick_value':0,'driver':'natural_pending_preflight_and_caller_return'}
  if not self.preflight_inputs['main_owner']:raise RuntimeError('preflight unsupported missing main owner')
  before=self.preflight_regions();self.preflight_primitives=[];self.preflight_commands=[];self.preflight_bindings=[]
  self.preflight_allowed=[(STACK,STACK+65536),(VM,VM+0x9400),(WORK,WORK+3),(0x7A4E18,0x7A4E20),
   (TACT+0x43,TACT+0x60),(CONTROL+12,CONTROL+13)]+[(a,a+n) for a,n in SPARSE]
  retained=self.capture_scene_memory(self.preflight_allowed[1:]);null=bytes(self.uc.mem_read(0,4));root_frame=self.uc.reg_read(UC_X86_REG_EBP)
  self.preflight_loading=True
  try:
   self.uc.emu_start(0x4551C0,0x49A0D4,timeout=5_000_000,count=500000)
   if (self.uc.reg_read(UC_X86_REG_EIP),self.uc.reg_read(UC_X86_REG_EAX),self.uc.reg_read(UC_X86_REG_ESP))!=(0x49A0D4,1,sp+12):raise RuntimeError('preflight natural return/stack')
   intermediate=self.preflight_regions();commands=deepcopy(self.preflight_commands)
   self.uc.emu_start(0x49A0D4,RETURN,timeout=2_000_000,count=100000)
   if (self.uc.reg_read(UC_X86_REG_EIP),self.uc.reg_read(UC_X86_REG_EAX),self.uc.reg_read(UC_X86_REG_ESP))!=(RETURN,0,root_frame+8):raise RuntimeError('preflight controller natural return/stack')
   if self.read(CONTROL+12,'B')!=7 or self.read(TACT+0x43,'B')!=1 or self.read(VM+4,'B')!=1 or self.read(VM+0x1C)!=0 or self.read(VM+0x92E1,'B'):raise RuntimeError('preflight selected VM initial state')
   if bytes(self.uc.mem_read(0,4))!=null:raise RuntimeError('preflight null retention')
   return {'inputs':deepcopy(self.preflight_inputs),'before':before,'preflight_after':intermediate,'after':self.preflight_regions(),
    'commands':commands,'binding_calls':deepcopy(self.preflight_bindings),'primitives':deepcopy(self.preflight_primitives),
    'preflight_return':1,'controller_return':0,'natural_returns':['0x49a0d4',hex(RETURN)],'natural_stack_verified':True,
    'selected_vm_bound':True,'preflight_vm_executed':True,'playback_vm_executed':False,'world_update_loop_executed':False,
    'live_rendering':False,'live_audio':False,**self.verify_scene_memory(retained)}
  finally:self.preflight_loading=False

def restored_preflight_case(index,parent,previous,opening,entry):
 name,sha=CHECKPOINTS[index];raw=(ROOT/f'.venv-audit/formation-actual-checkpoint-{index}.pkl').read_bytes()
 if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('preflight trusted checkpoint identity')
 payload=pickle.loads(raw)
 if payload['source_sha']!=SOURCE_SHA256 or payload['evidence_kind']!='private_actual_cpu_after_full35_before_placement':raise ValueError('preflight checkpoint provenance')
 e=SchoolScriptPreflightEmulator();e.__dict__.update({k:v for k,v in payload['state'].items() if not k.startswith('_audit_') and k!='uc'})
 for at,data in payload['memory']:e.uc.mem_write(at,data)
 e.uc.context_restore(payload['cpu'])
 for result,expected in ((e.run_placement(),parent['cases'][index]['formation_placement']),
  (e.run_deployment_tail(),previous['cases'][index]['deployment_tail']),
  (e.run_initialization_and_opening(),opening['cases'][index]['scene_opening']),
  (e.run_entry_control(),entry['cases'][index]['entry_control'])):
  if result!=expected:raise ValueError('preflight complete parent stage mismatch')
 return e,{'name':name,'provenance':{'checkpoint_sha256':sha,'parent_entry_sha256':ENTRY_SHA,
  'complete_parent_stages_equal':True,'upstream_rerun':False}}

def report():
 parent=parent_evidence();previous=read_deployment();opening=read_opening();entry=read_entry();cases=[]
 for index in range(3):
  e,c=restored_preflight_case(index,parent,previous,opening,entry);c['script_preflight']=e.run_script_preflight();cases.append(c)
  print('Actual script preflight '+c['name']+': return1, selected0/1 VM bound, controller7',flush=True)
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,'inherited_refusals':deepcopy(entry['inherited_refusals']),
  'boundary':'Natural preflight VM and selected script binding complete; normal playback, world loop and battle remain pending.',**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use a new immutable evidence path')
 path.write_text(report_text(report()),encoding='utf-8',newline='\n')
