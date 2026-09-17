#!/usr/bin/env python3
"""PyGhidra 全程序化分析 CROSS HERMIT 脱壳镜像:
1. 打开 analysis/hermit_game.exe, 全量自动分析 (首次约 10-40 分钟)
2. 给真 IAT (0x592000+, 249 槽) 建指针数据+标签
3. 按启发式地图重命名关键函数
4. 反编译重点函数 -> analysis/decomp/*.c
用法: python tools/ghidra_analyze.py [--all]   (--all 追加全函数反编译导出)
"""
import json
import os
import sys

os.environ.setdefault("GHIDRA_INSTALL_DIR", "F:/ghidra/ghidra_12.1.3_PUBLIC")
os.environ.setdefault("JAVA_HOME", "C:/Program Files/Microsoft/jdk-21.0.12.101-hotspot")

import pyghidra

pyghidra.start()
from ghidra.program.model.data import PointerDataType  # noqa: E402
from ghidra.program.model.symbol import SourceType  # noqa: E402
from ghidra.app.decompiler import DecompInterface  # noqa: E402
from ghidra.util.task import ConsoleTaskMonitor  # noqa: E402

EXE = os.path.abspath("analysis/hermit_game.exe")
PROJ = os.path.abspath("analysis/ghidra_proj")
KEY_FUNCS = {
    0x49DD70: "WinMain_message_loop",
    0x49E2B0: "game_tick_frame",
    0x49E850: "main_wndproc",
    0x424980: "wndproc_2",
    0x41B4A0: "dlg_proc_with_timer",
    0x423540: "create_game_window",
    0x450350: "create_window_2",
    0x424A90: "mdi_frame_proc",
    0x42B870: "imagelist_dragdrop",
    0x421850: "thread_sync_helper",
    0x423800: "blit_pipeline_A",
    0x405160: "text_render_A",
    0x406DF0: "text_render_B",
    0x4010D0: "text_render_font",
    0x4150E0: "timing_fn_A",
    0x415570: "timing_fn_B",
    0x415610: "timing_fn_C",
    0x415990: "timing_fn_D",
    0x415B40: "timing_fn_E",
    0x4170C0: "timing_fn_F",
    0x420210: "blit_0x420210",
    0x420610: "blit_0x420610",
    0x420760: "stretchblt_wrap",
    0x420830: "stretchblt_wrap2",
    0x422CD0: "blit_0x422cd0",
    0x422F20: "blit_0x422f20",
    0x423100: "blit_0x423100",
    0x424140: "blit_0x424140",
    0x411516: "input_poll_async_key",
    0x426820: "tick_0x426820",
    0x4551C0: "tick_0x4551c0",
}


def af(pgm, x):
    return pgm.getAddressFactory().getDefaultAddressSpace().getAddress(x)


def main():
    do_all = "--all" in sys.argv
    os.makedirs("analysis/decomp", exist_ok=True)
    with pyghidra.open_program(EXE, PROJ, "Hermit", analyze=True) as flat:
        pgm = flat.getCurrentProgram()
        tx = pgm.startTransaction("annotate")
        try:
            # 1) 真 IAT: 指针数据 + 标签
            iat = {int(k): v for k, v in json.load(open("analysis/hermit_real_iat.json")).items()}
            n_ok = 0
            for slot, name in sorted(iat.items()):
                a = af(pgm, slot)
                safe = "API_" + name.replace("!", "_").replace(".", "_")
                try:
                    flat.createData(a, PointerDataType.dataType)
                except Exception:
                    pass
                try:
                    flat.createLabel(a, safe, True)
                    flat.setEOLComment(a, name)
                    n_ok += 1
                except Exception:
                    pass
            print(f"IAT 标签 {n_ok}/{len(iat)}")

            # 2) 关键函数重命名
            fm = pgm.getFunctionManager()
            n_fn = 0
            for va, name in KEY_FUNCS.items():
                f = fm.getFunctionAt(af(pgm, va))
                if f is None:
                    f = flat.createFunction(af(pgm, va), name)
                if f is not None:
                    f.setName(name, SourceType.USER_DEFINED)
                    n_fn += 1
            print(f"关键函数命名 {n_fn}/{len(KEY_FUNCS)}")
        finally:
            pgm.endTransaction(tx, True)

        # 3) 反编译重点函数
        ifc = DecompInterface()
        ifc.openProgram(pgm)
        mon = ConsoleTaskMonitor()
        for va, name in KEY_FUNCS.items():
            f = fm.getFunctionAt(af(pgm, va))
            if f is None:
                continue
            res = ifc.decompileFunction(f, 120, mon)
            if res.decompileCompleted():
                c = res.getDecompiledFunction().getC()
                open(f"analysis/decomp/{name}_{va:x}.c", "w", encoding="utf-8", errors="replace").write(c)
                print(f"  反编译 {name} @ {va:#x} ({len(c)}B)")
            else:
                print(f"  失败 {name}: {res.getErrorMessage()}")

        # 4) 可选: 全函数反编译
        if do_all:
            os.makedirs("analysis/decomp_all", exist_ok=True)
            funcs = list(fm.getFunctions(True))
            print(f"全量反编译 {len(funcs)} 函数...")
            done = 0
            for i, f in enumerate(funcs):
                out = f"analysis/decomp_all/{f.getBody().getMinAddress().getOffset():x}.c"
                if os.path.exists(out):
                    continue
                try:
                    r = ifc.decompileFunction(f, 60, mon)
                    if r.decompileCompleted():
                        open(out, "w", encoding="utf-8", errors="replace").write(r.getDecompiledFunction().getC())
                except Exception as e:
                    print(f"  err {f.getName()}: {e}")
                done += 1
                if done % 200 == 0:
                    print(f"  进度 {i+1}/{len(funcs)}")
            print("全量反编译完成")
    print("完成")


if __name__ == "__main__":
    main()
