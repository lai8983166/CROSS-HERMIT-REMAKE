"""Source-only first scene role406 initializer, terminal animation and unit tail."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_following_students import ROOT,SOURCE,SOURCE_SHA256,BASE,STRIDE,COUNT,data
from tools.school_scene_unit_work_catalog import source_catalog as scene_rules
from tools.school_scene_remaining_emulation import remaining_resource
from tools.school_student_action import program,frame_setup,put,u32
from tools.school_student_tail import regen,get
from tools.school_world_command import cell
from tools.school_world_lists import vision_merge
from tools.school_unitctrl_map_emulation import map_resource

INDEX=217
FUNCTIONS=(0x4761C0,0x480A60,0x46B0B0,0x46B0F0,0x46BCC0,0x465040,0x409FF0,
  0x40A100,0x40A800,0x46A430,0x46A5E0,0x4305C0)


@lru_cache(maxsize=1)
def source_contract():
    exe=SOURCE.read_bytes()
    if hashlib.sha256(exe).hexdigest()!=SOURCE_SHA256:raise ValueError('scene first source identity')
    md=Cs(CS_ARCH_X86,CS_MODE_32);bodies=[]
    for va in FUNCTIONS:
        end=next(i.address+i.size for i in md.disasm(exe[va-BASE:va-BASE+8192],va) if i.mnemonic=='ret')
        bodies.append({'va':hex(va),'end':hex(end),'sha256':hashlib.sha256(exe[va-BASE:end-BASE]).hexdigest()})
    rule=scene_rules()['jobs']['406'];raw,identity,_=remaining_resource(406,0);direction=exe[0x610519-BASE]
    table=rule['animation_table_pointer'];positions=rule['position_table_pointer'];at=table-BASE+(8+direction)*2;lookup=exe[at:at+2]
    code=struct.unpack_from('<H',exe,positions-BASE+lookup[0]*2)[0];main=program(raw,code>>8,code&255)
    if bytes.fromhex(main['frame_hex'])[0]!=0x80 or main['duration']!=1:raise ValueError('scene exact terminal frame')
    if struct.unpack_from('<I',exe,0x475CE3-BASE+28*4)[0]!=0x475BD1:raise ValueError('scene mode28 second-table dispatch')
    checks={0x475BD8:('call','0x4761c0'),0x475C50:('call','0x480a60'),0x480A89:('je','0x480a92'),
      0x480A8B:('xor','eax, eax'),0x40A92D:('and','edx, 0x80'),0x40A93A:('mov','byte ptr [eax + 0xb], 1'),
      0x40A93E:('mov','eax, 1'),0x46A66E:('movsx','edx, byte ptr [eax + ecx]')}
    proof=[]
    for va,wanted in checks.items():
        i=next(md.disasm(exe[va-BASE:va-BASE+16],va))
        if (i.mnemonic,i.op_str)!=wanted:raise ValueError('scene source exact operand '+hex(va))
        proof.append({'va':hex(va),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
    category=exe[0x6B2D8A-BASE+406*64]
    return {'source_image_sha256':SOURCE_SHA256,'functions':bodies,'instructions':proof,'job':406,'group':6,
      'pose':1,'direction':9,'direction_index':direction,'pose_lookup_hex':lookup.hex(),'pose_code':code,
      'animation_table_pointer':table,'position_table_pointer':positions,'main_source':identity,'main':main,
      'category':category,'category_mask':1<<(category-1) if 1<=category<=5 else 0,
      'scope':'Original scene217 initializer and terminal-frame first unit return; no release/next unit/world/AI/VM completion'}


def ranges():return tuple((int(r['va'],16),int(r['end'],16)) for r in source_contract()['functions'])


def project(inputs,before,phase):
    if phase not in ('initializer','complete'):raise ValueError('scene bounded phase')
    d=data(before);s=source_contract();ctrl=d['control'];at=INDEX*STRIDE;w=bytearray(d['works'][at:at+STRIDE]);ptr=before[0]['pointer']+at
    if struct.unpack_from('<h',ctrl,2)[0]!=1 or (ctrl[4],ctrl[24],ctrl[26])!=(1,1,5) or any(ctrl[i] for i in (6,9,10)):raise ValueError('scene actual action/opening gates')
    rp=u32(w,0x258);off=rp-before[1]['pointer']
    if not 0<=off<=len(d['records'])-176 or off%176:raise ValueError('scene source record bounds')
    r=d['records'][off:off+176]
    if struct.unpack_from('<H',r,2)[0]!=406 or struct.unpack_from('<H',r,12)[0]!=406 or r[15]!=1 or r[164]!=6 or inputs['record_pointer']!=rp or inputs['record_hex']!=r.hex():raise ValueError('scene complete actual source record')
    if not get(w,0) or w[0x28A]!=9 or w[0x290]!=28 or w[0x292] or w[0x293] or w[0x2A7]!=1 or u32(w,0x518):raise ValueError('scene initial mode/phase/closed work queue')
    binding=inputs['main_binding'];owner=bytes.fromhex(binding['controller_hex']);main=s['main']
    if len(owner)!=84 or u32(owner,0)!=binding['metadata_pointer'] or u32(owner,0x4C)!=s['animation_table_pointer'] or u32(owner,0x50)!=s['position_table_pointer'] or binding['owner']!=u32(w,0x44) or binding['metadata_bytes']!=main['metadata_bytes'] or binding['metadata_sha256']!=main['metadata_sha256'] or binding['source_sha256']!=s['main_source']['sha256']:raise ValueError('scene full source metadata/controller tables')
    for pos in [0x48]+[0xA0+n*88 for n in range(5)]:
        if u32(w,pos+0x20) or u32(w,pos+0x34) or u32(w,pos+0x40) or (pos!=0x48 and u32(w,pos+4)):raise ValueError('scene empty linked/effect/damage/auxiliary scope')
    if get(w,0x48+0x48)!=0 or u32(w,0x510) or w[0x14] or w[0x34]:raise ValueError('scene unmodified view/zero frame queue delay/empty damage scope')
    if get(r,0x14)!=get(r,0x16) or get(r,0x1A)!=get(r,0x1C) or get(r,0x16)<=0:raise ValueError('scene actual full values')
    relation=bytes.fromhex(inputs['relation_matrix_hex']);raw,mapid=map_resource('map05.bin')
    if len(relation)!=256 or inputs['team']!=0 or inputs['map_sha256']!=mapid['sha256'] or inputs['map_all_bytes_verified']!=len(raw):raise ValueError('scene complete source map/relation inputs')
    w[8]&=0x7F;w[6]=1;w[7]=1;aw=bytearray(w[0x48:0xA0]);put(aw,0xC,1,'h');aw[3]=bytes.fromhex(s['pose_lookup_hex'])[1]&3;aw[8]=0
    put(aw,0x18,7);put(aw,0x12,0,'h');put(aw,0x14,0,'h');put(aw,0x24,ptr+0x48);aw[0xB]=0;put(aw,0x10,0,'h')
    frame_setup(aw,binding['metadata_pointer']+main['offset'],main);w[0x48:0xA0]=aw;w[4]=0;put(w,10,0,'h');w[0x293]=1
    put(d['current_work'],0,ptr);event=None;vision=None;animation_return=None
    if phase=='complete':
        aw[1]=1;put(aw,0xE,0,'h');aw[0xB]=1;w[0x48:0xA0]=aw;w[4]=1;put(w,10,1,'h');animation_return=1
        recovered=regen(w,r)
        if recovered['heals'] or recovered['record_hex']!=r.hex():raise ValueError('scene no actual heal')
        w[:]=bytes.fromhex(recovered['work_hex']);px,py=struct.unpack_from('<2i',w,0x2EC);cx,cy=cell(px,32),cell(py,16)
        if not 0<=cx<64 or not 0<=cy<96 or list(w[0x4E7:0x4EB])!=[cx,cy,cx,cy]:raise ValueError('scene stationary map cell')
        event=raw[16+(cy*64+cx)*6+2]
        if event<32:
            e=event*64+r[164]*4;struct.pack_into('<H',d['region_stats'],e,(struct.unpack_from('<H',d['region_stats'],e)[0]+1)&65535);d['region_stats'][e+2]|=s['category_mask']
        own=inputs['team']==r[164];allied=not own and relation[inputs['team']*16+r[164]]==0
        if own or allied:
            view=min(32,max(0,r[44]-256 if r[44]>=128 else r[44]));cur,hist=vision_merge(d['fog_current'],d['fog_history'],cx,cy,view);d['fog_current'][:]=cur;d['fog_history'][:]=hist;vision=[cx,cy,view]
    d['works'][at:at+STRIDE]=w;out=deepcopy(before)
    for row in out:row['hex']=d[row['name']].hex()
    return {'after':out,'post_handler_return':0,'main_animation_return':animation_return,'event_region':event,'category_mask':s['category_mask'],
      'vision_args':vision,'unit_completed':phase=='complete','next_slot':218 if phase=='complete' else None,'world_completed':False}
