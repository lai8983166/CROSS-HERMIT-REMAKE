"""Bounded actual control-path poisoning checks in an owned diskless guest."""
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
    raw, expected = image()
    (out / 'guest.elf').write_bytes(raw)
    report = dict(accepted=False, errors=[], mode=args.mode, binary=identity(args.binary))
    vm = None
    done = threading.Event()
    start = time.monotonic()
    def watchdog():
        if not done.wait(15):
            report['errors'].append('15 second budget')
            if vm and vm.proc.poll() is None:
                os.killpg(vm.proc.pid, signal.SIGKILL)
    threading.Thread(target=watchdog, daemon=True).start()
    try:
        vm = VM(args, out, 'source', expected)
        vm.bp('Z', expected['a'])
        vm.stop()
        report['arm'] = json.loads(vm.call('x-query-tcg-state', {'cpu-index': -2})['state'])
        if args.mode == 'memory':
            # Same-value write in owned zero-initialized RAM still must poison.
            report['action_reply'] = vm.rsp.command('M102000,4:00000000')
        else:
            report['action_reply'] = vm.call('system_reset')
        report['end'] = json.loads(vm.call('x-query-tcg-state', {'cpu-index': -3})['state'])
        report['rearm_reply'] = vm.qmp.call('x-query-tcg-state', {'cpu-index': -2})
        report['checks'] = dict(poisoned=report['end']['poisoned'] is True,
                                reason_present=bool(report['end']['poison_reason']),
                                rearm_refused='error' in report['rearm_reply'])
        report['quit'] = vm.call('quit')
        vm.proc.wait(timeout=3)
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
        report['rejection_passed'] = bool(report.get('checks')) and all(report['checks'].values()) and not report['errors']
        (out / 'report.json').write_text(json.dumps(report, indent=2))
    print(json.dumps({k: report.get(k) for k in ('rejection_passed', 'errors', 'seconds', 'checks')}))
    return report['rejection_passed']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for key in ('binary', 'firmware', 'output'):
        parser.add_argument('--' + key, type=Path, required=True)
    parser.add_argument('--mode', choices=('memory', 'reset'), required=True)
    raise SystemExit(not run(parser.parse_args()))
