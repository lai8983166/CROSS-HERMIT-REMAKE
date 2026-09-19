# -*- coding: utf-8 -*-
"""验证原始 DxAnim 与运行时 JSON 的八向 MOVE，并生成 A0A/B1A 六帧对照表。"""
import json
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dxanim_lib as dx


ROOT = Path(__file__).resolve().parents[1]
DX_DIR = ROOT / 'CROSS HERMIT' / 'CROSS HERMIT' / 'DATA' / 'DXANIM'
SPRITES = ROOT / 'prototype' / 'data' / 'unit_sprites.json'
ASSETS = ROOT / 'prototype' / 'assets' / 'unit'
OUTPUT = ROOT / 'analysis' / 'dxanim_walk_comparison.png'
DIRECTIONS = ('NW', 'N', 'NE', 'W', 'E', 'SW', 'S', 'SE')


def semantic_steps(timeline):
    return [
        (
            step['duration_ticks'],
            [
                (layer['frame'], layer['x'], layer['y'], layer['descriptor'])
                for layer in step['layers']
            ],
        )
        for step in timeline['steps']
    ]


def paste_layer(canvas, frame_image, frame_data, layer, flags):
    image = frame_image
    flip_x = bool(layer.get('flip_x', False)) != bool(flags & 1)
    flip_y = bool(layer.get('flip_y', False)) != bool(flags & 2)
    if flip_x:
        image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if flip_y:
        image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    canvas_data = frame_data['canvas']
    x = canvas_data['x'] - canvas_data['w'] / 2 + layer.get('x', 0)
    y = canvas_data['y'] - canvas_data['h'] / 2 + layer.get('y', 0)
    if flip_x:
        x = -x - image.width
    if flip_y:
        y = -y - image.height
    canvas.alpha_composite(image, (round(64 + x), round(64 + y)))


def render_cell(unit_id, unit, step, flags):
    canvas = Image.new('RGBA', (128, 128), (42, 42, 42, 255))
    for layer in step['layers']:
        frame = layer['frame']
        image = Image.open(ASSETS / unit_id / unit['frames'][frame]['file']).convert('RGBA')
        paste_layer(canvas, image, unit['frames'][frame], layer, flags)
    return canvas


def main():
    exported = json.loads(SPRITES.read_text('utf-8'))['units']
    cell_w, cell_h = 132, 152
    sheet = Image.new('RGBA', (cell_w * 6, cell_h * 16), (24, 24, 24, 255))
    draw = ImageDraw.Draw(sheet)

    row = 0
    for unit_id in ('A0A', 'B1A'):
        raw_data = (DX_DIR / f'{unit_id}.BIN').read_bytes()
        unit = exported[unit_id]
        mapping = unit['anim_map']['walk_by_dir']
        for direction in DIRECTIONS:
            entry = mapping[direction]
            animation = entry['anim']
            flags = entry['flags']
            raw = dx.interpret_animation(raw_data, 0, animation)
            runtime = unit['anims'][animation]
            if raw['loop_from'] != runtime['loop_from'] or semantic_steps(raw) != semantic_steps(runtime):
                raise dx.DxAnimError(f'{unit_id} {direction}: raw/runtime timeline mismatch')
            if len(runtime['steps']) != 6 or runtime['loop_from'] != 0:
                raise dx.DxAnimError(f'{unit_id} {direction}: expected six-step loop from zero')

            draw.text((4, row * cell_h + 3),
                      f'{unit_id} {direction}  block0#{animation} flags={flags}  raw=runtime',
                      fill=(255, 255, 255, 255))
            for index, step in enumerate(runtime['steps']):
                cell = render_cell(unit_id, unit, step, flags)
                x = index * cell_w
                y = row * cell_h + 20
                sheet.alpha_composite(cell, (x, y))
                frames = '+'.join(str(layer['frame']) for layer in step['layers']) or 'blank'
                draw.text((x + 3, y + 3), f'{index}: f{frames} d{step["duration_ticks"]}',
                          fill=(255, 230, 90, 255))
            row += 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.crop((0, 0, sheet.width, row * cell_h)).save(OUTPUT)
    print(f'16 direction rows verified; raw descriptor timelines equal runtime JSON')
    print(OUTPUT)


if __name__ == '__main__':
    main()
