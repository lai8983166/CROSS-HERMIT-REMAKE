"""Current original GYBC overlay initialization and continuous terminal task VM."""
import argparse,copy,gzip,json,struct,types
from collections import Counter
from unicorn import UC_PROT_READ,UC_PROT_WRITE
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EAX,UC_X86_REG_ECX
from tools import terminal_task_emulation as parent
from tools import school_crt_init_fixture as crt
from tools.school_retained_crt_image import DOMAIN
from tools.school_retained_rendering import AddressSpace
from tools.school_tactical_resources_emulation import original_resource,RESOURCE_NAMES
from tools import terminal_overlay_platform as platform
ROOT,SOURCE,need,sha,terminal=parent.ROOT,parent.SOURCE,parent.need,parent.sha,parent.terminal
CTRL,TASK,MAIN,INPUT,VM,WORK,STACK,RETURN,SCRIPT=(getattr(parent,n) for n in ('CTRL','TASK','MAIN','INPUT','VM','WORK','STACK','RETURN','SCRIPT'))
PATH=0x12B00000;MANAGER=MAIN+0x1058;BANK=MAIN+0x844+20*8
RESOURCE_NAME=RESOURCE_NAMES[2];CODE=SOURCE.read_bytes();RESOURCE,IDENTITY=original_resource(RESOURCE_NAME)
# Exact source bodies exercised by the current resource and overlay path.
EXTRA_RANGES=((0x403620,0x403AA0),(0x403B70,0x403DA0),(0x4046F0,0x404870),(0x404FB0,0x405129),
 (0x407AD0,0x408130),(0x40D970,0x40D9BA),(0x40DB10,0x40DE91),(0x40DEC0,0x40E32F),(0x56DB00,0x56DB30),
 (0x416790,0x416865),(0x41F090,0x41FAE0),(0x420990,0x420B99),(0x4288E0,0x428B30),
 (0x42AC50,0x42AE6C),(0x56CEC0,0x56CF18),(0x56D4D0,0x56D810),(0x56DDA0,0x56DF30),
 (0x575FA0,0x576680),(0x576F60,0x576FF0),(0x57B7A0,0x57BAB0),(0x56E230,0x56E260),(0x56F4C0,0x56F8B0))
CRT_SOURCE='analysis/school-crt-init-fixture-v2-20261022.json.gz'
CRT_SOURCE_SHA='4296435909bf43e6413a82b8fcb986a7074940f30ac18949f2434bccc078f5ac'
def known_CRT():
 raw=(ROOT/CRT_SOURCE).read_bytes();need(sha(raw)==CRT_SOURCE_SHA,'fixed accepted original CRT instruction provenance');r=json.loads(gzip.decompress(raw));out=set()
 def visit(x):
  if isinstance(x,dict):
   for y in x.get('instruction_counts',[]):out.add(int(y['va'],0) if isinstance(y['va'],str) else y['va'])
   for v in x.values():visit(v)
  elif isinstance(x,list):
   for v in x:visit(v)
 visit(r);return tuple((a,a+1) for a in sorted(out))
from tools.school_vm_draw import native_ranges as vm_maintenance
RANGES=parent.RANGES+EXTRA_RANGES+known_CRT()+vm_maintenance()
ALLOWED=frozenset(a for lo,hi in RANGES for a in range(lo,hi))
REFERENCE=types.FunctionType(parent.REFERENCE.__code__,dict(parent.REFERENCE.__globals__,RANGES=RANGES))

class CrtGuest(crt.Guest):
 # Only the actual open leaf changes its exact admitted path; all CRT bodies remain original.
 def api(self,slot):
  if slot==0x5921EC:
   need(crt.old.text(self,struct.unpack('<I',self.read(self.cpu()['ESP']+4))[0])==RESOURCE_NAME.encode(),'exact GYBC source path')
   # Execute the same full read-only open contract against the new native owner.
   sp=self.cpu()['ESP'];args=[struct.unpack('<I',self.read(sp+4+i*4))[0] for i in range(7)];start=len(self.live.trace)
   r=self.live.request('open',path=RESOURCE_NAME,**dict(zip(('access','share','security','disposition','attributes','template'),args[1:])))
   self.file_handle=r['handle'];value=0x62001000
   self.api_calls.append(dict(name='CreateFileA',import_slot=slot,target=struct.unpack('<I',self.read(slot))[0],sp=sp,return_va=struct.unpack('<I',self.read(sp))[0],args=args,pop=28,value=value,new_mappings=[],memory_outputs=[],wire_start=start,wire_end=len(self.live.trace),native_handle=r['handle']))
   for reg,v in ((UC_X86_REG_EAX,value),(UC_X86_REG_ESP,sp+32),(UC_X86_REG_EIP,struct.unpack('<I',self.read(sp))[0])):self.u.reg_write(reg,v)
   return
  # File handles are translated only at the Windows leaf, never in guest memory.
  original=self.live.request
  def request(op,**kw):
   if 'handle' in kw:need(kw['handle']==0x62001000,'logical current file');kw['handle']=self.file_handle
   return original(op,**kw)
  self.live.request=request
  try:super().api(slot)
  finally:self.live.request=original

class OverlayMachine(parent.TaskMachine):
 source_code=types.FunctionType(parent.TaskMachine.source_code.__code__,dict(parent.TaskMachine.source_code.__globals__,ALLOWED=ALLOWED,REFERENCE=REFERENCE))
 def __init__(self,c,live,gpu,tick_inputs=None):
  super().__init__(c,tick_inputs);self.live,self.gpu=live,gpu;self.extra_counts=Counter();self.overlay_calls=[];self.overlay_returns=[];self.overlay_stack=[];self.gpu_calls=[];self.resource_steps=[];self.overlay_commands=[];self.active_overlay=False;self.copy_rows=[]
  self.crt=CrtGuest(live,0);cold=self.crt.u
  self.domain=[]
  for p,n,role in DOMAIN:
   self.uc.mem_protect(p&~4095,((p%4096+n+4095)//4096)*4096,UC_PROT_READ|UC_PROT_WRITE)
   b=bytes(cold.mem_read(p,n));self.uc.mem_write(p,b);self.domain.append(dict(pointer=p,bytes=n,role=role,hex=b.hex()));self.mutable.append((p,p+n))
  self.uc.mem_protect(0x7A0000,0x1000,UC_PROT_READ|UC_PROT_WRITE);self.uc.mem_protect(0x79F000,0x1000,UC_PROT_READ|UC_PROT_WRITE);self.mutable.append((0x79FC74,0x79FC78))
  self.uc.mem_map(PATH,4096);self.uc.mem_write(PATH,RESOURCE_NAME.encode()+b'\0');self.crt.u=self.uc
  self.api_targets={self.get(slot):slot for slot in crt.IMPORTS}
  for at in self.api_targets:
   p=at&~4095
   if not any(a<=p<=b for a,b,_ in self.uc.mem_regions()):self.uc.mem_map(p,4096)
  self.space=AddressSpace();self.space.next=0x64001000
  self.device=self.space.result('overlay',gpu.device);self.device_ptr=self.device['pointer'];self.device_method=self.device['methods']['80'];self.map_identity(self.device)
  self.put(MAIN+0xB210,self.device_ptr);self.put(MAIN+0xB28E,1,'h');self.put(MAIN+0xB278,gpu.hello['window_size'][0]);self.put(MAIN+0xB27C,gpu.hello['window_size'][1])
  self.mutable += [(MAIN+0x844,MAIN+0x1044),(MANAGER,MANAGER+0x38),(0x7A0EBC,0x7A0FC0),(0x765720,0x765724)]
  self.methods={self.device_method:80};self.crt_apis=[];self.accounting_baseline=dict(game_bytes=self.get(0x79FC74),texture_bytes=self.get(0x765720))
 def map_new(self,p,n):
  lo=p&~4095;end=(p+n+4095)&~4095
  for a in range(lo,end,4096):
   if not any(x<=a<=y for x,y,_ in self.uc.mem_regions()):self.uc.mem_map(a,4096)
 def map_identity(self,t):
  for p in (t['pointer'],t['vtable'],*t['methods'].values()):self.map_new(p,4)
  self.uc.mem_write(t['pointer'],struct.pack('<I',t['vtable']))
  for slot,p in t['methods'].items():self.uc.mem_write(t['vtable']+int(slot),struct.pack('<I',p))
 def snapshot(self):
  return [dict(pointer=a,bytes=b-a+1,hex=bytes(self.uc.mem_read(a,b-a+1)).hex()) for a,b,_ in self.uc.mem_regions()]
 def api_crt(self,slot):
  before=len(self.crt.api_calls);self.crt.api(slot);need(len(self.crt.api_calls)==before+1,'one actual CRT OS leaf');r=self.crt.api_calls[-1]
  # CRITICAL_SECTION.DebugInfo/OwningThread/LockSemaphore are opaque native identities.
  if r['name'] in ('InitializeCriticalSection','EnterCriticalSection','LeaveCriticalSection'):
   for out in r['memory_outputs']:
    b=bytearray.fromhex(out['hex']);original=bytes(b)
    for off in (0,12,16):
     p=struct.unpack_from('<I',b,off)[0]
     if p not in (0,0xFFFFFFFF):struct.pack_into('<I',b,off,0x63000000+off+(out['pointer']-0x80A480)*0x100)
    self.uc.mem_write(out['pointer'],bytes(b));out['hex']=b.hex();out['native_hex']=original.hex()
  for p,r0 in self.crt.allocations.items():
   interval=(p,p+r0['bytes'])
   if interval not in self.mutable:self.mutable.append(interval)
  self.crt_apis.append(copy.deepcopy(r))
 def gpu_api(self,at):
  slot=self.methods[at];pop={80:32,56:12,64:20,68:8,8:4}[slot];sp=self.getreg('ESP');bp=self.getreg('EBP');ret=self.get(sp);args=[self.get(sp+4+i) for i in range(0,pop,4)];outputs=[];native_pointer=getattr(self,'texture_native',None)
  need(ret=={80:0x403C8A,56:(0x403CBE if len(self.gpu_calls)<4 else 0x403A44),64:0x40395E,68:0x4039D3,8:0x40378D}[slot],'original COM caller')
  def put(p,b):self.map_new(p,len(b));self.uc.mem_write(p,b);outputs.append(dict(pointer=p,hex=b.hex()))
  if slot==80:
   need(args[:7]==[self.device_ptr,512,512,1,0,25,1],'original GYBC full CreateTexture ABI');native=self.gpu.create(512,512);result=self.space.result('overlay',native);self.texture=result['texture'];self.texture_native=native['texture']['pointer'];self.image_record=args[-1]-44;self.map_identity(self.texture);self.methods.update({p:int(k) for k,p in self.texture['methods'].items()});put(args[-1],struct.pack('<I',self.texture['pointer']));op='create'
  else:
   need(args[0]==self.texture['pointer'],'same current owned texture')
   if slot==56:
    need(args==[self.texture['pointer'],0,bp-(52 if ret==0x403CBE else 36)],'original descriptor ABI');op='describe';native=self.gpu.describe(native_pointer);result=copy.deepcopy(native);put(args[-1],bytes.fromhex(result['hex']))
   elif slot==64:
    need(args==[self.texture['pointer'],0,self.get(bp+8),0,2048],'original LockRect ABI');op='lock';native=self.gpu.lock(native_pointer);result=self.space.result('overlay',native);self.lock=result;raw=bytes.fromhex(result['hex']);put(result['bits'],raw);self.mutable.append((result['bits'],result['bits']+len(raw)));put(args[2],struct.pack('<II',result['pitch'],result['bits']))
   elif slot==68:
    need(args==[self.texture['pointer'],0],'original UnlockRect ABI');op='unlock';self.upload=bytes(self.uc.mem_read(self.lock['bits'],len(bytes.fromhex(self.lock['hex']))));native=self.gpu.unlock(native_pointer,self.upload);result=copy.deepcopy(native);self.readback=self.gpu.readback(native_pointer);need(self.readback['hex']==self.upload.hex(),'entire current actual GPU readback')
   else:need(args==[self.texture['pointer']],'original Release ABI');op='release';native=self.gpu.release(native_pointer);result=copy.deepcopy(native)
  value=result['count'] if slot==8 else result['hr'];need(value==0,'actual COM result successful')
  self.gpu_calls.append(dict(slot=slot,target=at,sp=sp,return_va=ret,args=args,pop=pop,value=value,op=op,native_result=native,result=result,memory_outputs=outputs,actual_API_executed=True))
  for reg,v in ((UC_X86_REG_EAX,value),(UC_X86_REG_ESP,sp+4+pop),(UC_X86_REG_EIP,ret)):self.uc.reg_write(reg,v)
 def getreg(self,name):return self.cpu()[name]
 def code(self,uc,at,size,context):
  if at in getattr(self,'api_targets',{}) and at not in parent.APIS:self.api_crt(self.api_targets[at]);return
  if at in getattr(self,'methods',{}):self.gpu_api(at);return
  super().code(uc,at,size,context)
  if at in ALLOWED and at not in parent.ALLOWED:self.extra_counts[hex(at)]+=1
  if not self.active_overlay:return
  sp=uc.reg_read(UC_X86_REG_ESP)
  while self.overlay_stack and (at,sp)==(self.overlay_stack[-1]['caller'],self.overlay_stack[-1]['return_ESP']):
   r=self.overlay_stack.pop();r.update(cpu_after=self.cpu(),result=self.getreg('EAX'),packet_after=bytes(uc.mem_read(r['receiver'],128)).hex() if r['entry']==0x407870 else None)
  if at in (0x407870,0x41F5A0,0x407AD0,0x40DCD0,0x40DF20):
   n,pop={0x407870:(2,8),0x41F5A0:(2,8),0x407AD0:(2,8),0x40DCD0:(1,4),0x40DF20:(2,8)}[at]
   r=dict(entry=at,caller=self.get(sp),receiver=uc.reg_read(UC_X86_REG_ECX),args=[self.get(sp+4+i*4) for i in range(n)],cpu_before=self.cpu(),return_ESP=sp+4+pop);self.overlay_calls.append(r);self.overlay_stack.append(r)
  if at==0x4CE9C5:
   p=self.get(VM+0x10)+self.get(VM+0x1C);op,n=struct.unpack('<HH',uc.mem_read(p,4));self.overlay_commands.append(dict(PC=self.get(VM+0x1C),opcode=op,bytes=n,source_offset=p-SCRIPT))
 def resource_root(self,label,entry,args=(),receiver=0,cdecl=False):
  before=self.mark();cpu=self.cpu();sp=STACK+0xF000;self.put(sp,RETURN)
  for i,a in enumerate(args):self.put(sp+4+i*4,a)
  self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_ECX,receiver);self.uc.emu_start(entry,RETURN,timeout=60_000_000,count=4_000_000)
  need(self.getreg('EIP')==RETURN and self.getreg('ESP')==sp+4+(0 if cdecl else 4*len(args)),'original resource root return '+label)
  row=dict(label=label,entry=entry,args=list(args),receiver=receiver,cdecl=cdecl,before_cpu=cpu,cpu_after=self.cpu(),trace_before=before,trace_after=self.mark());self.resource_steps.append(row);return self.getreg('EAX')
 def initialize_resources(self):
  self.resource_root('original_heap_initialization',0x57B9D0,[1],cdecl=True);self.resource_root('original_lock_initialization',0x576F60)
  self.resource_root('original_queue_owner_binding',0x40D970,[MAIN],MANAGER)
  self.resource_root('original_queue_4096_heads',0x40DB10,[4096],MANAGER)
  self.resource_root('original_bounded_64KiB_arena',0x40DBF0,[65536],MANAGER)
  p=self.resource_root('original_complete_GYBC_file',0x42AE20,[PATH],cdecl=True);need(bytes(self.uc.mem_read(p,len(RESOURCE)))==RESOURCE,'actual original file read bytes')
  self.file_pointer=p;self.resource_root('original_GYBC_register_and_upload',0x416790,[p,20],MAIN)
  self.resource_root('original_file_buffer_free',0x428AD0,[p],cdecl=True)
  self.loaded=dict(record=self.image_record,record_hex=bytes(self.uc.mem_read(self.image_record,84)).hex(),bank=bytes(self.uc.mem_read(BANK,8)).hex(),upload_hex=self.upload.hex(),readback=self.readback,lock=self.lock,texture=self.texture,owner_device=self.device,CPU=self.cpu(),memory=self.snapshot(),trace=self.mark())
 def admission(self):
  self.initialize_resources();self.active_overlay=True;a=super().admission();before=self.mark();cpu=self.cpu();self.task_active=True
  self.uc.emu_start(parent.STOP,RETURN,timeout=60_000_000,count=4_000_000);self.close_task_returns(self.getreg('EIP'),self.getreg('ESP'))
  need(self.getreg('EIP')==RETURN,'third original task returns through real overlay');self.task_active=False
  first=dict(after_CPU=self.cpu(),after=self.task_state(),memory=self.snapshot(),trace_after=self.mark())
  frames=[]
  for index in range(12):
   self.resource_root('original_frame_queue_heads_reset',0x40DB90,receiver=MANAGER)
   self.resource_root('original_frame_queue_arena_reset',0x40DC80,receiver=MANAGER)
   self.task_active=True
   reset=self.task_step(0x425DE0,INPUT);task=self.task_step(0x454CF0,TASK)
   self.task_active=False
   frames.append(dict(index=index,reset=reset,task=task))
   if self.get(VM+0x92E0,'B'):break
  else:raise ValueError('natural first WORK wait required')
  self.active_overlay=False
  self.continuation=dict(first_task=first,frames=frames,before_CPU=cpu,after_CPU=self.cpu(),trace_before=before,trace_after=self.mark(),after=self.task_state(),memory=self.snapshot(),calls=copy.deepcopy(self.overlay_calls),commands=copy.deepcopy(self.overlay_commands))
  return a
 def run(self):
  row=super().run();row.update(resource_initialization=copy.deepcopy(self.resource_steps),resource_loaded=self.loaded,overlay_continuation=self.continuation,resource_domain=self.domain,accounting_baseline=self.accounting_baseline,CRT_APIs=self.crt_apis,GPU_APIs=self.gpu_calls,extra_original_instruction_counts=dict(self.extra_counts),current_GPU_hello=self.gpu.hello,current_CRT_hello=self.live.hello,typed_GPU_projection=self.space.ledger())
  # Freeze the forward boundary before supplemental original resource teardown.
  self.resource_root('supplemental_original_group20_destructor',0x41F4E0,[20],MAIN+0x844)
  for label,off in (('heads',0x10),('arena',0x14)):
   self.resource_root('supplemental_original_queue_'+label+'_free',0x428AD0,[self.get(MANAGER+off)],cdecl=True)
  self.resource_root('original_lock_teardown',0x576FA0);self.resource_root('original_heap_teardown',0x57BA60)
  need(not self.crt.allocations and not self.crt.criticals,'all current original CRT resources released');need(self.get(0x79FC74)==self.accounting_baseline['game_bytes'] and self.get(0x765720)==self.accounting_baseline['texture_bytes'],'original accounting returns to preserved baseline');row.update(cleanup_steps=self.resource_steps[len(row['resource_initialization']):],cleanup_state=dict(bank=bytes(self.uc.mem_read(BANK,8)).hex(),game_bytes=self.get(0x79FC74),texture_bytes=self.get(0x765720)),CRT_APIs=copy.deepcopy(self.crt_apis),GPU_APIs=copy.deepcopy(self.gpu_calls));return row

def source_contract():
 return dict(parent_driver=parent.source_contract(),resource=IDENTITY,resource_group=20,resource_index=0,resource_records=1,original_register=0x416790,original_lookup=0x407870,render_gate=1,queue_heads=4096,queue_arena_bytes=65536,cold_CRT_domain=crt.PROBE_SHA,known_CRT_instructions=dict(path=CRT_SOURCE,sha256=CRT_SOURCE_SHA),maintenance=sha(str(vm_maintenance()).encode()),initial_owner_geometry_source='actual native helper window_size',actual_current_file_CRT_and_GPU=True,historical_platform_replies=False,game_function_substitutions=False,host_PC_wait_or_phase_writes=False,original_full_renderer_startup=False,draw_or_Present=False,extra_code=[dict(start=a,end=b,sha256=sha(CODE[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES])

def run_case(c,crt_helper,gpu_helper,ticks=None):
 live=platform.crt.Live(crt_helper);gpu=platform.OverlayGPU(gpu_helper);m=None
 try:
  m=OverlayMachine(c,live,gpu,ticks);row=m.run();row.update(CRT_cleanup=live.close(),GPU_cleanup=gpu.close(),CRT_trace=live.trace,GPU_trace=gpu.trace,CRT_exit=live.exit_code,GPU_exit=gpu.process.returncode);return row
 except BaseException as exc:
  if m is not None:terminal.save('analysis/terminal-overlay-diagnostic-'+str(__import__('time').time_ns())+'.json.gz',dict(accepted=False,error=repr(exc),CPU=m.cpu(),resource_steps=m.resource_steps,APIs=m.crt_apis[-6:],GPU_APIs=m.gpu_calls,owner=m.task_state()))
  raise
 finally:
  if not live.closed:live._terminate()
  if not gpu.closed:gpu._terminate()

def helpers():
 a,aa=platform.build(ROOT/'tools/terminal_overlay_crt_platform.cs','terminal-overlay-crt');b,bb=platform.build(ROOT/'tools/terminal_overlay_d3d8_platform.cs','terminal-overlay-gpu');return a,b,dict(CRT=aa,GPU=bb)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case',type=int);a=p.parse_args();need(not (ROOT/a.out).exists(),'fresh immutable overlay output');ch,gh,b=helpers();rows=[]
 for c in (parent.corpus() if a.case is None else [parent.corpus()[a.case]]):
  r=run_case(c,ch,gh);rows.append(r);print(c['name'],r['instructions'],r['writes'],'PC',r['overlay_continuation']['after']['VM'][56:64],flush=True)
 terminal.save(a.out,dict(schema_version=1,source_contract=source_contract(),helper_build=b,cases=rows,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False))
