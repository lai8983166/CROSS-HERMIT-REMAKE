# -*- coding: utf-8 -*-
"""地图逻辑层导出器: MAP##.BIN → prototype/data/map##.json

格式 (docs/formats.md §5, 已逆向定案):
  头 16B = 8×u16 [pxW][pxH][cellW][cellH][tileW=256][tileH=256][pageX][pageY]
  体 = cellW×cellH × 3 层 u16 (层序: terrain / variant / object, 行优先)
校验: 文件大小 == 16 + 6×格数 (不符报错退出, 不产出半成品)

用法: python tools/map_export.py 01
"""
import json
import os
import struct
import sys

BIN_DIR = 'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/MAP'
OUTDIR = 'prototype/data'
TOOL_VER = '1.0'
LAYER_NAMES = ('terrain', 'variant', 'object')


def export(num: str) -> None:
    src = os.path.join(BIN_DIR, f'MAP{num}.BIN')
    if not os.path.exists(src):
        sys.stderr.write(f'错误: 找不到 {src}\n')
        sys.exit(1)
    data = open(src, 'rb').read()
    if len(data) < 16:
        sys.stderr.write(f'错误: {src} 过小 ({len(data)}B < 16B 头)\n')
        sys.exit(1)

    px_w, px_h, cell_w, cell_h, tile_w, tile_h, page_x, page_y = \
        struct.unpack_from('<8H', data, 0)
    cells = cell_w * cell_h
    expect = 16 + 6 * cells
    if len(data) != expect:
        sys.stderr.write(f'错误: {src} 尺寸不符 (实际 {len(data):,}, 头部推定 {expect:,} '
                         f'= 16+6×{cell_w}×{cell_h}); BIN 格式或地图编号有误\n')
        sys.exit(1)
    if px_w != cell_w * 32 or px_h != cell_h * 16:
        sys.stderr.write(f'警告: px/格 不符 32×16 ({px_w}×{px_h} vs {cell_w}×{cell_h})\n')

    layers = {}
    for li, name in enumerate(LAYER_NAMES):
        layers[name] = list(struct.unpack_from(f'<{cells}H', data, 16 + li * 2 * cells))

    out = {
        '_meta': {
            'map': f'MAP{num}', 'source_bin': src,
            'px_w': px_w, 'px_h': px_h,
            'cell_w': cell_w, 'cell_h': cell_h,
            'tile_w': tile_w, 'tile_h': tile_h,
            'page_x': page_x, 'page_y': page_y,
            'layers': list(LAYER_NAMES), 'layout': 'row-major, index = y*cell_w + x',
            'naming_ref': 'docs/formats.md#5 (BIN 逻辑格图)',
            'tool': f'map_export v{TOOL_VER}',
        },
        'layers': layers,
    }
    os.makedirs(OUTDIR, exist_ok=True)
    dst = os.path.join(OUTDIR, f'map{num}.json')
    with open(dst, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    zero_ratio = sum(1 for v in layers['terrain'] if v == 0) / cells
    print(f'MAP{num}: {cell_w}x{cell_h} 格 ({px_w}x{px_h}px, 页 {page_x}x{page_y}) '
          f'-> {dst} | terrain 零值占比 {zero_ratio:.1%}')


if __name__ == '__main__':
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        sys.stderr.write('用法: python tools/map_export.py <两位地图编号, 如 01>\n')
        sys.exit(2)
    export(sys.argv[1].zfill(2))
