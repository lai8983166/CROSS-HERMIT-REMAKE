"""Continue the accepted terminal VM stop through original task completion.

The four original frame roots run in the existing native owner lifetime.  The
parent's script-exit guard remains intact and inactive throughout this stage.
"""
import argparse,copy,hashlib,json,struct,time,types
from functools import lru_cache
from tools import terminal_script_exit_emulation as parent

ROOT,CODE,need,sha,terminal,MAIN,VM,STACK,RETURN,TASK,INPUT,MANAGER,KEYBOARD,overlay=(getattr(parent,n) for n in ('ROOT','CODE','need','sha','terminal','MAIN','VM','STACK','RETURN','TASK','INPUT','MANAGER','KEYBOARD','overlay'))
followup=parent.followup
EXTRA_RANGES=((0x454EE0,0x454F4D),)
NEW_MUTABLE=((TASK+0x171,TASK+0x173),)
RANGES=parent.RANGES+EXTRA_RANGES
ALLOWED=frozenset(a for lo,hi in RANGES for a in range(lo,hi))
REFERENCE=types.FunctionType(parent.REFERENCE.__code__,dict(parent.REFERENCE.__globals__,RANGES=RANGES))
PARENT_ACCEPTANCE='analysis/terminal-script-exit-acceptance-v1-20261030.json'
PARENT_ACCEPTANCE_SHA='2223c1d28e459805547be409cb669219392b73f6a73d0f02617c8e441a6e9d2d'
PARENT_SOURCE='analysis/terminal-script-exit-source-v2-20261030.json.gz'
PARENT_SOURCE_SHA='d505cf449749a8c3061eb4da920edc9782b4d01ada3d61968031f17bfa915ae5'
PARENT_PROOF='analysis/terminal-script-exit-proof-v1-20261030.json'
PARENT_PROOF_SHA='74900bd5817d3064daa9758afa0edc466fc1b61a50a879c3848f9b9b5dba5b1f'
GROUPS=tuple(i for i in range(10,89) if i!=20)
EVENTS={0x497C50:(0,0),0x454EE0:(0,0),0x41F4E0:(1,4),
 0x41F2A0:(1,4),0x41F890:(0,0),0x56DE40:(4,16),0x428AD0:(1,0),
 0x403730:(0,0),0x403A00:(0,0),0x41F710:(0,0),
 0x454C40:(0,0),0x457830:(0,0),0x497AA0:(0,0),0x498310:(0,0)}
QUERIES=(0x497C50,0x454EE0,0x41F4E0,0x41F2A0,0x41F710)

@lru_cache(maxsize=1)
def fixed_parents():
 refs={k:followup.parent.file_ref(p,h) for k,p,h in (('acceptance',PARENT_ACCEPTANCE,PARENT_ACCEPTANCE_SHA),('source',PARENT_SOURCE,PARENT_SOURCE_SHA),('proof',PARENT_PROOF,PARENT_PROOF_SHA))}
 a=json.loads((ROOT/PARENT_ACCEPTANCE).read_text(encoding='utf8'))
 need(a['source_report']==refs['source'] and a['independent_proof']==refs['proof'] and a['tasks_complete']==3,'fixed accepted original script exit')
 return refs

def fixed_parent_times():return parent.fixed_parent_times()
def helper_contract():return parent.helper_contract()
def helpers(prefix='terminal-task-completion'):return parent.helpers(prefix)

@lru_cache(maxsize=1)
def fixed_parent_forward_summaries():
 raw=(ROOT/PARENT_PROOF).read_bytes();need(sha(raw)==PARENT_PROOF_SHA,'fixed script exit proof')
 return {c['name']:c['forward_summary']['full_cumulative'] for c in json.loads(raw)['cases']}

def validate_parent_prefix(machine):
 name=machine.live_input['name'];expected=fixed_parent_forward_summaries()[name];actual=machine.mark()
 need(actual==expected,'fixed complete script exit prefix '+name+' expected='+repr(expected)+' actual='+repr(actual))
 print('task_completion prefix preflight',name,actual,flush=True)
 return dict(case=name,fixed_proof_sha256=PARENT_PROOF_SHA,expected=expected,actual=actual)

def namespaced(fn):
 def rename(n):return 'tc_'+n[3:] if n.startswith('fu_') else 'task_completion_'+n[9:] if n.startswith('followup_') else n
 return types.FunctionType(fn.__code__.replace(co_names=tuple(rename(n) for n in fn.__code__.co_names)),fn.__globals__,fn.__name__,fn.__defaults__,fn.__closure__)

class TaskCompletionMachine(parent.ScriptExitMachine):
 source_code=types.FunctionType(parent.ScriptExitMachine.source_code.__code__,dict(parent.ScriptExitMachine.source_code.__globals__,ALLOWED=ALLOWED,REFERENCE=REFERENCE))
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.task_completion_active=self.task_completion_ready=self.task_completion_cleaning=False;self.task_completion_stop=None
  self.mutable+=list(NEW_MUTABLE)
  for n in ('segments','frames','leaves','commands','writes','queries','bindings','gpu','calls','conversions','resources','observers','cleanup','events','cleanup_skips'):setattr(self,'tc_'+n,[])
  self.tc_live={};self.tc_count=self.tc_write_count=0;self.tc_ih=hashlib.sha256();self.tc_wh=hashlib.sha256();self.tc_current=None;self.tc_event_stack=[];self.tc_branch=dict(role=None)
 tc_mark=namespaced(followup.FollowupMachine.fu_mark)
 tc_capture=namespaced(followup.FollowupMachine.fu_capture)
 tc_prefix_counts=namespaced(followup.FollowupMachine.fu_prefix_counts)
 tc_observe=namespaced(followup.FollowupMachine.fu_observe)
 tc_segment=namespaced(followup.FollowupMachine.fu_segment)
 tc_frame=namespaced(followup.FollowupMachine.fu_frame)
 _tc_actual_root=namespaced(followup.FollowupMachine.fu_actual_root)
 _tc_gpu_api=namespaced(followup.FollowupMachine.gpu_api)
 _tc_api_crt=namespaced(followup.FollowupMachine.api_crt)
 def api_crt(self,slot):
  if not self.task_completion_ready:return super().api_crt(slot)
  return self._tc_api_crt(slot)
 def gpu_api(self,at):
  if not self.task_completion_ready:return super().gpu_api(at)
  need(self.methods[at] in (56,8),'task completion only describes and releases inherited textures')
  self._tc_gpu_api(at);call=self.tc_gpu[-1]
  if call['op']!='release':return
  for prefix in ('se','ld','ml','nd','nx','fu'):
   resources,live=getattr(self,prefix+'_resources'),getattr(self,prefix+'_live')
   for r in resources:
    if r['generation']==call['generation']:
     need(r['alive'] and r['record']==call['record'] and live.get(r['texture']['pointer']) is r,'same inherited generation released exactly once')
     r.update(alive=False,release_wire_index=call['wire_index'],released_phase='task_completion_'+call['phase']);del live[r['texture']['pointer']]
 def write_hook(self,uc,access,at,size,value,context):
  super().write_hook(uc,access,at,size,value,context)
  if self.task_completion_active:
   self.tc_write_count+=1;self.tc_wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
   if VM<=at<VM+0x9400 or KEYBOARD<=at<KEYBOARD+0xA00 or TASK<=at<TASK+0x190 or MAIN+0x844<=at<MAIN+0x1044 or at==0:self.tc_writes.append(dict(pc=self.getreg('EIP'),address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))
 def tc_event_state(self):
  return dict(VM_PC=self.get(VM+28),VM_wait=self.get(VM+32,'H'),VM_active=self.get(VM+4,'B'),accounting=self.get(0x765720),task_hex=self.read(TASK+0x44,0x20).hex(),work_hex=self.read(overlay.WORK,0x2500).hex(),task_full_hex=self.read(TASK,0x190).hex(),resource_table_hex=self.read(MAIN+0x844,0x800).hex())
 def code(self,uc,at,size,context):
  active=self.task_completion_active
  if active:
   need(not self.script_exit_active,'separate completed parent script-exit guard')
   sp=uc.reg_read(followup.x86.UC_X86_REG_ESP)
   while self.tc_event_stack and (at,sp)==(self.tc_event_stack[-1]['caller'],self.tc_event_stack[-1]['return_ESP']):
    r=self.tc_event_stack.pop();r.update(after_CPU=self.cpu(),after=self.tc_event_state(),result=self.getreg('EAX'))
   if at==self.task_completion_stop:uc.emu_stop();return
   need(at not in (0x453F10,0x454793,0x473860,0x4CE9C5) and not 0x41F732<=at<0x41F811,'task completion finite original boundary')
   if at in EVENTS:
    n,pop=EVENTS[at];r=dict(entry=at,caller=self.get(sp),receiver=self.getreg('ECX'),args=[self.get(sp+4+j*4) for j in range(n)],return_ESP=sp+4+pop,before_CPU=self.cpu(),before=self.tc_event_state());self.tc_events.append(r);self.tc_event_stack.append(r)
   if at in overlay.parent.APIS and self.get(sp)==overlay.parent.APIS[at][2]:
    ret=self.get(sp);first=len(self.task_APIs);super().code(uc,at,size,context);need(len(self.task_APIs)==first+1,'one actual task completion task leaf');r=self.task_APIs[-1];self.tc_leaves.append(dict(kind='TASK',call=dict(r,sp=sp,return_va=ret,pop=4,value=r['result'],memory_outputs=[],new_mappings=[])));return
   if at in self.gdi_targets:raise ValueError('task completion unexpectedly creates or uses GDI')
   if at in QUERIES:self.tc_queries.append(dict(entry=at,CPU=self.cpu(),receiver=self.getreg('ECX'),stack_hex=self.read(sp,68).hex(),state=self.tc_event_state()))
  super().code(uc,at,size,context)
  if active and at in ALLOWED:self.tc_count+=1;self.tc_ih.update(struct.pack('<I',at))
 def admission(self):
  a=super().admission();self.tc_prefix_preflight=validate_parent_prefix(self);self.tc_prefix=self.tc_prefix_counts();self.tc_before=self.tc_capture()
  need(not self.script_exit_active and (self.get(VM+4,'B'),self.get(VM+32,'H'),self.get(TASK+0x44,'B'),self.get(TASK+0x59,'B'))==(0,0,4,2),'accepted stopped VM and original phase4/status2')
  self.tc_resources=copy.deepcopy(self.se_resources);self.tc_resources_before=copy.deepcopy(self.tc_resources);self.tc_live={r['texture']['pointer']:r for r in self.tc_resources if r['alive']}
  need(len(self.tc_live)==10,'ten currently live inherited textures')
  self.tc_projection_before=copy.deepcopy(self.space.ledger());self.tc_projection_next=self.space.next
  end=len(self.se_leaves);self.se_cleanup.append(dict(label='forward_leaf_end_only',leaves=[end,end]))
  self.task_completion_ready=self.task_completion_active=self.active_overlay=True
  self.tc_frame('original_phase4_resource_groups')
  need(self.get(TASK+0x44,'B')==5,'original readiness and resource loop advance to phase5')
  need([r['args'][0] for r in self.tc_events if r['entry']==0x41F4E0]==list(GROUPS),'all 78 original groups in exact loop order;20 skipped')
  self.tc_phase4=self.tc_capture();self.tc_frame('original_phase5_completion_handshake')
  need(self.getreg('EIP')==RETURN and self.getreg('ESP')==STACK+0xF004 and not self.tc_event_stack,'entire final original task naturally returned')
  need((self.get(TASK+0x44,'B'),self.get(TASK+0x59,'B'),self.get(TASK+0x171,'B'),self.get(TASK+0x172,'B'),self.getreg('EAX'))==(6,3,1,1,1),'original task completion handshake')
  need(not self.tc_commands and not self.tc_calls and not self.tc_conversions,'no new script commands or rendering calls')
  need(len(self.tc_resources)==len(self.tc_resources_before),'no new texture creation')
  need(all(self.get(r['record']+44)==r['texture']['pointer'] for r in self.tc_resources if r['alive']),'each surviving actual generation still owned')
  need(self.space.ledger()==self.tc_projection_before and self.space.next==self.tc_projection_next,'GPU identities unchanged')
  final=self.tc_capture();observations=self.tc_observe('final');self.task_completion_active=self.active_overlay=False
  for r in self.tc_resources:r['alive_after_forward']=r['alive']
  self.tc_result=dict(prefix=self.tc_prefix,prefix_preflight=self.tc_prefix_preflight,before=self.tc_before,phase4=self.tc_phase4,final=final,resources_before=self.tc_resources_before,resources=copy.deepcopy(self.tc_resources),bindings=self.tc_bindings,segments=self.tc_segments,frames=self.tc_frames,leaves=self.tc_leaves,commands=self.tc_commands,writes=self.tc_writes,queries=self.tc_queries,events=self.tc_events,GPU_APIs=self.tc_gpu,calls=self.tc_calls,conversions=self.tc_conversions,readbacks=observations,readback_observers=self.tc_observers,GDI_trace=copy.deepcopy(self.name_platform.trace[self.tc_prefix['GDI_trace']:]),GDI_handle_projection=self.name_platform.space.ledger(),accounting=self.get(0x765720),forward_wire_end=len(self.gpu.trace),CRT_forward_wire_end=len(self.live.trace),GPU_projection_before=dict(next=self.tc_projection_next,ledger=self.tc_projection_before),GPU_projection=copy.deepcopy(self.space.ledger()),VM_script_stopped=True,terminal_task_completion_executed=True,terminal_battle_exit_executed=False,rewards_or_school_executed=False)
  return a
 def tc_actual_root(self,label,entry,args=(),receiver=0,cdecl=False):
  if entry==0x41F4E0:
   slot=receiver+args[0]*8;raw=self.read(slot,8)
   if raw==bytes(8):
    self.tc_cleanup_skips.append(dict(label=label,entry=entry,args=list(args),receiver=receiver,cdecl=cdecl,slot=slot,slot_hex=raw.hex(),record_pointer=struct.unpack_from('<I',raw)[0],reason='original forward resource loop already cleared this container'))
    return None
  return self._tc_actual_root(label,entry,args,receiver,cdecl)
 def se_actual_root(self,*args,**kwargs):
  if not self.task_completion_ready:return super().se_actual_root(*args,**kwargs)
  return self.tc_actual_root(*args,**kwargs)
 def run(self):
  row=super().run();need(not self.tc_live and all(not r['alive'] for r in self.tc_resources),'all actual current generations released once')
  row.update(terminal_task_completion=self.tc_result,task_completion_cleanup=self.tc_cleanup,task_completion_cleanup_skips=self.tc_cleanup_skips,task_completion_resources_after_cleanup=copy.deepcopy(self.tc_resources));return row

def source_contract():
 return dict(parent=parent.source_contract(),fixed_predecessor=fixed_parents(),forward_roots=[0x40DB90,0x40DC80,0x425DE0,0x454CF0],new_VM_or_handler_roots=0,derived_input_host_writes=0,PC_or_wait_or_phase_host_writes=0,new_OS_input=False,new_capture_cycle=False,draw_or_Present=False,helper=helper_contract(),extra_code=[dict(start=a,end=b,sha256=sha(CODE[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES],new_mutable=[dict(start=a,end=b,original_write_PCs=[0x454E4B,0x454E55]) for a,b in NEW_MUTABLE],resource_groups=list(GROUPS),skipped_group=20,resource_group_entry=0x41F4E0,record_bytes=0x54,dynamic_supplemental_cleanup=True,GPU_projection=dict(parent_entries_unchanged=True,new_domains=[],new_creations=0),GDI_projection=dict(current_parent_lifetimes=True,new_creations=0),freeze_boundary='original phase5 completion handshake and same complete454CF0 natural return',terminal_task_completion_executed=True,terminal_battle_exit_executed=False,rewards_or_school_executed=False)

save_source=parent.save_source

def run_case(c,ch,gh,ticks=None):
 fixed=fixed_parent_times()[c['name']];ticks=list(fixed) if ticks is None else ticks;need(ticks==fixed,'exact accepted original clock stream');instances=[]
 class Attached(TaskCompletionMachine):
  def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);instances.append(self)
 class Diagnostics:
  @staticmethod
  def save(path,data):
   if instances:
    m=instances[0];data['task_completion']=dict(active=m.task_completion_active,segments=m.tc_segments,frames=m.tc_frames,leaves=m.tc_leaves,resources=m.tc_resources,commands=m.tc_commands,events=m.tc_events,CRT_trace=copy.deepcopy(m.live.trace),GPU_trace=copy.deepcopy(m.gpu.trace),GDI_trace=copy.deepcopy(m.name_platform.trace),GDI_lifetimes=m.ld_gdi_projection.report(),memory=m.snapshot(),trace=m.mark(),local_trace=m.tc_mark())
   save_source(path.replace('terminal-overlay-diagnostic-','terminal-task-completion-diagnostic-').replace('.json.gz','-20261030-'+str(time.time_ns())+'.json.gz'),data)
 fn=types.FunctionType(overlay.run_case.__code__,dict(overlay.run_case.__globals__,OverlayMachine=Attached,terminal=Diagnostics),closure=overlay.run_case.__closure__);return fn(c,ch,gh,ticks)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case',type=int);p.add_argument('--helper-prefix',default='terminal-task-completion');a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable task completion source');fixed_parents();ch,gh,b=helpers(a.helper_prefix);rows=[]
 for c in (overlay.parent.corpus() if a.case is None else [overlay.parent.corpus()[a.case]]):rows.append(run_case(c,ch,gh));print('task_completion source',c['name'],'original task completion returned',flush=True)
 save_source(a.out,dict(schema_version=1,source_contract=source_contract(),helper_build=b,cases=rows,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False))
