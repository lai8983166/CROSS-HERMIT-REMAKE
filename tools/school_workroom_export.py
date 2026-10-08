"""Export the actual fifth-week workroom background from original RGB555 bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
from PIL import Image

from tools.render_dximg import render
from tools.school_story_export import source_string
from tools.school_fifth_story_export import text_pool,sc_atlas
from tools.school_story_export import immediate
from tools.tactics_exit_emulation import ROOT,SOURCE,SOURCE_SHA256

BACKGROUND = 'data/adv/bin/bg002_b.bin'


def dialogue(image):
    game = ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/ADV'
    raw = (game/'DAT/CHAPTER205.YBC').read_bytes()
    if (game/'DAT/BIG5/CHAPTER205.YBC').read_bytes() != raw:
        raise ValueError('Chinese Chapter205 differs')
    pool,normalized = text_pool(raw)
    pages,boards,visible,lines,indices = [],{},set(),[],[]
    speaker,active,background = None,None,None
    at,end = struct.unpack_from('<2I',raw,4)
    allowed = {12,17,19,20,21,27,30,43,44,50,51,56,59,151}
    def flush(offset):
        if lines:
            pages.append({'source_offset':offset,'speaker':speaker,'text_indices':indices[:],
                'text':'\n'.join(lines),'background':background,
                'characters':[boards[s].copy() for s in sorted(visible)]})
            lines.clear();indices.clear()
    while at < end:
        op,size = struct.unpack_from('<HH',raw,at)
        if op not in allowed or size < 4 or at+size > end:
            raise ValueError('unsupported workroom dialogue opcode')
        payload = raw[at+4:at+size]
        if op == 59:
            if immediate(payload) != [0,6,1]:
                raise ValueError('unsupported workroom dialogue background')
            background = 6
        elif op == 27:
            if immediate(payload) != [4,0xfffffff,0xfffffff]:
                raise ValueError('unsupported narrator')
            boards[4] = {'asset_key':'narrator'}
        elif op == 30:
            slot,identity,expression,duration = immediate(payload)
            mode = struct.unpack_from('<h',image,0x624520-0x400000+slot*38+8)[0]
            if slot not in (7,8,10) or mode not in (0,1) or expression != 0:
                raise ValueError('unsupported workroom board')
            flush(at)
            kind = 'body' if mode else 'portrait'
            boards[slot] = {'slot':slot,'id':identity,'kind':kind,'asset_key':f'{kind}:{identity}'}
            visible.add(slot)
        elif op == 43:
            flush(at)
            active = immediate(payload)[0]
        elif op == 17:
            index = struct.unpack('<H',payload)[0]
            if active not in boards or not 0 <= index < len(pool):
                raise ValueError('invalid workroom text board')
            speaker = boards[active]['asset_key']
            lines.append(pool[index]['text']);indices.append(index)
        elif op == 51:
            flush(at)
        elif op == 21:
            flush(at);visible.clear()
        elif op == 151 and immediate(payload) != [2,1]:
            raise ValueError('unknown workroom dialogue effect')
        elif op == 19 and at+size != end:
            raise ValueError('unparsed workroom code')
        at += size
    if lines or [i for p in pages for i in p['text_indices']] != list(range(len(pool))):
        raise ValueError('workroom text coverage differs')
    return {'chapter':205,'label':'巡逻班的建议','source':'ADV/DAT/CHAPTER205.YBC',
        'sha256':hashlib.sha256(raw).hexdigest(),'text_pool':pool,'text_encoding':'cp950',
        'cp950_extension_indices':normalized,'pages':pages}


def export(target):
    target = Path(target)
    target.mkdir(parents=True,exist_ok=True)
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError('source executable differs')
    # Chapter018 chooses index6. Native49F6C0 reads the same table.
    if source_string(image,0x621BBC,6).decode('ascii').lower() != 'bg002_b.bin':
        raise ValueError('workroom background source table differs')
    source = ROOT/'CROSS HERMIT/CROSS HERMIT'/BACKGROUND
    raw = source.read_bytes()
    if len(raw) != 24+1024*1024*2 or raw[12:16] != b'DX'+bytes([2,0]) \
            or tuple(struct.unpack_from('<4H',raw,16)) != (1024,768,1024,1024):
        raise ValueError('unsupported workroom background header')
    decoded = render(source)
    if decoded.getbbox() != (0,0,1024,768):
        raise ValueError('workroom content bounds differ')
    decoded.crop((0,0,1024,768)).save(target/'background.png')
    story = dialogue(image)
    actors = {'narrator':{'name':'老师','image':''}}
    sources = {}
    game = ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/ADV'
    for kind,identity in sorted({(c['kind'],c['id']) for p in story['pages'] for c in p['characters']}):
        table,stride = (0x622250,8) if kind == 'body' else (0x622668,60)
        filename = source_string(image,table,identity,stride).decode('ascii').upper()
        path = game/'BIN'/filename
        if kind == 'body':
            rendered = render(path)
            atlas = Image.frombytes('RGBA',(512,1024),rendered.tobytes())
            x,y = struct.unpack_from('<2h',image,table-0x400000+identity*stride+4)
            body = atlas.crop((0,0,512,768));crop = [0,768,128,896]
        else:
            atlas = sc_atlas(path)
            x,y,w,h = struct.unpack_from('<4h',image,table-0x400000+identity*stride+4)
            flags,sx,sy = struct.unpack_from('<3h',image,table-0x400000+identity*stride+12)
            if flags != 0:
                raise ValueError('unsupported portrait expression')
            body = atlas.crop((0,0,256,296));crop = [sx,sy,sx+w,sy+h]
        body.alpha_composite(atlas.crop(tuple(crop)),(x,y))
        output = f'{kind}_{identity}.png';body.save(target/output)
        actors[f'{kind}:{identity}'] = {'name':source_string(image,0x621F2C,identity).decode('cp950'),
            'image':output,'kind':kind,'id':identity,'source':'ADV/BIN/'+filename,
            'atlas_size':list(atlas.size),'body_crop':[0,0,*body.size],
            'expression_crop':crop,'expression_destination':[x,y]}
        sources['ADV/BIN/'+filename] = hashlib.sha256(path.read_bytes()).hexdigest()
    catalog = {'schema_version':1,'source_image_sha256':SOURCE_SHA256,
        'source_table_va':'0x621bbc','background_id':6,'source_path':BACKGROUND,
        'source_sha256':hashlib.sha256(raw).hexdigest(),'crop':[0,0,1024,768],
        'pixel_format':'X1RGB555 little endian, bit15 alpha',
        'outputs_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(target.glob('*.png'))},
        'scenes':[story],'actors':actors,'backgrounds':{'6':{'image':'background.png','source':BACKGROUND}},
        'source_assets_sha256':sources,
        'scope':'Original background and Chapter205 dialogue/default portraits. Remake controls; shopping/news original menus are not reproduced.'}
    (target/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    return catalog


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',default='prototype/assets/school_workroom')
    args = parser.parse_args()
    export(ROOT/args.out)
