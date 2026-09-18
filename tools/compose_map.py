# -*- coding: utf-8 -*-
"""世界布局定稿 (add-map-composition): **直角投影** —— 图集即世界图 (2048×1536 == px 头)

定案证据 (2026-09-18):
  1. 引擎像素→格 = 线性整除 (x>>21=px/32, y>>20=py/16) — battle_mechanics §1
  2. BMP 宽高比 1.34 ≈ 地图 1.33
  3. iso 仿射 8 朝向 corr ≤0.113 vs 直角 0.488 (全灭反证)
结论: composed == atlas (恒等); 本工具留作管线锚点 (后续层烘焙/物件叠加在此扩展)
用法: python tools/compose_map.py 01 [--report]
"""
import json
import os
import sys

from PIL import Image

ATLAS = 'prototype/assets/map{num}_atlas.png'
BMP = 'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/MAP/MAP{num}.BMP'
OUT = 'prototype/assets/map{num}_composed.png'


def corr_vs_bmp(img: Image.Image, bmp: Image.Image) -> float:
    a = img.convert('L').resize(bmp.size).tobytes()
    b = bmp.convert('L').tobytes()
    n = len(b)
    ma, mb = sum(a) / n, sum(b) / n
    cov = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
    return cov / (sum((a[i] - ma) ** 2 for i in range(n)) ** 0.5) / (sum((b[i] - mb) ** 2 for i in range(n)) ** 0.5)


def main() -> None:
    num = None
    for arg in sys.argv[1:]:
        if arg.isdigit():
            num = arg.zfill(2)
    if not num:
        sys.stderr.write('用法: python tools/compose_map.py <编号> [--report]\n')
        sys.exit(2)
    atlas_path = ATLAS.format(num=num)
    if not os.path.exists(atlas_path):
        sys.stderr.write(f'错误: 缺 {atlas_path}\n')
        sys.exit(1)
    atlas = Image.open(atlas_path).convert('RGB')
    atlas.save(OUT.format(num=num))   # 直角定案: 世界图 == 图集 (恒等; 层烘焙扩展点)
    meta = {
        'map': f'MAP{num}', 'projection': 'straight (cell rect [32x,16y,32,16])',
        'identity_of': atlas_path,
        'evidence': 'engine linear cell div (x>>21,y>>20) + bmp aspect + iso variants corr<=0.113',
        # 实机截图模板匹配验证过的世界窗口 (analysis/map_window_match.md):
        # 屏幕 ≈ 图集该窗口 ×1.02 平移 (+428,+434); 取景=引擎视口 1024x568 (43b460 钳制)
        'verified_window': {'x': 421, 'y': 434, 'w': 1018, 'h': 668},
        'regen': f'python tools/compose_map.py {num}',
    }
    with open(OUT.format(num=num) + '.json', 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    if '--report' in sys.argv:
        bmp = Image.open(BMP.format(num=num))
        print(f'直角(=图集) corr = {corr_vs_bmp(atlas, bmp):.3f} | iso 变体 ≤0.113 (已灭)')
    print(f'-> {OUT.format(num=num)}')


if __name__ == '__main__':
    main()
