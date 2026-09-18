# -*- coding: utf-8 -*-
"""攻击特效导出器: DATA/DXANIM/##E.BIN → prototype/assets/fx/<档>/ + prototype/data/attack_effects.json

##E 特效档 = 与单位档同容器 9 块格式 (01E 侦察 2026-09-18):
  块0 #1..#N 全是播一次序列 (首帧 dur=20 定格起手 + 后续 dur=6 降序帧串)
  块5=帧数×8B, 块6=帧 BMP, 块7=6 张换色板 (选择规则开口)
解码在 tools/dxanim_lib.py。帧表 schema 与 unit_sprites.json 相同 (视图共用渲染路径)。

attack_effects.json: {files: {档: {frames/anims/anim_map.PLAY}}, effects: {名字: {file, anim}},
default: 名字} — anim 缺省取该档 PLAY 自动挑选结果。

用法: python tools/fx_export.py            # 默认 01E
      python tools/fx_export.py 01E 20E   # 多档
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dxanim_lib as dx

DX_DIR = 'CROSS HERMIT/CROSS HERMIT/DATA/DXANIM'
OUT_ASSETS = 'prototype/assets/fx'
OUT_JSON = 'prototype/data/attack_effects.json'
TOOL_VER = '1.0'
DEFAULT_FILES = ['01E.BIN']


def export_fx(name: str):
    src = os.path.join(DX_DIR, name)
    data = open(src, 'rb').read()
    offs = dx.parse_dxanim(data)
    b0, b5, b6, b7 = offs[0], offs[5], offs[6], offs[7]

    _, nf, foffs = dx.parse_container(data, b6)
    rects = dx.parse_block5_rects(data, b5, nf)
    _, npal, _ = dx.parse_container(data, b7)
    anims = dx.parse_block0_anims(data, b0)

    fx_dir = os.path.join(OUT_ASSETS, name[:-4])  # 去 .BIN
    os.makedirs(fx_dir, exist_ok=True)

    frames = []
    for i in range(nf):
        w, h, idx, pal = dx.decode_bmp(data, b6 + foffs[i])
        rel = f'frame_{i:03d}.png'
        dx.write_png(os.path.join(fx_dir, rel), w, h, idx, pal)
        frames.append({
            'file': rel, 'w': w, 'h': h,
            'canvas': {'w': rects[i][0], 'h': rects[i][1], 'x': rects[i][2], 'y': rects[i][3]},
            'anchor': dx.frame_anchor(rects[i]),
        })

    play = dx.pick_play_sequence(anims, nf)
    amap = {'PLAY': {'anim': play['id']}} if play else {}
    return name[:-4], {
        'source': src, 'frame_count': nf, 'anim_count': len(anims),
        'recolor_palettes': npal, 'frames': frames, 'anims': anims, 'anim_map': amap,
    }


def main():
    files = [f if f.endswith('.BIN') else f + '.BIN' for f in (sys.argv[1:] or DEFAULT_FILES)]
    out_files = {}
    for name in files:
        fid, entry = export_fx(name)
        out_files[fid] = entry
        play = entry['anim_map'].get('PLAY', {}).get('anim')
        recs = entry['anims'][play]['records'] if play is not None else []
        blanks = sum(1 for r in recs if r['frame'] < 0)
        print(f'{fid}: {entry["frame_count"]}帧 {entry["anim_count"]}动画 '
              f'{entry["recolor_palettes"]}调色板 -> {OUT_ASSETS}/{fid} '
              f'| PLAY=anim#{play} ({len(recs)}记录, 空白{blanks})')

    out = {
        '_meta': {
            'source_dir': DX_DIR,
            'tool': f'fx_export v{TOOL_VER} (dxanim_lib)',
            'format_ref': 'docs/formats.md §DxAnim',
            'schema': 'files.* 与 unit_sprites.json units.* 同 schema (视图共用渲染路径)',
            'playback': 'PLAY = 播一次; 时长单位沿用 unit_sprites.json _meta.dur_unit_seconds',
            'open_items': [
                '##E 动画语义未标注 (哪档哪条 = 何种斩击/魔法) — effects.default 可配置, 默认 01E',
                '块7 特效换色板 (6×256) 选择规则未定 — v1 基色',
            ],
        },
        'files': out_files,
        # 命名只收"亲眼逐帧验证过"的 (2026-09-18 两次事故: #22/#19 均为软泥素材被误标斩击):
        # 帧5..10 = 紫月斩 (唯一已验真斩击) | 帧88..93 = 灰蓝光球弹丸
        # 帧11..30 = 软泥怪素材带 (23..26 = 史莱姆本体!) | 帧31..75 = 蓝色弹体/软泥带
        'effects': {
            'slash': {'file': '01E', 'anim': 15},
            'orb': {'file': '01E', 'anim': 28},
        },
        'default': 'slash',
    }
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    print(f'-> {OUT_JSON} ({len(out_files)} 档, default=slash@01E)')


if __name__ == '__main__':
    main()
