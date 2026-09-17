# -*- coding: utf-8 -*-
"""原版地图纹理图集渲染器: MAP##.MAP → prototype/assets/map##_atlas.png

格式 (docs/formats.md §5, B 线实证):
  头 8B = [u16 pageX][u16 pageY][u16 起始xy对][u16 ?]
  纹理页 = pageX×pageY × 256×256 X1RGB555 (bit15=alpha, 地图页实测 100% 置位→按不透明解码)
  页序 = 行优先 (相关系数 0.488 vs 列优先 -0.012)
  页起点 = 变长 (MAP01=0x4D8, MAP02=0x404) → 行重复签名扫描定位 + 连续性自校验

用法: python tools/render_map_atlas.py 01
产物: prototype/assets/map##_atlas.png + map##_atlas.json
"""
import json
import os
import struct
import sys

from PIL import Image

MAP_DIR = 'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/MAP'
OUTDIR = 'prototype/assets'
PS = 256                       # 页边长
PAGE_BYTES = PS * PS * 2       # X1RGB555
ROW_SIG = 512                  # 行字节距 (256px×2B)


def find_page_start(data: bytes, pages: int) -> int:
    """页起点检测 (2026-09-18 定案: 行相关不可判别 — 真页起点 0.04~0.55, 页中点可达 0.39;
    BMP 缩略相关也全平 ±8B — 无独立地面真值):
    表区为小整数 (bit15 不置位), 图像页 X1RGB555 的 bit15 实测 100% 置位 →
    严门 = 候选处前 256 u16 全不透明 + 大窗 ≥64 不同值, 且末页起点同检;
    升序扫描首中即真起点 (0x436/0x4D4 两次误检均为 99% 容差被表尾 2 个非透明 u16 钻空)."""
    def looks_like_page(off: int) -> bool:
        for p in struct.unpack_from('<256H', data, off):
            if not (p & 0x8000):
                return False
        return True   # 多样性辅证已移除: 错杀 MAP02 平坦页角 (<64 distinct)

    end = len(data) - pages * PAGE_BYTES
    off = 0x400
    while off < end:
        if looks_like_page(off) and looks_like_page(off + (pages - 1) * PAGE_BYTES):
            return off
        off += 2
    return -1


def decode_page(data: bytes, off: int) -> bytes:
    px = struct.unpack_from(f'<{PS*PS}H', data, off)
    buf = bytearray(PS * PS * 3)
    for i, p in enumerate(px):
        buf[i*3] = (p >> 10 & 31) * 255 // 31
        buf[i*3+1] = (p >> 5 & 31) * 255 // 31
        buf[i*3+2] = (p & 31) * 255 // 31
    return bytes(buf)


def render(num: str) -> None:
    src = os.path.join(MAP_DIR, f'MAP{num}.MAP')
    if not os.path.exists(src):
        sys.stderr.write(f'错误: 找不到 {src}\n')
        sys.exit(1)
    data = open(src, 'rb').read()
    page_x, page_y = struct.unpack_from('<2H', data, 0)
    pages = page_x * page_y
    if pages < 1 or len(data) < pages * PAGE_BYTES:
        sys.stderr.write(f'错误: 头部页数 {page_x}x{page_y} 与文件大小 {len(data):,} 不符\n')
        sys.exit(1)

    start = find_page_start(data, pages)
    if start < 0:
        sys.stderr.write(f'错误: 页起点签名扫描失败 ({src}), 请核对格式\n')
        sys.exit(1)

    atlas = Image.new('RGB', (page_x * PS, page_y * PS))
    for idx in range(pages):
        px, py = idx % page_x, idx // page_x          # 行优先 (design 决策/B线实证)
        img = Image.frombytes('RGB', (PS, PS), decode_page(data, start + idx * PAGE_BYTES))
        atlas.paste(img, (px * PS, py * PS))

    os.makedirs(OUTDIR, exist_ok=True)
    png = os.path.join(OUTDIR, f'map{num}_atlas.png')
    atlas.save(png, optimize=True)
    meta = {
        'map': f'MAP{num}', 'source': src, 'page_start': start,
        'page_layout': 'row-major', 'pixel_format': 'X1RGB555 (bit15 alpha ignored)',
        'size': [atlas.size[0], atlas.size[1]], 'pages': [page_x, page_y],
        'regen': f'python tools/render_map_atlas.py {num}',
    }
    with open(os.path.join(OUTDIR, f'map{num}_atlas.json'), 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    print(f'MAP{num}: {page_x}x{page_y} 页 @{start:#x} -> {png} ({atlas.size[0]}x{atlas.size[1]})')


if __name__ == '__main__':
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        sys.stderr.write('用法: python tools/render_map_atlas.py <两位地图编号, 如 01>\n')
        sys.exit(2)
    render(sys.argv[1].zfill(2))
