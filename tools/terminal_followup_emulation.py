"""Original terminal confirmation, second role and following dialogue resources."""
import argparse,copy,gc,hashlib,json,struct,time,types
from functools import lru_cache
import unicorn.x86_const as x86
from tools import terminal_panel_dialogue_emulation as parent
from tools import terminal_overlay_emulation as overlay
from tools import terminal_name_emulation as name
from tools import terminal_dialogue_emulation as dialogue
from tools import school_retained_keyboard as keyboard
from tools.school_retained_name_corpus import source_names
from tools.school_retained_portrait_file_catalog import parse
from tools.school_font_raster_catalog import geometry

ROOT,CODE,need,sha,terminal,MAIN,VM,STACK,RETURN,TASK,INPUT,MANAGER=(getattr(parent,n) for n in ('ROOT','CODE','need','sha','terminal','MAIN','VM','STACK','RETURN','TASK','INPUT','MANAGER'))
KEYBOARD=parent.parent.KEYBOARD;EXTRA_RANGES=((0x4C4EB0,0x4C4F23),)
RANGES=parent.RANGES+EXTRA_RANGES;ALLOWED=frozenset(a for lo,hi in RANGES for a in range(lo,hi))
REFERENCE=types.FunctionType(parent.REFERENCE.__code__,dict(parent.REFERENCE.__globals__,RANGES=RANGES))
PARENT_ACCEPTANCE='analysis/terminal-panel-dialogue-acceptance-v1-20261027.json'
PARENT_ACCEPTANCE_SHA='ac1937ef900d1ebb2bae5d70ca60f6ea7ae0949e8fc093af867fb6fcea27beab'
PARENT_SOURCE='analysis/terminal-panel-dialogue-source-v1-20261026.json.gz'
PARENT_SOURCE_SHA='d2be32fc2c14d47f4824aa456956c568f7cf86bc9adbf6b8a3207a692074edd3'
PARENT_PROOF='analysis/terminal-panel-dialogue-proof-v2-20261027.json'
PARENT_PROOF_SHA='7f1a8df210b6cc9fe7bbff76a8756000d083faba79543671d75c8b2c65082f7b'
NAME_NODE=VM+0x6F60+4*0xE0;NAME_RECORD=NAME_NODE+0x60
OLD_TEXT_RECORD=VM+0x430+5*0xAB8+0x28
NAME_RASTER=0x3E800000;TEXT_RASTER=0x3E900000;RASTER_LIMIT=0x100000
GDI=dict(name.GDI);QUERIES=(0x4C61C0,0x4C4DC0,0x4C4EB0,0x4CC600,0x4CC0F0,0x4CC3E0,0x4CC810,0x4CA770,0x4CA9B0,0x4CBF90,0x4CDE10,0x407870,0x403730,0x4CABD0,0x4128F0,0x4CD350,0x4CD402,0x4CD432)

@lru_cache(maxsize=1)
def fixed_parents():
 a=parent.file_ref(PARENT_ACCEPTANCE,PARENT_ACCEPTANCE_SHA);s=parent.file_ref(PARENT_SOURCE,PARENT_SOURCE_SHA);p=parent.file_ref(PARENT_PROOF,PARENT_PROOF_SHA)
 accepted=json.loads((ROOT/PARENT_ACCEPTANCE).read_text(encoding='utf8'))
 need(accepted['source_report']==s and accepted['independent_proof']==p and accepted['tasks_complete']==3 and accepted['boundaries']['VM_PC_per_case']==[156,168] and accepted['boundaries']['VM_wait']==1,'accepted complete layer7 group and new confirmation')
 return dict(acceptance=a,source=s,proof=p)

@lru_cache(maxsize=1)
def fixed_parent_times():
 # This is exactly the frozen parent's provider; the latest large source is not
 # decoded a second time just to recover unchanged clock method inputs.
 fixed_parents();return parent.fixed_parent_times()

def branch(name):
 need(name in ('neutral_running','timeout_before_combat'),'one original terminal followup branch')
 win=name=='neutral_running';layer=4 if win else 5
 return dict(first_PC=156 if win else 168,role=1 if win else None,configuration=7 if win else 8,layer=layer,object=VM+0x430+layer*0xAB8,node=VM+0x6F60+layer*0xE0,text_index=2 if win else 4,text_PC=184 if win else 180,ready_PC=194 if win else 190,final_PC=198 if win else 194,scene_capture=76 if win else 77)

def helper_contract():
 old=ROOT/'tools/terminal_portrait_d3d8_platform.cs';new=ROOT/'tools/terminal_followup_d3d8_platform.cs';a=old.read_bytes();b=new.read_bytes()
 expected=a.replace(b'retired.Contains(key) || resources.ContainsKey(key)',b'resources.ContainsKey(key)').replace(b'retired or duplicate texture address; new session required',b'duplicate live texture address')
 need(a!=expected and b==expected,'only new helper retired-address policy changes; original helper remains frozen')
 return dict(original=dict(path=old.relative_to(ROOT).as_posix(),sha256=sha(a)),current=dict(path=new.relative_to(ROOT).as_posix(),sha256=sha(b)),only_retired_native_address_reuse_allowed=True,duplicate_live_address_still_rejected=True,capacity_and_ABI_unchanged=True)

class FollowupMachine(parent.PanelDialogueMachine):
 source_code=types.FunctionType(parent.PanelDialogueMachine.source_code.__code__,dict(parent.PanelDialogueMachine.source_code.__globals__,ALLOWED=ALLOWED,REFERENCE=REFERENCE))
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.followup_active=self.followup_ready=self.followup_cleaning=False;self.followup_stop=None
  self.fu_segments=[];self.fu_frames=[];self.fu_leaves=[];self.fu_commands=[];self.fu_writes=[];self.fu_queries=[];self.fu_bindings=[];self.fu_gpu=[];self.fu_calls=[];self.fu_conversions=[];self.fu_resources=[];self.fu_live={};self.fu_observers=[];self.fu_cleanup=[];self.fu_replacements=[]
  self.fu_count=self.fu_write_count=0;self.fu_ih=hashlib.sha256();self.fu_wh=hashlib.sha256();self.fu_current=None;self.fu_pending_release=None;self.fu_copy_rows=[]
 def fu_mark(self):return dict(instructions=self.fu_count,writes=self.fu_write_count,code_sha256=self.fu_ih.hexdigest(),write_sha256=self.fu_wh.hexdigest())
 def fu_capture(self,full=True):
  memory=self.snapshot() if full else [dict(pointer=a,bytes=b-a+1,sha256=sha(self.read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()]
  return dict(memory=memory,CPU=self.cpu(),state=self.task_state(),queue=self.queue_state(),trace=self.mark(),local_trace=self.fu_mark())
 def fu_prefix_counts(self):
  return dict(CRT_APIs=len(self.crt_apis),CRT_wire=len(self.live.trace),resource_steps=len(self.resource_steps),task_APIs=len(self.task_APIs),task_calls=len(self.task_calls),task_writes=len(self.task_writes),APIs=len(self.api_trace),extra_counts=copy.deepcopy(dict(self.extra_counts)),GPU_wire=len(self.gpu.trace),GDI_trace=len(self.name_platform.trace),GDI_stages=len(self.name_platform.service.stages),overlay_commands=len(self.overlay_commands))
 def fu_seed_resources(self):
  old=[('GYBC','GYBC',self.image_record,self.texture,self.texture_native,self.lock,self.upload,self.readback),('name5','name',name.TEXTURE,self.name_texture,self.name_native,self.name_lock,self.name_upload,self.name_readback),('portrait32','portrait',self.portrait_record,self.portrait_texture,self.portrait_native,self.portrait_lock,self.portrait_upload,self.portrait_readback),('text5','text',OLD_TEXT_RECORD,self.dialogue_texture,self.dialogue_native,self.dialogue_lock,self.dialogue_upload,self.dialogue_readback)]
  old += [('text7_'+str(s['text_index']),'text',s['record'],s['texture'],s['native_pointer'],s['lock'],bytes.fromhex(s['upload_hex']),s['readback']) for s in self.pd_sentences]
  for label,kind,record,t,native,lock,upload,readback in old:
   matches=[(i,x) for i,x in enumerate(self.gpu.trace) if x['request']['op']=='create' and x['reply']['result']['texture']['pointer']==native]
   need(len(matches)==1 and self.get(record+44)==t['pointer'],'one current original prefix texture lifetime');i,x=matches[0]
   r=dict(label=label,kind=kind,generation=i+1,record=record,texture=copy.deepcopy(t),native_pointer=native,create_wire_index=i,release_wire_index=None,alive=True,size=[x['request']['width'],x['request']['height']],lock=copy.deepcopy(lock),upload_hex=(upload if isinstance(upload,str) else upload.hex()),readback=copy.deepcopy(readback),created_phase='prefix')
   need(t['pointer'] not in self.fu_live,'one live generation per current guest texture');self.fu_resources.append(r);self.fu_live[t['pointer']]=r
 def fu_observe(self,label):
  rows=[]
  for r in self.fu_resources:
   if not r['alive']:continue
   wire=len(self.gpu.trace);b=self.gpu.readback(r['native_pointer']);need(b['hex']==r['upload_hex'],'all current live texture bytes retained '+r['label'])
   row=dict(label=label,generation=r['generation'],record=r['record'],wire_index=wire,result=b);self.fu_observers.append(row);rows.append(copy.deepcopy(row))
  return rows
 def fu_set_raster(self,address):
  need(address in (NAME_RASTER,TEXT_RASTER),'finite new real DIB destinations');service=self.name_platform.service;fn=service.call_raster
  service.call_raster=types.MethodType(types.FunctionType(fn.__func__.__code__,dict(fn.__func__.__globals__,RASTER=address)),service)
 def fu_prepare(self,kind,label,record,raster=None):
  need(self.fu_current is None and kind in ('name','portrait','text'),'finite sequential original followup resource')
  r=dict(kind=kind,label=label,record=record,created_phase='forward',alive=False)
  if raster is not None:r['raster_address']=raster;self.fu_set_raster(raster)
  self.fu_current=r;return r
 def fu_gdi(self,target):
  r=self.fu_current;need(r is not None and r['kind'] in ('name','text'),'GDI only for current original followup text resource')
  slot=self.gdi_targets[target];nm,caller,pop=GDI[slot];sp=self.getreg('ESP');ret=self.get(sp)
  if nm=='CreateFontA':caller=0x4CA7CB if r['kind']=='name' else 0x4CAD09
  need(caller is None or ret==caller,'exact original followup GDI caller '+nm);args=[self.get(sp+4+j) for j in range(0,pop,4)]
  wire=len(self.name_platform.trace);row=self.name_platform.call(self,nm,args,ret);row.update(import_slot=slot,target=target,sp=sp,return_va=ret,pop=pop,value=row['result'],GDI_trace_index=wire)
  if nm=='CreateDIBSection':need(row['guest_bits']==r['raster_address'] and row['mapped_bytes']<=RASTER_LIMIT,'current real separately mapped DIB');self.mutable.append((row['guest_bits'],row['guest_bits']+row['mapped_bytes']))
  self.fu_calls.append(row);self.fu_leaves.append(dict(kind='GDI',call=copy.deepcopy(row),resource_label=r['label']));self.return_api(sp,row['result'],pop)
 def api_crt(self,slot):
  if not self.followup_ready:return super().api_crt(slot)
  original=self.crt.api
  if self.followup_active and self.fu_branch['role'] is not None and slot==0x5921EC:
   fn=overlay.CrtGuest.api;self.crt.api=types.MethodType(types.FunctionType(fn.__code__,dict(fn.__globals__,RESOURCE_NAME=self.fu_role_path),closure=fn.__closure__),self.crt)
  try:super().api_crt(slot)
  finally:self.crt.api=original
  self.fu_leaves.append(dict(kind='CRT',call=copy.deepcopy(self.crt_apis[-1]),phase='forward' if self.followup_active else 'cleanup'))
 def gpu_api(self,at):
  if not self.followup_ready:return super().gpu_api(at)
  slot=self.methods[at];pop={80:32,56:12,64:20,68:8,8:4}[slot];sp=self.getreg('ESP');bp=self.getreg('EBP');ret=self.get(sp);args=[self.get(sp+4+j) for j in range(0,pop,4)];wire=len(self.gpu.trace);outputs=[];phase='forward' if self.followup_active else 'cleanup'
  need(ret=={80:0x403C8A,64:0x40395E,68:0x4039D3,8:0x40378D}.get(slot,ret) and (slot!=56 or ret in (0x403CBE,0x403A44)),'original actual current followup COM caller')
  def put(p,b):self.map_new(p,len(b));self.uc.mem_write(p,b);outputs.append(dict(pointer=p,hex=b.hex()))
  if slot==80:
   r=self.fu_current;need(self.followup_active and r is not None and not r.get('texture'),'one original current resource CreateTexture')
   if r['kind']=='portrait':w,h=256,512
   else:
    cfg=geometry(self.name_platform.service.measured);w,h=[1<<(v-1).bit_length() for v in cfg['texture_size']];r['geometry']=cfg
   need(args==[self.device_ptr,w,h,1,0,25,1,r['record']+44] and self.get(r['record']+44)==0,'original source-derived followup texture record and full CreateTexture ABI')
   native=self.gpu.create(w,h);result=self.space.result('overlay',native);t=result['texture'];r.update(texture=t,native_pointer=native['texture']['pointer'],generation=wire+1,create_wire_index=wire,release_wire_index=None,alive=True,size=[w,h]);need(t['pointer'] not in self.fu_live,'native address reuse only after prior lifetime release');self.fu_live[t['pointer']]=r;self.fu_resources.append(r)
   self.map_identity(t);self.methods.update({p:int(k) for k,p in t['methods'].items()});put(args[-1],struct.pack('<I',t['pointer']));op='create'
  else:
   need(args[0] in self.fu_live,'current live texture generation only');r=self.fu_live[args[0]];t=r['texture'];need(r['alive'] and self.get(r['record']+44)==t['pointer'],'current record still owns selected texture generation');p=r['native_pointer']
   if slot==56:
    need(args==[t['pointer'],0,bp-(52 if ret==0x403CBE else 36)],'original descriptor destination');native=self.gpu.describe(p);result=copy.deepcopy(native);put(args[-1],bytes.fromhex(result['hex']));op='describe'
   elif slot==64:
    need(self.followup_active and r is self.fu_current and args==[t['pointer'],0,self.get(bp+8),0,2048] and 'lock' not in r,'original new texture LockRect ABI');native=self.gpu.lock(p);result=self.space.result('overlay',native);r['lock']=result;raw=bytes.fromhex(result['hex']);put(result['bits'],raw);self.mutable.append((result['bits'],result['bits']+len(raw)));put(args[2],struct.pack('<II',result['pitch'],result['bits']));op='lock'
   elif slot==68:
    need(self.followup_active and r is self.fu_current and args==[t['pointer'],0] and 'upload_hex' not in r,'original new texture UnlockRect ABI');raw=self.read(r['lock']['bits'],len(bytes.fromhex(r['lock']['hex'])));r['upload_hex']=raw.hex();native=self.gpu.unlock(p,raw);result=copy.deepcopy(native);op='unlock'
    observer=len(self.gpu.trace);r['readback']=self.gpu.readback(p);need(r['readback']['hex']==raw.hex(),'all actual uploaded followup texels');r['readback_wire_index']=observer;self.fu_observers.append(dict(label='unlock_'+r['label'],generation=r['generation'],record=r['record'],wire_index=observer,result=copy.deepcopy(r['readback'])))
   else:
    need(args==[t['pointer']],'original actual Release receiver');native=self.gpu.release(p);result=copy.deepcopy(native);r.update(alive=False,release_wire_index=wire,released_phase=phase);del self.fu_live[t['pointer']];op='release'
    for s in self.pd_sentences:
     if s['texture']['pointer']==t['pointer'] and s['record']==r['record']:s['alive']=False
  value=result['count'] if slot==8 else result['hr'];need(value==0,'actual followup COM operation succeeds')
  row=dict(generation=r['generation'],record=r['record'],resource_kind=r['kind'],resource_label=r['label'],wire_index=wire,phase=phase,slot=slot,target=at,sp=sp,return_va=ret,args=args,pop=pop,value=value,op=op,native_result=native,result=result,memory_outputs=outputs,actual_API_executed=True)
  self.fu_gpu.append(row);self.fu_leaves.append(dict(kind='GPU',call=copy.deepcopy(row),phase=phase))
  # Only compatibility receipts for the actual current late roots are appended.
  # Frozen predecessor forward copies and their native ownership are untouched.
  if phase=='cleanup':
   if self.panel_dialogue_cleaning:self.pd_gpu.append(copy.deepcopy(row))
   elif self.dialogue_cleaning:self.dialogue_gpu.append(copy.deepcopy(row))
   elif self.portrait_cleaning:self.portrait_gpu.append(copy.deepcopy(row))
   elif self.name_cleaning:self.name_gpu.append(copy.deepcopy(row))
   elif r['label']=='GYBC':self.gpu_calls.append(copy.deepcopy(row))
  self.return_api(sp,value,pop)
 def write_hook(self,uc,access,at,size,value,context):
  super().write_hook(uc,access,at,size,value,context)
  if self.followup_active:
   if getattr(self,'fu_keyboard_fragment',False):need(KEYBOARD<=at and at+size<=KEYBOARD+0xA00 or STACK<=at and at+size<=STACK+0x20000,'finite original followup keyboard writes')
   self.fu_write_count+=1;self.fu_wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
   if VM<=at<VM+0x9400 or KEYBOARD<=at<KEYBOARD+0xA00 or TASK<=at<TASK+0x190 or at==0:self.fu_writes.append(dict(pc=self.getreg('EIP'),address=at,bytes=size,value=value&((1<<min(size*8,64))-1)))
 def code(self,uc,at,size,context):
  active=self.followup_active
  if active:
   if at==self.followup_stop:uc.emu_stop();return
   if self.fu_pending_release and at==self.fu_pending_release['caller'] and self.getreg('ESP')==self.fu_pending_release['return_ESP']:
    q=self.fu_pending_release;need(self.get(q['record']+44)==0 and not self.fu_resources[q['ledger_index']]['alive'],'original forward destructor clears retired record');q['after']=self.fu_capture();q['GPU_APIs']=copy.deepcopy(self.fu_gpu[q.pop('GPU_start'):]);self.fu_replacements.append(q);self.fu_pending_release=None
   if at==0x403730:
    record=self.getreg('ECX');pointer=self.get(record+44);sp=self.getreg('ESP')
    if pointer in self.fu_live and self.get(sp)==0x4051AE:
     r=self.fu_live[pointer];need(self.fu_branch['role'] is None and r['label']=='text5' and record==OLD_TEXT_RECORD,'only original old layer5 text forward replacement');self.fu_pending_release=dict(entry=at,caller=self.get(sp),return_ESP=sp+4,record=record,generation=r['generation'],ledger_index=self.fu_resources.index(r),before=self.fu_capture(),GPU_start=len(self.fu_gpu))
   if at==0x4CE9C5:
    p=self.get(VM+16)+self.get(VM+28);op,n=struct.unpack('<HH',self.read(p,4));need(self.get(VM+28)<self.fu_branch['final_PC'],'next confirmation successor stays unexecuted');self.fu_commands.append(dict(PC=self.get(VM+28),opcode=op,bytes=n,source_pointer=p))
   if at in overlay.parent.APIS and self.get(self.getreg('ESP'))==overlay.parent.APIS[at][2]:
    sp=self.getreg('ESP');ret=self.get(sp);first=len(self.task_APIs);super().code(uc,at,size,context);need(len(self.task_APIs)==first+1,'one actual current followup task leaf');r=self.task_APIs[-1];self.fu_leaves.append(dict(kind='TASK',call=dict(r,sp=sp,return_va=ret,pop=4,value=r['result'],memory_outputs=[],new_mappings=[])));return
   if at in self.gdi_targets:self.fu_gdi(at);return
   if at==0x405869:
    sp=self.getreg('ESP');args=[self.get(sp+j) for j in range(0,24,4)];self.fu_conversions.append(dict(entry=at,args=args,resource_label=self.fu_current['label'],record=self.fu_current['record'],rect=list(struct.unpack('<4I',self.read(args[4],16))),point=list(struct.unpack('<2I',self.read(args[5],8)))))
   if at==0x56D4D0 and self.get(self.getreg('ESP'))==0x40483F:
    sp=self.getreg('ESP');args=[self.get(sp+4+j) for j in (0,4,8)];i=len(self.fu_copy_rows);r=self.fu_current;need(r is not None and r['kind']=='portrait' and i<512 and args==[r['lock']['bits']+i*r['lock']['pitch'],self.fu_file_pointer+24+i*512,512],'all original new SC001 memcpy row arguments');self.fu_copy_rows.append(dict(row=i,args=args,caller=0x40483F))
   if at in QUERIES:
    sp=self.getreg('ESP');self.fu_queries.append(dict(entry=at,CPU=self.cpu(),receiver=self.getreg('ECX'),stack_hex=self.read(sp,68).hex(),selected_layer=self.get(VM+0x1CC,'B'),nodes={str(i):self.read(VM+0x6F60+i*0xE0,0xE0).hex() for i in (4,5,7)},objects={str(i):self.read(VM+0x430+i*0xAB8,0xAB8).hex() for i in (4,5,7)}))
  super().code(uc,at,size,context)
  if active and at in ALLOWED:self.fu_count+=1;self.fu_ih.update(struct.pack('<I',at))
 def fu_segment(self,label,entry,stop=RETURN,root=None,kind='task'):
  before=self.cpu();trace=self.mark();local=self.fu_mark();first=len(self.fu_leaves)
  if root:
   sp=STACK+0xF000;self.put(sp,RETURN)
   for j,a in enumerate(root['args']):self.put(sp+4+j*4,a)
   self.uc.reg_write(x86.UC_X86_REG_ESP,sp);self.uc.reg_write(x86.UC_X86_REG_ECX,root['receiver'])
  self.followup_stop=stop;self.uc.ctl_remove_cache(entry,entry+1);self.uc.emu_start(entry,0,timeout=60_000_000,count=4_000_000);self.followup_stop=None
  need(self.getreg('EIP')==stop,'natural original followup segment '+label)
  if stop==RETURN:need(self.getreg('ESP')==STACK+0xF004,'complete original followup task stack')
  row=dict(label=label,kind=kind,entry=entry,stop=stop,root=root,before_CPU=before,CPU=self.cpu(),trace_before=trace,trace_after=self.mark(),local_before=local,local_after=self.fu_mark(),leaves=[first,len(self.fu_leaves)]);self.fu_segments.append(row);return row
 def fu_frame(self,phase,stop=RETURN):
  i=len(self.fu_frames);before=self.task_state();queue=self.queue_state();first=len(self.fu_segments)
  for label,entry,recv in (('heads',0x40DB90,MANAGER),('arena',0x40DC80,MANAGER),('input',0x425DE0,INPUT),('task',0x454CF0,TASK)):
   self.fu_segment(label+'_'+str(i),entry,stop if label=='task' else RETURN,dict(receiver=recv,args=[]))
  row=dict(index=i,phase=phase,before=before,after=self.task_state(),queue_before=queue,queue_after=self.queue_state(),segments=[first,len(self.fu_segments)],capture=self.fu_capture(False),complete=stop==RETURN);self.fu_frames.append(row)
  print(self.live_input['name'],'followup',phase,i,self.get(VM+28),self.get(VM+32,'H'),flush=True);return row
 def fu_resume_frame(self,phase,callback):
  i=len(self.fu_frames)-1;row=self.fu_frames[i];need(not row['complete'],'only currently pending original task can continue');callback();need(self.getreg('EIP')==RETURN and self.getreg('ESP')==STACK+0xF004,'same original task naturally returns after resources')
  row.update(phase=phase,after=self.task_state(),queue_after=self.queue_state(),segments=[row['segments'][0],len(self.fu_segments)],capture=self.fu_capture(False),complete=True)
 def fu_captured(self,capture):
  index=len(self.fu_bindings);scene=self.fu_branch['scene_capture'];stream=parent.parent.input_contract()['streams'][str(scene)]
  need(index<3 and capture==stream['captures'][index],'new independent cycle uses exact accepted raw sample sequence')
  raw=bytes.fromhex(capture['raw_device_hex']);need(len(raw)==256,'entire original current keyboard raw sample');before=self.read(KEYBOARD,0xA00);bound=bytearray(before);bound[12:268]=raw;cpu=self.cpu();trace=self.mark();local=self.fu_mark();self.uc.mem_write(KEYBOARD+12,raw);bp=STACK+0xF800;self.put(bp-4,KEYBOARD)
  for key,value in dict(EBP=bp,ESP=bp-0x70,EFLAGS=0x202).items():self.uc.reg_write(getattr(x86,'UC_X86_REG_'+key),value)
  self.fu_keyboard_fragment=True
  try:step=self.fu_segment('followup_captured_'+capture['label'],0x4113D5,0x4116A4,kind='keyboard')
  finally:self.fu_keyboard_fragment=False
  step['bound_CPU']=step['before_CPU'];step['before_CPU']=cpu;after=self.read(KEYBOARD,0xA00);need(after==keyboard.predict_keyboard(bytes(bound)),'independent entire original new-cycle A00 keyboard output')
  result=dict(cycle='followup_confirmation',capture=copy.deepcopy(capture),before_CPU=cpu,trace_before=trace,local_before=local,before_hex=before.hex(),bound_hex=bound.hex(),after_hex=after.hex(),only_device_output_written=dict(pointer=KEYBOARD+12,bytes=256),fragment=dict(va=0x4113D5,bp=bp,sp=bp-0x70,receiver_slot=bp-4,receiver=KEYBOARD,stop=0x4116A4),segment_index=len(self.fu_segments)-1,after=self.fu_capture());self.fu_bindings.append(result);return result
 def fu_font(self,r):
  need(self.getreg('EIP')==self.font_target,'natural current followup font entry');sp=self.getreg('ESP');caller=0x4CA7CB if r['kind']=='name' else 0x4CAD09
  r['font_boundary']=self.fu_capture();r['pending_font']=dict(entry=self.font_target,caller=self.get(sp),args=[self.get(sp+4+j*4) for j in range(14)],CPU=self.cpu(),first_instruction_executed=False);need(self.get(sp)==caller,'natural source-derived name/text font caller')
  r['first_calls']=len(self.fu_calls);r['first_gpu']=len(self.fu_gpu);r['first_conversion']=len(self.fu_conversions);r['first_GDI']=len(self.name_platform.trace);r['first_stage']=len(self.name_platform.service.stages);r['first_leaf']=len(self.fu_leaves)
  self.fu_segment(r['label']+'_font_and_raster',self.font_target,0x403BD0);s=self.name_platform.service
  r['raster']=dict(self.fu_capture(),measured=copy.deepcopy(s.measured),selected_face=s.face,ACP=s.gdi.acp,raster_hex=s.gdi.raster(s.bitmap).hex(),stages=copy.deepcopy(s.stages[r['first_stage']:]),calls=copy.deepcopy(self.fu_calls[r['first_calls']:]))
 def fu_finish_resource(self,r):
  r.update(calls=copy.deepcopy(self.fu_calls[r.pop('first_calls',len(self.fu_calls)):]),GPU_APIs=copy.deepcopy(self.fu_gpu[r.pop('first_gpu',len(self.fu_gpu)):]),conversions=copy.deepcopy(self.fu_conversions[r.pop('first_conversion',len(self.fu_conversions)):]),GDI_trace=copy.deepcopy(self.name_platform.trace[r.pop('first_GDI',len(self.name_platform.trace)):]),leaves=[r.pop('first_leaf',len(self.fu_leaves)),len(self.fu_leaves)])
  r.pop('first_stage',None);need(r['alive'],'new resource remains alive at original completion');r['retained_readbacks']=self.fu_observe(r['label']+'_complete');self.fu_current=None
 def fu_role(self):
  r=self.fu_prepare('name','name4',NAME_RECORD,NAME_RASTER);self.fu_frame('role30_to_name_font',self.font_target);self.fu_font(r);self.fu_segment('new_name_texture_to_IMAGE',0x403BD0,0x4CDE10);r['completion']=self.fu_capture();sp=self.getreg('ESP');args=[self.get(sp+4),self.get(sp+8)];side=self.get(NAME_NODE+0x32,'B')
  # The actual helper-independent side getter is also retained in query records;
  # both candidate group words and the actual IMAGE argument remain explicit.
  pending=dict(entry=0x4CDE10,receiver=self.getreg('ECX'),caller=self.get(sp),args=args,CPU=self.cpu(),first_instruction_executed=False,node_hex=self.read(NAME_NODE,0xE0).hex(),group_words=[self.get(NAME_NODE+0x40,'H'),self.get(NAME_NODE+0x42,'H')],side_byte=side,side_pointer=NAME_NODE+0x32,side_getter=0x4CA9B0,path=self.string(args[0]).decode('ascii'))
  need(pending['receiver']==VM and pending['caller']==0x4CC0D2 and pending['group_words']==[30,31] and side in (0,1) and args[1]==pending['group_words'][side] and pending['path']==self.fu_role_path,'actual original side-derived layer4 IMAGE slot and SC001 path');self.fu_image_group=args[1];self.fu_role_record=dict(role=1,configuration=7,node=NAME_NODE,name_record=NAME_RECORD,pending_image=pending,source=self.fu_role_source,name_resource_label=r['label']);self.fu_finish_resource(r)
  q=self.fu_prepare('portrait','portrait'+str(self.fu_image_group),0);q['first_gpu']=len(self.fu_gpu);q['first_leaf']=len(self.fu_leaves);self.fu_segment('new_SC001_file_and_constructor',0x4CDE10,0x403BD0);q['record']=self.get(MAIN+0x844+self.fu_image_group*8);read_api=next(x['call'] for x in self.fu_leaves[q['first_leaf']:] if x['kind']=='CRT' and x['call']['name']=='ReadFile');self.fu_file_pointer=read_api['args'][1];need(self.read(self.fu_file_pointer,len(self.fu_asset))==self.fu_asset,'complete actual original SC001 file')
  native=[]
  for p,b in self.crt.allocations.items():
   if p<=self.fu_file_pointer<p+b['bytes'] or p<=q['record']<p+b['bytes']:
    self.crt.sync(p);reply=self.live.request('readback',pointer=b['native']);need(reply['hex']==self.read(p,b['bytes']).hex(),'actual entire new SC001/vector native buffer');native.append(dict(guest=p,bytes=b['bytes'],wire_index=len(self.live.trace)-1,result=reply))
  q['constructed']=dict(self.fu_capture(),file_pointer=self.fu_file_pointer,file_hex=self.fu_asset.hex(),record=q['record'],record_hex=self.read(q['record'],84).hex(),bank_hex=self.read(MAIN+0x844+self.fu_image_group*8,8).hex(),native_allocation_readbacks=native,allocations=copy.deepcopy(self.crt.allocations));self.fu_segment('new_SC001_pixels_free_IMAGE_return',0x403BD0,0x4CC0D2);q['image_return']=self.fu_capture();q['copy_rows']=copy.deepcopy(self.fu_copy_rows);need(len(q['copy_rows'])==512,'all new SC001 rows originally copied');self.fu_segment('new_role_handler_complete_task',0x4CC0D2);q['completion']=self.fu_capture();self.fu_finish_resource(q);self.fu_resume_frame('role30_complete',lambda:None)
  need(self.get(VM+28)==176,'original role30 advances full twenty-byte command')
  for _ in range(200):
   if self.get(VM+32,'H')==0:break
   self.fu_frame('role_readiness');need(self.get(VM+28)==176,'only original new role readiness before176')
  else:raise ValueError('bounded new layer4 original role readiness')
  self.fu_role_record['ready']=self.fu_capture();self.fu_frame('select_layer4');need(self.get(VM+28)==184 and self.get(VM+0x1CC,'B')==4,'original config7 selects layer4')
 def fu_text(self):
  b=self.fu_branch;r=self.fu_prepare('text','followup_text',b['object']+0x28,TEXT_RASTER);r.update(text_index=b['text_index'],PC=b['text_PC'],object=b['object'],node=b['node'],record_index=0)
  need(self.get(b['object']+22,'H')==0,'original new or cleared target text count is zero');self.fu_frame('text_to_font',self.font_target);self.fu_font(r);self.fu_segment('followup_text_pixels_handler_complete_task',0x403BD0);r['completion']=self.fu_capture();need(self.get(VM+28)==b['text_PC']+6 and self.get(b['object']+22,'H')==1,'original full followup text task and count');self.fu_finish_resource(r);self.fu_resume_frame('followup_text_complete',lambda:None)
 def admission(self):
  a=super().admission();self.fu_branch=branch(self.live_input['name']);self.fu_prefix=self.fu_prefix_counts();self.fu_before=self.fu_capture();need((self.get(VM+28),self.get(VM+32,'H'))==(self.fu_branch['first_PC'],1),'accepted complete parent waiting boundary')
  self.fu_seed_resources();self.fu_resources_before=copy.deepcopy(self.fu_resources);self.followup_ready=self.followup_active=self.active_overlay=True
  if self.fu_branch['role'] is not None:
   catalog,_=source_names();self.fu_role_source=catalog['roles']['1'];self.fu_role_path='data\\adv\\bin\\'+self.fu_role_source['filename'];self.fu_asset=(ROOT/self.fu_role_source['image_path']).read_bytes();need(sha(self.fu_asset)==self.fu_role_source['image_sha256'],'fixed actual SC001');self.fu_role_container=parse(self.fu_asset)
  stream=parent.parent.input_contract()['streams'][str(self.fu_branch['scene_capture'])];self.fu_captured(stream['captures'][0])
  for _ in range(2):
   self.fu_frame('held_parent_confirmation');need((self.get(VM+28),self.get(VM+32,'H'),self.get(KEYBOARD+0x4B9,'B'))==(self.fu_branch['first_PC'],1,0),'current idle keeps parent confirmation')
  self.fu_captured(stream['captures'][1]);self.fu_frame('captured_press');need((self.get(VM+28),self.get(VM+32,'H'),self.get(KEYBOARD+0x4B9,'B'))==(self.fu_branch['first_PC'],0,128),'original task consumes new cycle captured press');confirmed=self.fu_capture();self.fu_captured(stream['captures'][2]);need(self.get(KEYBOARD+0x4B9,'B')==0,'original new-cycle release')
  clear=None
  if self.fu_branch['role'] is not None:self.fu_role()
  else:
   self.fu_frame('select_layer5');need(self.get(VM+28)==176 and self.get(VM+0x1CC,'B')==5,'original config8 selects layer5');before=self.fu_capture();wire=len(self.gpu.trace);self.fu_frame('clear_layer5_text');need(self.get(VM+28)==180 and self.get(self.fu_branch['object']+22,'H')==0 and len(self.gpu.trace)==wire and self.get(OLD_TEXT_RECORD+44)==self.dialogue_texture['pointer'],'original44 clears count without releasing old texture');clear=dict(before=before,after=self.fu_capture(),GPU_wire_before=wire,GPU_wire_after=len(self.gpu.trace))
  self.fu_text()
  for _ in range(100):
   self.fu_frame('text_readiness');need(self.get(VM+28)==self.fu_branch['ready_PC'],'only original50 before new confirmation')
   if self.get(VM+32,'H')==0:break
  else:raise ValueError('bounded current followup text readiness')
  ready=self.fu_capture();self.fu_frame('enter_new_confirmation');need((self.get(VM+28),self.get(VM+32,'H'))==(self.fu_branch['final_PC'],1),'natural original next confirmation')
  confirmation=self.fu_capture()
  for _ in range(2):
   self.fu_frame('held_new_confirmation');need((self.get(VM+28),self.get(VM+32,'H'),self.get(KEYBOARD+0x4B9,'B'))==(self.fu_branch['final_PC'],1,0),'two full tasks hold new confirmation without input')
  final=self.fu_capture();observations=self.fu_observe('final');self.followup_active=self.active_overlay=False
  for r in self.fu_resources:r['alive_after_forward']=r['alive']
  self.fu_result=dict(prefix=self.fu_prefix,before=self.fu_before,branch=self.fu_branch,resources_before=self.fu_resources_before,resources=copy.deepcopy(self.fu_resources),bindings=self.fu_bindings,confirmed=confirmed,clear=clear,role=copy.deepcopy(getattr(self,'fu_role_record',None)),role_container=getattr(self,'fu_role_container',None),ready=ready,confirmation=confirmation,final=final,segments=self.fu_segments,frames=self.fu_frames,leaves=self.fu_leaves,commands=self.fu_commands,writes=self.fu_writes,queries=self.fu_queries,replacements=self.fu_replacements,GPU_APIs=self.fu_gpu,calls=self.fu_calls,conversions=self.fu_conversions,readbacks=observations,readback_observers=self.fu_observers,GDI_trace=copy.deepcopy(self.name_platform.trace[self.fu_prefix['GDI_trace']:]),GDI_handle_projection=self.name_platform.space.ledger(),accounting=self.get(0x765720))
  self.fu_result.update(forward_wire_end=len(self.gpu.trace),CRT_forward_wire_end=len(self.live.trace))
  return a
 def fu_actual_root(self,label,entry,args=(),receiver=0,cdecl=False):
  before=self.fu_capture();first=len(self.fu_leaves);first_gpu=len(self.fu_gpu);first_crt=len(self.crt_apis)
  # Reuse the frozen root wrapper itself. All callee bodies remain original and
  # the source-code code object still supplies instruction/write guards.
  result=overlay.OverlayMachine.resource_root(self,label,entry,args,receiver,cdecl);after=self.fu_capture()
  self.fu_cleanup.append(dict(label=label,entry=entry,args=list(args),receiver=receiver,cdecl=cdecl,before=before,after=after,leaves=[first,len(self.fu_leaves)],GPU_APIs=copy.deepcopy(self.fu_gpu[first_gpu:]),CRT_APIs=copy.deepcopy(self.crt_apis[first_crt:])))
  return result
 def resource_root(self,label,*args,**kwargs):
  if not self.followup_ready:return super().resource_root(label,*args,**kwargs)
  if label!='supplemental_original_group20_destructor':return self.fu_actual_root(label,*args,**kwargs)
  if self.fu_branch['role'] is not None:
   self.fu_actual_root('supplemental_original_followup_text_destructor',0x403730,receiver=self.fu_branch['object']+0x28)
   self.fu_actual_root('supplemental_original_followup_portrait_container_destructor',0x41F4E0,[self.fu_image_group],MAIN+0x844)
   self.fu_actual_root('supplemental_original_followup_name_destructor',0x403730,receiver=NAME_RECORD)
  # Preserve the predecessor's root order and compatibility metadata using the
  # actual new boundary. No old CPU/hash or cleanup-state view is manufactured.
  self.panel_dialogue_cleaning=True
  try:
   for s in reversed(self.pd_sentences):
    first=len(self.pd_gpu);before=self.pd_capture();self.fu_actual_root('supplemental_original_panel_dialogue_line_'+str(s['text_index'])+'_destructor',0x403730,receiver=s['record']);after=self.pd_capture();need(not s['alive'] and self.get(s['record']+44)==0,'actual current old layer7 record released once');self.pd_cleanup.append(dict(text_index=s['text_index'],record=s['record'],before=before,after=after,GPU_APIs=copy.deepcopy(self.pd_gpu[first:]),record_hex=self.read(s['record'],0x68).hex(),accounting=self.get(0x765720)))
  finally:self.panel_dialogue_cleaning=False
  self.dialogue_cleaning=True;first=len(self.dialogue_gpu);before=self.cpu()
  try:self.fu_actual_root('supplemental_original_dialogue_texture_destructor',0x403730,receiver=OLD_TEXT_RECORD)
  finally:self.dialogue_cleaning=False
  self.dialogue_cleanup=dict(GPU_APIs=copy.deepcopy(self.dialogue_gpu[first:]),texture_bytes=self.get(0x765720),record_hex=self.read(OLD_TEXT_RECORD,0x68).hex(),before_CPU=before,CPU=self.cpu())
  self.portrait_cleaning=True;first=len(self.portrait_gpu)
  try:self.fu_actual_root('supplemental_original_portrait_container_destructor',0x41F4E0,[32],MAIN+0x844)
  finally:self.portrait_cleaning=False
  self.portrait_cleanup=dict(GPU_APIs=copy.deepcopy(self.portrait_gpu[first:]),texture_bytes=self.get(0x765720),game_bytes=self.get(0x79FC74),bank_hex=self.read(MAIN+0x844+32*8,8).hex(),old_CRT_cleanup_start=len(self.crt_apis))
  self.name_cleaning=True;first=len(self.name_gpu)
  try:self.fu_actual_root('supplemental_original_name_texture_destructor',0x403730,receiver=name.TEXTURE);self.name_cleanup=dict(GPU_APIs=copy.deepcopy(self.name_gpu[first:]),texture_bytes=self.get(0x765720),GDI=self.name_platform.close())
  finally:self.name_cleaning=False
  return self.fu_actual_root(label,*args,**kwargs)
 def run(self):
  r=super().run();need(not self.fu_live and all(not x['alive'] for x in self.fu_resources),'every old/new current texture lifetime originally released');r.update(terminal_followup=self.fu_result,followup_cleanup=self.fu_cleanup,followup_resources_after_cleanup=copy.deepcopy(self.fu_resources));return r

def source_contract():
 return dict(parent=parent.source_contract(),fixed_predecessor=fixed_parents(),branches={n:branch(n) for n in ('neutral_running','timeout_before_combat')},keyboard=KEYBOARD,raw_device_offset=12,raw_device_bytes=256,new_capture_cycle=True,captured_inputs=parent.parent.input_contract(),first_confirmation_released=True,next_confirmation_released=False,forward_roots=[0x40DB90,0x40DC80,0x425DE0,0x454CF0],new_VM_or_handler_roots=0,derived_input_host_writes=0,PC_or_wait_host_writes=0,new_OS_input=False,draw_or_Present=False,new_rasters=[NAME_RASTER,TEXT_RASTER],helper=helper_contract(),extra_code=[dict(start=a,end=b,sha256=sha(CODE[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES])

def helpers(prefix='terminal-followup'):
 helper_contract();a,aa=overlay.platform.build(ROOT/'tools/terminal_portrait_crt_platform.cs',prefix+'-crt');b,bb=overlay.platform.build(ROOT/'tools/terminal_followup_d3d8_platform.cs',prefix+'-gpu');return a,b,dict(CRT=aa,GPU=bb)

def run_case(c,ch,gh,ticks=None):
 fixed=fixed_parent_times()[c['name']]
 if ticks is None:ticks=list(fixed)
 need(ticks==fixed,'exact frozen parent original clock stream');instances=[]
 class Attached(FollowupMachine):
  def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);instances.append(self)
 class Diagnostics:
  @staticmethod
  def save(path,data):
   if instances:
    m=instances[0];data['followup']=dict(active=m.followup_active,segments=m.fu_segments,frames=m.fu_frames,leaves=m.fu_leaves,resources=m.fu_resources,bindings=m.fu_bindings,commands=m.fu_commands,queries=m.fu_queries,replacements=m.fu_replacements,CRT_trace=copy.deepcopy(m.live.trace),GPU_trace=copy.deepcopy(m.gpu.trace),GDI_trace=copy.deepcopy(m.name_platform.trace),readback_observers=m.fu_observers,memory=m.snapshot(),trace=m.mark(),local_trace=m.fu_mark())
   return terminal.save(path.replace('terminal-overlay-diagnostic-','terminal-followup-diagnostic-').replace('.json.gz','-20261027.json.gz'),data)
 fn=types.FunctionType(overlay.run_case.__code__,dict(overlay.run_case.__globals__,OverlayMachine=Attached,terminal=Diagnostics),closure=overlay.run_case.__closure__)
 return fn(c,ch,gh,ticks)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case',type=int);p.add_argument('--helper-prefix',default='terminal-followup');a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable followup report');fixed_parent_times();ch,gh,b=helpers(a.helper_prefix);rows=[]
 for c in (overlay.parent.corpus() if a.case is None else [overlay.parent.corpus()[a.case]]):rows.append(run_case(c,ch,gh));print('followup source',c['name'],'new confirmation held',flush=True)
 terminal.save(a.out,dict(schema_version=1,source_contract=source_contract(),helper_build=b,cases=rows,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False))
