"""Independent full scene217 source/calls and fixed private phase provenance."""
import hashlib,json,pickle,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP
from tools.school_scene_first import *
from tools.school_scene_first_emulation import UNITCTRL,STACK,MAPCTRL,PARENT,PARENT_SHA
from tools.school_deferred_units_verification import verify_case as verify_parent
from tools.school_following_students_verification import pinned,pending as unit_pending,read_memory
from tools.school_student_tail_verification import retained

REPORTS={p:ROOT/f'analysis/school-scene-first-{p}-v1-20261015.json' for p in ('initializer','complete')}
SHAS={'initializer':'728c9f9d5458b36780505191b9a4d7fe4a122586ef669ac214dbb43d45c687cc','complete':'9c7f3f2fb79209bf0f971ccf34f783ee7857f6be4dfb21d0f86f38b204ee7122'}
INPUTS=ROOT/'analysis/school-scene-first-inputs-20261015.json'
INPUTS_SHA='e5794df3b0f416d8bfeee64f1f6dfe6a5f9bb93477d58999cb4b8e89c0e1899c'


def pending(phase,inputs):
    w=UNITCTRL+0x80AEC+INDEX*STRIDE
    return {'va':'0x40a100','receiver':inputs['main_binding']['owner'],'return_va':'0x46b80c','sp':STACK+0xFF00-204,'args':[w+0x48],'first_instruction_executed':False} if phase=='initializer' else unit_pending(218)


def expected_calls(phase,inputs,result):
    w=UNITCTRL+0x80AEC+INDEX*STRIDE;owner=inputs['main_binding']['owner'];out=[]
    def add(va,recv,ret,depth,args):out.append({'va':hex(va),'receiver':recv,'return_va':hex(ret),'sp':STACK+0xFF00-depth,'args':args})
    if phase=='initializer':
        for va,ret,depth,args in ((0x46B760,0x46B584,100,[w,217]),(0x48D720,0x46B7C9,208,[w,217]),(0x48E2A0,0x46B7D5,204,[w]),(0x475700,0x46B7E1,204,[w]),
          (0x4751F0,0x475734,316,[w]),(0x4697F0,0x475740,316,[w]),(0x4761C0,0x475BDD,316,[w]),(0x46B0F0,0x47620F,424,[w,1]),(0x46B0B0,0x47621D,424,[w,1]),(0x46BCC0,0x47622B,424,[w,1])):add(va,UNITCTRL,ret,depth,args)
        add(0x465040,owner,0x46BCFE,524,[w+0x48,1,9]);add(0x409FF0,owner,0x465126,644,[w+0x48,0,2,1])
        add(0x480A60,UNITCTRL,0x475C55,316,[w]);add(0x490350,UNITCTRL,0x46B7FA,208,[w,217])
        for n,ret in enumerate((0x49037F,0x490391,0x4903A3)):add(0x490A50,UNITCTRL,ret,308,[n,w,217])
    else:
        add(0x40A100,owner,0x46B80C,204,[w+0x48]);add(0x40A800,owner,0x40A165,308,[w+0x48])
        for n in range(5):add(0x40A100,inputs['effect_controller'],0x46B85B,204,[w+0xA0+n*88])
        controllers=[w+0x48]+[w+0xA0+n*88 for n in range(5)]
        for va,ret,child,first,aux in ((0x482A30,0x46B86D,0x482AC0,0x482A64,0x482A9D),(0x4918D0,0x46B87D,0x491960,0x491904,0x49193D)):
            add(va,UNITCTRL,ret,208,[w,217])
            for n,controller in enumerate(controllers):add(child,UNITCTRL,first if n==0 else aux,312,[w,217,controller])
        for va,ret in ((0x493450,0x46B889),(0x472370,0x46B895),(0x472770,0x46B8BF),(0x430400,0x46B8CB)):add(va,UNITCTRL,ret,204,[w])
        add(0x43BB90,MAPCTRL,0x430485,324,[59,12]);add(0x4305C0,UNITCTRL,0x4304A4,324,[w,result['event_region']])
        add(0x46A430,UNITCTRL,0x46B8EB,204,[w]);add(0x46A5E0,UNITCTRL,0x46B8FB,204,[w]);add(0x46A430,UNITCTRL,0x46A63D,296,[w]);add(0x46B2C0,UNITCTRL,0x46B967,204,[w])
    return out


def verify_case(case,phase):
    if phase not in REPORTS:raise ValueError('scene exact phase')
    parent=next((c for c in pinned(PARENT,PARENT_SHA)['cases'] if c['name']==case['name']),None)
    capture=next((c for c in pinned(INPUTS,INPUTS_SHA)['cases'] if c['name']==case['name']),None)
    if parent is None or capture is None or case['parent_checkpoint']!=parent['continuation_checkpoint'] or capture['parent_checkpoint']!=case['parent_checkpoint']:raise ValueError('scene exact original parent')
    verify_parent(parent);a=case['actual'];inputs=a['inputs'];before=a['initial_before']
    if a['phase']!=phase or inputs!=capture['inputs'] or before!=capture['before'] or before!=parent['actual']['after']:raise ValueError('scene entire captured parent state')
    expected=project(inputs,before,phase)
    if any(a[k]!=v for k,v in expected.items()):raise ValueError('scene entire independent projection')
    previous=before
    if phase=='complete':
        init=next(c for c in pinned(REPORTS['initializer'],SHAS['initializer'])['cases'] if c['name']==case['name']);verify_case(init,'initializer')
        if case['initializer_checkpoint']!=init['continuation_checkpoint'] or inputs!=init['actual']['inputs'] or before!=init['actual']['initial_before']:raise ValueError('scene exact initializer continuation')
        previous=init['actual']['after']
    if a['before']!=previous or a['pending']!=pending(phase,inputs) or a['tested_slots']!=([218] if phase=='complete' else []):raise ValueError('scene original phase/boundary stack')
    if a['calls']!=expected_calls(phase,inputs,expected):raise ValueError('scene complete original typed calls')
    exe=SOURCE.read_bytes()
    for row in a['calls']:
        ret=int(row['return_va'],16);code=exe[ret-5-BASE:ret-BASE]
        if code[0]!=0xE8 or ret+struct.unpack_from('<i',code,1)[0]!=int(row['va'],16):raise ValueError('scene original direct caller bytes')
    if phase=='initializer':
        wanted=[{'va':'0x475bdd','sp':STACK+0xFF00-308,'eax':0},{'va':'0x475c55','sp':STACK+0xFF00-308,'eax':0},{'va':'0x46b7e1','sp':STACK+0xFF00-196,'eax':0}]
        if a['returns']!=wanted or 0x480D00 in a['visited'] or 0x40A100 in a['visited']:raise ValueError('scene closed original post-handler/initializer returns')
    else:
        wanted=[{'va':'0x46b80c','sp':STACK+0xFF00-196,'eax':1}]+[{'va':'0x46b85b','sp':STACK+0xFF00-196,'eax':1}]*5
        returns=deepcopy(a['returns'])
        if len(returns)!=7 or returns[:-1]!=wanted:raise ValueError('scene terminal and all auxiliary returns')
        eax=returns[-1].pop('eax')
        if not isinstance(eax,int) or not 0<=eax<=0xFFFFFFFF or returns[-1]!={'va':'0x46ba07','sp':STACK+0xFF00-100}:raise ValueError('scene void unit ret8 observation')
        if not {0x40A93A,0x40A93E,0x46BA07}<=set(a['visited']) or any(va in a['visited'] for va in (0x40A948,0x40AB80,0x43D270,0x472550,0x43C470)):raise ValueError('scene source terminal/vision and unexecuted release branches')
    if not {int(c['va'],16) for c in a['calls']}<=set(a['visited']):raise ValueError('scene all original recorded bodies')
    for k in ('owned_bodies_stubbed','next_unit_executed','animation_release_executed','VM_or_AI_completed','world_completed'):
        if a.get(k) is not False:raise ValueError('scene bounded authority')
    retained(a);cp=case['continuation_checkpoint']
    if cp['path']!=f'.venv-audit/scene-first-{phase}-{case["name"]}.pkl' or cp['pending_eip']!=pending(phase,inputs)['va'] or cp['runtime_or_original_save'] is not False:raise ValueError('scene private identity/scope')
    return True


def load_verified_checkpoint(name,phase='complete'):
    if phase not in REPORTS or SHAS[phase] is None:raise ValueError('scene pinned phase required')
    raw=REPORTS[phase].read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SHAS[phase]:raise ValueError('scene current report SHA before unpickle')
    case=next((c for c in json.loads(raw)['cases'] if c['name']==name),None)
    if case is None:raise ValueError('scene private case')
    verify_case(case,phase);cp=case['continuation_checkpoint'];raw=(ROOT/cp['path']).read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('scene private file SHA before unpickle')
    payload=pickle.loads(raw);cpu=payload['cpu'];a=case['actual'];p=pending(phase,a['inputs']);sp=cpu.reg_read(UC_X86_REG_ESP)
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=name or payload['phase']!=phase or payload['evidence_kind']!='private_original_scene_first_'+phase:raise ValueError('scene private exact provenance')
    if payload['pending_eip']!=int(p['va'],16) or cpu.reg_read(UC_X86_REG_EIP)!=payload['pending_eip'] or cpu.reg_read(UC_X86_REG_ECX)!=p['receiver'] or sp!=p['sp']:raise ValueError('scene private exact CPU')
    words=list(struct.unpack('<'+'I'*(len(p['args'])+1),read_memory(payload,sp,4*(len(p['args'])+1))))
    if words!=[int(p['return_va'],16)]+p['args']:raise ValueError('scene private natural return/args')
    for r in a['after']:
        if read_memory(payload,r['pointer'],r['bytes']).hex()!=r['hex']:raise ValueError('scene private complete owned bytes')
    for r in a['retained_ranges']:
        if hashlib.sha256(read_memory(payload,r['pointer'],r['bytes'])).hexdigest()!=r['sha256']:raise ValueError('scene private complete retained bytes')
    if read_memory(payload,UNITCTRL+0x115AAC,256).hex()!=a['inputs']['relation_matrix_hex']:raise ValueError('scene private source relation matrix')
    b=a['inputs']['main_binding'];raw=read_memory(payload,b['metadata_pointer'],b['metadata_bytes'])
    if hashlib.sha256(raw).hexdigest()!=b['metadata_sha256'] or read_memory(payload,b['owner'],84).hex()!=b['controller_hex']:raise ValueError('scene private entire source metadata/owner')
    return payload,cp
