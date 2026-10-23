"""Whole remaining original opening dialogue/control sequence in current resource lifetimes."""
import copy,gzip,json,struct,types
from functools import lru_cache
from unicorn import UC_HOOK_CODE
from tools import school_retained_role9 as previous
from tools import school_retained_third_dialogue as dialogue
from tools import school_retained_third_confirmation as keyboard
from tools import school_retained_portrait_file as old_name
from tools import school_retained_portrait_file_catalog as name_catalog
from tools.school_text_preparation_catalog import source_catalog as text_catalog
from tools.school_font_raster_catalog import geometry

ROOT=previous.ROOT;base=previous.base;need=previous.need;word=previous.word;sha=previous.sha;canonical=previous.canonical
VM=base.VM;STACK=previous.STACK;RETURN=previous.RETURN;task=previous.task;adapt=keyboard.adapt_validation
ACCEPTANCE='analysis/school-retained-role9-acceptance-v1-20261023.json'
ACCEPTANCE_SHA='417f7961e3cc1f181657e2052e8482832905a6f4737d875be6022eeb46ec969c'

@lru_cache(maxsize=1)
def contracts():
 a=json.loads(base.pinned(ACCEPTANCE,ACCEPTANCE_SHA));need(a['final_PC']==332 and a['final_wait']==0 and a['role9_task_completed'] and a['tasks_complete']==3,'accepted original role9 readiness');r=json.loads(base.pinned('analysis/school-retained-role9-following-script-v1-20261023.json',next(x['sha256'] for x in a['artifact_manifest'] if x['path'].endswith('following-script-v1-20261023.json'))));return dict(parent_acceptance=ACCEPTANCE,parent_acceptance_sha256=ACCEPTANCE_SHA,commands=r['commands'],texts=text_catalog()['entries'][4:10],previous=previous.contracts(),mode='original complete opening tasks and captured keyboard processing; current GDI/GPU; explicit old historical platform contracts; no draw/Present or OS input')

def state(g):
 r=previous.state(g);r.update(vm_header_hex=g.read(VM,64).hex(),vm_control_hex=g.read(VM+0x9228,0x118).hex(),all_role_nodes_hex=g.read(VM+0x6f60,10*224).hex(),text_headers=[g.read(VM+0x430+i*0xab8,40).hex() for i in range(10)],accounting=word(g.read(0x765720)),game_bytes=word(g.read(0x79fc74)));return r

class Guest(previous.Guest):
 continue_third=adapt(dialogue.Guest.continue_third,[("word(self.read(0x765720))==account","word(self.read(0x765720))==account-getattr(self,'replaced_texture_bytes',0)-getattr(self,'opening_third_adjustment',0)")])
 continue_fourth=adapt(previous.previous.Guest.continue_fourth,[("self.fourth_gpu_count==6 and word(self.read(0x765720))==account","self.fourth_gpu_count==6 and word(self.read(0x765720))==account-getattr(self,'opening_fourth_adjustment',0)")])
 continue_role9=adapt(previous.Guest.continue_role9,[("list(self.allocations)==[0x50201000] and word(self.read(0x765720))==account and word(self.read(0x79fc74))==game_bytes","list(self.allocations)==([] if getattr(self,'opening_done',False) else [0x50201000]) and word(self.read(0x765720))==account-getattr(self,'opening_role_adjustment',0) and word(self.read(0x79fc74))==game_bytes-(88 if getattr(self,'opening_done',False) else 0)")])
 def execute(self,label,stop,root=None):
  if label=='supplemental_original_character_container_cleanup':self.third_record=self.continue_third()
  return super().execute(label,stop,root)
 def new_root(self,label,va,recv):
  if label=='supplemental_original_third_texture_destructor':self.confirm_record=self.continue_confirmation(self.opening_scene)
  elif label=='supplemental_original_fourth_texture_destructor':self.role9_record=self.continue_role9()
  return dialogue.Guest.new_root(self,label,va,recv)
 def role_step(self,label,stop=RETURN,root=None):
  if label=='supplemental_original_role9_image_container_cleanup':self.opening_record=self.continue_opening()
  return super().role_step(label,stop,root)
 def new_api(self,slot):
  if not getattr(self,'opening_running',False):return super().new_api(slot)
  sp=self.cpu()['ESP'];ret=word(self.read(sp))
  if slot in dialogue.GDI and not(slot==task.LENGTH_SLOT and ret==0x425a7e):
   if slot==task.FONT_SLOT:
    need(ret==0x4cad09,'original remaining dialogue font caller');index=len(self.opening_fonts);raster=0x39000000+index*0x100000;need(index<10,'bounded remaining dialogue font operations');args=[word(self.read(sp+4+i*4)) for i in range(14)];call=types.FunctionType(dialogue.Offscreen.call_raster.__code__,dict(dialogue.Offscreen.call_raster.__globals__,RASTER=raster),'current_opening_raster')
    Service=type('OpeningOffscreen',(dialogue.Offscreen,),dict(call_raster=call));service=Service(word(self.read(self.renderer+0xb208)));self.opening_services.append(service);self.offscreen=service;self.opening_raster=raster;self.opening_fonts.append(dict(index=index,raster=raster,font_args=args,return_va=ret,cpu=self.cpu(),frames=previous.chain(self,[('font',0x4c4d04),('text',0x4cec2b),('VM',0x454d90),('task',RETURN)])))
   need(self.opening_fonts,'owned font scope before raster API');call=types.FunctionType(dialogue.Guest.new_api.__code__,dict(dialogue.Guest.new_api.__globals__,RASTER=self.opening_raster),'actual_remaining_dialogue_API');call(self,slot);self.api_calls[-1].update(kind='actual_opening_GDI',font_index=len(self.opening_fonts)-1);return
  self.task_api(slot)
  if self.api_calls[-1].get('kind')!='recorded_task_platform':self.api_calls[-1]['kind']='actual_opening_CRT'
  self.memory_evidence.refresh()
  for o in self.api_calls[-1]['memory_outputs']:self.memory_evidence.mark(o['pointer'],len(bytes.fromhex(o['hex'])))
 def new_gpu(self,at):
  if not getattr(self,'opening_running',False):return super().new_gpu(at)
  sp=self.cpu()['ESP'];receiver=word(self.read(sp+4))
  if at==self.device_method or any(r['texture']['pointer']==receiver for r in self.opening_textures):return self.opening_gpu_api(at)
  if receiver==self.texture['pointer']:
   task.parent.Guest.gpu(self,at);self.memory_evidence.refresh()
   for o in self.api_calls[-1]['memory_outputs']:self.memory_evidence.mark(o['pointer'],len(bytes.fromhex(o['hex'])))
  elif receiver in self.opening_historical:self.historical_gpu_api(at,self.opening_historical[receiver])
  else:super().new_gpu(at)
  self.opening_parent_calls.append(copy.deepcopy(self.api_calls[-1]))
 def historical_gpu_api(self,at,r):
  phase=r['phase'];need(phase in (4,5),'source historical object still live');slot=(56 if phase==4 else 8);pop=(12 if phase==4 else 4);sp=self.cpu()['ESP'];bp=self.cpu()['EBP'];ret=word(self.read(sp));args=[word(self.read(sp+4+j)) for j in range(0,pop,4)];t=r['texture'];need(at==t['methods'][str(slot)] and ret==(0x403a44 if phase==4 else 0x40378d) and args==([t['pointer'],0,bp-36] if phase==4 else [t['pointer']]),'source historical owner/method/full ABI');result=copy.deepcopy(r['descriptor']) if phase==4 else dict(count=0);out=[dict(pointer=args[2],hex=result['hex'])] if phase==4 else []
  for o in out:self.u.mem_write(o['pointer'],bytes.fromhex(o['hex']));self.memory_evidence.mark(o['pointer'],len(bytes.fromhex(o['hex'])))
  value=result['hr'] if phase==4 else result['count'];self.api_calls.append(dict(kind='recorded_opening_historical_GPU',owner=r['owner'],phase=phase,slot=slot,target=at,sp=sp,return_va=ret,pop=pop,args=args,value=value,result=result,source=r['source'],new_mappings=[],memory_outputs=out));r['phase']+=1;self.u.reg_write(base.REGISTERS['EAX'],value);self.u.reg_write(base.REGISTERS['ESP'],sp+4+pop);self.u.reg_write(base.REGISTERS['EIP'],ret)
 def opening_gpu_api(self,at):
  slot=80 if at==self.device_method else self.opening_methods[at];pop={80:32,56:12,64:20,68:8,8:4}[slot];sp=self.cpu()['ESP'];bp=self.cpu()['EBP'];ret=word(self.read(sp));args=[word(self.read(sp+4+j)) for j in range(0,pop,4)];maps=[];out=[];extra={}
  def put(p,b):out.append(dict(pointer=p,hex=b.hex()))
  if slot==80:
   index=len(self.opening_textures);service=self.offscreen;cfg=geometry(service.measured);dims=[1<<(v-1).bit_length() for v in cfg['texture_size']];record=args[7]-44;need(index<10 and args==[self.device,*dims,1,0,25,1,record+44] and ret==0x403c8a,'original remaining dialogue CreateTexture');op='create';req=dict(width=dims[0],height=dims[1],levels=1,usage=0,format=25,pool=1);native=self.opening_gpu.create(*dims);result=self.opening_space.result('opening',native);t=result['texture'];r=dict(index=index,font_index=len(self.opening_fonts)-1,record=record,width=dims[0],height=dims[1],texture=t,native_pointer=native['texture']['pointer'],phase=0,live=True);self.opening_textures.append(r);raw=service.gdi.raster(service.bitmap);self.opening_fonts[-1]['raster_record']=dict(ACP=service.gdi.acp,measured=service.measured,selected_face=service.face,font=service.font,bitmap=service.bitmap,raster_dc=service.raster_dc,logical_measurement_dc=service.logical,fresh_owned_measurement_dc=service.actual,stages=copy.deepcopy(service.stages),raster_hex=raw.hex(),raster_sha256=sha(raw))
   for k,p in t['methods'].items():self.opening_methods[p]=int(k);self.third_methods.add(p)
   for p in (t['pointer'],t['vtable'],*t['methods'].values()):
    lo=p&~4095
    if not any(a<=lo<=b for a,b,_ in self.u.mem_regions()) and (lo,4096) not in maps:maps.append((lo,4096))
   put(t['pointer'],struct.pack('<I',t['vtable']))
   for k,p in t['methods'].items():put(t['vtable']+int(k),struct.pack('<I',p))
   put(args[7],struct.pack('<I',t['pointer']))
  else:
   found=[r for r in self.opening_textures if r['texture']['pointer']==args[0] and r['live']];need(len(found)==1,'unique current dialogue texture owner');r=found[0];t=r['texture'];p=r['native_pointer'];index=r['index']
   if slot==56:need(args==[t['pointer'],0,bp-(52 if ret==0x403cbe else 36)] and ret in (0x403cbe,0x403a44),'source whole dialogue descriptor');op='describe';req=dict(pointer=p);native=self.opening_gpu.describe(p);result=copy.deepcopy(native);put(args[2],bytes.fromhex(result['hex']))
   elif slot==64:
    need(ret==0x40395e and args==[t['pointer'],0,word(self.read(bp+8)),0,2048],'source whole dialogue lock');op='lock';req=dict(pointer=p,flags=2048);native=self.opening_gpu.lock(p);result=self.opening_space.result('opening',native);r['lock']=result;b=bytes.fromhex(result['hex']);lo=result['bits']&~4095;maps=[(lo,(result['bits']-lo+len(b)+4095)&~4095)];put(result['bits'],b);put(args[2],struct.pack('<2I',result['pitch'],result['bits']))
   elif slot==68:
    need(ret==0x4039d3 and args==[t['pointer'],0],'source whole dialogue unlock');raw=self.read(r['lock']['bits'],len(bytes.fromhex(r['lock']['hex'])));op='unlock';req=dict(pointer=p,hex=raw.hex());native=self.opening_gpu.unlock(p,raw);result=copy.deepcopy(native);r.update(uploaded_hex=raw.hex(),uploaded_sha256=sha(raw));extra['uploaded_hex']=raw.hex()
   else:need(slot==8 and ret==0x40378d and args==[t['pointer']],'source dialogue release');op='release';req=dict(pointer=p);native=self.opening_gpu.release(p);result=copy.deepcopy(native);r['live']=False
  need(slot==[80,56,64,68,56,8][r['phase']],'six ordered source calls per dialogue texture');value=result['count'] if slot==8 else result['hr'];need(value==0,'successful actual remaining dialogue resource');row=dict(kind='actual_opening_GPU',index=self.opening_gpu_count,object_index=index,phase=r['phase'],slot=slot,target=at,sp=sp,return_va=ret,pop=pop,args=args,value=value,native_op=op,native_request=req,native_result=native,result=result,native_wire_index=len(self.opening_gpu.trace)-1,new_mappings=[dict(pointer=p,bytes=n) for p,n in maps],memory_outputs=out,**extra)
  for p,n in maps:need(all(not(a<p+n and p<=b) for a,b,_ in self.u.mem_regions()),'fresh dialogue interface/surface mapping');self.u.mem_map(p,n)
  self.memory_evidence.refresh()
  for o in out:self.u.mem_write(o['pointer'],bytes.fromhex(o['hex']));self.memory_evidence.mark(o['pointer'],len(bytes.fromhex(o['hex'])))
  self.memory_evidence.refresh();self.api_calls.append(row);r['phase']+=1;self.opening_gpu_count+=1;self.u.reg_write(base.REGISTERS['EAX'],value);self.u.reg_write(base.REGISTERS['ESP'],sp+4+pop);self.u.reg_write(base.REGISTERS['EIP'],ret)
  if slot==68:r['readback']=self.opening_gpu.readback(r['native_pointer']);need(r['readback']['hex']==r['uploaded_hex'],'whole actual remaining dialogue GPU readback')
 def opening_step(self,label,root=None,stop=RETURN):
  decoded=[]
  def source(u,at,n,_):
   if at==0x4ce9c5:
    pc=word(self.read(VM+28));p=word(self.read(self.cpu()['EBP']-8));op,size=struct.unpack('<2H',self.read(p,4));decoded.append(dict(PC=pc,opcode=op,size=size,pointer=p,hex=self.read(p,size).hex()))
  hook=self.u.hook_add(UC_HOOK_CODE,source)
  try:s=self.advance_new(label,stop,root)
  finally:self.u.hook_del(hook)
  s.update(opening_state=state(self),decoded=decoded);return s
 def opening_frame(self,label):
  steps=[]
  for va,recv in ((0x425de0,task.INPUT),(0x40db90,task.MANAGER),(0x40dc80,task.MANAGER),(0x454cf0,task.TACT)):
   steps.append(self.opening_step(label+'_'+hex(va),root=dict(va=va,receiver=recv,args=[],sp=STACK,return_va=RETURN)))
  r=dict(label=label,steps=steps,state=state(self));print('opening',label,r['state']['PC'],r['state']['wait'],r['state']['opcode'],flush=True);return r
 def continue_opening(self):
  need(state(self)['PC']==332 and state(self)['wait']==0,'natural whole opening entry');old_service=self.offscreen;self.opening_running=True;self.opening_fonts=[];self.opening_services=[];self.opening_textures=[];self.opening_methods={};self.opening_parent_calls=[];self.opening_space=previous.previous.AddressSpace();self.opening_space.next=0x6f001000;self.opening_gpu=previous.previous.ImageD3D8(self.opening_gpu_helper);self.opening_gpu_count=0;self.opening_historical={};before=state(self);entry=base.architectural_cpu(self.u);frames=[];bindings=[]
  nc,nl,_=old_name.mapped_texture();n=name_catalog.contracts()[1];self.opening_historical[nc['texture']['pointer']]=dict(owner='historical_name4',texture=nc['texture'],descriptor=n['COM_calls'][1]['result'],source=name_catalog.contracts()[2],phase=4)
  p=base.inputs()['parents'][self.confirm_branch];parent=json.loads(gzip.decompress(base.pinned(p['path'],p['sha256'])))['case'];creates=[r for r in parent['device_proxy_trace'] if r['op']=='text_create'];t=creates[1]['result']['texture'];desc=next(r['result'] for r in parent['device_proxy_trace'] if r['op']=='text_desc' and r['request']['pointer']==t['pointer']);self.opening_historical[t['pointer']]=dict(owner='historical_second_text',texture=t,descriptor=desc,source=p,phase=4)
  for r in self.opening_historical.values():self.third_methods.update(r['texture']['methods'].values())
  self.third_methods.update(self.texture['methods'].values())
  try:
   completed_confirms=set();controls={};release=False
   for i in range(500):
    now=state(self)
    if now['PC'] in (362,412) and now['wait']==1:
     pc=now['PC'];controls[pc]=controls.get(pc,0)+1
     if controls[pc]==3:
      stream=keyboard.contracts()['streams'][str(self.opening_scene)];bindings.append(self.captured(stream['captures'][1]));release=True;completed_confirms.add(pc)
    elif release:
     stream=keyboard.contracts()['streams'][str(self.opening_scene)];bindings.append(self.captured(stream['captures'][2]));release=False
    f=self.opening_frame('frame_'+str(i));frames.append(f)
    if any(d['opcode']==19 for d in f['steps'][-1]['decoded']):break
   else:raise ValueError('bounded remaining opening task sequence')
   need(completed_confirms=={362,412},'both original confirmations reached');final=state(self);memory=base.memory_rows(self.u);need(memory==frames[-1]['steps'][-1]['full_memory'],'whole final opening byte rehash');out=dict(contract=contracts(),before=before,entry_architectural_cpu=entry,frames=frames,bindings=bindings,fonts=copy.deepcopy(self.opening_fonts),textures=copy.deepcopy(self.opening_textures),historical=copy.deepcopy(list(self.opening_historical.values())),parent_GPU_calls=copy.deepcopy(self.opening_parent_calls),typed_projection=self.opening_space.ledger(),final=final,final_memory=memory,final_architectural_cpu=base.architectural_cpu(self.u),GPU_hello=self.opening_gpu.hello,GPU_build=self.opening_gpu_build,new_VM_roots=0,PC_or_wait_host_writes=0,new_OS_input=False)
   self.opening_role_adjustment=327680;self.opening_fourth_adjustment=319488;self.opening_third_adjustment=286720;self.opening_done=True;return out
  finally:
   self.opening_running=False;self.offscreen=old_service;cleanup=self.opening_gpu.close();gd=[s.close() for s in self.opening_services];self.opening_cleanup=dict(GPU=cleanup,GPU_exit=self.opening_gpu.process.returncode,GPU_trace=copy.deepcopy(self.opening_gpu.trace),GDI=gd)

def run_case(helper,build,gpu,gpubuild,role_gpu,rolebuild,opening_gpu,openingbuild,name,scene):
 instances=[]
 class Attached(Guest):
  def __init__(self,*args):
   super().__init__(*args);self.gpu_helper=gpu;self.gpu_build=gpubuild;self.role_gpu_helper=role_gpu;self.role_gpu_build=rolebuild;self.opening_gpu_helper=opening_gpu;self.opening_gpu_build=openingbuild;self.confirm_branch=name;self.opening_scene=scene;instances.append(self)
 call=adapt(task.run_case,[("word(g.read(0x765720))==accounting","word(g.read(0x765720))==accounting-getattr(g,'replaced_texture_bytes',0)-(24576 if getattr(g,'opening_done',False) else 0)")],Guest=Attached)
 try:c=call(helper,build,name,scene)
 except BaseException as exc:
  if instances:
   g=instances[0];p=ROOT/('analysis/school-retained-opening-failed-'+helper.stem+'-'+name+'-'+str(scene)+'-20261023.json.gz');need(not p.exists(),'fresh opening failure');p.write_bytes(gzip.compress(json.dumps(dict(accepted=False,error=repr(exc),CPU=g.cpu(),state=state(g),native_trace=g.live.trace,CRT_exit=g.live.process.returncode,CRT_cleanup=g.live.cleanup,opening_cleanup=getattr(g,'opening_cleanup',None),fonts=getattr(g,'opening_fonts',[]),textures=getattr(g,'opening_textures',[]),parent_GPU_calls=getattr(g,'opening_parent_calls',[])),separators=(',',':')).encode(),mtime=0))
  raise
 g=instances[0];c.update(third_dialogue=g.third_record,third_confirmation=g.confirm_record,fourth_texture=g.fourth_record,role9=g.role9_record,opening=dict(g.opening_record,**g.opening_cleanup));return c
