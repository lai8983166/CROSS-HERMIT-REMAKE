"""Reproduce original initialization -> retained VM -> actual rectangle/text GPU output."""
import argparse,gzip,hashlib,json,struct
from pathlib import Path
from PIL import Image
from tools.school_retained_rendering import *
from tools.school_retained_text_platform import RetainedTextGDI,StartupGDI
from tools.school_vm_graphics_verification import load_verified_checkpoint
from tools.school_world_mode_emulation import architectural_cpu

ROOT_RETURN=0x32000000
VM=0x7d7c28

class Pipeline:
 def __init__(self,e):self.e=e;self.steps=[]
 def resume(self,label,stop):
  r=self.e.continue_vm(stop)
  if r['pending'] or r['boundary']!=stop:raise RuntimeError('unhandled original '+label+': '+str(r['pending']))
  self.steps.append(dict(label=label,root=None,result=r));return r
 def root(self,label,va,receiver,args=(),stop=ROOT_RETURN):
  e=self.e;e.map_missing(ROOT_RETURN,4096);sp=0x2100f000
  e.uc.mem_write(sp,struct.pack('<'+'I'*(len(args)+1),ROOT_RETURN,*args))
  for k,v in dict(EIP=va,ESP=sp,ECX=receiver,EFLAGS=0x202).items():e.uc.reg_write(REGISTERS[k],v)
  r=self.resume(label,stop);self.steps[-1]['root']=dict(va=va,receiver=receiver,args=list(args),sp=sp,return_va=ROOT_RETURN)
  return r
 def reset(self):
  for va in (0x40db90,0x40dc80):self.root('original_queue_reset',va,TASK+0x1058)
 def frame(self,index):
  self.reset();r=self.root('bounded_original_VM_'+str(index),0x4ce8f0,VM)
  return dict(index=index,PC=self.e.read(VM+28),wait=struct.unpack('<H',self.e.uc.mem_read(VM+32,2))[0],original_instructions=sum(x['count'] for x in r['instruction_counts']))
 def render(self,out):
  e=self.e;queue=dict(heads=buffer_evidence(bytes(e.uc.mem_read(0x24001000,32768))),arena=buffer_evidence(bytes(e.uc.mem_read(0x25001000,1048576))))
  self.root('original_BeginScene_Clear_states',0x414c30,TASK)
  draw=self.root('original_queue_device_drawing',0x40e330,TASK+0x1058)
  self.root('original_EndScene',0x414de0,TASK,stop=0x414eaa)
  pixels=e.bridge.request('render_readback',pointer=e.objects['device']['pointer'])
  self.resume('original_Present_return',ROOT_RETURN)
  raw=bytes.fromhex(pixels['hex'])
  if hashlib.sha256(raw).hexdigest()!=pixels['sha256']:raise ValueError('actual framebuffer identity')
  im=Image.frombytes('RGB',(pixels['width'],pixels['height']),raw,'raw','BGRX',pixels['pitch'])
  out=Path(out)
  if out.exists():raise ValueError('fresh actual output image required')
  im.save(out);colors=im.getcolors(im.width*im.height)
  indexed=[a for a in draw['api_calls'] if a.get('key')=='device' and a.get('slot')==73]
  if not indexed or len(colors)<=3:raise ValueError('original visible character drawing required')
  return dict(queue=queue,pixels=buffer_evidence(raw),metadata={k:v for k,v in pixels.items() if k!='hex'},image=out.relative_to(ROOT).as_posix(),image_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),bbox=im.getbbox(),colors=len(colors),indexed_text_draws=len(indexed))

def run_case(name,image,frames=67):
 payload,checkpoint=load_verified_checkpoint(name,'rectangle')
 with owner_configuration() as configuration:
  with RenderingDevice() as native_device:
   with FinishGDI() as native_gdi:
    with RetainedTextGDI() as text:
     space=AddressSpace();db=MappedPlatform(native_device,space,'device');gp=StartupGDI(native_gdi,space,text)
     e=RetainedStartup(db,gp,0xa5);startup=initialize(e,db,gp)
     reconstruction=e.rehydrate(payload,checkpoint);prepared=e.prepare_rendering();e.bind_text(text)
     pipeline=Pipeline(e);pipeline.resume('retained_original_VM_return',0x454d90);pipeline.resume('retained_original_task_return',0x3000000)
     states=[]
     for i in range(frames):
      states.append(pipeline.frame(i))
      if i%20==0:print(name,'original VM',i,'PC',states[-1]['PC'],flush=True)
     output=pipeline.render(image)
     refusals=[]
     for op,request in [('render_call',dict(pointer=0,slot=34,args=[],buffers=[])),('text_create',dict(pointer=space.native('device',e.objects['device']['pointer']),width=256,height=32,levels=1,usage=0,format=21,pool=1))]:
      try:native_device.request(op,**request)
      except ValueError as exc:refusals.append(dict(op=op,request=request,observed_error=str(exc)))
      else:raise ValueError('owned protocol accepted invalid request')
     result=dict(name=name,source_sha256=SOURCE_SHA256,configuration=configuration,initialization=e.initialization_declaration,startup=startup,reconstruction=reconstruction,prepared=prepared,
      steps=pipeline.steps,frames=states,output=output,protocol_refusals=refusals,objects=e.objects,
      scope=dict(source_initialized_resource_reconstruction=True,new_bounded_original_VM_roots=frames,full_input_or_outer_world_frame=False,Godot=False,original_sprite_asset_textures_restored=False))
    result['text_GDI_cleanup']=text.cleanup;result['text_GDI_trace']=text.trace
   result['GDI_cleanup']=native_gdi.cleanup;result['GDI_process_exit_code']=native_gdi.process.returncode
  result['device_cleanup']=native_device.cleanup;result['device_process_exit_code']=native_device.process.returncode
 result.update(address_translation=space.ledger(),device_proxy_trace=db.trace,GDI_proxy_trace=gp.trace,native_device_trace=native_device.trace,native_GDI_trace=native_gdi.trace)
 if result['device_process_exit_code']!=0 or result['GDI_process_exit_code']!=0:raise RuntimeError('owned native helper must exit normally')
 if not result['device_cleanup']['all_owned_resources_released'] or not result['text_GDI_cleanup']['all_resources_released'] or any(result['device_cleanup'].get('text_texture_release_counts',[])):raise RuntimeError('full actual rendering lifetime cleanup')
 return result

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--case',choices=['initial','student9_waiting','fifth_class'],required=True);p.add_argument('--out',required=True);p.add_argument('--image',required=True);a=p.parse_args()
 out=ROOT/a.out
 if out.exists() or (ROOT/a.image).exists():p.error('fresh immutable report/image paths required')
 result=run_case(a.case,ROOT/a.image)
 out.write_bytes(gzip.compress(json.dumps(dict(schema_version=1,case=result),separators=(',',':')).encode(),mtime=0))
 print(a.case,'actual visible text, original Present, normal complete helper exit; report bytes',out.stat().st_size,flush=True)
