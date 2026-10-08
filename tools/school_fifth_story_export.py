"""Export bounded Chapter018 MC/SC presentation; preserve the older catalog."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import struct

from PIL import Image
from tools.school_story_export import GAME, immediate, source_string
from tools.render_dximg import render
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256

ALLOWED = {12,13,17,19,20,21,30,32,33,36,43,44,50,51,56,59,63,65,67,69,74,91,151}


def text_pool(raw):
    pool = struct.unpack_from('<I',raw,12)[0]
    count = struct.unpack_from('<I',raw,pool)[0]
    if not 1 <= count <= 256:
        raise ValueError('unbounded text pool')
    result,extended = [],[]
    for index in range(count):
        off,param = struct.unpack_from('<HH',raw,pool+4+index*4)
        if off < 4+count*4 or pool+off >= len(raw):
            raise ValueError('invalid text offset')
        data = raw[pool+off:raw.index(0,pool+off)]
        try:
            data.decode('big5',errors='strict')
        except UnicodeDecodeError:
            extended.append(index)
        # Source Windows Chinese codepage includes F9D8 (裏) in text99.
        text = data.decode('cp950',errors='strict')
        result.append({'text':text,'pool_parameter':param,'raw_sha256':hashlib.sha256(data).hexdigest()})
    return result,extended


def instructions(raw):
    if struct.unpack_from('<I',raw)[0] != 4:
        raise ValueError('unsupported ADV container')
    offsets = struct.unpack_from('<4I',raw,4)
    if not 20 == offsets[0] < offsets[1] <= offsets[2] <= offsets[3] <= len(raw):
        raise ValueError('invalid ADV offsets')
    at = offsets[0]
    while at < offsets[1]:
        op,size = struct.unpack_from('<HH',raw,at)
        if op not in ALLOWED or size < 4 or at+size > offsets[1]:
            raise ValueError(f'unsupported fifth-week instruction {op} at {at:#x}')
        yield at,op,raw[at+4:at+size]
        at += size
        if op == 19:
            if at != offsets[1]:
                raise ValueError('unparsed code tail')
            return
    raise ValueError('missing END')


def sc_atlas(path):
    raw = path.read_bytes()
    if len(raw) != 24+256*512*2 or raw[12:16] != b'DX\x02\x00' \
            or struct.unpack_from('<4H',raw,16) != (256,512,256,512):
        raise ValueError('unsupported SC atlas header')
    # Same byte length as 512x512 TC masks, but source header declares 16bit SC.
    pixels = struct.unpack('<'+str(256*512)+'H',raw[24:])
    atlas = Image.new('RGBA',(256,512))
    atlas.putdata([(((v >> 10)&31)*255//31,((v >> 5)&31)*255//31,
        (v&31)*255//31,255 if v&0x8000 else 0) for v in pixels])
    return atlas


def scene(image):
    raw = (GAME/'DAT/CHAPTER018.YBC').read_bytes()
    if (GAME/'DAT/BIG5/CHAPTER018.YBC').read_bytes() != raw:
        raise ValueError('Chinese control bytes differ')
    pool,normalized = text_pool(raw)
    pages,boards,visible,lines,indices,effects = [],{},set(),[],[],[]
    background,active,speaker = None,None,None
    def page(offset):
        return {'source_offset':offset,'speaker':speaker,'text_indices':indices[:],
            'text':'\n'.join(lines),'background':background,
            'characters':[deepcopy(boards[slot]) for slot in sorted(visible)]}
    for offset,op,payload in instructions(raw):
        if op == 59:
            slot,background,mode = immediate(payload)
            if (slot,mode) != (0,1):
                raise ValueError('unsupported background')
        elif op in (30,33):
            values = immediate(payload)
            slot,identity,expression = values[:3]
            # Original board configuration selects MC (mode1) vs SC (mode0).
            mode = struct.unpack_from('<h',image,0x624520-0x400000+slot*38+8)[0]
            if slot not in (5,6,7,8,9) or mode not in (0,1) or expression != 0:
                raise ValueError('unsupported character board/expression')
            if lines:
                pages.append(page(offset))
                lines,indices,speaker = [],[],None
            kind = 'body' if mode == 1 else 'portrait'
            boards[slot] = {'slot':slot,'id':identity,'kind':kind,'asset_key':f'{kind}:{identity}'}
            if op == 30:
                visible.add(slot)
        elif op == 32:
            visible.discard(immediate(payload)[0])
        elif op == 43:
            if lines:
                pages.append(page(offset))
                lines,indices,speaker = [],[],None
            active = immediate(payload)[0]
        elif op == 17:
            index = struct.unpack('<H',payload)[0]
            if active not in boards or index >= len(pool):
                raise ValueError('unknown text board/index')
            current = boards[active]['asset_key']
            if lines and speaker != current:
                raise ValueError('mixed speakers')
            speaker = current
            lines.append(pool[index]['text'])
            indices.append(index)
        elif op == 51 and lines:
            pages.append(page(offset))
            lines,indices,speaker = [],[],None
        elif op == 21:
            visible.clear()
        elif op in (91,151):
            operands = immediate(payload)
            if operands != ([2,1] if op == 151 else [6,2]):
                raise ValueError('unknown fifth-week effect')
            effects.append({'offset':offset,'opcode':op,'operands':operands})
    if lines or [i for p in pages for i in p['text_indices']] != list(range(len(pool))):
        raise ValueError('text coverage differs')
    return {'chapter':18,'label':'前往沉思之都','source':'ADV/DAT/CHAPTER018.YBC',
        'sha256':hashlib.sha256(raw).hexdigest(),'text_pool':pool,
        'text_encoding':'cp950','cp950_extension_indices':normalized,'pages':pages,'effectful_tail':effects}


def export(out):
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError('source executable differs')
    story = scene(image)
    out.mkdir(parents=True,exist_ok=True)
    actors,sources = {},{}
    appearances = {(c['kind'],c['id']) for p in story['pages'] for c in p['characters']}
    for kind,identity in sorted(appearances):
        table,stride = (0x622250,8) if kind == 'body' else (0x622668,60)
        filename = source_string(image,table,identity,stride).decode('ascii').upper()
        atlas = render(str(GAME/'BIN'/filename)) if kind == 'body' else sc_atlas(GAME/'BIN'/filename)
        if kind == 'body':
            atlas = Image.frombytes('RGBA',(512,1024),atlas.tobytes())
            x,y = struct.unpack_from('<hh',image,table-0x400000+identity*stride+4)
            body = atlas.crop((0,0,512,768))
            crop = [0,768,128,896]
        else:
            x,y,w,h = struct.unpack_from('<4h',image,table-0x400000+identity*stride+4)
            flags,sx,sy = struct.unpack_from('<3h',image,table-0x400000+identity*stride+12)
            if flags != 0 or w <= 0 or h <= 0:
                raise ValueError('unsupported SC expression geometry')
            body = atlas.crop((0,0,256,296))
            crop = [sx,sy,sx+w,sy+h]
        body.alpha_composite(atlas.crop(tuple(crop)),(x,y))
        output = f'{kind}_{identity}.png'
        body.save(out/output)
        actors[f'{kind}:{identity}'] = {'name':source_string(image,0x621F2C,identity).decode('big5',errors='strict'),
            'image':output,'source':'ADV/BIN/'+filename,'kind':kind,'id':identity,
            'atlas_size':list(atlas.size),'body_crop':[0,0,*body.size],
            'expression_crop':crop,'expression_destination':[x,y],'expression':0}
        sources['ADV/BIN/'+filename] = hashlib.sha256((GAME/'BIN'/filename).read_bytes()).hexdigest()
    backgrounds = {}
    for identity in sorted({p['background'] for p in story['pages']}):
        filename = source_string(image,0x621BBC,identity).decode('ascii').upper()
        output = f'background_{identity}.png'
        render(str(GAME/'BIN'/filename)).crop((0,0,1024,768)).save(out/output)
        backgrounds[str(identity)] = {'image':output,'source':'ADV/BIN/'+filename}
        sources['ADV/BIN/'+filename] = hashlib.sha256((GAME/'BIN'/filename).read_bytes()).hexdigest()
    sources['ADV/BIN/TC0405.BIN'] = hashlib.sha256((GAME/'BIN/TC0405.BIN').read_bytes()).hexdigest()
    result = {'version':1,'source_image_sha256':SOURCE_SHA256,'scenes':[story],
        'actors':actors,'backgrounds':backgrounds,'source_assets_sha256':sources,
        'outputs_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('*.png'))},
        'presentation_scope':'Original dialogue, current board identity, MC/SC geometry, default expression and visibility; remake layout/click timing; movie/audio/fade rendering not reproduced.',
        'tables':{'names':'0x621f2c','board_configuration':'0x624520','MC':'0x622250','SC':'0x622668',
            'body_draw':'0x4c9690','expression_draw':'0x4c97a0','character_replace':'0x4cc0f0'}}
    (out/'catalog.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    return deepcopy(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=ROOT/'prototype/assets/school_fifth_story')
    args = parser.parse_args()
    result = export(args.out)
    print('Exported fifth-week pages:',len(result['scenes'][0]['pages']))
