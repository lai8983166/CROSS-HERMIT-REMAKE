# -*- coding: utf-8 -*-
"""攻击特效导出器: DATA/DXANIM/##E.BIN → prototype/assets/fx/<档>/ + prototype/data/attack_effects.json

##E 特效档 = 与单位档同容器 9 块格式 (01E 侦察 2026-09-18):
  块0～3 是动画程序，块4 描述符解析到最终 BMP；opcode1 子动画与父动画并发。
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
TOOL_VER = '2.0'
DEFAULT_FILES = ['01E.BIN']


def decode_timelines(data, offs, frame_count):
    programs = dx.parse_program_blocks(data, offs)
    timelines = []
    for animation in range(len(programs[0])):
        timeline = dx.interpret_animation(data, 0, animation, offs=offs)
        for step_index, step in enumerate(timeline['steps']):
            for layer in step['layers']:
                if layer['frame'] >= frame_count:
                    raise dx.DxAnimError(
                        f'block0 animation {animation} step {step_index}: '
                        f'frame {layer["frame"]} >= {frame_count}'
                    )
        timelines.append({
            'id': animation,
            'steps': timeline['steps'],
            'loop_from': timeline['loop_from'],
        })
    return timelines


def pick_play_timeline(timelines, min_steps=4):
    """选最长的非循环可见时间线作为未命名 PLAY；具名效果仍由 effects 显式指定。"""
    candidates = []
    for timeline in timelines:
        visible = [step for step in timeline['steps'] if step['layers']]
        if timeline['loop_from'] is None and len(visible) >= min_steps:
            candidates.append((len(visible), sum(step['duration_ticks'] for step in visible), timeline))
    return max(candidates, key=lambda item: (item[0], item[1]))[2] if candidates else None


def export_fx(name: str):
    src = os.path.join(DX_DIR, name)
    data = open(src, 'rb').read()
    offs = dx.parse_dxanim(data)
    b0, b5, b6, b7 = offs[0], offs[5], offs[6], offs[7]

    _, nf, foffs = dx.parse_container(data, b6)
    rects = dx.parse_block5_rects(data, b5, nf)
    _, npal, _ = dx.parse_container(data, b7)
    anims = decode_timelines(data, offs, nf)

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

    play = pick_play_timeline(anims)
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
        recs = entry['anims'][play]['steps'] if play is not None else []
        blanks = sum(1 for step in recs if not step['layers'])
        print(f'{fid}: {entry["frame_count"]}帧 {entry["anim_count"]}动画 '
              f'{entry["recolor_palettes"]}调色板 -> {OUT_ASSETS}/{fid} '
              f'| PLAY=anim#{play} ({len(recs)}记录, 空白{blanks})')

    out = {
        '_meta': {
            'source_dir': DX_DIR,
            'tool': f'fx_export v{TOOL_VER} (dxanim_lib)',
            'format_ref': 'docs/formats.md §DxAnim',
            'schema': 'files.* 与 unit_sprites.json units.* 同 schema (视图共用渲染路径)',
            'schema_version': 2,
            'playback': 'PLAY = 播一次; steps[].duration_ticks 使用 1/60 秒 tick',
            'open_items': [
                '##E 动画语义未标注 (哪档哪条 = 何种斩击/魔法) — effects.default 可配置, 默认 01E',
                '块7 特效换色板 (6×256) 选择规则未定 — v1 基色',
            ],
        },
        'files': out_files,
        # v2 按最终描述符帧逐步复核：#21 在蓝色本体动作中并发生成紫色斩击层；#28 为蓝色旋转体。
        # 旧配置 #15 是纯软泥循环，是把指令短整数误作 BMP 帧号后产生的错误标签。
        'effects': {
            'slash': {'file': '01E', 'anim': 21},
            'orb': {'file': '01E', 'anim': 28},
        },
        'default': 'slash',
    }
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    print(f'-> {OUT_JSON} ({len(out_files)} 档, default=slash@01E)')


if __name__ == '__main__':
    main()
