"""Independent x86, recorded COM and real CRT ownership proof of IMAGE return."""
import copy,gzip,json,struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from tools import school_retained_image_return as work
from tools import school_retained_crt_image_verification as previous
from tools.school_retained_rendering import AddressSpace

ROOT=work.ROOT;base=work.base;need=work.need;word=work.word;canonical=work.canonical;sha=work.sha
LABELS=['original_heap_initialization','original_static_lock_initialization','original_static_lock_teardown','original_heap_teardown']

def protocol(c):
 need(c['name'] in ('initial','student9_waiting','fifth_class') and c['scene_capture'] in (76,77),'six known source branches');need([s['label'] for s in c['steps']]==LABELS and c['step']['root'] is None and c['step']['result']['boundary']==0x4cc0d2,'two source init/teardown roots and continuous IMAGE return');need(c['helper_exit_code']==0 and c['helper_cleanup']==dict(all_owned_resources_released=True,heap_destroyed=True,critical_deleted=True,open_files=0,allocations=0,depth=0,forced_cleanup=False),'source-owned normal native cleanup')
 h=c['initial_native_hello'];need(h['pointer_bytes']==4 and h['heap']==h['critical']==0 and h['critical_hex']=='' and h['window_created']is h['GPU_created']is False and Path(h['directory']).resolve()==work.old.init.platform.old.INSTALLED.resolve(),'headless owner without driver-precreated CRT resources');b=c['helper_build'];p=Path(b['helper_path']);need(b['source_sha256']==sha(work.old.init.platform.SOURCE.read_bytes()) and b['compiler_sha256']==sha(work.old.init.platform.old.COMPILER.read_bytes()) and b['machine']==work.old.init.platform.old.machine(p)==0x14c and b['helper_sha256']==sha(p.read_bytes()),'actual helper source/compiler/binary identity')
 for i,t in enumerate(c['native_trace']):need(t['request']['id']==t['reply']['id']==i+1 and t['reply']['ok']is True,'ordered native operations')
 p=c['projection'];need(p['kind']=='explicit fresh source-initialized CRT resource domain' and p['historical_heap_restored']is p['game_accounting_reset']is False and p['all_other_retained_bytes_unchanged']is True and [(r['pointer'],r['bytes'],r['role']) for r in p['rows']]==list(previous.EXPECTED_DOMAIN),'only the six original-source CRT ranges, no game/CPU reset');need(len(c['copy_rows'])==512,'all 512 original row memcpy invocations')

class Replay(previous.Replay):
 def configure(self,c):
  self.native,self.release,_=work.contracts();space=AddressSpace();space.next=0x6b001000;self.creation=space.result('recorded_portrait',self.native['COM_calls'][0]['result']);self.lock=space.result('recorded_portrait',self.native['COM_calls'][2]['result']);self.texture=self.creation['texture'];need(space.ledger()==c['typed_texture_projection'],'independent typed rebasing of all expired native addresses');self.gpu_count=0;self.renderer=word(self.read(0x7a49fc));self.device=word(self.read(self.renderer+0xb210));self.device_method=word(self.read(word(self.read(self.device))+80));self.copy_rows=[]
 def api(self,a):
  if a.get('kind')!='recorded_GPU_only':return super().api(a)
  index=self.gpu_count;need(0<=index<6 and a['index']==index,'bounded original texture lifecycle');slot=[80,56,64,68,56,8][index];pop={80:32,56:12,64:20,68:8,8:4}[slot];sp=self.cpu()['ESP'];ret=word(self.read(sp));args=[word(self.read(sp+4+i)) for i in range(0,pop,4)];target=self.device_method if index==0 else self.texture['methods'][str(slot)];need(a['target']==a['va']==target and a['sp']==sp and a['return_va']==ret==[0x403c8a,0x403cbe,0x40395e,0x4039d3,0x403a44,0x40378d][index] and a['args']==args and a['slot']==slot and a['pop']==pop,'original source COM object/method/full ABI/caller');outputs=[];maps=[];bp=self.cpu()['EBP'];record=0x50201024
  def put(p,b):outputs.append(dict(pointer=p,hex=b.hex()))
  if index==0:
   need(args==[self.device,256,512,1,0,25,1,record+44],'source portrait dimensions/format/pool');result=copy.deepcopy(self.creation);t=self.texture;maps=list(dict.fromkeys((p&~4095,4096) for p in (t['pointer'],t['vtable'],*t['methods'].values())));put(t['pointer'],struct.pack('<I',t['vtable']))
   for k,p in t['methods'].items():put(t['vtable']+int(k),struct.pack('<I',p))
   put(args[7],struct.pack('<I',t['pointer']))
  elif index in (1,4):
   need(args==[self.texture['pointer'],0,bp-(52 if index==1 else 36)],'original descriptor output');result=copy.deepcopy(self.native['COM_calls'][1]['result']);need(bytes.fromhex(result['hex'])==struct.pack('<8I',25,1,0,1,262144,0,256,512),'independent actual portrait descriptor');put(args[2],bytes.fromhex(result['hex']))
  elif index==2:
   need(args==[self.texture['pointer'],0,word(self.read(bp+8)),0,2048],'original lock output/flags');result=copy.deepcopy(self.lock);b=bytes.fromhex(result['hex']);need(len(b)==262144 and result['pitch']==512,'complete historical lock extent');p=result['bits']&~4095;maps=[(p,(result['bits']-p+len(b)+4095)&~4095)];put(result['bits'],b);put(args[2],struct.pack('<2I',512,result['bits']))
  elif index==3:
   need(args==[self.texture['pointer'],0],'source texture unlock');result=copy.deepcopy(self.native['COM_calls'][3]['result']);pixels=self.read(self.lock['bits'],262144);need(pixels==self.filebytes[24:] and a['uploaded_hex']==pixels.hex() and sha(pixels)==result['uploaded_sha256'],'independent every source A1R5G5B5 pixel and original upload buffer')
  else:
   need(args==[self.texture['pointer']] and self.release==dict(pointer=self.native['texture']['pointer'],unlock_hr=0,count=0),'only the newly reconstructed logical texture released');result=copy.deepcopy(self.release)
  value=result['count'] if index==5 else result['hr'];origin=dict(kind='historical_native_texture_release',response=self.release) if index==5 else dict(kind='historical_native_COM_response',call_index=1 if index==4 else index,response=self.native['COM_calls'][1 if index==4 else index]['result']);need(a['value']==value and a['result']==result and a['historical_origin']==origin and a['memory_outputs']==outputs and a['new_mappings']==[dict(pointer=p,bytes=n) for p,n in maps],'all pinned historical response bytes and only typed interface outputs')
  for p,n in maps:need(all(not(lo<p+n and p<=hi) for lo,hi,_ in self.u.mem_regions()),'new bounded logical GPU maps');self.u.mem_map(p,n)
  for o in outputs:self.u.mem_write(o['pointer'],bytes.fromhex(o['hex']))
  self.u.reg_write(base.REGISTERS['EAX'],value);self.u.reg_write(base.REGISTERS['ESP'],sp+4+pop);self.u.reg_write(base.REGISTERS['EIP'],ret);self.gpu_count+=1

def step(r,s):
 maps=[]
 for at in [r.device_method,*[word(r.read(k)) for k in work.old.init.IMPORTS]]:
  if not any(a<=at<=b for a,b,_ in r.u.mem_regions()):p=at&~4095;r.u.mem_map(p,4096);maps.append(dict(pointer=p,bytes=4096))
 need(maps==s['entry_mappings'],'only missing original platform entry pages');a=s['result']
 def observe(u,at,n,_):
  if at==0x56d4d0:
   sp=r.cpu()['ESP'];row=len(r.copy_rows);args=[word(r.read(sp+i)) for i in (4,8,12)];need(row<512 and args==[r.lock['bits']+row*512,0x50001038+row*512,512] and word(r.read(sp))==0x40483f,'independent full original memcpy row caller');r.copy_rows.append(dict(row=row,args=args,return_va=0x40483f))
 h=r.u.hook_add(UC_HOOK_CODE,observe)
 try:count=r.step(dict(s,result=dict(a,api_calls=[dict(q,va=q['target'],key='recorded_COM' if q.get('kind')=='recorded_GPU_only' else 'original_CRT_OS_leaf') for q in a['api_calls']])) )
 finally:r.u.hook_del(h)
 need(base.memory_rows(r.u)==s['full_memory'] and canonical(base.architectural_cpu(r.u))==canonical(s['architectural_cpu']) and work.old.init.old.ledger(r)==s['ledger'],'every final CPU register/mapped byte and source ledger');return count

def verify_after(r,c):
 after=c['after'];array=0x50201020;record=array+4;expected=bytearray(84);struct.pack_into('<2I',expected,40,r.device,r.texture['pointer']);struct.pack_into('<I4H',expected,52,25,256,512,256,512);struct.pack_into('<H',expected,68,2);expected[70:72]=bytes([205,205]);table=r.renderer+0x844+256;sp=r.cpu()['ESP'];pending=c['parent_boundary']['pending_image'];frames=work.old.parent.chain(r,[('resource',0x4cc26d)])
 need(after['record_hex']==r.read(record,84).hex()==expected.hex() and after['array_hex']==r.read(array,88).hex()==(struct.pack('<I',1)+expected).hex(),'all original completed record and untouched CD padding');need(after['table_pointer']==table and after['table_hex']==r.read(table,8).hex()==struct.pack('<2I',record,1).hex(),'original slot32 registration remains live');need(after['image_loaded_flag']==r.read(base.VM+0x92c0,1).hex()=='01' and after['vm_pc']==word(r.read(base.VM+28))==252,'source loaded flag only, no VM progress claim');need(after['pixel_hex']==r.read(r.lock['bits'],262144).hex()==r.filebytes[24:].hex(),'complete every-row source pixels');need(after['accounting']==word(r.read(0x765720))==c['accounting_before']+262144,'source texture byte accounting');need(after['SEH_hex']==r.read(0,4).hex()==c['source_entry_SEH_hex'],'original container restores source exception chain');need(after['natural_return']==dict(va=0x4cc0d2,sp=pending['sp']+12,ebp=pending['frames'][0]['bp'],eax=0) and r.cpu()['EIP']==0x4cc0d2 and sp==pending['sp']+12 and r.cpu()['EBP']==pending['frames'][0]['bp'] and r.cpu()['EAX']==0 and after['frames']==frames,'natural IMAGE ret8 and original resource frame, no new root');need(list(r.blocks)==[0x50201000] and r.history[0]['freed'] and not r.history[1]['freed'],'original file free and live vector ownership');previous.init.old.header(r.read(0x50201000,128).hex(),88,2,payload=struct.pack('<I',1)+expected);need(r.read(0x50001000,262204)==bytes([221])*262204,'original entire freed source block DD poisoned');need(work.old.init.old.ledger(r)==dict(first=0x50201000,total=262256,last=0x50201000,current=88,high=262256,next_request=3,game_bytes=c['game_accounting_baseline']+88),'independent source unlink/statistics after natural free')

def verify_case(c):
 protocol(c);r=Replay(c);counts=[]
 for s,va,args in zip(c['steps'][:2],(0x57b9d0,0x576f60),([1],[])):
  need(s['root']==dict(va=va,args=args,sp=0x2100f000,return_va=0x32000000,receiver=0),'original source initialization roots');counts.append(previous.replay_step(r,s))
 previous.project(r,c);need(r.read(0,4).hex()==c['source_entry_SEH_hex'],'source original IMAGE entry exception chain');p=c['prefix'];maps=[]
 for slot in work.old.init.IMPORTS:
  at=word(r.read(slot))
  if not any(a<=at<=b for a,b,_ in r.u.mem_regions()):p0=at&~4095;r.u.mem_map(p0,4096);maps.append(dict(pointer=p0,bytes=4096))
 need(maps==p['entry_mappings'],'only original CRT entry maps');prefix_count=r.step(dict(label=p['label'],root=None,result=dict(p,api_calls=[dict(a,va=a['target'],key='original_CRT_OS_leaf') for a in p['api_calls']])));need(prefix_count==69440 and base.memory_rows(r.u)==p['full_memory'] and canonical(base.architectural_cpu(r.u))==canonical(p['architectural_cpu']) and work.old.init.old.ledger(r)==p['ledger'],'entire newly owned original IMAGE prefix');previous.snapshot(r,dict(c,boundary=c['pending_texture']));r.configure(c);need(word(r.read(0x765720))==c['accounting_before'],'source original texture accounting baseline');count=step(r,c['step']);need(r.gpu_count==4 and r.copy_rows==c['copy_rows'],'all four COM replays and 512 independent original memcpy invocations');visited={x['va'] for x in c['step']['result']['instruction_counts']};need({0x403bd0,0x4046f0,0x56d4d0,0x428ad0,0x56f3b0,0x56f420}<=visited and c['step']['result']['instruction_counts'][0]['va']!=0,'original GPU body/memcpy/CRT free bodies executed');verify_after(r,c);raw=r.sync(0x50201000);block=r.blocks[0x50201000];reply=r.consume('readback',pointer=block['native']);need(reply==dict(pointer=block['native'],hex=raw.hex()) and c['readback']==dict(guest=0x50201000,wire_index=r.wire-1,result=reply),'full actual native vector readback after original file free')
 root=dict(va=0x41f4e0,args=[32],sp=0x2100f000,return_va=0x32000000,receiver=r.renderer+0x844);need(c['cleanup']['root']==root,'explicit original registered container cleanup root');cleanup_count=step(r,c['cleanup']);need(r.cpu()['ESP']==root['sp']+8 and r.gpu_count==6 and not r.blocks and r.read(c['after']['table_pointer'],8)==bytes(8) and word(r.read(0x765720))==c['accounting_before'] and work.old.init.old.ledger(r)['game_bytes']==c['game_accounting_baseline'],'source full vector destruction/table and counters balanced');visited={x['va'] for x in c['cleanup']['result']['instruction_counts']};need({0x41f4e0,0x403730,0x403a00,0x41f2a0,0x56de40,0x41f890,0x428ad0}<=visited,'original descriptor/release/vector destructor/free bodies')
 for s,va in zip(c['steps'][2:],(0x576fa0,0x57ba60)):
  need(s['root']==dict(va=va,args=[],sp=0x2100f000,return_va=0x32000000,receiver=0),'source original final lock/heap teardown');counts.append(previous.replay_step(r,s))
 need(not r.blocks and not r.files and not r.criticals and r.depth==0 and r.history==c['allocation_history'],'all and only live owned resources naturally gone');need(r.consume('close')==c['helper_cleanup'] and r.wire==len(c['native_trace']),'complete actual OS trace and normal helper exit');return dict(name=c['name'],scene_capture=c['scene_capture'],original_prefix_instructions=prefix_count,new_original_IMAGE_instructions=count,new_original_IMAGE_writes=c['step']['result']['writes'],supplemental_container_cleanup_instructions=cleanup_count,initialization_and_teardown_instructions=sum(counts),recorded_COM_calls=6,actual_OS_calls=sum(len(s['result']['api_calls']) for s in c['steps'])+len(c['prefix']['api_calls'])+sum(a.get('kind')!='recorded_GPU_only' for s in (c['step'],c['cleanup']) for a in s['result']['api_calls']),original_memcpy_rows=512,complete_pixels_bytes=262144,original_IMAGE_returned=True,original_file_free_executed=True,full_CPU_memory_verified=True,normal_native_cleanup=True,new_GPU=False,historical_heap_restored=False,R3_complete=False)

def verify(r):
 need(r['schema_version']==1 and r['platform_contract']==work.contracts()[2] and r['new_game_roots']==r['game_function_substitutions']==r['IAT_rebindings']==0,'source identity and original-function-only contract')
 for k in ('fresh_CRT_domain_reconstructed','recorded_GPU_only','original_IMAGE_returned','original_memcpy_executed','original_file_free_executed','supplemental_container_cleanup'):need(r[k]is True,'required source lifecycle '+k)
 for k in ('new_GPU','new_window','new_OS_input','same_native_lifetime','historical_heap_restored','handler_animation_completed','R3_complete','R6_complete'):need(r[k]is False,'honest remaining scope '+k)
 need([(c['name'],c['scene_capture']) for c in r['cases']]==[(n,s) for n in ('initial','student9_waiting','fifth_class') for s in (76,77)],'all six retained branches');return dict(schema_version=1,cases=[verify_case(c) for c in r['cases']],six_original_IMAGE_returns_verified=True,all_original_memcpy_pixels_and_source_frees_verified=True,recorded_GPU_only=True,new_GPU=False,interactive_desktop_required=False,handler_animation_completed=False,R3_complete=False,R6_complete=False)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable proof')
 result=verify(json.loads(gzip.decompress((ROOT/a.report).read_bytes())));out.write_text(json.dumps(result,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('six original IMAGE returns, memcpy rows and CRT/container cleanup independently verified',flush=True)
