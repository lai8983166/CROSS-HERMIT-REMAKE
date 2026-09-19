# -*- coding: utf-8 -*-
"""单位精灵导出器: DATA/DXANIM/{A..E}{0,1}A.BIN → prototype/assets/unit/<档名>/ + prototype/data/unit_sprites.json

容器/帧/序列解码在 tools/dxanim_lib.py (与 fx_export 共享)。
格式定案: docs/formats.md §10; 逆向过程见 openspec/changes/archive/2026-09-18-add-unit-sprites/design.md

锚点 = 画布底中 (脚底), 帧内偏移 (cw/2 - fx, ch - fy), 数据推导非硬编码。
anim_map 自动挑选 (全部写入 JSON, 手改即生效):
  MOVE = 帧数最多的全界内连续+等时长纯循环 (无空白帧 — 空白会造成移动隐身断流)
  IDLE = 首条非空白单帧动画
用法: python tools/unit_anim_export.py            # 导出全部 10 档
      python tools/unit_anim_export.py A0A C0A   # 只导指定档
"""
import json
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dxanim_lib as dx

DX_DIR = 'CROSS HERMIT/CROSS HERMIT/DATA/DXANIM'
OUT_ASSETS = 'prototype/assets/unit'
OUT_JSON = 'prototype/data/unit_sprites.json'
TOOL_VER = '1.1'
UNIT_FILES = [f'{g}{v}A.BIN' for g in 'ABCDE' for v in '01']
# IDLE 人工覆盖 (视觉逐帧验证 2026-09-18): 启发式"贴行走带"在 B1A 抓到击飞带尾帧 43 (倒栽葱骑士,
# 小图下即"黑软泥怪"); B1A 真立姿 = anim#116 (帧226, 金盔朝上标准站姿)
IDLE_OVERRIDES = {}   # 引擎表 (dxanim_lib.ENGINE_IDLE_ANIM=#7) 已验证优于人工挑选, 覆盖表留空备用


def export_unit(name: str):
    src = os.path.join(DX_DIR, name)
    data = open(src, 'rb').read()
    offs = dx.parse_dxanim(data)
    b0, b5, b6, b7 = offs[0], offs[5], offs[6], offs[7]

    _, nf, foffs = dx.parse_container(data, b6)
    rects = dx.parse_block5_rects(data, b5, nf)
    _, npal, _ = dx.parse_container(data, b7)
    anims = dx.parse_block0_anims(data, b0)
    # 块1 合成动画 (引擎 off=1 朝向引用; 0x409b70/0x4214f0 链定案)
    b1 = offs[1]
    _, n1, eo1 = dx.parse_container(data, b1)
    eo1 = eo1 + [struct.unpack_from('<I', data, b1)[0]]   # 终点=块长
    composites = [{'id': i, 'records': dx.flatten_composite(data, b1, eo1, i, anims)}
                  for i in range(n1)]

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
        'composites': composites,
        '_preview': f'{name[:-4]}/_preview.png',
    }, unit_dir


def pick_anim_map(anims, composites, frame_count, unit_uid):
    """自动挑默认序列 (JSON 可手改): MOVE=帧数最多的连续+等时长纯循环, IDLE=首条单帧动画。
    只认界内引用 (-b ≥ frame_count 的外部引用语义未定, 见 _meta.open_items)。"""
    move = None
    for a in anims:
        recs = a['records']
        # 纯循环: 全部记录都是界内帧 (无空白帧 — 否则移动中会"隐身", 目检 2026-09-18 抓出)
        if len(recs) < 4 or any(r['frame'] < 0 or r['frame'] >= frame_count for r in recs):
            continue
        fr = [r['frame'] for r in recs]
        durs = {r['dur'] for r in recs}
        if len(durs) == 1 and max(fr) - min(fr) + 1 == len(fr):  # 等时长 + 帧号连续
            if move is None or len(recs) > len(move['records']):
                move = a
    idle = None
    # IDLE 挑选: 单帧动画中取"帧号最贴近 MOVE 行走带"者 —— 立绘常紧邻行走帧带排版;
    # 首条单帧会误选同档特效帧 (B0A 目检 2026-09-18: 抓到魔法阵帧)
    if move is not None:
        mv_fr = [r['frame'] for r in move['records']]
        band = (min(mv_fr) + max(mv_fr)) * 0.5
        best_d = None
        for a in anims:
            recs = a['records']
            if len(recs) == 1 and 0 <= recs[0]['frame'] < frame_count:
                dist = abs(recs[0]['frame'] - band)
                if best_d is None or dist < best_d:
                    idle, best_d = a, dist
    if idle is None:
        for a in anims:
            recs = a['records']
            if len(recs) == 1 and 0 <= recs[0]['frame'] < frame_count:
                idle = a
                break
    amap = {}
    if move:
        amap['MOVE'] = {'anim': move['id'], 'flip_x_when_facing_right': True}
    # 引擎朝向表 (汇编链完整闭合): walk/idle 按朝向 → 块0(+5)/块1(直引)
    walk_by_dir, idle_by_dir = dx.engine_dir_map(anims, composites, frame_count)
    if walk_by_dir:
        amap['walk_by_dir'] = walk_by_dir
    if idle_by_dir:
        amap['idle_by_dir'] = idle_by_dir
    if idle_by_dir:
        first_idle = idle_by_dir.get('W') or idle_by_dir.get('S') or {}
        if 'anim' in first_idle:
            idle = anims[first_idle['anim']]
    idle_override = IDLE_OVERRIDES.get(unit_uid)
    if idle_override is not None and 0 <= idle_override < len(anims):
        idle = anims[idle_override]
    if idle:
        amap['IDLE'] = {'anim': idle['id'], 'flip_x_when_facing_right': True}
    for st in ('ATTACK', 'DEAD'):  # 语义标签未定案 → 跟随 IDLE (开口项)
        if idle:
            amap[st] = {'anim': idle['id'], 'flip_x_when_facing_right': True}
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
        unit['anim_map'] = pick_anim_map(unit['anims'], unit['composites'], unit['frame_count'], name[:-4])
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
            'dur_unit_seconds': 1.0 / 60.0,  # 记录 dur 的单位 (秒) — 引擎按 60fps 计帧的假设, 可改
            'frame_index_rule': 'anims[].records[].frame: >=0 → frames 下标; -1 → 空白帧(不绘制)',
            'open_items': [
                '部分档 (D0A/D1A/E0A/E1A 等) 的动画记录存在 -b ≥ 本档帧数的外部引用 (anim#2→250 等; '
                '同构位置在其他档全在界内) — 跨档续编/部件表两种假设均未证实, 默认序列只选界内引用',
                '块1 合成动画表 (27条, 头0x0801) 未解码 — v1 不导出',
                '块4 运动步进字节码 (0xFF06/0x7F06 记录) 未解码 — 攻击位移等细节缺失',
                '块8 (帧数+1 × u8 标志) 语义未定',
                '块7 换色调色板 (40×256) 选择字段未定位 — v1 用帧内嵌调色板',
                '动画语义标签 (哪个 anim id = 何动作/朝向) 未从引擎定案; anim_map 为启发式默认, JSON 手改即生效',
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
