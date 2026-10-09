"""Independent original-byte inputs for the current tactical resource audit.

Contains no emulator output, unit placement or inferred map identity.
"""
import argparse
import hashlib
import json
import struct
from copy import deepcopy
from tools.school_tactical_resources_emulation import RESOURCE_NAMES, original_resource
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256, BASE, report_text
from tools.school_course_unlock_emulation import AUTHORITY

EVIDENCE=ROOT/'analysis/school-tactical-resources-v1-20261009.json'
EVIDENCE_SHA256='4c48078de40cd452b486292c5b7e17d08ea0319f39339281d3d1f4a710a30a42'


def container_sections(raw):
    if len(raw)<12 or struct.unpack_from('<I',raw)[0]!=len(raw):
        raise ValueError('container total length differs')
    count=struct.unpack_from('<I',raw,4)[0]
    if not 1<=count<=580 or 8+count*4>len(raw):raise ValueError('container count differs')
    offsets=list(struct.unpack_from('<'+str(count)+'I',raw,8))+[len(raw)]
    if offsets[0]!=8+count*4 or any(a>=b for a,b in zip(offsets,offsets[1:])):
        raise ValueError('container offset bounds/order differs')
    return [{'index':i,'offset':a,'bytes':b-a,'sha256':hashlib.sha256(raw[a:b]).hexdigest()}
            for i,(a,b) in enumerate(zip(offsets,offsets[1:]))]


def texture_inputs(raw):
    entries=container_sections(raw)
    for entry in entries:
        at=entry['offset'];chunk=raw[at:at+entry['bytes']]
        entry['header_hex']=chunk[:16].hex()
        if chunk.startswith(b'Dm-No-MakeTex\0'):
            if len(chunk)!=16 or chunk[13:]!=bytes(3):raise ValueError('no-texture marker differs')
            kind,width,height,fmt='no_texture',0,0,0x19
        elif chunk.startswith(b'BM'):
            if len(chunk)<54:raise ValueError('short bitmap header')
            size,body=struct.unpack_from('<I',chunk,2)[0],struct.unpack_from('<I',chunk,10)[0]
            header,width,height,planes,bpp,compression=struct.unpack_from('<IiiHHI',chunk,14)
            colors=struct.unpack_from('<I',chunk,46)[0] or (body-54)//4
            stride=(width+3)&~3
            if header!=40 or planes!=1 or bpp!=8 or compression!=0 or not 1<=colors<=256 \
                or width<1 or height<1 or body!=54+colors*4 \
                or size not in (body+stride*height,(body+stride*height+3)&~3) \
                or len(chunk)!=((body+stride*height+3)&~3):
                raise ValueError('unsupported indexed bitmap layout')
            kind,fmt='indexed_bmp',0x19
            entry.update({'bitmap_bytes':size,'pixel_offset':body,'row_stride':stride,'palette_count':colors})
        elif chunk.startswith(b'DX'):
            if len(chunk)<12:raise ValueError('short DX header')
            mode,width,height,storage_width,storage_height=struct.unpack_from('<5H',chunk,2)
            if mode!=2 or min(width,height)<1 or (width,height)!=(storage_width,storage_height) \
                or len(chunk)!=12+width*height*2:
                raise ValueError('unsupported RGB555 layout')
            kind,fmt='rgb555_dx',0x19
        else:raise ValueError('unknown texture entry')
        entry.update({'kind':kind,'width':width,'height':height,'native_format':fmt})
    return entries


def source_catalog():
    image=SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest()!=SOURCE_SHA256:raise ValueError('source executable differs')
    selections=[]
    for table,name in [(0x60C2B8,'TactStart05.bin'),(0x60BC78,'t0005.bin')]:
        pointer=struct.unpack_from('<I',image,table-BASE+5*4)[0]
        value=image[pointer-BASE:pointer-BASE+260].split(b'\0',1)[0].decode('ascii')
        if value!=name:raise ValueError('scene5 source selection differs')
        selections.append({'table_va':hex(table),'pointer_va':hex(pointer),'scene_id':5,'filename':value})
    resources=[]
    for i,name in enumerate(RESOURCE_NAMES):
        raw,identity=original_resource(name)
        resource={'source':identity,'sections':container_sections(raw),
                  'kind':'scene_script' if i==3 else 'texture_container'}
        if i<3:
            resource['texture_entries']=texture_inputs(raw)
            resource['native_texture_slot']=[0x5A,0x5B,0x14][i]
        resources.append(resource)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'scene_id':5,
        'selections':selections,'resources':resources,
        'scope':'Source byte inputs only; scene script sections remain opaque, VM/map/enemy/event initialization unexecuted.',
        **AUTHORITY}


def native_fixture():
    raw=EVIDENCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('frozen native resource evidence differs')
    data=json.loads(raw);cases=[]
    fields=('resource','index','offset','bytes','header_hex','width','height','format')
    for c in data['cases']:
        cases.append({'name':c['name'],'ready':c['ready'],
            'loaded_resources':[{'relative_path':r['source']['relative_path'],'bytes':r['loaded_bytes'],
                                 'sha256':r['loaded_sha256']} for r in c['requests']],
            'texture_entries':[{k:deepcopy(e[k]) for k in fields} for e in c['texture_entries']],
            'scene_script':deepcopy(c['scene_script']),
            **{k:c[k] for k in ('persistent_ranges_unchanged','buffers_loaded','gpu_textures_uploaded',
                                'unitctrl_constructed','battle_world_constructed','stop_reason')}})
    return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,'cases':cases,**AUTHORITY}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',default='prototype/data/school_tactical_resources_rules.json')
    p.add_argument('--fixture-out');args=p.parse_args()
    (ROOT/args.out).write_text(report_text(source_catalog()),encoding='utf-8',newline='\n')
    if args.fixture_out:
        (ROOT/args.fixture_out).write_text(report_text(native_fixture()),encoding='utf-8',newline='\n')
