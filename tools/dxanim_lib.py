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


def flatten_composite(data, b1, eo, idx, block0_anims, block0_plus=5, sub_cap=8):
    """块1[idx] → [{frame,dur}] 展平序列

    记录语义 (0x409b70/0x4214f0 链 + 结构对比定案):
      (0x0801=2049 / 0x0601=1537 / 0x0501=1281, X, dx, dy, 0) = 引用块0动画 #(X+block0_plus), 带位移
      (0, -帧, -1, d, dur) = 直接帧;  (2,...) = 控制记录 (v1 跳过)
    引用内联取子动画前 sub_cap 帧; 位移(dx,dy) v1 不应用 (开口)。
    """
    s, e = b1 + eo[idx], b1 + eo[idx + 1]
    out = []
    for k in range((e - s) // 10):
        a, b, c, d_field, dur = struct.unpack_from('<5h', data, s + k * 10)
        if a in (2049, 1537, 1281):
            ref = b + block0_plus
            if 0 <= ref < len(block0_anims):
                for r in block0_anims[ref]['records'][:sub_cap]:
                    out.append((r['frame'], r['dur']))
        elif a == 0 and b <= -2:
            out.append((-b, dur))
    return [{'frame': f, 'dur': du} for f, du in out]


## ── 引擎动画表 (EXE .data 逆向定案 2026-09-18/19, 汇编链完整闭合) ─────────────
## UnitAnim.cpp 0x464d70/0x465040/0x409ff0 → DxAnim.cpp 0x40a400 → 0x4214f0 (容器访问器):
##   表A@0x60D160[布局表@0x610510[dir] + no*8] 取字节对 (b0, b1) → 恒等表B → (动画号=b0, off=b1&3)
##   → 0x409f70(manager, off) = 档案对象字段[off] = 块[off] → 0x4214f0(块[off], 动画号) = 该块第(动画号)条
##   即: off=0 → 块0 条目(引擎号+5=块0下标), off=1 → 块1 条目(直引)
## 移动 no=2 (dir → (b0, off)): d1=(9,0) d2=(10,0) d3=(10,1) d4=(8,0) d5=(6,0)
##   d6=(8,1) d7=(7,0) d8=(6,0) d9=(7,1)
## 待机 no=1 (dir → (b0, off)): d1=(4,0) d2=(4,0) d3=(4,1) d4=(4,0) d5=(2,0)
##   d6=(4,1) d7=(2,0) d8=(2,0) d9=(2,1)
## 朝向→罗盘 (视觉标注: d5/d8=块0#11 面左, d7=块0#12 面右, d4=块0#13 右斜, d1=块0#14 左斜, d2=块0#15 正面):
ENGINE_DIR8 = {
    # 罗盘: (dir号, no=2 移动, no=1 待机)
    'W':  (5, (6, 0), (2, 0)),
    'E':  (7, (7, 0), (2, 0)),
    'NW': (1, (9, 0), (4, 0)),
    'NE': (4, (8, 0), (4, 0)),
    'S':  (2, (10, 0), (4, 0)),
    'N':  (3, (10, 1), (4, 1)),
    'SW': (6, (8, 1), (4, 1)),
    'SE': (9, (7, 1), (2, 1)),
}
ENGINE_BLOCK0_PLUS = 5   # 引擎动画号 → 块0 下标 偏移 (锚: 引擎0=空→#5 空白; 引擎6..10→#11..15 行走带)


def engine_dir_map(anims, composites, frame_count):
    """生成 walk_by_dir / idle_by_dir: off=0 → 块0[#b0+5], off=1 → 块1[b0] (直引)"""
    def entry(b0, off):
        if off == 0:
            slot = b0 + ENGINE_BLOCK0_PLUS
            if slot >= len(anims):
                return {}
            recs = anims[slot]['records']
            if not recs or any(r['frame'] >= frame_count for r in recs):
                return {}
            return {'block': 0, 'anim': slot}
        else:
            if b0 >= len(composites):
                return {}
            recs = composites[b0]['records']
            if not recs or any(r['frame'] >= frame_count for r in recs):
                return {}
            return {'block': 1, 'composite': b0}
    walk, idle = {}, {}
    for d, (_dirno, mv, idl) in ENGINE_DIR8.items():
        e1 = entry(*mv)
        if e1:
            walk[d] = e1
        e2 = entry(*idl)
        if e2:
            idle[d] = e2
    return walk, idle
