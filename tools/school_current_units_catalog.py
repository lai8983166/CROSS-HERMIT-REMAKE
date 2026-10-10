"""Independent current selection/progress/job/cache/archive/constructor rules."""
import argparse
from copy import deepcopy
import hashlib
import json
import struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_first_unit_work_catalog import source_catalog as work_catalog,expected_first_work
from tools.school_first_unit_constructor_catalog import source_catalog as constructor_catalog
from tools.school_first_unit_animation_catalog import source_catalog as binding_catalog,normalize_palette
from tools.school_tactical_resource_catalog import texture_inputs
from tools.dxanim_lib import parse_dxanim,parse_container,parse_program_blocks
from tools.tactics_exit_emulation import ROOT,SOURCE,SOURCE_SHA256,BASE,report_text
from tools.school_course_unlock_emulation import AUTHORITY

EVIDENCE = ROOT/'analysis/school-current-units-v1-20261010.json'
EVIDENCE_SHA256 = '01cc487814a01ed2ad61c1f061b6b125ba587ff58fdd7957584bed525f1cd7ef'
CACHE_EVIDENCE = ROOT/'analysis/school-current-cache-reuse-v3-20261010.json'
CACHE_SHA256 = '487665ecb2fc353dbd827153ddb9cc1a2a6285f50cabd79f508963e20792eaed'


def digest(raw):return hashlib.sha256(raw).hexdigest()


def source_catalog():
    image = SOURCE.read_bytes()
    if digest(image)!=SOURCE_SHA256:raise ValueError('current executable source differs')
    work,constructor,binding = work_catalog(),constructor_catalog(),binding_catalog()
    jobs = {}
    for j in work['jobs']:
        raw = (ROOT/j['resource_identity']['path']).read_bytes()
        if digest(raw)!=j['resource_identity']['sha256']:raise ValueError('current archive source differs')
        a = archive_inputs(raw);r = deepcopy(constructor)
        offsets = parse_dxanim(raw);programs = parse_program_blocks(raw)
        table,positions = j['animation_table_pointer'],j['position_table_pointer']
        identity = {'relative_path':j['relative_path'],'local_file':j['resource_identity']['path'],'bytes':len(raw),'sha256':digest(raw)}
        r.update({'source':identity,'action_table_pointer':table,
            'action_rows':[image[table-BASE+i*16:table-BASE+(i+1)*16].hex() for i in range(25)],
            'position_table_pointer':positions,'position_words':list(struct.unpack_from('<121H',image,positions-BASE)),
            'program_sections':offsets[:5],'programs':programs,'metadata_bytes':offsets[6],
            'descriptor_hex':raw[offsets[4]:offsets[5]].hex(),
            'job_input':deepcopy(j),'animation':a,'binding_constants':deepcopy(binding['constants'])})
        r['scope'] = f"Original friendly job{j['job']} constructor/binding source inputs; no scene placement or live GPU."
        jobs[str(j['job'])] = r
    md = Cs(CS_ARCH_X86,CS_MODE_32);md.detail = True
    code = []
    for va in (0x45338F,0x4533A6,0x4533AE,0x4533B4,0x4533B6,0x4533B8,0x4533D8,0x453416,0x45342D,
               0x45343C,0x45345F,0x451DA3,0x451DB4,0x451DBF,0x451DC9,0x451DDA,0x451DE5):
        i = next(md.disasm(image[va-BASE:va-BASE+16],va,count=1))
        code.append({'va':hex(va),'instruction_hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
    bodies = [{'start':hex(a),'end':hex(b),'instruction_hex':image[a-BASE:b-BASE].hex(),'sha256':digest(image[a-BASE:b-BASE])}
        for a,b in ((0x45337D,0x453493),(0x451D9D,0x451DE9),(0x466E20,0x466E90),(0x466B40,0x466C78))]
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'jobs':jobs,'work':work,
        'selection':{'count_va':'0x7f448d','category_va':'0x7f4490','header_base':0x7F4488,
            'count_offset':5,'category_offset':8,'record_category_offset':0xA4},
        'progress':{'decrement':1,'threshold':128,'receiver_offset':0x40,'second_compare_reads_first_byte':True},
        'code_inputs':code,'source_branch_bodies':bodies,
        'scope':'Original supported friendly jobs6/7/10; full current loops only, no enemies/placement/VM/GPU witness.',**AUTHORITY}


def expected_order(header_hex,records,rules=None):
    r = source_catalog() if rules is None else rules
    try:header = bytes.fromhex(header_hex);raw = [bytes.fromhex(s) for s in records]
    except (TypeError,ValueError) as error:raise ValueError('current selection encoding') from error
    if len(header)!=144 or any(len(s)!=176 for s in raw):raise ValueError('current selection size')
    s = r['selection'];count = struct.unpack_from('<b',header,s['count_offset'])[0];priority = header[s['category_offset']]
    if count!=len(raw) or not 1<=count<=34 or priority>=4 or any(x[0xA4]>=4 or x[15]!=1 for x in raw):
        raise ValueError('unsupported current selection/header/state')
    return [i for i,x in enumerate(raw) if x[s['record_category_offset']]==priority]+ \
           [i for i,x in enumerate(raw) if x[s['record_category_offset']]!=priority]


def expected_progress(before_hex,count,rules=None):
    r = source_catalog() if rules is None else rules
    try:value = bytearray.fromhex(before_hex)
    except (TypeError,ValueError) as error:raise ValueError('current progress encoding') from error
    if len(value)!=2 or type(count) is not int or not 0<=count<=34:raise ValueError('current progress size/count')
    c = r['progress'];events = []
    for _ in range(count):
        before = value.hex();value[0] = (value[0]-c['decrement'])&255
        if value[0]<=c['threshold']:
            value[0] = c['threshold'];value[1] = (value[1]-c['decrement'])&255
            if value[0]<=c['threshold']:value[1] = c['threshold']
        events.append({'before_hex':before,'after_hex':value.hex()})
    return {'events':events,'after_hex':value.hex()}


def expected_cache(before_hex,job,variant,controller,rules=None):
    r = source_catalog() if rules is None else rules
    try:cache = bytearray.fromhex(before_hex)
    except (TypeError,ValueError) as error:raise ValueError('current cache encoding') from error
    if len(cache)!=4096 or type(job) is not int or str(job) not in r['jobs'] or type(variant) is not int or not 1<=variant<=40 \
        or type(controller) is not int or not 0<controller<=0xFFFFFFAC or controller%4:
        raise ValueError('current cache inputs')
    group = r['jobs'][str(job)]['job_input']['group']
    if any(cache[i*8] not in (0,1) for i in range(512)):raise ValueError('unsupported current cache state')
    hits = [i for i in range(512) if cache[i*8]==1 and cache[i*8+1]==variant and struct.unpack_from('<H',cache,i*8+2)[0]==group]
    if len(hits)>1:raise ValueError('duplicate current cache ownership')
    if hits:
        slot = hits[0]
        if struct.unpack_from('<I',cache,slot*8+4)[0]!=controller:raise ValueError('current cache controller differs')
    else:
        empty = [i for i in range(512) if cache[i*8]==0]
        if not empty:raise ValueError('current cache exhausted')
        slot = empty[0];struct.pack_into('<BBHI',cache,slot*8,1,variant,group,controller)
    return {'slot':slot,'hit':bool(hits),'cache_hex':cache.hex(),'counter_delta':int(not hits)}


def native_fixture():
    raw = EVIDENCE.read_bytes()
    if digest(raw)!=EVIDENCE_SHA256:raise ValueError('frozen current school evidence differs')
    fields = ('name','ready','current_units_constructed','current_units','current_loop','stop_reason',
              'persistent_ranges_unchanged','battle_world_constructed')
    return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,
        'cases':[{k:deepcopy(c[k]) for k in fields if k in c} for c in json.loads(raw)['cases']],**AUTHORITY}


def archive_inputs(raw):
    offsets = parse_dxanim(raw)
    if len(offsets)!=9 or any(a>b for a,b in zip(offsets,offsets[1:])):
        raise ValueError('unit animation needs nine ordered sections')
    sections = []
    ends = offsets[1:]+[len(raw)]
    for index,(start,end) in enumerate(zip(offsets,ends)):
        s = {'index':index,'offset':start,'bytes':end-start,'sha256':digest(raw[start:end])}
        if index in (0,1,2,3,6,7) and start<end:
            size,count,entries = parse_container(raw,start)
            if size<8+4*count or size>end-start or any(x>size for x in entries):
                raise ValueError('unit animation nested section bounds')
            s.update({'container_bytes':size,'entry_count':count,'entry_offsets':entries})
        sections.append(s)
    images,palettes = sections[6],sections[7]
    count = images.get('entry_count')
    if count not in (147,193,219) or palettes.get('entry_count')!=40:
        raise ValueError('unsupported unit image/palette count')
    if sections[8]['bytes']!=((count+3)&~3) or raw[offsets[8]+count:]!=bytes((-count)%4):
        raise ValueError('unit palette mask size/padding')
    mask = raw[offsets[8]:offsets[8]+count]
    if any(x not in (0,1) for x in mask):
        raise ValueError('unit palette mask values')
    palette_entries = []
    for index,at in enumerate(palettes['entry_offsets']):
        end = palettes['entry_offsets'][index+1] if index+1<40 else palettes['container_bytes']
        if end-at!=1024:
            raise ValueError('unit palette entry size')
        p = raw[offsets[7]+at:offsets[7]+end]
        palette_entries.append({'index':index,'offset':at,'file_offset':offsets[7]+at,'raw_hex':p.hex(),'sha256':digest(p)})
    entries = texture_inputs(raw[offsets[6]:offsets[7]])
    for e in entries:
        if e['kind']!='indexed_bmp' or e['palette_count']!=256:
            raise ValueError('unsupported unit animation image type/palette')
        at = offsets[6]+e['offset']
        chunk = raw[at:at+e['bytes']]
        e.update({'file_offset':at,'palette_mask':mask[e['index']],
            'embedded_palette_hex':chunk[54:54+1024].hex(),
            'pixel_sha256':digest(chunk[e['pixel_offset']:e['pixel_offset']+e['row_stride']*e['height']])})
    programs = parse_program_blocks(raw,offsets)
    return {'sections':sections,'metadata_bytes':offsets[6],'metadata_hex':raw[:offsets[6]].hex(),
        'metadata_sha256':digest(raw[:offsets[6]]),'texture_entries':entries,'palettes':palette_entries,
        'mask_hex':mask.hex(),'program_counts':[len(p) for p in programs],
        'instructions':sum(len(p) for b in programs for p in b)}


def expected_current_binding(before_controller_hex,file_pointer,metadata_pointer,texture_allocation,texture_table,variant=3,rules=None,job=10):
    catalog = source_catalog() if rules is None else rules
    if type(job) is not int or str(job) not in catalog['jobs']:raise ValueError('unsupported current binding job')
    r = catalog['jobs'][str(job)]
    rules = {'source':r['source'],'animation':r['animation'],'constants':r['binding_constants']}
    if not isinstance(before_controller_hex,str):
        raise ValueError('invalid first animation controller hex type')
    try:
        controller = bytearray.fromhex(before_controller_hex)
    except ValueError as exc:
        raise ValueError('invalid first animation controller hex') from exc
    if len(controller)!=84 or isinstance(variant,bool) or not isinstance(variant,int) or not 1<=variant<=40:
        raise ValueError('unsupported unit animation binding inputs')
    pointers = (file_pointer,metadata_pointer,texture_allocation,texture_table)
    if any(isinstance(p,bool) or not isinstance(p,int) or not 0<p<0xFFFFFFFF-0x200000 or p%4 for p in pointers):
        raise ValueError('unit animation pointer bounds')
    slot = struct.unpack_from('<I',controller,0x28)[0]
    if not 110<=slot<114:
        raise ValueError('unsupported unit texture slot')
    a,c = rules['animation'],rules['constants']
    spans = [(file_pointer,file_pointer+rules['source']['bytes']),
        (metadata_pointer,metadata_pointer+a['metadata_bytes']),
        (texture_allocation,texture_allocation+len(a['texture_entries'])*c['texture_stride']+4),
        (texture_table+slot*8,texture_table+slot*8+8)]
    if any(max(a,b)<min(x,y) for i,(a,x) in enumerate(spans) for b,y in spans[i+1:]):
        raise ValueError('unit animation allocation overlap')
    if struct.unpack_from('<I',controller)[0]!=0 or struct.unpack_from('<I',controller,c['mode_field'])[0]!=0xFFFFFFFF:
        raise ValueError('unit animation controller is not the unloaded source input')
    sections = a['sections']
    selected = a['palettes'][variant-c['palette_index_subtract']]
    selected_pointer = file_pointer+selected['file_offset']
    selected_palette = normalize_palette(bytes.fromhex(selected['raw_hex']))
    records = []
    raw = (ROOT/rules['source']['local_file']).read_bytes()
    if digest(raw)!=rules['source']['sha256']:raise ValueError('current binding archive identity')
    mutated = bytearray(raw)
    palette_used = False
    for e in a['texture_entries']:
        p = file_pointer+e['file_offset']
        external = e['palette_mask']==0
        palette = selected_palette if external else normalize_palette(bytes.fromhex(e['embedded_palette_hex']))
        if external:
            palette_used = True
        else:
            mutated[e['file_offset']+54:e['file_offset']+54+1024]=palette
        colors_at = e['file_offset']+46
        if struct.unpack_from('<I',mutated,colors_at)[0]==0:
            struct.pack_into('<I',mutated,colors_at,c['palette_colors'])
        record = bytearray(84)  # Declared zero finite allocation, before native constructors/GPU.
        struct.pack_into('<I',record,0x34,c['native_format'])
        struct.pack_into('<H',record,c['width_field'],e['width'])
        struct.pack_into('<H',record,c['height_field'],e['height'])
        records.append({'index':e['index'],'record_pointer':texture_allocation+4+e['index']*c['texture_stride'],
            'raw_record_hex':record.hex(),'palette_pointer':selected_pointer if external else 0,
            'upload_palette_pointer':selected_pointer if external else p+c['bitmap_palette_offset'],
            'upload_palette_hex':palette.hex(),'upload_palette_sha256':digest(palette),
            'pixel_sha256':e['pixel_sha256'],'mask_value':e['palette_mask'],
            'upload_args':[p,1,0,selected_pointer if external else 0]})
    if palette_used:
        mutated[selected['file_offset']:selected['file_offset']+1024]=selected_palette
    struct.pack_into('<I',controller,0,metadata_pointer)
    for index in range(5):
        struct.pack_into('<I',controller,4+index*4,metadata_pointer+sections[index]['offset'])
    struct.pack_into('<I',controller,0x18,file_pointer+sections[c['image_section']]['offset'])
    struct.pack_into('<I',controller,0x1C,metadata_pointer+sections[5]['offset'])
    struct.pack_into('<I',controller,0x24,texture_table)
    struct.pack_into('<I',controller,0x2C,0)
    struct.pack_into('<I',controller,c['mode_field'],c['mode'])
    return {'controller_hex':controller.hex(),'metadata_hex':a['metadata_hex'],'metadata_sha256':a['metadata_sha256'],
        'section_pointers':[metadata_pointer+s['offset'] for s in sections[:5]],'texture_entries':records,
        'binding_args':[0,texture_table,metadata_pointer+sections[5]['offset'],file_pointer+sections[6]['offset'],
            0,selected_pointer,file_pointer+sections[8]['offset']],
        'source_sha256_at_release':digest(mutated),'texture_records':texture_allocation+4,
        'texture_count':len(records),'mode_field':c['mode']}


def expected_current_constructor(before_work_hex,record_hex,work_pointer,controller_pointer,metadata_pointer,before_cm_hex,rules=None):
    catalog = source_catalog() if rules is None else rules
    try:input_record = bytes.fromhex(record_hex)
    except (TypeError,ValueError) as error:raise ValueError('current constructor record encoding') from error
    if len(input_record)!=176:raise ValueError('current constructor record size')
    job_key = str(struct.unpack_from('<H',input_record,12)[0])
    if job_key not in catalog['jobs']:raise ValueError('unsupported current constructor job')
    r = catalog['jobs'][job_key]
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
    if not 1<=role<=34 or job not in (6,7,10) or record[0xA4]>=r['constants']['friendly_category_limit'] or record[0xF]!=1:
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
    archive = (ROOT/r['source']['local_file']).read_bytes()
    if digest(archive)!=r['source']['sha256']:raise ValueError('current constructor archive identity')
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



if __name__=='__main__':
    p = argparse.ArgumentParser(description=__doc__);p.add_argument('--rules-out',required=True);p.add_argument('--fixture-out',required=True)
    args = p.parse_args()
    for path,data in ((args.rules_out,source_catalog()),(args.fixture_out,native_fixture())):
        (ROOT/path).write_text(report_text(data),encoding='utf-8',newline='\n')
