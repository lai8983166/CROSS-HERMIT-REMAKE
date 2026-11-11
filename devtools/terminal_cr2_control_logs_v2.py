"""Recover bounded ended-guest control logs without another Windows boot."""
import json
from pathlib import Path
from dissect.hypervisor.disk.vmdk import VMDK
from dissect.hypervisor.disk.qcow2 import QCow2
from dissect.ntfs import NTFS
from dissect.volume.disk import Disk
from devtools.terminal_tcg_roundtrip_probe import identity


def run():
    root=Path(__file__).resolve().parents[1];work=root/'.venv-audit/native-worker'
    out=work/'tcg-cr2-control-logs-v2';out.mkdir(exist_ok=False)
    case=work/'tcg-wait-native-v7';receipt=json.loads((case/'report.json').read_bytes())
    if not receipt['process_exited']:raise ValueError('ended guest required')
    layers=[work/n/'disk.qcow2'for n in ('tcg-windows-compat-v2','tcg-windows-current-v1','tcg-wait-native-v5','tcg-wait-native-v7')]
    before=[identity(p)for p in layers]
    if before[-1]['sha256']!=receipt['overlay']['sha256'] or before[-2]['sha256']!=receipt['parent']['sha256']:raise ValueError('source identity')
    stream=VMDK(work/'worker.vmdk')
    for path in layers:
        stream.seek(0);stream=QCow2(path.open('rb'),backing_file=stream).open()
    ntfs=NTFS(next(p for p in Disk(stream).partitions if p.offset==525336576).open())
    report=dict(accepted=False,sources=before,base_fresh_sha=False,files=[],missing=[])
    for name in ('Application.evtx','Windows PowerShell.evtx','Microsoft-Windows-WinRM%4Operational.evtx'):
        try:raw=ntfs.mft.get('Windows/System32/winevt/Logs/'+name).open().read(32*1024**2+1)
        except FileNotFoundError:report['missing'].append(name);continue
        if len(raw)>32*1024**2:raise ValueError('32MiB log budget')
        path=out/name;path.write_bytes(raw);report['files'].append(identity(path))
    names=list(ntfs.mft.get('ChaomofaWorker').listdir(ignore_dos=True));report['owned_directories']=names
    for name in ('tcg-wait-native-v5','tcg-wait-native-v7'):
        if name in names:report[name]=list(ntfs.mft.get('ChaomofaWorker/'+name).listdir(ignore_dos=True))
    if before!=[identity(p)for p in layers]:raise ValueError('source changed')
    (out/'report.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items()if k not in ('sources','files')}))

if __name__=='__main__':run()
