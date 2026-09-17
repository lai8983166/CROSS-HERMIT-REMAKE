#!/usr/bin/env python3
"""扫描游戏目录：输出每个文件的 magic bytes、大小、熵，辅助判断打包/压缩/加密格式。

用法:
    python tools/scan_pack.py <游戏目录> [--min-size 1024]
熵参考: ~0-3 文本/简单数据, 4-6 位图/音频, >7.5 压缩或加密
"""
import argparse
import math
import os
import struct
import sys

# 常见老游戏资源格式的 magic 签名
KNOWN_MAGICS = {
    b"RIFF": "RIFF (WAV/AVI)",
    b"MThd": "MIDI",
    b"BM": "BMP",
    b"\x89PNG": "PNG",
    b"\xff\xd8\xff": "JPEG",
    b"OggS": "OGG",
    b"ID3": "MP3 (ID3)",
    b"\x1f\x8b": "GZIP",
    b"PK\x03\x04": "ZIP",
    b"Rar!": "RAR",
    b"MZ": "PE 可执行文件",
    b"\x00\x01\x00\x00": "TrueType/可能为索引表",
}


def entropy(data: bytes) -> float:
    if not data:
        return 0.0
    counts = [0] * 256
    for b in data:
        counts[b] += 1
    total = len(data)
    ent = 0.0
    for c in counts:
        if c:
            p = c / total
            ent -= p * math.log2(p)
    return ent


def guess(data: bytes) -> str:
    for magic, name in KNOWN_MAGICS.items():
        if data.startswith(magic):
            return name
    return "未知 (自定义格式?)"


def scan(path: str, min_size: int):
    rows = []
    for root, _dirs, files in os.walk(path):
        for name in files:
            fp = os.path.join(root, name)
            try:
                size = os.path.getsize(fp)
                if size < min_size:
                    continue
                with open(fp, "rb") as f:
                    head = f.read(16)
                    f.seek(0)
                    sample = f.read(min(size, 1 << 20))  # 采样前 1MB 算熵
                rows.append((fp, size, head, entropy(sample)))
            except OSError as e:
                print(f"[跳过] {fp}: {e}", file=sys.stderr)
    rows.sort(key=lambda r: -r[1])
    for fp, size, head, ent in rows:
        rel = os.path.relpath(fp, path)
        print(f"{rel:50s} {size:>12,}  熵={ent:5.2f}  "
              f"magic={head[:8].hex():16s}  {guess(head)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("directory")
    ap.add_argument("--min-size", type=int, default=1024)
    args = ap.parse_args()
    if not os.path.isdir(args.directory):
        sys.exit(f"目录不存在: {args.directory}")
    scan(args.directory, args.min_size)
