"""Independent EXE action/default inputs and first constructor byte rules."""
import argparse
from copy import deepcopy
import hashlib
import json
import struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from capstone.x86_const import X86_OP_IMM,X86_OP_MEM
from tools.school_first_unit_work_catalog import source_catalog as prefix_catalog
from tools.school_first_unit_animation_emulation import unit_resource
from tools.school_unitctrl_map_emulation import map_resource
from tools.dxanim_lib import parse_dxanim,parse_program_blocks
from tools.tactics_exit_emulation import ROOT,SOURCE,SOURCE_SHA256,BASE,report_text
from tools.school_course_unlock_emulation import AUTHORITY

EVIDENCE = ROOT/'analysis/school-first-unit-constructor-v2-20261010.json'
EVIDENCE_SHA256 = '406331ecf5f8441f17d56a34a0324a16c9be9c68f610b208e532f3a7a8faf921'


def source_catalog():
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest()!=SOURCE_SHA256:
        raise ValueError('first constructor executable identity')
    md = Cs(CS_ARCH_X86,CS_MODE_32);md.detail = True
    code = []
    def instruction(va,mnemonic):
        i = next(md.disasm(image[va-BASE:va-BASE+16],va,count=1))
        if i.mnemonic!=mnemonic:
            raise ValueError(f'constructor source instruction differs at {va:#x}')
        code.append({'va':hex(va),'instruction_hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
        return i
    def constant(va,mnemonic,index=-1):
        op = instruction(va,mnemonic).operands[index]
        if op.type==X86_OP_IMM:return op.imm
        if op.type==X86_OP_MEM:return op.mem.disp
        raise ValueError('constructor source constant operand')
    def stores(start,end):
        result = []
        for i in md.disasm(image[start-BASE:end-BASE],start):
            if i.mnemonic!='mov' or len(i.operands)!=2:continue
            dest,value = i.operands
            if dest.type!=X86_OP_MEM or value.type!=X86_OP_IMM or md.reg_name(dest.mem.base)=='ebp' or dest.mem.index:continue
            result.append({'offset':dest.mem.disp,'bytes':dest.size,'value':value.imm&((1<<(dest.size*8))-1)})
            instruction(i.address,'mov')
        return result
    selector = constant(0x46BD79,'mov')
    jump = constant(0x46BD7F,'jmp')
    arms = list(struct.unpack_from('<7I',image,jump-BASE))
    actions = [constant(a,'push') for a in arms[:5]]
    actions += [None,None]
    status_actions = [actions[s] for s in image[selector-BASE:selector-BASE+25]]
    directions = constant(0x4650AE,'mov')
    prefix = prefix_catalog()
    j = next(j for j in prefix['jobs'] if j['job']==10)
    raw,identity = unit_resource();offsets = parse_dxanim(raw)
    programs = parse_program_blocks(raw)
    map_raw,map_identity = map_resource('map05.bin')
    dimensions = list(struct.unpack_from('<HH',map_raw,4))
    table = j['animation_table_pointer']
    positions = j['position_table_pointer']
    position_count = len(programs[0])
    constants = {'work_offset':prefix['work_offset'],'work_bytes':prefix['work_bytes'],
        'record_offset':prefix['record_offset'],'record_bytes':prefix['record_stride'],
        'animation_bytes':constant(0x409F0D,'push'),
        'image_bytes':constant(0x437CAD,'push'),'shared_bytes':constant(0x480F78,'push'),
        'shared_offset':constant(0x480F70,'add'),'shared_count':constant(0x480FA0,'cmp'),
        'shared_value':constant(0x480FAC,'mov'),'aux_count':constant(0x467195,'cmp'),
        'aux_stride':constant(0x46719E,'imul'),'aux_offset':constant(0x4671A4,'lea'),
        'context_offset':constant(0x46716B,'add'),'role_table':constant(0x466FEC,'lea'),
        'friendly_timeout':constant(0x4683EB,'mov'),'other_timeout':constant(0x4683F9,'mov'),
        'friendly_category_limit':constant(0x468DE2,'cmp'),
        'x_shift':constant(0x468745,'shl'),'x_center':constant(0x468748,'add'),
        'y_shift':constant(0x46875B,'shl'),'y_center':constant(0x46875E,'add')}
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'source':identity,
        'constants':constants,'status_actions':status_actions,
        'direction_map':list(image[directions-BASE:directions-BASE+10]),
        'action_table_pointer':table,'action_rows':[image[table-BASE+i*16:table-BASE+(i+1)*16].hex() for i in range(25)],
        'position_table_pointer':positions,'position_words':list(struct.unpack_from('<'+str(position_count)+'H',image,positions-BASE)),
        'role_defaults_hex':image[constants['role_table']-BASE:constants['role_table']-BASE+70].hex(),
        'animation_stores':stores(0x409F1D,0x409F5C),'image_stores':stores(0x437CC0,0x437CF2),
        'work_stores':stores(0x468301,0x4683A0),
        'select_stores':stores(0x40A091,0x40A0D6),
        'program_sections':offsets[:5],'programs':programs,'metadata_bytes':offsets[6],
        'descriptor_hex':raw[offsets[4]:offsets[5]].hex(),'code_inputs':code,
        'logical_map_source':map_identity,'logical_dimensions':dimensions,
        'source_branch_bodies':[{'start':hex(a),'end':hex(b),'instruction_hex':image[a-BASE:b-BASE].hex(),
            'sha256':hashlib.sha256(image[a-BASE:b-BASE]).hexdigest()} for a,b in
            ((0x46509E,0x465126),(0x40A567,0x40A774),(0x468741,0x4687F2),(0x468DD1,0x468DF0),(0x468443,0x468630))],
        'scope':'Friendly role IDs1..34, job10, valid direction1..9, initial opcode0 without event bits. Exactly one constructor; no scene placement/GPU.',**AUTHORITY}


def expected_constructor(before_work_hex,record_hex,work_pointer,controller_pointer,metadata_pointer,before_cm_hex,rules=None):
    r = source_catalog() if rules is None else rules
    width,height = r['logical_dimensions']
    if (width,height)!=(64,96):raise ValueError('unsupported constructor logical map')
    try:
        work,record,cm = bytearray.fromhex(before_work_hex),bytes.fromhex(record_hex),bytearray.fromhex(before_cm_hex)
    except (TypeError,ValueError) as error:
        raise ValueError('constructor input encoding') from error
    if len(work)!=r['constants']['work_bytes'] or len(record)!=r['constants']['record_bytes'] or len(cm)!=width*height*2:
        raise ValueError('constructor input size')
    if struct.unpack_from('<H',work)[0]!=1 or struct.unpack_from('<H',work,2)[0]>=250 or any(work[0x44:0x258]):
        raise ValueError('constructor input is not an unbound initialized work')
    pointers = (work_pointer,controller_pointer,metadata_pointer)
    if any(type(p) is not int or p<=0 or p%4 or p+n>0x100000000 for p,n in zip(pointers,(len(work),84,r['metadata_bytes']))):
        raise ValueError('constructor pointer bounds/alignment')
    spans = [(p,p+n) for p,n in zip(pointers,(len(work),84,r['metadata_bytes']))]
    if any(max(a,b)<min(x,y) for i,(a,x) in enumerate(spans) for b,y in spans[i+1:]):
        raise ValueError('constructor pointer overlap')
    role,job = struct.unpack_from('<H',record,2)[0],struct.unpack_from('<H',record,12)[0]
    if not 1<=role<=34 or job!=10 or record[0xA4]>=r['constants']['friendly_category_limit'] or record[0xF]!=1:
        raise ValueError('unsupported first constructor role/job/state/category')
    status,direction = work[0x290],work[0x28A]
    if not 1<=status<=len(r['status_actions']) or r['status_actions'][status-1] is None or not 1<=direction<=9:
        raise ValueError('unsupported first constructor status/direction')
    x,y = record[0x9B:0x9D]
    if x>=width or y>=height:raise ValueError('constructor coordinates outside logical map')
    c = r['constants']
    index = struct.unpack_from('<H',work,2)[0]
    receiver = work_pointer-(c['work_offset']+index*c['work_bytes'])
    if struct.unpack_from('<I',work,0x258)[0]!=receiver+c['record_offset']+index*c['record_bytes']:
        raise ValueError('constructor copied record ownership')
    def put(at,value,size=4):work[at:at+size]=value.to_bytes(size,'little')
    def defaults(at,size,stores):
        work[at:at+size] = bytes(size)
        for s in stores:put(at+s['offset'],s['value'],s['bytes'])
    put(0x44,controller_pointer)
    for offset in [0x48,*[c['aux_offset']+i*c['aux_stride'] for i in range(c['aux_count'])]]:
        defaults(offset,c['animation_bytes'],r['animation_stores'])
        put(offset+0x1C,controller_pointer);put(offset+0x24,work_pointer+offset)
    context = receiver+c['context_offset']
    if not 0<context<0x100000000:raise ValueError('constructor context pointer')
    put(0x74,context);put(0xCC,context)
    action = r['status_actions'][status-1]
    mapped = r['direction_map'][direction]
    row = bytes.fromhex(r['action_rows'][action])
    index,flags = row[mapped*2:mapped*2+2]
    if index>=len(r['position_words']):raise ValueError('constructor action position index')
    position = r['position_words'][index];block,animation = position>>8,position&255
    if block>=4 or animation>=len(r['programs'][block]):raise ValueError('constructor animation index')
    program = r['programs'][block][animation]
    if not program or program[0]['opcode']!=0 or program[0]['flags']&12:
        raise ValueError('unsupported first constructor initial animation opcode/events')
    raw = bytes.fromhex(program[0]['raw'])
    section = r['program_sections'][block]
    archive,_ = unit_resource()
    first_offset = section+struct.unpack_from('<I',archive,section+8+animation*4)[0]
    put(0x54,action,2)  # main animation +0C action label from465040
    for s in r['select_stores']:put(0x48+s['offset'],s['value'],s['bytes'])
    put(0x4B,flags&3,1);put(0x4C,metadata_pointer+first_offset)
    put(0x70,metadata_pointer+first_offset);put(0x56,struct.unpack_from('<H',raw,8)[0],2)
    if raw[0]&4:put(0x51,1,1)
    if raw[0]&8:put(0x52,1,1)
    descriptor = raw[2]|((struct.unpack_from('<H',raw,6)[0]&15)<<8)
    if descriptor<0xFFF:
        descriptors = bytes.fromhex(r['descriptor_hex'])
        if descriptor*10+10>len(descriptors):raise ValueError('constructor descriptor index')
        put(0x60,descriptors[descriptor*10+8])
    put(4,0,1);put(0xA,0,2)
    for s in r['work_stores']:put(s['offset'],s['value'],s['bytes'])
    for at in (0x4E7,0x4E9,0x2E8):put(at,x,1);put(at+1,y,1)
    for at in (0x4CC,0x4CE,0x4D0,0x4D2):put(at,0,2)
    put(0x2EC,((x<<c['x_shift'])+c['x_center'])<<16)
    put(0x2F0,((y<<c['y_shift'])+c['y_center'])<<16)
    for offset in (0x2F4,0x3E0):defaults(offset,c['image_bytes'],r['image_stores'])
    put(0x4FE,c['friendly_timeout'],2)
    work[0x502:0x504]=bytes.fromhex(r['role_defaults_hex'])[role*2:role*2+2]
    for at in (0x4F8,0x4FA,0x4FC):put(at,0xFFFF,2)
    shared = bytearray(c['shared_bytes'])
    for i in range(c['shared_count']):struct.pack_into('<H',shared,2+i*2,c['shared_value'])
    cm_at = 2*(y*width+x)+1;cm[cm_at] = (cm[cm_at]+1)&255
    return {'work_hex':work.hex(),'record_hex':record.hex(),'shared_hex':shared.hex(),'cm_hex':cm.hex(),
        'cm_sha256':hashlib.sha256(cm).hexdigest(),'action':action,'direction':direction,'mapped_direction':mapped,
        'block':block,'animation':animation,'flags':flags&3,'first_program_offset':first_offset,
        'descriptor_index':descriptor,'constructor_coordinates':[x,y],'fixed_coordinates':list(struct.unpack_from('<II',work,0x2EC))}


def native_fixture():
    raw = EVIDENCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:
        raise ValueError('frozen first constructor evidence differs')
    fields = ('name','ready','first_unit_constructor_completed','first_unit_constructor','stop_reason',
        'persistent_ranges_unchanged','battle_world_constructed')
    return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,
        'cases':[{k:deepcopy(c[k]) for k in fields if k in c} for c in json.loads(raw)['cases']],**AUTHORITY}


if __name__=='__main__':
    p = argparse.ArgumentParser(description=__doc__);p.add_argument('--rules-out',required=True);p.add_argument('--fixture-out',required=True)
    args = p.parse_args()
    for path,data in ((args.rules_out,source_catalog()),(args.fixture_out,native_fixture())):
        (ROOT/path).write_text(report_text(data),encoding='utf-8',newline='\n')
