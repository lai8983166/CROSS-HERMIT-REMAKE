"""Independent full-sprite/ABI/read-boundary proof and immutable checkpoint loading."""
import hashlib,pickle,struct
from functools import lru_cache
from tools.school_vm_graphics import *
from tools.school_vm_character_verification import load_verified_checkpoint as load_parent,fresh_identities as parent_identities,REPORTS as PARENT_REPORTS,SHAS as PARENT_SHAS,read_memory,retained,pinned
from tools.school_world_life_codec import unpack
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX,UC_X86_REG_ECX
PARENT=PARENT_REPORTS['layer_entry'];PARENT_SHA=PARENT_SHAS['layer_entry']
REPORTS={p:ROOT/f'analysis/school-vm-graphics-{p}-v1-20261017.json.gz' for p in PHASES};SHAS={p:None for p in PHASES}
SHAS['graphics']='3e8458505616476975ecf27b76f69580e34c8fa220d927f3f87413524a642498'

@lru_cache(maxsize=3)
def seed(name):
 payload,cp=load_parent(name,'layer_entry');before=[dict(pointer=a,bytes=n,hex=read_memory(payload,a,n).hex()) for a,n in REGIONS];ptr=int.from_bytes(read_memory(payload,TACT+0x64,4),'little');tex=int.from_bytes(read_memory(payload,BANK,4),'little');table=read_memory(payload,FRAME,50);inputs=dict(script_pointer=ptr,script_sha256=SCRIPT_SHA,driver='continuous_original_graphics_VM_task',texture_record=dict(pointer=tex,bytes=84,hex=read_memory(payload,tex,84).hex()),frame_table=dict(pointer=FRAME,bytes=50,hex=table.hex(),rows=[list(struct.unpack_from('<6h',table,i*12)) for i in range(4)]),manager_owner=int.from_bytes(read_memory(payload,MANAGER,4),'little'));ranges=[];exclusions=[(STACK,STACK+65536)]+[(a,a+n) for a,n in REGIONS]
 for start,buf in payload['memory']:
  pieces=[(start,start+len(buf))]
  for left,right in exclusions:pieces=[p for a,b in pieces for p in ((a,min(b,left)),(max(a,right),b)) if p[0]<p[1]]
  ranges.extend(dict(pointer=a,bytes=b-a,sha256=hashlib.sha256(buf[a-start:b-start]).hexdigest()) for a,b in pieces)
 return cp,before,inputs,ranges

@lru_cache(maxsize=9)
def checked(name,phase):
 c=next(c for c in pinned(REPORTS[phase],SHAS[phase])['cases'] if c['name']==name);return c,verify_case(c,phase)

def verify_calls(a,phase):
 rules={int(r['va'],16):r for r in source_contract()['functions']};calls=a['calls'];raw=SOURCE.read_bytes();v=layout()['vm'];active=[(0x454CF0,BASE_SP),(0x4CE8F0,v),(0x4CA1B0,v-132)]
 if phase=='owner_read':active.append((0x410310,v-276))
 wanted_calls=call_protocol(phase,a['inputs'],a['before'])
 if len(calls)!=len(wanted_calls) or any((c['va'],c['return_va'],c['args'])!=(hex(va),hex(ret),args) or type(c['receiver']) is not int or (recv is not None and c['receiver']!=recv) for c,(va,ret,recv,args) in zip(calls,wanted_calls)):raise ValueError('VM graphics exact original calls/receivers/full arguments')
 for c in calls:
  va=int(c['va'],16);ret=int(c['return_va'],16);op=raw[ret-BASE-5:ret-BASE]
  if op[0]!=0xE8 or ret+struct.unpack_from('<i',op,1)[0]!=va:raise ValueError('VM graphics original E8 bytes')
  owner=next((p for p,r in rules.items() if p<=ret-5<int(r['end'],16)),None)
  while active and active[-1][0]!=owner:active.pop()
  if not active:raise ValueError('VM graphics retained original source caller')
  wanted=active[-1][1]-rules[owner]['frame']-rules[va]['args']*4-4
  if c['sp']!=wanted or len(c['args'])!=rules[va]['args']:raise ValueError('VM graphics complete original ABI/SEH stack')
  active.append((va,c['sp']))
 def result(c,eax,ecx):return dict(va=rules[int(c['va'],16)]['ret'],return_va=c['return_va'],sp=c['sp'],eax=eax,ecx=ecx)
 returns=[]
 if phase=='graphics':
  sprites=[c for c in calls if c['va']=='0x4cbdb0'];draws=[c for c in calls if c['va']=='0x407ad0']
  for sprite,draw in zip(sprites,draws):returns.extend([result(draw,1,positions()['packet']),result(sprite,0xCCCCCC01,0)])
  returns.append(result(calls[0],24,FRAME))
 elif phase=='rectangle':returns=[result(calls[0],0,204)]
 if a['returns']!=returns:raise ValueError('VM graphics actual original critical returns')

def verify_case(c,phase):
 if phase not in PHASES or c['name'] not in ('initial','student9_waiting','fifth_class'):raise ValueError('VM graphics known phase/case')
 cp,before,inputs,ranges=seed(c['name'])
 if phase in PREVIOUS:
  parent,before=checked(c['name'],PREVIOUS[phase]);cp=parent['continuation_checkpoint']
 a=unpack(c['actual']);expected=project(phase,inputs,before)
 if c['prior_checkpoint']!=cp or a['phase']!=phase or a['inputs']!=inputs or a['before']!=before or any(a[k]!=v for k,v in expected.items()):raise ValueError('VM graphics complete independent state/CPU/packets/boundary/provenance')
 verify_calls(a,phase);visited=set(a['visited']);required={va for va,ret,recv,args in call_protocol(phase,inputs,before)};forbidden={STOP[phase],0x40DCD0,0x424F80,0x56DB00,0x40E32C,0x4103E0,0x4CA417,0x4D03B6,0x454EC1,0x425DE0,0x454CF0}
 if a['pending']:required.remove(STOP[phase])
 if phase=='graphics':required|={0x4CA650,0x4CA655,0x4CA711,0x4CBEDC,0x4CBEF6,0x407B17,0x408124};forbidden.add(0x407B21)
 elif phase=='rectangle':required|={0x4CA397,0x4CD8CB,0x4CA404,0x410340}
 else:required|={0x40E2CB,0x40E2CE}
 clip_end=next(int(r['end'],16) for r in source_contract()['functions'] if int(r['va'],16)==0x40E2A0)
 later_clip=any((0x40E2A0 if phase=='rectangle' else 0x40E2D0)<=at<clip_end for at in visited) if phase!='graphics' else False
 if not required<=visited or forbidden&visited or later_clip:raise ValueError('VM graphics original branches and unexecuted target read')
 if a['owned_bodies_stubbed'] is not False or a['platform_adapters']!=[] or a['debug_stack_check_adapter'] is not True or a['new_root_calls']!=0:raise ValueError('VM graphics native continuous/no extra platform or root scope')
 retained(a)
 if a['retained_ranges']!=ranges or a['retained_bytes']!=sum(r['bytes'] for r in ranges):raise ValueError('VM graphics all parent retained bytes')
 cp=c['continuation_checkpoint']
 if cp['path']!=f'.venv-audit/vm-graphics-{phase}-{c["name"]}.pkl' or cp['pending_eip']!=hex(STOP[phase]) or cp['runtime_or_original_save'] is not False:raise ValueError('VM graphics fixed private checkpoint identity')
 return expected['after']

def fresh_identities(phase):
 parent_identities('layer_entry')
 if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA256 or hashlib.sha256(SCRIPT.read_bytes()).hexdigest()!=SCRIPT_SHA:raise ValueError('VM graphics fresh source before unpickle')
 while True:
  if phase not in SHAS or SHAS[phase] is None or hashlib.sha256(REPORTS[phase].read_bytes()).hexdigest()!=SHAS[phase]:raise ValueError('VM graphics fresh current/ancestor report SHA before unpickle')
  if phase not in PREVIOUS:break
  phase=PREVIOUS[phase]

def envelope(r,phase):
 if r['phase']!=phase or r['source_contract']!=source_contract() or r['parent_report']!=PARENT.relative_to(ROOT).as_posix() or r['parent_sha256']!=PARENT_SHA or len(r['cases'])!=3 or {c['name'] for c in r['cases']}!={'initial','student9_waiting','fifth_class'} or r['new_root_calls']!=0 or any(r.get(k) is not False for k in ('queue_executed','clipping_returned','GPU_executed','dialogue_executed','VM_returned','task_returned','full_outer_frame_executed','persistent_write_authority')):raise ValueError('VM graphics source/parent/scope envelope')

def verify_payload(payload,c,phase,after):
 a=unpack(c['actual']);cpu=payload['cpu'];v=layout()['vm']
 if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=c['name'] or payload['phase']!=phase or payload['evidence_kind']!='private_original_vm_graphics_'+phase or payload['pending_eip']!=STOP[phase]:raise ValueError('VM graphics private source/case identity')
 observed={k:cpu.reg_read(reg) for k,reg in zip(('EIP','ESP','EBP','EAX','ECX'),(UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX,UC_X86_REG_ECX))}
 if observed!=a['CPU']:raise ValueError('VM graphics private actual CPU')
 for row in after+([] if a['packet'] is None else [a['packet']]):
  if read_memory(payload,row['pointer'],row['bytes']).hex()!=row['hex']:raise ValueError('VM graphics all private owned/packet memory')
 if read_memory(payload,BASE_SP-4,8)!=struct.pack('<II',BASE_SP-4,RETURN) or read_memory(payload,MANAGER,4)!=bytes(4) or read_memory(payload,FRAME,50).hex()!=a['inputs']['frame_table']['hex']:raise ValueError('VM graphics private root/owner/source-table proof')
 wanted_stack=[(v,0x454D90),(v-4,BASE_SP-4),(v-8,VM),(v-20,1),(v-132,0x4D028E),(v-136,v-4),(v-140,LAYER)]
 if phase in ('rectangle','owner_read'):wanted_stack.extend([(v-276,0x4CA409),(v-280,v-136),(v-284,MANAGER)])
 if phase=='owner_read':wanted_stack.extend([(v-384,0x410345),(v-388,v-280),(v-392,MANAGER)])
 for at,value in wanted_stack:
  if read_memory(payload,at,4)!=struct.pack('<I',value):raise ValueError('VM graphics private original VM/layer/rectangle/clip stack')
 if phase=='graphics':
  args=call_protocol(phase,a['inputs'],a['before'])[0][3]
  if read_memory(payload,v-264,20)!=struct.pack('<5I',*args):raise ValueError('VM graphics private original cdecl caller arguments')
 else:
  if read_memory(payload,v-272,28)!=struct.pack('<7I',*RECT) or read_memory(payload,v-384,20)!=struct.pack('<5I',0x410345,*RECT[:4]):raise ValueError('VM graphics private exact rectangle/clip arguments')
 for row in a['retained_ranges']:
  if hashlib.sha256(read_memory(payload,row['pointer'],row['bytes'])).hexdigest()!=row['sha256']:raise ValueError('VM graphics all private retained bytes')

def load_verified_checkpoint(name,phase):
 fresh_identities(phase);r=pinned(REPORTS[phase],SHAS[phase]);envelope(r,phase);c=next((c for c in r['cases'] if c['name']==name),None)
 if c is None:raise ValueError('VM graphics known private case')
 after=verify_case(c,phase);cp=c['continuation_checkpoint'];raw=(ROOT/cp['path']).read_bytes()
 if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('VM graphics file SHA before unpickle')
 payload=pickle.loads(raw);verify_payload(payload,c,phase,after);return payload,cp
