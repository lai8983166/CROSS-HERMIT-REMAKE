#!/usr/bin/env python3
"""对脱壳镜像做轻量 x86 分析, 不等 Ghidra:
1. 扫 .text 中 `call [imm32]` / `jmp [imm32]`, 对照符号表 → API 调用点
2. 线性扫 `call rel32` 收集函数入口
3. 归属: 每个调用点 → 所属函数 → 函数的 API 集合
4. 特殊: SetTimer/BeginPaint/CreateWindowExA 调用点往前找 push imm32 提取回调地址
"""
import json
import re
import struct

data = open("analysis/hermit_dump.exe", "rb").read()
syms = {int(a, 16): n for a, n in json.load(open("analysis/hermit_dump_symbols.json")).items()}

TEXT_OFF, TEXT_END = 0x1000, 0x192000
BASE = 0x400000


def va(off):
    return BASE + off


def off(va_):
    return va_ - BASE


# 1. 间接调用/跳转 [imm32] → API
api_sites = {}  # site_va -> api name
for m in re.finditer(rb"\xff[\x15\x25]", data[TEXT_OFF:TEXT_END]):
    o = TEXT_OFF + m.start()
    imm = struct.unpack_from("<I", data, o + 2)[0]
    if imm in syms:
        api_sites[va(o)] = syms[imm]
print(f"API 调用点: {len(api_sites)} 个")

# 2. call rel32 → 函数入口集合
funcs = set()
for m in re.finditer(rb"\xe8", data[TEXT_OFF:TEXT_END]):
    o = TEXT_OFF + m.start()
    rel = struct.unpack_from("<i", data, o + 1)[0]
    t = va(o) + 5 + rel
    if TEXT_OFF + BASE <= t < TEXT_END + BASE:
        funcs.add(t)
func_list = sorted(funcs)
print(f"函数入口候选: {len(func_list)} 个")

import bisect


def owner(site_va):
    i = bisect.bisect_right(func_list, site_va) - 1
    return func_list[i] if i >= 0 else 0


# 3. 函数 → API 集合
fapi = {}
for site, api in api_sites.items():
    fapi.setdefault(owner(site), set()).add(api)

# 4. 关键函数定位: 在调用点前 32B 内找 push imm32 回调参数
def pushes_before(site_va, span=40):
    o = off(site_va)
    out = []
    for k in range(o - 1, max(o - span, TEXT_OFF), -1):
        if data[k] == 0x68:  # push imm32
            imm = struct.unpack_from("<I", data, k + 1)[0]
            if TEXT_OFF + BASE <= imm < BASE + len(data) or imm in syms:
                out.append((va(k), imm))
    return out


print("\n== 关键回调提取 ==")
for api_key in ["USER32.dll!SetTimer", "USER32.dll!CreateWindowExA",
                "USER32.dll!RegisterClassA", "USER32.dll!GetMessageA",
                "USER32.dll!PeekMessageA", "USER32.dll!GetAsyncKeyState",
                "GDI32.dll!SelectObject", "GDI32.dll!DeleteDC"]:
    for site, api in sorted(api_sites.items()):
        if not api.endswith(api_key):
            continue
        ps = pushes_before(site)
        labeled = [(pv, syms.get(v, f"{v:#x}")) for pv, v in ps]
        print(f"{api_key.split('!')[1]:16s} 调用点 {site:#x} (函数 {owner(site):#x}) 参数: {labeled}")

print("\n== API 数最多的函数 TOP 15 ==")
for f, apis in sorted(fapi.items(), key=lambda kv: -len(kv[1]))[:15]:
    print(f"{f:#x} ({len(apis)} API): {', '.join(sorted(a.split('!')[1] for a in apis))}")

json.dump({f"{f:#x}": sorted(apis) for f, apis in fapi.items()},
          open("analysis/function_api_map.json", "w"), ensure_ascii=False, indent=1)
print("\n已写 analysis/function_api_map.json")
