"""Linux/WSL headless x87 roundtrip and stopped-state source preflight.

Own ELF32 only. No Windows/game, no host input, no CPU state injected by host.
"""
import argparse
import ast
import hashlib
import json
import os
import signal
import socket
import struct
import subprocess
import threading
import time
from pathlib import Path


def identity(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def image(root):
    # Evaluate only the frozen pure ELF builder, without Windows module imports.
    tree = ast.parse((root / 'devtools/terminal_tcg_predecessor_probe_v3.py').read_text())
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'image')
    space = {'struct': struct}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), '<frozen-elf-builder>', 'exec'), space)
    elf = bytearray(space['image']())
    def word(x): return struct.pack('<I', x)
    code = bytes.fromhex('66b810008ed88ec08ed0bc00401000')
    code += bytes.fromhex('0f20c083e0f383c8020f22c00f20e00d000200000f22e0')
    code += bytes.fromhex('bf00201000b980020000b8a5a5a5a5fcf3ab')
    code += bytes.fromhex('b80700000031c90fa2891d') + word(0x102440)
    code += bytes.fromhex('dbe3d905') + word(0x100900)
    code += bytes.fromhex('d92d') + word(0x10090c)  # non-default precision control
    code += bytes.fromhex('660f6f05') + word(0x100910)  # distinct XMM0 lanes
    fip = 0x100120 + len(code)
    code += bytes.fromhex('d805') + word(0x100904)
    code += bytes.fromhex('0fae05') + word(0x102000)  # baseline FX image
    code += bytes.fromhex('dbe3')  # clear tags/control/pointers via guest instruction
    code += bytes.fromhex('660f76c00fae15') + word(0x100908)  # disturb XMM0/MXCSR
    code += bytes.fromhex('0fae0d') + word(0x102000)  # guest FXRSTOR
    stop = 0x100120 + len(code)
    code += bytes.fromhex('0fae05') + word(0x102200)
    code += bytes.fromhex('d935') + word(0x102400)
    for address, count in ((0x102000, 512), (0x102200, 512), (0x102400, 28), (0x102440, 4)):
        code += b'\xbe' + word(address) + b'\xb9' + word(count) + bytes.fromhex('ace6e9e2fb')
    code += bytes.fromhex('b810000000e7f4f4ebfd')
    elf[4096+0x120:4096+0x120+len(code)] = code
    elf[4096+0x900:4096+0x908] = struct.pack('<ff', 1, 2)
    elf[4096+0x908:4096+0x90e] = struct.pack('<IH', 0x3f80, 0x027f)
    elf[4096+0x910:4096+0x920] = bytes(range(16))
    return bytes(elf), dict(fip=fip, fdp=0x100904, fcs=8, fds=16, fop=5, stop=stop)


class RSP:
    def __init__(self, path):
        self.s = socket.socket(socket.AF_UNIX)
        self.s.settimeout(10)
        self.s.connect('\0' + str(path))

    def command(self, text):
        data = text.encode()
        self.s.sendall(b'$' + data + b'#' + f'{sum(data)%256:02x}'.encode())
        while True:
            lead = self.s.recv(1)
            if not lead: raise EOFError('RSP closed before packet')
            if lead == b'$': break
        reply = bytearray()
        while True:
            b = self.s.recv(1)
            if b == b'#': break
            if not b: raise EOFError('RSP closed')
            reply.extend(b)
        check = self.s.recv(2)
        if len(check) != 2 or int(check, 16) != sum(reply) % 256:
            raise ValueError('RSP checksum')
        self.s.sendall(b'+')
        return reply.decode()

    def resume(self):
        self.s.sendall(b'$c#63')


class QMP:
    def __init__(self, path):
        self.s = socket.socket(socket.AF_UNIX)
        self.s.settimeout(5)
        self.s.connect('\0' + str(path))
        self.f = self.s.makefile('rwb', buffering=0)
        self.greeting = json.loads(self.f.readline())
        self.receipts = []
        self.call('qmp_capabilities')

    def call(self, name, args=None):
        request = dict(execute=name, id=len(self.receipts)+1)
        if args is not None: request['arguments'] = args
        self.f.write(json.dumps(request).encode()+b'\n')
        while True:
            response = json.loads(self.f.readline())
            if response.get('id') == request['id']: break
        self.receipts.append(dict(request=request, response=response))
        return response


def run(args, image_builder=image, validator=None):
    root = Path(__file__).resolve().parents[1]
    out = args.output.resolve()
    if not str(out).startswith('/mnt/f/'):
        raise ValueError('F-backed output required')
    out.mkdir(exist_ok=False)
    guest, expected = image_builder(root)
    (out/'guest.elf').write_bytes(guest)
    # NTFS/DrvFS cannot create AF_UNIX filesystem sockets. Linux abstract
    # sockets live only in this WSL kernel namespace and leave no C: files.
    qmp_path, gdb_path = 'chaomofa-'+out.name+'-qmp', 'chaomofa-'+out.name+'-gdb'
    command = [str(args.binary.resolve()), '-L', str(args.firmware.resolve()), '-machine', 'pc',
               '-accel', 'tcg,thread=single,one-insn-per-tb=on', '-smp', '2', '-m', '4G',
               '-display', 'none', '-serial', 'none', '-monitor', 'none', '-nic', 'none',
               '-no-reboot', '-kernel', str(out/'guest.elf'), '-debugcon', 'file:'+str(out/'guest.bin'),
               '-device', 'isa-debug-exit,iobase=0xf4,iosize=4', '-S',
               '-qmp', 'unix:'+qmp_path+',abstract=on,server=on,wait=off',
               '-gdb', 'unix:'+gdb_path+',abstract=on,server=on,wait=off',
               '-d', 'exec,int,nochain', '-dfilter', expected.get('trace_filter', '0x100000..0x105000'), '-D', str(out/'trace.log')]
    result = dict(accepted=False, full57=False, windows_admitted=False, windows_boots=0,
                  game_starts=0, host_input=0, expected=expected, command=command,
                  binary=identity(args.binary), errors=[], deadline_seconds=30,
                  trace_budget_bytes=2*1024**2, transport='Linux abstract AF_UNIX; no filesystem socket')
    start = time.monotonic()
    qmp = rsp = proc = None
    finished = threading.Event()
    def watchdog():
        while not finished.wait(.1):
            trace = out/'trace.log'
            if time.monotonic()-start > 30 or (trace.exists() and trace.stat().st_size > 2*1024**2):
                result['errors'].append('30 second/2 MiB watchdog')
                if proc and proc.poll() is None:
                    os.killpg(proc.pid, signal.SIGKILL)
                return
    try:
        with (out/'stderr.txt').open('wb') as stderr:
            proc = subprocess.Popen(command, stdout=stderr, stderr=stderr, start_new_session=True)
            threading.Thread(target=watchdog, daemon=True).start()
            while True:
                if proc.poll() is not None or time.monotonic()-start > 5:
                    raise RuntimeError('startup deadline/failure')
                try:
                    qmp = QMP(qmp_path)
                    rsp = RSP(gdb_path)
                    break
                except (ConnectionRefusedError, FileNotFoundError):
                    if qmp:
                        qmp.f.close(); qmp.s.close(); qmp = None
                time.sleep(.05)
            result['invalid_cpu_rejected'] = 'error' in qmp.call('x-query-tcg-state', {'cpu-index':-1})
            if rsp.command(f'Z1,{expected["stop"]:x},1') != 'OK':
                raise ValueError('breakpoint refused')
            result['stop_reply'] = rsp.command('c')
            if not result['stop_reply'].startswith('T05'):
                raise ValueError('unexpected stop')
            states = []
            for _ in range(2):
                response = qmp.call('x-query-tcg-state', {'cpu-index':0})
                if 'error' in response: raise ValueError(response)
                states.append(json.loads(response['return']['state']))
            result['states'] = states
            if rsp.command(f'z1,{expected["stop"]:x},1') != 'OK':
                raise ValueError('breakpoint removal refused')
            rsp.resume()
            result['exit_code'] = proc.wait(timeout=5)
        raw = (out/'guest.bin').read_bytes()
        if validator:
            result['bounded_case_passed'] = validator(raw, expected, states, result)
        else:
            if len(raw) != 1056: raise ValueError('output size')
            a, b = raw[:512], raw[512:1024]
            # Compare architecturally written bytes, excluding reserved/sentinel areas.
            spans = [(0,5),(6,14),(16,22),(24,32)] + [(32+i*16,42+i*16) for i in range(8)] + [(160,288)]
            equal = all(a[x:y] == b[x:y] for x,y in spans)
            fields = dict(fop=struct.unpack_from('<H',b,6)[0], fip=struct.unpack_from('<I',b,8)[0],
                          fcs=struct.unpack_from('<H',b,12)[0], fdp=struct.unpack_from('<I',b,16)[0],
                          fds=struct.unpack_from('<H',b,20)[0])
            state = states[0]
            cpuid = struct.unpack_from('<I',raw,1052)[0]
            physical_match = all(
                state['fp_physical_low64_high16'][(i+state['top'])&7] ==
                [f'{struct.unpack_from("<Q",b,32+i*16)[0]:016x}', f'{struct.unpack_from("<H",b,40+i*16)[0]:016x}']
                for i in range(8))
            xmm_match = all(state['xmm_low64_high64'][i] ==
                            [f'{struct.unpack_from("<Q",b,160+i*16+j*8)[0]:016x}' for j in range(2)]
                            for i in range(8))
            result.update(roundtrip_equal=equal, restored_fields=fields,
                          stopped_reads_equal=states[0]==states[1], cpuid_7_0_ebx=cpuid,
                          qmp_physical_fp_match=physical_match, qmp_xmm_match=xmm_match)
            result['bounded_case_passed'] = (equal and fields == {k:expected[k] for k in fields}
                and state['fop']==5 and int(state['fip'],16)==expected['fip']
                and int(state['fdp'],16)==expected['fdp'] and int(state['eip'],16)==expected['stop']
                and state['fcs']==8 and state['fds']==16 and state['top']==7
                and state['cpu']==0 and sorted(state.get('vp_stopped',[]),key=lambda v:v['cpu'])==[dict(cpu=0,stopped=True),dict(cpu=1,stopped=True)]
                and cpuid & ((1<<6)|(1<<13)) == 0 and physical_match and xmm_match
                and state['fp_control']==struct.unpack_from('<H',b,0)[0]==0x27f
                and state['fp_status']==struct.unpack_from('<H',b,2)[0]
                and state['fp_empty_mask']==(b[4]^0xff)
                and state['mxcsr']==struct.unpack_from('<I',b,24)[0]==0x1f80
                and state['fp_physical_low64_high16'][7]==['c000000000000000','0000000000004000']
                and result['invalid_cpu_rejected'] and result['stopped_reads_equal'] and result['exit_code']==33
                and not result['errors'])
    except Exception as exc:
        result['errors'].append(str(exc))
        result['bounded_case_passed'] = False
    finally:
        finished.set()
        if proc and proc.poll() is None:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait(timeout=3)
        if qmp:
            result['qmp_receipts'] = qmp.receipts
            qmp.f.close(); qmp.s.close()
        if rsp: rsp.s.close()
        result['process_exited'] = proc is not None and proc.poll() is not None
        if result['errors'] or not result['process_exited']:
            result['bounded_case_passed'] = False
        result['seconds'] = time.monotonic()-start
        result['files'] = [identity(p) for p in out.iterdir() if p.is_file()]
        (out/'report.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ('states','qmp_receipts','files','command')},indent=2))
    return result['bounded_case_passed']


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--binary',type=Path,required=True)
    p.add_argument('--firmware',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    raise SystemExit(not run(p.parse_args()))
