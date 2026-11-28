"""Export the winter ADV programs, dated sections and original visual calendar cards."""
import hashlib
import json
import struct

from tools.school_postbattle_story_export import ALLOWED
from tools.school_sortie_week_story_export import GAME, SOURCE, date_route, join_data, _date_card_metadata
from tools.school_story_export import source_string
from tools.tactics_exit_emulation import SOURCE_SHA256

from tools.school_year_story_export import ROOT, build, july_date_card


def december_three():
    return build({78: 113, 232: 40}, {(12, 3): (78, None, 232)})


def calendar_card(month, week, chapter, router):
    display_month = (month - 1) % 12 + 1
    resource = f'data/adv/bin/tc{display_month:02}{week:02}.bin'
    if chapter:
        raw = (GAME / f'DAT/CHAPTER{chapter}.YBC').read_bytes()
        _, at, end, pool, _ = struct.unpack_from('<5I', raw)
        commands = []
        while at < end:
            op, size = struct.unpack_from('<2H', raw, at)
            if op in (56, 67, 69, 13, 74, 12):
                fields = struct.unpack_from('<'+'I'*((size-4)//4), raw, at+4)
                if op == 67:
                    start = end + fields[0] * 48
                    assert start + 48 <= pool
                    name = raw[start:start+48].split(bytes(1))[0].decode('ascii')
                    commands.append({'opcode': op, 'resource': '/'.join(part for part in name.split(chr(92)) if part)})
                else:
                    assert all(value >> 28 == 2 for value in fields)
                    commands.append({'opcode': op, 'operands': [value & 0xfffffff for value in fields]})
            at += size
    else:
        commands = router['presentation']
    card_index, = [i for i, op in enumerate(commands) if op.get('resource') == resource]
    prefix = commands[card_index-1:card_index+7]
    assert [op['opcode'] for op in prefix] == [56, 67, 69, 56, 13, 56, 74, 12]
    assert [prefix[i]['operands'] for i in (0, 3, 4, 5, 7)] == [[0], [3], [600], [4], [30]]
    draw = prefix[2]['operands']
    assert draw == [0, 0, 324, 0, 53, 0, 0, 1024, 128]
    return _date_card_metadata(week, resource, draw, prefix[4]['operands'][0], display_month)


# The calendar globals continue past December (13 is January). TC assets use
# display months. The final state12 advances before CH003 and bypasses CH001/2.
def winter():
    image = SOURCE.read_bytes()
    assert hashlib.sha256(image).hexdigest() == SOURCE_SHA256
    scenes = {}
    def chapter(name):
        if name in scenes:
            return
        raw = (GAME / f'DAT/CHAPTER{name}.YBC').read_bytes()
        assert raw == (GAME / f'DAT/BIG5/CHAPTER{name}.YBC').read_bytes()
        _, start, end, pool, _ = struct.unpack_from('<5I', raw)
        def resource(i):
            assert end + (i + 1) * 48 <= pool
            return '/'.join(part for part in raw[end+i*48:end+(i+1)*48].split(bytes(1))[0].decode().split(chr(92)) if part)
        count, = struct.unpack_from('<I', raw, pool)
        texts = []
        for i in range(count):
            offset, = struct.unpack_from('<H', raw, pool+4+4*i)
            line = raw[pool+offset:raw.index(0,pool+offset)].replace(b'\x81\x40',b'\xa1\x40')
            texts.append(line.decode('cp950'))
        program = []
        at = start
        while at < end:
            op, size = struct.unpack_from('<HH', raw, at)
            assert op in ALLOWED | {8,11,61,64,169,171,172} and size >= 4 and at+size<=end,(name,at,op)
            values = list(struct.unpack_from('<'+'I'*((size-4)//4),raw,at+4))
            if op in (22,27,29,30,33,26):
                assert all(v>>28==2 for v in values)
                v=[v&0xfffffff for v in values]
                board, speaker=(v[1],v[2]) if op==26 else (v[0],v[1])
                speaker_name=('老师' if board in (3,4) else '旁白') if speaker==0xfffffff else source_string(image,0x621F2C,speaker).decode('cp950')
                program.append([at,'board',board,speaker,speaker_name])
            elif op==43:program.append([at,'active',values[0]&0xfffffff])
            elif op==17:
                i,=struct.unpack_from('<H',raw,at+4)
                program.append([at,'line',i,texts[i]])
            elif op==51:program.append([at,'page'])
            elif op in (144,145,151,91):program.append([at,'effect',op,*[v&0xfffffff for v in values]])
            elif op==61:
                var,n,*indices=values
                assert var==0 and n==len(indices)
                program.append([at,'choice',[texts[i] for i in indices]])
            elif op==8:
                comparison,var,val,dest=values
                assert [comparison,var,val>>28]==[1,0,2]
                program.append([at,'if',val&0xfffffff,start+dest])
            elif op==11:program.append([at,'jump',start+values[0]])
            elif op==169:
                assert values[0]==0
                program.append([at,'grade',values[1]&0xfffffff])
            elif op==171:program.append([at,'winner'])
            elif op in (15,172):
                link=resource(values[0]).split('/')[-1][7:-4]
                program.append([at,'chapter',link]);chapter(link)
            elif op==19:program.append([at,'end'])
            at+=size
        scenes[name]={'sha256':hashlib.sha256(raw).hexdigest(),'program':program}
    dates=[]
    for month in range(12,16):
        for week in range(1,6):
            if month==12 and week<4:continue
            previous=(month,week-1) if week>1 else (month-1,5)
            terminal=(month,week)==(15,5)
            routes=[date_route('CH003',*((month,week) if terminal else previous))]
            if not terminal:routes+=[date_route(f'CH00{i}',month,week) for i in (1,2)]
            sections=[]
            for route in routes:
                target=route['target']
                name=target.split('/')[-1][7:-4] if target else ''
                if name:chapter(name)
                sections.append({'chapter':name,'effects':route.get('effects',[])})
            entry={'arrival':[month,week],'departure':previous,'routes':routes,'sections':sections,'terminal':terminal}
            if not terminal:
                entry['date_card'] = calendar_card(month, week, sections[1]['chapter'], routes[1])
            dates.append(entry)
    members=list(range(1,34))+[101,107,110,112,113,115,116,118]
    joins={}
    for student in [3,4,10,12,22,23,24,25,26,27,29,30,31,33]:
        joins[str(student)]=join_data({},student,None,members)
    for teacher in (112,113):
        source=join_data({},10,teacher,members)
        joins[str(teacher)]={'profile':source['join_profiles'][1], 'join_relationships':[r for r in source['join_relationships'] if teacher in (r['from'],r['to'])]}
    return {'scenes':scenes,'arrivals':dates,'joins':joins}


if __name__ == '__main__':
    out = ROOT / 'prototype/data/school_year_december_three.json'
    out.write_text(json.dumps(december_three(), ensure_ascii=False, indent=2) + '\n',
                   encoding='utf8', newline='\n')
    (ROOT / 'prototype/assets/school_story/tc1203.png').write_bytes(july_date_card(3, 12)[1])

    data=winter()
    (ROOT/'prototype/data/school_year_winter.json').write_text(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf8',newline='\n')
    for row in data['arrivals']:
        if row['terminal']:continue
        month,week=row['arrival'];display=(month-1)%12+1
        (ROOT/f'prototype/assets/school_story/tc{display:02}{week:02}.png').write_bytes(july_date_card(week,display)[1])
