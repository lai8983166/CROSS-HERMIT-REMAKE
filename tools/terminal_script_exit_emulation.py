"""Complete the two selected original terminal scripts, freezing at task return.

The retained current native owners and every predecessor forward byte remain
in the same machine. Only raw keyboard samples and the four accepted frame
roots enter the new stage; opcode 19 follows its original special dispatch.
"""
import argparse,copy,hashlib,json,struct,time,types
from functools import lru_cache
from tools import terminal_last_dialogue_emulation as parent

ROOT,CODE,need,sha,terminal,MAIN,VM,STACK,RETURN,TASK,INPUT,MANAGER,KEYBOARD,overlay=(getattr(parent,n) for n in ('ROOT','CODE','need','sha','terminal','MAIN','VM','STACK','RETURN','TASK','INPUT','MANAGER','KEYBOARD','overlay'))
followup=parent.followup
# Exact original prologue-through-ret bodies reached by 21,24,31; no stubs.
EXTRA_RANGES=((0x4C5590,0x4C56BE),(0x4C5BC0,0x4C5CEC),
 (0x4C9590,0x4C9610),(0x4CB120,0x4CB175),(0x4CC8D0,0x4CC90E),
 (0x4CC910,0x4CC9D1),(0x4C7130,0x4C718A),(0x4C6DA0,0x4C6DCB))
RANGES=parent.RANGES+EXTRA_RANGES
ALLOWED=frozenset(a for lo,hi in RANGES for a in range(lo,hi))
REFERENCE=types.FunctionType(parent.REFERENCE.__code__,dict(parent.REFERENCE.__globals__,RANGES=RANGES))
PARENT_ACCEPTANCE='analysis/terminal-last-dialogue-acceptance-v1-20261029.json'
PARENT_ACCEPTANCE_SHA='01b0d5f4dabe43a7e53cf149693760ec4098918b5b7670a29499bf28a11cd1fa'
PARENT_SOURCE='analysis/terminal-last-dialogue-source-v3-20261029.json.gz'
PARENT_SOURCE_SHA='4554fe112274ac681ce43e2f0360874456605573837438fe2f90e07f35d2de5a'
PARENT_PROOF='analysis/terminal-last-dialogue-proof-v1-20261029.json'
PARENT_PROOF_SHA='812cc338198ece5d07e1e40a25da25dd1e5795bf19362e1412a2884d3a44591d'
EVENTS={0x4C2670:(3,12),0x4C4DC0:(3,12),0x4C4EB0:(3,12),0x497C50:(0,0),
 0x403730:(0,0),0x4CADE0:(0,0),0x4C6DA0:(0,0),0x4C6330:(3,12),0x4C5BC0:(3,12),0x4C5590:(3,12),
 0x42D9F0:(3,12),0x4CE090:(1,4),0x4CE800:(0,0),0x4CE8F0:(0,0),
 0x4563D0:(0,0),0x497980:(1,0),0x4CC8D0:(1,4),0x4CC910:(2,8),
 0x4CC540:(2,8),0x4C9590:(0,0),0x4CB120:(2,8),0x4C7130:(0,0)}
QUERIES=(0x4C4DC0,0x4C4EB0,0x497C50)

def branch(name):
 need(name in ('neutral_running','timeout_before_combat'),'one original terminal script branch')
 delta=0 if name=='neutral_running' else 30
 ops=[(320,44,4),(324,43,8),(332,44,4),(336,43,8),(344,44,4),
      (348,31,12),(360,31,12),(372,24,12),(384,12,8),(392,21,4),(396,118,8),(404,19,4)]
 return dict(first_PC=320+delta,final_PC=404+delta,segment=2 if delta==0 else 11,
  scene_capture=76 if delta==0 else 77,role=None,commands=[dict(PC=p+delta,opcode=op,bytes=n) for p,op,n in ops])

@lru_cache(maxsize=1)
def fixed_parents():
 refs={k:followup.parent.file_ref(p,h) for k,p,h in (('acceptance',PARENT_ACCEPTANCE,PARENT_ACCEPTANCE_SHA),('source',PARENT_SOURCE,PARENT_SOURCE_SHA),('proof',PARENT_PROOF,PARENT_PROOF_SHA))}
 a=json.loads((ROOT/PARENT_ACCEPTANCE).read_text(encoding='utf8'))
 need(a['source_report']==refs['source'] and a['independent_proof']==refs['proof'] and a['tasks_complete']==3 and a['boundaries']['VM_PC_per_case']==[320,350] and a['boundaries']['VM_wait']==1,'fixed accepted last dialogue confirmation')
 return refs

def fixed_parent_times():return parent.fixed_parent_times()
def helper_contract():return parent.helper_contract()
def helpers(prefix='terminal-script-exit'):return parent.helpers(prefix)

@lru_cache(maxsize=1)
def fixed_parent_forward_summaries():
 raw=(ROOT/PARENT_PROOF).read_bytes();need(sha(raw)==PARENT_PROOF_SHA,'fixed last dialogue proof')
 return {c['name']:c['forward_summary']['full_cumulative'] for c in json.loads(raw)['cases']}

def validate_parent_prefix(machine):
 name=machine.live_input['name'];expected=fixed_parent_forward_summaries()[name];actual=machine.mark()
 need(actual==expected,'fixed complete last dialogue prefix '+name+' expected='+repr(expected)+' actual='+repr(actual))
 print('script_exit prefix preflight',name,actual,flush=True)
 return dict(case=name,fixed_proof_sha256=PARENT_PROOF_SHA,expected=expected,actual=actual)

def namespaced(fn):
 def rename(n):return 'se_'+n[3:] if n.startswith('fu_') else 'script_exit_'+n[9:] if n.startswith('followup_') else n
 return types.FunctionType(fn.__code__.replace(co_names=tuple(rename(n) for n in fn.__code__.co_names)),fn.__globals__,fn.__name__,fn.__defaults__,fn.__closure__)

class ScriptExitMachine(parent.LastDialogueMachine):
 source_code=types.FunctionType(parent.LastDialogueMachine.source_code.__code__,dict(parent.LastDialogueMachine.source_code.__globals__,ALLOWED=ALLOWED,REFERENCE=REFERENCE))
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.script_exit_active=self.script_exit_ready=self.script_exit_cleaning=False;self.script_exit_stop=None
  for n in ('segments','frames','leaves','commands','writes','queries','bindings','gpu','calls','conversions','resources','observers','cleanup','events'):setattr(self,'se_'+n,[])
  self.se_live={};self.se_count=self.se_write_count=0;self.se_ih=hashlib.sha256();self.se_wh=hashlib.sha256();self.se_current=None;self.se_event_stack=[]
 se_mark=namespaced(followup.FollowupMachine.fu_mark)
 se_capture=namespaced(followup.FollowupMachine.fu_capture)
 se_prefix_counts=namespaced(followup.FollowupMachine.fu_prefix_counts)
 se_observe=namespaced(followup.FollowupMachine.fu_observe)
 se_segment=namespaced(followup.FollowupMachine.fu_segment)
 se_frame=namespaced(followup.FollowupMachine.fu_frame)
 se_actual_root=namespaced(followup.FollowupMachine.fu_actual_root)
 _se_captured=namespaced(followup.FollowupMachine.fu_captured)
 _se_gpu_api=namespaced(followup.FollowupMachine.gpu_api)
 _se_api_crt=namespaced(followup.FollowupMachine.api_crt)
 def se_captured(self,capture):
  row=self._se_captured(capture);row['cycle']='terminal_script_exit_confirmation';return row
 def api_crt(self,slot):
  if not self.script_exit_ready:return super().api_crt(slot)
  return self._se_api_crt(slot)
 def gpu_api(self,at):
  if not self.script_exit_ready:return super().gpu_api(at)
  need(self.methods[at] in (56,8),'script exit only describes and releases inherited textures')
  self._se_gpu_api(at);call=self.se_gpu[-1]
  if call['op']!='release':return
  for prefix in ('ld','ml','nd','nx','fu'):
   resources,live=getattr(self,prefix+'_resources'),getattr(self,prefix+'_live')
   for r in resources:
    if r['generation']==call['generation']:
     need(r['alive'] and r['record']==call['record'] and live.get(r['texture']['pointer']) is r,'same actual inherited generation released exactly once')
     r.update(alive=False,release_wire_index=call['wire_index'],released_phase='script_exit_'+call['phase']);del live[r['texture']['pointer']]
 def write_hook(self,uc,access,at,size,value,context):
  super().write_hook(uc,access,at,size,value,context)
  if self.script_exit_active:
   if getattr(self,'se_keyboard_fragment',False):need(KEYBOARD<=at and at+size<=KEYBOARD+0xA00 or STACK<=at and at+size<=STACK+0x20000,'original script exit keyboard writes')
   self.se_write_count+=1;self.se_wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
   if VM<=at<VM+0x9400 or KEYBOARD<=at<KEYBOARD+0xA00 or TASK<=at<TASK+0x190 or at==0:self.se_writes.append(dict(pc=self.getreg('EIP'),address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))
 def se_event_state(self):
  return dict(VM_PC=self.get(VM+28),VM_wait=self.get(VM+32,'H'),VM_active=self.get(VM+4,'B'),accounting=self.get(0x765720),task_hex=self.read(TASK+0x44,0x20).hex(),work_hex=self.read(overlay.WORK,0x2500).hex())
 def code(self,uc,at,size,context):
  active=self.script_exit_active
  if active:
   if at==self.script_exit_stop:uc.emu_stop();return
   need(at!=0x454E18,'successor task cleanup body remains unexecuted')
   sp=uc.reg_read(followup.x86.UC_X86_REG_ESP)
   while self.se_event_stack and (at,sp)==(self.se_event_stack[-1]['caller'],self.se_event_stack[-1]['return_ESP']):
    r=self.se_event_stack.pop();r.update(after_CPU=self.cpu(),after=self.se_event_state(),result=self.getreg('EAX'))
   if at in EVENTS:
    n,pop=EVENTS[at];r=dict(entry=at,caller=self.get(sp),receiver=self.getreg('ECX'),args=[self.get(sp+4+j*4) for j in range(n)],return_ESP=sp+4+pop,before_CPU=self.cpu(),before=self.se_event_state());self.se_events.append(r);self.se_event_stack.append(r)
   if at==0x4CE9C5:
    p=self.get(VM+16)+self.get(VM+28);op,n=struct.unpack('<HH',self.read(p,4));i=len(self.se_commands)
    need(i<len(self.se_branch['commands']) and dict(PC=self.get(VM+28),opcode=op,bytes=n)==self.se_branch['commands'][i],'exact remaining original command order, including special19')
    self.se_commands.append(dict(PC=self.get(VM+28),opcode=op,bytes=n,source_pointer=p,raw_hex=self.read(p,n).hex()))
   if at in overlay.parent.APIS and self.get(sp)==overlay.parent.APIS[at][2]:
    ret=self.get(sp);first=len(self.task_APIs);super().code(uc,at,size,context);need(len(self.task_APIs)==first+1,'one actual script exit task leaf');r=self.task_APIs[-1];self.se_leaves.append(dict(kind='TASK',call=dict(r,sp=sp,return_va=ret,pop=4,value=r['result'],memory_outputs=[],new_mappings=[])));return
   if at in self.gdi_targets:raise ValueError('script exit unexpectedly creates or uses GDI')
   if at in QUERIES:self.se_queries.append(dict(entry=at,CPU=self.cpu(),receiver=self.getreg('ECX'),stack_hex=self.read(sp,68).hex(),state=self.se_event_state()))
  super().code(uc,at,size,context)
  if active and at in ALLOWED:self.se_count+=1;self.se_ih.update(struct.pack('<I',at))
 def admission(self):
  a=super().admission();self.se_prefix_preflight=validate_parent_prefix(self);self.se_branch=branch(self.live_input['name']);self.se_prefix=self.se_prefix_counts();self.se_before=self.se_capture()
  need((self.get(VM+28),self.get(VM+32,'H'))==(self.se_branch['first_PC'],1),'accepted parent wait in same resource lifetime')
  self.se_resources=copy.deepcopy(self.ld_resources);self.se_resources_before=copy.deepcopy(self.se_resources);self.se_live={r['texture']['pointer']:r for r in self.se_resources if r['alive']}
  need(len(self.se_live)==10,'ten currently live inherited textures')
  self.se_projection_before=copy.deepcopy(self.space.ledger());self.se_projection_next=self.space.next
  end=len(self.ld_leaves);self.ld_cleanup.append(dict(label='forward_leaf_end_only',leaves=[end,end]))
  self.script_exit_ready=self.script_exit_active=self.active_overlay=True
  stream=followup.parent.parent.input_contract()['streams'][str(self.se_branch['scene_capture'])];self.se_captured(stream['captures'][0])
  for _ in range(2):
   self.se_frame('held_parent_confirmation');need((self.get(VM+28),self.get(VM+32,'H'),self.get(KEYBOARD+0x4B9,'B'))==(self.se_branch['first_PC'],1,0),'two idle tasks preserve last dialogue wait')
  self.se_captured(stream['captures'][1]);self.se_frame('captured_press');need((self.get(VM+28),self.get(VM+32,'H'),self.get(KEYBOARD+0x4B9,'B'))==(self.se_branch['first_PC'],0,128),'original complete task consumes new press');confirmed=self.se_capture();self.se_captured(stream['captures'][2]);need(self.get(KEYBOARD+0x4B9,'B')==0,'original raw release')
  for _ in range(600):
   self.se_frame('remaining_original_script')
   if self.get(VM+4,'B')==0:break
  else:raise ValueError('bounded original script exit')
  need(self.getreg('EIP')==RETURN and self.getreg('ESP')==STACK+0xF004 and not self.se_event_stack,'entire final original task naturally returned')
  need(len(self.se_commands)==12 and self.se_commands[-1]['opcode']==19 and self.get(VM+28)==self.se_branch['final_PC'],'special19 naturally disables slot without advancing PC')
  need(len(self.se_resources)==len(self.se_resources_before),'no texture creation during original script exit')
  need(all(self.get(r['record']+44)==r['texture']['pointer'] for r in self.se_resources if r['alive']),'each surviving actual generation remains in its original record')
  need(self.space.ledger()==self.se_projection_before and self.space.next==self.se_projection_next,'all GPU identities unchanged; no new projection')
  final=self.se_capture();observations=self.se_observe('final');self.script_exit_active=self.active_overlay=False
  for r in self.se_resources:r['alive_after_forward']=r['alive']
  self.se_result=dict(prefix=self.se_prefix,prefix_preflight=self.se_prefix_preflight,before=self.se_before,branch=self.se_branch,resources_before=self.se_resources_before,resources=copy.deepcopy(self.se_resources),bindings=self.se_bindings,confirmed=confirmed,final=final,segments=self.se_segments,frames=self.se_frames,leaves=self.se_leaves,commands=self.se_commands,writes=self.se_writes,queries=self.se_queries,events=self.se_events,GPU_APIs=self.se_gpu,calls=self.se_calls,conversions=self.se_conversions,readbacks=observations,readback_observers=self.se_observers,GDI_trace=copy.deepcopy(self.name_platform.trace[self.se_prefix['GDI_trace']:]),GDI_handle_projection=self.name_platform.space.ledger(),accounting=self.get(0x765720),forward_wire_end=len(self.gpu.trace),CRT_forward_wire_end=len(self.live.trace),GPU_projection_before=dict(next=self.se_projection_next,ledger=self.se_projection_before),GPU_projection=copy.deepcopy(self.space.ledger()),VM_script_stopped=True,terminal_task_exit_executed=False,rewards_or_school_executed=False)
  return a
 def ld_actual_root(self,*args,**kwargs):
  if not self.script_exit_ready:return super().ld_actual_root(*args,**kwargs)
  return self.se_actual_root(*args,**kwargs)
 def run(self):
  row=super().run();need(not self.se_live and all(not r['alive'] for r in self.se_resources),'all current generations released once')
  row.update(terminal_script_exit=self.se_result,script_exit_cleanup=self.se_cleanup,script_exit_resources_after_cleanup=copy.deepcopy(self.se_resources));return row

def source_contract():
 return dict(parent=parent.source_contract(),fixed_predecessor=fixed_parents(),branches={n:branch(n) for n in ('neutral_running','timeout_before_combat')},keyboard=KEYBOARD,raw_device_bytes=256,new_capture_cycle=True,captured_inputs=followup.parent.parent.input_contract(),forward_roots=[0x40DB90,0x40DC80,0x425DE0,0x454CF0],new_VM_or_handler_roots=0,derived_input_host_writes=0,PC_or_wait_or_phase_host_writes=0,new_OS_input=False,draw_or_Present=False,helper=helper_contract(),extra_code=[dict(start=a,end=b,sha256=sha(CODE[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES],GPU_projection=dict(parent_entries_unchanged=True,new_domains=[],new_creations=0),GDI_projection=dict(current_parent_lifetimes=True,new_creations=0),freeze_boundary='opcode19 disables original slot, then same complete454CF0 returns',terminal_task_exit_executed=False,rewards_or_school_executed=False)

save_source=parent.save_source

def run_case(c,ch,gh,ticks=None):
 fixed=fixed_parent_times()[c['name']];ticks=list(fixed) if ticks is None else ticks;need(ticks==fixed,'exact accepted original clock stream');instances=[]
 class Attached(ScriptExitMachine):
  def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);instances.append(self)
 class Diagnostics:
  @staticmethod
  def save(path,data):
   if instances:
    m=instances[0];data['script_exit']=dict(active=m.script_exit_active,segments=m.se_segments,frames=m.se_frames,leaves=m.se_leaves,resources=m.se_resources,bindings=m.se_bindings,commands=m.se_commands,events=m.se_events,CRT_trace=copy.deepcopy(m.live.trace),GPU_trace=copy.deepcopy(m.gpu.trace),GDI_trace=copy.deepcopy(m.name_platform.trace),GDI_lifetimes=m.ld_gdi_projection.report(),memory=m.snapshot(),trace=m.mark(),local_trace=m.se_mark())
   save_source(path.replace('terminal-overlay-diagnostic-','terminal-script-exit-diagnostic-').replace('.json.gz','-20261030-'+str(time.time_ns())+'.json.gz'),data)
 fn=types.FunctionType(overlay.run_case.__code__,dict(overlay.run_case.__globals__,OverlayMachine=Attached,terminal=Diagnostics),closure=overlay.run_case.__closure__);return fn(c,ch,gh,ticks)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case',type=int);p.add_argument('--helper-prefix',default='terminal-script-exit');a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable script exit source');fixed_parents();ch,gh,b=helpers(a.helper_prefix);rows=[]
 for c in (overlay.parent.corpus() if a.case is None else [overlay.parent.corpus()[a.case]]):rows.append(run_case(c,ch,gh));print('script_exit source',c['name'],'original VM stopped; final task returned',flush=True)
 save_source(a.out,dict(schema_version=1,source_contract=source_contract(),helper_build=b,cases=rows,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False))
