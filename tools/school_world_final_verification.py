"""Independent final-unit calls and bounded enabled-world return provenance."""
import hashlib,json,pickle,struct
from copy import deepcopy
from functools import lru_cache
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX
from tools.school_world_final import *
from tools.school_world_final_emulation import UNITCTRL,STACK,RETURN,MAPCTRL,PARENT,PARENT_SHA,ROOTS
from tools.school_scene_templates_verification import verify_case as verify_parent
from tools.school_following_students_verification import pinned,read_memory
from tools.school_student_tail_verification import retained
from tools.school_world_tail_verification import effect_calls

REPORTS={p:ROOT/f'analysis/school-world-final-{p}-v1-20261015.json' for p in ('units','return')}
SHAS={'units':'55db19a7b77bac377de783e61ff63e1da0a0404584ead42c4ff3786e35cd10b5','return':'f070a74c78eaab9024bb1cfac32b7ebbec8116814226a2d806225337a5dd5329'}
INPUTS=ROOT/'analysis/school-world-final-inputs-20261015.json'
INPUTS_SHA='9ad9906f38f47770d8cc6bb201a6ab6e1db8c5ac83ea8d68c245472ddbdaa4f0'


def pending():return {'va':'0x490fc0','receiver':UNITCTRL,'return_va':'0x46b620','sp':STACK+0xFF00-92,'args':[],'first_instruction_executed':False}


@lru_cache(maxsize=3)
def verified_parent(name):
    parent=next(c for c in pinned(PARENT,PARENT_SHA)['cases'] if c['name']==name)
    verify_parent(parent)
    return parent


@lru_cache(maxsize=3)
def verified_units(name):
    parent=next(c for c in pinned(REPORTS['units'],SHAS['units'])['cases'] if c['name']==name)
    verify_case(parent,'units')
    return parent


def unit_calls(inputs,units):
    out=[]
    def add(va,recv,ret,depth,args):out.append({'va':hex(va),'receiver':recv,'return_va':hex(ret),'sp':STACK+0xFF00-depth,'args':args})
    for x,u in zip(inputs['units'],units):
        i=u['index'];w=UNITCTRL+0x80AEC+i*STRIDE;owner=x['binding']['owner'];rule=source_contract()['jobs'][str(u['class'])]
        for va,ret,depth,args in ((0x46B760,0x46B584,100,[w,i]),(0x48D720,0x46B7C9,208,[w,i]),(0x48E2A0,0x46B7D5,204,[w]),(0x475700,0x46B7E1,204,[w]),
          (0x4751F0,0x475734,316,[w]),(0x4697F0,0x475740,316,[w]),(0x476250,0x475A42 if u['group']>=4 else 0x4757B7,316,[w]),(0x46BCC0,0x4762AE,432,[w,1])):add(va,UNITCTRL,ret,depth,args)
        add(0x465040,owner,0x46BCFE,532,[w+0x48,1,rule['direction']]);add(0x409FF0,owner,0x465126,652,[w+0x48,rule['main']['bank'],rule['main']['index'],bytes.fromhex(rule['lookup_hex'])[1]&3])
        if u['post_handler_called']:add(0x480A60,UNITCTRL,0x475C55,316,[w])
        add(0x490350,UNITCTRL,0x46B7FA,208,[w,i])
        for n,ret in enumerate((0x49037F,0x490391,0x4903A3)):add(0x490A50,UNITCTRL,ret,308,[n,w,i])
        add(0x40A100,owner,0x46B80C,204,[w+0x48]);add(0x40A800,owner,0x40A165,308,[w+0x48])
        for n in range(5):add(0x40A100,inputs['effect_controller'],0x46B85B,204,[w+0xA0+n*88])
        controllers=[w+0x48]+[w+0xA0+n*88 for n in range(5)]
        for va,ret,child,first,aux in ((0x482A30,0x46B86D,0x482AC0,0x482A64,0x482A9D),(0x4918D0,0x46B87D,0x491960,0x491904,0x49193D)):
            add(va,UNITCTRL,ret,208,[w,i])
            for n,c in enumerate(controllers):add(child,UNITCTRL,first if n==0 else aux,312,[w,i,c])
        for va,ret in ((0x493450,0x46B889),(0x472370,0x46B895),(0x472770,0x46B8BF),(0x430400,0x46B8CB)):add(va,UNITCTRL,ret,204,[w])
        add(0x43BB90,MAPCTRL,0x430485,324,u['cell'])
        if u['event_region']<32:add(0x4305C0,UNITCTRL,0x4304A4,324,[w,u['event_region']])
        add(0x46A430,UNITCTRL,0x46B8EB,204,[w])
        if u['group']!=inputs['team']:
            add(0x46A5E0,UNITCTRL,0x46B8FB,204,[w]);add(0x46A430,UNITCTRL,0x46A63D,296,[w])
        if u['vision_args'] is not None:
            add(0x4DDBB0,None,0x46B93E,204,[w]);add(0x43D270,MAPCTRL,0x46B95B,212,u['vision_args'])
        add(0x46B2C0,UNITCTRL,0x46B967,204,[w])
    return out


def verify_case(case,phase):
    if phase not in REPORTS:raise ValueError('world final exact phase')
    parent=next((c for c in pinned(PARENT,PARENT_SHA)['cases'] if c['name']==case['name']),None);capture=next((c for c in pinned(INPUTS,INPUTS_SHA)['cases'] if c['name']==case['name']),None)
    if parent is None or capture is None or case['parent_checkpoint']!=parent['continuation_checkpoint'] or capture['parent_checkpoint']!=case['parent_checkpoint']:raise ValueError('world final original parent identity')
    verified_parent(case['name']);a=case['actual']
    if a['phase']!=phase or a['tail_inputs']!=capture['tail_inputs'] or a['tail_before']!=capture['tail_before']:raise ValueError('world final complete captured suffix state')
    if phase=='units':
        if a['before']!=parent['actual']['after'] or a['before']!=capture['before'] or a['inputs']!=capture['inputs']:raise ValueError('world final complete unit parent bytes')
        result=units_project(a['inputs'],a['before'])
        if any(a[k]!=v for k,v in result.items()) or a['tail_after']!=a['tail_before']:raise ValueError('world final entire independent unit projection')
        calls=deepcopy(a['calls'])
        for row in calls:
            if row['va']=='0x4ddbb0':row['receiver']=None
        if calls!=unit_calls(a['inputs'],result['units']) or a['unit_entries']!=INDICES or a['tested_slots']!=list(range(241,250)) or a['pending']!=pending():raise ValueError('world final original unit calls/loop/stack')
        wanted=[]
        for u in result['units']:
            i=u['index'];w=UNITCTRL+0x80AEC+i*STRIDE
            values=[(0x475A42 if u['group']>=4 else 0x4757B7,308,0),(0x475C55,308,0 if u['post_handler_called'] else w),(0x46B7E1,196,0),(0x46B80C,196,u['main_return'])]+[(0x46B85B,196,1)]*5
            for va,depth,eax in values:wanted.append({'index':i,'va':hex(va),'sp':STACK+0xFF00-depth,'eax':eax})
            wanted.append({'index':i,'va':'0x46ba07','sp':STACK+0xFF00-100,'eax':None})
        actual=deepcopy(a['returns'])
        for row in actual:
            if row['va']=='0x46ba07':
                if not isinstance(row['eax'],int) or not 0<=row['eax']<=0xFFFFFFFF:raise ValueError('world final void unit return observation')
                row['eax']=None
        if actual!=wanted or not {0x46BA07,0x46B586,0x46B59C,0x46B61B}<=set(a['visited']) or any(va in a['visited'] for va in (0x490FC0,0x495220,0x46BC20,0x40AB80,0x472550,0x43C470)):raise ValueError('world final unit natural returns/loop clear/closed events')
        required={int(r['va'],16) for r in a['calls']}
    else:
        prior=verified_units(case['name'])
        if case['units_checkpoint']!=prior['continuation_checkpoint'] or a['before']!=prior['actual']['after'] or a['after']!=a['before'] or a['inputs']!=a['tail_inputs'] or a['tail_after']!=suffix_project(a['inputs'],a['tail_before']):raise ValueError('world final entire enabled suffix projection/provenance')
        sp=STACK+0xFF00-92;calls=[{'va':hex(va),'receiver':UNITCTRL,'return_va':hex(ret),'sp':sp} for va,ret in ROOTS.items()]
        calls += [{'va':'0x456b20','receiver':a['inputs']['entry_receiver'],'return_va':'0x48ce8b','sp':sp-88},{'va':'0x48d5d0','receiver':UNITCTRL,'return_va':'0x48ce99','sp':sp-88},
          {'va':'0x496450','receiver':UNITCTRL,'return_va':'0x48d5f5','sp':sp-192},{'va':'0x427de0','receiver':UNITCTRL+0x2A80,'return_va':'0x48d618','sp':sp-192}]
        if a['calls']!=calls or a['effect_calls']!=effect_calls(a['inputs'],True) or a['effect_returns']!=[1]*10:raise ValueError('world final original suffix and ten effect calls')
        if a['real_ret']!={'va':'0x46b662','return_va':hex(RETURN),'sp':STACK+0xFF00,'eax':0,'original_outer_caller':False}:raise ValueError('world final original ret/declared driver')
        if a['driver_return']!={'va':hex(RETURN),'sp':STACK+0xFF00+4,'ebp':STACK+0xFF00-4,'expected_caller_ebp':STACK+0xFF00-4,'eax':0,'declared_audit_sentinel':True}:raise ValueError('world final exact driver CPU')
        if a.get('second_46B470_body_completed') is not True or a.get('original_outer_task_frame_completed') is not False:raise ValueError('world final bounded body completion')
        required=set(ROOTS)|{0x40A100,0x456B20,0x48D5D0,0x496450,0x427DE0,0x46B662}
        if any(va in a['visited'] for va in (0x40A800,0x409FF0,0x427D60,0x496690,0x49CE90,0x4CE8F0)):raise ValueError('world final skipped active effect/command/VM')
    if not required<=set(a['visited']):raise ValueError('world final original required bodies')
    exe=SOURCE.read_bytes()
    for row in a['calls']:
        ret=int(row['return_va'],16);code=exe[ret-BASE-5:ret-BASE]
        if code[0]!=0xE8 or ret+struct.unpack_from('<i',code,1)[0]!=int(row['va'],16):raise ValueError('world final original direct call bytes')
    for key in ('owned_bodies_stubbed','VM_or_AI_completed','original_opening_completed','180_enabled_updates_completed'):
        if a.get(key) is not False:raise ValueError('world final exact authority')
    retained(a);cp=case['continuation_checkpoint'];eip='0x490fc0' if phase=='units' else hex(RETURN)
    if cp['path']!=f'.venv-audit/world-final-{phase}-{case["name"]}.pkl' or cp['pending_eip']!=eip or cp['runtime_or_original_save'] is not False:raise ValueError('world final private phase/path/scope')
    return True


def load_verified_checkpoint(name,phase='return'):
    if phase not in REPORTS or SHAS[phase] is None:raise ValueError('world final pinned phase required')
    raw=REPORTS[phase].read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SHAS[phase]:raise ValueError('world final current report SHA before unpickle')
    identities=[(PARENT,PARENT_SHA),(INPUTS,INPUTS_SHA)]
    if phase=='return':identities.append((REPORTS['units'],SHAS['units']))
    for path,sha in identities:
        if hashlib.sha256(path.read_bytes()).hexdigest()!=sha:raise ValueError('world final current source/parent report SHA before unpickle')
    case=next((c for c in json.loads(raw)['cases'] if c['name']==name),None)
    if case is None:raise ValueError('world final private case')
    verify_case(case,phase);cp=case['continuation_checkpoint'];raw=(ROOT/cp['path']).read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('world final private file SHA before unpickle')
    payload=pickle.loads(raw);cpu=payload['cpu'];a=case['actual'];sp=cpu.reg_read(UC_X86_REG_ESP)
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=name or payload['phase']!=phase or payload['evidence_kind']!='private_original_world_final_'+phase:raise ValueError('world final private provenance')
    if payload['pending_eip']!=int(cp['pending_eip'],16) or cpu.reg_read(UC_X86_REG_EIP)!=payload['pending_eip']:raise ValueError('world final private EIP')
    if phase=='units':
        if sp!=pending()['sp'] or cpu.reg_read(UC_X86_REG_ECX)!=UNITCTRL or struct.unpack('<I',read_memory(payload,sp,4))[0]!=0x46B620:raise ValueError('world final private natural suffix CPU/stack')
    elif sp!=a['driver_return']['sp'] or cpu.reg_read(UC_X86_REG_EBP)!=a['driver_return']['ebp'] or cpu.reg_read(UC_X86_REG_EAX)!=a['driver_return']['eax']:raise ValueError('world final private actual returned CPU')
    for row in a['after']+a['tail_after']:
        if read_memory(payload,row['pointer'],row['bytes']).hex()!=row['hex']:raise ValueError('world final private complete owned memory')
    for row in a['retained_ranges']:
        if hashlib.sha256(read_memory(payload,row['pointer'],row['bytes'])).hexdigest()!=row['sha256']:raise ValueError('world final private complete retained memory')
    return payload,cp
