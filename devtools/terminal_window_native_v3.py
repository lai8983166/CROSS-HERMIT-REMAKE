"""Build-only correction of GetProp absence bookkeeping; frozen v2 is retained."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
from devtools import terminal_window_native_v2 as parent

ROOT, base = parent.ROOT, parent.base
need, identity = parent.need, parent.identity
PARENT_SHA = 'eaf079888f8543b27efccbde2caae702111e255a19a5fbcf2db3d9bd275ccd2f'
CASE = ROOT/'.venv-audit/terminal-window-destruction-build-v1-20261114/native-window-case-v1.json.gz'
CASE_SHA = 'b0ca313f94e737821eac86dae289a5b4cedc80afdc015079c81977fbd1cb5175'
OLD = 'if(r.value == windowGuestOwner && !observed && !error) windowPropertyRemoved=true;'
NEW = 'if(removedOwnedProperty(windowGuestOwner, r.value, observed)) windowPropertyRemoved=true;'
PREDICATE = r'''// GetPropA defines absent properties by NULL, not GetLastError()==0.
// The auxiliary error is still recorded; original leaf LastError is restored.
constexpr bool removedOwnedProperty(U32 owner, U32 removed, U32 observed) {
    return owner != 0 && removed == owner && observed == 0;
}
static_assert(removedOwnedProperty(1348472864u,1348472864u,0), "recorded owner removed");
static_assert(!removedOwnedProperty(0,0,0), "nonzero bound owner required");
static_assert(!removedOwnedProperty(1348472864u,0,0), "failed RemoveProp rejected");
static_assert(!removedOwnedProperty(1348472864u,1348472865u,0), "foreign owner rejected");
static_assert(!removedOwnedProperty(1348472864u,1348472864u,1348472864u), "live property rejected");
static_assert(!removedOwnedProperty(1348472864u,1348472864u,1), "foreign property rejected");
'''


def source():
    need(identity(parent.__file__)['sha256'] == PARENT_SHA, 'frozen executed v2 generator')
    s = parent.source()
    s = parent.replace(s, 'bool windowGate = false,', PREDICATE+'bool windowGate = false,')
    return parent.replace(s, OLD, NEW)


def self_check():
    inherited = parent.self_check()
    data = CASE.read_bytes()
    need(hashlib.sha256(data).hexdigest() == CASE_SHA, 'exact sole failed native source')
    case = json.loads(gzip.decompress(data))
    calls = [r for c in case['callbacks'] for r in c['API_calls']]
    removed = [r for r in calls if r['name'] == 'RemovePropA']
    need(len(removed) == 1, 'one original property removal')
    leaf = removed[0]['native_leaf']
    need(removed[0]['ret'] == 0x42495e and leaf['id'] == 397 and leaf['ok'] == 1,
         'original removal call site and actual success receipt')
    need(leaf['result'] == 1348472864 and leaf['observed_property'] == 0 and
         leaf['observed_property_error'] == 2 and leaf['last_error'] == 0,
         'recorded nonzero owner, absent readback, distinct auxiliary error')
    need(not case['accepted'] and case['cleanup']['forced'] and case['desktop_restored'],
         'failed native case remains failed, containment distinct from normal cleanup')
    before, after = parent.source(), source()
    need(after.replace(PREDICATE, '', 1).replace(NEW, OLD, 1) == before,
         'only property predicate and compile-time assertions changed')
    return dict(native_executed=False, parent_checks=inherited,
        regression_source=identity(CASE), recorded_remove_receipt=leaf,
        compiled_assertions=6, exact_two_source_edits=True,
        source_sha256=hashlib.sha256(after.encode()).hexdigest(),
        original_last_error_and_aux_error_preserved=True,
        all_other_native_ownership_and_cleanup_guards_unchanged=True,
        failed_case_reclassified=False, normal_native_cleanup_proven=False,
        contract_references=[
            'https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getpropa',
            'https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-removepropa'])


def build(folder):
    import pefile
    b = base.parent.parent
    folder = Path(folder).resolve()
    need(folder.is_relative_to(ROOT/'.venv-audit') and folder.drive.lower() == 'f:' and not folder.exists(), 'fresh F build')
    checked = self_check()
    folder.mkdir(parents=True)
    cpp, exe, obj = [folder/n for n in ('terminal-window-destruction-owner.cpp', 'terminal-window-destruction-owner.exe', 'owner.obj')]
    recipe, log = folder/'build.cmd', folder/'build.log'
    cpp.write_text(source(), encoding='utf-8', newline='\n')
    vcvars = b.VC/'Auxiliary/Build/vcvarsall.bat'
    compiler, linker = [b.MSVC/'bin/Hostx64/x86'/n for n in ('cl.exe', 'link.exe')]
    recipe.write_text('\n'.join(['@echo off', f'call "{vcvars}" x86 {b.SDK} -vcvars_ver=14.44 >nul',
        'if errorlevel 1 exit /b %errorlevel%',
        f'"{compiler}" /nologo /O2 /W4 /WX /MT /EHsc /std:c++17 /Fe:"{exe}" /Fo:"{obj}" "{cpp}" /link /SUBSYSTEM:WINDOWS /ENTRY:wmainCRTStartup gdi32.lib user32.lib shlwapi.lib',
        'exit /b %errorlevel%'])+'\n', encoding='utf-8', newline='\r\n')
    env = dict(os.environ, TEMP=str(folder), TMP=str(folder))
    with log.open('wb') as stream:
        done = subprocess.run([env.get('COMSPEC', 'cmd.exe'), '/d', '/c', str(recipe)],
            cwd=folder, env=env, stdout=stream, stderr=subprocess.STDOUT, timeout=90,
            creationflags=subprocess.CREATE_NO_WINDOW)
    need(done.returncode == 0, 'warnings-as-errors build failed: '+str(log))
    pe = pefile.PE(str(exe))
    imports = {x.dll.decode().lower(): [i.name.decode() for i in x.imports] for x in pe.DIRECTORY_ENTRY_IMPORT}
    need(pe.FILE_HEADER.Machine == 0x14c and pe.OPTIONAL_HEADER.Subsystem == 2, 'x86 Windows subsystem')
    need(set(imports) == {'kernel32.dll', 'gdi32.dll', 'user32.dll', 'shlwapi.dll'}, 'bounded DLL imports')
    need(set(imports['user32.dll']) == base.USER_IMPORTS|{'SendMessageA'} and
         set(imports['gdi32.dll']) == base.GDI_IMPORTS, 'no added desktop APIs')
    report = dict(kind='same_owner_window_property_absence_fix_build', native_executed=False,
        generator=identity(__file__), generated_source=identity(cpp), helper=identity(exe),
        inputs=[identity(p) for p in (parent.__file__, base.__file__, base.INCLUDE, base.RESOURCE)],
        artifacts=[identity(p) for p in (cpp, exe, obj, recipe, log)],
        dependencies=[identity(p) for p in (vcvars, compiler, linker, b.KIT/f'Include/{b.SDK}/um/WinUser.h')],
        imports=imports, offline_checks=checked, normal_window_cleanup_observed=False)
    (folder/'static-report.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8', newline='\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-dir')
    args = parser.parse_args()
    print(json.dumps(build(args.build_dir)['helper'] if args.build_dir else self_check()))
