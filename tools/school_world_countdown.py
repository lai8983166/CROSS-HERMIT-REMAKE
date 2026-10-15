"""Finite original enabled worlds4–6, source2063 opcode2 and closed audio guard."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_world_third import ROOT,SOURCE,SOURCE_SHA256,BASE,STRIDE,COUNT,data,INACTIVE,regen,get,u32,put,POOL,NODE,map_resource,vision_merge,cell,effect_resource,source_contract as third_source
from tools.school_world_final import suffix_project as old_suffix
from tools.school_student_action import source_contract as student_source,frame_setup
from tools.school_first_unit_work_catalog import source_catalog
from tools.school_world_second import NAMES
from tools.school_world_map import project_map_frame
from tools.school_world_lists import project as list_project
from tools.school_world_command import normalize_selection
from tools.dxanim_lib import parse_dxanim


def check_tick(tick):
    if type(tick) is not int or tick not in (4,5,6):raise ValueError('finite original calls4–6 required')


@lru_cache(maxsize=1)
def source_contract():
    old=deepcopy(third_source());st=student_source();rule=next(r for r in source_catalog()['jobs'] if r['job']==10);exe=SOURCE.read_bytes()
    if hashlib.sha256(exe).hexdigest()!=SOURCE_SHA256:raise ValueError('countdown source executable')
    category=exe[0x6B2D8A-BASE+10*64]
    old['jobs']['3']=dict(job=3,**{'class':10},group=0,mode=25,main=st['main'],attachments=st['attachments'],main_source=st['main_source'],effect_source=st['effect_source'],animation_table_pointer=rule['animation_table_pointer'],position_table_pointer=rule['position_table_pointer'],category_mask=1<<(category-1))
    raw,identity=effect_resource();offset=st['attachments'][0]['offset']+20;frame=raw[offset:offset+10];offs=parse_dxanim(raw);sprite=frame[2]+((struct.unpack_from('<H',frame,6)[0]&15)<<8)
    if frame[0]&15 or frame.hex()!='0000b1fffffff7ff0600':raise ValueError('countdown next source2063 frame')
    following=dict(offset=offset,frame_hex=frame.hex(),duration=struct.unpack_from('<h',frame,8)[0],sprite=sprite,sprite_hex=raw[offs[4]+sprite*10:offs[4]+sprite*10+10].hex())
    md=Cs(CS_ARCH_X86,CS_MODE_32);bodies=[]
    for a in (0x40B990,0x40D390):
        end=next(i.address+i.size for i in md.disasm(exe[a-BASE:a-BASE+4096],a) if i.mnemonic=='ret');bodies.append(dict(va=hex(a),end=hex(end),sha256=hashlib.sha256(exe[a-BASE:end-BASE]).hexdigest()))
    proof=[]
    for a,wanted in {0x40D3B0:('cmp','dword ptr [eax + 8], 0'),0x40D3B6:('jmp','0x40d4b6'),0x40AA6C:('jmp','0x40a8c4'),0x40A910:('sub','ax, 1')}.items():
        i=next(md.disasm(exe[a-BASE:a-BASE+16],a))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('countdown exact source operand '+hex(a))
        proof.append(dict(va=hex(a),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    return dict(source_image_sha256=SOURCE_SHA256,jobs=old['jobs'],upcoming2063=old['upcoming2063'],following2063=following,audio_functions=bodies,instructions=proof,scope='Finite whole original calls4–6 and opcode2 natural uninitialized audio guard; no backend playback/180/VM/AI/attached-node free')


def audio_ranges():return tuple((int(r['va'],16),int(r['end'],16)) for r in source_contract()['audio_functions'])


def suffix_project(inputs,before,tick):
    check_tick(tick)
    if get(bytes.fromhex(before[5]['hex']),28)!=182-tick:raise ValueError('countdown suffix actual delay')
    effects=bytes.fromhex(before[3]['hex'])
    if any(struct.unpack_from('<H',effects,i*1312+10)[0]!=tick-1 for i in range(10)):raise ValueError('countdown exact idle counters')
    return old_suffix(inputs,before)


def overlay(before,changed):
    out=deepcopy(before);physical={r['pointer']:r for r in changed}
    for r in out:
        if r['pointer'] in physical:
            p=physical[r['pointer']]
            if p['bytes']!=r['bytes']:raise ValueError('countdown exact overlapping region size')
            r['hex']=p['hex']
    return out


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
    if not struct.unpack_from('<h',works)[0] or works[0x290]!=25 or works[0x292] or works[0x293]!=1 or works[4] or works[0x2A7] or u32(works,0x518):raise ValueError('next actual phase1 first student')
    struct.pack_into('<h',ctrl,28,182-tick)
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
    return dict(after=out,display_indices=listed['display_indices'],category_counts=listed['category_counts'],selected_indices=indices,selection_kind=kind,delay=182-tick,action=1,controller_state=5)


def units_project(inputs,before,tick):
    s=source_contract();check_tick(tick);d=data(before);ctrl=d['control'];works=d['works'];units=[];used_nodes=set()
    if inputs['audio_manager_hex']!=bytes(20).hex():raise ValueError('countdown captured uninitialized audio manager required')
    if get(ctrl,2)!=1 or (ctrl[4],ctrl[24],ctrl[26])!=(1,1,5) or get(ctrl,28)!=182-tick or any(ctrl[i] for i in (5,6,8,9,10)):raise ValueError('third actual enabled opening scope')
    raw,mapid=map_resource('map05.bin');rel=bytes.fromhex(inputs['relation_matrix_hex'])
    if len(rel)!=256 or inputs['team']!=0 or inputs['map_sha256']!=mapid['sha256'] or inputs['map_all_bytes_verified']!=len(raw):raise ValueError('third entire source map/relations')
    indices=[i for i in range(COUNT) if get(works,i*STRIDE)]
    if indices not in ([0,1,2]+list(range(215,250)),[0,1]+list(range(215,250))) or [x['index'] for x in inputs['units']]!=indices:raise ValueError('third exact remaining occupied order')
    for x in inputs['units']:
        i=x['index'];at=i*STRIDE;ptr=before[0]['pointer']+at;w=bytearray(works[at:at+STRIDE]);rp=u32(w,0x258);roff=rp-before[1]['pointer']
        if roff%176 or not 0<=roff<=len(d['records'])-176:raise ValueError('third record bounds')
        r=d['records'][roff:roff+176];job=struct.unpack_from('<H',r,2)[0];klass=struct.unpack_from('<H',r,12)[0]
        if x['record_pointer']!=rp or x['record_hex']!=r.hex() or w[0x293]!=1 or w[0x292] or u32(w,0x518):raise ValueError('third complete record/phase/queue')
        w[8]&=127
        if i in INACTIVE:
            if r[15] or r[164]!=5 or klass!=job or job not in (301,316,317,337,452) or w[0x290]!=11 or w[0x2A7]!=1 or w[6] or w[7] or get(w,10):raise ValueError('third exact inactive phase1')
            works[at:at+STRIDE]=w;units.append(dict(index=i,job=job,inactive=True,handler_return=1));continue
        rule=s['jobs'].get(str(job));group=r[164]
        expected_job=job if i in (0,1,2) else 406 if i==217 else 383 if i<247 else {247:393,248:387,249:5}[i]
        if rule is None or job!=expected_job or klass!=rule['class'] or group!=rule['group'] or r[15]!=1 or w[0x290]!=rule['mode'] or w[0x2A7]!=int(group>=4) or get(w,10)!=tick-2:raise ValueError('third actual active identity/mode/counter')
        if i in (0,1,2) and job not in (3,4,9):raise ValueError('third current friendly jobs')
        for b,p,identity in [(x['bindings'][0],rule['main'],rule['main_source'])]+([(x['bindings'][1],rule['attachments'][0],rule['effect_source'])] if rule['attachments'] else []):
            owner=bytes.fromhex(b['controller_hex'])
            if len(owner)!=84 or u32(owner,0)!=b['metadata_pointer'] or b['metadata_bytes']!=p['metadata_bytes'] or b['metadata_sha256']!=p['metadata_sha256'] or b['source_sha256']!=identity['sha256']:raise ValueError('third source metadata/controller')
        b=x['bindings'][0];owner=bytes.fromhex(b['controller_hex'])
        if b['owner']!=u32(w,0x44) or u32(owner,0x4C)!=rule['animation_table_pointer'] or u32(owner,0x50)!=rule['position_table_pointer']:raise ValueError('third source pose owner')
        aw=bytearray(w[0x48:0xA0]);main=rule['main'];ended=main['duration']==1
        if aw[8] or aw[11]!=int(ended) or w[4]!=int(ended) or u32(aw,4)!=(0 if ended else b['metadata_pointer']+main['offset']) or get(aw,14)!=(0 if ended else main['duration']-(tick-2)) or get(aw,0x48):raise ValueError('third exact existing main frame')
        for pos in [0x48]+[0xA0+n*NODE for n in range(5)]:
            if u32(w,pos+0x34) or u32(w,pos+0x40) or (pos!=0x48 and (u32(w,pos+4) or u32(w,pos+0x20))):raise ValueError('third empty controller queues/aux')
        nodes=[];p=u32(aw,32)
        for pr in rule['attachments'][::-1]:
            off=p-POOL
            if off<0 or off%NODE or off+NODE>len(d['pool']) or p in used_nodes:raise ValueError('third exact unique linked bounds')
            n=bytearray(d['pool'][off:off+NODE]);eb=x['bindings'][1]
            if n[0]!=1 or n[2]!=1 or n[8]!=1 or n[11] or u32(n,4)!=eb['metadata_pointer']+pr['offset'] or u32(n,0x24)!=ptr+0x48 or get(n,14)!=pr['duration']-(tick-1) or u32(n,0x34) or u32(n,0x40) or get(n,0x48):raise ValueError('third existing persistent attached frame')
            used_nodes.add(p);nodes.append(p);n[1]=1
            if tick==6 and pr['animation']==2063:
                frame_setup(n,eb['metadata_pointer']+s['following2063']['offset'],s['following2063']);put(n,14,s['following2063']['duration']-1,'h')
            else:put(n,14,get(n,14)-1,'h')
            d['pool'][off:off+NODE]=n;p=u32(n,32)
        if p:raise ValueError('third exact captured children')
        if ended:pass
        else:aw[1]=1;put(aw,14,get(aw,14)-1,'h')
        w[0x48:0xA0]=aw;w[4]=int(ended);put(w,10,tick-1,'H')
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
        works[at:at+STRIDE]=w;units.append(dict(index=i,job=job,klass=klass,group=group,inactive=False,handler_return=0,main_return=int(ended),main_wait=get(aw,14),root_idle=ended,linked_order=nodes,sound_nodes=nodes[-1:] if tick==6 and nodes else [],cell=[cx,cy],event_region=event,vision_args=vision))
    put(d['current_work'],0,0);out=deepcopy(before)
    for row in out:row['hex']=d[row['name']].hex()
    return dict(after=out,units=units,unit_indices=indices,templates_activated=0,idle_root_indices=[u['index'] for u in units if u.get('root_idle')],all250_slot_loop_completed=True,world_completed=False)
