"""Source remaining ten mode2 units and actual action1 world suffix."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_following_students import ROOT,SOURCE,SOURCE_SHA256,BASE,STRIDE,COUNT,data
from tools.school_scene_unit_work_catalog import source_catalog as scene_rules
from tools.school_scene_batch_emulation import batch_resource
from tools.school_scene_second_constructor_emulation import second_resource
from tools.school_scene_unit_constructor_emulation import scene_resource
from tools.school_student_action import program,frame_setup,put,u32
from tools.school_student_tail import regen,get
from tools.school_world_command import cell
from tools.school_world_lists import vision_merge
from tools.school_unitctrl_map_emulation import map_resource
from tools.school_world_tail import source_contract as tail_contract,idle_effects,EFFECT_STRIDE,SECONDARY_STRIDE

INDICES=list(range(240,250))


def resource(klass):
    if klass==383:return batch_resource(383,1)
    if klass==393:return batch_resource(393,0)
    if klass==387:return second_resource(387,0)
    if klass==4:return scene_resource(4,1)
    raise ValueError('remaining scene source class')


@lru_cache(maxsize=1)
def source_contract():
    exe=SOURCE.read_bytes()
    if hashlib.sha256(exe).hexdigest()!=SOURCE_SHA256:raise ValueError('world final executable identity')
    rules=scene_rules();jobs={};md=Cs(CS_ARCH_X86,CS_MODE_32)
    end=next(i.address+i.size for i in md.disasm(exe[0x476250-BASE:0x476250-BASE+2048],0x476250) if i.mnemonic=='ret')
    for klass,direction in ((383,2),(393,2),(387,3),(4,2)):
        rule=rules['jobs'][str(klass)];table=rule['animation_table_pointer'];positions=rule['position_table_pointer'];mapped=exe[0x610510-BASE+direction]
        lookup=exe[table-BASE+(8+mapped)*2:table-BASE+(8+mapped)*2+2];code=struct.unpack_from('<H',exe,positions-BASE+lookup[0]*2)[0]
        raw,identity,_=resource(klass);main=program(raw,code>>8,code&255);category=exe[0x6B2D8A-BASE+klass*64]
        jobs[str(klass)]={'class':klass,'direction':direction,'direction_index':mapped,'lookup_hex':lookup.hex(),'pose_code':code,'animation_table_pointer':table,'position_table_pointer':positions,
          'main_source':identity,'main':main,'category_mask':1<<(category-1) if 1<=category<=5 else 0}
    proof=[]
    checks={0x4762A9:('call','0x46bcc0'),0x4762B8:('mov','byte ptr [ecx], al'),0x4762C6:('je','0x4762cf'),0x4762C8:('xor','eax, eax'),
      0x46B586:('mov','dword ptr [0x7a49e0], 0'),0x46B59C:('je','0x46b618'),0x46B61B:('call','0x490fc0')}
    for va,wanted in checks.items():
        i=next(md.disasm(exe[va-BASE:va-BASE+16],va))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('world final exact operand '+hex(va))
        proof.append({'va':hex(va),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
    return {'source_image_sha256':SOURCE_SHA256,'mode2_body':{'va':'0x476250','end':hex(end),'sha256':hashlib.sha256(exe[0x476250-BASE:end-BASE]).hexdigest()},
      'instructions':proof,'jobs':jobs,'suffix_source':tail_contract(),'scope':'Remaining ten actual units and second46B470 return to declared driver; no outer task/180/VM completion'}


def ranges():
    s=source_contract();return ((0x476250,int(s['mode2_body']['end'],16)),(0x46B586,0x46B620))


def units_project(inputs,before):
    d=data(before);s=source_contract();ctrl=d['control'];units=[]
    if struct.unpack_from('<h',ctrl,2)[0]!=1 or (ctrl[4],ctrl[24],ctrl[26])!=(1,1,5) or any(ctrl[i] for i in (6,8,9,10)):raise ValueError('remaining actual opening/action gates')
    raw,mapid=map_resource('map05.bin');rel=bytes.fromhex(inputs['relation_matrix_hex'])
    if len(rel)!=256 or inputs['team']!=0 or inputs['map_sha256']!=mapid['sha256'] or inputs['map_all_bytes_verified']!=len(raw) or [u['index'] for u in inputs['units']]!=INDICES:raise ValueError('remaining complete map/relation/indices')
    for x,klass,job,group in zip(inputs['units'],[383]*7+[393,387,4],[383]*7+[393,387,5],[5]*7+[7,0,7]):
        i=x['index'];at=i*STRIDE;w=bytearray(d['works'][at:at+STRIDE]);ptr=before[0]['pointer']+at;rp=u32(w,0x258);roff=rp-before[1]['pointer'];rule=s['jobs'][str(klass)]
        if not 0<=roff<=len(d['records'])-176 or roff%176:raise ValueError('remaining exact record bounds')
        r=d['records'][roff:roff+176]
        if get(w,0)==0 or struct.unpack_from('<H',r,2)[0]!=job or struct.unpack_from('<H',r,12)[0]!=klass or r[15]!=1 or r[164]!=group or x['record_pointer']!=rp or x['record_hex']!=r.hex():raise ValueError('remaining complete actual record')
        if w[0x290]!=2 or w[0x292] or w[0x293] or w[0x2A7]!=int(group>=4) or w[0x28A]!=rule['direction'] or u32(w,0x518):raise ValueError('remaining mode2 initialization gates')
        for pos in [0x48]+[0xA0+n*88 for n in range(5)]:
            if u32(w,pos+0x20) or u32(w,pos+0x34) or u32(w,pos+0x40) or (pos!=0x48 and u32(w,pos+4)):raise ValueError('remaining empty children/events/auxiliaries')
        if get(w,0x48+0x48) or u32(w,0x510) or w[0x14] or w[0x34] or get(r,0x14)!=get(r,0x16) or get(r,0x1A)!=get(r,0x1C) or get(r,0x16)<=0:raise ValueError('remaining actual full values/zero frame delay')
        b=x['binding'];owner=bytes.fromhex(b['controller_hex']);main=rule['main']
        if len(owner)!=84 or u32(owner,0)!=b['metadata_pointer'] or b['owner']!=u32(w,0x44) or u32(owner,0x4C)!=rule['animation_table_pointer'] or u32(owner,0x50)!=rule['position_table_pointer'] or b['metadata_bytes']!=main['metadata_bytes'] or b['metadata_sha256']!=main['metadata_sha256'] or b['source_sha256']!=rule['main_source']['sha256']:raise ValueError('remaining full source metadata/pose tables')
        frame=bytes.fromhex(main['frame_hex'])
        if frame[0]&3 or frame[0]&12 or main['duration']<1:raise ValueError('remaining supported frame command')
        w[8]&=0x7F;aw=bytearray(w[0x48:0xA0]);put(aw,0xC,1,'h');aw[3]=bytes.fromhex(rule['lookup_hex'])[1]&3;aw[8]=0;put(aw,0x18,7)
        put(aw,0x12,0,'h');put(aw,0x14,0,'h');put(aw,0x24,ptr+0x48);aw[0xB]=0;put(aw,0x10,0,'h');frame_setup(aw,b['metadata_pointer']+main['offset'],main)
        aw[1]=1;timer=main['duration']-1;put(aw,0xE,timer,'h');done=int(timer<=0 and bool(frame[0]&128))
        if timer<=0 and not done:raise ValueError('remaining unsupported frame advance')
        aw[0xB]=done;w[0x48:0xA0]=aw;w[4]=done;put(w,10,1,'h');w[0x293]=1
        recovered=regen(w,r)
        if recovered['heals'] or recovered['record_hex']!=r.hex():raise ValueError('remaining no actual healing')
        w[:]=bytes.fromhex(recovered['work_hex']);px,py=struct.unpack_from('<2i',w,0x2EC);cx,cy=cell(px,32),cell(py,16)
        if not 0<=cx<64 or not 0<=cy<96 or list(w[0x4E7:0x4EB])!=[cx,cy,cx,cy]:raise ValueError('remaining stationary map cells')
        event=raw[16+(cy*64+cx)*6+2]
        if event<32:
            e=event*64+group*4;struct.pack_into('<H',d['region_stats'],e,(struct.unpack_from('<H',d['region_stats'],e)[0]+1)&65535);d['region_stats'][e+2]|=rule['category_mask']
        vision=None
        if group==inputs['team'] or rel[inputs['team']*16+group]==0:
            view=min(32,max(0,r[44]-256 if r[44]>=128 else r[44]));cur,hist=vision_merge(d['fog_current'],d['fog_history'],cx,cy,view);d['fog_current'][:]=cur;d['fog_history'][:]=hist;vision=[cx,cy,view]
        d['works'][at:at+STRIDE]=w;units.append({'index':i,'job':job,'class':klass,'group':group,'frame_wait':timer,'main_return':done,'cell':[cx,cy],'event_region':event,'category_mask':rule['category_mask'],'vision_args':vision,'post_handler_called':387<=job<=406})
    put(d['current_work'],0,0);out=deepcopy(before)
    for row in out:row['hex']=d[row['name']].hex()
    return {'after':out,'units':units,'units_completed':10,'all250_slot_loop_completed':True,'world_completed':False}


def suffix_project(inputs,before):
    source_contract();out=deepcopy(before)
    names=['cursor','window','menu','effects','secondary','control','outgoing_queue','incoming_queue','dispatch_mode','script_busy']
    sizes=[10,20,1,EFFECT_STRIDE*10,SECONDARY_STRIDE*5,50,20,20,1,1]
    if [r['name'] for r in out]!=names or [r['bytes'] for r in out]!=sizes:raise ValueError('enabled suffix complete regions')
    d={r['name']:bytearray.fromhex(r['hex']) for r in out}
    if any(len(d[n])!=b for n,b in zip(names,sizes)):raise ValueError('enabled suffix complete bytes')
    c=d['control']
    if struct.unpack_from('<h',c,2)[0]!=1 or (c[4],c[24],c[26])!=(1,1,5) or any(c[i] for i in (6,8,9,10)):raise ValueError('enabled suffix actual action1 gates')
    if inputs['pointer_xy']!=[-1,-1] or inputs['selection_count']!=0 or d['dispatch_mode']!=b'\0' or d['script_busy']!=b'\0':raise ValueError('enabled suffix closed input/driver')
    if any(d[n][8:20]!=bytes(12) for n in ('outgoing_queue','incoming_queue')) or any(d['secondary'][i*SECONDARY_STRIDE] for i in range(5)):raise ValueError('enabled suffix empty queues/secondary')
    d['cursor'][8]=0;d['window'][16]=0;d['menu'][0]=0;d['effects'][:]=idle_effects(d['effects'])
    for row in out:row['hex']=d[row['name']].hex()
    return out
