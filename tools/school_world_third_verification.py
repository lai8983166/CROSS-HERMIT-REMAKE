"""Independent complete third-world continuation and private checkpoint proof."""
import hashlib,json,pickle,struct
from copy import deepcopy
from functools import lru_cache
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX
from tools.school_world_third import *
from tools.school_world_third_emulation import UNITCTRL,STACK,RETURN,PARENT,PARENT_SHA
from tools.school_world_next_verification import verify_case as verify_parent
from tools.school_following_students_verification import read_memory
from tools.school_student_tail_verification import retained
from tools.school_world_tail_emulation import ROOTS
from tools.school_world_tail_verification import effect_calls
from tools.school_world_final_verification import pending

REPORTS={p:ROOT/f'analysis/school-world-third-{p}-v1-20261015.json' for p in ('units','return')}
SHAS={'units':'f9c8f251691a7e621b10fa9975aef37f42f75dc42c6667d6e0b7facd23cc06f0','return':'4cb1a243cc4b02efc153088ac94043868bee345085ebd08173552c455f46183a'}
INPUTS=ROOT/'analysis/school-world-third-inputs-20261015.json'
INPUTS_SHA='71a105d32046c9a140f69656fd823683e8a012c245f1f08775ca09fa392e77d9'


@lru_cache(maxsize=8)
def pinned(path,sha):
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('third immutable source/report SHA')
    return json.loads(raw)


@lru_cache(maxsize=3)
def parent_checked(name):
    c=next(c for c in pinned(PARENT,PARENT_SHA)['cases'] if c['name']==name);verify_parent(c,'unit');return c


@lru_cache(maxsize=3)
def units_checked(name):
    c=next(c for c in pinned(REPORTS['units'],SHAS['units'])['cases'] if c['name']==name);verify_case(c,'units');return c


def unit_calls(inputs,units):
    out=[];mapctrl=UNITCTRL+0x3D68
    def add(va,recv,ret,depth,args):out.append(dict(va=hex(va),receiver=recv,return_va=hex(ret),sp=STACK+0xFF00-depth,args=args))
    for x,u in zip(inputs['units'],units):
        i=u['index'];w=UNITCTRL+0x80AEC+i*STRIDE
        for va,ret,depth,args in ((0x46B760,0x46B584,100,[w,i]),(0x48D720,0x46B7C9,208,[w,i]),(0x48E2A0,0x46B7D5,204,[w]),(0x475700,0x46B7E1,204,[w]),(0x4751F0,0x475734,316,[w]),(0x4697F0,0x475740,316,[w])):add(va,UNITCTRL,ret,depth,args)
        va,ret=(0x479F40,0x475B0A) if u['inactive'] else (0x475D60,0x4757A3) if i in (1,2) else (0x4761C0,0x475BDD) if i==217 else (0x476250,0x4757B7 if u['group']==0 else 0x475A42)
        add(va,UNITCTRL,ret,316,[w])
        if u['inactive']:continue
        owner=x['bindings'][0]['owner']
        if 387<=u['job']<=406:add(0x480A60,UNITCTRL,0x475C55,316,[w])
        add(0x490350,UNITCTRL,0x46B7FA,208,[w,i])
        for n,r in enumerate((0x49037F,0x490391,0x4903A3)):add(0x490A50,UNITCTRL,r,308,[n,w,i])
        add(0x40A100,owner,0x46B80C,204,[w+0x48]);add(0x40A800,owner,0x40A165,308,[w+0x48])
        if u['cleared_PC']:add(0x40AB80,owner,0x40A845,424,[w+0x48])
        for p in u['linked_order']:add(0x40A800,owner,0x40A1B0,308,[p])
        for n in range(5):add(0x40A100,inputs['effect_controller'],0x46B85B,204,[w+0xA0+n*NODE])
        for va,ret,child,first,aux in ((0x482A30,0x46B86D,0x482AC0,0x482A64,0x482A9D),(0x4918D0,0x46B87D,0x491960,0x491904,0x49193D)):
            add(va,UNITCTRL,ret,208,[w,i])
            for n,p in enumerate([w+0x48]+[w+0xA0+k*NODE for k in range(5)]):add(child,UNITCTRL,first if n==0 else aux,312,[w,i,p])
        for va,ret in ((0x493450,0x46B889),(0x472370,0x46B895),(0x472770,0x46B8BF),(0x430400,0x46B8CB)):add(va,UNITCTRL,ret,204,[w])
        add(0x43BB90,mapctrl,0x430485,324,u['cell'])
        if u['event_region']<32:add(0x4305C0,UNITCTRL,0x4304A4,324,[w,u['event_region']])
        add(0x46A430,UNITCTRL,0x46B8EB,204,[w])
        if u['group']!=inputs['team']:
            add(0x46A5E0,UNITCTRL,0x46B8FB,204,[w]);add(0x46A430,UNITCTRL,0x46A63D,296,[w])
        if u['vision_args'] is not None:
            add(0x4DDBB0,None,0x46B93E,204,[w]);add(0x43D270,mapctrl,0x46B95B,212,u['vision_args'])
        add(0x46B2C0,UNITCTRL,0x46B967,204,[w])
    return out


def verify_case(c,phase):
    if phase not in REPORTS:raise ValueError('third exact phase')
    cap=next((r for r in pinned(INPUTS,INPUTS_SHA)['cases'] if r['name']==c['name']),None)
    if cap is None or c['parent_checkpoint']!=cap['parent_checkpoint'] or c['parent_checkpoint']!=parent_checked(c['name'])['continuation_checkpoint']:raise ValueError('third exact source capture/parent')
    a=c['actual']
    if a['tail_before']!=cap['tail_before'] or a['tail_inputs']!=cap['tail_inputs']:raise ValueError('third captured full suffix')
    if phase=='units':
        if a['before']!=cap['before'] or a['before']!=parent_checked(c['name'])['full_after'] or a['inputs']!=cap['inputs']:raise ValueError('third full original before/input')
        result=project(a['inputs'],a['before'])
        if any(a[k]!=v for k,v in result.items()) or a['tail_after']!=a['tail_before']:raise ValueError('third complete source unit projection')
        calls=deepcopy(a['calls'])
        for r in calls:
            if r['va']=='0x4ddbb0':r['receiver']=None
        if calls!=unit_calls(a['inputs'],result['units']) or a['unit_entries']!=result['unit_indices'] or a['tested_slots']!=list(range(2,250)) or a['pending']!=pending():raise ValueError('third original calls/order/250-loop/boundary')
        wanted=[]
        for u in result['units']:
            i=u['index'];w=UNITCTRL+0x80AEC+i*STRIDE
            if u['inactive']:values=[(0x475B0A,308,1),(0x46B7E1,196,1),(0x46BA07,100,1)]
            else:
                ret=0x4757A3 if i in (1,2) else 0x475BDD if i==217 else 0x4757B7 if u['group']==0 else 0x475A42
                values=[(ret,308,0),(0x475C55,308,0 if 387<=u['job']<=406 else w),(0x46B7E1,196,0),(0x46B80C,196,u['main_return'])]+[(0x46B85B,196,1)]*5+[(0x46BA07,100,None)]
            wanted.extend(dict(index=i,va=hex(va),sp=STACK+0xFF00-depth,eax=eax) for va,depth,eax in values)
        actual=deepcopy(a['returns'])
        for r in actual:
            if r['va']=='0x46ba07' and r['index'] not in INACTIVE:
                if type(r['eax']) is not int or not 0<=r['eax']<=0xFFFFFFFF:raise ValueError('third void ret observation')
                r['eax']=None
        if actual!=wanted:raise ValueError('third all original handler/animation/unit returns')
        required={int(r['va'],16) for r in a['calls']}|{0x46B586,0x46B59C,0x46B61B}
        if not required<=set(a['visited']) or {0x490FC0,0x40A520,0x40B660,0x40B6A0,0x40B990,0x40AF40,0x46BC20,0x495220}&set(a['visited']):raise ValueError('third original branch boundary/closed audio/free/events')
        for k in ('owned_bodies_stubbed','audio_executed','attached_node_free_executed','VM_or_AI_completed'):
            if a.get(k) is not False:raise ValueError('third unit exact authority')
    else:
        prior=units_checked(c['name'])
        if c['units_checkpoint']!=prior['continuation_checkpoint'] or a['before']!=prior['actual']['after'] or a['after']!=a['before'] or a['inputs']!=a['tail_inputs'] or a['tail_after']!=suffix_project(a['inputs'],a['tail_before']):raise ValueError('third complete enabled suffix/provenance')
        sp=STACK+0xFF00-92;calls=[dict(va=hex(va),receiver=UNITCTRL,return_va=hex(ret),sp=sp) for va,ret in ROOTS.items()]
        calls += [dict(va='0x456b20',receiver=a['inputs']['entry_receiver'],return_va='0x48ce8b',sp=sp-88),dict(va='0x48d5d0',receiver=UNITCTRL,return_va='0x48ce99',sp=sp-88),dict(va='0x496450',receiver=UNITCTRL,return_va='0x48d5f5',sp=sp-192),dict(va='0x427de0',receiver=UNITCTRL+0x2A80,return_va='0x48d618',sp=sp-192)]
        if a['calls']!=calls or a['effect_calls']!=effect_calls(a['inputs'],True) or a['effect_returns']!=[1]*10:raise ValueError('third original suffix/effects/forwarding')
        if a['real_ret']!=dict(va='0x46b662',return_va=hex(RETURN),sp=STACK+0xFF00,eax=0,original_outer_caller=False):raise ValueError('third real ret to declared driver')
        if a['driver_return']!=dict(va=hex(RETURN),sp=STACK+0xFF00+4,ebp=STACK+0xFF00-4,expected_caller_ebp=STACK+0xFF00-4,eax=0,declared_audit_sentinel=True):raise ValueError('third exact natural returned CPU')
        if a.get('third_46B470_body_completed') is not True or a.get('original_outer_task_frame_completed') is not False:raise ValueError('third exact function-body scope')
        required=set(ROOTS)|{0x40A100,0x456B20,0x48D5D0,0x496450,0x427DE0,0x46B662}
        if not required<=set(a['visited']) or {0x40A800,0x40B660,0x4CE8F0,0x49CE90}&set(a['visited']):raise ValueError('third original suffix branch proof')
        for k in ('owned_bodies_stubbed','VM_or_AI_completed','original_opening_completed','180_enabled_updates_completed'):
            if a.get(k) is not False:raise ValueError('third suffix exact authority')
    exe=SOURCE.read_bytes()
    for r in a['calls']:
        ret=int(r['return_va'],16);op=exe[ret-BASE-5:ret-BASE]
        if op[0]!=0xE8 or ret+struct.unpack_from('<i',op,1)[0]!=int(r['va'],16):raise ValueError('third original direct call bytes')
    retained(a);cp=c['continuation_checkpoint'];eip='0x490fc0' if phase=='units' else hex(RETURN)
    if cp['path']!=f'.venv-audit/world-third-{phase}-{c["name"]}.pkl' or cp['pending_eip']!=eip or cp['runtime_or_original_save'] is not False:raise ValueError('third private scope/path/phase')
    return True


def load_verified_checkpoint(name,phase='return'):
    if phase not in REPORTS or SHAS[phase] is None:raise ValueError('third pinned phase required')
    identities=[(REPORTS[phase],SHAS[phase]),(PARENT,PARENT_SHA),(INPUTS,INPUTS_SHA)]
    if phase=='return':identities.append((REPORTS['units'],SHAS['units']))
    for path,sha in identities:
        if hashlib.sha256(path.read_bytes()).hexdigest()!=sha:raise ValueError('third current source/parent/report SHA before unpickle')
    c=next((r for r in pinned(REPORTS[phase],SHAS[phase])['cases'] if r['name']==name),None)
    if c is None:raise ValueError('third private case')
    verify_case(c,phase);cp=c['continuation_checkpoint'];raw=(ROOT/cp['path']).read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('third private file SHA before unpickle')
    payload=pickle.loads(raw);cpu=payload['cpu'];a=c['actual'];sp=cpu.reg_read(UC_X86_REG_ESP)
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=name or payload['phase']!=phase or payload['evidence_kind']!='private_original_world_third_'+phase:raise ValueError('third private source/parent/case/phase')
    if payload['pending_eip']!=int(cp['pending_eip'],16) or cpu.reg_read(UC_X86_REG_EIP)!=payload['pending_eip']:raise ValueError('third private exact EIP')
    if phase=='units':
        if sp!=pending()['sp'] or cpu.reg_read(UC_X86_REG_ECX)!=UNITCTRL or struct.unpack('<I',read_memory(payload,sp,4))[0]!=0x46B620:raise ValueError('third private natural suffix CPU/stack')
    elif sp!=a['driver_return']['sp'] or cpu.reg_read(UC_X86_REG_EBP)!=a['driver_return']['ebp'] or cpu.reg_read(UC_X86_REG_EAX)!=a['driver_return']['eax']:raise ValueError('third private returned CPU')
    for r in a['after']+a['tail_after']:
        if read_memory(payload,r['pointer'],r['bytes']).hex()!=r['hex']:raise ValueError('third complete owned private memory')
    for r in a['retained_ranges']:
        if hashlib.sha256(read_memory(payload,r['pointer'],r['bytes'])).hexdigest()!=r['sha256']:raise ValueError('third complete retained private memory')
    return payload,cp
