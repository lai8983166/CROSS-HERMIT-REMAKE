"""Extract bounded original WOW64 modules from a stopped authenticated disk chain."""
import gzip
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
    w = root / '.venv-audit/native-worker'
    prior = json.loads((root/'analysis/terminal-wait-tcg-gated-closeout-v1-20261111.json').read_bytes())
    layers = [w/x/'disk.qcow2' for x in ('tcg-windows-compat-v2','tcg-windows-current-v1','tcg-wait-native-v2')]
    before = [identity(p) for p in layers]
    if before[-1]['sha256'] != prior['sources']['new_overlay']['sha256'] or before[-2]['sha256'] != prior['sources']['parent_current']['sha256']:
        raise ValueError('frozen source mismatch')
    if not json.loads((layers[-1].parent/'report.json').read_bytes())['process_exited']:
        raise ValueError('stopped source required')
    out = w/'tcg-wow64-path-v1'
    out.mkdir(exist_ok=False)
    stream = VMDK(w/'worker.vmdk')
    for p in layers:
        stream.seek(0)
        stream = QCow2(p.open('rb'), backing_file=stream).open()
    volumes = []
    for part in Disk(stream).partitions:
        ntfs = NTFS(part.open())
        try:
            ntfs.mft.get('Windows/System32/wow64cpu.dll')
            volumes.append((part, ntfs))
        except FileNotFoundError:
            pass
    if len(volumes) != 1:
        raise ValueError('unique Windows volume required')
    part, ntfs = volumes[0]
    records = []
    for path in ('Windows/System32/wow64cpu.dll','Windows/System32/wow64.dll',
                 'Windows/System32/ntdll.dll','Windows/SysWOW64/ntdll.dll'):
        raw = ntfs.mft.get(path).open().read(4*1024*1024+1)
        if len(raw) > 4*1024*1024:
            raise ValueError('module budget')
        target = out/(path.split('/')[-2]+'-'+path.split('/')[-1])
        target.write_bytes(raw)
        records.append(dict(guest_path=path, **identity(target)))
    if [identity(p) for p in layers] != before:
        raise ValueError('source disk changed')
    r = dict(accepted=False, source_disks=before, disks_unchanged=True,
             partition_offset=part.offset, modules=records,
             scope='Original on-disk module identity; not live mapping authentication or executed-path proof')
    (out/'extraction.json').write_text(json.dumps(r,indent=2))
    print(json.dumps(dict(modules=len(records),bytes=sum(x['bytes'] for x in records))))


if __name__ == '__main__':
    run()
