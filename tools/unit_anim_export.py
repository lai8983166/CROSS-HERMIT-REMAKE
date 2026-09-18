# -*- coding: utf-8 -*-
"""单位精灵导出器: DATA/DXANIM/{A..E}{0,1}A.BIN → prototype/assets/unit/<档名>/ + prototype/data/unit_sprites.json

DxAnim 格式 (docs/formats.md §DxAnim, 逆向定案见 openspec/changes/add-unit-sprites/design.md):
  容器 = {u32 总长; u32 块数; u32 offs[块数]} (offs[0] == 8+4×块数 自洽校验)
  块0 = 动画定义表 {len; n; offs[n]}, 条目 = k × 10B 记录 (i16 画布w, i16 -帧号, i16 -1, i16 -14, i16 时长)
        帧号 <0 且 ≠-1 → 块6 帧索引; -1 = 空白帧; 记录顺序 = 播放顺序
  块5 = 帧数 × 8B 直排 (i16 画布w, 画布h, 帧x, 帧y)  —— 帧在画布中的摆放
  块6 = 帧容器 {len; n; offs[n]}, 每帧 = 标准 8bpp BMP (内嵌 1024B 调色板, 底上行序, 4 对齐, 索引0=透明)
  块7 = 换色调色板 {len; n; offs[n]} (单位档 40×1024B, v1 不应用)
锚点 = 画布底中 (脚底), 帧内偏移 (cw/2 - fx, ch - fy), 数据推导非硬编码。

anim_map 自动挑选 (全部写入 JSON, 手改即生效):
  MOVE = 帧数最多的"连续帧号+等时长"序列 (行走循环特征)
  IDLE = 首个非空白单帧动画
用法: python tools/unit_anim_export.py            # 导出全部 10 档
      python tools/unit_anim_export.py A0A C0A   # 只导指定档
"""
import json
import os
import struct
import sys

sys.stdout.reconfigure(encoding='utf-8')

DX_DIR = 'CROSS HERMIT/CROSS HERMIT/DATA/DXANIM'
OUT_ASSETS = 'prototype/assets/unit'
OUT_JSON = 'prototype/data/unit_sprites.json'
TOOL_VER = '1.0'
UNIT_FILES = [f'{g}{v}A.BIN' for g in 'ABCDE' for v in '01']


def parse_container(data: bytes, base: int):
    """通用档案容器 {u32 len; u32 n; u32 offs[n]} → (n, offs列表, 终点=len)"""
    clen, n = struct.unpack_from('<II', data, base)
    offs = list(struct.unpack_from(f'<{n}I', data, base + 8))
    return clen, n, offs


def parse_dxanim(data: bytes):
    """容器级解析 + 自洽校验, 返回块偏移表

    校验: offs[0] == 8+4×块数; 偏移严格递增; 头部总长 == 文件长度。
    (末块 块8 无 {len;n} 头 —— 前 4B 即数据, 不能对其做块长校验)
    """
    total, nblk = struct.unpack_from('<II', data, 0)
    offs = list(struct.unpack_from(f'<{nblk}I', data, 8))
    if offs[0] != 8 + 4 * nblk:
        raise ValueError(f'offset table not self-consistent: offs[0]={offs[0]} != {8 + 4 * nblk}')
    if any(offs[i] > offs[i + 1] for i in range(nblk - 1)):
        raise ValueError('block offsets not increasing')  # 相邻相等 = 空块 (如 A0A 块2 len=0)
    if len(data) != total:
        raise ValueError(f'file size {len(data)} != header total {total}')
    return offs


def decode_bmp(data: bytes, s: int):
    """块6 内单帧 (标准 8bpp BMP, 内嵌调色板) → (w, h, 索引数组[h][w], 调色板[256][4])"""
    if data[s:s + 2] != b'BM':
        raise ValueError(f'非 BMP 帧 @{s}: {data[s:s + 2]!r}')
    w, h = struct.unpack_from('<ii', data, s + 18)
    px_off = struct.unpack_from('<I', data, s + 10)[0]
    if px_off != 54 + 1024:
        raise ValueError(f'BMP 像素偏移 {px_off} != 54+1024 (非内嵌 1024B 调色板)')
    stride = (w + 3) // 4 * 4
    rows = []
    for y in range(h):  # 底上行序 → 顶向下
        rows.append(data[s + px_off + y * stride: s + px_off + y * stride + w])
    idx = b''.join(reversed(rows))
    pal = [tuple(data[s + 54 + c * 4: s + 54 + c * 4 + 3]) + (0 if c == 0 else 255,)
           for c in range(256)]  # BGRX → 保留 BGR, 索引0 透明
    return w, h, idx, pal


def write_png(path: str, w: int, h: int, idx: bytes, pal) -> None:
    from PIL import Image
    import numpy as np
    a = np.frombuffer(idx, np.uint8).reshape(h, w)
    p = np.array(pal, np.uint8)  # (256,4) BGRA
    rgba = p[a][:, :, [2, 1, 0, 3]]  # → RGBA
    Image.fromarray(rgba).save(path)


def export_unit(name: str):
    src = os.path.join(DX_DIR, name)
    data = open(src, 'rb').read()
    offs = parse_dxanim(data)
    b0, b5, b6, b7 = offs[0], offs[5], offs[6], offs[7]

    # 块6 帧
    _, nf, foffs = parse_container(data, b6)
    # 块5 画布矩形 (帧数×8B 直排无头)
    rects = [struct.unpack_from('<4h', data, b5 + i * 8) for i in range(nf)]
    if len(rects) != nf:
        raise ValueError(f'块5 条数 {len(rects)} != 帧数 {nf}')
    # 块7 调色板数 (元数据)
    _, npal, _ = parse_container(data, b7)
    # 块0 动画定义
    _, na, aoffs = parse_container(data, b0)
    aoffs = aoffs + [struct.unpack_from('<I', data, b0)[0]]

    unit_dir = os.path.join(OUT_ASSETS, name[:-4])  # 去 .BIN
    os.makedirs(unit_dir, exist_ok=True)

    frames = []
    for i in range(nf):
        w, h, idx, pal = decode_bmp(data, b6 + foffs[i])
        cw, ch, fx, fy = rects[i]
        rel = f'frame_{i:03d}.png'
        write_png(os.path.join(unit_dir, rel), w, h, idx, pal)
        frames.append({
            'file': rel, 'w': w, 'h': h,
            'canvas': {'w': cw, 'h': ch, 'x': fx, 'y': fy},
            'anchor': {'x': cw / 2 - fx, 'y': ch - fy},  # 画布底中 → 帧内偏移
        })

    anims = []
    for ai in range(na):
        s, e = b0 + aoffs[ai], b0 + aoffs[ai + 1]
        recs = []
        for k in range((e - s) // 10):
            cw, b, c, d_field, dur = struct.unpack_from('<5h', data, s + k * 10)
            # b <= -2 → 帧索引(-b); b == -1 → 空白帧; b >= 0 → 控制/终止记录 (0x0801头/32643终止符等)
            frame = -b if b <= -2 else -1
            recs.append({'frame': frame, 'dur': dur})
        anims.append({'id': ai, 'records': recs})

    return {
        'source': src, 'frame_count': nf, 'anim_count': na,
        'recolor_palettes': npal, 'frames': frames, 'anims': anims,
        '_preview': f'{name[:-4]}/_preview.png',
    }, unit_dir


def pick_anim_map(anims):
    """自动挑默认序列 (JSON 可手改): MOVE=最多帧的连续+等时长序列, IDLE=首条非空白单帧动画"""
    move = None
    for a in anims:
        recs = a['records']
        valid = [r for r in recs if r['frame'] >= 0]
        if len(valid) < 4 or len(valid) != len(recs):
            continue  # 混有空白/控制记录的 (如 anim#89 带 30/58 帧停顿) 不作默认 MOVE
        fr = [r['frame'] for r in valid]
        durs = {r['dur'] for r in valid}
        span = max(fr) - min(fr) + 1
        if len(durs) == 1 and span == len(fr):  # 全有效 + 等时长 + 帧号连续 = 纯循环
            if move is None or len(valid) > len(move['records']):
                move = a
    idle = None
    for a in anims:
        if len(a['records']) == 1 and a['records'][0]['frame'] >= 0:
            idle = a
            break
    amap = {}
    if move:
        amap['MOVE'] = {'anim': move['id'], 'flip_x_when_facing_right': True}
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
        unit['anim_map'] = pick_anim_map(unit['anims'])
        make_preview(unit_dir, unit['frames'])
        units[name[:-4]] = unit
        mv = unit['anim_map'].get('MOVE', {})
        print(f'{name[:-4]}: {unit["frame_count"]}帧 {unit["anim_count"]}动画 '
              f'{unit["recolor_palettes"]}调色板 -> {unit_dir} '
              f'| 默认 MOVE=anim#{mv.get("anim")} IDLE=anim#{unit["anim_map"].get("IDLE", {}).get("anim")}')

    out = {
        '_meta': {
            'source_dir': DX_DIR,
            'tool': f'unit_anim_export v{TOOL_VER}',
            'format_ref': 'docs/formats.md §DxAnim',
            'anchor_rule': '画布底中 = 脚底; anchor 为画布底中在帧图像内的像素偏移',
            'frame_index_rule': 'anims[].records[].frame: >=0 → frames 下标; -1 → 空白帧(不绘制)',
            'open_items': [
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
