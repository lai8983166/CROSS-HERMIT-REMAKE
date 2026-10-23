"""Independent original role9 resources, native ownership and natural task readiness."""
import copy,gzip,json,struct,types
from functools import lru_cache
from tools import school_retained_role9 as work
from tools import school_retained_fourth_texture_verification as previous
from tools import school_retained_third_confirmation_verification as keyboard
from tools import school_retained_third_dialogue_verification as text
from tools import school_retained_crt_fixture_verification as crtcheck
from tools.school_font_raster_catalog import geometry,convert_surface
from tools.school_second_live_text_catalog import bands
from tools.school_d3d8_platform import machine

ROOT=work.ROOT;base=work.base;need=work.need;word=work.word;sha=work.sha;canonical=work.canonical
GDI_WORK=types.SimpleNamespace(**dict(vars(work.dialogue),RASTER=work.RASTER,GDI=work.NAME_GDI,rules=types.SimpleNamespace(source_rules=lambda:dict(text=dict(hex=work.contracts()['role']['name_hex'])))))
name_redraw=types.FunctionType(text.reproduce_pixels.__code__,dict(text.reproduce_pixels.__globals__,work=GDI_WORK),'independent_source_role9_glyphs')

def ordered(e,cleanup=False):
 rows=[e[k] for k in ('name','name_upload','image_prefix','image','completion')]+[s for f in e['frames'] for s in f['steps']]
 return rows+([e['image_cleanup'],e['name_cleanup']] if cleanup else [])

def protocol(c):
 previous.protocol(c);e=c['role9'];need(e['contract']==work.contracts(),'pinned role9 source/asset/platform identities');need(e['before']['PC']==312 and e['final']['PC']==332 and e['final']['wait']==0 and e['final']['opcode']==30,'original role9 task and natural readiness before opcode43');need(e['role9_complete_task_returned']is e['role9_naturally_ready']is e['fourth_domain_retained']is True and e['next_script_instruction_executed']is False,'honest role9 completion and following boundary');need(e['new_VM_roots']==e['input_host_writes']==e['PC_or_wait_host_writes']==0,'no control or game function substitutes');need(0<=len(e['frames'])<=200 and [f['index'] for f in e['frames']]==list(range(len(e['frames']))),'bounded consecutive source readiness updates')
 for k,stop in [('name',0x403bd0),('name_upload',0x4cde10),('image_prefix',0x403bd0),('image',0x4cc0d2),('completion',work.RETURN)]:need(e[k]['root']is None and e[k]['result']['boundary']==stop,'continuous original '+k)
 for f in e['frames']:
  need(len(f['steps'])==4 and f['state']['PC']==332 and f['state']['wait']==int(f['index']<76) and f['state']['input_words']==[0,0,0],'complete natural no-input readiness state')
  for s,va,receiver in zip(f['steps'],(0x425de0,0x40db90,0x40dc80,0x454cf0),(work.task.INPUT,work.task.MANAGER,work.task.MANAGER,work.task.TACT)):text.previous.root_check(s,va,receiver)
 need(len(e['frames'])==77 and len(e['pending_name_texture']['frames'])==7 and len(e['image_record']['frames'])==12,'full role9 original readiness and nested name/portrait stacks')
 need(e['name_cleanup']['root']==dict(va=0x403730,receiver=work.TEXTURE,args=[],sp=work.STACK,return_va=work.RETURN),'explicit original name destructor');need(e['image_cleanup']['root']['va']==0x41f4e0 and e['image_cleanup']['root']['args']==[30] and e['image_cleanup']['root']['sp']==work.STACK and e['image_cleanup']['root']['return_va']==work.RETURN,'explicit slot30 original container cleanup');need(len(e['textures'])==2 and all(r['phase']==4 and r['live'] for r in e['textures']) and all(r['phase']==6 and not r['live'] for r in e['textures_after_cleanup']),'two source-owned live textures then exact destruction');need(e['GPU_exit']==0 and e['GPU']==dict(texture_releases=[],device_release_count=0,factory_release_count=0,window_destroyed=True,all_owned_resources_released=True) and e['GDI']==dict(fonts=0,bitmaps=0,dcs=1,all_resources_released=True) and e['files']==dict(actual_handles_closed=1,open_handles=0,all_owned_files_closed=True),'normal role9 native/GDI/file cleanup');need(len(e['GPU_trace'])==15 and [r['request']['op'] for r in e['GPU_trace']]==['create','describe','lock','unlock','readback','create','describe','lock','unlock','readback','describe','release','describe','release','close'],'whole two-texture native transcript')
 for i,r in enumerate(e['GPU_trace'],1):need(r['request']['id']==r['reply']['id']==i and r['reply']['ok']is True,'actual ordered native requests')
 hello=e['GPU_hello'];build=e['GPU_build'];need(hello['pointer_bytes']==4 and hello['window_visible']is False and hello['sdk']==220 and machine(hello['runtime_path'])==0x14c and sha((ROOT/hello['runtime_path']).read_bytes())==hello['runtime_sha256'],'current x86 hidden role9 runtime');need(build['machine']==0x14c and build['source_sha256']==work.previous.contracts()['GPU_source_sha256'],'bounded role9 native helper identity');need(e['GPU_trace'][-1]['reply']['result']==e['GPU'],'actual normal role9 close receipt')
 need([a['name'] for a in e['file_trace']]==['CreateFileA','GetFileSize','ReadFile','CloseHandle'] and [a['index'] for a in e['file_trace']]==list(range(4)),'full actual original SC009 lifecycle');need(e['image_record']['file_hex']==work.asset().hex() and len(e['copy_rows'])==512,'complete source SC009 bytes and every source row');need(e['accounting_after_cleanup']==e['accounting_before'] and e['game_bytes_after_cleanup']==e['game_bytes_before'] and e['game_bytes_with_role']==e['game_bytes_before']+88,'both original counters naturally balanced');need(e['fourth_trace_count_before']==e['fourth_trace_count_after']==5,'fourth native domain remains untouched');need(all('role_state' in s and 'copy_rows' in s and 'full_memory' in s and 'architectural_cpu' in s and 'queue' in s for s in ordered(e,True)),'complete state and provenance on every source interval')

@lru_cache(maxsize=1)
def proof_helper():return work.previous.build_gpu(ROOT/'.venv-audit/school-retained-role9-independent-v1.exe')

def pixels(c):
 e=c['role9'];proxy=dict(c,third_dialogue=e,pending_font=c['fourth_texture']['pending_font']);reference=name_redraw(proxy);name,image=e['textures'];cfg=geometry(e['raster']['measured']);need([name['width'],name['height']]==[1<<(x-1).bit_length() for x in cfg['texture_size']] and [image['width'],image['height']]==[256,512],'source role9 dimensions');expected=bytes.fromhex(name['lock']['hex'])
 for b in bands(cfg):expected=convert_surface(reference['stages'][-1],cfg['raster_size'],b['rect'],expected,name['lock']['pitch'],b['point'])
 photo=bytearray.fromhex(image['lock']['hex']);raw=work.asset()
 for i in range(512):photo[i*image['lock']['pitch']:i*image['lock']['pitch']+512]=raw[24+i*512:24+(i+1)*512]
 values=[expected,bytes(photo)]
 for i,(r,b) in enumerate(zip(e['textures'],values)):
  need(r['uploaded_hex']==r['readback']['hex']==b.hex() and r['uploaded_sha256']==r['readback']['sha256']==sha(b) and e['GPU_trace'][4 if i==0 else 9]['reply']['result']==r['readback'],'every independent name/portrait byte and actual source readback')
 helper,build=proof_helper();gpu=work.previous.ImageD3D8(helper);pointers=[]
 try:
  for r,b in zip(e['textures'],values):
   made=gpu.create(r['width'],r['height']);p=made['texture']['pointer'];pointers.append(p);gpu.describe(p);locked=gpu.lock(p);need(locked['pitch']==r['lock']['pitch'],'independent fresh native pitch');gpu.unlock(p,b);got=gpu.readback(p);need(bytes.fromhex(got['hex'])==b and got['sha256']==sha(b),'independent fresh GPU whole name/portrait readback')
  for p in reversed(pointers):need(gpu.release(p)==dict(count=0),'independent zero-reference resource release')
 finally:cleanup=gpu.close()
 need(cleanup==e['GPU'] and gpu.process.returncode==0,'independent normal native ownership cleanup');files=work.Files()
 try:h=files.open([0x80000000,1,0,3,1,0]);need(files.size(h)==262168 and files.read(h,262168)==raw,'independent actual full SC009 read');files.release(h)
 finally:file_cleanup=files.close()
 need(file_cleanup==e['files'],'independent normal read-only file ownership');return dict(reference=reference,cfg=cfg,bytes=values,fresh_GPU=dict(build=build,hello=gpu.hello,trace=gpu.trace,cleanup=cleanup,exit_code=gpu.process.returncode),fresh_file_cleanup=file_cleanup)

ROLE_ALLOWED="'actual_role9_GDI','actual_role9_GPU','actual_role9_CRT','actual_role9_file','recorded_task_platform'"
class Replay(previous.Replay):
 original_name_gdi=work.previous.previous.adapt_validation(text.Replay.gdi,[("-0x110","-0x108")],work=GDI_WORK)
 role_crt_api=work.previous.previous.adapt_validation(crtcheck.Replay.api,[("[262208,128,262208][len(self.history)]","[262208,128,262208,128][len(self.history)]"),("[262168,88,262168][sum(h['freed'] for h in self.history)]","[262168,262168,88,88][sum(h['freed'] for h in self.history)]")])
 def api(self,a):
  if a.get('kind')!='recorded_task_platform' and a.get('import_slot') in crtcheck.work.IMPORTS:return self.role_crt_api(a)
  return super().api(a)
 role_code=work.previous.previous.adapt_validation(keyboard.Replay.next_step,[("'actual_owned_fourth_GDI','recorded_replaced_text_GPU','recorded_task_platform'",ROLE_ALLOWED),("if kind=='actual_owned_fourth_GDI':self.next_gdi(q)\n   elif kind=='recorded_replaced_text_GPU':self.existing_gpu(q)\n   else:self.api(q)","if kind=='actual_role9_GDI':self.role_gdi(q)\n   elif kind=='actual_role9_GPU':self.role_gpu_api(q)\n   elif kind=='actual_role9_file':self.role_file_api(q)\n   else:self.api(q)"),("display=[]","display=[];conversions=[]"),("if at in work.previous.DISPLAY:","if at==0x405869:\n   sp=self.cpu()['ESP'];args=[word(self.read(sp+j)) for j in range(0,24,4)];conversions.append(dict(va=at,args=args,lock_hex=self.read(args[1],8).hex(),rect=list(struct.unpack('<4I',self.read(args[4],16))),point=list(struct.unpack('<2I',self.read(args[5],8)))))\n  if at==0x56d4d0 and word(self.read(self.cpu()['ESP']))==0x40483f:self.observe_copy()\n  if at in work.previous.DISPLAY:"),("s['conversions']==[]","conversions==s['conversions']")])
 def next_step(self,s):
  if s['label']=='supplemental_original_fourth_texture_destructor':self.role9_extension()
  return super().next_step(s)
 def role_step(self,s):
  self.step_copies=[];count=self.role_code(s);need(self.step_copies==s['copy_rows'] and work.state(self)==s['role_state'],'every SC009 copy and full role9 state');return count
 def observe_copy(self):
  e=self.role_case;row=len(self.all_copies);sp=self.cpu()['ESP'];args=[word(self.read(sp+4+i)) for i in (0,4,8)];lock=self.role_objects[1]['lock'];need(row<512 and args==[lock['bits']+row*lock['pitch'],e['image_record']['file_buffer']+24+row*512,512],'independent all original SC009 row memcpy arguments');r=dict(row=row,args=args,return_va=0x40483f);self.all_copies.append(r);self.step_copies.append(r)
 def role_gdi(self,a):
  old=(self.third_case,self.reference,self.case);self.third_case=self.role_case;self.reference=self.role_pixels['reference'];self.case=dict(self.case,pending_font=self.case['fourth_texture']['pending_font'])
  try:return self.original_name_gdi(a)
  finally:self.third_case,self.reference,self.case=old
 def role_file_api(self,a):
  e=self.role_case;i=self.role_file_count;slot=a['import_slot'];name,pop=work.FILE_SLOTS[slot];sp=self.cpu()['ESP'];ret=word(self.read(sp));args=[word(self.read(sp+4+j)) for j in range(0,pop,4)];need(i<4 and a['index']==i and name==['CreateFileA','GetFileSize','ReadFile','CloseHandle'][i] and a['name']==name and a['pop']==pop and a['target']==word(self.read(slot)) and a['sp']==sp and a['return_va']==ret==[0x42ac9c,0x42ad0d,0x42ad82,0x42ada5][i] and a['args']==args and a==dict(e['file_trace'][i],va=a['va'],key=a['key']),'exact actual source file import/full ABI and receipt');outputs=[]
  if i==0:need(work.crt.old.text(self,args[0])==b'data\\adv\\bin\\sc009.bin' and args[1:]==[0x80000000,1,0,3,1,0] and a['source_relative_path_hex']==b'data\\adv\\bin\\sc009.bin'.hex() and 0<a['value']<0xffffffff,'only fixed source read-only SC009');self.role_file_handle=a['value'];value=a['value']
  elif i==1:need(args==[self.role_file_handle,0],'owned SC009 size');value=262168
  elif i==2:
   p=self.history[-1]['guest'];need(args[0]==self.role_file_handle and args[1]==p+32 and args[2]==262168 and args[4]==0 and p in self.blocks,'original owned entire SC009 allocation/read');raw=work.asset();outputs=[dict(pointer=args[1],hex=raw.hex()),dict(pointer=args[3],hex=struct.pack('<I',len(raw)).hex())];need(a['file_sha256']==sha(raw) and a['bytes_read']==262168 and a['source_allocation']==p,'complete pinned actual SC009 bytes');value=1
  else:need(args==[self.role_file_handle],'original closes its own current file');value=1;self.role_file_handle=None
  need(a['value']==value and a['memory_outputs']==outputs and a['new_mappings']==[],'all and only independent actual SC009 outputs');self.apply_outputs(a);self.api_return(value,pop,ret,sp);self.role_file_count+=1
 def role_gpu_api(self,a):
  e=self.role_case;i=self.role_native_count;need(0<=i<12 and a['index']==i,'twelve ordered original role9 COM calls');obj=0 if i<4 or i>=10 else 1;phase=i if i<4 else i-4 if i<8 else i-4 if i<10 else i-6;slot=[80,56,64,68,56,8][phase];pop={80:32,56:12,64:20,68:8,8:4}[slot];sp=self.cpu()['ESP'];bp=self.cpu()['EBP'];ret=word(self.read(sp));args=[word(self.read(sp+4+j)) for j in range(0,pop,4)];need(a['object_index']==obj and a['phase']==phase and a['slot']==slot and a['pop']==pop and a['sp']==sp and a['return_va']==ret==[0x403c8a,0x403cbe,0x40395e,0x4039d3,0x403a44,0x40378d][phase] and a['args']==args,'original role9 COM full ABI and exact owner/phase');out=[];maps=[];trace=e['GPU_trace'][i+int(i>=4)+int(i>=8)];native=trace['reply']['result'];request=trace['request'];need(a['native_result']==native and dict(id=request['id'],op=a['native_op'],**a['native_request'])==request,'whole actual native source request/reply')
  def put(p,b):out.append(dict(pointer=p,hex=b.hex()))
  if phase==0:
   w,h=([64,32] if obj==0 else [256,512]);record=work.TEXTURE if obj==0 else e['image_record']['record'];need(a['target']==self.device_method and args==[self.device,w,h,1,0,25,1,record+44] and a['native_op']=='create' and a['native_request']==dict(width=w,height=h,levels=1,usage=0,format=25,pool=1),'original role9 source device, shape and output record');result=self.role_space.result('role9',native);t=result['texture'];r=dict(index=obj,record=record,width=w,height=h,texture=t,native_pointer=native['texture']['pointer'],phase=0,live=True);need(len(self.role_objects)==obj and all(o['native_pointer']!=r['native_pointer'] for o in self.role_objects),'two different concurrently owned current objects');self.role_objects.append(r)
   for p in (t['pointer'],t['vtable'],*t['methods'].values()):
    page=p&~4095
    if not any(lo<=page<=hi for lo,hi,_ in self.u.mem_regions()) and (page,4096) not in maps:maps.append((page,4096))
   put(t['pointer'],struct.pack('<I',t['vtable']))
   for k,p in t['methods'].items():put(t['vtable']+int(k),struct.pack('<I',p))
   put(args[7],struct.pack('<I',t['pointer']))
  else:
   r=self.role_objects[obj];t=r['texture'];p=r['native_pointer'];need(r['live'] and r['phase']==phase and a['target']==t['methods'][str(slot)] and args[0]==t['pointer'],'same owned live role9 texture and current method')
   if phase in (1,4):
    need(args==[t['pointer'],0,bp-(52 if phase==1 else 36)] and a['native_op']=='describe' and a['native_request']==dict(pointer=p),'original role9 descriptor output');result=copy.deepcopy(native);w,h=r['width'],r['height'];need(bytes.fromhex(result['hex'])==struct.pack('<8I',25,1,0,1,2*w*h,0,w,h) and result['width']==w and result['height']==h and result['size']==2*w*h and result['hr']==0,'independent full format25 descriptor');put(args[2],bytes.fromhex(result['hex']))
   elif phase==2:
    need(args==[t['pointer'],0,word(self.read(bp+8)),0,2048] and a['native_op']=='lock' and a['native_request']==dict(pointer=p,flags=2048),'original role9 whole surface lock');result=self.role_space.result('role9',native);need(result==e['textures'][obj]['lock'] and result['pitch']>=2*r['width'] and len(bytes.fromhex(result['hex']))==result['pitch']*r['height'],'whole bounded current native surface');r['lock']=result;b=bytes.fromhex(result['hex']);lo=result['bits']&~4095;maps=[(lo,(result['bits']-lo+len(b)+4095)&~4095)];put(result['bits'],b);put(args[2],struct.pack('<2I',result['pitch'],result['bits']))
   elif phase==3:
    raw=self.read(r['lock']['bits'],len(bytes.fromhex(r['lock']['hex'])));need(args==[t['pointer'],0] and a['native_op']=='unlock' and a['native_request']==dict(pointer=p,hex=raw.hex()) and raw==self.role_pixels['bytes'][obj] and a['uploaded_hex']==raw.hex(),'independent every original name/SC009 pixel uploaded');result=copy.deepcopy(native);need(result['uploaded_sha256']==sha(raw) and result['hr']==0,'actual whole native source upload receipt');r.update(uploaded_hex=raw.hex(),uploaded_sha256=sha(raw))
   else:need(args==[t['pointer']] and a['native_op']=='release' and a['native_request']==dict(pointer=p) and native==dict(count=0),'source role9 releases exactly its own current object');result=copy.deepcopy(native);r['live']=False
  value=result['count'] if phase==5 else result['hr'];need(a['value']==value==0 and a['result']==result and a['new_mappings']==[dict(pointer=p,bytes=n) for p,n in maps] and a['memory_outputs']==out and ('uploaded_hex' in a)==(phase==3),'all and only independent role9 COM outputs');r['phase']+=1;self.apply_outputs(a);self.api_return(value,pop,ret,sp);self.role_native_count+=1
 def role9_extension(self):
  e=self.case['role9'];self.role_case=e;need(work.state(self)==e['before'] and canonical(base.architectural_cpu(self.u))==canonical(e['entry_architectural_cpu'])==canonical(self.case['fourth_texture']['final_architectural_cpu']),'continuous whole role9 entry CPU/state');account=word(self.read(0x765720));game=word(self.read(0x79fc74));need((account,game)==(e['accounting_before'],e['game_bytes_before']),'both untouched original entry counters');self.role_pixels=pixels(self.case);self.role_objects=[];self.role_native_count=self.role_file_count=0;self.role_file_handle=None;self.all_copies=[];self.role_space=work.previous.AddressSpace();self.role_space.next=0x6e001000;fourth_bytes=self.read(self.new_lock['bits'],len(self.fourth_pixels['bytes']));count=self.role_step(e['name']);sp=self.cpu()['ESP'];outer=[('name',0x4cc1de),('layer',0x4c62d4),('handler',0x4ceda7),('VM',0x454d90),('task',work.RETURN)];pending=dict(va=0x403bd0,receiver=self.cpu()['ECX'],args=[word(self.read(sp+4)),word(self.read(sp+8))],return_va=word(self.read(sp)),frames=work.chain(self,[('raster',0x408e81),('texture_wrapper',0x4ca82c),*outer]),first_instruction_executed=False);need(pending==e['pending_name_texture'] and pending['receiver']==work.TEXTURE and pending['args']==[self.device,0] and pending['return_va']==0x405779,'natural role9 name texture ABI and seven source frames');need(self.read(work.RASTER,len(self.role_pixels['reference']['stages'][-1]))==self.role_pixels['reference']['stages'][-1],'whole independently redrawn source role9 raster');count+=self.role_step(e['name_upload']);sp=self.cpu()['ESP'];pending=dict(va=0x4cde10,receiver=self.cpu()['ECX'],args=[word(self.read(sp+4)),word(self.read(sp+8))],return_va=word(self.read(sp)),frames=work.chain(self,[('resource',0x4cc26d),*outer[1:]]),first_instruction_executed=False);need(pending==e['pending_image'] and pending['receiver']==work.VM and pending['args'][1]==30 and pending['return_va']==0x4cc0d2 and work.crt.old.text(self,pending['args'][0])==b'data\\adv\\bin\\sc009.bin' and self.role_native_count==4,'natural source SC009 path/slot and original name completion');count+=self.role_step(e['image_prefix']);r=e['image_record'];need(len(self.history)==4 and r['file_buffer']==self.history[2]['guest']+32==0x50401020 and r['array']==self.history[3]['guest']+32==0x50601020 and r['record']==r['array']+4==word(self.read(self.renderer+0x844+30*8)) and self.read(r['record'],84).hex()==r['record_hex'] and self.read(self.renderer+0x844+30*8,8).hex()==r['table_hex'] and self.read(r['file_buffer'],262168)==work.asset(),'all full source file/vector/header/registration bytes');need(work.chain(self,[('dx',0x41f3e0),('entry',0x41f25a),('container',0x41f0c9),('container_wrapper',0x41684b),('extended_register',0x4167bf),('register',0x4cde8a),('image',0x4cc0d2),('resource',0x4cc26d),*outer[1:]])==r['frames'],'all twelve natural portrait source frames')
  for p,receipt in zip((0x50401000,0x50601000),e['native_allocation_readbacks']):
   raw=self.sync(p);actual=self.consume('readback',pointer=self.blocks[p]['native']);need(receipt==dict(guest=p,wire_index=self.wire-1,result=actual) and actual['hex']==raw.hex(),'entire actual native source SC009/vector allocation readback')
  need(len(e['native_allocation_readbacks'])==2,'exact two current allocation readbacks');count+=self.role_step(e['image']);need(self.cpu()['EIP']==0x4cc0d2 and len(self.all_copies)==512 and self.all_copies==e['copy_rows'] and self.role_native_count==8 and set(self.blocks)=={0x50201000,0x50601000} and self.read(work.VM+0x92a0+30,1)==b'\x01','complete original SC009 rows, IMAGE return, owned source file free and loaded flag');count+=self.role_step(e['completion']);need(self.cpu()['EIP']==work.RETURN and self.cpu()['ESP']==work.STACK+4 and work.state(self)['PC']==332 and work.state(self)['wait']==1,'original full role9 handler/VM/task returns before readiness');need(len(e['frames'])==77,'77 original role9 readiness updates')
  for f in e['frames']:
   for s in f['steps']:count+=self.role_step(s);need(self.cpu()['EIP']==work.RETURN and self.cpu()['ESP']==work.STACK+4,'each original complete request/reset/task natural return')
   need(work.state(self)==f['state'] and f['state']['PC']==332 and f['state']['wait']==int(f['index']<76) and f['state']['input_words']==[0,0,0],'all source natural wait states without input or control changes')
  need(work.state(self)==e['final'] and base.memory_rows(self.u)==e['final_memory']==ordered(e)[-1]['full_memory'] and canonical(base.architectural_cpu(self.u))==canonical(e['final_architectural_cpu']),'every final original mapping and full architectural CPU');need(e['typed_projection']==self.role_space.ledger() and self.role_native_count==8 and self.role_file_count==4 and self.role_file_handle is None,'whole typed domain and closed source file');need(self.read(self.new_lock['bits'],len(fourth_bytes))==fourth_bytes and sha(fourth_bytes)==e['fourth_surface_sha256'],'old fourth surface retained throughout source role9 scope');need(word(self.read(0x765720))==e['accounting_with_role']==account+266240 and word(self.read(0x79fc74))==e['game_bytes_with_role']==game+88,'two original current texture extents and source vector accounting')
  for actual,declared in zip(self.role_objects,e['textures']):need(dict(actual,readback=declared['readback'])==declared,'all current live source resource state')
  need(e['image_cleanup']['root']==dict(va=0x41f4e0,receiver=self.renderer+0x844,args=[30],sp=work.STACK,return_va=work.RETURN),'source image container receiver and exact slot');cleanup=sum(self.role_step(e[k]) for k in ('image_cleanup','name_cleanup'));need(self.role_native_count==12 and set(self.blocks)=={0x50201000} and word(self.read(0x765720))==account and word(self.read(0x79fc74))==game and word(self.read(work.TEXTURE+44))==0 and self.read(self.renderer+0x844+30*8,8)==bytes(8),'source containers/textures/vector cleanup and both exact counter balances')
  for actual,declared in zip(self.role_objects,e['textures_after_cleanup']):need(dict(actual,readback=declared['readback'])==declared,'all final source releases and object ownership')
  writes=sum(s['result']['writes'] for s in ordered(e));need((count,writes,cleanup)==(4512473,2495055,1580),'all original role9 forward instruction/write/cleanup totals');self.role_proof=dict(new_original_forward_instructions=count,new_original_writes=writes,original_cleanup_instructions=cleanup,source_forward_intervals=len(ordered(e)),complete_original_tasks=78,natural_readiness_updates=77,final_PC=332,final_wait=0,next_script_instruction_executed=False,role_index=9,role_name_big5=work.contracts()['role']['name_big5'],name_texture=[64,32],portrait_texture=[256,512],actual_source_COM_calls=12,actual_source_read_only_file_calls=4,original_copy_rows=512,complete_source_file_bytes=262168,final_mappings=len(e['final_memory']),natural_name_frames=7,natural_portrait_frames=12,whole_CPU_memory_and_queues_verified=True,both_original_counters_balanced=True,independent_fresh_GDI_verified=True,independent_fresh_GPU=self.role_pixels['fresh_GPU'],independent_fresh_file=self.role_pixels['fresh_file_cleanup'],fourth_domain_retained=True,separate_native_GPU_domain=True,new_OS_input=False,interactive_desktop_required=False,actual_draw_or_Present=False,R3_complete=False,R6_complete=False)

def verify_case(c,boundary_observer=None):
 protocol(c);observed=[]
 class Observed(Replay):
  def role9_extension(self):
   if boundary_observer is not None:boundary_observer(self)
   super().role9_extension();observed.append(self.role_proof)
 call=types.FunctionType(previous.verify_case.__code__,dict(previous.verify_case.__globals__,Replay=Observed),'verify_all_original_stages_and_role9_resources');parent=call(c,None);need(len(observed)==1,'one full independent original role9 scope');return dict(name=c['name'],scene_capture=c['scene_capture'],parent=parent,role9=observed[0])

def verify(r):
 need(r['schema_version']==1 and r['contract']==work.contracts() and r['new_VM_roots']==r['game_function_substitutions']==r['IAT_rebindings']==0,'pinned source/asset and no substitutes')
 for k in ('new_OS_input','actual_D3D_draw_or_Present','original_outer_scheduler','historical_heap_restored','R3_complete','R6_complete'):need(r[k]is False,'honest role9 scope '+k)
 need(r['new_GPU']is r['new_hidden_windows']is True,'actual new owned texture domains');need([(c['name'],c['scene_capture']) for c in r['cases']]==[(n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],'all six complete role9 branches');proofs=[]
 for c in r['cases']:proofs.append(verify_case(c));print('independent original role9 verified',c['name'],c['scene_capture'],flush=True)
 return dict(schema_version=1,cases=proofs,six_original_role9_resources_tasks_and_readiness_verified=True,new_GPU=True,actual_D3D_draw_or_Present=False,interactive_desktop_required=False,new_OS_input=False,R3_complete=False,R6_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable proof')
 raw=(ROOT/a.report).read_bytes();result=verify(json.loads(gzip.decompress(raw)));result['source_report_sha256']=sha(raw);out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n');print('six full original role9 proofs',flush=True)
