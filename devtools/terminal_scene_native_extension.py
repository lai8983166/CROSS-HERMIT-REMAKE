"""Build, never execute, the bounded scene-resource extension of the frozen owner.

The existing worker, TLS, queue and pointer projection remain byte-identical
within the generated source. Only owned font/string leaves and stated bounds
are added. Compilation is not native qualification or scene acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE_SOURCE = ROOT / "devtools/terminal_native_owner.cpp"
BASE_SHA256 = "a77132eae20424f1e6fc5eb6e792de5c41b018e787cedbcda6cb975b2435be43"
BUILD = ROOT / ".venv-audit/terminal-scene-owner-build-v3-20261113"
VC = Path("C:/Program Files/Microsoft Visual Studio/2022/Community/VC")
MSVC = VC / "Tools/MSVC/14.44.35207"
KIT = Path("C:/Program Files (x86)/Windows Kits/10")
SDK = "10.0.26100.0"

STRING_HELPER = r'''
// The dispatch state lock remains held while bounded strings are inspected.
bool ownedCString(U32 address, U32 &length) {
    Allocation *a = ownedRange(address, 1);
    if (!a) return false;
    const U32 available = std::min<U32>(260, a->size - (address - a->base));
    if (overlapsCritical(address, available)) return false;
    const auto *s = static_cast<const unsigned char *>(pointer(address));
    for (U32 i = 0; i < available; ++i) {
        if (!s[i]) { length = i; return true; }
    }
    return false;
}
bool overlap(U32 a, U32 an, U32 b, U32 bn) {
    return a < static_cast<uint64_t>(b) + bn && b < static_cast<uint64_t>(a) + an;
}
'''

LEAVES = r'''
    if (q.op == "CreateFontA") {
        U32 faceLength = 0;
        if (!args(14) || fonts.size() >= 16 || !ownedCString(a[13], faceLength))
            return reject("FONT_ARGUMENTS_OR_OWNERSHIP");
        begin(); HFONT h = CreateFontA(static_cast<int>(a[0]), static_cast<int>(a[1]),
            static_cast<int>(a[2]), static_cast<int>(a[3]), static_cast<int>(a[4]),
            a[5], a[6], a[7], a[8], a[9], a[10], a[11], a[12],
            static_cast<LPCSTR>(pointer(a[13]))); capture(); r.value = ptr(h);
        if (h) { fonts.emplace(r.value, h); retiredFonts.erase(r.value); }
    } else if (q.op == "DeleteObject") {
        if (!args(1)) return reject("ARGUMENTS");
        auto f = fonts.find(a[0]);
        if (f == fonts.end()) return reject("FONT_NOT_OWNED");
        begin(); r.value = DeleteObject(f->second); capture();
        if (r.value) { retiredFonts.emplace(a[0], true); fonts.erase(f); }
    } else if (q.op == "FONT_INFO") {
        if (!args(1) || (!fonts.count(a[0]) && !retiredFonts.count(a[0])))
            return reject("FONT_NOT_OBSERVED");
        static_assert(sizeof(LOGFONTA) == 60, "original LOGFONTA extent");
        std::array<unsigned char, 60> data; data.fill(0xa5);
        begin(); const int count = GetObjectA(handle(a[0]), static_cast<int>(data.size()), data.data()); capture();
        r.value = static_cast<U32>(count);
        r.extras = "infrastructure=1 native_last_error=" + number(r.error) +
            " live=" + number(fonts.count(a[0]) != 0) + " hex=" + encodeHex(data.data(), 60);
        r.error = savedError; SetLastError(savedError);
    } else if (q.op == "GetDC") {
        if (!args(1) || a[0] || !dcs.empty()) return reject("ONE_SCREEN_DC_ONLY");
        begin(); HDC dc = GetDC(nullptr); capture(); r.value = ptr(dc);
        if (dc) dcs.emplace(r.value, DeviceContext{dc, q.lane});
    } else if (q.op == "DeleteDC") {
        if (!args(1)) return reject("ARGUMENTS");
        auto dc = dcs.find(a[0]);
        if (dc == dcs.end() || dc->second.lane != q.lane) return reject("DC_NOT_OWNED_BY_LANE");
        // The original destructor calls DeleteDC on its GetDC result. Preserve
        // the real return; that call is not the GetDC/ReleaseDC ownership pair.
        begin(); r.value = DeleteDC(dc->second.handle); capture();
        r.extras = "getdc_release_still_required=1";
    } else if (q.op == "ReleaseDC") {
        if (!args(2) || a[0]) return reject("SCREEN_DC_ARGUMENTS");
        auto dc = dcs.find(a[1]);
        if (dc == dcs.end() || dc->second.lane != q.lane) return reject("DC_NOT_OWNED_BY_LANE");
        begin(); r.value = static_cast<U32>(ReleaseDC(nullptr, dc->second.handle)); capture();
        if (r.value) dcs.erase(dc);
    } else if (q.op == "QueryPerformanceCounter" || q.op == "QueryPerformanceFrequency") {
        if (!args(1) || !ownedRange(a[0], 8) || overlapsCritical(a[0], 8))
            return reject("PERFORMANCE_OUTPUT_RANGE");
        static_assert(sizeof(LARGE_INTEGER) == 8, "original counter extent");
        begin(); r.value = q.op == "QueryPerformanceCounter" ?
            QueryPerformanceCounter(static_cast<LARGE_INTEGER *>(pointer(a[0]))) :
            QueryPerformanceFrequency(static_cast<LARGE_INTEGER *>(pointer(a[0]))); capture();
    } else if (q.op == "GetLocalTime" || q.op == "GetSystemTime" || q.op == "GetTimeZoneInformation") {
        const U32 size = q.op == "GetTimeZoneInformation" ? sizeof(TIME_ZONE_INFORMATION) : sizeof(SYSTEMTIME);
        static_assert(sizeof(SYSTEMTIME) == 16 && sizeof(TIME_ZONE_INFORMATION) == 172, "original time extents");
        if (!args(1) || !ownedRange(a[0], size) || overlapsCritical(a[0], size))
            return reject("TIME_OUTPUT_RANGE");
        begin();
        if (q.op == "GetTimeZoneInformation") {
            r.value = GetTimeZoneInformation(static_cast<LPTIME_ZONE_INFORMATION>(pointer(a[0])));
        } else if (q.op == "GetLocalTime") {
            GetLocalTime(static_cast<LPSYSTEMTIME>(pointer(a[0]))); r.extras = "void=1";
        } else {
            GetSystemTime(static_cast<LPSYSTEMTIME>(pointer(a[0]))); r.extras = "void=1";
        }
        capture();
    } else if (q.op == "WideCharToMultiByte") {
        if (!args(8) || a[6] || a[5] > 4096 || !a[3] ||
            (a[3] != UINT32_MAX && a[3] > 512)) return reject("WIDE_CONVERSION_ARGUMENTS");
        U32 inputUnits = a[3];
        if (inputUnits == UINT32_MAX) {
            inputUnits = 0;
            for (U32 i = 0; i < 512; ++i) {
                const uint64_t at = static_cast<uint64_t>(a[2]) + static_cast<uint64_t>(i) * sizeof(WCHAR);
                if (at > UINT32_MAX || !ownedRange(static_cast<U32>(at), sizeof(WCHAR)) ||
                    overlapsCritical(static_cast<U32>(at), sizeof(WCHAR))) return reject("WIDE_INPUT_RANGE");
                WCHAR ch = 0; memcpy(&ch, pointer(static_cast<U32>(at)), sizeof(ch));
                if (!ch) { inputUnits = i + 1; break; }
            }
            if (!inputUnits) return reject("WIDE_INPUT_TERMINATOR");
        }
        const U32 inputBytes = inputUnits * sizeof(WCHAR);
        if (!ownedRange(a[2], inputBytes) || overlapsCritical(a[2], inputBytes))
            return reject("WIDE_INPUT_RANGE");
        if (a[5]) {
            if (!ownedRange(a[4], a[5]) || overlapsCritical(a[4], a[5]) ||
                overlap(a[2], inputBytes, a[4], a[5])) return reject("WIDE_OUTPUT_RANGE");
        } else if (a[4] && (!ownedRange(a[4], 1) || overlapsCritical(a[4], 1))) {
            return reject("WIDE_QUERY_POINTER");
        }
        static_assert(sizeof(BOOL) == 4, "original used-default output extent");
        if (a[7] && (!ownedRange(a[7], sizeof(BOOL)) || overlapsCritical(a[7], sizeof(BOOL)) ||
            overlap(a[2], inputBytes, a[7], sizeof(BOOL)) ||
            (a[5] && overlap(a[4], a[5], a[7], sizeof(BOOL)))))
            return reject("WIDE_USED_DEFAULT_RANGE");
        begin(); r.value = static_cast<U32>(WideCharToMultiByte(a[0], a[1],
            static_cast<LPCWCH>(pointer(a[2])), static_cast<int>(a[3]),
            static_cast<LPSTR>(pointer(a[4])), static_cast<int>(a[5]), nullptr,
            static_cast<LPBOOL>(pointer(a[7])))); capture();
        if (a[7]) r.extras = "used_default_hex=" + encodeHex(pointer(a[7]), sizeof(BOOL));
    } else if (q.op == "PathAddBackslashA") {
        U32 length = 0;
        if (!args(1) || !ownedRange(a[0], 260) || overlapsCritical(a[0], 260) ||
            !ownedCString(a[0], length)) return reject("PATH_RANGE");
        auto *s = static_cast<LPSTR>(pointer(a[0]));
        const U32 extra = length && s[length - 1] != '\\' ? 1 : 0;
        if (length + extra + 1 > 260) return reject("PATH_CAPACITY");
        begin(); r.value = ptr(PathAddBackslashA(s)); capture();
    } else if (q.op == "lstrcpyA" || q.op == "lstrcatA") {
        U32 sourceLength = 0, destinationLength = 0;
        if (!args(2) || !ownedRange(a[0], 260) || overlapsCritical(a[0], 260) ||
            !ownedCString(a[1], sourceLength)) return reject("STRING_RANGE");
        if (q.op == "lstrcatA" && !ownedCString(a[0], destinationLength))
            return reject("STRING_DESTINATION");
        const U32 resultBytes = destinationLength + sourceLength + 1;
        if (resultBytes > 260 || overlap(a[0], resultBytes, a[1], sourceLength + 1))
            return reject("STRING_CAPACITY_OR_OVERLAP");
        begin(); r.value = ptr(q.op == "lstrcpyA" ?
            lstrcpyA(static_cast<LPSTR>(pointer(a[0])), static_cast<LPCSTR>(pointer(a[1]))) :
            lstrcatA(static_cast<LPSTR>(pointer(a[0])), static_cast<LPCSTR>(pointer(a[1])))); capture();
    } else '''


def need(value, reason):
    if not value:
        raise ValueError(reason)


def identity(path):
    path = Path(path).resolve()
    raw = path.read_bytes()
    return dict(path=path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.as_posix(),
                bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def replace_once(text, before, after):
    need(text.count(before) == 1, "frozen source anchor must occur once: " + before[:80])
    return text.replace(before, after, 1)


def generated_source():
    raw = BASE_SOURCE.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == BASE_SHA256, "frozen owner source identity")
    source = raw.decode("utf-8")
    edits = [
        ("#include <windows.h>", "#include <windows.h>\n#include <shlwapi.h>"),
        ("constexpr U32 kMaxBlock = 1u << 20;", "constexpr U32 kMaxBlock = 2u << 20;"),
        ("std::map<U32, Tls> tlsSlots;", "std::map<U32, Tls> tlsSlots;\nstd::map<U32, HFONT> fonts;\nstd::map<U32, bool> retiredFonts;\nstruct DeviceContext { HDC handle; U32 lane; };\nstd::map<U32, DeviceContext> dcs;"),
        ("bool allocationInTls(const Allocation &a) {", STRING_HELPER + "\nbool allocationInTls(const Allocation &a) {"),
        ('    if (q.op == "GetCurrentThreadId") {', LEAVES + 'if (q.op == "GetCurrentThreadId") {'),
        ('" heaps=" + number(static_cast<U32>(heaps.size()))', '" dcs=" + number(static_cast<U32>(dcs.size())) + " fonts=" + number(static_cast<U32>(fonts.size())) + " retired_fonts=" + number(static_cast<U32>(retiredFonts.size())) +\n            " heaps=" + number(static_cast<U32>(heaps.size()))'),
        ('if (!allocations.empty() || !heaps.empty() || !handles.empty() || !criticals.empty() || !tlsSlots.empty() ||',
         'if (!dcs.empty() || !fonts.empty() || !allocations.empty() || !heaps.empty() || !handles.empty() || !criticals.empty() || !tlsSlots.empty() ||'),
        ('if (q.args.size() == 8) fatal(83);', 'if (q.args.size() == 16) fatal(83);'),
        ('if (!args(2) || !a[1] || a[1] > kMaxTransfer || !ownedRange(a[0], a[1]) || overlapsCritical(a[0], a[1]))\n            return reject("POINTER_PROBE_NOT_OWNED");',
         'if (!args(2) || !a[1] || a[1] > kMaxBlock || !ownedRange(a[0], a[1]) || overlapsCritical(a[0], a[1]))\n            return reject("POINTER_PROBE_NOT_OWNED");'),
        ('// No console, GUI, arbitrary process attachment, file, desktop or input APIs.',
         '// No console/window/input operations or pixel access. Owned DC/font resources are explicitly tracked.'),
    ]
    for before, after in edits:
        source = replace_once(source, before, after)
    need("constexpr U32 kMaxTransfer = 32768;" in source and "constexpr U32 kMaxMemory = 4u << 20;" in source,
         "unchanged wire transfer and total memory limits")
    return source


def build(folder=BUILD):
    import pefile
    folder = Path(folder).resolve()
    need(folder.is_relative_to(ROOT / ".venv-audit") and folder.drive.lower() == "f:", "F evidence directory only")
    need(not folder.exists(), "fresh immutable scene owner build directory")
    folder.mkdir(parents=True)
    source = folder / "terminal-scene-owner.cpp"
    exe, obj = folder / "terminal-scene-owner.exe", folder / "owner.obj"
    recipe, log = folder / "build.cmd", folder / "build.log"
    source.write_text(generated_source(), encoding="utf-8", newline="\n")
    vcvars = VC / "Auxiliary/Build/vcvarsall.bat"
    compiler = MSVC / "bin/Hostx64/x86/cl.exe"
    linker = MSVC / "bin/Hostx64/x86/link.exe"
    lines = ["@echo off", f'call "{vcvars}" x86 {SDK} -vcvars_ver=14.44 >nul',
             "if errorlevel 1 exit /b %errorlevel%",
             f'"{compiler}" /nologo /O2 /W4 /WX /MT /EHsc /std:c++17 /Fe:"{exe}" /Fo:"{obj}" "{source}" /link /SUBSYSTEM:WINDOWS /ENTRY:wmainCRTStartup gdi32.lib user32.lib shlwapi.lib',
             "exit /b %errorlevel%"]
    recipe.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\r\n")
    env = dict(os.environ, TEMP=str(folder), TMP=str(folder))
    with log.open("wb") as stream:
        result = subprocess.run([env.get("COMSPEC", "cmd.exe"), "/d", "/c", str(recipe)], cwd=folder,
                                env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=90,
                                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    need(result.returncode == 0, "warnings-as-errors compile failed; inspect " + str(log))
    pe = pefile.PE(str(exe))
    imports = {r.dll.decode("ascii"): [i.name.decode("ascii") if i.name else f"ordinal:{i.ordinal}" for i in r.imports]
               for r in pe.DIRECTORY_ENTRY_IMPORT}
    need(pe.FILE_HEADER.Machine == 0x14c and pe.OPTIONAL_HEADER.Subsystem == 2, "x86 Windows subsystem")
    need({n.lower() for n in imports} == {"kernel32.dll", "gdi32.dll", "user32.dll", "shlwapi.dll"}, "exact imported DLLs")
    need(set(next(v for n, v in imports.items() if n.lower() == "user32.dll")) == {"GetDC", "ReleaseDC"},
         "USER32 imports limited to screen DC acquisition and release")
    names = {i for row in imports.values() for i in row}
    need({"CreateFontA", "GetObjectA", "DeleteObject", "DeleteDC", "PathAddBackslashA", "lstrcpyA", "lstrcatA",
          "GetLocalTime", "GetSystemTime", "GetTimeZoneInformation", "WideCharToMultiByte", "GetDC", "ReleaseDC",
          "QueryPerformanceCounter", "QueryPerformanceFrequency"} <= names,
         "real required resource/string API imports")
    dependencies = [vcvars, compiler, linker, KIT / f"Include/{SDK}/um/Windows.h", KIT / f"Include/{SDK}/um/Shlwapi.h"]
    dependencies += [KIT / f"Lib/{SDK}/um/x86/{n}.lib" for n in ("kernel32", "gdi32", "user32", "shlwapi")]
    report = dict(kind="terminal_scene_owner_static_build_only", native_executed=False, accepted=False,
        base_source=identity(BASE_SOURCE), generator=identity(__file__), generated_source=identity(source), helper=identity(exe),
        machine=pe.FILE_HEADER.Machine, subsystem=pe.OPTIONAL_HEADER.Subsystem, imports=imports,
        dependencies=[identity(p) for p in dependencies],
        artifacts=[identity(p) for p in (source, exe, obj, recipe, log)],
        limits=dict(block_bytes=2 << 20, total_memory_bytes=4 << 20, transfer_bytes=32768, arguments=16,
                    simultaneous_fonts=16, simultaneous_screen_DCs=1, string_bytes=260,
                    wide_input_units=512, multibyte_output_bytes=4096, used_default_output_bytes=4),
        validation=["frozen_base_hash", "exact_generation_anchors", "warnings_as_errors", "x86_windows_subsystem",
                    "exact_import_DLLs", "owned_font_and_string_leaves", "FONT_INFO_preserves_lane_LastError",
                    "Shutdown_rejects_live_fonts_and_DCs", "same_lane_DC_release", "worker_TLS_dispatch_source_preserved"],
        limitations=["Built only; no helper process or game executed", "No scene construction or wait acceptance",
                     "GDI may load process dependencies; no window/input API is called by this extension",
                     "FONT_INFO accepts only this owner's live or successfully deleted HFONT identities"])
    report["artifact_bytes_before_report"] = sum(p.stat().st_size for p in folder.iterdir() if p.is_file())
    (folder / "static-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", default=str(BUILD))
    args = parser.parse_args()
    report = build(args.build_dir)
    print(json.dumps(dict(helper=report["helper"], native_executed=False, accepted=False)))
