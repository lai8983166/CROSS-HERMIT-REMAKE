"""Build-only D3D8 adapter0 to actual Win32 display binding; no launcher."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
from devtools import terminal_texture_native as parent

ROOT=parent.ROOT
INCLUDE=ROOT/'devtools/terminal_display_native.inc'
need,identity,replace=parent.need,parent.identity,parent.replace
PARENT_SHA='96439bf36446a0d61bd197cd7958dca6014398a45130b67b7134accf031e2cde'
PARENT_INCLUDE_SHA='e56d91be68516be5084757c71ed500c2d9adfec64aa7d136e389fcc5160499b6'
OPS={'DISPLAY_BIND':3,'DISPLAY_STATE':2}
BLOB_BYTES=16204

def source():
    need(identity(parent.__file__)['sha256']==PARENT_SHA and identity(parent.INCLUDE)['sha256']==PARENT_INCLUDE_SHA,'frozen texture native parent')
    s=parent.source()
    # The complete recorded original route sends 21,654,756 bytes, crossing the
    # old total cap during cleanup. Per-line/block/queue limits stay unchanged.
    s=replace(s,'constexpr uint64_t kMaxInput = 16u << 20;','constexpr uint64_t kMaxInput = 32u << 20;')
    s=replace(s,'U32 windowGuestOwner = 0, windowParentRequest = 0, callbackSequence = 0;',
        'U32 windowGuestOwner = 0, windowParentRequest = 0, callbackSequence = 0;\nU32 displayWindowGeneration=0;')
    s=replace(s,'if (creatingWindow && !ownedWindow) ownedWindow = hwnd;',
        'if (creatingWindow && !ownedWindow) { ownedWindow = hwnd; ++displayWindowGeneration; }')
    s=replace(s,'r.extras = "callbacks=" + number(callbackSequence) + " guest_owner="',
        'r.extras = "window_generation="+number(displayWindowGeneration)+" callbacks=" + number(callbackSequence) + " guest_owner="')
    s=replace(s,'" quit_posted="+number(windowQuitPosted)+" property_removed="+number(windowPropertyRemoved);',
        '" quit_posted="+number(windowQuitPosted)+" property_removed="+number(windowPropertyRemoved)+" window_generation="+number(displayWindowGeneration);')
    s=replace(s,'Result dispatch(const Request &q) {',INCLUDE.read_text(encoding='utf8')+'\nResult dispatch(const Request &q) {')
    s=replace(s,'    if (q.op == "TEX_VERIFY") return textureVerify(q, guard, savedError);',
        '    if (q.op == "DISPLAY_BIND" || q.op == "DISPLAY_STATE") return displaySnapshot(q,guard,savedError);\n    if (q.op == "TEX_VERIFY") return textureVerify(q, guard, savedError);')
    s=replace(s,'    if (gfxOp(q.op)) return gfxDispatch(q, guard, savedError);',
        '    if (gfxOp(q.op)) return displayGraphics(q,guard,savedError);')
    s=replace(s,'    if (inputOp(q.op)) return inputDispatch(q, guard, savedError);',
        '    if (inputOp(q.op)) { Result inputReply=inputDispatch(q,guard,savedError); inputReply.extras+=" display_window_generation="+number(displayWindowGeneration); return inputReply; }')
    s=replace(s,'r.extras = textureStatus()', 'r.extras = displayStatus() + " " + textureStatus()')
    s=replace(s,'if(textureFailed) return reject(',
        'if(displayBound || displayFailed || displayDC) return reject("SHUTDOWN_DISPLAY_OBLIGATION",ERROR_BUSY);\n            if(textureFailed) return reject(')
    return s

def self_check():
    s=source();before=parent.source()
    for a,b in [('DWORD WINAPI WorkerDispatcher(void *parameter) {','DWORD WINAPI Reader(void *) {'),('DWORD WINAPI Reader(void *) {','\n} // namespace')]:
        need(before[before.index(a):before.index(b,before.index(a))]==s[s.index(a):s.index(b,s.index(a))],'frozen Reader and worker retained')
    return dict(native_executed=False,desktop_used=False,native_admission=False,operations=OPS,blob_bytes=BLOB_BYTES,
        wire_budget=dict(max_input_bytes=32<<20,max_output_bytes=16<<20,measured_model_input_bytes=21654756,max_single_transfer=32768,max_commands=100000,Reader_worker_logic_unchanged=True),
        generator=identity(__file__),include=identity(INCLUDE),parent=identity(parent.__file__),parent_include=identity(parent.INCLUDE),generated_source_sha256=hashlib.sha256(s.encode()).hexdigest(),
        ABI=dict(factory_kind=10,GetAdapterMonitor_slot=14,adapter=0,MONITORINFOEXW=104,DISPLAY_DEVICEW=840,DEVMODEW=220,gamma=1536),
        offsets=dict(header=0,monitor=64,adapter=168,monitors=1008,mode=14448,gamma=14668),
        limitations=['Build-only; no actual D3D mapping or display API executed.','Display observations do not authorize restoration; independent current lifetime/wire/Job authentication is required.','Phase2 re-queries the live original factory after final device Release, before factory Release.','Read failure is sticky, and an actual failed DeleteDC retains its native obligation.'])

def build(folder):
    import pefile
    p=parent.parent;b=p.parent.parent.parent.base.parent.parent;folder=Path(folder).resolve()
    need(folder.is_relative_to(ROOT/'.venv-audit') and folder.drive.lower()=='f:' and not folder.exists(),'fresh F display build directory')
    checked=self_check();folder.mkdir(parents=True)
    cpp,exe,obj=[folder/n for n in ('terminal-display-owner.cpp','terminal-display-owner.exe','owner.obj')]
    recipe,log=folder/'build.cmd',folder/'build.log';cpp.write_text(source(),encoding='utf8',newline='\n')
    vcvars=b.VC/'Auxiliary/Build/vcvarsall.bat';compiler=b.MSVC/'bin/Hostx64/x86/cl.exe';linker=b.MSVC/'bin/Hostx64/x86/link.exe'
    recipe.write_text('\n'.join(['@echo off',f'call "{vcvars}" x86 {b.SDK} -vcvars_ver=14.44 >nul','if errorlevel 1 exit /b %errorlevel%',
        f'"{compiler}" /nologo /O2 /W4 /WX /MT /EHsc /std:c++17 /Fe:"{exe}" /Fo:"{obj}" "{cpp}" /link /SUBSYSTEM:WINDOWS /ENTRY:wmainCRTStartup gdi32.lib user32.lib shlwapi.lib ole32.lib comctl32.lib','exit /b %errorlevel%'])+'\n',encoding='utf8',newline='\r\n')
    with log.open('wb') as stream:
        done=subprocess.run([os.environ.get('COMSPEC','cmd.exe'),'/d','/c',str(recipe)],cwd=folder,env=dict(os.environ,TEMP=str(folder),TMP=str(folder)),stdout=stream,stderr=subprocess.STDOUT,timeout=90,creationflags=subprocess.CREATE_NO_WINDOW)
    need(done.returncode==0,'strict display build failed: '+str(log))
    pe=pefile.PE(str(exe));imports={x.dll.decode().lower():[i.name.decode() for i in x.imports] for x in pe.DIRECTORY_ENTRY_IMPORT}
    need(pe.FILE_HEADER.Machine==0x14c and pe.OPTIONAL_HEADER.Subsystem==2,'strict x86 Windows subsystem')
    old=json.loads((ROOT/'.venv-audit/terminal-texture-owner-build-v1-20261114/static-report.json').read_text())['imports']
    need(set(imports)==set(old),'no added DLL imports')
    added={dll:sorted(set(imports[dll])-set(old[dll])) for dll in imports}
    allowed={'user32.dll':{'GetMonitorInfoW','EnumDisplayDevicesW','EnumDisplaySettingsW'},'gdi32.dll':{'CreateDCW','GetDeviceGammaRamp'}}
    for dll,names in added.items():need(set(names)<=allowed.get(dll,set()),'only fixed read-only display imports '+dll)
    report=dict(kind='same_MAIN_D3D8_adapter_display_build_only',native_executed=False,desktop_used=False,native_admission=False,
        generator=identity(__file__),include=identity(INCLUDE),parent_generator=identity(parent.__file__),parent_include=identity(parent.INCLUDE),
        generated_source=identity(cpp),helper=identity(exe),artifacts=[identity(x) for x in (cpp,exe,obj,recipe,log)],
        dependencies=[identity(x) for x in (vcvars,compiler,linker)],imports=imports,added_imports=added,offline_checks=checked,formal_acceptance='2/8 unchanged')
    (folder/'static-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8',newline='\n');return report
