"""Independent typed original calls, full projections and private continuation."""
import hashlib,json,pickle,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP
from tools.school_following_students import *
from tools.school_following_students_emulation import UNITCTRL,TACT,STACK,MAPCTRL,PARENT,PARENT_SHA
from tools.school_student_action_verification import pinned
from tools.school_student_tail_verification import verify_case as verify_parent,retained

REPORT=ROOT/'analysis/school-following-students-native-v1-20261015.json'
REPORT_SHA='63aee6a4f7a243d0ea86687e13533dad9531abe11e8dfdfe80cbbf1adcb0c4d1'
INPUTS=ROOT/'analysis/school-following-students-inputs-20261015.json'
INPUTS_SHA='b0bcb2c6bb23afb666ea211b909cd0f2682c430cfa551aa67cd58e5e2839b9d6'


def pending(index):
    return {'va':'0x46b760','receiver':UNITCTRL,'return_va':'0x46b584','sp':STACK+0xFF00-100,
      'args':[UNITCTRL+0x80AEC+index*STRIDE,index],'first_instruction_executed':False}


def expected_calls(inputs,units):
    out=[]
    def add(va,recv,ret,depth,args):out.append({'va':hex(va),'receiver':recv,'return_va':hex(ret),'sp':STACK+0xFF00-depth,'args':args})
    for x,u in zip(inputs['units'],units):
        i=u['index'];w=UNITCTRL+0x80AEC+i*STRIDE;main,effect=x['bindings'];owner=main['owner'];efct=effect['owner'];rule=source_contract()['jobs'][str(u['job'])]
        for va,ret,depth,args in [(0x46B760,0x46B584,100,[w,i]),(0x48D720,0x46B7C9,208,[w,i]),(0x48E2A0,0x46B7D5,204,[w]),(0x475700,0x46B7E1,204,[w]),
          (0x4751F0,0x475734,316,[w]),(0x4697F0,0x475740,316,[w]),(0x475D60,0x4757A3,316,[w]),(0x46C040,0x475DBC,428,[w,2]),(0x46BCC0,0x475DCA,428,[w,18])]:add(va,UNITCTRL,ret,depth,args)
        add(0x465040,owner,0x46BCFE,528,[w+0x48,18,2]);add(0x409FF0,owner,0x465126,648,[w+0x48,rule['main']['bank'],rule['main']['index'],0])
        for n,p in enumerate(rule['attachments']):
            add(0x46BE50,UNITCTRL,0x475DEF if n==0 else 0x475E24,436,[w,p['animation'],0,0])
            add(0x465140,owner,0x46BE97,548,[w+0x48,efct,p['animation'],0,0,7]);definition=bytes.fromhex(p['definition_hex'])
            table=0x60F890+(p['animation']//1000-1)*800+p['animation']%1000*4
            add(0x40AF40,owner,0x465269,680,[w+0x48,efct,definition[1],definition[2],0,table&0xFFFF0000,7,definition[0]])
            add(0x40B5E0,owner,0x40AF6B,776,[]);add(0x40A800,owner,0x40B0DB,780,[u['allocated_nodes'][n]])
        add(0x40A100,owner,0x46B80C,204,[w+0x48]);add(0x40A800,owner,0x40A165,308,[w+0x48])
        for node in u['linked_order']:add(0x40A800,owner,0x40A1B0,308,[node])
        for n in range(5):add(0x40A100,efct,0x46B85B,204,[w+0xA0+n*NODE])
        controllers=[w+0x48]+[w+0xA0+n*NODE for n in range(5)]
        for va,ret,child,first,aux in ((0x482A30,0x46B86D,0x482AC0,0x482A64,0x482A9D),(0x4918D0,0x46B87D,0x491960,0x491904,0x49193D)):
            add(va,UNITCTRL,ret,208,[w,i])
            for n,controller in enumerate(controllers):add(child,UNITCTRL,first if n==0 else aux,312,[w,i,controller])
        for va,ret in ((0x493450,0x46B889),(0x472370,0x46B895),(0x472770,0x46B8BF),(0x430400,0x46B8CB)):add(va,UNITCTRL,ret,204,[w])
        add(0x43BB90,MAPCTRL,0x430485,324,u['cell']);add(0x4305C0,UNITCTRL,0x4304A4,324,[w,u['event_region']])
        add(0x43D270,MAPCTRL,0x46B95B,212,u['vision_args']);add(0x46B2C0,UNITCTRL,0x46B967,204,[w])
    return out


def verify_case(case):
    parent=next((r for r in pinned(PARENT,PARENT_SHA)['cases'] if r['name']==case['name']),None)
    capture=next((r for r in pinned(INPUTS,INPUTS_SHA)['cases'] if r['name']==case['name']),None)
    if parent is None or capture is None or case['parent_checkpoint']!=parent['continuation_checkpoint'] or capture['parent_checkpoint']!=case['parent_checkpoint']:raise ValueError('following exact trusted parent')
    verify_parent(parent);a=case['actual']
    if a['inputs']!=capture['inputs'] or a['before']!=capture['before']:raise ValueError('following full captured source inputs')
    pa=parent['actual_tail']['after']
    for i in (0,2,3,4,5,6,7,8,9):
        if a['before'][i]!=pa[i]:raise ValueError('following complete parent owned region')
    rec=pa[1];off=(rec['pointer']-a['before'][1]['pointer'])*2
    if a['before'][1]['hex'][off:off+rec['bytes']*2]!=rec['hex']:raise ValueError('following first record parent bytes')
    result=project(a['inputs'],a['before'])
    if any(a[k]!=v for k,v in result.items()):raise ValueError('following complete independent projection')
    if a['calls']!=expected_calls(a['inputs'],result['units']):raise ValueError('following complete original typed calls/stack')
    # Verify every direct caller against the immutable executable as well.
    exe=SOURCE.read_bytes()
    for row in a['calls']:
        ret=int(row['return_va'],16);call=exe[ret-5-BASE:ret-BASE]
        if len(call)!=5 or call[0]!=0xE8 or ret+struct.unpack_from('<i',call,1)[0]!=int(row['va'],16):raise ValueError('following original direct call bytes')
    indices=[u['index'] for u in result['units']]
    if a['unit_entries']!=indices or a['tested_slots']!=list(range(2,216)) or a['pending']!=pending(215):raise ValueError('following natural full empty interval')
    returns=deepcopy(a['unit_returns'])
    for row in returns:
        eax=row.pop('eax')
        if not isinstance(eax,int) or not 0<=eax<=0xFFFFFFFF:raise ValueError('following void return observation')
    wanted=[{'index':i,'va':'0x46ba07','return_va':'0x46b584','sp':STACK+0xFF00-100} for i in indices]
    nodes=[p for u in result['units'] for p in u['allocated_nodes']]
    if returns!=wanted or a['native_clears']!=[{'return_va':'0x409f1a','args':[p,0,88]} for p in nodes]:raise ValueError('following original ret8/first-free clear')
    required={int(r['va'],16) for r in a['calls']}|{0x46BA07,0x468D10,0x490350}
    if not required<=set(a['visited']) or any(v in a['visited'] for v in (0x479F40,0x46BC20,0x472550,0x480A60,0x43C470)):raise ValueError('following actual bodies/closed gates')
    for k in ('owned_bodies_stubbed','deferred_unit_executed','VM_or_AI_completed','world_completed'):
        if a.get(k) is not False:raise ValueError('following exact authority scope')
    retained(a);cp=case['continuation_checkpoint']
    if cp['path']!=f'.venv-audit/following-students-before-slot215-{case["name"]}.pkl' or cp['pending_eip']!='0x46b760' or cp['runtime_or_original_save'] is not False:raise ValueError('following private scope')
    return True


def read_memory(payload,at,n):
    for start,buf in payload['memory']:
        if start<=at and at+n<=start+len(buf):return buf[at-start:at-start+n]
    raise ValueError('following private missing memory')


def load_verified_checkpoint(name):
    raw=REPORT.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=REPORT_SHA:raise ValueError('following current fixed report SHA before unpickle')
    case=next((r for r in json.loads(raw)['cases'] if r['name']==name),None)
    if case is None:raise ValueError('following private case')
    verify_case(case);cp=case['continuation_checkpoint'];raw=(ROOT/cp['path']).read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('following fixed file SHA before unpickle')
    payload=pickle.loads(raw);cpu=payload['cpu'];p=pending(215);sp=cpu.reg_read(UC_X86_REG_ESP)
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=name or payload['evidence_kind']!='private_original_following_students_before_slot215':raise ValueError('following private provenance')
    if payload['pending_eip']!=0x46B760 or cpu.reg_read(UC_X86_REG_EIP)!=0x46B760 or cpu.reg_read(UC_X86_REG_ECX)!=UNITCTRL or sp!=p['sp']:raise ValueError('following private actual CPU')
    if list(struct.unpack('<3I',read_memory(payload,sp,12)))!=[int(p['return_va'],16)]+p['args']:raise ValueError('following next original stack')
    for r in case['actual']['after']:
        if read_memory(payload,r['pointer'],r['bytes']).hex()!=r['hex']:raise ValueError('following private complete owned memory')
    for r in case['actual']['retained_ranges']:
        if hashlib.sha256(read_memory(payload,r['pointer'],r['bytes'])).hexdigest()!=r['sha256']:raise ValueError('following private complete retained memory')
    return payload,cp
