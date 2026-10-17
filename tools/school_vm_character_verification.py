"""Independent continuous source/ABI/state proof and immutable private CPU/memory loads."""
import hashlib,pickle,struct
from functools import lru_cache
from tools.school_vm_character import *
from tools.school_vm_panel_verification import load_verified_checkpoint as load_parent,fresh_identities as parent_identities,REPORTS as PARENT_REPORTS,SHAS as PARENT_SHAS,read_memory,retained,pinned
from tools.school_world_life_codec import unpack
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX,UC_X86_REG_ECX
PARENT=PARENT_REPORTS['character_entry'];PARENT_SHA=PARENT_SHAS['character_entry']
REPORTS={p:ROOT/f'analysis/school-vm-character-{p}-v1-20261017.json.gz' for p in PHASES};SHAS={p:None for p in PHASES}
SHAS['layer_entry']='180e55eb7e7822b87eebceb007d3d59c20fb5b157f57caae3d17537d6fbd1f31'
SHAS['overlay']='e26da8892f05bcf5e0f6417866f1144c03c6a447ddd85c0b7d1ffe0fe732883b'
SHAS['handler']='4cdc6b9d12b78ef1049590647a3fd3abc5ca17fbb7fa2690f81871185bff5c0d'
SHAS['template']='047e6e1d9177f1af290cf9bf77a0a7bbb655596e539457c82aea614c6e415ef1'

@lru_cache(maxsize=3)
def seed(name):
 payload,cp=load_parent(name,'character_entry');before=[dict(pointer=a,bytes=n,hex=read_memory(payload,a,n).hex()) for a,n in REGIONS];ptr=int.from_bytes(read_memory(payload,TACT+0x64,4),'little');tex=int.from_bytes(read_memory(payload,BANK,4),'little');inputs=dict(script_pointer=ptr,script_sha256=SCRIPT_SHA,driver='continuous_original_character_VM_task',texture_record=dict(pointer=tex,bytes=84,hex=read_memory(payload,tex,84).hex()),template=dict(pointer=TABLE,bytes=38,hex=read_memory(payload,TABLE,38).hex(),index=4,layer=7));ranges=[];exclusions=[(STACK,STACK+65536)]+[(a,a+n) for a,n in REGIONS]
 for start,buf in payload['memory']:
  pieces=[(start,start+len(buf))]
  for left,right in exclusions:pieces=[p for a,b in pieces for p in ((a,min(b,left)),(max(a,right),b)) if p[0]<p[1]]
  ranges.extend(dict(pointer=a,bytes=b-a,sha256=hashlib.sha256(buf[a-start:b-start]).hexdigest()) for a,b in pieces)
 return cp,before,inputs,ranges

@lru_cache(maxsize=12)
def checked(name,phase):
 c=next(c for c in pinned(REPORTS[phase],SHAS[phase])['cases'] if c['name']==name);return c,verify_case(c,phase)

def verify_calls(a,phase):
 rules={int(r['va'],16):r for r in source_contract()['functions']};calls=a['calls'];raw=SOURCE.read_bytes();l=layout();active=[(0x454CF0,BASE_SP),(0x4CE8F0,l['vm'])]
 if phase=='handler':active.append((ENTRY,l['vm']-144))
 wanted_calls=call_protocol(phase,a['inputs'],a['before'])
 if len(calls)!=len(wanted_calls) or any((c['va'],c['return_va'],c['args'])!=(hex(va),hex(ret),args) or type(c['receiver']) is not int or (recv is not None and c['receiver']!=recv) for c,(va,ret,recv,args) in zip(calls,wanted_calls)):raise ValueError('VM character exact source calls/receivers/full argument words')
 for c in calls:
  va=int(c['va'],16);ret=int(c['return_va'],16);op=raw[ret-BASE-5:ret-BASE]
  if op[0]!=0xE8 or ret+struct.unpack_from('<i',op,1)[0]!=va:raise ValueError('VM character original E8 call bytes')
  owner=next((p for p,r in rules.items() if p<=ret-5<int(r['end'],16)),None)
  while active and active[-1][0]!=owner:active.pop()
  if not active:raise ValueError('VM character retained original source caller')
  wanted=active[-1][1]-rules[owner]['frame']-rules[va]['args']*4-4
  if c['sp']!=wanted or len(c['args'])!=rules[va]['args']:raise ValueError('VM character complete retained ABI stack')
  active.append((va,c['sp']))
 returns=[]
 for c in calls:
  va=int(c['va'],16);eax=ecx=None
  if va==0x4C1EB0:eax=c['args'][2];ecx=2
  elif va==0x4CC600:eax=(LAYER&0xFFFFFF00)|1;ecx=(LAYER&0xFFFF0000)|8
  elif va==0x4CC0F0 and phase=='handler':eax=0;ecx=LAYER
  elif va==0x4CC7D0:eax=0xFFFFFF01;ecx=LAYER
  elif va==0x407AD0:eax=1;ecx=l['packet']
  elif va==0x4D29E0:eax=0xCCCCCCCC;ecx=0
  elif va==0x4CD850:eax=0;ecx=255
  if eax is not None:returns.append(dict(va=rules[va]['ret'],return_va=c['return_va'],sp=c['sp'],eax=eax,ecx=ecx))
 if phase=='handler':returns.append(dict(va='0x4c5fbb',return_va='0x4ced48',sp=l['vm']-144,eax=1,ecx=0))
 if phase=='overlay':returns=sorted(returns,key=lambda r:r['va']=='0x4d2b83')
 if a['returns']!=returns:raise ValueError('VM character actual critical return instructions/values')

def verify_case(c,phase):
 if phase not in PHASES or c['name'] not in ('initial','student9_waiting','fifth_class'):raise ValueError('VM character known case/phase')
 cp,before,inputs,ranges=seed(c['name'])
 if phase in PREVIOUS:
  parent,before=checked(c['name'],PREVIOUS[phase]);cp=parent['continuation_checkpoint']
 a=unpack(c['actual']);expected=project(phase,inputs,before)
 if c['prior_checkpoint']!=cp or a['phase']!=phase or a['inputs']!=inputs or a['before']!=before or any(a[k]!=v for k,v in expected.items()):raise ValueError('VM character complete independent source state/CPU/provenance')
 verify_calls(a,phase);visited=set(a['visited']);required={va for va,ret,recv,args in call_protocol(phase,inputs,before)};forbidden={STOP[phase],0x4CE9C5,0x4C4B80,0x425DE0,0x454CF0,0x4CE8F0,0x4D03B6,0x454EC1,0x410310,0x4CBF90,0x4CC17D,0x4CC1D1}
 if a['pending']:required.remove(STOP[phase])
 if phase=='template':required|={0x4CC64E,0x4CC6A2,0x4CC6CC};forbidden.add(0x4C5FBB)
 elif phase=='handler':required|={0x4CC177,0x4CC38E,0x4CC39B,0x4CC89C,0x4C5FBB}
 elif phase=='overlay':required|={0x407B17,0x408124,0x4D2DB3,0x4D2B83}
 else:required|={0x4CA330,0x4CA34A,0x4CA375,0x4CD8CB};forbidden|={0x4CA37A,0x4CA417}
 end=next(int(r['end'],16) for r in source_contract()['functions'] if int(r['va'],16)==0x4CA600)
 if not required<=visited or forbidden&visited or any(0x4CA600<=a<end for a in visited):raise ValueError('VM character original branches and unexecuted graphics body')
 if a['owned_bodies_stubbed'] is not False or a['platform_adapters']!=[] or a['debug_stack_check_adapter'] is not True or a['new_root_calls']!=0:raise ValueError('VM character continuous native/no new platform or root authority')
 retained(a)
 if a['retained_ranges']!=ranges or a['retained_bytes']!=sum(r['bytes'] for r in ranges):raise ValueError('VM character all parent retained bytes')
 cp=c['continuation_checkpoint']
 if cp['path']!=f'.venv-audit/vm-character-{phase}-{c["name"]}.pkl' or cp['pending_eip']!=hex(STOP[phase]) or cp['runtime_or_original_save'] is not False:raise ValueError('VM character fixed private checkpoint identity')
 return expected['after']

def fresh_identities(phase):
 parent_identities('character_entry')
 if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA256 or hashlib.sha256(SCRIPT.read_bytes()).hexdigest()!=SCRIPT_SHA:raise ValueError('VM character fresh source before unpickle')
 while True:
  if phase not in SHAS or SHAS[phase] is None or hashlib.sha256(REPORTS[phase].read_bytes()).hexdigest()!=SHAS[phase]:raise ValueError('VM character fresh current/ancestor report SHA before unpickle')
  if phase not in PREVIOUS:break
  phase=PREVIOUS[phase]

def envelope(r,phase):
 if r['phase']!=phase or r['source_contract']!=source_contract() or r['parent_report']!=PARENT.relative_to(ROOT).as_posix() or r['parent_sha256']!=PARENT_SHA or len(r['cases'])!=3 or {c['name'] for c in r['cases']}!={'initial','student9_waiting','fifth_class'} or r['new_root_calls']!=0 or any(r.get(k) is not False for k in ('graphics_list_executed','GPU_executed','dialogue_executed','VM_returned','task_returned','full_outer_frame_executed','persistent_write_authority')):raise ValueError('VM character source/parent/scope envelope')

def verify_payload(payload,c,phase,after):
 a=unpack(c['actual']);cpu=payload['cpu']
 if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=c['name'] or payload['phase']!=phase or payload['evidence_kind']!='private_original_vm_character_'+phase or payload['pending_eip']!=STOP[phase]:raise ValueError('VM character private source/case identity')
 observed={k:cpu.reg_read(reg) for k,reg in zip(('EIP','ESP','EBP','EAX','ECX'),(UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX,UC_X86_REG_ECX))}
 if observed!=a['CPU']:raise ValueError('VM character private actual CPU')
 for row in after+([] if a['packet'] is None else [a['packet']]):
  if read_memory(payload,row['pointer'],row['bytes']).hex()!=row['hex']:raise ValueError('VM character full private owned/packet memory')
 if read_memory(payload,BASE_SP-4,8)!=struct.pack('<II',BASE_SP-4,RETURN):raise ValueError('VM character private original root stack')
 for at,value in ((layout()['vm'],0x454D90),(layout()['vm']-4,BASE_SP-4),(layout()['vm']-8,VM),(layout()['vm']-20,1)):
  if read_memory(payload,at,4)!=struct.pack('<I',value):raise ValueError('VM character private original VM caller/locals')
 pending=a['pending']
 if pending and read_memory(payload,pending['sp'],4*(len(pending['args'])+1))!=struct.pack('<'+'I'*(len(pending['args'])+1),int(pending['return_va'],16),*pending['args']):raise ValueError('VM character private actual pending arguments')
 if phase=='template':
  sp=layout()['vm']-144
  for at,wanted in ((sp,struct.pack('<4I',0x4CED48,0,a['inputs']['script_pointer']+660,1)),(sp-4,struct.pack('<I',layout()['vm']-4)),(sp-8,struct.pack('<I',VM))):
   if read_memory(payload,at,len(wanted))!=wanted:raise ValueError('VM character private original handler stack')
 if phase=='layer_entry':
  sp=layout()['vm']-132
  for at,value in ((sp,0x4D028E),(sp-4,layout()['vm']-4),(sp-8,LAYER)):
   if read_memory(payload,at,4)!=struct.pack('<I',value):raise ValueError('VM character private original active layer stack')
 for row in a['retained_ranges']:
  if hashlib.sha256(read_memory(payload,row['pointer'],row['bytes'])).hexdigest()!=row['sha256']:raise ValueError('VM character all private retained bytes')

def load_verified_checkpoint(name,phase):
 fresh_identities(phase);r=pinned(REPORTS[phase],SHAS[phase]);envelope(r,phase);c=next((c for c in r['cases'] if c['name']==name),None)
 if c is None:raise ValueError('VM character known private case')
 after=verify_case(c,phase);cp=c['continuation_checkpoint'];raw=(ROOT/cp['path']).read_bytes()
 if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('VM character file SHA before unpickle')
 payload=pickle.loads(raw);verify_payload(payload,c,phase,after);return payload,cp
