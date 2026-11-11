"""Read the frozen failed fixture directory without booting or writing its disks."""
import hashlib
import json
import time
from pathlib import Path
from dissect.hypervisor.disk.vmdk import VMDK
from dissect.hypervisor.disk.qcow2 import QCow2
from dissect.volume.disk import Disk
from dissect.ntfs import NTFS
from devtools.terminal_tcg_roundtrip_probe import identity


def recover():
    root = Path(__file__).resolve().parents[1]
    w = root / '.venv-audit/native-worker'
    out = w / 'tcg-wait-recovery-v1'
    out.mkdir(exist_ok=False)
    start = time.monotonic()
    prior = json.loads((root / 'analysis/terminal-wait-tcg-native-control-closeout-v1-20261111.json').read_bytes())
    layers = [w / x / 'disk.qcow2' for x in ('tcg-windows-compat-v2', 'tcg-windows-current-v1', 'tcg-wait-native-v1')]
    before = [identity(p) for p in layers]
    if before[-1]['sha256'] != prior['case_disk']['sha256'] or before[-2]['sha256'] != prior['current_parent']['sha256']:
        raise ValueError('frozen parent identity')
    stream = VMDK(w / 'worker.vmdk')
    for p in layers:
        stream.seek(0)
        stream = QCow2(p.open('rb'), backing_file=stream).open()
    found = []
    for partition in Disk(stream).partitions:
        ntfs = NTFS(partition.open())
        try:
            directory = ntfs.mft.get('ChaomofaWorker/tcg-wait-native-v1')
        except FileNotFoundError:
            continue
        names = directory.listdir(ignore_dos=True)
        records = []
        for name in ('ready.json', 'result.json', 'fixture.exe', 'fixture.bin', 'manifest.json', 'terminal_tcg_wait_fixture.cs'):
            raw = ntfs.mft.get('ChaomofaWorker/tcg-wait-native-v1/' + name).open().read(131073)
            if len(raw) > 131072:
                raise ValueError('file budget')
            (out / name).write_bytes(raw)
            records.append(dict(name=name, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
        found.append(dict(offset=partition.offset, directory_names=list(names), files=records))
    if len(found) != 1:
        raise ValueError('unique owned directory required')
    expected = json.loads((w / 'tcg-wait-native-v1/fixture-inputs.json').read_bytes())['files']
    actual = {r['name']: r for r in found[0]['files']}
    if any(actual[x['name']]['sha256'] != x['sha256'] for x in expected):
        raise ValueError('guest uploaded bytes mismatch')
    after = [identity(p) for p in layers]
    if before != after:
        raise ValueError('source changed')
    result = json.loads((out / 'result.json').read_text(encoding='utf-8-sig'))
    report = dict(accepted=False, offline=True, sources=before, sources_unchanged=True,
                  extraction=found, uploaded_bytes_match=True, seconds=time.monotonic()-start,
                  gate_error=result['error'], signals=result['signals'],
                  cleanup={k: result[k] for k in ('workers_stopped','handles_closed','buffers_released',
                           'main_affinity_restored','watchdog_disarmed','cleanup_errors')},
                  target_wait_executed=False, original_game=False)
    (out / 'report.json').write_text(json.dumps(report, indent=2))
    print(json.dumps({k: report[k] for k in ('seconds','gate_error','signals','cleanup')}))


if __name__ == '__main__':
    recover()
