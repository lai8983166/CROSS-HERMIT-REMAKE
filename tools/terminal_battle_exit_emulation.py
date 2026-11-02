"""Original battle exit prefix with complete current COMMON resource ownership.

The accepted stage boundary is preserved before any new initialization.  New
roots are explicit contracts, never an original thread-stack restoration.  The
original scene loop stops at each case's first unmet frontend dependency: a
unit-image lookup CALL or a zero-maximum-MP HUD division, both unexecuted.
"""
import argparse,copy,gc,hashlib,json,os,shutil,struct,tempfile,time,types
from pathlib import Path
from functools import lru_cache
from tools import terminal_battle_stage_handoff_emulation as parent
from tools import terminal_battle_exit_budget as budget
ROOT,CODE,need,sha,terminal,MAIN,VM,STACK,RETURN,TASK,INPUT,MANAGER,KEYBOARD,overlay,followup,x86,CTRL=(getattr(parent,n) for n in ('ROOT','CODE','need','sha','terminal','MAIN','VM','STACK','RETURN','TASK','INPUT','MANAGER','KEYBOARD','overlay','followup','x86','CTRL'))
PARENT_ACCEPTANCE='analysis/terminal-battle-stage-handoff-acceptance-v1-20261101.json'
PARENT_ACCEPTANCE_SHA='1b6f1d29bb50228546639be89fa715737f12edfa0d3eb54ab7434650481d3c2d'
PARENT_SOURCE='analysis/terminal-battle-stage-handoff-source-v3-20261101.json.gz'
PARENT_SOURCE_SHA='8368fa6369d51fc7398d2f73893a712d7d7ebead93c5c4b8d43eccd8e87a67ba'
PARENT_SOURCE_BYTES=3575860639
PARENT_PROOF='analysis/terminal-battle-stage-handoff-proof-v7-20261101.json'
PARENT_PROOF_SHA='914e0b55b6a336d4e52a4b5c1038dd7385ebd6ea7eb42c58b01ee33e40fbbb8a'
PARENT_PROOF_BYTES=14075
COMMON_NAME='data\Tactics\common.bin'
COMMON_PATH='CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/COMMON.BIN'
COMMON_SHA='110e230ffa1f3457ab7f5d7d4a31334e933c5edc90962855e921d86b84700d85'
COMMON_GROUP=90
COMMON_PATH_PTR=0x59A438
STOP=0x40B2EC
MP_STOP=0x46D3F4
CASE_FRONTIERS={'neutral_running':STOP,'timeout_before_combat':MP_STOP}
SORTING_RW_PAGES=(0x791000,0x3000)
# Each extent is a complete original function, admitted only after a diagnostic
# or direct original-call audit established its role in this finite prefix.
EXTRA_RANGES=((0x403AA0,0x403AEC),(0x404150,0x40440D),(0x4048D0,0x404B0D),
 (0x56E260,0x56E298),(0x467C20,0x467D4F),(0x472F40,0x473383),(0x4539B0,0x453CFC),(0x453E10,0x453F0F),(0x457AA0,0x457C3A))
EXTRA_RANGES=EXTRA_RANGES+((4666256, 4666730), (4558384, 4558604), (4446576, 4446612), (4455712, 4455793), (4261680, 4261800), (4436928, 4436982), (4443504, 4443651), (4634224, 4634450), (4639696, 4641230), (4642464, 4642878), (4641600, 4642433), (4235744, 4235798), (4241328, 4241394), (4235808, 4235917), (4241408, 4241546), (4235920, 4236069), (4241552, 4241758), (4239600, 4240779))
NEW_MUTABLE=((TASK+0x68,TASK+0xE8),(CTRL+0xDE4B0,CTRL+0xDE7B0),(0x765520,0x765720),(0x791730,0x793734))
CONTROLLER_PACKETS=(910512, 910640, 910768, 910896, 911024, 911152)
PACKET_CALL_SITES={910512: {'0x4075e0': 4609208, '0x4077c0': 4610553}, 910640: {'0x4075e0': 4609226, '0x4077c0': 4610574}, 910768: {'0x4075e0': 4609244, '0x4077c0': 4610594}, 910896: {'0x4075e0': 4609262, '0x4077c0': 4610615}, 911024: {'0x4075e0': 4609280, '0x4077c0': 4610636}, 911152: {'0x4075e0': 4609298, '0x4077c0': 4610656}}
RANGES=parent.RANGES+EXTRA_RANGES
ALLOWED=frozenset(a for lo,hi in RANGES for a in range(lo,hi))
REFERENCE=types.FunctionType(parent.REFERENCE.__code__,dict(parent.REFERENCE.__globals__,RANGES=RANGES))
TEXT_APIS={0x76182A80:('ImmGetOpenStatus',0x5920EC,0x425C99),0x770206E0:('lstrlenA',0x5922C4,0x425A7E)}
EVENT_ABI={0x46D340:(4,16),0x4075E0:(0,0),0x4077C0:(1,4),0x467C20:(1,4),0x472F40:(8,32),0x4539B0:(0,0),0x454CF0:(0,0),0x453F10:(0,0),0x46B470:(0,0),0x432100:(0,0),0x457AA0:(0,0),0x454C40:(0,0),0x453E10:(0,0),0x407870:(2,8),0x41F5A0:(2,8),0x41F340:(6,24),0x403BD0:(2,8),0x4048D0:(7,28),0x404150:(4,16),0x41F4E0:(1,4)}
recorded_write_PCs=[]

@lru_cache(maxsize=1)
def common_resource():
 raw=(ROOT/COMMON_PATH).read_bytes();need(len(raw)==1793036 and sha(raw)==COMMON_SHA,'exact complete original COMMON container')
 count=struct.unpack_from('<I',raw,4)[0];offsets=struct.unpack_from('<%dI'%count,raw,8);need(count==580 and len(set(offsets))==580,'all original COMMON records')
 rows=[]
 for i,p in enumerate(offsets):
  end=offsets[i+1] if i+1<count else len(raw);b=raw[p:end]
  row=dict(index=i,offset=p,bytes=end-p,sha256=sha(b),marker=b.startswith(b'Dm-No-MakeTex'))
  if row['marker']:need(b.startswith(b'Dm-No-MakeTex'),'original marker')
  else:
   need(b[:2]==b'BM' and struct.unpack_from('<H',b,28)[0]==8,'only original eight-bit BMPs')
   w,h=struct.unpack_from('<ii',b,18);need(w>0 and h>0,'original bottom-up BMP extent');row.update(width=w,height=h,texture_size=[1<<(w-1).bit_length(),1<<(h-1).bit_length()])
  rows.append(row)
 need(sum(not r['marker'] for r in rows)==461,'461 original COMMON images')
 return raw,rows

def bmp8_upload(blob,before,pitch,texture_height,colorkey,normalize_black=1):
 """Independent integer interpretation of original BMP8 palette conversion."""
 w,h=struct.unpack_from('<ii',blob,18);bits=struct.unpack_from('<I',blob,10)[0];stride=1 if w==1 else (w+3)&~3
 need(len(before)==pitch*texture_height and pitch>=stride*2 and h<=texture_height,'complete original destination surface')
 palette=[];key=blob[54:57];palette_count=struct.unpack_from('<I',blob,46)[0]
 if palette_count==0:palette_count=(bits-54)//4
 for i in range(256):
  b,g,r=blob[54+4*i:57+4*i]
  if normalize_black==1 and 0<i<palette_count and (b,g,r)==(0,0,0):b,g,r=key
  pixel=((r>>3)<<10)|((g>>3)<<5)|(b>>3)|0x8000
  palette.append(0 if i==0 or colorkey==1 and bytes((b,g,r))==key else pixel)
 out=bytearray(before)
 for y in range(h):
  row=bits+(h-1-y)*stride
  for x in range(stride):struct.pack_into('<H',out,y*pitch+2*x,palette[blob[row+x]])
 return bytes(out)

@lru_cache(maxsize=1)
def fixed_parents():
 refs={k:followup.parent.file_ref(p,h) for k,p,h in (('acceptance',PARENT_ACCEPTANCE,PARENT_ACCEPTANCE_SHA),('source',PARENT_SOURCE,PARENT_SOURCE_SHA),('proof',PARENT_PROOF,PARENT_PROOF_SHA))}
 a=json.loads((ROOT/PARENT_ACCEPTANCE).read_text(encoding='utf8'));need(a['source_report']==refs['source'] and a['independent_proof']==refs['proof'] and a['tasks_complete']==3,'fixed accepted original late stages')
 need(refs['source']['bytes']==PARENT_SOURCE_BYTES and refs['proof']['bytes']==PARENT_PROOF_BYTES,'fixed predecessor extents');return refs

@lru_cache(maxsize=1)
def fixed_parent_forward_summaries():
 raw=(ROOT/PARENT_PROOF).read_bytes();need(len(raw)==PARENT_PROOF_BYTES and sha(raw)==PARENT_PROOF_SHA,'fixed accepted stage proof')
 return {c['name']:c['forward_summary']['full_cumulative'] for c in json.loads(raw)['cases']}

def validate_parent_prefix(machine):
 name=machine.live_input['name'];expected=fixed_parent_forward_summaries()[name];actual=machine.mark();need(actual==expected,'exact full accepted battle stage digest '+name)
 return dict(case=name,fixed_proof_sha256=PARENT_PROOF_SHA,expected=expected,actual=actual)

def fixed_parent_times():return parent.fixed_parent_times()

def helper_contract():
 oldgpu=(ROOT/'tools/terminal_followup_d3d8_platform.cs').read_bytes();gpu=(ROOT/'tools/terminal_battle_exit_d3d8_platform.cs').read_bytes()
 need(gpu==oldgpu.replace(b'resources.Count>=10 || issued>=32',b'resources.Count>=500 || issued>=512').replace(b'max_textures=10,max_creates=32',b'max_textures=500,max_creates=512'),'only bounded GPU capacity changes')
 oldcrt=(ROOT/'tools/terminal_portrait_crt_platform.cs').read_bytes();crt=(ROOT/'tools/terminal_battle_exit_crt_platform.cs').read_bytes()
 slash=bytes((92,92));oldpath=b'path=="'+slash.join((b'data',b'adv',b'bin',b'sc002.bin'))+b'"';newpath=oldpath+b' || path=="'+slash.join((b'data',b'Tactics',b'common.bin'))+b'"'
 expected=oldcrt.replace(b'MaxJsonLength=4000000',b'MaxJsonLength=16777216').replace(b's.Length<=2097152',b's.Length<=4194304').replace(b'n<=1048576',b'n<=2097152').replace(b'z<=1048576',b'z<=2097152').replace(b'line.Length<=3000000',b'line.Length<=5000000').replace(oldpath,newpath).replace(b'?524312u:262168u',b'?524312u:(path.EndsWith("common.bin")?1793036u:262168u)')
 need(crt==expected,'only exact COMMON read-only path/extent and bounded complete buffer capacity changes')
 return dict(parent=parent.helper_contract(),GPU=dict(previous_sha256=sha(oldgpu),source='tools/terminal_battle_exit_d3d8_platform.cs',sha256=sha(gpu),max_textures=500,max_creates=512,peak_required=469,total_creates_required=479,all_other_ABI_unchanged=True),CRT=dict(previous_sha256=sha(oldcrt),source='tools/terminal_battle_exit_crt_platform.cs',sha256=sha(crt),additional_path=COMMON_NAME,exact_file_bytes=1793036,max_allocation_bytes=2097152,read_only=True),parent_hello_capacity_is_explicitly_different=True)

def helpers(prefix='terminal-battle-exit'):
 helper_contract();ch,cb=overlay.platform.build(ROOT/'tools/terminal_battle_exit_crt_platform.cs',prefix+'-crt');gh,gb=overlay.platform.build(ROOT/'tools/terminal_battle_exit_d3d8_platform.cs',prefix+'-gpu');return ch,gh,dict(CRT=cb,GPU=gb)

def _bounded_live_method(fn,limit):
 need(3000000 in fn.__code__.co_consts,'fixed original transport bound')
 return types.FunctionType(fn.__code__.replace(co_consts=tuple(limit if v==3000000 else v for v in fn.__code__.co_consts)),fn.__globals__,fn.__name__,fn.__defaults__,fn.__closure__)

class CommonCRTLive(overlay.platform.crt.Live):
 _read=_bounded_live_method(overlay.platform.crt.Live._read,16777216)
 request=_bounded_live_method(overlay.platform.crt.Live.request,5000000)

class CommonAddressSpace(overlay.AddressSpace):
 """Append deterministic per-record identities in a disjoint bounded guest pool.

 Parent IPC identities and its 1MiB cursor remain exactly unchanged.  A COMMON
 record reserves 512KiB: identity pages below 0x20000 and its complete surface
 at 0x20000 (maximum 0x40000 bytes for the actual catalog).
 """
 prefix='overlay-battle-exit-common-'
 def common_address(self,domain,pointer,bits=False):
  if not pointer:return 0
  index=int(domain[len(self.prefix):]);need(0<=index<580,'finite COMMON projection domain');key=(domain,pointer)
  if key not in self.native_to_guest:
   ordinal=sum(d==domain for d,p in self.native_to_guest);offset=0x20000 if bits else (ordinal+1)*0x1000;need(bits or offset<0x20000,'bounded COMMON interface identities');guest=0x20000000+index*0x80000+offset;need(guest not in self.guest_to_native,'no overlapping COMMON logical identities');self.native_to_guest[key]=guest;self.guest_to_native[guest]=key
  return self.native_to_guest[key]
 def guest(self,domain,pointer):return self.common_address(domain,pointer) if domain.startswith(self.prefix) else super().guest(domain,pointer)
 def result(self,domain,value,key=None):
  if domain.startswith(self.prefix) and key=='bits' and type(value)is int:return self.common_address(domain,value,True)
  return super().result(domain,value,key)

class CommonResourceMixin:
 def common_init(self):
  self.mutable+=list(NEW_MUTABLE)
  self.common_active=self.common_cleaning=False;self.common_current=None;self.common_resources=[];self.common_live={};self.common_leaves=[];self.common_entries=[];self.common_observers=[];self.common_cleanup=[]
 def api_crt(self,slot):
  if not(self.common_active or self.common_cleaning):return super().api_crt(slot)
  original=self.crt.api
  if self.common_active and slot==0x5921EC:
   fn=overlay.CrtGuest.api;self.crt.api=types.MethodType(types.FunctionType(fn.__code__,dict(fn.__globals__,RESOURCE_NAME=COMMON_NAME),closure=fn.__closure__),self.crt)
  try:overlay.OverlayMachine.api_crt(self,slot)
  finally:self.crt.api=original
  self.common_leaves.append(dict(kind='CRT',phase='cleanup' if self.common_cleaning else 'dependency',call=copy.deepcopy(self.crt_apis[-1])))
 def gpu_api(self,at):
  if not(self.common_active or self.common_cleaning):return super().gpu_api(at)
  slot=self.methods[at];pop={80:32,56:12,64:20,68:8,8:4}[slot];sp=self.getreg('ESP');bp=self.getreg('EBP');ret=self.get(sp);args=[self.get(sp+4+j) for j in range(0,pop,4)];wire=len(self.gpu.trace);outputs=[]
  need(ret=={80:0x403C8A,64:0x40395E,68:0x4039D3,8:0x40378D}.get(slot,ret) and (slot!=56 or ret in (0x403CBE,0x403A44)),'original COMMON COM caller')
  def put(p,b):self.map_new(p,len(b));self.uc.mem_write(p,b);outputs.append(dict(pointer=p,hex=b.hex()))
  if slot==80:
   r=self.common_current;need(self.common_active and r is not None and not r['source']['marker'] and not r.get('texture'),'one complete current COMMON image creation')
   w,h=r['source']['texture_size'];need(args==[self.device_ptr,w,h,1,0,25,1,r['record']+44],'original source-derived COMMON texture ABI')
   domain='overlay-battle-exit-common-'+str(r['source']['index']);native=self.gpu.create(w,h);result=self.space.result(domain,native);t=result['texture'];r.update(projection_domain=domain,texture=t,native_pointer=native['texture']['pointer'],generation=wire+1,create_wire_index=wire,alive=True,size=[w,h]);self.common_resources.append(r);self.common_live[t['pointer']]=r;self.map_identity(t);self.methods.update({p:int(k) for k,p in t['methods'].items()});put(args[-1],struct.pack('<I',t['pointer']));op='create'
  else:
   need(args[0] in self.common_live,'owned current COMMON texture');r=self.common_live[args[0]];t=r['texture'];p=r['native_pointer'];need(self.get(r['record']+44)==t['pointer'],'COMMON record still owns actual generation')
   if slot==56:
    need(args==[t['pointer'],0,bp-(52 if ret==0x403CBE else 36)],'original COMMON descriptor destination');native=self.gpu.describe(p);result=copy.deepcopy(native);put(args[-1],bytes.fromhex(result['hex']));op='describe'
   elif slot==64:
    need(self.common_active and r is self.common_current and args==[t['pointer'],0,self.get(bp+8),0,2048],'original COMMON lock ABI');native=self.gpu.lock(p);result=self.space.result(r['projection_domain'],native);r['lock']=copy.deepcopy(result);raw=bytes.fromhex(result['hex']);need(len(raw)<=0x40000,'full COMMON surface fits source-derived reserved extent');put(result['bits'],raw);self.mutable.append((result['bits'],result['bits']+len(raw)));put(args[2],struct.pack('<II',result['pitch'],result['bits']));op='lock'
   elif slot==68:
    need(self.common_active and r is self.common_current and args==[t['pointer'],0],'original COMMON unlock ABI');raw=self.read(r['lock']['bits'],len(bytes.fromhex(r['lock']['hex'])));source,rows=common_resource();b=source[r['source']['offset']:r['source']['offset']+r['source']['bytes']]
    expected=bmp8_upload(b,bytes.fromhex(r['lock']['hex']),r['lock']['pitch'],r['size'][1],r['conversion']['args'][1],r['bitmap_loader']['args'][4]);need(raw==expected,'all original BMP8 palette/stride/padding bytes independently predicted')
    r.update(upload_hex=raw.hex(),expected_sha256=sha(expected));native=self.gpu.unlock(p,raw);result=copy.deepcopy(native);op='unlock';observer=len(self.gpu.trace);r['readback']=self.gpu.readback(p);r['readback_wire_index']=observer;need(r['readback']['hex']==raw.hex(),'all actual COMMON surface readback bytes');self.common_observers.append(dict(index=r['source']['index'],wire_index=observer,result=copy.deepcopy(r['readback'])))
   else:
    need(self.common_cleaning and args==[t['pointer']],'only original supplemental COMMON Release');native=self.gpu.release(p);result=copy.deepcopy(native);r.update(alive=False,release_wire_index=wire);del self.common_live[t['pointer']];op='release'
  value=result['count'] if slot==8 else result['hr'];need(value==0,'current COMMON COM success');row=dict(generation=r['generation'],record=r['record'],index=r['source']['index'],wire_index=wire,phase='cleanup' if self.common_cleaning else 'dependency',slot=slot,target=at,sp=sp,return_va=ret,args=args,pop=pop,value=value,op=op,native_result=native,result=result,memory_outputs=outputs,actual_API_executed=True)
  self.common_leaves.append(dict(kind='GPU',call=row));self.return_api(sp,value,pop)
 def common_text(self,at):
  if not self.common_active or at!=0x770206E0:return False
  sp=self.getreg('ESP');caller=self.get(sp);arg=self.get(sp+4)
  if caller!=0x41F416:return False
  need(self.get(0x5922C4)==at and arg==0x594734 and self.read(arg,14)==b'Dm-No-MakeTex'+bytes((0,)),'exact original COMMON marker length ABI')
  value=int(self.kernel.lstrlenA(b'Dm-No-MakeTex'));need(value==13,'actual COMMON marker string length')
  self.common_leaves.append(dict(kind='COMMON_STRING',call=dict(name='lstrlenA',entry=at,import_slot=0x5922C4,caller=caller,sp=sp,return_va=caller,args=[arg],pop=4,value=value,result=value,string_hex=b'Dm-No-MakeTex'.hex(),memory_outputs=[],new_mappings=[],actual_API_executed=True)))
  self.return_api(sp,value,4);return True
 def common_code(self,at):
  if not(self.common_active or self.common_cleaning):return
  if at not in (0x41F340,0x4048D0,0x404150):return
  sp=self.uc.reg_read(x86.UC_X86_REG_ESP)
  if at==0x41F340:
   args=[self.get(sp+4+4*j) for j in range(6)];raw,rows=common_resource();index=args[2];need(index==len(self.common_entries) and args[1]==self.common_buffer and 0<=index<580,'each original complete COMMON record in original order');r=dict(source=copy.deepcopy(rows[index]),record=args[3]+index*84,loader=dict(entry=at,receiver=self.getreg('ECX'),caller=self.get(sp),args=args,CPU=self.cpu()),alive=False);self.common_entries.append(r);self.common_current=r
  if at==0x4048D0:
   need(self.common_current is not None,'current original COMMON bitmap loader');self.common_current['bitmap_loader']=dict(entry=at,caller=self.get(sp),receiver=self.getreg('ECX'),args=[self.get(sp+4+j*4) for j in range(7)],CPU=self.cpu());need(self.common_current['bitmap_loader']['args'][6]==0,'original COMMON uses embedded palette without override')
  if at==0x404150:
   need(self.common_current is not None,'current COMMON palette conversion');self.common_current['conversion']=dict(entry=at,caller=self.get(sp),receiver=self.getreg('ECX'),args=[self.get(sp+4+j*4) for j in range(4)],CPU=self.cpu())
 def initialize_common(self,segment):
  raw,rows=common_resource();need(self.read(MAIN+0x844+90*8,8)==bytes(8),'source group90 genuinely uninitialized')
  need(not any(a<0x32200000 and b>=0x20000000 for a,b,p in self.uc.mem_regions()),'complete deterministic COMMON projection pool is disjoint from every parent mapping')
  self.common_projection_before=dict(next=self.space.next,ledger=copy.deepcopy(self.space.ledger()));space=CommonAddressSpace();space.native_to_guest=self.space.native_to_guest;space.guest_to_native=self.space.guest_to_native;space.next=self.space.next;self.space=space
  need(self.read(COMMON_PATH_PTR,len(COMMON_NAME)+1)==COMMON_NAME.encode()+bytes((0,)),'unchanged original static COMMON path at59A438');self.common_active=True
  try:
   segment('common_read',0x42AE20,root=dict(receiver=0,args=[COMMON_PATH_PTR],cdecl=True,origin='original 451670 resource initialization: complete COMMON source file'))
   self.common_buffer=self.getreg('EAX');need(self.read(self.common_buffer,len(raw))==raw,'actual original COMMON complete file read')
   self.common_file_capture=dict(pointer=self.common_buffer,bytes=len(raw),sha256=sha(raw),hex=raw.hex())
   segment('common_register',0x416790,root=dict(receiver=MAIN,args=[self.common_buffer,90],origin='original scene initialization group0x5A'))
   need(len(self.common_entries)==580 and len(self.common_resources)==461 and len(self.common_live)==461,'all original 580 COMMON records and 461 actual textures')
   self.common_record_base=self.get(MAIN+0x844+90*8);self.common_record_count=self.get(MAIN+0x844+90*8+4);need(self.common_record_count==580,'original group90 publishes full count')
   self.common_records_forward=self.read(self.common_record_base,580*84).hex()
   for r in self.common_entries:r['record_forward_hex']=self.read(r['record'],84).hex()
   segment('common_file_free',0x428AD0,root=dict(receiver=0,args=[self.common_buffer],cdecl=True,origin='original full read buffer release'))
  finally:self.common_active=False;self.common_current=None
 def destroy_common(self,segment):
  self.common_cleaning=True
  try:segment('supplemental_common_group90_destructor',0x41F4E0,root=dict(receiver=MAIN+0x844,args=[90],origin='explicit supplemental cleanup after frozen forward boundary'))
  finally:self.common_cleaning=False
  need(not self.common_live and self.read(MAIN+0x844+90*8,8)==bytes(8),'all COMMON textures/vector released by original destructor')

class BattleExitMachine(CommonResourceMixin,parent.BattleStageMachine):
 source_code=types.FunctionType(parent.BattleStageMachine.source_code.__code__,dict(parent.BattleStageMachine.source_code.__globals__,ALLOWED=ALLOWED,REFERENCE=REFERENCE))
 def __init__(self,*args,**kwargs):
  super().__init__(*args,**kwargs);self.common_init();self.bex_active=False;self.bex_stop=None;self.bex_segments=[];self.bex_events=[];self.bex_pending=[];self.bex_writes=[];self.bex_text=[];self.bex_count=self.bex_write_count=0;self.bex_slice_first=0;self.bex_ih=hashlib.sha256();self.bex_wh=hashlib.sha256();self.bex_entries={};self.completed_task_observations=[];self.complete_task_pending=[]
 def expose_sorting_scratch(self):
  # The original PE .data is writable.  Preserve the accepted parent region
  # partition until its full capture, then expose these pages while write_hook
  # still admits only the precise791730..793734 sorting object (and old owners).
  self.uc.mem_protect(*SORTING_RW_PAGES,3)
 def bex_mark(self):return dict(instructions=self.bex_count,writes=self.bex_write_count,code_sha256=self.bex_ih.hexdigest(),write_sha256=self.bex_wh.hexdigest())
 def bex_state(self):return dict(task_hex=self.read(TASK,0x190).hex(),VM_PC=self.get(VM+28),VM_wait=self.get(VM+32,'H'),VM_active=self.get(VM+4,'B'),selector=self.get(TASK+0x38),result_type=self.get(TASK+0x174),packet_owner=self.get(TASK+0xB4),time_packet_hex=self.read(CTRL+0xDE730,0x80).hex(),group90=self.read(MAIN+0x844+90*8,8).hex())
 def bex_capture(self,full=True):
  memory=self.snapshot() if full else [dict(pointer=a,bytes=b-a+1,sha256=sha(self.read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()]
  return dict(memory=memory,CPU=self.cpu(),state=self.bex_state(),queue=self.queue_state(),trace=self.mark(),local_trace=self.bex_mark())
 def strict_text(self,at):
  name,slot,caller=TEXT_APIS[at];sp=self.getreg('ESP');arg=self.get(sp+4);need(self.get(slot)==at and self.get(sp)==caller,'exact original finite text caller '+name)
  if name=='lstrlenA':need(arg==INPUT+0x528 and self.read(arg,1)==b'\0','only fixed empty original INPUT+528 buffer')
  else:need(arg==self.get(INPUT+8)==0,'only original owned null IME')
  return dict(name=name,entry=at,import_slot=slot,caller=caller,args=[arg],string_hex='' if name=='lstrlenA' else None)
 def code(self,uc,at,size,context):
  # An engine timeout/count limit can interrupt inside a Python hook after its
  # observation but before the instruction executes. Yield before all observers
  # instead; resume the unchanged PC once, with neither observation nor write
  # counted at the host boundary.
  if self.bex_active and not(self.bex_label=='original_scene_loop' and at==MP_STOP and self.getreg('ECX')==0) and budget.yield_before_observation(uc,at,self.bex_stop,self.bex_count,self.bex_slice_first):return
  if at==0x454CF0:self.complete_task_pending.append(dict(entry=at,caller=self.get(self.getreg('ESP')),entry_ESP=self.getreg('ESP'),phase='prefix' if self.bex_active else 'parent'))
  if at==0x454EC1:
   need(bool(self.complete_task_pending),'original complete task has its entry');ev=self.complete_task_pending.pop();need(self.getreg('ESP')==ev['entry_ESP'] and self.get(self.getreg('ESP'))==ev['caller'],'original complete task ret stack');ev.update(return_PC=at,result=self.getreg('EAX'));self.completed_task_observations.append(ev)
  # Strengthen the inherited late-stage leaf without changing its response,
  # receipt, CPU or cumulative instruction/write digest.
  if self.battle_stage_active and at in TEXT_APIS:self.strict_text(at)
  if self.bex_active:
   sp=uc.reg_read(x86.UC_X86_REG_ESP)
   while self.bex_pending and (at,sp)==(self.bex_pending[-1]['caller'],self.bex_pending[-1]['return_ESP']):
    ev=self.bex_pending.pop();ev.update(after_CPU=self.cpu(),result=self.getreg('EAX'),after=self.bex_state())
   if at==self.bex_stop or self.bex_label=='original_scene_loop' and at==MP_STOP and self.getreg('ECX')==0:
    self.bex_actual_stop=at;uc.emu_stop();return
   need(at not in (0x424F80,0x4CE9C5,0x454E18,0x4967B0),'finite original scene prefix boundary')
   if self.common_text(at):return
   if at in TEXT_APIS:
    row=self.strict_text(at);name=row['name'];arg=row['args'][0]
    if name=='ImmGetOpenStatus':obs=self.ime.query(arg);value=obs['result'];row['observed']=obs
    else:value=int(self.kernel.lstrlenA(b''))
    row.update(result=value,actual_API_executed=True,segment=self.bex_label,sp=sp,pop=4,value=value,return_va=self.get(sp),memory_outputs=[],new_mappings=[]);self.bex_text.append(row);self.return_api(sp,value,4);return
   if at in self.gdi_targets:raise ValueError('unexpected GDI during finite exit prefix '+hex(at))
   self.common_code(at)
   if at in EVENT_ABI:
    n,pop=EVENT_ABI[at];ev=dict(entry=at,caller=self.get(sp),receiver=self.getreg('ECX'),args=[self.get(sp+4+j*4) for j in range(n)],return_ESP=sp+4+pop,before_CPU=self.cpu(),before=self.bex_state(),phase='cleanup' if self.common_cleaning else 'dependency' if self.common_active else 'prefix');self.bex_events.append(ev);self.bex_pending.append(ev)
   self.bex_entries[hex(at)]=self.bex_entries.get(hex(at),0)+1
  super().code(uc,at,size,context)
  if self.bex_active and at in ALLOWED:self.bex_count+=1;self.bex_ih.update(struct.pack('<I',at))
 def write_hook(self,uc,access,at,size,value,context):
  super().write_hook(uc,access,at,size,value,context)
  if self.bex_active:
   self.bex_write_count+=1;self.bex_wh.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))
   if not STACK<=at<STACK+0x20000:self.bex_writes.append(dict(pc=uc.reg_read(x86.UC_X86_REG_EIP),address=at,bytes=size,value=value&((1<<min(64,size*8))-1)))
 def bex_segment(self,label,entry,stop=RETURN,root=None):
  before=self.cpu();trace=self.mark();local=self.bex_mark();first=len(self.bex_events)
  if root:
   sp=STACK+0xF000;self.put(sp,RETURN)
   for j,a in enumerate(root['args']):self.put(sp+4+j*4,a)
   self.uc.reg_write(x86.UC_X86_REG_ESP,sp);self.uc.reg_write(x86.UC_X86_REG_ECX,root['receiver'])
  self.bex_stop=stop;self.bex_actual_stop=None;self.bex_label=label;self.uc.ctl_remove_cache(entry,entry+1)
  try:
   for chunk in range(512):
    self.bex_slice_first=self.bex_count;start=entry if chunk==0 else self.getreg('EIP');self.uc.emu_start(start,0,timeout=0,count=0)
    if self.bex_actual_stop is not None or self.getreg('EIP')==stop:break
    need(self.getreg('EIP')!=RETURN,'unexpected prefix root return '+label)
    print(self.live_input['name'],'battle_exit',label,'chunk',chunk+1,hex(self.getreg('EIP')),flush=True)
   else:raise ValueError('finite original exit segment budget '+label)
  finally:self.bex_stop=None
  actual=self.getreg('EIP');need(actual==stop or label=='original_scene_loop' and actual==MP_STOP and self.getreg('ECX')==0,'natural original exit prefix segment '+label)
  if stop==RETURN:need(self.getreg('ESP')==STACK+0xF004+(0 if root.get('cdecl') else 4*len(root['args'])),'complete original exit segment stack '+label)
  row=dict(label=label,entry=entry,stop=actual,root=root,before_CPU=before,CPU=self.cpu(),trace_before=trace,trace_after=self.mark(),local_before=local,local_after=self.bex_mark(),events=[first,len(self.bex_events)],capture_after=self.bex_capture(False));self.bex_segments.append(row);return row
 def capture_frontier(self):
  sp=self.getreg('ESP');bp=self.getreg('EBP');outer_bp=STACK+0xF000-4;point=self.getreg('EIP')
  need(point==CASE_FRONTIERS[self.live_input['name']],'exact declared case-specific frontend frontier')
  freeze=dict(entry=point,first_instruction_executed=False,frame_EBP=bp,outer_frame_EBP=outer_bp,local_result=self.get(outer_bp-8),root_return_address=self.get(outer_bp+4),original_wait_reached=False,stack_pointer=STACK,stack_bytes=0x20000,stack_hex=self.read(STACK,0x20000).hex(),open_events=[self.bex_events.index(v) for v in self.bex_pending])
  if point==STOP:
   packet=self.getreg('ECX');args=[self.get(sp),self.get(sp+4)]
   freeze.update(kind='unavailable_unit_graphics',call_site=point,call_target=0x407870,call_instruction_executed=False,return_address=STOP+5,receiver=packet,args=args,resource_owner=self.get(packet+0x4C),resource_slot=MAIN+0x844+args[0]*8,resource_slot_hex=self.read(MAIN+0x844+args[0]*8,8).hex(),unit_graphics_lookup_reached=True)
   need((packet,args[0],freeze['resource_owner'],freeze['resource_slot_hex'])==(CTRL+0xDE4B0,0,MAIN,bytes(8).hex()) and 0<=args[1]<=65535,'natural original unit graphics query with genuine empty bank0')
  else:
   unit=self.get(bp+8);record=self.get(unit+0x258);maximum=self.get(record+0x1A,'h');current=self.get(record+0x1C,'h')
   freeze.update(kind='zero_MP_HUD_input',idiv_instruction_executed=False,receiver=self.get(bp-4),HUD_args=[self.get(bp+8+j*4) for j in range(4)],frame_return_address=self.get(bp+4),unit=unit,stats_record=record,stats_record_hex=self.read(record,0xB0).hex(),maximum_MP_pointer=record+0x1A,maximum_MP=maximum,current_MP=current,numerator=self.getreg('EAX'),denominator=self.getreg('ECX'),unit_graphics_lookup_reached=False)
   need(unit==terminal.TARGET and record==terminal.RECORD+0x100 and maximum==current==self.getreg('EAX')==self.getreg('ECX')==self.getreg('EDX')==0 and self.get(bp+4)==0x46CF71,'genuine existing target record zero-MP input before original HUD division')
  need(freeze['local_result']==1 and freeze['root_return_address']==RETURN,'original outer stage result remains unconsumed')
  return freeze
 def admission(self):
  a=super().admission();self.bex_prefix_preflight=validate_parent_prefix(self);self.bex_prefix=self.bsh_prefix_counts();self.bex_before=self.bex_capture();self.bex_parent_entries=dict(self.entries);self.bex_parent_complete_tasks=len(self.completed_task_observations);need(not self.complete_task_pending,'no pending parent original task');self.bex_active=True
  self.uc.ctl_flush_tb()
  self.expose_sorting_scratch()
  self.initialize_common(self.bex_segment)
  need(self.read(TASK+0x68,0x88)==bytes(0x88),'original scene packet genuinely uninitialized')
  self.bex_segment('original_scene_packet_constructor',0x4075E0,root=dict(receiver=TASK+0x68,args=[],origin='original constructor call 4511B7 / return4511BC'))
  self.bex_segment('original_scene_packet_owner_binding',0x4077C0,root=dict(receiver=TASK+0x68,args=[MAIN],origin='original call 45350F / return453514'))
  need(self.read(CTRL+0xDE4B0,0x300)==bytes(0x300),'all six original controller UI packets genuinely uninitialized')
  for off in CONTROLLER_PACKETS:
   self.bex_segment('original_controller_packet_constructor_'+hex(off),0x4075E0,root=dict(receiver=CTRL+off,args=[],origin='original constructor call '+hex(PACKET_CALL_SITES[off]['0x4075e0'])))
  for off in CONTROLLER_PACKETS:
   self.bex_segment('original_controller_packet_owner_'+hex(off),0x4077C0,root=dict(receiver=CTRL+off,args=[MAIN],origin='original owner binding call '+hex(PACKET_CALL_SITES[off]['0x4077c0'])))
  self.bex_dependencies=self.bex_capture()
  for name,entry,receiver in (('heads',0x40DB90,MANAGER),('arena',0x40DC80,MANAGER),('input',0x425DE0,INPUT)):
   self.bex_segment(name,entry,root=dict(receiver=receiver,args=[],origin='original outer frame maintenance'))
  self.bex_segment('original_scene_loop',0x4539B0,STOP,root=dict(receiver=TASK,args=[],origin='explicit original CALL root; not restored CRT thread'))
  self.bex_freeze=self.capture_frontier()
  self.bex_final=self.bex_capture();self.bex_final_state=self.state();self.bex_counts_after=self.bsh_prefix_counts();self.bex_entries_forward=dict(self.bex_entries);self.bex_pending_forward=copy.deepcopy(self.bex_pending);self.bex_events_forward=copy.deepcopy(self.bex_events);self.bex_segments_forward=copy.deepcopy(self.bex_segments);self.bex_writes_forward=copy.deepcopy(self.bex_writes);self.bex_leaves_forward=copy.deepcopy(self.common_leaves);self.bex_resources_forward=copy.deepcopy(self.common_resources)
  self.bex_pending=[];self.destroy_common(self.bex_segment);self.bex_cleanup_capture=self.bex_capture();self.bex_active=False
  self.bex_result=dict(prefix=self.bex_prefix,counts_after=self.bex_counts_after,prefix_preflight=self.bex_prefix_preflight,before=self.bex_before,dependencies=self.bex_dependencies,final=self.bex_final,freeze=self.bex_freeze,parent_entries=self.bex_parent_entries,entries=self.bex_entries_forward,strict_text_receipts=self.bex_text,segments=self.bex_segments_forward,events=self.bex_events_forward,writes=self.bex_writes_forward,leaves=self.bex_leaves_forward,common_file=self.common_file_capture,common_entries=self.common_entries,common_resources=self.bex_resources_forward,common_resources_after_cleanup=copy.deepcopy(self.common_resources),common_records_forward_hex=self.common_records_forward,common_record_base=self.common_record_base,common_record_count=self.common_record_count,common_observers=self.common_observers,common_projection_before=self.common_projection_before,common_projection_after=dict(next=self.space.next,ledger=copy.deepcopy(self.space.ledger())),cleanup=dict(segments=self.bex_segments[len(self.bex_segments_forward):],events=self.bex_events[len(self.bex_events_forward):],leaves=self.common_leaves[len(self.bex_leaves_forward):],capture=self.bex_cleanup_capture),parent_complete_tasks=self.bex_parent_complete_tasks,complete_tasks=len(self.completed_task_observations),complete_task_observations=copy.deepcopy(self.completed_task_observations),terminal_battle_exit_prefix_executed=True,terminal_battle_exit_executed=False,outer_result_consumed=False,rewards_or_school_executed=False,original_outer_thread_restored=False,terminal_presentation_complete=False)
  return a
 def run(self):
  row=super().run();cap=self.bex_final;row.update(terminal_battle_exit_prefix=self.bex_result,final_state=self.bex_final_state,final=cap['memory'],pending_CPU=cap['CPU'],instructions=cap['trace']['instructions'],writes=cap['trace']['writes'],code_trace_sha256=cap['trace']['code_sha256'],write_trace_sha256=cap['trace']['write_sha256']);return row

def source_contract():
 raw,rows=common_resource()
 return dict(parent=parent.source_contract(),fixed_predecessor=fixed_parents(),extra_code=[dict(start=a,end=b,sha256=sha(CODE[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES],new_mutable=[dict(start=a,end=b,write_PCs=recorded_write_PCs) for a,b in NEW_MUTABLE],helper=helper_contract(),new_RW_pages=[dict(start=SORTING_RW_PAGES[0],bytes=SORTING_RW_PAGES[1],permission=3,after_parent_capture=True)],common=dict(path=COMMON_PATH,bytes=len(raw),sha256=sha(raw),records=580,images=461,markers=119,group=90),forward_roots=[0x42AE20,0x416790,0x428AD0,0x4075E0,0x4077C0]+[0x4075E0]*6+[0x4077C0]*6+[0x40DB90,0x40DC80,0x425DE0,0x4539B0],execution_slices=dict(policy='host_budget_before_code_observation',budget=budget.SLICE_INSTRUCTIONS,engine_timeout=0,engine_count=0,helper_sha256=sha((ROOT/'tools/terminal_battle_exit_budget.py').read_bytes())),new_VM_or_handler_roots=0,host_PC_wait_or_phase_or_result_writes=False,original_outer_thread_restored=False,cooperative_wait_executed=False,freeze_points=[STOP,MP_STOP],case_frontiers={k:dict(entry=v,kind='unavailable_unit_graphics' if v==STOP else 'zero_MP_HUD_input') for k,v in CASE_FRONTIERS.items()},freeze_target=0x407870,first_unavailable_resource_group=0,maximum_MP_input_modified=False,terminal_battle_exit_executed=False,outer_result_consumed=False,rewards_or_school_executed=False,draw_or_Present=False)

save_source=parent.save_source
save_source_cases=parent.save_source_cases

def run_case(c,ch,gh,ticks=None):
 fixed=fixed_parent_times()[c['name']];ticks=list(fixed) if ticks is None else ticks;need(ticks==fixed,'exact accepted original clock stream');instances=[]
 class Attached(BattleExitMachine):
  def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);instances.append(self)
 class Diagnostics:
  @staticmethod
  def save(path,data):
   if instances:
    m=instances[0];data['battle_exit_prefix']=dict(active=m.bex_active,segments=m.bex_segments,events=m.bex_events,writes=m.bex_writes,text=m.bex_text,leaves=m.common_leaves,entries=m.common_entries,resources=m.common_resources,memory=m.snapshot(),CPU=m.cpu(),trace=m.mark(),local_trace=m.bex_mark())
   save_source(path.replace('terminal-overlay-diagnostic-','terminal-battle-exit-diagnostic-').replace('.json.gz','-'+str(time.time_ns())+'.json.gz'),data)
 runtime=types.SimpleNamespace(**vars(overlay.platform));runtime.crt=types.SimpleNamespace(Live=CommonCRTLive)
 fn=types.FunctionType(overlay.run_case.__code__,dict(overlay.run_case.__globals__,OverlayMachine=Attached,terminal=Diagnostics,platform=runtime),closure=overlay.run_case.__closure__);return fn(c,ch,gh,ticks)

def finish_case_files(work,complete):
 path=Path(work).resolve();base=(ROOT/'.venv-audit').resolve()
 need(path.parent==base and path.name.startswith('bex-cases-'),'owned private case directory before recursive cleanup')
 if complete:shutil.rmtree(path,ignore_errors=True)
 return path

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case',type=int);p.add_argument('--helper-prefix');a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable exit prefix source');fixed_parents();ch,gh,b=helpers(a.helper_prefix or Path(a.out).name.removesuffix('.json.gz'));files=[];pcs=set();case_root=ROOT/'.venv-audit';work=tempfile.mkdtemp(prefix='bex-cases-'+Path(a.out).name.replace('.json.gz','')+'-',dir=case_root);complete=False;encoder=json.JSONEncoder(ensure_ascii=False,separators=(',',':'))
 try:
  for index,c in enumerate(overlay.parent.corpus() if a.case is None else [overlay.parent.corpus()[a.case]]):
   row=run_case(c,ch,gh);pcs.update(w['pc'] for w in row['terminal_battle_exit_prefix']['writes']);name=os.path.join(work,'case-'+str(index)+'.json')
   with open(name,'xb') as stream:
    for block in encoder.iterencode(row):stream.write(block.encode('utf8'))
   del row;gc.collect();files.append(name)
  recorded_write_PCs[:]=sorted(pcs);save_source_cases(a.out,dict(schema_version=1,source_contract=source_contract(),helper_build=b),files,dict(R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False));complete=True
 finally:
  finish_case_files(work,complete)
  if not complete:print('incomplete source cases retained locally',work,flush=True)
