"""Original fog texture reconstruction and ordinary-loop upload to natural wait/dependency."""
import copy,gzip,json,struct
from functools import lru_cache
from tools import school_retained_world_loop as previous
from tools.school_d3d8_image_bridge import ImageD3D8,build as build_gpu
from tools.school_retained_rendering import AddressSpace

ROOT=previous.ROOT;base=previous.base;need=previous.need;sha=previous.sha;word=previous.word;canonical=previous.canonical
STACK=previous.STACK;RETURN=previous.RETURN;TACT=previous.TACT;MAP=TACT+0x3ef8;FOG=MAP+0x2650c
ACCEPTANCE='analysis/school-retained-world-loop-acceptance-v1-20261023.json'
ACCEPTANCE_SHA='6c9ba686bbfd1e037c770854e8874f821b48571074c4a9ec8e321732fc365dbe'
SPACE=0x60001000

@lru_cache(maxsize=1)
def contracts():
 a=json.loads(base.pinned(ACCEPTANCE,ACCEPTANCE_SHA));need(a['tasks_complete']==3 and a['map_texture_pointer']==0 and a['exact_fault_instruction']==0x56e3c5,'accepted actual map/fog gap');image=base.SOURCE.read_bytes();return dict(parent_acceptance=ACCEPTANCE,parent_acceptance_sha256=ACCEPTANCE_SHA,previous=previous.contracts(),original_resource_call_hex=image[0x440547-base.BASE:0x440563-base.BASE].hex(),original_query=0x4142b0,original_create=0x403bd0,record=FOG,source_size=[172,128],native_size=[256,128],format=25,typed_space=SPACE,GPU_source_sha256=sha((ROOT/'tools/school_d3d8_image_bridge.cs').read_bytes()),scope='two declared original resource roots; current actual fog GPU; original world/row copy/loop; supplemental original destructor; no outer scheduler or draw/Present')

def fog_state(g):
 p=word(g.read(MAP+0x2658c));w,h=struct.unpack('<2H',g.read(FOG+56,4));return dict(parent=previous.state(g),record_hex=g.read(FOG,128).hex(),source_pointer=p,source_width=w,source_height=h,source_hex=g.read(p,w*h*2).hex(),texture=word(g.read(FOG+44)),accounting=word(g.read(0x765720)))

class Guest(previous.Guest):
 loop_step=previous.previous.adapt(previous.Guest.loop_step,[("if at==self.device_method:frontier(","if at==self.device_method and not getattr(self,'fog_creating',False):frontier("),("if at in self.third_methods:self.new_gpu(at);return","if at==self.device_method or at in self.third_methods:self.new_gpu(at);return")])
 def new_gpu(self,at):
  if not getattr(self,'fog_active',False) or not(at==self.device_method and self.fog_creating or at in getattr(self,'fog_methods',set())):return super().new_gpu(at)
  sp=self.cpu()['ESP'];bp=self.cpu()['EBP'];ret=word(self.read(sp));phase={0x403c8a:0,0x403cbe:1,0x40395e:2,0x4039d3:3,0x403a44:4,0x40378d:5}.get(ret);need(phase is not None,'original current fog COM caller');slot=[80,56,64,68,56,8][phase];pop={80:32,56:12,64:20,68:8,8:4}[slot];args=[word(self.read(sp+4+j)) for j in range(0,pop,4)];outputs=[];maps=[];extra={};start=len(self.fog_gpu.trace)
  def put(p,b):outputs.append(dict(pointer=p,hex=b.hex()))
  if phase==0:
   need(self.fog_creating and at==self.device_method and args==[self.device,256,128,1,0,25,1,FOG+44],'original fog power-of-two geometry and full CreateTexture ABI');op='create';request=dict(width=256,height=128,levels=1,usage=0,format=25,pool=1);native=self.fog_gpu.create(256,128);result=self.fog_space.result('fog',native);self.fog_texture=result['texture'];self.fog_pointer=native['texture']['pointer'];self.fog_methods=set(self.fog_texture['methods'].values());self.third_methods.update(self.fog_methods);maps=list(dict.fromkeys((p&~4095,4096) for p in (self.fog_texture['pointer'],self.fog_texture['vtable'],*self.fog_methods)));put(self.fog_texture['pointer'],struct.pack('<I',self.fog_texture['vtable']))
   for k,p in self.fog_texture['methods'].items():put(self.fog_texture['vtable']+int(k),struct.pack('<I',p))
   put(FOG+44,struct.pack('<I',self.fog_texture['pointer']))
  else:
   t=self.fog_texture;need(at==t['methods'][str(slot)] and args[0]==t['pointer'],'same current fog native owner/interface')
   if phase in (1,4):
    need(args==[t['pointer'],0,bp-(52 if phase==1 else 36)],'original fog complete descriptor ABI');op='describe';request=dict(pointer=self.fog_pointer);native=self.fog_gpu.describe(self.fog_pointer);result=copy.deepcopy(native);put(args[2],bytes.fromhex(result['hex']))
   elif phase==2:
    need(args==[t['pointer'],0,word(self.read(bp+8)),0,2048],'original fog whole LockRect ABI');op='lock';request=dict(pointer=self.fog_pointer,flags=2048);native=self.fog_gpu.lock(self.fog_pointer);result=self.fog_space.result('fog',native);self.fog_lock=result;raw=bytes.fromhex(result['hex']);p=result['bits']&~4095;maps=[(p,(result['bits']-p+len(raw)+4095)&~4095)];put(result['bits'],raw);put(args[2],struct.pack('<2I',result['pitch'],result['bits']))
   elif phase==3:
    need(args==[t['pointer'],0],'original fog UnlockRect ABI');op='unlock';raw=self.read(self.fog_lock['bits'],len(bytes.fromhex(self.fog_lock['hex'])));source=self.read(word(self.read(MAP+0x2658c)),44032);expected=bytearray.fromhex(self.fog_lock['hex']);pitch=self.fog_lock['pitch']
    for y in range(128):expected[y*pitch:y*pitch+344]=source[y*344:(y+1)*344]
    need(raw==bytes(expected),'every original fog row and all unchanged actual surface padding');request=dict(pointer=self.fog_pointer,hex=raw.hex());native=self.fog_gpu.unlock(self.fog_pointer,raw);result=copy.deepcopy(native);extra=dict(uploaded_hex=raw.hex(),source_hex=source.hex());self.fog_upload=extra;self.fog_readback=self.fog_gpu.readback(self.fog_pointer);need(self.fog_readback['hex']==raw.hex() and self.fog_readback['sha256']==sha(raw),'entire actual current fog texture readback')
   else:
    need(args==[t['pointer']],'original fog zero-reference Release ABI');op='release';request=dict(pointer=self.fog_pointer);native=self.fog_gpu.release(self.fog_pointer);result=copy.deepcopy(native)
  value=result['count'] if phase==5 else result['hr'];need(value==0,'actual current fog successful COM result')
  for p,n in maps:need(all(not(a<p+n and p<=b) for a,b,_ in self.u.mem_regions()),'fresh separate fog interface/surface mapping');self.u.mem_map(p,n)
  for o in outputs:self.u.mem_write(o['pointer'],bytes.fromhex(o['hex']))
  self.memory_evidence.refresh()
  for o in outputs:self.memory_evidence.mark(o['pointer'],len(bytes.fromhex(o['hex'])))
  self.api_calls.append(dict(kind='actual_fog_GPU',index=self.fog_calls,phase=phase,slot=slot,target=at,sp=sp,return_va=ret,pop=pop,args=args,value=value,native_op=op,native_request=request,native_result=native,result=result,new_mappings=[dict(pointer=p,bytes=n) for p,n in maps],memory_outputs=outputs,native_wire_index=start,**extra));self.fog_calls+=1;self.u.reg_write(base.REGISTERS['EAX'],value);self.u.reg_write(base.REGISTERS['ESP'],sp+4+pop);self.u.reg_write(base.REGISTERS['EIP'],ret)
 def continue_loop(self):
  contracts();self.loop_attempts=[];self.fog_gpu=ImageD3D8(self.fog_helper);self.fog_space=AddressSpace();self.fog_space.next=SPACE;self.fog_calls=0;self.fog_methods=set();self.fog_active=self.fog_creating=True;self.fog_record=dict(contract=contracts(),entry=fog_state(self),entry_memory=base.memory_rows(self.u),entry_architectural_cpu=base.architectural_cpu(self.u),GPU_build=self.fog_build,GPU_hello=copy.deepcopy(self.fog_gpu.hello),creation=[])
  e=self.fog_record
  try:
   need((e['entry']['source_width'],e['entry']['source_height'],e['entry']['texture'])==(172,128,0) and word(self.read(FOG+52))==25,'preserved source fog initialization, format and actual missing texture');s=self.loop_step('original_fog_device_query',RETURN,dict(va=0x4142b0,receiver=self.renderer,args=[0],sp=STACK,return_va=RETURN));e['creation'].append(s);need(self.cpu()['EAX']==self.device,'original source query selects existing logical current device');s=self.loop_step('original_fog_texture_creation',RETURN,dict(va=0x403bd0,receiver=FOG,args=[self.device,0],sp=STACK,return_va=RETURN));e['creation'].append(s);need(self.cpu()['EAX']==0 and self.fog_calls==2,'complete original fog texture creation');self.fog_creating=False;e['created']=fog_state(self);loop=super().continue_loop();e['business_final']=fog_state(self);e['business_memory']=base.memory_rows(self.u);e['business_architectural_cpu']=base.architectural_cpu(self.u);e['texture']=copy.deepcopy(self.fog_texture);e['lock']=copy.deepcopy(getattr(self,'fog_lock',None));e['upload']=copy.deepcopy(getattr(self,'fog_upload',None));e['readback']=copy.deepcopy(getattr(self,'fog_readback',None));e['typed_projection']=self.fog_space.ledger();e['cleanup']=self.loop_step('supplemental_original_fog_texture_destructor',RETURN,dict(va=0x403730,receiver=FOG,args=[],sp=STACK,return_va=RETURN));e['after_cleanup']=fog_state(self);need(e['after_cleanup']['texture']==0 and e['after_cleanup']['accounting']==e['entry']['accounting'],'original fog release/clear and byte accounting balance');return loop
  finally:
   e['GPU']=self.fog_gpu.close();e['GPU_exit']=self.fog_gpu.process.returncode;e['GPU_trace']=copy.deepcopy(self.fog_gpu.trace);e['source_COM_calls']=self.fog_calls;self.fog_active=False

def run_case(helper,build,gpu,gb,role,rb,opening,ob,name,scene,fog,fb):
 instances=[]
 class Attached(Guest):
  def __init__(self,*a,**kw):super().__init__(*a,**kw);self.fog_helper=fog;self.fog_build=fb;instances.append(self)
 call=previous.previous.adapt(previous.run_case,[("analysis/school-retained-world-loop-failed-","analysis/school-retained-fog-failed-")],Guest=Attached)
 try:c=call(helper,build,gpu,gb,role,rb,opening,ob,name,scene)
 except BaseException as exc:
  if instances:
   g=instances[0];out='analysis/school-retained-fog-own-failed-'+helper.stem+'-'+name+'-'+str(scene)+'-20261023.json.gz';previous.previous.write_report(out,dict(accepted=False,error=repr(exc),fog_texture=getattr(g,'fog_record',None),loop_attempts=getattr(g,'loop_attempts',[]),CPU=g.cpu()))
  raise
 c['fog_texture']=instances[0].fog_record;return c

def matrix_header(rows):
 r=previous.matrix_header(rows);r['contract']=contracts();return r

def produce_group(args):
 import contextlib
 name,prefix,existing=args;rows=[];built=None
 with open(ROOT/('analysis/'+prefix+'-'+name+'.log'),'x',encoding='utf8',buffering=1) as log,contextlib.redirect_stdout(log),contextlib.redirect_stderr(log):
  for scene in (76,77):
   if name=='initial' and scene==76 and existing:
    path=existing
    with gzip.open(ROOT/path,'rt',encoding='utf8') as f:c=json.load(f)
    need((c['name'],c['scene_capture'])==(name,scene) and c['fog_texture']['contract']==contracts(),'existing exact complete fog source identity')
   else:
    if built is None:
     tag=prefix+'-'+name;helper,build=previous.platform.build(ROOT/('.venv-audit/'+tag+'-crt.exe'));gpu,gb=build_gpu(ROOT/('.venv-audit/'+tag+'-fourth.exe'));role,rb=build_gpu(ROOT/('.venv-audit/'+tag+'-role9.exe'));opening,ob=build_gpu(ROOT/('.venv-audit/'+tag+'-opening.exe'));fog,fb=build_gpu(ROOT/('.venv-audit/'+tag+'-fog.exe'));built=(helper,build,gpu,gb,role,rb,opening,ob,fog,fb)
    helper,build,gpu,gb,role,rb,opening,ob,fog,fb=built;path='analysis/'+prefix+'-'+name+'-'+str(scene)+'.json.gz';need(not (ROOT/path).exists(),'fresh immutable current fog source');c=run_case(helper,build,gpu,gb,role,rb,opening,ob,name,scene,fog,fb);previous.previous.write_report(path,c)
   raw=(ROOT/path).read_bytes();rows.append(dict(name=name,scene_capture=scene,path=path,sha256=sha(raw),bytes=len(raw)));del c;print('source fog case saved',name,scene,flush=True)
 return rows

if __name__=='__main__':
 import argparse
 from concurrent.futures import ProcessPoolExecutor
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--existing-initial76');p.add_argument('--jobs',type=int,default=1);a=p.parse_args();out=ROOT/a.out
 if out.exists() or not 1<=a.jobs<=3:p.error('fresh immutable matrix; 1..3 source worker processes')
 args=[(name,out.stem,a.existing_initial76) for name in ('initial','student9_waiting','fifth_class')];rows=[]
 if a.jobs==1:
  for group in args:rows.extend(produce_group(group))
 else:
  with ProcessPoolExecutor(max_workers=a.jobs) as executor:
   for group in executor.map(produce_group,args):rows.extend(group)
 result=matrix_header(rows);result['source_processes']=a.jobs;out.write_text(json.dumps(result,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('six current source fog resources and natural loop boundaries saved',flush=True)
