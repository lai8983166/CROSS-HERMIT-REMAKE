"""Consume the original completion flag through the real late battle stages.

453F10 reads the completed task object and walks its own selector sequence
5,15,16,17,18,19,20: the completion flag is consumed, the rectangle fade
runs to 0x100, the result type dispatches the original 4998B0/499910
animation, the accepted raw keyboard cycle opens only 499910's state2 gate,
the 0x4FF rectangle countdown runs 214 frames, and 0x473860 is entered
naturally from 0x454793.  The stage freezes at selector 20 returning 1.
"""
import argparse,copy,gc,gzip,hashlib,json,os,shutil,struct,tempfile,time,types
from functools import lru_cache
from unicorn import UC_PROT_READ,UC_PROT_WRITE
from tools import terminal_task_completion_emulation as parent
from tools import terminal_dialogue_emulation as dialogue
from tools import school_retained_keyboard as keyboard

ROOT,CODE,need,sha,terminal,MAIN,VM,STACK,RETURN,TASK,INPUT,MANAGER,KEYBOARD,overlay=(getattr(parent,n) for n in ('ROOT','CODE','need','sha','terminal','MAIN','VM','STACK','RETURN','TASK','INPUT','MANAGER','KEYBOARD','overlay'))
followup=parent.followup
x86=followup.x86
CTRL=overlay.CTRL
ANIM=CTRL+0x30998
# Exact original bodies reached from the accepted completion handshake.
EXTRA_RANGES=((0x4998B0,0x499901),(0x499910,0x499B5D),(0x49AD50,0x49AD8C),(0x4DB2B0,0x4DB2F4),(0x4116A4,0x411CE2),(0x4DAAE0,0x4DAB06))
NEW_MUTABLE=((TASK+0x38,TASK+0x3C),(TASK+0x108CC2,TASK+0x108CC4),(0x7A417C,0x7A4186),(0x5FF720,0x5FF724),(ANIM,ANIM+0x14),(0x7F44BE,0x7F44CE),(0x7F4518,0x7F7C18))
RANGES=parent.RANGES+EXTRA_RANGES
ALLOWED=frozenset(a for lo,hi in RANGES for a in range(lo,hi))
REFERENCE=types.FunctionType(parent.REFERENCE.__code__,dict(parent.REFERENCE.__globals__,RANGES=RANGES))
PARENT_ACCEPTANCE='analysis/terminal-task-completion-acceptance-v1-20261030.json'
PARENT_ACCEPTANCE_SHA='aacfdcd38f622bc2ab4ee0455d826c78b38e78331a2150a85ae76d0291671fcc'
PARENT_SOURCE='analysis/terminal-task-completion-source-v4-20261030.json.gz'
PARENT_SOURCE_SHA='795bc3e641ca3085991851ee71f0b2b7547b54fcf940e93f60f0b2abefec711b'
PARENT_SOURCE_BYTES=3544248882
PARENT_PROOF='analysis/terminal-task-completion-proof-v1-20261030.json'
PARENT_PROOF_SHA='e17bd23efe9691d7bf6f14ef808500b9d827fd84496c52bb9513b66a6900a3ce'
PARENT_PROOF_BYTES=30263
# Original OR-mask order at 0x4116A4..0x4119B1: (key offset from 0x480, bit).
ACTION_CODES=((0xC8,0),(0xD0,1),(0xCB,2),(0xCD,3),(0x52,4),(0x4F,5),(0x50,6),(0x51,7),
 (0x4B,8),(0x4C,9),(0x4D,10),(0x47,11),(0x48,12),(0x49,13),(0x1C,14),(0x39,15),
 (0x01,16),(0x2A,17),(0x36,17),(0x1D,18),(0x9D,18))
SELECTOR_FRAMES=dict(selector5=1,selector15=1,fade_in=64,animation=32,gate=2,fade_out=32,complete=1,selector18=1,rectangles=214,selector20=1)
RESULT_TYPE_CONFIGURATION={1:2,2:3,3:4,4:5,5:6}
# Mode word stored by the same original result-type arms at 0x4544ec/0x45450b/
# 0x45452a/0x454546/0x454562: [0x5ff720] = 0,1,1,2,2.
RESULT_MODES={1:0,2:1,3:1,4:2,5:2}
# The accepted terminal task stage already owns these two original input-platform
# calls (terminal_task_emulation.APIS): the IME context query at 0x425C99 and the
# kernel32 string length at the original text buffers.  They are not GDI.
TEXT_APIS={0x76182A80:('ImmGetOpenStatus',0x5920EC,0x425C99),0x770206E0:('lstrlenA',0x5922C4,None)}
# The counters that can only move through a host platform call.  The result
# stage must leave every one of them at its accepted task-completion boundary;
# the two accepted text endpoints are recorded separately in bsh_text_APIs.
STAGE_PLATFORM_COUNTS=('CRT_APIs','CRT_wire','resource_steps','task_APIs','APIs','GPU_wire','GDI_trace','GDI_stages','overlay_commands')
recorded_write_PCs=[]


def action_word(block,base):
 value=0
 for offset,bit in ACTION_CODES:
  if block[base+offset]&0x80:value|=1<<bit
 return value


def predict_keyboard(before):
 """Independent host model of 0x4113D5..0x411CE2 over one raw device sample."""
 need(len(before)==0xA00,'complete keyboard model input')
 after=bytearray(keyboard.predict_keyboard(bytes(before)))
 previous=struct.unpack_from('<I',after,0x894)[0];current=action_word(after,0x480);repeat=action_word(after,0x680)
 struct.pack_into('<5I',after,0x890,previous,current,(previous^current)&current,repeat,(previous^current)&previous)
 return bytes(after)


@lru_cache(maxsize=1)
def fixed_parents():
 refs={k:followup.parent.file_ref(p,h) for k,p,h in (('acceptance',PARENT_ACCEPTANCE,PARENT_ACCEPTANCE_SHA),('source',PARENT_SOURCE,PARENT_SOURCE_SHA),('proof',PARENT_PROOF,PARENT_PROOF_SHA))}
 a=json.loads((ROOT/PARENT_ACCEPTANCE).read_text(encoding='utf8'))
 need(a['source_report']==refs['source'] and a['independent_proof']==refs['proof'] and a['tasks_complete']==3,'fixed accepted original task completion')
 need(refs['source']['bytes']==PARENT_SOURCE_BYTES and refs['proof']['bytes']==PARENT_PROOF_BYTES,'fixed task completion report sizes')
 return refs

def fixed_parent_times():return parent.fixed_parent_times()
def helper_contract():return parent.helper_contract()
def helpers(prefix='terminal-battle-stage-handoff'):return parent.helpers(prefix)

@lru_cache(maxsize=1)
def fixed_parent_forward_summaries():
 raw=(ROOT/PARENT_PROOF).read_bytes();need(len(raw)==PARENT_PROOF_BYTES and sha(raw)==PARENT_PROOF_SHA,'fixed task completion proof')
 return {c['name']:c['forward_summary']['full_cumulative'] for c in json.loads(raw)['cases']}

def validate_parent_prefix(machine):
 name=machine.live_input['name'];expected=fixed_parent_forward_summaries()[name];actual=machine.mark()
 need(actual==expected,'fixed complete task completion prefix '+name+' expected='+repr(expected)+' actual='+repr(actual))
 print('battle_stage prefix preflight',name,actual,flush=True)
 return dict(case=name,fixed_proof_sha256=PARENT_PROOF_SHA,expected=expected,actual=actual)


class BattleStageMachine(parent.TaskCompletionMachine):
 source_code=types.FunctionType(parent.TaskCompletionMachine.source_code.__code__,dict(parent.TaskCompletionMachine.source_code.__globals__,ALLOWED=ALLOWED,REFERENCE=REFERENCE))
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.battle_stage_active=self.battle_stage_ready=self.battle_stage_stop=None
  self.battle_stage_result_seen=False;self.battle_stage_result_call=False;self.bsh_keyboard_fragment=False;self.bsh_scene=None;self.bsh_rectangles=0;self.bsh_result=None;self.bsh_result_before=None
  self.bsh_ring_on=False;self.bsh_ring=[None]*64;self.bsh_ring_i=0;self.bsh_ring_label=None;self.gdi_names={slot:row[0] for slot,row in dialogue.GDI.items()}
  self.mutable+=list(NEW_MUTABLE)
  for n in ('segments','frames','bindings','events','writes','calls','rectangles','text_APIs'):setattr(self,'bsh_'+n,[])
  self.bsh_count=self.bsh_write_count=0;self.bsh_ih=hashlib.sha256();self.bsh_wh=hashlib.sha256()
 def bsh_expose_animation_mode(self):
  # 0x5FF720 is the animation mode word in the original writable .data section
  # (PE characteristics 0xC0000040).  The image is mapped RX as one RAM backing,
  # so expose exactly this page while 0x5FF720..0x5FF724 remains the only
  # declared and recorded mutable word on it.  The page is exposed only when the
  # original 453F10 body actually starts: changing one page's protection splits
  # the mapped image into three Unicorn regions, so doing it any earlier would
  # also change the recorded region partition of every accepted parent capture.
  self.uc.mem_protect(0x5FF000,0x1000,UC_PROT_READ|UC_PROT_WRITE)
 def bsh_mark(self):return dict(instructions=self.bsh_count,writes=self.bsh_write_count,code_sha256=self.bsh_ih.hexdigest(),write_sha256=self.bsh_wh.hexdigest())
 def bsh_recent(self):
  n=min(self.bsh_ring_i,64);tail=self.bsh_ring_i%64
  values=self.bsh_ring[:n] if self.bsh_ring_i<64 else self.bsh_ring[tail:]+self.bsh_ring[:tail]
  return [hex(x) for x in values if x is not None]
 def bsh_capture(self,full=True):
  memory=self.snapshot() if full else [dict(pointer=a,bytes=b-a+1,sha256=sha(self.read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()]
  return dict(memory=memory,CPU=self.cpu(),state=self.bsh_state(),queue=self.queue_state(),trace=self.mark(),local_trace=self.bsh_mark())
 def bsh_prefix_counts(self):
  return dict(CRT_APIs=len(self.crt_apis),CRT_wire=len(self.live.trace),resource_steps=len(self.resource_steps),task_APIs=len(self.task_APIs),task_calls=len(self.task_calls),task_writes=len(self.task_writes),APIs=len(self.api_trace),extra_counts=copy.deepcopy(dict(self.extra_counts)),GPU_wire=len(self.gpu.trace),GDI_trace=len(self.name_platform.trace),GDI_stages=len(self.name_platform.service.stages),overlay_commands=len(self.overlay_commands))
 def bsh_state(self):
  return dict(selector=self.get(TASK+0x38),stage_word=self.get(TASK+0x108CC2,'H'),fade=self.get(0x7A4184,'h'),countdown=self.get(0x7A417C,'h'),result_type=self.get(TASK+0x174),
   animation=dict(active=self.get(ANIM,'B'),state=self.get(ANIM+1,'B'),configuration=self.get(ANIM+2,'B'),countdown=self.get(ANIM+4,'H'),progress=self.get(ANIM+8),step=self.get(ANIM+0xC),word_10=self.get(ANIM+0x10,'H'),word_12=self.get(ANIM+0x12,'H')),
   animation_mode=self.get(0x5FF720),held=self.get(MAIN+0x1950),mouse=self.get(MAIN+0x1990),result_flags=self.read(0x7F44BE,16).hex(),
   result_words=[self.get(0x7F450C,'H'),self.get(0x7F450E,'H'),self.get(0x7F4510,'H'),self.get(0x7F4512,'H')],
   actor_word=self.get(0x7F4488,'h'),actor_byte=self.get(0x7F448D,'B'),actor_pair=[self.get(0x7F44AC,'h'),self.get(0x7F44B0,'h')],
   VM_PC=self.get(VM+28),VM_wait=self.get(VM+32,'H'),VM_active=self.get(VM+4,'B'))
 def write_hook(self,uc,access,at,size,value,context):
  super().write_hook(uc,access,at,size,value,context)
  if self.battle_stage_active:
   if self.bsh_keyboard_fragment:need(KEYBOARD<=at and at+size<=KEYBOARD+0xA00 or STACK<=at and at+size<=STACK+0x20000,'finite original battle stage keyboard writes')
   self.bsh_write_count+=1;self.bsh_wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
   if KEYBOARD<=at<KEYBOARD+0xA00 or INPUT<=at<INPUT+0x680 or TASK<=at<TASK+0x190 or ANIM<=at<ANIM+0x20 or 0x7A4178<=at<0x7A4188 or 0x5FF720<=at<0x5FF724 or 0x7F44B0<=at<0x7F7C20 or at==0:
    self.bsh_writes.append(dict(pc=self.getreg('EIP'),address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))
 def code(self,uc,at,size,context):
  active=self.battle_stage_active
  if active:
   need(not (self.task_completion_active or self.script_exit_active or self.followup_active or self.panel_dialogue_active),'separate completed predecessor guards')
   sp=uc.reg_read(x86.UC_X86_REG_ESP)
   if self.bsh_ring_on:self.bsh_ring[self.bsh_ring_i%64]=at;self.bsh_ring_i+=1
   if at==self.battle_stage_stop:uc.emu_stop();return
   need(at not in (0x424F80,0x4CE9C5,0x454E18) and not 0x41F732<=at<0x41F811,'terminal battle stage finite original boundary')
   if self.bsh_keyboard_fragment:need(at not in (0x4CE9C5,0x424F80),'finite original keyboard transform')
   if at==0x4998B0:
    configuration=self.get(sp+4);need(self.getreg('ECX')==CTRL and self.get(TASK+0x38)==17 and configuration in (2,3,4,5,6),'original result animation dispatch on the controller')
    self.bsh_calls.append(dict(entry=at,kind='dispatch',receiver=self.getreg('ECX'),configuration=configuration,result_type=self.get(TASK+0x174)))
   if at==0x499910:
    need(self.getreg('ECX')==CTRL and self.get(TASK+0x38)==17,'original result animation lifecycle only in stage17')
    self.bsh_calls.append(dict(entry=at,kind='animation',state=self.get(ANIM+1,'B'),progress=self.get(ANIM+8),step=self.get(ANIM+0xC),held=self.get(MAIN+0x1950)))
   if at==0x49AD50:
    need(self.getreg('ECX')==CTRL and self.get(sp+4)==5 and self.get(TASK+0x38)==17,'original selected result transition type 5')
    self.bsh_calls.append(dict(entry=at,kind='transition',argument=5,state=self.get(ANIM+1,'B')))
   if at==0x410310:self.bsh_rectangles+=1
   if at==0x454793:
    need(self.getreg('ECX')==CTRL and self.get(TASK+0x38)==20 and not self.battle_stage_result_call and not self.battle_stage_result_seen,'only the original late-stage call instruction reaches 473860')
    self.battle_stage_result_call=True
   if at==0x473860:
    need(self.battle_stage_result_call and self.get(sp)==0x454798 and self.getreg('ECX')==CTRL and not self.battle_stage_result_seen,'only the original 0x454793 result hand-off')
    self.battle_stage_result_seen=True;self.bsh_result_before=self.bsh_state();self.bsh_calls.append(dict(entry=at,kind='result_handoff',call_site=0x454793,return_address=self.get(sp),selector=self.get(TASK+0x38)))
    self.bsh_events.append(dict(entry=at,kind='result_initialization',selector=self.get(TASK+0x38),before=self.bsh_state(),before_CPU=self.cpu()))
   if at in TEXT_APIS:
    name,slot,expected=TEXT_APIS[at];sp=self.getreg('ESP');caller=self.get(sp);arg=self.get(sp+4)
    need(self.get(slot)==at and (expected is None or caller==expected),'exact original input API import '+name)
    if name=='ImmGetOpenStatus':
     need(arg==self.get(INPUT+8)==0,'owned null IME context only');observed=self.ime.query(arg);value=observed['result'];extra=dict(observed=observed)
    else:
     data=self.string(arg);need(len(data)<=0x100,'declared bounded original input text');value=int(self.kernel.lstrlenA(data));extra=dict(string_hex=data.hex())
    row=dict(name=name,entry=at,import_slot=slot,caller=caller,args=[arg],result=value,actual_API_executed=True,segment=self.bsh_ring_label,recent=self.bsh_recent(),**extra)
    self.bsh_text_APIs.append(row);self.return_api(sp,value,4);return
   if at in self.gdi_targets:
    slot=self.gdi_targets[at];raise ValueError('terminal battle stage unexpectedly creates or uses GDI at '+hex(at)+' '+self.gdi_names[slot]+' caller='+hex(self.get(sp))+' segment='+str(self.bsh_ring_label))
  super().code(uc,at,size,context)
  if active and at in ALLOWED:self.bsh_count+=1;self.bsh_ih.update(struct.pack('<I',at))
 def bsh_segment(self,label,entry,stop=RETURN,root=None,kind='task'):
  before=self.cpu();trace=self.mark();local=self.bsh_mark()
  if root:
   sp=STACK+0xF000;self.put(sp,RETURN)
   for j,a in enumerate(root['args']):self.put(sp+4+j*4,a)
   self.uc.reg_write(x86.UC_X86_REG_ESP,sp);self.uc.reg_write(x86.UC_X86_REG_ECX,root['receiver'])
  self.battle_stage_stop=stop;self.uc.ctl_remove_cache(entry,entry+1);self.bsh_ring_label=label;self.bsh_ring_i=0;self.bsh_ring_on=True
  try:self.uc.emu_start(entry,0,timeout=60_000_000,count=4_000_000)
  finally:self.bsh_ring_on=False;self.battle_stage_stop=None
  need(self.getreg('EIP')==stop,'natural original battle stage segment '+label)
  if stop==RETURN:need(self.getreg('ESP')==STACK+0xF004,'complete original battle stage stack '+label)
  row=dict(label=label,kind=kind,entry=entry,stop=stop,root=root,before_CPU=before,CPU=self.cpu(),trace_before=trace,trace_after=self.mark(),local_before=local,local_after=self.bsh_mark());self.bsh_segments.append(row);return row
 def bsh_frame(self,phase,capture=None):
  i=len(self.bsh_frames);before=self.bsh_state();queue=self.queue_state();first=len(self.bsh_segments);selector=self.get(TASK+0x38)
  if capture is not None:self.bsh_captured(capture)
  self.bsh_rectangles=0
  for label,entry,recv in (('heads',0x40DB90,MANAGER),('arena',0x40DC80,MANAGER),('input',0x425DE0,INPUT),('task',0x454CF0,TASK),('stage',0x453F10,TASK)):
   self.bsh_segment(label+'_'+str(i),entry,RETURN,dict(receiver=recv,args=[]))
  row=dict(index=i,phase=phase,capture=None if capture is None else capture['label'],selector=selector,result=self.getreg('EAX'),rectangles=self.bsh_rectangles,before=before,after=self.bsh_state(),queue_before=queue,queue_after=self.queue_state(),segments=[first,len(self.bsh_segments)],capture_after=self.bsh_capture(False));self.bsh_frames.append(row)
  print(self.live_input['name'],'battle_stage',phase,i,selector,'->',row['after']['selector'],flush=True);return row
 def bsh_captured(self,capture):
  index=len(self.bsh_bindings);stream=followup.parent.parent.input_contract()['streams'][str(self.bsh_scene)]
  need(index<3 and capture==stream['captures'][index],'new independent stage cycle uses exact accepted raw sample sequence')
  raw=bytes.fromhex(capture['raw_device_hex']);need(len(raw)==256,'entire original current keyboard raw sample')
  before=self.read(KEYBOARD,0xA00);bound=bytearray(before);bound[12:268]=raw
  cpu=self.cpu();trace=self.mark();local=self.bsh_mark();self.uc.mem_write(KEYBOARD+12,raw);bp=STACK+0xF800;self.put(bp-4,KEYBOARD)
  # 0x4112b0/0x4112b5 of the same original function compute [ebp-8] = receiver
  # + 0x890, the five action words written past 0x4116a4.  Entering at the
  # accepted 0x4113d5 fragment therefore has to supply that original local too.
  self.put(bp-8,KEYBOARD+0x890)
  for key,value in dict(EBP=bp,ESP=bp-0x70,EFLAGS=0x202).items():self.uc.reg_write(getattr(x86,'UC_X86_REG_'+key),value)
  self.bsh_keyboard_fragment=True
  try:self.bsh_segment('battle_stage_captured_'+capture['label'],0x4113D5,0x411CE2,kind='keyboard')
  finally:self.bsh_keyboard_fragment=False
  after=self.read(KEYBOARD,0xA00);expected=predict_keyboard(bytes(bound))
  need(after==expected,'independent entire original keyboard and action word output '+capture['label'])
  result=dict(cycle='battle_stage_'+capture['label'],capture=copy.deepcopy(capture),before_CPU=cpu,trace_before=trace,local_before=local,before_hex=before.hex(),bound_hex=bytes(bound).hex(),after_hex=after.hex(),expected_hex=expected.hex(),held_word=self.get(MAIN+0x1950),
   only_device_output_written=dict(pointer=KEYBOARD+12,bytes=256),fragment=dict(va=0x4113D5,bp=bp,sp=bp-0x70,receiver_slot=bp-4,receiver=KEYBOARD,action_word_slot=bp-8,action_word_pointer=KEYBOARD+0x890,stop=0x411CE2),segment_index=len(self.bsh_segments)-1,after_capture=self.bsh_capture(False));self.bsh_bindings.append(result);return result
 def admission(self):
  a=super().admission();self.bsh_prefix_preflight=validate_parent_prefix(self);self.bsh_prefix=self.bsh_prefix_counts()
  result_type=self.get(TASK+0x174)
  need((self.get(TASK+0x38),self.get(TASK+0x171,'B'),self.get(TASK+0x172,'B'))==(5,1,1) and result_type in RESULT_TYPE_CONFIGURATION,'accepted original completion flag and dispatched result type '+str(result_type))
  self.bsh_result_type=result_type;self.bsh_configuration=RESULT_TYPE_CONFIGURATION[result_type];self.bsh_animation_mode=RESULT_MODES[result_type]
  need(self.get(0x7A4184,'h')==0 and self.get(0x7A417C,'h')==0 and self.get(ANIM,'B')==0 and self.get(0x5FF720)==0xFFFFFFFF,'untouched late stage counters')
  self.bsh_before=self.bsh_capture();self.bsh_expose_animation_mode()
  self.bsh_scene=followup.branch(self.live_input['name'])['scene_capture']
  self.battle_stage_ready=self.battle_stage_active=self.active_overlay=True
  captures=followup.parent.parent.input_contract()['streams'][str(self.bsh_scene)]['captures']
  r=self.bsh_frame('selector5');need(r['after']['selector']==15 and self.get(TASK+0x108CC2,'H')==0,'original completion flag consumed into stage15')
  r=self.bsh_frame('selector15');need(r['after']['selector']==16 and self.get(0x7A4184,'h')==0,'original stage15 arms the rectangle fade')
  for k in range(1,65):
   r=self.bsh_frame('fade_in_'+str(k));need(self.get(0x7A4184,'h')==4*k,'original rectangle fade increment '+str(k));need(r['after']['selector']==(17 if k==64 else 16),'original fade completes at 0x100')
  need((self.get(ANIM,'B'),self.get(ANIM+1,'B'),self.get(ANIM+2,'B'),self.get(ANIM+8),self.get(0x5FF720))==(1,0,self.bsh_configuration,0,self.bsh_animation_mode),'original result type '+str(self.bsh_result_type)+' dispatches configuration '+str(self.bsh_configuration)+' and mode '+str(self.bsh_animation_mode))
  self.bsh_dispatch=self.bsh_capture(False)
  # 0x49999d initializes progress/step and advances the state byte, then falls
  # through into 0x4999cf (progress += step), so the first selector-17 frame
  # already ends with progress 0x800.
  r=self.bsh_frame('animation_start');need((self.get(ANIM+1,'B'),self.get(ANIM+8),self.get(ANIM+0xC))==(1,0x800,0x800),'original animation start frame')
  for k in range(2,33):
   r=self.bsh_frame('animation_progress_'+str(k));need(self.get(ANIM+1,'B')==(1 if k<32 else 2),'original animation state '+str(k));need(self.get(ANIM+8)==(k*0x800 if k<32 else 0xFF00),'original animation progress '+str(k))
  need(self.get(0x7F4491,'B')==0,'original result guard word stays clear')
  r=self.bsh_frame('animation_gate_control',captures[0]);need((self.get(ANIM+1,'B'),self.get(MAIN+0x1950),self.get(0x5FF720))==(2,0,self.bsh_animation_mode),'no input keeps the original animation gate closed')
  self.bsh_gate=self.bsh_capture(False)
  r=self.bsh_frame('animation_gate_press',captures[1]);need((self.get(ANIM+1,'B'),self.get(ANIM+0xC),self.get(MAIN+0x1950))==(4,0x800,0x8000),'original captured press opens only the original gate')
  for k in range(1,33):
   r=self.bsh_frame('animation_fade_'+str(k),captures[2] if k==1 else None);need(self.get(ANIM+8)==(0xFF00-k*0x800 if k<32 else 0),'original animation fade '+str(k));need(self.get(ANIM+1,'B')==(4 if k<32 else 5),'original fade state '+str(k))
  r=self.bsh_frame('animation_complete');need((self.get(ANIM,'B'),r['after']['selector'])==(0,18),'original animation 499910 returns 1 exactly once')
  self.bsh_fade=self.bsh_capture(False)
  r=self.bsh_frame('selector18');need(self.get(0x7A417C,'h')==0x4FF and r['after']['selector']==19,'original result rectangle countdown armed')
  for k in range(1,215):
   r=self.bsh_frame('result_rectangles_'+str(k));need(self.bsh_rectangles==128,'128 original result rectangles in frame '+str(k));need(self.get(0x7A417C,'h')==0x4FF-6*k,'original result countdown '+str(k));need(r['after']['selector']==(20 if k==214 else 19),'original result countdown drives stage'+str(k))
   self.bsh_rectangles_rows=self.bsh_rectangles
  need(self.battle_stage_result_seen and self.bsh_result_before is not None,'original 473860 entered from 0x454793 in the completing frame')
  self.bsh_result=dict(frame=self.bsh_frames[-1]['index'],before=self.bsh_result_before,event=copy.deepcopy(self.bsh_events),after=r['after'],capture=self.bsh_capture())
  r=self.bsh_frame('selector20');need(r['result']==1 and self.get(TASK+0x38)==20,'original stage20 returns 1')
  self.bsh_identity_after=dict(actor_word=self.get(0x7F4488,'h'),actor_byte=self.get(0x7F448D,'B'),actor_pair=[self.get(0x7F44AC,'h'),self.get(0x7F44B0,'h')],result_words=[self.get(0x7F450C+(j*2),'H') for j in range(4)],flags_hex=self.read(0x7F44BE,16).hex(),VM_PC=self.get(VM+28),VM_wait=self.get(VM+32,'H'),VM_active=self.get(VM+4,'B'))
  need(not self.bsh_keyboard_fragment and self.getreg('EIP')==RETURN and self.getreg('ESP')==STACK+0xF004,'entire final original stage naturally returned')
  self.bsh_final=self.bsh_capture();self.battle_stage_active=self.active_overlay=False
  self.bsh_counts_after=self.bsh_prefix_counts()
  need(all(self.bsh_counts_after[k]==self.bsh_prefix[k] for k in STAGE_PLATFORM_COUNTS),'no new platform call during the original result stage')
  self.bsh_result_summary=dict(prefix=self.bsh_prefix,counts_after=self.bsh_counts_after,text_APIs=self.bsh_text_APIs,prefix_preflight=self.bsh_prefix_preflight,before=self.bsh_before,dispatch=self.bsh_dispatch,gate=self.bsh_gate,fade=self.bsh_fade,result=self.bsh_result,final=self.bsh_final,identity_after=self.bsh_identity_after,bindings=self.bsh_bindings,frames=self.bsh_frames,segments=self.bsh_segments,events=self.bsh_events,calls=self.bsh_calls,writes=self.bsh_writes,rectangles_per_frame=128,rectangle_frames=214,frames_total=len(self.bsh_frames),captures_used=len(self.bsh_bindings),freeze_selector=20,freeze_EAX=1,result_type=self.bsh_result_type,result_configuration=self.bsh_configuration,animation_mode=self.bsh_animation_mode,terminal_battle_stage_handoff_executed=True,terminal_battle_exit_executed=False,rewards_or_school_executed=False,terminal_presentation_complete=False)
  return a
 def run(self):
  row=super().run();row.update(terminal_battle_stage_handoff=self.bsh_result_summary);return row


def source_contract():
 return dict(parent=parent.source_contract(),fixed_predecessor=fixed_parents(),forward_roots=[0x40DB90,0x40DC80,0x425DE0,0x454CF0,0x453F10],new_VM_or_handler_roots=0,derived_input_host_writes=0,PC_or_wait_or_phase_host_writes=0,new_OS_input=False,new_capture_cycle=False,draw_or_Present=False,helper=helper_contract(),
  extra_code=[dict(start=a,end=b,sha256=sha(CODE[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES],
  new_mutable=[dict(start=a,end=b,write_PCs=recorded_write_PCs) for a,b in NEW_MUTABLE],
  result_types=[1,2,3,4,5],result_configurations=[2,3,4,5,6],result_modes=[0,1,1,2,2],selectors=[5,15,16,17,18,19,20],selector_frames=dict(SELECTOR_FRAMES),frames_total=1+1+64+32+2+32+1+1+214+1,
  rectangle_arguments=dict(entry=0x410310,receiver=MANAGER,per_frame=128,source_rows=0x40,color_step=0x10,countdown_step=6),
  natural_result_handoff=dict(entry=0x473860,call_site=0x454793,return_address=0x454798,receiver='TASK+0x190',executed_once=True),
  supplemental_calls_outside_source=0,GPU_or_GDI_or_Present=False,terminal_battle_stage_handoff_executed=True,terminal_battle_exit_executed=False,rewards_or_school_executed=False,terminal_presentation_complete=False)


save_source=parent.save_source


def save_source_cases(path,head,case_files,footer):
 """Write the exact same single report object, one case row at a time.

 Each row is already on disk, so only one case is ever held in memory and the
 compressed stream is produced without building a second full-text copy.
 """
 p=ROOT/path;need(not p.exists(),'fresh immutable battle stage handoff source');encoder=json.JSONEncoder(ensure_ascii=False,separators=(',',':'))
 def write(output):
  output.write(b'{')
  for key,value in head.items():output.write(encoder.encode(key).encode('utf8')+b':'+encoder.encode(value).encode('utf8')+b',')
  output.write(b'"cases":[')
  for index,source in enumerate(case_files):
   if index:output.write(b',')
   with open(source,'rb') as stream:
    for block in iter(lambda:stream.read(1048576),b''):output.write(block)
  output.write(b']')
  for key,value in footer.items():output.write(b','+encoder.encode(key).encode('utf8')+b':'+encoder.encode(value).encode('utf8'))
  output.write(b'}\n')
 with p.open('xb') as output:
  if p.suffix=='.gz':
   with gzip.GzipFile(fileobj=output,mode='wb',filename='',mtime=0,compresslevel=6) as compressed:write(compressed)
  else:write(output)

def run_case(c,ch,gh,ticks=None):
 fixed=fixed_parent_times()[c['name']];ticks=list(fixed) if ticks is None else ticks;need(ticks==fixed,'exact accepted original clock stream');instances=[]
 class Attached(BattleStageMachine):
  def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);instances.append(self)
 class Diagnostics:
  @staticmethod
  def save(path,data):
   if instances:
    m=instances[0];data['battle_stage']=dict(active=m.battle_stage_active,segments=m.bsh_segments,frames=m.bsh_frames,events=m.bsh_events,calls=m.bsh_calls,writes=m.bsh_writes,bindings=m.bsh_bindings,text_APIs=m.bsh_text_APIs,recent=m.bsh_recent(),state=m.bsh_state(),CRT_trace=copy.deepcopy(m.live.trace),GPU_trace=copy.deepcopy(m.gpu.trace),GDI_trace=copy.deepcopy(m.name_platform.trace),GDI_lifetimes=m.name_platform.space.ledger(),memory=m.snapshot(),trace=m.mark(),local_trace=m.bsh_mark())
   save_source(path.replace('terminal-overlay-diagnostic-','terminal-battle-stage-handoff-diagnostic-').replace('.json.gz','-20261031-'+str(time.time_ns())+'.json.gz'),data)
 fn=types.FunctionType(overlay.run_case.__code__,dict(overlay.run_case.__globals__,OverlayMachine=Attached,terminal=Diagnostics),closure=overlay.run_case.__closure__);return fn(c,ch,gh,ticks)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case',type=int);p.add_argument('--helper-prefix',default='terminal-battle-stage-handoff');a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable battle stage handoff source');fixed_parents();ch,gh,b=helpers(a.helper_prefix);files=[];pcs=set();work=tempfile.mkdtemp(prefix='terminal-battle-stage-handoff-');encoder=json.JSONEncoder(ensure_ascii=False,separators=(',',':'))
 try:
  for index,c in enumerate(overlay.parent.corpus() if a.case is None else [overlay.parent.corpus()[a.case]]):
   row=run_case(c,ch,gh);pcs.update(w['pc'] for w in row['terminal_battle_stage_handoff']['writes']);name=os.path.join(work,'case-'+str(index)+'.json')
   with open(name,'xb') as stream:
    for block in encoder.iterencode(row):stream.write(block.encode('utf8'))
   del row;gc.collect();files.append(name);print('battle_stage source',c['name'],'original late battle stage returned',flush=True)
  recorded_write_PCs[:]=sorted(pcs)
  save_source_cases(a.out,dict(schema_version=1,source_contract=source_contract(),helper_build=b),files,dict(R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False))
 finally:shutil.rmtree(work,ignore_errors=True)
