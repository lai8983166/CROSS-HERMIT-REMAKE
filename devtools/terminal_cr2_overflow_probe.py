"""Actual bounded saturation, preserving compressed event bytes once."""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import signal
import struct
import threading
import time
from devtools.terminal_cr2_microguest import image
from devtools.terminal_cr2_normal_vm import VM
from devtools.terminal_tcg_roundtrip_probe import identity


def run(args):
    out = args.output.resolve()
    if not str(out).startswith('/mnt/f/'):
        raise ValueError('F-backed output required')
    out.mkdir(exist_ok=False)
    raw, expected = image()
    raw = bytearray(raw)
    body = bytes.fromhex('b878563412b9') + struct.pack('<I', 65537) + bytes.fromhex('0f22d04975fa')
    expected['b'] = 0x100300 + len(body)
    body += bytes.fromhex('b810000000e7f4f4ebfd')
    raw[4096+0x300:4096+0x300+len(body)] = body
    (out/'guest.elf').write_bytes(raw)
    report = dict(accepted=False, errors=[], binary=identity(args.binary))
    vm = None
    done = threading.Event()
    start = time.monotonic()
    def watch():
        if not done.wait(15):
            report['errors'].append('15 second budget')
            if vm and vm.proc.poll() is None:
                os.killpg(vm.proc.pid, signal.SIGKILL)
    threading.Thread(target=watch, daemon=True).start()
    try:
        vm = VM(args, out, 'source', expected)
        vm.bp('Z', expected['a'])
        vm.stop()
        report['arm'] = json.loads(vm.call('x-query-tcg-state', {'cpu-index': -2})['state'])
        vm.bp('z', expected['a'])
        vm.call('cont')
        while True:
            status = vm.call('query-status')
            if not status['running']:
                break
            time.sleep(.01)
        report['status'] = status
        payload = vm.call('x-query-tcg-state', {'cpu-index': -3})['state']
        data = payload.encode()
        (out/'end.json.gz').write_bytes(gzip.compress(data, mtime=0))
        ledger = json.loads(payload)
        report['ledger'] = {k: v for k, v in ledger.items() if k != 'events_json'}
        report['full_ledger'] = dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), compressed=identity(out/'end.json.gz'))
        report['rearm_reply'] = vm.qmp.call('x-query-tcg-state', {'cpu-index': -2})
        report['checks'] = dict(poisoned=ledger['poisoned'] is True, overflow=ledger['overflow'] is True,
            reason=ledger['poison_reason'] == 'overflow', stopped=status['running'] is False,
            records_bounded=0 < ledger['count'] <= 65536, bytes_bounded=ledger['bytes'] <= 16777216,
            rearm_refused='error' in report['rearm_reply'],
            digest=hashlib.sha256(ledger['events_json'].encode()).hexdigest() == ledger['events_sha256'])
        vm.call('quit')
        vm.proc.wait(timeout=3)
    except Exception as exc:
        report['errors'].append(type(exc).__name__ + ': ' + str(exc))
    finally:
        done.set()
        if vm:
            report['command'] = vm.command
            vm.close()
            report['process_exited'] = vm.proc.poll() is not None
        report['seconds'] = time.monotonic() - start
        report['overflow_rejected'] = bool(report.get('checks')) and all(report['checks'].values()) and not report['errors']
        (out/'report.json').write_text(json.dumps(report, indent=2))
    print(json.dumps({k: report.get(k) for k in ('overflow_rejected', 'seconds', 'errors', 'checks')}))
    return report['overflow_rejected']

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    for key in ('binary', 'firmware', 'output'):
        parser.add_argument('--' + key, type=Path, required=True)
    raise SystemExit(not run(parser.parse_args()))
