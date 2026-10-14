"""Independent current student byte projections, source bindings and boundaries."""
import hashlib,json,pickle,struct
from functools import lru_cache
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP
from tools.school_student_action_emulation import ROOT,UNITCTRL,TACT,STACK,PARENT,PARENT_SHA,REPORTS,PHASE_SHAS,PHASES
from tools.school_student_action import *
from tools.school_world_second_verification import verify_case as verify_parent


@lru_cache(maxsize=8)
def pinned(path,sha):
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('student immutable report identity')
    return json.loads(raw)


def boundary(phase,inputs):
    w=inputs['work_pointer'];main=inputs['main_controller'];effect=inputs['effect_controller']
    return {'binding':{'va':'0x465140','receiver':main,'return_va':'0x46be97','sp':STACK+0xFF00-548,'args':[w+0x48,effect,2063,0,0,7],'first_instruction_executed':False},
      'initializer':{'va':'0x40a100','receiver':main,'return_va':'0x46b80c','sp':STACK+0xFF00-204,'args':[w+0x48],'first_instruction_executed':False},
      'animation':{'va':'0x482a30','receiver':UNITCTRL,'return_va':'0x46b86d','sp':STACK+0xFF00-208,'args':[w,0],'first_instruction_executed':False}}[phase]


def verify_case(case,phase):
    parent=next((r for r in pinned(PARENT,PARENT_SHA)['cases'] if r['name']==case['name']),None)
    if parent is None or case['parent_checkpoint']!=parent['continuation_checkpoint']:raise ValueError('student actual checkpoint provenance')
    verify_parent(parent);a=case['actual'];inputs=a['inputs'];baseline=a['initial_before'];s=source_contract()
    if inputs['work_pointer']!=UNITCTRL+0x80AEC or baseline[0]!=parent['actual_second_prefix']['after'][12] or baseline[2]!=parent['actual_second_prefix']['after'][1] or baseline[3]!=parent['actual_second_prefix']['after'][0] or baseline[4]!=parent['actual_second_prefix']['after'][18] or baseline[1]['pointer']!=POOL:raise ValueError('student complete parent work/control/task/pool identities')
    record=parent['actual_second_prefix']['inputs']['lists']['works'][0]
    if inputs['record_hex']!=record['record_hex'] or inputs['record_pointer']!=record['record_pointer']:raise ValueError('student unchanged actual source record')
    for b,p,resource in zip(inputs['metadata_bindings'],[s['main'],s['attachments'][0]],[s['main_source'],s['effect_source']]):
        owner=bytes.fromhex(b['controller_hex'])
        if len(owner)!=84 or u32(owner,0)!=b['metadata_pointer'] or b['metadata_bytes']!=p['metadata_bytes'] or b['metadata_sha256']!=p['metadata_sha256'] or b['source_sha256']!=resource['sha256']:raise ValueError('student full source metadata identity')
    if inputs['main_controller']!=inputs['metadata_bindings'][0]['owner'] or inputs['effect_controller']!=inputs['metadata_bindings'][1]['owner'] or inputs['attachment_program_pointers']!=[inputs['metadata_bindings'][1]['metadata_pointer']+p['offset'] for p in s['attachments']]:raise ValueError('student source owners/attached program pointers')
    expected={'binding':lambda:{'after':bind_project(inputs,baseline)},'initializer':lambda:initialized_project(inputs,baseline),'animation':lambda:animated_project(inputs,baseline)}[phase]()
    if a['phase']!=phase or any(a[k]!=v for k,v in expected.items()):raise ValueError('student complete independent '+phase+' projection')
    priors=list(PHASES[:PHASES.index(phase)])
    if case['replayed_prior_phases_equal']!=priors:raise ValueError('student complete actual prior-phase replay scope')
    previous=baseline
    if priors:
        prev=next(r for r in pinned(REPORTS[priors[-1]],PHASE_SHAS[priors[-1]])['cases'] if r['name']==case['name'])
        if prev['actual']['inputs']!=inputs or prev['actual']['initial_before']!=baseline:raise ValueError('student prior exact captured input')
        previous=prev['actual']['after']
    if a['before']!=previous or a['pending']!=boundary(phase,inputs):raise ValueError('student phase before/natural pending stack')
    calls=a['calls'];required={'binding':{0x475D60,0x46C040,0x46BCC0,0x465040,0x409FF0,0x40A400,0x40A520,0x468EB0,0x46BE50},
      'initializer':{0x465140,0x40AF40,0x40B5E0,0x409EF0,0x40A400,0x40A520,0x40A800,0x47A8E0,0x480A60,0x490350,0x490A50},
      'animation':{0x40A100,0x40A800}}[phase]
    if not required<={int(r['va'],16) for r in calls} or not required<=set(a['visited']):raise ValueError('student original required bodies')
    if phase=='binding':
        if a['native_clears'] or a['returns']:raise ValueError('student binding prematurely updates pool/returns')
        maincalls=[r for r in calls if r['va']=='0x409ff0']
        if len(maincalls)!=1 or maincalls[0]['args']!=[inputs['work_pointer']+0x48,0,89,0]:raise ValueError('student original pose program call')
    if phase=='initializer':
        nodes=expected['allocated_nodes'];clears=[{'return_va':'0x409f1a','args':[p,0,88]} for p in nodes]
        if a['native_clears']!=clears or len([r for r in calls if r['va']=='0x40b5e0'])!=2:raise ValueError('student original first-free nodes/clears')
        if [r['args'][0] for r in calls if r['va']=='0x40a800']!=nodes:raise ValueError('student immediate attached original steps')
        if [r['args'] for r in calls if r['va']=='0x490a50']!=[[n,inputs['work_pointer'],0] for n in range(3)]:raise ValueError('student original empty status slots')
        if [(r['va'],r['eax']) for r in a['returns']]!=[('0x4757a3',0),('0x46b7e1',0)]:raise ValueError('student initializer/status original returns')
    if phase=='animation':
        w=inputs['work_pointer'];anim=[r for r in calls if r['va']=='0x40a100'];steps=[r['args'][0] for r in calls if r['va']=='0x40a800']
        if [r['args'] for r in anim]!=[[w+0x48]]+[[w+0xA0+i*NODE] for i in range(5)] or steps!=[w+0x48]+expected['linked_order']:raise ValueError('student all original main/linked/auxiliary updates')
        if [(r['va'],r['eax']) for r in a['returns']]!=[('0x46b80c',0)]+[('0x46b85b',1)]*5 or a['native_clears']:raise ValueError('student original distinct animation returns')
    if a['source_metadata_all_bytes_verified'] is not True or a['retained_ranges_unchanged'] is not True or a['retained_bytes']<100000000:raise ValueError('student source/retained memory')
    for k in ('owned_bodies_stubbed','GPU_rendering_executed','full_unit_or_world_completed','VM_or_AI_completed'):
        if a.get(k) is not False:raise ValueError('student exact scope/authority')
    return True


def load_verified_checkpoint(name,phase='animation'):
    if phase not in ('initializer','animation'):raise ValueError('student private phase')
    report=pinned(REPORTS[phase],PHASE_SHAS[phase]);case=next((r for r in report['cases'] if r['name']==name),None)
    if case is None:raise ValueError('student private case')
    verify_case(case,phase);cp=case['continuation_checkpoint'];path=ROOT/f'.venv-audit/student-action-{phase}-{name}.pkl'
    if cp['path']!=path.relative_to(ROOT).as_posix():raise ValueError('student exact private file path')
    raw=path.read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('student private file SHA before unpickle')
    payload=pickle.loads(raw);cpu=payload['cpu'];pending=case['actual']['pending'];sp=cpu.reg_read(UC_X86_REG_ESP)
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=name or payload['phase']!=phase or payload['evidence_kind']!='private_actual_student_action_'+phase:raise ValueError('student private provenance')
    if payload['pending_eip']!=int(pending['va'],16) or cpu.reg_read(UC_X86_REG_EIP)!=payload['pending_eip'] or cpu.reg_read(UC_X86_REG_ECX)!=pending['receiver'] or sp!=pending['sp']:raise ValueError('student exact pending CPU')
    def read(at,n):
        for start,buf in payload['memory']:
            if start<=at and at+n<=start+len(buf):return buf[at-start:at-start+n]
        raise ValueError('student missing private memory')
    words=list(struct.unpack('<'+'I'*(len(pending['args'])+1),read(sp,(len(pending['args'])+1)*4)))
    if words!=[int(pending['return_va'],16)]+pending['args']:raise ValueError('student original private return/argument stack')
    for r in case['actual']['after']:
        if read(r['pointer'],r['bytes']).hex()!=r['hex']:raise ValueError('student entire private owned memory')
    return payload,cp
