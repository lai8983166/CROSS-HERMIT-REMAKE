#!/usr/bin/env python3
"""渲染 CROSS HERMIT 的裸 16bit 位图 (.BIN: 24字节容器头 + X1RGB555 像素体)。

用法:
    python tools/render_dximg.py <文件.BIN...> [-o 输出目录] [--sheet out.png]
        --sheet  额外把所有渲染结果拼成一张缩略对比图
已确认格式: 头部24B [u32总长][u32条目数][u32=0x0C]["DX\\2\\0"][4B参数][4B参数]
            像素体 1024x1024 X1RGB555 小端, bit15=alpha(1=不透明)
            内容区约 1024x784, 其余为透明填充
"""
import argparse
import os
import struct

import sys
from PIL import Image

W, H, HEADER = 1024, 1024, 24

# 像素体大小 -> (宽, 高, bpp)。0x80 参数标记 = 8bit 强度/蒙版, 否则 16bit X1RGB555
SIZE_TABLE = {
    2097152: (1024, 1024, 16),   # BG/BATTLE/HAN/KOJIN 大图
    1048576: (1024, 512, 16),    # H-PART
    524288:  (512, 512, 16),     # GYBC
    262144:  (512, 512, 8),      # TC 系列文字蒙版 (参数含0x80)
    65536:   (256, 256, 8),      # B-PART (参数含0x80)
}


def render(path: str) -> Image.Image:
    raw = open(path, "rb").read()
    body = raw[HEADER:]
    if len(body) not in SIZE_TABLE:
        raise ValueError(f"未知像素体大小: {len(body)}")
    w, h, bpp = SIZE_TABLE[len(body)]
    if bpp == 8:
        return Image.frombytes("L", (w, h), body[: w * h])
    n = w * h
    px = struct.unpack(f"<{n}H", body[: n * 2])
    img = Image.new("RGBA", (w, h))
    img.putdata([
        (
            ((v >> 10) & 31) * 255 // 31,
            ((v >> 5) & 31) * 255 // 31,
            (v & 31) * 255 // 31,
            255 if v & 0x8000 else 0,
        )
        for v in px
    ])
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("-o", "--out", default="extracted/render")
    ap.add_argument("--sheet", help="拼接缩略对比图输出路径")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    thumbs = []
    for f in args.files:
        try:
            img = render(f)
        except (OSError, ValueError) as e:
            print(f"[失败] {f}: {e}")
            continue
        out = os.path.join(args.out, os.path.splitext(os.path.basename(f))[0] + ".png")
        img.save(out)
        print(f"[OK] {f} -> {out}")
        thumbs.append((os.path.basename(f), img))

    if args.sheet and thumbs:
        tw, th = 340, 340
        cols = 3
        rows = (len(thumbs) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * tw, rows * th), (24, 24, 24))
        for i, (name, img) in enumerate(thumbs):
            x, y = (i % cols) * tw, (i // cols) * th
            sheet.paste(img.resize((tw, th)), (x, y))
        sheet.save(args.sheet)
        print(f"[OK] 对比图 -> {args.sheet}")


if __name__ == "__main__":
    main()
