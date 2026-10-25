"""Fresh original combat/world clock and scene events in one declared instance."""
import argparse,ctypes,hashlib,json,types
from concurrent.futures import ProcessPoolExecutor
from unicorn import UC_PROT_READ,UC_PROT_WRITE
from unicorn.x86_const import UC_X86_REG_ESP
from tools import battle_terminal_selection_emulation as terminal
from tools.battle_lethal_combat import corpus as combat_corpus,pages
from tools.battle_hit_damage_platform import NativeTLS

ROOT,SOURCE,need,sha=terminal.ROOT,terminal.SOURCE,terminal.need,terminal.sha
CTRL,UNIT,TARGET,RECORD,TASK,VM,WORK,SCRIPT=terminal.CTRL,terminal.UNIT,terminal.TARGET,terminal.RECORD,terminal.TASK,terminal.VM,terminal.WORK,terminal.SCRIPT
FINE=terminal.parent.FINE
REGIONS=terminal.REGIONS
EXTRA_RANGES=((0x415040,0x415070),(0x495220,0x495630),(0x4727F0,0x472860),(0x472960,0x472A70),
 (0x458580,0x4586D0),(0x458BE0,0x458D80),(0x457890,0x457AA0),(0x458180,0x458280),(0x4577F0,0x457830),(0x42B0D0,0x42B1D0),(0x470070,0x470170),(0x4958B0,0x495AA0))
RANGES=terminal.RANGES+EXTRA_RANGES
ALLOWED=frozenset(at for lo,hi in RANGES for at in range(lo,hi))
REFERENCE=types.FunctionType(terminal.REFERENCE.__code__,dict(terminal.REFERENCE.__globals__,RANGES=RANGES))
GATED=(0x415040,0x495220,0x4727F0,0x472960,0x454C40,0x458580,0x458BE0,0x457890,0x458180)


class TraceCount:
 """The frozen source guard separately hashes every PC and original write."""
 def __init__(self):self.count=0
 def append(self,value):self.count+=1
 def __getitem__(self,key):return []


def corpus():
 rows=[dict(name=c['name'],base=c['name'],limit=36000,budget=384) for c in combat_corpus()[:4]]
 rows += [dict(name='threshold_running',base='player_threshold_survives',limit=36000,budget=192),
  dict(name='neutral_running',base='neutral_living_control',limit=36000,budget=2),
  dict(name='timeout_before_combat',base='player_dies_job1',limit=3,budget=4)]
 return rows


def validate(c):need(c in corpus() and all(type(c[k]) is type(v) for k,v in corpus()[0].items()),'exact live terminal inputs')


def declarations(c):
 return terminal.declarations(dict(remaining=c['limit']))+[(CTRL+0x108B3A,1,'B'),(CTRL+0x10F9C0,-1,'h'),(CTRL+0x10F9C2,-1,'h')]


def source_contract():
 raw=SOURCE.read_bytes()
 return dict(frozen_terminal_driver=terminal.source_contract(),fresh_combat_initialization=True,combat_snapshot_loaded=False,
  world_event_same_instance=True,original_outer_scheduler_connected=False,world_gate_108B3A=1,
  original_world_clock=True,first_original_terminal_request_is_stop=True,explicit_result_input_root=0x473860,
  extra_code=[dict(start=a,end=b,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES],
  all_original_PC_and_write_digests=True,whole_VM_world_independent_byte_model=False,rewards_complete=False)


class LiveMachine(terminal.TerminalMachine):
 source_code=types.FunctionType(terminal.TerminalMachine.source_code.__code__,dict(terminal.TerminalMachine.source_code.__globals__,ALLOWED=ALLOWED,REFERENCE=REFERENCE))

 def __init__(self,c,tick_inputs=None):
  validate(c);self.live_input=c;base=next(x for x in combat_corpus() if x['name']==c['base'])
  # This is the fresh constructor, not TerminalMachine's combat snapshot loader.
  terminal.parent.LethalMachine.__init__(self,base)
  for at,n in terminal.EXTRA_REGIONS:
   if at in (0x7D7000,0x7F6000):self.uc.mem_protect(at,n,UC_PROT_READ|UC_PROT_WRITE)
   else:self.uc.mem_map(at,n)
  self.uc.mem_write(TASK,bytes(self.uc.mem_read(0x12700000,0x190)))
  self.uc.mem_write(VM,bytes(0x9400));self.uc.mem_write(SCRIPT,(ROOT/terminal.SCRIPT_PATH).read_bytes())
  for at,v,f in declarations(c):self.put(at,v,f)
  self.mutable += [(VM,VM+0x9400),(0x7A4E18,0x7A4E20),(WORK,WORK+3),(TASK+0x43,TASK+0x60),(TASK+0x174,TASK+0x178),
   (CTRL+0x115CBA,CTRL+0x115CEC),(CTRL+0x108B3B,CTRL+0x108B3D),(CTRL+0x2E6F4,CTRL+0x2E6FC),
   (CTRL+0x109344,CTRL+0x109345),(CTRL+0x10934A,CTRL+0x10934C),(TASK+0x11804C,TASK+0x11804D)]+[(VM+0x446+j*0xAB8,VM+0x448+j*0xAB8) for j in range(14,56)]
  self.calls=[];self.pending=[];self.returns=set();self.api_trace=[];self.tick_inputs=tick_inputs;self.tick_index=0
  self.code_trace=TraceCount();self.original_write_trace=TraceCount();self.commands=[];self.active=False
  self.kernel=ctypes.WinDLL('kernel32',use_last_error=True)
  self.kernel.lstrcmpA.argtypes=[ctypes.c_char_p,ctypes.c_char_p];self.kernel.lstrcmpA.restype=ctypes.c_int
  self.kernel.GetTickCount.argtypes=[];self.kernel.GetTickCount.restype=ctypes.c_uint32

 def selected_state(self):
  s=super().selected_state();s['units']=[bytes(self.uc.mem_read(u,0x520)).hex() for u in (UNIT,TARGET)]
  return pages(s,self.blobs)

 def state(self):
  s=super().state();s['terminal_state']=self.selected_state();return s

 def code(self,uc,at,size,context):
  super().code(uc,at,size,context)
  if self.frame_observation is not None and at in GATED:
   sp=uc.reg_read(UC_X86_REG_ESP);self.frame_observation['gated_calls'].append(dict(entry=at,caller=self.get(sp),receiver=self.cpu()['ECX'],args=[self.get(sp+4)] if at==0x415040 else []))

 def mark(self):return dict(instructions=self.instructions,writes=self.writes,code_sha256=self.code_hash.hexdigest(),write_sha256=self.write_hash.hexdigest())

 def event(self):
  self.active=True;start=len(self.calls);before=self.selected_state();mark=self.mark()
  try:call=self.call(0x432100)
  finally:self.active=False
  need(len(self.pending)==1 and self.pending[0]['entry']==0x432100,'only event root awaits actual return')
  root=self.pending.pop();need((self.cpu()['EIP'],self.cpu()['ESP'])==(root['caller'],root['return_ESP']),'complete original event return CPU')
  after=self.selected_state();root.update(result=self.cpu()['EAX'],after=after,cpu_after=self.cpu())
  return dict(before=before,call=call,after=after,calls=[start,len(self.calls)],trace_before=mark,trace_after=self.mark())

 def run(self):
  self.native=NativeTLS(terminal.parent.parent.parent.world.parent.parent.TLS)
  try:
   initial=self.snapshot();image_before=self.image_identity();target_before=self.state();target_bind=self.call(0x467020,(TARGET,self.combat_input['job']));target_after=self.state()
   roots=[self.call(0x437C90,(u+off,),FINE) for u in (UNIT,TARGET) for off in (0x2F4,0x3E0)]
   before=self.state();bind=self.call(0x467020,(UNIT,self.combat_input['job']));after=self.state();frames=[];events=[]
   for i in range(self.live_input['budget']):
    f=dict(index=i,before=self.state(),entries=[],scanned_slots=[],unit_calls=[],stages=[],controls=[],nested_calls=[],ai_calls=[],gated_calls=[],trace_before=self.mark())
    self.frame_observation=f;self.running_update=True
    try:f['call']=self.call(0x46B470)
    finally:self.frame_observation=None;self.running_update=False
    need(not self.pending_contracts,'all whole-world original contracts returned');f['after']=self.state();f['trace_after']=self.mark();frames.append(f)
    events.append(self.event())
    if i%64==0:print(self.live_input['name'],'world/event',i,flush=True)
    if self.get(TASK+0x174):break
   else:need(self.live_input['name']=='threshold_running','only live survival control reaches declared budget')
   final_before=self.selected_state();self.active=True;result_call=self.call(0x473860);self.active=False;final_after=self.selected_state();need(not self.pending,'all finalization contracts returned')
   cleanup=[]
   for u in (UNIT,TARGET):
    cleanup.append(self.call(0x40AC90,(u+0x48,),self.get(u+0x44)))
    for off in (0x30,0x3C):
     while self.get(u+0x48+off+4):cleanup.append(self.call(0x40BE20,(self.get(u+0x48+off+4),),terminal.parent.parent.parent.world.parent.parent.EVENT_CTRL))
    for j in range(5):cleanup.append(self.call(0x40AC90,(u+0xA0+j*88,),0x12620000))
   cleanup.append(self.call(0x439C60,receiver=FINE+0x18));popup_cleanup=[self.call(0x494D70,(terminal.parent.parent.parent.world.parent.parent.POPUP+j*16,)) for j in range(512) if self.get(terminal.parent.parent.parent.world.parent.parent.POPUP+j*16,'B')&128]
   row=dict(input=self.live_input,combat_input=self.cycle_input,initial=initial,image_before=image_before,image_after=self.image_identity(),
    target_bind=dict(before=target_before,call=target_bind,after=target_after),roots=roots,bind_before=before,bind=bind,bind_after=after,world_frames=frames,events=events,
    hit=self.hit_observations,hit_sides=self.hit_sides,contracts=self.contracts,both_hp_writes=self.both_hp_writes,calls=self.calls,APIs=self.api_trace,commands=self.commands,
    finalization=dict(before=final_before,call=result_call,after=final_after),cleanup=cleanup,popup_cleanup=popup_cleanup,final_state=self.state(),**self.common())
   row['platform']=dict(creation=self.native.creation,trace=self.native.trace,cleanup=self.native.close());row['blobs']=self.blobs
   need(self.tick_inputs is None or self.tick_index==len(self.tick_inputs),'captured original time inputs consumed');return row
  except Exception as error:
   self.failure=dict(error=str(error),CPU=self.cpu(),state=self.selected_state(),pending=self.pending,last_contracts=self.contracts[-12:],calls=self.calls[-12:],trace=self.mark());raise
  finally:
   self.active=False
   if not self.native.closed:self.native.close()


def emit_case(task):
 c,out=task;m=LiveMachine(c)
 try:r=m.run()
 except Exception:
  if hasattr(m,'failure'):terminal.save(out+'.failure.json.gz',dict(accepted=False,input=c,source_contract=source_contract(),failure=m.failure,blobs=m.blobs))
  raise RuntimeError(c['name']+' original live world/event failed') from None
 terminal.save(out,dict(schema_version=1,source_contract=source_contract(),cases=[r],R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False));print(c['name'],len(r['world_frames']),r['instructions'],flush=True)
 return dict(name=c['name'],**terminal.ref(out))


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case');p.add_argument('--jobs',type=int,default=3);a=p.parse_args();out=ROOT/a.out;need(not out.exists() and 1<=a.jobs<=3,'fresh bounded live world report')
 if a.case:
  cs=[c for c in corpus() if c['name']==a.case];need(len(cs)==1,'one original live case');emit_case((cs[0],a.out))
 else:
  tasks=[(c,out.with_name(out.stem+'-'+c['name']+'.json.gz').relative_to(ROOT).as_posix()) for c in corpus()];need(all(not (ROOT/s).exists() for c,s in tasks),'fresh live case files')
  with ProcessPoolExecutor(max_workers=a.jobs) as pool:refs=list(pool.map(emit_case,tasks))
  terminal.save(a.out,dict(schema_version=1,source_contract=source_contract(),case_reports=refs,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False))
