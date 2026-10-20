"""Independent reconstruction and original VM/rectangle replay on pinned inputs."""
import gzip,hashlib,json,struct,zlib,base64
from collections import Counter
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from tools.school_retained_rendering import ROOT,TASK,BASE,SOURCE,SOURCE_SHA256,FRESH_GLOBALS,AddressSpace
from tools.school_renderer_init_emulation import REGISTERS
from tools.school_owner_startup import project_constructor,project_image
from tools.school_device_init import project_owner
from tools.school_device_init_verification import unpack
from tools.school_font_cache import HEAD,CACHE,COUNTER
from tools.school_font_caller import LAYER_BYTES,ARENA_BYTES,HEADS,ARENA
from tools.school_vm_graphics_verification import load_verified_checkpoint
from tools.school_world_mode_emulation import architectural_cpu

def need(v,msg):
 if not v:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def word(b,at=0):return struct.unpack_from('<I',b,at)[0]
def read_report(path):return json.loads(gzip.decompress((ROOT/path).read_bytes()))

def source_image(api):
 image=bytearray(project_image(api))
 for a,v in FRESH_GLOBALS.items():struct.pack_into('<I',image,a-BASE,v)
 struct.pack_into('<I',image,COUNTER-BASE,word(image,COUNTER-BASE)+3600+LAYER_BYTES+ARENA_BYTES)
 struct.pack_into('<I',image,HEAD-BASE,CACHE)
 return bytes(image)

def replay(u,actual):
 counts=Counter();ih=hashlib.sha256();wh=hashlib.sha256();writes=0;stop=actual['boundary'];raw=SOURCE.read_bytes()
 need(stop is not None and actual['pending'] is None and actual['api_calls']==[],'this reconstruction proof has no substituted platform/game calls')
 need({k:u.reg_read(r) for k,r in REGISTERS.items()}==actual['before_cpu'],'original continuation CPU')
 def code(uc,at,n,_):
  if at==stop:uc.emu_stop();return
  need(BASE<=at<0x592000,'unexpected original continuation external')
  b=bytes(uc.mem_read(at,n));need(b==raw[at-BASE:at-BASE+n],'original instruction bytes')
  counts[at]+=1;ih.update(struct.pack('<I',at)+b)
 def write(uc,access,at,n,value,_):
  nonlocal writes
  writes+=1;wh.update(struct.pack('<IIQ',at,n,value&0xffffffffffffffff))
 c=u.hook_add(UC_HOOK_CODE,code);w=u.hook_add(UC_HOOK_MEM_WRITE,write)
 try:u.emu_start(actual['before_cpu']['EIP'],0,count=2000000,timeout=120_000_000)
 finally:u.hook_del(c);u.hook_del(w)
 need({k:u.reg_read(r) for k,r in REGISTERS.items()}==actual['cpu'],'independent full general-register/flags return')
 need([dict(va=a,count=n) for a,n in sorted(counts.items())]==actual['instruction_counts'] and ih.hexdigest()==actual['instruction_sha256'],'independent original instruction stream')
 need(writes==actual['writes'] and wh.hexdigest()==actual['write_sha256'],'independent complete original writes')
 return sum(counts.values())

def verify(r):
 need(r['schema_version']==1 and r['source_sha256']==SOURCE_SHA256 and sha(SOURCE.read_bytes())==SOURCE_SHA256,'source identity')
 declaration=r['initialization'];raw=bytearray(SOURCE.read_bytes())
 for at,v in FRESH_GLOBALS.items():struct.pack_into('<I',raw,at-BASE,v)
 need(declaration['before_first_original_instruction'] and declaration['owner']==TASK and declaration['globals']=={hex(a):v for a,v in FRESH_GLOBALS.items()} and declaration['loaded_image_sha256']==sha(raw) and not declaration['original_code_modified'] and declaration['retained_checkpoint_not_loaded_yet'],'declared fresh source-backed loader inputs')
 space=AddressSpace()
 for row in r['address_translation']:need(space.guest(row['domain'],row['native'])==row['guest'],'typed native pointer ledger')
 for domain,proxy,wire in [('device',r['device_proxy_trace'],r['native_device_trace']),('GDI',r['GDI_proxy_trace'],r['native_GDI_trace'])]:
  for row in proxy:
   matches=[x for x in wire if {k:v for k,v in x['request'].items() if k!='id'}==dict(op=row['op'],**row['native_request']) and x['reply'].get('ok') is True and x['reply']['result']==row['native_result']]
   need(matches and space.result(domain,row['native_result'])==row['result'],'real native request/reply and explicit pointer translation')
 c=r['startup'];apis={a['name']:a['result'] for a in c['constructor']['platform_calls']}
 constructed=project_constructor(bytes([c['fill']])*0xc000,apis)
 need(unpack(c['constructor']['state']['owner'])==constructed and c['constructor']['native']['cpu']['EAX']==TASK,'independent original full owner constructor')
 device=c['device'];expected=project_owner(constructed,1024,768,c['hello']['window'],device['native']['live_results'])
 need(unpack(device['state']['owner'])==expected,'independent actual device initialization fields')
 final=unpack(c['startup_return']['state']['owner']);dev=word(final,0xb210)
 need(word(final,0x1058)==TASK and word(final,0x105c)==dev and dev and word(final,0xb20c),'source-created manager/device ownership')
 need(word(final,0x1060)==4096 and word(final,0x1064)==0x100000 and word(final,0x1068)==HEADS and word(final,0x106c)==ARENA,'original queue allocation/binding')
 need(word(final,0x1090) and word(final,0x1094) and word(final,0xb270) and struct.unpack_from('<H',final,0xb28e)[0]==1,'original font publications and constructor gate')
 need(c['startup_return']['cpu']['EAX']==0 and c['startup_return']['cpu']['EIP']==0x22000000 and c['startup_return']['full413450_returned'],'natural original renderer startup return')
 rc=r['reconstruction'];payload,cp=load_verified_checkpoint('initial','rectangle');need(cp==rc['checkpoint'],'pinned original VM ancestor')
 image=source_image(apis);expected_regions=[('original_manager_fonts',TASK+0x1058,final[0x1058:0x10b8]),('original_renderer',TASK+0xb180,final[0xb180:0xba20])]
 for name,at,n in [('original_constructor_table',0x765728,0x2c002),('original_timer',0x799ae0,16),('original_constructor_scalar',0x5ff530,4),('original_CRT_counter',COUNTER,4),('original_cache_head',HEAD,4)]:expected_regions.append((name,at,image[at-BASE:at-BASE+n]))
 need(rc['overlays']==[dict(name=name,pointer=at,bytes=len(b),hex=b.hex()) for name,at,b in expected_regions],'only original-initialization-owned overlays')
 u=Uc(UC_ARCH_X86,UC_MODE_32);maps=[]
 for start,b in payload['memory']:
  expected=bytearray(b)
  for name,at,contents in expected_regions:
   a=max(start,at);end=min(start+len(b),at+len(contents))
   if a<end:expected[a-start:end-start]=contents[a-at:end-at]
  u.mem_map(start,len(expected));u.mem_write(start,bytes(expected));maps.append(dict(pointer=start,bytes=len(b),parent_sha256=sha(b),reconstructed_sha256=sha(expected)))
 need(maps==rc['full_parent_maps'] and not rc['original_checkpoint_modified'] and rc['logical_rehydration'] and not rc['in_place_unmodified_checkpoint_resume'],'all retained logical memory and explicit reconstruction scope')
 u.context_restore(payload['cpu']);initial={k:u.reg_read(reg) for k,reg in REGISTERS.items()}
 need(rc['cpu_before']==rc['cpu_after']==initial,'retained original registers/stack')
 arch=rc['architectural_restore_recheck'];need(canonical(arch['actual'])==canonical(arch['expected'])==canonical(architectural_cpu(u)),'typed FPU/SIMD/system-register restore recheck')
 for q in c['startup_return']['queues']:
  evidence=q['buffer'];b=zlib.decompress(base64.b64decode(evidence['zlib_base64']))
  need(len(b)==evidence['bytes']==q['payload_bytes']+2*q['guard_bytes']<=0x102000 and sha(b)==evidence['sha256'],'source queue guard extent and identity')
  u.mem_map(q['pointer']-q['guard_bytes'],len(b));u.mem_write(q['pointer']-q['guard_bytes'],b)
 vm_instructions=replay(u,r['actual_VM_continuation']);packet=bytes(u.mem_read(ARENA,24))
 need(word(packet,4)==4 and packet[8]==1 and list(struct.unpack_from('<5H',packet,10))==[274,580,473,154,67] and word(packet,20)==0x223438,'original rectangle command from retained VM')
 task_instructions=replay(u,r['actual_task_return']);need(r['actual_task_return']['cpu']['EAX']==0,'original selected-task natural return')
 need(r['owned_device_exited'] and r['owned_GDI_exited'] and r['device_cleanup']['all_owned_resources_released'] and r['GDI_cleanup']['all_owned_resources_released'],'actual complete owned platform cleanup')
 need(r['device_cleanup']['gamma_device_restored'] and r['device_cleanup']['gamma_desktop_restored'],'actual gamma restoration')
 return dict(original_source_sha256=SOURCE_SHA256,retained_checkpoint=cp,full_parent_maps=len(maps),parent_bytes=sum(x['bytes'] for x in maps),original_rectangle_packet_hex=packet.hex(),VM_original_instructions=vm_instructions,task_original_instructions=task_instructions,R2_complete=False,GPU_output_accepted=False,R3_input_boundary=0x425f17)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('report');p.add_argument('--out',required=True);a=p.parse_args()
 result=verify(read_report(a.report));(ROOT/a.out).write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
 print(json.dumps(result,ensure_ascii=False))
