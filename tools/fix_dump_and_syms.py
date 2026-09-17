#!/usr/bin/env python3
"""离线修复 dump 并解析 API 符号:
1. 修正节表 SizeOfRawData (= 对齐后的虚拟大小) — 此前误写为节偏移
2. 扫描镜像中所有落在系统 DLL 地址范围内的 DWORD, 用 SysWOW64 磁盘 DLL 的
   导出表离线解析成 `dll!name`, 产出 Ghidra 可用的符号 JSON
"""
import json
import os
import struct

DUMP = "analysis/hermit_dump.exe"
FILE_ALIGN = 0x1000

# 游戏运行时的系统模块基址 (来自 unpack_dump 枚举, 本次开机会话内有效)
MODULES = {
    "KERNEL32.DLL": (0x77000000, "KERNEL32.dll"),
    "KERNELBASE.dll": (0x76260000, "KernelBase.dll"),
    "msvcrt.dll": (0x76d70000, "msvcrt.dll"),
    "USER32.dll": (0x75fe0000, "USER32.dll"),
    "GDI32.dll": (0x76bd0000, "GDI32.dll"),
    "SHELL32.dll": (0x77390000, "SHELL32.dll"),
    "SHLWAPI.dll": (0x75800000, "SHLWAPI.dll"),
    "OLEAUT32.dll": (0x772f0000, "OLEAUT32.dll"),
    "RPCRT4.dll": (0x76e40000, "RPCRT4.dll"),
    "SETUPAPI.dll": (0x75a30000, "SETUPAPI.dll"),
    "WINSPOOL.DRV": (0x73ad0000, "WINSPOOL.DRV"),
    "IMM32.DLL": (0x76180000, "IMM32.DLL"),
    "combase.dll": (0x764e0000, "combase.dll"),
    "ucrtbase.dll": (0x771d0000, "ucrtbase.dll"),
    "win32u.dll": (0x76bb0000, "win32u.dll"),
    "gdi32full.dll": (0x769c0000, "gdi32full.dll"),
    "MSCTF.dll": (0x75f00000, "MSCTF.dll"),
    "sechost.dll": (0x76760000, "sechost.dll"),
    "bcrypt.dll": (0x761b0000, "bcrypt.dll"),
}


def fix_sections(data: bytearray):
    e = struct.unpack_from("<I", data, 0x3C)[0]
    nsec = struct.unpack_from("<H", data, e + 6)[0]
    secoff = e + 24 + struct.unpack_from("<H", data, e + 20)[0]
    total = len(data)
    for k in range(nsec):
        o = secoff + k * 40
        name = data[o:o + 8].rstrip(b"\x00").decode(errors="replace")
        vsize, vaddr = struct.unpack_from("<II", data, o + 8)
        raw = min((vsize + FILE_ALIGN - 1) & ~(FILE_ALIGN - 1), total - vaddr)
        struct.pack_into("<II", data, o + 16, raw, vaddr)  # SizeOfRawData, PointerToRawData
        print(f"  {name:8s} va={vaddr:#010x} rawsize修正={raw:#8x}")


def load_exports(dll_file: str):
    """从磁盘 PE 解析导出表: 返回 (rva->name, ordinal->name, 映像大小)"""
    data = open(os.path.join(r"C:\Windows\SysWOW64", dll_file), "rb").read()
    e = struct.unpack_from("<I", data, 0x3C)[0]
    opt = e + 24
    magic = struct.unpack_from("<H", data, opt)[0]
    if magic != 0x10B:
        return {}, {}, 0
    imgsize = struct.unpack_from("<I", data, opt + 56)[0]
    secoff = opt + struct.unpack_from("<H", data, e + 20)[0]
    nsec = struct.unpack_from("<H", data, e + 6)[0]
    secs = []
    for k in range(nsec):
        o = secoff + k * 40
        vsize, vaddr, rsize, roff = struct.unpack_from("<4I", data, o + 8)
        secs.append((vaddr, vsize, roff, rsize))

    def r2o(rva):
        for va, vs, ro, rs in secs:
            if va <= rva < va + max(vs, rs):
                return ro + (rva - va)
        return None

    exp_rva = struct.unpack_from("<I", data, opt + 96)[0]
    if not exp_rva:
        return {}, {}, imgsize
    eo = r2o(exp_rva)
    nfunc, nnames = struct.unpack_from("<II", data, eo + 20)
    aof, aon, aoord = struct.unpack_from("<3I", data, eo + 28)
    funcs = struct.unpack_from(f"<{nfunc}I", data, r2o(aof))
    names = struct.unpack_from(f"<{nnames}I", data, r2o(aon))
    ords = struct.unpack_from(f"<{nnames}H", data, r2o(aoord))
    by_rva, by_ord = {}, {}
    for i in range(nnames):
        no = r2o(names[i])
        name = data[no:data.index(b"\x00", no)].decode(errors="replace")
        fn_rva = funcs[ords[i]]
        by_rva[fn_rva] = name
        by_ord[ords[i] + 1] = name  # 导出序号从 1 起
    return by_rva, by_ord, imgsize


def main():
    data = bytearray(open(DUMP, "rb").read())
    print("== 修正节表 ==")
    fix_sections(data)
    open(DUMP, "wb").write(data)

    print("\n== 解析系统 DLL 导出表 ==")
    ranges = []  # (base, end, by_rva, by_ord, dll)
    for mod, (base, dll) in MODULES.items():
        try:
            by_rva, by_ord, imgsize = load_exports(dll)
        except OSError as ex:
            print(f"  {dll}: 读取失败 {ex}")
            continue
        if not by_rva:
            continue
        ranges.append((base, base + imgsize, by_rva, by_ord, dll))
        print(f"  {dll:16s} @{base:#x}..{base+imgsize:#x} 导出 {len(by_rva)} 个")
    ranges.sort()

    print("\n== 扫描镜像中的 API 地址 ==")
    syms = {}
    for off in range(0, len(data) - 4, 4):
        v = struct.unpack_from("<I", data, off)[0]
        for base, end, by_rva, by_ord, dll in ranges:
            if not base <= v < end:
                continue
            rva = v - base
            name = by_rva.get(rva) or by_ord.get(rva // 4 + 1) or f"{dll}+{rva:#x}"
            syms[f"{v:#x}"] = f"{dll}!{name}"
            break
    out = "analysis/hermit_dump_symbols.json"
    json.dump(syms, open(out, "w"), ensure_ascii=False, indent=0)
    print(f"标注 {len(syms)} 个地址 -> {out}")
    top = [s for s in syms.values() if "!" in s][:12]
    for t in top:
        print("  ", t)


if __name__ == "__main__":
    main()
