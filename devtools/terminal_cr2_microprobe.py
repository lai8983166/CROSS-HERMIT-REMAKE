"""Bounded, diskless CR2 baseline/ledger probe; no Windows or game acceptance."""
import argparse
import json
import os
from pathlib import Path
import signal
import threading
import time
from devtools.terminal_cr2_microguest import image
from devtools.terminal_tcg_ram_event_probe_v2 import VM
from devtools.terminal_tcg_roundtrip_probe import identity


def run(args):
    out = args.output.resolve()
    if not str(out).startswith('/mnt/f/'):
        raise ValueError('F-backed output required')
    out.mkdir(exist_ok=False)
    elf, expected = image()
    (out / 'guest.elf').write_bytes(elf)
    report = dict(accepted=False, windows_admitted=False, game_started=False, errors=[],
                  binary=identity(args.binary), expected=expected, ledger_enabled=args.ledger)
    vm = None
    done = threading.Event()
    start = time.monotonic()
    def watch():
        while not done.wait(.1):
            if time.monotonic() - start > 15 or any(p.stat().st_size > 2*1024**2 for p in out.glob('*.trace')):
                report['errors'].append('15s / 2MiB trace budget')
                if vm and vm.proc.poll() is None:
                    os.killpg(vm.proc.pid, signal.SIGKILL)
                return
    threading.Thread(target=watch, daemon=True).start()
    try:
        vm = VM(args, out, 'source', expected)
        def states():
            return [json.loads(vm.call('x-query-tcg-state', {'cpu-index': i})['state']) for i in range(2)]
        vm.bp('Z', expected['a'])
        vm.stop()
        report['start'] = states()
        if args.ledger:
            report['arm'] = json.loads(vm.call('x-query-tcg-state', {'cpu-index': -2})['state'])
        vm.bp('z', expected['a'])
        vm.bp('Z', expected['handler'])
        vm.stop()
        report['fault_handler'] = states()
        sp = int(report['fault_handler'][0]['gpr'][4], 16)
        report['fault_frame'] = vm.rsp.command(f'm{sp:x},10')
        vm.bp('z', expected['handler'])
        vm.bp('Z', expected['b'])
        vm.stop()
        report['end'] = states()
        if args.ledger:
            report['ledger'] = json.loads(vm.call('x-query-tcg-state', {'cpu-index': -3})['state'])
        report['fault_count'] = int.from_bytes(bytes.fromhex(vm.rsp.command('m102000,4')), 'little')
        report['exit_code'] = vm.exit()
        frame = bytes.fromhex(report['fault_frame'])
        report['checks'] = dict(start_pc=int(report['start'][0]['eip'], 16) == expected['a'],
            end_pc=int(report['end'][0]['eip'], 16) == expected['b'],
            actual_fault_pc=int.from_bytes(frame[4:8], 'little') == expected['pf_pc'],
            fault_error=int.from_bytes(frame[:4], 'little') == 0,
            actual_cr2=int(report['end'][0]['cr0_cr2_cr3_cr4'][1], 16) == expected['pf_address'],
            one_fault=report['fault_count'] == 1, natural_exit=report['exit_code'] == 33,
            consumed=(out / 'source.bin').read_bytes() == b'C',
            no_stderr=not (out / 'source.stderr').read_bytes())
    except Exception as exc:
        report['errors'].append(type(exc).__name__ + ': ' + str(exc))
    finally:
        done.set()
        if vm:
            report['command'] = vm.command
            report['qmp'] = vm.qmp.receipts if vm.qmp else []
            vm.close()
            report['process_exited'] = vm.proc.poll() is not None
        report['seconds'] = time.monotonic() - start
        report['microguest_passed'] = bool(report.get('checks')) and all(report['checks'].values()) and not report['errors']
        (out / 'report.json').write_text(json.dumps(report, indent=2))
    print(json.dumps({k: report.get(k) for k in ('microguest_passed', 'errors', 'seconds', 'checks')}))
    return report['microguest_passed']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for key in ('binary', 'firmware', 'output'):
        parser.add_argument('--' + key, type=Path, required=True)
    parser.add_argument('--ledger', action='store_true')
    raise SystemExit(not run(parser.parse_args()))
