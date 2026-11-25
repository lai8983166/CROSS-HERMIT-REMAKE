"""Replay original weekly unlock checks and personal-screen lookups on campaign students."""
import argparse
import json
from pathlib import Path

from tools.battle_preparation_emulation import CHAR_BASE, CHAR_STRIDE, PACKAGE_BASE, PACKAGE_STRIDE
from tools.school_job_menu_export import source_menu
from tools.school_year_loop_emulation import fingerprint
from tools.tactics_exit_emulation import SOURCE_SHA256
from tools.week_settlement_emulation import WeekSettlementEmulator


def compare(directory):
    dates = [(10, week) for week in range(1, 6)]+[(11, 1)]
    cpu = WeekSettlementEmulator()
    entries = []
    for prior, arrival in zip(dates, dates[1:]):
        def read(date):
            return json.loads((directory/('settlement-%02d-%d.json' % date)).read_bytes())
        before = read(prior)['after']
        after = read(arrival)['before']
        assert [after['school'][key] for key in ('month','week')] == list(arrival)
        cpu.write(0x7A528E, arrival[0], 'h')
        cpu.write(0x7A5290, arrival[1], 'h')
        probes = []
        new_unlocks = []
        for row, next_row in zip(before['participants'], after['participants'], strict=True):
            member = row['character_id']
            assert member == next_row['character_id']
            base = CHAR_BASE+member*CHAR_STRIDE
            package = PACKAGE_BASE+member*PACKAGE_STRIDE
            for i, value in enumerate(row['attributes']):
                cpu.write(base+0xc+8*i, value, 'B')
            cpu.uc.mem_write(package+0xd7, bytes(row['job_progress']))
            cpu.uc.mem_write(package+0xf9, bytes(row['unlock_flags']))
            cpu.call(0x4d3aa0, (member,))
            flags = list(cpu.uc.mem_read(package+0xf9, 30))
            if flags != next_row['unlock_flags']:
                raise ValueError(f'{arrival} student {member}: unlock flags differ')
            probes.append((member, [i+1 for i,x in enumerate(flags) if x]))
            new_unlocks.extend([member,i+1] for i,x in enumerate(flags) if x and not row['unlock_flags'][i])
        menus = source_menu(probes)['lookup_probes']
        entries.append({'date':arrival,'students':len(menus),'new_unlocks':new_unlocks,
                        'menus_sha256':fingerprint(menus)})
    return {'source_image_sha256':SOURCE_SHA256,'weeks':entries}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    result = compare(args.directory)
    with args.output.open('x', encoding='utf8', newline='\n') as file:
        json.dump(result, file, indent=2)
        file.write('\n')
