"""Guest-only bounded own-fixture lifetime and native64 module metadata."""
import ctypes as C
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def main():
    d=Path(sys.argv[1]).resolve()
    if os.environ.get('COMPUTERNAME')!='CHAOMOFA-WORKER' or d.parent!=Path('C:/ChaomofaWorker') or d.name!='kd-cli-wait-v3-20261110' or C.sizeof(C.c_void_p)!=8:
        raise ValueError('owned guest native64 supervisor only')
    if (d/'supervisor.json').exists()or(d/'ready.json').exists():raise ValueError('fresh fixture')
    r=dict(accepted=False,errors=[],phases=[]);p=None;t=time.monotonic()
    def phase(s):
        r['phases'].append(dict(name=s,seconds=time.monotonic()-t))
        (d/'supervisor-progress.json').write_text(json.dumps(r))
    try:
        for i in range(4):(d/('ack-'+str(i))).write_text('continue')
        p=subprocess.Popen([str(d/'fixture.exe'),'--owned-vmm-fixture',str(d)],cwd=d,creationflags=subprocess.CREATE_NO_WINDOW)
        r['pid']=p.pid;phase('fixture started')
        deadline=time.monotonic()+10
        while not(d/'ready.json').exists():
            if p.poll()is not None or time.monotonic()>deadline:raise ValueError('bounded ready deadline')
            time.sleep(.05)
        ready=json.loads((d/'ready.json').read_text());r['ready']=ready
        if ready['pid']!=p.pid:raise ValueError('child identity')
        phase('original fixture ready')
        k=C.WinDLL('kernel32',use_last_error=True);nt=C.WinDLL('ntdll')
        k.OpenProcess.argtypes=[C.c_ulong,C.c_int,C.c_ulong];k.OpenProcess.restype=C.c_void_p
        k.CloseHandle.argtypes=[C.c_void_p];k.CloseHandle.restype=C.c_int
        k.ReadProcessMemory.argtypes=[C.c_void_p,C.c_void_p,C.c_void_p,C.c_size_t,C.POINTER(C.c_size_t)];k.ReadProcessMemory.restype=C.c_int
        nt.NtQueryInformationProcess.argtypes=[C.c_void_p,C.c_ulong,C.c_void_p,C.c_ulong,C.POINTER(C.c_ulong)];nt.NtQueryInformationProcess.restype=C.c_long
        h=k.OpenProcess(0x410,False,p.pid)
        if not h:raise OSError(C.get_last_error(),'own child read open')
        def read(a,n):
            if not 0<a<0x800000000000 or not 0<n<=1024:raise ValueError('bounded user read')
            b=C.create_string_buffer(n);got=C.c_size_t()
            if not k.ReadProcessMemory(h,a,b,n,C.byref(got))or got.value!=n:raise OSError(C.get_last_error(),'exact user read')
            return b.raw
        def word(b,o=0):return int.from_bytes(b[o:o+8],'little')
        def name(b,o):
            size=int.from_bytes(b[o:o+2],'little');maximum=int.from_bytes(b[o+2:o+4],'little')
            if size%2 or not 0<size<=maximum or size>512:raise ValueError('bounded Unicode string')
            return read(word(b,o+8),size).decode('utf-16le')
        try:
            b=C.create_string_buffer(48);got=C.c_ulong()
            if nt.NtQueryInformationProcess(h,0,b,48,C.byref(got))or got.value!=48:raise ValueError('native PBI')
            peb=word(b.raw,8);ldr=word(read(peb+0x18,8));head=ldr+0x10;node=word(read(head,8));seen=set();module=None
            for i in range(64):
                if node==head:break
                if node in seen:raise ValueError('loader cycle')
                seen.add(node);entry=read(node,0x68)
                if name(entry,0x58).lower()=='wow64cpu.dll':
                    path=Path(name(entry,0x48));module=dict(peb=peb,ldr=ldr,entry=node,image_base=word(entry,0x30),path=str(path),size=int.from_bytes(entry[0x40:0x44],'little'),sha256=hashlib.sha256(path.read_bytes()).hexdigest());break
                node=word(entry)
            if module is None:raise ValueError('module absent in bounded native loader list')
            r['module']=module
        finally:
            if not k.CloseHandle(h):raise OSError(C.get_last_error(),'reader handle cleanup')
        phase('module captured')
        (d/'supervisor-ready.json').write_text(json.dumps(dict(ready=ready,module=module)))
        r['exit_code']=p.wait(timeout=60)
        r['fixture_result']=json.loads((d/'result.json').read_text())
        phase('fixture finished')
    except Exception as exc:r['errors'].append(repr(exc))
    finally:
        if p and p.poll()is None:
            (d/'go').write_text('continue')
            try:p.wait(timeout=10)
            except subprocess.TimeoutExpired:p.terminate();p.wait(timeout=5);r['forced_own_fixture_exit']=True
        r['elapsed_seconds']=time.monotonic()-t
        (d/'supervisor.json').write_text(json.dumps(r,indent=2))
    return bool(r['errors'])


if __name__=='__main__':raise SystemExit(main())
