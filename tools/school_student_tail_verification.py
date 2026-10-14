"""Independent first-unit return, restored probes and trusted next-unit state."""
import hashlib,json,pickle,struct
from copy import deepcopy
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP
from tools.school_student_tail import *
from tools.school_student_tail_emulation import ROOT,UNITCTRL,TACT,STACK,PARENT,PARENT_SHA,MAPCTRL
from tools.school_student_action_verification import pinned,verify_case as verify_student
from tools.school_student_action_emulation import PARENT as WORLD_PARENT,PARENT_SHA as WORLD_SHA
from tools.school_world_mode_emulation import architectural_cpu,cpu_digest

REPORT=ROOT/'analysis/school-student-tail-native-v2-20261015.json'
REPORT_SHA='e6d66cf9386c9d2222aefeb716047b06f43eb3612769931a27e70d9f549fd6ce'


def pending():
    return {'va':'0x46b760','receiver':UNITCTRL,'return_va':'0x46b584','sp':STACK+0xFF00-100,
      'args':[UNITCTRL+0x80AEC+STRIDE,1],'first_instruction_executed':False}


def retained(row):
    ranges=row['retained_ranges']
    if row['retained_ranges_unchanged'] is not True or row['retained_bytes']!=sum(r['bytes'] for r in ranges) or row['retained_bytes']<100000000:raise ValueError('tail complete retained memory')
    for r in ranges:
        if r['bytes']<=0 or len(r['sha256'])!=64:raise ValueError('tail retained range identity')


def restored(row):
    if row['register_count']!=50 or row['complete_owned_input_restored'] is not True:raise ValueError('tail complete restoration')
    for kind in ('cpu','stack'):
        a,b=row[kind+'_before_sha256'],row[kind+'_after_sha256']
        if len(a)!=64 or a!=b:raise ValueError('tail restored '+kind)


def expected_calls():
    w=UNITCTRL+0x80AEC;sp=STACK+0xFF00
    specs=[(0x482A30,UNITCTRL,0x46B86D,208,[w,0]),(0x4918D0,UNITCTRL,0x46B87D,208,[w,0]),
      (0x493450,UNITCTRL,0x46B889,204,[w]),(0x472370,UNITCTRL,0x46B895,204,[w]),
      (0x472770,UNITCTRL,0x46B8BF,204,[w]),(0x430400,UNITCTRL,0x46B8CB,204,[w]),
      (0x43BB90,MAPCTRL,0x430485,324,[10,17]),(0x4305C0,UNITCTRL,0x4304A4,324,[w,0]),
      (0x4DDBB0,None,0x46B93E,204,[w]),(0x43D270,MAPCTRL,0x46B95B,212,[10,17,9]),
      (0x46B2C0,UNITCTRL,0x46B967,204,[w])]
    return [{'va':hex(va),'receiver':recv,'return_va':hex(ret),'sp':sp-depth,'args':args} for va,recv,ret,depth,args in specs]


def verify_case(case):
    parent=next((r for r in pinned(PARENT,PARENT_SHA)['cases'] if r['name']==case['name']),None)
    if parent is None or case['parent_checkpoint']!=parent['continuation_checkpoint']:raise ValueError('tail actual parent checkpoint')
    verify_student(parent,'animation');a=case['actual_tail'];b=a['before'];pa=parent['actual'];w=UNITCTRL+0x80AEC
    world=next(r for r in pinned(WORLD_PARENT,WORLD_SHA)['cases'] if r['name']==case['name'])['actual_second_prefix']['after']
    for i,j in ((0,0),(6,1),(7,2),(8,3),(9,4)):
        if b[i]!=pa['after'][j]:raise ValueError('tail exact parent work/pool/control/task/pointer')
    if b[1]['pointer']!=pa['inputs']['record_pointer'] or b[1]['hex']!=pa['inputs']['record_hex']:raise ValueError('tail unchanged complete source record')
    for i,j in ((2,15),(3,7),(4,5),(5,17)):
        if any(b[i][k]!=world[j][k] for k in ('pointer','bytes','hex')):raise ValueError('tail original region/fog/occupancy provenance')
    inputs=a['inputs']
    if inputs!={'team':0,'map_sha256':source_contract()['map_source']['sha256'],'map_header_pointer':0xE745190,'map_all_bytes_verified':36880}:raise ValueError('tail complete original map identity')
    expected=project(inputs,b)
    if any(a[k]!=v for k,v in expected.items()):raise ValueError('tail complete independent byte projection')
    calls=deepcopy(a['calls'])
    if len(calls)!=11:raise ValueError('tail exact natural calls')
    calls[8]['receiver']=None # Original cdecl view helper has no ECX receiver contract.
    if calls!=expected_calls():raise ValueError('tail original typed calls/stack')
    controllers=[w+0x48]+[w+0xA0+i*88 for i in range(5)]
    for key,first,aux in (('effect_scans','0x482a64','0x482a9d'),('damage_scans','0x491904','0x49193d')):
        wanted=[{'args':[w,0,p],'return_va':first if i==0 else aux,'sp':STACK+0xFF00-312} for i,p in enumerate(controllers)]
        if a[key]!=wanted:raise ValueError('tail all six original scans')
    if a['native_heals'] or a['actual_heals'] or a['next_tests']!=[1] or a['pending']!=pending():raise ValueError('tail actual no heal/next slot boundary')
    ret=deepcopy(a['real_ret']);eax=ret.pop('eax')
    if not isinstance(eax,int) or not 0<=eax<=0xFFFFFFFF or ret!={'va':'0x46ba07','sp':STACK+0xFF00-100,'return_va':'0x46b584'} or a['returned']!={'va':'0x46b584','sp':STACK+0xFF00-88}:raise ValueError('tail natural ret8/returned stack')
    required={0x482A30,0x482AC0,0x4918D0,0x491960,0x493450,0x472370,0x472770,0x430400,0x43BB90,0x4305C0,0x4DDBB0,0x43D270,0x46B2C0,0x468D10,0x46BA07,0x46B584}
    if not required<=set(a['visited']) or any(v in a['visited'] for v in (0x46B760,0x472550,0x46BC20,0x43C470,0x496E70)):raise ValueError('tail required actual bodies/unexecuted next unit')
    for k in ('next_unit_executed','nonempty_effect_or_damage_executed','world_or_VM_or_AI_completed','owned_bodies_stubbed'):
        if a.get(k) is not False:raise ValueError('tail exact completion scope')
    retained(a);probes=case['declared_probes'];restored(probes['final_restoration'])
    if probes['live_input_captured'] is not False or [r['declared'] for r in probes['rows']]!=PROBES:raise ValueError('tail isolated declared probes')
    for row in probes['rows']:
        d=row['declared'];before=deepcopy(a['after']);record=bytearray.fromhex(before[1]['hex']);work=bytearray.fromhex(before[0]['hex'])
        record[15]=d['state'];put(record,0x16,get(record,0x14)-d['hp_gap']);put(record,0x1C,get(record,0x1A)-d['mp_gap'])
        put(work,0x504,d['hp_counter']);put(work,0x506,d['mp_counter']);before[0]['hex']=work.hex();before[1]['hex']=record.hex()
        if row['before']!=before:raise ValueError('tail probe exact declared input')
        result=regen(work[:STRIDE],record);after=deepcopy(before);after[0]['hex']=result['work_hex']+work[STRIDE:].hex();after[1]['hex']=result['record_hex']
        heals=[{'args':[w,kind,amount],'return_va':'0x47246b' if kind==0 else '0x47253b','sp':STACK+0xFF00-104} for kind,amount in result['heals']]
        if row['after']!=after or row['heals']!=heals:raise ValueError('tail independent full original recovery probe')
        wanted={0x472370}|({0x469220} if d['hp_gap'] or d['mp_gap'] else set())|({0x472550} if result['heals'] else set())
        if not wanted<=set(row['visited']) or (not result['heals'] and 0x472550 in row['visited']):raise ValueError('tail actual recovery helper visits')
        retained(row);restored(row['restoration'])
        if row['restoration']!=probes['final_restoration']:raise ValueError('tail all probes restore same actual continuation')
    cp=case['continuation_checkpoint']
    if cp['path']!=f'.venv-audit/student-tail-before-slot1-{case["name"]}.pkl' or cp['pending_eip']!='0x46b760' or cp['runtime_or_original_save'] is not False:raise ValueError('tail private next-unit scope')
    return True


def load_verified_checkpoint(name):
    raw=REPORT.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=REPORT_SHA:raise ValueError('tail current immutable report SHA before unpickle')
    report=json.loads(raw);case=next((r for r in report['cases'] if r['name']==name),None)
    if case is None:raise ValueError('tail private case identity')
    verify_case(case);cp=case['continuation_checkpoint'];raw=(ROOT/cp['path']).read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('tail private file SHA before unpickle')
    payload=pickle.loads(raw);cpu=payload['cpu'];p=pending();sp=cpu.reg_read(UC_X86_REG_ESP)
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=name or payload['evidence_kind']!='private_actual_first_student_returned_before_slot1':raise ValueError('tail private source/parent/case')
    if payload['pending_eip']!=0x46B760 or cpu.reg_read(UC_X86_REG_EIP)!=0x46B760 or cpu.reg_read(UC_X86_REG_ECX)!=UNITCTRL or sp!=p['sp']:raise ValueError('tail private actual CPU')
    def read(at,n):
        for start,buf in payload['memory']:
            if start<=at and at+n<=start+len(buf):return buf[at-start:at-start+n]
        raise ValueError('tail missing private memory')
    if list(struct.unpack('<3I',read(sp,12)))!=[int(p['return_va'],16)]+p['args']:raise ValueError('tail original next-unit stack')
    for r in case['actual_tail']['after']:
        if read(r['pointer'],r['bytes']).hex()!=r['hex']:raise ValueError('tail all private owned bytes')
    restoration=case['declared_probes']['final_restoration']
    # UcContext.reg_read exposes scalar FP/descriptor fields, unlike Uc.reg_read.
    # Restore the context and compare the live architectural API used by probes.
    live=Uc(UC_ARCH_X86,UC_MODE_32);live.context_restore(cpu)
    if cpu_digest(architectural_cpu(live))!=restoration['cpu_after_sha256'] or hashlib.sha256(read(STACK,65536)).hexdigest()!=restoration['stack_after_sha256']:raise ValueError('tail restored live CPU/full stack identity')
    return payload,cp
