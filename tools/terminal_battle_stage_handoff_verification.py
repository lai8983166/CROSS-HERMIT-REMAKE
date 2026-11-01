"""Independent original battle stage 5..20 handoff and natural 473860."""
from tools.terminal_task_completion_verification import *
from tools import terminal_task_completion_verification as previous_stage
from tools import terminal_battle_stage_handoff_emulation as e
import ast,inspect,textwrap
from unicorn import UC_PROT_READ,UC_PROT_WRITE
ROOT=e.ROOT
IMPLEMENTATIONS=('tools/terminal_battle_stage_handoff_emulation.py','tools/terminal_battle_stage_handoff_verification.py','tools/terminal_battle_stage_handoff_preservation.py','tools/tests/test_terminal_battle_stage_handoff.py','tools/tests/test_terminal_battle_stage_handoff_source.py')
EXTRA_RANGES=e.EXTRA_RANGES
NEW_MUTABLE=e.NEW_MUTABLE
SELECTOR_FRAMES=e.SELECTOR_FRAMES
TEXT_APIS=e.TEXT_APIS
RESULT_TYPE_CONFIGURATION=e.RESULT_TYPE_CONFIGURATION
RESULT_MODES=e.RESULT_MODES
TOTAL_FRAMES=sum(SELECTOR_FRAMES.values())

@lru_cache(maxsize=1)
def task_completion_report():
 e.fixed_parents()
 need(e.PARENT_SOURCE_BYTES==(ROOT/e.PARENT_SOURCE).stat().st_size,'fixed task completion source size')
 return load_report(ROOT/e.PARENT_SOURCE)

def parent_case(row):return next(x for x in task_completion_report()['cases'] if x['input']==row['input'])
def accepted_clock_inputs():return {r['input']['name']:[a['result'] for a in r['APIs'] if a['name']=='GetTickCount'] for r in task_completion_report()['cases']}

@lru_cache(maxsize=1)
def accepted_case_witness():
 """Keep only the accepted task completion boundary each stage case starts from.

 The boundary is the parent summary's own final capture plus the receipt counts
 and fixed clock inputs; the supplementary original cleanup the accepted change
 appended afterwards is not part of it.  Building the witness once and releasing
 the cached parent report keeps one complete accepted case out of memory while
 the streamed stage row and the reused parent chain are held.
 """
 rows=task_completion_report()['cases'];out={r['input']['name']:dict(final=r['terminal_task_completion']['final'],counts={k:len(r[k]) for k in ('task_APIs','task_calls','task_writes','APIs')},entries=dict(r['entries']),ticks=[a['result'] for a in r['APIs'] if a['name']=='GetTickCount']) for r in rows}
 task_completion_report.cache_clear()
 return out

@lru_cache(maxsize=1)
def parent_trace_summaries():
 raw=(ROOT/e.PARENT_PROOF).read_bytes();need(len(raw)==e.PARENT_PROOF_BYTES and sha(raw)==e.PARENT_PROOF_SHA,'fixed task completion proof')
 return {c['name']:c['forward_summary']['full_cumulative'] for c in json.loads(raw)['cases']}

def prefix_trace(row):
 name=row['input']['name'];d=row['terminal_battle_stage_handoff'];want=parent_trace_summaries()[name]
 need(d['before']['trace']==want,'exact accepted task completion cumulative boundary '+name)
 need(d['prefix_preflight']==dict(case=name,fixed_proof_sha256=e.PARENT_PROOF_SHA,expected=want,actual=want),'entire fixed task completion prefix preflight independently bound')

def stage_mark_expected(d):
 counts=d['prefix'];return dict(CRT_APIs=counts['CRT_APIs'],CRT_wire=counts['CRT_wire'],task_APIs=counts['task_APIs'],APIs=counts['APIs'],GPU_wire=counts['GPU_wire'],GDI_trace=counts['GDI_trace'])

def no_new_platform_calls(row,prior):
 d=row['terminal_battle_stage_handoff'];p=d['prefix'];a=d['counts_after']
 need(sorted(a)==sorted(p),'stage-local counters recorded at the same boundary keys')
 for k in e.STAGE_PLATFORM_COUNTS:need(a[k]==p[k],'no new '+k+' during the original result stage')
 need(prior['current_GDI_calls']==a['GDI_trace'],'whole current GDI receipts still equal the frozen stage boundary')
 return dict({k:a[k] for k in e.STAGE_PLATFORM_COUNTS},no_new_platform_calls=True)

def staged_state(r):
 def g(p,f):return num(r.read(p,struct.calcsize('<'+f)),0,f)
 return dict(selector=g(e.TASK+0x38,'I'),stage_word=g(e.TASK+0x108CC2,'H'),fade=g(0x7A4184,'h'),countdown=g(0x7A417C,'h'),result_type=g(e.TASK+0x174,'I'),
  animation=dict(active=g(e.ANIM,'B'),state=g(e.ANIM+1,'B'),configuration=g(e.ANIM+2,'B'),countdown=g(e.ANIM+4,'H'),progress=g(e.ANIM+8,'I'),step=g(e.ANIM+0xC,'I'),word_10=g(e.ANIM+0x10,'H'),word_12=g(e.ANIM+0x12,'H')),
  animation_mode=g(0x5FF720,'I'),held=g(e.MAIN+0x1950,'I'),mouse=g(e.MAIN+0x1990,'I'),result_flags=r.read(0x7F44BE,16).hex(),
  result_words=[g(0x7F450C+2*j,'H') for j in range(4)],actor_word=g(0x7F4488,'h'),actor_byte=g(0x7F448D,'B'),actor_pair=[g(0x7F44AC,'h'),g(0x7F44B0,'h')],
  VM_PC=g(e.VM+28,'I'),VM_wait=g(e.VM+32,'H'),VM_active=g(e.VM+4,'B'))

def staged_queue(r):
 manager=r.read(e.MANAGER,0x38);heads=num(manager,16);arena=num(manager,20);used=num(manager,0x30)-arena
 need(0<=used<=65536,'bounded current arena')
 return dict(manager=manager.hex(),heads=r.read(heads,4096*8).hex(),arena_pointer=arena,used=used,arena=r.read(arena,used).hex(),unused_tail_sha256=sha(r.read(arena+used,65536-used)))

def staged_regions(r):
 return sorted((dict(pointer=a,bytes=b-a+1,sha256=sha(bytes(r.u.mem_read(a,b-a+1)))) for a,b,_ in r.u.mem_regions()),key=lambda x:x['pointer'])

def snapshot_regions(r):
 return sorted((dict(pointer=a,bytes=b-a+1,hex=bytes(r.u.mem_read(a,b-a+1)).hex()) for a,b,_ in r.u.mem_regions()),key=lambda x:x['pointer'])

def stage_state_memory_equal(replay,rows,label):
 actual=snapshot_regions(replay)
 need([(x['pointer'],x['bytes']) for x in actual]==[(x['pointer'],x['bytes']) for x in rows],label+' complete mapped region set')
 for x,y in zip(actual,rows):
  need(x['hex']==y['hex'],label+' full region bytes at '+hex(x['pointer']))

def capture_equal(replay,cap,label):
 need(replay.cpu()==cap['CPU'],label+' all57 architectural registers')
 need(staged_state(replay)==cap['state'],label+' complete original task state')
 need(staged_queue(replay)==cap['queue'],label+' complete manager queue')
 need(staged_regions(replay)==sorted(cap['memory'],key=lambda x:x['pointer']),label+' every mapped region digest')

def expected_phases():
 phases=['selector5','selector15']+['fade_in_'+str(k) for k in range(1,65)]+['animation_start']+['animation_progress_'+str(k) for k in range(2,33)]
 phases+=['animation_gate_control','animation_gate_press']+['animation_fade_'+str(k) for k in range(1,33)]+['animation_complete','selector18']
 phases+=['result_rectangles_'+str(k) for k in range(1,215)]+['selector20']
 return phases

def protocol(row):
 d=row['terminal_battle_stage_handoff'];frames=d['frames'];segs=d['segments'];name=row['input']['name']
 need(TOTAL_FRAMES==349 and len(frames)==TOTAL_FRAMES,'complete 349-frame original selector schedule')
 need([f['phase'] for f in frames]==expected_phases(),'exact original selector phase order 5,15,16,17,18,19,20')
 need(len(d['bindings'])==3 and len(segs)==TOTAL_FRAMES*5+3,'three captured raw samples over the five original roots')
 prior=d['before'];capture_labels=[b['capture']['label'] for b in d['bindings']]
 # The stage records its own platform counters at the accepted task-completion
 # boundary and again after the final selector-20 frame; no counter that only a
 # host platform call can move may change across the whole original stage.
 counts=d['counts_after'];need(sorted(counts)==sorted(d['prefix']),'stage-local counters recorded at the same boundary keys')
 for k in e.STAGE_PLATFORM_COUNTS:need(counts[k]==d['prefix'][k],'no new '+k+' during the original result stage')
 text=d['text_APIs'];need(all(r['entry'] in TEXT_APIS and r['name']==TEXT_APIS[r['entry']][0] and r['import_slot']==TEXT_APIS[r['entry']][1] and (TEXT_APIS[r['entry']][2] is None or r['caller']==TEXT_APIS[r['entry']][2]) and r['actual_API_executed'] is True for r in text),'only the two accepted input endpoints are called during the stage')
 # Every one of the 349 frames runs the original input and task segments; the
 # owned null-IME query stays inside input_<frame> and the declared bounded
 # string inside task_<frame>.  The three captured keyboard gateway segments
 # add no text call of their own, so the receipts are the per-frame sequence.
 want=[s for i in range(TOTAL_FRAMES) for s in ('input_'+str(i),'task_'+str(i))]
 need([r['segment'] for r in text]==want,'input endpoints stay in each frame own input and task segment')
 need([r['name'] for r in text]==['ImmGetOpenStatus','lstrlenA']*TOTAL_FRAMES,'three captured gateway segments add no text endpoint')
 for i,f in enumerate(frames):
  need(f['index']==i and f['segments']==[f['segments'][0],f['segments'][0]+(5+(1 if i in (98,99,100) else 0))],'exact contiguous frame segment range')
  need(f['before']==prior['state'] and f['queue_before']==prior['queue'],'every frame starts from the prior frame completed state')
  need(f['capture']==(capture_labels[i-98] if i in (98,99,100) else None),'raw device sample bound only at the original gate frames')
  cap=f['capture_after'];need(cap['state']==f['after'] and cap['queue']==f['queue_after'],'capture after state/queue equals frame output')
  prior=cap
 need(d['before']['local_trace']==mark_zero(),'new stage-local instruction digest starts empty')
 need(len(d['before']['CPU'])==57,'all57 architectural registers at the stage boundary')
 need(d['result']['frame']==347,'473860 naturally called in the 214th rectangle frame')
 # The sub-stage word is written only as 1 (0x453f4d/0x4543f6, the waiting arm)
 # or 0 (0x4542a1/0x45442e, the completion arm).  neutral_running still has 0;
 # the timeout branch passed the waiting arm, so it keeps 1 until selector5's
 # own completion arm zeroes it in the first frame (checked next).
 need(d['before']['state']['selector']==5 and d['before']['state']['fade']==0,'stage begins at selector5 with untouched late counters')
 need(d['before']['state']['stage_word'] in (0,1),'original sub-stage word at the boundary is one of its own two written values')
 f=frames
 need(f[0]['after']['selector']==15 and f[0]['after']['stage_word']==0,'selector5 consumes the original completion flag into 15')
 need(f[1]['after']['selector']==16 and f[1]['after']['fade']==0,'selector15 arms the rectangle fade')
 for k in range(1,65):
  row_f=f[1+k];need(row_f['after']['fade']==4*k and row_f['after']['selector']==(17 if k==64 else 16),'original rectangle fade frame '+str(k))
 rt=d['result_type'];need(rt in RESULT_TYPE_CONFIGURATION,'frozen result type is one of the original dispatched arms')
 need(d['result_configuration']==RESULT_TYPE_CONFIGURATION[rt] and d['animation_mode']==RESULT_MODES[rt],'frozen result type '+str(rt)+' dispatch matches its original arm')
 need((f[65]['after']['animation']['active'],f[65]['after']['animation']['state'],f[65]['after']['animation']['configuration'],f[65]['after']['animation']['progress'],f[65]['after']['animation_mode'])==(1,0,RESULT_TYPE_CONFIGURATION[rt],0,RESULT_MODES[rt]),'original result type '+str(rt)+' dispatches its configuration and mode word')
 # 0x49999d (state 0) falls through into 0x4999cf, so the first selector-17
 # frame already adds the 0x800 step to the zeroed progress.
 need((f[66]['after']['animation']['state'],f[66]['after']['animation']['progress'],f[66]['after']['animation']['step'])==(1,0x800,0x800),'original animation start frame')
 for k in range(2,33):
  a=f[65+k]['after']['animation'];need(a['state']==(1 if k<32 else 2) and a['progress']==(k*0x800 if k<32 else 0xFF00),'4910 original animation progress '+str(k))
 need(f[98]['after']['animation']['state']==2 and f[98]['after']['held']==0 and f[98]['after']['animation_mode']==RESULT_MODES[rt],'no input keeps the original animation gate closed')
 need((f[99]['after']['animation']['state'],f[99]['after']['animation']['step'],f[99]['after']['held'])==(4,0x800,0x8000),'captured press opens only the original gate')
 for k in range(1,33):
  a=f[99+k]['after']['animation'];need(a['progress']==(0xFF00-k*0x800 if k<32 else 0) and a['state']==(4 if k<32 else 5),'original animation fade frame '+str(k))
 need((f[132]['after']['animation']['active'],f[132]['after']['selector'])==(0,18),'original 499910 returns 1 exactly once')
 need(f[133]['after']['countdown']==0x4FF and f[133]['after']['selector']==19,'original result rectangle countdown armed')
 for k in range(1,215):
  row_f=f[133+k];need(row_f['rectangles']==128,'128 original result rectangles in frame '+str(k));need(row_f['after']['countdown']==0x4FF-6*k,'original result countdown '+str(k));need(row_f['after']['selector']==(20 if k==214 else 19),'original countdown drives stage '+str(k))
 need(f[348]['result']==1 and f[348]['after']['selector']==20,'original stage20 returns 1 and freezes')
 need(d['identity_after']==dict(actor_word=f[348]['after']['actor_word'],actor_byte=f[348]['after']['actor_byte'],actor_pair=f[348]['after']['actor_pair'],result_words=f[348]['after']['result_words'],flags_hex=f[348]['after']['result_flags'],VM_PC=f[348]['after']['VM_PC'],VM_wait=f[348]['after']['VM_wait'],VM_active=f[348]['after']['VM_active']),'frozen result identity equals the final original task state')
 branch=previous_stage.branch(name);need(f[348]['after']['VM_PC']==branch['final_PC'] and f[348]['after']['VM_wait']==0 and f[348]['after']['VM_active']==0,'stopped VM remains at its exact final PC')
 bound=[b for b in d['bindings']]
 need([b['capture']['label'] for b in bound]==capture_labels and [b['cycle'] for b in bound]==['battle_stage_'+x for x in capture_labels],'each raw device sample is used once in its own original keyboard cycle')
 stream=e.followup.parent.parent.input_contract()['streams'][str(e.followup.branch(name)['scene_capture'])]['captures']
 for i,b in enumerate(bound):
  need(b['capture']==stream[i],'raw device sample '+str(i)+' is the accepted finite capture sequence')
  need(bytes.fromhex(b['bound_hex'])[12:268]==bytes.fromhex(b['capture']['raw_device_hex']) and bytes.fromhex(b['bound_hex'])[0:12]==bytes.fromhex(b['before_hex'])[0:12],'entire original current keyboard sample binding')
  need(b['after_hex']==b['expected_hex'] and b['after_hex']==e.predict_keyboard(bytes.fromhex(b['bound_hex'])).hex(),'independent complete original keyboard transform output')
  need(b['only_device_output_written']==dict(pointer=e.KEYBOARD+12,bytes=256) and b['fragment']==dict(va=0x4113D5,bp=e.STACK+0xF800,sp=e.STACK+0xF800-0x70,receiver_slot=e.STACK+0xF800-4,receiver=e.KEYBOARD,action_word_slot=e.STACK+0xF800-8,action_word_pointer=e.KEYBOARD+0x890,stop=0x411CE2),'keyboard fragment operates only on the owned device block and stack')
  need(b['segment_index']==frames[98+i]['segments'][0],'keyboard fragment belongs to its exact gate frame')
 need([r['kind'] for r in d['calls']].count('dispatch')==1 and [r['kind'] for r in d['calls']].count('result_handoff')==1,'one original result dispatch and one natural 473860 hand-off')
 hand=[r for r in d['calls'] if r['kind']=='result_handoff'][0];need(hand['entry']==0x473860 and hand['call_site']==0x454793 and hand['return_address']==0x454798 and hand['selector']==20,'natural call exactly at the original 0x454793/0x454798 site')
 ev=d['events'];need(len(ev)==1 and ev[0]['entry']==0x473860 and ev[0]['kind']=='result_initialization' and ev[0]['before']['selector']==20,'original 473860 entered once from its own call site')
 return dict(complete_frames=len(frames),segments=len(segs),selector_sequence=[5,15,16,17,18,19,20],rectangle_frames=214,rectangles_per_frame=128,result_handoff='0x454793->0x473860->0x454798',freeze_selector=20,freeze_EAX=1,new_input_bindings=3,battle_exit_consumer_executed=False)

def bind_keyboard(replay,binding):
 u=replay.u;need(replay.cpu()==binding['before_CPU'],'keyboard fragment begins at the recorded pre-binding CPU')
 raw=bytes.fromhex(binding['capture']['raw_device_hex']);need(len(raw)==256,'complete raw device sample')
 need(replay.read(e.KEYBOARD,0xA00).hex()==binding['before_hex'],'entire current keyboard sample before binding')
 u.mem_write(e.KEYBOARD+12,raw);u.mem_write(e.STACK+0xF800-4,struct.pack('<I',e.KEYBOARD))
 # Original prologue local at 0x4112b0/0x4112b5: [ebp-8] = receiver + 0x890.
 u.mem_write(e.STACK+0xF800-8,struct.pack('<I',e.KEYBOARD+0x890))
 need(replay.read(e.KEYBOARD,0xA00).hex()==binding['bound_hex'],'exact whole keyboard block after sample binding')
 for key,value in dict(EBP=binding['fragment']['bp'],ESP=binding['fragment']['sp'],EFLAGS=0x202).items():u.reg_write(getattr(x86,'UC_X86_REG_'+key),value)

def apply_text(replay,receipt,used,label):
 u=replay.u;at=receipt['entry'];name,slot,expected=TEXT_APIS[at];sp=u.reg_read(x86.UC_X86_REG_ESP)
 caller=num(bytes(u.mem_read(sp,4)),0);arg=num(bytes(u.mem_read(sp+4,4)),0)
 need(num(bytes(u.mem_read(slot,4)),0)==at,'unchanged original input-platform IAT '+name)
 need((receipt['segment'],receipt['import_slot'],receipt['caller'],receipt['args'])==(label,slot,caller,[arg]),'one recorded original '+name+' call at its exact stack')
 if name=='ImmGetOpenStatus':
  need(arg==num(bytes(u.mem_read(e.INPUT+8,4)),0)==0 and receipt['result']==0,'owned null IME context query')
 else:
  data=b'';p=arg
  while len(data)<=0x100:
   b=bytes(u.mem_read(p+len(data),1))
   if b==b'\x00':break
   data+=b
  need(len(data)<=0x100 and data.hex()==receipt['string_hex'] and receipt['result']==len(data),'original bounded text length input')
 u.reg_write(x86.UC_X86_REG_EAX,receipt['result']);u.reg_write(x86.UC_X86_REG_ESP,sp+8);u.reg_write(x86.UC_X86_REG_EIP,caller)

def execute_stage(replay):
 """Re-execute every original stage segment in the actual parent lifetime."""
 row=replay.row;d=row['terminal_battle_stage_handoff'];u=replay.u;frames=d['frames'];segs=d['segments']
 # Same point as the source machine: the accepted parent lifetime was already
 # replayed and compared against the unsplit stage-before capture, so only now
 # expose the original .data mode-word page for the first stage segment.
 u.mem_protect(0x5FF000,0x1000,UC_PROT_READ|UC_PROT_WRITE)
 bindings={b['segment_index']:b for b in d['bindings']};text={}
 for r in d['text_APIs']:text.setdefault(r['segment'],[]).append(r)
 used={};count=writes=0;ih=hashlib.sha256();wh=hashlib.sha256();stop=None;label=None;rectangles=0;calls=[];events=[];pc_counts={}
 handoff_seen=False;call_seen=False
 def mark():return dict(instructions=count,writes=writes,code_sha256=ih.hexdigest(),write_sha256=wh.hexdigest())
 def code(uc,at,size,_):
  nonlocal count,rectangles,handoff_seen,call_seen
  if at==stop:uc.emu_stop();return
  pc_counts[at]=pc_counts.get(at,0)+1
  if at in TEXT_APIS:
   rows=text.get(label,[]);index=used.get(label,0);need(index<len(rows),'recorded original input endpoint at '+hex(at)+' in '+str(label))
   used[label]=index+1;apply_text(replay,rows[index],used,label);return
  need(at not in (0x424F80,0x4CE9C5,0x454E18) and not 0x41F732<=at<0x41F811,'terminal battle stage never enters a successor root or supplemental cleanup')
  need(at in e.ALLOWED and replay.read(at,size)==e.CODE[at-0x400000:at-0x400000+size] and e.CODE[at-0x400000]!=0xCC,'only finite unchanged original stage instruction '+hex(at)+' in '+str(label)+' after '+str(d.get('recent','')))
  if at==0x4998B0:
   need(uc.reg_read(x86.UC_X86_REG_ECX)==e.CTRL and staged_state(replay)['selector']==17,'original result dispatch after the stage word advances')
   calls.append(dict(entry=at,kind='dispatch',receiver=uc.reg_read(x86.UC_X86_REG_ECX),configuration=num(bytes(u.mem_read(uc.reg_read(x86.UC_X86_REG_ESP)+4,4)),0),result_type=staged_state(replay)['result_type']))
  if at==0x499910:
   need(uc.reg_read(x86.UC_X86_REG_ECX)==e.CTRL and staged_state(replay)['selector']==17,'original animation lifecycle only in stage17')
   s=staged_state(replay);calls.append(dict(entry=at,kind='animation',state=s['animation']['state'],progress=s['animation']['progress'],step=s['animation']['step'],held=s['held']))
  if at==0x49AD50:
   need(uc.reg_read(x86.UC_X86_REG_ECX)==e.CTRL and num(bytes(u.mem_read(uc.reg_read(x86.UC_X86_REG_ESP)+4,4)),0)==5 and staged_state(replay)['selector']==17,'original selected result transition type 5')
   calls.append(dict(entry=at,kind='transition',argument=5,state=staged_state(replay)['animation']['state']))
  if at==0x410310:rectangles+=1
  if at==0x454793:
   need(uc.reg_read(x86.UC_X86_REG_ECX)==e.CTRL and staged_state(replay)['selector']==20 and not call_seen and not handoff_seen,'only the original late-stage call instruction reaches 473860')
   call_seen=True
  if at==0x473860:
   s=staged_state(replay);sp=uc.reg_read(x86.UC_X86_REG_ESP)
   need(call_seen and num(bytes(u.mem_read(sp,4)),0)==0x454798 and uc.reg_read(x86.UC_X86_REG_ECX)==e.CTRL and not handoff_seen,'only the original 0x454793 result hand-off')
   handoff_seen=True;calls.append(dict(entry=at,kind='result_handoff',call_site=0x454793,return_address=num(bytes(u.mem_read(sp,4)),0),selector=s['selector']))
   events.append(dict(entry=at,kind='result_initialization',selector=s['selector'],before=s,before_CPU=replay.cpu()))
  count+=1;ih.update(struct.pack('<I',at))
 def write(uc,access,at,size,value,_):
  nonlocal writes
  need(not 0x400000<=at<0x593000,'original stage cannot mutate code or IAT')
  writes+=1;wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
 hc=u.hook_add(UC_HOOK_CODE,code);hw=u.hook_add(UC_HOOK_MEM_WRITE,write)
 try:
  for i,f in enumerate(frames):
   rectangles=0
   for j in range(f['segments'][0],f['segments'][1]):
    seg=segs[j]
    if j in bindings:bind_keyboard(replay,bindings[j])
    need(replay.cpu()==seg['before_CPU'],'segment begins at its recorded 57 CPU '+seg['label'])
    need(mark()==seg['local_before'],'segment-local digest/continuity before '+seg['label'])
    label=seg['label'];stop=seg['stop']
    if seg['root']:
     sp=e.STACK+0xF000;u.mem_write(sp,struct.pack('<I',e.RETURN))
     for k,a in enumerate(seg['root']['args']):u.mem_write(sp+4+4*k,struct.pack('<I',a))
     u.reg_write(x86.UC_X86_REG_ESP,sp);u.reg_write(x86.UC_X86_REG_ECX,seg['root']['receiver'])
    u.ctl_remove_cache(seg['entry'],seg['entry']+1)
    u.emu_start(seg['entry'],0,timeout=60_000_000,count=4_000_000)
    need(u.reg_read(x86.UC_X86_REG_EIP)==stop,'natural original stage segment '+seg['label'])
    if stop==e.RETURN:need(u.reg_read(x86.UC_X86_REG_ESP)==e.STACK+0xF004,'complete original stage stack '+seg['label'])
    need(replay.cpu()==seg['CPU'],'segment ends at its recorded 57 CPU '+seg['label'])
    need(mark()==seg['local_after'],'segment-local instruction/write digest '+seg['label'])
   need(f['rectangles']==rectangles,'exact 128 original result rectangle calls per countdown frame '+str(f['index']))
   capture_equal(replay,f['capture_after'],'frame '+str(f['index']))
   need(staged_state(replay)==f['after'],'frame '+str(f['index'])+' complete original state')
   need(staged_queue(replay)==f['queue_after'],'frame '+str(f['index'])+' complete original queue')
  need(all(used.get(k,0)==len(v) for k,v in text.items()),'every recorded input-platform call consumed once')
  need(calls==d['calls'],'exact original dispatch/animation/transition/natural hand-off call order')
  need(events==d['events'],'exact original 473860 entry state and 57 CPU')
 finally:u.hook_del(hc);u.hook_del(hw)
 stage_state_memory_equal(replay,d['final']['memory'],'complete final stage memory')
 need(replay.cpu()==d['final']['CPU'],'complete final stage 57 CPU')
 need(staged_state(replay)==d['final']['state'] and staged_queue(replay)==d['final']['queue'],'complete final stage state/queue')
 need(mark()==d['final']['local_trace'],'complete final stage-local digest')
 return dict(stage_segments=len(segs),stage_frames=len(frames),input_platform_calls=sum(len(v) for v in text.values()),result_rectangle_calls=214*128,original_call_events=len(calls),local_instructions=count,local_writes=writes,stage_pc_counts=pc_counts)

def source(row):
 need(e.EXTRA_RANGES==EXTRA_RANGES and e.NEW_MUTABLE==NEW_MUTABLE,'only the declared original late-stage extents and writes')
 need(e.RANGES==e.parent.RANGES+EXTRA_RANGES and e.ALLOWED==frozenset(a for lo,hi in e.RANGES for a in range(lo,hi)),'exactly derived original source guard extent')
 need(e.BattleStageMachine.source_code.__code__ is e.parent.TaskCompletionMachine.source_code.__code__,'unchanged original source instruction guard algorithm')
 need(e.SELECTOR_FRAMES==SELECTOR_FRAMES and sum(SELECTOR_FRAMES.values())==349,'original selector frame schedule')
 need(e.RESULT_TYPE_CONFIGURATION==RESULT_TYPE_CONFIGURATION and RESULT_TYPE_CONFIGURATION=={1:2,2:3,3:4,4:5,5:6} and e.RESULT_MODES==RESULT_MODES and RESULT_MODES=={1:0,2:1,3:1,4:2,5:2},'original result type configuration and mode words')
 need(e.TEXT_APIS==TEXT_APIS,'only the two accepted predecessor input endpoints')
 from capstone import Cs,CS_ARCH_X86,CS_MODE_32
 md=Cs(CS_ARCH_X86,CS_MODE_32);off=lambda a:a-0x400000
 expected={0x454293:('movsx','edx, byte ptr [ecx + 0x171]'),0x45429c:('je','0x4542b4'),0x4542a1:('mov','word ptr [eax + 0x108cc2], 0'),0x4542ad:('mov','dword ptr [ecx + 0x38], 0xf'),
   0x453F4D:('mov','word ptr [eax + 0x108cc2], 1'),0x4543F6:('mov','word ptr [edx + 0x108cc2], 1'),0x45442E:('mov','word ptr [eax + 0x108cc2], 0'),
  0x4112ad:('mov','eax, dword ptr [ebp - 4]'),0x4112b0:('add','eax, 0x890'),0x4112b5:('mov','dword ptr [ebp - 8], eax'),
  0x45444b:('mov','word ptr [0x7a4184], 0'),0x454470:('call','0x415040'),0x45447c:('add','cx, ax'),0x45448d:('cmp','edx, 0xff'),0x454493:('jl','0x454628'),
  0x45449f:('add','ecx, 1'),0x4544a5:('mov','dword ptr [edx + 0x38], ecx'),0x4544b4:('cmp','dword ptr [ebp - 0x18], 5'),
  0x4544c1:('jmp','dword ptr [edx*4 + 0x454816]'),0x4544dc:('push','2'),0x4544de:('mov','ecx, dword ptr [ebp - 4]'),
  0x4544e1:('add','ecx, 0x190'),0x4544e7:('call','0x4998b0'),0x4544ec:('mov','dword ptr [0x5ff720], 0'),0x454636:('call','0x499910'),
  0x45463b:('test','eax, eax'),0x45464b:('mov','dword ptr [ecx + 0x38], eax'),0x454653:('mov','word ptr [0x7a417c], 0x4ff'),
  0x454692:('cmp','dword ptr [ebp - 8], 0x40'),0x4546a6:('shl','edx, 4'),0x4546a9:('sub','ecx, edx'),0x45470b:('call','0x410310'),0x454748:('call','0x410310'),
  0x45475a:('call','0x415040'),0x454766:('sub','dx, ax'),0x454769:('mov','word ptr [0x7a417c], dx'),0x454779:('jge','0x45479f'),
  0x454793:('call','0x473860'),0x454798:('mov','eax, 1'),0x4547a1:('mov','eax, 1'),0x4547c1:('ret','')}
 for at,want in expected.items():
  i=next(md.disasm(e.CODE[off(at):off(at)+16],at));need((i.mnemonic,i.op_str)==want,'exact independently derived stage instruction '+hex(at))
 # Every reference to the sub-stage word in the whole original image is one of
 # those four word stores, and the only stored immediates are 0 and 1.
 word_sites=[0x400000+i for i in range(len(e.CODE)-3) if e.CODE[i:i+4]==b'\xc2\x8c\x10\x00']
 need(word_sites==[0x453F50,0x4542A4,0x4543F9,0x454431],'every original sub-stage word reference is one of the four decoded stores')
 for at in (0x453F4D,0x4542A1,0x4543F6,0x45442E):
  i=next(md.disasm(e.CODE[off(at):off(at)+12],at));need(i.mnemonic=='mov' and i.op_str.rsplit(', ',1)[1] in ('0','1'),'original sub-stage word store '+hex(at)+' writes only 0 or 1')
 need(e.CODE[off(0x454793):off(0x454798)]==b'\xe8'+struct.pack('<i',0x473860-0x454798) and e.CODE[off(0x454798):off(0x45479d)]==b'\xb8\x01\x00\x00\x00','original natural result call and return-one bytes')
 sites=[0x400000+i for i in range(len(e.CODE)-5) if e.CODE[i]==0xE8 and 0x400000+i+5==0x454798]
 need(sites==[0x454793],'the only original call returning to 0x454798 is the 0x454793 site')
 for lo,hi in EXTRA_RANGES:
  seq=list(md.disasm(e.CODE[off(lo):off(hi)],lo));need(seq,'declared original extent '+hex(lo))
  if lo==0x4116A4:need(seq[-1].mnemonic=='xor' and seq[-1].op_str=='eax, eax' and seq[-1].address+seq[-1].size==hi,'original keyboard transform tail')
  else:need(seq[0].mnemonic=='push' and seq[0].op_str=='ebp' and seq[-1].mnemonic=='ret' and seq[-1].address+seq[-1].size==hi,'whole original function extent '+hex(lo))
 selectors=(0x453F4A,0x453F77,0x454063,0x45413B,0x454266,0x454290,0x4542B9,0x4542EC,0x454310,0x454336,0x45435A,0x454380,0x45439D,0x4543E9,0x45441D,0x45444B,0x454468,0x45462D,0x454653,0x454670,0x4547A1)
 need(struct.unpack_from('<21I',e.CODE,off(0x4547C2))==selectors and e.CODE[off(0x4547C1)]==0xC3,'original 21-entry selector table')
 need(struct.unpack_from('<6I',e.CODE,off(0x454816))==(0x4544C8,0x4544DC,0x4544FB,0x45451A,0x454536,0x454552),'original result type table')
 types=(0x4544C8,0x4544DC,0x4544FB,0x45451A,0x454536,0x454552);derived={}
 for t in range(1,6):
  seq=list(md.disasm(e.CODE[off(types[t]):off(0x45459e)],types[t]))
  push=next(i for i in seq if i.mnemonic=='push');mode=next(i for i in seq if i.mnemonic=='mov' and '0x5ff720' in i.op_str)
  derived[t]=(int(push.op_str,0),int(mode.op_str.rsplit(', ',1)[1],0))
 need(derived=={1:(2,0),2:(3,1),3:(4,1),4:(5,2),5:(6,2)},'every original result type arm dispatch and mode word independently decoded')
 need({t:derived[t][0] for t in derived}==RESULT_TYPE_CONFIGURATION and {t:derived[t][1] for t in derived}==RESULT_MODES,'declared result dispatch equals the decoded original arms')
 need(struct.unpack_from('<6I',e.CODE,off(0x499B5D))==(0x49999D,0x4999CF,0x499A50,0x499ABE,0x499AFD,0x499B35),'original 499910 state table')
 timer={i.address:(i.mnemonic,i.op_str,i.size) for i in md.disasm(e.CODE[off(0x415040):off(0x415070)],0x415040)}
 need(timer[0x415040][:2]==('push','ebp') and timer[0x41505d][:2]==('mov','eax, dword ptr [ebp + 8]') and timer[0x415066][:2]==('ret','4') and 0x415066+timer[0x415066][2]==0x415069,'original 415040 naturally returns its single argument')
 for k in range(8):
  need(struct.unpack_from('<7h',e.CODE,off(0x59EAA4+k*0xE))[4]==0x200 and struct.unpack_from('<7h',e.CODE,off(0x59EAA4+k*0xE))[5]==(336 if k in (0,7) else 304),'original animation configuration table row '+str(k))
 for slot,target in ((0x5920EC,0x76182A80),(0x5922C4,0x770206E0)):
  need(struct.unpack_from('<I',e.CODE,off(slot))[0]==target,'original input IAT target '+hex(slot))
 need(e.CODE[off(0x425C94):off(0x425C99)]==bytes.fromhex('e8b1701400') and e.CODE[off(0x56CD4A):off(0x56CD50)]==bytes.fromhex('ff25ec205900'),'original IME query call and import thunk bytes')
 actions=derive_action_codes(md);declared={}
 for offset,value in e.ACTION_CODES:declared.setdefault(offset,set()).add(value)
 need(actions==declared,'every original action OR site independently decoded')
 return dict(original_instruction_checks=len(expected),selectors=list(selectors),result_types=derived,frames=TOTAL_FRAMES,rectangle_calls=214*128,text_APIs=sorted(TEXT_APIS.values()),keyboard_function=0x4113D5,battle_exit_consumer_executed=False)

def derive_action_codes(md):
 import re
 ins=list(md.disasm(e.CODE[0x4116A4-0x400000:0x411CE2-0x400000],0x4116A4));key=re.compile(r'^mov (al|cl|dl|bl), byte ptr \[[a-z0-9]+ \+ (0x[0-9a-f]+)\]$');bit=re.compile(r'^or (al|cl|dl|bl|ah|ch|dh|bh|eax|ecx|edx|ebx), (0x[0-9a-f]+|\d+)$')
 found={};pending=None
 for n in ins:
  text=n.mnemonic+' '+n.op_str;m=key.match(text)
  if m:
   d=int(m.group(2),16);pending=d if 0x480<=d<0x780 else None;continue
  if pending is not None and n.mnemonic=='or':
   o=bit.match(text);need(o is not None,'parsed original OR '+hex(n.address)+' '+text);reg,imm=o.group(1),int(o.group(2),0)
   value=imm.bit_length()-1+(8 if reg in ('ah','ch','dh','bh') else 0);offset=pending-0x480 if pending<0x680 else pending-0x680
   found.setdefault(offset,set()).add(value);pending=None
 need(len(found)==len({o for o,_ in e.ACTION_CODES}),'every declared action word has one original site')
 return found

def native(row,old=None):
 prior=previous_stage.native(row,old);platform=no_new_platform_calls(row,prior)
 d=row['terminal_battle_stage_handoff'];need(not d['terminal_battle_exit_executed'] and not d['rewards_or_school_executed'] and not d['terminal_presentation_complete'],'stage hand-off separated from battle exit, rewards and presentation')
 need(d['captures_used']==3 and d['frames_total']==349 and d['freeze_selector']==20 and d['freeze_EAX']==1,'exact bounded stage summary contract')
 return dict(parent=prior,no_new_platform_calls=platform,no_new_texture_or_GDI_creation=True,all_native_ownership_and_protocol_verified=True)

def final_summary(row):
 d=row['terminal_battle_stage_handoff'];memory=d['final']['memory'];t=e.terminal;s=expand(row['final_state']['terminal_state'],row['blobs'])
 want=dict(task=read(memory,e.TASK,0x190).hex(),records=[read(memory,t.RECORD+i*256,256).hex() for i in (0,1)],counters=read(memory,t.CTRL+0x2EF14,0x31).hex(),remaining=num(read(memory,t.CTRL+0x2E6F4,4),0,'i'),elapsed=num(read(memory,t.CTRL+0x2E6F8,4),0,'i'),result=read(memory,0x7F4000,0x2000).hex(),work=read(memory,t.WORK,3).hex(),VM=read(memory,e.VM,0x9400).hex(),units=[read(memory,p,0x520).hex() for p in (t.UNIT,t.TARGET)])
 need(s==want,'all final terminal summary pages equal independently verified full memory')
 return True

class Replay(previous_stage.Replay):
 """Accepted parent lifetime with the original writable .data mode-word page.

 Only 0x5FF720..0x5FF724 is accepted as mutable by the source contract; the
 page itself is writable in the original .data section.  The page is exposed at
 exactly the source machine's point: after the complete accepted parent
 lifetime has been replayed and compared, at the first original stage segment.
 Exposing it in __init__ would split the common RX image mapping and change the
 recorded region partition of the accepted parent captures.
 """
 def __init__(self,row,refs=None):
  super().__init__(row,refs)


def verify_case(row,old=None):
 old=accepted_case_witness()[row['input']['name']] if old is None else old;d=row['terminal_battle_stage_handoff']
 # The immediate parent of this stage is the accepted task completion case, whose
 # own summary captured the exact boundary this stage starts from.  Its row-level
 # receipts also contain the accepted change's later supplementary original
 # cleanup (38 more CRT API receipts and 12 more GPU/CRT wires), which this stage
 # must not consume, so the full boundary comparison is the summary final capture
 # plus the receipt kinds that cleanup does not append to.
 fixed=old['final']
 need(all(d['before'][k]==fixed[k] for k in ('memory','CPU','queue','trace')),'stage-before equals the accepted task completion final capture')
 need(all(d['prefix'][k]==old['counts'][k] for k in ('task_APIs','task_calls','task_writes','APIs')),'stage boundary equals the accepted task completion receipt counts')
 # The reused parent guards were written against the accepted script exit case;
 # task completion's own prefix is the boundary captured before its final task
 # leaves, so it has to be given that ancestor rather than the task completion case.
 base=previous_stage.parent_case(row)
 prefix_trace(row);p_source=previous_stage.source(row);p_protocol=previous_stage.protocol(row)
 replay=Replay(row);parent_counts=previous_stage.execute_with_events(replay)
 stage_state_memory_equal(replay,d['before']['memory'],'complete stage-before memory after independent parent replay')
 need(replay.cpu()==d['before']['CPU'],'stage-before 57 CPU after independent parent replay')
 need(staged_state(replay)==d['before']['state'] and staged_queue(replay)==d['before']['queue'],'stage-before state/queue after independent parent replay')
 # The original entry-hit counter is cumulative.  Every entry the accepted
 # parent recorded stays exactly as recorded, but the 349 original frames also
 # enter the result audio-play body, which no earlier stage reached.  The
 # independent stage execution records how often it entered every original PC;
 # each accepted parent count must survive unchanged and each addition must be
 # exactly the number of times this independent replay entered that PC.  The
 # reused parent guards then receive the exact accepted boundary view.
 timing=protocol(row);provenance=source(row);counts=execute_stage(replay)
 pc_counts=counts.pop('stage_pc_counts')
 added={k:int(v)-int(old['entries'].get(k,0)) for k,v in row['entries'].items() if int(v)!=int(old['entries'].get(k,0))}
 need(all(v>0 for v in added.values()),'accepted parent entry counts only grow during the original result stage')
 need(all(pc_counts.get(int(k,16),0)==v for k,v in added.items()),'every added original entry is entered exactly by the independent stage execution')
 boundary=dict(row);boundary['entries']=old['entries']
 p_native=previous_stage.native(row,base);prior=previous_stage.prefix(boundary,base,replay=False)
 counts['stage_entry_hits']=added
 platform=native(row,base)
 need(row['pending_CPU']==d['final']['CPU'] and row['image_before']==row['image_after'],'all57 final CPU and original code/IAT unchanged')
 need((row['instructions'],row['writes'],row['code_trace_sha256'],row['write_trace_sha256'])==tuple(d['final']['trace'][k] for k in ('instructions','writes','code_sha256','write_sha256')),'all original cumulative source fields')
 equal(row['final'],d['final']['memory'],'complete final mapped memory');checked=final_summary(row)
 summary=dict(full_cumulative=d['final']['trace'],mapped_regions=len(d['final']['memory']),CPU_registers=len(d['final']['CPU']),complete_tasks=(760 if row['input']['name']=='neutral_running' else 787)+2,pending_tasks=0,live_textures=sum(r['alive'] for r in row['terminal_task_completion']['resources']),new_textures=[],task_phase=6,result_type=d['result_type'],result_configuration=d['result_configuration'],animation_mode=d['animation_mode'])
 return dict(name=row['input']['name'],prefix=prior,parent_source=p_source,parent_protocol=p_protocol,parent_native=p_native,parent_replay=parent_counts,source=provenance,timing=timing,added=counts,native=platform,forward_summary=summary,current_terminal_summary_pages_equal_verified_final_memory=checked,whole_memory_CPU_original_events_and_trace_verified=True,terminal_battle_stage_handoff_executed=True,terminal_battle_exit_executed=False,rewards_complete=False)

def fresh_case(case,ch,gh,ticks):
 need(ticks==accepted_case_witness()[case['name']]['ticks'],'fresh original fixed clock input');return e.run_case(case,ch,gh,ticks)


def stream_report(path):
 """Yield the leading members, each case row once, then the remaining members.

 The report stays a single JSON object; only one case row is held at a time, so
 the independent verification never needs both complete native rows in memory.
 """
 path=Path(path);opener=gzip.open if path.suffix=='.gz' else open;stream=opener(path,'rt',encoding='utf8');decoder=StreamingJSON(stream)
 try:
  need(decoder.take()=='{','report JSON object');members={};decoder.whitespace()
  if decoder.peek()=='}':decoder.take()
  else:
   while True:
    key=decoder.string();decoder.whitespace();need(decoder.take()==':','report member colon')
    if key=='cases':
     yield 'header',dict(members)
     decoder.whitespace();need(decoder.take()=='[','report cases array');decoder.whitespace()
     if decoder.peek()!=']':
      while True:
       row=decoder.value();yield 'case',row;del row
       # Long immutable strings are pooled only to share identical values inside
       # the case that owns them; dropping the pool lets the completed row go.
       decoder.pool.clear()
       decoder.whitespace();end=decoder.take()
       if end==']':break
       need(end==',','report case separator');decoder.whitespace()
     else:decoder.take()
    else:members[key]=decoder.value()
    decoder.whitespace();end=decoder.take()
    if end=='}':break
    need(end==',','report member separator');decoder.whitespace()
  yield 'footer',members
 finally:stream.close()


def verify(path):
 witness=accepted_case_witness();corpus=e.overlay.parent.corpus();helpers=e.helpers('terminal-battle-stage-handoff-proof');rows=[];observed=set();index=0
 stream=stream_report(path)
 try:
  kind,members=next(stream);need(kind=='header' and members.get('schema_version')==1,'report schema before its cases')
  declared=members.get('source_contract');need(declared is not None,'declared full source contract')
  need(Path(members['helper_build']['GPU']['source']).as_posix()=='tools/terminal_followup_d3d8_platform.cs' and members['helper_build']['GPU']['source_sha256']==e.helper_contract()['current']['sha256'] and members['helper_build']['GPU']['machine']==0x14C,'same bounded x86 native helper')
  writes=declared['new_mutable'];need(all(w['start']==a and w['end']==b for w,(a,b) in zip(writes,NEW_MUTABLE)),'declared stage mutable extents')
  lists={tuple(w['write_PCs']) for w in writes};need(len(lists)==1,'one declared late-stage write PC list')
  pcs=list(lists.pop());need(pcs==sorted(set(pcs)) and all(pc in e.ALLOWED for pc in pcs),'every observed late-stage write PC is one of the declared original extents')
  need(any(pc in range(0x454290,0x4542b4) for pc in pcs) and any(pc in range(0x45444b,0x4547c2) for pc in pcs),'selector and timer writes originate in the original 453F10 body')
  independent=copy.deepcopy(declared)
  for w in independent['new_mutable']:w['write_PCs']=[]
  need(independent==e.source_contract(),'full source contract')
  footer=None
  for kind,item in stream:
   if kind=='footer':footer=item;break
   row=item;del item;need(index<len(corpus) and row['input']==corpus[index],'both selected source cases in corpus order')
   old=witness[row['input']['name']];proof=verify_case(row,old);other=None
   try:
    other=fresh_case(row['input'],helpers[0],helpers[1],old['ticks']);verify_case(other,old)
    for key in ('initial','final'):equal(row[key],other[key],'fresh entire '+key+' memory')
    for key in ('pending_CPU','instructions','writes','code_trace_sha256','write_trace_sha256','cleanup_steps','cleanup_state','resource_initialization','world_frames','events','commands','task_calls','task_writes','admission'):need(row[key]==other[key],'fresh all cumulative and original boundary '+key)
    for key in ('terminal_battle_stage_handoff',):need(guest(row[key])==guest(other[key]),'fresh whole current stage '+key)
   except Exception as error:
    if other is not None:
     name='analysis/terminal-battle-stage-handoff-diagnostic-fresh-'+row['input']['name']+'-20261031-'+str(time.time_ns())+'.json.gz';e.save_source(name,dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(ROOT).as_posix()),error=str(error),fresh_original_case=other));print('full fresh failure preserved locally',name,flush=True)
    raise
   observed.update(w['pc'] for w in row['terminal_battle_stage_handoff']['writes'])
   proof.update(current_native_resources_recreated=True,complete_cumulative_digests_reproduced_by_new_full_original_instance=True);rows.append(proof);print('independent battle stage',row['input']['name'],'all current original lifetimes verified',flush=True);del row,old,other;gc.collect();index+=1
  need(index==len(corpus) and footer is not None,'both selected source cases')
  need(footer.get('R3_complete') is False and footer.get('R4_complete') is False and footer.get('R5_complete') is False and footer.get('R6_complete') is False,'declared unresolved R3..R6 boundaries')
  need(sorted(observed)==pcs,'declared write PCs equal every observed original stage write')
 finally:stream.close()
 return dict(schema_version=1,source_report=e.terminal.ref(path.relative_to(ROOT).as_posix()),implementation_sha256={p:sha((ROOT/p).read_bytes()) for p in IMPLEMENTATIONS},cases=rows,whole_current_native_protocol_independently_verified=True,current_native_resources_recreated=True,complete_cumulative_digests_reproduced=True,cumulative_digest_reconstructed=False,historical_cleanup_projection=False,terminal_battle_stage_handoff_executed=True,terminal_battle_exit_executed=False,new_OS_input=False,draw_or_Present=False,terminal_presentation_complete=False,rewards_complete=False,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable battle stage proof');e.terminal.save(a.out,verify(ROOT/a.report))
