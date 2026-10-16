"""Independent whole-state/source ABI proof for the native normal VM display prefix."""
import gzip,hashlib,json,pickle,struct
from functools import lru_cache
from tools.school_vm_present import *
from tools.school_world_life_codec import unpack
from tools.school_task_cycle_verification import load_verified_checkpoint as load_parent,fresh_identities as parent_identities,REPORTS as PARENT_REPORTS,SHAS as PARENT_SHAS,read_memory,retained,pinned
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX,UC_X86_REG_ECX

PARENT=PARENT_REPORTS['vm_entry'];PARENT_SHA=PARENT_SHAS['vm_entry']
REPORTS={p:ROOT/f'analysis/school-vm-present-{p}-v1-20261016.json.gz' for p in PHASES};SHAS={p:None for p in PHASES}
SHAS['packet']='a19eb46aa8213c52385512cdb9b45aaf59e66445ad4bb699c6a1d9f6416fed83'
SHAS['command']='11c14cf25a955cd860582b0e171fc4f8c251df730255580bc3d4108ee0da4923'

@lru_cache(maxsize=3)
def seed(name):
    payload,cp=load_parent(name,'vm_entry');before=[dict(pointer=a,bytes=n,hex=read_memory(payload,a,n).hex()) for a,n in REGIONS];p=int.from_bytes(read_memory(payload,TACT+0x64,4),'little');inputs=dict(script_pointer=p,script_sha256=SCRIPT_SHA,driver='continuous_original_task_VM',texture_record=dict(pointer=int.from_bytes(read_memory(payload,BANK,4),'little'),bytes=84,hex=read_memory(payload,int.from_bytes(read_memory(payload,BANK,4),'little'),84).hex()));exclusions=[(STACK,STACK+65536)]+[(a,a+n) for a,n in REGIONS];ranges=[]
    for start,buf in payload['memory']:
        pieces=[(start,start+len(buf))]
        for left,right in exclusions:pieces=[p for a,b in pieces for p in ((a,min(b,left)),(max(a,right),b)) if p[0]<p[1]]
        ranges.extend(dict(pointer=a,bytes=b-a,sha256=hashlib.sha256(buf[a-start:b-start]).hexdigest()) for a,b in pieces)
    return cp,before,inputs,ranges

@lru_cache(maxsize=9)
def checked(name,phase):
    c=next(c for c in pinned(REPORTS[phase],SHAS[phase])['cases'] if c['name']==name);return c,verify_case(c,phase)


def verify_calls(a,phase):
    calls=a['calls'];raw=SOURCE.read_bytes();rules={int(r['va'],16):r for r in source_contract()['functions']};rules[0x407AD0]=dict(frame=0,args=2,end=hex(0x407AD0));l=layout();active=[]
    if [int(c['return_va'],16) for c in calls]!=call_protocol(phase):raise ValueError('VM present exact source call protocol')
    roots={'command':0x4CE8F0,'packet':0x4D29E0,'draw':0x407870};sp=l[{'command':'vm','packet':'overlay','draw':'resource'}[phase]]
    if int(calls[0]['va'],16)!=roots[phase]:raise ValueError('VM present natural root identity')
    for index,c in enumerate(calls):
        va=int(c['va'],16);ret=int(c['return_va'],16);op=raw[ret-BASE-5:ret-BASE]
        if va not in rules or op[0]!=0xE8 or ret+struct.unpack_from('<i',op,1)[0]!=va:raise ValueError('VM present original E8 call bytes')
        if not index:wanted=sp
        else:
            owner=next((p for p,r in rules.items() if p<=ret-5<int(r['end'],16)),None)
            while active and active[-1][0]!=owner:active.pop()
            if not active:raise ValueError('VM present source ABI owner')
            wanted=active[-1][1]-rules[owner]['frame']-rules[va]['args']*4-4
        if c['sp']!=wanted or type(c['receiver']) is not int or len(c['args'])!=rules[va]['args']:raise ValueError('VM present original ABI stack/args')
        active.append((va,c['sp']))


def verify_case(c,phase):
    if phase not in PHASES or c['name'] not in ('initial','student9_waiting','fifth_class'):raise ValueError('VM present known phase/case')
    cp,before,inputs,ranges=seed(c['name']);root_args=project('command',inputs,before)['pending']['args']
    if phase in PREVIOUS:
        parent,before=checked(c['name'],PREVIOUS[phase]);cp=parent['continuation_checkpoint']
    a=unpack(c['actual']);expected=project(phase,inputs,before);l=layout();p=l['packet']
    if c['prior_checkpoint']!=cp or a['phase']!=phase or a['inputs']!=inputs or a['before']!=before or any(a[k]!=v for k,v in expected.items()):raise ValueError('VM present full independent state/provenance/packet')
    verify_calls(a,phase)
    calls=a['calls'];wanted={'command':[(VM,[]),(VM,[0,inputs['script_pointer']+452,0]),(VM,[]),(VM,[0,0,0,1]),(OVERLAY,root_args)],'packet':[(OVERLAY,root_args),(OVERLAY,[20,51,0,0,0,424,24,20,30]),(p,[]),(p,[]),(p,[]),(p,[]),(p,[p+0x24,0,4]),(p+0x50,[]),(p,[TASK]),(p,[20,0])],'draw':[(p,[20,0]),(TASK+0x844,[20,0]),(TASK,[]),(p,[0,0]),(p,[0,0]),(p,[0,0])]}[phase]
    if [(x['receiver'],x['args']) for x in calls]!=wanted:raise ValueError('VM present exact original arguments and receivers')
    returns=[]
    if phase=='command':returns=[dict(va='0x496de6',return_va='0x42fc88',sp=calls[2]['sp'],eax=1)]
    if phase=='draw':returns=[dict(va='0x41f667',return_va='0x407904',sp=calls[1]['sp'],eax=inputs['texture_record']['pointer']),dict(va='0x4142dc',return_va='0x4079a5',sp=calls[2]['sp'],eax=int.from_bytes(bytes.fromhex(next(r['hex'] for r in before if r['pointer']==TASK+0xB210)),'little'))]
    commands=[dict(offset=452,opcode=167,advance=8)] if phase=='command' else []
    seh=None if phase=='command' else struct.pack('<III',0,0x59081C,0).hex();packet_before=dict(pointer=p,bytes=128,hex=packet_project()) if phase=='draw' else None
    pending=expected['pending'];cpu=dict(EIP=int(pending['va'],16),ESP=pending['sp'],EBP=pending['ebp'],EAX=pending['eax'],ECX=pending['receiver'])
    if a['returns']!=returns or a['commands']!=commands or a['seh_record']!=seh or a['packet_before']!=packet_before or a['CPU']!=cpu:raise ValueError('VM present original returns/commands/SEH/private CPU')
    required={int(x['va'],16) for x in calls[:-1]};forbidden={int(pending['va'],16),0x424F80}
    if phase=='command':required|={0x4CE9C5,0x4CFE35,0x4C1F89,0x4CFEF2,0x4D024A}
    elif phase=='packet':required|={0x4D2A45,0x4D2D36,0x4D2D52};forbidden.add(0x4D2BA0)
    else:required|={0x41F5E0,0x41F624,0x41F654,0x407947,0x4D2D57,0x407A80};forbidden|={0x41F5DC,0x407A99}
    if not required<=set(a['visited']) or forbidden&set(a['visited']):raise ValueError('VM present source native branches and unexecuted boundary')
    if a['platform_adapters']!=[] or a['debug_stack_check_adapter'] is not True or any(a.get(k) is not False for k in ('owned_bodies_stubbed','original_outer_task_frame_completed')):raise ValueError('VM present no body stubs or fabricated completion')
    retained(a)
    if a['retained_ranges']!=ranges or a['retained_bytes']!=sum(r['bytes'] for r in ranges):raise ValueError('VM present exact parent retained coverage')
    cp=c['continuation_checkpoint']
    if cp['path']!=f'.venv-audit/vm-present-{phase}-{c["name"]}.pkl' or cp['pending_eip']!=pending['va'] or cp['runtime_or_original_save'] is not False:raise ValueError('VM present fixed immutable private checkpoint')
    return expected['after']


def fresh_identities(phase):
    parent_identities('vm_entry')
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA256 or hashlib.sha256(SCRIPT.read_bytes()).hexdigest()!=SCRIPT_SHA:raise ValueError('VM present fresh source before unpickle')
    while True:
        if phase not in SHAS or SHAS[phase] is None or hashlib.sha256(REPORTS[phase].read_bytes()).hexdigest()!=SHAS[phase]:raise ValueError('VM present fresh report SHA before unpickle')
        if phase not in PREVIOUS:break
        phase=PREVIOUS[phase]


def load_verified_checkpoint(name,phase):
    fresh_identities(phase);r=pinned(REPORTS[phase],SHAS[phase])
    if r['phase']!=phase or r['source_contract']!=source_contract() or r['parent_report']!=PARENT.relative_to(ROOT).as_posix() or r['parent_sha256']!=PARENT_SHA or len(r['cases'])!=3 or {c['name'] for c in r['cases']}!={'initial','student9_waiting','fifth_class'} or r['normal_first_opcode_executed'] is not True or any(r.get(k) is not False for k in ('VM_returned','full_outer_frame_executed','live_rendering','persistent_write_authority')):raise ValueError('VM present source/parent/scope envelope')
    c=next((c for c in r['cases'] if c['name']==name),None)
    if c is None:raise ValueError('VM present known private case')
    after=verify_case(c,phase);cp=c['continuation_checkpoint'];raw=(ROOT/cp['path']).read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('VM present file SHA before unpickle')
    payload=pickle.loads(raw);a=unpack(c['actual']);cpu=payload['cpu']
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=name or payload['phase']!=phase or payload['evidence_kind']!='private_original_vm_present_'+phase or payload['pending_eip']!=a['CPU']['EIP']:raise ValueError('VM present private identity')
    observed={k:cpu.reg_read(reg) for k,reg in zip(('EIP','ESP','EBP','EAX','ECX'),(UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX,UC_X86_REG_ECX))}
    if observed!=a['CPU']:raise ValueError('VM present private original CPU')
    for row in after+([] if a['packet'] is None else [a['packet']]):
        if read_memory(payload,row['pointer'],row['bytes']).hex()!=row['hex']:raise ValueError('VM present full private owned/packet memory')
    if phase!='command' and read_memory(payload,layout()['seh'],12).hex()!=a['seh_record']:raise ValueError('VM present private SEH chain')
    p=a['pending'];wanted=struct.pack('<'+'I'*(len(p['args'])+1),int(p['return_va'],16),*p['args'])
    if read_memory(payload,p['sp'],len(wanted))!=wanted:raise ValueError('VM present private natural caller/arguments')
    for row in a['retained_ranges']:
        if hashlib.sha256(read_memory(payload,row['pointer'],row['bytes'])).hexdigest()!=row['sha256']:raise ValueError('VM present all private retained bytes')
    return payload,cp
