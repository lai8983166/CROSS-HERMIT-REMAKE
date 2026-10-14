"""Independent full paused suffix verification and trusted continuation loading."""
import hashlib,json,pickle,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_ECX
from tools.school_world_command import project,normalize_selection,STRIDE
from tools.school_world_command_emulation import ROOT,UNITCTRL,MAPCTRL,STACK,PARENT,PARENT_SHA,PROBES
from tools.tactics_exit_emulation import SOURCE_SHA256

REPORT=ROOT/'analysis/school-world-command-native-v1-20261014.json'
REPORT_SHA='7bfecbc6d729269e596b0c6b9d3d223a5e24f1f2dd62df87e2c398f642338112'


def pinned_parent():
    raw=PARENT.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=PARENT_SHA:raise ValueError('command parent identity')
    return json.loads(raw)


def verify_case(case):
    parent=next((r for r in pinned_parent()['cases'] if r['name']==case['name']),None)
    if parent is None or case['parent_checkpoint']!=parent['continuation_checkpoint']:raise ValueError('command exact checkpoint provenance')
    a=case['actual_suffix'];inputs=a['inputs'];p=project(inputs,a['before'])
    for k in ('after','occupied_indices','active_indices','selected_indices','selection_kind','vision_calls','cell_changes'):
        if a[k]!=p[k]:raise ValueError('command full source projection '+k)
    prev=parent['actual_list_suffix'];records=[r['record_hex'] for r in prev['inputs']['works']]
    if inputs['record_hex']!=records or inputs['team']!=prev['inputs']['team'] or inputs['relations']!=prev['inputs']['relation_hex'] or inputs['work_base']!=UNITCTRL+0x80AEC:raise ValueError('command source records/group unchanged')
    pointers=[UNITCTRL+0x1798,UNITCTRL+0x80AEC,UNITCTRL+0x108B50,UNITCTRL+0x3098C,UNITCTRL+0x2E714,
       prev['after'][1]['pointer'],prev['after'][2]['pointer'],a['before'][7]['pointer'],0x7A49E0]
    if [r['pointer'] for r in a['before']]!=pointers:raise ValueError('command exact owned pointers')
    for n in (5,6):
        if a['before'][n]['hex']!=prev['after'][n-4]['hex']:raise ValueError('command full parent fog bytes')
    works=bytes.fromhex(a['before'][1]['hex'])
    for r in prev['inputs']['works']:
        at=r['index']*STRIDE
        if struct.unpack_from('<h',works,at)[0]!=r['used_word'] or struct.unpack_from('<I',works,at+0x258)[0]!=r['record_pointer'] or list(struct.unpack_from('<2i',works,at+0x2EC))!=[r['x_fixed'],r['y_fixed']]:raise ValueError('command actual work source equality')
    sp=STACK+0xFF00-92
    calls=[{'va':'0x48cd90','receiver':UNITCTRL,'return_va':'0x46b500','sp':sp},
      {'va':'0x427de0','receiver':UNITCTRL+0x1798,'return_va':'0x48cdc8','sp':sp-100},
      {'va':'0x46ea10','receiver':UNITCTRL,'return_va':'0x46b508','sp':sp},
      {'va':'0x46f440','receiver':UNITCTRL,'return_va':'0x46b510','sp':sp}]
    if a['calls']!=calls or a['pending']!={'va':'0x490fc0','receiver':UNITCTRL,'return_va':'0x46b620','sp':sp,'first_instruction_executed':False}:raise ValueError('command natural stack/call/boundary')
    if a['tested_indices']!=list(range(250)) or a['updated_indices']!=p['occupied_indices'] or a['native_vision_calls']!=p['vision_calls']:raise ValueError('command complete original loop')
    cells=[{'index':r['index'],'args':v} for r in p['cell_changes'] for v in r['calls']]
    if a['native_cell_calls']!=cells or a['native_clears']!=[{'return_va':'0x46f46f','args':[UNITCTRL+0x3098C,0,10]}, {'return_va':'0x46b526','args':[UNITCTRL+0x2E714,0,2048]}]:raise ValueError('command original cells/clears')
    required={0x48CD90,0x427DE0,0x46EA10,0x493670,0x4945B0,0x4947B0,0x494620,0x494690,0x4128F0,0x46F170,0x4690A0,0x46F440,0x46B760,0x46B2C0,0x4DDBB0,0x43D270,0x56CEC0,0x46B586}
    if not required<=set(a['visited']) or any(v in a['visited'] for v in (0x40A100,0x46BC20,0x48DCD0)):raise ValueError('command original bodies/skipped branch')
    for k in ('full_world_tick_executed','action_animation_AI_executed','nonempty_queue_consumed','input_injected','owned_bodies_stubbed'):
        if a.get(k) is not False:raise ValueError('command scope authority')
    if a['retained_ranges_unchanged'] is not True or a['retained_bytes']<100000000:raise ValueError('command complete retained memory')
    probes=case['declared_probes']
    if probes['live_input_captured'] is not False or [r['declared_indices'] for r in probes['selection']]!=[list(r) for r in PROBES]:raise ValueError('command finite declared selection probes')
    for row in probes['selection']:
        if row['inputs']!=inputs:raise ValueError('command declared probe input identity')
        before=deepcopy(a['after']);buf=bytearray.fromhex(before[1]['hex'])
        for i in p['occupied_indices']:buf[i*STRIDE+0x28C]=int(i in row['declared_indices'])
        before[1]['hex']=buf.hex()
        if row['before']!=before:raise ValueError('command declared exact selection byte binding')
        wanted=deepcopy(before);works,selected,kind=normalize_selection(buf,[bytes.fromhex(r) if r else None for r in records],inputs['team']);wanted[1]['hex']=works.hex()
        selection=bytearray.fromhex(wanted[2]['hex']);struct.pack_into('<2I',selection,0,len(selected),kind)
        for n,i in enumerate(selected):struct.pack_into('<I',selection,16+n*4,UNITCTRL+0x80AEC+i*STRIDE)
        wanted[2]['hex']=selection.hex()
        if row['after']!=wanted or row['selected_indices']!=selected or row['selection_kind']!=kind:raise ValueError('command complete declared selection projection')
        if row['retained_ranges_unchanged'] is not True or row['retained_bytes']<100000000:raise ValueError('command probe retained memory')
    for row in [r['restoration'] for r in probes['selection']]+[probes['final_restoration']]:
        if row['register_count']!=50 or row['complete_owned_input_restored'] is not True:raise ValueError('command whole probe restoration')
        for k in ('cpu','stack'):
            if len(row[k+'_before_sha256'])!=64 or row[k+'_before_sha256']!=row[k+'_after_sha256']:raise ValueError('command restored CPU/stack')
    return True


def load_verified_checkpoint(name):
    raw=REPORT.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=REPORT_SHA:raise ValueError('command report identity')
    cases=json.loads(raw)['cases'];case=next((r for r in cases if r['name']==name),None)
    if case is None:raise ValueError('command checkpoint case')
    verify_case(case);cp=case['continuation_checkpoint'];path=ROOT/f'.venv-audit/world-command-before-effects-{name}.pkl'
    if cp['path']!=path.relative_to(ROOT).as_posix():raise ValueError('command exact checkpoint path')
    raw=path.read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('command private identity before unpickle')
    payload=pickle.loads(raw)
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=name or payload['evidence_kind']!='private_actual_school_after_paused_unit_loop':raise ValueError('command checkpoint provenance')
    cpu=payload['cpu'];sp=cpu.reg_read(UC_X86_REG_ESP)
    if payload['pending_eip']!=0x490FC0 or cpu.reg_read(UC_X86_REG_EIP)!=0x490FC0 or cpu.reg_read(UC_X86_REG_ECX)!=UNITCTRL or sp!=STACK+0xFF00-92:raise ValueError('command natural pending CPU')
    def read(at,n):
        for start,data in payload['memory']:
            if start<=at and at+n<=start+len(data):return data[at-start:at-start+n]
        raise ValueError('command checkpoint mapped memory')
    if struct.unpack('<I',read(sp,4))[0]!=0x46B620:raise ValueError('command natural pending return')
    for r in case['actual_suffix']['after']:
        if read(r['pointer'],r['bytes']).hex()!=r['hex']:raise ValueError('command checkpoint full byte equality')
    return payload,cp
