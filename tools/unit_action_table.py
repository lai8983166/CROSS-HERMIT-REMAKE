# -*- coding: utf-8 -*-
"""Decode the executable's unit archive and two-stage action lookup."""
import argparse
import json
import struct
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import dxanim_lib as dx

EXE = ROOT / 'analysis/hermit_game.exe'
DX_DIR = ROOT / 'CROSS HERMIT/CROSS HERMIT/DATA/DXANIM'
IMAGE_BASE = 0x400000
ACTION_POINTERS_VA = 0x60E850
PROGRAM_POINTERS_VA = 0x60F070
DIRECTION_OFFSETS_VA = 0x610510
ARCHIVE_POINTERS_VA = 0x610538
TYPE_COUNT = (PROGRAM_POINTERS_VA - ACTION_POINTERS_VA) // 4
UNIT_ARCHIVE_IDS = range(1, 11)
ENGINE_DIRECTIONS = {'N': 8, 'NE': 9, 'E': 6, 'SE': 3,
                     'S': 2, 'SW': 1, 'W': 4, 'NW': 7}


def read_at(image, va, fmt):
    offset = va - IMAGE_BASE
    size = struct.calcsize(fmt)
    if offset < 0 or offset + size > len(image):
        raise ValueError(f'VA {va:#x} outside image')
    return struct.unpack_from(fmt, image, offset)[0]


def archive_for_type(image, type_index):
    """UnitCtrl 0x466C80 uses param_2 + 8 as type and slot param_2 as path."""
    archive_id = type_index - 8
    if archive_id not in UNIT_ARCHIVE_IDS:
        raise ValueError(f'type {type_index} is not one of the ten unit archives')
    pointer = read_at(image, ARCHIVE_POINTERS_VA + archive_id * 8, '<I')
    start = pointer - IMAGE_BASE
    if not 0 <= start < len(image):
        raise ValueError(f'archive path pointer {pointer:#x} outside image')
    end = image.find(b'\0', start)
    if end < 0:
        raise ValueError(f'archive path at {pointer:#x} is not terminated')
    path = image[start:end].decode('ascii')
    if not path.lower().startswith('data\\dxanim\\') or not path.lower().endswith('.bin'):
        raise ValueError(f'unexpected archive path at {pointer:#x}: {path}')
    return path.rsplit('\\', 1)[-1][:-4].upper()


def type_for_archive(image, archive):
    archive = archive.upper()
    matches = [index + 8 for index in UNIT_ARCHIVE_IDS
               if archive_for_type(image, index + 8) == archive]
    if len(matches) != 1:
        raise ValueError(f'expected one runtime type for archive {archive}, found {matches}')
    return matches[0]


def decode_action(image, type_index, action):
    if not 0 <= type_index < TYPE_COUNT:
        raise ValueError(f'unit type index outside 0..{TYPE_COUNT - 1}')
    if action < 0:
        raise ValueError('action must be nonnegative')
    action_table = read_at(image, ACTION_POINTERS_VA + type_index * 4, '<I')
    program_table = read_at(image, PROGRAM_POINTERS_VA + type_index * 4, '<I')
    if not action_table or not program_table:
        raise ValueError(f'unit type {type_index} has no action/program table')

    directions = {}
    for name, engine_dir in ENGINE_DIRECTIONS.items():
        direction_offset = read_at(image, DIRECTION_OFFSETS_VA + engine_dir, '<B')
        action_entry_va = action_table + (action * 8 + direction_offset) * 2
        program_index = read_at(image, action_entry_va, '<B')
        flags = read_at(image, action_entry_va + 1, '<B')
        encoded_program = read_at(image, program_table + program_index * 2, '<H')
        directions[name] = {
            'engine_direction': engine_dir,
            'program_index': program_index,
            'block': encoded_program >> 8,
            'animation': encoded_program & 0xff,
            'flags': flags & 3,
        }
    return {
        'type_index': type_index,
        'archive': archive_for_type(image, type_index) if type_index - 8 in UNIT_ARCHIVE_IDS else None,
        'action': action,
        'source': 'analysis/hermit_game.exe',
        'action_table_va': action_table,
        'program_table_va': program_table,
        'directions': directions,
    }


def check_archive_programs(result, dx_dir=DX_DIR):
    """Check lookup results against actual BIN program counts; never imply use."""
    archive = result['archive']
    if archive is None:
        return result
    raw = (dx_dir / f'{archive}.BIN').read_bytes()
    programs = dx.parse_program_blocks(raw, dx.parse_dxanim(raw))
    counts = [len(block) for block in programs]
    for entry in result['directions'].values():
        block = entry['block']
        entry['program_present'] = block < len(counts) and entry['animation'] < counts[block]
    result['archive_program_counts'] = counts
    result['all_programs_present'] = all(
        entry['program_present'] for entry in result['directions'].values()
    )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', type=int)
    unit = parser.add_mutually_exclusive_group(required=True)
    unit.add_argument('--type-index', type=int, help='original runtime unit type index')
    unit.add_argument('--archive', help='DXANIM archive name, e.g. D0A')
    args = parser.parse_args()
    try:
        image = EXE.read_bytes()
        type_index = (type_for_archive(image, args.archive) if args.archive
                      else args.type_index)
        result = check_archive_programs(decode_action(image, type_index, args.action))
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
