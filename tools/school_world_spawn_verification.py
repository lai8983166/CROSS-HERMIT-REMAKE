"""Independent original opcode1 spawn, pool reuse and complete world continuation proof."""
import gzip,hashlib,json,pickle,struct
from copy import deepcopy
from functools import lru_cache
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX
from tools.school_world_spawn import *
from tools.school_world_life_codec import unpack
from tools.school_world_spawn_emulation import UNITCTRL,STACK,RETURN,PARENT,PARENT_SHA,TASK,PHASES,PREVIOUS
from tools.school_world_life_verification import verify_case as verify_parent, REPORTS as PARENT_REPORTS, SHAS as PARENT_SHAS
from tools.school_world_frames_verification import REPORTS as FRAME_REPORTS, SHAS as FRAME_SHAS
from tools.school_world_countdown_verification import INPUTS as PARENT_INPUTS, INPUTS_SHA as PARENT_INPUTS_SHA, PARENT as THIRD_REPORT, PARENT_SHA as THIRD_SHA, REPORTS as COUNT_REPORTS, SHAS as COUNT_SHAS
from tools.school_following_students_verification import read_memory
from tools.school_student_tail_verification import retained
from tools.school_world_second_verification import expected_calls as old_prefix_calls
from tools.school_world_tail_emulation import ROOTS
from tools.school_world_tail_verification import effect_calls
from tools.school_world_final_verification import pending as suffix_pending

REPORTS={p:ROOT/f'analysis/school-world-spawn-{p}-v1-20261015.json.gz' for p in PHASES}
SHAS={'frames': 'd75d1d17f49ebf3c21372ac4d1e07e6b6dda8ad5e48c6009c3c533c328a1dc25', 'spawn': None, 'tail': None}


@lru_cache(maxsize=8)
def pinned(path,sha):
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('countdown fixed source/report SHA')
    return json.loads(gzip.decompress(raw) if path.suffix=='.gz' else raw)


@lru_cache(maxsize=3)
def parent_checked(name):
    c=next(c for c in pinned(PARENT,PARENT_SHA)['cases'] if c['name']==name);return c,verify_parent(c,'release')


@lru_cache(maxsize=6)
def phase_checked(name,phase):
    c=next(c for c in pinned(REPORTS[phase],SHAS[phase])['cases'] if c['name']==name);return c,verify_case(c,phase)


def unit_calls(inputs,units,tick):
    out=[];mapctrl=UNITCTRL+0x3D68
    def add(va,recv,ret,depth,args):out.append(dict(va=hex(va),receiver=recv,return_va=hex(ret),sp=STACK+0xFF00-depth,args=args))
    def frame_calls(u,owner,node):
        item=next((a for a in u['animation_steps'] if a['node']==node),None)
        for event in item['events'] if item else []:
            if event['kind']=='clear':
                add(0x40AB80,owner,0x40A845,424,[node])
                if event['depth']:
                    add(0x40B660,owner,0x40AC6C,524,[node]);add(0x40B6A0,owner,0x40B689,616,[node])
            elif event['kind']=='setup':
                frame=event['frame'];add(0x40A520,owner,int(event['return_va'],16),424,[node])
                if frame['opcode']==0:
                    add(0x415070,TASK,0x40A5C1,576,[frame['duration']])
                    if frame['sprite']<4095 and item['kind']!='spawned':add(0x409FB0,owner,0x40A763,580,[node,frame['sprite']])
                elif frame['opcode'] not in (1,3):raise ValueError('life unsupported native setup opcode')
            elif event['kind']=='spawn':
                child=event['node'];meta=x['bindings'][0]['metadata_pointer'];instruction=meta+event['instruction']['offset'];table=u32(bytes.fromhex(x['bindings'][0]['controller_hex']),16)
                if event['immediate_events'] or event['immediate_return']!=0:raise ValueError('spawn actual initial child step scope')
                add(0x40ADA0,owner,0x40A9C1,428,[node,instruction]);add(0x40B5E0,owner,0x40ADCB,524,[]);add(0x409EF0,owner,0x40B63E,620,[child]);add(0x56CEC0,owner,0x409F1A,720,[child,0,88])
                add(0x40A400,owner,0x40AF21,536,[child,3,1]);add(0x409F70,owner,0x40A42D,636,[child,3]);add(0x4214F0,owner,0x40A4F0,636,[table,1]);add(0x40A520,owner,0x40A502,632,[child]);add(0x415070,TASK,0x40A5C1,784,[event['program']['duration']]);add(0x40A800,owner,0x40AF2D,528,[child])
            elif event['kind']!='repeat':raise ValueError('life unsupported native event')
    for x,u in zip(inputs['units'],units):
        i=u['index'];w=UNITCTRL+0x80AEC+i*STRIDE
        for va,ret,depth,args in ((0x46B760,0x46B584,100,[w,i]),(0x48D720,0x46B7C9,208,[w,i]),(0x48E2A0,0x46B7D5,204,[w]),(0x475700,0x46B7E1,204,[w]),(0x4751F0,0x475734,316,[w]),(0x4697F0,0x475740,316,[w])):add(va,UNITCTRL,ret,depth,args)
        va,ret=(0x479F40,0x475B0A) if u['inactive'] else (0x475D60,0x4757A3) if i in (0,1,2) else (0x4761C0,0x475BDD) if i==217 else (0x476250,0x4757B7 if u['group']==0 else 0x475A42)
        add(va,UNITCTRL,ret,316,[w])
        if u['inactive']:continue
        owner=x['bindings'][0]['owner']
        if 387<=u['job']<=406:add(0x480A60,UNITCTRL,0x475C55,316,[w])
        add(0x490350,UNITCTRL,0x46B7FA,208,[w,i])
        for n,r in enumerate((0x49037F,0x490391,0x4903A3)):add(0x490A50,UNITCTRL,r,308,[n,w,i])
        add(0x40A100,owner,0x46B80C,204,[w+0x48])
        if not u['root_idle']:add(0x40A800,owner,0x40A165,308,[w+0x48]);frame_calls(u,owner,w+0x48)
        for p in u['linked_order']:
            add(0x40A800,owner,0x40A1B0,308,[p])
            frame_calls(u,owner,p)
        for n in range(5):add(0x40A100,inputs['effect_controller'],0x46B85B,204,[w+0xA0+n*NODE])
        for va,ret,child,first,aux in ((0x482A30,0x46B86D,0x482AC0,0x482A64,0x482A9D),(0x4918D0,0x46B87D,0x491960,0x491904,0x49193D)):
            add(va,UNITCTRL,ret,208,[w,i])
            for n,p in enumerate([w+0x48]+[w+0xA0+k*NODE for k in range(5)]):add(child,UNITCTRL,first if n==0 else aux,312,[w,i,p])
        for va,ret in ((0x493450,0x46B889),(0x472370,0x46B895),(0x472770,0x46B8BF),(0x430400,0x46B8CB)):add(va,UNITCTRL,ret,204,[w])
        add(0x43BB90,mapctrl,0x430485,324,u['cell'])
        if u['event_region']<32:add(0x4305C0,UNITCTRL,0x4304A4,324,[w,u['event_region']])
        add(0x46A430,UNITCTRL,0x46B8EB,204,[w])
        if u['group']!=inputs['team']:
            add(0x46A5E0,UNITCTRL,0x46B8FB,204,[w]);add(0x46A430,UNITCTRL,0x46A63D,296,[w])
        if u['vision_args'] is not None:
            add(0x4DDBB0,None,0x46B93E,204,[w]);add(0x43D270,mapctrl,0x46B95B,212,u['vision_args'])
        add(0x46B2C0,UNITCTRL,0x46B967,204,[w])
    return out


def verify_world(w,state,tick):
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
            ret=0x4757A3 if i in (0,1,2) else 0x475BDD if i==217 else 0x4757B7 if a['group']==0 else 0x475A42
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
    forbidden={0x40B990,0x40D390,0x40D4A6,0x490FC0,0x46BCC0,0x46BC20}
    if any(e['kind']=='setup' for e in events):required|={0x40A95E,0x40A97E}
    else:forbidden.add(0x40A520)
    repeat=any(e['kind']=='repeat' for e in events);free=any(a.get('released_nodes') for a in r['units']['units'])
    if repeat:required|={0x40AA71,0x40AA86,0x40AB54,0x40AB1D,0x40AB46}
    else:forbidden.add(0x40AA71)
    spawn=any(e['kind']=='spawn' for e in events)
    if spawn:required|={0x40ADA0,0x40B5E0,0x409EF0,0x40A400,0x409F70,0x4214F0,0x40A1A2}
    else:forbidden|={0x40ADA0,0x40B5E0,0x409EF0,0x40A400,0x409F70,0x4214F0,0x56CEC0}
    if not any(e['kind']=='clear' for e in events):forbidden.add(0x40AB80)
    if not free:forbidden|={0x40B660,0x40B6A0}
    if not required<=set(u['visited']) or forbidden&set(u['visited']):raise ValueError('life exact source native branches')
    observations=[]
    for a in r['units']['units']:
        for n in a.get('allocated_nodes',[]):
            observations += [dict(index=a['index'],kind='allocation',va=hex(0x40ADCB),sp=base-520,eax=n),dict(index=a['index'],kind='immediate',va=hex(0x40AF2D),sp=base-520,eax=0)]
    if u.get('spawn_returns')!=observations or u.get('spawn_opcode_executed') is not spawn:raise ValueError('spawn natural allocator/immediate returns and exact authority')
    if u.get('attached_node_free_executed') is not free or ('repeat_opcode_executed' in u and u['repeat_opcode_executed'] is not repeat):raise ValueError('life native lifecycle authority')
    for k in ('owned_bodies_stubbed','audio_backend_executed'):
        if u.get(k) is not False:raise ValueError('life unit exact authority')
    if s['before']!=u['after'] or s['after']!=s['before'] or s['tail_inputs']!=state['tail_inputs'] or s['inputs']!=state['tail_inputs'] or s['tail_before']!=r['tail_before'] or s['tail_after']!=r['tail_after']:raise ValueError('countdown complete enabled suffix projection')
    sp=base-92;calls=[dict(va=hex(va),receiver=UNITCTRL,return_va=hex(ret),sp=sp) for va,ret in ROOTS.items()]
    calls += [dict(va='0x456b20',receiver=s['inputs']['entry_receiver'],return_va='0x48ce8b',sp=sp-88),dict(va='0x48d5d0',receiver=UNITCTRL,return_va='0x48ce99',sp=sp-88),dict(va='0x496450',receiver=UNITCTRL,return_va='0x48d5f5',sp=sp-192),dict(va='0x427de0',receiver=UNITCTRL+0x2A80,return_va='0x48d618',sp=sp-192)]
    if s['calls']!=calls or s['effect_calls']!=effect_calls(s['inputs'],True) or s['effect_returns']!=[1]*10:raise ValueError('countdown original suffix/effect calls')
    if s['real_ret']!=dict(va='0x46b662',return_va=hex(RETURN),sp=base,eax=0,original_outer_caller=False) or s['driver_return']!=dict(va=hex(RETURN),sp=base+4,ebp=base-4,expected_caller_ebp=base-4,eax=0,declared_audit_sentinel=True):raise ValueError('countdown actual complete function return CPU')
    if s['world_body_completed'] is not True:raise ValueError('countdown bounded world completion')
    for k in ('original_outer_task_frame_completed','owned_bodies_stubbed','VM_or_AI_completed','original_opening_completed','180_enabled_updates_completed'):
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


def verify_case(c,phase):
    if phase not in PHASES:raise ValueError('life exact phase')
    parent,state=parent_checked(c['name'])
    if c['parent_checkpoint']!=parent['continuation_checkpoint']:raise ValueError('life exact fifteenth-return parent')
    if phase in PREVIOUS:
        prev,state=phase_checked(c['name'],PREVIOUS[phase])
        if c['prior_checkpoint']!=prev['continuation_checkpoint']:raise ValueError('life actual prior returned provenance')
    if [w['tick'] for w in c['worlds']]!=list(PHASES[phase]):raise ValueError('life no skipped world invocations')
    for w in c['worlds']:state=verify_world(w,state,w['tick'])
    cp=c['continuation_checkpoint']
    if cp['path']!=f'.venv-audit/world-spawn-{phase}-{c["name"]}.pkl' or cp['pending_eip']!=hex(RETURN) or cp['runtime_or_original_save'] is not False:raise ValueError('life private phase/path/scope')
    return state


def load_verified_checkpoint(name,phase='tail'):
    if phase not in REPORTS or SHAS[phase] is None:raise ValueError('countdown pinned phase required')
    identities=[(REPORTS[phase],SHAS[phase]),(PARENT_INPUTS,PARENT_INPUTS_SHA),(THIRD_REPORT,THIRD_SHA)]
    identities += [(path,PARENT_SHAS[key]) for key,path in PARENT_REPORTS.items()]+[(path,FRAME_SHAS[key]) for key,path in FRAME_REPORTS.items()]+[(path,COUNT_SHAS[key]) for key,path in COUNT_REPORTS.items()]
    prior=phase
    while prior in PREVIOUS:
        prior=PREVIOUS[prior];identities.append((REPORTS[prior],SHAS[prior]))
    for path,sha in identities:
        if hashlib.sha256(path.read_bytes()).hexdigest()!=sha:raise ValueError('countdown fresh current SHA before unpickle')
    c=next((r for r in pinned(REPORTS[phase],SHAS[phase])['cases'] if r['name']==name),None)
    if c is None:raise ValueError('countdown private case')
    state=verify_case(c,phase);cp=c['continuation_checkpoint'];raw=(ROOT/cp['path']).read_bytes()
    if len(raw)!=cp['bytes'] or hashlib.sha256(raw).hexdigest()!=cp['sha256']:raise ValueError('countdown private file SHA before unpickle')
    payload=pickle.loads(raw);cpu=payload['cpu'];s=unpack(c['worlds'][-1])['suffix'];base=STACK+0xFF00
    if payload['source_sha']!=SOURCE_SHA256 or payload['parent_report_sha']!=PARENT_SHA or payload['case_name']!=name or payload['phase']!=phase or payload['evidence_kind']!='private_original_world_spawn_'+phase:raise ValueError('countdown private source/parent/case/phase')
    if payload['pending_eip']!=RETURN or cpu.reg_read(UC_X86_REG_EIP)!=RETURN or cpu.reg_read(UC_X86_REG_ESP)!=base+4 or cpu.reg_read(UC_X86_REG_EBP)!=base-4 or cpu.reg_read(UC_X86_REG_EAX)!=0:raise ValueError('countdown private natural returned CPU')
    for r in state['prefix_before']+state['unit_before']+state['tail_before']:
        if read_memory(payload,r['pointer'],r['bytes']).hex()!=r['hex']:raise ValueError('countdown private full owned bytes')
    if read_memory(payload,TASK+0x1A98,20).hex()!=state['unit_inputs']['audio_manager_hex']:raise ValueError('countdown actual audio manager retained')
    for r in s['retained_ranges']:
        if hashlib.sha256(read_memory(payload,r['pointer'],r['bytes'])).hexdigest()!=r['sha256']:raise ValueError('countdown private119MB retained memory')
    return payload,cp
