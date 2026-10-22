"""Original heap/lock initialization from observed cold data; separate VM fixture."""
import copy,gzip,json,struct,types
from functools import lru_cache
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
from tools import school_retained_crt_fixture as old
from tools import school_crt_init_platform as platform
from tools import school_crt_init_verification as native

base=old.base;ROOT=base.ROOT;need=base.need;sha=base.sha;word=base.word
PROBE='analysis/school-crt-init-probe-v2-20261022.json.gz'
PROBE_SHA='850b684f76c67e674bc1ba4a79b398bcb18f8b6abb01cda1e4d8908830c07a82'
PROOF='analysis/school-crt-init-probe-proof-v1-20261022.json'
PROOF_SHA='5ecc8e2275bb263d6a5f9ff61cf6f93fdd09821a3b4f3e22c9cc03a4233a1840'
IMPORTS=dict(old.IMPORTS);IMPORTS.update({0x59212c:('HeapCreate',12),0x5922ac:('GetVersionExA',4),0x59227c:('InitializeCriticalSection',4),0x592280:('DeleteCriticalSection',4),0x592174:('HeapDestroy',4)})
HEAP_TOKEN=0x61001000

@lru_cache(maxsize=1)
def inputs():
 r=json.loads(gzip.decompress(base.pinned(PROBE,PROBE_SHA)));p=json.loads(base.pinned(PROOF,PROOF_SHA));need(native.verify(r)==p,'independently verified actual native cold-source origin');return r

def initialize(g,round):
 r=inputs();s=r['cases'][round*4]['captures'][0];need(s['EIP']==0x5713c0,'actual source before CRT');g.u=Uc(UC_ARCH_X86,UC_MODE_32);g.image=base.SOURCE.read_bytes();need(sha(g.image)==old.SOURCE_SHA,'original source image');g.u.mem_map(base.BASE,(len(g.image)+4095)&~4095);g.u.mem_write(base.BASE,g.image);data=bytes.fromhex(s['original_data']['hex']);g.u.mem_write(0x5ff000,data)
 for p,n in [(0,4096),(old.STACK,65536),(old.PATH,4096),(old.RETURN,4096)]:g.u.mem_map(p,n)
 g.u.mem_write(0,struct.pack('<I',0xffffffff));g.u.mem_write(old.PATH,b'data\\adv\\bin\\sc004.bin\0');maps=[]
 for slot in IMPORTS:
  target=word(g.read(slot))
  if not any(a<=target<=b for a,b,_ in g.u.mem_regions()):p=target&~4095;g.u.mem_map(p,4096);maps.append(dict(pointer=p,bytes=4096))
 return dict(kind='separate original-function roots from observed pre-CRT data, not retained restoration',native_probe=PROBE,native_probe_sha256=PROBE_SHA,native_proof=PROOF,native_proof_sha256=PROOF_SHA,round=round,source_data_pointer=0x5ff000,source_data_bytes=len(data),source_data_sha256=sha(data),host_debug_ledger_or_lock_initialization=False,source_only_heap_and_lock_initialization=True,full_CRT_startup_replayed=False,entry_maps=maps,initial_memory=base.memory_rows(g.u),initial_architectural_cpu=base.architectural_cpu(g.u),heap_token_translation=dict(guest=HEAP_TOKEN,native=0))

class Guest(old.Guest):
 def __init__(self,live,round):
  self.live=live;self.declaration=initialize(self,round);self.allocations={};self.history=[];self.next=old.HEAP;self.steps=[];self.api_calls=[];self.criticals={};self.heap_created=None
 def api(self,slot):
  if slot in old.IMPORTS:return super().api(slot)
  name,pop=IMPORTS[slot];sp=self.cpu()['ESP'];ret=word(self.read(sp));args=[word(self.read(sp+4+i)) for i in range(0,pop,4)];start=len(self.live.trace);outputs=[]
  def put(p,b):self.u.mem_write(p,b);outputs.append(dict(pointer=p,hex=b.hex()))
  if name=='HeapCreate':
   need(args==[0,4096,0] and word(self.read(0x80ab28))==0,'source fresh heap initialization');r=self.live.request('heap_create',flags=args[0],initial=args[1],maximum=args[2]);self.live.hello['heap']=r['pointer'];self.declaration['heap_token_translation']['native']=r['pointer'];self.heap_created=r['pointer'];value=HEAP_TOKEN
  elif name=='GetVersionExA':
   b=self.read(args[0],148);r=self.live.request('version',hex=b.hex());put(args[0],bytes.fromhex(r['hex']));value=r['value']
  elif name=='InitializeCriticalSection':
   r=self.live.request('initialize',guest=args[0]);self.criticals[args[0]]=r['pointer'];put(args[0],bytes.fromhex(r['hex']));value=0
   if args[0]==0x80a4b0:self.live.hello['critical']=r['pointer']
  elif name=='DeleteCriticalSection':
   need(args[0] in self.criticals,'source destroys initialized static lock');r=self.live.request('delete',guest=args[0],pointer=self.criticals.pop(args[0]));value=0
  else:
   need(name=='HeapDestroy' and args==[HEAP_TOKEN],'source owns heap teardown');r=self.live.request('heap_destroy',heap=self.heap_created);value=r['value']
  self.api_calls.append(dict(name=name,import_slot=slot,target=word(self.read(slot)),sp=sp,return_va=ret,args=args,pop=pop,value=value,new_mappings=[],memory_outputs=outputs,wire_start=start,wire_end=len(self.live.trace),void_return_normalized=name in ('InitializeCriticalSection','DeleteCriticalSection')))
  self.u.reg_write(base.REGISTERS['EAX'],value);self.u.reg_write(base.REGISTERS['ESP'],sp+4+pop);self.u.reg_write(base.REGISTERS['EIP'],ret)
 root=types.FunctionType(old.Guest.root.__code__,dict(old.Guest.root.__globals__,IMPORTS=IMPORTS),'original_function_root_with_initialization_APIs')

def run(helper,build,round):
 live=platform.Live(helper);hello=copy.deepcopy(live.hello)
 try:
  need(hello['heap']==hello['critical']==0,'native service has no pre-created CRT objects');g=Guest(live,round);g.root('original_heap_initialization',0x57b9d0,[1]);need(word(g.read(0x80ab28))==HEAP_TOKEN and word(g.read(0x80ab2c))==1,'source writes its heap token and selects mode1');g.root('original_static_lock_initialization',0x576f60);g.root('reset_source_game_accounting',0x4288e0)
  first=g.root('allocate_source_262168',0x428a40,[262168]);a=dict(pointer=first,raw_hex=g.read(first-32,262208).hex());second=g.root('allocate_source_88_concurrently',0x428a40,[88]);both=[dict(pointer=p,raw_hex=g.read(p-32,n).hex()) for p,n in [(first,262208),(second,128)]];g.root('free_source_first_while_second_alive',0x428ad0,[first]);remaining=dict(pointer=second,raw_hex=g.read(second-32,128).hex());g.root('free_source_second',0x428ad0,[second]);p=g.root('source_complete_SC004_file_loader',0x42ae20,[old.PATH]);need(sha(g.read(p,262168))==old.FILE_SHA,'complete original SC004 read');raw,entry=g.owned(p,262168);g.sync(raw);r=live.request('readback',pointer=entry['native']);need(r['hex']==g.read(raw,entry['bytes']).hex(),'complete actual native file buffer');file=dict(pointer=p,raw_hex=r['hex'],file_sha256=old.FILE_SHA,native_readback_wire_index=len(live.trace)-1);g.root('free_source_file_buffer',0x428ad0,[p]);g.root('original_static_lock_teardown',0x576fa0);g.root('original_heap_teardown',0x57ba60);need(not g.criticals and not g.allocations,'all source resources naturally destroyed');live.close()
 except BaseException:
  if not live.closed:
   try:live.close()
   except BaseException:pass
  raise
 return dict(schema_version=1,round=round,fixture_inputs=g.declaration,initial_native_hello=hello,helper_build=build,native_trace=live.trace,helper_exit_code=live.exit_code,helper_cleanup=live.cleanup,steps=g.steps,allocation_history=g.history,first_allocation=a,concurrent_allocations=both,remaining_allocation=remaining,file_allocation=file,source_heap_created=g.heap_created,original_heap_and_lock_initialization_executed=True,original_heap_and_lock_teardown_executed=True,host_debug_ledger_or_lock_initialization=False,retained_heap_restored=False,retained_integration=False,R3_complete=False,new_window=False,new_GPU=False,new_OS_input=False,full_CRT_startup_replayed=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--helper',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable report')
 helper,build=platform.build(ROOT/a.helper);r=dict(schema_version=1,cases=[run(helper,build,i) for i in range(2)]);out.write_bytes(gzip.compress(json.dumps(r,separators=(',',':')).encode(),mtime=0));print('two observed-cold source initialization/file/free/teardown fixtures completed',flush=True)
