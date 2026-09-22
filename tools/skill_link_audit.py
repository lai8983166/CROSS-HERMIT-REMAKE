# -*- coding: utf-8 -*-
"""Audit known links between attack, presentation, unit action and EFCT IDs.

This is an evidence inventory, not a reconstruction of runtime dispatch.
An absent exported action/FX is not proof that the original game lacks it.
"""
import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'prototype/data'
ACTION_FIELDS = ('cast_action', 'release_action', 'recover_action')
FX_FIELDS = ('cast_fx', 'release_fx', 'sync_fx', 'impact_fx')


def load_sources(data_dir=DATA):
    def read(name):
        return json.loads((data_dir / name).read_text(encoding='utf-8'))

    return {
        'attack': read('attack_table.json'),
        'visual': read('skill_visuals.json'),
        'unit': read('unit_sprites.json'),
        'fx': read('attack_effects.json'),
    }


def audit_action(action_id, unit, direction):
    if action_id == 0:
        return {'id': action_id, 'status': 'none'}
    anim_map = unit['anim_map']
    if action_id == 3:
        mapping = anim_map.get('walk_by_dir', {})
    elif action_id == 5:
        mapping = anim_map.get('attack_by_dir', {})
    else:
        mapping = anim_map.get('skill_actions', {}).get(str(action_id))
    if mapping is None:
        return {'id': action_id, 'status': 'not_exported'}
    entry = mapping.get(direction)
    if entry is None:
        return {'id': action_id, 'status': 'no_exported_direction'}
    return {
        'id': action_id,
        'status': 'exported',
        'animation': entry['anim'],
        'block': entry['block'],
        'flags': entry['flags'],
    }


def audit_fx(global_id, fx):
    if global_id == 0:
        return {'id': global_id, 'status': 'none'}
    if global_id < 1000:
        return {'id': global_id, 'status': 'outside_archive'}
    block = global_id // 1000 - 1
    animation = global_id % 1000
    counts = fx['_meta']['block_animation_counts']
    result = {'id': global_id, 'block': block, 'animation': animation}
    if block < 0 or block >= len(counts) or animation >= counts[block]:
        result['status'] = 'outside_archive'
    elif str(global_id) in fx['animations']:
        result['status'] = 'exported'
    else:
        result['status'] = 'valid_not_exported'
    return result


def audit_skill(skill_id, unit_id, direction, sources):
    attacks = sources['attack']['rows']
    visuals = sources['visual']['rows']
    units = sources['unit']['units']
    if not 0 <= skill_id < len(visuals):
        raise ValueError(f'skill ID {skill_id} outside visual table 0..{len(visuals) - 1}')
    if skill_id >= len(attacks):
        raise ValueError(f'skill ID {skill_id} outside attack table')
    if unit_id not in units:
        raise ValueError(f'unknown unit archive {unit_id}; available: {", ".join(sorted(units))}')
    if direction not in ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'):
        raise ValueError(f'unknown direction {direction}')
    attack = attacks[skill_id]
    visual = visuals[skill_id]
    if attack['id'] != skill_id or visual['id'] != skill_id:
        raise ValueError(f'row ID mismatch at skill {skill_id}')

    return {
        'skill_id': skill_id,
        'unit_archive': unit_id,
        'direction': direction,
        'attack': {
            'source': 'attack_table.json',
            'targeting': attack['targeting'],
            'target_filter': attack['target_filter'],
            'hit_effect': attack['hit_effect'],
            'mp_cost': attack['mp_cost'],
            'cast_frames': attack['cast_frames'],
            'recovery_frames': attack['recovery_frames'],
        },
        'visual': {
            'source': 'skill_visuals.json',
            'detail_id': visual['detail_id'],
            'gameplay_effect_id': visual['gameplay_effect_id'],
            'effect_id_matches_attack': visual['gameplay_effect_id'] == attack['hit_effect'],
            'actions': {
                field: audit_action(visual[field], units[unit_id], direction)
                for field in ACTION_FIELDS
            },
            'fx': {
                field: audit_fx(visual[field], sources['fx'])
                for field in FX_FIELDS
            },
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('skill_id', type=int)
    parser.add_argument('--unit', required=True, help='DXANIM unit archive, e.g. C0A')
    parser.add_argument('--direction', default='N', help='N/NE/E/SE/S/SW/W/NW')
    args = parser.parse_args()
    try:
        result = audit_skill(args.skill_id, args.unit, args.direction.upper(), load_sources())
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
