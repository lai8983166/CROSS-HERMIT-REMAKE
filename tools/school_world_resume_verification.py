"""Independent full-state original countdown boundary and checkpoint proof."""
import gzip,hashlib,json,pickle,struct
from copy import deepcopy
from functools import lru_cache
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX,UC_X86_REG_ECX
from tools.school_world_resume import *
from tools.school_world_life_codec import unpack
from tools.school_world_resume_emulation import UNITCTRL,STACK,RETURN,PARENT,PARENT_SHA,TASK,PHASES,PREVIOUS
from tools.school_world_idle_verification import phase_checked as parent_phase,unit_calls,old_prefix_calls,ROOTS,effect_calls,suffix_pending,pinned,read_memory,retained
from tools import school_world_idle_verification as prior

REPORTS={p:ROOT/f'analysis/school-world-resume-{p}-v1-20261015.json.gz' for p in PHASES}
SHAS={'zero':'fe530d8d9f49384f671e0b0a655aa6e40e98abd180396a6ce91696729ad65002','pause':'bd925383e5e94023cc028e1469701a6889fd2625dea89ef274b7c4c0dbe875fa','entry':'8ddcff0897900200f6f91e593cd65853b7ae9f4da32ac19ad38e095640edfc52'}

@lru_cache(maxsize=3)
def parent_checked(name):return parent_phase(name,'wait')

@lru_cache(maxsize=9)
def phase_checked(name,phase):
    c=next(c for c in pinned(REPORTS[phase],SHAS[phase])['cases'] if c['name']==name);return c,verify_case(c,phase)

def verify_enabled_world(w,state,tick):
    w=unpack(w);r=world_project(state,tick);p=w['prefix'];u=w['units'];s=w['suffix'];base=STACK+0xFF00;work=UNITCTRL+0x80AEC
    if w['tick']!=tick or any(a['tick']!=tick for a in (p,u,s)):raise ValueError('countdown finite world order')
    if p['before']!=state['prefix_before'] or p['inputs']!=state['prefix_inputs'] or any(p[k]!=v for k,v in r['prefix'].items()):raise ValueError('countdown entire prefix/state chain')
    excluded={'0x415070','0x46b760','0x48d720','0x48e2a0','0x475700','0x4751f0','0x4697f0'}
    if p['calls']!=[c for c in old_prefix_calls(p['inputs']) if c['va'] not in excluded] or p['tested_slots']!=[0] or p['pending']!=dict(va='0x46b760',receiver=UNITCTRL,return_va='0x46b584',sp=base-100,args=[work,0],first_instruction_executed=False):raise ValueError('countdown original prefix calls/entry')
    clears=[dict(return_va='0x43d10c',args=[p['before'][7]['pointer'],0,6144]),dict(return_va='0x46f46f',args=[UNITCTRL+0x3098C,0,10]),dict(return_va='0x46b526',args=[UNITCTRL+0x2E714,0,2048])]
    if p['native_clears']!=clears or p['declared_root'] is not True or p['owned_bodies_stubbed'] is not False:raise ValueError('countdown native prefix clear/authority')
    if 0x46B760 in p['visited'] or not {0x46B470,0x499DA0,0x49A099,0x468D10,0x56CEC0}<=set(p['visited']):raise ValueError('countdown prefix natural branch boundary')
    if u['before']!=r['unit_before'] or u['inputs']!=state['unit_inputs'] or any(u[k]!=v for k,v in r['units'].items()) or u['tail_before']!=r['tail_before'] or u['tail_after']!=r['tail_before']:raise ValueError('countdown complete independent unit projection')
    calls=deepcopy(u['calls'])
    for c in calls:
        if c['va']=='0x4ddbb0':c['receiver']=None
    if calls!=unit_calls(u['inputs'],r['units']['units'],tick) or u['unit_entries']!=r['units']['unit_indices'] or u['tested_slots']!=list(range(1,250)) or u['pending']!=suffix_pending():raise ValueError('countdown original unit calls/order/loop')
    wanted=[]
    for a in r['units']['units']:
        i=a['index'];ptr=work+i*STRIDE
        if a['inactive']:values=[(0x475B0A,308,1),(0x46B7E1,196,1),(0x46BA07,100,1)]
        else:
            ret=(0x4757A3 if a['mode_after']==25 else 0x4757B7) if i in (0,1,2) else 0x475BDD if i==217 else 0x4757B7 if a['group']==0 else 0x475A42
            values=[(ret,308,0),(0x475C55,308,0 if 387<=a['job']<=406 else ptr),(0x46B7E1,196,0),(0x46B80C,196,a['main_return'])]+[(0x46B85B,196,1)]*5+[(0x46BA07,100,None)]
        wanted.extend(dict(index=i,va=hex(va),sp=base-depth,eax=eax) for va,depth,eax in values)
    actual=deepcopy(u['returns'])
    for a in actual:
        if a['va']=='0x46ba07' and a['index'] not in INACTIVE:
            if type(a['eax']) is not int or not 0<=a['eax']<=0xFFFFFFFF:raise ValueError('countdown void unit return observation')
            a['eax']=None
    if actual!=wanted:raise ValueError('countdown original all unit returns')
    required={int(c['va'],16) for c in u['calls']}|{0x46B586,0x46B59C,0x46B61B}
    events=[event for a in r['units']['units'] for n in a.get('animation_steps',[]) for event in n['events']]
    forbidden={0x40B990,0x40D4A6,0x490FC0,0x46BC20}
    bound=any(a.get('idle_bound') for a in r['units']['units'])
    mode_returns=[dict(index=a['index'],va=hex(0x475734),sp=base-308,eax=int(a.get('mode_applied',False))) for a in r['units']['units']]
    if u.get('mode_returns')!=mode_returns:raise ValueError('idle original pending commit returns')
    for a in u['units']:
        if not a['inactive'] and any(type(a[k]) is not bool for k in ('mode_applied','mode_requested','idle_bound')):raise ValueError('idle typed mode authority')
    if not bound:forbidden.add(0x46BCC0)
    if any(e['kind']=='setup' for e in events):required|={0x40A95E,0x40A97E}
    elif not bound:forbidden.add(0x40A520)
    repeat=any(e['kind']=='repeat' for e in events);free=any(a.get('released_nodes') for a in r['units']['units'])
    if repeat:required|={0x40AA71,0x40AA86,0x40AB54,0x40AB1D,0x40AB46}
    else:forbidden.add(0x40AA71)
    spawn=any(e['kind']=='spawn' for e in events)
    if spawn:required|={0x40ADA0,0x40B5E0,0x409EF0,0x40A400,0x409F70,0x4214F0,0x40A1A2}
    else:
        forbidden|={0x40ADA0,0x40B5E0,0x409EF0,0x56CEC0}
        if not bound:forbidden|={0x40A400,0x409F70,0x4214F0}
    if not any(e['kind']=='clear' for e in events):forbidden.add(0x40AB80)
    if not free:forbidden|={0x40B660,0x40B6A0}
    voices=[a['voice'] for a in r['units']['units'] if a.get('voice')]
    draws=[(a['index'],draw) for a in r['units']['units'] if a.get('voice') for draw in a['voice']['draws']]
    expected_returns=[dict(index=i,va=hex(0x467E92),sp=base-628,eax=d['value'],seed=d['after']) for i,d in draws]
    adapters=[dict(return_va=hex(0x570FE9),sp=base-644,thread_pointer=TLS,does_not_reseed=True) for _ in draws]
    if u.get('random_returns')!=expected_returns or u.get('thread_adapters')!=adapters or u.get('CRT_rand_executed') is not bool(draws):raise ValueError('handoff natural original RNG returns and declared thread adapter')
    if voices:required|={0x49AD90,0x46A4C0,0x468E10,0x467E70,0x570FE0,0x5753B0}
    else:forbidden|={0x49AD90,0x46A4C0,0x468E10,0x467E70,0x570FE0,0x5753B0}
    if any(v['selected'] for v in voices):required.add(0x40D390)
    else:forbidden.add(0x40D390)
    if not required<=set(u['visited']) or forbidden&set(u['visited']):raise ValueError('life exact source native branches')
    observations=[]
    for a in r['units']['units']:
        for n in a.get('allocated_nodes',[]):
            observations += [dict(index=a['index'],kind='allocation',va=hex(0x40ADCB),sp=base-520,eax=n),dict(index=a['index'],kind='immediate',va=hex(0x40AF2D),sp=base-520,eax=0)]
    if u.get('spawn_returns')!=observations or u.get('spawn_opcode_executed') is not spawn:raise ValueError('spawn natural allocator/immediate returns and exact authority')
    if u.get('attached_node_free_executed') is not free or ('repeat_opcode_executed' in u and u['repeat_opcode_executed'] is not repeat):raise ValueError('life native lifecycle authority')
    for k in ('owned_bodies_stubbed','audio_backend_executed'):
        if u.get(k) is not False:raise ValueError('life unit exact authority')
    if s['before']!=u['after'] or s['after']!=s['before'] or s['inputs']!=state['tail_inputs'] or s['tail_before']!=r['tail_before'] or s['tail_after']!=r['tail_after']:raise ValueError('countdown complete enabled suffix projection')
    sp=base-92;calls=[dict(va=hex(va),receiver=UNITCTRL,return_va=hex(ret),sp=sp) for va,ret in ROOTS.items()]
    calls += [dict(va='0x456b20',receiver=s['inputs']['entry_receiver'],return_va='0x48ce8b',sp=sp-88),dict(va='0x48d5d0',receiver=UNITCTRL,return_va='0x48ce99',sp=sp-88),dict(va='0x496450',receiver=UNITCTRL,return_va='0x48d5f5',sp=sp-192),dict(va='0x427de0',receiver=UNITCTRL+0x2A80,return_va='0x48d618',sp=sp-192)]
    if s['calls']!=calls or s['effect_calls']!=effect_calls(s['inputs'],True) or s['effect_returns']!=[1]*10:raise ValueError('countdown original suffix/effect calls')
    if s['real_ret']!=dict(va='0x46b662',return_va=hex(RETURN),sp=base,eax=0,original_outer_caller=False) or s['driver_return']!=dict(va=hex(RETURN),sp=base+4,ebp=base-4,expected_caller_ebp=base-4,eax=0,declared_audit_sentinel=True):raise ValueError('countdown actual complete function return CPU')
    if s['world_body_completed'] is not True:raise ValueError('countdown bounded world completion')
    for k in ('original_outer_task_frame_completed','owned_bodies_stubbed','VM_or_AI_completed','original_opening_completed'):
        if s.get(k) is not False:raise ValueError('countdown suffix exact authority')
    exe=SOURCE.read_bytes()
    for a in (p,u,s):
        retained(a)
        for c in a['calls']:
            ret=int(c['return_va'],16)
            if ret==RETURN:continue
            op=exe[ret-BASE-5:ret-BASE]
            if op[0]!=0xE8 or ret+struct.unpack_from('<i',op,1)[0]!=int(c['va'],16):raise ValueError('countdown original direct source calls')
    return r['next_state']


def paused_calls(units):
    out=[];base=STACK+0xFF00
    def add(va,recv,ret,depth,args):out.append(dict(va=hex(va),receiver=recv,return_va=hex(ret),sp=base-depth,args=args))
    for u in units:
        w=UNITCTRL+0x80AEC+u['index']*STRIDE;add(0x46B760,UNITCTRL,0x46B584,100,[w,u['index']]);add(0x469480,UNITCTRL,0x46B8D7,204,[w])
        if u['inactive']:continue
        add(0x46A430,UNITCTRL,0x46B8EB,204,[w])
        if u['group']!=0:
            add(0x46A5E0,UNITCTRL,0x46B8FB,204,[w]);add(0x46A430,UNITCTRL,0x46A63D,296,[w])
        if u['vision_args'] is not None:
            add(0x4DDBB0,None,0x46B93E,204,[w]);add(0x43D270,UNITCTRL+0x3D68,0x46B95B,212,u['vision_args'])
        add(0x46B2C0,UNITCTRL,0x46B967,204,[w])
    return out


def check_calls(parts):
    exe=SOURCE.read_bytes()
    for a in parts:
        retained(a)
        for c in a['calls']:
            ret=int(c['return_va'],16)
            if ret==RETURN:continue
            op=exe[ret-BASE-5:ret-BASE]
            if op[0]!=0xE8 or ret+struct.unpack_from('<i',op,1)[0]!=int(c['va'],16):raise ValueError('resume direct original source calls')


def verify_paused_world(raw,state):
    w=unpack(raw);r=world_project(state,183);p,u,s=w['prefix'],w['units'],w['suffix'];base=STACK+0xFF00
    if w['tick']!=183 or any(a['tick']!=183 for a in (p,u,s)):raise ValueError('resume actual paused world order')
    if p['before']!=state['prefix_before'] or p['inputs']!=state['prefix_inputs'] or any(p[k]!=v for k,v in r['prefix'].items()):raise ValueError('resume full paused prefix chain')
    excluded={'0x415070','0x46b760','0x48d720','0x48e2a0','0x475700','0x4751f0','0x4697f0'}
    pending=dict(va='0x46b760',receiver=UNITCTRL,return_va='0x46b584',sp=base-100,args=[UNITCTRL+0x80AEC,0],first_instruction_executed=False)
    clears=[dict(return_va='0x43d10c',args=[p['before'][7]['pointer'],0,6144]),dict(return_va='0x46f46f',args=[UNITCTRL+0x3098C,0,10]),dict(return_va='0x46b526',args=[UNITCTRL+0x2E714,0,2048])]
    if p['calls']!=[c for c in old_prefix_calls(p['inputs']) if c['va'] not in excluded] or p['tested_slots']!=[0] or p['pending']!=pending or p['native_clears']!=clears or p['declared_root'] is not True:raise ValueError('resume paused prefix original caller/clears')
    if not {0x49A07F,0x49A082,0x49A094}<=set(p['visited']) or {0x49A099,0x46B760}&set(p['visited']):raise ValueError('resume zero-test native branch')
    if u['before']!=r['unit_before'] or u['inputs']!=state['unit_inputs'] or any(u[k]!=v for k,v in r['units'].items()) or u['tail_before']!=r['tail_before'] or u['tail_after']!=r['tail_before']:raise ValueError('resume all paused owned bytes/frozen works')
    calls=deepcopy(u['calls'])
    for c in calls:
        if c['va']=='0x4ddbb0':c['receiver']=None
    wanted_pending=suffix_pending();wanted_pending.pop('args')
    if calls!=paused_calls(r['units']['units']) or u['unit_entries']!=r['units']['unit_indices'] or u['tested_slots']!=list(range(1,250)) or u['pending']!=wanted_pending or u['vision_calls']!=[dict(index=a['index'],args=a['vision_args']) for a in r['units']['units'] if a['vision_args'] is not None]:raise ValueError('resume paused original full loop/calls')
    if not {0x46B7A6,0x46B9ED,0x46B8CB,0x46B61B}<=set(u['visited']) or {0x475700,0x40A100,0x472370,0x430400,0x490FC0}&set(u['visited']):raise ValueError('resume paused source skip branches')
    if s['before']!=u['after'] or s['after']!=s['before'] or s['inputs']!=state['tail_inputs'] or s['tail_before']!=r['tail_before'] or s['tail_after']!=r['tail_after']:raise ValueError('resume full paused suffix')
    sp=base-92;calls=[dict(va=hex(va),receiver=UNITCTRL,return_va=hex(ret),sp=sp) for va,ret in ROOTS.items()]
    calls += [dict(va='0x456b20',receiver=s['inputs']['entry_receiver'],return_va='0x48ce8b',sp=sp-88),dict(va='0x48d5d0',receiver=UNITCTRL,return_va='0x48ce99',sp=sp-88),dict(va='0x496450',receiver=UNITCTRL,return_va='0x48d5f5',sp=sp-192),dict(va='0x427de0',receiver=UNITCTRL+0x2A80,return_va='0x48d618',sp=sp-192)]
    if s['calls']!=calls or s['effect_calls']!=effect_calls(s['inputs'],True) or s['effect_returns']!=[1]*10:raise ValueError('resume paused suffix original calls')
    if s['real_ret']!=dict(va='0x46b662',return_va=hex(RETURN),sp=base,eax=0,original_outer_caller=False) or s['driver_return']!=dict(va=hex(RETURN),sp=base+4,ebp=base-4,expected_caller_ebp=base-4,eax=0,declared_audit_sentinel=True) or s['world_body_completed'] is not True:raise ValueError('resume paused complete natural return')
    for part in (p,u,s):
        if part.get('owned_bodies_stubbed') is not False:raise ValueError('resume no owned stubs')
    for k in ('original_outer_task_frame_completed','VM_or_AI_completed','original_opening_completed'):
        if s.get(k) is not False:raise ValueError('resume bounded suffix authority')
    check_calls((p,u,s));return r['next_state']

def verify_entry(raw,state):
    a=unpack(raw);base=STACK+0xFF00;expected=preflight_boundary(a['inputs'],state['prefix_before'])
    if a['tick']!=184 or a['before']!=state['prefix_before'] or any(a[k]!=v for k,v in expected.items()):raise ValueError('resume complete actual184 prefix')
    calls=[dict(va='0x46b470',receiver=UNITCTRL,return_va=hex(RETURN),sp=base,declared_root=True),dict(va='0x4678c0',receiver=UNITCTRL,return_va='0x46b4b2',sp=base-92),dict(va='0x499da0',receiver=UNITCTRL,return_va='0x46b4c8',sp=base-92),dict(va='0x456b20',receiver=a['inputs']['entry_receiver'],return_va='0x49a0be',sp=base-204,args=[])]
    pending=dict(va='0x4551c0',receiver=a['inputs']['entry_receiver'],return_va='0x49a0d4',sp=base-212,args=[0,1],first_instruction_executed=False)
    if a['calls']!=calls or a['pending']!=pending or a['declared_root'] is not True or a['owned_bodies_stubbed'] is not False or a['world_body_completed'] is not False:raise ValueError('resume actual preflight entry/caller/authority')
    if not {0x46B48D,0x499DA0,0x49A0B0,0x456B20,0x456B3F,0x456B4F,0x49A0BE,0x49A0C2}<=set(a['visited']) or {0x4551C0,0x49A114,0x493630,0x46B760}&set(a['visited']):raise ValueError('resume actual busy-zero native branch')
    check_calls((a,));return state


def verify_case(c,phase):
    if phase not in PHASES:raise ValueError('resume finite phase')
    parent,state=parent_checked(c['name'])
    if c['parent_checkpoint']!=parent['continuation_checkpoint']:raise ValueError('resume exact181 parent')
    if phase in PREVIOUS:
        previous,state=phase_checked(c['name'],PREVIOUS[phase])
        if c['prior_checkpoint']!=previous['continuation_checkpoint']:raise ValueError('resume previous checkpoint chain')
    if phase=='zero':state=verify_enabled_world(c['actual'],state,182)
    elif phase=='pause':state=verify_paused_world(c['actual'],state)
    else:state=verify_entry(c['actual'],state)
    cp=c['continuation_checkpoint'];eip=0x4551C0 if phase=='entry' else RETURN
    if cp['path']!=f'.venv-audit/world-resume-{phase}-{c["name"]}.pkl' or cp['pending_eip']!=hex(eip) or cp['runtime_or_original_save'] is not False:raise ValueError('resume fixed checkpoint path/boundary')
    return state


def fresh_identities(phase):
    identities=[(SOURCE,SOURCE_SHA256),(SCRIPT,SCRIPT_SHA),(PARENT,PARENT_SHA),(prior.PARENT_INPUTS,prior.PARENT_INPUTS_SHA),(prior.THIRD_REPORT,prior.THIRD_SHA)]
    for reports,shas in ((prior.REPORTS,prior.SHAS),(prior.PARENT_REPORTS,prior.PARENT_SHAS),(prior.SPAWN_REPORTS,prior.SPAWN_SHAS),(prior.LIFE_REPORTS,prior.LIFE_SHAS),(prior.FRAME_REPORTS,prior.FRAME_SHAS),(prior.COUNT_REPORTS,prior.COUNT_SHAS)):
        identities.extend((p,shas[k]) for k,p in reports.items())
    while True:
        identities.append((REPORTS[phase],SHAS[phase]))
        if phase not in PREVIOUS:break
        phase=PREVIOUS[phase]
    for path,sha in identities:
        if sha is None or hashlib.sha256(path.read_bytes()).hexdigest()!=sha:raise ValueError('resume fresh source/ancestor/report SHA before unpickle')


def load_verified_checkpoint(name,phase='entry'):
    if phase not in PHASES:raise ValueError('resume finite checkpoint phase')
    fresh_identities(phase)
    report=pinned(REPORTS[phase],SHAS[phase]);c=next((c for c in report['cases'] if c['name']==name),None)
    if c is None:raise ValueError('resume known private case')
    if report['source_contract']!=source_contract() or report['parent_report']!=PARENT.relative_to(ROOT).as_posix() or report['parent_sha256']!=PARENT_SHA:raise ValueError('resume source/parent report envelope')
    state=verify_case(c,phase);cp=c['continuation_checkpoint'];raw=(ROOT/cp['path']).read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('resume fixed private bytes/SHA before unpickle')
    payload=pickle.loads(raw);cpu=payload['cpu'];base=STACK+0xFF00;eip=0x4551C0 if phase=='entry' else RETURN
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=name or payload['phase']!=phase or payload['evidence_kind']!='private_original_world_resume_'+phase or payload['pending_eip']!=eip:raise ValueError('resume private source/parent/case/phase')
    wanted=(eip,base-212,base-96,UNITCTRL) if phase=='entry' else (eip,base+4,base-4,0)
    if tuple(cpu.reg_read(reg) for reg in (UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX))!=wanted:raise ValueError('resume exact private native CPU')
    if phase=='entry':
        a=unpack(c['actual']);pending=a['pending']
        if cpu.reg_read(UC_X86_REG_ECX)!=pending['receiver'] or read_memory(payload,base-212,12)!=struct.pack('<3I',0x49A0D4,0,1):raise ValueError('resume private actual preflight stack')
        pointer=a['inputs']['script_pointer']
        if read_memory(payload,pointer,SCRIPT.stat().st_size)!=SCRIPT.read_bytes():raise ValueError('resume private full source script bytes')
    else:a=unpack(c['actual'])['suffix']
    for r in state['prefix_before']+state['unit_before']+state['tail_before']:
        if read_memory(payload,r['pointer'],r['bytes']).hex()!=r['hex']:raise ValueError('resume private complete owned bytes')
    if read_memory(payload,TASK+0x1A98,20).hex()!=state['unit_inputs']['audio_manager_hex']:raise ValueError('resume private retained audio bytes')
    for r in a['retained_ranges']:
        if hashlib.sha256(read_memory(payload,r['pointer'],r['bytes'])).hexdigest()!=r['sha256']:raise ValueError('resume private complete retained memory')
    return payload,cp
