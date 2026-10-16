"""Independent source/call/whole-state verification of the original first-return continuation."""
import gzip,hashlib,json,pickle,struct
from functools import lru_cache
from tools.school_vm_draw import *
from tools.school_vm_present_verification import load_verified_checkpoint as load_parent,fresh_identities as parent_identities,REPORTS as PARENT_REPORTS,SHAS as PARENT_SHAS,read_memory,retained,pinned
from tools.school_world_life_codec import unpack
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX,UC_X86_REG_ECX

PARENT=PARENT_REPORTS['draw'];PARENT_SHA=PARENT_SHAS['draw']
REPORTS={p:ROOT/f'analysis/school-vm-draw-{p}-v1-20261016.json.gz' for p in PHASES};SHAS={p:None for p in PHASES}
SHAS['cleanup']='ce7544f3a3061ac0337ef79e1126e9bb8467ef4b4314519aecfc9262fee5d8f9'

@lru_cache(maxsize=3)
def seed(name):
    payload,cp=load_parent(name,'draw');before=[dict(pointer=a,bytes=n,hex=read_memory(payload,a,n).hex()) for a,n in REGIONS];pointer=int.from_bytes(read_memory(payload,TACT+0x64,4),'little');texture=int.from_bytes(read_memory(payload,BANK,4),'little');inputs=dict(script_pointer=pointer,script_sha256=SCRIPT_SHA,driver='continuous_original_task_VM',texture_record=dict(pointer=texture,bytes=84,hex=read_memory(payload,texture,84).hex()));exclusions=[(STACK,STACK+65536)]+[(a,a+n) for a,n in REGIONS];ranges=[]
    for start,buf in payload['memory']:
        pieces=[(start,start+len(buf))]
        for left,right in exclusions:pieces=[p for a,b in pieces for p in ((a,min(b,left)),(max(a,right),b)) if p[0]<p[1]]
        ranges.extend(dict(pointer=a,bytes=b-a,sha256=hashlib.sha256(buf[a-start:b-start]).hexdigest()) for a,b in pieces)
    return cp,before,inputs,ranges

@lru_cache(maxsize=9)
def checked(name,phase):
    c=next(c for c in pinned(REPORTS[phase],SHAS[phase])['cases'] if c['name']==name);return c,verify_case(c,phase)

def verify_calls(a,phase):
    rules={int(r['va'],16):r for r in source_contract()['functions']};calls=a['calls'];raw=SOURCE.read_bytes();l=layout()
    if [(int(c['va'],16),int(c['return_va'],16),c['receiver'],c['args']) for c in calls]!=call_protocol(phase):raise ValueError('VM draw exact source calls/receivers/arguments')
    active=[(0x4CE8F0,l['vm'])]
    if phase=='cleanup':active.extend([(0x4D29E0,l['overlay']),(0x4D2CA0,l['kind']),(0x4079C0,l['resource']),(0x407A50,l['drawbp']+4)])
    if phase=='task':active=[(0x454CF0,BASE_SP)]
    for index,c in enumerate(calls):
        va=int(c['va'],16);ret=int(c['return_va'],16);op=raw[ret-BASE-5:ret-BASE]
        if op[0]!=0xE8 or ret+struct.unpack_from('<i',op,1)[0]!=va:raise ValueError('VM draw original E8 call bytes')
        if phase=='cleanup' and not index:wanted=l['draw']
        else:
            owner=next((p for p,r in rules.items() if p<=ret-5<int(r['end'],16)),None)
            while active and active[-1][0]!=owner:active.pop()
            if not active:raise ValueError('VM draw retained source ABI caller')
            wanted=active[-1][1]-rules[owner]['frame']-rules[va]['args']*4-4
        if c['sp']!=wanted or len(c['args'])!=rules[va]['args']:raise ValueError('VM draw exact source ABI stack')
        active.append((va,c['sp']))

def verify_case(c,phase):
    if phase not in PHASES or c['name'] not in ('initial','student9_waiting','fifth_class'):raise ValueError('VM draw known phase/case')
    cp,before,inputs,ranges=seed(c['name'])
    if phase in PREVIOUS:
        parent,before=checked(c['name'],PREVIOUS[phase]);cp=parent['continuation_checkpoint']
    a=unpack(c['actual']);expected=project(phase,inputs,before)
    if c['prior_checkpoint']!=cp or a['phase']!=phase or a['before']!=before or a['inputs']!=inputs or any(a[k]!=v for k,v in expected.items()):raise ValueError('VM draw full source projection/provenance/packet/CPU')
    verify_calls(a,phase);l=layout()
    returns={'cleanup':[dict(va='0x408124',sp=l['draw'],return_va='0x407ab0',eax=1,ecx=l['packet']),dict(va='0x4d2b83',sp=l['overlay'],return_va='0x4d024f',eax=0xCCCCCCCC,ecx=0)],'vm':[dict(va='0x4d03b6',sp=l['vm'],return_va='0x454d90',eax=1,ecx=0)],'task':[dict(va='0x454ec1',sp=BASE_SP,return_va=hex(RETURN),eax=0,ecx=0)]}[phase]
    if a['returns']!=returns:raise ValueError('VM draw native actual return instructions/values')
    required={va for va,ret,recv,args in call_protocol(phase)};forbidden={STOP[phase],0x424F80,0x403A00,0x428AD0,0x4C7190}
    if phase=='cleanup':required|={0x407B0C,0x407B15,0x407B17,0x408124,0x4037D5,0x41FAE4,0x4209D2,0x4D2DB3,0x4D2B83};forbidden|={0x407B21,0x40378A,0x4037BB,0x41FA7F,0x41FAA8}
    elif phase=='vm':required|={0x4CA1FE,0x4CA5D0,0x4C9AC8,0x4CA029,0x4CD527,0x4CD54B,0x4D0327,0x4C7A0E,0x4CBC79,0x4D03B6};forbidden|={0x4CD520,0x4CD53C,0x4D033F,0x4CBA8E}
    else:required|={0x454DA0,0x454DC5,0x456404,0x456615,0x497AC6,0x497C2D,0x498339,0x498725,0x454EC1};forbidden|={0x454DA2,0x45640A,0x497ACC,0x49833F}
    if not required<=set(a['visited']) or forbidden&set(a['visited']):raise ValueError('VM draw source branches and unexecuted boundary')
    if a['owned_bodies_stubbed'] is not False or a['platform_adapters']!=[] or a['debug_stack_check_adapter'] is not True:raise ValueError('VM draw original bodies/adapters scope')
    retained(a)
    if a['retained_ranges']!=ranges or a['retained_bytes']!=sum(r['bytes'] for r in ranges):raise ValueError('VM draw exact entire parent retained coverage')
    cp=c['continuation_checkpoint']
    if cp['path']!=f'.venv-audit/vm-draw-{phase}-{c["name"]}.pkl' or cp['pending_eip']!=hex(STOP[phase]) or cp['runtime_or_original_save'] is not False:raise ValueError('VM draw fixed private continuation identity')
    return expected['after']

def fresh_identities(phase):
    parent_identities('draw')
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA256 or hashlib.sha256(SCRIPT.read_bytes()).hexdigest()!=SCRIPT_SHA:raise ValueError('VM draw fresh source before unpickle')
    while True:
        if phase not in SHAS or SHAS[phase] is None or hashlib.sha256(REPORTS[phase].read_bytes()).hexdigest()!=SHAS[phase]:raise ValueError('VM draw fresh report SHA before unpickle')
        if phase not in PREVIOUS:break
        phase=PREVIOUS[phase]

def envelope(r,phase):
    if r['phase']!=phase or r['source_contract']!=source_contract() or r['parent_report']!=PARENT.relative_to(ROOT).as_posix() or r['parent_sha256']!=PARENT_SHA or len(r['cases'])!=3 or {c['name'] for c in r['cases']}!={'initial','student9_waiting','fifth_class'} or r['VM_returned']!=(phase!='cleanup') or r['selected_task_returned']!=(phase=='task') or any(r.get(k) is not False for k in ('GPU_executed','full_outer_frame_executed','persistent_write_authority')):raise ValueError('VM draw source/parent/scope envelope')

def load_verified_checkpoint(name,phase):
    fresh_identities(phase);r=pinned(REPORTS[phase],SHAS[phase]);envelope(r,phase);c=next((c for c in r['cases'] if c['name']==name),None)
    if c is None:raise ValueError('VM draw known private case')
    after=verify_case(c,phase);cp=c['continuation_checkpoint'];raw=(ROOT/cp['path']).read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('VM draw file SHA before unpickle')
    payload=pickle.loads(raw);a=unpack(c['actual']);cpu=payload['cpu']
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=name or payload['phase']!=phase or payload['evidence_kind']!='private_original_vm_draw_'+phase or payload['pending_eip']!=STOP[phase]:raise ValueError('VM draw private source/case identity')
    observed={k:cpu.reg_read(reg) for k,reg in zip(('EIP','ESP','EBP','EAX','ECX'),(UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX,UC_X86_REG_ECX))}
    if observed!=a['CPU']:raise ValueError('VM draw private original CPU')
    for row in after+([] if a['packet'] is None else [a['packet']]):
        if read_memory(payload,row['pointer'],row['bytes']).hex()!=row['hex']:raise ValueError('VM draw full private owned/packet memory')
    if read_memory(payload,BASE_SP-4,8)!=struct.pack('<II',BASE_SP-4,RETURN):raise ValueError('VM draw private retained task return stack')
    if phase=='cleanup':
        for at,wanted in ((layout()['vm'],struct.pack('<I',0x454D90)),(layout()['vm']-4,struct.pack('<I',BASE_SP-4)),(layout()['vm']-8,struct.pack('<I',VM)),(layout()['vm']-20,struct.pack('<I',1))):
            if read_memory(payload,at,len(wanted))!=wanted:raise ValueError('VM draw private retained VM caller/locals')
    for row in a['retained_ranges']:
        if hashlib.sha256(read_memory(payload,row['pointer'],row['bytes'])).hexdigest()!=row['sha256']:raise ValueError('VM draw all private retained bytes')
    return payload,cp
