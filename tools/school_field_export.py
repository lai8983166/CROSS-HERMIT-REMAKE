"""Source-only MAP05 navigation, formation and current student presentation.

No native output case supplies runtime values. Movement scheduling is a remake
interaction, not a projection of the original world loop.
"""
import argparse
import hashlib
import json
import struct
from pathlib import Path
from PIL import Image
from tools.school_formation_placement_catalog import source_catalog as formation_source
from tools.school_current_units_catalog import source_catalog as units_source
from tools.school_enemy_records_catalog import source_catalog as scene_source, expected_record
from tools.school_first_unit_animation_catalog import normalize_palette
from tools.school_adventure_handoff_emulation import ROOT
from tools import dxanim_lib as dx

SKINS = {3: 10, 4: 6, 9: 7}
DIRECTIONS = {'NW': 1, 'N': 2, 'NE': 3, 'W': 4, 'E': 6, 'SW': 7, 'S': 8, 'SE': 9}
OUTPUT = ROOT / 'prototype/assets/school_field'


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def skin_inputs(character, job, rules, *, actions=None, variant=None):
    identity = rules['source']
    raw = (ROOT / identity['local_file']).read_bytes()
    if digest(raw) != identity['sha256']:
        raise ValueError('field animation source identity')
    offsets = dx.parse_dxanim(raw)
    _, count, image_offsets = dx.parse_container(raw, offsets[6])
    rects = dx.parse_block5_rects(raw, offsets[5], count)
    if variant is None:
        palette_index = rules['job_input']['palettes_by_character'][character]
        variant = palette_index + 1 if palette_index else 0
    _, palette_count, palette_offsets = dx.parse_container(raw, offsets[7])
    if not 0 <= variant <= palette_count:
        raise ValueError('field palette index')
    at = offsets[7] + palette_offsets[variant-1] if variant else 0
    external = normalize_palette(raw[at:at+1024]) if variant else None
    selected_actions = actions or [('idle', 1), ('move', 3)]
    actions, frames, images = {}, {}, {}
    for name, action in selected_actions:
        directions = {}
        for direction, engine_direction in DIRECTIONS.items():
            mapped = rules['direction_map'][engine_direction]
            position, flags = bytes.fromhex(rules['action_rows'][action])[mapped*2:mapped*2+2]
            word = rules['position_words'][position]
            block, animation = word >> 8, word & 255
            timeline = dx.interpret_animation(raw, block, animation, offs=offsets)
            directions[direction] = {k: timeline[k] for k in ('steps', 'loop_from')}
            directions[direction].update(flags=flags & 3, block=block, animation=animation)
            for step in timeline['steps']:
                for layer in step['layers']:
                    frame = layer['frame']
                    if not 0 <= frame < count:
                        raise ValueError('field frame bounds')
                    if str(frame) in frames:
                        continue
                    frame_at = offsets[6] + image_offsets[frame]
                    w, h, indices, _ = dx.decode_bmp(raw, frame_at)
                    embedded = normalize_palette(raw[frame_at+54:frame_at+1078])
                    use_external = bool(variant) and raw[offsets[8]+frame] == 0
                    palette = external if use_external else embedded
                    # Existing DxAnim export convention: indexed zero is transparent.
                    rgba = b''.join(palette[i*4:i*4+3][::-1] + bytes([0 if i == 0 else 255]) for i in indices)
                    image = Image.frombytes('RGBA', (w, h), rgba)
                    filename = f'{character}/frame_{frame:03d}.png'
                    cw, ch, x, y = rects[frame]
                    frames[str(frame)] = {'file': filename, 'w': w, 'h': h,
                        'canvas': {'w': cw, 'h': ch, 'x': x, 'y': y},
                        'rgba_sha256': digest(rgba), 'palette_sha256': digest(palette),
                        'external_palette': use_external}
                    images[filename] = image
        actions[name] = directions
    return {'character_id': character, 'job': job, 'source': identity,
        'palette_variant': variant, 'frames': frames, 'actions': actions}, images


def source_inputs():
    formation = formation_source()
    scene = scene_source()
    units = units_source()
    logical = bytes.fromhex(formation['map_hex'])
    terrain = bytes.fromhex(formation['terrain_hex'])
    config = bytes.fromhex(json.loads((ROOT/'prototype/data/school_adventure_handoff_rules.json').read_text('utf-8'))['configuration_record_hex'])
    if config.hex() != '050000000001140910000000000000051e050a0f01010111111121000000000000000000000000000000':
        raise ValueError('field configuration identity')
    cells = [list(c) for c in struct.iter_unpack('<3H', logical[16:])]
    passability = []
    for mode in range(5):
        row = []
        for cell in cells:
            if cell[0] >= len(terrain)//76:
                raise ValueError('field terrain bounds')
            row.append(int(mode == 4 or struct.unpack_from('<i', terrain, cell[0]*76+mode*16+12)[0] != 0))
        passability.append(row)
    occupied = []
    for ordinal, template in enumerate(scene['templates']):
        record = expected_record(template, rules=scene)
        if record['state'] == 1:
            occupied.append({'ordinal': ordinal, 'character_id': record['identity'],
                'category': record['category'], 'cell': record['coordinates']})
    grid = [list(v[:3]) for v in struct.iter_unpack('<bbHH', bytes.fromhex(formation['grid_hex']))]
    result = {'schema_version': 1, 'scene_id': 5, 'cell_size': [64, 96],
        'pixel_size': [2048, 1536], 'cell_pixels': [32, 16],
        'source_image_sha256': formation['source_image_sha256'],
        'logical_source': formation['logical_source'], 'terrain_source': formation['terrain_source'],
        'configuration_hex': config.hex(), 'origin': list(config[7:9]), 'formation_radius': config[15],
        'formation_grid': grid, 'initial_rotation': 0, 'permutation_size': 5, 'rotation_multiplier': 3,
        'cells': cells, 'passability': passability, 'static_occupancy': occupied,
        'skins': {}, 'interaction': {'logic_hz': 30, 'move_interval': 12, 'delta_cap': 0.2},
        'scope': 'Read-only current-student deployment and remake movement trial; no source world loop, enemy AI, waves, victory or save authority.'}
    images = {}
    for character, job in SKINS.items():
        row = bytes.fromhex(scene['jobs'][str(job)]['row_hex'])
        mode = bytes.fromhex(scene['movement_types_hex'])[row[0x16]]
        skin, pixels = skin_inputs(character, job, units['jobs'][str(job)])
        skin['movement_type'] = mode
        result['skins'][str(character)] = skin
        images.update(pixels)
    return result, images


def export(destination=OUTPUT):
    catalog, images = source_inputs()
    for filename, image in images.items():
        target = destination / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        image.save(target)
    for skin in catalog['skins'].values():
        for frame in skin['frames'].values():
            frame['file_sha256'] = digest((destination/frame['file']).read_bytes())
    (destination/'catalog.json').write_text(json.dumps(catalog, ensure_ascii=False, separators=(',', ':'))+'\n', encoding='utf-8', newline='\n')
    return catalog


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=OUTPUT)
    args = parser.parse_args()
    catalog = export(args.out)
    print('MAP05 cells=%d; source skins=%d; frames=%d' % (len(catalog['cells']), len(catalog['skins']), sum(len(s['frames']) for s in catalog['skins'].values())))
