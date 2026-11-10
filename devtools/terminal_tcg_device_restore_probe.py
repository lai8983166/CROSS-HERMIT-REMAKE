"""Bounded same-process device/CPU restore; own diskless guest, no RAM rollback claim."""
import argparse
import ast
import json
import os
import signal
import struct
import subprocess
import threading
import time
from pathlib import Path
from devtools.terminal_tcg_roundtrip_probe import QMP, RSP, identity


def image(root, inverse=False):
    tree = ast.parse((root/'devtools/terminal_tcg_predecessor_probe_v3.py').read_text())
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'image')
    scope = {'struct': struct}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), '<frozen-elf>', 'exec'), scope)
    elf = bytearray(scope['image']())
    w = lambda x: struct.pack('<I', x)
    code = bytes.fromhex('66b810008ed88ec08ed0bc00401000')
    code += bytes.fromhex('0f20c083e0f383c8020f22c00f20e00d000200000f22e0')
    rich = bytes.fromhex('dbe3d905')+w(0x100900)+bytes.fromhex('d805')+w(0x100904)
    rich += bytes.fromhex('660f6f05')+w(0x100910)+bytes.fromhex('0fae15')+w(0x100908)
    rich += bytes.fromhex('b878563412bb21436587b91122334439c0f9fd')
    zero = bytes.fromhex('dbe3660fefc00fae15')+w(0x10090c)+bytes.fromhex('31c031db31c983c001fc')
    code += zero if inverse else rich
    a = 0x100120+len(code)
    code += b'\x90' + (rich if inverse else zero)
    b = 0x100120+len(code)
    code += bytes.fromhex('90b052e6e9b810000000e7f4f4ebfd')
    elf[4096+0x120:4096+0x120+len(code)] = code
    elf[4096+0x900:4096+0x910] = struct.pack('<ffII', 1, 2, 0x3f80, 0x1f80)
    elf[4096+0x910:4096+0x920] = bytes(range(16))
    return bytes(elf), dict(a=a, b=b, inverse=inverse, interval_writes_ram=False)


def run(args):
    out = args.output.resolve()
    if not str(out).startswith('/mnt/f/'): raise ValueError('F-backed output required')
    out.mkdir(exist_ok=False)
    elf, expected = image(Path(__file__).resolve().parents[1], args.inverse)
    (out/'guest.elf').write_bytes(elf)
    qp, gp = ['chaomofa-'+out.name+'-'+s for s in ('qmp','gdb')]
    snapshot = out/'devices.bin'
    command = [str(args.binary.resolve()), '-L', str(args.firmware.resolve()),
        '-machine','pc,suppress-vmdesc=on','-accel','tcg,thread=single,one-insn-per-tb=on','-smp','2','-m','4G',
        '-display','none','-serial','none','-monitor','none','-nic','none','-no-reboot',
        '-global','migration.send-configuration=off', '-kernel',str(out/'guest.elf'),
        '-debugcon','file:'+str(out/'guest.bin'),'-device','isa-debug-exit,iobase=0xf4,iosize=4','-S',
        '-qmp','unix:'+qp+',abstract=on,server=on,wait=off',
        '-gdb','unix:'+gp+',abstract=on,server=on,wait=off']
    result = dict(accepted=False, windows_admitted=False, full57=False, command=command,
        binary=identity(args.binary), expected=expected, errors=[], deadline_seconds=30,
        device_budget_bytes=8*1024**2, ram_restore_tested=False, native_lifetime_tested=False)
    proc = qmp = rsp = None
    done = threading.Event(); start = time.monotonic()
    def watchdog():
        while not done.wait(.05):
            if time.monotonic()-start > 30 or (snapshot.exists() and snapshot.stat().st_size > 8*1024**2):
                result['errors'].append('time/device-size budget exceeded')
                if proc and proc.poll() is None: os.killpg(proc.pid, signal.SIGKILL)
                return
    def call(name, args=None):
        r = qmp.call(name, args)
        if 'error' in r: raise ValueError(r)
        return r['return']
    def states():
        return [json.loads(call('x-query-tcg-state', {'cpu-index':i})['state']) for i in range(2)]
    def bp(op, address):
        if rsp.command(f'{op}1,{address:x},1') != 'OK': raise ValueError('breakpoint refused')
    def step_to_stop():
        if not rsp.command('c').startswith('T05'): raise ValueError('unexpected stop')
    try:
        with (out/'stderr.txt').open('wb') as err:
            proc = subprocess.Popen(command, stdout=err, stderr=err, start_new_session=True)
            threading.Thread(target=watchdog,daemon=True).start()
            while qmp is None:
                if proc.poll() is not None or time.monotonic()-start > 5: raise RuntimeError('startup failed')
                try: qmp = QMP(qp)
                except (FileNotFoundError,ConnectionRefusedError): time.sleep(.05)
            rsp = RSP(gp)
            bp('Z',expected['a']); step_to_stop()
            before = states(); result['before'] = before
            call('xen-save-devices-state', {'filename':str(snapshot),'live':False})
            result['after_save'] = states()
            bp('z',expected['a']); bp('Z',expected['b']); step_to_stop()
            result['disturbed'] = states()
            call('xen-load-devices-state', {'filename':str(snapshot)})
            result['status_after_load'] = call('query-status')
            after = states(); result['after'] = after
            result['differences'] = {str(i):[k for k in before[i] if before[i][k]!=after[i].get(k)] for i in range(2)}
            step_to_stop(); result['second_b'] = states()
            bp('z',expected['b']); rsp.resume()
            result['exit_code'] = proc.wait(timeout=5)
        result['checks'] = dict(saved_unchanged=before==result['after_save'],
            all_exported_fields_restored=before==after,
            disturbed_flags=before[0]['eflags']!=result['disturbed'][0]['eflags'],
            disturbed_fp=before[0]['fp_empty_mask']!=result['disturbed'][0]['fp_empty_mask'],
            disturbed_gpr=before[0]['gpr']!=result['disturbed'][0]['gpr'],
            exact_a=int(before[0]['eip'],16)==expected['a'],
            exact_b=int(result['disturbed'][0]['eip'],16)==expected['b'],
            natural_reexecution=result['disturbed']==result['second_b'],
            stopped_after_load=not result['status_after_load']['running'],
            natural_output=(out/'guest.bin').read_bytes()==b'R',clean_exit=result['exit_code']==33)
    except Exception as exc: result['errors'].append(str(exc))
    finally:
        done.set()
        if proc and proc.poll() is None:
            os.killpg(proc.pid,signal.SIGKILL); proc.wait(timeout=3)
        if qmp:
            result['qmp_receipts']=qmp.receipts; qmp.f.close(); qmp.s.close()
        if rsp: rsp.s.close()
        result['process_exited']=proc is not None and proc.poll() is not None
        result['seconds']=time.monotonic()-start
        result['bounded_case_passed']=bool(result.get('checks')) and all(result['checks'].values()) and not result['errors'] and result['process_exited']
        result['files']=[identity(p) for p in out.iterdir() if p.is_file()]
        (out/'report.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:result[k] for k in ('bounded_case_passed','errors','seconds')},indent=2))
    return result['bounded_case_passed']


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--binary',type=Path,required=True); p.add_argument('--firmware',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True); p.add_argument('--inverse',action='store_true')
    raise SystemExit(not run(p.parse_args()))
