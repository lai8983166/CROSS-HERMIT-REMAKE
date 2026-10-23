"""Independent full opening instructions, captured controls, native glyphs and natural resource retirement."""
import copy,gzip,json,struct,types,hashlib
from collections import Counter
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from tools import school_retained_opening as work
from tools import school_retained_role9_verification as previous
from tools import school_retained_third_dialogue_verification as text
from tools import school_retained_third_confirmation_verification as keycheck
from tools import school_retained_image_return_verification as imagecheck
from tools.school_gdi_platform import WindowsGDI
from tools.school_font_raster_catalog import geometry,convert_surface
from tools.school_d3d8_platform import machine
from functools import lru_cache

ROOT=work.ROOT;base=work.base;need=work.need;word=work.word;sha=work.sha;canonical=work.canonical
RETURN=work.RETURN
fourth_protocol=work.adapt(previous.previous.protocol,[("e['accounting_after_cleanup']==e['accounting_before']","e['accounting_after_cleanup']==e['accounting_before']-65536")])
fourth_proxy=types.SimpleNamespace(**dict(vars(previous.previous),protocol=fourth_protocol))
fourth_proxy.verify_case=types.FunctionType(previous.previous.verify_case.__code__,dict(previous.previous.verify_case.__globals__,protocol=fourth_protocol),'verify_changed_fourth_retirement_protocol')
parent_protocol=work.adapt(previous.protocol,[("e['accounting_after_cleanup']==e['accounting_before']","e['accounting_after_cleanup']==e['accounting_before']-73728"),("e['game_bytes_after_cleanup']==e['game_bytes_before']","e['game_bytes_after_cleanup']==e['game_bytes_before']")],previous=fourth_proxy)

def ordered(e):
 rows=[s for f in e['frames'] for s in f['steps']]+[b['step'] for b in e['bindings']]
 return rows

def protocol(c):
 parent_protocol(c);e=c['opening'];need(e['contract']==work.contracts(),'all opening parent/script/text/source pins');need(e['new_VM_roots']==e['PC_or_wait_host_writes']==0 and e['new_OS_input']is False,'no new VM/control or OS input writes');need(len(e['frames'])==222 and len(e['bindings'])==4,'whole 222-task opening and two captured press/release pairs');need((e['before']['PC'],e['before']['wait'],e['final']['PC'],e['final']['wait'],e['final']['opcode'])==(332,0,492,0,19),'natural script terminal without advancing past opcode19');need([f['label'] for f in e['frames']]==['frame_'+str(i) for i in range(222)],'all consecutive complete source tasks')
 for f in e['frames']:
  need(len(f['steps'])==4,'every complete original request/two resets/task')
  for s,va,recv in zip(f['steps'],(0x425de0,0x40db90,0x40dc80,0x454cf0),(work.task.INPUT,work.task.MANAGER,work.task.MANAGER,work.task.TACT)):text.previous.root_check(s,va,recv)
 need(e['GPU_exit']==0 and e['GPU']==dict(texture_releases=[],device_release_count=0,factory_release_count=0,window_destroyed=True,all_owned_resources_released=True),'source glyph releases then normal helper/device/window cleanup');need(len(e['fonts'])==len(e['textures'])==len(e['supplemental_cleanup'])==6 and all(t['live'] and t['phase']==4 for t in e['textures']) and all(not t['live'] and t['phase']==6 for t in e['textures_after_cleanup']),'retained glyphs then explicit original destruction');need(all(g==dict(fonts=0,bitmaps=0,dcs=1,all_resources_released=True) for g in e['GDI']),'source glyph GDI deletion and supplemental owned measurement DCs');need(e['GPU_trace'][-1]['reply']['result']==e['GPU'],'actual final GPU close receipt')
 for i,t in enumerate(e['GPU_trace'],1):need(t['request']['id']==t['reply']['id']==i and t['reply']['ok']is True,'every current native request/reply')
 h=e['GPU_hello'];need(h['pointer_bytes']==4 and h['window_visible']is False and h['sdk']==220 and machine(h['runtime_path'])==0x14c and sha((ROOT/h['runtime_path']).read_bytes())==h['runtime_sha256'],'current hidden x86 D3D8 runtime');need(e['GPU_build']['machine']==0x14c and e['GPU_build']['source_sha256']==work.previous.previous.contracts()['GPU_source_sha256'],'pinned original current GPU helper source');need(all('full_memory' in s and 'architectural_cpu' in s and 'queue' in s for s in ordered(e)+e['supplemental_cleanup']),'every source interval retains complete provenance');need([x['request']['op'] for x in e['GPU_trace']]==['create','describe','lock','unlock','readback']*6+['describe','release']*6+['close'],'six entire source uploads/readbacks then explicit destruction');need([(b['capture']['label'],b['state']['PC']) for b in e['bindings']]==[('press',366),('release',366),('press',416),('release',416)],'both original captured confirmation pairs in source order')
 need(e['parent_GPU_calls']==[a for f in e['frames'] for s in f['steps'] for a in s['result']['api_calls'] if a.get('kind') in ('recorded_third_GPU_only','actual_owned_fourth_GPU','recorded_opening_historical_GPU')],'all and only natural older-resource COM calls');need(len(e['parent_GPU_calls'])==6 and e['natural_parent_texture_bytes_retired']==73728,'six natural parent retirement calls and full 32K second-text extent')
 need(bytes.fromhex(e['before']['vm_header_hex'])[4:6]==b'\x01\x01' and bytes.fromhex(e['final']['vm_header_hex'])[4:6]==bytes(2),'original opcode19 clears both active channel bytes')

class PrefixReady(Exception):
 def __init__(self,replay):self.replay=replay

class Replay(previous.Replay):
 prefix_role=work.adapt(previous.Replay.role9_extension,[("need(e['image_cleanup']['root']==", "self.prefix_ready();need(e['image_cleanup']['root']==")])
 def prefix_ready(self):
  self.prefix_verified_memory=base.memory_rows(self.u);self.prefix_verified_cpu=base.architectural_cpu(self.u);print('independent prefix ready',self.case['name'],self.case['scene_capture'],flush=True);raise PrefixReady(self)
 def role9_extension(self):return self.prefix_role()
 def source_step(self,s):
  maps=[]
  for slot in work.dialogue.IMPORTS:
   at=word(self.read(slot))
   if not any(a<=at<=b for a,b,_ in self.u.mem_regions()):lo=at&~4095;self.u.mem_map(lo,4096);maps.append(dict(pointer=lo,bytes=4096))
  need(maps==s['entry_mappings'],'only independently derived missing platform pages');a=s['result'];root=s['root']
  if root:
   self.u.mem_write(root['sp'],struct.pack('<'+'I'*(len(root['args'])+1),root['return_va'],*root['args']))
   for k,v in dict(EIP=root['va'],ESP=root['sp'],ECX=root['receiver'],EFLAGS=0x202).items():self.u.reg_write(base.REGISTERS[k],v)
  need(self.cpu()==a['before_cpu'],'whole source CPU before each opening interval');calls=iter(a['api_calls']);pending=next(calls,None);ih=hashlib.sha256();wh=hashlib.sha256();counts=Counter();writes=0;display=[];conversions=[];decoded=[]
  def code(u,at,n,_):
   nonlocal pending
   if at==a['boundary']:u.emu_stop();return
   if pending and at==pending['target']:
    q=dict(pending,va=at,key='opening_platform');kind=q.get('kind')
    if kind=='actual_opening_GDI':self.gdi(q)
    elif kind=='actual_opening_GPU':self.gpu(q)
    elif kind=='actual_role9_GPU':self.retire_role9(q)
    elif kind=='actual_owned_fourth_GPU':self.native_gpu(q)
    elif kind=='recorded_third_GPU_only':text.Replay.third_gpu(self,q)
    elif kind=='recorded_GPU_only':imagecheck.Replay.api(self,q)
    elif kind=='recorded_opening_historical_GPU':self.historical(q)
    else:need(kind in (None,'actual_opening_CRT','actual_role9_CRT','recorded_task_platform'),'only declared current/historical platform leaves');self.api(q)
    pending=next(calls,None);return
   need(base.BASE<=at<0x592000 and self.read(at,n)==self.image[at-base.BASE:at-base.BASE+n],'every immutable original opening instruction byte');counts[at]+=1;ih.update(struct.pack('<I',at)+self.read(at,n))
   if at in work.dialogue.DISPLAY:display.append(dict(va=at,receiver=self.cpu()['ECX'],return_va=word(self.read(self.cpu()['ESP']))))
   if at==0x405869:
    sp=self.cpu()['ESP'];args=[word(self.read(sp+j)) for j in range(0,24,4)];conversions.append(dict(va=at,args=args,lock_hex=self.read(args[1],8).hex(),rect=list(struct.unpack('<4I',self.read(args[4],16))),point=list(struct.unpack('<2I',self.read(args[5],8)))))
   if at==0x4ce9c5:
    pc=word(self.read(work.VM+28));p=word(self.read(self.cpu()['EBP']-8));op,size=struct.unpack('<2H',self.read(p,4));decoded.append(dict(PC=pc,opcode=op,size=size,pointer=p,hex=self.read(p,size).hex()))
  def write(u,access,at,n,value,_):
   nonlocal writes
   need(not base.BASE<=at<0x592000,'no original code patch');writes+=1;wh.update(struct.pack('<IIQ',at,n,value&0xffffffffffffffff))
  ch=self.u.hook_add(UC_HOOK_CODE,code);wr=self.u.hook_add(UC_HOOK_MEM_WRITE,write)
  try:self.u.ctl_remove_cache(a['before_cpu']['EIP'],a['before_cpu']['EIP']+1);self.u.emu_start(a['before_cpu']['EIP'],0,count=2000000,timeout=120000000)
  finally:self.u.hook_del(ch);self.u.hook_del(wr)
  need(pending is None and self.cpu()==a['cpu'] and ih.hexdigest()==a['instruction_sha256'] and [dict(va=p,count=n) for p,n in sorted(counts.items())]==a['instruction_counts'],'all independently executed original instructions/APIs and natural CPU return');need(writes==a['writes'] and wh.hexdigest()==a['write_sha256'] and display==s['display_calls'] and conversions==s['conversions'] and decoded==s.get('decoded',[]),'every source write, display, conversion and actual opcode fetch');need(base.memory_rows(self.u)==s['full_memory'] and canonical(base.architectural_cpu(self.u))==canonical(s['architectural_cpu']),'all current source mappings and full architectural CPU');need(work.dialogue.text_state(self)==s['state'] and work.previous.crt.old.ledger(self)==s['ledger'],'whole source state and allocator ledger');b=self.read(work.task.MANAGER,96);head=word(b,16);arena=word(b,20);end=word(b,48);need(word(b,8)==4096 and word(b,12)==1048576 and arena<=end<=arena+1048576 and s['queue']==dict(manager_hex=b.hex(),head_pointer=head,head_hex=self.read(head,32768).hex(),arena_pointer=arena,used_bytes=end-arena,arena_hex=self.read(arena,end-arena).hex()),'every source queue head/tail and live draw record')
  if 'opening_state' in s:need(work.state(self)==s['opening_state'],'full opening role/layer/control state')
  if 'role_state' in s:need(work.previous.state(self)==s['role_state'],'whole supplemental original role state')
  return sum(counts.values())
 def gdi(self,a):
  if a.get('kind')!='actual_opening_GDI':return text.Replay.gdi(self,a)
  i=a['font_index'];need(0<=i<len(self.opening_case['fonts']),'source font index');f=self.opening_case['fonts'][i];proxy=types.SimpleNamespace(**dict(vars(work.dialogue),RASTER=f['raster'],rules=types.SimpleNamespace(source_rules=lambda:dict(text=work.contracts()['texts'][i]))));need(f['index']==i and f['raster']==0x39000000+i*0x100000 and f['return_va']==0x4cad09,'independent font scope/raster/caller')
  if i not in self.opening_refs:
   redraw=types.FunctionType(text.reproduce_pixels.__code__,dict(text.reproduce_pixels.__globals__,work=proxy),'independent_remaining_source_glyph');self.opening_refs[i]=redraw(dict(third_dialogue=dict(raster=f['raster_record']),pending_font=dict(args=f['font_args'])) )
  ref=self.opening_refs[i];old=(self.third_case,self.reference,self.case);self.third_case=dict(raster=f['raster_record']);self.reference=ref;self.case=dict(self.case,pending_font=dict(args=f['font_args'],frames=f['frames']));call=types.FunctionType(text.Replay.gdi.__code__,dict(text.Replay.gdi.__globals__,work=proxy),'independent_remaining_GDI_ABI')
  if a['name']=='CreateFontA':need(self.cpu()==f['cpu'] and work.previous.chain(self,[('font',0x4c4d04),('text',0x4cec2b),('VM',0x454d90),('task',RETURN)])==f['frames'],'all natural source font CPU and four frames')
  try:return call(self,a)
  finally:self.third_case,self.reference,self.case=old
 def gpu(self,a):
  e=self.opening_case;i=self.opening_gpu_count;need(a['index']==i,'all source opening COM calls ordered');slot=a['slot'];pop={80:32,56:12,64:20,68:8,8:4}[slot];sp=self.cpu()['ESP'];bp=self.cpu()['EBP'];ret=word(self.read(sp));args=[word(self.read(sp+4+j)) for j in range(0,pop,4)];obj=a['object_index'];phase=a['phase'];need(0<=obj<len(e['textures']) and 0<=phase<6 and slot==[80,56,64,68,56,8][phase] and a['sp']==sp and a['pop']==pop and a['return_va']==ret==[0x403c8a,0x403cbe,0x40395e,0x4039d3,0x403a44,0x40378d][phase] and a['args']==args,'full original opening COM ABI and caller');trace=e['GPU_trace'][a['native_wire_index']];request=trace['request'];native=trace['reply']['result'];need(a['native_result']==native and request==dict(id=a['native_wire_index']+1,op=a['native_op'],**a['native_request']),'exact current native request/reply bound to source');out=[];maps=[]
  def put(p,b):out.append(dict(pointer=p,hex=b.hex()))
  if phase==0:
   need(obj==len(self.opening_objects),'consecutive source owned glyph objects');f=e['fonts'][obj];cfg=self.opening_refs[obj]['cfg'];w,h=[1<<(v-1).bit_length() for v in cfg['texture_size']];record=args[7]-44;need(a['target']==self.device_method and a['native_op']=='create' and a['native_request']==dict(width=w,height=h,levels=1,usage=0,format=25,pool=1) and args==[self.device,w,h,1,0,25,1,record+44] and record==e['textures'][obj]['record'],'source geometry, device and destination');result=self.opening_space.result('opening',native);t=result['texture'];r=dict(index=obj,font_index=obj,record=record,width=w,height=h,texture=t,native_pointer=native['texture']['pointer'],phase=0,live=True);need(all(x['native_pointer']!=r['native_pointer'] for x in self.opening_objects),'no current object address reused');self.opening_objects.append(r)
   for p in (t['pointer'],t['vtable'],*t['methods'].values()):
    lo=p&~4095
    if not any(a<=lo<=b for a,b,_ in self.u.mem_regions()) and (lo,4096) not in maps:maps.append((lo,4096))
   put(t['pointer'],struct.pack('<I',t['vtable']))
   for k,p in t['methods'].items():put(t['vtable']+int(k),struct.pack('<I',p))
   put(args[7],struct.pack('<I',t['pointer']))
  else:
   r=self.opening_objects[obj];t=r['texture'];p=r['native_pointer'];need(r['phase']==phase and r['live'] and a['target']==t['methods'][str(slot)],'same live source glyph owner/phase/method')
   if phase in (1,4):
    need(args==[t['pointer'],0,bp-(52 if phase==1 else 36)] and a['native_op']=='describe' and a['native_request']==dict(pointer=p),'original glyph descriptor destination');result=copy.deepcopy(native);need(bytes.fromhex(result['hex'])==struct.pack('<8I',25,1,0,1,2*r['width']*r['height'],0,r['width'],r['height']),'independently derived complete glyph descriptor');put(args[2],bytes.fromhex(result['hex']))
   elif phase==2:
    need(args==[t['pointer'],0,word(self.read(bp+8)),0,2048] and a['native_op']=='lock' and a['native_request']==dict(pointer=p,flags=2048),'original whole glyph lock');result=self.opening_space.result('opening',native);need(result==e['textures'][obj]['lock'] and len(bytes.fromhex(result['hex']))==result['pitch']*r['height'] and result['pitch']>=2*r['width'],'complete actual bounded glyph surface');r['lock']=result;b=bytes.fromhex(result['hex']);lo=result['bits']&~4095;maps=[(lo,(result['bits']-lo+len(b)+4095)&~4095)];put(result['bits'],b);put(args[2],struct.pack('<2I',result['pitch'],result['bits']))
   elif phase==3:
    ref=self.opening_refs[obj];raw=bytes.fromhex(r['lock']['hex'])
    for band in previous.bands(ref['cfg']):raw=convert_surface(ref['stages'][-1],ref['cfg']['raster_size'],band['rect'],raw,r['lock']['pitch'],band['point'])
    need(args==[t['pointer'],0] and a['native_op']=='unlock' and a['native_request']==dict(pointer=p,hex=raw.hex()) and a['uploaded_hex']==raw.hex() and self.read(r['lock']['bits'],len(raw))==raw,'every independent source glyph conversion byte');result=copy.deepcopy(native);need(result['uploaded_sha256']==sha(raw),'actual current glyph upload receipt');r.update(uploaded_hex=raw.hex(),uploaded_sha256=sha(raw));rb=e['textures'][obj]['readback'];need(rb['hex']==raw.hex() and rb['sha256']==sha(raw) and e['GPU_trace'][a['native_wire_index']+1]['request']==dict(id=a['native_wire_index']+2,op='readback',pointer=p) and e['GPU_trace'][a['native_wire_index']+1]['reply']['result']==rb,'whole actual source glyph GPU readback');self.opening_pixels.append(raw)
   else:need(args==[t['pointer']] and a['native_op']=='release' and a['native_request']==dict(pointer=p) and native==dict(count=0),'source releases its own current glyph at zero references');result=copy.deepcopy(native);r['live']=False
  value=result['count'] if phase==5 else result['hr'];need(a['value']==value==0 and a['result']==result and a['memory_outputs']==out and a['new_mappings']==[dict(pointer=p,bytes=n) for p,n in maps] and ('uploaded_hex' in a)==(phase==3),'all and only independent glyph COM outputs');self.apply_outputs(a);self.api_return(value,pop,ret,sp);r['phase']+=1;self.opening_gpu_count+=1
 def retire_role9(self,a):
  i=self.role_native_count;need(8<=i<12 and a['index']==i,'four source role9 retirement calls');sp=self.cpu()['ESP'];bp=self.cpu()['EBP'];receiver=word(self.read(sp+4));found=[r for r in self.role_objects if r['texture']['pointer']==receiver and r['live']];need(len(found)==1,'unique current role9 retirement owner');r=found[0];phase=r['phase'];slot=56 if phase==4 else 8;pop=12 if phase==4 else 4;ret=word(self.read(sp));args=[word(self.read(sp+4+j)) for j in range(0,pop,4)];t=r['texture'];p=r['native_pointer'];need(phase in (4,5) and a['object_index']==r['index'] and a['phase']==phase and a['slot']==slot and a['target']==t['methods'][str(slot)] and a['sp']==sp and a['pop']==pop and a['return_va']==ret==(0x403a44 if phase==4 else 0x40378d) and a['args']==args==([receiver,0,bp-36] if phase==4 else [receiver]),'full natural role9 retire ABI');trace=self.role_case['GPU_trace'][i+2];op='describe' if phase==4 else 'release';native=trace['reply']['result'];need(a['native_op']==op and a['native_request']==dict(pointer=p) and trace['request']==dict(id=i+3,op=op,pointer=p) and a['native_result']==a['result']==native,'current role9 source owner native receipt');out=[dict(pointer=args[2],hex=struct.pack('<8I',25,1,0,1,2*r['width']*r['height'],0,r['width'],r['height']).hex())] if phase==4 else [];need((phase!=4 or native['hex']==out[0]['hex']) and (phase!=5 or native==dict(count=0)) and a['value']==0 and a['memory_outputs']==out and a['new_mappings']==[],'independent role9 descriptor/release outputs');self.apply_outputs(a);self.api_return(0,pop,ret,sp);r['phase']+=1;r['live']=phase!=5;self.role_native_count+=1
 def historical(self,a):
  sp=self.cpu()['ESP'];p=word(self.read(sp+4));need(p in self.opening_historical,'source-backed historical owner');r=self.opening_historical[p];phase=r['phase'];slot=56 if phase==4 else 8;pop=12 if phase==4 else 4;ret=word(self.read(sp));args=[word(self.read(sp+4+j)) for j in range(0,pop,4)];need(phase in (4,5) and a['owner']==r['owner'] and a['source']==r['source'] and a['phase']==phase and a['slot']==slot and a['target']==r['texture']['methods'][str(slot)] and a['sp']==sp and a['pop']==pop and a['return_va']==ret==(0x403a44 if phase==4 else 0x40378d) and a['args']==args==([p,0,self.cpu()['EBP']-36] if phase==4 else [p]),'independent historical descriptor/release full source ABI');result=copy.deepcopy(r['descriptor']) if phase==4 else dict(count=0);out=[dict(pointer=args[2],hex=result['hex'])] if phase==4 else [];need(a['result']==result and a['value']==0 and a['memory_outputs']==out and a['new_mappings']==[],'all and only pinned historical platform outputs');self.apply_outputs(a);self.api_return(0,pop,ret,sp);r['phase']+=1

def prepare(c):
 call=types.FunctionType(previous.verify_case.__code__,dict(previous.verify_case.__globals__,Replay=Replay,protocol=parent_protocol,previous=fourth_proxy),'independently_verify_prefix_before_natural_opening')
 try:call(c,None)
 except PrefixReady as found:return found.replay
 raise ValueError('one exact independently replayed opening boundary required')

@lru_cache(maxsize=1)
def proof_helper():return work.previous.previous.build_gpu(ROOT/'.venv-audit/school-retained-opening-independent-v1.exe')

def fresh_GPU(e,pixels):
 helper,build=proof_helper();gpu=work.previous.previous.ImageD3D8(helper);owned=[]
 try:
  for t,raw in zip(e['textures'],pixels):
   r=gpu.create(t['width'],t['height']);p=r['texture']['pointer'];need(p not in owned,'independent simultaneous live glyph owners');owned.append(p);desc=gpu.describe(p);need(desc['hex']==struct.pack('<8I',25,1,0,1,2*t['width']*t['height'],0,t['width'],t['height']).hex(),'independent fresh GPU complete descriptor');lock=gpu.lock(p);need(lock['pitch']==t['lock']['pitch'],'independent fresh native glyph pitch');gpu.unlock(p,raw);got=gpu.readback(p);need(got['hex']==raw.hex() and got['sha256']==sha(raw),'independent whole fresh GPU glyph pixels')
  for p in reversed(owned):need(gpu.release(p)==dict(count=0),'independent current GPU glyph release')
 finally:cleanup=gpu.close()
 need(cleanup==e['GPU'] and gpu.process.returncode==0,'independent normal current GPU owner cleanup');return dict(build=build,hello=gpu.hello,trace=gpu.trace,cleanup=cleanup,exit_code=gpu.process.returncode)

def begin(r,c):
 e=c['opening'];r.opening_case=e;r.opening_refs={};r.opening_objects=[];r.opening_pixels=[];r.opening_gpu_count=0;r.opening_space=work.previous.previous.AddressSpace();r.opening_space.next=0x69001000;r.opening_historical={};nc,_,_=work.old_name.mapped_texture();n=work.name_catalog.contracts()[1];r.opening_historical[nc['texture']['pointer']]=dict(owner='historical_name4',texture=nc['texture'],descriptor=n['COM_calls'][1]['result'],source=work.name_catalog.contracts()[2],phase=4);p=base.inputs()['parents'][c['name']];old=json.loads(gzip.decompress(base.pinned(p['path'],p['sha256'])))['case'];t=[x for x in old['device_proxy_trace'] if x['op']=='text_create'][1]['result']['texture'];desc=next(x['result'] for x in old['device_proxy_trace'] if x['op']=='text_desc' and x['request']['pointer']==t['pointer']);r.opening_historical[t['pointer']]=dict(owner='historical_second_text',texture=t,descriptor=desc,source=p,phase=4);need(work.state(r)==e['before'] and base.memory_rows(r.u)==c['role9']['final_memory'] and canonical(base.architectural_cpu(r.u))==canonical(e['entry_architectural_cpu'])==canonical(c['role9']['final_architectural_cpu']),'whole independently executed parent readiness and source opening entry')

def binding(r,b):
 stream=work.keyboard.contracts()['streams'][str(r.case['scene_capture'])];capture=next(x for x in stream['captures'] if x['label']==b['capture']['label']);need(capture==b['capture'] and r.read(work.keyboard.KEYBOARD,0xa00).hex()==b['before_hex'],'source capture identity and full before keyboard');before=r.read(work.keyboard.KEYBOARD,0xa00);bound=bytearray(before);bound[12:268]=bytes.fromhex(capture['raw_device_hex']);need(bytes(bound).hex()==b['bound_hex'] and b['binding']==dict(pointer=work.keyboard.KEYBOARD+12,bytes=256),'only captured raw device binding');f=b['fragment'];need(f==dict(va=0x4113d5,bp=work.STACK+0x800,sp=work.STACK+0x800-0x70,receiver_slot=work.STACK+0x800-4,receiver=work.keyboard.KEYBOARD,stop=0x4116a4),'declared original keyboard fragment inputs');r.u.mem_write(work.keyboard.KEYBOARD+12,bytes.fromhex(capture['raw_device_hex']));r.u.mem_write(f['receiver_slot'],struct.pack('<I',f['receiver']))
 for k,v in dict(EIP=f['va'],EBP=f['bp'],ESP=f['sp'],EFLAGS=0x202).items():r.u.reg_write(base.REGISTERS[k],v)
 n=r.source_step(b['step']);need(r.read(work.keyboard.KEYBOARD,0xa00)==base.predict_keyboard(bytes(bound))==bytes.fromhex(b['after_hex']) and work.keyboard.state(r)==b['state'],'independently derived whole source keyboard and control state');return n

def verify_case(c,boundary_observer=None):
 protocol(c);r=prepare(c);begin(r,c)
 if boundary_observer is not None:boundary_observer(r)
 e=c['opening'];count=writes=0;bindings=iter(e['bindings']);pending=next(bindings,None);decoded=[];confirm_controls={};confirmation_held=set()
 for frame_index,f in enumerate(e['frames']):
  now=work.state(r)
  is_press=pending is not None and pending['capture']['label']==work.keyboard.contracts()['streams'][str(c['scene_capture'])]['captures'][1]['label']
  if pending and r.read(work.keyboard.KEYBOARD,0xa00).hex()==pending['before_hex'] and pending['state']['PC']==now['PC'] and (not is_press or confirm_controls.get(now['PC'],0)>=2):
   if pending['capture']['label']==work.keyboard.contracts()['streams'][str(c['scene_capture'])]['captures'][1]['label']:need(now['PC'] in (366,416) and now['wait']==1 and confirm_controls.get(now['PC'],0)>=2,'at least two actual no-input confirmation controls before captured press');confirmation_held.add(now['PC'])
   count+=binding(r,pending);writes+=pending['step']['result']['writes'];pending=next(bindings,None)
  elif now['PC'] in (366,416) and now['wait']==1:confirm_controls[now['PC']]=confirm_controls.get(now['PC'],0)+1
  for s in f['steps']:
   count+=r.source_step(s);writes+=s['result']['writes'];decoded.extend(s['decoded']);need(r.cpu()['EIP']==RETURN and r.cpu()['ESP']==work.STACK+4,'every complete source request/reset/task naturally returns')
  need(work.state(r)==f['state'],'whole source opening frame state')
  if frame_index%50==0 or frame_index==221:print('independent opening frame',c['name'],c['scene_capture'],frame_index,f['state']['PC'],f['state']['wait'],flush=True)
 need(pending is None and confirmation_held=={366,416},'all and only two captured press/release pairs used');expect=work.contracts()['commands'];need([dict(PC=d['PC'],file_offset=452+d['PC'],opcode=d['opcode'],size=d['size'],hex=d['hex']) for d in decoded]==expect,'all 26 original remaining commands in source order, including terminal19');need(base.memory_rows(r.u)==e['final_memory']==e['frames'][-1]['steps'][-1]['full_memory'] and canonical(base.architectural_cpu(r.u))==canonical(e['final_architectural_cpu']) and work.state(r)==e['final'],'every final source mapping/CPU/role/VM state');need(len(r.opening_objects)==6 and len(r.opening_refs)==6 and r.opening_gpu_count==24 and e['typed_projection']==r.opening_space.ledger(),'six source glyphs and complete typed current domain')
 for actual,declared in zip(r.opening_objects,e['textures']):need(dict(actual,readback=declared['readback'])==declared,'all source glyph lifetimes, uploads and zero-reference releases')
 need(list(r.opening_historical.values())==e['historical'] and [h['phase'] for h in r.opening_historical.values()]==[4,6] and r.role_native_count==8 and r.native_count==6 and r.third_gpu_count==6 and r.gpu_count==4 and set(r.blocks)=={0x50201000,0x50601000},'natural third/fourth/second-text retirement and retained name/portrait vectors');glyph_cleanup=[]
 for t,s in zip(e['textures'],e['supplemental_cleanup']):
  need(s['root']==dict(va=0x403730,receiver=t['record'],args=[],sp=work.STACK,return_va=RETURN),'explicit original supplemental glyph destructor');glyph_cleanup.append(r.source_step(s))
 need(glyph_cleanup==[149]*6 and r.opening_gpu_count==36 and word(r.read(0x765720))==e['accounting_after_glyph_cleanup']==e['before']['accounting']-73728 and word(r.read(0x79fc74))==e['before']['game_bytes'] and e['natural_parent_texture_bytes_retired']==73728,'six complete original glyph destructors, all new glyph bytes returned and exact natural prior-resource accounting')
 for actual,declared in zip(r.opening_objects,e['textures_after_cleanup']):need(dict(actual,readback=declared['readback'])==declared,'all explicit source glyph releases and complete current owner state')
 fresh=fresh_GPU(e,r.opening_pixels);closure=[]
 for s in (c['role9']['image_cleanup'],c['role9']['name_cleanup'],c['fourth_texture']['cleanup'],c['third_dialogue']['cleanup'],c['cleanup']):closure.append(r.source_step(s))
 # Use the established original CRT replay implementation, without new fixture roots.
 from tools import school_retained_crt_image_verification as initcheck
 for s,va in zip(c['steps'][2:],(0x576fa0,0x57ba60)):
  need(s['root']==dict(va=va,args=[],sp=work.STACK,return_va=RETURN,receiver=0),'original empty CRT teardown roots');initcheck.replay_step(r,s)
 need(not r.blocks and not r.files and not r.criticals and r.depth==0 and r.history==c['allocation_history'] and r.consume('close')==c['helper_cleanup'] and r.wire==len(c['native_trace']),'all original CRT cleanup, history and entire normal native transcript');return dict(name=c['name'],scene_capture=c['scene_capture'],new_original_forward_instructions=count,new_original_writes=writes,source_forward_intervals=len(ordered(e)),complete_original_tasks=len(e['frames']),actual_remaining_commands=26,source_text_indices=list(range(4,10)),captured_confirmation_pairs=2,new_source_GDI_fonts=6,new_source_GPU_calls=36,new_forward_GPU_calls=24,supplemental_glyph_GPU_calls=12,all_current_glyphs_released=True,natural_parent_texture_bytes_retired=73728,parent_original_cleanup_verified=True,whole_CPU_memory_and_queue_verified=True,independent_fresh_GPU=fresh,parent_supplemental_cleanup_instructions=closure,final_PC=e['final']['PC'],final_wait=e['final']['wait'],final_opcode=e['final']['opcode'],final_mappings=len(e['final_memory']),new_OS_input=False,interactive_desktop_required=False,actual_D3D_draw_or_Present=False,R3_complete=False,R6_complete=False)

def verify(report):
 need(report['schema_version']==1 and report['contract']==work.contracts() and report['new_VM_roots']==report['game_function_substitutions']==report['IAT_rebindings']==0,'all source identities and no substitutes')
 for k in ('new_OS_input','actual_D3D_draw_or_Present','original_outer_scheduler','historical_heap_restored','R3_complete','R6_complete'):need(report[k]is False,'honest remaining opening scope '+k)
 need([(c['name'],c['scene_capture']) for c in report['cases']]==[(n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],'six complete opening branches');proofs=[]
 for c in report['cases']:proofs.append(verify_case(c));print('independent whole opening verified',c['name'],c['scene_capture'],flush=True)
 return dict(schema_version=1,cases=proofs,six_original_complete_openings_verified=True,interactive_desktop_required=False,new_OS_input=False,actual_D3D_draw_or_Present=False,R3_complete=False,R6_complete=False)

def verify_matrix(matrix,case_observer=None):
 need(matrix['schema_version']==1 and matrix['contract']==work.contracts() and matrix['new_VM_roots']==matrix['game_function_substitutions']==matrix['IAT_rebindings']==0,'all complete opening matrix source pins and no substitutes')
 for k in ('new_OS_input','actual_D3D_draw_or_Present','original_outer_scheduler','historical_heap_restored','R3_complete','R6_complete'):need(matrix[k]is False,'honest matrix scope '+k)
 need(matrix['new_GPU']is matrix['new_hidden_windows']is True,'actual independently owned hidden native resource domains');rows=matrix['case_reports'];need([(c['name'],c['scene_capture']) for c in rows]==[(n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],'all six immutable source opening case bindings');proofs=[]
 for row in rows:
  path=ROOT/row['path'];raw=base.pinned(row['path'],row['sha256']);need(len(raw)==row['bytes'],'whole compressed case byte length')
  with gzip.open(path,'rt',encoding='utf8') as f:c=json.load(f)
  need((c['name'],c['scene_capture'])==(row['name'],row['scene_capture']),'case source identity');p=verify_case(c);p['source_case']=row;proofs.append(p)
  if case_observer is not None:case_observer(p)
  del c;print('independent whole opening verified',row['name'],row['scene_capture'],flush=True)
 return dict(schema_version=1,cases=proofs,six_original_complete_openings_verified=True,interactive_desktop_required=False,new_OS_input=False,actual_D3D_draw_or_Present=False,R3_complete=False,R6_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('matrix');p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable proof')
 raw=(ROOT/a.matrix).read_bytes();result=verify_matrix(json.loads(raw));result['source_matrix_sha256']=sha(raw);result['verification_source_sha256']=sha((ROOT/'tools/school_retained_opening_verification.py').read_bytes());out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n');print('six whole original opening proofs saved',flush=True)
