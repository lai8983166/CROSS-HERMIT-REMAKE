"""Natural original VM text fade/readiness and held confirmation with live textures."""
from tools.school_second_live_text_emulation import *
from tools.school_dialogue_wait_catalog import advance,HOLD_UPDATES

WAIT_RANGES=((0x4C5260,0x4C529B),(0x4C4210,0x4C4271),(0x4CD350,0x4CD4CE),(0x4CB5F0,0x4CB698),
 (0x4CCE20,0x4CD056),(0x4D5EC0,0x4D5FA7),(0x4D5B70,0x4D5BEC),(0x4128F0,0x412A10),(0x4CCB30,0x4CCB85))
WAIT_CODE=frozenset(a for lo,hi in WAIT_RANGES for a in range(lo,hi))

class SchoolDialogueWaitEmulator(SchoolSecondLiveTextEmulator):
 def __init__(self):
  self.wait_loading=False;super().__init__()

 def _write_hook(self,uc,access,address,size,value,context):
  if not self.wait_loading:return super()._write_hook(uc,access,address,size,value,context)
  if not any(a<=address and address+size<=b for a,b in self.wait_allowed):raise RuntimeError(f'wait finite write {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')

 def _hook(self,uc,address,size,context):
  if not self.wait_loading:return super()._hook(uc,address,size,context)
  sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
  if address in (0x4C5260,0x4C4210):
   offset=696 if address==0x4C5260 else 700;caller=0x4CF020 if address==0x4C5260 else 0x4CF040
   args=[self.read(sp+4+i*4) for i in range(3)]
   if (recv,ret,args)!=(VM,caller,[0,self.read(TACT+0x64)+offset,1]):raise RuntimeError('natural wait handler exact source caller')
   self.wait_handlers.append({'va':hex(address),'receiver':recv,'args':args,'return_va':hex(ret)})
  if address==0x4CB5F0:
   if ret!=0x4CD3B7 or recv!=VM+0x430+len(self.wait_predicates)*0xAB8 or len(self.wait_predicates)>=10:raise RuntimeError('natural all-object readiness source caller')
   self.wait_predicates.append({'receiver':recv,'return_value':None})
  if address==0x4CD3B7:
   if not self.wait_predicates or self.wait_predicates[-1]['return_value']is not None:raise RuntimeError('natural readiness return order')
   self.wait_predicates[-1]['return_value']=uc.reg_read(UC_X86_REG_EAX)&255
  if address in (0x4D5EC0,0x4128F0,0x4CCB30):
   frame=uc.reg_read(UC_X86_REG_EBP)
   if address==0x4D5EC0:
    args=[self.read(sp+4+i*4) for i in range(5)];wanted=[frame-0x20,0,0,1024,768]
    if (recv,ret,args)!=(0x7E1110,0x4CD402,wanted):raise RuntimeError('natural original mouse-result source call')
    self.wait_inputs.append({'kind':'mouse','va':hex(address),'receiver':recv,'args':args,'return_va':hex(ret),'output':args[0]})
   elif address==0x4128F0:
    args=[self.read(sp+4),self.read(sp+8)]
    if recv!=TASK+0x10B8 or ret not in (0x4CD432,0x4CCFF7) or args!=[57,0]:raise RuntimeError('natural original keyboard source call')
    self.wait_inputs.append({'kind':'keyboard','va':hex(address),'receiver':recv,'args':args,'return_va':hex(ret)})
   else:
    args=[self.read(sp+4+i*4) for i in range(4)]
    if (recv,ret,args)!=(VM,0x4CD02D,[0,0,frame-0xC,frame-0x10]):raise RuntimeError('natural original confirmation mouse source call')
    self.wait_inputs.append({'kind':'mouse_buttons','va':hex(address),'receiver':recv,'args':args,'return_va':hex(ret),'output':args[2:]})
  if address in (0x4CD402,0x4CD432,0x4CCFF7,0x4CD02D):
   record=self.wait_inputs[-1]
   if record['return_va']!=hex(address):raise RuntimeError('original input return order')
   record['return_eax']=uc.reg_read(UC_X86_REG_EAX)
   if record['kind']=='mouse':record['output_hex']=bytes(uc.mem_read(record['output'],14)).hex()
   elif record['kind']=='mouse_buttons':record['output_hex']=[bytes(uc.mem_read(a,4)).hex() for a in record['output']]
  if address==0x4D29E0 and ret==0x4CCFCF:
   record={'va':hex(address),'receiver':recv,'args':[self.read(sp+4+i*4) for i in range(16)],'return_va':hex(ret),'return_value':0}
   if [record]!=self.step_expected['arrow_draws']:raise RuntimeError('original exact confirmation arrow terminal')
   self.arrow_draws.append(record);self._stub_return(0,64);return
  if address in WAIT_CODE:self.visited.add(address);return
  return SchoolSecondLiveTextEmulator._hook(self,uc,address,size,context)

 def one_wait_update(self,index,events):
  self.step_expected=advance(self.script_regions(),events);self.wait_predicates=[];self.wait_handlers=[];self.wait_inputs=[];self.arrow_draws=[]
  self.text_draws=[];self.text_updates=[];self.board_records=[];self.board_index=46
  sp=STACK+0xFF00;self.write(sp,RETURN);self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_ECX,VM)
  self.uc.emu_start(0x4CE8F0,RETURN,timeout=2_000_000,count=100000)
  if (self.uc.reg_read(UC_X86_REG_EIP),self.uc.reg_read(UC_X86_REG_ESP),self.uc.reg_read(UC_X86_REG_EAX))!=(RETURN,STACK+0xFF04,1):raise RuntimeError('wait original root return')
  if self.script_regions()!=self.step_expected['after'] or self.wait_predicates!=self.step_expected['predicates'] or self.text_draws!=self.step_expected['text_draws'] or self.arrow_draws!=self.step_expected['arrow_draws'] or [r['kind'] for r in self.wait_inputs]!=self.step_expected['input_call_order']:raise RuntimeError('complete independent natural wait step '+str(index))
  if self.board_records!=self.wait_parent['presentation']:raise RuntimeError('wait original board presentation changed')
  return {'index':index,'events':deepcopy(events),'after':self.script_regions(),'state':self.step_expected['state'],'predicates':self.wait_predicates,'input_calls':self.wait_inputs,
   'handlers':self.wait_handlers,'text_draws':self.text_draws,'arrow_draws':self.arrow_draws,'text_updates':self.text_updates,'presentation_sha256':hashlib.sha256(trace_bytes(self.board_records)).hexdigest(),
   'natural_return':{'va':RETURN,'sp':STACK+0xFF04,'eax':1}}

 def complete_waits(self,second):
  if self.bridge.closed or not self.live_loading or self.uc.reg_read(UC_X86_REG_EIP)!=RETURN or self.read(VM+0x1C)!=244:raise RuntimeError('wait requires actual live second return')
  inputs={'mouse_words':[self.read(TASK+o) for o in (0x198C,0x1990,0x19A0)],'space_key_byte':self.read(TASK+0x10B8+0x480+57,'B'),
   'mouse_position':[self.read(TASK+o,'H') for o in (0x196C,0x1970)],'TASK':TASK,'driver':'declared bounded original VM calls; captured zero input buffers','hold_updates':HOLD_UPDATES}
  if inputs['mouse_words']!=[0,0,0] or inputs['space_key_byte']!=0:raise RuntimeError('captured no-input buffers required')
  before=self.script_regions();self.wait_parent=second
  self.wait_allowed=[(STACK,STACK+65536),(VM+0x1C,VM+0x26),(VM+0x30,VM+0x34),(VM+0x93E2,VM+0x93E3),(NODE+4,NODE+6),(0x7A4E18,0x7A4E20)]
  self.wait_allowed += [(OBJECT+i*0x110+o,OBJECT+i*0x110+o+2) for i in range(2) for o in (24,26,30,34)]
  retained=self.capture_scene_memory(self.wait_allowed[1:]);steps=[];self.wait_loading=True;self.second_loading=True
  try:
   for index in range(80):
    step=self.one_wait_update(index,{'mouse_buttons':0,'space_key':0});steps.append(step)
    if self.read(VM+0x1C)==248 and self.read(VM+0x20,'H')==0:break
   else:raise RuntimeError('natural text wait instruction limit')
   released=index;steps.append(self.one_wait_update(index+1,{'mouse_buttons':0,'space_key':0}))
   for j in range(HOLD_UPDATES):steps.append(self.one_wait_update(released+2+j,{'mouse_buttons':0,'space_key':0}))
   pixels=[self.bridge.readback(t['pointer']) for t in self.resource_textures]
   if pixels!=self.resource_pixels:raise RuntimeError('wait both complete actual textures retained')
   return {'inputs':inputs,'before':before,'after':self.script_regions(),'steps':steps,'text_wait_release_update':released,
    'confirmation_started_update':released+1,'held_confirmation_updates':HOLD_UPDATES,'actual_readbacks':pixels,'resources_retained':True,
    'natural_text_readiness_executed':True,'original_input_query_bodies_executed':True,'live_input_capture_executed':False,'GPU_draw_or_present_executed':False,
    'world_update_loop_executed':False,'waves_executed':False,'dialogue_playback_completed':False,**self.verify_scene_memory(retained)}
  finally:self.wait_loading=False;self.second_loading=False

 def complete_second(self,first):
  second=super().complete_second(first)
  self.resource_textures=[first['texture'],second['texture']];self.resource_pixels=[first['actual_readback'],second['actual_readback']]
  return {'second_live_text':second,'waits':self.complete_waits(second)}

def report(helper_path,emulator_type=SchoolDialogueWaitEmulator):
 helper,identity=build_multi(helper_path);parents=(parent_evidence(),read_deployment(),read_opening(),read_entry(),read_preflight(),read_script_opening(),read_parent());cases=[]
 for index in range(3):
  e,text,case=restored_case(index,parents,emulator_type)
  if hashlib.sha256(helper.read_bytes()).hexdigest()!=identity['helper_sha256']:raise ValueError('wait fixed helper identity')
  case['provenance']['helper_sha256']=identity['helper_sha256'];first=e.run_live_text(text,helper,bridge_type=MultiD3D8,continuation=e.complete_second)
  case.update(first.pop('continuation'));case['first_live_text']=first
  if hashlib.sha256(helper.read_bytes()).hexdigest()!=identity['helper_sha256']:raise ValueError('wait helper changed during case')
  cases.append(case);print('Native '+case['name']+': original text readiness then held confirmation; both textures retained',flush=True)
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'bridge_build':identity,'cases':cases,'inherited_refusals':deepcopy(read_text_parent()['inherited_refusals']),**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use new immutable evidence path')
 path.write_text(report_text(report(ROOT/'.venv-audit'/f'{path.stem}-bridge.exe')),encoding='utf-8',newline='\n')
