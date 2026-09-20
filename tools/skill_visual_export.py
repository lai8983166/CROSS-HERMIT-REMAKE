# -*- coding: utf-8 -*-
"""Export the executable's skill-presentation table.

This table is deliberately kept separate from ``attack_table.json``: the
attack table describes gameplay, while this table selects unit actions and
global animations from ``DATA/DXANIM/EFCT.BIN``.
"""
import hashlib
import json
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / 'analysis/hermit_game.exe'
ATTACK_JSON = ROOT / 'prototype/data/attack_table.json'
OUTPUT = ROOT / 'prototype/data/skill_visuals.json'

IMAGE_BASE = 0x400000
DETAIL_VA = 0x611538
NEXT_TABLE_VA = 0x613B78
DETAIL_STRIDE = 0x10
DETAIL_COUNT = (NEXT_TABLE_VA - DETAIL_VA) // DETAIL_STRIDE
TOOL_VERSION = '1.0'


def decode_skill_visuals(exe_data: bytes, attack_rows: list[dict], image_sha1: str):
    gameplay_effects = {row['id']: row.get('hit_effect', 0) for row in attack_rows}
    rows = []
    for skill_id in range(DETAIL_COUNT):
        offset = DETAIL_VA - IMAGE_BASE + skill_id * DETAIL_STRIDE
        (
            cast_action,
            release_action,
            recover_action,
            flags,
            cast_fx,
            release_fx,
            detail_id,
            sync_fx,
            impact_fx,
            shape,
        ) = struct.unpack_from('<BBBBhhhhhh', exe_data, offset)
        rows.append({
            'id': skill_id,
            'cast_action': cast_action,
            'release_action': release_action,
            'recover_action': recover_action,
            'flags': flags,
            'cast_fx': cast_fx,
            'release_fx': release_fx,
            'detail_id': detail_id,
            'sync_fx': sync_fx,
            'impact_fx': impact_fx,
            'shape': shape,
            'gameplay_effect_id': gameplay_effects.get(skill_id, 0),
        })
    return {
        '_meta': {
            'table': 'skill_visuals',
            'source_va': DETAIL_VA,
            'stride': DETAIL_STRIDE,
            'count': DETAIL_COUNT,
            'image_sha1_8': image_sha1[:8],
            'tool': f'skill_visual_export v{TOOL_VERSION}',
            'fx_source': 'CROSS HERMIT/CROSS HERMIT/DATA/DXANIM/EFCT.BIN',
            'fx_id_rule': 'global_id // 1000 - 1 = block; global_id % 1000 = animation',
            'notes': [
                'gameplay_effect_id comes from attack_table.hit_effect and is not a visual resource id',
                'detail_id names the observed +0x08 value without assigning unproven runtime semantics',
            ],
        },
        'rows': rows,
    }


def main():
    exe_data = EXE.read_bytes()
    attack_data = json.loads(ATTACK_JSON.read_text('utf-8'))
    result = decode_skill_visuals(
        exe_data,
        attack_data['rows'],
        hashlib.sha1(exe_data).hexdigest(),
    )
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'skill_visuals: {len(result["rows"])} rows -> {OUTPUT.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
