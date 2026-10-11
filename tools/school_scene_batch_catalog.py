"""Independent original job393/383 resource, constructor and cache byte rules."""
import argparse,hashlib,json,struct
from copy import deepcopy
from tools.school_first_unit_animation_catalog import source_catalog as base_binding,normalize_palette,digest
from tools.school_scene_second_constructor_catalog import source_catalog as second_rules
from tools.school_scene_unit_work_catalog import source_catalog as prefix_rules
from tools.school_enemy_records_catalog import source_catalog as record_rules,expected_record
from tools.school_scene_batch_emulation import batch_resource,ROOT,SOURCE,SOURCE_SHA256,AUTHORITY,report_text,ORDINALS
from tools.school_tactical_resource_catalog import texture_inputs
from tools.dxanim_lib import parse_dxanim,parse_container,parse_program_blocks,parse_block4_descriptors,resolve_visible_instruction,DxAnimError

EVIDENCE=ROOT/'analysis/school-scene-batch-v1-20261011.json'
EVIDENCE_SHA256='e3cd62002440f9d1a91eb0ddb35cc0fc987a964995c9ee94fd3b52ea756fd706'

def source_catalog():
 prefix=prefix_rules();image=SOURCE.read_bytes();base=second_rules()
 if digest(image)!=SOURCE_SHA256:raise ValueError('scene batch executable identity')
 bindings={};constructors={}
 for job,variant in ((393,0),(383,1)):
  raw,identity,_=batch_resource(job,variant,prefix);o=parse_dxanim(raw);programs=parse_program_blocks(raw)
  binding=base_binding();binding.update(source=identity,animation=animation_inputs(raw),job=job,variant=variant)
  binding['scope']='Original scene batch job'+str(job)+'; GPU declared.'
  binding['mode0']=deepcopy(base['binding']['mode0'])
  binding['mode0']['source_job']=deepcopy(prefix['jobs'][str(job)])
  r=deepcopy(base['constructor']);j=prefix['jobs'][str(job)];table=j['animation_table_pointer'];positions=j['position_table_pointer']
  r.update(source=identity,job=job,variant=variant,action_table_pointer=table,
   action_rows=[image[table-0x400000+i*16:table-0x400000+(i+1)*16].hex() for i in range(25)],
   position_table_pointer=positions,position_words=list(struct.unpack_from('<'+str(len(programs[0]))+'H',image,positions-0x400000)),
   program_sections=o[:5],programs=programs,metadata_bytes=o[6],descriptor_hex=raw[o[4]:o[5]].hex(),
   role_defaults_hex=image[r['constants']['role_table']-0x400000:r['constants']['role_table']-0x400000+394*2].hex(),
   scope='Complete actual ordinals2–9 only; remaining25/deployment/VM unexecuted.')
  # Source prefix selects status/direction before the action bind; special393 tail recalculates direction later.
  direction=prefix['mode_dispatch']['mode_cases'][0] if job==393 else prefix['common']['mode_value']
  action=r['status_actions'][1];mapped=r['direction_map'][direction]
  pos,flags=bytes.fromhex(r['action_rows'][action])[mapped*2:mapped*2+2];word=r['position_words'][pos]
  block,animation=word>>8,word&255;first=programs[block][animation][0]
  r['initial_program']={'action':action,'direction':direction,'mapped_direction':mapped,'position_index':pos,
   'position_word':word,'block':block,'animation':animation,'flags':flags&3,'first_instruction':first,
   'visible_layers':resolve_visible_instruction(first,parse_block4_descriptors(raw,o),block=block,animation=animation,mirror_flags=flags&3)}
  bindings[str(job)]=binding;constructors[str(job)]=r
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'ordinals':list(ORDINALS),
  'prefix':prefix,'records':record_rules(),'bindings':bindings,'constructors':constructors,**AUTHORITY}

def native_fixture():
 raw=EVIDENCE.read_bytes()
 if digest(raw)!=EVIDENCE_SHA256:raise ValueError('frozen scene batch evidence differs')
 return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,
  'cases':[{k:deepcopy(c[k]) for k in ('name','ready','scene_batch_completed','scene_batch','stop_reason','persistent_ranges_unchanged','battle_world_constructed')}
   for c in json.loads(raw)['cases']],**AUTHORITY}
def animation_inputs(raw):
    if not isinstance(raw,(bytes,bytearray)):raise ValueError('scene animation byte input required')
    offsets = parse_dxanim(raw)
    if len(offsets) != 9 or any((a > b for (a, b) in zip(offsets, offsets[1:]))):
        raise ValueError('unit animation needs nine ordered sections')
    sections = []
    ends = offsets[1:] + [len(raw)]
    for (index, (start, end)) in enumerate(zip(offsets, ends)):
        s = {'index': index, 'offset': start, 'bytes': end - start, 'sha256': digest(raw[start:end])}
        if index in (0, 1, 2, 3, 6, 7) and start < end:
            (size, count, entries) = parse_container(raw, start)
            if size < 8 + 4 * count or size > end - start or (index >= 6 and size != end - start) or any((x > size for x in entries)):
                raise ValueError('unit animation nested section bounds')
            s.update({'container_bytes': size, 'entry_count': count, 'entry_offsets': entries})
        sections.append(s)
    (images, palettes) = (sections[6], sections[7])
    if images.get('entry_count') not in (109,43) or palettes.get('entry_count') != 4:
        raise ValueError('unsupported unit image/palette count')
    if sections[8]['bytes'] != ((images['entry_count']+3)&~3) or any(raw[offsets[8] + images['entry_count']:]):
        raise ValueError('unit palette mask size/padding')
    mask = raw[offsets[8]:offsets[8] + images["entry_count"]]
    if any((x not in (0, 1) for x in mask)):
        raise ValueError('unit palette mask values')
    palette_entries = []
    for (index, at) in enumerate(palettes['entry_offsets']):
        end = palettes['entry_offsets'][index + 1] if index + 1 < 4 else palettes['container_bytes']
        if end - at != 1024:
            raise ValueError('unit palette entry size')
        p = raw[offsets[7] + at:offsets[7] + end]
        palette_entries.append({'index': index, 'offset': at, 'file_offset': offsets[7] + at, 'raw_hex': p.hex(), 'sha256': digest(p)})
    entries = texture_inputs(raw[offsets[6]:offsets[7]])
    for e in entries:
        if e['kind'] != 'indexed_bmp' or e['palette_count'] != 256:
            raise ValueError('unsupported unit animation image type/palette')
        at = offsets[6] + e['offset']
        chunk = raw[at:at + e['bytes']]
        e.update({'file_offset': at, 'palette_mask': mask[e['index']], 'embedded_palette_hex': chunk[54:54 + 1024].hex(), 'pixel_sha256': digest(chunk[e['pixel_offset']:e['pixel_offset'] + e['row_stride'] * e['height']])})
    programs = parse_program_blocks(raw, offsets)
    return {'sections': sections, 'metadata_bytes': offsets[6], 'metadata_hex': raw[:offsets[6]].hex(), 'metadata_sha256': digest(raw[:offsets[6]]), 'texture_entries': entries, 'palettes': palette_entries, 'mask_hex': mask.hex(), 'program_counts': [len(p) for p in programs], 'instructions': sum((len(p) for b in programs for p in b))}

def expected_binding(before_controller_hex,file_pointer,metadata_pointer,texture_allocation,texture_table,job=393,variant=0,rules=None):
    if type(job) is not int or type(variant) is not int or (job,variant) not in ((393,0),(383,1)):
        raise ValueError('unsupported scene batch job/variant')
    rules = source_catalog()['bindings'][str(job)] if rules is None else rules
    if rules['job']!=job or rules['variant']!=variant:raise ValueError('incompatible scene binding rules')
    if not isinstance(before_controller_hex,str):
        raise ValueError('invalid scene batch animation controller hex type')
    try:
        controller = bytearray.fromhex(before_controller_hex)
    except ValueError as exc:
        raise ValueError('invalid scene batch animation controller hex') from exc
    if len(controller)!=84 or isinstance(variant,bool) or not isinstance(variant,int) or (job,variant) not in ((393,0),(383,1)) or type(job) is not int:
        raise ValueError('unsupported unit animation binding inputs')
    pointers = (file_pointer,metadata_pointer,texture_allocation,texture_table)
    if any(isinstance(p,bool) or not isinstance(p,int) or not 0<p<0xFFFFFFFF-0x200000 or p%4 for p in pointers):
        raise ValueError('unit animation pointer bounds')
    slot = struct.unpack_from('<I',controller,0x28)[0]
    if slot not in (114,115,116):
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
    selected = a['palettes'][variant-c['palette_index_subtract']] if variant else None
    selected_pointer = file_pointer+selected['file_offset'] if selected else 0
    selected_palette = normalize_palette(bytes.fromhex(selected['raw_hex'])) if selected else None
    records = []
    raw,_,_ = batch_resource(job,variant)
    mutated = bytearray(raw)
    palette_used = False
    for e in a['texture_entries']:
        p = file_pointer+e['file_offset']
        external = bool(variant) and e['palette_mask']==0
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
            0,selected_pointer,file_pointer+sections[8]['offset'] if variant else 0],
        'source_sha256_at_release':digest(mutated),'texture_records':texture_allocation+4,
        'texture_count':len(records),'mode_field':c['mode']}

def expected_constructor(before_work_hex, record_hex, work_pointer, controller_pointer, metadata_pointer, before_cm_hex, selector=0, relation_hex=None, rules=None):
    if rules is None:
        try:
            raw=bytes.fromhex(record_hex)
            if len(raw)!=176:raise ValueError('scene constructor record size')
            key=str(struct.unpack_from('<H',raw,12)[0])
        except (ValueError,TypeError,struct.error) as error:raise ValueError('scene constructor record encoding') from error
        if key not in ('393','383'):raise ValueError('unsupported scene constructor job')
        r=source_catalog()['constructors'][key]
    else:r=rules
    (width, height) = r['logical_dimensions']
    if (width, height) != (64, 96):
        raise ValueError('unsupported constructor logical map')
    try:
        (work, record, cm) = (bytearray.fromhex(before_work_hex), bytearray.fromhex(record_hex), bytearray.fromhex(before_cm_hex))
    except (TypeError, ValueError) as error:
        raise ValueError('constructor input encoding') from error
    if len(work) != r['constants']['work_bytes'] or len(record) != r['constants']['record_bytes'] or len(cm) != width * height * 2:
        raise ValueError('constructor input size')
    if struct.unpack_from('<H', work)[0] != 1 or not 240<=struct.unpack_from('<H', work, 2)[0]<=247 or any(work[68:600]):
        raise ValueError('constructor input is not an unbound initialized work')
    pointers = (work_pointer, controller_pointer, metadata_pointer)
    if any((type(p) is not int or p <= 0 or p % 4 or (p + n > 4294967296) for (p, n) in zip(pointers, (len(work), 84, r['metadata_bytes'])))):
        raise ValueError('constructor pointer bounds/alignment')
    spans = [(p, p + n) for (p, n) in zip(pointers, (len(work), 84, r['metadata_bytes']))]
    if any((max(a, b) < min(x, y) for (i, (a, x)) in enumerate(spans) for (b, y) in spans[i + 1:])):
        raise ValueError('constructor pointer overlap')
    (role, job) = (struct.unpack_from('<H', record, 2)[0], struct.unpack_from('<H', record, 12)[0])
    if role != job or job not in (393,383) or job!=r['job'] or record[164] != (7 if job==393 else 5) or (record[15] != 1):
        raise ValueError('unsupported scene batch constructor role/job/state/category')
    (status, direction) = (work[656], work[650])
    if not 1 <= status <= len(r['status_actions']) or r['status_actions'][status - 1] is None or (not 1 <= direction <= 9):
        raise ValueError('unsupported scene batch constructor status/direction')
    (x, y) = record[155:157]
    if x >= width or y >= height:
        raise ValueError('constructor coordinates outside logical map')
    c = r['constants']
    index = struct.unpack_from('<H', work, 2)[0]
    receiver = work_pointer - (c['work_offset'] + index * c['work_bytes'])
    if struct.unpack_from('<I', work, 600)[0] != receiver + c['record_offset'] + index * c['record_bytes']:
        raise ValueError('constructor copied record ownership')

    def put(at, value, size=4):
        work[at:at + size] = value.to_bytes(size, 'little')

    def defaults(at, size, stores):
        work[at:at + size] = bytes(size)
        for s in stores:
            put(at + s['offset'], s['value'], s['bytes'])
    put(68, controller_pointer)
    for offset in [72, *[c['aux_offset'] + i * c['aux_stride'] for i in range(c['aux_count'])]]:
        defaults(offset, c['animation_bytes'], r['animation_stores'])
        put(offset + 28, controller_pointer)
        put(offset + 36, work_pointer + offset)
    context = receiver + c['context_offset']
    if not 0 < context < 4294967296:
        raise ValueError('constructor context pointer')
    put(116, context)
    put(204, context)
    action = r['status_actions'][status - 1]
    mapped = r['direction_map'][direction]
    row = bytes.fromhex(r['action_rows'][action])
    (index, flags) = row[mapped * 2:mapped * 2 + 2]
    if index >= len(r['position_words']):
        raise ValueError('constructor action position index')
    position = r['position_words'][index]
    (block, animation) = (position >> 8, position & 255)
    if block >= 4 or animation >= len(r['programs'][block]):
        raise ValueError('constructor animation index')
    program = r['programs'][block][animation]
    if not program or program[0]['opcode'] != 0 or program[0]['flags'] & 12:
        raise ValueError('unsupported scene batch constructor initial animation opcode/events')
    raw = bytes.fromhex(program[0]['raw'])
    section = r['program_sections'][block]
    (archive, _, _) = batch_resource(job,r['variant'])
    first_offset = section + struct.unpack_from('<I', archive, section + 8 + animation * 4)[0]
    put(84, action, 2)
    for s in r['select_stores']:
        put(72 + s['offset'], s['value'], s['bytes'])
    put(75, flags & 3, 1)
    put(76, metadata_pointer + first_offset)
    put(112, metadata_pointer + first_offset)
    put(86, struct.unpack_from('<H', raw, 8)[0], 2)
    if raw[0] & 4:
        put(81, 1, 1)
    if raw[0] & 8:
        put(82, 1, 1)
    descriptor = raw[2] | (struct.unpack_from('<H', raw, 6)[0] & 15) << 8
    if descriptor < 4095:
        descriptors = bytes.fromhex(r['descriptor_hex'])
        if descriptor * 10 + 10 > len(descriptors):
            raise ValueError('constructor descriptor index')
        put(96, descriptors[descriptor * 10 + 8])
    put(4, 0, 1)
    put(10, 0, 2)
    for s in r['work_stores']:
        put(s['offset'], s['value'], s['bytes'])
    for at in (1255, 1257, 744):
        put(at, x, 1)
        put(at + 1, y, 1)
    for at in (1228, 1230, 1232, 1234):
        put(at, 0, 2)
    put(748, (x << c['x_shift']) + c['x_center'] << 16)
    put(752, (y << c['y_shift']) + c['y_center'] << 16)
    for offset in (756, 992):
        defaults(offset, c['image_bytes'], r['image_stores'])
    put(1278, c['friendly_timeout'] if record[164]<c['friendly_category_limit'] else c['other_timeout'], 2)
    work[1282:1284] = bytes.fromhex(r['role_defaults_hex'])[role * 2:role * 2 + 2]
    for at in (1272, 1274, 1276):
        put(at, 65535, 2)
    if r['special']['role_min']<=role<=r['special']['role_max']:
        try:relation=bytes.fromhex(relation_hex)
        except (ValueError,TypeError) as error:raise ValueError('special constructor relation encoding') from error
        if type(selector) is not int or not 0<=selector<16 or len(relation)!=256:
            raise ValueError('special constructor relation ownership')
        mode=r['mode_dispatch'];category=record[164];cell=relation[selector*16+category]
        if category==selector:classification=0
        elif cell<4:classification=mode['relation_cases'][cell]
        else:raise ValueError('unsupported special constructor relation')
        if not 0<=classification<len(mode['mode_cases']):raise ValueError('unsupported special constructor classification')
        put(650,mode['mode_cases'][classification],1)
        record[r['special']['record_field']]=r['special']['record_value']
    shared = bytearray(c['shared_bytes'])
    for i in range(c['shared_count']):
        struct.pack_into('<H', shared, 2 + i * 2, c['shared_value'])
    cm_at = 2 * (y * width + x) + 1
    cm[cm_at] = cm[cm_at] + 1 & 255
    return {'work_hex': work.hex(), 'record_hex': record.hex(), 'shared_hex': shared.hex(), 'cm_hex': cm.hex(), 'cm_sha256': hashlib.sha256(cm).hexdigest(), 'action': action, 'direction': direction, 'mapped_direction': mapped, 'block': block, 'animation': animation, 'flags': flags & 3, 'first_program_offset': first_offset, 'descriptor_index': descriptor, 'constructor_coordinates': [x, y], 'fixed_coordinates': list(struct.unpack_from('<II', work, 748))}

def expected_prefix(record_hex,ordinal,cache_hex,counter,renderer,controller,selector,relation_hex,rules=None,template_hex=None,controller_hex=None):
    r=source_catalog()['prefix'] if rules is None else rules;c=r['common']
    try:record=bytearray.fromhex(record_hex);cache=bytearray.fromhex(cache_hex);relation=bytes.fromhex(relation_hex)
    except (TypeError,ValueError) as error:raise ValueError('scene prefix byte encoding') from error
    if type(ordinal) is not int or ordinal not in ORDINALS or len(record)!=176 or len(cache)!=c['cache_count']*8 or len(relation)!=256:
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
    matches=[i for i in range(c['cache_count']) if cache[i*8] and cache[i*8+1]==variant and struct.unpack_from('<H',cache,i*8+2)[0]==j['group']]
    slots=matches or [i for i in range(c['cache_count']) if cache[i*8]==0]
    if len(matches)>1 or not slots:raise ValueError('scene batch cache ownership')
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
    if matches:
        try:obj=bytearray.fromhex(controller_hex)
        except (ValueError,TypeError) as error:raise ValueError('cached controller encoding') from error
        if len(obj)!=84 or struct.unpack_from('<I',cache,slot*8+4)[0]!=controller or struct.unpack_from('<I',obj,64)[0]!=1:
            raise ValueError('cached controller ownership')
    else:
        obj=bytearray(c['controller_bytes'])
        for s in c['controller_stores']:obj[s['offset']:s['offset']+s['bytes']]=s['value'].to_bytes(s['bytes'],'little')
        struct.pack_into('<I',obj,0x28,counter);struct.pack_into('<I',obj,0x44,renderer)
        struct.pack_into('<H',obj,0x48,j['animation_id']);struct.pack_into('<II',obj,0x4C,j['animation_table_pointer'],j['position_table_pointer'])
        struct.pack_into('<BBHI',cache,slot*8,1,variant,j['group'],controller)
    return {'work_hex':work.hex(),'record_hex':record.hex(),'cache_hex':cache.hex(),'controller_hex':obj.hex(),
        'counter':counter+int(not matches),'cache_slot':slot,'resource_args':None if matches else [j['filename_pointer'],variant,int(variant!=0),0],
        'relative_path':j['relative_path']}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--rules-out',required=True);p.add_argument('--fixture-out',required=True);a=p.parse_args()
 for name,data in ((a.rules_out,source_catalog()),(a.fixture_out,native_fixture())):
  (ROOT/name).write_text(report_text(data),encoding='utf-8',newline='\n')
