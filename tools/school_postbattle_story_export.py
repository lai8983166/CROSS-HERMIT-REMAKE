"""Export only source text/key-wait pages for the first post-battle return.

Uses existing ADV operand/name decoding; not a VM or observation backend.
Images, movie playback, audio and original presentation timing are not exported.
"""
import hashlib
import json
import struct
from pathlib import Path
from tools.school_story_export import GAME, immediate, source_string
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256

CHAPTERS = (20, 21, 22, 208)
ALLOWED = {12,13,15,17,19,20,21,22,24,26,27,28,30,31,32,33,35,36,40,43,44,50,51,56,59,63,65,67,69,74,91,144,151,153}


def catalog():
    image = SOURCE.read_bytes()
    assert hashlib.sha256(image).hexdigest() == SOURCE_SHA256
    scenes = []
    for chapter in CHAPTERS:
        raw = (GAME/f'DAT/CHAPTER{chapter:03}.YBC').read_bytes()
        assert raw == (GAME/f'DAT/BIG5/CHAPTER{chapter:03}.YBC').read_bytes()
        header, at, end, pool, _ = struct.unpack_from('<5I', raw)
        assert header == 4 and at == 20 and at < end <= pool < len(raw)
        count = struct.unpack_from('<I', raw, pool)[0]
        assert count == {20:378,21:91,22:90,208:22}[chapter]
        texts = []
        for i in range(count):
            offset, parameter = struct.unpack_from('<2H', raw, pool+4+4*i)
            assert offset >= 4+4*count and pool+offset<len(raw)
            data = raw[pool+offset:raw.index(0,pool+offset)]
            text = data.replace(b'\x81\x40',b'\xa1\x40').decode('cp950',errors='strict')
            texts.append(text)
        pages, effects, boards, lines, indices = [], [], {}, [], []
        active = None
        def flush(offset):
            if not lines: return
            identity = boards[active]
            name = ('老师' if active in (3,4) else '旁白') if identity==0xfffffff else source_string(image,0x621F2C,identity).decode('cp950')
            pages.append({'chapter':chapter,'source_offset':offset,'speaker_id':identity,
                          'speaker':name,'text_indices':indices[:],'text':'\n'.join(lines)})
            lines.clear(); indices.clear()
        while at < end:
            op, size = struct.unpack_from('<2H',raw,at)
            assert op in ALLOWED and size>=4 and at+size<=end, (chapter,at,op,size)
            payload = raw[at+4:at+size]
            if op in (22,27,30,33):
                flush(at); values = immediate(payload); boards[values[0]]=values[1]
            elif op == 26:
                flush(at); values=immediate(payload); assert values==[3,6,101,0];boards[3]=101
            elif op == 43:
                flush(at); active=immediate(payload)[0]
            elif op == 17:
                index = struct.unpack('<H',payload)[0]
                assert active in boards and index < count
                lines.append(texts[index]);indices.append(index)
            elif op == 51:
                flush(at)
            elif op in (144,151,153,91):
                effects.append({'offset':at,'opcode':op,'operands':immediate(payload)})
            elif op == 15:
                index = struct.unpack('<I',payload)[0]
                strings=raw[end:pool].split(b'\0')
                effects.append({'offset':at,'opcode':op,'string_index':index})
            at += size
        assert not lines and [i for p in pages for i in p['text_indices']]==list(range(count))
        scenes.append({'chapter':chapter,'source':f'ADV/DAT/CHAPTER{chapter:03}.YBC',
                       'sha256':hashlib.sha256(raw).hexdigest(),'text_count':count,'pages':pages,'effects':effects})
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'scenes':scenes,
            'scope':'All source text in original order and key-wait grouping; remake text presentation. No original movies/audio/fades or native execution.'}


if __name__ == '__main__':
    output = ROOT/'prototype/data/school_postbattle_story.json'
    data = catalog()
    output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    print([(s['chapter'],len(s['pages']),s['text_count']) for s in data['scenes']])
