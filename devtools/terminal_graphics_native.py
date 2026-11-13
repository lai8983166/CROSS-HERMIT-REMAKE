"""Build-only fixed D3D8/font/cache extension on the current MAIN owner; no launcher."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess

from devtools import terminal_game_native as parent

ROOT=parent.ROOT
INCLUDE=ROOT/'devtools/terminal_graphics_native.inc'
need,identity,replace=parent.need,parent.identity,parent.replace
PARENT_SHA='8490e81e84be1e02ff0fb37e93f737a546f53f7f73a431dc958a659aee7322e1'
PARENT_INCLUDE_SHA='3d7227944852f57643465990ba5b717fde0d385ff3d47a31d5487bf1c32f1184'
OPS={'GFX_GATE':1,'GFX_BASELINE':1,'GFX_BASELINE_CLEAR':0,'GFX_FACTORY':1,'GFX_RUNTIME_CLOSE':0,'GFX_INFO':1,
 'GFX_MODULE_GET':1,'GFX_MODULE_LOAD':1,'GFX_PROC':2,'GFX_DEBUG_MUTE_RESOLVED':2,
 'GFX_ADDREF':1,'GFX_RELEASE':1,'GFX_MODE_COUNT':2,'GFX_ENUM_MODE':4,'GFX_DISPLAY_MODE':3,'GFX_CREATE_DEVICE':7,
 'GFX_CAPS':2,'GFX_CREATION':2,'GFX_DEVICE_MODE':2,'GFX_SURFACE_DESC':2,'GFX_VERTEX_DESC':2,'GFX_GET_FACTORY':2,
 'GFX_BACKBUFFER':4,'GFX_TEXTURE_SURFACE':3,'GFX_CHECK_FORMAT':7,'GFX_VIEWPORT':2,'GFX_DEBUG_MUTE':1,'GFX_TEXTURE':8,
 'GFX_LEVEL_DESC':3,'GFX_LOCK':5,'GFX_LOCK_READ':4,'GFX_LOCK_WRITE':4,'GFX_UNLOCK':2,'GFX_VERTEX_BUFFER':6,
 'GFX_BEGIN':1,'GFX_END':2,'GFX_TEXTURE_BIND':3,'GFX_RENDER_STATE':3,'GFX_STAGE_STATE':4,'GFX_DELETE_BLOCK':2,
 'GFX_GET_RENDER_STATE':3,'GFX_GAMMA_READ':2,'GFX_GAMMA_SAVE':2,'GFX_GAMMA_SET':3,'GFX_GAMMA_RESTORE':2,
 'GFX_GET_OBJECT':3,'GFX_DC_CREATE':1,'GFX_DIB':6,'GFX_FONT_INDIRECT':1,'GFX_SELECT':2,'GFX_BK_MODE':2,
 'GFX_BK_COLOR':2,'GFX_TEXT_COLOR':2,'GFX_MAP_MODE':2,'GFX_TEXT_ALIGN':2,'GFX_MULDIV':3,'GFX_TEXT_EXTENT':4,
 'GFX_TEXT_OUT':8,'GFX_DIB_READ':4,'GFX_DIB_WRITE':4,'GFX_DELETE_OBJECT':1,'GFX_DC_DELETE':1}
METHODS={10:{2:'GFX_RELEASE',6:'GFX_MODE_COUNT',7:'GFX_ENUM_MODE',8:'GFX_DISPLAY_MODE',10:'GFX_CHECK_FORMAT',15:'GFX_CREATE_DEVICE'},
 11:{1:'GFX_ADDREF',2:'GFX_RELEASE',6:'GFX_GET_FACTORY',7:'GFX_CAPS',8:'GFX_DEVICE_MODE',9:'GFX_CREATION',16:'GFX_BACKBUFFER',
 18:'GFX_GAMMA_SET',19:'GFX_GAMMA_READ',20:'GFX_TEXTURE',23:'GFX_VERTEX_BUFFER',40:'GFX_VIEWPORT',50:'GFX_RENDER_STATE',51:'GFX_GET_RENDER_STATE',
 52:'GFX_BEGIN',53:'GFX_END',56:'GFX_DELETE_BLOCK',61:'GFX_TEXTURE_BIND',63:'GFX_STAGE_STATE'},
 12:{2:'GFX_RELEASE',8:'GFX_SURFACE_DESC'},13:{2:'GFX_RELEASE',14:'GFX_LEVEL_DESC',15:'GFX_TEXTURE_SURFACE',16:'GFX_LOCK',17:'GFX_UNLOCK'},14:{2:'GFX_RELEASE',13:'GFX_VERTEX_DESC'}}
ABI_SITES={0x413888:'e883020000',0x413b68:'e883010000',0x413d52:'ff5118',0x413dc1:'ff511c',0x413c76:'ff513c',
 0x413b7e:'c78050b2000000000000',0x413c4d:'83c904',0x414061:'ff511c',0x4140f8:'ff5240',0x414126:'ff5220',0x41414b:'ff5208',0x414226:'ff5128'}

def source():
 need(identity(parent.__file__)['sha256']==PARENT_SHA and identity(parent.INCLUDE)['sha256']==PARENT_INCLUDE_SHA,'frozen GAME native parent')
 s=parent.source();s=replace(s,'Result dispatch(const Request &q) {',INCLUDE.read_text(encoding='utf8')+'\nResult dispatch(const Request &q) {')
 s=replace(s,'    if (gameOp(q.op)) return gameDispatch(q, guard, savedError);',
  '    if (gfxGate && q.op == "DeleteObject") return reject("USE_TRACKED_GFX_DELETE_OBJECT");\n'
  '    if (!gfxResourcesEmpty() && (q.op == "WINDOW_CLOSE" || q.op == "DestroyWindow" || q.op == "WINDOW_MODULE_CLOSE" || q.op == "CoUninitialize" || q.op == "GAME_GATE")) return reject("GRAPHICS_CLEANUP_BEFORE_PARENT_TEARDOWN", ERROR_BUSY);\n'
  '    if (gfxOp(q.op)) return gfxDispatch(q, guard, savedError);\n    if (gameOp(q.op)) return gameDispatch(q, guard, savedError);')
 s=replace(s,'r.extras = gameStatus() + " ui_gate="','r.extras = gfxStatus() + " " + gameStatus() + " ui_gate="')
 s=replace(s,'if(gameGate || !gameEmpty()) return reject("SHUTDOWN_GAME_RESOURCES_LIVE", ERROR_BUSY);',
  'if(gfxGate || !gfxEmpty()) return reject("SHUTDOWN_GRAPHICS_RESOURCES_LIVE", ERROR_BUSY);\n            if(gameGate || !gameEmpty()) return reject("SHUTDOWN_GAME_RESOURCES_LIVE", ERROR_BUSY);')
 return s

def self_check():
 from tools.school_device_init import source_contract
 from tools.school_font_state import source_contract as font_contract,RENDER,STAGES
 inherited=parent.self_check();legacy=source_contract();raw=parent.IMAGE.read_bytes()
 for va,code in ABI_SITES.items():need(raw[va-0x400000:va-0x400000+len(bytes.fromhex(code))].hex()==code,'original fullscreen/ABI '+hex(va))
 oft,_,_,name,first=struct.unpack_from('<5I',raw,0x1fd5cc)
 imports=[]
 for slot,label in ((0x5922c8,'GetModuleHandleA'),(0x592184,'LoadLibraryA'),(0x5922cc,'GetProcAddress')):
  thunk=struct.unpack_from('<I',raw,oft+slot-0x400000-first)[0]
  actual=raw[thunk+2:].split(b'\0',1)[0].decode('ascii');need(actual==label,'raw cold debug import '+hex(slot))
  imports.append(dict(slot=hex(slot),name=actual))
 s=source();need(all('"'+op+'"' in s for op in OPS),'all graphics typed operations implemented')
 font=font_contract()
 need(all('{2,%d,%d,0}'%(a,b)in s for _,a,b in RENDER) and all('{3,%d,%d,%d}'%(a,b,c)in s for _,a,b,c in STAGES),'exact original font-state immediate plan')
 need(max(OPS.values())<=16 and 'gfxGate=false' in s,'numeric bound/default closed gate')
 before=parent.source()
 for a,b in [('DWORD WINAPI WorkerDispatcher(void *parameter) {','DWORD WINAPI Reader(void *) {'),('DWORD WINAPI Reader(void *) {','\n} // namespace')]:
  need(before[before.index(a):before.index(b,before.index(a))]==s[s.index(a):s.index(b,s.index(a))],'frozen queue/worker unchanged')
 return dict(native_executed=False,desktop_used=False,graphics_gate_enabled=False,source=identity(parent.IMAGE),
  parent_checks=inherited,legacy_device_contract=legacy,legacy_font_state_contract=font,cold_debug_imports=imports,original_fullscreen_bytes=[dict(va=hex(a),hex=b)for a,b in ABI_SITES.items()],
  operations=OPS,methods=METHODS,generated_source_sha256=hashlib.sha256(s.encode()).hexdigest(),
  mute_contract=dict(max_modules=2,max_calls_per_module=4,max_total_calls=8,per_module_sequence=[1,0,1,0],compile_time_assertions=['both modules two pairs admitted','third pair refused','repeated state and non-BOOL refused']),
  structures=dict(presentation=52,display_mode=16,caps=212,surface_desc=32,creation=16,viewport=24,locked_rect=8,vertex_desc=24,gamma=1536,LOGFONTA=60,BITMAPINFOHEADER=40),
  limitations=['ABI/build only, no actual device/audio/window/desktop run.','Fullscreen1024x768 PP comes from real enumerated mode; windowed PP is refused.',
   'Baseline registration is only a token binding and is not proof that an external desktop baseline was captured.',
   'Device gamma readback before final device release does not qualify final desktop gamma after display restoration.',
   'No DirectInput, global input, draw, Present, Reset or generic COM call. No native admission or launcher.'])

def build(folder):
 import pefile
 b=parent.parent.base.parent.parent;folder=Path(folder).resolve()
 need(folder.is_relative_to(ROOT/'.venv-audit') and folder.drive.lower()=='f:' and not folder.exists(),'fresh F build directory')
 checked=self_check();folder.mkdir(parents=True)
 cpp,exe,obj=[folder/n for n in ('terminal-graphics-owner.cpp','terminal-graphics-owner.exe','owner.obj')]
 recipe,log=folder/'build.cmd',folder/'build.log';cpp.write_text(source(),encoding='utf8',newline='\n')
 vcvars=b.VC/'Auxiliary/Build/vcvarsall.bat';compiler=b.MSVC/'bin/Hostx64/x86/cl.exe';linker=b.MSVC/'bin/Hostx64/x86/link.exe'
 recipe.write_text('\n'.join(['@echo off',f'call "{vcvars}" x86 {b.SDK} -vcvars_ver=14.44 >nul','if errorlevel 1 exit /b %errorlevel%',
  f'"{compiler}" /nologo /O2 /W4 /WX /MT /EHsc /std:c++17 /Fe:"{exe}" /Fo:"{obj}" "{cpp}" /link /SUBSYSTEM:WINDOWS /ENTRY:wmainCRTStartup gdi32.lib user32.lib shlwapi.lib ole32.lib comctl32.lib','exit /b %errorlevel%'])+'\n',encoding='utf8',newline='\r\n')
 with log.open('wb')as stream:
  done=subprocess.run([os.environ.get('COMSPEC','cmd.exe'),'/d','/c',str(recipe)],cwd=folder,env=dict(os.environ,TEMP=str(folder),TMP=str(folder)),stdout=stream,stderr=subprocess.STDOUT,timeout=90,creationflags=subprocess.CREATE_NO_WINDOW)
 need(done.returncode==0,'strict build failed: '+str(log))
 pe=pefile.PE(str(exe));imports={x.dll.decode().lower():[i.name.decode()for i in x.imports]for x in pe.DIRECTORY_ENTRY_IMPORT}
 need(pe.FILE_HEADER.Machine==0x14c and pe.OPTIONAL_HEADER.Subsystem==2,'strict x86 Windows subsystem')
 old=json.loads((ROOT/'.venv-audit/terminal-game-owner-build-v1-20261114/static-report.json').read_text())['imports']
 need(set(imports)==set(old),'no additional import DLLs; D3D8 dynamically loaded from System32 only')
 for dll in ('user32.dll','ole32.dll','comctl32.dll','shlwapi.dll'):need(set(imports[dll])==set(old[dll]),'unchanged '+dll)
 added={dll:sorted(set(imports[dll])-set(old[dll]))for dll in imports}
 need(set(added['gdi32.dll'])<={'CreateCompatibleDC','CreateDIBSection','CreateFontIndirectA','SelectObject','SetBkMode','SetBkColor','SetTextColor','SetMapMode','SetTextAlign','GetTextExtentPoint32A','ExtTextOutA'},'owned memory-DC GDI leaf imports only')
 need(set(added['kernel32.dll'])<={'LoadLibraryExW','GetModuleFileNameW','GetModuleHandleA','GetProcAddress','FreeLibrary','MulDiv'},'fixed module/number operations only')
 report=dict(kind='same_MAIN_D3D8_font_cache_build_only',native_executed=False,desktop_used=False,native_admission=False,
  generator=identity(__file__),include=identity(INCLUDE),parent_generator=identity(parent.__file__),parent_include=identity(parent.INCLUDE),
  generated_source=identity(cpp),helper=identity(exe),artifacts=[identity(p)for p in (cpp,exe,obj,recipe,log)],
  dependencies=[identity(p)for p in (vcvars,compiler,linker,b.KIT/f'Include/{b.SDK}/um/wingdi.h')],legacy_sources=[identity(ROOT/p)for p in ('tools/school_startup_return_device.cs','tools/school_device_init.py','tools/school_font_state.py','tools/school_font_finish_gdi.cs')],
  imports=imports,added_imports=added,offline_checks=checked,
  dynamic_exports=dict(modules=['d3d8.dll','d3d8d.dll'],load_flags=0x800,exports=['Direct3DCreate8','DebugSetMute'],GetModuleHandle_AddRef=False,extra_LoadLibrary_refs='explicitly retired by GFX_RUNTIME_CLOSE; absent debug DLL returns actual0'),
  notes='Build only. SDK D3D8 header is not assumed: fixed original byte/legacy typed ABI contracts and local x86 layouts are used. Runtime DLL identity is returned only when explicitly launched later.')
 (folder/'static-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8',newline='\n');return report

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--build-dir');a=p.parse_args()
 print(json.dumps(build(a.build_dir)['helper']if a.build_dir else self_check()))
