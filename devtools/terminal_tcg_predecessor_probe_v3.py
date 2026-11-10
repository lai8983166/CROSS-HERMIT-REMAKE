"""Bounded diskless TCG event microguest. Not Windows or full-state acceptance."""
import json,struct,subprocess,time
from pathlib import Path
from devtools.isolated_windows_vm import WORKER,VMX,vmrun,identity,environment
from devtools.isolated_vm_bounded_query_v3 import _supervise,runtime_paths,completed

def image():
    base=0x100000;m=bytearray(4096)
    def word(v):return struct.pack('<I',v)
    def put(off,b):m[off:off+len(b)]=b
    def emit(c):return bytes([0xb0,ord(c),0xe6,0xe9])
    put(0,struct.pack('<III',0x1badb002,0,(-0x1badb002)&0xffffffff))
    put(0x800,bytes.fromhex('0000000000000000ffff0000009bcf00ffff00000093cf00'))
    put(0x820,struct.pack('<HI',23,base+0x800));put(0x828,struct.pack('<HI',0x7ff,base+0x1000))
    # IDT lives in zero-filled ELF bss; vector1 gate is installed by guest stores.
    start=bytes.fromhex('fa0f0115')+word(base+0x820)+b'\xea'+word(base+0x120)+bytes.fromhex('0800')
    put(0x100,start)
    code=bytes.fromhex('66b810008ed88ec08ed0bc00401000')
    gate=struct.pack('<HHBBH',(base+0x400)&0xffff,8,0,0x8e,(base+0x400)>>16)
    for offset in (0,4):code+=bytes.fromhex('c705')+word(base+0x1008+offset)+gate[offset:offset+4]
    code+=bytes.fromhex('0f011d')+word(base+0x828)
    code+=b'\xb8'+word(base+0x305)+bytes.fromhex('0f23c0b8010400000f23f8')
    code+=emit('S');code+=b'\xe9'+word((base+0x300)-(base+0x120+len(code)+5))
    put(0x120,code)
    put(0x300,b'\xe8'+word((base+0x380)-(base+0x305)))
    end=emit('R')+bytes.fromhex('a0')+word(base+0x2000)+bytes.fromhex('0430e6e9')+emit('E')+bytes.fromhex('b810000000e7f4f4ebfd')
    put(0x305,end);put(0x380,emit('H')+b'\xc3')
    handler=bytes.fromhex('60ff05')+word(base+0x2000)+emit('D')+bytes.fromhex('8d742420b90c000000ace6e9e2fb0f21f05089e6b904000000ace6e9e2fb58814c24280000010061cf')
    put(0x400,handler)
    elf=bytearray(4096);elf[:16]=bytes.fromhex('7f454c46010101000000000000000000')
    elf[16:52]=struct.pack('<HHIIIIIHHHHHH',2,3,1,base+0x100,52,0,0,52,32,1,0,0,0)
    elf[52:84]=struct.pack('<IIIIIIII',1,4096,base,base,len(m),0x5000,7,4096)
    return bytes(elf+m)

def run():
    d=WORKER/'tcg-predecessor-v3-20261110';d.mkdir(exist_ok=False)
    root=WORKER/'qemu-worker/runtime';exe=root/'qemu-system-x86_64.exe'
    manifest=json.loads((WORKER/'qemu-worker/runtime-v1.json').read_bytes())
    for row in manifest['files']:
        if identity(Path(row['path']))!=row:raise ValueError('frozen runtime identity')
    firmware=identity(root/'share/multiboot_dma.bin')
    elf=d/'guest.elf';elf.write_bytes(image());log=d/'trace.log';console=d/'guest.txt'
    args=[str(exe),'-machine','pc','-accel','tcg,thread=single,one-insn-per-tb=on','-smp','2','-m','4G',
          '-display','none','-serial','none','-monitor','none','-nic','none','-no-reboot',
          '-kernel',str(elf),'-debugcon','file:'+str(console),'-device','isa-debug-exit,iobase=0xf4,iosize=4',
          '-d','exec,int,nochain','-dfilter','0x100000..0x105000','-D',str(log)]
    r=dict(accepted=False,fullstate=False,windows_boots=0,original_game_starts=0,host_input_actions=0,args=args,
           executable=identity(exe),firmware=firmware,guest=identity(elf),errors=[],deadline_seconds=15,trace_budget_bytes=2*1024*1024)
    started=time.monotonic()
    with (d/'stderr.txt').open('wb')as err:
        p=subprocess.Popen(args,stdout=err,stderr=err,env=environment(),creationflags=subprocess.CREATE_NO_WINDOW)
        while p.poll()is None:
            if time.monotonic()-started>15 or (log.exists()and log.stat().st_size>r['trace_budget_bytes']):
                r['errors'].append('deadline or trace budget');p.kill();break
            time.sleep(.05)
        r['exit_code']=p.wait(timeout=3)
    r['seconds']=time.monotonic()-started;r['guest_output']=console.read_bytes().hex()if console.exists()else None
    r['files']=[identity(p)for p in d.iterdir()if p.is_file()]
    r['execution_complete']=r['exit_code']==33 and len(bytes.fromhex(r['guest_output'] or ''))==22 and bytes.fromhex(r['guest_output']).startswith(b'SHD') and bytes.fromhex(r['guest_output']).endswith(b'R1E')and not r['errors']
    (d/'report.json').write_text(json.dumps(r,indent=2));return r

if __name__=='__main__':
    if str(VMX).lower()in vmrun(['list'],timeout=10).lower():raise ValueError('Windows VM must remain off')
    out=WORKER/'tcg-predecessor-supervision-v3.json'
    if out.exists():raise ValueError('fresh output')
    code='import sys,json;json.loads(sys.stdin.readline());sys.path[:0]='+repr(runtime_paths())+';from devtools.terminal_tcg_predecessor_probe_v3 import run;r=run();print(json.dumps(dict(ok=r["execution_complete"],remote_completion="observed",exit_code=r["exit_code"],guest_output=r["guest_output"],errors=r["errors"])))'
    r=_supervise({},25,code);out.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
    raise SystemExit(not completed(r))
