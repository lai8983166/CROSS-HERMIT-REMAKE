"""Full owned/retained state and original call/CPU proof for world184 scripts."""
import gzip,hashlib,json,pickle,struct
from copy import deepcopy
from functools import lru_cache
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX,UC_X86_REG_ECX
from tools.school_world_script import *
from tools.school_world_script_inputs import checked_parent,INPUTS,INPUTS_SHA
from tools.school_world_script_emulation import PHASES,PREVIOUS,PARENT,PARENT_SHA,STACK,RETURN,UNITCTRL,ENTRIES,SCRIPT_NATIVE
from tools.school_world_life_codec import unpack
from tools.school_world_resume_verification import fresh_identities as parent_identities,read_memory,pinned,retained,paused_calls,old_prefix_calls,ROOTS,effect_calls,suffix_pending,check_calls

REPORTS={p:ROOT/f'analysis/school-world-script-{p}-v1-20261016.json.gz' for p in PHASES}
SHAS={'preflight':'670b12fcacef2480f4c16c95c815939ab733c9147cf592dd0490b1c23245a167','binding':None,'world184':None,'world185':None}

@lru_cache(maxsize=16)
def phase_checked(name,phase):
    c=next(c for c in pinned(REPORTS[phase],SHAS[phase])['cases'] if c['name']==name);return c,verify_case(c,phase)

@lru_cache(maxsize=1)
def abi():
    raw=SOURCE.read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_32);out={};cdecl={0x42B2D0:1,0x496D80:1,0x496DF0:1,0x42FC60:1,0x42FBE0:1,0x56CEC0:3}
    for va in ENTRIES:
        if va==0x56CEC0:out[va]=dict(end=0x56CF18,frame=0,args=3);continue
        seq=list(md.disasm(raw[va-BASE:va-BASE+16384],va));ret=next(i for i in seq if i.mnemonic=='ret');prefix=seq[:12];local=next(i for i in prefix if i.mnemonic=='sub' and i.op_str.startswith('esp, '))
        if seq[0].mnemonic!='push' or seq[0].op_str!='ebp':raise ValueError('world script source function prologue')
        count=int(ret.op_str,0)//4 if ret.op_str else cdecl.get(va,0)
        out[va]=dict(end=ret.address+ret.size,frame=4+int(local.op_str.split(', ')[1],0)+12,args=count)
    return out


def verify_calls(a,phase):
    calls=a['calls'];protocol=call_protocol(phase);raw=SOURCE.read_bytes();base=STACK+0xFF00;rules=abi();active=[]
    if [int(c['return_va'],16) for c in calls]!=protocol:raise ValueError('world script exact source call protocol')
    for index,c in enumerate(calls):
        va=int(c['va'],16);ret=int(c['return_va'],16);op=raw[ret-BASE-5:ret-BASE]
        if va not in rules or op[0]!=0xE8 or ret+struct.unpack_from('<i',op,1)[0]!=va:raise ValueError('world script direct original call bytes')
        if not index:wanted=base-(212 if phase=='preflight' else 232)
        else:
            owner=next((p for p,r in rules.items() if p<=ret-5<r['end']),None)
            while active and active[-1][0]!=owner:active.pop()
            if not active:raise ValueError('world script natural source parent stack')
            wanted=active[-1][1]-rules[owner]['frame']-rules[va]['args']*4-4
        if c['sp']!=wanted or type(c['receiver']) is not int or not 0<=c['receiver']<=0xFFFFFFFF:raise ValueError('world script native ABI depth/receiver')
        if va in (0x4551C0,0x455060,0x4549D0) and c['receiver']!=TACT:raise ValueError('world script original task receiver')
        if va in (0x4CE460,0x4CE4B0,0x4CE090,0x4CD8D0,0x4CE560,0x4CD700,0x4CE030,0x4CE8F0,0x4D0790,0x4CE060) and c['receiver']!=VM:raise ValueError('world script original VM receiver')
        if va==0x41E500 and c['receiver']!=MUSIC or va==0x40D120 and c['receiver']!=AUDIO:raise ValueError('world script native guarded audio receiver')
        active.append((va,c['sp']))


def verify_script(a,state,phase):
    a=unpack(a);inputs=state['inputs'];before=state['script'];expected=(preflight_project if phase=='preflight' else binding_project)(inputs,before);base=STACK+0xFF00
    if a['phase']!=phase or a['inputs']!=inputs or a['before']!=before or any(a[k]!=v for k,v in expected.items()):raise ValueError('world script all independent owned bytes and result')
    verify_calls(a,phase)
    pointer=inputs['script_pointer'];script=SCRIPT.read_bytes();exe=SOURCE.read_bytes();left=script[432:].split(bytes(1),1)[0];right=exe[0x59A60C-BASE:].split(bytes(1),1)[0];difference=next((x-y for x,y in zip(left+bytes(1),right+bytes(1)) if x!=y),0)&0xFFFFFFFF
    adapters=[]
    if phase=='preflight':adapters=[dict(va=hex(inputs['strcmp_import']),receiver=pointer+432,return_va='0x45521c',sp=base-324,args=[pointer+432,0x59A60C],result=difference),dict(va=hex(inputs['tick_import']),receiver=VM,return_va='0x45528d',sp=base-316,args=[],result=0)]
    if a['adapters']!=adapters:raise ValueError('world script exact declared platform adapters')
    pending=dict(va='0x49a0d4' if phase=='preflight' else '0x49a0f4',sp=base-200,ebp=base-96,eax=1 if phase=='preflight' else 0,ecx=WORK if phase=='preflight' else TACT,first_instruction_executed=False)
    if a['pending']!=pending or a['owned_bodies_stubbed'] is not False or a['debug_stack_check_is_declared_adapter'] is not True or a['audio_backend_executed'] is not False:raise ValueError('world script original return/authority')
    required={int(c['va'],16) for c in a['calls']};forbidden={0x4D29E0,0x49A146,0x41E53E,0x40D150}
    if phase=='preflight':required|={0x41E520,0x41E527,0x41D7B0,0x40D146};forbidden.add(0x49A0D4)
    else:
        required|={0x49A0D4,0x454A63};forbidden.add(0x49A0F4)
        if a.get('binding_observation')!=dict(receiver=TACT,return_va='0x49a0f4',sp=base-232,args=[0,0,1,0,1,1,0]):raise ValueError('world script original seven binding arguments')
    if not required<=set(a['visited']) or forbidden&set(a['visited']):raise ValueError('world script native cleanup/selected branches')
    retained(a)
    return dict(world=merge_script_state(state['world'],expected['after']),script=expected['after'],inputs=inputs)


def verify_world(raw,state,tick):
    outer=state;state=state['world']
    w=unpack(raw);r=world_project(state,tick);p,u,s=w['prefix'],w['units'],w['suffix'];base=STACK+0xFF00
    if w['tick']!=tick or any(a['tick']!=tick for a in (p,u,s)):raise ValueError('resume actual paused world order')
    if p['before']!=state['prefix_before'] or p['inputs']!=state['prefix_inputs'] or any(p[k]!=v for k,v in r['prefix'].items()):raise ValueError('resume full paused prefix chain')
    excluded={'0x415070','0x46b760','0x48d720','0x48e2a0','0x475700','0x4751f0','0x4697f0'}
    if tick==184:excluded|={'0x46b470','0x4678c0','0x499da0'}
    pending=dict(va='0x46b760',receiver=UNITCTRL,return_va='0x46b584',sp=base-100,args=[UNITCTRL+0x80AEC,0],first_instruction_executed=False)
    clears=[dict(return_va='0x43d10c',args=[p['before'][7]['pointer'],0,6144]),dict(return_va='0x46f46f',args=[UNITCTRL+0x3098C,0,10]),dict(return_va='0x46b526',args=[UNITCTRL+0x2E714,0,2048])]
    if p['calls']!=[c for c in old_prefix_calls(p['inputs']) if c['va'] not in excluded] or p['tested_slots']!=[0] or p['pending']!=pending or p['native_clears']!=clears or p['declared_root'] is not (tick==185):raise ValueError('resume paused prefix original caller/clears')
    required={0x49A146,0x49A151,0x493630} if tick==184 else {0x499DA0,0x49A159,0x49A162,0x454C40,0x49A167}
    forbidden={0x49A159,0x46B760} if tick==184 else {0x49A146,0x46B760}
    if not required<=set(p['visited']) or forbidden&set(p['visited']):raise ValueError('world script native controller7 branch')
    status=[] if tick==184 else [dict(va='0x454c40',receiver=TACT,return_va='0x49a167',sp=base-204,args=[])]
    if p['status_calls']!=status or p['status_result']!=(None if tick==184 else 1):raise ValueError('world script original status1 query')
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
    check_calls((p,u,s));return dict(world=r['next_state'],script=merge_ranges(outer['script'],p['after']+u['after']+s['tail_after']),inputs=outer['inputs'])


def verify_case(c,phase):
    parent,world,seed=checked_parent(c['name']);state=dict(world=world,script=seed['before'],inputs=seed['inputs'])
    if c['parent_checkpoint']!=parent['continuation_checkpoint']:raise ValueError('world script preceding184 checkpoint')
    if phase in PREVIOUS:
        previous,state=phase_checked(c['name'],PREVIOUS[phase])
        if c['prior_checkpoint']!=previous['continuation_checkpoint']:raise ValueError('world script original phase provenance')
    if phase in ('preflight','binding'):state=verify_script(c['actual'],state,phase)
    else:state=verify_world(c['actual'],state,184 if phase=='world184' else 185)
    cp=c['continuation_checkpoint'];eip={'preflight':0x49A0D4,'binding':0x49A0F4,'world184':RETURN,'world185':RETURN}[phase]
    if cp['path']!=f'.venv-audit/world-script-{phase}-{c["name"]}.pkl' or cp['pending_eip']!=hex(eip) or cp['runtime_or_original_save'] is not False:raise ValueError('world script fixed private phase path')
    return state


def fresh_identities(phase):
    parent_identities('entry')
    if hashlib.sha256(INPUTS.read_bytes()).hexdigest()!=INPUTS_SHA:raise ValueError('world script fresh source inputs before unpickle')
    while True:
        if phase not in REPORTS or SHAS[phase] is None or hashlib.sha256(REPORTS[phase].read_bytes()).hexdigest()!=SHAS[phase]:raise ValueError('world script fresh phase SHA before unpickle')
        if phase not in PREVIOUS:break
        phase=PREVIOUS[phase]


def load_verified_checkpoint(name,phase):
    fresh_identities(phase);report=pinned(REPORTS[phase],SHAS[phase]);c=next((c for c in report['cases'] if c['name']==name),None)
    if c is None:raise ValueError('world script known checkpoint case')
    if report['source_contract']!=source_contract() or report['parent_report']!=PARENT.relative_to(ROOT).as_posix() or report['parent_sha256']!=PARENT_SHA:raise ValueError('world script source/parent envelope')
    state=verify_case(c,phase);cp=c['continuation_checkpoint'];raw=(ROOT/cp['path']).read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('world script fixed file SHA before unpickle')
    payload=pickle.loads(raw);cpu=payload['cpu'];a=unpack(c['actual']);base=STACK+0xFF00
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=name or payload['phase']!=phase or payload['evidence_kind']!='private_original_world_script_'+phase or hex(payload['pending_eip'])!=cp['pending_eip']:raise ValueError('world script private identity')
    if phase in ('preflight','binding'):wanted=(int(a['pending']['va'],16),a['pending']['sp'],a['pending']['ebp'],a['pending']['eax'],a['pending']['ecx'])
    else:wanted=(RETURN,base+4,base-4,0,None);a=a['suffix']
    observed=tuple(cpu.reg_read(reg) for reg in (UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX,UC_X86_REG_ECX))
    if observed[:4]!=wanted[:4] or wanted[4] is not None and observed[4]!=wanted[4]:raise ValueError('world script exact private CPU')
    for r in state['script']+state['world']['prefix_before']+state['world']['unit_before']+state['world']['tail_before']:
        if read_memory(payload,r['pointer'],r['bytes']).hex()!=r['hex']:raise ValueError('world script complete private owned memory')
    for r in a['retained_ranges']:
        if hashlib.sha256(read_memory(payload,r['pointer'],r['bytes'])).hexdigest()!=r['sha256']:raise ValueError('world script entire private retained memory')
    return payload,cp
