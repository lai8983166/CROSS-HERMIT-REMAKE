"""Export the May school date routes through August week 1 and source dialogue from the shipped ADV."""
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
    presentation = []
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
        elif opcode in (12, 13, 56, 67, 69, 74):
            item = {'offset': at, 'opcode': opcode}
            if opcode == 67:
                offset = end + values[0]*48
                assert end <= offset <= pool-48
                item['resource'] = '/'.join(part for part in raw[offset:offset+48].split(bytes(1))[0].decode('ascii').split(chr(92)) if part)
            else:
                assert all(v >> 28 == 2 for v in values)
                item['operands'] = [v & 0xfffffff for v in values]
            presentation.append(item)
        elif opcode in (91, 144, 145, 151):
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
                    'date': [month, week], 'offsets': visited, 'target': target, **({'effects': effects} if effects else {}),
                    **({'presentation': presentation} if presentation else {})}
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
    return join_data(data, 8, 110, [101,3,4,9,5,8,110])


def build_week5():
    data = catalog({'030B': 99, 31: 110})
    routes = [date_route('CH003', 5, 4), date_route('CH001', 5, 5), date_route('CH002', 5, 5)]
    assert [route['target'] for route in routes] == [
        'data/adv/dat/Chapter030B.ybc', 'data/adv/dat/Chapter031.ybc', None]
    assert routes[2]['effects'] == [{'offset': 0x540, 'opcode': 151, 'operands': [11, 1]}]
    assert [scene['effects'] for scene in data['scenes']] == [[
        {'offset': 0x14, 'opcode': 144, 'operands': [6]},
        {'offset': 0x1c, 'opcode': 144, 'operands': [115]}], [
        {'offset': 0x7fc, 'opcode': 151, 'operands': [11, 0]},
        {'offset': 0x808, 'opcode': 91, 'operands': [6, 2]}]]
    data['routes'] = routes
    return join_data(data, 6, 115, [101,3,4,9,5,8,110,6,115])


def build_june_week1():
    data = catalog({32: 85, 33: 83})
    routes = [date_route('CH003', 5, 5), date_route('CH001', 6, 1), date_route('CH002', 6, 1)]
    assert [r['target'] for r in routes] == ['data/adv/dat/Chapter032.ybc', 'data/adv/dat/Chapter033.ybc', None]
    assert [s['effects'] for s in data['scenes']] == [[], [
        {'offset': 0x14, 'opcode': 144, 'operands': [1]},
        {'offset': 0x75e, 'opcode': 151, 'operands': [8, 1]},
        {'offset': 0x76a, 'opcode': 91, 'operands': [6, 2]}]]
    assert routes[2]['effects'] == [{'offset': 0x554, 'opcode': 151, 'operands': [11, 0]}]
    data['routes'] = routes
    return join_data(data, 1, None, [101,3,4,9,5,8,110,6,115,1])


def build_june_week2():
    data = catalog({35: 108, 36: 47, 37: 119, 38: 96, 39: 163})
    routes = [date_route('CH003', 6, 1), date_route('CH001', 6, 2), date_route('CH002', 6, 2)]
    assert [r['target'] for r in routes] == [f'data/adv/dat/Chapter{c:03}.ybc' for c in (35, 37, 39)]
    assert [s['effects'] for s in data['scenes']] == [
        [{'offset': 0xaf8, 'opcode': 15, 'string_index': 0}],
        [{'offset': 0x14, 'opcode': 144, 'operands': [2]}],
        [{'offset': 0xaba, 'opcode': 15, 'string_index': 1}],
        [{'offset': 0x928, 'opcode': 151, 'operands': [6, 1]},
         {'offset': 0x934, 'opcode': 91, 'operands': [7, 2]}],
        [{'offset': 0xfe2, 'opcode': 151, 'operands': [11, 0]}]]
    _link_chapters(data['scenes'][0], '035', 36)
    _link_chapters(data['scenes'][2], '037', 38)
    data['routes'] = routes
    return join_data(data, 2, None, [101,3,4,9,5,8,110,6,115,1,2])


def build_june_week3():
    data = catalog({'039A': 87, 40: 103, 41: 11, 210: 60})
    routes = [date_route('CH003', 6, 2), date_route('CH001', 6, 3), date_route('CH002', 6, 3)]
    assert [r['target'] for r in routes] == ['data/adv/dat/Chapter039A.ybc', 'data/adv/dat/Chapter041.ybc', None]
    assert 'effects' not in routes[2]
    assert [s['effects'] for s in data['scenes']] == [
        [{'offset': 0xa3e, 'opcode': 15, 'string_index': 0}], [],
        [{'offset': 0x19e, 'opcode': 15, 'string_index': 1}],
        [{'offset': 0x408, 'opcode': 151, 'operands': [16, 1]},
         {'offset': 0x414, 'opcode': 91, 'operands': [6, 2]}]]
    _link_chapters(data['scenes'][0], '039A', 40)
    _link_chapters(data['scenes'][2], '041', 210)
    data['routes'] = routes
    return data


def build_june_week4():
    data = catalog({213: 25})
    routes = [date_route('CH003', 6, 3), date_route('CH001', 6, 4), date_route('CH002', 6, 4)]
    assert [r['target'] for r in routes] == [None, 'data/adv/dat/Chapter213.ybc', None]
    assert routes[0]['offsets'][-3:] == [0x5b8, 0x5c0, 0x5d0]
    assert routes[0]['effects'] == [{'offset': 0x5b8, 'opcode': 145, 'operands': [117]}]
    assert 'effects' not in routes[2]
    assert data['scenes'][0]['effects'] == [
        {'offset': 0x25a, 'opcode': 151, 'operands': [9, 1]},
        {'offset': 0x266, 'opcode': 91, 'operands': [8, 2]}]
    data['routes'] = routes
    return data


def build_june_week5():
    data = catalog({42: 118, 302: 118})
    routes = [date_route('CH003', 6, 4), date_route('CH001', 6, 5), date_route('CH002', 6, 5)]
    assert [r['target'] for r in routes] == [None, 'data/adv/dat/Chapter042.ybc', None]
    assert routes[0]['effects'] == [{'offset': 0x5c8, 'opcode': 144, 'operands': [118]}]
    assert 'effects' not in routes[2]
    _link_chapters(data['scenes'][0], '042', 302)
    assert data['scenes'][1]['effects'] == [
        {'offset': 0x8a4, 'opcode': 151, 'operands': [2, 1]},
        {'offset': 0x8b0, 'opcode': 91, 'operands': [8, 2]}]
    data['routes'] = routes
    return join_data(data, None, 118, [101, 3, 4, 9, 5, 8, 110, 6, 115, 1, 2, 118])


def build_july_week1():
    data = catalog({303: 60, 218: 25})
    routes = [date_route('CH003', 6, 5), date_route('CH001', 7, 1), date_route('CH002', 7, 1)]
    assert [r['target'] for r in routes] == [None, 'data/adv/dat/Chapter303.ybc', None]
    assert not any('effects' in route for route in routes)
    _link_chapters(data['scenes'][0], '303', 218)
    assert data['scenes'][1]['effects'] == [
        {'offset': 0x286, 'opcode': 151, 'operands': [12, 1]},
        {'offset': 0x292, 'opcode': 91, 'operands': [8, 2]}]
    data['routes'] = routes
    return data


def july_date_card(week=2, month=7):
    from io import BytesIO
    from tools.school_opening_presentation_export import dx_image

    raw = (GAME/f'BIN/TC{month:02}{week:02}.BIN').read_bytes()
    image = dx_image(raw)
    assert image.size == (1024, 128)
    stream = BytesIO()
    image.save(stream, format='PNG')
    return raw, stream.getvalue()


def build_july_week2():
    data = catalog({})
    routes = [date_route('CH003', 7, 1), date_route('CH001', 7, 2), date_route('CH002', 7, 2)]
    assert [r['target'] for r in routes] == [None, None, None]
    assert 'effects' not in routes[0]
    movie = routes[1]['presentation']
    assert [e['opcode'] for e in movie] == [56, 67, 69, 56, 13, 56, 74, 12]
    assert movie[1]['resource'] == 'data/adv/bin/tc0702.bin'
    draw = movie[2]['operands']
    assert draw == [0, 0, 324, 0, 53, 0, 0, 1024, 128]
    assert routes[1]['effects'] == [
        {'offset':0xc94, 'opcode':151, 'operands':[3,0]},
        {'offset':0xca0, 'opcode':91, 'operands':[2,2]}]
    assert routes[2]['effects'] == [{'offset':0x568, 'opcode':151, 'operands':[3,1]}]
    data['routes'] = routes
    data['date_card'] = _date_card_metadata(2, movie[1]['resource'], draw, movie[4]['operands'][0])
    return data


def _date_card_metadata(week, resource, draw, wait, month=7):
    raw, png = july_date_card(week, month)
    return {'image':f'res://assets/school_story/tc{month:02}{week:02}.png', 'source':resource,
            'size':draw[7:9], 'position':draw[1:3], 'source_rect':draw[5:9],
            'canvas_size':[1024,768], 'wait_ticks':wait,
            'source_sha256':hashlib.sha256(raw).hexdigest(), 'png_sha256':hashlib.sha256(png).hexdigest()}


def build_july_week3():
    data = catalog({209: 75})
    routes = [date_route('CH003', 7, 2), date_route('CH001', 7, 3), date_route('CH002', 7, 3)]
    assert [r['target'] for r in routes] == [None, 'data/adv/dat/Chapter209.ybc', None]
    assert not any('effects' in route for route in routes)
    assert data['scenes'][0]['effects'] == [
        {'offset':0x83e, 'opcode':151, 'operands':[17,1]},
        {'offset':0x84a, 'opcode':91, 'operands':[8,2]}]
    data['routes'] = routes
    return data


def build_july_week4():
    data = catalog({214: 49})
    routes = [date_route('CH003', 7, 3), date_route('CH001', 7, 4), date_route('CH002', 7, 4)]
    assert [r['target'] for r in routes] == [None, 'data/adv/dat/Chapter214.ybc', None]
    assert not any('effects' in route for route in routes)
    assert data['scenes'][0]['effects'] == [
        {'offset':0x522, 'opcode':151, 'operands':[10,1]},
        {'offset':0x52e, 'opcode':91, 'operands':[8,2]}]
    data['routes'] = routes
    add_july_chapter_card(data,0,214,4)
    return data


def build_july_week5():
    data = catalog({304:100,305:40})
    routes = [date_route('CH003',7,4),date_route('CH001',7,5),date_route('CH002',7,5)]
    assert [r['target'] for r in routes] == ['data/adv/dat/Chapter304.ybc','data/adv/dat/Chapter305.ybc',None]
    assert not any('effects' in r for r in routes)
    assert [s['effects'] for s in data['scenes']] == [
        [{'offset':0x14,'opcode':144,'operands':[16]}, {'offset':0x1c,'opcode':144,'operands':[17]}],
        [{'offset':0x3bc,'opcode':151,'operands':[9,1]}, {'offset':0x3c8,'opcode':91,'operands':[122,2]}]]
    data['routes'] = routes
    add_july_chapter_card(data,1,305,5)
    members = [101,3,4,9,5,8,110,6,115,1,2,118]
    data['joins'] = []
    for identity in (16,17):
        members.append(identity)
        data['joins'].append(join_data({},identity,None,members))
    return data


def add_july_chapter_card(data,index,chapter,week):
    raw = (GAME/f'DAT/CHAPTER{chapter}.YBC').read_bytes()
    _, start, end, pool, _ = struct.unpack_from('<5I',raw)
    assert raw[end:pool].split(bytes(1))[0].replace(bytes([92,92]),b'/') == f'data/adv/bin/tc07{week:02}.bin'.encode()
    ops = []
    at = start
    while at < 0x70:
        op, size = struct.unpack_from('<HH',raw,at)
        cells = struct.unpack_from('<'+'I'*((size-4)//4),raw,at+4)
        assert all(v >> 28 == 2 for v in cells) if op!=67 else cells==(0,)
        ops.append({'offset':at,'opcode':op,'operands':[v & 0xfffffff for v in cells]})
        at += size
    assert [e['opcode'] for e in ops] == [56,67,69,56,13,56,74,12]
    assert ops[2]['operands'] == [0,0,324,0,53,0,0,1024,128]
    assert ops[4]['operands'] == [600] and ops[7]['operands'] == [30]
    data['scenes'][index]['presentation_prefix'] = ops
    data['date_card'] = _date_card_metadata(week,f'data/adv/bin/tc07{week:02}.bin',ops[2]['operands'],ops[4]['operands'][0])


def build_august_week1():
    data = catalog({})
    routes = [date_route('CH003',7,5), date_route('CH001',8,1), date_route('CH002',8,1)]
    assert all(route['target'] is None for route in routes) and 'effects' not in routes[0]
    assert routes[1]['effects'] == [
        {'offset':0xcd0,'opcode':151,'operands':[9,0]}, {'offset':0xcdc,'opcode':91,'operands':[122,2]}]
    assert routes[2]['effects'] == [{'offset':0x57c,'opcode':151,'operands':[9,1]}]
    movie = routes[1]['presentation']
    assert [e['opcode'] for e in movie] == [56,67,69,56,13,56,74,12]
    assert movie[1]['resource'] == 'data/adv/bin/tc0801.bin'
    assert movie[2]['operands'] == [0,0,324,0,53,0,0,1024,128]
    assert [movie[i]['operands'] for i in (0,3,4,5,7)] == [[0],[3],[600],[4],[30]]
    data['routes'] = routes
    data['date_card'] = _date_card_metadata(1,movie[1]['resource'],movie[2]['operands'],movie[4]['operands'][0],8)
    return data


def _link_chapters(scene, label, next_chapter):
    raw = (GAME/f'DAT/CHAPTER{label}.YBC').read_bytes()
    _, _, end, pool, _ = struct.unpack_from('<5I', raw)
    effect = scene['effects'][0]
    pos = end + 48 * effect['string_index']
    assert end <= pos <= pool-48
    target = raw[pos:pos+48].split(bytes(1))[0].decode('ascii')
    target = '/'.join(part for part in target.split(chr(92)) if part)
    assert target == f'data/adv/dat/Chapter{next_chapter:03}.ybc'
    effect['target'] = target


def join_data(data, student, teacher, members):
    image = SOURCE.read_bytes()
    profiles = []
    for identity in (n for n in (student, teacher) if n is not None):
        start = 0x6f5088 - 0x400000 + identity * 0x4a0
        raw = image[start:start + 0x4a0]
        profile = {'member_id': identity, 'job': struct.unpack_from('<h', raw, 6)[0],
                   'level_50': raw[0x50], 'attributes': list(raw[0xc:0x44:8]),
                   'storage_kind': 'student_record' if identity == student else 'static_teacher_template',
                   'template_sha256': hashlib.sha256(raw).hexdigest()}
        profiles.append(profile)
        if identity == student:
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
    def row(identity):
        return identity - 55 if identity > 100 else identity
    data['join_relationships'] = [{'from': a, 'to': b, 'value': image[0x34e4b0 + row(a)*68 + 1 + row(b)]}
                                  for a in members for b in members if a != b and (a in (student,teacher) or b in (student,teacher))]
    return data


if __name__ == '__main__':
    for name, make in [('school_sortie_week_story', build), ('school_may_week3_story', build_week3),
                       ('school_may_week4_story', build_week4), ('school_may_week5_story', build_week5),
                       ('school_june_week1_story', build_june_week1), ('school_june_week2_story', build_june_week2),
                       ('school_june_week3_story', build_june_week3), ('school_june_week4_story', build_june_week4), ('school_june_week5_story', build_june_week5), ('school_july_week1_story', build_july_week1),
                       ('school_july_week2_story', build_july_week2), ('school_july_week3_story', build_july_week3), ('school_july_week4_story', build_july_week4), ('school_july_week5_story', build_july_week5),
                       ('school_august_week1_story', build_august_week1)]:
        target = ROOT / f'prototype/data/{name}.json'
        target.write_text(json.dumps(make(), ensure_ascii=False, indent=2)+'\n', encoding='utf8', newline='\n')
    for month,week in ((7,2),(7,4),(7,5),(8,1)):
        (ROOT/f'prototype/assets/school_story/tc{month:02}{week:02}.png').write_bytes(july_date_card(week,month)[1])
