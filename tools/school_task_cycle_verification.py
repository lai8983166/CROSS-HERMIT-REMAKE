"""Source/ABI/whole-memory verification of the bounded captured input cycle."""
import gzip,hashlib,json,pickle,struct
from functools import lru_cache
from tools.school_world_life_codec import unpack
from tools.school_task_cycle import *
from tools.school_world_script_verification import load_verified_checkpoint as load_parent,fresh_identities as parent_identities,REPORTS as PARENT_REPORTS,SHAS as PARENT_SHAS,read_memory,retained,abi as parent_abi,pinned
from tools.school_world_script_emulation import STACK,RETURN
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX,UC_X86_REG_ECX

PARENT=PARENT_REPORTS['task'];PARENT_SHA=PARENT_SHAS['task']
REPORTS={p:ROOT/f'analysis/school-task-cycle-{p}-v1-20261016.json.gz' for p in PHASES}
SHAS={p:None for p in PHASES}
SHAS['reset1']='0db812cb28e404705f4227f6dd151b70fe5cef617ffff12e0c00ebcf26262ec2'

@lru_cache(maxsize=3)
def seed(name):
    payload,cp=load_parent(name,'task');before=[dict(pointer=a,bytes=n,hex=read_memory(payload,a,n).hex()) for a,n in REGIONS]
    imports=dict(ime_target=int.from_bytes(read_memory(payload,0x5920EC,4),'little'),strlen_target=int.from_bytes(read_memory(payload,0x5922C4,4),'little'))
    target=imports['ime_target'];page=None if any(a<=target<a+len(b) for a,b in payload['memory']) else dict(pointer=target&~4095,bytes=4096,hex=bytes(4096).hex())
    exclusions=[(STACK,STACK+65536),(0,4)]+[(a,a+n) for a,n in REGIONS];ranges=[]
    memory=payload['memory']+([] if page is None else [(page['pointer'],bytes(page['bytes']))])
    for start,buf in sorted(memory):
        pieces=[(start,start+len(buf))]
        for left,right in exclusions:pieces=[p for a,b in pieces for p in ((a,min(b,left)),(max(a,right),b)) if p[0]<p[1]]
        ranges.extend(dict(pointer=a,bytes=b-a,sha256=hashlib.sha256(buf[a-start:b-start]).hexdigest()) for a,b in pieces)
    return cp,before,imports,page,ranges

@lru_cache(maxsize=12)
def checked(name,phase):
    c=next(c for c in pinned(REPORTS[phase],SHAS[phase])['cases'] if c['name']==name);return c,verify_case(c,phase)

@lru_cache(maxsize=1)
def abi():
    out=dict(parent_abi());raw=SOURCE.read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_32)
    for va,end in RESET_NATIVE[:3]:
        seq=list(md.disasm(raw[va-BASE:end-BASE],va));ret=seq[-1];local=next(i for i in seq[:12] if i.mnemonic=='sub' and i.op_str.startswith('esp, '))
        if ret.mnemonic!='ret':raise ValueError('task cycle original ABI return')
        out[va]=dict(end=end,frame=4+int(local.op_str.split(', ')[1],0)+12,args=int(ret.op_str,0)//4 if ret.op_str else 0)
    out[0x56CD4A]=dict(end=0x56CD50,frame=0,args=1)
    return out


def verify_calls(a,phase):
    calls=a['calls'];raw=SOURCE.read_bytes();rules=abi();active=[];base=STACK+0xFF00
    if [int(c['return_va'],16) for c in calls]!=call_protocol(phase):raise ValueError('task cycle exact original call order')
    if calls[0]['va']!=('0x425de0' if phase.startswith('reset') else '0x454cf0'):raise ValueError('task cycle declared root identity')
    for index,c in enumerate(calls):
        va=int(c['va'],16);ret=int(c['return_va'],16);op=raw[ret-BASE-5:ret-BASE]
        if va not in rules or index and (op[0]!=0xE8 or ret+struct.unpack_from('<i',op,1)[0]!=va):raise ValueError('task cycle original E8 call bytes')
        if not index:wanted=base
        else:
            owner=next((p for p,r in rules.items() if p<=ret-5<r['end']),None)
            while active and active[-1][0]!=owner:active.pop()
            if not active:raise ValueError('task cycle original ABI owner')
            wanted=active[-1][1]-rules[owner]['frame']-rules[va]['args']*4-4
        if c['sp']!=wanted or type(c['receiver']) is not int:raise ValueError('task cycle original ABI stack/receiver')
        task={0x454CF0,0x454C40,0x457830};inputs={0x425DE0,0x425E60,0x425C70,0x425ED0,0x425A10,0x425A50,0x426250,0x426110,0x426190}
        if va in task and c['receiver']!=TACT or va in inputs and c['receiver']!=INPUT or va==0x4CE8F0 and c['receiver']!=VM or va==0x56CD4A and c['receiver']!=0:raise ValueError('task cycle typed native receiver')
        active.append((va,c['sp']))


def verify_case(c,phase):
    if phase not in PHASES or c['name'] not in ('initial','student9_waiting','fifth_class'):raise ValueError('task cycle known case/phase')
    cp,before,imports,page,ranges=seed(c['name'])
    if phase in PREVIOUS:
        parent,before=checked(c['name'],PREVIOUS[phase]);cp=parent['continuation_checkpoint'];page=None
    if c['prior_checkpoint']!=cp:raise ValueError('task cycle parent checkpoint provenance')
    a=unpack(c['actual']);expected=project(phase,before);base=STACK+0xFF00
    if a['phase']!=phase or a['before']!=before or a['imports']!=imports or a['adapter_page_added']!=page or any(a[k]!=v for k,v in expected.items()):raise ValueError('task cycle full independent state and imports')
    if a['retained_ranges']!=ranges or a['retained_bytes']!=sum(r['bytes'] for r in ranges):raise ValueError('task cycle exact original parent retained coverage')
    verify_calls(a,phase)
    reset=phase.startswith('reset');entry=next(x for x in a['calls'] if x['va']==('0x56cd4a' if reset else '0x425a50'))
    adapter=dict(name='ImmGetOpenStatus',slot='0x5920ec',va=hex(imports['ime_target']),return_va='0x425c99',sp=entry['sp'],args=[0],result=0,declared_response=True,live_OS_observed=False) if reset else dict(name='lstrlenA',slot='0x5922c4',va=hex(imports['strlen_target']),return_va='0x425a7e',sp=entry['sp']-abi()[0x425A50]['frame']-8,args=[INPUT+0x528],result=0,read_hex='00',reads_existing_buffer_only=True)
    if a['adapters']!=[adapter]:raise ValueError('task cycle exact declared platform adapter')
    want_cpu=dict(EIP=0x4CE8F0 if phase=='vm_entry' else RETURN,ESP=base-100 if phase=='vm_entry' else base+4,EBP=base-4,EAX=2 if phase=='vm_entry' else 0,ECX=VM if phase=='vm_entry' else INPUT if reset else 0)
    ret=None if phase=='vm_entry' else dict(va='0x425e59' if reset else '0x454ec1',return_va=hex(RETURN),sp=base,eax=0)
    pending=dict(va='0x4ce8f0',sp=base-100,ebp=base-4,eax=2,ecx=VM,first_instruction_executed=False) if phase=='vm_entry' else None
    if a['CPU']!=want_cpu or a['real_ret']!=ret or a['pending']!=pending:raise ValueError('task cycle exact original return or pending VM CPU')
    required=({0x425DE0,0x425E2F,0x425E34,0x425E3F,0x425E60,0x425EA5,0x425EB8,0x425C70,0x56CD4A} if reset else {int(x['va'],16) for x in a['calls'] if x['va']!='0x4ce8f0'}|{0x425F34,0x425A78})
    forbidden={0x425CC0,0x425E25,0x424F80,0x4CE8F0} if reset else {0x424F80,0x4CE8F0,0x454D51}
    if phase=='phase2':required|={0x454D6C,0x454D76,0x497C2D,0x498725}
    if phase=='vm_entry':required|={0x454D7D,0x454D8B};forbidden|={0x454EA5,0x454D6C}
    if not required<=set(a['visited']) or forbidden&set(a['visited']):raise ValueError('task cycle source-selected native branches')
    if any(a.get(k) is not False for k in ('owned_bodies_stubbed','original_outer_task_frame_completed')):raise ValueError('task cycle bounded authority')
    retained(a);cp=c['continuation_checkpoint']
    if cp['path']!=f'.venv-audit/task-cycle-{phase}-{c["name"]}.pkl' or cp['pending_eip']!=hex(want_cpu['EIP']) or cp['runtime_or_original_save'] is not False:raise ValueError('task cycle fixed new checkpoint path')
    return expected['after']


def fresh_identities(phase):
    parent_identities('task')
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA256:raise ValueError('task cycle fresh original source')
    while True:
        if phase not in SHAS or SHAS[phase] is None or hashlib.sha256(REPORTS[phase].read_bytes()).hexdigest()!=SHAS[phase]:raise ValueError('task cycle fresh report SHA before unpickle')
        if phase not in PREVIOUS:break
        phase=PREVIOUS[phase]


def load_verified_checkpoint(name,phase):
    fresh_identities(phase);report=pinned(REPORTS[phase],SHAS[phase])
    if report['phase']!=phase or report['source_contract']!=source_contract() or report['parent_report']!=PARENT.relative_to(ROOT).as_posix() or report['parent_sha256']!=PARENT_SHA or len(report['cases'])!=3 or {x['name'] for x in report['cases']}!={'initial','student9_waiting','fifth_class'}:raise ValueError('task cycle exact source/parent envelope')
    if any(report.get(k) is not False for k in ('normal_VM_executed','live_input_sampled','full_outer_frame_executed','persistent_write_authority')):raise ValueError('task cycle report authority')
    c=next((c for c in report['cases'] if c['name']==name),None)
    if c is None:raise ValueError('task cycle known checkpoint case')
    after=verify_case(c,phase);cp=c['continuation_checkpoint'];raw=(ROOT/cp['path']).read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('task cycle checkpoint file SHA before unpickle')
    payload=pickle.loads(raw);cpu=payload['cpu'];a=unpack(c['actual'])
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=name or payload['phase']!=phase or payload['evidence_kind']!='private_original_task_cycle_'+phase or payload['pending_eip']!=a['CPU']['EIP']:raise ValueError('task cycle private checkpoint identity')
    observed={k:cpu.reg_read(reg) for k,reg in zip(('EIP','ESP','EBP','EAX','ECX'),(UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX,UC_X86_REG_ECX))}
    if observed!=a['CPU']:raise ValueError('task cycle exact private CPU')
    for r in after:
        if read_memory(payload,r['pointer'],r['bytes']).hex()!=r['hex']:raise ValueError('task cycle all private owned bytes')
    for r in a['retained_ranges']:
        if hashlib.sha256(read_memory(payload,r['pointer'],r['bytes'])).hexdigest()!=r['sha256']:raise ValueError('task cycle all private retained bytes')
    return payload,cp
