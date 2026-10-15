"""Independent source projection and original22-unit early-return loop proof."""
import hashlib,json,pickle,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP
from tools.school_scene_templates import *
from tools.school_scene_templates_emulation import UNITCTRL,STACK,PARENT,PARENT_SHA
from tools.school_scene_first_verification import verify_case as verify_parent
from tools.school_following_students_verification import pinned,pending,read_memory
from tools.school_deferred_units_verification import expected_calls as first_template_calls
from tools.school_student_tail_verification import retained

REPORT=ROOT/'analysis/school-scene-first-templates-v1-20261015.json'
REPORT_SHA='6243f5415fb629e3358402d6ceb548f94f3a851410f3cb948aa0a123a2ebbc5f'


def expected_calls():
    # The already source-checked mode11/state0 branch is identical for every
    # source job here; all lie outside the387–406 post-handler interval.
    pattern=first_template_calls()[:9];out=[]
    for i in INDICES:
        w=UNITCTRL+0x80AEC+i*STRIDE;calls=deepcopy(pattern)
        for row in calls:
            row['args'][0]=w
            if row['va'] in ('0x46b760','0x48d720'):row['args'][1]=i
        out.extend(calls)
    return out


def verify_case(case):
    parent=next((c for c in pinned(PARENT,PARENT_SHA)['cases'] if c['name']==case['name']),None)
    if parent is None or case['parent_checkpoint']!=parent['continuation_checkpoint']:raise ValueError('template batch exact source parent')
    verify_parent(parent,'complete');a=case['actual']
    if a['before']!=parent['actual']['after']:raise ValueError('template batch complete actual parent bytes')
    result=project(a['before'])
    if any(a[k]!=v for k,v in result.items()):raise ValueError('template batch entire independent projection')
    if a['calls']!=expected_calls() or a['tested_slots']!=list(range(219,241)) or a['pending']!=pending(240):raise ValueError('template batch original calls/loop/stack')
    expected=[]
    for i in INDICES:expected.extend([{'index':i,'va':'0x475b0a','sp':STACK+0xFF00-308,'eax':1},{'index':i,'va':'0x46ba07','sp':STACK+0xFF00-100,'eax':1}])
    if a['returns']!=expected:raise ValueError('template batch all original handler/unit returns')
    required={int(row['va'],16) for row in expected_calls()}|{0x475B0A,0x46BA07,0x468D10}
    if not required<=set(a['visited']) or any(va in a['visited'] for va in (0x40A100,0x490350,0x482A30,0x4918D0,0x472370,0x430400,0x480A60)):raise ValueError('template batch original skipped animation/regen/map/post-handler')
    for key in ('owned_bodies_stubbed','next_unit_executed','VM_or_AI_completed','world_completed'):
        if a.get(key) is not False:raise ValueError('template batch bounded authority')
    retained(a);cp=case['continuation_checkpoint']
    if cp['path']!=f'.venv-audit/scene-templates-before240-{case["name"]}.pkl' or cp['pending_eip']!='0x46b760' or cp['runtime_or_original_save'] is not False:raise ValueError('template batch private path/scope')
    return True


def load_verified_checkpoint(name):
    raw=REPORT.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=REPORT_SHA:raise ValueError('template batch current report SHA before unpickle')
    case=next((c for c in json.loads(raw)['cases'] if c['name']==name),None)
    if case is None:raise ValueError('template batch private case')
    verify_case(case);cp=case['continuation_checkpoint'];raw=(ROOT/cp['path']).read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('template batch private file SHA before unpickle')
    payload=pickle.loads(raw);cpu=payload['cpu'];p=pending(240);sp=cpu.reg_read(UC_X86_REG_ESP)
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=name or payload['evidence_kind']!='private_original_scene_templates_before240':raise ValueError('template batch private source/parent/case')
    if payload['pending_eip']!=0x46B760 or cpu.reg_read(UC_X86_REG_EIP)!=0x46B760 or cpu.reg_read(UC_X86_REG_ECX)!=UNITCTRL or sp!=p['sp']:raise ValueError('template batch private actual CPU')
    if list(struct.unpack('<3I',read_memory(payload,sp,12)))!=[int(p['return_va'],16)]+p['args']:raise ValueError('template batch original next-unit stack')
    for r in case['actual']['after']:
        if read_memory(payload,r['pointer'],r['bytes']).hex()!=r['hex']:raise ValueError('template batch complete private owned memory')
    for r in case['actual']['retained_ranges']:
        if hashlib.sha256(read_memory(payload,r['pointer'],r['bytes'])).hexdigest()!=r['sha256']:raise ValueError('template batch complete private retained memory')
    return payload,cp
