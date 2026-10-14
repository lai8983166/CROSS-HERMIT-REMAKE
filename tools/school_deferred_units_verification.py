"""Source-backed inactive dispatch/early return and complete next-scene state."""
import hashlib,json,pickle,struct
from tools.school_deferred_units import *
from tools.school_deferred_units_emulation import UNITCTRL,STACK,PARENT,PARENT_SHA
from tools.school_following_students_verification import pinned,pending,read_memory,verify_case as verify_parent
from tools.school_student_tail_verification import retained
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP

REPORT=ROOT/'analysis/school-following-students-deferred-native-v2-20261015.json'
REPORT_SHA='9f362468580653dfc2af36d66ae346a4700cdbf2252ccfcf969d5b3a1b678ee9'


def expected_calls():
    out=[]
    for index in (215,216):
        w=UNITCTRL+0x80AEC+index*STRIDE
        for va,ret,depth,args in ((0x46B760,0x46B584,100,[w,index]),(0x48D720,0x46B7C9,208,[w,index]),
          (0x48E2A0,0x46B7D5,204,[w]),(0x475700,0x46B7E1,204,[w]),(0x4751F0,0x475734,316,[w]),
          (0x4697F0,0x475740,316,[w]),(0x479F40,0x475B0A,316,[w]),(0x46B0B0,0x479F98,428,[w,0]),(0x46B0F0,0x479FA6,428,[w,0])):
            out.append({'va':hex(va),'receiver':UNITCTRL,'return_va':hex(ret),'sp':STACK+0xFF00-depth,'args':args})
    return out


def verify_case(case):
    parent=next((r for r in pinned(PARENT,PARENT_SHA)['cases'] if r['name']==case['name']),None)
    if parent is None or case['parent_checkpoint']!=parent['continuation_checkpoint']:raise ValueError('deferred exact actual parent checkpoint')
    verify_parent(parent);a=case['actual']
    if a['before']!=parent['actual']['after']:raise ValueError('deferred entire original parent state')
    expected=project(a['before'])
    if any(a[k]!=v for k,v in expected.items()):raise ValueError('deferred entire source projection')
    if a['calls']!=expected_calls() or a['unit_entries']!=[215,216] or a['tested_slots']!=[216,217] or a['pending']!=pending(217):raise ValueError('deferred natural typed calls/loop/stack')
    returns=[]
    for i in (215,216):
        returns.extend([{'index':i,'va':'0x475b0a','sp':STACK+0xFF00-308,'return_va':None,'eax':1},
          {'index':i,'va':'0x46ba07','sp':STACK+0xFF00-100,'return_va':'0x46b584','eax':1}])
    if a['returns']!=returns:raise ValueError('deferred original handler and unit return1')
    required={int(r['va'],16) for r in expected_calls()}|{0x475B0A,0x46BA07,0x468D10}
    if not required<=set(a['visited']) or any(va in a['visited'] for va in (0x40A100,0x490350,0x482A30,0x4918D0,0x493450,0x472370,0x472770,0x430400,0x43D270,0x480A60)):raise ValueError('deferred early-return skipped branches')
    exe=SOURCE.read_bytes()
    for row in a['calls']:
        ret=int(row['return_va'],16);call=exe[ret-BASE-5:ret-BASE]
        if call[0]!=0xE8 or ret+struct.unpack_from('<i',call,1)[0]!=int(row['va'],16):raise ValueError('deferred original caller bytes')
    for key in ('owned_bodies_stubbed','scene_unit_executed','VM_or_AI_completed','world_completed'):
        if a.get(key) is not False:raise ValueError('deferred exact authority')
    retained(a);cp=case['continuation_checkpoint']
    if cp['path']!=f'.venv-audit/deferred-units-before-scene217-{case["name"]}.pkl' or cp['pending_eip']!='0x46b760' or cp['runtime_or_original_save'] is not False:raise ValueError('deferred private source scope')
    return True


def load_verified_checkpoint(name):
    raw=REPORT.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=REPORT_SHA:raise ValueError('deferred current report SHA before unpickle')
    case=next((r for r in json.loads(raw)['cases'] if r['name']==name),None)
    if case is None:raise ValueError('deferred private case')
    verify_case(case);cp=case['continuation_checkpoint'];raw=(ROOT/cp['path']).read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('deferred private file SHA before unpickle')
    payload=pickle.loads(raw);cpu=payload['cpu'];p=pending(217);sp=cpu.reg_read(UC_X86_REG_ESP)
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=name or payload['evidence_kind']!='private_original_deferred_units_before_scene217':raise ValueError('deferred private original provenance')
    if payload['pending_eip']!=0x46B760 or cpu.reg_read(UC_X86_REG_EIP)!=0x46B760 or cpu.reg_read(UC_X86_REG_ECX)!=UNITCTRL or sp!=p['sp']:raise ValueError('deferred exact next CPU')
    if list(struct.unpack('<3I',read_memory(payload,sp,12)))!=[int(p['return_va'],16)]+p['args']:raise ValueError('deferred original return/next scene stack')
    for r in case['actual']['after']:
        if read_memory(payload,r['pointer'],r['bytes']).hex()!=r['hex']:raise ValueError('deferred private complete owned memory')
    for r in case['actual']['retained_ranges']:
        if hashlib.sha256(read_memory(payload,r['pointer'],r['bytes'])).hexdigest()!=r['sha256']:raise ValueError('deferred private complete retained memory')
    return payload,cp
