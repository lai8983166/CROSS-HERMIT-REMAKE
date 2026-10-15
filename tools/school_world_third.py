"""Source third-world remaining initialized units and enabled suffix."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_following_students import ROOT,SOURCE,SOURCE_SHA256,BASE,STRIDE,COUNT,data,source_contract as friendly_rules
from tools.school_scene_first import source_contract as scene_rule
from tools.school_world_final import source_contract as final_rules,suffix_project
from tools.school_world_next import clearing_project
from tools.school_student_action import u32,put,POOL,NODE
from tools.school_student_tail import regen,get
from tools.school_world_command import cell
from tools.school_world_lists import vision_merge
from tools.school_unitctrl_map_emulation import map_resource
from tools.school_unit_assets_emulation import effect_resource

FUNCTIONS=(0x475D60,0x479F40,0x4761C0,0x476250,0x40A100,0x40A800,0x40AB80)
INACTIVE=[215,216]+list(range(218,240))


@lru_cache(maxsize=1)
def source_contract():
    exe=SOURCE.read_bytes()
    if hashlib.sha256(exe).hexdigest()!=SOURCE_SHA256:raise ValueError('third source executable')
    md=Cs(CS_ARCH_X86,CS_MODE_32);bodies=[];proof=[]
    for va in FUNCTIONS+(0x40B990,):
        end=next(i.address+i.size for i in md.disasm(exe[va-BASE:va-BASE+8192],va) if i.mnemonic=='ret')
        bodies.append(dict(va=hex(va),end=hex(end),sha256=hashlib.sha256(exe[va-BASE:end-BASE]).hexdigest(),executed_scope=va!=0x40B990))
    checks={0x4761FF:('jmp','0x476238'),0x476293:('je','0x4762ba'),0x4762C6:('je','0x4762cf'),
        0x479F83:('je','0x479fbc'),0x479FE1:('jmp','0x47a224'),0x47A224:('mov','eax, 1'),
        0x40AA2A:('call','0x40b990'),0x40B9FE:('call','0x40d390')}
    for va,wanted in checks.items():
        i=next(md.disasm(exe[va-BASE:va-BASE+16],va))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('third exact source operand '+hex(va))
        proof.append(dict(va=hex(va),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    jobs={}
    for k,r in friendly_rules()['jobs'].items():jobs[k]={**r,'group':0,'mode':25}
    r=scene_rule();jobs['406']={**r,'class':406,'mode':28,'group':6,'attachments':[]}
    for k,r in final_rules()['jobs'].items():
        job=5 if k=='4' else int(k);jobs[str(job)]={**r,'job':job,'group':5 if job==383 else 0 if job==387 else 7,'mode':2,'attachments':[]}
    efct,identity=effect_resource();p=jobs['4']['attachments'][0];at=p['offset']+10;frame=efct[at:at+10]
    if frame.hex()!='02000000000000003b00':raise ValueError('third source2063 next opcode')
    return dict(source_image_sha256=SOURCE_SHA256,functions=bodies,instructions=proof,jobs=jobs,inactive_indices=INACTIVE,
        upcoming2063=dict(source=identity,offset=at,frame_hex=frame.hex(),opcode=frame[0]&3,sound=struct.unpack_from('<H',frame,8)[0],native_dispatch='0x40b990',forwarding='0x40d390',native_executed=False),
        scope='Remaining third-world units and natural world return only; no fourth world/180 interval/VM/AI/audio/attached-node free')


def ranges():return tuple((int(r['va'],16),int(r['end'],16)) for r in source_contract()['functions'] if r['executed_scope'])


def project(inputs,before):
    s=source_contract();d=data(before);ctrl=d['control'];works=d['works'];units=[];used_nodes=set()
    if get(ctrl,2)!=1 or (ctrl[4],ctrl[24],ctrl[26])!=(1,1,5) or get(ctrl,28)!=179 or any(ctrl[i] for i in (5,6,8,9,10)):raise ValueError('third actual enabled opening scope')
    raw,mapid=map_resource('map05.bin');rel=bytes.fromhex(inputs['relation_matrix_hex'])
    if len(rel)!=256 or inputs['team']!=0 or inputs['map_sha256']!=mapid['sha256'] or inputs['map_all_bytes_verified']!=len(raw):raise ValueError('third entire source map/relations')
    indices=[i for i in range(1,COUNT) if get(works,i*STRIDE)]
    if indices not in ([1,2]+list(range(215,250)),[1]+list(range(215,250))) or [x['index'] for x in inputs['units']]!=indices:raise ValueError('third exact remaining occupied order')
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
        expected_job=job if i in (1,2) else 406 if i==217 else 383 if i<247 else {247:393,248:387,249:5}[i]
        if rule is None or job!=expected_job or klass!=rule['class'] or group!=rule['group'] or r[15]!=1 or w[0x290]!=rule['mode'] or w[0x2A7]!=int(group>=4) or get(w,10)!=1:raise ValueError('third actual active identity/mode/counter')
        if i in (1,2) and job not in (4,9):raise ValueError('third current friendly jobs')
        for b,p,identity in [(x['bindings'][0],rule['main'],rule['main_source'])]+([(x['bindings'][1],rule['attachments'][0],rule['effect_source'])] if rule['attachments'] else []):
            owner=bytes.fromhex(b['controller_hex'])
            if len(owner)!=84 or u32(owner,0)!=b['metadata_pointer'] or b['metadata_bytes']!=p['metadata_bytes'] or b['metadata_sha256']!=p['metadata_sha256'] or b['source_sha256']!=identity['sha256']:raise ValueError('third source metadata/controller')
        b=x['bindings'][0];owner=bytes.fromhex(b['controller_hex'])
        if b['owner']!=u32(w,0x44) or u32(owner,0x4C)!=rule['animation_table_pointer'] or u32(owner,0x50)!=rule['position_table_pointer']:raise ValueError('third source pose owner')
        aw=bytearray(w[0x48:0xA0]);main=rule['main'];ended=main['duration']==1
        if aw[8] or aw[11]!=int(ended) or w[4]!=int(ended) or u32(aw,4)!=b['metadata_pointer']+main['offset'] or get(aw,14)!=main['duration']-1 or get(aw,0x48):raise ValueError('third exact existing main frame')
        for pos in [0x48]+[0xA0+n*NODE for n in range(5)]:
            if u32(w,pos+0x34) or u32(w,pos+0x40) or (pos!=0x48 and (u32(w,pos+4) or u32(w,pos+0x20))):raise ValueError('third empty controller queues/aux')
        nodes=[];p=u32(aw,32)
        for pr in rule['attachments'][::-1]:
            off=p-POOL
            if off<0 or off%NODE or off+NODE>len(d['pool']) or p in used_nodes:raise ValueError('third exact unique linked bounds')
            n=bytearray(d['pool'][off:off+NODE]);eb=x['bindings'][1]
            if n[0]!=1 or n[2]!=1 or n[8]!=1 or n[11] or u32(n,4)!=eb['metadata_pointer']+pr['offset'] or u32(n,0x24)!=ptr+0x48 or get(n,14)!=pr['duration']-2 or u32(n,0x34) or u32(n,0x40) or get(n,0x48):raise ValueError('third existing persistent attached frame')
            used_nodes.add(p);nodes.append(p);n[1]=1;put(n,14,get(n,14)-1,'h');d['pool'][off:off+NODE]=n;p=u32(n,32)
        if p:raise ValueError('third exact captured children')
        if ended:aw[:]=clearing_project(aw)
        else:aw[1]=1;put(aw,14,get(aw,14)-1,'h')
        w[0x48:0xA0]=aw;w[4]=int(ended);put(w,10,2,'H')
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
        works[at:at+STRIDE]=w;units.append(dict(index=i,job=job,klass=klass,group=group,inactive=False,handler_return=0,main_return=int(ended),main_wait=get(aw,14),cleared_PC=ended,linked_order=nodes,cell=[cx,cy],event_region=event,vision_args=vision))
    put(d['current_work'],0,0);out=deepcopy(before)
    for row in out:row['hex']=d[row['name']].hex()
    return dict(after=out,units=units,unit_indices=indices,templates_activated=0,cleared_root_indices=[u['index'] for u in units if u.get('cleared_PC')],all250_slot_loop_completed=True,third_world_completed=False)
