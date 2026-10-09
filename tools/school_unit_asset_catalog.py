"""Independent original unit text tables and effect metadata provenance."""
import argparse
from copy import deepcopy
import hashlib
import json
import struct
from tools.school_unit_assets_emulation import TEXT_GROUPS, effect_resource
from tools.school_tactical_resource_catalog import container_sections
from tools.dxanim_lib import parse_dxanim, parse_container, parse_program_blocks
from tools.tactics_exit_emulation import ROOT, BASE, SOURCE, SOURCE_SHA256, report_text
from tools.school_course_unlock_emulation import AUTHORITY

EVIDENCE = ROOT/'analysis/school-unit-assets-v1-20261010.json'
EVIDENCE_SHA256 = '2fc5bcefd011b62f1486a3edf3699b3cd528843a21910c64a6eee022c6be987d'


def original_text_tables(image):
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError('original image differs')
    tables = []
    for table,count,destination in TEXT_GROUPS:
        entries = []
        for index in range(count):
            pointer = struct.unpack_from('<I',image,table-BASE+index*4)[0]
            offset = pointer-BASE
            if not 0 <= offset <= len(image)-1024:
                raise ValueError('original unit text pointer bounds')
            candidate = image[offset:offset+1024]
            if b'\0' not in candidate:
                raise ValueError('original unit text lacks terminator')
            raw = candidate.split(b'\0',1)[0]
            entries.append({'index':index,'pointer':pointer,'text_hex':raw.hex(),
                            'destination_offset':destination+index*128})
        tables.append({'table_va':hex(table),'count':count,'destination_offset':destination,'entries':entries})
    return tables


def effect_metadata(raw):
    offsets = parse_dxanim(raw)
    if len(offsets) != 7:
        raise ValueError('effect needs original seven sections')
    sections = container_sections(raw)
    if offsets != [s['offset'] for s in sections] or offsets[6] <= offsets[5]:
        raise ValueError('effect source sections differ')
    for s in sections:
        at = s['offset']
        if s['index'] in (4,5):
            s['kind'] = 'draw_descriptors' if s['index'] == 4 else 'canvas_rectangles'
            continue
        size,count,entries = parse_container(raw,at)
        if size > s['bytes'] or size < 8+count*4 or any(x > size for x in entries):
            raise ValueError('effect nested section bounds')
        s.update({'container_bytes':size,'entry_count':count,'entry_offsets':entries})
    # Animation programs are decoded by the existing independent source parser.
    programs = parse_program_blocks(raw,offsets)
    return {'sections':sections,'metadata_bytes':offsets[6],
            'metadata_sha256':hashlib.sha256(raw[:offsets[6]]).hexdigest(),
            'program_counts':[len(p) for p in programs],
            'instructions':sum(len(program) for group in programs for program in group),
            'scope':'Exact effect metadata/input programs; no native texture binding/rendering'}


def source_catalog():
    image = SOURCE.read_bytes()
    raw,identity = effect_resource()
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,
            'text_tables':original_text_tables(image),'effect_source':identity,
            'effect':effect_metadata(raw),'effect_animation_table':struct.unpack_from('<I',image,0x60E850-BASE)[0],
            'effect_position_table':struct.unpack_from('<I',image,0x60F070-BASE)[0],
            'default_relation_hex':image[0x618568-BASE:0x618568-BASE+256].hex(),**AUTHORITY}


def native_fixture():
    raw = EVIDENCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != EVIDENCE_SHA256:
        raise ValueError('frozen unit asset report differs')
    data = json.loads(raw)
    return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,'cases':[
        {k:deepcopy(c[k]) for k in ('name','ready','unit_assets_prepared','unit_assets','unit_reset_snapshot',
            'text_requests','asset_requests','asset_allocations','persistent_ranges_unchanged',
            'current_combat_records_unchanged','stop_reason') if k in c} for c in data['cases']],**AUTHORITY}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rules-out',required=True)
    p.add_argument('--fixture-out',required=True)
    args = p.parse_args()
    rules,fixture = source_catalog(),native_fixture()
    for name,data in [(args.rules_out,rules),(args.fixture_out,fixture)]:
        (ROOT/name).write_text(report_text(data),encoding='utf-8',newline='\n')
