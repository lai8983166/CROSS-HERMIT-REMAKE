"""Independent original minimap/VPT inputs and current-map runtime art."""
import argparse
from copy import deepcopy
import hashlib
import io
import json
import struct
from PIL import Image
from tools.school_unitctrl_map_emulation import map_resource
from tools.school_tactical_resource_catalog import container_sections
from tools.school_scene_map_catalog import source_catalog as map_catalog,atlas_image
from tools.tactics_exit_emulation import ROOT,report_text
from tools.school_course_unlock_emulation import AUTHORITY

EVIDENCE=ROOT/'analysis/school-scene-resources-v1-20261009.json'
EVIDENCE_SHA256='81924937ded1ed70e5889dd068abe05e2479caf3c50210a9275bc3b7eb35abac'
ART=ROOT/'prototype/assets/current_scene'


def minimap_input(raw):
    if len(raw)<1078 or raw[:2]!=b'BM':raise ValueError('short/unknown minimap bitmap')
    size=struct.unpack_from('<I',raw,2)[0];body=struct.unpack_from('<I',raw,10)[0]
    header,w,h,planes,bpp,compression=struct.unpack_from('<IiiHHI',raw,14)
    colors=struct.unpack_from('<I',raw,46)[0] or 256
    stride=(w+3)&~3
    if header!=40 or min(w,h)<1 or planes!=1 or bpp!=8 or compression!=0 or colors!=256 \
        or body!=1078 or size!=len(raw) or len(raw)!=body+stride*h:raise ValueError('unsupported minimap layout')
    image=Image.open(io.BytesIO(raw)).convert('RGB')
    # BMP is bottom-up BGR palette indexed; independently check all pixels.
    pixels=bytearray()
    for y in range(h):
        row=body+(h-1-y)*stride
        for x in range(w):
            at=54+raw[row+x]*4;pixels.extend(raw[at:at+3][::-1])
    if image.tobytes()!=bytes(pixels):raise ValueError('minimap decoded pixels differ')
    return {'width':w,'height':h,'pixel_offset':body,'row_stride':stride,'palette_count':colors,
        'rgb_sha256':hashlib.sha256(pixels).hexdigest()},image


def pathfinding_input(raw,cells=6144):
    entries=container_sections(raw)
    if len(entries)!=8:raise ValueError('pathfinding needs eight sections')
    for e in entries:
        at=e['offset'];chunk=raw[at:at+e['bytes']]
        if e['index']<4:
            if chunk[:16]!=bytes.fromhex('4d617045646974466c4944436f646500') or len(chunk)<24 or struct.unpack_from('<I',chunk,16)[0]!=28:raise ValueError('pathfinding section marker differs')
            count=struct.unpack_from('<I',chunk,20)[0]
            if not 1<=count<=cells or 24+count*4>len(chunk):raise ValueError('pathfinding relocation count differs')
            offsets=list(struct.unpack_from('<'+str(count)+'I',chunk,24))
            if offsets[0]!=24+count*4 or any(x%4 or x>=len(chunk) for x in offsets) \
                or any(x>=y for x,y in zip(offsets,offsets[1:])):raise ValueError('pathfinding relocation offset bounds/order')
            e.update({'kind':'relocated_offset_table','relocation_count':count,'relative_offsets':offsets})
        else:
            if len(chunk)!=cells*2:raise ValueError('pathfinding cell section dimensions differ')
            e.update({'kind':'opaque_u16_cell_values','cell_count':cells})
    return entries


def relocated_pathfinding(raw,pointer,entries):
    out=bytearray(raw)
    for e in entries[:4]:
        for i,offset in enumerate(e['relative_offsets']):
            struct.pack_into('<I',out,e['offset']+24+i*4,pointer+e['offset']+offset)
    return bytes(out)


def source_catalog():
    maps=map_catalog();bmp,bmp_id=map_resource('map05.bmp');vpt,vpt_id=map_resource('map05.vpt')
    mini,_=minimap_input(bmp)
    return {'schema_version':1,'scene_id':5,'minimap_source':bmp_id,'minimap':mini,
        'pathfinding_source':vpt_id,'pathfinding_sections':pathfinding_input(vpt),
        'map_source':maps['graphics_source'],'texture_entries':maps['textures'],
        'fog_initial_u16':0x8000,'scope':'Original scene input bytes; no unit assets, VM/event/enemy/placement interpretation.',**AUTHORITY}


def native_fixture():
    raw=EVIDENCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('frozen scene resource evidence differs')
    data=json.loads(raw)
    return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,'cases':[
        {k:deepcopy(c[k]) for k in ('name','ready','scene_resources_loaded','scene_requests','scene_resources',
            'persistent_ranges_unchanged','current_combat_records_unchanged','stop_reason') if k in c}
        for c in data['cases']],**AUTHORITY}


def export_art():
    ART.mkdir(parents=True,exist_ok=True);maps=map_catalog();raw,_=map_resource('map05.map')
    atlas=atlas_image(raw,maps['logical'],maps['textures']);atlas.save(ART/'map05.png')
    bmp,_=map_resource('map05.bmp');mini_data,mini=minimap_input(bmp);mini.save(ART/'map05_minimap.png')
    manifest={'schema_version':1,'scene_id':5,'pixel_size':maps['logical']['pixel_size'],
        'cell_size':maps['logical']['cell_size'],'atlas':'res://assets/current_scene/map05.png',
        'minimap':'res://assets/current_scene/map05_minimap.png','scope':'current_scene_map_preview_only',
        'map_source':maps['graphics_source'],'minimap_source':map_resource('map05.bmp')[1],
        'atlas_file_sha256':hashlib.sha256((ART/'map05.png').read_bytes()).hexdigest(),
        'minimap_file_sha256':hashlib.sha256((ART/'map05_minimap.png').read_bytes()).hexdigest(),
        'atlas_rgb_sha256':hashlib.sha256(atlas.tobytes()).hexdigest(),'minimap_rgb_sha256':mini_data['rgb_sha256']}
    (ART/'catalog.json').write_text(report_text(manifest),encoding='utf-8',newline='\n')


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--fixture-out');p.add_argument('--art',action='store_true')
    args=p.parse_args();(ROOT/args.out).write_text(report_text(source_catalog()),encoding='utf-8',newline='\n')
    if args.fixture_out:(ROOT/args.fixture_out).write_text(report_text(native_fixture()),encoding='utf-8',newline='\n')
    if args.art:export_art()
