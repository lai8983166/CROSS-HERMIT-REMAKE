"""Independent original-instruction and OS-ownership replay of retained IMAGE."""
import copy,gzip,json,struct
from pathlib import Path
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
from tools import school_retained_crt_image as work
from tools import school_crt_init_fixture_verification as init

base=work.base;ROOT=work.ROOT;need=work.need;word=work.word;canonical=work.canonical;sha=work.sha
LABELS=['original_heap_initialization','original_static_lock_initialization','supplemental_original_free_file_buffer','supplemental_original_free_vector','original_static_lock_teardown','original_heap_teardown']
EXPECTED_DOMAIN=((0x7619c0,15,'debug controls and fill sentinels'),(0x761df0,192,'48 source lock slots'),(0x762130,4,'original allocation hook'),(0x80a430,20,'debug list and statistics'),(0x80a480,96,'four static critical sections'),(0x80ab28,8,'heap token and mode'))

def protocol(c):
 need(c['name'] in ('initial','student9_waiting','fifth_class') and c['scene_capture'] in (76,77),'known retained source branch');need([s['label'] for s in c['steps']]==LABELS,'two initialization and four supplemental cleanup roots');need('root' not in c['step'] and c['step']['boundary']==0x403bd0,'continuous original IMAGE to unexecuted texture');need(c['helper_exit_code']==0 and c['helper_cleanup']==dict(all_owned_resources_released=True,heap_destroyed=True,critical_deleted=True,open_files=0,allocations=0,depth=0,forced_cleanup=False),'normal empty native owner exit')
 h=c['initial_native_hello'];need(h['pointer_bytes']==4 and h['heap']==h['critical']==0 and h['critical_hex']=='' and h['window_created'] is h['GPU_created'] is False and Path(h['directory']).resolve()==work.init.platform.old.INSTALLED.resolve(),'new headless owner has no driver-precreated heap/lock')
 b=c['helper_build'];p=Path(b['helper_path']);need(b['source_sha256']==sha(work.init.platform.SOURCE.read_bytes()) and b['compiler_sha256']==sha(work.init.platform.old.COMPILER.read_bytes()) and b['machine']==work.init.platform.old.machine(p)==0x14c and b['helper_sha256']==sha(p.read_bytes()),'actual helper source/compiler/binary identities')
 for i,t in enumerate(c['native_trace']):need(t['request']['id']==t['reply']['id']==i+1 and t['reply']['ok'] is True,'exact ordered successful native trace')
 projection=c['projection'];need(projection['kind']=='explicit fresh source-initialized CRT resource domain' and projection['historical_heap_restored']is projection['game_accounting_reset']is False and projection['all_other_retained_bytes_unchanged']is True,'explicit source resource reconstruction, no historical restore');need([(r['pointer'],r['bytes'],r['role']) for r in projection['rows']]==list(EXPECTED_DOMAIN),'only six finite CRT regions, no game state or CPU overlay')

class Replay(init.Replay):
 def __init__(self,c):
  self.report=c;self.case=dict(c,native_hello=copy.deepcopy(c['initial_native_hello']));self.objects={};self.locks={};self.wire=0;self.blocks={};self.history=[];self.depth=0;self.files=set();self.criticals={};self.filebytes=work.image.RESOURCE.read_bytes();need(sha(self.filebytes)==work.image.RESOURCE_SHA,'pinned actual complete SC004');decl=work.init.initialize(self,0 if c['scene_capture']==76 else 1);expected=copy.deepcopy(c['fixture_inputs']);expected['heap_token_translation']['native']=0;need(canonical(decl)==canonical(expected),'all original cold-data provenance, mappings and complete initial CPU/memory')

def replay_step(r,s):
 a=s['result'];count=r.step(dict(s,result=dict(a,api_calls=[dict(q,va=q['target'],key='original_CRT_OS_leaf') for q in a['api_calls']])));need(work.init.old.ledger(r)==s['ledger'] and base.memory_rows(r.u)==s['full_memory'] and canonical(base.architectural_cpu(r.u))==canonical(s['architectural_cpu']),'independent entire CPU/memory and original ledger after root');return count

def project(r,c):
 memory,cpu,provenance=work.boundary(c['name'],c['scene_capture']);need(canonical(provenance)==canonical(c['parent_boundary']),'fully independently verified old source continuation');initialized=r.u;r.u=Uc(UC_ARCH_X86,UC_MODE_32)
 for p,b in memory:r.u.mem_map(p,len(b));r.u.mem_write(p,b)
 r.u.context_restore(cpu);before=base.architectural_cpu(r.u);need(canonical(before)==canonical(c['projection']['architectural_cpu']),'projection cannot change any original CPU register');expected=[]
 for p,n,role in EXPECTED_DOMAIN:
  source=bytes(initialized.mem_read(p,n));old=r.read(p,n);expected.append(dict(pointer=p,bytes=n,role=role,before_hex=old.hex(),source_hex=source.hex()));r.u.mem_write(p,source)
 need(expected==c['projection']['rows'],'all projection original bytes and actual source-init bytes independently derived');need(base.memory_rows(r.u)==c['projection']['full_memory'] and canonical(base.architectural_cpu(r.u))==canonical(before),'all projected and unchanged memory/CPU');need(word(r.read(0x79fc74))==c['game_accounting_baseline'],'retained game accounting never reset');need(work.init.old.ledger(r)==dict(first=0,total=0,last=0,current=0,high=0,next_request=1,game_bytes=c['game_accounting_baseline']),'fresh source CRT ledger with retained game accounting')

def snapshot(r,c):
 f=0x50001020;a=0x50201020;state=c['boundary'];need(state['file_buffer']==f and state['array']==a and state['record']==a+4,'exact original two allocations and vector prefix');record=bytearray(84);struct.pack_into('<I2H',record,0x34,25,256,512);record[70:72]=bytes([205,205]);need(r.read(f,len(r.filebytes))==r.filebytes and r.read(a,88)==struct.pack('<I',1)+record and state['record_hex']==record.hex(),'every source file byte and independently derived DX record/vector bytes, including uninitialized allocation padding')
 first=r.read(f-32,262208);second=r.read(a-32,128);init.old.header(first.hex(),262168,1,0,a-32,payload=r.filebytes);init.old.header(second.hex(),88,2,f-32,0,payload=struct.pack('<I',1)+record);need(state['allocations']==[dict(pointer=f,raw_hex=first.hex()),dict(pointer=a,raw_hex=second.hex())],'full source debug headers, linked list, both guards and all live user bytes')
 renderer=word(r.read(0x7a49fc));device=word(r.read(renderer+0xb210));table=renderer+0x844+32*8;need(state['renderer_table_pointer']==table and state['renderer_table_hex']==r.read(table,8).hex()==struct.pack('<2I',a+4,1).hex(),'source slot32 record/count registration');sp=r.cpu()['ESP'];need(r.cpu()['ECX']==a+4 and [word(r.read(sp+i)) for i in (0,4,8)]==[0x4050b4,device,0],'natural original texture ABI');frames=work.parent.chain(r,[('dx',0x41f3e0),('entry',0x41f25a),('container',0x41f0c9),('container_wrapper',0x41684b),('extended_register',0x4167bf),('register',0x4cde8a),('image',0x4cc0d2)]);need(state['pending_texture']==dict(va=0x403bd0,receiver=a+4,args=[device,0],return_va=0x4050b4,sp=sp,frames=frames,first_instruction_executed=False),'seven natural image constructor frames');need(state['vm_pc']==word(r.read(base.VM+28))==252 and state['image_loaded_flag']==r.read(base.VM+0x92a0+32,1).hex()=='00','image handler has not returned or set loaded flag');need(state['container']==work.image.parse_resource(r.filebytes),'source DX container identity')

def verify_case(c):
 protocol(c);r=Replay(c);counts=[]
 for s,va,args in zip(c['steps'][:2],(0x57b9d0,0x576f60),([1],[])):
  need(s['root']==dict(va=va,args=args,sp=work.init.old.STACK+0xf000,return_va=work.init.old.RETURN,receiver=0),'exact supplemental source initialization root');counts.append(replay_step(r,s))
 project(r,c);s=c['step'];maps=[]
 for slot in work.init.IMPORTS:
  p=word(r.read(slot))
  if not any(a<=p<=b for a,b,_ in r.u.mem_regions()):at=p&~4095;r.u.mem_map(at,4096);maps.append(dict(pointer=at,bytes=4096))
 need(maps==s['entry_mappings'],'only missing actual original OS entry pages');count=r.step(dict(label=s['label'],root=None,result=dict(s,api_calls=[dict(q,va=q['target'],key='original_CRT_OS_leaf') for q in s['api_calls']])));need(base.memory_rows(r.u)==s['full_memory'] and canonical(base.architectural_cpu(r.u))==canonical(s['architectural_cpu']),'entire continuous final IMAGE memory and CPU');baseline=c['game_accounting_baseline'];need(work.init.old.ledger(r)==s['ledger']==dict(first=0x50001000,total=262256,last=0x50201000,current=262256,high=262256,next_request=3,game_bytes=baseline+262256),'original source counters and retained accounting');snapshot(r,c)
 visited={x['va'] for x in s['instruction_counts']};need({0x4cde10,0x42ae20,0x42ac50,0x428a40,0x56e860,0x56e920,0x578120,0x416790,0x41f0e0,0x56dda0,0x41f830,0x41f930,0x56cec0,0x404fb0}<=visited and 0x403bd0 not in visited,'all original allocator, hook, vector and record constructors executed, texture unexecuted');need([a['name'] for a in s['api_calls']]==['GetCurrentDirectoryA','CreateFileA','GetFileSize','EnterCriticalSection','HeapAlloc','LeaveCriticalSection','ReadFile','CloseHandle','EnterCriticalSection','HeapAlloc','LeaveCriticalSection'],'one natural original file lifecycle and two original allocations');need(not r.files and len(r.blocks)==2 and r.depth==0,'original loader closed file; both source-owned allocations alive')
 need(len(c['readbacks'])==2,'two complete native allocation readbacks')
 for p,row in zip((0x50001000,0x50201000),c['readbacks']):
  raw=r.sync(p);b=r.blocks[p];reply=r.consume('readback',pointer=b['native']);need(reply==dict(pointer=b['native'],hex=raw.hex()) and row==dict(guest=p,wire_index=r.wire-1,result=reply),'every actual native allocation byte independently matches source mirror')
 cleanup_maps=[]
 for p,n in ((0x21000000,65536),(0x32000000,4096)):
  if not any(a<=p and p+n<=b+1 for a,b,_ in r.u.mem_regions()):
   need(all(not(a<p+n and p<=b) for a,b,_ in r.u.mem_regions()),'new cleanup harness pages');r.u.mem_map(p,n);cleanup_maps.append(dict(pointer=p,bytes=n))
 need(c['cleanup_entry_mappings']==cleanup_maps,'only missing explicit supplemental cleanup stack/sentinel pages')
 for s,va,args in zip(c['steps'][2:],(0x428ad0,0x428ad0,0x576fa0,0x57ba60),([0x50001020],[0x50201020],[],[])):
  need(s['root']==dict(va=va,args=args,sp=0x2100f000,return_va=0x32000000,receiver=0),'supplemental cleanup only frees new domain source objects');counts.append(replay_step(r,s))
 need(not r.blocks and not r.files and not r.criticals and r.depth==0 and r.history==c['allocation_history'],'all native source resources destroyed and exact allocation history');need(work.init.old.ledger(r)['game_bytes']==baseline,'source cleanup restores retained game accounting');need(r.consume('close')==c['helper_cleanup'] and r.wire==len(c['native_trace']),'whole normal native trace consumed with no extra operations');return dict(name=c['name'],scene_capture=c['scene_capture'],continuous_original_instructions=count,continuous_original_writes=c['step']['writes'],source_initialization_and_cleanup_instructions=sum(counts),actual_source_OS_calls=sum(len(s['result']['api_calls']) for s in c['steps'])+len(c['step']['api_calls']),full_file_bytes=262168,vector_bytes=88,complete_final_CPU_memory=True,original_vector_and_record_constructors=True,normal_native_cleanup=True,fresh_CRT_domain_reconstructed=True,historical_heap_restored=False,image_loader_completed=False,R3_complete=False)

def verify(r):
 need(r['schema_version']==1 and r['fresh_CRT_domain_reconstructed']is True and r['new_game_roots']==r['game_function_substitutions']==r['IAT_rebindings']==0 and r['supplemental_cleanup_roots_per_case']==4,'honest continuous source/resource reconstruction contract')
 for k in ('historical_heap_restored','new_window','new_GPU','new_OS_input','full_CRT_startup_replayed','image_loader_completed','same_native_lifetime','R3_complete','R6_complete'):need(r[k]is False,'no unsupported completion claim '+k)
 need([(c['name'],c['scene_capture']) for c in r['cases']]==[(n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],'all six retained branches');return dict(schema_version=1,cases=[verify_case(c) for c in r['cases']],six_continuous_original_IMAGE_prefixes_verified=True,all_CRT_projection_bytes_source_backed=True,historical_heap_restored=False,new_GPU=False,interactive_desktop_required=False,image_loader_completed=False,R3_complete=False,R6_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable proof')
 r=verify(json.loads(gzip.decompress((ROOT/a.report).read_bytes())));out.write_text(json.dumps(r,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('six retained original IMAGE prefixes independently verified',flush=True)
