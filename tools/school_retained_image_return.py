"""Continuous retained original IMAGE return with recorded native GPU contracts."""
import copy,gzip,hashlib,json,struct
from collections import Counter
from functools import lru_cache
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from tools import school_retained_crt_image as old
from tools import school_character_image_verification as historical
from tools.school_retained_rendering import AddressSpace

base=old.base;ROOT=old.ROOT;need=old.need;word=old.word;sha=old.sha;canonical=old.canonical
ACCEPTANCE='analysis/school-retained-crt-image-acceptance-v1-20261022.json'
ACCEPTANCE_SHA='98cc7bfacc46b4dca84fe3fc69b039e41bef456de4ed1c37029b8b15801e6083'
NATIVE_ACCEPTANCE='analysis/school-character-image-acceptance-20261013.json'
NATIVE_ACCEPTANCE_SHA='ac87ee39c3e3b9fdde10f20abf3103d11af607118e4efed72d8b376afe6523ff'
NATIVE='analysis/school-character-image-live-v3-20261013.json'
NATIVE_SHA='725d85f5f757ebda961c8b55dbcdf15b645f5a341a1012c0e856e2ed5e9b1908'

@lru_cache(maxsize=1)
def contracts():
 a=json.loads(base.pinned(ACCEPTANCE,ACCEPTANCE_SHA));n=json.loads(base.pinned(NATIVE_ACCEPTANCE,NATIVE_ACCEPTANCE_SHA));need(n['native_live']['path']==NATIVE and n['native_live']['sha256']==NATIVE_SHA,'accepted historical native texture source');r=json.loads(base.pinned(NATIVE,NATIVE_SHA));proof=[historical.compare_live(c) for c in r['cases']];c=r['cases'][0]
 return c['image_live'],c['first_live_text']['COM_process_cleanup']['texture_releases'][0],dict(parent_acceptance=ACCEPTANCE,parent_acceptance_sha256=ACCEPTANCE_SHA,native_acceptance=NATIVE_ACCEPTANCE,native_acceptance_sha256=NATIVE_ACCEPTANCE_SHA,native_report=NATIVE,native_report_sha256=NATIVE_SHA,historical_independent_proof=proof,mode='recorded GPU contracts only; no current native GPU or expired handles')

def mapped_texture():
 native,release,contract=contracts();space=AddressSpace();space.next=0x6b001000;creation=space.result('recorded_portrait',native['COM_calls'][0]['result']);lock=space.result('recorded_portrait',native['COM_calls'][2]['result']);return creation,lock,space.ledger()

class Guest(old.Guest):
 def configure(self):
  self.native,self.release,self.contract=contracts();self.creation,self.lock,self.translation=mapped_texture();self.texture=self.creation['texture'];self.renderer=word(self.read(0x7a49fc));self.device=word(self.read(self.renderer+0xb210));self.device_method=word(self.read(word(self.read(self.device))+80));self.methods={p:int(k) for k,p in self.texture['methods'].items()};self.gpu_count=0;self.copy_rows=[]
 def gpu(self,at):
  index=self.gpu_count;need(index<6,'bounded four texture and two cleanup interfaces');slot=[80,56,64,68,56,8][index];need(at==(self.device_method if index==0 else self.texture['methods'][str(slot)]),'source-owned texture dispatch');sp=self.cpu()['ESP'];ret=word(self.read(sp));need(ret==[0x403c8a,0x403cbe,0x40395e,0x4039d3,0x403a44,0x40378d][index],'exact original COM caller');pop={80:32,56:12,64:20,68:8,8:4}[slot];args=[word(self.read(sp+4+i)) for i in range(0,pop,4)];outputs=[];maps=[];extra={};record=0x50201024;bp=self.cpu()['EBP']
  def put(p,b):outputs.append(dict(pointer=p,hex=b.hex()))
  if index==0:
   need(args==[self.device,256,512,1,0,25,1,record+0x2c],'original portrait CreateTexture arguments');result=copy.deepcopy(self.creation);t=self.texture;maps=list(dict.fromkeys((p&~4095,4096) for p in (t['pointer'],t['vtable'],*t['methods'].values())));put(t['pointer'],struct.pack('<I',t['vtable']))
   for k,p in t['methods'].items():put(t['vtable']+int(k),struct.pack('<I',p))
   put(args[-1],struct.pack('<I',t['pointer']))
  elif index in (1,4):
   need(args==[self.texture['pointer'],0,bp-(0x34 if index==1 else 0x24)],'original descriptor destination');result=copy.deepcopy(self.native['COM_calls'][1]['result']);put(args[-1],bytes.fromhex(result['hex']))
  elif index==2:
   need(args==[self.texture['pointer'],0,word(self.read(bp+8)),0,0x800],'original bounded texture lock destination and flags');result=copy.deepcopy(self.lock);b=bytes.fromhex(result['hex']);p=result['bits']&~4095;maps=[(p,(result['bits']-p+len(b)+4095)&~4095)];put(result['bits'],b);put(args[2],struct.pack('<2I',result['pitch'],result['bits']))
  elif index==3:
   need(args==[self.texture['pointer'],0],'original texture unlock');result=copy.deepcopy(self.native['COM_calls'][3]['result']);pixels=self.read(self.lock['bits'],self.lock['pitch']*512);need(pixels==old.image.expected_pixels(bytes.fromhex(self.lock['hex']),self.lock['pitch']) and sha(pixels)==result['uploaded_sha256'],'every original pixel equals pinned historical upload');extra['uploaded_hex']=pixels.hex()
  else:
   need(args==[self.texture['pointer']] and self.release==dict(pointer=self.native['texture']['pointer'],unlock_hr=0,count=0),'historical owned texture release contract');result=copy.deepcopy(self.release)
  value=result['count'] if index==5 else result['hr'];origin=dict(kind='historical_native_texture_release',response=self.release) if index==5 else dict(kind='historical_native_COM_response',call_index=1 if index==4 else index,response=self.native['COM_calls'][1 if index==4 else index]['result']);row=dict(kind='recorded_GPU_only',target=at,sp=sp,return_va=ret,args=args,pop=pop,slot=slot,index=index,value=value,result=result,historical_origin=origin,new_mappings=[dict(pointer=p,bytes=n) for p,n in maps],memory_outputs=outputs,**extra)
  for p,n in maps:need(all(not(a<p+n and p<=b) for a,b,_ in self.u.mem_regions()),'fresh logical texture output pages');self.u.mem_map(p,n)
  for o in outputs:self.u.mem_write(o['pointer'],bytes.fromhex(o['hex']))
  self.u.reg_write(base.REGISTERS['EAX'],value);self.u.reg_write(base.REGISTERS['ESP'],sp+4+pop);self.u.reg_write(base.REGISTERS['EIP'],ret);self.gpu_count+=1;self.api_calls.append(row)
 def execute(self,label,stop,root=None):
  if root:
   sp=root['sp'];self.u.mem_write(sp,struct.pack('<'+'I'*(len(root['args'])+1),root['return_va'],*root['args']))
   for k,v in dict(EIP=root['va'],ESP=sp,ECX=root['receiver'],EFLAGS=0x202).items():self.u.reg_write(base.REGISTERS[k],v)
  before=self.cpu();counts=Counter();ih=hashlib.sha256();wh=hashlib.sha256();writes=0;self.api_calls=[];maps=[];targets={word(self.read(s)):s for s in old.init.IMPORTS};iat={s:self.read(s) for s in old.init.IMPORTS}
  for at in [self.device_method,*targets]:
   if not any(a<=at<=b for a,b,_ in self.u.mem_regions()):p=at&~4095;self.u.mem_map(p,4096);maps.append(dict(pointer=p,bytes=4096))
  def code(u,at,n,_):
   if at==stop:u.emu_stop();return
   if at in targets:self.api(targets[at]);return
   if at==self.device_method or at in self.methods:self.gpu(at);return
   need(base.BASE<=at<0x592000 and self.read(at,n)==self.image[at-base.BASE:at-base.BASE+n],'original code only '+hex(at))
   if at==0x56d4d0:
    sp=self.cpu()['ESP'];args=[word(self.read(sp+4+i)) for i in (0,4,8)];row=len(self.copy_rows);need(row<512 and word(self.read(sp))==0x40483f and args==[self.lock['bits']+row*self.lock['pitch'],0x50001020+24+row*512,512],'original row memcpy call ABI');self.copy_rows.append(dict(row=row,args=args,return_va=0x40483f))
   counts[at]+=1;ih.update(struct.pack('<I',at)+self.read(at,n))
  def write(u,access,at,n,value,_):
   nonlocal writes
   need(not base.BASE<=at<0x592000,'no source code patch');writes+=1;wh.update(struct.pack('<IIQ',at,n,value&0xffffffffffffffff))
  c=self.u.hook_add(UC_HOOK_CODE,code);w=self.u.hook_add(UC_HOOK_MEM_WRITE,write)
  try:self.u.ctl_remove_cache(before['EIP'],before['EIP']+1);self.u.emu_start(before['EIP'],0,count=2000000,timeout=120000000)
  except BaseException as exc:raise RuntimeError(label+' at '+hex(self.cpu()['EIP'])) from exc
  finally:self.u.hook_del(c);self.u.hook_del(w)
  need(self.cpu()['EIP']==stop and iat=={s:self.read(s) for s in old.init.IMPORTS},'natural boundary and unchanged original IAT');return dict(label=label,root=root,result=dict(before_cpu=before,cpu=self.cpu(),boundary=stop,instruction_counts=[dict(va=p,count=n) for p,n in sorted(counts.items())],instruction_sha256=ih.hexdigest(),writes=writes,write_sha256=wh.hexdigest(),api_calls=self.api_calls),entry_mappings=maps,full_memory=base.memory_rows(self.u),architectural_cpu=base.architectural_cpu(self.u),ledger=old.init.old.ledger(self))

def state(g):
 array=0x50201020;record=array+4;table=g.renderer+0x844+32*8
 return dict(record_hex=g.read(record,84).hex(),array_hex=g.read(array,88).hex(),table_pointer=table,table_hex=g.read(table,8).hex(),image_loaded_flag=g.read(base.VM+0x92c0,1).hex(),vm_pc=word(g.read(base.VM+28)),pixel_hex=g.read(g.lock['bits'],g.lock['pitch']*512).hex(),accounting=word(g.read(0x765720)),SEH_hex=g.read(0,4).hex(),frames=old.parent.chain(g,[('resource',0x4cc26d)]),natural_return=dict(va=g.cpu()['EIP'],sp=g.cpu()['ESP'],ebp=g.cpu()['EBP'],eax=g.cpu()['EAX']))

def run_case(helper,build,branch,scene):
 memory,cpu,provenance=old.boundary(branch,scene);live=old.init.platform.Live(helper);hello=copy.deepcopy(live.hello)
 try:
  g=Guest(live,0 if scene==76 else 1);g.root('original_heap_initialization',0x57b9d0,[1]);g.root('original_static_lock_initialization',0x576f60);projection=old.project(g,memory,cpu);baseline=word(g.read(0x79fc74));entry_fs=g.read(0,4).hex();prefix=g.continuous();pending=old.snapshot(g);g.configure();accounting=word(g.read(0x765720));first=g.execute('continuous_original_portrait_texture_copy_free_and_IMAGE_return',0x4cc0d2);after=state(g);need(g.gpu_count==4 and len(g.copy_rows)==512 and after['SEH_hex']==entry_fs,'all four historical texture calls, 512 original memcpy rows and original SEH restoration');need(after['accounting']==accounting+262144 and after['image_loaded_flag']=='01' and after['natural_return']==dict(va=0x4cc0d2,sp=provenance['pending_image']['sp']+12,ebp=provenance['pending_image']['frames'][0]['bp'],eax=0),'original IMAGE natural return/loaded flag/accounting');need(list(g.allocations)==[0x50201000] and old.init.old.ledger(g)['game_bytes']==baseline+88,'original file free leaves only vector alive');g.sync(0x50201000);native=live.request('readback',pointer=g.allocations[0x50201000]['native']);readback=dict(guest=0x50201000,wire_index=len(live.trace)-1,result=native);need(native['hex']==g.read(0x50201000,128).hex(),'actual complete native vector bytes');root=dict(va=0x41f4e0,args=[32],sp=old.init.old.STACK+0xf000,return_va=old.init.old.RETURN,receiver=g.renderer+0x844);cleanup=g.execute('supplemental_original_registered_image_container_cleanup',old.init.old.RETURN,root);need(g.cpu()['ESP']==root['sp']+8 and g.gpu_count==6 and not g.allocations and g.read(after['table_pointer'],8)==bytes(8) and word(g.read(0x765720))==accounting and old.init.old.ledger(g)['game_bytes']==baseline,'original descriptor/release/vector destructor/free/table and both counters balanced');g.root('original_static_lock_teardown',0x576fa0);g.root('original_heap_teardown',0x57ba60);live.close()
 except BaseException:
  if not live.closed:
   try:live.close()
   except BaseException:pass
  raise
 print(branch,scene,'original IMAGE returned;',sum(x['count'] for x in first['result']['instruction_counts']),'new original instructions;',len(g.copy_rows),'original row copies',flush=True)
 return dict(name=branch,scene_capture=scene,parent_boundary=provenance,fixture_inputs=g.declaration,initial_native_hello=hello,source_heap_created=g.heap_created,helper_build=build,projection=projection,game_accounting_baseline=baseline,source_entry_SEH_hex=entry_fs,prefix=prefix,pending_texture=pending,typed_texture_projection=g.translation,accounting_before=accounting,step=first,after=after,copy_rows=g.copy_rows,readback=readback,cleanup=cleanup,steps=g.steps,allocation_history=g.history,native_trace=live.trace,helper_exit_code=live.exit_code,helper_cleanup=live.cleanup)

def run(helper,build):
 return dict(schema_version=1,platform_contract=contracts()[2],cases=[run_case(helper,build,n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],fresh_CRT_domain_reconstructed=True,recorded_GPU_only=True,new_game_roots=0,game_function_substitutions=0,IAT_rebindings=0,original_IMAGE_returned=True,original_memcpy_executed=True,original_file_free_executed=True,supplemental_container_cleanup=True,new_GPU=False,new_window=False,new_OS_input=False,same_native_lifetime=False,historical_heap_restored=False,handler_animation_completed=False,R3_complete=False,R6_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--helper',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable report required')
 helper,build=old.init.platform.build(ROOT/a.helper);r=run(helper,build);out.write_bytes(gzip.compress(json.dumps(r,separators=(',',':')).encode(),mtime=0));print('six original retained IMAGE loaders returned and source containers cleaned',flush=True)
