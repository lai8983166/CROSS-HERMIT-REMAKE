"""Export the May week 1 through week 3 date routes and source dialogue from the shipped ADV."""
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
    effects = []
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
        elif opcode == 151:
            assert all(v >> 28 == 2 for v in values)
            effects.append(dict(offset=at, opcode=opcode, operands=[v & 0xfffffff for v in values]))
        elif opcode in (15, 19):
            target = None
            if opcode == 15:
                offset = end + values[0]*48
                assert end <= offset <= pool-48
                target = raw[offset:offset+48].split(b'\0')[0].decode('ascii')
                target = '/'.join(part for part in target.split(chr(92)) if part)
            return {'router': filename, 'sha256': hashlib.sha256(raw).hexdigest(),
                    'date': [month, week], 'offsets': visited, 'target': target, **({'effects': effects} if effects else {})}
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


def build_week3():
    data = catalog({25: 55, 26: 132, 27: 316})
    routes = [date_route('CH003', 5, 2), date_route('CH001', 5, 3), date_route('CH002', 5, 3)]
    assert [r['target'] for r in routes] == [
        'data/adv/dat/Chapter025.ybc', 'data/adv/dat/Chapter026.ybc', None]
    assert routes[2]['effects'] == [{'offset': 0x52c, 'opcode': 151, 'operands': [11, 1]}]
    pre_week, beginning, continuation = data['scenes']
    assert pre_week['effects'] == []
    assert beginning['effects'] == [{'offset': 0xd2c, 'opcode': 15, 'string_index': 1}]
    raw = (GAME / 'DAT/CHAPTER026.YBC').read_bytes()
    _, _, end, pool, _ = struct.unpack_from('<5I', raw)
    assert pool == end + 96
    target = raw[end+48:pool].split(b'\0')[0].decode('ascii')
    target = '/'.join(part for part in target.split(chr(92)) if part)
    assert target == 'data/adv/dat/Chapter027.ybc'
    beginning['effects'][0]['target'] = target
    assert continuation['effects'] == [
        {'offset': 0x1d40, 'opcode': 151, 'operands': [11, 0]},
        {'offset': 0x1d4c, 'opcode': 91, 'operands': [8, 2]}]
    data['routes'] = routes
    return data


if __name__ == '__main__':
    for name, make in [('school_sortie_week_story', build), ('school_may_week3_story', build_week3)]:
        target = ROOT / f'prototype/data/{name}.json'
        target.write_text(json.dumps(make(), ensure_ascii=False, indent=2)+'\n', encoding='utf8', newline='\n')
