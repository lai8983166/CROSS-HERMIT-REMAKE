"""Independent original x86 replay and owned native transcript audit of fixtures."""
import gzip,json,struct
from pathlib import Path
from tools import school_retained_crt_fixture as work
from tools.school_retained_render_pipeline_verification import Replay as SourceReplay

base=work.base;ROOT=work.ROOT;need=base.need;word=base.word;sha=base.sha
LABELS=['reset_source_game_accounting','allocate_source_262168','allocate_source_88_concurrently','free_source_first_while_second_alive','free_source_second','source_complete_SC004_file_loader','free_source_file_buffer']
API_ORDER=[[],['EnterCriticalSection','HeapAlloc','LeaveCriticalSection'],['EnterCriticalSection','HeapAlloc','LeaveCriticalSection'],['EnterCriticalSection','IsBadReadPtr','IsBadWritePtr','HeapValidate','LeaveCriticalSection','EnterCriticalSection','IsBadReadPtr','IsBadWritePtr','HeapValidate','HeapFree','LeaveCriticalSection'],['EnterCriticalSection','IsBadReadPtr','IsBadWritePtr','HeapValidate','LeaveCriticalSection','EnterCriticalSection','IsBadReadPtr','IsBadWritePtr','HeapValidate','HeapFree','LeaveCriticalSection'],['GetCurrentDirectoryA','CreateFileA','GetFileSize','EnterCriticalSection','HeapAlloc','LeaveCriticalSection','ReadFile','CloseHandle'],['EnterCriticalSection','IsBadReadPtr','IsBadWritePtr','HeapValidate','LeaveCriticalSection','EnterCriticalSection','IsBadReadPtr','IsBadWritePtr','HeapValidate','HeapFree','LeaveCriticalSection']]

def protocol(r):
 need(r['schema_version']==1 and r['original_source_executed']is True,'source fixture schema')
 for k in ('retained_heap_restored','retained_integration','R3_complete','new_window','new_GPU','new_OS_input','other_heap_modes_tested'):need(r[k]is False,'honest isolated fixture scope '+k)
 need(r['debug_tracking_enabled']is True and r['heap_mode']==1,'debug heap tracking retained in test')
 need(r['fixture_inputs']['kind']=='separate declared function-test inputs, never retained state','explicit fixture distinction');need(r['fixture_inputs']['source_sha256']==work.SOURCE_SHA,'source provenance')
 need([s['label'] for s in r['steps']]==LABELS,'seven exact declared source roots')
 need([[a['name'] for a in s['result']['api_calls']] for s in r['steps']]==API_ORDER,'complete original API order')
 need(r['helper_exit_code']==0 and r['helper_cleanup']==dict(all_owned_resources_released=True,heap_destroyed=True,critical_deleted=True,open_files=0,allocations=0,depth=0,forced_cleanup=False),'normal source-owned cleanup required')
 h=r['native_hello'];need(h['pointer_bytes']==4 and h['window_created']is h['GPU_created']is False and h['heap']>0 and h['critical']>0 and Path(h['directory']).resolve()==work.platform.INSTALLED.resolve(),'owned headless native lifetime')
 need(r['helper_build']['source_sha256']==sha(work.platform.SOURCE.read_bytes()) and r['helper_build']['compiler_sha256']==sha(work.platform.COMPILER.read_bytes()) and r['helper_build']['machine']==0x14c,'helper source/compiler provenance')
 p=Path(r['helper_build']['helper_path']);need(work.platform.machine(p)==0x14c and sha(p.read_bytes())==r['helper_build']['helper_sha256'],'actual compiled x86 helper identity')
 need(len(r['native_trace'])==72,'bounded complete actual API/mirror transcript')
 for i,t in enumerate(r['native_trace']):need(t['request']['id']==t['reply']['id']==i+1 and t['reply']['ok']is True,'ordered successful real API replies')

class Replay(SourceReplay):
 def __init__(self,report):
  self.case=report;self.objects={};self.locks={};self.wire=0;self.blocks={};self.history=[];self.depth=0;self.files=set();self.filebytes=(work.platform.INSTALLED/'DATA/ADV/BIN/SC004.BIN').read_bytes();need(sha(self.filebytes)==work.FILE_SHA,'independent installed file identity')
  declaration=work.initialize(self,report['native_hello']);need(base.canonical(declaration)==base.canonical(report['fixture_inputs']),'all explicitly declared test inputs/maps/CPU and source defaults')
 def consume(self,op,**args):
  need(self.wire<len(self.case['native_trace']),'bounded exact wire cursor');t=self.case['native_trace'][self.wire];need(t['request']==dict(id=self.wire+1,op=op,**args),'independent actual native request '+op);self.wire+=1;return t['reply']['result']
 def locate(self,p,n=1):
  found=[(a,b) for a,b in self.blocks.items() if a<=p and p+n<=a+b['bytes']];need(len(found)==1,'independent native allocation ownership/bounds');return found[0]
 def sync(self,p):
  b=self.blocks[p];raw=self.read(p,b['bytes']);r=self.consume('sync',pointer=b['native'],hex=raw.hex());need(r==dict(pointer=b['native'],hex=raw.hex()),'entire source/native mirror exact');return raw
 def api(self,a):
  sp=self.cpu()['ESP'];slot=a['import_slot'];need(slot in work.IMPORTS,'declared API slot');name,pop=work.IMPORTS[slot];args=[word(self.read(sp+4+i)) for i in range(0,pop,4)];ret=word(self.read(sp));need(a['name']==name and a['target']==a['va']==word(self.read(slot)) and a['sp']==sp and a['return_va']==ret and a['args']==args and a['pop']==pop and a['wire_start']==self.wire,'original source IAT/caller/full ABI and native cursor');maps=[];outputs=[];hello=self.case['native_hello']
  def put(p,b):outputs.append(dict(pointer=p,hex=b.hex()))
  if name in ('EnterCriticalSection','LeaveCriticalSection'):
   need(args==[0x80a4b0] and ret=={'EnterCriticalSection':0x5770d3,'LeaveCriticalSection':0x5770f4}[name],'source lock9 caller');op='enter' if name[0]=='E' else 'leave';self.depth+=1 if op=='enter' else -1;need(0<=self.depth<=4,'balanced source critical section');r=self.consume(op,critical=hello['critical']);need(r['depth']==self.depth and len(bytes.fromhex(r['critical_hex']))==24,'actual lock extent/depth');put(args[0],bytes.fromhex(r['critical_hex']));value=0
  elif name=='HeapAlloc':
   need(ret==0x57810c and args[:2]==[self.case['fixture_inputs']['heap_token_translation']['guest'],0] and self.depth>0,'original raw allocator and logical heap only');expected_size=[262208,128,262208][len(self.history)];need(args[2]==expected_size,'original debug overhead and 16-byte allocation alignment');r=self.consume('alloc',heap=hello['heap'],flags=0,bytes=expected_size);need(r['bytes']==expected_size and r['pointer']>0 and all(b['native']!=r['pointer'] for b in self.blocks.values()) and len(bytes.fromhex(r['hex']))==expected_size,'real fresh owned native allocation');p=work.HEAP+len(self.history)*0x200000;b=dict(guest=p,native=r['pointer'],bytes=expected_size,freed=False);self.blocks[p]=b;self.history.append(b);maps=[dict(pointer=p,bytes=(expected_size+4095)&~4095)];put(p,bytes.fromhex(r['hex']));value=p
  elif name in ('HeapValidate','HeapFree'):
   need(args[:2]==[self.case['fixture_inputs']['heap_token_translation']['guest'],0] and self.depth>0 and ret==(0x570170 if name=='HeapValidate' else 0x578915),'original native heap caller and owned logical token');p,b=self.locate(args[2]);need(p==args[2],'raw exact block');raw=self.sync(p);r=self.consume('validate' if name=='HeapValidate' else 'free',heap=hello['heap'],flags=0,pointer=b['native']);need(r==dict(value=1,pointer=b['native'],before_hex=raw.hex()),'actual successful native heap operation on complete source bytes');value=1
   if name=='HeapFree':
    size=[262168,88,262168][sum(h['freed'] for h in self.history)];need(raw[:size+36]==bytes([0xdd])*(size+36),'original entire debug block poisoned before native free');b['freed']=True;del self.blocks[p]
  elif name in ('IsBadReadPtr','IsBadWritePtr'):
   need(args[1]==32 and ret==(0x570018 if name=='IsBadReadPtr' else 0x570030),'source debug header range checks');p,b=self.locate(args[0],args[1]);self.sync(p);r=self.consume('badread' if name=='IsBadReadPtr' else 'badwrite',pointer=b['native'],offset=args[0]-p,bytes=args[1]);need(r==dict(value=0,pointer=b['native'],offset=args[0]-p,bytes=args[1]),'actual native readable/writable owned range');value=0
  elif name=='GetCurrentDirectoryA':
   need(ret==0x42ac7a and args==[260,0x7a0ebc],'original file directory caller');r=self.consume('directory',bytes=260);b=(str(work.platform.INSTALLED.resolve())+chr(0)).encode('mbcs');need(r==dict(value=len(b)-1,hex=b.hex()),'actual full installed working directory');put(args[1],b);value=len(b)-1
  elif name=='CreateFileA':
   need(ret==0x42ac9c and work.text(self,args[0])==b'data\\adv\\bin\\sc004.bin' and args[1:]==[0x80000000,1,0,3,1,0] and not self.files,'original read-only SC004 path/flags');r=self.consume('open',path='data\\adv\\bin\\sc004.bin',access=0x80000000,share=1,security=0,disposition=3,attributes=1,template=0);value=r['handle'];need(0<value<0xffffffff,'actual valid owned file handle');self.files.add(value)
  elif name=='GetFileSize':
   need(ret==0x42ad0d and args[0] in self.files and args[1]==0,'original owned size caller');r=self.consume('size',handle=args[0],high=0);need(r==dict(value=len(self.filebytes)),'actual full source file size');value=len(self.filebytes)
  elif name=='ReadFile':
   need(ret==0x42ad82 and args[0] in self.files and args[2]==len(self.filebytes) and args[4]==0,'original owned synchronous full ReadFile');p,b=self.locate(args[1],args[2]);need(args[1]==p+32,'source allocated user buffer');before=self.sync(p);r=self.consume('read',handle=args[0],pointer=b['native'],offset=32,bytes=len(self.filebytes),overlapped=0);after=before[:32]+self.filebytes+before[32+len(self.filebytes):];need(r==dict(value=1,read=len(self.filebytes),pointer=b['native'],before_hex=before.hex(),after_hex=after.hex()),'actual complete file read changes user bytes only');put(p,after);put(args[3],struct.pack('<I',len(self.filebytes)));value=1
  else:
   need(name=='CloseHandle' and ret==0x42ada5 and args[0] in self.files,'original owned source file close');need(self.consume('file_close',handle=args[0])==dict(value=1),'actual source CloseHandle success');self.files.remove(args[0]);value=1
  need(a['wire_end']==self.wire and a['value']==value and a['new_mappings']==maps and a['memory_outputs']==outputs and a['void_return_normalized']==(name in ('EnterCriticalSection','LeaveCriticalSection')),'independent complete OS outputs and typed translations')
  for r in maps:
   need(all(not(lo<r['pointer']+r['bytes'] and r['pointer']<=hi) for lo,hi,_ in self.u.mem_regions()),'fresh mirror maps');self.u.mem_map(r['pointer'],r['bytes'])
  for r in outputs:self.u.mem_write(r['pointer'],bytes.fromhex(r['hex']))
  self.u.reg_write(base.REGISTERS['EAX'],value);self.u.reg_write(base.REGISTERS['ESP'],sp+4+pop);self.u.reg_write(base.REGISTERS['EIP'],ret)

def header(raw,size,index,prev=0,nxt=0,payload=None):
 b=bytes.fromhex(raw);aligned=(size+36+15)&~15;need(len(b)==aligned,'entire aligned raw block');need(b[:32]==struct.pack('<7I',prev,nxt,0x594e28,141,size,1,index)+bytes([0xfd])*4,'independent original debug header/list/source-line/request/guard');need(b[32:32+size]==(bytes([0xcd])*size if payload is None else payload) and b[32+size:36+size]==bytes([0xfd])*4,'every user and guard byte')

def verify(report):
 protocol(report);r=Replay(report);counts=[];first=work.HEAP+32;second=first+0x200000;file=first+0x400000
 roots=[(0x4288e0,[]),(0x428a40,[262168]),(0x428a40,[88]),(0x428ad0,[first]),(0x428ad0,[second]),(0x42ae20,[work.PATH]),(0x428ad0,[file])]
 ledgers=[(0,0,0,0,0,1,0),(first-32,262168,first-32,262168,262168,2,262168),(first-32,262256,second-32,262256,262256,3,262256),(second-32,262256,second-32,88,262256,3,88),(0,262256,0,0,262256,3,0),(file-32,524424,file-32,262168,262256,4,262168),(0,524424,0,0,262256,4,0)]
 for i,s in enumerate(report['steps']):
  va,args=roots[i];need(s['root']==dict(va=va,args=args,sp=work.STACK+0xf000,return_va=work.RETURN,receiver=0),'independent declared original function root');a=s['result'];adapt=dict(s,result=dict(a,api_calls=[dict(c,va=c['target'],key='owned_headless_CRT_OS') for c in a['api_calls']]));counts.append(r.step(adapt));expected=dict(zip(('first','total','last','current','high','next_request','game_bytes'),ledgers[i]));need(work.ledger(r)==s['ledger']==expected,'independent source list/counter transition');need(base.memory_rows(r.u)==s['full_memory'] and base.canonical(base.architectural_cpu(r.u))==base.canonical(s['architectural_cpu']),'whole original memory and full CPU after every root')
  if i==1:
   b=r.read(first-32,262208).hex();need(report['first_allocation']==dict(pointer=first,raw_hex=b),'first source bytes captured');header(b,262168,1)
  elif i==2:
   for row,p,size,request,prev,nxt in zip(report['concurrent_allocations'],(first,second),(262168,88),(1,2),(0,first-32),(second-32,0)):
    b=r.read(p-32,(size+51)&~15).hex();need(row==dict(pointer=p,raw_hex=b),'both complete concurrently live blocks');header(b,size,request,prev,nxt)
  elif i==3:
   b=r.read(second-32,128).hex();need(report['remaining_allocation']==dict(pointer=second,raw_hex=b),'remaining live block after head unlink');header(b,88,2)
  elif i==5:
   p,b=r.locate(file,len(r.filebytes));r.sync(p);native=r.consume('readback',pointer=b['native']);raw=r.read(p,b['bytes']);need(native==dict(pointer=b['native'],hex=raw.hex()),'actual native full-buffer readback after original file return');need(report['file_allocation']==dict(pointer=file,raw_hex=raw.hex(),file_sha256=sha(r.filebytes),native_readback_wire_index=r.wire-1),'complete source file return/captured native readback');header(raw.hex(),262168,3,payload=r.filebytes)
 need(not r.blocks and not r.files and r.depth==0 and report['allocation_history']==r.history,'source releases every owned file/block and lock');need(r.consume('close')==report['helper_cleanup'] and r.wire==len(report['native_trace']),'normal entire helper shutdown transcript, no leftovers')
 need(counts==[33,65954,436,66251,734,68036,66254],'complete original instruction counts');return dict(schema_version=1,original_instructions_replayed=sum(counts),original_writes=sum(s['result']['writes'] for s in report['steps']),source_roots=7,actual_OS_calls=sum(len(s['result']['api_calls']) for s in report['steps']),actual_allocations=3,actual_frees=3,actual_source_file_reads=1,complete_file_bytes=len(r.filebytes),all_debug_headers_guards_and_CD_DD_fills_verified=True,concurrent_debug_unlink_verified=True,full_CPU_memory_after_each_root=True,normal_native_cleanup_verified=True,retained_heap_restored=False,retained_integration=False,R3_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable proof')
 result=verify(json.loads(gzip.decompress((ROOT/a.report).read_bytes())));out.write_text(json.dumps(result,indent=2)+chr(10),encoding='utf8',newline=chr(10));print(result,flush=True)
