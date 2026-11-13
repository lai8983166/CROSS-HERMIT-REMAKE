"""Build-only and bounded symbolic original publication with texture re-lock checks."""
from __future__ import annotations
import argparse,gzip,json,os,subprocess,time
from pathlib import Path
from devtools import terminal_texture_native as native
from devtools.terminal_texture_platform import TextureEngine,base,need
from devtools.terminal_texture_model import TextureModel
from devtools.terminal_input_platform import cleanup_after_publication
from devtools.terminal_input_model import CURSOR
from devtools.terminal_game_platform import begin_original_game
from devtools.terminal_graphics_model import checks as graphics_checks,CAPS_SOURCE
from devtools.review_terminal_input_platform import audit as input_audit

ROOT=base.ROOT

def build(folder):
    import pefile
    from devtools.terminal_scene_native_extension import VC,MSVC,SDK
    folder=(ROOT/folder).resolve();need(folder.is_relative_to(ROOT/'.venv-audit') and not folder.exists(),'fresh F texture build')
    checked=native.self_check();folder.mkdir();cpp=folder/'terminal-texture-owner.cpp';exe=folder/'terminal-texture-owner.exe';obj=folder/'owner.obj';recipe=folder/'build.cmd';log=folder/'build.log'
    cpp.write_text(native.source(),encoding='utf8',newline='\n');vcvars=VC/'Auxiliary/Build/vcvarsall.bat';compiler=MSVC/'bin/Hostx64/x86/cl.exe';linker=MSVC/'bin/Hostx64/x86/link.exe'
    recipe.write_text('\n'.join(['@echo off',f'call "{vcvars}" x86 {SDK} -vcvars_ver=14.44 >nul','if errorlevel 1 exit /b %errorlevel%',f'"{compiler}" /nologo /O2 /W4 /WX /MT /EHsc /std:c++17 /Fe:"{exe}" /Fo:"{obj}" "{cpp}" /link /SUBSYSTEM:WINDOWS /ENTRY:wmainCRTStartup gdi32.lib user32.lib shlwapi.lib ole32.lib comctl32.lib','exit /b %errorlevel%'])+'\n',encoding='utf8',newline='\r\n')
    with log.open('wb')as stream:done=subprocess.run([os.environ.get('COMSPEC','cmd.exe'),'/d','/c',str(recipe)],cwd=folder,env=dict(os.environ,TEMP=str(folder),TMP=str(folder)),stdout=stream,stderr=subprocess.STDOUT,timeout=90,creationflags=subprocess.CREATE_NO_WINDOW)
    need(done.returncode==0,'strict texture build failed: '+str(log));pe=pefile.PE(str(exe));imports={x.dll.decode().lower():[i.name.decode()for i in x.imports]for x in pe.DIRECTORY_ENTRY_IMPORT}
    old=json.loads((ROOT/'.venv-audit/terminal-input-owner-build-v2-20261114/static-report.json').read_text())['imports'];need(set(imports)==set(old),'same imported DLLs')
    added={dll:sorted(set(imports[dll])-set(old[dll]))for dll in imports}
    for dll,names in added.items():need(set(names)<=({'ReadProcessMemory','GetCurrentProcess'} if dll=='kernel32.dll' else set()),'only own locked texture read import added')
    need(pe.FILE_HEADER.Machine==0x14c and pe.OPTIONAL_HEADER.Subsystem==2,'x86 no-console helper')
    r=dict(kind='same_MAIN_texture_relock_build_only',native_executed=False,desktop_used=False,helper=base.identity(exe),generated_source=base.identity(cpp),generator=base.identity(Path(__file__)),native_generator=base.identity(Path(native.__file__)),include=base.identity(native.INCLUDE),parent=checked['parent'],parent_include=checked['parent_include'],artifacts=[base.identity(p)for p in (cpp,exe,obj,recipe,log)],dependencies=[native.identity(p)for p in (vcvars,compiler,linker)],imports=imports,added_imports=added,checks=checked)
    (folder/'static-report.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf8',newline='\n');return r

def model(path):
    out=(ROOT/path).resolve();need(out.is_relative_to(ROOT/'.venv-audit') and not out.exists(),'fresh F bounded texture model')
    template=ROOT/'analysis/school-window-startup-trajectory-v3-20261020.json';need(base.sha(template.read_bytes())=='a5f30898f2add507e70277617838ad51e5328b56915c227460e3bc43f2afcd48','fixed creation template')
    e=TextureEngine();m=TextureModel(e,json.loads(template.read_text())['cases'][0]);m.engine=e;start=time.monotonic()
    sources=['devtools/prove_terminal_texture.py','devtools/terminal_texture_platform.py','devtools/terminal_texture_model.py','devtools/terminal_texture_native.py','devtools/terminal_texture_native.inc','devtools/terminal_input_platform.py','devtools/terminal_input_model.py','devtools/terminal_graphics_platform.py','devtools/terminal_graphics_model.py']
    r=dict(kind='symbolic_original_GAME_with_post_unlock_readback',native_executed=False,desktop_used=False,ready_for_native=False,formal_acceptance=False,implementation=[base.identity(ROOT/p)for p in sources],capability_input=base.identity(ROOT/CAPS_SOURCE),symbolic_inputs='Frozen input/graphics model values remain symbolic; TEX_VERIFY reads model persistent pixels after original Unlock and returns declared success HRESULTs. No real GPU, desktop, input, gamma or glyph observation.')
    try:
        begin_original_game(e,m,0x413450);game=e.reg('ECX');m.call('GFX_GATE',1);token=m.call('MEM_ALLOC',32)['result'];m.call('MEM_WRITE',token,'ab'*32);m.call('GFX_BASELINE',token)
        m.call('INPUT_GATE',1);cursor=m.call('MEM_ALLOC',36)['result'];m.call('MEM_WRITE',cursor,CURSOR.hex());m.call('INPUT_BASELINE',token,cursor);m.call('MEM_FREE',cursor);m.call('MEM_FREE',token)
        e.stop=0x4506eb;e.done[0]=False;e.drive();e.checkpoint('original_GAME_publication_after_input')
        need(e.reg('EIP')==0x4506eb and e.word(0x7a49fc)==game and 0x4506e9 in e.sites,'original successful GAME publication')
        r['published_GAME']=game;r['cleanup']=cleanup_after_publication(e,m,game)
        need(all(r['cleanup']['status'][key]==0 for key in ('texture_verify_pending','texture_verify_failed')),'new actual texture obligation ledger empty')
        need(len(e.texture_verifications)==2 and all(x['accepted'] and x['temporary_freed'] and x['CPU57_restored'] and len(x['CPU57_before'])==57 and x['CPU57_before']==x['CPU57_after'] for x in e.texture_verifications),'two original font uploads verified with full state restoration')
        r['reached']=True
    except BaseException as exc:r.update(reached=False,failure=repr(exc))
    r.update(seconds=round(time.monotonic()-start,3),instructions=e.count,final=e.state(),API_calls=e.records,callbacks=e.callbacks,roots=e.roots,native_trace=m.trace,checkpoints=e.checkpoints,texture_verifications=e.texture_verifications,instruction_sites=[dict(pc=p,hex=e.image[p-0x400000:p-0x400000+n].hex(),count=c)for p,(n,c)in sorted(e.sites.items())],limits=dict(seconds=90,instructions=6000000,compressed_bytes=8*1024*1024),native_cleanup_qualified=False,worker_created=False,wait_return=False,result_consumed=False)
    if r['reached']:r['graphics_regressions']=graphics_checks(r);r['input_record_revalidation']=input_audit(r)
    raw=gzip.compress(json.dumps(r,separators=(',',':')).encode(),mtime=0);need(len(raw)<8*1024*1024,'bounded compressed texture evidence');out.write_bytes(raw)
    return dict(output=base.identity(out),reached=r['reached'],failure=r.get('failure'),seconds=r['seconds'],instructions=e.count,verifications=len(e.texture_verifications),pc=hex(e.reg('EIP')))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True);g.add_argument('--build-dir');g.add_argument('--model-out');a=p.parse_args();r=build(a.build_dir)if a.build_dir else model(a.model_out);print(json.dumps(r['helper']if a.build_dir else r));raise SystemExit(0 if a.build_dir or r['reached'] else 1)
