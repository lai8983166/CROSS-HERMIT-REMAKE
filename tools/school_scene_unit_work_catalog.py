"""Independent source-derived scene work/status/resource prefix rules."""
import argparse
from copy import deepcopy
import hashlib
import json
import struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from capstone.x86_const import X86_OP_IMM,X86_OP_MEM
from tools.tactics_exit_emulation import ROOT,SOURCE,SOURCE_SHA256,BASE,report_text
from tools.school_course_unlock_emulation import AUTHORITY
from tools.school_first_unit_work_catalog import source_catalog as base_catalog
from tools.school_enemy_records_catalog import source_catalog as record_catalog,expected_record
from tools.dxanim_lib import parse_dxanim,parse_container,parse_block4_descriptors,DxAnimError

EVIDENCE=ROOT/'analysis/school-scene-unit-work-v1-20261010.json'
EVIDENCE_SHA256='74c4c43d8befdffcdaac206955956d919f1437e3a1ce808dbfc0a969b6e1d5e7'
COUNTER_EVIDENCE=ROOT/'analysis/school-scene-unit-work-counter-v1-20261010.json'
COUNTER_SHA256='fe80cd0e5e0b938364e9bf6d772266e8d33f9d44719add18ea1dd802afd387be'


def archive_inventory(raw):
    try:
        offsets=parse_dxanim(raw)
        if len(offsets)!=9:raise ValueError('scene archive section count')
        sections=[]
        for i in range(8):
            start,end=offsets[i:i+2]
            if start==end:
                sections.append({'section':i,'start':start,'end':end,'count':0,'empty':True});continue
            if i in (4,5):
                count=len(parse_block4_descriptors(raw,offsets)) if i==4 else (end-start)//8
                if i==5 and (end-start)%8:raise ValueError('scene archive canvas ownership')
                sections.append({'section':i,'start':start,'end':end,'count':count,'empty':False,'encoding':'raw_records'});continue
            size,count,entries=parse_container(raw,start)
            if not 0<size<=end-start or (i>=6 and size!=end-start) or any(p>end-start for p in entries):raise ValueError('scene archive section ownership')
            sections.append({'section':i,'start':start,'end':end,'count':count,'header_length':size,'empty':False})
        count=sections[6]['count']
        if count<=0 or offsets[8]+((count+3)&~3)!=len(raw) or any(v not in (0,1) for v in raw[offsets[8]:offsets[8]+count]):
            raise ValueError('scene archive mask ownership')
        return {'offsets':offsets,'sections':sections,'image_count':count,'palette_count':sections[7]['count'],
            'mask_sha256':hashlib.sha256(raw[offsets[8]:offsets[8]+count]).hexdigest(),'native_loaded':False}
    except (DxAnimError,struct.error) as error:
        raise ValueError('scene archive malformed') from error


def source_catalog():
    image=SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest()!=SOURCE_SHA256:raise ValueError('scene work source identity')
    md=Cs(CS_ARCH_X86,CS_MODE_32);md.detail=True;code=[]
    def ins(va,mnemonic):
        i=next(md.disasm(image[va-BASE:va-BASE+16],va,count=1))
        if i.mnemonic!=mnemonic:raise ValueError(f'scene source instruction differs at {va:#x}')
        code.append({'va':hex(va),'instruction_hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str});return i
    def immediate(va,mnemonic,index=-1):
        operand=ins(va,mnemonic).operands[index]
        if operand.type not in (X86_OP_IMM,X86_OP_MEM):raise ValueError('scene source constant operand')
        return operand.imm if operand.type==X86_OP_IMM else operand.mem.disp
    common=base_catalog();records=record_catalog()
    status_base=immediate(0x475084,'add');status_bytes=immediate(0x475090,'mov')*4
    overlay_source=immediate(0x4DA765,'add');overlay_dest=immediate(0x4DA76B,'add');overlay_bytes=immediate(0x4DA771,'mov')*4
    resets=[]
    for va in (0x4DA77B,0x4DA788,0x4DA795,0x4DA7A2,0x4DA7AF,0x4DA7B9):
        dest,value=ins(va,'mov').operands
        if dest.type!=X86_OP_MEM or value.type!=X86_OP_IMM:raise ValueError('scene source overlay reset')
        resets.append({'offset':dest.mem.disp,'bytes':dest.size,'value':value.imm})
    mode_base=immediate(0x46C0A7,'sub');mode_max=immediate(0x46C0AF,'cmp')
    mode_switch=immediate(0x46C0C0,'jmp');mode_selector=immediate(0x46C0BA,'mov')
    switch=list(struct.unpack_from('<2I',image,mode_switch-BASE))
    mode_cases=[]
    for target in struct.unpack_from('<5I',image,0x46C33C-BASE):
        store=next(i for i in md.disasm(image[target-BASE:target-BASE+16],target) if i.mnemonic=='mov' and i.operands[0].type==X86_OP_MEM)
        ins(store.address,'mov');mode_cases.append(store.operands[1].imm)
    relation_cases=[]
    for target in struct.unpack_from('<4I',image,0x46AA22-BASE):relation_cases.append(immediate(target,'mov'))
    jobs={};archives={}
    for template in records['templates']:
        record=bytes.fromhex(expected_record(template,rules=records)['record_hex']);job=struct.unpack_from('<H',record,12)[0]
        if str(job) in jobs:continue
        at=common['source_tables']['job']+job*8;path_ptr,group,mode,variant=struct.unpack_from('<IhBb',image,at-BASE)
        path=image[path_ptr-BASE:path_ptr-BASE+260].split(b'\0',1)[0].decode('ascii')
        if group!=job or mode not in (0,1,2) or not path.startswith('data\\DxAnim\\'):raise ValueError('scene source unsupported job')
        animation=group+8
        j={'job':job,'table_pointer':at,'row_hex':image[at-BASE:at-BASE+8].hex(),'filename_pointer':path_ptr,
            'group':group,'mode':mode,'fixed_variant':variant,'relative_path':path,'animation_id':animation,
            'animation_table_pointer':struct.unpack_from('<I',image,common['source_tables']['animation']-BASE+animation*4)[0],
            'position_table_pointer':struct.unpack_from('<I',image,common['source_tables']['position']-BASE+animation*4)[0]}
        if mode==2:j['palettes_by_character']=list(struct.unpack_from('<35b',image,common['source_tables']['palette']-BASE+job*40))
        jobs[str(job)]=j
        if path not in archives:
            file=ROOT/'CROSS HERMIT/CROSS HERMIT'/path.replace('\\','/');raw=file.read_bytes()
            archives[path]={'path':file.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),**archive_inventory(raw)}
    from tools.school_scene_unit_work_emulation import PREFIX_RANGES
    bodies=[{'start':hex(a),'end':hex(b),'sha256':hashlib.sha256(image[a-BASE:b-BASE]).hexdigest(),
        'instruction_hex':image[a-BASE:b-BASE].hex()} for a,b in PREFIX_RANGES]
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'common':{k:deepcopy(common[k]) for k in (
        'work_bytes','work_offset','record_stride','record_offset','record_pointer_offset','work_stores','record_stores',
        'mode_field','mode_value','classification_offset','classification_limit','status_work_offset',
        'status_template_offset','status_template_hex','status_by_record','controller_bytes','controller_stores',
        'cache_offset','cache_count','cache_stride','counter_offset')},
        'templates':deepcopy(records['templates']),'template_pointer':records['template_pointer'],
        'scene_status_template_pointer':status_base,'scene_status_template_hex':image[status_base-BASE:status_base-BASE+status_bytes].hex(),
        'scene_overlay':{'source':overlay_source,'destination':overlay_dest,'bytes':overlay_bytes,'resets':resets,
            'record_source':immediate(0x4DA7CC,'mov'),'record_destination':immediate(0x4DA7D0,'mov',0)},
        'mode_dispatch':{'role_base':mode_base,'role_max_delta':mode_max,
            'selector_hex':image[mode_selector-BASE:mode_selector-BASE+mode_max+1].hex(),
            'targets':switch,'special_target':0x46C0C7,'mode_cases':mode_cases,'relation_cases':relation_cases},
        'jobs':jobs,'archives':archives,'code_inputs':common['code_inputs']+code,'source_branch_bodies':bodies,
        'scope':'Scene5 uncached work/controller prefixes only; archive inventory read-only, no native archive loading or completed scene loop/constructor/placement/VM.',**AUTHORITY}


def expected_prefix(record_hex,ordinal,cache_hex,counter,renderer,controller,selector,relation_hex,rules=None,template_hex=None):
    r=source_catalog() if rules is None else rules;c=r['common']
    try:record=bytearray.fromhex(record_hex);cache=bytearray.fromhex(cache_hex);relation=bytes.fromhex(relation_hex)
    except (TypeError,ValueError) as error:raise ValueError('scene prefix byte encoding') from error
    if type(ordinal) is not int or not 0<=ordinal<35 or len(record)!=176 or len(cache)!=c['cache_count']*8 or len(relation)!=256:
        raise ValueError('scene prefix input ownership')
    for value,limit in ((counter,256),(renderer,2**32),(controller,2**32),(selector,16)):
        if type(value) is not int or not 0<=value<limit:raise ValueError('scene prefix scalar input')
    role,job=struct.unpack_from('<H',record,2)[0],struct.unpack_from('<H',record,12)[0]
    try:template=bytes.fromhex(r['templates'][ordinal] if template_hex is None else template_hex)
    except (TypeError,ValueError) as error:raise ValueError('scene prefix template encoding') from error
    if len(template)!=84:raise ValueError('scene prefix template ownership')
    category=record[c['classification_offset']]
    if role!=struct.unpack_from('<h',template)[0] or str(job) not in r['jobs'] or category>=16 or record[15] not in (0,1):
        raise ValueError('scene prefix unsupported identity/category/job/state')
    j=r['jobs'][str(job)]
    if j['mode']==0:variant=0
    elif j['mode']==1:variant=j['fixed_variant']
    elif role<=34 and job<=39:
        palette=j['palettes_by_character'][role];variant=palette+1 if palette else 0
    else:variant=0
    if not 0<=variant<=40:raise ValueError('scene prefix unsupported variant')
    if any(cache[i*8] not in (0,1) for i in range(c['cache_count'])):raise ValueError('scene prefix malformed cache')
    if any(cache[i*8]==1 and struct.unpack_from('<H',cache,i*8+2)[0]==j['group'] for i in range(c['cache_count'])):
        raise ValueError('scene prefix cache hit outside verified scope')
    slots=[i for i in range(c['cache_count']) if cache[i*8]==0]
    if not slots:raise ValueError('scene prefix cache exhausted')
    slot=slots[0];index=249-ordinal;work=bytearray(c['work_bytes'])
    for s in c['work_stores']:work[s['offset']:s['offset']+s['bytes']]=s['value'].to_bytes(s['bytes'],'little')
    struct.pack_into('<H',work,2,index)
    struct.pack_into('<I',work,c['record_pointer_offset'],0xE000190+c['record_offset']+index*c['record_stride'])
    mode=c['mode_value'];dispatch=r['mode_dispatch'];delta=role-dispatch['role_base']
    if 0<=delta<=dispatch['role_max_delta'] and dispatch['targets'][bytes.fromhex(dispatch['selector_hex'])[delta]]==dispatch['special_target']:
        value=0 if category==selector else dispatch['relation_cases'][relation[selector*16+category]] if relation[selector*16+category]<=3 else -1
        if not 0<=value<len(dispatch['mode_cases']):raise ValueError('scene prefix unsupported relation')
        mode=dispatch['mode_cases'][value]
    work[c['mode_field']]=mode
    friendly=category<c['classification_limit'];at=c['status_work_offset']+c['status_template_offset']
    work[at:at+64]=bytes.fromhex(c['status_template_hex'] if friendly else r['scene_status_template_hex'])
    if not friendly:work[c['status_work_offset']+0x17]=1
    for s in c['record_stores']:
        if s['offset'] in (0x9F,0xA0) and not friendly:continue
        record[s['offset']:s['offset']+s['bytes']]=s['value'].to_bytes(s['bytes'],'little')
    if not friendly:
        o=r['scene_overlay'];work[o['destination']:o['destination']+o['bytes']]=template[o['source']:o['source']+o['bytes']]
        for s in o['resets']:work[s['offset']:s['offset']+s['bytes']]=s['value'].to_bytes(s['bytes'],'little')
        record[o['record_destination']:o['record_destination']+2]=template[o['record_source']:o['record_source']+2]
    work[c['status_work_offset']]=c['status_by_record']['inactive'] if record[15]!=1 else c['status_by_record']['character'] if friendly and 1<=role<=45 else c['status_by_record']['other']
    obj=bytearray(c['controller_bytes'])
    for s in c['controller_stores']:obj[s['offset']:s['offset']+s['bytes']]=s['value'].to_bytes(s['bytes'],'little')
    struct.pack_into('<I',obj,0x28,counter);struct.pack_into('<I',obj,0x44,renderer)
    struct.pack_into('<H',obj,0x48,j['animation_id']);struct.pack_into('<II',obj,0x4C,j['animation_table_pointer'],j['position_table_pointer'])
    struct.pack_into('<BBHI',cache,slot*8,1,variant,j['group'],controller)
    return {'work_hex':work.hex(),'record_hex':record.hex(),'cache_hex':cache.hex(),'controller_hex':obj.hex(),
        'counter':counter+1,'cache_slot':slot,'resource_args':[j['filename_pointer'],variant,int(variant!=0),0],
        'relative_path':j['relative_path']}


def native_fixture():
    raw=EVIDENCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('frozen scene prefix evidence differs')
    full=json.loads(raw);fields=('name','ready','scene_unit_work_prefix_initialized','scene_unit_work','stop_reason',
        'persistent_ranges_unchanged','battle_world_constructed')
    return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,
        'cases':[{k:deepcopy(c[k]) for k in fields if k in c} for c in full['cases']],
        'declared_scene_prefix_diagnostic':deepcopy(full['declared_scene_prefix_diagnostic']),**AUTHORITY}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--rules-out',required=True);p.add_argument('--fixture-out',required=True);a=p.parse_args()
    for path,data in ((a.rules_out,source_catalog()),(a.fixture_out,native_fixture())):
        (ROOT/path).write_text(report_text(data),encoding='utf-8',newline='\n')
