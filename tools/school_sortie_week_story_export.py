"""Export the May 1/May 2 date routes and source dialogue from the shipped ADV."""
import hashlib
import json
import struct
from tools.school_postbattle_story_export import GAME, ROOT, catalog


def date_route(router, month, week):
    filename = router + '.YBC'
    raw = (GAME / 'DAT' / filename).read_bytes()
    _, start, end, pool, _ = struct.unpack_from('<5I', raw)
    variables = {}
    at = start
    visited = []
    while start <= at < end and at not in visited:
        visited.append(at)
        opcode, size = struct.unpack_from('<HH', raw, at)
        values = struct.unpack_from('<' + 'I' * ((size-4)//4), raw, at+4)
        if opcode == 90:  # Read the calendar globals into the two script variables.
            target, selector = values
            variables[target] = {0x20000000: month, 0x20000001: week}[selector]
        elif opcode == 8:
            comparison, target, immediate, jump = values
            assert comparison == 1 and immediate >> 28 == 2
            if variables[target] == immediate & 0xfffffff:
                at = start + jump
                continue
        elif opcode == 11:
            at = start + values[0]
            continue
        elif opcode in (15, 19):
            target = None
            if opcode == 15:
                offset = end + values[0]*48
                assert end <= offset <= pool-48
                target = raw[offset:offset+48].split(b'\0')[0].decode('ascii')
                target = '/'.join(part for part in target.split(chr(92)) if part)
            return {'router': filename, 'sha256': hashlib.sha256(raw).hexdigest(),
                    'date': [month, week], 'offsets': visited, 'target': target}
        else:
            raise ValueError((filename, at, opcode))
        at += size
    raise ValueError('unresolved calendar route')


def build():
    data = catalog({23: 236, 24: 243})
    routes = [date_route('CH003',5,1), date_route('CH001',5,2), date_route('CH002',5,2)]
    assert [r['target'] for r in routes] == [
        'data/adv/dat/Chapter023.ybc', 'data/adv/dat/Chapter024.ybc', None]
    assert data['scenes'][0]['effects'] == []
    assert data['scenes'][1]['effects'] == [
        {'offset': 0x133e, 'opcode': 151, 'operands': [16,1]},
        {'offset': 0x134a, 'opcode': 91, 'operands': [8,2]}]
    data['routes'] = routes
    return data


if __name__ == '__main__':
    target = ROOT/'prototype/data/school_sortie_week_story.json'
    target.write_text(json.dumps(build(),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
