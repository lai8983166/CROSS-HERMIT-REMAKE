"""Export only the linear Chapter016/017 presentation from original bytes."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import struct

from PIL import Image
from tools.render_dximg import render
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256

GAME = ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/ADV'
CHAPTERS = (16,17)
ALLOWED = {12,15,17,19,20,21,22,24,27,30,32,35,43,44,50,51,56,59,63,65}


def source_string(image,table,index,stride=4):
    pointer = struct.unpack_from('<I',image,table-0x400000+index*stride)[0]
    at = pointer-0x400000
    return image[at:image.index(0,at)]


def instructions(raw):
    count = struct.unpack_from('<I',raw)[0]
    if count != 4:
        raise ValueError('unsupported ADV container')
    offsets = struct.unpack_from('<4I',raw,4)
    if not 20 == offsets[0] < offsets[1] <= offsets[2] <= offsets[3] <= len(raw):
        raise ValueError('invalid ADV offsets')
    at = offsets[0]
    while at < offsets[1]:
        op,size = struct.unpack_from('<HH',raw,at)
        if op not in ALLOWED or size < 4 or at+size > offsets[1]:
            raise ValueError(f'unsupported presentation instruction {op} at {at:#x}')
        yield at,op,raw[at+4:at+size]
        at += size
        if op == 19:
            if at != offsets[1]:
                raise ValueError('unparsed code tail')
            return
    raise ValueError('missing END')


def immediate(payload):
    if len(payload)%4:
        raise ValueError('unaligned operands')
    result = []
    for at in range(0,len(payload),4):
        value = struct.unpack_from('<I',payload,at)[0]
        if value >> 28 != 2:
            raise ValueError('presentation operand must be immediate')
        result.append(value & 0xfffffff)
    return result


def text_pool(raw):
    pool = struct.unpack_from('<I',raw,12)[0]
    count = struct.unpack_from('<I',raw,pool)[0]
    if not 1 <= count <= 256:
        raise ValueError('unbounded text pool')
    result,normalized = [],[]
    for index in range(count):
        off,param = struct.unpack_from('<HH',raw,pool+4+index*4)
        if off < 4+count*4 or pool+off >= len(raw):
            raise ValueError('invalid text offset')
        end = raw.index(0,pool+off)
        data = raw[pool+off:end]
        if b'\x81\x40' in data:
            normalized.append(index)
        # Japanese fullwidth-space bytes survive in six Chinese source strings.
        text = data.replace(b'\x81\x40',b'\xa1\x40').decode('big5',errors='strict')
        result.append({'text':text,'pool_parameter':param,'raw_sha256':hashlib.sha256(data).hexdigest()})
    return result,normalized


def scene(chapter,image):
    filename = f'CHAPTER{chapter:03}.YBC'
    raw = (GAME/'DAT'/filename).read_bytes()
    if (GAME/'DAT/BIG5'/filename).read_bytes() != raw:
        raise ValueError('Chinese resource/control bytes differ')
    pool,normalized = text_pool(raw)
    pages,boards,visible,lines,indices = [],{},set(),[],[]
    active,background = None,None
    speaker = None
    def page(offset):
        return {'source_offset':offset,'speaker':speaker,'text_indices':indices[:],
            'text':'\n'.join(lines),'background':background,
            'characters':[{'slot':slot,'id':boards[slot]} for slot in sorted(visible)]}
    for offset,op,payload in instructions(raw):
        if op == 59:
            slot,identity,mode = immediate(payload)
            if slot != 0 or mode != 1:
                raise ValueError('unsupported background mode')
            background = identity
        elif op in (22,27,30):
            values = immediate(payload)
            slot,identity = values[:2]
            boards[slot] = identity
            if op == 30:
                visible.add(slot)
        elif op == 35:
            slot,mode = immediate(payload)
            if mode in (0,1):
                visible.add(slot)
            elif mode in (2,3):
                visible.discard(slot)
            else:
                raise ValueError('unknown character visibility')
        elif op == 32:
            visible.discard(immediate(payload)[0])
        elif op == 43:
            if lines:
                pages.append(page(offset))
                lines,indices,speaker = [],[],None
            active = immediate(payload)[0]
        elif op == 17:
            index = struct.unpack('<H',payload)[0]
            identity = boards.get(active)
            current = 101 if identity == 0xfffffff and active in (1,3) else identity
            if current not in (101,4,7,130) or index >= len(pool):
                raise ValueError('unknown text speaker or index')
            if lines and speaker != current:
                raise ValueError('mixed speakers in one key-wait page')
            speaker = current
            lines.append(pool[index]['text'])
            indices.append(index)
        elif op == 51 and lines:
            pages.append(page(offset))
            lines,indices,speaker = [],[],None
        elif op == 15:
            record = raw[struct.unpack_from('<I',raw,8)[0]:].split(b'\0')[0].decode('ascii')
            path = '/'.join(p for p in record.replace(chr(92),'/').split('/') if p)
            if chapter != 16 or path != 'data/adv/dat/Chapter017.ybc':
                raise ValueError('unsupported chapter replacement')
        elif op == 21:
            visible.clear()
    if lines or len([i for page in pages for i in page['text_indices']]) != len(pool):
        raise ValueError('text coverage differs')
    return {'chapter':chapter,'label':'月下的交谈' if chapter == 16 else '北方的誓愿',
        'source':'ADV/DAT/'+filename,'sha256':hashlib.sha256(raw).hexdigest(),
        'text_pool':pool,'normalized_fullwidth_space_indices':normalized,'pages':pages}


def export(out):
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError('source executable differs')
    out.mkdir(parents=True,exist_ok=True)
    scenes = [scene(c,image) for c in CHAPTERS]
    sources,actors,backgrounds = {},{},{}
    for identity in (4,7,130):
        filename = source_string(image,0x622250,identity,8).decode('ascii').upper()
        name = source_string(image,0x621F2C,identity).decode('big5',errors='strict')
        decoded = render(str(GAME/'BIN'/filename))
        # MC source dimensions differ from H-PART despite identical byte counts.
        atlas = Image.frombytes('RGBA',(512,1024),decoded.tobytes())
        x,y = struct.unpack_from('<hh',image,0x622250-0x400000+identity*8+4)
        body = atlas.crop((0,0,512,768))
        body.alpha_composite(atlas.crop((0,768,128,896)),(x,y))
        actorfile = f'actor_{identity}.png'
        body.save(out/actorfile)
        actors[str(identity)] = {'name':name,'image':actorfile,'source':'ADV/BIN/'+filename,
            'atlas_size':[512,1024],'body_crop':[0,0,512,768],
            'expression_crop':[0,768,128,896],'expression_destination':[x,y],
            'expression':'source default expression0; alternate expressions not requested by these scenes'}
        sources['ADV/BIN/'+filename] = hashlib.sha256((GAME/'BIN'/filename).read_bytes()).hexdigest()
    actors['101'] = {'name':'老师','image':'','source':'Chapter016 board3 narrator; player teacher101'}
    for identity in sorted({p['background'] for s in scenes for p in s['pages']}):
        filename = source_string(image,0x621BBC,identity).decode('ascii').upper()
        backgroundfile = f'background_{identity}.png'
        render(str(GAME/'BIN'/filename)).crop((0,0,1024,768)).save(out/backgroundfile)
        backgrounds[str(identity)] = {'image':backgroundfile,'source':'ADV/BIN/'+filename,'crop':[0,0,1024,768]}
        sources['ADV/BIN/'+filename] = hashlib.sha256((GAME/'BIN'/filename).read_bytes()).hexdigest()
    catalog = {'version':1,'source_image_sha256':SOURCE_SHA256,'scenes':scenes,
        'actors':actors,'backgrounds':backgrounds,'source_assets_sha256':sources,
        'outputs_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('*.png'))},
        'presentation_scope':'Original text order, board speakers, backgrounds, default character art and visibility; remake layout and click timing; audio/fades not reproduced.',
        'tables':{'names':'0x621f2c','backgrounds':'0x621bbc','characters':'0x622250',
            'body_draw':'0x4c9690','expression_draw':'0x4c97a0'}}
    (out/'catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    return deepcopy(catalog)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,default=ROOT/'prototype/assets/school_story')
    args = parser.parse_args()
    result = export(args.out)
    print('Exported pages:',[len(s['pages']) for s in result['scenes']])
