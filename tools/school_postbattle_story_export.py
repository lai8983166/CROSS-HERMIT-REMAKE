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

CHAPTER_COUNTS = {20:378,21:91,22:90,208:22}
CHAPTERS = tuple(CHAPTER_COUNTS)
ALLOWED = {12,13,15,17,19,20,21,22,24,26,27,28,29,30,31,32,33,35,36,40,43,44,50,51,56,59,63,65,67,69,74,91,144,145,151,153}


def catalog(chapter_counts=None):
    if chapter_counts is None:
        chapter_counts = CHAPTER_COUNTS
    image = SOURCE.read_bytes()
    assert hashlib.sha256(image).hexdigest() == SOURCE_SHA256
    scenes = []
    for chapter in chapter_counts:
        label = f'{chapter:03}' if isinstance(chapter, int) else chapter
        raw = (GAME/f'DAT/CHAPTER{label}.YBC').read_bytes()
        assert raw == (GAME/f'DAT/BIG5/CHAPTER{label}.YBC').read_bytes()
        header, at, end, pool, _ = struct.unpack_from('<5I', raw)
        assert header == 4 and at == 20 and at < end <= pool < len(raw)
        count = struct.unpack_from('<I', raw, pool)[0]
        assert count == chapter_counts[chapter]
        texts = []
        for i in range(count):
            offset, parameter = struct.unpack_from('<2H', raw, pool+4+4*i)
            assert offset >= 4+4*count and pool+offset<len(raw)
            data = raw[pool+offset:raw.index(0,pool+offset)]
            if chapter == 23 and i == 157:
                # Big5 period followed by its Shift-JIS twin in this one source line.
                assert data.endswith(bytes.fromhex("a1438142"))
                data = data[:-2] + bytes.fromhex("a143")
            if chapter == 42 and i == 12:
                # The shipped title includes a Shift-JIS 代 immediately after its Big5 代理.
                assert data.count(bytes.fromhex("91e3")) == 1
                data = data.replace(bytes.fromhex("91e3"), "代".encode("cp950"))
            text = data.replace(b'\x81\x40',b'\xa1\x40').decode('cp950',errors='strict')
            texts.append(text)
        pages, effects, boards, lines, indices = [], [], {}, [], []
        choice_labels = []
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
            assert (op in ALLOWED or (chapter == 309 and op in (8, 11, 61))) and size>=4 and at+size<=end, (chapter,at,op,size)
            payload = raw[at+4:at+size]
            if chapter == 309 and op == 61:
                flush(at)
                assert at == 0x39e and struct.unpack('<4I',payload) == (0,2,47,48)
                choice_labels = texts[47:49]
            elif chapter == 309 and op in (8,11):
                jumps = {0x3b2:(1,0,0x20000000,0x3da-20),
                         0x3c6:(1,0,0x20000001,0x756-20),0x74e:(0xc5c-20,)}
                assert struct.unpack('<'+'I'*(len(payload)//4),payload) == jumps[at]
            elif op in (22,27,29,30,33):
                flush(at); values = immediate(payload); boards[values[0]]=values[1]
            elif op == 26:
                flush(at); values=immediate(payload)
                if chapter in (304,305,309):
                    old, new, speaker, _ = values
                    assert old in boards and [old,new] in ([4,9],[9,4])
                    boards[new] = speaker
                else:
                    assert values==[3,6,101,0];boards[3]=101
            elif op == 43:
                flush(at); active=immediate(payload)[0]
            elif op == 17:
                index = struct.unpack('<H',payload)[0]
                assert active in boards and index < count
                lines.append(texts[index]);indices.append(index)
            elif op == 51:
                flush(at)
            elif op in (144,145,151,153,91):
                effects.append({'offset':at,'opcode':op,'operands':immediate(payload)})
            elif op == 15:
                index = struct.unpack('<I',payload)[0]
                strings=raw[end:pool].split(b'\0')
                effects.append({'offset':at,'opcode':op,'string_index':index})
            at += size
        assert not lines and [i for p in pages for i in p['text_indices']]==[i for i in range(count) if not (choice_labels and i in (47,48))]
        scenes.append({'chapter':chapter,'source':f'ADV/DAT/CHAPTER{label}.YBC',
                       'sha256':hashlib.sha256(raw).hexdigest(),'text_count':count,'pages':pages,'effects':effects})
        if choice_labels:
            scenes[-1]['choice_labels'] = choice_labels
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'scenes':scenes,
            'scope':'All source text in original order and key-wait grouping; remake text presentation. No original movies/audio/fades or native execution.'}


if __name__ == '__main__':
    output = ROOT/'prototype/data/school_postbattle_story.json'
    data = catalog()
    output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    print([(s['chapter'],len(s['pages']),s['text_count']) for s in data['scenes']])
