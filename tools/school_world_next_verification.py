"""Independent next-world source, original calls and private-state validation."""
import hashlib,json,pickle,struct
from copy import deepcopy
from functools import lru_cache
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP
from tools.school_world_next import *
from tools.school_world_next_emulation import UNITCTRL,STACK,RETURN,PARENT,PARENT_SHA
from tools.school_world_final_verification import verify_case as verify_parent
from tools.school_following_students_verification import pinned,read_memory
from tools.school_world_second_verification import expected_calls as prefix_calls
from tools.school_student_tail_verification import retained,restored,pending as tail_pending,expected_calls as tail_calls
from tools.school_student_tail import project as tail_project

REPORTS={p:ROOT/f'analysis/school-world-next-{p}-v1-20261015.json' for p in ('prefix','unit')}
SHAS={'prefix':'91a358f2bb1b78839454963d7e9c540e624d94fa69375c34abae73d0d511558b','unit':None}
INPUTS=ROOT/'analysis/school-world-next-inputs-20261015.json'
INPUTS_SHA='5d7b2a48bb260635db0f9c3e79fc93d86432c698574f3d643ea94cc1d3842722'


def pending(phase):
    if phase=='unit':return tail_pending()
    return dict(va='0x475d60',receiver=UNITCTRL,return_va='0x4757a3',sp=STACK+0xFF00-316,args=[UNITCTRL+0x80AEC],first_instruction_executed=False)


@lru_cache(maxsize=3)
def parent_checked(name):
    c=next(c for c in pinned(PARENT,PARENT_SHA)['cases'] if c['name']==name);verify_parent(c,'return');return c


@lru_cache(maxsize=3)
def prefix_checked(name):
    c=next(c for c in pinned(REPORTS['prefix'],SHAS['prefix'])['cases'] if c['name']==name);verify_case(c,'prefix');return c


def animation_calls(inputs,result):
    w=UNITCTRL+0x80AEC;owner=inputs['main_controller'];effect=inputs['effect_controller'];out=[]
    def add(va,recv,ret,depth,args):out.append(dict(va=hex(va),receiver=recv,return_va=hex(ret),sp=STACK+0xFF00-depth,args=args))
    add(0x475D60,UNITCTRL,0x4757A3,316,[w]);add(0x490350,UNITCTRL,0x46B7FA,208,[w,0]);add(0x40A100,owner,0x46B80C,204,[w+0x48]);add(0x40A800,owner,0x40A165,308,[w+0x48])
    for p in result['linked_order']:add(0x40A800,owner,0x40A1B0,308,[p])
    for i in range(5):add(0x40A100,effect,0x46B85B,204,[w+0xA0+i*88])
    return out


def verify_case(c,phase):
    if phase not in REPORTS:raise ValueError('next exact phase')
    capture=next((r for r in pinned(INPUTS,INPUTS_SHA)['cases'] if r['name']==c['name']),None)
    if capture is None or c['parent_checkpoint']!=capture['parent_checkpoint'] or c['parent_checkpoint']!=parent_checked(c['name'])['continuation_checkpoint']:raise ValueError('next exact parent/capture')
    a=c['actual']
    if phase=='prefix':
        if a['before']!=capture['prefix_before'] or a['inputs']!=capture['prefix_inputs']:raise ValueError('next full original prefix input')
        result=prefix_project(a['inputs'],a['before'])
        calls=[r for r in prefix_calls(a['inputs']) if r['va']!='0x415070']
        if a['calls']!=calls or a['pending']!=pending(phase) or a['tested_slots']!=[0]:raise ValueError('next natural prefix calls/stack/boundary')
        clears=[dict(return_va='0x43d10c',args=[a['before'][7]['pointer'],0,6144]),dict(return_va='0x46f46f',args=[UNITCTRL+0x3098C,0,10]),dict(return_va='0x46b526',args=[UNITCTRL+0x2E714,0,2048])]
        if a['native_clears']!=clears or a['declared_root'] is not True:raise ValueError('next native clear/declared root')
        required={int(r['va'],16) for r in calls}|{0x56CEC0,0x468D10,0x49A099}
        if not required<=set(a['visited']) or {0x475D60,0x415070,0x40A100,0x4CE8F0}&set(a['visited']):raise ValueError('next prefix exact original branches')
        probes=c['clearing_probes']
        if probes['declared_isolated_calls'] is not True or any(probes[k] is not False for k in ('live_input_captured','world_advanced','attached_node_free_executed')) or len(probes['rows'])!=3:raise ValueError('next isolated scope')
        for p,s in zip(probes['rows'],capture['ended']):
            if any(p[k]!=s[k] for k in s) or p['after_hex']!=clearing_project(bytes.fromhex(p['before_hex'])).hex() or p['return_eax']!=1:raise ValueError('next complete ended root source')
            calls=[dict(va=hex(va),receiver=p['receiver'],return_va=hex(ret),sp=STACK+0xFF00-depth,args=[p['pointer']]) for va,ret,depth in ((0x40A100,RETURN,0),(0x40A800,0x40A165,104),(0x40AB80,0x40A845,220))]
            if p['calls']!=calls or not {0x40A100,0x40A800,0x40AB80}<=set(p['visited']) or {0x40B660,0x40B6A0}&set(p['visited']):raise ValueError('next original delayed clear calls/empty children')
            restored(p['restoration']);retained(p)
        for k in ('third_world_completed','VM_or_AI_completed','owned_bodies_stubbed'):
            if a.get(k) is not False:raise ValueError('next prefix completion scope')
    else:
        prior=prefix_checked(c['name'])
        if c['prefix_checkpoint']!=prior['continuation_checkpoint'] or a['before']!=capture['animation_before'] or a['inputs']!=capture['animation_inputs']:raise ValueError('next actual phase1 captured input')
        result=animation_project(a['inputs'],a['before'])
        if a['calls']!=animation_calls(a['inputs'],result):raise ValueError('next phase1 animation original calls')
        wanted=[dict(va=hex(va),sp=STACK+0xFF00-depth,eax=eax) for va,depth,eax in [(0x4757A3,308,0),(0x46B7E1,196,0),(0x46B80C,196,0)]+[(0x46B85B,196,1)]*5]
        if a['returns']!=wanted or a['pending']!=dict(va='0x482a30',receiver=UNITCTRL,return_va='0x46b86d',sp=STACK+0xFF00-208,args=[UNITCTRL+0x80AEC,0],first_instruction_executed=False):raise ValueError('next original phase1 returns/boundary')
        for k in ('original_initialization_repeated','allocation_executed','audio_executed','owned_bodies_stubbed'):
            if a.get(k) is not False:raise ValueError('next animation scope')
        if not {0x475E7A,0x475ED6,0x40A100,0x40A800}<=set(a['visited']) or {0x46BCC0,0x40B5E0,0x40A520,0x40B990}&set(a['visited']):raise ValueError('next phase1 branch proof')
        verify_tail(c,a)
    if any(a[k]!=v for k,v in result.items()):raise ValueError('next entire independent source projection')
    exe=SOURCE.read_bytes();calls=a['calls'][:]
    if phase=='prefix':calls += [r for p in c['clearing_probes']['rows'] for r in p['calls']]
    else:calls += c['actual_tail']['calls']
    for r in calls:
        ret=int(r['return_va'],16)
        if ret==RETURN:continue
        op=exe[ret-BASE-5:ret-BASE]
        if op[0]!=0xE8 or ret+struct.unpack_from('<i',op,1)[0]!=int(r['va'],16):raise ValueError('next original direct call bytes')
    retained(a);cp=c['continuation_checkpoint']
    if cp['path']!=f'.venv-audit/world-next-{phase}-{c["name"]}.pkl' or cp['pending_eip']!=pending(phase)['va'] or cp['runtime_or_original_save'] is not False:raise ValueError('next private path/phase/scope')
    return True


def verify_tail(c,animation):
    t=c['actual_tail'];expected_before=deepcopy(animation['after']);r=expected_before[1];p=animation['inputs']['record_pointer'];off=(p-r['pointer'])*2
    expected_before[1]=dict(name='record',pointer=p,bytes=176,hex=r['hex'][off:off+352])
    if t['before']!=expected_before:raise ValueError('next tail full animation provenance')
    if any(t[k]!=v for k,v in tail_project(t['inputs'],t['before']).items()):raise ValueError('next tail entire source projection')
    calls=deepcopy(t['calls'])
    for r in calls:
        if r['va']=='0x4ddbb0':r['receiver']=None
    if calls!=tail_calls():raise ValueError('next original tail calls')
    w=UNITCTRL+0x80AEC
    for key,first,aux in (('effect_scans','0x482a64','0x482a9d'),('damage_scans','0x491904','0x49193d')):
        wanted=[dict(args=[w,0,p],return_va=first if i==0 else aux,sp=STACK+0xFF00-312) for i,p in enumerate([w+0x48]+[w+0xA0+n*88 for n in range(5)])]
        if t[key]!=wanted:raise ValueError('next all six effect/damage scans')
    if t['native_heals'] or t['next_tests']!=[1] or t['pending']!=pending('unit') or t['returned']!=dict(va='0x46b584',sp=STACK+0xFF00-88):raise ValueError('next natural unit return/slot1')
    ret=deepcopy(t['real_ret']);eax=ret.pop('eax')
    if type(eax) is not int or not 0<=eax<=0xFFFFFFFF or ret!=dict(va='0x46ba07',sp=STACK+0xFF00-100,return_va='0x46b584'):raise ValueError('next original ret8')
    full=deepcopy(animation['after'])
    for i in (0,2,3,4,5,6,7,8,9):full[i]=t['after'][i]
    if c['full_after']!=full:raise ValueError('next complete250 records and all final regions')
    for k in ('next_unit_executed','nonempty_effect_or_damage_executed','world_or_VM_or_AI_completed','owned_bodies_stubbed'):
        if t.get(k) is not False:raise ValueError('next tail exact authority')
    if not {0x46BA07,0x46B584,0x468D10}<=set(t['visited']) or {0x46B760,0x472550,0x46BC20}&set(t['visited']):raise ValueError('next tail unexecuted slot1')
    retained(t)


def load_verified_checkpoint(name,phase='unit'):
    if phase not in REPORTS or SHAS[phase] is None:raise ValueError('next pinned phase')
    identities=[(REPORTS[phase],SHAS[phase]),(PARENT,PARENT_SHA),(INPUTS,INPUTS_SHA)]
    if phase=='unit':identities.append((REPORTS['prefix'],SHAS['prefix']))
    for path,sha in identities:
        if hashlib.sha256(path.read_bytes()).hexdigest()!=sha:raise ValueError('next current source/parent/report SHA before unpickle')
    report=pinned(REPORTS[phase],SHAS[phase]);pinned(PARENT,PARENT_SHA);pinned(INPUTS,INPUTS_SHA)
    if phase=='unit':pinned(REPORTS['prefix'],SHAS['prefix'])
    c=next((r for r in report['cases'] if r['name']==name),None)
    if c is None:raise ValueError('next private case')
    verify_case(c,phase);cp=c['continuation_checkpoint'];raw=(ROOT/cp['path']).read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('next file SHA before unpickle')
    payload=pickle.loads(raw);cpu=payload['cpu'];p=pending(phase);sp=cpu.reg_read(UC_X86_REG_ESP)
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=name or payload['phase']!=phase or payload['evidence_kind']!='private_original_world_next_'+phase:raise ValueError('next source/parent/case/phase')
    if payload['pending_eip']!=int(p['va'],16) or cpu.reg_read(UC_X86_REG_EIP)!=payload['pending_eip'] or cpu.reg_read(UC_X86_REG_ECX)!=UNITCTRL or sp!=p['sp']:raise ValueError('next natural CPU')
    if list(struct.unpack('<'+'I'*(1+len(p['args'])),read_memory(payload,sp,4+len(p['args'])*4)))!=[int(p['return_va'],16)]+p['args']:raise ValueError('next natural return/args stack')
    owned=c['actual']['after'] if phase=='prefix' else c['full_after'];a=c['actual'] if phase=='prefix' else c['actual_tail']
    for r in owned:
        if read_memory(payload,r['pointer'],r['bytes']).hex()!=r['hex']:raise ValueError('next complete private owned memory')
    for r in a['retained_ranges']:
        if hashlib.sha256(read_memory(payload,r['pointer'],r['bytes'])).hexdigest()!=r['sha256']:raise ValueError('next complete private retained memory')
    return payload,cp
