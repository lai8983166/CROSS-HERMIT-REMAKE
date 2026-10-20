"""Fresh owned x86 class registration with dormant stdcall callback transport."""
import json
import struct
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tools.school_window_module import RESOURCE_DLL,inspect_module,resource_bytes
from tools.school_d3d8_bridge import LiveD3D8, ROOT, COMPILER, sha, machine

SOURCE=ROOT/'tools/school_window_class_platform.cs'
HELPER=ROOT/'.venv-audit/school-window-class-platform-v1.exe'
WORKDIR=ROOT/'CROSS HERMIT/CROSS HERMIT'


def build():
    if HELPER.exists():raise ValueError('fresh immutable main-context helper required')
    p=subprocess.run([str(COMPILER),'/nologo','/platform:x86','/r:System.Web.Extensions.dll',
        '/out:'+str(HELPER),str(SOURCE)],capture_output=True,timeout=30,creationflags=subprocess.CREATE_NO_WINDOW)
    if p.returncode:raise RuntimeError((p.stdout+p.stderr).decode('cp936',errors='replace'))
    return dict(source_sha256=sha(SOURCE.read_bytes()),compiler_sha256=sha(COMPILER.read_bytes()),
        helper_sha256=sha(HELPER.read_bytes()),machine=machine(HELPER))


class ClassPlatform(LiveD3D8):
    def __init__(self):
        if machine(HELPER)!=0x14C:raise ValueError('real x86 main-context helper required')
        inspect_module(RESOURCE_DLL.read_bytes())
        self.process=subprocess.Popen([str(HELPER),str(RESOURCE_DLL)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,text=True,encoding='utf8',cwd=WORKDIR,creationflags=subprocess.CREATE_NO_WINDOW)
        self.reader=ThreadPoolExecutor(max_workers=1)
        self.sequence,self.closed,self.trace,self.cleanup=0,False,[],None
        self.callback_packets=[]
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
            self.process.stdin.write(line+'\n');self.process.stdin.flush();reply=self._read()
            if reply.get('event_kind')=='wndproc':
                self.callback_packets.append(reply)
                # This registration-only helper exposes no window-creation operation.
                # Never supply a constant/DefWindowProc stand-in for original424980.
                raise RuntimeError('unexpected callback: original guest dispatcher not yet admitted')
            self.trace.append(dict(request=r,reply=reply))
            if reply.get('id')!=self.sequence:raise RuntimeError('class helper sequence')
        except BaseException:self._terminate();raise
        if reply.get('ok') is not True:raise ValueError(reply.get('error','class helper refused'))
        return reply['result']


def verify_registration(r,guest):
    from tools.school_window_class import CALLBACK,window,NAME_BYTES
    if r['guest_hex']!=guest.hex() or r['class_name_hex']!=NAME_BYTES.hex():raise ValueError('class original registration input')
    host=bytearray(guest);ledger=r['pointer_translations']
    if len(ledger)!=2:raise ValueError('class exact two host translations')
    for row,offset,value in zip(ledger,(8,40),(CALLBACK,window.TITLE)):
        if set(row)!={'offset','guest','host'} or row['offset']!=offset or row['guest']!=value or type(row['host']) is not int or not 65536<=row['host']<=0xFFFFFFFF:
            raise ValueError('class owned host pointer translation')
        struct.pack_into('<I',host,offset,row['host'])
    if r['host_hex']!=host.hex() or r['result']!=r['eax_bits_observed'] or r['atom']!=r['result']&0xFFFF or not 0<r['atom']<65536:
        raise ValueError('class actual result/low-word atom/host input')
    if r['preflight']['result']!=0:raise ValueError('class actual absence before registration')
    for name in ('by_atom','by_name'):
        q=r[name];raw=bytearray.fromhex(q['hex'])
        if not q['result'] or not q['guards_unchanged'] or len(raw)!=48:raise ValueError('class actual post-registration query')
        key=struct.unpack_from('<I',raw,40)[0]
        if name=='by_atom' and key==r['atom']:
            if q['class_name'] is not None:raise ValueError('class atom-valued name field is not a string')
        elif q['class_name']!='Cross Hermit' or not 65536<=key<=0xFFFFFFFF:raise ValueError('class OS string pointer/name')
        raw[40:44]=host[40:44]
        if raw!=host:raise ValueError('class exact queried semantic fields')
    if not r['forwarder_freed'] or not r['guards_unchanged'] or not r['guest_class_unchanged'] or r['callback_calls']!=0 or r['window_created']:
        raise ValueError('class raw input/ownership/dormant callback boundary')
    if r['native_return_type']!='ATOM' or r['callback_transport']!='stdcall IPC requires original guest result; no fallback':raise ValueError('class native result/transport type')
    code=bytes.fromhex(r['forwarder_hex'])
    if len(code)!=19 or code[:7]!=bytes.fromhex('558becff7508b8') or code[11:]!=bytes.fromhex('ffd08be55dc20400') or not struct.unpack_from('<I',code,7)[0]:raise ValueError('class actual EAX-capture forwarder')
    if type(r['last_error']) is not int:raise ValueError('class GetLastError observation')
    return dict(atom=r['atom'],guest_class_unchanged=True,pointer_translations=2,actual_queries=2,callback_calls=0,window_created=False)


def verify_unregistration(r,atom):
    if r['atom']!=atom or not r['result'] or not r['callback_retained_until_unregister'] or not r['class_storage_freed']:
        raise ValueError('class owned unregister lifetime')
    q=r['query_after']
    if q['result']!=0 or q['class_name'] is not None or not q['guards_unchanged'] or bytes.fromhex(q['hex'])!=struct.pack('<12I',48,*([0]*11)):
        raise ValueError('class actual absence after unregister')
    return True
