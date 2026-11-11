"""Read the v5 guest receipt files from authenticated ended overlays only."""
import hashlib
import json
from pathlib import Path
from dissect.hypervisor.disk.vmdk import VMDK
from dissect.hypervisor.disk.qcow2 import QCow2
from dissect.ntfs import NTFS
from dissect.volume.disk import Disk
from devtools.terminal_tcg_roundtrip_probe import identity


def run():
    root = Path(__file__).resolve().parents[1]
    work = root / '.venv-audit/native-worker'
    case = work / 'tcg-wait-native-v6'
    out = work / 'tcg-cr2-guest-recovery-v2'
    out.mkdir(exist_ok=False)
    receipt = json.loads((case / 'report.json').read_bytes())
    if not receipt['process_exited']:
        raise ValueError('ended guest required')
    layers = [work / name / 'disk.qcow2' for name in ('tcg-windows-compat-v2', 'tcg-windows-current-v1', 'tcg-wait-native-v5', case.name)]
    before = [identity(path) for path in layers]
    if before[-1]['sha256'] != receipt['overlay']['sha256'] or before[-2]['sha256'] != receipt['parent']['sha256']:
        raise ValueError('disk identity')
    stream = VMDK(work / 'worker.vmdk')
    for path in layers:
        stream.seek(0)
        stream = QCow2(path.open('rb'), backing_file=stream).open()
    part = next(p for p in Disk(stream).partitions if p.offset == 525336576)
    ntfs = NTFS(part.open())
    directory = 'ChaomofaWorker/' + case.name
    names = list(ntfs.mft.get(directory).listdir(ignore_dos=True))
    records = []
    for name in names:
        if name not in ('ready.json', 'result.json', 'result.json.watchdog.json', 'launch-receipt.json',
                        'fixture.exe', 'fixture.bin', 'manifest.json', 'terminal_tcg_wait_fixture_v3.cs', 'go'):
            continue
        raw = ntfs.mft.get(directory + '/' + name).open().read(131073)
        if len(raw) > 131072:
            raise ValueError('file budget')
        (out / name).write_bytes(raw)
        records.append(dict(name=name, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
    if before != [identity(p) for p in layers]:
        raise ValueError('source changed')
    report = dict(accepted=False, sources=before, base_worker_fresh_sha=False,
                  directory_names=names, files=records, sources_unchanged=True)
    (out / 'report.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(dict(names=names, records=len(records))))

if __name__ == '__main__':
    run()
