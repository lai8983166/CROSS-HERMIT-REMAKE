"""Bounded register-division comparisons with actual retained hardware state."""
import argparse
import ast
import json
import os
import signal
import struct
import subprocess
import time
from pathlib import Path
from devtools.terminal_tcg_unmasked_probe import identity

CASES={'invalid-unmasked':(0x37e,'d9ee'),'zero-unmasked':(0x37b,'d9e8'),
       'invalid-masked':(0x37f,'d9ee'),'zero-masked':(0x37f,'d9e8'),
       'normal-forward':(0x37f,'d90504091000'),'normal-reverse':(0x37f,'d90504091000')}

def image(root,case):
    cw,first=CASES[case]
    tree=ast.parse((root/'devtools/terminal_tcg_predecessor_probe_v3.py').read_text())
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='image')
    scope={'struct':struct}
    exec(compile(ast.Module(body=[fn],type_ignores=[]),'<pure-elf>','exec'),scope)
    elf=bytearray(scope['image']())
    def w(x):return struct.pack('<I',x)
    code=bytes.fromhex('66b810008ed88ec08ed0bc004010000f20c083e0f383c8220f22c00f20e00d000200000f22e0')
    second='d90508091000' if case.startswith('normal-') else 'd9ee'
    operation='def1' if case=='normal-reverse' else 'def9'
    code+=bytes.fromhex('dbe3d92d')+w(0x100900)+bytes.fromhex(first+second+operation+'d935')+w(0x102000)
    code+=bytes.fromhex('0fae05')+w(0x102200)+bytes.fromhex('dbe3')
    for address,count in((0x102000,28),(0x102200,512)):
        code+=b'\xbe'+w(address)+b'\xb9'+w(count)+bytes.fromhex('ace6e9e2fb')
    code+=bytes.fromhex('b810000000e7f4f4ebfd')
    elf[4096+0x120:4096+0x120+len(code)]=code
    elf[4096+0x900:4096+0x902]=struct.pack('<H',cw)
    elf[4096+0x904:4096+0x90c]=struct.pack('<ff',8.,2.)
    return bytes(elf)

def decode(raw):
    if len(raw)!=540:raise ValueError('exact 540-byte hardware comparison frame required')
    cw,sw,tag=(struct.unpack_from('<H',raw,x)[0]for x in(0,4,8))
    top=(sw>>11)&7
    fp={str(p):raw[28+32+((p-top)&7)*16:28+42+((p-top)&7)*16].hex()
        for p in range(8)if(tag>>(2*p))&3!=3}
    return dict(cw=cw,sw=sw,top=top,tag=tag,nonempty_physical_fp80=fp)

def run(a):
    root=Path(__file__).resolve().parents[1];out=a.output.resolve()
    if not str(out).startswith('/mnt/f/'):raise ValueError('F output required')
    out.mkdir(exist_ok=False);(out/'guest.elf').write_bytes(image(root,a.case))
    args=[str(a.binary.resolve()),'-L',str(a.firmware.resolve()),'-machine','pc','-accel','tcg,thread=single,one-insn-per-tb=on',
          '-smp','2','-m','4G','-display','none','-serial','none','-monitor','none','-nic','none','-no-reboot',
          '-kernel',str(out/'guest.elf'),'-debugcon','file:'+str(out/'state.bin'),'-device','isa-debug-exit,iobase=0xf4,iosize=4',
          '-d','exec,int,nochain','-dfilter','0x100000..0x105000','-D',str(out/'trace.log')]
    r=dict(accepted=False,full57=False,windows_admitted=False,host_input=0,windows_boots=0,case=a.case,
           binary=identity(a.binary),oracle=identity(a.oracle),command=args,errors=[],deadline_seconds=15,trace_budget_bytes=2*1024**2)
    start=time.monotonic()
    with (out/'stderr.txt').open('wb')as stderr:
        p=subprocess.Popen(args,stdout=stderr,stderr=stderr,start_new_session=True)
        while p.poll() is None:
            trace=out/'trace.log'
            if time.monotonic()-start>15 or (trace.exists()and trace.stat().st_size>2*1024**2):
                r['errors'].append('deadline/output bound');os.killpg(p.pid,signal.SIGKILL);break
            time.sleep(.05)
        r['exit_code']=p.wait(timeout=3)
    raw=(out/'state.bin').read_bytes()if(out/'state.bin').exists()else b''
    r['observed']=decode(raw)if len(raw)==540 else None;r['hardware']=decode(a.oracle.read_bytes())
    r['bounded_case_passed']=r['exit_code']==33 and not r['errors']and r['observed']==r['hardware']
    r['seconds']=time.monotonic()-start;r['process_exited']=p.poll()is not None
    r['files']=[identity(p)for p in out.iterdir()if p.is_file()]
    (out/'report.json').write_text(json.dumps(r,indent=2))
    print(json.dumps({k:v for k,v in r.items()if k not in('files','command')},indent=2))
    return r['bounded_case_passed']

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in('binary','firmware','oracle','output'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--case',choices=CASES,required=True)
    raise SystemExit(not run(p.parse_args()))
