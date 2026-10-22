"""Independent source replay from native cold inputs through CRT resource teardown."""
import copy,gzip,json,struct
from pathlib import Path
from tools import school_crt_init_fixture as work
from tools import school_retained_crt_fixture_verification as old

base=work.base;ROOT=work.ROOT;need=base.need;sha=base.sha;word=base.word
COUNTS=[58,16,33,65954,436,66251,734,68036,66254,474,13]
LABELS=['original_heap_initialization','original_static_lock_initialization',*old.LABELS,'original_static_lock_teardown','original_heap_teardown']

def protocol(c):
 need(c['schema_version']==1 and c['round'] in (0,1),'known observed-cold fixture')
 for k in ('host_debug_ledger_or_lock_initialization','retained_heap_restored','retained_integration','R3_complete','new_window','new_GPU','new_OS_input','full_CRT_startup_replayed'):need(c[k]is False,'honest source-init fixture scope '+k)
 need(c['original_heap_and_lock_initialization_executed']is c['original_heap_and_lock_teardown_executed']is True,'original CRT lifecycle required');need([s['label'] for s in c['steps']]==LABELS,'eleven declared original roots');need(c['helper_exit_code']==0 and c['helper_cleanup']==dict(all_owned_resources_released=True,heap_destroyed=True,critical_deleted=True,open_files=0,allocations=0,depth=0,forced_cleanup=False),'normal resource-free helper exit');need(len(c['native_trace'])==83,'entire native lifecycle/mirror transcript')
 for i,t in enumerate(c['native_trace']):need(t['request']['id']==t['reply']['id']==i+1 and t['reply']['ok']is True,'successful ordered native transcript')
 h=c['initial_native_hello'];need(h['pointer_bytes']==4 and h['heap']==h['critical']==0 and h['critical_hex']=='' and h['window_created']is h['GPU_created']is False and Path(h['directory']).resolve()==work.platform.old.INSTALLED.resolve(),'native helper has no precreated heap/lock');b=c['helper_build'];need(b['source_sha256']==sha(work.platform.SOURCE.read_bytes()) and b['compiler_sha256']==sha(work.platform.old.COMPILER.read_bytes()) and b['machine']==work.platform.old.machine(b['helper_path'])==0x14c and b['helper_sha256']==sha(Path(b['helper_path']).read_bytes()),'actual new helper source/compiler/x86 identity')

class Replay(old.Replay):
 def __init__(self,c):
  self.report=c;self.case=dict(c,native_hello=copy.deepcopy(c['initial_native_hello']));self.objects={};self.locks={};self.wire=0;self.blocks={};self.history=[];self.depth=0;self.files=set();self.criticals={};self.filebytes=(work.platform.old.INSTALLED/'DATA/ADV/BIN/SC004.BIN').read_bytes();need(sha(self.filebytes)==work.old.FILE_SHA,'actual installed source file');decl=work.initialize(self,c['round']);expected=copy.deepcopy(c['fixture_inputs']);expected['heap_token_translation']['native']=0;need(base.canonical(decl)==base.canonical(expected),'entire observed original cold data and all declared independent fixture inputs')
 def api(self,a):
  slot=a['import_slot']
  if slot in work.old.IMPORTS:return super().api(a)
  name,pop=work.IMPORTS[slot];sp=self.cpu()['ESP'];ret=word(self.read(sp));args=[word(self.read(sp+4+i)) for i in range(0,pop,4)];need(a['name']==name and a['target']==a['va']==word(self.read(slot)) and a['sp']==sp and a['return_va']==ret and a['args']==args and a['pop']==pop and a['wire_start']==self.wire,'original source initialization/teardown IAT and exact ABI');outputs=[];hello=self.case['native_hello']
  if name=='HeapCreate':
   need(ret==0x57b9ea and args==[0,4096,0] and hello['heap']==0 and word(self.read(0x80ab28))==0,'original fresh heap source call before store');r=self.consume('heap_create',flags=0,initial=4096,maximum=0);need(set(r)=={'pointer'} and r['pointer']>0 and r['pointer']==self.report['source_heap_created']==self.report['fixture_inputs']['heap_token_translation']['native'],'actual owned fresh heap identity');hello['heap']=r['pointer'];value=work.HEAP_TOKEN
  elif name=='GetVersionExA':
   need(ret==0x57b7ce and args==[self.cpu()['EBP']-0x98],'original OS heap mode query');before=self.read(args[0],148);need(word(before)==148,'source OSVERSIONINFOA size');r=self.consume('version',hex=before.hex());raw=bytes.fromhex(r['hex']);need(r['value']==1 and len(raw)==148 and word(raw)==148 and word(raw,4)>=5 and word(raw,16)==2,'actual successful modern Windows version selects original mode1');outputs=[dict(pointer=args[0],hex=raw.hex())];value=1
  elif name=='InitializeCriticalSection':
   need((ret,args[0]) in ((0x576f6f,0x80a498),(0x576f7c,0x80a4c8),(0x576f89,0x80a4b0),(0x576f95,0x80a480)) and args[0] not in self.criticals,'original four source static locks');r=self.consume('initialize',guest=args[0]);raw=bytes.fromhex(r['hex']);need(r['pointer']>0 and r['pointer'] not in self.criticals.values() and len(raw)==24 and word(raw,4)==0xffffffff and raw[8:20]==bytes(12),'actual initialized native critical section');self.criticals[args[0]]=r['pointer'];outputs=[dict(pointer=args[0],hex=raw.hex())];value=0
   if args[0]==0x80a4b0:hello['critical']=r['pointer']
  elif name=='DeleteCriticalSection':
   need((ret,args[0]) in ((0x577015,0x80a4b0),(0x577022,0x80a4c8),(0x57702f,0x80a498),(0x57703b,0x80a480)) and args[0] in self.criticals and self.depth==0,'original static lock teardown and balanced use');need(self.consume('delete',guest=args[0],pointer=self.criticals.pop(args[0]))==dict(value=1),'actual owned source lock deleted');value=0
  else:
   need(name=='HeapDestroy' and ret==0x57bb44 and args==[work.HEAP_TOKEN] and not self.blocks and not self.criticals and self.depth==0,'original owned empty heap teardown');need(self.consume('heap_destroy',heap=hello['heap'])==dict(value=1),'actual source HeapDestroy success');hello['heap']=0;value=1
  need(a['wire_end']==self.wire and a['value']==value and a['new_mappings']==[] and a['memory_outputs']==outputs and a['void_return_normalized']==(name in ('InitializeCriticalSection','DeleteCriticalSection')),'independent complete initialization/native outputs')
  for o in outputs:self.u.mem_write(o['pointer'],bytes.fromhex(o['hex']))
  self.u.reg_write(base.REGISTERS['EAX'],value);self.u.reg_write(base.REGISTERS['ESP'],sp+4+pop);self.u.reg_write(base.REGISTERS['EIP'],ret)

def verify_case(c):
 protocol(c);r=Replay(c);first=work.old.HEAP+32;second=first+0x200000;file=first+0x400000;roots=[(0x57b9d0,[1]),(0x576f60,[]),(0x4288e0,[]),(0x428a40,[262168]),(0x428a40,[88]),(0x428ad0,[first]),(0x428ad0,[second]),(0x42ae20,[work.old.PATH]),(0x428ad0,[file]),(0x576fa0,[]),(0x57ba60,[])];transitions=[(0,0,0,0,0,1,0)]*3+[(first-32,262168,first-32,262168,262168,2,262168),(first-32,262256,second-32,262256,262256,3,262256),(second-32,262256,second-32,88,262256,3,88),(0,262256,0,0,262256,3,0),(file-32,524424,file-32,262168,262256,4,262168)]+[(0,524424,0,0,262256,4,0)]*3;counts=[]
 for i,s in enumerate(c['steps']):
  va,args=roots[i];need(s['root']==dict(va=va,args=args,sp=work.old.STACK+0xf000,return_va=work.old.RETURN,receiver=0),'exact declared original source root');a=s['result'];counts.append(r.step(dict(s,result=dict(a,api_calls=[dict(q,va=q['target'],key='original_CRT_native_leaf') for q in a['api_calls']]))));expected=dict(zip(('first','total','last','current','high','next_request','game_bytes'),transitions[i]));need(work.old.ledger(r)==s['ledger']==expected,'independent source debug ledger/accounting after every root');need(base.memory_rows(r.u)==s['full_memory'] and base.canonical(base.architectural_cpu(r.u))==base.canonical(s['architectural_cpu']),'entire source mirror memory and architectural CPU after every root')
  if i==3:
   raw=r.read(first-32,262208).hex();need(c['first_allocation']==dict(pointer=first,raw_hex=raw),'entire first source allocation');old.header(raw,262168,1)
  elif i==4:
   for row,p,size,index,prev,nxt in zip(c['concurrent_allocations'],(first,second),(262168,88),(1,2),(0,first-32),(second-32,0)):
    raw=r.read(p-32,(size+51)&~15).hex();need(row==dict(pointer=p,raw_hex=raw),'both entire source allocations');old.header(raw,size,index,prev,nxt)
  elif i==5:
   raw=r.read(second-32,128).hex();need(c['remaining_allocation']==dict(pointer=second,raw_hex=raw),'source unlinks head and preserves second');old.header(raw,88,2)
  elif i==7:
   p,b=r.locate(file,len(r.filebytes));r.sync(p);reply=r.consume('readback',pointer=b['native']);raw=r.read(p,b['bytes']);need(reply==dict(pointer=b['native'],hex=raw.hex()) and c['file_allocation']==dict(pointer=file,raw_hex=raw.hex(),file_sha256=sha(r.filebytes),native_readback_wire_index=r.wire-1),'actual complete source file/native readback');old.header(raw.hex(),262168,3,payload=r.filebytes)
 need(counts==COUNTS and not r.blocks and not r.files and not r.criticals and r.case['native_hello']['heap']==0 and r.depth==0 and c['allocation_history']==r.history,'all original source init/lifecycle/teardown and ownership');need(r.consume('close')==c['helper_cleanup'] and r.wire==len(c['native_trace']),'normal helper exit with no driver resource destruction')
 return dict(round=c['round'],original_instructions_replayed=sum(counts),original_writes=sum(s['result']['writes'] for s in c['steps']),source_roots=11,actual_source_OS_calls=sum(len(s['result']['api_calls']) for s in c['steps']),source_heap_creates=1,source_critical_initializations=4,source_allocations=3,source_frees=3,source_file_read_bytes=len(r.filebytes),source_file_closes=1,source_critical_deletes=4,source_heap_destroys=1,host_debug_ledger_or_lock_initialization=False,observed_original_cold_data=True,whole_mirror_memory_and_CPU_verified=True,normal_helper_shutdown_verified=True,full_CRT_startup_replayed=False,retained_heap_restored=False,retained_integration=False,R3_complete=False)

def verify(r):
 need(r['schema_version']==1 and [c['round'] for c in r['cases']]==[0,1],'two independent cold-source fixtures');return dict(schema_version=1,cases=[verify_case(c) for c in r['cases']],observed_cold_source_initialization_lifecycle_verified=True,retained_heap_restored=False,retained_integration=False,R3_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable proof')
 result=verify(json.loads(gzip.decompress((ROOT/a.report).read_bytes())));out.write_text(json.dumps(result,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('two observed-cold source initialization/lifecycle/teardown fixtures independently verified',flush=True)
