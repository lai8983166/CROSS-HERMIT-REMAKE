#!/usr/bin/env python3
"""运行时内存 dump: 把加壳的 CROSS HERMIT.EXE 从运行中的进程里解出完整镜像。

前提: 游戏已启动并进入标题/主菜单 (壳已解完 .text, 代码在内存中就位)
用法: python tools/unpack_dump.py [--pid PID] [--out analysis/hermit_dump.exe]
流程: 找进程 → 定位主模块基址 → 读 SizeOfImage 全镜像 → 重建 PE 节表
      (虚拟布局落地为文件布局) → 导出系统模块符号地址表供 Ghidra 贴标签
"""
import argparse
import ctypes
import ctypes.wintypes as wt
import json
import os
import struct
import sys

TARGET_NAMES = ("CROSS HERMIT.EXE", "CROSS HERMIT CHT.EXE")
TH32CS_SNAPPROCESS = 0x2
TH32CS_SNAPMODULE = 0x8
TH32CS_SNAPMODULE32 = 0x10
PROCESS_VM_READ = 0x10
PROCESS_QUERY_INFORMATION = 0x400

k32 = ctypes.WinDLL("kernel32", use_last_error=True)


class PROCESSENTRY32W(ctypes.Structure):
    _fields_ = [("dwSize", wt.DWORD), ("cntUsage", wt.DWORD),
                ("th32ProcessID", wt.DWORD), ("th32DefaultHeapID", ctypes.POINTER(wt.ULONG)),
                ("th32ModuleID", wt.DWORD), ("cntThreads", wt.DWORD),
                ("th32ParentProcessID", wt.DWORD), ("pcPriClassBase", ctypes.c_long),
                ("dwFlags", wt.DWORD), ("szExeFile", wt.WCHAR * 260)]


class MODULEENTRY32W(ctypes.Structure):
    _fields_ = [("dwSize", wt.DWORD), ("th32ModuleID", wt.DWORD), ("th32ProcessID", wt.DWORD),
                ("GlblcntUsage", wt.DWORD), ("ProccntUsage", wt.DWORD),
                ("modBaseAddr", ctypes.POINTER(ctypes.c_byte)), ("modBaseSize", wt.DWORD),
                ("hModule", wt.HMODULE), ("szModule", wt.WCHAR * 256),
                ("szExePath", wt.WCHAR * 260)]


def find_process():
    snap = k32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    entry = PROCESSENTRY32W(); entry.dwSize = ctypes.sizeof(entry)
    found = []
    ok = k32.Process32FirstW(snap, ctypes.byref(entry))
    while ok:
        name = entry.szExeFile
        if any(t.lower() == name.lower() for t in TARGET_NAMES):
            found.append((entry.th32ProcessID, name))
        ok = k32.Process32NextW(snap, ctypes.byref(entry))
    k32.CloseHandle(snap)
    return found


def list_modules(pid):
    """目标进程模块列表 [(名称, 基址, 大小)] — 64位Python枚举32位进程用 SNAPMODULE32"""
    snap = k32.CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, pid)
    if snap == -1 or snap == 0xFFFFFFFFFFFFFFFF:
        return None
    entry = MODULEENTRY32W(); entry.dwSize = ctypes.sizeof(entry)
    mods, ok = [], k32.Module32FirstW(snap, ctypes.byref(entry))
    while ok:
        # 指针必须在循环内立即取值: entry 缓冲区会被下次遍历复用
        base_addr = ctypes.cast(entry.modBaseAddr, ctypes.c_void_p).value
        mods.append((entry.szModule, base_addr, entry.modBaseSize))
        ok = k32.Module32NextW(snap, ctypes.byref(entry))
    k32.CloseHandle(snap)
    return mods


class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [("BaseAddress", ctypes.c_void_p), ("AllocationBase", ctypes.c_void_p),
                ("AllocationProtect", wt.DWORD), ("__a1", wt.DWORD),
                ("RegionSize", ctypes.c_size_t), ("State", wt.DWORD),
                ("Protect", wt.DWORD), ("Type", wt.DWORD), ("__a2", wt.DWORD)]


MEM_COMMIT = 0x1000
READABLE = {0x02, 0x04, 0x08, 0x20, 0x40, 0x80}  # READONLY/READWRITE/WRITECOPY/X_R/X_RW/X
PAGE_GUARD = 0x100


def read_image(hproc, base, size):
    """按区域遍历 [base, base+size): 可读页实读, 不可读页填零"""
    buf = (ctypes.c_char * size)()
    got = ctypes.c_size_t()
    pos, ok_bytes = 0, 0
    while pos < size:
        mbi = MEMORY_BASIC_INFORMATION()
        if k32.VirtualQueryEx(hproc, ctypes.c_void_p(base + pos), ctypes.byref(mbi),
                              ctypes.sizeof(mbi)) == 0:
            pos += 0x1000
            continue
        region = min(mbi.RegionSize, size - pos)
        readable = mbi.State == MEM_COMMIT and (mbi.Protect & PAGE_GUARD) == 0 \
            and (mbi.Protect & 0xFF) in READABLE
        if readable:
            r = 0
            while r < region:
                n = min(region - r, 0x100000)
                if k32.ReadProcessMemory(hproc, ctypes.c_void_p(base + pos + r),
                                         ctypes.byref(buf, pos + r), n, ctypes.byref(got)):
                    ok_bytes += got.value
                    r += got.value
                    if got.value < n:
                        break
                else:
                    break
        pos += region
    return buf, ok_bytes


def read_mem(hproc, addr, size):
    buf = (ctypes.c_char * size)()
    got = ctypes.c_size_t()
    pos = 0
    while pos < size:
        n = min(size - pos, 0x100000)
        if not k32.ReadProcessMemory(hproc, ctypes.c_void_p(addr + pos),
                                     ctypes.byref(buf, pos), n, ctypes.byref(got)) or got.value == 0:
            raise OSError(f"ReadProcessMemory 失败 @ {addr+pos:#x} (err={ctypes.get_last_error()})")
        pos += got.value
    return buf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pid", type=int)
    ap.add_argument("--out", default="analysis/hermit_dump.exe")
    args = ap.parse_args()

    procs = find_process()
    if not procs and not args.pid:
        sys.exit("未找到运行中的 CROSS HERMIT 进程 — 请先启动游戏到标题画面")
    pid = args.pid or procs[0][0]
    print(f"目标 PID {pid} ({procs[0][1] if procs else '指定'})")

    mods = list_modules(pid)
    if not mods:
        sys.exit("枚举模块失败")
    main_mod = next((m for m in mods if m[0].lower().endswith(".exe")
                     and m[1] and m[1] < 0x100000000), None)  # 主 exe 基址必在低 4GB (32位进程)
    base, imgsize = main_mod[1], main_mod[2]
    print(f"主模块 {main_mod[0]} 基址 {base:#x} 大小 {imgsize:#x}")

    hproc = k32.OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, pid)
    if not hproc:
        sys.exit(f"OpenProcess 失败 err={ctypes.get_last_error()}")

    # 校验基址: 头两个字节必须是 'MZ'
    probe = read_mem(hproc, base, 2)
    if probe[:2] != b"MZ":
        sys.exit(f"基址 {base:#x} 处不是 PE 头 (MZ 校验失败), 模块枚举异常")

    image, ok_bytes = read_image(hproc, base, imgsize)
    print(f"实读 {ok_bytes:,}B / {imgsize:,}B ({ok_bytes*100//imgsize}%), 其余为不可读区(填零)")
    image = bytearray(image)
    e_lfanew = struct.unpack_from("<I", image, 0x3C)[0]
    nsec = struct.unpack_from("<H", image, e_lfanew + 6)[0]
    opt_off = e_lfanew + 24
    sec_off = opt_off + struct.unpack_from("<H", image, e_lfanew + 20)[0]
    file_align = struct.unpack_from("<I", image, opt_off + 36)[0]
    print(f"PE: {nsec} 节, 文件对齐 {file_align:#x}")

    # 重建节表: 原始数据落盘 = 虚拟位置, 大小 = 虚拟大小
    for i in range(nsec):
        o = sec_off + i * 40
        name = image[o:o + 8].rstrip(b"\x00").decode(errors="replace")
        vsize, vaddr, rsize, roff = struct.unpack_from("<4I", image, o + 8)
        raw = min(vsize, imgsize - vaddr)
        pad = (-raw) % file_align
        image[o + 16:o + 24] = struct.pack("<II", vaddr, vaddr)  # raw size/off = virtual
        print(f"  {name:8s} va={vaddr:#010x} vsize={vsize:#8x} -> raw@{vaddr:#x} ({raw:#x}B)")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "wb") as f:
        f.write(image)
    print(f"已写出 {args.out} ({len(image):,}B)")

    # 系统模块导出符号表 (供 Ghidra 给 IAT 地址贴名字)
    syms = {}
    for mname, mbase, msize in mods:
        if mname == main_mod[0]:
            continue
        mb = mbase  # list_modules 已返回 int
        try:
            data = read_mem(hproc, mb, msize)
        except OSError:
            continue
        try:
            e = struct.unpack_from("<I", data, 0x3C)[0]
            exp_rva = struct.unpack_from("<I", data, e + 24 + 96)[0]  # 32位: 导出目录RVA
            if not exp_rva:
                continue
            nnames = struct.unpack_from("<I", data, exp_rva + 24)[0]
            aof, aon, aoa = struct.unpack_from("<3I", data, exp_rva + 28)
            funcs = struct.unpack_from(f"<{struct.unpack_from('<I', data, exp_rva+20)[0]}I", data, aoa)
            names = struct.unpack_from(f"<{nnames}I", data, aon)
            ords = struct.unpack_from(f"<{nnames}H", data, aof)
            for i in range(nnames):
                fname = data[names[i]:data.index(b"\x00", names[i])].decode(errors="replace")
                syms[f"{mb + funcs[ords[i]]:#x}"] = f"{mname[:-4]}!{fname}"
        except Exception:
            continue
    sym_path = args.out.rsplit(".", 1)[0] + "_symbols.json"
    json.dump(syms, open(sym_path, "w"))
    print(f"系统符号 {len(syms)} 条 -> {sym_path}")
    print("\n下一步: 用 analysis/ 下脚本跑 Ghidra headless 分析")


if __name__ == "__main__":
    main()
