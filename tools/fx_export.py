# -*- coding: utf-8 -*-
"""Export selected global animations from the runtime ``EFCT.BIN`` archive.

Global animation IDs use the executable's mapping:
``block = global_id // 1000 - 1`` and ``animation = global_id % 1000``.
Only frames referenced by the selected timelines are written.
"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dxanim_lib as dx


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'CROSS HERMIT/CROSS HERMIT/DATA/DXANIM/EFCT.BIN'
OUT_ASSETS = ROOT / 'prototype/assets/fx/EFCT'
OUT_JSON = ROOT / 'prototype/data/attack_effects.json'
TOOL_VERSION = '3.0'

# Skill 29's complete visual chain plus two reverse-engineering anchors.
DEFAULT_GLOBAL_IDS = (2042, 2050, 2098, 3017, 3027, 3032)


def split_global_id(global_id: int):
    if global_id < 1000:
        raise dx.DxAnimError(f'invalid global animation id {global_id}')
    return global_id // 1000 - 1, global_id % 1000


def export_fx(global_ids):
    data = SOURCE.read_bytes()
    offs = dx.parse_dxanim(data)
    programs = dx.parse_program_blocks(data, offs)
    if len(offs) <= 6:
        raise dx.DxAnimError('EFCT.BIN does not contain its frame block')
    _, frame_count, frame_offsets = dx.parse_container(data, offs[6])
    rects = dx.parse_block5_rects(data, offs[5], frame_count)

    animations = {}
    referenced_frames = set()
    for global_id in sorted(set(global_ids)):
        block, animation = split_global_id(global_id)
        if block >= len(programs) or animation >= len(programs[block]):
            raise dx.DxAnimError(
                f'global animation {global_id} maps outside EFCT.BIN: '
                f'block={block} animation={animation}'
            )
        timeline = dx.interpret_animation(data, block, animation, offs=offs)
        for step_index, step in enumerate(timeline['steps']):
            for layer in step['layers']:
                frame = layer['frame']
                if not 0 <= frame < frame_count:
                    raise dx.DxAnimError(
                        f'global animation {global_id} step {step_index}: '
                        f'frame {frame} outside 0..{frame_count - 1}'
                    )
                referenced_frames.add(frame)
        animations[str(global_id)] = {
            'global_id': global_id,
            'block': block,
            'animation': animation,
            'steps': timeline['steps'],
            'loop_from': timeline['loop_from'],
            'duration_ticks': timeline['duration_ticks'],
        }

    OUT_ASSETS.mkdir(parents=True, exist_ok=True)
    frames = {}
    for frame in sorted(referenced_frames):
        width, height, indices, palette = dx.decode_bmp(data, offs[6] + frame_offsets[frame])
        filename = f'frame_{frame:04d}.png'
        dx.write_png(str(OUT_ASSETS / filename), width, height, indices, palette)
        rect = rects[frame]
        frames[str(frame)] = {
            'file': filename,
            'w': width,
            'h': height,
            'canvas': {'w': rect[0], 'h': rect[1], 'x': rect[2], 'y': rect[3]},
            'anchor': dx.frame_anchor(rect),
        }

    return {
        '_meta': {
            'source': str(SOURCE.relative_to(ROOT)).replace('\\', '/'),
            'tool': f'fx_export v{TOOL_VERSION} (dxanim_lib)',
            'format_ref': 'docs/formats.md §DxAnim',
            'schema_version': 3,
            'frame_count': frame_count,
            'exported_frame_count': len(frames),
            'block_animation_counts': [len(block_programs) for block_programs in programs],
            'global_id_rule': 'block = global_id // 1000 - 1; animation = global_id % 1000',
            'playback': 'steps[].duration_ticks use 1/60 second ticks; loop_from is a step index',
        },
        'frames': frames,
        'animations': animations,
    }


def main():
    global_ids = [int(value) for value in sys.argv[1:]] or list(DEFAULT_GLOBAL_IDS)
    result = export_fx(global_ids)
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding='utf-8')
    print(
        f'EFCT: {len(result["animations"])} animations, '
        f'{len(result["frames"])} / {result["_meta"]["frame_count"]} frames '
        f'-> {OUT_JSON.relative_to(ROOT)}'
    )


if __name__ == '__main__':
    main()
