# -*- coding: utf-8 -*-
"""Decode the executable's two-stage UnitAnim action/direction lookup.

The unit type index used by the executable is intentionally not equated with
a DXANIM archive name here; that relationship has not yet been established.
"""
import argparse
import json
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / 'analysis/hermit_game.exe'
IMAGE_BASE = 0x400000
ACTION_POINTERS_VA = 0x60E850
PROGRAM_POINTERS_VA = 0x60F070
DIRECTION_OFFSETS_VA = 0x610510
TYPE_COUNT = (PROGRAM_POINTERS_VA - ACTION_POINTERS_VA) // 4
ENGINE_DIRECTIONS = {'N': 8, 'NE': 9, 'E': 6, 'SE': 3,
                     'S': 2, 'SW': 1, 'W': 4, 'NW': 7}


def read_at(image, va, fmt):
    offset = va - IMAGE_BASE
    size = struct.calcsize(fmt)
    if offset < 0 or offset + size > len(image):
        raise ValueError(f'VA {va:#x} outside image')
    return struct.unpack_from(fmt, image, offset)[0]


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
        'action': action,
        'source': 'analysis/hermit_game.exe',
        'action_table_va': action_table,
        'program_table_va': program_table,
        'directions': directions,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', type=int)
    parser.add_argument('--type-index', type=int, required=True,
                        help='original runtime unit type index, not DXANIM archive name')
    args = parser.parse_args()
    try:
        result = decode_action(EXE.read_bytes(), args.type_index, args.action)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
