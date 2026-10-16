"""Independent original-call ABI, per-invocation state and immutable checkpoint proof."""
import hashlib,pickle,struct
from functools import lru_cache
from tools.school_vm_flow import *
from tools.school_vm_draw_verification import load_verified_checkpoint as load_parent,fresh_identities as parent_identities,REPORTS as PARENT_REPORTS,SHAS as PARENT_SHAS,read_memory,retained,pinned
from tools.school_world_life_codec import unpack
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX,UC_X86_REG_ECX

PARENT=PARENT_REPORTS['task'];PARENT_SHA=PARENT_SHAS['task']
REPORTS={p:ROOT/f'analysis/school-vm-flow-{p}-v1-20261017.json.gz' for p in PHASES};SHAS={p:None for p in PHASES}
SHAS['slots']='2ba99d49c37f47db6d31fa948bc422acc3d4f5d15c2ea4e48e2d35102847bab4'
SHAS['globals']='2128fee0a928909b300be867629a95d39a5c4dfc8a6806f6c6368ef3b789e5d6'
SHAS['assign']='6ee1db97f5140946a99d640e34acfd96a9127aa0ac670cb1321df37817ea8a29'
SHAS['branch']='65931374d72147e61ab8da05168f46e06ffcea37675bd155c2792fbf1546993f'

@lru_cache(maxsize=3)
def seed(name):
    payload,cp=load_parent(name,'task');before=[dict(pointer=a,bytes=n,hex=read_memory(payload,a,n).hex()) for a,n in REGIONS];p=int.from_bytes(read_memory(payload,TACT+0x64,4),'little');tex=int.from_bytes(read_memory(payload,BANK,4),'little');inputs=dict(script_pointer=p,script_sha256=SCRIPT_SHA,driver='explicit_original_reset_and_selected_task_calls_after_verified_return',texture_record=dict(pointer=tex,bytes=84,hex=read_memory(payload,tex,84).hex()),ime_target=int.from_bytes(read_memory(payload,0x5920EC,4),'little'),strlen_target=int.from_bytes(read_memory(payload,0x5922C4,4),'little'));exclusions=[(STACK,STACK+65536)]+[(a,a+n) for a,n in REGIONS];ranges=[]
    for start,buf in payload['memory']:
        pieces=[(start,start+len(buf))]
        for left,right in exclusions:pieces=[p for a,b in pieces for p in ((a,min(b,left)),(max(a,right),b)) if p[0]<p[1]]
        ranges.extend(dict(pointer=a,bytes=b-a,sha256=hashlib.sha256(buf[a-start:b-start]).hexdigest()) for a,b in pieces)
    return cp,before,inputs,ranges

@lru_cache(maxsize=21)
def checked(name,phase):
    c=next(c for c in pinned(REPORTS[phase],SHAS[phase])['cases'] if c['name']==name);return c,verify_case(c,phase)

def verify_calls(step,inputs,before):
    wanted=call_protocol(step['kind'],inputs,before,step['fade_completed']);calls=step['calls'];rules={int(r['va'],16):r for r in source_contract()['functions']};raw=SOURCE.read_bytes();active=[]
    if len(calls)!=len(wanted):raise ValueError('VM flow exact native call count')
    for c,(va,ret,receiver,args) in zip(calls,wanted):
        if (c['va'],c['return_va'],c['args'])!=(hex(va),hex(ret),args) or (receiver is not None and c['receiver']!=receiver) or type(c['receiver']) is not int:raise ValueError('VM flow complete source call/receiver/arguments')
        if ret==RETURN:active=[];expected_sp=BASE_SP
        else:
            op=raw[ret-BASE-5:ret-BASE]
            if op[0]!=0xE8 or ret+struct.unpack_from('<i',op,1)[0]!=va:raise ValueError('VM flow original E8 call bytes')
            owner=next((a for a,r in rules.items() if a<=ret-5<int(r['end'],16)),None)
            while active and active[-1][0]!=owner:active.pop()
            if not active:raise ValueError('VM flow actual source ABI owner')
            expected_sp=active[-1][1]-rules[owner]['frame']-len(args)*4-4
        if c['sp']!=expected_sp or len(args)!=rules[va]['args']:raise ValueError('VM flow complete original ABI stack')
        active.append((va,c['sp']))
    # The only platform responses are the inherited null-context IME response and
    # reading the captured empty string; the native thunk/IAT callsites remain real.
    thunk=next(c for c in calls if c['va']=='0x56cd4a');length=next(c for c in calls if c['va']=='0x425a50');length_sp=length['sp']-rules[0x425A50]['frame']-8
    adapters=[dict(name='ImmGetOpenStatus',slot='0x5920ec',va=hex(inputs['ime_target']),return_va='0x425c99',sp=thunk['sp'],args=[0],result=0,declared_response=True,live_OS_observed=False),dict(name='lstrlenA',slot='0x5922c4',va=hex(inputs['strlen_target']),return_va='0x425a7e',sp=length_sp,args=[INPUT+0x528],result=0,read_hex='00',reads_existing_buffer_only=True)]
    if step['adapters']!=adapters or raw[0x425A78-BASE:0x425A7E-BASE]!=bytes.fromhex('ff15c4225900') or raw[0x56CD4A-BASE:0x56CD50-BASE]!=bytes.fromhex('ff25ec205900'):raise ValueError('VM flow bounded inherited platform/callsite proof')
    returns=[];v=data(before)[VM]
    for c in calls:
        va=int(c['va'],16);eax=ecx=None
        if va==0x425DE0:eax=0;ecx=INPUT
        elif va==0x4C1EB0:
            typ,index=c['args'][1:];eax=typed((typ<<28)|index,v);ecx=VM+4 if typ==0 else typ
        elif va==0x4C2060:eax=1;ecx=1
        elif va==0x56CFCC:eax=648;ecx=WORK
        elif va==0x407AD0:eax=1;ecx=layout()['packet']
        elif va==0x4CE8F0:eax=1;ecx=0
        elif va==0x454CF0:eax=0;ecx=0
        if eax is not None:returns.append(dict(va=rules[va]['ret'],return_va=c['return_va'],sp=c['sp'],eax=eax,ecx=ecx))
    # Function entries precede nested returns: the enclosing VM/task return events
    # occur after all typed helpers and the drawing body.
    roots=[r for r in returns if r['va'] in ('0x4d03b6','0x454ec1')];returns=[r for r in returns if r not in roots]+sorted(roots,key=lambda r:0 if r['va']=='0x4d03b6' else 1)
    if step['returns']!=returns:raise ValueError('VM flow original typed/draw/VM/task return instructions/values')
    return calls

def verify_step(step,index,kind,inputs,before):
    expected=project_step(kind,inputs,before)
    if step['index']!=index or any(step[k]!=v for k,v in expected.items()):raise ValueError('VM flow full independent intermediate state/packet/CPU')
    calls=verify_calls(step,inputs,before);prior=expected['CPU'];reset=expected['reset_CPU']
    declarations=[dict(entry='0x425de0',receiver=INPUT,return_va=hex(RETURN),sp=BASE_SP,previous_CPU=prior,driver_declared=True,original_outer_callsite_observed=False),dict(entry='0x454cf0',receiver=TACT,return_va=hex(RETURN),sp=BASE_SP,previous_CPU=reset,driver_declared=True,original_outer_callsite_observed=False)]
    if step['declarations']!=declarations or step['owned_bodies_stubbed'] is not False or step['debug_stack_check_adapter'] is not True:raise ValueError('VM flow explicit driver/whole bodies/debug scope')
    required={int(c['va'],16) for c in calls}|{0x407B17,0x408124,0x4D2DB3,0x4CD54B,0x4D03B6,0x454DA0,0x454EC1};forbidden={0x424F80,0x407B21,0x4C7190,0x40378A,0x4037BB,0x41FA7F,0x41FAA8}
    if kind=='wait':
        required.add(0x4CFF20);forbidden.add(0x4CE9C5)
        if not data(before)[VM][0x92E0]:required.add(0x4CFF41)
        else:forbidden.add(0x4CFF41)
    elif kind=='branch':required|={0x4C20A4,0x4C24B6,0x4C24CF}
    elif kind=='assign':required.add(0x4C1F89)
    elif kind=='bit':required.add(0x4E2BBC)
    elif kind=='word':required.add(0x4E2B04)
    elif kind.startswith('hide'):required.add(0x497290)
    elif kind.startswith('pose'):required|={0x49962E,0x497331,0x4977B8}
    elif kind=='fade':required|={0x49790B,0x497955,0x56CFE5,0x497969}
    if kind=='fade' or data(before)[WORK+0x2490][9]:
        required|={0x497B4D,0x497BB7}
        if step['fade_completed']:required|={0x497BD1,0x497C0A,0x4977B8}
        else:required.add(0x497C22)
    else:required.add(0x497C2D)
    if not required<=set(step['visited']) or forbidden&set(step['visited']):raise ValueError('VM flow original state branches and native bodies')
    return expected['after']

def verify_case(c,phase):
    if phase not in PHASES or c['name'] not in ('initial','student9_waiting','fifth_class'):raise ValueError('VM flow known phase/case')
    cp,before,inputs,ranges=seed(c['name'])
    if phase in PREVIOUS:
        parent,before=checked(c['name'],PREVIOUS[phase]);cp=parent['continuation_checkpoint']
    a=unpack(c['actual'])
    if c['prior_checkpoint']!=cp or a['phase']!=phase or a['inputs']!=inputs or a['before']!=before or len(a['steps'])!=len(KINDS[phase]) or a['declared_task_calls']!=len(KINDS[phase]) or a['declared_reset_calls']!=len(KINDS[phase]):raise ValueError('VM flow actual case/provenance/complete step count')
    current=before
    for index,(step,kind) in enumerate(zip(a['steps'],KINDS[phase])):current=verify_step(step,index,kind,inputs,current)
    if a['after']!=current or any(a.get(k) is not False for k in ('live_OS_observed','GPU_executed','full_outer_frame_executed','persistent_write_authority')):raise ValueError('VM flow complete final state/scope')
    retained(a)
    if a['retained_ranges']!=ranges or a['retained_bytes']!=sum(r['bytes'] for r in ranges):raise ValueError('VM flow all parent retained bytes')
    cp=c['continuation_checkpoint']
    if cp['path']!=f'.venv-audit/vm-flow-{phase}-{c["name"]}.pkl' or cp['pending_eip']!=hex(RETURN) or cp['runtime_or_original_save'] is not False:raise ValueError('VM flow fixed private checkpoint identity')
    return current

def fresh_identities(phase):
    parent_identities('task')
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA256 or hashlib.sha256(SCRIPT.read_bytes()).hexdigest()!=SCRIPT_SHA:raise ValueError('VM flow fresh source before unpickle')
    while True:
        if phase not in SHAS or SHAS[phase] is None or hashlib.sha256(REPORTS[phase].read_bytes()).hexdigest()!=SHAS[phase]:raise ValueError('VM flow fresh current/ancestor report SHA before unpickle')
        if phase not in PREVIOUS:break
        phase=PREVIOUS[phase]

def envelope(r,phase):
    if r['phase']!=phase or r['source_contract']!=source_contract() or r['parent_report']!=PARENT.relative_to(ROOT).as_posix() or r['parent_sha256']!=PARENT_SHA or len(r['cases'])!=3 or {c['name'] for c in r['cases']}!={'initial','student9_waiting','fifth_class'} or any(r.get(k) is not False for k in ('live_OS_observed','GPU_executed','full_outer_frame_executed','persistent_write_authority')):raise ValueError('VM flow source/parent/scope envelope')

def verify_payload(payload,c,phase,after):
    a=unpack(c['actual']);cpu=payload['cpu']
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=c['name'] or payload['phase']!=phase or payload['evidence_kind']!='private_original_vm_flow_'+phase or payload['pending_eip']!=RETURN:raise ValueError('VM flow private source/case identity')
    observed={k:cpu.reg_read(reg) for k,reg in zip(('EIP','ESP','EBP','EAX','ECX'),(UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX,UC_X86_REG_ECX))}
    if observed!=a['steps'][-1]['CPU']:raise ValueError('VM flow private actual CPU')
    for row in after+[a['steps'][-1]['packet']]:
        if read_memory(payload,row['pointer'],row['bytes']).hex()!=row['hex']:raise ValueError('VM flow full private owned/packet memory')
    if read_memory(payload,BASE_SP-4,8)!=struct.pack('<II',BASE_SP-4,RETURN):raise ValueError('VM flow private original declared return stack')
    for row in a['retained_ranges']:
        if hashlib.sha256(read_memory(payload,row['pointer'],row['bytes'])).hexdigest()!=row['sha256']:raise ValueError('VM flow all private retained bytes')

def load_verified_checkpoint(name,phase):
    fresh_identities(phase);r=pinned(REPORTS[phase],SHAS[phase]);envelope(r,phase);c=next((c for c in r['cases'] if c['name']==name),None)
    if c is None:raise ValueError('VM flow known private case')
    after=verify_case(c,phase);cp=c['continuation_checkpoint'];raw=(ROOT/cp['path']).read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('VM flow file SHA before unpickle')
    payload=pickle.loads(raw);verify_payload(payload,c,phase,after);return payload,cp
