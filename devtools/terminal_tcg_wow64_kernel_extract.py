"""Recover/verify the retained kernel bytes, without booting or writing source disks."""
import argparse,hashlib,json
from pathlib import Path
from dissect.hypervisor.disk.vmdk import VMDK
from dissect.hypervisor.disk.qcow2 import QCow2
from dissect.ntfs import NTFS
from dissect.volume.disk import Disk
from devtools.terminal_tcg_roundtrip_probe import identity

def recover(out):
    root=Path(__file__).resolve().parents[1];w=root/'.venv-audit/native-worker';d=w/'tcg-wow64-path-v1'
    prior=json.loads((root/'analysis/terminal-wait-tcg-gated-closeout-v1-20261111.json').read_bytes())
    layers=[w/x/'disk.qcow2'for x in ('tcg-windows-compat-v2','tcg-windows-current-v1','tcg-wait-native-v2')]
    before=[identity(p)for p in layers]
    if before[-1]['sha256']!=prior['sources']['new_overlay']['sha256']or before[-2]['sha256']!=prior['sources']['parent_current']['sha256']:raise ValueError('source identity')
    stream=VMDK(w/'worker.vmdk')
    for p in layers:
        stream.seek(0);stream=QCow2(p.open('rb'),backing_file=stream).open()
    part=next(p for p in Disk(stream).partitions if p.offset==525336576)
    raw=NTFS(part.open()).mft.get('Windows/System32/ntoskrnl.exe').open().read(32*1024*1024+1)
    if len(raw)>32*1024*1024:raise ValueError('kernel budget')
    target=d/'System32-ntoskrnl.exe';expected=json.loads((d/'kernel-extraction.json').read_bytes())
    if hashlib.sha256(raw).hexdigest()!=expected['sha256']:raise ValueError('retained kernel source identity')
    if target.exists():
        if target.read_bytes()!=raw:raise ValueError('existing kernel mismatch')
    else:target.write_bytes(raw)
    if [identity(p)for p in layers]!=before:raise ValueError('disk changed')
    with out.open('x',encoding='utf8')as f:json.dump(dict(accepted=False,original_bytes_recovered=True,kernel=identity(target),source_disks=before,worker_base_fresh_sha=False),f,indent=2)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);recover(p.parse_args().out)
