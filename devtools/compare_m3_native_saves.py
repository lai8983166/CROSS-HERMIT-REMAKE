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
            'equipped_skills': fields(base + 0x52, '8h'), 'equipped_items': fields(base + 0x62, '8h'),
            'staged_package': fields(package, '8i'), 'staged_total': value(package + 0x20, 'i')}
    teacher_count = value(0x7A528A, 'h')
    if not 0 <= teacher_count <= 20:
        raise ValueError('Invalid teacher count')
    return data | {'sha256': identity, 'build': build, 'teachers': fields(0x7A5262, f'{teacher_count}h'),
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
        if changed:
            deltas[member] = changed
    return {'before': before, 'after': after, 'growth_differences': deltas,
            'global_score_delta': after['global_score'] - before['global_score'],
            'grade44_before_after': [before['mission44_grade'], after['mission44_grade']]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for endpoint in ('before', 'after'):
        parser.add_argument(endpoint, type=Path)
        parser.add_argument(f'--{endpoint}-sha256', required=True)
    parser.add_argument('--require-44', action='store_true', help='validate mission/date fields of the pair')
    args = parser.parse_args()
    try:
        before = snapshot(args.before.read_bytes(), args.before_sha256)
        after = snapshot(args.after.read_bytes(), args.after_sha256)
        report = compare(before, after, args.require_44)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'{exc}\n')
    print(json.dumps(report, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
