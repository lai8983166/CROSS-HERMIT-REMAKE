"""Export the November 3 battle return from the shipped ADV and student templates."""
import json
import struct
from tools.school_sortie_week_story_export import (
    GAME, ROOT, _date_card_metadata, catalog, date_route, join_data, july_date_card,
)


def build():
    data = catalog({72:147, 74:66, 307:116, 312:67})
    routes = [date_route('CH003',11,3), date_route('CH001',11,4), date_route('CH002',11,4)]
    assert [r['target'] for r in routes] == [f'data/adv/dat/Chapter{i:03}.ybc' for i in (72,307,312)]
    assert not any(r.get('effects') for r in routes)
    pre, linked, new, school = data['scenes']
    assert [(e['offset'], e['opcode'], e.get('operands')) for e in pre['effects']] == [
        (20,144,[2]), (0x9c2,153,[1,6,0]), (0xe16,15,None)]
    raw = (GAME/'DAT/CHAPTER072.YBC').read_bytes()
    _, _, end, pool, _ = struct.unpack_from('<5I',raw)
    index = pre['effects'][-1]['string_index']
    target = raw[end+48*index:end+48*(index+1)].split(bytes(1))[0]
    assert target.replace(bytes([92,92]),b'/') == b'data/adv/dat/Chapter074.ybc'
    pre['effects'][-1]['target'] = 'data/adv/dat/Chapter074.ybc'
    assert [s['effects'] for s in (linked,new,school)] == [
        [dict(offset=20,opcode=144,operands=[7])],
        [dict(offset=20,opcode=144,operands=[107]),dict(offset=28,opcode=144,operands=[28]),
         dict(offset=0x954,opcode=151,operands=[5,1]),dict(offset=0x960,opcode=91,operands=[122,2])],
        [dict(offset=0x4da,opcode=151,operands=[11,0])]]
    raw = (GAME/'DAT/CHAPTER307.YBC').read_bytes()
    _, _, end, pool, _ = struct.unpack_from('<5I',raw)
    assert raw[end:pool].split(bytes(1))[0].replace(bytes([92,92]),b'/') == b'data/adv/bin/tc1104.bin'
    pos = 36
    for opcode, args in [(56,[0]),(67,[0]),(69,[0,0,324,0,53,0,0,1024,128]),(56,[3]),(13,[600]),(56,[4]),(74,[]),(12,[30])]:
        op, size = struct.unpack_from('<HH',raw,pos)
        operands = list(struct.unpack_from('<'+'I'*((size-4)//4),raw,pos+4))
        assert op==opcode and operands==[n+(0 if op==67 else 0x20000000) for n in args], (op, operands)
        pos += size
    data['date_card'] = _date_card_metadata(4,'data/adv/bin/tc1104.bin',[0,0,324,0,53,0,0,1024,128],600,11)
    data['routes'] = routes
    members = [101,3,4,9,5,8,6,1,16,17,13,14,15,11,18,32,2,110,115,118,116]
    data['joins'] = [join_data({},7,None,members+[7]),join_data({},28,107,members+[7,107,28])]
    return data


if __name__ == '__main__':
    data = build()
    (ROOT/'prototype/data/school_november_four_story.json').write_text(
        json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    (ROOT/'prototype/assets/school_story/tc1104.png').write_bytes(july_date_card(4,11)[1])
