"""Build-only original WM_CLOSE/DestroyWindow extension of the frozen bridge."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
from devtools import terminal_window_native as base

ROOT=base.ROOT
PARENT_SHA='e55a84b45831a5b28ee27e958654e63513e8c78f4ddf5fb1d837d23c2f9fe83a'
INCLUDE_SHA='8eaf3c751f879f0f92b7505cc033c2d1d1e408f43a92626e575205fc4354f9c9'
need=base.need
identity=base.identity
replace=base.replace_once
BUILD=ROOT/'.venv-audit/terminal-window-destruction-build-v1-20261114'

DESTROY=r'''        if (q.op == "CB_DESTROY_WINDOW") {
            if (c.message != WM_CLOSE || c.w || c.l || destroyingWindow || c.hwnd != ownedWindow)
                return reject("ORIGINAL_WM_CLOSE_DESTRUCTION_ONLY");
            HWND target=c.hwnd; destroyingWindow=true;
            { WindowCallScope call(guard,q.id); begin(); r.value=DestroyWindow(target); capture(); }
            destroyingWindow=false; const DWORD saved=GetLastError(); const BOOL still=IsWindow(target); SetLastError(saved);
            r.extras="is_window_after="+number(still)+" ncdestroy_observed="+number(retiredWindow==target);
            if(r.value && (still || ownedWindow || retiredWindow!=target)) return reject("WINDOW_DESTRUCTION_NOT_OBSERVED");
            return r;
        }
'''
CLOSE=r'''    if (q.op == "WINDOW_CLOSE") {
        HWND target=ownedWindow;
        { WindowCallScope call(guard,q.id); begin(); r.value=static_cast<U32>(SendMessageA(target,WM_CLOSE,0,0)); capture(); }
        const DWORD saved=GetLastError(); const BOOL still=IsWindow(target); SetLastError(saved);
        r.extras="is_window_after="+number(still)+" ncdestroy_observed="+number(retiredWindow==target)+
            " quit_posted="+number(windowQuitPosted)+" property_removed="+number(windowPropertyRemoved);
        // LRESULT itself is not interpreted as a boolean success code.
        if(still || ownedWindow || retiredWindow!=target || !windowQuitPosted || !windowPropertyRemoved)
            return reject("ORIGINAL_CLOSE_LIFETIME_INCOMPLETE");
        return r;
    }
'''


def source():
    need(identity(base.__file__)['sha256']==PARENT_SHA and identity(base.INCLUDE)['sha256']==INCLUDE_SHA,'frozen window parent sources')
    s=base.source()
    s=replace(s,'bool windowGate = false, creatingWindow = false, destroyingWindow = false;',
        'bool windowGate = false, creatingWindow = false, destroyingWindow = false;\nbool windowQuitPosted = false, windowPropertyRemoved = false;')
    s=replace(s,'"RegisterClassExA", "CreateWindowExA", "ShowWindow",',
        '"RegisterClassExA", "CreateWindowExA", "WINDOW_CLOSE", "CB_DESTROY_WINDOW", "ShowWindow",')
    s=replace(s,'return op == "CB_GET_PROP" || op == "CB_SET_PROP" || op == "CB_GET_LONG" ||',
        'return op == "CB_DESTROY_WINDOW" || op == "CB_GET_PROP" || op == "CB_SET_PROP" || op == "CB_GET_LONG" ||')
    s=replace(s,'begin(); PostQuitMessage(0); capture(); r.extras = "void=1"; return r;',
        'begin(); PostQuitMessage(0); capture(); windowQuitPosted=true; r.extras = "void=1 quit_posted=1"; return r;')
    anchor='''            begin(); r.value = ptr(RemovePropA(c.hwnd, kWindowProperty)); capture();
            SetLastError(0); const U32 observed = ptr(GetPropA(c.hwnd,kWindowProperty)); const U32 error = GetLastError();'''
    s=replace(s,anchor,anchor+'\n            if(r.value == windowGuestOwner && !observed && !error) windowPropertyRemoved=true;')
    s=replace(s,'        if (q.op == "CB_GET_LONG") {',DESTROY+'        if (q.op == "CB_GET_LONG") {')
    s=replace(s,'    if (q.op == "ShowWindow") {',CLOSE+'    if (q.op == "ShowWindow") {')
    return s


def self_check():
    parent=base.self_check();before=base.source();after=source()
    for marker,end in [('DWORD WINAPI Reader(void *) {','\n} // namespace'),
                       ('DWORD WINAPI WorkerDispatcher(void *parameter) {','DWORD WINAPI Reader(void *) {')]:
        a=before.index(marker);b=after.index(marker)
        need(before[a:before.index(end,a)]==after[b:after.index(end,b)],'unchanged original queue/worker implementation')
    need('bool windowGate = false' in after and after.count('SendMessageA(target,WM_CLOSE,0,0)')==1,'exact owned close only, default gate closed')
    return dict(native_executed=False,parent_protocol=parent,source_sha256=hashlib.sha256(after.encode()).hexdigest(),
        new_operations={'WINDOW_CLOSE':1,'CB_DESTROY_WINDOW':2},expected_message=16,
        unchanged_Reader_and_worker=True,normal_destruction_observed=False)


def build(folder=BUILD):
    import pefile
    b=base.parent.parent;folder=Path(folder).resolve()
    need(folder.is_relative_to(ROOT/'.venv-audit') and folder.drive.lower()=='f:' and not folder.exists(),'fresh F build')
    checked=self_check();folder.mkdir(parents=True)
    cpp=folder/'terminal-window-destruction-owner.cpp';exe=folder/'terminal-window-destruction-owner.exe';obj=folder/'owner.obj'
    recipe=folder/'build.cmd';log=folder/'build.log';cpp.write_text(source(),encoding='utf-8',newline='\n')
    vcvars=b.VC/'Auxiliary/Build/vcvarsall.bat';compiler=b.MSVC/'bin/Hostx64/x86/cl.exe';linker=b.MSVC/'bin/Hostx64/x86/link.exe'
    recipe.write_text('\n'.join(['@echo off',f'call "{vcvars}" x86 {b.SDK} -vcvars_ver=14.44 >nul',
        'if errorlevel 1 exit /b %errorlevel%',f'"{compiler}" /nologo /O2 /W4 /WX /MT /EHsc /std:c++17 /Fe:"{exe}" /Fo:"{obj}" "{cpp}" /link /SUBSYSTEM:WINDOWS /ENTRY:wmainCRTStartup gdi32.lib user32.lib shlwapi.lib','exit /b %errorlevel%'])+'\n',encoding='utf-8',newline='\r\n')
    env=dict(os.environ,TEMP=str(folder),TMP=str(folder))
    with log.open('wb') as stream:
        done=subprocess.run([env.get('COMSPEC','cmd.exe'),'/d','/c',str(recipe)],cwd=folder,env=env,
            stdout=stream,stderr=subprocess.STDOUT,timeout=90,creationflags=subprocess.CREATE_NO_WINDOW)
    need(done.returncode==0,'warnings-as-errors build failed; inspect '+str(log))
    pe=pefile.PE(str(exe));imports={x.dll.decode().lower():[i.name.decode() for i in x.imports] for x in pe.DIRECTORY_ENTRY_IMPORT}
    need(pe.FILE_HEADER.Machine==0x14c and pe.OPTIONAL_HEADER.Subsystem==2,'x86 Windows subsystem')
    need(set(imports)=={'kernel32.dll','gdi32.dll','user32.dll','shlwapi.dll'},'bounded DLL imports')
    need(set(imports['user32.dll'])==base.USER_IMPORTS|{'SendMessageA'} and set(imports['gdi32.dll'])==base.GDI_IMPORTS,'only owned-window SendMessage added')
    report=dict(kind='same_owner_original_window_destruction_build',native_executed=False,ui_gate_default=False,
        generator=identity(__file__),parent_generator=identity(base.__file__),parent_include=identity(base.INCLUDE),
        resource=identity(base.RESOURCE),generated_source=identity(cpp),helper=identity(exe),
        artifacts=[identity(p) for p in (cpp,exe,obj,recipe,log)],dependencies=[identity(p) for p in (vcvars,compiler,linker,b.KIT/f'Include/{b.SDK}/um/WinUser.h')],
        imports=imports,offline_checks=checked,normal_window_cleanup_observed=False,
        limits='No helper launched; new code awaits actual same-owner callback and cleanup evidence.')
    (folder/'static-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n');return report


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--build-dir');a=ap.parse_args()
    print(json.dumps(build(a.build_dir)['helper'] if a.build_dir else self_check()))
