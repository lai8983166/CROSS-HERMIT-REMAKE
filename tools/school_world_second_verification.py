"""Independent full second-world prefix and trusted student checkpoint verifier."""
import hashlib,json,pickle,struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP
from tools.school_world_second_emulation import ROOT,UNITCTRL,TACT,MAPCTRL,STACK,RETURN,PARENT,PARENT_SHA,ROOT_RETURNS
from tools.school_world_second import source_contract,project
from tools.school_world_tail_verification import verify_case as verify_tail
from tools.school_world_command_verification import REPORT as COMMAND_PARENT,REPORT_SHA as COMMAND_SHA
from tools.tactics_exit_emulation import SOURCE,SOURCE_SHA256,BASE,TASK

REPORT=ROOT/'analysis/school-world-second-native-v1-20261014.json'
REPORT_SHA='0c4d56fc839cbaff6c0b14e93f178e877d786ac725b52572dc0bc344fa9f66f1'


def pinned(path,sha):
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('second pinned report identity')
    return json.loads(raw)


def expected_calls(inputs):
    # Derive stack depths from original debug-build prologues, not output rows.
    raw=SOURCE.read_bytes();source_contract();md=Cs(CS_ARCH_X86,CS_MODE_32)
    def frame(va):
        code=list(md.disasm(raw[va-BASE:va-BASE+11],va))
        if [i.mnemonic for i in code[:6]]!=['push','mov','sub','push','push','push'] or code[0].op_str!='ebp' or code[2].op_str.split(',')[0]!='esp':raise ValueError('second original frame prologue')
        return int(code[2].op_str.split(',')[1].strip(),0)+16
    world=frame(0x46B470);unit=frame(0x46B760);dispatch=frame(0x475700);root_sp=STACK+0xFF00;inner=root_sp-world-4;work=UNITCTRL+0x80AEC
    out=[{'va':'0x46b470','receiver':UNITCTRL,'return_va':hex(RETURN),'sp':root_sp,'declared_root':True}]
    for va,ret in ROOT_RETURNS.items():
        sp=inner;args=None
        if va==0x46B760:sp=root_sp-world-12;args=[work,0]
        if va in (0x48D720,0x48E2A0,0x475700):
            args=[work,0] if va==0x48D720 else [work];sp=root_sp-world-12-unit-4-len(args)*4
        if va in (0x4751F0,0x4697F0):args=[work];sp=root_sp-world-12-unit-8-dispatch-8
        row={'va':hex(va),'receiver':UNITCTRL,'return_va':hex(ret),'sp':sp}
        if args is not None:row['args']=args
        out.append(row)
        if va==0x499DA0:out.append({'va':'0x415070','receiver':TASK,'return_va':'0x49a068','sp':inner-frame(0x499DA0)-8,'args':[180]})
        if va==0x49B180:out.append({'va':'0x43d270','receiver':MAPCTRL,'return_va':'0x49ba3e','sp':inner-frame(0x49B180)-4-frame(0x49B9F0)-16,'args':[9,16,0]})
        if va==0x48CD90:out.append({'va':'0x427de0','receiver':UNITCTRL+0x1798,'return_va':'0x48cdc8','sp':inner-frame(0x48CD90)-4})
    return out


def verify_case(case):
    parent=next((r for r in pinned(PARENT,PARENT_SHA)['cases'] if r['name']==case['name']),None)
    if parent is None or case['parent_checkpoint']!=parent['parent_checkpoint'] or case['complete_actual_tail_equality'] is not True:raise ValueError('second full actual tail/checkpoint provenance')
    verify_tail(parent)
    command=next(r for r in pinned(COMMAND_PARENT,COMMAND_SHA)['cases'] if r['name']==case['name'])
    a=case['actual_second_prefix'];p=project(a['inputs'],a['before'])
    for k,v in p.items():
        if a[k]!=v:raise ValueError('second full independent projection '+k)
    before=a['before'];cmd=command['actual_suffix']['after'];tail=parent['actual_tail']['after']
    for i,j in ((12,1),(13,2),(14,3),(15,4),(16,0),(17,7),(18,8)):
        if before[i]!=cmd[j]:raise ValueError('second exact first-world complete owned bytes')
    if before[1]['hex']!=tail[5]['hex'] or before[9]!=tail[1] or before[0]['pointer']!=TACT or before[1]['pointer']!=UNITCTRL+0x108B30 or before[2]['pointer']!=UNITCTRL+0x2E6F4:raise ValueError('second first-tail task/control/window provenance')
    if before[5]['hex']!=cmd[6]['hex'] or before[6]['hex']!=cmd[5]['hex'] or before[5]['pointer']!=cmd[6]['pointer'] or before[6]['pointer']!=cmd[5]['pointer']:raise ValueError('second first-world fog parent equality')
    inputs=a['inputs'];works=bytes.fromhex(before[12]['hex'])
    for row,rec in zip(inputs['lists']['works'],command['actual_suffix']['inputs']['record_hex']):
        i=row['index'];at=i*0x520
        if row['pointer']!=UNITCTRL+0x80AEC+at or row['record_hex']!=rec or struct.unpack_from('<h',works,at)[0]!=row['used_word'] or list(struct.unpack_from('<2i',works,at+0x2EC))!=[row['x_fixed'],row['y_fixed']]:raise ValueError('second full current work/record provenance')
    if a['calls']!=expected_calls(inputs):raise ValueError('second exact source-derived natural calls/stack')
    if a['pending']!={'va':'0x475d60','receiver':UNITCTRL,'return_va':'0x4757a3','sp':STACK+0xFF00-316,'args':[UNITCTRL+0x80AEC],'first_instruction_executed':False}:raise ValueError('second student pending original stack')
    if a['native_tested_indices']!=[0] or a['native_clears']!=[{'return_va':'0x43d10c','args':[before[7]['pointer'],0,6144]}, {'return_va':'0x46f46f','args':[UNITCTRL+0x3098C,0,10]}, {'return_va':'0x46b526','args':[UNITCTRL+0x2E714,0,2048]}]:raise ValueError('second original first test/complete native clears')
    required=set(ROOT_RETURNS)|{0x415070,0x43D270,0x56CEC0,0x468D10,0x493670,0x494690,0x46F170}
    if not required<=set(a['visited']) or any(va in a['visited'] for va in (0x475D60,0x40A100,0x46BC20,0x4CE8F0)):raise ValueError('second original body/exact unexecuted boundary')
    for k in ('root_call_declared','controller_in_original_world_order'):
        if a.get(k) is not True:raise ValueError('second declared driver/natural nested provenance')
    for k in ('second_world_body_completed','student_handler_executed','active_animation_executed','180_enabled_world_updates_executed','VM_or_AI_completed','owned_bodies_stubbed'):
        if a.get(k) is not False:raise ValueError('second scope/authority')
    if a['retained_ranges_unchanged'] is not True or a['retained_bytes']<100000000:raise ValueError('second whole retained memory')
    return True


def load_verified_checkpoint(name):
    raw=REPORT.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=REPORT_SHA:raise ValueError('second checkpoint report identity')
    case=next((r for r in json.loads(raw)['cases'] if r['name']==name),None)
    if case is None:raise ValueError('second checkpoint case identity')
    verify_case(case);cp=case['continuation_checkpoint'];path=ROOT/f'.venv-audit/world-second-before-student-{name}.pkl'
    if cp['path']!=path.relative_to(ROOT).as_posix():raise ValueError('second exact private checkpoint path')
    raw=path.read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('second checkpoint file SHA before unpickle')
    payload=pickle.loads(raw)
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=name or payload['evidence_kind']!='private_actual_second_world_before_student_handler':raise ValueError('second private checkpoint provenance')
    cpu=payload['cpu'];sp=cpu.reg_read(UC_X86_REG_ESP)
    if payload['pending_eip']!=0x475D60 or cpu.reg_read(UC_X86_REG_EIP)!=0x475D60 or cpu.reg_read(UC_X86_REG_ECX)!=UNITCTRL or sp!=STACK+0xFF00-316:raise ValueError('second exact pending CPU')
    def read(at,n):
        for start,buf in payload['memory']:
            if start<=at and at+n<=start+len(buf):return buf[at-start:at-start+n]
        raise ValueError('second missing private memory range')
    if struct.unpack('<2I',read(sp,8))!=(0x4757A3,UNITCTRL+0x80AEC):raise ValueError('second natural original return/work stack')
    for row in case['actual_second_prefix']['after']:
        if read(row['pointer'],row['bytes']).hex()!=row['hex']:raise ValueError('second checkpoint complete owned byte equality')
    return payload,cp
