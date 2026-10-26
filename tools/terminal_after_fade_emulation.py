"""Continue original terminal tasks in the current GYBC/CRT lifetime after PC52."""
import argparse,copy,struct,types
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_ECX
from tools import terminal_overlay_emulation as parent
from tools.school_character_prefix_emulation import PREFIX_RANGES

ROOT,SOURCE,CODE,need,sha,terminal=(getattr(parent,n) for n in ('ROOT','SOURCE','CODE','need','sha','terminal'))
CTRL,TASK,MAIN,INPUT,VM,WORK,STACK,RETURN,SCRIPT,MANAGER=(getattr(parent,n) for n in ('CTRL','TASK','MAIN','INPUT','VM','WORK','STACK','RETURN','SCRIPT','MANAGER'))
EXTRA_RANGES=((0x4C5430,0x4C5587),(0x4C76B0,0x4C7770),(0x4C7AB0,0x4C7B15),(0x4C2670,0x4C2730),(0x4C1E20,0x4C1EB0),
 (0x4C61C0,0x4C6500),(0x4CA030,0x4CA1B0),(0x4CA600,0x4CA860),(0x4CBDB0,0x4CBDF0),(0x4CCB90,0x4CCE1C))+PREFIX_RANGES
RANGES=parent.RANGES+EXTRA_RANGES
ALLOWED=frozenset(a for lo,hi in RANGES for a in range(lo,hi))
REFERENCE=types.FunctionType(parent.REFERENCE.__code__,dict(parent.REFERENCE.__globals__,RANGES=RANGES))
OBSERVED={0x454CF0:(0,0),0x4CE8F0:(0,0),0x497AA0:(0,0),0x4977A0:(0,0),0x4C5430:(3,12),0x4C5500:(3,12),0x4C2670:(3,12),0x4C61C0:(3,12)}

class FadeMachine(parent.OverlayMachine):
 source_code=types.FunctionType(parent.OverlayMachine.source_code.__code__,dict(parent.OverlayMachine.source_code.__globals__,ALLOWED=ALLOWED,REFERENCE=REFERENCE))
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.after_fade_active=False;self.fade_calls=[];self.fade_stack=[];self.fade_writes=[];self.fade_frames=[];self.pending_resource=None
  self.font_target=self.get(0x5920A0);self.map_new(self.font_target,1)
 def compact(self):
  return dict(PC=self.get(VM+28),wait=self.get(VM+0x92E0,'B'),value=self.get(WORK+0x2490,'i'),delta=self.get(WORK+0x2494,'i'),active=self.get(WORK+0x2499,'B'),status=self.get(WORK+0x249A,'B'),remaining=self.get(WORK+0x249C,'i'))
 def code(self,uc,at,size,context):
  if self.after_fade_active:
   sp=uc.reg_read(UC_X86_REG_ESP)
   if at==self.font_target or at==0x407870 and (self.get(sp+4),self.get(sp+8))!=(20,0):
    n=14 if at==self.font_target else 2
    self.pending_resource=dict(kind='CreateFontA' if n==14 else 'new_image_resource',entry=at,receiver=uc.reg_read(UC_X86_REG_ECX),caller=self.get(sp),args=[self.get(sp+4+j*4) for j in range(n)],CPU=self.cpu(),first_instruction_executed=False,stack=bytes(uc.mem_read(STACK,0x20000)).hex(),SEH=bytes(uc.mem_read(0,4)).hex(),open_calls=[self.fade_calls.index(x) for x in self.fade_stack])
    uc.emu_stop();return
  super().code(uc,at,size,context)
  if not self.after_fade_active:return
  self.close_fade_returns(at,uc.reg_read(UC_X86_REG_ESP))
  if at in OBSERVED:
   n,pop=OBSERVED[at];sp=uc.reg_read(UC_X86_REG_ESP);r=dict(entry=at,receiver=uc.reg_read(UC_X86_REG_ECX),caller=self.get(sp),args=[self.get(sp+4+4*j) for j in range(n)],return_ESP=sp+4+pop,before=self.compact(),cpu_before=self.cpu())
   self.fade_calls.append(r);self.fade_stack.append(r)
 def close_fade_returns(self,at,sp):
  while self.fade_stack and (at,sp)==(self.fade_stack[-1]['caller'],self.fade_stack[-1]['return_ESP']):
   r=self.fade_stack.pop();r.update(after=self.compact(),cpu_after=self.cpu(),result=self.cpu()['EAX'])
 def write_hook(self,uc,access,at,size,value,context):
  super().write_hook(uc,access,at,size,value,context)
  if self.after_fade_active and (VM<=at<VM+0x9400 or WORK<=at<WORK+0x24C0 or INPUT<=at<INPUT+0x680 or at==0):
   self.fade_writes.append(dict(pc=uc.reg_read(UC_X86_REG_EIP),address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))
 def queue_state(self):
  heads=self.get(MANAGER+16);arena=self.get(MANAGER+20);used=self.get(MANAGER+0x30)-arena
  need(0<=used<=65536,'bounded current arena')
  return dict(manager=bytes(self.uc.mem_read(MANAGER,0x38)).hex(),heads=bytes(self.uc.mem_read(heads,4096*8)).hex(),arena_pointer=arena,used=used,arena=bytes(self.uc.mem_read(arena,used)).hex(),unused_tail_sha256=sha(bytes(self.uc.mem_read(arena+used,65536-used))))
 def advance_task(self):
  before=self.task_state();mark=self.mark();cpu=self.cpu();sp=STACK+0xF000;self.put(sp,RETURN);self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_ECX,TASK)
  self.uc.emu_start(0x454CF0,RETURN,timeout=60_000_000,count=4_000_000);self.close_fade_returns(self.cpu()['EIP'],self.cpu()['ESP'])
  complete=self.cpu()['EIP']==RETURN
  need(complete or self.pending_resource is not None,'genuine next source resource boundary')
  if complete:need(self.cpu()['ESP']==sp+4 and not self.fade_stack,'complete original task ABI and observers')
  return dict(before=before,after=self.task_state(),trace_before=mark,trace_after=self.mark(),cpu_before_setup=cpu,CPU=self.cpu(),root=dict(entry=0x454CF0,receiver=TASK,args=[],SP=sp,return_address=RETURN),returned=complete,pending=copy.deepcopy(self.pending_resource))
 def admission(self):
  a=super().admission();self.prefix=dict(continuation=copy.deepcopy(self.continuation),CPU=self.cpu(),state=self.task_state(),memory=self.snapshot(),trace=self.mark(),task_calls=copy.deepcopy(self.task_calls),task_writes=copy.deepcopy(self.task_writes),task_APIs=copy.deepcopy(self.task_APIs),resource_steps=copy.deepcopy(self.resource_steps),overlay_calls=copy.deepcopy(self.overlay_calls),overlay_commands=copy.deepcopy(self.overlay_commands))
  self.after_fade_active=self.active_overlay=True
  for i in range(128):
   first=len(self.resource_steps);calls=len(self.fade_calls);writes=len(self.fade_writes);apis=len(self.task_APIs);q=self.queue_state();state=self.task_state();mark=self.mark()
   self.resource_root('original_continuation_queue_heads_reset',0x40DB90,receiver=MANAGER);self.resource_root('original_continuation_queue_arena_reset',0x40DC80,receiver=MANAGER)
   reset=self.task_step(0x425DE0,INPUT);task=self.advance_task()
   self.fade_frames.append(dict(index=i,before=state,trace_before=mark,queue_before=q,queue_roots=[first,len(self.resource_steps)],reset=reset,task=task,queue_after=self.queue_state(),calls=[calls,len(self.fade_calls)],writes=[writes,len(self.fade_writes)],APIs=[apis,len(self.task_APIs)]))
   if i%20==0:print(self.live_input['name'],'after-fade',i,self.compact(),flush=True)
   if not task['returned']:break
  else:raise ValueError('next real source resource dependency required')
  self.after_fade_active=self.active_overlay=False
  self.fade=dict(prefix=self.prefix,frames=self.fade_frames,calls=self.fade_calls,writes=self.fade_writes,final=self.task_state(),CPU=self.cpu(),memory=self.snapshot(),trace=self.mark(),pending=self.pending_resource,overlay_calls=copy.deepcopy(self.overlay_calls[len(self.prefix['overlay_calls']):]),commands=copy.deepcopy(self.overlay_commands[len(self.prefix['overlay_commands']):]))
  return a
 def run(self):
  r=super().run();r['after_fade']=self.fade;return r

def source_contract():
 return dict(parent=parent.source_contract(),first_PC=52,first_WORK_remaining=59,first_wait=1,forward_roots=[0x40DB90,0x40DC80,0x425DE0,0x454CF0],new_VM_or_work_update_roots=0,next_resource_not_stubbed=True,host_PC_wait_phase_or_work_writes=False,extra_code=[dict(start=a,end=b,sha256=sha(CODE[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES])

def run_case(c,ch,gh,ticks=None):
 # Keep the established current-native lifetime and failure cleanup algorithm.
 class Diagnostics:
  @staticmethod
  def save(path,data):return terminal.save(path.replace('terminal-overlay-diagnostic-','terminal-after-fade-diagnostic-'),data)
 call=types.FunctionType(parent.run_case.__code__,dict(parent.run_case.__globals__,OverlayMachine=FadeMachine,terminal=Diagnostics),closure=parent.run_case.__closure__)
 return call(c,ch,gh,ticks)

def helpers():
 a,aa=parent.platform.build(ROOT/'tools/terminal_overlay_crt_platform.cs','terminal-after-fade-crt');b,bb=parent.platform.build(ROOT/'tools/terminal_overlay_d3d8_platform.cs','terminal-after-fade-gpu');return a,b,dict(CRT=aa,GPU=bb)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case',type=int);a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable after-fade report');ch,gh,b=helpers();rows=[]
 for c in (parent.parent.corpus() if a.case is None else [parent.parent.corpus()[a.case]]):
  r=run_case(c,ch,gh);rows.append(r);print('source completed',c['name'],r['after_fade']['pending']['kind'],r['after_fade']['frames'][-1]['task']['returned'],flush=True)
 terminal.save(a.out,dict(schema_version=1,source_contract=source_contract(),helper_build=b,cases=rows,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False))
