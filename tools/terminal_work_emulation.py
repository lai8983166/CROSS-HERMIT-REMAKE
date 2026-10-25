"""Original pending pause and explicit sourced terminal work-handler contracts."""
import argparse,json,struct,types
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_ECX
from tools import battle_live_terminal_emulation as parent
from tools.battle_hit_damage_platform import NativeTLS
from tools.battle_lethal_combat import pages
from tools.school_retained_portrait_catalog import commands

ROOT,SOURCE,need,sha,terminal=parent.ROOT,parent.SOURCE,parent.need,parent.sha,parent.terminal
CTRL,UNIT,TARGET,RECORD,TASK,VM,WORK,SCRIPT,FINE=(getattr(parent,n) for n in ('CTRL','UNIT','TARGET','RECORD','TASK','VM','WORK','SCRIPT','FINE'))
REGIONS=parent.REGIONS+((WORK+0x1000,0x2000),)
EXTRA_RANGES=((0x43B250,0x43B338),(0x455160,0x4551B4),(0x4553E0,0x455415),(0x4558A0,0x4558D5),(0x455D00,0x455D35),
 (0x497800,0x497848),(0x4978C0,0x497980),(0x497980,0x497A40),(0x497AA0,0x497C43),(0x4977A0,0x4977C6),
 (0x497C50,0x497C88),(0x498310,0x498739),(0x42D960,0x42D9E2),(0x42D9F0,0x42DA72),(0x56CFCC,0x56CFF3))
RANGES=parent.RANGES+EXTRA_RANGES
ALLOWED=frozenset(a for lo,hi in RANGES for a in range(lo,hi))
REFERENCE=types.FunctionType(parent.REFERENCE.__code__,dict(parent.REFERENCE.__globals__,RANGES=RANGES))
ROOTS=parent.LiveMachine.base_call.__globals__['ROOTS']|{0x497800,0x42D960,0x42D9F0,0x497AA0,0x498310,0x497C50}
# entry -> (visible arguments, callee-popped bytes). Cdecl fade setters pop zero.
OBSERVED={0x4678C0:(0,0),0x43B250:(1,4),0x455160:(1,4),0x4553E0:(1,4),0x4558A0:(1,4),0x455D00:(1,4),
 0x497800:(0,0),0x42D960:(3,12),0x42D9F0:(3,12),0x4978C0:(1,0),0x497980:(1,0),0x56CFCC:(0,0),
 0x497AA0:(0,0),0x498310:(0,0),0x4977A0:(0,0),0x497C50:(0,0)}


def corpus():return parent.corpus()[5:7]


def source_contract():
 raw=SOURCE.read_bytes()
 return dict(parent_driver=parent.source_contract(),fresh_battle_instance=True,combat_snapshot_loaded=False,
  task_member60_declared_work_pointer=WORK,original_VM_global=VM,work_object_zero_initial_fields=True,
  explicit_handler_roots=[0x42D960,0x42D9F0],explicit_work_update_roots=[0x497AA0,0x498310],
  VM_PC_not_advanced_by_host=True,normal_VM_or_task_playback_connected=False,world_consumes_pause=True,
  original_game_functions_stubbed=False,original_IAT_unchanged=True,owned_regions=len(REGIONS),
  extra_code=[dict(start=a,end=b,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES],
  inactive_scroll_work_declared=True,script_work_handler_experiment_not_full_script_sequence=True)


class WorkMachine(parent.LiveMachine):
 source_code=types.FunctionType(parent.LiveMachine.source_code.__code__,dict(parent.LiveMachine.source_code.__globals__,ALLOWED=ALLOWED,REFERENCE=REFERENCE))
 base_call=types.FunctionType(parent.LiveMachine.base_call.__code__,dict(parent.LiveMachine.base_call.__globals__,ROOTS=ROOTS))
 snapshot=types.FunctionType(parent.LiveMachine.snapshot.__code__,dict(parent.LiveMachine.snapshot.__globals__,REGIONS=REGIONS))

 def __init__(self,c,tick_inputs=None):
  need(c in corpus(),'exact two terminal work cases');super().__init__(c,tick_inputs)
  self.uc.mem_map(WORK+0x1000,0x2000);self.put(TASK+0x60,WORK)
  self.mutable += [(WORK+0x2490,WORK+0x24C0),(WORK+0x20E8,WORK+0x20E9),(WORK+0x216C,WORK+0x216D),(WORK+0x2230,WORK+0x2231),
   (CTRL+0x108B34,CTRL+0x108B3D),(CTRL+0x2A2FD,CTRL+0x2A301)]
  self.work_active=False;self.work_calls=[];self.work_stack=[];self.key_writes=[]

 def work_state(self):
  return dict(work=bytes(self.uc.mem_read(WORK,0x24C0)).hex(),VM=bytes(self.uc.mem_read(VM,0x9400)).hex(),
   gates=bytes(self.uc.mem_read(CTRL+0x108B32,12)).hex(),owner_flags=bytes(self.uc.mem_read(CTRL+0x2A2FD,4)).hex(),
   task=bytes(self.uc.mem_read(TASK,0x190)).hex(),remaining=self.get(CTRL+0x2E6F4,'i'),elapsed=self.get(CTRL+0x2E6F8,'i'),
   units=[bytes(self.uc.mem_read(u,0x520)).hex() for u in (UNIT,TARGET)])

 def close_work_returns(self,at,sp):
  while self.work_stack and (at,sp)==(self.work_stack[-1]['caller'],self.work_stack[-1]['return_ESP']):
   r=self.work_stack.pop();r.update(after=self.work_state(),cpu_after=self.cpu(),result=self.cpu()['EAX'])

 def code(self,uc,at,size,context):
  super().code(uc,at,size,context)
  if not self.work_active:return
  sp=uc.reg_read(UC_X86_REG_ESP);self.close_work_returns(at,sp)
  if at in OBSERVED:
   n,pop=OBSERVED[at];r=dict(entry=at,receiver=uc.reg_read(UC_X86_REG_ECX),caller=self.get(sp),args=[self.get(sp+4+j*4) for j in range(n)],
    return_ESP=sp+4+pop,before=self.work_state(),cpu_before=self.cpu())
   self.work_calls.append(r);self.work_stack.append(r)

 def write_hook(self,uc,access,at,size,value,context):
  super().write_hook(uc,access,at,size,value,context)
  if self.work_active and (WORK<=at<WORK+0x24C0 or at==VM+0x92E0 or CTRL+0x108B34<=at<CTRL+0x108B3D):
   self.key_writes.append(dict(pc=uc.reg_read(UC_X86_REG_EIP),address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))

 def step(self,entry,args=(),receiver=WORK):
  before=self.work_state();mark=self.mark();first=len(self.work_calls);writes=len(self.key_writes)
  call=self.call(entry,args,receiver);self.close_work_returns(self.cpu()['EIP'],self.cpu()['ESP']);need(not self.work_stack,'all original work calls returned')
  return dict(before=before,call=call,after=self.work_state(),trace_before=mark,trace_after=self.mark(),calls=[first,len(self.work_calls)],writes=[writes,len(self.key_writes)])

 def work_tick(self):
  return [self.step(0x497AA0),self.step(0x498310),self.step(0x497C50)]

 def experiment(self):
  before=self.work_state();self.work_active=True
  try:
   pause=self.step(0x46B470,receiver=CTRL);idle=self.work_tick();sub={1:2,4:11}[self.get(TASK+0x174)]
   data=(ROOT/terminal.SCRIPT_PATH).read_bytes();decoded=commands(data);seg=next(s for s in decoded['segments'] if s['index']==sub)
   rows=decoded['commands'][seg['first_command']:seg['first_command']+seg['command_count']];experiments=[]
   for op,entry in ((117,0x42D960),(118,0x42D9F0)):
    c=next(x for x in rows if x['opcode']==op);need(c['bytes']==8 and data[c['offset']+4:c['offset']+8]==struct.pack('<I',0x2000003C),'sourced exact terminal fade60 command')
    handler=self.step(entry,(0,SCRIPT+c['offset'],c['bytes']),VM);ticks=[]
    for _ in range(61):ticks.append(self.work_tick())
    experiments.append(dict(opcode=op,source_command=c,handler=handler,ticks=ticks))
   return dict(before=before,pause=pause,idle=idle,experiments=experiments,after=self.work_state())
  finally:self.work_active=False

 def run(self):
  self.native=NativeTLS(terminal.parent.parent.parent.world.parent.parent.TLS)
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
    need(not self.pending_contracts,'all combat contracts returned');f['after']=self.state();f['trace_after']=self.mark();frames.append(f);events.append(self.event())
    if self.get(TASK+0x174):break
   else:raise ValueError('fresh terminal selection required')
   work=self.experiment();need(not self.pending_contracts,'pause world contracts returned')
   final_before=self.selected_state();result_call=self.call(0x473860);final_after=self.selected_state();cleanup=[]
   for u in (UNIT,TARGET):
    cleanup.append(self.call(0x40AC90,(u+0x48,),self.get(u+0x44)))
    for off in (0x30,0x3C):
     while self.get(u+0x48+off+4):cleanup.append(self.call(0x40BE20,(self.get(u+0x48+off+4),),terminal.parent.parent.parent.world.parent.parent.EVENT_CTRL))
    for j in range(5):cleanup.append(self.call(0x40AC90,(u+0xA0+j*88,),0x12620000))
   cleanup.append(self.call(0x439C60,receiver=FINE+0x18));popup_cleanup=[self.call(0x494D70,(terminal.parent.parent.parent.world.parent.parent.POPUP+j*16,)) for j in range(512) if self.get(terminal.parent.parent.parent.world.parent.parent.POPUP+j*16,'B')&128]
   row=dict(input=self.live_input,combat_input=self.cycle_input,initial=initial,initialization=initialization,image_before=image_before,image_after=self.image_identity(),
    target_bind=dict(before=target_before,call=target_bind,after=target_after),roots=roots,bind_before=before,bind=bind,bind_after=after,world_frames=frames,events=events,
    hit=self.hit_observations,hit_sides=self.hit_sides,contracts=self.contracts,both_hp_writes=self.both_hp_writes,calls=self.calls,APIs=self.api_trace,commands=self.commands,
    work=work,work_calls=self.work_calls,key_writes=self.key_writes,finalization=dict(before=final_before,call=result_call,after=final_after),cleanup=cleanup,popup_cleanup=popup_cleanup,
    final_state=self.state(),**self.common())
   row['platform']=dict(creation=self.native.creation,trace=self.native.trace,cleanup=self.native.close());row['blobs']=self.blobs
   need(self.tick_inputs is None or self.tick_index==len(self.tick_inputs),'all replay platform times consumed');return row
  except Exception as error:
   self.failure=dict(error=str(error),CPU=self.cpu(),work=self.work_state(),pending=self.work_stack,calls=self.work_calls[-10:],key_writes=self.key_writes[-32:]);raise
  finally:
   self.work_active=False
   if not self.native.closed:self.native.close()


def report(diagnostic_prefix):
 rows=[]
 for c in corpus():
  m=WorkMachine(c)
  try:r=m.run()
  except Exception:
   if hasattr(m,'failure'):terminal.save(diagnostic_prefix+'-'+c['name']+'.failure.json.gz',dict(accepted=False,failure=m.failure))
   raise
  rows.append(r);print(c['name'],r['instructions'],r['writes'],flush=True)
 return dict(schema_version=1,source_contract=source_contract(),cases=rows,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();need(not (ROOT/a.out).exists(),'fresh terminal work report');terminal.save(a.out,report(a.out))
