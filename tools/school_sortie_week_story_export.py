"""Export the May week 1 through week 4 date routes and source dialogue from the shipped ADV."""
import hashlib
import json
import struct
from tools.school_postbattle_story_export import GAME, ROOT, SOURCE, catalog


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


def build_week4():
    data = catalog({28: 93, 29: 202, 207: 33})
    routes = [date_route('CH003', 5, 3), date_route('CH001', 5, 4), date_route('CH002', 5, 4)]
    assert [r['target'] for r in routes] == [f'data/adv/dat/Chapter{i:03}.ybc' for i in (28, 29, 207)]
    assert [s['effects'] for s in data['scenes']] == [[], [
        {'offset': 0x14, 'opcode': 144, 'operands': [8]},
        {'offset': 0x1c, 'opcode': 144, 'operands': [110]},
        {'offset': 0x120c, 'opcode': 151, 'operands': [11, 0]},
        {'offset': 0x1218, 'opcode': 91, 'operands': [6, 2]}],
        [{'offset': 0x276, 'opcode': 151, 'operands': [11, 1]}]]
    data['routes'] = routes
    image = SOURCE.read_bytes()
    profiles = []
    for identity in (8, 110):
        start = 0x6f5088 - 0x400000 + identity * 0x4a0
        raw = image[start:start + 0x4a0]
        profile = {'member_id': identity, 'job': struct.unpack_from('<h', raw, 6)[0],
                   'level_50': raw[0x50], 'attributes': list(raw[0xc:0x44:8]),
                   'storage_kind': 'student_record' if identity == 8 else 'static_teacher_template',
                   'template_sha256': hashlib.sha256(raw).hexdigest()}
        profiles.append(profile)
        if identity == 8:
            progress = [0] + [max(0, min(100, x)) for x in struct.unpack_from('<32h', image, 0x351242 + identity * 0x42)]
            data['history'] = {'character_id': identity, 'job_progress': progress, 'week_records': [0] * 177}
            data['candidate'] = {'character_id': identity, **{k: profile[k] for k in ('job', 'level_50', 'attributes')},
                                 'growth_pools': [struct.unpack_from('<I', raw, 0x10 + k*8)[0] for k in range(7)],
                                 'skill_statuses': list(raw[0xb8:0xb8 + 84*12:12]),
                                 'equipped_skills': list(struct.unpack_from('<8h', raw, 0x52)),
                                 'equipped_items': list(struct.unpack_from('<8h', raw, 0x62)),
                                 'job_progress': progress[:31], 'unlock_flags': [0]*30, 'unlock_reserved_bytes': [0, 0],
                                 'job_sums': [sum(progress[1 + 2*k + n] for n in (0,1,10,11,20,21)) for k in range(5)],
                                 'staged_total': 0}
    data['join_profiles'] = profiles
    members = [101,3,4,9,5,8,110]
    def row(identity):
        return identity - 55 if identity > 100 else identity
    data['join_relationships'] = [{'from': a, 'to': b, 'value': image[0x34e4b0 + row(a)*68 + 1 + row(b)]}
                                  for a in members for b in members if a != b and (a in (8,110) or b in (8,110))]
    return data


if __name__ == '__main__':
    for name, make in [('school_sortie_week_story', build), ('school_may_week3_story', build_week3),
                       ('school_may_week4_story', build_week4)]:
        target = ROOT / f'prototype/data/{name}.json'
        target.write_text(json.dumps(make(), ensure_ascii=False, indent=2)+'\n', encoding='utf8', newline='\n')
