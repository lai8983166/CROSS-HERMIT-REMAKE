#!/usr/bin/env python3
"""文件指纹: 打印文件头 hex + ASCII + 熵, 并给出格式猜测。

用法:
    python tools/fingerprint.py <文件...>        # 指定文件
    python tools/fingerprint.py --tree <目录>    # 每个子目录抽1个样本
"""
import argparse
import math
import os
import sys


def entropy_head(data: bytes) -> float:
    if not data:
        return 0.0
    counts = [0] * 256
    for b in data:
        counts[b] += 1
    ent = 0.0
    for c in counts:
        if c:
            p = c / len(data)
            ent -= p * math.log2(p)
    return ent


def guess(head: bytes, size: int) -> str:
    mags = [(b"RIFF", "RIFF容器"), (b"BM", "BMP"), (b"\x89PNG", "PNG"),
            (b"ID3", "MP3"), (b"\xff\xfb", "MP3"), (b"MThd", "MIDI"),
            (b"PK\x03\x04", "ZIP"), (b"MZ", "PE程序"), (b"MSCF", "CAB")]
    for m, name in mags:
        if head.startswith(m):
            return name
    # 2MB+N 模式 -> 未压缩裸位图
    body = size - len(head)
    if body % 1048576 == 0:
        return f"疑似裸图像数据 ({body//1024}KB 像素体, 头部{len(head)}B)"
    return "自定义格式"


def show(path: str):
    with open(path, "rb") as f:
        head = f.read(64)
    size = os.path.getsize(path)
    asc = "".join(chr(c) if 32 <= c < 127 else "." for c in head[:32])
    print(f"{path}")
    print(f"  大小 {size:,} B | 熵(头64B) {entropy_head(head):.2f} | {guess(head, size)}")
    print(f"  hex : {head[:32].hex()}")
    print(f"  asc : |{asc}|")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--tree", action="store_true", help="把参数当目录, 每个子目录抽1个样本")
    args = ap.parse_args()

    targets = []
    for p in args.paths:
        if args.tree:
            for root, dirs, files in os.walk(p):
                bins = [f for f in files if not f.lower().endswith((".mp3", ".wav", ".bmp", ".jpg", ".txt"))]
                if bins:
                    targets.append(os.path.join(root, sorted(bins)[0]))
        else:
            targets.append(p)
    for t in targets:
        try:
            show(t)
        except OSError as e:
            print(f"{t}: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
