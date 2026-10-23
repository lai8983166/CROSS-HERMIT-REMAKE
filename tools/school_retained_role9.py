"""Complete source role9 name, actual portrait textures and original task readiness."""
import copy,gzip,json,struct,types
from functools import lru_cache
from tools import school_retained_fourth_texture as previous
from tools import school_retained_third_dialogue as dialogue
from tools import school_retained_character_task as task
from tools import school_crt_init_fixture as crt
from tools.school_character_image_file import WindowsImageFile
from tools.school_retained_portrait_file_catalog import parse
from tools.school_retained_portrait_file_verification import chain
from tools.school_font_raster_catalog import geometry
from unicorn import UC_HOOK_CODE

ROOT=previous.ROOT;base=previous.base;need=previous.need;word=previous.word;sha=previous.sha;canonical=previous.canonical
ACCEPTANCE='analysis/school-retained-fourth-texture-acceptance-v1-20261023.json'
ACCEPTANCE_SHA='b54ab995b052bc737f8be34dbe428fb75169e8c85628644c07c34631cb1a4162'
VM=base.VM;NODE=VM+0x6f60+4*0xe0;OBJECT=VM+0x430+4*0xab8;TEXTURE=NODE+0x60;RASTER=0x3b000000;STACK=previous.STACK;RETURN=previous.RETURN
FILE_SLOTS={0x5921ec:('CreateFileA',28),0x5921f0:('GetFileSize',8),0x5921e8:('ReadFile',20),0x592270:('CloseHandle',4)}
NAME_GDI=dict(dialogue.GDI);NAME_GDI[task.FONT_SLOT]=('CreateFontA',0x4ca7cb,56)

@lru_cache(maxsize=1)
def contracts():
 a=json.loads(base.pinned(ACCEPTANCE,ACCEPTANCE_SHA));need(a['final_PC']==312 and a['role_index']==9 and a['role9_font_executed']is False and a['tasks_complete']==3,'accepted natural role9 font entry');old=previous.contracts();role=old['role9'];raw=(ROOT/role['image_path']).read_bytes();need(sha(raw)==role['image_sha256'],'complete source SC009 identity');return dict(parent_acceptance=ACCEPTANCE,parent_acceptance_sha256=ACCEPTANCE_SHA,previous=old,role=role,configuration=old['configuration7'],image=parse(raw),mode='original role9 resources/task/readiness; fresh GDI and independent owned name/portrait GPU domain; separately bound actual read-only SC009')

def asset():return (ROOT/contracts()['role']['image_path']).read_bytes()

class Files(WindowsImageFile):
 open=types.FunctionType(WindowsImageFile.open.__code__,dict(WindowsImageFile.open.__globals__,RESOURCE=ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/ADV/BIN/SC009.BIN'),'source_bound_SC009_open')
 read=types.FunctionType(WindowsImageFile.read.__code__,dict(WindowsImageFile.read.__globals__,RESOURCE_SHA='3a647f12dc0a828ccaaa888f5a2d64b9832ee82e519db7a9ee326cccfa87d060'),'source_bound_SC009_read')

class Offscreen(dialogue.Offscreen):
 call_raster=types.FunctionType(dialogue.Offscreen.call_raster.__code__,dict(dialogue.Offscreen.call_raster.__globals__,RASTER=RASTER),'owned_role9_name_raster')

def state(g):
 result=previous.state(g);result.update(role_node_hex=g.read(NODE,224).hex(),role_text_hex=g.read(OBJECT,0xab8).hex(),loaded_flag=g.read(VM+0x92a0+30,1).hex(),image_table_hex=g.read(g.renderer+0x844+30*8,8).hex());return result

class Guest(previous.Guest):
 name_api=types.FunctionType(dialogue.Guest.new_api.__code__,dict(dialogue.Guest.new_api.__globals__,RASTER=RASTER,GDI=NAME_GDI),'actual_original_role9_GDI')
 def new_root(self,label,va,recv):
  if label=='supplemental_original_fourth_texture_destructor':self.role9_record=self.continue_role9()
  return super().new_root(label,va,recv)
 def new_api(self,slot):
  if not getattr(self,'role_running',False):return super().new_api(slot)
  if slot in FILE_SLOTS:self.role_file_api(slot)
  elif slot in dialogue.GDI and not(slot==task.LENGTH_SLOT and word(self.read(self.cpu()['ESP']))==0x425a7e):
   self.name_api(slot)
   if self.api_calls[-1]['kind']=='actual_owned_third_GDI':self.api_calls[-1]['kind']='actual_role9_GDI'
   return
  else:
   self.task_api(slot)
   if self.api_calls[-1].get('kind')!='recorded_task_platform':self.api_calls[-1]['kind']='actual_role9_CRT'
  self.memory_evidence.refresh()
  for o in self.api_calls[-1]['memory_outputs']:self.memory_evidence.mark(o['pointer'],len(bytes.fromhex(o['hex'])))
 def role_file_api(self,slot):
  name,pop=FILE_SLOTS[slot];sp=self.cpu()['ESP'];ret=word(self.read(sp));args=[word(self.read(sp+4+i)) for i in range(0,pop,4)];outputs=[];extra={};i=len(self.role_file_trace);need(i<4 and name==['CreateFileA','GetFileSize','ReadFile','CloseHandle'][i],'one exact source SC009 file lifecycle')
  if i==0:
   path=crt.old.text(self,args[0]);need(path==b'data\\adv\\bin\\sc009.bin' and ret==0x42ac9c,'natural original SC009 relative path');value=self.role_files.open(args[1:]);extra['source_relative_path_hex']=path.hex()
  elif i==1:need(ret==0x42ad0d and args[1]==0,'original SC009 size caller');value=self.role_files.size(args[0])
  elif i==2:
   need(ret==0x42ad82 and args[2]==262168 and args[4]==0,'original synchronous whole SC009 read');p,entry=self.owned(args[1],args[2]);need(args[1]==p+32,'original source file user buffer');raw=self.role_files.read(args[0],args[2]);need(raw==asset(),'entire actual read equals fixed installed/private SC009');outputs=[dict(pointer=args[1],hex=raw.hex()),dict(pointer=args[3],hex=struct.pack('<I',len(raw)).hex())];extra.update(file_sha256=sha(raw),bytes_read=len(raw),source_allocation=p);value=1;self.role_file_buffer=args[1]
  else:need(ret==0x42ada5,'original SC009 CloseHandle caller');value=self.role_files.release(args[0])
  for o in outputs:self.u.mem_write(o['pointer'],bytes.fromhex(o['hex']))
  row=dict(kind='actual_role9_file',name=name,index=i,import_slot=slot,target=word(self.read(slot)),sp=sp,return_va=ret,pop=pop,args=args,value=value,new_mappings=[],memory_outputs=outputs,**extra);self.role_file_trace.append(copy.deepcopy(row));self.api_calls.append(row);self.u.reg_write(base.REGISTERS['EAX'],value);self.u.reg_write(base.REGISTERS['ESP'],sp+4+pop);self.u.reg_write(base.REGISTERS['EIP'],ret)
 def new_gpu(self,at):
  if not getattr(self,'role_running',False) or at not in {self.device_method,*getattr(self,'role_methods',{})}:return super().new_gpu(at)
  slot=80 if at==self.device_method else self.role_methods[at];pop={80:32,56:12,64:20,68:8,8:4}[slot];sp=self.cpu()['ESP'];bp=self.cpu()['EBP'];ret=word(self.read(sp));args=[word(self.read(sp+4+j)) for j in range(0,pop,4)];need(ret=={80:0x403c8a,64:0x40395e,68:0x4039d3,8:0x40378d}.get(slot,ret) and (slot!=56 or ret in (0x403cbe,0x403a44)),'original role9 COM caller');maps=[];outputs=[];extra={}
  def put(p,b):outputs.append(dict(pointer=p,hex=b.hex()))
  if slot==80:
   index=len(self.role_textures);need(index<2,'two actual role9 textures');w,h=args[1:3];receiver=TEXTURE if index==0 else self.role_image_record;expected=[1<<(x-1).bit_length() for x in geometry(self.role_service.measured)['texture_size']] if index==0 else [256,512];need(args==[self.device,*expected,1,0,25,1,receiver+44],'full original role9 name/portrait CreateTexture ABI');op='create';request=dict(width=w,height=h,levels=1,usage=0,format=25,pool=1);native=self.role_gpu.create(w,h);result=self.role_space.result('role9',native);t=result['texture'];r=dict(index=index,record=receiver,width=w,height=h,texture=t,native_pointer=native['texture']['pointer'],phase=0,live=True);self.role_textures.append(r)
   for k,p in t['methods'].items():self.role_methods[p]=int(k);self.third_methods.add(p)
   for p in (t['pointer'],t['vtable'],*t['methods'].values()):
    page=p&~4095
    if not any(a<=page<=b for a,b,_ in self.u.mem_regions()) and (page,4096) not in maps:maps.append((page,4096))
   put(t['pointer'],struct.pack('<I',t['vtable']))
   for k,p in t['methods'].items():put(t['vtable']+int(k),struct.pack('<I',p))
   put(args[7],struct.pack('<I',t['pointer']))
  else:
   found=[r for r in self.role_textures if r['texture']['pointer']==args[0] and r['live']];need(len(found)==1,'current uniquely owned role9 texture');r=found[0];t=r['texture'];index=r['index'];p=r['native_pointer']
   if slot==56:need(args==[t['pointer'],0,bp-(52 if ret==0x403cbe else 36)],'original role9 descriptor destination');op='describe';request=dict(pointer=p);native=self.role_gpu.describe(p);result=copy.deepcopy(native);put(args[2],bytes.fromhex(result['hex']))
   elif slot==64:
    need(args==[t['pointer'],0,word(self.read(bp+8)),0,2048],'original role9 lock ABI');op='lock';request=dict(pointer=p,flags=2048);native=self.role_gpu.lock(p);result=self.role_space.result('role9',native);r['lock']=result;b=bytes.fromhex(result['hex']);lo=result['bits']&~4095;maps=[(lo,(result['bits']-lo+len(b)+4095)&~4095)];put(result['bits'],b);put(args[2],struct.pack('<2I',result['pitch'],result['bits']))
   elif slot==68:
    need(args==[t['pointer'],0],'original role9 unlock ABI');op='unlock';raw=self.read(r['lock']['bits'],len(bytes.fromhex(r['lock']['hex'])));request=dict(pointer=p,hex=raw.hex());native=self.role_gpu.unlock(p,raw);result=copy.deepcopy(native);r.update(uploaded_hex=raw.hex(),uploaded_sha256=sha(raw));extra['uploaded_hex']=raw.hex()
   else:need(slot==8 and args==[t['pointer']],'original role9 Release ABI');op='release';request=dict(pointer=p);native=self.role_gpu.release(p);result=copy.deepcopy(native);r['live']=False
  need(slot==[80,56,64,68,56,8][r['phase']],'ordered original six interfaces per role9 texture');value=result['count'] if slot==8 else result['hr'];need(value==0,'actual role9 GPU successful result');row=dict(kind='actual_role9_GPU',index=self.role_gpu_count,object_index=index,phase=r['phase'],slot=slot,target=at,sp=sp,return_va=ret,pop=pop,args=args,value=value,native_op=op,native_request=request,native_result=native,result=result,new_mappings=[dict(pointer=p,bytes=n) for p,n in maps],memory_outputs=outputs,**extra)
  for p,n in maps:need(all(not(a<p+n and p<=b) for a,b,_ in self.u.mem_regions()),'fresh source role9 interface or surface page');self.u.mem_map(p,n)
  for o in outputs:self.u.mem_write(o['pointer'],bytes.fromhex(o['hex']))
  self.memory_evidence.refresh()
  for o in outputs:self.memory_evidence.mark(o['pointer'],len(bytes.fromhex(o['hex'])))
  r['phase']+=1;self.role_gpu_count+=1;self.api_calls.append(row);self.u.reg_write(base.REGISTERS['EAX'],value);self.u.reg_write(base.REGISTERS['ESP'],sp+4+pop);self.u.reg_write(base.REGISTERS['EIP'],ret)
 def role_step(self,label,stop=RETURN,root=None):
  first=len(self.role_copy_rows)
  def row_hook(u,at,n,_):
   if at!=0x56d4d0:return
   sp=self.cpu()['ESP']
   if word(self.read(sp))!=0x40483f:return
   row=len(self.role_copy_rows);args=[word(self.read(sp+4+i)) for i in (0,4,8)];lock=self.role_textures[1]['lock'];need(row<512 and args==[lock['bits']+row*lock['pitch'],self.role_file_buffer+24+row*512,512],'all original SC009 memcpy row arguments');self.role_copy_rows.append(dict(row=row,args=args,return_va=0x40483f))
  hook=self.u.hook_add(UC_HOOK_CODE,row_hook)
  try:result=self.advance_new(label,stop,root)
  finally:self.u.hook_del(hook)
  result.update(role_state=state(self),copy_rows=copy.deepcopy(self.role_copy_rows[first:]));return result
 def role_frame(self,index):
  steps=[self.role_step('role9_request_'+str(index),root=dict(va=0x425de0,receiver=task.INPUT,args=[],sp=STACK,return_va=RETURN))]
  for va in (0x40db90,0x40dc80):steps.append(self.role_step('role9_queue_'+str(index)+'_'+hex(va),root=dict(va=va,receiver=task.MANAGER,args=[],sp=STACK,return_va=RETURN)))
  steps.append(self.role_step('role9_complete_task_'+str(index),root=dict(va=0x454cf0,receiver=task.TACT,args=[],sp=STACK,return_va=RETURN)));return dict(index=index,steps=steps,state=state(self))
 def continue_role9(self):
  contracts();need(self.cpu()['EIP']==word(self.read(task.FONT_SLOT)) and previous.state(self)['PC']==312,'natural role9 font entry in current lifetime');old_service=self.offscreen;old_fourth_running=self.fourth_running;self.role_service=Offscreen(word(self.read(self.renderer+0xb208)));self.role_gpu=previous.ImageD3D8(self.role_gpu_helper);self.role_files=Files();self.role_file_trace=[];self.role_textures=[];self.role_methods={};self.role_space=previous.AddressSpace();self.role_space.next=0x6e001000;self.role_gpu_count=0;self.role_copy_rows=[];self.offscreen=self.role_service;self.role_running=True;before=state(self);entry=base.architectural_cpu(self.u);account=word(self.read(0x765720));game_bytes=word(self.read(0x79fc74));fourth_trace_count=len(self.fourth_gpu.trace);fourth_pixels=self.read(self.fourth_lock['bits'],len(self.fourth_uploaded));out=None
  try:
   name=self.role_step('continuous_original_role9_name_font_raster',0x403bd0);gd=self.role_service;raw=gd.gdi.raster(gd.bitmap);sp=self.cpu()['ESP'];font_frames=[('name',0x4cc1de),('layer',0x4c62d4),('handler',0x4ceda7),('VM',0x454d90),('task',RETURN)];pending_name=dict(va=0x403bd0,receiver=self.cpu()['ECX'],args=[word(self.read(sp+4)),word(self.read(sp+8))],return_va=word(self.read(sp)),frames=chain(self,[('raster',0x408e81),('texture_wrapper',0x4ca82c),*font_frames]),first_instruction_executed=False);need(pending_name['receiver']==TEXTURE and pending_name['args']==[self.device,0] and pending_name['return_va']==0x405779,'natural role9 name texture entry');raster=dict(ACP=gd.gdi.acp,measured=gd.measured,selected_face=gd.face,font=gd.font,bitmap=gd.bitmap,raster_dc=gd.raster_dc,logical_measurement_dc=gd.logical,fresh_owned_measurement_dc=gd.actual,stages=copy.deepcopy(gd.stages),raster_hex=raw.hex(),raster_sha256=sha(raw));name_upload=self.role_step('continuous_original_role9_name_texture_to_IMAGE',0x4cde10);sp=self.cpu()['ESP'];image_entry=dict(va=0x4cde10,receiver=self.cpu()['ECX'],args=[word(self.read(sp+4)),word(self.read(sp+8))],return_va=word(self.read(sp)),frames=chain(self,[('resource',0x4cc26d),*font_frames[1:]]),first_instruction_executed=False);need(image_entry['receiver']==VM and image_entry['args'][1]==30 and image_entry['return_va']==0x4cc0d2 and crt.old.text(self,image_entry['args'][0])==b'data\\adv\\bin\\sc009.bin','source natural role9 SC009 slot30 loader entry');self.role_textures[0]['readback']=self.role_gpu.readback(self.role_textures[0]['native_pointer']);need(self.role_textures[0]['readback']['hex']==self.role_textures[0]['uploaded_hex'],'actual name whole readback')
   image_prefix=self.role_step('continuous_original_SC009_read_allocate_construct',0x403bd0);self.role_image_record=word(self.read(self.renderer+0x844+30*8));need(len(self.history)==4 and self.role_image_record==self.history[-1]['guest']+36 and self.read(self.role_file_buffer,262168)==asset(),'complete original SC009 and registered new vector');file_p=self.history[-2]['guest'];array_p=self.history[-1]['guest'];file_record=dict(file_buffer=self.role_file_buffer,array=array_p+32,record=self.role_image_record,file_hex=self.read(self.role_file_buffer,262168).hex(),record_hex=self.read(self.role_image_record,84).hex(),table_hex=self.read(self.renderer+0x844+30*8,8).hex(),frames=chain(self,[('dx',0x41f3e0),('entry',0x41f25a),('container',0x41f0c9),('container_wrapper',0x41684b),('extended_register',0x4167bf),('register',0x4cde8a),('image',0x4cc0d2),('resource',0x4cc26d),*font_frames[1:]]));readbacks=[]
   for p in (file_p,array_p):
    self.sync(p);reply=self.live.request('readback',pointer=self.allocations[p]['native']);need(reply['hex']==self.read(p,self.allocations[p]['bytes']).hex(),'complete actual native SC009/vector bytes');readbacks.append(dict(guest=p,wire_index=len(self.live.trace)-1,result=reply))
   image=self.role_step('continuous_original_SC009_pixels_free_and_IMAGE_return',0x4cc0d2);need(len(self.role_copy_rows)==512 and len(self.role_textures)==2 and self.role_gpu_count==8 and file_p not in self.allocations and list(self.allocations)==[0x50201000,array_p],'source SC009 full copy and natural file free');self.role_textures[1]['readback']=self.role_gpu.readback(self.role_textures[1]['native_pointer']);need(self.role_textures[1]['readback']['hex']==self.role_textures[1]['uploaded_hex'],'actual portrait whole readback');complete=self.role_step('continuous_original_role9_handler_and_complete_task');need(self.cpu()['EIP']==RETURN and self.cpu()['ESP']==STACK+4 and previous.state(self)['PC']==332,'role9 full task returns naturally after op30');frames=[]
   for i in range(200):
    s=previous.state(self)
    if s['PC']==332 and s['wait']==0:break
    need(s['PC']==332 and s['wait']==1,'hold only original role9 readiness');f=self.role_frame(i);frames.append(f)
    if i%20==0:print('role9 natural wait',i,previous.state(self),flush=True)
   else:raise ValueError('bounded original role9 natural readiness')
   final_memory=base.memory_rows(self.u);last=frames[-1]['steps'][-1] if frames else complete;need(final_memory==last['full_memory'],'fresh entire role9 boundary rehash');need(self.read(self.fourth_lock['bits'],len(fourth_pixels))==fourth_pixels and len(self.fourth_gpu.trace)==fourth_trace_count and not self.fourth_gpu.closed,'fourth texture domain remains alive and untouched');out=dict(contract=contracts(),before=before,entry_architectural_cpu=entry,name=name,raster=raster,pending_name_texture=pending_name,name_upload=name_upload,pending_image=image_entry,image_prefix=image_prefix,image_record=file_record,native_allocation_readbacks=readbacks,image=image,completion=complete,frames=frames,final=state(self),final_memory=final_memory,final_architectural_cpu=base.architectural_cpu(self.u),textures=copy.deepcopy(self.role_textures),typed_projection=self.role_space.ledger(),copy_rows=copy.deepcopy(self.role_copy_rows),file_trace=copy.deepcopy(self.role_file_trace),accounting_before=account,accounting_with_role=word(self.read(0x765720)),game_bytes_before=game_bytes,game_bytes_with_role=word(self.read(0x79fc74)),fourth_domain_retained=True,fourth_trace_count_before=fourth_trace_count,fourth_trace_count_after=len(self.fourth_gpu.trace),fourth_surface_sha256=sha(fourth_pixels),GPU_hello=self.role_gpu.hello,GPU_build=self.role_gpu_build,role9_complete_task_returned=True,role9_naturally_ready=True,next_script_instruction_executed=False,new_VM_roots=0,input_host_writes=0,PC_or_wait_host_writes=0)
   root=dict(va=0x41f4e0,receiver=self.renderer+0x844,args=[30],sp=STACK,return_va=RETURN);photo_cleanup=self.role_step('supplemental_original_role9_image_container_cleanup',root=root);name_cleanup=self.role_step('supplemental_original_role9_name_texture_cleanup',root=dict(va=0x403730,receiver=TEXTURE,args=[],sp=STACK,return_va=RETURN));need(self.role_gpu_count==12 and list(self.allocations)==[0x50201000] and word(self.read(0x765720))==account and word(self.read(0x79fc74))==game_bytes,'source role9 image/vector/name cleanup and both accounting balances');out.update(image_cleanup=photo_cleanup,name_cleanup=name_cleanup,accounting_after_cleanup=word(self.read(0x765720)),game_bytes_after_cleanup=word(self.read(0x79fc74)),textures_after_cleanup=copy.deepcopy(self.role_textures))
  finally:
   self.role_running=False;self.offscreen=old_service;self.fourth_running=old_fourth_running;gpu_cleanup=self.role_gpu.close();file_cleanup=self.role_files.close();gdi_cleanup=self.role_service.close();self.role_cleanup=dict(GPU=gpu_cleanup,files=file_cleanup,GDI=gdi_cleanup,GPU_exit=self.role_gpu.process.returncode,GPU_trace=copy.deepcopy(self.role_gpu.trace),file_trace=copy.deepcopy(self.role_file_trace))
  out.update(self.role_cleanup);return out

def run_case(helper,build,gpu_helper,gpu_build,role_gpu_helper,role_gpu_build,name,scene):
 instances=[]
 class Attached(Guest):
  def __init__(self,*args):super().__init__(*args);self.role_gpu_helper=role_gpu_helper;self.role_gpu_build=role_gpu_build;instances.append(self)
 call=previous.previous.adapt_validation(previous.run_case,[("school-retained-fourth-texture-failed-run-","school-retained-role9-failed-CRT-")],Guest=Attached)
 try:c=call(helper,build,gpu_helper,gpu_build,name,scene)
 except BaseException as exc:
  if instances:
   g=instances[0];path=ROOT/('analysis/school-retained-role9-failed-platform-'+helper.stem+'-'+name+'-'+str(scene)+'-20261023.json.gz');need(not path.exists(),'fresh immutable role9 failure');path.write_bytes(gzip.compress(json.dumps(dict(accepted=False,error=repr(exc),CPU=g.cpu(),state=state(g),native_trace=g.live.trace,CRT_exit=g.live.process.returncode,CRT_cleanup=g.live.cleanup,role_cleanup=getattr(g,'role_cleanup',None)),separators=(',',':')).encode(),mtime=0))
  raise
 need(len(instances)==1 and hasattr(instances[0],'role9_record'),'one role9 continuation before fourth cleanup');c['role9']=instances[0].role9_record;return c

def run(helper,build,gpu_helper,gpu_build,role_gpu_helper,role_gpu_build):return dict(schema_version=1,contract=contracts(),cases=[run_case(helper,build,gpu_helper,gpu_build,role_gpu_helper,role_gpu_build,n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],new_GPU=True,new_hidden_windows=True,new_OS_input=False,actual_D3D_draw_or_Present=False,new_VM_roots=0,game_function_substitutions=0,IAT_rebindings=0,original_outer_scheduler=False,historical_heap_restored=False,R3_complete=False,R6_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable report')
 helper,build=crt.platform.build(ROOT/'.venv-audit/school-retained-role9-crt.exe');gpu,b=previous.build_gpu(ROOT/'.venv-audit/school-retained-role9-fourth.exe');role_gpu,rb=previous.build_gpu(ROOT/'.venv-audit/school-retained-role9-native.exe');r=run(helper,build,gpu,b,role_gpu,rb);out.write_bytes(gzip.compress(json.dumps(r,separators=(',',':')).encode(),mtime=0));print('six full original role9 resource/task/readiness cases',flush=True)
