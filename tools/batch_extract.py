#!/usr/bin/env python3
"""批量提取 CROSS HERMIT 素材:
  1. ADV/BIN/*.BIN  -> extracted/img/<名>.png        (X1RGB555 渲染)
  2. 全部 *.YBC     -> extracted/text/<相对路径>.txt  (Big5 -> UTF-8, 带偏移)
  3. extracted/manifest.csv  全量文件清单 (路径/大小/类别)

用法: python tools/batch_extract.py [游戏DATA目录] (默认 CROSS HERMIT/CROSS HERMIT/DATA)
"""
import csv
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_dximg import render  # noqa: E402

GAME = sys.argv[1] if len(sys.argv) > 1 else "CROSS HERMIT/CROSS HERMIT/DATA"
OUT_IMG = "extracted/img"
OUT_TXT = "extracted/text"
SKIP_EXT = {".mp3", ".wav", ".bmp"}  # 标准格式, 留在原地不复制


def dump_ybc(src: str, dst: str):
    """YBC -> UTF-8 文本, 每行: 十六进制偏移 + 内容 (复用 extract_big5 逻辑)"""
    data = open(src, "rb").read()

    def is_b5(b0, b1):
        return 0x81 <= b0 <= 0xFE and (0x40 <= b1 <= 0x7E or 0xA1 <= b1 <= 0xFE)

    lines, i, n, last = [], 0, len(data), 0
    while i < n:
        start, run = i, b""
        while i < n:
            b = data[i]
            if 0x20 <= b <= 0x7E:
                run += bytes([b]); i += 1
            elif i + 1 < n and is_b5(b, data[i + 1]):
                run += bytes([b, data[i + 1]]); i += 2
            else:
                break
        han = sum(1 for j in range(len(run) - 1) if run[j] >= 0x81 and is_b5(run[j], run[j + 1])) // 2
        if han >= 2:
            try:
                lines.append(f"0x{start:06X}  {run.decode('big5')}")
                last = i
            except UnicodeDecodeError:
                pass
            continue
        i = start + 1
    open(dst, "w", encoding="utf-8").write("\n".join(lines))
    return len(lines)


def main():
    os.makedirs(OUT_IMG, exist_ok=True)
    ok_img = fail_img = ok_txt = 0
    manifest = []

    for root, _dirs, files in os.walk(GAME):
        for f in sorted(files):
            src = os.path.join(root, f)
            rel = os.path.relpath(src, GAME)
            ext = os.path.splitext(f)[1].lower()
            cat = {" .bin": "容器/图像", ".ybc": "YBC文本"}.get(ext, ext.strip(".").upper())
            manifest.append([rel, os.path.getsize(src), cat])

            if root.replace("/", os.sep).endswith("ADV\\BIN") and ext == ".bin":
                dst = os.path.join(OUT_IMG, f[:-4] + ".png")
                try:
                    render(src).save(dst, optimize=True)
                    ok_img += 1
                except (ValueError, OSError) as e:
                    print(f"[图跳过] {rel}: {e}")
                    fail_img += 1
            elif ext == ".ybc":
                dst = os.path.join(OUT_TXT, rel[:-4] + ".txt")
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                try:
                    dump_ybc(src, dst)
                    ok_txt += 1
                except OSError as e:
                    print(f"[文跳过] {rel}: {e}")

    with open("extracted/manifest.csv", "w", newline="", encoding="utf-8-sig") as fp:
        csv.writer(fp).writerows([["相对路径", "字节", "类别"]] + manifest)
    print(f"\n图像: 成功 {ok_img} / 跳过 {fail_img}")
    print(f"YBC 文本: 成功 {ok_txt}")
    print(f"清单: extracted/manifest.csv ({len(manifest)} 项)")


if __name__ == "__main__":
    main()
