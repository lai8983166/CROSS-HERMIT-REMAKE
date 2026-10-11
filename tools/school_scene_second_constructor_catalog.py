"""Independent51e mode0 binding and role387 constructor byte rules."""
import argparse,hashlib,json,struct
from copy import deepcopy
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from capstone.x86_const import X86_OP_IMM,X86_OP_MEM
from tools.school_first_unit_animation_catalog import source_catalog as base_binding,normalize_palette,digest
from tools.school_first_unit_constructor_catalog import source_catalog as base_constructor
from tools.school_scene_unit_work_catalog import source_catalog as scene_prefix
from tools.school_scene_second_constructor_emulation import second_resource,ROOT,SOURCE,SOURCE_SHA256,BASE,AUTHORITY,report_text
from tools.dxanim_lib import parse_dxanim,parse_container,parse_program_blocks,parse_block4_descriptors,resolve_visible_instruction,DxAnimError
from tools.school_tactical_resource_catalog import texture_inputs

EVIDENCE=ROOT/'analysis/school-scene-second-constructor-v1-20261011.json'
EVIDENCE_SHA256='4a73435783457dca57f928b71f5421458824828b6b43611275c822b3b231c0a6'

def source_catalog():
 raw,identity,_=second_resource();offsets=parse_dxanim(raw);programs=parse_program_blocks(raw)
 binding=base_binding();binding['source']=identity;binding['animation']=animation_inputs(raw)
 binding['scope']='Exactly second scene-unit job387 variant0; embedded palettes; texture slots113/114. GPU declared.'
 constructor=base_constructor();prefix=scene_prefix();job=prefix['jobs']['387'];image=SOURCE.read_bytes()
 if digest(image)!=SOURCE_SHA256:raise ValueError('second constructor executable identity')
 table,positions=job['animation_table_pointer'],job['position_table_pointer']
 constructor.update({'source':identity,'action_table_pointer':table,
  'action_rows':[image[table-BASE+i*16:table-BASE+(i+1)*16].hex() for i in range(25)],
  'position_table_pointer':positions,'position_words':list(struct.unpack_from('<'+str(len(programs[0]))+'H',image,positions-BASE)),
  'program_sections':offsets[:5],'programs':programs,'metadata_bytes':offsets[6],
  'descriptor_hex':raw[offsets[4]:offsets[5]].hex(),
  'role_defaults_hex':image[constructor['constants']['role_table']-BASE:constructor['constants']['role_table']-BASE+388*2].hex(),
  'mode_dispatch':prefix['mode_dispatch'],
  'scope':'Exactly role/job387 state1 category0 index248; natural453630 return; remaining33/deployment/VM unexecuted.'})
 md=Cs(CS_ARCH_X86,CS_MODE_32);md.detail=True
 def value(va,mnemonic,index=-1):
  i=next(md.disasm(image[va-BASE:va-BASE+16],va,count=1))
  if i.mnemonic!=mnemonic:raise ValueError(f'special role source instruction{va:#x}')
  constructor['code_inputs'].append({'va':hex(va),'instruction_hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
  o=i.operands[index]
  if o.type==X86_OP_IMM:return o.imm
  if o.type==X86_OP_MEM:return o.mem.disp
  raise ValueError('special role constant operand')
 constructor['special']={'role_min':value(0x469B60,'cmp'),'role_max':value(0x469B6B,'cmp'),
  'record_field':value(0x4684CD,'mov',0),'record_value':value(0x4684CD,'mov'),
  'relation_offset':value(0x46A995,'lea'),'relation_selector_offset':value(0x46A989,'mov',-1)}
 binding['mode0']={'palette_pointer':value(0x41EC0F,'push'),'mask_pointer':value(0x41EC0D,'push'),
  'source_job':deepcopy(job),'variant_branch':'409D04<=0 selects409DE9 then41EBF0'}
 if binding['mode0']['palette_pointer']!=0 or binding['mode0']['mask_pointer']!=0:
  raise ValueError('unsupported mode0 palette/mask source')
 for a,b in ((0x409BF1,0x409E0B),(0x41EBF0,0x41EC40),(0x409FB0,0x409FE7),
  (0x469AD0,0x469B8D),(0x46A430,0x46A4BD),(0x46A950,0x46AA22),
  (0x46C040,0x46C0F4),(0x46C290,0x46C33C),(0x475370,0x4753E6),(0x475650,0x475694)):
  body={'start':hex(a),'end':hex(b),'instruction_hex':image[a-BASE:b-BASE].hex(),'sha256':digest(image[a-BASE:b-BASE])}
  constructor['source_branch_bodies'].append(body)
 action=constructor['status_actions'][1];direction=prefix['mode_dispatch']['mode_cases'][0]
 mapped=constructor['direction_map'][direction]
 index,flags=bytes.fromhex(constructor['action_rows'][action])[mapped*2:mapped*2+2]
 position=constructor['position_words'][index];block,animation=position>>8,position&255
 first=programs[block][animation][0]
 layers=resolve_visible_instruction(first,parse_block4_descriptors(raw,offsets),block=block,animation=animation,mirror_flags=flags&3)
 if any(not 0<=layer['frame']<126 for layer in layers):raise ValueError('second initial descriptor image ownership')
 constructor['initial_program']={'status':2,'action':action,'direction':direction,'mapped_direction':mapped,
  'position_index':index,'position_word':position,'block':block,'animation':animation,
  'flags':flags&3,'first_instruction':first,'visible_layers':layers}
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'source':identity,
  'binding':binding,'constructor':constructor,**AUTHORITY}

def native_fixture():
 raw=EVIDENCE.read_bytes()
 if digest(raw)!=EVIDENCE_SHA256:raise ValueError('frozen second scene constructor evidence differs')
 fields=('name','ready','second_scene_work','second_scene_record','scene_progress',
  'second_scene_animation_loaded','second_scene_animation','second_scene_constructor_completed',
  'second_scene_constructor','stop_reason','persistent_ranges_unchanged','battle_world_constructed')
 return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,
  'cases':[{k:deepcopy(c[k]) for k in fields if k in c} for c in json.loads(raw)['cases']],**AUTHORITY}

def animation_inputs(raw):
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
    if images.get('entry_count') != 126 or palettes.get('entry_count') != 4:
        raise ValueError('unsupported unit image/palette count')
    if sections[8]['bytes'] != 128 or raw[offsets[8] + 126:] != bytes(2):
        raise ValueError('unit palette mask size/padding')
    mask = raw[offsets[8]:offsets[8] + 126]
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

def expected_binding(before_controller_hex, file_pointer, metadata_pointer, texture_allocation, texture_table, variant=0, rules=None):
    rules = source_catalog()['binding'] if rules is None else rules
    if not isinstance(before_controller_hex, str):
        raise ValueError('invalid first animation controller hex type')
    try:
        controller = bytearray.fromhex(before_controller_hex)
    except ValueError as exc:
        raise ValueError('invalid first animation controller hex') from exc
    if len(controller) != 84 or isinstance(variant, bool) or (not isinstance(variant, int)) or (variant != 0):
        raise ValueError('unsupported unit animation binding inputs')
    pointers = (file_pointer, metadata_pointer, texture_allocation, texture_table)
    if any((isinstance(p, bool) or not isinstance(p, int) or (not 0 < p < 4294967295 - 2097152) or p % 4 for p in pointers)):
        raise ValueError('unit animation pointer bounds')
    slot = struct.unpack_from('<I', controller, 40)[0]
    if slot not in (113, 114):
        raise ValueError('unsupported unit texture slot')
    (a, c) = (rules['animation'], rules['constants'])
    spans = [(file_pointer, file_pointer + rules['source']['bytes']), (metadata_pointer, metadata_pointer + a['metadata_bytes']), (texture_allocation, texture_allocation + len(a['texture_entries']) * c['texture_stride'] + 4), (texture_table + slot * 8, texture_table + slot * 8 + 8)]
    if any((max(a, b) < min(x, y) for (i, (a, x)) in enumerate(spans) for (b, y) in spans[i + 1:])):
        raise ValueError('unit animation allocation overlap')
    if struct.unpack_from('<I', controller)[0] != 0 or struct.unpack_from('<I', controller, c['mode_field'])[0] != 4294967295:
        raise ValueError('unit animation controller is not the unloaded source input')
    sections = a['sections']
    selected_pointer = rules['mode0']['palette_pointer']
    records = []
    (raw, _, _) = second_resource(387, variant)
    mutated = bytearray(raw)
    for e in a['texture_entries']:
        p = file_pointer + e['file_offset']
        palette = normalize_palette(bytes.fromhex(e['embedded_palette_hex']))
        mutated[e['file_offset'] + 54:e['file_offset'] + 54 + 1024] = palette
        colors_at = e['file_offset'] + 46
        if struct.unpack_from('<I', mutated, colors_at)[0] == 0:
            struct.pack_into('<I', mutated, colors_at, c['palette_colors'])
        record = bytearray(84)
        struct.pack_into('<I', record, 52, c['native_format'])
        struct.pack_into('<H', record, c['width_field'], e['width'])
        struct.pack_into('<H', record, c['height_field'], e['height'])
        records.append({'index': e['index'], 'record_pointer': texture_allocation + 4 + e['index'] * c['texture_stride'], 'raw_record_hex': record.hex(), 'palette_pointer': 0, 'upload_palette_pointer': p + c['bitmap_palette_offset'], 'upload_palette_hex': palette.hex(), 'upload_palette_sha256': digest(palette), 'pixel_sha256': e['pixel_sha256'], 'mask_value': e['palette_mask'], 'upload_args': [p, 1, 0, 0]})
    struct.pack_into('<I', controller, 0, metadata_pointer)
    for index in range(5):
        struct.pack_into('<I', controller, 4 + index * 4, metadata_pointer + sections[index]['offset'])
    struct.pack_into('<I', controller, 24, file_pointer + sections[c['image_section']]['offset'])
    struct.pack_into('<I', controller, 28, metadata_pointer + sections[5]['offset'])
    struct.pack_into('<I', controller, 36, texture_table)
    struct.pack_into('<I', controller, 44, 0)
    struct.pack_into('<I', controller, c['mode_field'], c['mode'])
    return {'controller_hex': controller.hex(), 'metadata_hex': a['metadata_hex'], 'metadata_sha256': a['metadata_sha256'], 'section_pointers': [metadata_pointer + s['offset'] for s in sections[:5]], 'texture_entries': records, 'binding_args': [0, texture_table, metadata_pointer + sections[5]['offset'], file_pointer + sections[6]['offset'], 0, selected_pointer, rules['mode0']['mask_pointer']], 'source_sha256_at_release': digest(mutated), 'texture_records': texture_allocation + 4, 'texture_count': len(records), 'mode_field': c['mode']}

def expected_constructor(before_work_hex, record_hex, work_pointer, controller_pointer, metadata_pointer, before_cm_hex, selector=0, relation_hex=None, rules=None):
    r = source_catalog()['constructor'] if rules is None else rules
    (width, height) = r['logical_dimensions']
    if (width, height) != (64, 96):
        raise ValueError('unsupported constructor logical map')
    try:
        (work, record, cm) = (bytearray.fromhex(before_work_hex), bytearray.fromhex(record_hex), bytearray.fromhex(before_cm_hex))
    except (TypeError, ValueError) as error:
        raise ValueError('constructor input encoding') from error
    if len(work) != r['constants']['work_bytes'] or len(record) != r['constants']['record_bytes'] or len(cm) != width * height * 2:
        raise ValueError('constructor input size')
    if struct.unpack_from('<H', work)[0] != 1 or struct.unpack_from('<H', work, 2)[0] != 248 or any(work[68:600]):
        raise ValueError('constructor input is not an unbound initialized work')
    pointers = (work_pointer, controller_pointer, metadata_pointer)
    if any((type(p) is not int or p <= 0 or p % 4 or (p + n > 4294967296) for (p, n) in zip(pointers, (len(work), 84, r['metadata_bytes'])))):
        raise ValueError('constructor pointer bounds/alignment')
    spans = [(p, p + n) for (p, n) in zip(pointers, (len(work), 84, r['metadata_bytes']))]
    if any((max(a, b) < min(x, y) for (i, (a, x)) in enumerate(spans) for (b, y) in spans[i + 1:])):
        raise ValueError('constructor pointer overlap')
    (role, job) = (struct.unpack_from('<H', record, 2)[0], struct.unpack_from('<H', record, 12)[0])
    if role != 387 or job != 387 or record[164] != 0 or (record[15] != 1):
        raise ValueError('unsupported first constructor role/job/state/category')
    (status, direction) = (work[656], work[650])
    if not 1 <= status <= len(r['status_actions']) or r['status_actions'][status - 1] is None or (not 1 <= direction <= 9):
        raise ValueError('unsupported first constructor status/direction')
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
        raise ValueError('unsupported first constructor initial animation opcode/events')
    raw = bytes.fromhex(program[0]['raw'])
    section = r['program_sections'][block]
    (archive, _, _) = second_resource(387, 0)
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
    put(1278, c['friendly_timeout'], 2)
    work[1282:1284] = bytes.fromhex(r['role_defaults_hex'])[role * 2:role * 2 + 2]
    for at in (1272, 1274, 1276):
        put(at, 65535, 2)
    try:relation=bytes.fromhex(relation_hex)
    except (ValueError,TypeError) as error:raise ValueError('special constructor relation encoding') from error
    if type(selector) is not int or not 0<=selector<16 or len(relation)!=256:
        raise ValueError('special constructor relation ownership')
    mode=r['mode_dispatch'];category=record[164]
    cell=relation[selector*16+category]
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

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--rules-out',required=True);p.add_argument('--fixture-out',required=True);a=p.parse_args()
 for name,data in ((a.rules_out,source_catalog()),(a.fixture_out,native_fixture())):
  (ROOT/name).write_text(report_text(data),encoding='utf-8',newline='\n')
