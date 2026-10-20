"""Fresh owned x86 client-rectangle and ordinary creation callback capture."""
import json
import struct
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tools.school_window_module import RESOURCE_DLL,inspect_module,resource_bytes
from tools.school_d3d8_bridge import LiveD3D8, ROOT, COMPILER, sha, machine

SOURCE=ROOT/'tools/school_window_create_platform.cs'
HELPER=ROOT/'.venv-audit/school-window-create-platform-v1.exe'
WORKDIR=ROOT/'CROSS HERMIT/CROSS HERMIT'


from tools.school_window_callback_platform import CallbackBoundary


def build():
    if HELPER.exists():raise ValueError('fresh immutable main-context helper required')
    p=subprocess.run([str(COMPILER),'/nologo','/platform:x86','/r:System.Web.Extensions.dll',
        '/out:'+str(HELPER),str(SOURCE)],capture_output=True,timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
    if p.returncode:raise RuntimeError((p.stdout+p.stderr).decode('cp936',errors='replace'))
    return dict(source_sha256=sha(SOURCE.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),
        helper_sha256=sha(HELPER.read_bytes()),machine=machine(HELPER))


class CreatePlatform(LiveD3D8):
    def __init__(self):
        if machine(HELPER)!=0x14C:raise ValueError('real x86 main-context helper required')
        inspect_module(RESOURCE_DLL.read_bytes())
        self.process=subprocess.Popen([str(HELPER),str(RESOURCE_DLL)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,text=True,encoding='utf8',cwd=WORKDIR,creationflags=subprocess.CREATE_NO_WINDOW)
        self.reader=ThreadPoolExecutor(max_workers=1)
        self.sequence,self.closed,self.trace,self.cleanup=0,False,[],None
        self.callback_packets=[]
        self.wire=[];self.callback_handler=None;self.abort_proof=None
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

    def request(self,op,**args):
        if self.closed:raise ValueError('class helper closed')
        r=dict(id=self.sequence+1,op=op,**args);line=json.dumps(r,separators=(',',':'))
        if len(line)>8192:raise ValueError('bounded class request')
        self.sequence+=1
        try:
            self.wire.append(dict(direction='request',value=r));self.process.stdin.write(line+'\n');self.process.stdin.flush()
            while True:
                reply=self._read();self.wire.append(dict(direction='response',value=reply))
                if reply.get('event_kind')!='wndproc':break
                self.callback_packets.append(reply)
                if self.callback_handler is None:raise CallbackBoundary(reply,'callback executor not admitted')
                value=self.callback_handler(reply)
                response=dict(op='callback_return',callback_id=reply['callback_id'],result=value)
                self.wire.append(dict(direction='callback_return',value=response))
                self.process.stdin.write(json.dumps(response,separators=(',',':'))+'\n');self.process.stdin.flush()
            self.trace.append(dict(request=r,reply=reply))
            if reply.get('id')!=r['id']:raise RuntimeError('class helper sequence')
        except CallbackBoundary as boundary:
            self._terminate()
            self.abort_proof=dict(owned_process_exited=self.process.poll() is not None,exit_code=self.process.returncode,
                reason=boundary.reason,pending_callback=boundary.packet,unanswered=True,explicit_cleanup_performed=False,
                CreateWindowExA_return_received=False,normal_class_unregistration_performed=False)
            raise
        except BaseException:self._terminate();raise
        if reply.get('ok') is not True:raise ValueError(reply.get('error','class helper refused'))
        return reply['result']
