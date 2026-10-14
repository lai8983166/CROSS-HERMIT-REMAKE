"""Source-derived remaining friendly initializers, whole units and next loop gate."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.tactics_exit_emulation import ROOT,SOURCE,SOURCE_SHA256,BASE
from tools.school_first_unit_work_catalog import source_catalog as work_catalog
from tools.school_current_units_emulation import current_resource
from tools.school_unit_assets_emulation import effect_resource
from tools.school_student_action import program,frame_setup,u32,put,POOL,NODE,SLOTS
from tools.school_student_tail import regen,get
from tools.school_world_command import STRIDE,COUNT,cell
from tools.school_world_lists import vision_merge
from tools.school_unitctrl_map_emulation import map_resource

FUNCTIONS=(0x46B760,0x48D720,0x48E2A0,0x475700,0x4751F0,0x4697F0,0x475D60,0x46C040,0x46BCC0,
  0x465040,0x409FF0,0x409F70,0x40A400,0x40A520,0x468EB0,0x468D80,0x468E10,0x46BE50,0x465140,
  0x40AF40,0x40B5E0,0x409EF0,0x40A800,0x47A8E0,0x490350,0x490A50,0x40A100,0x468D10)


@lru_cache(maxsize=1)
def source_contract():
    exe=SOURCE.read_bytes()
    if hashlib.sha256(exe).hexdigest()!=SOURCE_SHA256:raise ValueError('following student source identity')
    md=Cs(CS_ARCH_X86,CS_MODE_32);functions=[]
    for va in FUNCTIONS:
        end=next((i.address+i.size for i in md.disasm(exe[va-BASE:va-BASE+8192],va) if i.mnemonic=='ret'),None)
        if end is None:raise ValueError('following complete source body')
        functions.append({'va':hex(va),'end':hex(end),'sha256':hashlib.sha256(exe[va-BASE:end-BASE]).hexdigest()})
    direction=exe[0x610512-BASE];efct,efctid=effect_resource();jobs={}
    for job,klass in ((4,6),(9,7)):
        rule=next(r for r in work_catalog()['jobs'] if r['job']==klass)
        lookup=exe[rule['animation_table_pointer']-BASE+(18*8+direction)*2:rule['animation_table_pointer']-BASE+(18*8+direction)*2+2]
        code=struct.unpack_from('<H',exe,rule['position_table_pointer']-BASE+lookup[0]*2)[0]
        raw,identity,_=current_resource(klass,1);main=program(raw,code>>8,code&255);attachments=[]
        for anim in (2063,2100+job):
            at=0x60F890-BASE+(anim//1000-1)*800+anim%1000*4;definition=exe[at:at+4]
            p=program(efct,definition[1],definition[2]);p.update(animation=anim,definition_hex=definition.hex());attachments.append(p)
        category=exe[0x6B2D8A-BASE+klass*64]
        jobs[str(job)]={'job':job,'class':klass,'main_source':identity,'main':main,'effect_source':efctid,
          'pose_lookup_hex':lookup.hex(),'pose_code':code,'animation_table_pointer':rule['animation_table_pointer'],
          'position_table_pointer':rule['position_table_pointer'],'attachments':attachments,'category':category,
          'category_mask':1<<(category-1) if 1<=category<=5 else 0}
    return {'source_image_sha256':SOURCE_SHA256,'functions':functions,'pose':18,'direction':2,'direction_index':direction,
      'jobs':jobs,'scope':'Remaining actual mode25 phase0 current friendly units through native return and slot215 entry only'}


def ranges():return tuple((int(r['va'],16),int(r['end'],16)) for r in source_contract()['functions'])


def data(regions):
    names=['works','records','region_stats','fog_current','fog_history','occupancy','pool','control','task','current_work']
    sizes=[STRIDE*COUNT,176*COUNT,2048,6144,6144,12288,NODE*SLOTS,50,400,4]
    if [r['name'] for r in regions]!=names or [r['bytes'] for r in regions]!=sizes:raise ValueError('following complete owned regions')
    out={r['name']:bytearray.fromhex(r['hex']) for r in regions}
    if any(len(out[n])!=size for n,size in zip(names,sizes)):raise ValueError('following complete owned byte lengths')
    return out


def project(inputs,before):
    d=data(before);s=source_contract();ctrl=d['control'];units=[]
    if struct.unpack_from('<h',ctrl,2)[0]!=1 or (ctrl[4],ctrl[24],ctrl[26])!=(1,1,5) or any(ctrl[i] for i in (6,9,10)):raise ValueError('following opening/action/command/AI gates')
    raw,mapid=map_resource('map05.bin')
    if inputs['map_sha256']!=mapid['sha256'] or inputs['map_all_bytes_verified']!=len(raw) or inputs['team']!=0:raise ValueError('following complete map/team identity')
    if [x['index'] for x in inputs['units']] not in ([1],[1,2]):raise ValueError('following captured current slots')
    for x in inputs['units']:
        i=x['index'];at=i*STRIDE;w=bytearray(d['works'][at:at+STRIDE]);ptr=before[0]['pointer']+at
        recptr=u32(w,0x258);roff=recptr-before[1]['pointer']
        if not 0<=roff<=len(d['records'])-176 or roff%176:raise ValueError('following source record bounds')
        r=d['records'][roff:roff+176];job=struct.unpack_from('<H',r,2)[0];klass=struct.unpack_from('<H',r,12)[0];rule=s['jobs'].get(str(job))
        if rule is None or klass!=rule['class'] or r[15]!=1 or r[164]!=0 or x['record_hex']!=r.hex() or x['record_pointer']!=recptr:raise ValueError('following full current source record')
        if get(w,0)==0 or w[0x290]!=25 or w[0x292] or w[0x293] or w[0x2A7] or u32(w,0x518) or u32(w,0x48+0x20):raise ValueError('following initial status/queue/child scope')
        if w[0x14] or w[0x34] or get(r,0x14)!=get(r,0x16) or get(r,0x1A)!=get(r,0x1C) or get(r,0x16)<=0:raise ValueError('following full-value view scope')
        for off in [0x48]+[0xA0+n*NODE for n in range(5)]:
            if u32(w,off+0x34) or u32(w,off+0x40) or (off!=0x48 and (u32(w,off+4) or u32(w,off+0x20))):raise ValueError('following empty events/auxiliary scope')
        if u32(w,0x510):raise ValueError('following empty damage scope')
        main=x['bindings'][0];effect=x['bindings'][1]
        for binding,p,identity in ((main,rule['main'],rule['main_source']),(effect,rule['attachments'][0],rule['effect_source'])):
            owner=bytes.fromhex(binding['controller_hex'])
            if len(owner)!=84 or u32(owner,0)!=binding['metadata_pointer'] or binding['metadata_bytes']!=p['metadata_bytes'] or binding['metadata_sha256']!=p['metadata_sha256'] or binding['source_sha256']!=identity['sha256']:raise ValueError('following complete source controller binding')
        owner=bytes.fromhex(main['controller_hex'])
        if u32(owner,0x4C)!=rule['animation_table_pointer'] or u32(owner,0x50)!=rule['position_table_pointer'] or main['owner']!=u32(w,0x44):raise ValueError('following source pose tables')
        w[8]&=0x7F;w[0x28A]=2;aw=bytearray(w[0x48:0xA0]);put(aw,0xC,18,'h');aw[3]=bytes.fromhex(rule['pose_lookup_hex'])[1]&3;aw[8]=0
        put(aw,0x18,7);put(aw,0x12,0,'h');put(aw,0x14,0,'h');put(aw,0x24,ptr+0x48);aw[0xB]=0;put(aw,0x10,0,'h')
        frame_setup(aw,main['metadata_pointer']+rule['main']['offset'],rule['main']);w[4]=0;put(w,10,0,'h');nodes=[]
        for p in rule['attachments']:
            n=next((n for n in range(SLOTS) if d['pool'][n*NODE]==0),None)
            if n is None:raise ValueError('following finite first-free pool')
            nodeptr=POOL+n*NODE;node=bytearray(NODE);node[0]=1;put(node,0xC,-1,'h');node[0x54:0x57]=bytes([128])*3
            definition=bytes.fromhex(p['definition_hex']);node[3]=(aw[3] if not definition[0]&128 else 128)|64
            put(node,0x1C,effect['owner']);node[2]=1;put(node,0x24,u32(aw,0x24));put(node,0x20,u32(aw,0x20));put(aw,0x20,nodeptr)
            node[0x12:0x16]=aw[0x12:0x16];node[8]=aw[8]+1;put(node,0x18,7)
            if u32(aw,0x2C):put(node,0x2C,u32(aw,0x2C));node[0x48:0x54]=aw[0x48:0x54]
            frame_setup(node,effect['metadata_pointer']+p['offset'],p);node[1]=1;put(node,0xE,p['duration']-2,'h')
            d['pool'][n*NODE:(n+1)*NODE]=node;nodes.append(nodeptr)
        aw[1]=1;put(aw,0xE,rule['main']['duration']-1,'h');w[0x48:0xA0]=aw;w[4]=0;put(w,10,1,'H')
        px,py=struct.unpack_from('<2i',w,0x2EC);cx,cy=cell(px,32),cell(py,16)
        if list(w[0x4E7:0x4EB])!=[cx,cy,cx,cy] or not 0<=cx<64 or not 0<=cy<96:raise ValueError('following stationary source cell')
        w[0x2E8:0x2EA]=bytes([cx,cy]);w[0x293]=1;recovered=regen(w,r)
        if recovered['record_hex']!=r.hex() or recovered['heals']:raise ValueError('following no actual healing')
        w[:]=bytes.fromhex(recovered['work_hex']);event=raw[16+(cy*64+cx)*6+2]
        if event<32:
            t=event*64;count=(struct.unpack_from('<H',d['region_stats'],t)[0]+1)&65535
            struct.pack_into('<H',d['region_stats'],t,count);d['region_stats'][t+2]|=rule['category_mask']
        view=min(32,max(0,r[44]-256 if r[44]>=128 else r[44]));cur,hist=vision_merge(d['fog_current'],d['fog_history'],cx,cy,view);d['fog_current'][:]=cur;d['fog_history'][:]=hist
        d['works'][at:at+STRIDE]=w;put(d['current_work'],0,ptr)
        units.append({'index':i,'job':job,'class':klass,'allocated_nodes':nodes,'linked_order':nodes[::-1],'frame_waits':[29,4,28],
          'cell':[cx,cy],'event_region':event,'category_mask':rule['category_mask'],'vision_args':[cx,cy,view]})
    # The original loop tests every intervening empty slot and admits215 next.
    if any(get(d['works'],i*STRIDE) for i in range(inputs['units'][-1]['index']+1,215)) or not get(d['works'],215*STRIDE):raise ValueError('following exact empty interval/next occupied slot')
    out=deepcopy(before)
    for row in out:row['hex']=d[row['name']].hex()
    return {'after':out,'units':units,'next_slot':215,'friendly_unit_updates_completed':len(units),'world_completed':False}
