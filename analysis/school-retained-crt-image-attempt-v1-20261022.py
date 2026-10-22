"""Source-backed fresh CRT domain in retained IMAGE; no historical heap claim."""
import copy,gzip,hashlib,json,struct,types
from collections import Counter
from functools import lru_cache
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from tools import school_crt_init_fixture as init
from tools import school_retained_crt as retained
from tools import school_retained_portrait_file_verification as parent
from tools import school_character_image_catalog as image

base=init.base;ROOT=base.ROOT;need=base.need;word=base.word;sha=base.sha;canonical=base.canonical
DOMAIN=((0x7619c0,15,'debug controls and fill sentinels'),(0x761df0,192,'48 source lock slots'),(0x762130,4,'original allocation hook'),(0x80a430,20,'debug list and statistics'),(0x80a480,96,'four static critical sections'),(0x80ab28,8,'heap token and mode'))
IMAGE=0x4cde10;TEXTURE=0x403bd0

@lru_cache(maxsize=6)
def boundary(branch,scene):
 report,source=retained.inputs();c=next(c for c in report['cases'] if (c['name'],c['scene_capture'])==(branch,scene));observed=[]
 class Observer(parent.Replay):
  def step(self,s):
   count=super().step(s)
   if s['result']['boundary']==IMAGE:observed.append((tuple((a,bytes(self.u.mem_read(a,b-a+1))) for a,b,_ in self.u.mem_regions()),self.u.context_save(),base.memory_rows(self.u),base.architectural_cpu(self.u)))
   return count
 verify=types.FunctionType(parent.verify_case.__code__,dict(parent.verify_case.__globals__,Replay=Observer),'observe_verified_natural_IMAGE_entry');checked=verify(c);need(len(observed)==1,'one independently verified natural IMAGE entry');memory,cpu,rows,arch=observed[0]
 return memory,cpu,dict(source=source,name=branch,scene_capture=scene,parent_proof=checked,pending_image=c['pending_image'],memory=rows,architectural_cpu=arch)

def project(g,memory,cpu):
 """Only source-initialized CRT bytes enter retained state; never reset game data."""
 initialized=g.u;u=Uc(UC_ARCH_X86,UC_MODE_32)
 for at,b in memory:u.mem_map(at,len(b));u.mem_write(at,b)
 u.context_restore(cpu);before=base.architectural_cpu(u);rows=[]
 for p,n,role in DOMAIN:
  b=bytes(initialized.mem_read(p,n));old=bytes(u.mem_read(p,n));u.mem_write(p,b);rows.append(dict(pointer=p,bytes=n,role=role,before_hex=old.hex(),source_hex=b.hex()))
 for p,b in memory:
  expected=bytearray(b)
  for row in rows:
   at=row['pointer'];n=row['bytes']
   if p<=at and at+n<=p+len(b):expected[at-p:at-p+n]=bytes.fromhex(row['source_hex'])
  need(bytes(u.mem_read(p,len(b)))==expected,'all non-domain retained memory unchanged')
 need(canonical(base.architectural_cpu(u))==canonical(before),'complete retained CPU unchanged by CRT projection');g.u=u
 return dict(kind='explicit fresh source-initialized CRT resource domain',rows=rows,architectural_cpu=before,full_memory=base.memory_rows(u),historical_heap_restored=False,all_other_retained_bytes_unchanged=True,game_accounting_reset=False)

class Guest(init.Guest):
 def continuous(self):
  before=self.cpu();need(before['EIP']==IMAGE,'natural original IMAGE entry');counts=Counter();ih=hashlib.sha256();wh=hashlib.sha256();writes=0;self.api_calls=[];maps=[]
  for slot in init.IMPORTS:
   at=word(self.read(slot))
   if not any(a<=at<=b for a,b,_ in self.u.mem_regions()):p=at&~4095;self.u.mem_map(p,4096);maps.append(dict(pointer=p,bytes=4096))
  targets={word(self.read(slot)):slot for slot in init.IMPORTS};iat={slot:self.read(slot) for slot in init.IMPORTS}
  def code(u,at,n,_):
   if at==TEXTURE:u.emu_stop();return
   if at in targets:self.api(targets[at]);return
   need(base.BASE<=at<0x592000 and self.read(at,n)==self.image[at-base.BASE:at-base.BASE+n],'unaltered original instruction '+hex(at));counts[at]+=1;ih.update(struct.pack('<I',at)+self.read(at,n))
  def write(u,access,at,n,value,_):
   nonlocal writes
   need(not base.BASE<=at<0x592000,'no code patch');writes+=1;wh.update(struct.pack('<IIQ',at,n,value&0xffffffffffffffff))
  c=self.u.hook_add(UC_HOOK_CODE,code);w=self.u.hook_add(UC_HOOK_MEM_WRITE,write)
  try:self.u.emu_start(IMAGE,0,count=2000000,timeout=120000000)
  except Exception as exc:raise RuntimeError('continuous IMAGE at '+hex(self.cpu()['EIP'])) from exc
  finally:self.u.hook_del(c);self.u.hook_del(w)
  need(self.cpu()['EIP']==TEXTURE and iat=={slot:self.read(slot) for slot in init.IMPORTS},'first original texture instruction unexecuted and IAT unchanged')
  return dict(label='continuous_original_IMAGE_to_first_portrait_texture',before_cpu=before,cpu=self.cpu(),boundary=TEXTURE,instruction_counts=[dict(va=a,count=n) for a,n in sorted(counts.items())],instruction_sha256=ih.hexdigest(),writes=writes,write_sha256=wh.hexdigest(),api_calls=self.api_calls,entry_mappings=maps,full_memory=base.memory_rows(self.u),architectural_cpu=base.architectural_cpu(self.u),ledger=init.old.ledger(self))

def snapshot(g):
 need(len(g.history)==2 and len(g.allocations)==2,'exact two live original allocations');f,a=[r['guest']+32 for r in g.history];raw,meta=image.resource();need(g.read(f,len(raw))==raw,'entire original SC004 file user bytes');need(word(g.read(a))==1 and g.read(a+4,84)==image.record_prefix(),'original vector count and every DX record byte');sp=g.cpu()['ESP'];receiver=g.cpu()['ECX'];renderer=word(g.read(0x7a49fc));device=word(g.read(renderer+0xb210));table=renderer+0x844+32*8
 need(receiver==a+4 and [word(g.read(sp+i)) for i in (0,4,8)]==[0x4050b4,device,0],'natural first portrait texture call ABI');need(g.read(table,8)==struct.pack('<2I',a+4,1),'original renderer registers vector record and count');frames=parent.chain(g,[('dx',0x41f9bb),('entry',0x41f24a),('container',0x41f0c2),('container_wrapper',0x41680b),('extended_register',0x4167b8),('register',0x4cde8a),('image',0x4cc0d2)])
 return dict(file_buffer=f,array=a,record=a+4,container=meta,allocations=[dict(pointer=p,raw_hex=g.read(p-32,r['bytes']).hex()) for p,r in zip((f,a),g.history)],record_hex=g.read(a+4,84).hex(),renderer_table_pointer=table,renderer_table_hex=g.read(table,8).hex(),pending_texture=dict(va=TEXTURE,receiver=receiver,args=[device,0],return_va=0x4050b4,sp=sp,frames=frames,first_instruction_executed=False),vm_pc=word(g.read(base.VM+28)),image_loaded_flag=g.read(base.VM+0x92a0+32,1).hex())

def run_case(helper,build,branch,scene):
 memory,cpu,provenance=boundary(branch,scene);live=init.platform.Live(helper);hello=copy.deepcopy(live.hello)
 try:
  g=Guest(live,0 if scene==76 else 1);g.root('original_heap_initialization',0x57b9d0,[1]);g.root('original_static_lock_initialization',0x576f60);projection=project(g,memory,cpu);baseline=word(g.read(0x79fc74));step=g.continuous();state=snapshot(g);need(init.old.ledger(g)['game_bytes']==baseline+262256,'original retained game accounting increment');readbacks=[]
  for p in list(g.allocations):
   g.sync(p);r=live.request('readback',pointer=g.allocations[p]['native']);need(r['hex']==g.read(p,g.allocations[p]['bytes']).hex(),'every actual native allocation byte agrees');readbacks.append(dict(guest=p,wire_index=len(live.trace)-1,result=r))
  cleanup_maps=[]
  for p,n in ((init.old.STACK,65536),(init.old.RETURN,4096)):
   need(all(not(a<p+n and p<=b) for a,b,_ in g.u.mem_regions()),'fresh supplemental cleanup harness mapping');g.u.mem_map(p,n);cleanup_maps.append(dict(pointer=p,bytes=n))
  g.root('supplemental_original_free_file_buffer',0x428ad0,[state['file_buffer']]);g.root('supplemental_original_free_vector',0x428ad0,[state['array']]);need(init.old.ledger(g)['game_bytes']==baseline and not g.allocations,'original frees restore retained game accounting');g.root('original_static_lock_teardown',0x576fa0);g.root('original_heap_teardown',0x57ba60);live.close()
 except BaseException:
  if not live.closed:
   try:live.close()
   except BaseException:pass
  raise
 print(branch,scene,sum(r['count'] for r in step['instruction_counts']),'continuous original IMAGE instructions',flush=True)
 return dict(name=branch,scene_capture=scene,parent_boundary=provenance,fixture_inputs=g.declaration,initial_native_hello=hello,source_heap_created=g.heap_created,helper_build=build,projection=projection,game_accounting_baseline=baseline,step=step,boundary=state,readbacks=readbacks,cleanup_entry_mappings=cleanup_maps,steps=g.steps,allocation_history=g.history,native_trace=live.trace,helper_exit_code=live.exit_code,helper_cleanup=live.cleanup)

def run(helper,build):
 return dict(schema_version=1,cases=[run_case(helper,build,n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],fresh_CRT_domain_reconstructed=True,historical_heap_restored=False,new_game_roots=0,supplemental_cleanup_roots_per_case=4,game_function_substitutions=0,IAT_rebindings=0,new_window=False,new_GPU=False,new_OS_input=False,full_CRT_startup_replayed=False,image_loader_completed=False,same_native_lifetime=False,R3_complete=False,R6_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--helper',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable report required')
 helper,build=init.platform.build(ROOT/a.helper);r=run(helper,build);out.write_bytes(gzip.compress(json.dumps(r,separators=(',',':')).encode(),mtime=0));print('six retained source IMAGE prefixes with fresh CRT resources and normal teardown',flush=True)
