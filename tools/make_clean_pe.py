#!/usr/bin/env python3
"""把子进程 dump (pid34888_main.exe) 重建成 Ghidra 可用的干净 PE:
- 镜像基址改为实际加载地址 0x400000
- 节表修正: PointerToRawData=RVA, SizeOfRawData=对齐 VS
- 解析导入描述符 → IAT 槽位名表 (RVA 0x46e000, 3 DLL)
产出: analysis/hermit_game.exe + analysis/hermit_game_iat.json
"""
import json
import struct

SRC = "analysis/pid34888_main.exe"
OUT = "analysis/hermit_game.exe"
BASE = 0x400000
FILE_ALIGN = 0x1000

data = bytearray(open(SRC, "rb").read())
e = struct.unpack_from("<I", data, 0x3C)[0]
opt = e + 24
nsec = struct.unpack_from("<H", data, e + 6)[0]
secoff = opt + struct.unpack_from("<H", data, e + 20)[0]
struct.pack_into("<I", data, opt + 28, BASE)  # ImageBase = 实际加载地址

print("== 修正节表 ==")
for k in range(nsec):
    o = secoff + k * 40
    nm = data[o:o + 8].rstrip(b"\x00").decode(errors="replace")
    vs, va = struct.unpack_from("<II", data, o + 8)
    raw = min((vs + FILE_ALIGN - 1) & ~(FILE_ALIGN - 1), len(data) - va)
    struct.pack_into("<II", data, o + 16, raw, va)
    print(f"  {nm:8s} VA={va:#010x} VS={vs:#8x} raw={va:#x}+{raw:#x}")

open(OUT, "wb").write(data)
print(f"已写 {OUT}")

# ---- 导入描述符 → IAT 槽名 (文件偏移 == RVA, raw=va 映射) ----
ddoff = opt + 96
imp_rva = struct.unpack_from("<I", data, ddoff + 8)[0]
iat = {}  # rva -> "dll!name"
o = imp_rva
while True:
    oft, t, fc, nmRVA, fthunk = struct.unpack_from("<5I", data, o)
    if not any((oft, t, fc, nmRVA, fthunk)):
        break
    dll = data[nmRVA:data.index(b"\x00", nmRVA)].decode(errors="replace")
    thunk = oft or fthunk
    k = 0
    while True:
        v = struct.unpack_from("<I", data, thunk + k * 4)[0]
        if v == 0:
            break
        if v & 0x80000000:  # 序号导入
            name = f"Ordinal_{v & 0xFFFF}"
        else:
            no = v + 2
            name = data[no:data.index(b"\x00", no)].decode(errors="replace")
        iat[fthunk + k * 4] = f"{dll[:-4]}!{name}" if dll.lower().endswith(".dll") else f"{dll}!{name}"
        k += 1
    o += 20
json.dump(iat, open("analysis/hermit_game_iat.json", "w"), ensure_ascii=False, indent=1)
from collections import Counter
c = Counter(v.split("!")[0] for v in iat.values())
print(f"\nIAT 槽位 {len(iat)} 个: {dict(c)}")
gs = [n for n in iat.values() if any(x in n for x in ("BitBlt", "DIB", "Stretch", "Palette", "Tick", "Timer", "Key"))]
print("渲染/计时相关:")
for g in sorted(gs):
    print(f"  {g}")
