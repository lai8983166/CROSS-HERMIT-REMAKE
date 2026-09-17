#!/usr/bin/env python3
"""从二进制文件中提取 Big5 繁体中文文本串，用于定位剧情/对话脚本数据。

用法:
    python tools/extract_big5.py <文件> [--min-len 4] [--offset]
光谱繁中版的剧本文本大概率是 Big5（或含 ASCII 混排）。
输出格式: `偏移  长度  文本`，偏移为十六进制，方便用十六进制编辑器跳转。
"""
import argparse
import sys


def is_big5_double(b0: int, b1: int) -> bool:
    """标准 Big5 高位字节 0x81-0xFE，低位 0x40-0x7E / 0xA1-0xFE。"""
    return 0x81 <= b0 <= 0xFE and (0x40 <= b1 <= 0x7E or 0xA1 <= b1 <= 0xFE)


def is_ascii(b: int) -> bool:
    return 0x20 <= b <= 0x7E


def decode_run(data: bytes) -> str | None:
    """把一段字节按 Big5+ASCII 尽力解码，失败返回 None。"""
    try:
        return data.decode("big5")
    except (UnicodeDecodeError, ValueError):
        return None


def extract(data: bytes, min_len: int):
    i, n = 0, len(data)
    while i < n:
        start = i
        # 尝试从当前位置开始收集一段连续的 Big5/ASCII 文本
        run = b""
        while i < n:
            b = data[i]
            if is_ascii(b):
                run += bytes([b])
                i += 1
            elif i + 1 < n and is_big5_double(b, data[i + 1]):
                run += bytes([b, data[i + 1]])
                i += 2
            else:
                break
        # 中文字符数需达到 min_len 才算有效命中（纯 ASCII 忽略）
        han = sum(1 for j in range(0, len(run), 1)
                  if j + 1 < len(run) and run[j] >= 0x81 and is_big5_double(run[j], run[j + 1])) // 2
        if han >= min_len:
            text = decode_run(run)
            if text:
                print(f"0x{start:08X}  {len(run):>5}  {text}")
        else:
            i = start + 1  # 前进一字节重试


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--min-len", type=int, default=4, help="最少中文字符数")
    args = ap.parse_args()
    try:
        with open(args.file, "rb") as f:
            extract(f.read(), args.min_len)
    except OSError as e:
        sys.exit(str(e))
