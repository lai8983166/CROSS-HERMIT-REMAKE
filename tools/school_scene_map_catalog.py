"""Independent scene5 source map inputs and RGB555 texture-page preview.

The preview is a source atlas, not a battle screenshot or unit placement.
"""
import argparse
import hashlib
import json
import struct
from copy import deepcopy
from collections import Counter
from tools.school_unitctrl_map_emulation import map_resource, MAP_HASHES
from tools.school_tactical_resource_catalog import texture_inputs
from tools.school_course_unlock_emulation import AUTHORITY
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256, BASE, report_text

EVIDENCE=ROOT/'analysis/school-unitctrl-map-v1-20261009.json'
EVIDENCE_SHA256='a3153daa1b814e534f9791395bd51db891296db012a38e3b4d2751abe36d499c'


def logical_cells(raw):
    if len(raw)<16:raise ValueError('short logical-map header')
    pw,ph,w,h,tw,th,px,py=struct.unpack_from('<8H',raw)
    if min(w,h,tw,th,px,py)<1 or pw!=w*32 or ph!=h*16 or (pw,ph)!=(tw*px,th*py) \
        or len(raw)!=16+6*w*h:raise ValueError('logical-map dimensions or body differ')
    cells=[list(c) for c in struct.iter_unpack('<3H',raw[16:])]
    return {'pixel_size':[pw,ph],'cell_size':[w,h],'texture_page_size':[tw,th],
        'texture_page_grid':[px,py],'layout':'row-major cell triples, u16 terrain/variant/object',
        'cells':cells,'terrain_counts':{str(k):v for k,v in sorted(Counter(c[0] for c in cells).items())},
        'object_nonzero_count':sum(c[2]!=0 for c in cells)}


def map_textures(raw,logical):
    # Native 43A9F6 passes map resource +0x404 into container loader 4167E0.
    if len(raw)<0x404:raise ValueError('short map texture prefix')
    px,py=logical['texture_page_grid'];tw,th=logical['texture_page_size']
    if struct.unpack_from('<2H',raw)!=(px,py):raise ValueError('map page grids differ')
    entries=texture_inputs(raw[0x404:])
    if len(entries)!=px*py or any(e['kind']!='rgb555_dx' or (e['width'],e['height'])!=(tw,th) for e in entries):
        raise ValueError('map texture-page dimensions/count differ')
    for e in entries:
        e['file_offset']=0x404+e['offset'];e['pixel_file_offset']=e['file_offset']+12
        e['atlas_origin']=[e['index']%px*tw,e['index']//px*th]
    return entries


def decode_rgb555(raw):
    """Expand five-bit channels by bit replication; high bit is not alpha."""
    if len(raw)%2:raise ValueError('odd RGB555 payload')
    result=bytearray()
    for (word,) in struct.iter_unpack('<H',raw):
        for channel in ((word>>10)&31,(word>>5)&31,word&31):
            result.append((channel<<3)|(channel>>2))
    return bytes(result)


def atlas_image(raw,logical,entries):
    from PIL import Image
    image=Image.new('RGB',tuple(logical['pixel_size']));tw,th=logical['texture_page_size']
    for e in entries:
        at=e['pixel_file_offset'];pixels=decode_rgb555(raw[at:at+tw*th*2])
        image.paste(Image.frombytes('RGB',(tw,th),pixels),tuple(e['atlas_origin']))
    return image


def source_catalog():
    image=SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest()!=SOURCE_SHA256:raise ValueError('source executable differs')
    selections=[]
    for i,name in enumerate(MAP_HASHES):
        table=0x6B13F0+i*4;pointer=struct.unpack_from('<I',image,table-BASE+5*16)[0]
        value=image[pointer-BASE:pointer-BASE+260].split(b'\0',1)[0].decode('ascii')
        if value!=name:raise ValueError('original scene5 map table differs')
        selections.append({'table_va':hex(table),'pointer_va':hex(pointer),'scene_id':5,'filename':value})
    raw,identity=map_resource('map05.bin');logical=logical_cells(raw)
    graphics,graphics_identity=map_resource('map05.map');entries=map_textures(graphics,logical)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'scene_id':5,
        'selections':selections,'logical_source':identity,'logical':logical,
        'graphics_source':graphics_identity,'textures':entries,'texture_container_file_offset':0x404,
        'preview_scope':'Source RGB555 pages in row-major order; no camera, units, VM, enemies or events.',**AUTHORITY}


def native_fixture():
    raw=EVIDENCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('frozen native map evidence differs')
    data=json.loads(raw);cases=[]
    for c in data['cases']:
        cases.append({k:deepcopy(c[k]) for k in ('name','ready','unitctrl_constructed','logical_map_loaded',
            'logical_unitctrl','logical_map','scene_graphics_request','persistent_ranges_unchanged','stop_reason')})
        cases[-1]['appearance_grid_sha256']=c['appearance_grid']['sha256'] if c['appearance_grid'] else None
    return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,'cases':cases,**AUTHORITY}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--preview')
    p.add_argument('--fixture-out')
    args=p.parse_args();data=source_catalog()
    (ROOT/args.out).write_text(report_text(data),encoding='utf-8',newline='\n')
    if args.preview:
        raw,_=map_resource('map05.map');atlas_image(raw,data['logical'],data['textures']).save(ROOT/args.preview)
    if args.fixture_out:
        (ROOT/args.fixture_out).write_text(report_text(native_fixture()),encoding='utf-8',newline='\n')
