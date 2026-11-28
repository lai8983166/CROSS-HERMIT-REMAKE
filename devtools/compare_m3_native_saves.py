"""Compare externally pinned v7 school saves, without running the game or writing files."""
import argparse
import hashlib
import json
import struct
from pathlib import Path

from devtools.inspect_m3_adventure44_guest_saves import inspect_save

STATE = 0x7A50E8


def snapshot(raw, expected_sha256):
    identity = hashlib.sha256(raw).hexdigest()
    if identity != expected_sha256:
        raise ValueError('Native save SHA-256 mismatch')
    data = inspect_save(raw)

    def fields(address, fmt):
        return list(struct.unpack_from('<' + fmt, raw, address - STATE))

    def value(address, fmt):
        return fields(address, fmt)[0]

    build = value(STATE + 4, 'I')
    if build > 0x10002:
        raise ValueError('Unsupported native save build')
    roster = data['roster']
    if len(set(roster)) != len(roster) or any(not 0 <= member < 65 for member in roster):
        raise ValueError('Invalid serialized role index')
    groups = []
    for group in range(5):
        base = 0x7AAA12 + 28 * group
        groups.append({'teacher': value(base, 'h'), 'activity': value(base + 3, 'B'),
                       'student_count': value(base + 14, 'B'), 'student_slots': fields(base + 16, '4h')})
    roles = {}
    for member in roster:
        # 4D7720 copies 65 live records into this section of the serialized state.
        base = 0x7BC6AC + member * 0x4A0
        package = 0x7CF34C + member * 0x124
        roles[str(member)] = {
            'job': value(base + 6, 'h'), 'level': value(base + 0x50, 'B'),
            'attributes': [value(base + 0xC + 8*i, 'B') for i in range(7)],
            'growth_pools': [value(base + 0x10 + 8*i, 'I') for i in range(7)],
            'skill_statuses': [value(base + 0xB8 + 12*i, 'B') for i in range(84)],
            'week_records': fields(package + 0x24, '177B'),
            'job_progress': fields(package + 0xD7, '33B'),
            'unlock_flags': fields(package + 0xF9, '30B'),
            'mvp_count': value(package + 0x120, 'h'),
            'relationships': fields(0x7D3D71 + 68*member, '68B'),
            'equipped_skills': fields(base + 0x52, '8h'), 'equipped_items': fields(base + 0x62, '8h'),
            'staged_package': fields(package, '8i'), 'staged_total': value(package + 0x20, 'i')}
    teacher_count = value(0x7A528A, 'h')
    if not 0 <= teacher_count <= 20:
        raise ValueError('Invalid teacher count')
    teachers = fields(0x7A5262, f'{teacher_count}h')
    if any(not 101 <= teacher <= 120 for teacher in teachers):
        raise ValueError('Invalid serialized teacher index')
    return data | {'sha256': identity, 'build': build, 'teachers': teachers,
                   'teacher_relationships': {str(t): fields(0x7D3D71 + 68*(t-55), '68B') for t in teachers},
                   'item_flags': fields(0x7AACAC, '360H'),
                   'groups': groups, 'selected_mission': value(0x7AAB16, 'h'),
                   'departure_mission': value(0x7A5294, 'h'), 'global_score': value(0x7A511C, 'i'),
                   'mission44_grade': value(0x7A54CA + 44, 'B'), 'roles': roles}


def compare(before, after, require_44=False):
    if require_44:
        if before['date'] != [13, 2] or before['selected_mission'] != 44:
            raise ValueError('Pre-save must show January week 2 with mission 44 selected')
        if after['date'] != [13, 3] or after['departure_mission'] != 44:
            raise ValueError('Post-save must show January week 3 after departure mission 44')
        if before['sha256'] == after['sha256']:
            raise ValueError('Pre-save and post-save are identical')
    deltas = {}
    for member in before['roles'].keys() & after['roles'].keys():
        first, last = before['roles'][member], after['roles'][member]
        changed = {}
        for key in ('attributes', 'growth_pools', 'staged_package'):
            if first[key] != last[key]:
                changed[key] = [b-a for a,b in zip(first[key], last[key], strict=True)]
        for key in ('level', 'staged_total'):
            if first[key] != last[key]:
                changed[key] = last[key] - first[key]
        if first['job'] != last['job']:
            changed['job'] = [first['job'], last['job']]
        for key in ('skill_statuses', 'week_records', 'job_progress', 'relationships',
                    'equipped_skills', 'equipped_items'):
            entries = {i: [a, b] for i, (a, b) in enumerate(zip(first[key], last[key], strict=True))
                       if a != b}
            if entries:
                changed[key] = entries
        if changed:
            deltas[member] = changed
    return {'before': before, 'after': after, 'growth_differences': deltas,
            'global_score_delta': after['global_score'] - before['global_score'],
            'grade44_before_after': [before['mission44_grade'], after['mission44_grade']]}


def adventure44_party(raw, before):
    from devtools.verify_native_april_return import prepare_native_school
    if before['date'] != [13, 2] or before['selected_mission'] != 44:
        raise ValueError('Pre-save must show January week 2 with mission 44 selected')
    _, prepared = prepare_native_school(raw)
    rounds = prepared['rounds']
    if len(rounds) != 1 or rounds[0]['scene_id'] != 44:
        raise ValueError('Original departure did not select one round of adventure 44')
    ids = rounds[0]['student_ids']
    if len(ids) != 19 or len(set(ids)) != 19 or not set(ids).issubset(before['roster']):
        raise ValueError(f'Adventure 44 requires 19 distinct enrolled students, original prepared {len(ids)}')
    return {'original_prepared': prepared, 'original_party_size': len(ids)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before', type=Path)
    parser.add_argument('--before-sha256', required=True)
    parser.add_argument('after', type=Path, nargs='?')
    parser.add_argument('--after-sha256')
    parser.add_argument('--departure-only', action='store_true', help='verify the January week 2 squad before playing the original battle')
    parser.add_argument('--require-44', action='store_true', help='validate mission/date fields of the pair')
    args = parser.parse_args()
    if args.departure_only:
        if args.after or args.after_sha256:
            parser.error('--departure-only accepts only the pre-save')
    elif not args.after or not args.after_sha256:
        parser.error('a comparison requires the post-save and --after-sha256')
    try:
        raw = args.before.read_bytes()
        before = snapshot(raw, args.before_sha256)
        if args.departure_only:
            report = {'before': before, **adventure44_party(raw, before)}
        else:
            after = snapshot(args.after.read_bytes(), args.after_sha256)
            report = compare(before, after, args.require_44)
            if args.require_44:
                report.update(adventure44_party(raw, before))
    except (OSError, ValueError) as exc:
        parser.exit(1, f'{exc}\n')
    print(json.dumps(report, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
