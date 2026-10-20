"""Fresh owned x86 main-context helper; observations cannot resume expired objects."""
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tools.school_window_module import RESOURCE_DLL,inspect_module,resource_bytes
from tools.school_d3d8_bridge import LiveD3D8, ROOT, COMPILER, sha, machine

SOURCE=ROOT/'tools/school_window_module_platform.cs'
HELPER=ROOT/'.venv-audit/school-window-module-platform-v1.exe'
WORKDIR=ROOT/'CROSS HERMIT/CROSS HERMIT'


def build():
    if HELPER.exists():raise ValueError('fresh immutable main-context helper required')
    p=subprocess.run([str(COMPILER),'/nologo','/platform:x86','/r:System.Web.Extensions.dll',
        '/out:'+str(HELPER),str(SOURCE)],capture_output=True,timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
    if p.returncode:raise RuntimeError((p.stdout+p.stderr).decode('cp936',errors='replace'))
    return dict(source_sha256=sha(SOURCE.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),
        helper_sha256=sha(HELPER.read_bytes()),machine=machine(HELPER))


class ModulePlatform(LiveD3D8):
    def __init__(self):
        if machine(HELPER)!=0x14C:raise ValueError('real x86 main-context helper required')
        inspect_module(RESOURCE_DLL.read_bytes())
        self.process=subprocess.Popen([str(HELPER),str(RESOURCE_DLL)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,text=True,encoding='utf8',cwd=WORKDIR,creationflags=subprocess.CREATE_NO_WINDOW)
        self.reader=ThreadPoolExecutor(max_workers=1)
        self.sequence,self.closed,self.trace,self.cleanup=0,False,[],None
        try:
            r=self._read()
            if r.get('ok') is not True or r.get('id')!=0:raise RuntimeError(r)
            self.hello=r['hello']
            if self.hello['pointer_bytes']!=4 or self.hello['window_created'] is not False:raise ValueError('main helper ABI')
            if Path(self.hello['working_directory']).resolve()!=WORKDIR.resolve():raise ValueError('main declared helper cwd')
            module=self.hello['resource_module']
            if module['entry_point']!=0 or module['sha256']!=sha(RESOURCE_DLL.read_bytes()) or Path(module['path']).resolve()!=RESOURCE_DLL.resolve():raise ValueError('actual resource module identity')
            if type(module['pointer']) is not int or not 0<module['pointer']<=0xFFFFFFFF:raise ValueError('actual x86 module handle')
            for row in module['resources']:
                blob=resource_bytes()[(row['type_id'],row['id'],row['language'])]
                if bytes.fromhex(row['hex'])!=blob or row['sha256']!=sha(blob):raise ValueError('actual loaded source resource bytes')
            self.module=module['pointer']
            self.provenance={}
            for key in ('kernel32_path','shlwapi_path','user32_path','gdi32_path'):
                reported=Path(self.hello[key]);actual=reported
                # GetModuleFileName in WOW64 reports System32; the 64-bit auditor must
                # read the redirected x86 file explicitly, never hash its x64 twin.
                if reported.parent.name.lower()=='system32' and machine(reported)==0x8664:
                    actual=reported.parent.parent/'SysWOW64'/reported.name
                self.provenance[key]=dict(reported_path=str(reported),path=str(actual),
                    sha256=sha(actual.read_bytes()),machine=machine(actual),
                    WOW64_file_redirection_explicit=actual!=reported)
            if any(r['machine']!=0x14C for r in self.provenance.values()):raise ValueError('main actual x86 system modules')
        except BaseException:self._terminate();raise
