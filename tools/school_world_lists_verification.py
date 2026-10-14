"""Independent list/mask/stack evidence and trusted private checkpoint loading."""
import hashlib,json,pickle,struct
from tools.school_world_lists import project,source_contract,viewport
from tools.school_world_lists_emulation import ROOT,PARENT,PARENT_SHA,VIEW_PROBES,SORT_PROBES
from tools.school_deployment_tail_emulation import UNITCTRL,STACK,CHECKPOINTS
from tools.school_entry_control_emulation import MAPCTRL
from tools.tactics_exit_emulation import SOURCE_SHA256,report_text
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP

REPORT=ROOT/'analysis/school-world-lists-native-v1-20261014.json'
REPORT_SHA='a53782f2d596964181721cf81c837773a3eb378242667a1031f6c818f7400bbd'


def verify_case(case):
    if case.get('checkpoint_sha256')!=dict(CHECKPOINTS).get(case.get('name')) or case.get('complete_parent_equality') is not True:raise ValueError('list actual-school provenance')
    a=case['actual_list_suffix'];expected=project(a['inputs'],a['before'])
    if a['after']!=expected['after'] or any(a[k]!=expected[k] for k in ('display_indices','category_counts','occupied_slots','display_state1_slots')):
        raise ValueError('list complete independent source projection')
    if a['before'][0]['pointer']!=UNITCTRL+0x2F150 or a['before'][3]['pointer']!=UNITCTRL+0xDC30C or a['before'][4]['pointer']!=UNITCTRL+0xDC8EC:raise ValueError('list owned output identity')
    for r in a['inputs']['works']:
        if r['pointer']!=UNITCTRL+0x80AEC+r['index']*0x520:raise ValueError('list exact work pointer')
    sp=STACK+0xFF00-92
    calls=[{'va':'0x49b180','receiver':UNITCTRL,'return_va':'0x46b4e8','sp':sp},
       {'va':'0x43d270','receiver':MAPCTRL,'return_va':'0x49ba3e','args':a['inputs']['origin']+[a['inputs']['view']]},
       {'va':'0x46e520','receiver':UNITCTRL,'return_va':'0x46b4f0','sp':sp},
       {'va':'0x46e730','receiver':UNITCTRL,'return_va':'0x46b4f8','sp':sp}]
    if a['calls']!=calls or a['pending']!={'va':'0x48cd90','receiver':UNITCTRL,'return_va':'0x46b500','sp':sp,'first_instruction_executed':False}:raise ValueError('list natural caller/queue boundary')
    for k in ('full_world_tick_executed','AI_or_waves_executed','predicates_stubbed'):
        if a.get(k) is not False:raise ValueError('list original body/scope')
    if not a['retained_ranges_unchanged'] or a['retained_bytes']<100000000:raise ValueError('list retained full work/record and other memory')
    masks=source_contract()['masks']
    if len(a['mask_bindings'])!=33:raise ValueError('list complete mask binding')
    for native,source in zip(a['mask_bindings'],masks):
        if native['view']!=source['view'] or native['bytes']!=source['payload_bytes'] or native['sha256']!=source['sha256']:raise ValueError('list mask source bytes')
    probes=case['declared_probes']
    if probes['live_input_captured'] is not False or [r['declared_xy'] for r in probes['viewport']]!=[list(p) for p in VIEW_PROBES] or [r['declared_depths'] for r in probes['sorting']]!=SORT_PROBES:raise ValueError('list finite declared probe matrix')
    for row in probes['viewport']:
        if row['return_eax']!=int(viewport(*row['declared_xy'])):raise ValueError('original viewport short boundary')
    for row in probes['sorting']:
        p=project(row['inputs'],row['before'])
        if row['after']!=p['after'] or row['display_indices']!=p['display_indices'] or row['category_counts']!=p['category_counts']:raise ValueError('original sorting complete projection')
        chosen=row['selected_indices']
        for i,y in zip(chosen,row['declared_depths']):
            r=row['inputs']['works'][i]
            if r['x_fixed']!=100<<16 or r['y_fixed']!=y or bytes.fromhex(r['record_hex'])[15]!=1:raise ValueError('list declared chosen geometry')
        if any(bytes.fromhex(r['record_hex'])[15]!=0 for r in row['inputs']['works'] if r['used_word'] and r['index'] not in chosen):raise ValueError('list explicitly hidden other records')
        if not row['retained_ranges_unchanged'] or row['retained_bytes']<100000000:raise ValueError('list probe retention')
    for row in [p['restoration'] for p in probes['sorting']]+[probes['final_restoration']]:
        if row['register_count']!=50 or row['complete_owned_input_restored'] is not True:raise ValueError('list whole checkpoint restoration scope')
        for k in ('cpu','stack'):
            if len(row[k+'_before_sha256'])!=64 or row[k+'_before_sha256']!=row[k+'_after_sha256']:raise ValueError('list CPU/stack restoration')
    if probes['retained_ranges_unchanged'] is not True:raise ValueError('list complete probe retained memory')
    return True


def load_verified_checkpoint(name):
    """Only private bytes pinned by our immutable verified report may unpickle."""
    report_raw=REPORT.read_bytes()
    if hashlib.sha256(report_raw).hexdigest()!=REPORT_SHA:raise ValueError('list checkpoint report identity')
    data=json.loads(report_raw)
    if name not in dict(CHECKPOINTS):raise ValueError('list checkpoint case name')
    case=next(c for c in data['cases'] if c['name']==name);verify_case(case)
    cp=case['continuation_checkpoint'];path=ROOT/f'.venv-audit/world-lists-before-queue-{name}.pkl'
    if cp['path']!=path.relative_to(ROOT).as_posix():raise ValueError('list checkpoint exact private path')
    raw=path.read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('list private checkpoint identity before unpickle')
    payload=pickle.loads(raw)
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=name or payload['evidence_kind']!='private_actual_school_after_verified_lists_before_queue':raise ValueError('list checkpoint provenance')
    if payload['pending_eip']!=0x48CD90 or payload['cpu'].reg_read(UC_X86_REG_EIP)!=0x48CD90:raise ValueError('list checkpoint exact pending CPU')
    parent_raw=PARENT.read_bytes()
    if hashlib.sha256(parent_raw).hexdigest()!=PARENT_SHA:raise ValueError('list checkpoint parent report identity')
    parent=next(c for c in json.loads(parent_raw)['cases'] if c['name']==name)
    if payload['parent_case_sha']!=cp['parent_case_sha256'] or cp['parent_case_sha256']!=hashlib.sha256(report_text(parent).encode('utf-8')).hexdigest():raise ValueError('list checkpoint exact parent-case equality')
    def read(at,n):
        for start,buf in payload['memory']:
            if start<=at and at+n<=start+len(buf):return buf[at-start:at-start+n]
        raise ValueError('list checkpoint missing owned range')
    for row in case['actual_list_suffix']['after']:
        if read(row['pointer'],row['bytes']).hex()!=row['hex']:raise ValueError('list checkpoint complete owned byte equality')
    sp=payload['cpu'].reg_read(UC_X86_REG_ESP)
    if sp!=STACK+0xFF00-92 or struct.unpack('<I',read(sp,4))[0]!=0x46B500:raise ValueError('list checkpoint natural return stack')
    return payload,cp
