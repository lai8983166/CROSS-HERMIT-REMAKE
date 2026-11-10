"""Compare an owned TCG deferred-invalid fixture against retained hardware bytes."""
import argparse
import ast
import hashlib
import json
import os
import signal
import struct
import subprocess
import time
from pathlib import Path


def image(root):
    tree = ast.parse((root/'devtools/terminal_tcg_predecessor_probe_v3.py').read_text())
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name=='image')
    scope={'struct':struct}
    exec(compile(ast.Module(body=[fn],type_ignores=[]),'<pure-elf>','exec'),scope)
    elf=bytearray(scope['image']())
    def w(x):return struct.pack('<I',x)
    code=bytes.fromhex('66b810008ed88ec08ed0bc004010000f20c083e0f383c8020f22c0')
    code+=bytes.fromhex('dbe3d92d')+w(0x100900)+bytes.fromhex('d9eed9eedef9d935')+w(0x102000)
    code+=bytes.fromhex('dbe3be00201000b91c000000ace6e9e2fbb810000000e7f4f4ebfd')
    elf[4096+0x120:4096+0x120+len(code)]=code
    elf[4096+0x900:4096+0x902]=struct.pack('<H',0x037e)
    return bytes(elf)


def decode(raw):
    if len(raw)!=28:raise ValueError('exact environment required')
    cw,sw,tag=(struct.unpack_from('<H',raw,x)[0]for x in(0,4,8))
    return dict(cw=cw,sw=sw,top=(sw>>11)&7,tag=tag,invalid=bool(sw&1),summary=bool(sw&0x80))


def identity(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())


def run(a):
    root=Path(__file__).resolve().parents[1];out=a.output.resolve()
    if not str(out).startswith('/mnt/f/'):raise ValueError('F output required')
    out.mkdir(exist_ok=False);(out/'guest.elf').write_bytes(image(root))
    args=[str(a.binary.resolve()),'-L',str(a.firmware.resolve()),'-machine','pc','-accel','tcg,thread=single,one-insn-per-tb=on',
          '-smp','2','-m','4G','-display','none','-serial','none','-monitor','none','-nic','none','-no-reboot',
          '-kernel',str(out/'guest.elf'),'-debugcon','file:'+str(out/'env.bin'),'-device','isa-debug-exit,iobase=0xf4,iosize=4',
          '-d','exec,int,nochain','-dfilter','0x100000..0x105000','-D',str(out/'trace.log')]
    r=dict(accepted=False,full57=False,windows_admitted=False,host_input=0,windows_boots=0,
           binary=identity(a.binary),oracle=identity(a.oracle),command=args,errors=[])
    start=time.monotonic()
    with (out/'stderr.txt').open('wb')as stderr:
        p=subprocess.Popen(args,stdout=stderr,stderr=stderr,start_new_session=True)
        while p.poll() is None:
            trace=out/'trace.log'
            if time.monotonic()-start>15 or (trace.exists()and trace.stat().st_size>2*1024**2):
                r['errors'].append('deadline/output bound');os.killpg(p.pid,signal.SIGKILL);break
            time.sleep(.05)
        r['exit_code']=p.wait(timeout=3)
    raw=(out/'env.bin').read_bytes()if(out/'env.bin').exists()else b''
    r['observed']=decode(raw)if len(raw)==28 else None
    r['hardware']=decode(a.oracle.read_bytes())
    r['bounded_case_passed']=r['exit_code']==33 and not r['errors']and r['observed']==r['hardware']
    r['seconds']=time.monotonic()-start;r['process_exited']=p.poll()is not None
    r['files']=[identity(p)for p in out.iterdir()if p.is_file()]
    (out/'report.json').write_text(json.dumps(r,indent=2))
    print(json.dumps({k:v for k,v in r.items()if k not in('files','command')},indent=2))
    return r['bounded_case_passed']


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('binary','firmware','oracle','output'):p.add_argument('--'+name,type=Path,required=True)
    raise SystemExit(not run(p.parse_args()))
