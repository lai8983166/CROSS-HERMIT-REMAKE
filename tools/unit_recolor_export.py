# -*- coding: utf-8 -*-
"""换色表导出器: DATA/DXANIM/{A..E}{0,1}A.BIN 块7 → prototype/data/unit_recolors.json
                       + prototype/assets/unit/<档>/_recolors.png (40 色预览)

块7 定案 (formats.md §10, add-unit-recolor 侦察):
  {len; n=40; offs[n]}, 每条 1024B BGRX 调色板 (0 号透明)
  [0] == 身体帧内嵌调色板 (基色, 逐字节 dist=0); [9] = 黑影红边特殊版;
  引擎侧 palette 选择字段未定位 (开口) — 重制侧由 battle_setup.json 手配

匹配率校验: 统计各档"内嵌调色板 == 块7[0]"的帧占比 (身体帧比例), 写入 _meta
用法: python tools/unit_recolor_export.py
"""
import json
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')

DX_DIR = 'CROSS HERMIT/CROSS HERMIT/DATA/DXANIM'
OUT_JSON = 'prototype/data/unit_recolors.json'
OUT_ASSETS = 'prototype/assets/unit'
TOOL_VER = '1.0'
UNIT_FILES = [f'{g}{v}A.BIN' for g in 'ABCDE' for v in '01']


def load_blocks(name: str):
    data = open(os.path.join(DX_DIR, name), 'rb').read()
    total, nblk = struct.unpack_from('<II', data, 0)
    offs = list(struct.unpack_from(f'<{nblk}I', data, 8))
    if offs[0] != 8 + 4 * nblk or len(data) != total:
        raise ValueError(f'{name} 容器不自洽')
    return data, offs


def parse_block7(data: bytes, b7: int):
    _, n = struct.unpack_from('<II', data, b7)
    offs = list(struct.unpack_from(f'<{n}I', data, b7 + 8))
    pals = []
    for i in range(n):
        p = []
        for c in range(256):
            b, g, r, _ = data[b7 + offs[i] + c * 4: b7 + offs[i] + c * 4 + 4]
            p.append(f'{r:02x}{g:02x}{b:02x}')
        pals.append(p)
    return n, pals


def frame_palettes(data: bytes, offs):
    """块6 每帧内嵌调色板 (用于匹配率统计与预览选基帧)"""
    b6 = offs[6]
    _, nf = struct.unpack_from('<II', data, b6)
    foffs = list(struct.unpack_from(f'<{nf}I', data, b6 + 8))
    out = []
    for i in range(nf):
        s = b6 + foffs[i]
        p = []
        for c in range(256):
            b, g, r, _ = data[s + 54 + c * 4: s + 58 + c * 4]
            p.append((r, g, b))
        out.append(p)
    return out


def make_preview(unit_id: str, data: bytes, offs, pals, fps):
    """基帧 (内嵌==块7[0] 的首个身体帧) × 40 色 → _recolors.png"""
    import numpy as np
    from PIL import Image
    b6 = offs[6]
    _, nf = struct.unpack_from('<II', data, b6)
    foffs = list(struct.unpack_from(f'<{nf}I', data, b6 + 8))
    base = [(int(p[0:2], 16), int(p[2:4], 16), int(p[4:6], 16)) for p in pals[0]]
    base_idx = next(i for i, fp in enumerate(fps) if fp == base)
    s = b6 + foffs[base_idx]
    w, h = struct.unpack_from('<ii', data, s + 18)
    px = struct.unpack_from('<I', data, s + 10)[0]
    st = (w + 3) // 4 * 4
    idx = np.zeros((h, w), np.uint8)
    for y in range(h):
        idx[h - 1 - y] = np.frombuffer(data[s + px + y * st: s + px + y * st + w], np.uint8)
    CW, CH = w + 6, h + 6
    sheet = Image.new('RGBA', (CW * 8, CH * -(-len(pals) // 8)), (50, 50, 50, 255))
    for k, pal in enumerate(pals):
        arr = np.zeros((256, 4), np.uint8)
        for c, hx in enumerate(pal):
            arr[c] = [int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16), 255]
        arr[0] = [0, 0, 0, 0]
        im = Image.fromarray(arr[idx])
        sheet.paste(im, ((k % 8) * CW + 3, (k // 8) * CH + 3), im)
    sheet = sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST)
    sheet.save(os.path.join(OUT_ASSETS, unit_id, '_recolors.png'))
    return base_idx


def main():
    units = {}
    stats = {}
    for name in UNIT_FILES:
        data, offs = load_blocks(name)
        npal, pals = parse_block7(data, offs[7])
        fps = frame_palettes(data, offs)
        base = [(int(p[0:2], 16), int(p[2:4], 16), int(p[4:6], 16)) for p in pals[0]]
        n_body = sum(1 for fp in fps if fp == base)
        uid = name[:-4]
        preview_frame = make_preview(uid, data, offs, pals, fps)
        units[uid] = {'palette_count': npal, 'palettes': pals}
        stats[uid] = n_body
        print(f'{uid}: {npal} 调色板, 身体帧(内嵌==[0]) {n_body}/{len(fps)}, '
              f'预览基帧 #{preview_frame} -> assets/unit/{uid}/_recolors.png')

    out = {
        '_meta': {
            'source_dir': DX_DIR,
            'tool': f'unit_recolor_export v{TOOL_VER}',
            'format_ref': 'docs/formats.md §10 块7',
            'entry_semantics': 'hex RRGGBB; 索引 0 = 透明; palettes[0] = 基色(==身体帧内嵌)',
            'special': 'palette 9 = 黑影红边特殊版 (语义未考据)',
            'body_frame_ratio': stats,
            'open_items': [
                '引擎侧 palette 选择字段未定位 — battle_setup.json 手配 palette_id 即用',
                '块7 分组 (步长9: {10,19,28,37} 等) 的语义规律未定',
            ],
        },
        'units': units,
    }
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    print(f'-> {OUT_JSON}')


if __name__ == '__main__':
    main()
