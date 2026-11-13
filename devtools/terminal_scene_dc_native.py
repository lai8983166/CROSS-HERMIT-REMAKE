"""Build the frozen scene owner with bounded, same-lane DC lifetime observations."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
from devtools import terminal_scene_native_extension as parent

ROOT=parent.ROOT
BUILD=ROOT/'.venv-audit/terminal-scene-dc-build-v1-20261113'
PARENT_SHA='0127f10f47abddc9dd429c5c208de9668529c277d944fc8889ef4a3ebf139b61'

OBSERVATION=r'''
struct DCObservation { U32 flush, type, typeError, font, fontError, count, countError; };
DCObservation observeDC(HDC dc) {
    const DWORD saved = GetLastError();
    DCObservation o{}; o.flush = GdiFlush();
    SetLastError(0); o.type = GetObjectType(dc); o.typeError = GetLastError();
    SetLastError(0); o.font = ptr(GetCurrentObject(dc, OBJ_FONT)); o.fontError = GetLastError();
    SetLastError(0); o.count = GetGuiResources(GetCurrentProcess(), GR_GDIOBJECTS); o.countError = GetLastError();
    SetLastError(saved); return o;
}
std::string dcFields(const char *prefix, const DCObservation &o) {
    const std::string p(prefix);
    return " " + p + "flush=" + number(o.flush) + " " + p + "type=" + number(o.type) +
        " " + p + "type_error=" + number(o.typeError) + " " + p + "font=" + number(o.font) +
        " " + p + "font_error=" + number(o.fontError) + " " + p + "gdi_count=" + number(o.count) +
        " " + p + "gdi_error=" + number(o.countError);
}
'''

LEAVES=r'''    } else if (q.op == "GetDC") {
        if (!args(1) || a[0] || !dcs.empty() || !retiredDCs.empty()) return reject("ONE_SCREEN_DC_LIFETIME_ONLY");
        const DWORD saved = GetLastError();
        SetLastError(0); const U32 baseline = GetGuiResources(GetCurrentProcess(), GR_GDIOBJECTS);
        const U32 baselineError = GetLastError(); SetLastError(saved);
        begin(); HDC dc = GetDC(nullptr); capture(); r.value = ptr(dc);
        if (dc) {
            dcs.emplace(r.value, DeviceContext{dc, q.lane, baseline, baselineError});
            const DCObservation live = observeDC(dc);
            r.extras = "baseline_gdi_count=" + number(baseline) + " baseline_gdi_error=" + number(baselineError) + dcFields("live_", live);
        }
    } else if (q.op == "DeleteDC") {
        if (!args(1)) return reject("ARGUMENTS");
        auto dc = dcs.find(a[0]);
        if (dc == dcs.end() || dc->second.lane != q.lane) return reject("DC_NOT_OWNED_BY_LANE");
        const DCObservation before = observeDC(dc->second.handle);
        begin(); r.value = DeleteDC(dc->second.handle); capture();
        const DCObservation after = observeDC(dc->second.handle);
        const bool retired = r.value && before.flush && before.type == OBJ_DC && before.font &&
            after.flush && !after.type && !after.font && !dc->second.baselineError &&
            !before.countError && !after.countError && after.count == dc->second.baseline;
        r.extras = "dc_retired=" + number(retired) + " baseline_gdi_count=" + number(dc->second.baseline) +
            " baseline_gdi_error=" + number(dc->second.baselineError) + dcFields("before_", before) + dcFields("after_", after);
        if (retired) { retiredDCs.emplace(a[0], dc->second); dcs.erase(dc); }
    } else if (q.op == "ReleaseDC") {
        if (!args(2) || a[0]) return reject("SCREEN_DC_ARGUMENTS");
        auto dc = dcs.find(a[1]);
        if (dc == dcs.end() || dc->second.lane != q.lane) return reject("DC_NOT_OWNED_BY_LANE");
        const DCObservation before = observeDC(dc->second.handle);
        begin(); r.value = static_cast<U32>(ReleaseDC(nullptr, dc->second.handle)); capture();
        const DCObservation after = observeDC(dc->second.handle);
        const bool retired = r.value && before.flush && before.type == OBJ_DC && before.font &&
            after.flush && !dc->second.baselineError && !after.countError && after.count == dc->second.baseline;
        r.extras = "dc_retired=" + number(retired) + " baseline_gdi_count=" + number(dc->second.baseline) +
            " baseline_gdi_error=" + number(dc->second.baselineError) + dcFields("before_", before) + dcFields("after_", after);
        if (retired) { retiredDCs.emplace(a[1], dc->second); dcs.erase(dc); }
    } else if (q.op == "DC_INFO") {
        if (!args(1)) return reject("ARGUMENTS");
        const bool retired = retiredDCs.count(a[0]) != 0;
        const auto &table = retired ? retiredDCs : dcs;
        const auto dc = table.find(a[0]);
        if (dc == table.end() || dc->second.lane != q.lane) return reject("DC_NOT_OBSERVED_BY_LANE");
        const DCObservation now = observeDC(dc->second.handle);
        r.value = 1; r.extras = "infrastructure=1 dc_retired=" + number(retired) +
            " baseline_gdi_count=" + number(dc->second.baseline) + " baseline_gdi_error=" + number(dc->second.baselineError) + dcFields("now_", now);
        r.error = savedError; SetLastError(savedError);
'''


def generated_source():
    parent.need(parent.identity(parent.__file__)['sha256']==PARENT_SHA,'frozen parent generator')
    source=parent.generated_source()
    source=parent.replace_once(source,'struct DeviceContext { HDC handle; U32 lane; };',
        'struct DeviceContext { HDC handle; U32 lane, baseline, baselineError; };')
    source=parent.replace_once(source,'std::map<U32, DeviceContext> dcs;',
        'std::map<U32, DeviceContext> dcs, retiredDCs;')
    source=parent.replace_once(source,'bool allocationInTls(const Allocation &a) {',OBSERVATION+'\nbool allocationInTls(const Allocation &a) {')
    start=source.index('    } else if (q.op == "GetDC") {')
    end=source.index('    } else if (q.op == "QueryPerformanceCounter"',start)
    source=source[:start]+LEAVES+source[end:]
    return source


def build(folder=BUILD):
    import pefile
    folder=Path(folder).resolve()
    parent.need(folder.is_relative_to(ROOT/'.venv-audit') and folder.drive.lower()=='f:' and not folder.exists(),'fresh F build')
    folder.mkdir(parents=True)
    source=folder/'terminal-scene-dc-owner.cpp';exe=folder/'terminal-scene-dc-owner.exe';obj=folder/'owner.obj'
    recipe=folder/'build.cmd';log=folder/'build.log'
    source.write_text(generated_source(),encoding='utf-8',newline='\n')
    vcvars=parent.VC/'Auxiliary/Build/vcvarsall.bat';compiler=parent.MSVC/'bin/Hostx64/x86/cl.exe';linker=parent.MSVC/'bin/Hostx64/x86/link.exe'
    recipe.write_text('\n'.join(['@echo off',f'call "{vcvars}" x86 {parent.SDK} -vcvars_ver=14.44 >nul',
        'if errorlevel 1 exit /b %errorlevel%',f'"{compiler}" /nologo /O2 /W4 /WX /MT /EHsc /std:c++17 /Fe:"{exe}" /Fo:"{obj}" "{source}" /link /SUBSYSTEM:WINDOWS /ENTRY:wmainCRTStartup gdi32.lib user32.lib shlwapi.lib','exit /b %errorlevel%'])+'\n',encoding='utf-8',newline='\r\n')
    env=dict(os.environ,TEMP=str(folder),TMP=str(folder))
    with log.open('wb') as stream:
        done=subprocess.run([env.get('COMSPEC','cmd.exe'),'/d','/c',str(recipe)],cwd=folder,env=env,
            stdout=stream,stderr=subprocess.STDOUT,timeout=90,creationflags=subprocess.CREATE_NO_WINDOW)
    parent.need(done.returncode==0,'warnings-as-errors build; inspect '+str(log))
    pe=pefile.PE(str(exe));imports={r.dll.decode().lower():[i.name.decode() for i in r.imports] for r in pe.DIRECTORY_ENTRY_IMPORT}
    parent.need(pe.FILE_HEADER.Machine==0x14c and pe.OPTIONAL_HEADER.Subsystem==2,'x86 no-console helper')
    parent.need(set(imports)=={'kernel32.dll','gdi32.dll','user32.dll','shlwapi.dll'},'bounded DLLs')
    parent.need(set(imports['user32.dll'])=={'GetDC','ReleaseDC','GetGuiResources'},'no window/input/display USER32 imports')
    parent.need(set(imports['gdi32.dll'])=={'CreateFontA','GetObjectA','DeleteObject','DeleteDC','GetObjectType','GetCurrentObject','GdiFlush'},'no pixel/display GDI32 imports')
    dependencies=[vcvars,compiler,linker,parent.KIT/f'Include/{parent.SDK}/um/Windows.h',parent.KIT/f'Include/{parent.SDK}/um/Shlwapi.h']
    dependencies += [parent.KIT/f'Lib/{parent.SDK}/um/x86/{n}.lib' for n in ('kernel32','gdi32','user32','shlwapi')]
    report=dict(kind='scene_DC_observer_build',native_executed=False,parent_generator=parent.identity(parent.__file__),
        base_source=parent.identity(parent.BASE_SOURCE),generator=parent.identity(__file__),generated_source=parent.identity(source),helper=parent.identity(exe),
        artifacts=[parent.identity(p) for p in (source,exe,obj,recipe,log)],dependencies=[parent.identity(p) for p in dependencies],imports=imports,
        observer_scope='Same-process/same-lane known screen DC only; handle metadata and current-process GDI count, no pixels or windows',
        original_DeleteDC_preserved=True,worker_TLS_dispatch_unchanged=True,LastError_preserved=True)
    (folder/'static-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--build-dir',default=str(BUILD));args=ap.parse_args()
    print(json.dumps(build(args.build_dir)['helper']))
