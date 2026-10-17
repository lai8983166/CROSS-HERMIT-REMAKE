"""Independent original-call ABI, per-invocation state and immutable checkpoint proof."""
import hashlib,pickle,struct
from functools import lru_cache
from tools.school_vm_panel import *
from tools.school_vm_flow_verification import load_verified_checkpoint as load_parent,fresh_identities as parent_identities,REPORTS as PARENT_REPORTS,SHAS as PARENT_SHAS,read_memory,retained,pinned
from tools.school_world_life_codec import unpack
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX,UC_X86_REG_ECX

PARENT=PARENT_REPORTS['fade_finish'];PARENT_SHA=PARENT_SHAS['fade_finish']
REPORTS={p:ROOT/f'analysis/school-vm-panel-{p}-v1-20261017.json.gz' for p in PHASES};SHAS={p:None for p in PHASES}
SHAS['release']='b4f49ab5db44b93e06d3173792254ab6d1496ba7320fd806c464030230536684'
SHAS['display']='b334cf13f49b09d8507d5a98b4c7a45da6f1bcad3497dbab3460ca21ac3fcfdc'

@lru_cache(maxsize=3)
def seed(name):
    payload,cp=load_parent(name,'fade_finish');before=[dict(pointer=a,bytes=n,hex=read_memory(payload,a,n).hex()) for a,n in REGIONS];p=int.from_bytes(read_memory(payload,TACT+0x64,4),'little');tex=int.from_bytes(read_memory(payload,BANK,4),'little');inputs=dict(script_pointer=p,script_sha256=SCRIPT_SHA,driver='explicit_original_reset_and_selected_task_calls_after_verified_return',texture_record=dict(pointer=tex,bytes=84,hex=read_memory(payload,tex,84).hex()),ime_target=int.from_bytes(read_memory(payload,0x5920EC,4),'little'),strlen_target=int.from_bytes(read_memory(payload,0x5922C4,4),'little'));exclusions=[(STACK,STACK+65536)]+[(a,a+n) for a,n in REGIONS];ranges=[]
    for start,buf in payload['memory']:
        pieces=[(start,start+len(buf))]
        for left,right in exclusions:pieces=[p for a,b in pieces for p in ((a,min(b,left)),(max(a,right),b)) if p[0]<p[1]]
        ranges.extend(dict(pointer=a,bytes=b-a,sha256=hashlib.sha256(buf[a-start:b-start]).hexdigest()) for a,b in pieces)
    return cp,before,inputs,ranges

@lru_cache(maxsize=21)
def checked(name,phase):
    c=next(c for c in pinned(REPORTS[phase],SHAS[phase])['cases'] if c['name']==name);return c,verify_case(c,phase)

def verify_calls(step,inputs,before):
    wanted=call_protocol(step['kind'],inputs,before);calls=step['calls'];rules={int(r['va'],16):r for r in source_contract()['functions']};raw=SOURCE.read_bytes();active=[]
    if len(calls)!=len(wanted):raise ValueError('VM panel exact native call count')
    for c,(va,ret,receiver,args) in zip(calls,wanted):
        if (c['va'],c['return_va'],c['args'])!=(hex(va),hex(ret),args) or (receiver is not None and c['receiver']!=receiver) or type(c['receiver']) is not int:raise ValueError('VM panel complete source call/receiver/arguments')
        if ret==RETURN:active=[];expected_sp=BASE_SP
        else:
            op=raw[ret-BASE-5:ret-BASE]
            if op[0]!=0xE8 or ret+struct.unpack_from('<i',op,1)[0]!=va:raise ValueError('VM panel original E8 call bytes')
            owner=next((a for a,r in rules.items() if a<=ret-5<int(r['end'],16)),None)
            while active and active[-1][0]!=owner:active.pop()
            if not active:raise ValueError('VM panel actual source ABI owner')
            expected_sp=active[-1][1]-rules[owner]['frame']-len(args)*4-4
        if c['sp']!=expected_sp or len(args)!=rules[va]['args']:raise ValueError('VM panel complete original ABI stack')
        active.append((va,c['sp']))
    # The only platform responses are the inherited null-context IME response and
    # reading the captured empty string; the native thunk/IAT callsites remain real.
    thunk=next(c for c in calls if c['va']=='0x56cd4a');length=next(c for c in calls if c['va']=='0x425a50');length_sp=length['sp']-rules[0x425A50]['frame']-8
    adapters=[dict(name='ImmGetOpenStatus',slot='0x5920ec',va=hex(inputs['ime_target']),return_va='0x425c99',sp=thunk['sp'],args=[0],result=0,declared_response=True,live_OS_observed=False),dict(name='lstrlenA',slot='0x5922c4',va=hex(inputs['strlen_target']),return_va='0x425a7e',sp=length_sp,args=[INPUT+0x528],result=0,read_hex='00',reads_existing_buffer_only=True)]
    if step['adapters']!=adapters or raw[0x425A78-BASE:0x425A7E-BASE]!=bytes.fromhex('ff15c4225900') or raw[0x56CD4A-BASE:0x56CD50-BASE]!=bytes.fromhex('ff25ec205900'):raise ValueError('VM panel bounded inherited platform/callsite proof')
    returns=[];v=data(before)[VM]
    for c in calls:
        va=int(c['va'],16);eax=ecx=None
        if va==0x425DE0:eax=0;ecx=INPUT
        elif va==0x4C1EB0:
            typ,index=c['args'][1:];eax=typed((typ<<28)|index,v);ecx=VM+4 if typ==0 else typ
        elif va in (0x4C76B0,0x4C7AB0):eax=(PANEL&0xFFFFFF00)|1;ecx=0
        elif va==0x4C1E20:eax=1;ecx=0
        elif va==0x4CCB90:eax=int(step['wait_completed']);ecx=VM if step['wait_completed'] else 0
        elif va==0x407AD0:eax=1;ecx=layout()['packet']
        elif va==0x4CE8F0 and step['pending'] is None:eax=1;ecx=0
        elif va==0x454CF0 and step['pending'] is None:eax=0;ecx=0
        if eax is not None:returns.append(dict(va=rules[va]['ret'],return_va=c['return_va'],sp=c['sp'],eax=eax,ecx=ecx))
    # Function entries precede nested returns: the enclosing VM/task return events
    # occur after all typed helpers and the drawing body.
    roots=[r for r in returns if r['va'] in ('0x4d03b6','0x454ec1')];returns=[r for r in returns if r not in roots]+sorted(roots,key=lambda r:0 if r['va']=='0x4d03b6' else 1)
    if step['returns']!=returns:raise ValueError('VM panel original typed/draw/VM/task return instructions/values')
    return calls

def verify_step(step,index,kind,inputs,before):
    expected=project_step(kind,inputs,before)
    if step['index']!=index or any(step[k]!=v for k,v in expected.items()):raise ValueError('VM panel full independent intermediate state/packet/CPU')
    calls=verify_calls(step,inputs,before);prior=dict(EIP=RETURN,ESP=BASE_SP+4,EBP=BASE_SP-4,EAX=0,ECX=0);reset=expected['reset_CPU']
    declarations=[dict(entry='0x425de0',receiver=INPUT,return_va=hex(RETURN),sp=BASE_SP,previous_CPU=prior,driver_declared=True,original_outer_callsite_observed=False),dict(entry='0x454cf0',receiver=TACT,return_va=hex(RETURN),sp=BASE_SP,previous_CPU=reset,driver_declared=True,original_outer_callsite_observed=False)]
    if step['declarations']!=declarations or step['owned_bodies_stubbed'] is not False or step['debug_stack_check_adapter'] is not True:raise ValueError('VM panel explicit driver/whole bodies/debug scope')
    required={int(c['va'],16) for c in calls};forbidden={0x424F80,0x407B21,0x4C7190,0x410310,0x4128F0,0x4CCB30,0x4CCC44,0x4CCD0C}
    if kind=='character_entry':
        required.remove(ENTRY);required|={0x4CE9C5,0x4CE9DD,0x4CE9FB,0x4CEA45,0x4CED43};forbidden|={ENTRY,0x407AD0,0x4D03B6,0x454EC1}
    else:
        required|={0x407B17,0x408124,0x4D2DB3,0x4CD54B,0x4D03B6,0x454DA0,0x454EC1,0x497C2D}
        if kind=='display':required|={0x4C76D4,0x4C771A,0x4C76EC}
        elif kind=='release':required|={0x4C7AD9,0x4D0133,0x4D01B5};forbidden.add(0x4CE9C5)
        elif kind=='text_mode':required.add(0x4C555E)
        elif kind=='timer_start':required|={0x4C1E40,0x4C1E57,0x4C1E6C,0x4C1E81,0x4C1E95}
        elif kind=='timer_poll':
            required|={0x4CFF53,0x4CCBE2,0x4CCC2C,0x4CCC31};forbidden.add(0x4CE9C5)
            if step['wait_completed']:required|={0x4CCDFF,0x4D01B5}
            else:forbidden|={0x4CCDFF,0x4D01B5}
    character_end=next(int(r['end'],16) for r in source_contract()['functions'] if int(r['va'],16)==ENTRY)
    if not required<=set(step['visited']) or forbidden&set(step['visited']) or any(ENTRY<=a<character_end for a in step['visited']):raise ValueError('VM panel original state branches and native bodies')
    return expected['after']

def verify_case(c,phase):
    if phase not in PHASES or c['name'] not in ('initial','student9_waiting','fifth_class'):raise ValueError('VM panel known phase/case')
    cp,before,inputs,ranges=seed(c['name'])
    if phase in PREVIOUS:
        parent,before=checked(c['name'],PREVIOUS[phase]);cp=parent['continuation_checkpoint']
    a=unpack(c['actual'])
    if c['prior_checkpoint']!=cp or a['phase']!=phase or a['inputs']!=inputs or a['before']!=before or len(a['steps'])!=len(KINDS[phase]) or a['declared_task_calls']!=len(KINDS[phase]) or a['declared_reset_calls']!=len(KINDS[phase]) or a['completed_task_calls']!=len(KINDS[phase])-(phase=='character_entry'):raise ValueError('VM panel actual case/provenance/complete step count')
    current=before
    for index,(step,kind) in enumerate(zip(a['steps'],KINDS[phase])):current=verify_step(step,index,kind,inputs,current)
    if a['after']!=current or any(a.get(k) is not False for k in ('live_OS_observed','GPU_executed','full_outer_frame_executed','persistent_write_authority')):raise ValueError('VM panel complete final state/scope')
    retained(a)
    if a['retained_ranges']!=ranges or a['retained_bytes']!=sum(r['bytes'] for r in ranges):raise ValueError('VM panel all parent retained bytes')
    cp=c['continuation_checkpoint']
    if cp['path']!=f'.venv-audit/vm-panel-{phase}-{c["name"]}.pkl' or cp['pending_eip']!=hex(ENTRY if phase=='character_entry' else RETURN) or cp['runtime_or_original_save'] is not False:raise ValueError('VM panel fixed private checkpoint identity')
    return current

def fresh_identities(phase):
    parent_identities('fade_finish')
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=SOURCE_SHA256 or hashlib.sha256(SCRIPT.read_bytes()).hexdigest()!=SCRIPT_SHA:raise ValueError('VM panel fresh source before unpickle')
    while True:
        if phase not in SHAS or SHAS[phase] is None or hashlib.sha256(REPORTS[phase].read_bytes()).hexdigest()!=SHAS[phase]:raise ValueError('VM panel fresh current/ancestor report SHA before unpickle')
        if phase not in PREVIOUS:break
        phase=PREVIOUS[phase]

def envelope(r,phase):
    if r['phase']!=phase or r['source_contract']!=source_contract() or r['parent_report']!=PARENT.relative_to(ROOT).as_posix() or r['parent_sha256']!=PARENT_SHA or len(r['cases'])!=3 or {c['name'] for c in r['cases']}!={'initial','student9_waiting','fifth_class'} or any(r.get(k) is not False for k in ('character_handler_executed','live_OS_observed','GPU_executed','full_outer_frame_executed','persistent_write_authority')):raise ValueError('VM panel source/parent/scope envelope')

def verify_payload(payload,c,phase,after):
    a=unpack(c['actual']);cpu=payload['cpu']
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=c['name'] or payload['phase']!=phase or payload['evidence_kind']!='private_original_vm_panel_'+phase or payload['pending_eip']!=a['steps'][-1]['CPU']['EIP']:raise ValueError('VM panel private source/case identity')
    observed={k:cpu.reg_read(reg) for k,reg in zip(('EIP','ESP','EBP','EAX','ECX'),(UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX,UC_X86_REG_ECX))}
    if observed!=a['steps'][-1]['CPU']:raise ValueError('VM panel private actual CPU')
    for row in after+([] if a['steps'][-1]['packet'] is None else [a['steps'][-1]['packet']]):
        if read_memory(payload,row['pointer'],row['bytes']).hex()!=row['hex']:raise ValueError('VM panel full private owned/packet memory')
    if read_memory(payload,BASE_SP-4,8)!=struct.pack('<II',BASE_SP-4,RETURN):raise ValueError('VM panel private original declared return stack')
    pending=a['steps'][-1]['pending']
    if pending:
        wanted=struct.pack('<4I',int(pending['return_va'],16),*pending['args'])
        if read_memory(payload,pending['sp'],16)!=wanted:raise ValueError('VM panel private actual pending arguments')
        for at,value in ((layout()['vm'],0x454D90),(layout()['vm']-4,BASE_SP-4),(layout()['vm']-8,VM),(layout()['vm']-20,1)):
            if read_memory(payload,at,4)!=struct.pack('<I',value):raise ValueError('VM panel private original VM caller/locals')
    for row in a['retained_ranges']:
        if hashlib.sha256(read_memory(payload,row['pointer'],row['bytes'])).hexdigest()!=row['sha256']:raise ValueError('VM panel all private retained bytes')

def load_verified_checkpoint(name,phase):
    fresh_identities(phase);r=pinned(REPORTS[phase],SHAS[phase]);envelope(r,phase);c=next((c for c in r['cases'] if c['name']==name),None)
    if c is None:raise ValueError('VM panel known private case')
    after=verify_case(c,phase);cp=c['continuation_checkpoint'];raw=(ROOT/cp['path']).read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('VM panel file SHA before unpickle')
    payload=pickle.loads(raw);verify_payload(payload,c,phase,after);return payload,cp
