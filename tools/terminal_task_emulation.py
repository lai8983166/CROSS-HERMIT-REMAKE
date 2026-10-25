"""Fresh terminal task/VM admission through the first original resource request."""
import argparse,ctypes,json,struct,types
from unicorn.x86_const import UC_X86_REG_ESP,UC_X86_REG_ECX,UC_X86_REG_EAX,UC_X86_REG_EIP
from tools import terminal_work_emulation as parent
from tools.school_world_task_start import TASK_NATIVE
from tools.school_task_cycle import RESET_NATIVE
from tools.school_vm_present import NATIVE as OVERLAY_NATIVE
from tools.school_task_frame import ActualIME

ROOT,SOURCE,need,sha,terminal=parent.ROOT,parent.SOURCE,parent.need,parent.sha,parent.terminal
CTRL,UNIT,TARGET,TASK,VM,WORK,SCRIPT,FINE=(getattr(parent,n) for n in ('CTRL','UNIT','TARGET','TASK','VM','WORK','SCRIPT','FINE'))
MAIN=0x12A00000;INPUT=MAIN+0x180;RETURN=0x12100000;STACK=0x12000000;STOP=0x407870
EXTRA_REGIONS=((MAIN,0x10000),(0,0x1000),(0x76182000,0x1000),(0x77020000,0x1000))
REGIONS=parent.REGIONS+EXTRA_REGIONS
EXTRA_RANGES=TASK_NATIVE+RESET_NATIVE+OVERLAY_NATIVE+((0x453F10,0x4547C2),(0x41E500,0x41E588),(0x41D790,0x41D7BB))
RANGES=parent.RANGES+EXTRA_RANGES
ALLOWED=frozenset(a for lo,hi in RANGES for a in range(lo,hi))
REFERENCE=types.FunctionType(parent.REFERENCE.__code__,dict(parent.REFERENCE.__globals__,RANGES=RANGES))
ROOTS=parent.ROOTS|{0x425DE0,0x454CF0,0x453F10}
OBSERVED={0x425DE0:(0,0),0x425E60:(1,4),0x425C70:(0,0),0x56CD4A:(1,4),
 0x454CF0:(0,0),0x453F10:(0,0),0x457830:(0,0),0x425ED0:(1,4),0x425A10:(0,0),0x425A50:(0,0),
 0x4CE8F0:(0,0),0x42FC60:(3,12),0x496DC0:(0,0),0x4C1F40:(4,16),
 0x4D29E0:(16,64),0x4D2CA0:(9,36),0x4075E0:(0,0),0x4077C0:(1,4)}
APIS={0x76182A80:('ImmGetOpenStatus',0x5920EC,0x425C99),0x770206E0:('lstrlenA',0x5922C4,0x425A7E)}


def corpus():return parent.corpus()


def source_contract():
 raw=SOURCE.read_bytes()
 for target,(name,slot,ret) in APIS.items():need(struct.unpack_from('<I',raw,slot-0x400000)[0]==target,'unchanged original API import '+name)
 return dict(parent_driver=parent.source_contract(),fresh_instance=True,combat_snapshot_loaded=False,
  owner_method_inputs=dict(owner=MAIN,input=INPUT,empty_buffers=True,IME_context=0,overlay_origin=[0,0],inactive_audio=True),
  first_root_globals={hex(0x7A4A00):MAIN,hex(0x7A49FC):MAIN},source_input_reset_root=0x425DE0,
  complete_post_terminal_frames=2,pending_third_task_root=0x454CF0,first_unexecuted_resource_entry=STOP,
  new_VM_roots=0,host_VM_PC_or_wait_writes=False,game_function_results_stubbed=False,
  resource_cache_or_device_initialized=False,render_gate_closed_to_bypass=False,original_outer_scheduler_connected=False,
  pending_task_or_VM_natural_return=False,original_guest_cleanup_executed=False,
  extra_code=[dict(start=a,end=b,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES])


class TaskMachine(parent.WorkMachine):
 source_code=types.FunctionType(parent.WorkMachine.source_code.__code__,dict(parent.WorkMachine.source_code.__globals__,ALLOWED=ALLOWED,REFERENCE=REFERENCE))
 base_call=types.FunctionType(parent.WorkMachine.base_call.__code__,dict(parent.WorkMachine.base_call.__globals__,ROOTS=ROOTS))
 snapshot=types.FunctionType(parent.WorkMachine.snapshot.__code__,dict(parent.WorkMachine.snapshot.__globals__,REGIONS=REGIONS))

 def __init__(self,c,tick_inputs=None):
  super().__init__(c,tick_inputs)
  for a,n in EXTRA_REGIONS:self.uc.mem_map(a,n)
  self.put(0x7A4A00,MAIN);self.put(0x7A49FC,MAIN)
  self.mutable += [(INPUT,INPUT+0x680),(MAIN+0x9321,MAIN+0x9323),(MAIN+0x8F21,MAIN+0x8F23),(0,4),(TASK+0x117F20,TASK+0x117F21)]
  self.task_active=False;self.task_calls=[];self.task_stack=[];self.task_writes=[];self.task_APIs=[];self.ime=ActualIME()
  self.kernel.lstrlenA.argtypes=[ctypes.c_char_p];self.kernel.lstrlenA.restype=ctypes.c_int

 def task_state(self):
  return dict(**self.work_state(),owner=bytes(self.uc.mem_read(MAIN,0x10000)).hex(),SEH=bytes(self.uc.mem_read(0,4)).hex(),
   task_input_flag=self.get(TASK+0x117F20,'B'),VM_counter=bytes(self.uc.mem_read(0x7A4E18,8)).hex())

 def close_task_returns(self,at,sp):
  while self.task_stack and (at,sp)==(self.task_stack[-1]['caller'],self.task_stack[-1]['return_ESP']):
   r=self.task_stack.pop();r.update(after=self.task_state(),cpu_after=self.cpu(),result=self.cpu()['EAX'])

 def code(self,uc,at,size,context):
  if at in APIS:
   name,slot,ret=APIS[at];sp=uc.reg_read(UC_X86_REG_ESP);arg=self.get(sp+4);need(self.get(sp)==ret and self.get(slot)==at,'exact original task API call/IAT')
   if name=='ImmGetOpenStatus':
    need(arg==self.get(INPUT+8)==0,'owned null IME context only');observed=self.ime.query(arg);value=observed['result'];extra=dict(observed=observed)
   else:
    need(arg==INPUT+0x528,'original task text buffer');data=self.string(arg);need(data==b'','declared empty task text');value=int(self.kernel.lstrlenA(data));extra=dict(string_hex=data.hex())
   self.task_APIs.append(dict(name=name,import_slot=slot,target=at,caller=ret,args=[arg],result=value,actual_API_executed=True,**extra))
   uc.reg_write(UC_X86_REG_EAX,value&0xFFFFFFFF);uc.reg_write(UC_X86_REG_ESP,sp+8);uc.reg_write(UC_X86_REG_EIP,ret);return
  super().code(uc,at,size,context)
  if not self.task_active:return
  sp=uc.reg_read(UC_X86_REG_ESP);self.close_task_returns(at,sp)
  if at in OBSERVED:
   n,pop=OBSERVED[at];r=dict(entry=at,receiver=uc.reg_read(UC_X86_REG_ECX),caller=self.get(sp),args=[self.get(sp+4+4*j) for j in range(n)],return_ESP=sp+4+pop,before=self.task_state(),cpu_before=self.cpu())
   self.task_calls.append(r);self.task_stack.append(r)

 def write_hook(self,uc,access,at,size,value,context):
  super().write_hook(uc,access,at,size,value,context)
  if self.task_active and (INPUT<=at<INPUT+0x680 or TASK<=at<TASK+0x190 or at==0 or VM<=at<VM+0x9400 or at==TASK+0x117F20):
   self.task_writes.append(dict(pc=uc.reg_read(UC_X86_REG_EIP),address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))

 def task_step(self,entry,receiver):
  before=self.task_state();mark=self.mark();first=len(self.task_calls);writes=len(self.task_writes);apis=len(self.task_APIs)
  call=self.call(entry,receiver=receiver);self.close_task_returns(self.cpu()['EIP'],self.cpu()['ESP']);need(not self.task_stack,'all complete task observations returned')
  return dict(before=before,call=call,after=self.task_state(),trace_before=mark,trace_after=self.mark(),calls=[first,len(self.task_calls)],writes=[writes,len(self.task_writes)],APIs=[apis,len(self.task_APIs)])

 def admission(self):
  self.task_active=True;frames=[]
  for _ in range(2):
   frame=[self.task_step(0x425DE0,INPUT),self.task_step(0x454CF0,TASK),self.task_step(0x453F10,TASK),self.task_step(0x46B470,CTRL)]
   before=self.task_state();mark=self.mark();event=self.event();frame.append(dict(before=before,event=event,after=self.task_state(),trace_before=mark,trace_after=self.mark()));frames.append(frame)
  reset=self.task_step(0x425DE0,INPUT);before=self.task_state();cpu_before=self.cpu();mark=self.mark();first=len(self.task_calls);writes=len(self.task_writes);apis=len(self.task_APIs)
  sp=STACK+0xF000;self.put(sp,RETURN);self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_ECX,TASK)
  self.uc.emu_start(0x454CF0,STOP,timeout=60_000_000,count=10_000_000);cpu=self.cpu();need(cpu['EIP']==STOP,'genuine first original resource entry boundary')
  packet=cpu['ECX'];pending=dict(entry=STOP,first_instruction_executed=False,receiver=packet,caller=self.get(cpu['ESP']),args=[self.get(cpu['ESP']+4),self.get(cpu['ESP']+8)],
   CPU=cpu,stack=bytes(self.uc.mem_read(STACK,0x20000)).hex(),packet=bytes(self.uc.mem_read(packet,128)).hex(),open_calls=[self.task_calls.index(x) for x in self.task_stack])
  partial=dict(before=before,after=self.task_state(),root=dict(entry=0x454CF0,receiver=TASK,args=[],ESP_before=sp,return_address=RETURN,cpu_before=cpu_before,returned=False),
   trace_before=mark,trace_after=self.mark(),calls=[first,len(self.task_calls)],writes=[writes,len(self.task_writes)],APIs=[apis,len(self.task_APIs)],pending=pending)
  self.task_active=False;return dict(frames=frames,reset=reset,partial=partial)

 def run(self):
  self.native=parent.NativeTLS(terminal.parent.parent.parent.world.parent.parent.TLS)
  try:
   initial=self.snapshot();image_before=self.image_identity();self.work_active=True;initialization=self.step(0x497800);self.work_active=False
   target_before=self.state();target_bind=self.call(0x467020,(TARGET,self.combat_input['job']));target_after=self.state()
   roots=[self.call(0x437C90,(u+off,),FINE) for u in (UNIT,TARGET) for off in (0x2F4,0x3E0)]
   before=self.state();bind=self.call(0x467020,(UNIT,self.combat_input['job']));after=self.state();frames=[];events=[]
   for i in range(self.live_input['budget']):
    f=dict(index=i,before=self.state(),entries=[],scanned_slots=[],unit_calls=[],stages=[],controls=[],nested_calls=[],ai_calls=[],gated_calls=[],trace_before=self.mark())
    self.frame_observation=f;self.running_update=True
    try:f['call']=self.call(0x46B470)
    finally:self.frame_observation=None;self.running_update=False
    need(not self.pending_contracts,'all live battle contracts returned');f['after']=self.state();f['trace_after']=self.mark();frames.append(f);events.append(self.event())
    if self.get(TASK+0x174):break
   else:raise ValueError('original terminal selection required')
   admission=self.admission();row=dict(input=self.live_input,combat_input=self.cycle_input,initial=initial,initialization=initialization,image_before=image_before,image_after=self.image_identity(),
    target_bind=dict(before=target_before,call=target_bind,after=target_after),roots=roots,bind_before=before,bind=bind,bind_after=after,world_frames=frames,events=events,
    hit=self.hit_observations,hit_sides=self.hit_sides,contracts=self.contracts,both_hp_writes=self.both_hp_writes,calls=self.calls,APIs=self.api_trace,commands=self.commands,
    admission=admission,task_calls=self.task_calls,task_writes=self.task_writes,task_APIs=self.task_APIs,IME_identity=self.ime.identity,
    final_state=self.state(),pending_CPU=self.cpu(),**self.common())
   row['platform']=dict(creation=self.native.creation,trace=self.native.trace,cleanup=self.native.close());row['blobs']=self.blobs
   need(self.tick_inputs is None or self.tick_index==len(self.tick_inputs),'captured condition time consumed');return row
  except Exception as error:
   self.failure=dict(error=str(error),CPU=self.cpu(),state=self.task_state(),pending=self.task_stack,calls=self.task_calls[-12:],writes=self.task_writes[-32:]);raise
  finally:
   self.task_active=False
   if not self.native.closed:self.native.close()


def report(prefix):
 rows=[]
 for c in corpus():
  m=TaskMachine(c)
  try:r=m.run()
  except Exception:
   if hasattr(m,'failure'):terminal.save(prefix+'-'+c['name']+'.failure.json.gz',dict(accepted=False,failure=m.failure))
   raise
  rows.append(r);print(c['name'],r['instructions'],r['writes'],'PC',m.get(VM+0x1C),flush=True)
 return dict(schema_version=1,source_contract=source_contract(),cases=rows,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();need(not (ROOT/a.out).exists(),'fresh task source output');terminal.save(a.out,report(a.out))
