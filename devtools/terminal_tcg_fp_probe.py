"""Bounded architectural x87 export probe; never game/full-state acceptance."""
import json
import struct
import subprocess
import time
from pathlib import Path

from devtools.isolated_windows_vm import WORKER, VMX, vmrun, identity, environment
from devtools.isolated_vm_bounded_query_v3 import _supervise, runtime_paths, completed
from devtools.terminal_tcg_predecessor_probe_v3 import image as parent_image


def image():
    elf = bytearray(parent_image())
    def put(offset, data):
        elf[4096 + offset:4096 + offset + len(data)] = data
    def u32(x):
        return struct.pack('<I', x)
    # Reuse only ELF loader/GDT. No inherited exception handler or DR setup runs.
    code = bytes.fromhex('66b810008ed88ec08ed0bc00401000')
    # CR0.EM/TS clear, MP set; CR4.OSFXSR set. CPUID captured before x87 work.
    code += bytes.fromhex('0f20c083e0f383c8020f22c00f20e00d000200000f22e0')
    code += bytes.fromhex('b80700000031c90fa2891d') + u32(0x102240)
    code += bytes.fromhex('bf00201000b980000000b8a5a5a5a5fcf3ab')
    code += bytes.fromhex('dbE3d905') + u32(0x100900)  # FNINIT; FLD m32real=1
    fip = 0x100120 + len(code)
    code += bytes.fromhex('d805') + u32(0x100904)  # FADD m32real=2; FOP=005
    code += bytes.fromhex('0fae05') + u32(0x102000)  # FXSAVE before FNSTENV
    code += bytes.fromhex('d935') + u32(0x102200)  # 28-byte protected env
    # Output exactly 512+28+4 raw bytes, then exit through isa-debug-exit.
    for address, count in ((0x102000, 512), (0x102200, 28), (0x102240, 4)):
        code += b'\xbe' + u32(address) + b'\xb9' + u32(count)
        code += bytes.fromhex('ace6e9e2fb')
    code += bytes.fromhex('b810000000e7f4f4ebfd')
    put(0x120, code)
    put(0x900, struct.pack('<ff', 1., 2.))
    return bytes(elf), dict(fip=fip, fdp=0x100904, fcs=8, fds=16, fop=5)


def decode(raw):
    if len(raw) != 544:
        raise ValueError('exact output size required')
    fx, env = raw[:512], raw[512:540]
    return dict(
        fx=dict(fop=struct.unpack_from('<H', fx, 6)[0],
                fip=struct.unpack_from('<I', fx, 8)[0], fcs=struct.unpack_from('<H', fx, 12)[0],
                fdp=struct.unpack_from('<I', fx, 16)[0], fds=struct.unpack_from('<H', fx, 20)[0],
                st0=fx[32:42].hex()),
        env=dict(fip=struct.unpack_from('<I', env, 12)[0],
                 fcs=struct.unpack_from('<H', env, 16)[0], fop=struct.unpack_from('<H', env, 18)[0] & 0x7ff,
                 fdp=struct.unpack_from('<I', env, 20)[0], fds=struct.unpack_from('<H', env, 24)[0]),
        cpuid_7_0_ebx=struct.unpack_from('<I', raw, 540)[0])


def run():
    d = WORKER / 'tcg-fp-v1-20261110'
    d.mkdir(exist_ok=False)
    root = WORKER / 'qemu-worker/runtime'
    for row in json.loads((WORKER / 'qemu-worker/runtime-v1.json').read_bytes())['files']:
        if identity(Path(row['path'])) != row:
            raise ValueError('runtime identity mismatch')
    blob, expected = image()
    elf, console, trace = d / 'guest.elf', d / 'guest.bin', d / 'trace.log'
    elf.write_bytes(blob)
    args = [str(root / 'qemu-system-x86_64.exe'), '-machine', 'pc', '-accel',
            'tcg,thread=single,one-insn-per-tb=on', '-smp', '2', '-m', '4G',
            '-display', 'none', '-serial', 'none', '-monitor', 'none', '-nic', 'none',
            '-no-reboot', '-kernel', str(elf), '-debugcon', 'file:' + str(console),
            '-device', 'isa-debug-exit,iobase=0xf4,iosize=4', '-d', 'exec,int,nochain',
            '-dfilter', '0x100000..0x105000', '-D', str(trace)]
    start = time.monotonic()
    errors = []
    with (d / 'stderr.txt').open('wb') as stderr:
        p = subprocess.Popen(args, stdout=stderr, stderr=stderr, env=environment(),
                             creationflags=subprocess.CREATE_NO_WINDOW)
        while p.poll() is None:
            if time.monotonic() - start > 15 or (trace.exists() and trace.stat().st_size > 2 * 1024**2):
                errors.append('deadline or output budget'); p.kill(); break
            time.sleep(.05)
        rc = p.wait(timeout=3)
    raw = console.read_bytes() if console.exists() else b''
    r = dict(accepted=False, fullstate=False, windows_boots=0, original_game_starts=0,
             host_input_actions=0, seconds=time.monotonic()-start, exit_code=rc, errors=errors,
             args=args, expected=expected, observed=decode(raw) if len(raw)==544 else None,
             files=[identity(x) for x in d.iterdir() if x.is_file()],
             execution_complete=rc==33 and len(raw)==544 and not errors)
    (d / 'report.json').write_text(json.dumps(r, indent=2))
    return r


if __name__ == '__main__':
    if str(VMX).lower() in vmrun(['list'], timeout=10).lower():
        raise ValueError('Windows VM must remain off')
    out = WORKER / 'tcg-fp-supervision-v1.json'
    if out.exists():
        raise ValueError('fresh output required')
    code = ('import sys,json;json.loads(sys.stdin.readline());sys.path[:0]=' + repr(runtime_paths()) +
            ';from devtools.terminal_tcg_fp_probe import run;r=run();'
            'print(json.dumps(dict(ok=r["execution_complete"],remote_completion="observed",'
            'exit_code=r["exit_code"],observed=r["observed"],errors=r["errors"])))')
    r = _supervise({}, 25, code)
    out.write_text(json.dumps(r, indent=2))
    print(json.dumps(r, indent=2))
    raise SystemExit(not completed(r))
