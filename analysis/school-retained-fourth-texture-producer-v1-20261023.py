"""Original fourth text in a fresh native D3D8 lifetime, then role9 handoff."""
import copy,gzip,json,struct,types
from functools import lru_cache
from tools import school_retained_third_confirmation as previous
from tools.school_d3d8_image_bridge import ImageD3D8,build as build_gpu
from tools.school_retained_rendering import AddressSpace
from tools.school_retained_portrait_file_verification import chain

ROOT=previous.ROOT;base=previous.base;need=previous.need;word=previous.word;sha=previous.sha;canonical=previous.canonical
ACCEPTANCE='analysis/school-retained-third-confirmation-acceptance-v1-20261023.json'
ACCEPTANCE_SHA='285de3c932f229b7c19f2f6a40b5c7370b0f4e2cc8131f5e81e837169601372f'
TEXTURE=previous.TEXTURE;STACK=previous.STACK;RETURN=previous.RETURN

@lru_cache(maxsize=1)
def contracts():
 a=json.loads(base.pinned(ACCEPTANCE,ACCEPTANCE_SHA));need(a['final_PC']==306 and a['tasks_complete']==3 and a['fourth_texture_created']is False,'accepted actual fourth raster entry');return dict(parent_acceptance=ACCEPTANCE,parent_acceptance_sha256=ACCEPTANCE_SHA,previous=previous.contracts(),GPU_source='tools/school_d3d8_image_bridge.cs',GPU_source_sha256=sha((ROOT/'tools/school_d3d8_image_bridge.cs').read_bytes()),mode='new owned native fourth texture; original conversion and complete task; old GPU contracts retained; no draw/Present')

def state(g):return previous.state(g)

class Guest(previous.Guest):
 def continue_confirmation(self,scene):
  owner=self
  class AttachedOffscreen(previous.Offscreen):
   def close(service):
    if not getattr(service,'continuation_done',False) and owner.cpu()['EIP']==0x403bd0 and getattr(owner,'replaced_texture_bytes',0)==16384:
     service.continuation_done=True;old=(owner.offscreen,owner.fourth_running);owner.offscreen=service;owner.fourth_running=True
     try:owner.fourth_record=owner.continue_fourth(service)
     finally:owner.offscreen,owner.fourth_running=old
    return super().close()
  call=types.FunctionType(previous.Guest.continue_confirmation.__code__,dict(previous.Guest.continue_confirmation.__globals__,Offscreen=AttachedOffscreen),'original_fourth_before_actual_GDI_close');return call(self,scene)
 def new_gpu(self,at):
  if not getattr(self,'native_fourth_running',False) or at not in {self.device_method,*getattr(self,'fourth_methods',set())}:return super().new_gpu(at)
  i=self.fourth_gpu_count;slot=[80,56,64,68,56,8][i];pop={80:32,56:12,64:20,68:8,8:4}[slot];sp=self.cpu()['ESP'];bp=self.cpu()['EBP'];ret=word(self.read(sp));args=[word(self.read(sp+4+j)) for j in range(0,pop,4)];need(ret==[0x403c8a,0x403cbe,0x40395e,0x4039d3,0x403a44,0x40378d][i],'original actual fourth COM caller');maps=[];outputs=[];extra={};native_pointer=getattr(self,'fourth_native_pointer',None)
  def put(p,b):outputs.append(dict(pointer=p,hex=b.hex()))
  if i==0:
   need(at==self.device_method and args==[self.device,128,32,1,0,25,1,TEXTURE+44],'original fourth CreateTexture full ABI');op='create';request=dict(width=128,height=32,levels=1,usage=0,format=25,pool=1);native=self.fourth_gpu.create(128,32);result=self.fourth_space.result('fourth',native);t=result['texture'];self.fourth_texture=t;self.fourth_native_pointer=native['texture']['pointer'];self.fourth_methods=set(t['methods'].values());self.third_methods.update(self.fourth_methods);maps=list(dict.fromkeys((p&~4095,4096) for p in (t['pointer'],t['vtable'],*t['methods'].values())));put(t['pointer'],struct.pack('<I',t['vtable']))
   for k,p in t['methods'].items():put(t['vtable']+int(k),struct.pack('<I',p))
   put(args[7],struct.pack('<I',t['pointer']))
  else:
   t=self.fourth_texture;need(at==t['methods'][str(slot)] and args[0]==t['pointer'],'current owned fourth texture identity')
   if i in (1,4):need(args==[t['pointer'],0,bp-(52 if i==1 else 36)],'original fourth descriptor output');op='describe';request=dict(pointer=native_pointer);native=self.fourth_gpu.describe(native_pointer);result=copy.deepcopy(native);put(args[2],bytes.fromhex(result['hex']))
   elif i==2:
    need(args==[t['pointer'],0,word(self.read(bp+8)),0,2048],'original fourth lock ABI');op='lock';request=dict(pointer=native_pointer,flags=2048);native=self.fourth_gpu.lock(native_pointer);result=self.fourth_space.result('fourth',native);self.fourth_lock=result;b=bytes.fromhex(result['hex']);p=result['bits']&~4095;maps=[(p,(result['bits']-p+len(b)+4095)&~4095)];put(result['bits'],b);put(args[2],struct.pack('<2I',result['pitch'],result['bits']))
   elif i==3:
    need(args==[t['pointer'],0],'original fourth unlock ABI');op='unlock';raw=self.read(self.fourth_lock['bits'],len(bytes.fromhex(self.fourth_lock['hex'])));request=dict(pointer=native_pointer,hex=raw.hex());native=self.fourth_gpu.unlock(native_pointer,raw);result=copy.deepcopy(native);self.fourth_uploaded=raw;extra['uploaded_hex']=raw.hex()
   else:need(args==[t['pointer']],'original fourth Release ABI');op='release';request=dict(pointer=native_pointer);native=self.fourth_gpu.release(native_pointer);result=copy.deepcopy(native)
  value=result['count'] if i==5 else result['hr'];need(value==0,'actual fourth successful result');row=dict(kind='actual_owned_fourth_GPU',index=i,slot=slot,target=at,sp=sp,return_va=ret,pop=pop,args=args,value=value,native_op=op,native_request=request,native_result=native,result=result,new_mappings=[dict(pointer=p,bytes=n) for p,n in maps],memory_outputs=outputs,**extra)
  for p,n in maps:need(all(not(a<p+n and p<=b) for a,b,_ in self.u.mem_regions()),'fresh fourth interface/lock pages');self.u.mem_map(p,n)
  for o in outputs:self.u.mem_write(o['pointer'],bytes.fromhex(o['hex']))
  self.memory_evidence.refresh()
  for o in outputs:self.memory_evidence.mark(o['pointer'],len(bytes.fromhex(o['hex'])))
  self.api_calls.append(row);self.fourth_gpu_count+=1;self.u.reg_write(base.REGISTERS['EAX'],value);self.u.reg_write(base.REGISTERS['ESP'],sp+4+pop);self.u.reg_write(base.REGISTERS['EIP'],ret)
 def continue_fourth(self,service):
  contracts();before=state(self);entry_cpu=base.architectural_cpu(self.u);account=word(self.read(0x765720));self.fourth_gpu=ImageD3D8(self.gpu_helper);self.native_fourth_running=True;self.fourth_gpu_count=0;self.fourth_methods=set();self.fourth_space=AddressSpace();self.fourth_space.next=0x6d001000;out=None
  try:
   completed=self.advance_new('continuous_original_fourth_texture_handler_and_task');need(self.cpu()['EIP']==RETURN and self.cpu()['ESP']==STACK+4 and state(self)['PC']==312,'original fourth full task return');need(self.fourth_gpu_count==4 and word(self.read(0x765720))==account+8192,'four actual fourth calls and original resource accounting');readback=self.fourth_gpu.readback(self.fourth_native_pointer);need(bytes.fromhex(readback['hex'])==self.fourth_uploaded and readback['sha256']==sha(self.fourth_uploaded),'whole actual native fourth readback');font_target=word(self.read(previous.previous.parent.FONT_SLOT));role=self.confirmation_frame('role9_source_prefix',font_target);sp=self.cpu()['ESP'];font=dict(target=font_target,import_slot=previous.previous.parent.FONT_SLOT,args=[word(self.read(sp+4+i*4)) for i in range(14)],return_va=word(self.read(sp)),cpu=self.cpu(),frames=chain(self,[('font',0x4c4c34),('role',0x4cec2b),('vm',0x454d90),('task',RETURN)]),first_instruction_executed=False);memory=base.memory_rows(self.u);need(memory==role['steps'][-1]['full_memory'],'fresh all-byte role9 boundary');out=dict(contract=contracts(),before=before,entry_architectural_cpu=entry_cpu,completion=completed,actual_readback=readback,role_prefix=role,pending_font=font,final=state(self),final_memory=memory,final_architectural_cpu=base.architectural_cpu(self.u),accounting_before=account,accounting_with_fourth=word(self.read(0x765720)),texture=self.fourth_texture,lock=self.fourth_lock,uploaded_hex=self.fourth_uploaded.hex(),uploaded_sha256=sha(self.fourth_uploaded),GPU_hello=self.fourth_gpu.hello,GPU_build=self.gpu_build,typed_projection=self.fourth_space.ledger(),fourth_task_completed=True,role9_font_executed=False,role9_task_completed=False,new_VM_roots=0,input_host_writes=0,PC_or_wait_host_writes=0)
   cleanup=self.new_root('supplemental_original_fourth_texture_destructor',0x403730,TEXTURE);need(self.fourth_gpu_count==6 and word(self.read(0x765720))==account and word(self.read(TEXTURE+44))==0,'original fourth destruction, actual Release and balanced accounting');out.update(cleanup=cleanup,accounting_after_cleanup=word(self.read(0x765720)),GPU_trace=copy.deepcopy(self.fourth_gpu.trace))
  finally:
   self.native_fourth_running=False;cleanup=self.fourth_gpu.close()
  out.update(GPU_cleanup=cleanup,GPU_helper_exit=self.fourth_gpu.process.returncode);return out

def run_case(helper,build,gpu_helper,gpu_build,name,scene):
 instances=[]
 class Attached(Guest):
  def __init__(self,*args):super().__init__(*args);self.gpu_helper=gpu_helper;self.gpu_build=gpu_build;instances.append(self)
 call=previous.adapt_validation(previous.run_case,[("'analysis/school-retained-third-confirmation-failed-run-'","'analysis/school-retained-fourth-texture-failed-run-'")],Guest=Attached);c=call(helper,build,name,scene);need(len(instances)==1 and hasattr(instances[0],'fourth_record'),'one fourth continuation in source resource lifetime');c['fourth_texture']=instances[0].fourth_record;return c

def run(helper,build,gpu_helper,gpu_build):return dict(schema_version=1,contract=contracts(),cases=[run_case(helper,build,gpu_helper,gpu_build,n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],new_forward_VM_roots=0,game_function_substitutions=0,IAT_rebindings=0,new_OS_input=False,new_hidden_GPU_window=True,new_native_fourth_texture=True,actual_D3D_draw_or_Present=False,original_outer_scheduler=False,historical_heap_restored=False,role9_font_executed=False,role9_task_completed=False,R3_complete=False,R6_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--helper',required=True);p.add_argument('--gpu-helper',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable report')
 helper,build=previous.previous.parent.parent.old.init.platform.build(ROOT/a.helper);gpu_helper,gpu_build=build_gpu(ROOT/a.gpu_helper);r=run(helper,build,gpu_helper,gpu_build);out.write_bytes(gzip.compress(json.dumps(r,separators=(',',':')).encode(),mtime=0));print('six actual fourth textures and source role9 handoffs',flush=True)
