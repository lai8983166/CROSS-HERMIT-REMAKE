#!/usr/bin/env python3
"""全量抓取: 游戏(含自调试保护的父子进程)的全部进程镜像 + 进程内所有可执行私有内存区。

背景: CROSS HERMIT.EXE 是保护壳 loader (自调试: 父进程调试子进程),
真游戏引擎在子进程或进程内模块外的私有可执行内存中。
用法: python tools/unpack_all.py   (游戏启动到标题画面后运行)
产出: analysis/pid<N>_main.exe          主模块镜像 (重建 PE)
      analysis/pid<N>_exec_<base>.bin   模块外可执行/可疑内存区
      analysis/pid<N>_mods.json         模块列表
"""
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
MEM_COMMIT = 0x1000
MEM_PRIVATE = 0x20000
PAGE_GUARD = 0x100
EXEC_PROTECT = {0x10, 0x20, 0x40, 0x80}  # EXECUTE / X_R / X_RW / X_WX
READABLE = {0x02, 0x04, 0x08, 0x20, 0x40, 0x80}

k32 = ctypes.WinDLL("kernel32", use_last_error=True)
k32.QueryFullProcessImageNameW.argtypes = [wt.HANDLE, wt.DWORD, wt.LPWSTR, ctypes.POINTER(wt.DWORD)]
GAME_DIR = r"f:\project\chaomofa\cross hermit"  # 进程路径前缀 (小写比较)


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


class MBI(ctypes.Structure):
    _fields_ = [("BaseAddress", ctypes.c_void_p), ("AllocationBase", ctypes.c_void_p),
                ("AllocationProtect", wt.DWORD), ("__a1", wt.DWORD),
                ("RegionSize", ctypes.c_size_t), ("State", wt.DWORD),
                ("Protect", wt.DWORD), ("Type", wt.DWORD), ("__a2", wt.DWORD)]


def find_processes():
    """枚举全部进程, 主模块路径在游戏目录内的一律收录 (防壳改名子进程)"""
    snap = k32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    e = PROCESSENTRY32W(); e.dwSize = ctypes.sizeof(e)
    out, ok = [], k32.Process32FirstW(snap, ctypes.byref(e))
    while ok:
        p = exe_path(e.th32ProcessID)
        if p and p.lower().startswith(GAME_DIR):
            out.append((e.th32ProcessID, e.th32ParentProcessID, p))
        ok = k32.Process32NextW(snap, ctypes.byref(e))
    k32.CloseHandle(snap)
    return out


def exe_path(pid):
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    h = k32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not h:
        return None
    buf = ctypes.create_unicode_buffer(520); sz = wt.DWORD(520)
    ok = k32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(sz))
    k32.CloseHandle(h)
    return buf.value if ok else None


def list_modules(pid):
    snap = k32.CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, pid)
    if snap in (-1, 0xFFFFFFFFFFFFFFFF):
        return []
    e = MODULEENTRY32W(); e.dwSize = ctypes.sizeof(e)
    mods, ok = [], k32.Module32FirstW(snap, ctypes.byref(e))
    while ok:
        base = ctypes.cast(e.modBaseAddr, ctypes.c_void_p).value
        mods.append((e.szModule, base, e.modBaseSize))
        ok = k32.Module32NextW(snap, ctypes.byref(e))
    k32.CloseHandle(snap)
    return mods


def read_range(hproc, addr, size):
    """读一段内存, 不可读页填零, 返回 (bytes, 实读字节数)"""
    buf = (ctypes.c_char * size)()
    got = ctypes.c_size_t()
    pos, ok_bytes = 0, 0
    while pos < size:
        mbi = MBI()
        if k32.VirtualQueryEx(hproc, ctypes.c_void_p(addr + pos), ctypes.byref(mbi), ctypes.sizeof(mbi)) == 0:
            pos += 0x1000
            continue
        region = min(mbi.RegionSize, size - pos)
        readable = mbi.State == MEM_COMMIT and (mbi.Protect & PAGE_GUARD) == 0 \
            and (mbi.Protect & 0xFF) in READABLE
        if readable:
            r = 0
            while r < region:
                n = min(region - r, 0x100000)
                if k32.ReadProcessMemory(hproc, ctypes.c_void_p(addr + pos + r),
                                         ctypes.byref(buf, pos + r), n, ctypes.byref(got)) and got.value:
                    ok_bytes += got.value
                    r += got.value
                else:
                    break
        pos += region
    return bytes(buf), ok_bytes


def dump_process(pid, ppid, name):
    print(f"\n===== PID {pid} ({name}) parent={ppid} =====")
    hproc = k32.OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, pid)
    if not hproc:
        print(f"  OpenProcess 失败 err={ctypes.get_last_error()}")
        return
    mods = list_modules(pid)
    if not mods:
        print("  模块枚举失败")
        return
    json.dump([[m[0], m[1], m[2]] for m in mods], open(f"analysis/pid{pid}_mods.json", "w"))
    main = next((m for m in mods if m[0].lower().endswith(".exe") and m[1] and m[1] < 0x100000000), None)
    if main:
        base, size = main[1], main[2]
        img, okb = read_range(hproc, base, size)
        open(f"analysis/pid{pid}_main.exe", "wb").write(img)
        print(f"  主模块 {base:#x}+{size:#x} 实读 {okb:,}B -> pid{pid}_main.exe")

    # 全地址空间扫可执行私有区域 (壳解密游戏代码的常见落脚点)
    seen_alloc = set()
    addr = 0x10000
    nfound = 0
    while addr < 0x7FFE0000:
        mbi = MBI()
        if k32.VirtualQueryEx(hproc, ctypes.c_void_p(addr), ctypes.byref(mbi), ctypes.sizeof(mbi)) == 0:
            addr += 0x10000
            continue
        region_base = mbi.BaseAddress or addr
        size = mbi.RegionSize
        alloc = mbi.AllocationBase or region_base
        is_exec = (mbi.Protect & 0xFF) in EXEC_PROTECT
        is_private = mbi.Type == MEM_PRIVATE
        in_module = any(m[1] and m[1] <= region_base < m[1] + m[2] for m in mods)
        if mbi.State == MEM_COMMIT and is_exec and is_private and not in_module \
                and alloc not in seen_alloc and size >= 0x1000:
            seen_alloc.add(alloc)
            alloc_size = size
            a = region_base
            # 把同一 allocation 的连续区域一并取
            data, okb = read_range(hproc, a, min(alloc_size, 0x2000000))
            mz = data[:2] == b"MZ"
            fn = f"analysis/pid{pid}_exec_{a:x}.bin"
            open(fn, "wb").write(data)
            nfound += 1
            print(f"  私有可执行区 {a:#x}+{size:#x} 实读 {okb:,}B {'[MZ!]' if mz else ''} -> {os.path.basename(fn)}")
        addr = region_base + size
    print(f"  模块外可执行区: {nfound} 个")
    k32.CloseHandle(hproc)


def main():
    os.makedirs("analysis", exist_ok=True)
    procs = find_processes()
    if not procs:
        sys.exit("未找到运行中的游戏进程 — 请先启动到标题画面")
    game_pids = {p[0] for p in procs}
    print(f"游戏相关进程: {[(p[0], os.path.basename(p[2])) for p in procs]}")
    for pid, ppid, name in procs:
        rel = "子进程(被调试?)" if ppid in game_pids else ("父进程(调试器?)" if any(p[1] == pid for p in procs) else "")
        print(f"  PID {pid} <- 父 {ppid} {rel}")
    for pid, ppid, name in procs:
        dump_process(pid, ppid, name)
    print("\n完成。真游戏 = 含 BitBlt/CreateDIBSection 导入或大代码量的那个。")


if __name__ == "__main__":
    main()
