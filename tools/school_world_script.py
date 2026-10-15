"""Original world184 preflight, binding and184/185 paused source projections."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_world_resume import ROOT,SOURCE,SOURCE_SHA256,BASE,STRIDE,COUNT,INACTIVE,get,u32,put,data,overlay,NAMES,project_map_frame,list_project,normalize_selection,friendly_status,cell,vision_merge
from tools.school_script_preflight_catalog import expected_preflight,source_catalog as preflight_source,REGIONS as VM_REGIONS,SCRIPT,SCRIPT_SHA,VM,WORK,CONTROL,TACT,TASK,script_layout
from tools.school_world_tail import project as paused_tail

MUSIC=TASK+0x8F00;AUDIO=TASK+0x1A98
SCRIPT_REGIONS=VM_REGIONS+((MUSIC,40),(AUDIO,20))
HELPERS=((0x42B2D0,0x42B2EF),(0x41E500,0x41E588),(0x41D790,0x41D7BB),(0x40D120,0x40D32A),(0x56CEC0,0x56CF18),(0x454C40,0x454C7A))

@lru_cache(maxsize=1)
def source_contract():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('world script EXE identity')
    return dict(source_image_sha256=SOURCE_SHA256,preflight=preflight_source(),native_helpers=[dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()) for a,b in HELPERS],source_script_sha256=SCRIPT_SHA,source_script_bytes=SCRIPT.stat().st_size,scope='Continuous184 original preflight and selected binding, complete184/185 paused returns; native debug/music/audio/memset; no playback/outer-task/AI/persistence',declared_adapters=['captured strcmp import','unused tick import returns0','existing debug stack check preserves registers'])


def script_data(before):
    if [(r['pointer'],r['bytes']) for r in before]!=list(SCRIPT_REGIONS) or any(set(r)!={'pointer','bytes','hex'} or len(bytes.fromhex(r['hex']))!=r['bytes'] for r in before):raise ValueError('world script complete owned regions')
    return {r['pointer']:bytearray.fromhex(r['hex']) for r in before}


def preflight_project(inputs,before):
    source_contract();memory=script_data(before)
    if inputs.get('driver')!='continuous_original_world184_preflight':raise ValueError('world script natural driver')
    legacy=dict(inputs,driver='natural_pending_preflight_and_caller_return');wanted=expected_preflight(legacy,before[:len(VM_REGIONS)])
    if any(memory[MUSIC]) or any(memory[AUDIO]):raise ValueError('world script captured inactive music/audio')
    out=deepcopy(before);out[:len(VM_REGIONS)]=wanted['preflight_after'];music=bytearray(memory[MUSIC]);music[0x21]=music[0x22]=0;out[-2]['hex']=music.hex()
    return dict(after=out,commands=wanted['commands'],preflight_return=1,selected_binding_executed=False,playback_vm_executed=False)


def binding_project(inputs,before):
    source_contract();d=script_data(before);script,layout=script_layout();vm=d[VM];task=d[TACT];control=d[CONTROL];ptr=inputs['script_pointer'];start,end=layout['selected_span'];offsets=layout['vm_offsets']
    if inputs['driver']!='continuous_original_world184_preflight' or inputs['script_sha256']!=SCRIPT_SHA or u32(task,0x64)!=ptr or task[0x43] or control[12]!=6 or get(control,14) or vm[4] or vm[5] or vm[0x92E1] or list(d[WORK])!=[1,1,1]:raise ValueError('world script exact preflight return1 binding scope')
    def putvm(at,value,fmt='I'):struct.pack_into('<'+fmt,vm,at,value)
    vm[4]=vm[5]=0
    for i in range(5):
        putvm(0x1CF+i*0x12,0,'B');putvm(0x1DC+i*0x12,65535,'H');putvm(0x1DE+i*0x12,65535,'H')
    for i in range(10):
        for at,v in ((0x6F60,0),(0x6F94,65535),(0x6F96,65535),(0x6F62,0),(0x6F82,0)):putvm(at+i*0xE0,v,'H')
    vm[0x92A0:0x92D8]=bytes(56)
    for i in range(56):
        at=0x446+i*0xAB8
        if at+2<=len(vm):putvm(at,0,'H')
        else:d[VM+at][:]=bytes(2)
    for i in range(20):putvm(0x228+i*0x1A,0,'B')
    putvm(0x9248,0,'H');putvm(8,end-start);putvm(12,ptr+start);vm[5]=1;vm[0x1CC]=255;vm[0x9228]=1
    for at,j in ((0x10,0),(0x14,1),(0x18,2)):putvm(at,ptr+start+offsets[j])
    vm[4]=1;putvm(0x1C,0);putvm(0x20,0,'H');vm[0x3C:0x104]=bytes(200);putvm(0x92DC,0xFFFFFFFF)
    task[0x43]=1;task[0x44:0x60]=bytes(28);struct.pack_into('<3I',task,0x48,1,0,1);task[0x59]=1
    out=deepcopy(before)
    for r in out:r['hex']=d[r['pointer']].hex()
    return dict(after=out,binding_args=[0,0,1,0,1,1,0],selected_binding_executed=True,playback_vm_executed=False)


def check_tick(tick):
    if type(tick) is not int or tick not in (184,185):raise ValueError('world script finite184/185 only')


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
    if len(task)!=400 or len(ctrl)!=50 or len(works)!=STRIDE*COUNT or task[0x170] or task[0x171] or task[0x43]!=1 or u32(task,0x38)!=5:raise ValueError('next actual task scope')
    if (ctrl[4],ctrl[24],ctrl[26])!=(0,1,6 if tick==184 else 7) or struct.unpack_from('<h',ctrl,28)[0]!=0 or struct.unpack_from('<h',ctrl,2)[0]!=1 or ctrl[11]!=255 or any(ctrl[i] for i in (5,6,8,9,10)):raise ValueError('next actual opening delay180')
    if inputs['mouse']!=[0,0] or inputs['map_state'] or inputs['task_input']!=[0,0,0] or inputs['ctrl_keys']!=[0,0]:raise ValueError('next closed input')
    if len(d['queue'])!=20 or d['queue'][8:]!=bytes(12) or len(d['selection'])!=1016 or len(d['cursor'])!=10 or len(d['scratch'])!=2048:raise ValueError('next empty queue/complete prefix bounds')
    if not struct.unpack_from('<h',works)[0] or tuple(works[0x290:0x294])!=friendly_status(3,183)[:4] or works[4]!=1 or works[0x2A7] or u32(works,0x518):raise ValueError('next actual phase1 first student')
    ctrl[26]=7
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
    return dict(after=out,display_indices=listed['display_indices'],category_counts=listed['category_counts'],selected_indices=indices,selection_kind=kind,delay=0,action=0,controller_state=7)


def units_project(inputs,before,tick):
    check_tick(tick)
    """Original action0 skips dispatch, animation, regeneration and region counting."""
    source_contract();d=data(before);ctrl=d['control'];works=d['works'];rel=bytes.fromhex(inputs['relation_matrix_hex'])
    if get(ctrl,2)!=1 or (ctrl[4],ctrl[24],ctrl[26])!=(0,1,7) or get(ctrl,28) or any(ctrl[i] for i in (5,6,8,9,10)):raise ValueError('resume exact paused state6')
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
    if (ctrl[4],ctrl[26],get(ctrl,28))!=(0,7,0) or any(get(effects,i*STRIDE+10)!=tick-1 for i in range(10)):raise ValueError('world script paused suffix schedule')
    return paused_tail(inputs,before)


def merge_ranges(rows,changes):
    """Project real physical overlaps, including18-byte control inside50 bytes."""
    out=deepcopy(rows)
    for row in out:
        raw=bytearray.fromhex(row['hex']);a=row['pointer'];b=a+row['bytes']
        for r in changes:
            lo=max(a,r['pointer']);hi=min(b,r['pointer']+r['bytes'])
            if lo<hi:raw[lo-a:hi-a]=bytes.fromhex(r['hex'])[lo-r['pointer']:hi-r['pointer']]
        row['hex']=raw.hex()
    return out


def merge_script_state(state,regions):
    out=deepcopy(state)
    for key in ('prefix_before','unit_before','tail_before'):out[key]=merge_ranges(out[key],regions)
    return out


def call_protocol(phase):
    """Selected source branches: two package lookups, bind, five opcodes, cleanup."""
    lookup=[0x4550F8,0x455143]
    bind=[0x4CE493,0x4CE4EE,0x4CE12F,0x4CE548,0x4CE5B2,0x4CE5E9,0x4CE620]
    if phase=='preflight':
        return [0x49A0D4,0x4551E2,0x49776C,0x497776,0x4551F2]+lookup+[0x455208]+lookup+[0x455264,0x45527B]+bind+[0x455285,0x4552AA,0x4CFE3A,0x42FC88,0x42FCB4,0x4552AA,0x4CEB0E,0x4C2439,0x4C2467,0x4C2495,0x4552AA,0x4CFE1A,0x42FC29,0x42FC41,0x4552AA,0x4CEB4D,0x4552AA,0x4CEA32,0x4CE12F,0x4CEA37,0x4CE822,0x4CE84C,0x41E533,0x4CE856,0x4552BE,0x4D083F,0x4552C8,0x4552CD,0x4552D8]
    if phase=='binding':return [0x49A0F4,0x454A03]+lookup+[0x454A19]+lookup+[0x454A39]+bind+[0x454A68]
    raise ValueError('world script bounded call protocol')
