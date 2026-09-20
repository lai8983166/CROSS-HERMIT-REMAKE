# -*- coding: utf-8 -*-
"""单位精灵导出器: DATA/DXANIM/{A..E}{0,1}A.BIN → prototype/assets/unit/<档名>/ + prototype/data/unit_sprites.json

容器/帧/序列解码在 tools/dxanim_lib.py (与 fx_export 共享)。
格式定案: docs/formats.md §10; 逆向过程见 openspec/changes/archive/2026-09-18-add-unit-sprites/design.md

锚点 = 画布底中 (脚底), 帧内偏移 (cw/2 - fx, ch - fy), 数据推导非硬编码。
anim_map 使用原版动作 no=3 的八向表选择 block0 #11～#15；低两位仅作为 x/y 镜像标志。
每条动画离线解释为 steps[].layers[]，运行时无需重做原版 VM。
用法: python tools/unit_anim_export.py            # 导出全部 10 档
      python tools/unit_anim_export.py A0A C0A   # 只导指定档
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dxanim_lib as dx

DX_DIR = 'CROSS HERMIT/CROSS HERMIT/DATA/DXANIM'
OUT_ASSETS = 'prototype/assets/unit'
OUT_JSON = 'prototype/data/unit_sprites.json'
TOOL_VER = '3.0'
UNIT_FILES = [f'{g}{v}A.BIN' for g in 'ABCDE' for v in '01']
IDLE_OVERRIDES = {}


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


def export_unit(name: str):
    src = os.path.join(DX_DIR, name)
    data = open(src, 'rb').read()
    offs = dx.parse_dxanim(data)
    b0, b5, b6, b7 = offs[0], offs[5], offs[6], offs[7]

    _, nf, foffs = dx.parse_container(data, b6)
    rects = dx.parse_block5_rects(data, b5, nf)
    _, npal, _ = dx.parse_container(data, b7)
    anims = decode_timelines(data, offs, nf)

    unit_dir = os.path.join(OUT_ASSETS, name[:-4])  # 去 .BIN
    os.makedirs(unit_dir, exist_ok=True)

    frames = []
    for i in range(nf):
        w, h, idx, pal = dx.decode_bmp(data, b6 + foffs[i])
        cw, ch, fx, fy = rects[i]
        rel = f'frame_{i:03d}.png'
        dx.write_png(os.path.join(unit_dir, rel), w, h, idx, pal)
        frames.append({
            'file': rel, 'w': w, 'h': h,
            'canvas': {'w': cw, 'h': ch, 'x': fx, 'y': fy},
            'anchor': dx.frame_anchor(rects[i]),
        })

    return {
        'source': src, 'frame_count': nf, 'anim_count': len(anims),
        'recolor_palettes': npal, 'frames': frames, 'anims': anims,
        '_preview': f'{name[:-4]}/_preview.png',
    }, unit_dir


def pick_anim_map(anims, frame_count, unit_uid):
    """生成数据驱动映射：MOVE=action 3，ATTACK=action 5。"""
    walk_by_dir, _unused = dx.engine_dir_map(anims, frame_count=frame_count)
    attack_by_dir = dx.engine_attack_dir_map(anims, frame_count=frame_count)
    skill_actions = {
        str(action): dx.engine_action_dir_map(anims, action)
        for action in range(11, 17)
    }
    amap = {
        'walk_by_dir': walk_by_dir,
        'attack_by_dir': attack_by_dir,
        'skill_actions': skill_actions,
    }
    move = walk_by_dir.get('W') or next(iter(walk_by_dir.values()), None)
    if move:
        amap['MOVE'] = {'anim': move['anim'], 'flags': move['flags']}

    idle_override = IDLE_OVERRIDES.get(unit_uid)
    idle_id = idle_override if idle_override is not None else 7
    if not (0 <= idle_id < len(anims)) or not any(step['layers'] for step in anims[idle_id]['steps']):
        idle_id = next((a['id'] for a in anims if any(step['layers'] for step in a['steps'])), None)
    if idle_id is not None:
        amap['IDLE'] = {'anim': idle_id, 'flags': 0}
    attack = attack_by_dir.get('W') or next(iter(attack_by_dir.values()), None)
    if attack:
        amap['ATTACK'] = {'anim': attack['anim'], 'flags': attack['flags']}
    if idle_id is not None:
        amap['DEAD'] = {'anim': idle_id, 'flags': 0}  # DEAD 动作仍待后续语义标注
    return amap


def make_preview(unit_dir, frames, sample=18):
    """抽样帧条带预览图 (目检/后续语义标注用)"""
    from PIL import Image
    step = max(1, len(frames) // sample)
    picks = frames[::step][:sample]
    ims = [Image.open(os.path.join(unit_dir, f['file'])) for f in picks]
    W = sum(im.width for im in ims) + 4 * len(ims)
    H = max(im.height for im in ims) + 12
    sh = Image.new('RGBA', (W, H), (50, 50, 50, 255))
    x = 2
    for im in ims:
        sh.paste(im, (x, H - 6 - im.height), im)
        x += im.width + 4
    sh.save(os.path.join(unit_dir, '_preview.png'))


def main():
    files = sys.argv[1:] or UNIT_FILES
    units = {}
    for name in files:
        unit, unit_dir = export_unit(name)
        unit['anim_map'] = pick_anim_map(unit['anims'], unit['frame_count'], name[:-4])
        make_preview(unit_dir, unit['frames'])
        units[name[:-4]] = unit
        mv = unit['anim_map'].get('MOVE', {})
        print(f'{name[:-4]}: {unit["frame_count"]}帧 {unit["anim_count"]}动画 '
              f'{unit["recolor_palettes"]}调色板 -> {unit_dir} '
              f'| 默认 MOVE=anim#{mv.get("anim")} IDLE=anim#{unit["anim_map"].get("IDLE", {}).get("anim")}')

    out = {
        '_meta': {
            'source_dir': DX_DIR,
            'tool': f'unit_anim_export v{TOOL_VER} (dxanim_lib)',
            'format_ref': 'docs/formats.md §DxAnim',
            'anchor_rule': '画布底中 = 脚底; anchor 为画布底中在帧图像内的像素偏移',
            'schema_version': 2,
            'tick_seconds': 1.0 / 60.0,
            'timeline_rule': 'anims[].steps[] = {duration_ticks,layers[]}; loop_from 为 step 下标或 null',
            'layer_rule': 'layers 按绘制顺序排列，含 frame/x/y/flip_x/flip_y/descriptor 与原始绘制属性',
            'open_items': [
                '块8 (帧数+1 × u8 标志) 语义未定',
                '块7 换色调色板 (40×256) 的逐描述符选择规则只保留原值，当前仍用帧内嵌调色板',
                'DEAD 的完整动作表尚未语义标注，暂沿用 IDLE；MOVE/ATTACK 已按原版动作3/5定案',
            ],
        },
        'units': units,
    }
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    print(f'-> {OUT_JSON} ({len(units)} 档)')


if __name__ == '__main__':
    main()
