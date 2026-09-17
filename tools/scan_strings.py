#!/usr/bin/env python3
"""扫描 dump 的 ASCII 字符串, 按 PE 节归类, 抽取高价值情报 (路径/调试/引擎关键词)。"""
import re
import sys

data = open("analysis/hermit_dump.exe", "rb").read()
secs = {".text": (0x1000, 0x192000), ".rdata": (0x192000, 0x1ff000),
        ".data": (0x1ff000, 0x40c000), ".idata": (0x40c000, 0x40e000)}

hits = [(m.start(), m.group().decode()) for m in re.finditer(rb"[\x20-\x7e]{6,}", data)]
print(f"全文件 ASCII>=6 字符串: {len(hits)} 条")
for name, (a, b) in secs.items():
    print(f"  {name}: {sum(1 for off, _ in hits if a <= off < b)}")

print("\n.rdata 样本 (前 50 条):")
a, b = secs[".rdata"]
shown = 0
for off, s in hits:
    if a <= off < b and shown < 50:
        print(f"  {off:08x}: {s[:72]}")
        shown += 1

print("\n.data 样本 (前 30 条):")
a, b = secs[".data"]
shown = 0
for off, s in hits:
    if a <= off < b and shown < 30:
        print(f"  {off:08x}: {s[:72]}")
        shown += 1
