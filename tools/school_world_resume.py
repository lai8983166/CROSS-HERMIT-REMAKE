"""Source-only last decrement, paused transition and next preflight boundary."""
from tools.school_world_idle import *
from tools.school_world_idle import source_contract as idle_contract
from tools.school_world_tail import project as paused_tail
from tools.school_script_preflight_catalog import SCRIPT,SCRIPT_SHA


def check_tick(tick):
    if type(tick) is not int or tick not in (182,183):raise ValueError('finite original calls182/183 required')


@lru_cache(maxsize=1)
def source_contract():
    s=deepcopy(idle_contract());exe=SOURCE.read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_32)
    checks={0x49A07D:('jne','0x49a099'),0x49A082:('mov','byte ptr [ecx + 0x108b34], 0'),0x49A094:('mov','byte ptr [ecx + 0xc], al'),0x49A0A7:('mov','word ptr [ecx + 0xe], ax'),0x49A0B9:('call','0x456b20'),0x456B3F:('mov','al, byte ptr [0x7f4491]'),0x49A0C0:('jne','0x49a114'),0x49A0CF:('call','0x4551c0'),0x46B7A6:('jmp','0x46b9ed')}
    proof=[]
    for va,wanted in checks.items():
        i=next(md.disasm(exe[va-BASE:va-BASE+16],va))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('resume exact source operand '+hex(va))
        proof.append(dict(va=hex(va),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    functions=[]
    for a,b in ((0x499DA0,0x49A2CD),(0x456B20,0x456B58),(0x46B760,0x46BA08)):
        functions.append(dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(exe[a-BASE:b-BASE]).hexdigest()))
    if hashlib.sha256(SCRIPT.read_bytes()).hexdigest()!=SCRIPT_SHA:raise ValueError('resume original script SHA')
    s.update(resume_functions=functions,resume_instructions=proof,script=dict(path=SCRIPT.relative_to(ROOT).as_posix(),sha256=SCRIPT_SHA,bytes=SCRIPT.stat().st_size),scope='Complete182 enabled delay0;183 paused action0/state6;184 original zero-busy predicate to unexecuted4551C0(0,1); no preflight body/playback/AI/outer-task')
    return s


def world_project(state,tick):
    """Compose physical plane ownership across prefix, units and suffix."""
    pb=state['prefix_before'];p=prefix_project(state['prefix_inputs'],pb,tick);slots=struct.unpack('<3I',bytes.fromhex(p['after'][3]['hex']))
    ub=overlay(state['unit_before'],p['after']);physical={r['pointer']:r for r in p['after']}
    ub[3]['pointer']=slots[1];ub[3]['hex']=physical[slots[1]]['hex']
    u=units_project(state['unit_inputs'],ub,tick);tb=overlay(state['tail_before'],p['after']+u['after']);tail=suffix_project(state['tail_inputs'],tb,tick)
    nxt=overlay(p['after'],u['after']+tail);physical={r['pointer']:r for r in nxt}
    for i,slot in ((5,0),(6,1),(7,2)):
        nxt[i]['pointer']=slots[slot];nxt[i]['hex']=physical[slots[slot]]['hex']
    return dict(prefix=p,unit_before=ub,units=u,tail_before=tb,tail_after=tail,
        next_state=dict(prefix_before=nxt,prefix_inputs=state['prefix_inputs'],unit_before=overlay(u['after'],tail),unit_inputs=state['unit_inputs'],tail_before=tail,tail_inputs=state['tail_inputs']))


def prefix_project(inputs,before,tick):
    source_contract();check_tick(tick);out=deepcopy(before)
    if [r['name'] for r in out]!=NAMES:raise ValueError('next full prefix regions')
    d={r['name']:bytearray.fromhex(r['hex']) for r in out}
    if any(len(d[r['name']])!=r['bytes'] for r in out):raise ValueError('next complete prefix bytes')
    task,ctrl,works=d['task'],d['control'],d['works']
    if len(task)!=400 or len(ctrl)!=50 or len(works)!=STRIDE*COUNT or task[0x170] or task[0x171] or task[0x43] or u32(task,0x38)!=5:raise ValueError('next actual task scope')
    if (ctrl[4],ctrl[24],ctrl[26])!=(1,1,5) or struct.unpack_from('<h',ctrl,28)[0]!=183-tick or struct.unpack_from('<h',ctrl,2)[0]!=1 or ctrl[11]!=255 or any(ctrl[i] for i in (5,6,8,9,10)):raise ValueError('next actual opening delay180')
    if inputs['mouse']!=[0,0] or inputs['map_state'] or inputs['task_input']!=[0,0,0] or inputs['ctrl_keys']!=[0,0]:raise ValueError('next closed input')
    if len(d['queue'])!=20 or d['queue'][8:]!=bytes(12) or len(d['selection'])!=1016 or len(d['cursor'])!=10 or len(d['scratch'])!=2048:raise ValueError('next empty queue/complete prefix bounds')
    if not struct.unpack_from('<h',works)[0] or tuple(works[0x290:0x294])!=friendly_status(3,tick)[:4] or works[4]!=1 or works[0x2A7] or u32(works,0x518):raise ValueError('next actual phase1 first student')
    if tick==182:struct.pack_into('<h',ctrl,28,0)
    else:ctrl[4]=0;ctrl[26]=6
    for r in project_map_frame(out[3:9],inputs['mouse']):d[r['name']][:]=bytes.fromhex(r['hex'])
    slots=struct.unpack('<3I',d['map_slots']);by_pointer={r['pointer']:r for r in out}
    def row(name,p):
        r=by_pointer[p];return dict(name=name,pointer=p,bytes=r['bytes'],hex=d[r['name']].hex())
    li=deepcopy(inputs['lists'])
    if li['opening']!=1 or li['event']!=0:raise ValueError('next actual list gates')
    listed=list_project(li,[row('window',out[9]['pointer']),row('fog_current',slots[1]),row('fog_history',slots[0]),row('visible',out[10]['pointer']),row('categories',out[11]['pointer'])])
    for r in listed['after']:d[by_pointer[r['pointer']]['name']][:]=bytes.fromhex(r['hex'])
    records=[bytes.fromhex(r['record_hex']) if r['record_hex'] else None for r in li['works']]
    selected,indices,kind=normalize_selection(works,records,li['team']);works[:]=selected
    struct.pack_into('<2I',d['selection'],0,len(indices),kind)
    for n,i in enumerate(indices):struct.pack_into('<I',d['selection'],16+n*4,li['works'][i]['pointer'])
    d['cursor'][:]=bytes(6)+b'\xff\xff'+bytes(2);d['scratch'][:]=bytes(2048)
    if u32(d['current_work'],0):raise ValueError('countdown current work must remain clear before first unit')
    for r in out:r['hex']=d[r['name']].hex()
    return dict(after=out,display_indices=listed['display_indices'],category_counts=listed['category_counts'],selected_indices=indices,selection_kind=kind,delay=0,action=int(tick==182),controller_state=5 if tick==182 else 6)


def units_project(inputs,before,tick):
    s=source_contract();check_tick(tick)
    if tick==183:return paused_units(inputs,before)
    d=data(before);ctrl=d['control'];works=d['works'];units=[];used_nodes=set()
    if inputs['audio_manager_hex']!=bytes(20).hex():raise ValueError('countdown captured uninitialized audio manager required')
    if get(ctrl,2)!=1 or (ctrl[4],ctrl[24],ctrl[26])!=(1,1,5) or get(ctrl,28)!=182-tick or any(ctrl[i] for i in (5,6,8,9,10)):raise ValueError('third actual enabled opening scope')
    raw,mapid=map_resource('map05.bin');rel=bytes.fromhex(inputs['relation_matrix_hex'])
    if len(rel)!=256 or inputs['team']!=0 or inputs['map_sha256']!=mapid['sha256'] or inputs['map_all_bytes_verified']!=len(raw):raise ValueError('third entire source map/relations')
    manager=bytes.fromhex(inputs['path_manager_hex'])
    if inputs['path_manager_pointer']!=before[0]['pointer']-0x80AEC+0x2A634 or len(manager)!=100 or u32(manager,96):raise ValueError('idle exact empty native path manager')
    indices=[i for i in range(COUNT) if get(works,i*STRIDE)]
    if indices not in ([0,1,2]+list(range(215,250)),[0,1]+list(range(215,250))) or [x['index'] for x in inputs['units']]!=indices:raise ValueError('third exact remaining occupied order')
    for x in inputs['units']:
        i=x['index'];at=i*STRIDE;ptr=before[0]['pointer']+at;w=bytearray(works[at:at+STRIDE]);rp=u32(w,0x258);roff=rp-before[1]['pointer']
        if roff%176 or not 0<=roff<=len(d['records'])-176:raise ValueError('third record bounds')
        r=d['records'][roff:roff+176];job=struct.unpack_from('<H',r,2)[0];klass=struct.unpack_from('<H',r,12)[0]
        if x['record_pointer']!=rp or x['record_hex']!=r.hex() or w[0x293]!=(friendly_prestate(job,tick)[0] if i in (0,1,2) else 1) or (w[0x292] if i not in (0,1,2) else tuple(w[0x290:0x294])!=friendly_status(job,tick)[:4]) or u32(w,0x518):raise ValueError('third complete record/phase/queue')
        w[8]&=127
        if i in INACTIVE:
            if r[15] or r[164]!=5 or klass!=job or job not in (301,316,317,337,452) or w[0x290]!=11 or w[0x2A7]!=1 or w[6] or w[7] or get(w,10):raise ValueError('third exact inactive phase1')
            works[at:at+STRIDE]=w;units.append(dict(index=i,job=job,inactive=True,handler_return=1));continue
        rule=s['jobs'].get(str(job));group=r[164]
        expected_job=job if i in (0,1,2) else 406 if i==217 else 383 if i<247 else {247:393,248:387,249:5}[i]
        if rule is None or job!=expected_job or klass!=rule['class'] or group!=rule['group'] or r[15]!=1 or w[0x290]!=(friendly_status(job,tick)[0] if i in (0,1,2) else rule['mode']) or w[0x2A7]!=int(group>=4) or get(w,10)!=(friendly_prestate(job,tick)[1] if i in (0,1,2) else tick-2):raise ValueError('third actual active identity/mode/counter')
        if i in (0,1,2) and job not in (3,4,9):raise ValueError('third current friendly jobs')
        for b,p,identity in [(x['bindings'][0],rule['main'],rule['main_source'])]+([(x['bindings'][1],rule['attachments'][0],rule['effect_source'])] if rule['attachments'] else []):
            owner=bytes.fromhex(b['controller_hex'])
            if len(owner)!=84 or u32(owner,0)!=b['metadata_pointer'] or b['metadata_bytes']!=p['metadata_bytes'] or b['metadata_sha256']!=p['metadata_sha256'] or b['source_sha256']!=identity['sha256']:raise ValueError('third source metadata/controller')
        b=x['bindings'][0];owner=bytes.fromhex(b['controller_hex'])
        if b['owner']!=u32(w,0x44) or u32(owner,0x4C)!=rule['animation_table_pointer'] or u32(owner,0x50)!=rule['position_table_pointer']:raise ValueError('third source pose owner')
        prior_idle=i in (0,1,2) and tick>binding_tick(job);key=('idle:' if prior_idle else 'main:')+str(job);updates=tick-binding_tick(job) if prior_idle else tick-2
        aw=bytearray(w[0x48:0xA0]);main=rule['main'];expected_main=schedule(s['programs'][key],updates);ended=bool(expected_main[11])
        if aw[8] or aw[11]!=int(ended) or w[4]!=int(ended)  or get(aw,0x48):raise ValueError('third exact existing main frame')
        validate_animation(aw,b['metadata_pointer'],s['programs'][key],updates)
        if i in (0,1,2) and (w[6] or w[7] or get(aw,12)!=(1 if prior_idle else 18)):raise ValueError('idle exact friendly flags and pose')
        root_idle=not bool(u32(aw,4));animation_steps=[]
        for pos in [0x48]+[0xA0+n*NODE for n in range(5)]:
            if u32(w,pos+0x34) or u32(w,pos+0x40) or (pos!=0x48 and (u32(w,pos+4) or u32(w,pos+0x20))):raise ValueError('third empty controller queues/aux')
        nodes=[];released=[];allocated=[];previous=None
        def create_child(parent,instruction):
            if i not in (0,1,2) or tick!=107 or parent[2] or parent[8]:raise ValueError('spawn actual bounded root/call required')
            spec=s['spawns'][str(job)]
            if u32(owner,16)!=b['metadata_pointer']+spec['table_offset']:raise ValueError('spawn source bank3 table binding')
            if instruction!=spec['instruction']:raise ValueError('spawn exact class opcode')
            slot=next((n for n in range(2048) if not d['pool'][n*NODE]),None)
            if slot!=i*2+1:raise ValueError('spawn exact first freed slot reuse required')
            off=slot*NODE;node=POOL+off;prior=d['pool'][off:off+NODE].hex();child=bytearray(NODE)
            child[0]=1;put(child,12,-1,'h');child[0x54:0x57]=bytes([128])*3;child[3]=parent[3]&191;child[2]=parent[2];child[8]=parent[8]+1
            put(child,0x1C,u32(parent,0x1C));put(child,0x24,u32(parent,0x24));put(child,0x20,u32(parent,0x20));put(parent,0x20,node)
            frame=bytes.fromhex(instruction['frame_hex'])
            for at,bit,operand in ((0x12,1,4),(0x14,2,6)):
                value=get(parent,at)+(-1 if child[3]&bit else 1)*struct.unpack_from('<h',frame,operand)[0];put(child,at,((value+32768)%65536)-32768,'h')
            put(child,0x18,spec['layer'])
            if u32(parent,0x2C):put(child,0x2C,u32(parent,0x2C));child[0x48:0x54]=parent[0x48:0x54]
            program=s['programs']['spawn:'+str(job)];setup(child,b['metadata_pointer'],program[0]);ret,events=step_animation(child,b['metadata_pointer'],program)
            d['pool'][off:off+NODE]=child;allocated.append(node)
            return dict(node=node,pool_slot=slot,prior_hex=prior,program=spec['program'],layer=spec['layer'],immediate_events=events,immediate_return=ret,immediate_wait=get(child,14))
        voice=None;mode_applied=False;mode_requested=False;idle_bound=False
        if i in (0,1,2):
            if w[0x292]:
                if tick!=binding_tick(job) or w[0x292]!=2:raise ValueError('idle exact pending commit')
                w[0x291]=w[0x290];w[0x290]=2;w[0x292]=0;w[0x293]=0;mode_applied=True
            if w[0x290]==25:
                if w[0x293]==1 and w[4]:
                    if job!=9 or tick!=129:raise ValueError('idle exact job9 prior completion')
                    voice=voice_project(d['crt_thread'],job);put(w,10,get(w,10)+1,'h');w[0x293]=2
                elif w[0x293]==2:
                    if job!=9 or tick!=130 or get(w,10)<60:raise ValueError('idle exact job9 phase2')
                    put(w,10,0,'h');w[0x293]=3
                elif w[0x293]==3:
                    if get(w,10)<=0:raise ValueError('idle positive phase3 counter')
                    w[0x292]=2;w[6]=0;w[7]=0;mode_requested=True
            elif w[0x290]==2 and w[0x293]==0:
                pose=s['idle_poses'][str(job)]
                if u32(aw,32) or u32(owner,4)!=b['metadata_pointer']+pose['table_offset']:raise ValueError('idle source bank0 binding/empty child root')
                put(aw,12,1,'h');aw[3]=bytes.fromhex(pose['lookup_hex'])[1]&3;aw[8]=0;put(aw,24,7);put(aw,18,0,'h');put(aw,20,0,'h');put(aw,36,ptr+0x48);aw[11]=0;put(aw,16,0,'h')
                frame_setup(aw,b['metadata_pointer']+pose['program']['offset'],pose['program']);w[4]=0;put(w,10,0,'h');w[0x293]=1;key='idle:'+str(job);idle_bound=True
        root_idle=not bool(u32(aw,4))
        main_return,events=step_animation(aw,b['metadata_pointer'],s['programs'][key],create_child)
        animation_steps.append(dict(node=ptr+0x48,kind='main',events=events))
        if any(e['kind']=='clear' and not e['depth'] for e in events) and u32(aw,32):
            p=u32(aw,32);off=p-POOL;n=bytearray(d['pool'][off:off+NODE])
            if i not in (0,1,2) or job!=9 or tick!=129 or p!=POOL+(2*i+1)*NODE or len(n)!=NODE or (n[0],n[2],n[8])!=(1,0,1) or u32(n,32) or u32(n,36)!=ptr+0x48 or u32(n,28)!=b['owner']:raise ValueError('handoff exact nonpersistent recursive child')
            if n[3]!=aw[3]&191 or u32(n,44)!=u32(aw,44) or n[0x48:0x54]!=aw[0x48:0x54]:raise ValueError('handoff exact recursive inherited child')
            validate_animation(n,b['metadata_pointer'],s['programs']['spawn:'+str(job)],tick-107,layer=s['spawns'][str(job)]['layer'],depth=1,flags=aw[3]&191)
            n[1]=0;n[0]=0;put(aw,32,0);d['pool'][off:off+NODE]=n;released.append(p)
            next(e for e in events if e['kind']=='clear')['recursive_nodes']=[p]
        specs=[]
        if i in (0,1,2) and tick>=107 and u32(aw,32):specs.append(('spawn:'+str(job),b,s['spawns'][str(job)]['layer'],0,tick-107))
        for pr in rule['attachments'][::-1]:
            program=s['programs']['attached:'+str(pr['animation'])]
            if u32(schedule(program,tick-1),4):specs.append(('attached:'+str(pr['animation']),x['bindings'][1],7,64,tick-1))
        p=u32(aw,32)
        for key,binding,layer,flags,updates in specs:
            off=p-POOL
            if off<0 or off%NODE or off+NODE>len(d['pool']) or p in used_nodes:raise ValueError('spawn exact unique linked bounds')
            n=bytearray(d['pool'][off:off+NODE]);program=s['programs'][key];is_child=key.startswith('spawn:')
            if n[0]!=1 or n[2]!=int(not is_child) or n[8]!=1 or u32(n,0x24)!=ptr+0x48 or u32(n,0x1C)!=binding['owner'] or u32(n,0x34) or u32(n,0x40) or get(n,0x48):raise ValueError('spawn exact source linked node type/owner')
            if is_child and (n[3]!=aw[3]&191 or u32(n,0x2C)!=u32(aw,0x2C) or n[0x48:0x54]!=aw[0x48:0x54]):raise ValueError('spawn exact inherited flags/handle/coordinates')
            used_nodes.add(p);following=u32(n,32)
            if is_child and tick==107:
                if p not in allocated or n[1]!=1:raise ValueError('spawn immediate visited-byte skip')
                validate_animation(n,binding['metadata_pointer'],program,1,layer=layer,depth=1,flags=aw[3]&191)
                previous=p;p=following;continue
            validate_animation(n,binding['metadata_pointer'],program,updates,layer=layer,depth=1,flags=flags)
            nodes.append(p);ret,events=step_animation(n,binding['metadata_pointer'],program)
            animation_steps.append(dict(node=p,kind='spawned' if is_child else 'attached',events=events))
            if any(e['kind']=='clear' for e in events):
                if previous is None:put(aw,32,following)
                else:put(d['pool'],previous-POOL+32,following)
                n[0]=0;released.append(p)
            else:previous=p
            d['pool'][off:off+NODE]=n;p=following
        if p:raise ValueError('spawn exact captured child order')
        w[0x48:0xA0]=aw;w[4]=main_return;put(w,10,(get(w,10)+1)&65535,'H')
        if get(r,0x14)!=get(r,0x16) or get(r,0x1A)!=get(r,0x1C) or get(r,0x16)<=0 or u32(w,0x510) or w[0x14] or w[0x34]:raise ValueError('third full live values/static view')
        recovered=regen(w,r)
        if recovered['heals'] or recovered['record_hex']!=r.hex():raise ValueError('third no actual healing')
        w[:]=bytes.fromhex(recovered['work_hex']);px,py=struct.unpack_from('<2i',w,0x2EC);cx,cy=cell(px,32),cell(py,16)
        if not 0<=cx<64 or not 0<=cy<96 or list(w[0x4E7:0x4EB])!=[cx,cy,cx,cy]:raise ValueError('third stationary source cells')
        event=raw[16+(cy*64+cx)*6+2]
        if event<32:
            z=event*64+group*4;struct.pack_into('<H',d['region_stats'],z,(struct.unpack_from('<H',d['region_stats'],z)[0]+1)&65535);d['region_stats'][z+2]|=rule['category_mask']
        vision=None
        if group==inputs['team'] or rel[inputs['team']*16+group]==0:
            view=min(32,max(0,r[44]-256 if r[44]>=128 else r[44]));cur,hist=vision_merge(d['fog_current'],d['fog_history'],cx,cy,view);d['fog_current'][:]=cur;d['fog_history'][:]=hist;vision=[cx,cy,view]
        works[at:at+STRIDE]=w;units.append(dict(index=i,job=job,klass=klass,group=group,inactive=False,handler_return=0,main_return=main_return,main_wait=get(aw,14),root_idle=root_idle,linked_order=nodes,sound_nodes=[],animation_steps=animation_steps,released_nodes=released,allocated_nodes=allocated,mode_applied=mode_applied,mode_requested=mode_requested,idle_bound=idle_bound,mode_after=w[0x290],previous_mode=w[0x291],pending_mode=w[0x292],phase_after=w[0x293],counter_after=get(w,10),voice=voice,cell=[cx,cy],event_region=event,vision_args=vision))
    put(d['current_work'],0,0);out=deepcopy(before)
    for row in out:row['hex']=d[row['name']].hex()
    return dict(after=out,units=units,unit_indices=indices,templates_activated=0,idle_root_indices=[u['index'] for u in units if u.get('root_idle')],all250_slot_loop_completed=True,world_completed=False)


def paused_units(inputs,before):
    """Original action0 skips dispatch, animation, regeneration and region counting."""
    source_contract();d=data(before);ctrl=d['control'];works=d['works'];rel=bytes.fromhex(inputs['relation_matrix_hex'])
    if get(ctrl,2)!=1 or (ctrl[4],ctrl[24],ctrl[26])!=(0,1,6) or get(ctrl,28) or any(ctrl[i] for i in (5,6,8,9,10)):raise ValueError('resume exact paused state6')
    indices=[i for i in range(COUNT) if get(works,i*STRIDE)]
    if indices not in ([0,1,2]+list(range(215,250)),[0,1]+list(range(215,250))) or [x['index'] for x in inputs['units']]!=indices or inputs['team']!=0 or len(rel)!=256:raise ValueError('resume paused complete occupied/relations')
    units=[]
    for x in inputs['units']:
        i=x['index'];at=i*STRIDE;w=bytearray(works[at:at+STRIDE]);rp=u32(w,0x258);off=rp-before[1]['pointer']
        if off%176 or not 0<=off<=len(d['records'])-176:raise ValueError('resume paused record bounds')
        r=d['records'][off:off+176]
        if x['record_pointer']!=rp or x['record_hex']!=r.hex():raise ValueError('resume paused entire record')
        vision=None;cx=cy=None
        if r[15]==1:
            px,py=struct.unpack_from('<2i',w,0x2EC);cx,cy=cell(px,32),cell(py,16)
            if not 0<=cx<64 or not 0<=cy<96 or list(w[0x4E7:0x4EB])!=[cx,cy,cx,cy]:raise ValueError('resume stationary actual cells')
            if r[164]==inputs['team'] or rel[inputs['team']*16+r[164]]==0:
                if w[0x34] in (46,47) or w[0x14]==6:raise ValueError('resume modified paused view unsupported')
                view=min(32,max(0,r[44]-256 if r[44]>=128 else r[44]));cur,hist=vision_merge(d['fog_current'],d['fog_history'],cx,cy,view);d['fog_current'][:]=cur;d['fog_history'][:]=hist;vision=[cx,cy,view]
            w[0x4E7:0x4EB]=bytes((cx,cy,cx,cy))
        works[at:at+STRIDE]=w
        units.append(dict(index=i,job=struct.unpack_from('<H',r,2)[0],inactive=r[15]!=1,group=r[164],cell=None if cx is None else [cx,cy],vision_args=vision,counter_after=get(w,10),animation_frozen=True))
    put(d['current_work'],0,0);out=deepcopy(before)
    for row in out:row['hex']=d[row['name']].hex()
    return dict(after=out,units=units,unit_indices=indices,templates_activated=0,all250_slot_loop_completed=True,world_completed=False,character_actions_executed=False)


def suffix_project(inputs,before,tick):
    check_tick(tick);ctrl=bytes.fromhex(before[5]['hex']);effects=bytes.fromhex(before[3]['hex'])
    if (ctrl[4],ctrl[26],get(ctrl,28))!=(int(tick==182),5 if tick==182 else 6,0):raise ValueError('resume exact suffix controller')
    if any(struct.unpack_from('<H',effects,i*1312+10)[0]!=tick-1 for i in range(10)):raise ValueError('resume complete effect counters')
    return old_suffix(inputs,before) if tick==182 else paused_tail(inputs,before)


def preflight_boundary(inputs,before):
    fields={'mouse','busy','entry_receiver','script_pointer','script_sha256','script_bytes'}
    if type(inputs) is not dict or set(inputs)!=fields or any(type(inputs[k]) is not int for k in ('busy','entry_receiver','script_pointer','script_bytes')) or inputs['mouse']!=[0,0] or any(type(n) is not int for n in inputs['mouse']):raise ValueError('resume finite exact preflight inputs')
    source_contract();d={r['name']:bytes.fromhex(r['hex']) for r in before}
    if list(d)!=NAMES or any(len(d[r['name']])!=r['bytes'] for r in before):raise ValueError('resume complete script boundary regions')
    c=d['control'];task=d['task']
    if u32(d['current_work'],0):raise ValueError('resume original world entry clears an already empty current pointer')
    if (c[4],c[24],c[26],get(c,28),c[11])!=(0,1,6,0,255) or any(c[i] for i in (5,6,8,9,10)) or inputs['busy']!=0:raise ValueError('resume exact state6 captured busy gate')
    if inputs['mouse']!=[0,0] or inputs['entry_receiver']!=before[0]['pointer'] or u32(task,0x38)!=5 or task[0x43] or task[0x170] or task[0x171]:raise ValueError('resume original preflight receiver/task')
    if inputs['script_pointer']!=u32(task,0x64) or inputs['script_sha256']!=SCRIPT_SHA or inputs['script_bytes']!=SCRIPT.stat().st_size:raise ValueError('resume entire captured source script')
    return dict(after=deepcopy(before),busy_result=0,preflight_args=[0,1],controller_state=6,preflight_body_executed=False)
