# -*- coding: utf-8 -*-
"""Scan original unit archives for skill 22's actions 13, 31 and 16.

This measures original-program availability and visible frame variation, not
whether any character is allowed to learn or cast the skill.
"""
import json
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))
import dxanim_lib as dx
from unit_action_table import (DX_DIR, EXE, archive_for_type,
                               check_archive_programs, decode_action)


ACTIONS = (13, 31, 16)


def frame_luma(raw, frame_start):
    """Mean visible-pixel luminance in the source BMP's embedded palette."""
    _, _, indices, palette = dx.decode_bmp(raw, frame_start)
    visible = [index for index in indices if index != 0]
    if not visible:
        return None
    total = sum(
        (palette[index][2] * 299 + palette[index][1] * 587 +
         palette[index][0] * 114) / 1000
        for index in visible
    )
    return round(total / len(visible), 1)


def scan_archive(image, archive, dx_dir=DX_DIR):
    from unit_action_table import type_for_archive

    type_index = type_for_archive(image, archive)
    raw = (dx_dir / f'{archive}.BIN').read_bytes()
    offsets = dx.parse_dxanim(raw)
    _, frame_count, frame_offsets = dx.parse_container(raw, offsets[6])
    luma_cache = {}
    actions = {}
    for action_id in ACTIONS:
        lookup = check_archive_programs(decode_action(image, type_index, action_id), dx_dir)
        directions = {}
        for name, entry in lookup['directions'].items():
            if not entry['program_present']:
                directions[name] = {'program_present': False}
                continue
            try:
                timeline = dx.interpret_animation(
                    raw, entry['block'], entry['animation'], offs=offsets
                )
                frames = sorted({layer['frame'] for step in timeline['steps']
                                 for layer in step['layers']})
                if any(frame < 0 or frame >= frame_count for frame in frames):
                    raise dx.DxAnimError('timeline frame outside source frame block')
                for frame in frames:
                    if frame not in luma_cache:
                        luma_cache[frame] = frame_luma(raw, offsets[6] + frame_offsets[frame])
                signatures = {
                    tuple((layer['frame'], layer['x'], layer['y']) for layer in step['layers'])
                    for step in timeline['steps'] if step['layers']
                }
                lumas = [luma_cache[frame] for frame in frames
                         if luma_cache[frame] is not None]
                directions[name] = {
                    'program_present': True,
                    'block': entry['block'],
                    'animation': entry['animation'],
                    'flags': entry['flags'],
                    'steps': len(timeline['steps']),
                    'visible_steps': sum(bool(step['layers']) for step in timeline['steps']),
                    'distinct_visual_states': len(signatures),
                    'distinct_frames': len(frames),
                    'mean_frame_luma': round(sum(lumas) / len(lumas), 1) if lumas else None,
                }
            except dx.DxAnimError as exc:
                directions[name] = {'program_present': True, 'decode_error': str(exc)}
        actions[str(action_id)] = {
            'all_programs_present': lookup['all_programs_present'],
            'all_directions_decoded': all(
                item.get('program_present') and 'decode_error' not in item
                for item in directions.values()
            ),
            'directions': directions,
        }
    return {'archive': archive, 'type_index': type_index,
            'frame_count': frame_count, 'actions': actions}


def scan_all(image=EXE.read_bytes()):
    return [scan_archive(image, archive_for_type(image, index))
            for index in range(9, 19)]


def main():
    print(json.dumps(scan_all(), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
