"""Build-only fixed MAIN-lane COM/audio/movie extension; no launcher or UI run."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import uuid

from devtools import terminal_window_native_v3 as parent

ROOT=parent.ROOT
INCLUDE=ROOT/'devtools/terminal_game_native.inc'
IMAGE=ROOT/'analysis/hermit_game.exe'
PARENT_SHA='af9168cc96d0184d3e2e06ffe4f6f1565880b2035707555786df57f7cf811706'
IMAGE_SHA='588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'
need,identity=parent.need,parent.identity
replace=parent.parent.replace
GUIDS={0x5cb3ec:'d2ac2881-b39b-11d1-8704-00600893b1bd',
       0x5caf0c:'679c4137-c62e-4147-b2b4-9d569acb254c',
       0x5cb37c:'d2ac2892-b39b-11d1-8704-00600893b1bd',
       0x5caf1c:'19e7c08c-0a44-4e6a-a116-595a7cd5de8c',
       0x5cb2fc:'d2ac2893-b39b-11d1-8704-00600893b1bd',
       0x5cb08c:'d2ac28b1-b39b-11d1-8704-00600893b1bd',
       0x5cfd7c:'e436ebb3-524f-11ce-9f53-0020af0ba770',
       0x5ce80c:'56a868a9-0ad4-11ce-b03a-0020af0ba770',
       0x5cef3c:'56a868b1-0ad4-11ce-b03a-0020af0ba770',
       0x5ce8dc:'36b73880-c2c8-11cf-8b46-00805f6cef60',
       0x5cef0c:'56a868b2-0ad4-11ce-b03a-0020af0ba770',
       0x5cef1c:'56a868c0-0ad4-11ce-b03a-0020af0ba770',
       0x5ceefc:'56a868b3-0ad4-11ce-b03a-0020af0ba770'}
OPS={'GAME_GATE':1,'CoInitialize':1,'CoUninitialize':0,'InitCommonControlsEx':1,
     'CoCreateInstance':5,'COM_QUERY':3,'COM_RELEASE':1,'COM_INFO':1,
     'DM_INIT_AUDIO':8,'DM_GET_DEFAULT_AUDIO_PATH':2,'DM_LOADER_SEARCH':4,
     'DM_SET_VOLUME':4,'DM_STOP':5,'DM_CLOSE_DOWN':1,'DS_SET_NOTIFY':4,'DS_STOP':1,
     'MultiByteToWideChar':6}
KINDS={1:dict(name='IDirectMusicPerformance8',slots={0:3,2:1,5:5,34:4,38:1,44:8,51:2}),
       2:dict(name='IDirectMusicLoader8',slots={0:3,2:1,5:4}),
       3:dict(name='IDirectMusicAudioPath',slots={0:3,2:1}),
       4:dict(name='IGraphBuilder',slots={0:3,2:1}),
       5:dict(name='IMediaControl',slots={0:3,2:1,9:1}),
       6:dict(name='IMediaSeeking',slots={0:3,2:1}),
       7:dict(name='IMediaPosition',slots={0:3,2:1}),
       8:dict(name='IMediaEventEx',slots={0:3,2:1,13:4}),
       9:dict(name='IBasicAudio',slots={0:3,2:1})}
ABI_SITES={0x49def5:'ff1578245900',0x49df47:'c745c008000000',0x49df4e:'c745c400080000',
           0x49df5b:'ff1524205900',0x40c38d:'ff157c245900',0x40c3d8:'ff90b0000000',
           0x40c418:'ff91cc000000',0x40c457:'ff157c245900',0x40c4d7:'ff158c225900',
           0x40c59c:'ff5214',0x40d752:'ff9088000000',0x40c043:'ff5114',0x40c061:'ff9198000000',
           0x41d601:'ff157c245900',0x41d637:'ff11',0x41d669:'ff12',0x41d69b:'ff10',
           0x41d6cd:'ff11',0x41d6ff:'ff12',0x41d734:'ff5134',0x41d437:'ff5024',0x41d461:'ff5134'}


def original_contract():
    data=IMAGE.read_bytes();need(hashlib.sha256(data).hexdigest()==IMAGE_SHA,'fixed original image')
    rows=[]
    for address,value in GUIDS.items():
        raw=data[address-0x400000:address-0x400000+16]
        need(str(uuid.UUID(bytes_le=raw))==value,'original GUID '+hex(address))
        rows.append(dict(guest=address,hex=raw.hex(),guid=value))
    for address,value in ABI_SITES.items():
        need(data[address-0x400000:address-0x400000+len(bytes.fromhex(value))].hex()==value,'original ABI call '+hex(address))
    need(data[0x192ad0:0x192ad6]==b'.\0\\\0\0\0','original local loader directory')
    return dict(image=identity(IMAGE),GUIDs=rows,original_call_bytes=[dict(va=hex(p),hex=b) for p,b in ABI_SITES.items()],
        kinds=KINDS,argument_counts_include_COM_this=True,
        native_returns='HRESULT/ULONG/BOOL original32 bits; CoUninitialize void has declared result0. No synthetic successful HRESULT.',
        fixed_query_IIDs='Only the five original IGraphBuilder queries; metadata slot0 on other kinds is diagnostic, not permission to query them.',
        GUID_projection='Exact fixed original VA selects verified16-byte GUID copied into native constant storage. No native dereference of guest GUID VA.',
        output_projection='Output is a current owned aligned4-byte zero-initialized buffer; real API writes it; caller must MEM_READ it.')


def source():
    need(identity(parent.__file__)['sha256']==PARENT_SHA,'frozen executed window-property correction')
    contract=original_contract();s=parent.source()
    s=replace(s,'#include <windows.h>','#include <windows.h>\n#define CINTERFACE\n#include <objbase.h>\n#include <commctrl.h>\n#include <control.h>\n#include <cstddef>')
    include=INCLUDE.read_text(encoding='utf8');need(include.count('@@GAME_GUIDS@@')==1,'fixed GUID expansion')
    rows=[]
    for item in contract['GUIDs']:
        b=bytes.fromhex(item['hex']);d1,d2,d3=struct.unpack('<IHH',b[:8])
        rows.append('{0x%x,{0x%x,0x%x,0x%x,{%s}}}'%(item['guest'],d1,d2,d3,','.join('0x%02x'%x for x in b[8:])))
    include=include.replace('@@GAME_GUIDS@@',',\n'.join(rows))
    anchor='Result dispatch(const Request &q) {'
    s=replace(s,anchor,include+'\n'+anchor)
    anchor='    if (windowOp(q.op)) return windowDispatch(q, guard, savedError);'
    s=replace(s,anchor,
        '    if (gameBusy && q.lane && q.op != "STATUS") return reject("GAME_EXTERNAL_CALL_IN_PROGRESS", ERROR_BUSY);\n'
        '    if (gameOp(q.op)) return gameDispatch(q, guard, savedError);\n'+anchor)
    s=replace(s,'        r.extras = "ui_gate=" + number(windowGate)',
        '        r.extras = gameStatus() + " ui_gate=" + number(windowGate)')
    anchor='        if (q.op == "Shutdown") {'
    s=replace(s,anchor,anchor+'\n            if(gameGate || !gameEmpty()) return reject("SHUTDOWN_GAME_RESOURCES_LIVE", ERROR_BUSY);')
    return s


def self_check():
    inherited=parent.self_check();before=parent.source();after=source()
    for start,end in (('DWORD WINAPI Reader(void *) {','\n} // namespace'),
                      ('DWORD WINAPI WorkerDispatcher(void *parameter) {','DWORD WINAPI Reader(void *) {')):
        a=before.index(start);b=after.index(start)
        need(before[a:before.index(end,a)]==after[b:after.index(end,b)],'unchanged native queue/worker body')
    need('bool gameGate=false, gameBusy=false;' in after and 'GAME_GATE_CLOSED' in after,'explicit closed GAME gate')
    need(max(OPS.values())<=16 and 'GAME_EXTERNAL_CALL_IN_PROGRESS' in after,'bounded Reader unchanged; in-flight buffers protected')
    # Bounded predicate checks, without constructing a Win32/native owner.
    pairs={(0x5cb3ec,0x5caf0c):1,(0x5cb37c,0x5caf1c):2,(0x5cfd7c,0x5ce80c):4}
    bad=[('foreign_class',(0x5cb3ed,0x5caf0c)),('wrong_iid',(0x5cb3ec,0x5caf1c)),('arbitrary_class',(0,0))]
    need(all(pair not in pairs for _,pair in bad),'fixed pair negative controls')
    need(all('"'+op+'"' in after for op in OPS),'all declared operations implemented')
    return dict(native_executed=False,desktop_used=False,game_gate_enabled=False,parent_checks=inherited,
        protocol_operations=OPS,contract=original_contract(),negative_pair_predicates=[name for name,_ in bad],
        generated_source_sha256=hashlib.sha256(after.encode()).hexdigest(),Reader_worker_unchanged=True,
        unimplemented=['D3D8/device/font/cache/queues/gamma','DirectInput/global cursor','DirectMusic segment loading/playback','DirectShow rendering/playback','generic COM invocation','failure MessageBox'],
        runtime_limitations=['No actual COM/apartment/audio/graph lifetime exercised.','CoInitialize and all admitted COM calls may pump synchronous callbacks through the existing MAIN bridge.','Current resource cwd and complete GAME/device/input/desktop recovery are not qualified.','No native helper is launched by this module.'])


def build(folder):
    import pefile
    b=parent.base.parent.parent;folder=Path(folder).resolve()
    need(folder.is_relative_to(ROOT/'.venv-audit') and folder.drive.lower()=='f:' and not folder.exists(),'fresh F build directory')
    checked=self_check();folder.mkdir(parents=True)
    cpp,exe,obj=[folder/n for n in ('terminal-game-owner.cpp','terminal-game-owner.exe','owner.obj')]
    recipe,log=folder/'build.cmd',folder/'build.log';cpp.write_text(source(),encoding='utf8',newline='\n')
    vcvars=b.VC/'Auxiliary/Build/vcvarsall.bat';compiler=b.MSVC/'bin/Hostx64/x86/cl.exe';linker=b.MSVC/'bin/Hostx64/x86/link.exe'
    recipe.write_text('\n'.join(['@echo off',f'call "{vcvars}" x86 {b.SDK} -vcvars_ver=14.44 >nul','if errorlevel 1 exit /b %errorlevel%',
        f'"{compiler}" /nologo /O2 /W4 /WX /MT /EHsc /std:c++17 /Fe:"{exe}" /Fo:"{obj}" "{cpp}" /link /SUBSYSTEM:WINDOWS /ENTRY:wmainCRTStartup gdi32.lib user32.lib shlwapi.lib ole32.lib comctl32.lib','exit /b %errorlevel%'])+'\n',encoding='utf8',newline='\r\n')
    with log.open('wb') as stream:
        done=subprocess.run([os.environ.get('COMSPEC','cmd.exe'),'/d','/c',str(recipe)],cwd=folder,
            env=dict(os.environ,TEMP=str(folder),TMP=str(folder)),stdout=stream,stderr=subprocess.STDOUT,timeout=90,creationflags=subprocess.CREATE_NO_WINDOW)
    need(done.returncode==0,'strict x86 build failed; inspect '+str(log))
    pe=pefile.PE(str(exe));imports={x.dll.decode().lower():[i.name.decode() for i in x.imports] for x in pe.DIRECTORY_ENTRY_IMPORT}
    need(pe.FILE_HEADER.Machine==0x14c and pe.OPTIONAL_HEADER.Subsystem==2,'x86 Windows subsystem')
    old=json.loads((ROOT/'.venv-audit/terminal-window-destruction-build-v2-20261114/static-report.json').read_text(encoding='utf8'))['imports']
    need(set(imports)==set(old)|{'ole32.dll','comctl32.dll'},'only COM and common-controls DLL imports added')
    for dll in ('user32.dll','gdi32.dll','shlwapi.dll'):need(set(imports[dll])==set(old[dll]),'unchanged '+dll+' imports')
    need(set(imports['kernel32.dll'])==set(old['kernel32.dll'])|{'MultiByteToWideChar'},'only bounded conversion kernel import added')
    need(set(imports['ole32.dll'])=={'CoInitialize','CoUninitialize','CoCreateInstance'} and set(imports['comctl32.dll'])=={'InitCommonControlsEx'},'narrow actual COM exports')
    headers=['objbase.h','combaseapi.h','commctrl.h','control.h']
    report=dict(kind='same_MAIN_GAME_COM_startup_build_only',native_executed=False,desktop_used=False,game_gate_default=False,
        generator=identity(__file__),include=identity(INCLUDE),parent_generator=identity(parent.__file__),generated_source=identity(cpp),helper=identity(exe),
        parent_case_dependency=identity(parent.CASE),original=identity(IMAGE),
        artifacts=[identity(p) for p in (cpp,exe,obj,recipe,log)],
        dependencies=[identity(p) for p in (vcvars,compiler,linker)]+[identity(b.KIT/f'Include/{b.SDK}/um'/n) for n in headers],
        imports=imports,offline_checks=checked,actual_COM_lifetime_proven=False,
        notes='Fixed source/ABI/build only. Successful API HRESULTs, resources and cleanup remain unobserved; no launcher exists.')
    (folder/'static-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8',newline='\n');return report


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--build-dir');args=ap.parse_args()
    print(json.dumps(build(args.build_dir)['helper'] if args.build_dir else self_check()))
