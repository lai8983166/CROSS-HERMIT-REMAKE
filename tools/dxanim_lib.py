# -*- coding: utf-8 -*-
"""DxAnim 共享解码库 (formats.md §10)

被 tools/unit_anim_export.py (单位档 {A..E}{0,1}A) 与 tools/fx_export.py (特效档 ##E)
共用：容器解析 / BMP 帧解码 / 块0 动画记录 / 块5 画布矩形与锚点。
"""
import struct


class DxAnimError(Exception):
    pass


def parse_dxanim(data: bytes):
    """容器级解析 + 自洽校验，返回块偏移表。

    校验: offs[0] == 8+4×块数; 偏移非递减 (相邻相等 = 空块); 头部总长 == 文件长度。
    (末块 块8 无 {len;n} 头 —— 前 4B 即数据, 不能对其做块长校验)
    """
    total, nblk = struct.unpack_from('<II', data, 0)
    offs = list(struct.unpack_from(f'<{nblk}I', data, 8))
    if offs[0] != 8 + 4 * nblk:
        raise DxAnimError(f'offset table not self-consistent: offs[0]={offs[0]} != {8 + 4 * nblk}')
    if any(offs[i] > offs[i + 1] for i in range(nblk - 1)):
        raise DxAnimError('block offsets not increasing')
    if len(data) != total:
        raise DxAnimError(f'file size {len(data)} != header total {total}')
    return offs


def parse_container(data: bytes, base: int):
    """通用档案容器 {u32 len; u32 n; u32 offs[n]} → (块长, 条数, 偏移列表)"""
    clen, n = struct.unpack_from('<II', data, base)
    offs = list(struct.unpack_from(f'<{n}I', data, base + 8))
    return clen, n, offs


def decode_bmp(data: bytes, s: int):
    """块6 内单帧 (标准 8bpp BMP, 内嵌调色板) → (w, h, 索引 bytes, 调色板[256][4 RGBA])"""
    if data[s:s + 2] != b'BM':
        raise DxAnimError(f'not a BMP frame @{s}: {data[s:s + 2]!r}')
    w, h = struct.unpack_from('<ii', data, s + 18)
    px_off = struct.unpack_from('<I', data, s + 10)[0]
    if px_off != 54 + 1024:
        raise DxAnimError(f'BMP pixel offset {px_off} != 54+1024 (no embedded 1024B palette)')
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


def parse_block5_rects(data: bytes, b5: int, frame_count: int):
    """块5 = 帧数×8B 直排 (无头): (画布w, 画布h, 帧x, 帧y) i16 —— 与帧数校验"""
    if (len(data) - b5) < frame_count * 8:
        raise DxAnimError(f'block5 too small for {frame_count} frames')
    return [struct.unpack_from('<4h', data, b5 + i * 8) for i in range(frame_count)]


def frame_anchor(rect):
    """画布底中 = 脚底 → 画布底中在帧图像内的像素偏移 (cw/2 - fx, ch - fy)"""
    cw, ch, fx, fy = rect
    return {'x': cw / 2 - fx, 'y': ch - fy}


def parse_block0_anims(data: bytes, b0: int):
    """块0 动画定义表 → [{id, records: [{frame, dur}]}]

    10B 记录 (i16 画布w, b, i16, i16, i16 时长):
      b <= -2 → 帧索引(-b); b == -1 → 空白帧 (隐身 dur, 特效的显隐演出语义);
      控制/终止记录 (a=32643 终止符 / a=2049 头 / b>=0) 跳过不进序列。
    """
    _, n, aoffs = parse_container(data, b0)
    aoffs = aoffs + [struct.unpack_from('<I', data, b0)[0]]
    anims = []
    for ai in range(n):
        s, e = b0 + aoffs[ai], b0 + aoffs[ai + 1]
        recs = []
        for k in range((e - s) // 10):
            cw, b, c, d_field, dur = struct.unpack_from('<5h', data, s + k * 10)
            if cw == 32643 or cw == 2049 or b >= 0:
                continue
            frame = -b if b <= -2 else -1
            recs.append({'frame': frame, 'dur': dur})
        anims.append({'id': ai, 'records': recs})
    return anims


def load_frames(data: bytes, offs):
    """块6 全帧解码 → (foffs, [(w,h,idx,pal), ...])"""
    b6 = offs[6]
    _, nf, foffs = parse_container(data, b6)
    frames = [decode_bmp(data, b6 + foffs[i]) for i in range(nf)]
    return foffs, frames


def pick_play_sequence(anims, frame_count, min_frames=4):
    """挑播一次序列 (fx PLAY): 帧引用全部界内 (无外部引用) 的 ≥min_frames 帧序列,
    取有效帧最多者。与 unit 的 MOVE 纯循环不同: 空白帧不否决 (特效显隐是演出语义)。"""
    best = None
    for a in anims:
        recs = a['records']
        if any(r['frame'] >= frame_count for r in recs):   # 外部引用 → 排除
            continue
        valid = [r for r in recs if r['frame'] >= 0]
        if len(valid) < min_frames:
            continue
        if best is None or len(valid) > sum(1 for r in best['records'] if r['frame'] >= 0):
            best = a
    return best
