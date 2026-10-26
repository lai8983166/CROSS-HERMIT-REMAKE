"""Captured device bytes through current terminal confirmation and original panel27."""
import argparse,copy,hashlib,struct,types
from functools import lru_cache
import unicorn.x86_const as x86
from tools import terminal_dialogue_emulation as parent
from tools import school_retained_keyboard as keyboard
from tools.school_vm_character import native_ranges as character_ranges

ROOT,CODE,need,sha,terminal,MAIN,VM,STACK,RETURN,TASK,INPUT,MANAGER=(getattr(parent,n) for n in ('ROOT','CODE','need','sha','terminal','MAIN','VM','STACK','RETURN','TASK','INPUT','MANAGER'))
KEYBOARD=MAIN+0x10B8;NODE=VM+0x6F60+7*0xE0;OBJECT=VM+0x430+7*0xAB8
EXTRA_RANGES=((0x4113D5,0x4116A4),(0x4C5EA0,0x4C5FBE),(0x4CC0F0,0x4CC3C3),(0x4CC600,0x4CC810))+character_ranges()
RANGES=parent.RANGES+EXTRA_RANGES;ALLOWED=frozenset(a for lo,hi in RANGES for a in range(lo,hi))
REFERENCE=types.FunctionType(parent.REFERENCE.__code__,dict(parent.REFERENCE.__globals__,RANGES=RANGES))

@lru_cache(maxsize=1)
def input_contract():
 c=keyboard.inputs()
 return dict(acceptance_pins=c['acceptance_pins'],streams={str(k):v for k,v in c['streams'].items()},source_sha256=c['source_sha256'])

class ConfirmationMachine(parent.DialogueMachine):
 source_code=types.FunctionType(parent.DialogueMachine.source_code.__code__,dict(parent.DialogueMachine.source_code.__globals__,ALLOWED=ALLOWED,REFERENCE=REFERENCE))
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.confirm_active=False;self.confirm_stop=None;self.confirm_segments=[];self.confirm_frames=[];self.confirm_leaves=[];self.confirm_writes=[];self.confirm_commands=[];self.confirm_queries=[];self.confirm_bindings=[];self.confirm_count=self.confirm_write_count=0;self.confirm_ih=hashlib.sha256();self.confirm_wh=hashlib.sha256()
  self.mutable.append((KEYBOARD,KEYBOARD+0xA00))
 def confirm_mark(self):return dict(instructions=self.confirm_count,writes=self.confirm_write_count,code_sha256=self.confirm_ih.hexdigest(),write_sha256=self.confirm_wh.hexdigest())
 def confirm_capture(self,full=True):
  memory=self.snapshot() if full else [dict(pointer=a,bytes=b-a+1,sha256=sha(bytes(self.uc.mem_read(a,b-a+1)))) for a,b,_ in self.uc.mem_regions()]
  return dict(memory=memory,CPU=self.cpu(),state=self.task_state(),queue=self.queue_state(),trace=self.mark(),local_trace=self.confirm_mark())
 def confirm_state(self):return dict(PC=self.get(VM+28),wait=self.get(VM+32,'H'),opcode=self.get(VM+34,'H'),selected_layer=self.get(VM+0x1CC,'B'),space_current=self.get(KEYBOARD+0x4B9,'B'),panel_hex=self.read(NODE,0xE0).hex())
 def write_hook(self,uc,access,at,size,value,context):
  super().write_hook(uc,access,at,size,value,context)
  if self.confirm_active:
   if getattr(self,'keyboard_fragment',False):need(KEYBOARD<=at and at+size<=KEYBOARD+0xA00 or STACK<=at and at+size<=STACK+0x20000,'original keyboard finite write domain')
   self.confirm_write_count+=1;self.confirm_wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
   if VM<=at<VM+0x9400 or KEYBOARD<=at<KEYBOARD+0xA00 or TASK<=at<TASK+0x190 or at==0:self.confirm_writes.append(dict(pc=self.getreg('EIP'),address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))
 def code(self,uc,at,size,context):
  active=self.confirm_active
  if active:
   if at==self.confirm_stop:uc.emu_stop();return
   if at==0x4CE9C5:
    p=self.get(VM+16)+self.get(VM+28);op,n=struct.unpack('<HH',self.read(p,4));self.confirm_commands.append(dict(PC=self.get(VM+28),opcode=op,bytes=n,source_pointer=p))
   if at in parent.parent.TASK_APIS and self.get(self.getreg('ESP'))==parent.parent.TASK_APIS[at][2]:
    sp=self.getreg('ESP');ret=self.get(sp);first=len(self.task_APIs);super().code(uc,at,size,context);need(len(self.task_APIs)==first+1,'one actual confirmation task query');r=self.task_APIs[-1];self.confirm_leaves.append(dict(kind='TASK',call=dict(r,sp=sp,return_va=ret,pop=4,value=r['result'],memory_outputs=[],new_mappings=[])));return
   if at in (0x4C5EA0,0x4CC600,0x4CC0F0,0x4CC7D0,0x4CC810,0x4CA600,0x4CBDB0,0x407870,0x4079C0,0x4128F0,0x4CCFF7,0x4CD02D,0x4CD350,0x4CD402,0x4CD432):
    sp=self.getreg('ESP');self.confirm_queries.append(dict(entry=at,CPU=self.cpu(),receiver=self.getreg('ECX'),stack_hex=self.read(sp,68).hex(),panel_hex=self.read(NODE,0xE0).hex(),object_hex=self.read(OBJECT,0xAB8).hex()))
  super().code(uc,at,size,context)
  if active and at in ALLOWED:self.confirm_count+=1;self.confirm_ih.update(struct.pack('<I',at))
 def confirm_segment(self,label,entry,stop=RETURN,root=None,kind='task'):
  before=self.cpu();trace=self.mark();local=self.confirm_mark();first=len(self.confirm_leaves)
  if root:
   sp=STACK+0xF000;self.put(sp,RETURN)
   for j,a in enumerate(root['args']):self.put(sp+4+j*4,a)
   self.uc.reg_write(x86.UC_X86_REG_ESP,sp);self.uc.reg_write(x86.UC_X86_REG_ECX,root['receiver'])
  self.confirm_stop=stop;self.uc.ctl_remove_cache(entry,entry+1);self.uc.emu_start(entry,0,timeout=60_000_000,count=4_000_000);self.confirm_stop=None
  need(self.getreg('EIP')==stop,'natural original confirmation segment '+label)
  if root and stop==RETURN:need(self.getreg('ESP')==STACK+0xF004,'complete original confirmation root stack '+label)
  row=dict(label=label,kind=kind,entry=entry,stop=stop,root=root,before_CPU=before,CPU=self.cpu(),trace_before=trace,trace_after=self.mark(),local_before=local,local_after=self.confirm_mark(),leaves=[first,len(self.confirm_leaves)]);self.confirm_segments.append(row);return row
 def confirm_frame(self,phase,stop=RETURN):
  index=len(self.confirm_frames);before=self.task_state();queue=self.queue_state();first=len(self.confirm_segments)
  for label,va,recv in (('heads',0x40DB90,MANAGER),('arena',0x40DC80,MANAGER),('input',0x425DE0,INPUT),('task',0x454CF0,TASK)):
   self.confirm_segment(label+'_'+str(index),va,stop if label=='task' else RETURN,dict(receiver=recv,args=[]))
  row=dict(index=index,phase=phase,before=before,after=self.task_state(),queue_before=queue,queue_after=self.queue_state(),segments=[first,len(self.confirm_segments)],capture=self.confirm_capture(False),state=self.confirm_state());self.confirm_frames.append(row)
  print(self.live_input['name'],phase,index,row['state']['PC'],row['state']['wait'],flush=True);return row
 def captured(self,capture):
  scene={'neutral_running':76,'timeout_before_combat':77}.get(self.live_input['name']);index=len(self.confirm_bindings)
  need(scene in (76,77) and 0<=index<3 and capture==input_contract()['streams'][str(scene)]['captures'][index],'exact pinned capture for current terminal branch and sequence')
  raw=bytes.fromhex(capture['raw_device_hex']);need(len(raw)==256,'full pinned raw device buffer');before=self.read(KEYBOARD,0xA00);bound=bytearray(before);bound[12:268]=raw;cpu=self.cpu();trace=self.mark();local=self.confirm_mark();self.uc.mem_write(KEYBOARD+12,raw);bp=STACK+0xF800;self.put(bp-4,KEYBOARD)
  for key,value in dict(EBP=bp,ESP=bp-0x70,EFLAGS=0x202).items():self.uc.reg_write(getattr(x86,'UC_X86_REG_'+key),value)
  self.keyboard_fragment=True
  try:step=self.confirm_segment('captured_'+capture['label'],0x4113D5,0x4116A4,kind='keyboard')
  finally:self.keyboard_fragment=False
  step['bound_CPU']=step['before_CPU'];step['before_CPU']=cpu
  after=self.read(KEYBOARD,0xA00);need(after==keyboard.predict_keyboard(bytes(bound)),'independent whole original keyboard processing');need(self.getreg('EBP')==bp and self.getreg('ESP')==bp-0x70,'original keyboard stack balance')
  result=dict(capture=copy.deepcopy(capture),before_CPU=cpu,trace_before=trace,local_before=local,before_hex=before.hex(),bound_hex=bound.hex(),after_hex=after.hex(),only_device_output_written=dict(pointer=KEYBOARD+12,bytes=256),fragment=dict(va=0x4113D5,bp=bp,sp=bp-0x70,receiver_slot=bp-4,receiver=KEYBOARD,stop=0x4116A4),segment_index=len(self.confirm_segments)-1,after=self.confirm_capture());self.confirm_bindings.append(result);return result
 def admission(self):
  a=super().admission();self.confirm_prefix=dict(CRT_APIs=len(self.crt_apis),resource_steps=len(self.resource_steps),task_APIs=len(self.task_APIs),extra_counts=copy.deepcopy(dict(self.extra_counts)),GPU_wire=len(self.gpu.trace),GDI_trace=len(self.name_platform.trace),overlay_commands=len(self.overlay_commands));self.confirm_before=self.confirm_capture();self.confirm_active=self.active_overlay=True
  scene=76 if self.live_input['name']=='neutral_running' else 77;stream=input_contract()['streams'][str(scene)];self.captured(stream['captures'][0])
  for _ in range(2):
   self.confirm_frame('held_confirmation');need((self.get(VM+28),self.get(VM+32,'H'),self.get(KEYBOARD+0x4B9,'B'))==(118,1,0),'captured idle holds original confirmation')
  self.captured(stream['captures'][1]);self.confirm_frame('captured_press');need((self.get(VM+28),self.get(VM+32,'H'),self.get(KEYBOARD+0x4B9,'B'))==(118,0,128),'original task consumes captured space');confirmed=self.confirm_capture()
  self.captured(stream['captures'][2]);need(self.get(KEYBOARD+0x4B9,'B')==0,'original keyboard release');self.confirm_frame('panel27');need(self.get(VM+28)==134,'original27 complete task returns PC134');completion=self.confirm_capture()
  for _ in range(100):
   if self.get(VM+32,'H')==0:break
   self.confirm_frame('panel_readiness');need(self.get(VM+28)==134,'only panel wait before134')
  else:raise ValueError('bounded original panel readiness')
  ready=self.confirm_capture();self.confirm_frame('select_layer7');need((self.get(VM+28),self.get(VM+32,'H'),self.get(VM+0x1CC,'B'))==(142,0,7),'original43 selects next text layer7');self.confirm_frame('next_sentence_font',self.font_target)
  need((self.get(VM+28),self.get(VM+34,'H'))==(142,17),'next original17 font boundary');sp=self.getreg('ESP');pending=dict(entry=self.font_target,caller=self.get(sp),args=[self.get(sp+4+j*4) for j in range(14)],CPU=self.cpu(),first_instruction_executed=False);need(pending['caller']==0x4CAD09,'natural next text font caller');final=self.confirm_capture();self.confirm_active=self.active_overlay=False
  readbacks=dict(GYBC=self.gpu.readback(self.texture_native),name=self.gpu.readback(self.name_native),portrait=self.gpu.readback(self.portrait_native),dialogue=self.gpu.readback(self.dialogue_native))
  self.confirm_result=dict(prefix=self.confirm_prefix,before=self.confirm_before,confirmed=confirmed,panel_completion=completion,ready=ready,font_boundary=final,final=final,pending_font=pending,scene_capture=scene,stream=copy.deepcopy(stream),bindings=self.confirm_bindings,segments=self.confirm_segments,frames=self.confirm_frames,leaves=self.confirm_leaves,writes=self.confirm_writes,commands=self.confirm_commands,queries=self.confirm_queries,readbacks=readbacks,accounting=self.get(0x765720),panel_record=NODE,text_object=OBJECT)
  return a
 def run(self):
  r=super().run();r['terminal_confirmation']=self.confirm_result;return r

def source_contract():return dict(parent=parent.source_contract(),captured_inputs=input_contract(),first_PC=118,first_wait=1,final_PC=142,next_text_index=1,font_created=False,keyboard=KEYBOARD,keyboard_bytes=0xA00,raw_device_offset=12,raw_device_bytes=256,keyboard_fragment=[0x4113D5,0x4116A4],forward_roots=[0x40DB90,0x40DC80,0x425DE0,0x454CF0],new_VM_or_handler_roots=0,derived_input_host_writes=0,PC_or_wait_host_writes=0,new_OS_input=False,draw_or_Present=False,extra_code=[dict(start=a,end=b,sha256=sha(CODE[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES])
def helpers(prefix='terminal-confirmation'):return parent.helpers(prefix)
def run_case(c,ch,gh,ticks=None):
 class Diagnostics:
  @staticmethod
  def save(path,data):return terminal.save(path.replace('terminal-overlay-diagnostic-','terminal-confirmation-diagnostic-').replace('.json.gz','-20261026.json.gz'),data)
 fn=types.FunctionType(parent.parent.overlay.run_case.__code__,dict(parent.parent.overlay.run_case.__globals__,OverlayMachine=ConfirmationMachine,terminal=Diagnostics),closure=parent.parent.overlay.run_case.__closure__);return fn(c,ch,gh,ticks)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case',type=int);p.add_argument('--helper-prefix',default='terminal-confirmation');a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable confirmation report');ch,gh,b=helpers(a.helper_prefix);rows=[]
 for c in (parent.parent.overlay.parent.corpus() if a.case is None else [parent.parent.overlay.parent.corpus()[a.case]]):
  rows.append(run_case(c,ch,gh));print('confirmation source',c['name'],'next font142 unexecuted',flush=True)
 terminal.save(a.out,dict(schema_version=1,source_contract=source_contract(),helper_build=b,cases=rows,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False))
