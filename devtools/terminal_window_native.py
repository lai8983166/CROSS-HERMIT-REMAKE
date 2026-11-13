"""Generate/build the same-owner synchronous window bridge; never launch it.

All new window/resource operations require an explicit WINDOW_GATE1 command.
The fixed original callback executes only in the external guest executor. Native
WNDPROC stays on the existing MAIN thread, transports bounded callback data and
waits for matching callback results. No fallback callback result is synthesized.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
from devtools import terminal_scene_dc_native as parent

ROOT = parent.ROOT
INCLUDE = ROOT/'devtools/terminal_window_native.inc'
RESOURCE = ROOT/'.venv-audit/school-window-icons-v1.dll'
PARENT_SHA = '51b52881441d65589462120ba4fb2a32f09df2a3bbf552db51d9d2926744ce53'
RESOURCE_SHA = '1c2efa226cb52e97696477964d85bb6f0b94f727c8c3c550ef57da41beb009d7'
BUILD = ROOT/'.venv-audit/terminal-window-owner-build-v1-20261113'
need = parent.parent.need
identity = parent.parent.identity
replace_once = parent.parent.replace_once

CALLBACK_OPS = {'CB_GET_PROP':2, 'CB_SET_PROP':3, 'CB_GET_LONG':3,
                'CB_DEFAULT':5, 'CB_RETURN':2, 'CB_REMOVE_PROP':2, 'CB_POST_QUIT':2}
WINDOW_OPS = {'WINDOW_GATE':1, 'WINDOW_MODULE':0, 'WINDOW_MODULE_CLOSE':1,
    'FindWindowA':2, 'SetRect':5, 'AdjustWindowRect':3, 'LoadIconA':2, 'LoadCursorA':2,
    'GetStockObject':1, 'RegisterClassExA':1, 'CreateWindowExA':12, 'ShowWindow':2,
    'UpdateWindow':1, 'GetClientRect':2, 'GetWindowRect':2, 'GetWindowLongA':2,
    'SetWindowLongA':3, 'DestroyWindow':1, 'UnregisterClassA':2, **CALLBACK_OPS}
USER_IMPORTS = {'GetDC','ReleaseDC','GetGuiResources','PostQuitMessage','GetPropA','SetPropA',
    'RemovePropA','GetWindowLongA','DefWindowProcA','FindWindowA','SetRect','AdjustWindowRect',
    'LoadIconA','LoadCursorA','GetClassInfoExA','RegisterClassExA','CreateWindowExA','UnregisterClassA',
    'GetClientRect','GetWindowRect','SetWindowLongA','ShowWindow','UpdateWindow','DestroyWindow','IsWindow'}
GDI_IMPORTS = {'CreateFontA','GetObjectA','DeleteObject','DeleteDC','GetObjectType','GetCurrentObject','GdiFlush','GetStockObject'}


def source():
    need(identity(parent.__file__)['sha256'] == PARENT_SHA, 'fixed DC observer generator')
    resource = RESOURCE.read_bytes()
    need(len(resource) == 3072 and hashlib.sha256(resource).hexdigest() == RESOURCE_SHA,
         'fixed code-free original-icon resource DLL')
    import pefile
    pe=pefile.PE(data=resource)
    need(pe.OPTIONAL_HEADER.AddressOfEntryPoint == pe.OPTIONAL_HEADER.SizeOfCode == 0 and
         len(pe.sections) == 1 and not (pe.sections[0].Characteristics & 0x20000000) and
         pe.OPTIONAL_HEADER.DATA_DIRECTORY[1].VirtualAddress == 0, 'resource module has no code, entry or imports')
    original=parent.generated_source()
    include=INCLUDE.read_text(encoding='utf-8')
    need(include.count('@@RESOURCE_PATH@@') == include.count('@@RESOURCE_HEX@@') == 1, 'exact resource substitutions')
    include=include.replace('@@RESOURCE_PATH@@',RESOURCE.as_posix()).replace('@@RESOURCE_HEX@@',resource.hex())
    result=replace_once(original,'DWORD WINAPI WorkerDispatcher(void *parameter);',
                        'DWORD WINAPI WorkerDispatcher(void *parameter);\n'+include)
    anchor='    const auto args = [&](size_t count) { return numeric(q, count, a); };'
    result=replace_once(result,anchor,anchor+'\n    if (windowOp(q.op)) return windowDispatch(q, guard, savedError);')
    result=replace_once(result,'        r.extras = "allocations=" + number(static_cast<U32>(allocations.size()))',
        '        r.extras = "ui_gate=" + number(windowGate) + " window_modules=" + number(windowModule != nullptr) +\n'
        '            " window_classes=" + number(windowClassAtom != 0) + " windows=" + number(ownedWindow != nullptr) +\n'
        '            " callback_depth=" + number(static_cast<U32>(windowCallbacks.size())) + " callback_count=" + number(callbackSequence) +\n'
        '            " allocations=" + number(static_cast<U32>(allocations.size()))')
    result=replace_once(result,'        if (q.op == "Shutdown") {',
        '        if (q.op == "Shutdown") {\n'
        '            if (windowModule || windowClassAtom || ownedWindow || !windowCallbacks.empty())\n'
        '                return reject("SHUTDOWN_WINDOW_RESOURCES_LIVE", ERROR_BUSY);')
    return result


def generated_source():
    return source()


def self_check():
    """Pure Python protocol/state checks and generated-source ancestry checks."""
    original=parent.generated_source(); generated=source()
    reader=lambda s:s[s.index('DWORD WINAPI Reader(void *) {'):s.index('\n} // namespace',s.index('DWORD WINAPI Reader(void *) {'))]
    worker=lambda s:s[s.index('DWORD WINAPI WorkerDispatcher(void *parameter) {'):s.index('DWORD WINAPI Reader(void *) {')]
    need(reader(original)==reader(generated), 'Reader byte-preserved, including wire command limits')
    need(worker(original)==worker(generated), 'native worker/TLS/dispatch loop byte-preserved')
    for marker in ('bool parseU32(', 'bool pop(', 'void push('):
        start=original.index(marker);end=original.index('\n}',start)+2
        need(original[start:end] in generated, 'existing wire/queue implementation unchanged')
    need('bool windowGate = false' in generated and 'WINDOW_GATE_CLOSED' in generated, 'default closed explicit UI gate')
    need('guard.unlock();' in generated and 'guard.lock(); windowParentRequest = previous;' in generated,
         'callback-capable calls release and restore stateMutex')
    need(max(WINDOW_OPS.values()) <= 16, 'fixed Reader argument cap respected')
    # The bounded state model encodes only wire admission and reentrancy. It
    # calls no collector/Win32 code and is not a simulated successful window.
    stack=[]; sequence=0; rows=[]
    def enter(parent,hwnd,message,w,l):
        nonlocal sequence
        need(len(stack)<8 and sequence<128, 'bounded callback model')
        sequence+=1;frame=dict(id=sequence,parent=parent,parent_callback=stack[-1]['id'] if stack else 0,
            depth=len(stack)+1,hwnd=hwnd,message=message,w=w,l=l);stack.append(frame);return frame
    def admit(op,args):
        need(stack and op in CALLBACK_OPS and len(args)==CALLBACK_OPS[op] and args[0]==stack[-1]['id'], 'active matching callback model')
        f=stack[-1]
        if op=='CB_RETURN':stack.pop();return
        if op=='CB_POST_QUIT':need(args[1]==0 and f['message']==2,'destroy quit model');return
        need(args[1]==f['hwnd'],'same callback HWND model')
        if op=='CB_DEFAULT':need(args[2:]==[f['message'],f['w'],f['l']],'exact native callback args model')
    first=enter(10,100,129,0,200);admit('CB_GET_PROP',[1,100]);admit('CB_DEFAULT',[1,100,129,0,200])
    second=enter(12,100,131,0,300);third=enter(14,100,70,0,400)
    need([f['depth'] for f in stack]==[1,2,3] and third['parent_callback']==2 and second['parent_callback']==1,'three-level actual protocol ancestry model')
    rejected=[]
    for label,op,args in [('wrong_id','CB_RETURN',[1,0]),('wrong_hwnd','CB_GET_PROP',[3,999]),
        ('wrong_lparam','CB_DEFAULT',[3,100,70,0,401]),('shutdown_in_callback','Shutdown',[]),
        ('wrong_arity','CB_DEFAULT',[3,100,70,0,400,0]),('create_in_callback','CreateWindowExA',[0]*12)]:
        try:admit(op,args)
        except ValueError:rejected.append(label)
        else:raise ValueError('protocol model accepted '+label)
    admit('CB_RETURN',[3,0]);admit('CB_RETURN',[2,0]);admit('CB_RETURN',[1,1]);need(not stack,'all original callback frames naturally unwind')
    for op,argc in CALLBACK_OPS.items():need('"'+op+'"' in generated and 0<argc<=5,'declared native callback protocol')
    return dict(native_executed=False,window_created=False,ui_gate_enabled=False,
        source_bytes=len(generated.encode()),source_sha256=hashlib.sha256(generated.encode()).hexdigest(),
        Reader_unchanged=True,worker_unchanged=True,callback_depth_model=3,protocol_negative_cases=rejected,
        callback_operations=CALLBACK_OPS,main_operations=WINDOW_OPS,
        scope='Offline source/protocol checks only. No actual mutex reentrancy, HWND callback, API return or lifecycle acceptance.')


def build(folder=BUILD):
    import pefile
    b=parent.parent;folder=Path(folder).resolve()
    need(folder.is_relative_to(ROOT/'.venv-audit') and folder.drive.lower()=='f:' and not folder.exists(),'fresh F build only')
    checked=self_check();folder.mkdir(parents=True)
    cpp=folder/'terminal-window-owner.cpp';exe=folder/'terminal-window-owner.exe';obj=folder/'owner.obj'
    recipe=folder/'build.cmd';log=folder/'build.log';cpp.write_text(source(),encoding='utf-8',newline='\n')
    vcvars=b.VC/'Auxiliary/Build/vcvarsall.bat';compiler=b.MSVC/'bin/Hostx64/x86/cl.exe';linker=b.MSVC/'bin/Hostx64/x86/link.exe'
    recipe.write_text('\n'.join(['@echo off',f'call "{vcvars}" x86 {b.SDK} -vcvars_ver=14.44 >nul',
        'if errorlevel 1 exit /b %errorlevel%',
        f'"{compiler}" /nologo /O2 /W4 /WX /MT /EHsc /std:c++17 /Fe:"{exe}" /Fo:"{obj}" "{cpp}" /link /SUBSYSTEM:WINDOWS /ENTRY:wmainCRTStartup gdi32.lib user32.lib shlwapi.lib',
        'exit /b %errorlevel%'])+'\n',encoding='utf-8',newline='\r\n')
    env=dict(os.environ,TEMP=str(folder),TMP=str(folder))
    with log.open('wb') as out:
        done=subprocess.run([env.get('COMSPEC','cmd.exe'),'/d','/c',str(recipe)],cwd=folder,env=env,
            stdout=out,stderr=subprocess.STDOUT,timeout=90,creationflags=subprocess.CREATE_NO_WINDOW)
    need(done.returncode==0,'window source build failed; inspect '+str(log))
    pe=pefile.PE(str(exe));imports={entry.dll.decode().lower():[i.name.decode() for i in entry.imports] for entry in pe.DIRECTORY_ENTRY_IMPORT}
    need(pe.FILE_HEADER.Machine==0x14c and pe.OPTIONAL_HEADER.Subsystem==2,'x86 Windows subsystem')
    need(set(imports)=={'kernel32.dll','gdi32.dll','user32.dll','shlwapi.dll'},'bounded native DLL imports')
    need(set(imports['user32.dll'])==USER_IMPORTS and set(imports['gdi32.dll'])==GDI_IMPORTS,'exact window and metadata imports')
    report=dict(kind='same_owner_window_callback_build_not_executed',native_executed=False,ui_gate_default=False,
        parent_generator=identity(parent.__file__),generator=identity(__file__),include=identity(INCLUDE),resource=identity(RESOURCE),
        generated_source=identity(cpp),helper=identity(exe),artifacts=[identity(p) for p in (cpp,exe,obj,recipe,log)],
        dependencies=[identity(p) for p in (vcvars,compiler,linker,b.KIT/f'Include/{b.SDK}/um/Windows.h',b.KIT/f'Include/{b.SDK}/um/WinUser.h')],
        parent_source_pins=[identity(b.BASE_SOURCE),identity(b.__file__)],imports=imports,offline_protocol=checked,
        limits=dict(callbacks=128,callback_depth=8,owned_windows=1,wire_transfer=32768,reader_changed=False),
        limitations=['UI execution is not admitted by this build. No helper/window was launched.',
            'Unknown callback operations fail closed. Full WM_PAINT/input/game/device routes remain outside this bridge.',
            'LastError and guest/native callback/pointer projections require fresh actual evidence after explicit UI admission.'])
    (folder/'static-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8',newline='\n')
    return report


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--build-dir');a=ap.parse_args()
    print(json.dumps(build(a.build_dir)['helper'] if a.build_dir else self_check()))
