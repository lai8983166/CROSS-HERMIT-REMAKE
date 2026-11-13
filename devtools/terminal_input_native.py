"""Build-only original MAIN DirectInput initialization and cursor ownership leaves."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import struct
import subprocess

from devtools import terminal_graphics_native as parent

ROOT=parent.ROOT
INCLUDE=ROOT/'devtools/terminal_input_native.inc'
IMAGE=parent.parent.IMAGE
need,identity,replace=parent.need,parent.identity,parent.replace
PARENT_SHA='98c77b4cdd4416db114e0bc74a285a5657a3e6722ab1c450af924ea715656b62'
PARENT_INCLUDE_SHA='cbb5cb623f80d6b84a43624a0a33b5ab47c11e939c802c47378b52bbdba2e99d'
OPS={'INPUT_GATE':1,'INPUT_BASELINE':2,'INPUT_INSTANCE_INFO':1,'INPUT_CREATE':5,'INPUT_DEVICE':4,
 'INPUT_FORMAT':2,'INPUT_COOPERATIVE':3,'INPUT_PROPERTY':3,'INPUT_DEVICE_INFO':2,'INPUT_ACQUIRE':1,
 'INPUT_UNACQUIRE':1,'INPUT_RELEASE':1,'INPUT_CLIENT_TO_SCREEN':2,'INPUT_CURSOR_POS':2,'INPUT_SHOW_CURSOR':1,
 'INPUT_METRIC':1,'INPUT_DOUBLE_CLICK':0,'INPUT_CURSOR_RESTORE':0,'INPUT_CLOSE':0}
METHODS={20:{2:('INPUT_RELEASE',1),3:('INPUT_DEVICE',4)},
 21:{2:('INPUT_RELEASE',1),7:('INPUT_ACQUIRE',1),8:('INPUT_UNACQUIRE',1),11:('INPUT_FORMAT',2),13:('INPUT_COOPERATIVE',3)},
 22:{2:('INPUT_RELEASE',1),6:('INPUT_PROPERTY',3),7:('INPUT_ACQUIRE',1),8:('INPUT_UNACQUIRE',1),11:('INPUT_FORMAT',2),13:('INPUT_COOPERATIVE',3),15:('INPUT_DEVICE_INFO',2)}}
IMPORTS={0x592050:('INPUT_CREATE',5),0x59235c:('INPUT_CLIENT_TO_SCREEN',2),0x592358:('INPUT_CURSOR_POS',2),
 0x592348:('INPUT_METRIC',1),0x592370:('INPUT_DOUBLE_CLICK',0),0x5923c0:('INPUT_SHOW_CURSOR',1)}
ABI={0x41359a:'e8f1d8ffff',0x410ed0:'e85b000000',0x410ee8:'e8a3000000',0x410f00:'e88b010000',
 0x410f64:'e8154c1100',0x525b7e:'ff2550205900',0x410fdc:'ff510c',0x41100f:'ff512c',
 0x41102b:'6a06',0x411043:'ff5234',0x41106e:'ff521c',0x4110e3:'ff155c235900',0x4110fa:'ff1558235900',
 0x411135:'ff510c',0x411168:'ff512c',0x411187:'6a06',0x41119f:'ff5234',0x4111f6:'ff5018',
 0x411250:'ff503c',0x41126e:'ff501c',0x410ce7:'ff5020',0x410d0b:'ff5120',0x410d2f:'ff5208',
 0x410d5d:'ff5108',0x410d88:'ff5008',0x49de26:'891528277a00',0x42b26b:'ff15c0235900',0x42b294:'ff15c0235900'}


def original_contract():
 raw=IMAGE.read_bytes();need(hashlib.sha256(raw).hexdigest()==parent.parent.IMAGE_SHA,'fixed original input image')
 for va,code in ABI.items():need(raw[va-0x400000:va-0x400000+len(bytes.fromhex(code))].hex()==code,'original input ABI '+hex(va))
 formats=[];guids={0x5cc1bc,0x5cc04c,0x5cc05c}
 for va,want in [(0x5cac3c,(24,16,2,256,256,0x525b90)),(0x5cae44,(24,16,2,20,11,0x526b90))]:
  header=raw[va-0x400000:va-0x400000+24];v=struct.unpack('<6I',header);need(v==want,'original complete input data format')
  objects=raw[v[5]-0x400000:v[5]-0x400000+v[4]*16];need(len(objects)==v[4]*16,'complete object format table')
  rows=[struct.unpack_from('<4I',objects,i*16)for i in range(v[4])]
  guids.update(x[0]for x in rows if x[0]);formats.append(dict(va=va,header_hex=header.hex(),header=list(v),objects_hex=objects.hex(),objects=rows,sha256=hashlib.sha256(header+objects).hexdigest()))
 # Original descriptor table survives even though the PE directory points at a loader IAT.
 imports=[]
 for descriptor,slot,symbol in [(0x1fd5e0,0x592358,'SetCursorPos'),(0x1fd694,0x592050,'DirectInput8Create')]:
  words=struct.unpack_from('<5I',raw,descriptor);index=(slot-0x400000-words[4])//4
  name=struct.unpack_from('<I',raw,words[0]+index*4)[0];actual=raw[name+2:raw.index(b'\0',name+2)].decode('ascii')
  need(actual==symbol,'original import spelling, not resolved alias name')
  imports.append(dict(descriptor_rva=descriptor,descriptor_hex=raw[descriptor:descriptor+20].hex(),slot=slot,index=index,name_rva=name,name=actual))
 return dict(image=identity(IMAGE),ABI=[dict(va=va,hex=code)for va,code in ABI.items()],formats=formats,
  GUIDs=[dict(va=va,hex=raw[va-0x400000:va-0x400000+16].hex())for va in sorted(guids)],original_imports=imports,
  HINSTANCE=dict(original_global=0x7a2728,writer=0x49de26,source='WinMain argument0',
   current_window_module='normal LoadLibraryExW executable image DLL, entry RVA0; not LOAD_LIBRARY_AS_DATAFILE',
   actual_gate='GetModuleHandleExW unchanged-reference identity, MEM_IMAGE, x86 DLL header and owned HWND GWLP_HINSTANCE',
   interpretation='Current declared WinMain creator/resource proxy is retained, never replaced with helper executable. Actual DI HRESULT and compatibility remain unobserved.'),
  cleanup='410CB0: keyboard Unacquire, mouse Unacquire, keyboard Release, mouse Release, factory Release; original HWND remains alive',
  additional_mouse_ABI=dict(DIPROPDWORD_bytes=20,values=[20,16,0,0,1],property_pseudo_guid=2,DIDEVICEINSTANCEA_bytes=580),
  cursor_baseline36='DWORD flags, HCURSOR32, LONG x,y,left,top,right,bottom, DWORD LastInputTick; exact actual comparison to supplied pre-device parent snapshot',
  sources=['https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ee416756(v=vs.85)',
           'https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ee417803(v=vs.85)'])


def constants(contract):
 lines=[]
 for x in contract['GUIDs']:
  b=bytes.fromhex(x['hex']);a,c,d=struct.unpack('<IHH',b[:8]);lines.append('const GUID inputGUID%x={0x%x,0x%x,0x%x,{%s}};'%(x['va'],a,c,d,','.join('0x%02x'%v for v in b[8:])))
 lines.append('const GUID *inputGuid(U32 va){switch(va){'+''.join('case 0x%x:return &inputGUID%x;'%(x['va'],x['va'])for x in contract['GUIDs'])+'default:return nullptr;}}')
 for label,f in zip(('Keyboard','Mouse'),contract['formats']):
  rows=['{%s,%du,0x%xu,0x%xu}'%('&inputGUID%x'%g if g else 'nullptr',offset,kind,flags)for g,offset,kind,flags in f['objects']]
  lines.append('const InputObjectFormat input%sObjects[]={%s};'%(label,','.join(rows)))
  lines.append('const InputDataFormat input%sFormat={24,16,2,%d,%d,input%sObjects};'%(label,f['header'][3],f['header'][4],label))
 return '\n'.join(lines)


def source():
 need(identity(parent.__file__)['sha256']==PARENT_SHA and identity(parent.INCLUDE)['sha256']==PARENT_INCLUDE_SHA,'frozen graphics owner parent')
 c=original_contract();inc=INCLUDE.read_text(encoding='utf8');need(inc.count('@@INPUT_CONSTANTS@@')==1,'one fixed original input table expansion')
 s=parent.source();s=replace(s,'Result dispatch(const Request &q) {',inc.replace('@@INPUT_CONSTANTS@@',constants(c))+'\nResult dispatch(const Request &q) {')
 s=replace(s,'    if (gfxOp(q.op)) return gfxDispatch(q, guard, savedError);',
  '    if (!inputEmpty() && (q.op == "WINDOW_CLOSE" || q.op == "DestroyWindow" || q.op == "WINDOW_MODULE_CLOSE" || q.op == "CoUninitialize" || q.op == "GFX_GATE" || q.op == "GFX_RELEASE" || q.op == "GFX_BASELINE_CLEAR")) return reject("INPUT_RELEASE_AND_CURSOR_RESTORE_BEFORE_PARENT_TEARDOWN", ERROR_BUSY);\n'
  '    if (inputOp(q.op)) return inputDispatch(q, guard, savedError);\n    if (gfxOp(q.op)) return gfxDispatch(q, guard, savedError);')
 s=replace(s,'r.extras = gfxStatus() + " " + gameStatus() + " ui_gate="','r.extras = inputStatus() + " " + gfxStatus() + " " + gameStatus() + " ui_gate="')
 s=replace(s,'if(gfxGate || !gfxEmpty()) return reject("SHUTDOWN_GRAPHICS_RESOURCES_LIVE", ERROR_BUSY);',
  'if(inputGate || !inputEmpty()) return reject("SHUTDOWN_INPUT_RESOURCES_LIVE", ERROR_BUSY);\n            if(gfxGate || !gfxEmpty()) return reject("SHUTDOWN_GRAPHICS_RESOURCES_LIVE", ERROR_BUSY);')
 return s


def self_check():
 contract=original_contract();s=source();before=parent.source()
 for a,b in [('DWORD WINAPI WorkerDispatcher(void *parameter) {','DWORD WINAPI Reader(void *) {'),('DWORD WINAPI Reader(void *) {','\n} // namespace')]:
  need(before[before.index(a):before.index(b,before.index(a))]==s[s.index(a):s.index(b,s.index(a))],'frozen Reader/worker source unchanged')
 need(all('"'+op+'"'in s for op in OPS),'all fixed input operations implemented')
 need('inputGate=false' in s and 'INPUT_GATE_CLOSED' in s,'closed default native input gate')
 need(not re.search(r'\b(?:SendInput|BlockInput|ClipCursor)\s*\(',INCLUDE.read_text()),'no injection/blocking/unproven original clipping API')
 return dict(native_executed=False,desktop_used=False,native_admission=False,contract=contract,operations=OPS,methods=METHODS,
  original_import_slots=IMPORTS,generated_source_sha256=hashlib.sha256(s.encode()).hexdigest(),Reader_worker_unchanged=True,
  limitations=['Build only; actual DirectInput HRESULTs, module compatibility, Acquire/Unacquire/window lifetime and cursor restore are unobserved.',
   'Parent must bind a genuine pre-device baseline and independently authenticate source-linked cleanup receipts; token registration alone is not proof.',
   'No GetDeviceState, runtime polling, artificial keys/clicks, arbitrary GUIDs/format tables, background cooperative flags, or launcher.',
   'Original native resource module remains the declared WinMain creator proxy; live query validates its image identity, not equivalence of all compatibility behavior.',
   'Original input init uses SetCursorPos, confirmed from original descriptor table; resolved-IAT export alias is not used as import spelling.',
   'Clip is captured and compared, never guessed or globally replaced; unexpected clip change refuses owner restoration.',
   'ShowCursor balance is tracked on this MAIN only; cursor restore requires no newer LastInput tick and the original current foreground/window.',
   'LastInput tick is not a complete input-generation proof; full parent recovery remains closed to native admission.'])


def build(folder):
 import pefile
 b=parent.parent.parent.base.parent.parent;folder=Path(folder).resolve()
 need(folder.is_relative_to(ROOT/'.venv-audit') and folder.drive.lower()=='f:' and not folder.exists(),'fresh F input build directory')
 checked=self_check();folder.mkdir(parents=True)
 cpp,exe,obj=[folder/n for n in ('terminal-input-owner.cpp','terminal-input-owner.exe','owner.obj')]
 recipe,log=folder/'build.cmd',folder/'build.log';cpp.write_text(source(),encoding='utf8',newline='\n')
 vcvars=b.VC/'Auxiliary/Build/vcvarsall.bat';compiler=b.MSVC/'bin/Hostx64/x86/cl.exe';linker=b.MSVC/'bin/Hostx64/x86/link.exe'
 recipe.write_text('\n'.join(['@echo off',f'call "{vcvars}" x86 {b.SDK} -vcvars_ver=14.44 >nul','if errorlevel 1 exit /b %errorlevel%',
  f'"{compiler}" /nologo /O2 /W4 /WX /MT /EHsc /std:c++17 /Fe:"{exe}" /Fo:"{obj}" "{cpp}" /link /SUBSYSTEM:WINDOWS /ENTRY:wmainCRTStartup gdi32.lib user32.lib shlwapi.lib ole32.lib comctl32.lib','exit /b %errorlevel%'])+'\n',encoding='utf8',newline='\r\n')
 with log.open('wb')as stream:
  done=subprocess.run([os.environ.get('COMSPEC','cmd.exe'),'/d','/c',str(recipe)],cwd=folder,env=dict(os.environ,TEMP=str(folder),TMP=str(folder)),stdout=stream,stderr=subprocess.STDOUT,timeout=90,creationflags=subprocess.CREATE_NO_WINDOW)
 need(done.returncode==0,'strict input build failed: '+str(log))
 pe=pefile.PE(str(exe));imports={x.dll.decode().lower():[i.name.decode()for i in x.imports]for x in pe.DIRECTORY_ENTRY_IMPORT}
 need(pe.FILE_HEADER.Machine==0x14c and pe.OPTIONAL_HEADER.Subsystem==2,'strict x86 Windows subsystem')
 old=json.loads((ROOT/'.venv-audit/terminal-graphics-owner-build-v3-20261114/static-report.json').read_text())['imports']
 need(set(imports)==set(old),'no added DLL imports; DirectInput8 loaded from System32')
 added={dll:sorted(set(imports[dll])-set(old[dll]))for dll in imports}
 allowed={'user32.dll':{'GetCursorInfo','GetCursorPos','GetClipCursor','GetLastInputInfo','GetForegroundWindow','GetWindowLongW','GetWindowLongPtrW','ClientToScreen','SetCursorPos','ShowCursor','GetSystemMetrics','GetDoubleClickTime'},
          'kernel32.dll':{'GetModuleHandleExW','VirtualQuery'}}
 for dll,names in added.items():need(set(names)<=allowed.get(dll,set()),'only fixed input/runtime qualification imports '+dll)
 report=dict(kind='same_MAIN_DirectInput_original_cursor_build_only',native_executed=False,desktop_used=False,native_admission=False,
  generator=identity(__file__),include=identity(INCLUDE),parent_generator=identity(parent.__file__),parent_include=identity(parent.INCLUDE),
  generated_source=identity(cpp),helper=identity(exe),artifacts=[identity(p)for p in (cpp,exe,obj,recipe,log)],
  dependencies=[identity(p)for p in (vcvars,compiler,linker)],imports=imports,added_imports=added,offline_checks=checked,
  dynamic_runtime=dict(module='dinput8.dll',load_flags=0x800,export='DirectInput8Create'),
  full_native_success=False,formal_acceptance='2/8 unchanged')
 (folder/'static-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8',newline='\n');return report


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--build-dir');a=p.parse_args()
 print(json.dumps(build(a.build_dir)['helper']if a.build_dir else self_check()))
