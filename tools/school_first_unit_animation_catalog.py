"""Independent original first unit archive, palette/mask and binding inputs."""
import argparse
from copy import deepcopy
import hashlib
import json
import struct
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from capstone.x86_const import X86_OP_IMM,X86_OP_MEM
from tools.dxanim_lib import parse_dxanim,parse_container,parse_program_blocks
from tools.school_tactical_resource_catalog import texture_inputs
from tools.school_first_unit_animation_emulation import unit_resource
from tools.tactics_exit_emulation import ROOT,SOURCE,SOURCE_SHA256,BASE,report_text
from tools.school_course_unlock_emulation import AUTHORITY

EVIDENCE = ROOT/'analysis/school-first-unit-animation-v1-20261010.json'
EVIDENCE_SHA256 = 'f929d55717a2ab6d2513db6834b455e73c1746b15d178e7588752143b0990c2f'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def animation_inputs(raw):
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
    if images.get('entry_count')!=193 or palettes.get('entry_count')!=40:
        raise ValueError('unsupported unit image/palette count')
    if sections[8]['bytes']!=196 or raw[offsets[8]+193:]!=bytes(3):
        raise ValueError('unit palette mask size/padding')
    mask = raw[offsets[8]:offsets[8]+193]
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


def source_catalog():
    image = SOURCE.read_bytes()
    if digest(image)!=SOURCE_SHA256:
        raise ValueError('first animation executable source differs')
    md = Cs(CS_ARCH_X86,CS_MODE_32)
    md.detail = True
    code = []
    def value(va,mnemonic):
        i = next(md.disasm(image[va-BASE:va-BASE+16],va,count=1))
        if i.mnemonic!=mnemonic or i.operands[-1].type not in (X86_OP_IMM,X86_OP_MEM):
            raise ValueError(f'first animation source instruction differs at {va:#x}')
        last = i.operands[-1]
        result = last.imm if last.type==X86_OP_IMM else last.mem.disp
        code.append({'va':hex(va),'instruction_hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str,'value':result})
        return result
    constants = {'image_section':value(0x409C36,'push'),'palette_section':value(0x409D0E,'push'),
        'mask_section':value(0x409DA3,'push'),'palette_index_subtract':value(0x409D54,'sub'),
        'palette_colors':value(0x4049F2,'cmp'),'palette_stride_shift':value(0x420A92,'shr'),
        'bitmap_palette_offset':value(0x404970,'add'),'texture_stride':value(0x41F136,'imul'),
        'texture_count_prefix':value(0x41F139,'add'),'native_format':value(0x4036A5,'mov'),
        'width_field':next(md.disasm(image[0x404A4A-BASE:0x404A4A-BASE+16],0x404A4A,count=1)).operands[0].mem.disp,
        'height_field':next(md.disasm(image[0x404A58-BASE:0x404A58-BASE+16],0x404A58,count=1)).operands[0].mem.disp,
        'mode_field':next(md.disasm(image[0x40B983-BASE:0x40B983-BASE+16],0x40B983,count=1)).operands[0].mem.disp,
        'mode':value(0x466D7B,'push')}
    # Include dynamic field-write instructions and exact palette branch bodies.
    for va in (0x404A4A,0x404A58,0x40B983,0x409C5F,0x409CA0,0x409CB4,0x409CC8,0x409CDC,
               0x409CF0,0x41EC6B,0x41EC73,0x41ECE5,0x409E3E,0x41F1E1,0x41F1ED):
        i = next(md.disasm(image[va-BASE:va-BASE+16],va,count=1))
        code.append({'va':hex(va),'instruction_hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
    blocks = [{'start':hex(a),'end':hex(b),'instruction_hex':image[a-BASE:b-BASE].hex(),'sha256':digest(image[a-BASE:b-BASE])}
              for a,b in ((0x409D1F,0x409D64),(0x41F20B,0x41F23A),(0x404967,0x404A40),(0x420A77,0x420AAA))]
    raw,identity = unit_resource()
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'source':identity,'animation':animation_inputs(raw),
        'constants':constants,'code_inputs':code,'source_branch_bodies':blocks,
        'scope':'Original bytes/EXE inputs only. Heap zero input and GPU boundaries remain explicit; no playable unit or placement.',**AUTHORITY}


def normalize_palette(raw):
    if len(raw)!=1024:
        raise ValueError('unit palette must contain256 BGRA colors')
    result = bytearray(raw)
    for index in range(1,256):
        at = index*4
        if result[at:at+3]==bytes(3):
            result[at:at+4]=result[:4]
    return bytes(result)


def expected_binding(before_controller_hex,file_pointer,metadata_pointer,texture_allocation,texture_table,variant=3,rules=None):
    rules = source_catalog() if rules is None else rules
    if not isinstance(before_controller_hex,str):
        raise ValueError('invalid first animation controller hex type')
    try:
        controller = bytearray.fromhex(before_controller_hex)
    except ValueError as exc:
        raise ValueError('invalid first animation controller hex') from exc
    if len(controller)!=84 or isinstance(variant,bool) or not isinstance(variant,int) or variant!=3:
        raise ValueError('unsupported unit animation binding inputs')
    pointers = (file_pointer,metadata_pointer,texture_allocation,texture_table)
    if any(isinstance(p,bool) or not isinstance(p,int) or not 0<p<0xFFFFFFFF-0x200000 or p%4 for p in pointers):
        raise ValueError('unit animation pointer bounds')
    slot = struct.unpack_from('<I',controller,0x28)[0]
    if slot!=110:
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
    raw,_ = unit_resource()
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


def native_fixture():
    raw = EVIDENCE.read_bytes()
    if digest(raw)!=EVIDENCE_SHA256:
        raise ValueError('frozen first unit animation report differs')
    data = json.loads(raw)
    fields = ('name','ready','first_unit_animation_loaded','first_unit_animation','unit_texture_entries',
        'unit_animation_boundaries','file_events','first_unit_animation_retained_ranges_unchanged',
        'persistent_ranges_unchanged','battle_world_constructed','stop_reason')
    return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,
        'cases':[{**{k:deepcopy(c[k]) for k in fields if k in c},
            'map_common_file_events':deepcopy((c.get('map_common') or {}).get('file_events',[]))} for c in data['cases']],**AUTHORITY}


if __name__=='__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rules-out',required=True)
    p.add_argument('--fixture-out',required=True)
    args = p.parse_args()
    for name,data in ((args.rules_out,source_catalog()),(args.fixture_out,native_fixture())):
        (ROOT/name).write_text(report_text(data),encoding='utf-8',newline='\n')
