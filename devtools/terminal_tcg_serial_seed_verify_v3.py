"""Verify stopped WinPE seed by reading its private FAT and NTFS bytes only."""
import hashlib,json
from pathlib import Path
from dissect.hypervisor.disk.vmdk import VMDK
from dissect.hypervisor.disk.qcow2 import QCow2
from dissect.ntfs import NTFS
from dissect.volume.disk import Disk
from pyfatfs.PyFatFS import PyFatFS
from devtools.isolated_windows_vm import WORKER,identity
from devtools.terminal_tcg_serial_media_v3 import STARTUP

def main():
 case=WORKER/'tcg-serial-seed-v3';r=json.loads((case/'report.json').read_bytes())
 if not r['process_exited'] or r['errors'] or not r.get('guest_poweroff') or not r['parent_size_mtime_unchanged']:raise ValueError('clean ended seed required')
 markers={}
 with PyFatFS(str(case/'seed.private.flp'),read_only=True) as fs:
  for name in ('SEED.START','SEED.OK','SEED.FAIL','COPY.LOG','REG.LOG','USERINIT.BEFORE','USERINIT.AFTER'):
   if fs.exists(name):markers[name]=fs.readbytes(name).decode('ascii')
 if 'SEED.OK' not in markers or 'SEED.FAIL' in markers:raise ValueError('seed did not complete: '+str(markers))
 layers=[WORKER/name/'disk.qcow2' for name in ('tcg-windows-compat-v2','tcg-windows-current-v1','tcg-wait-native-v5','tcg-wait-native-v10',case.name)]
 before=[identity(p) for p in layers]
 if before[-1]['sha256']!=r['overlay']['sha256'] or before[-2]['sha256']!=r['parent']['sha256']:raise ValueError('overlay chain identity')
 stream=VMDK(WORKER/'worker.vmdk')
 for path in layers:
  stream.seek(0);stream=QCow2(path.open('rb'),backing_file=stream).open()
 ntfs=NTFS(next(p for p in Disk(stream).partitions if p.offset==525336576).open())
 expected={'ChaomofaWorker/SerialV3/agent.exe':(WORKER/'tcg-serial-agent-build-v3/agent.exe').read_bytes(),'ChaomofaWorker/SerialV3/CONFIG.TXT':(case/'control-key.private').read_bytes()+bytes([13,10])}
 from dissect.regf import RegistryHive
 hive=RegistryHive(ntfs.mft.get('Windows/System32/config/SOFTWARE').open())
 userinit_value=hive.open('Microsoft/Windows NT/CurrentVersion/Winlogon'.replace('/',chr(92))).value('Userinit')
 if int(userinit_value.type)!=1:raise ValueError('installed Userinit REG_SZ type')
 userinit=userinit_value.value
 if userinit!='C:\\Windows\\system32\\userinit.exe,C:\\ChaomofaWorker\\SerialV3\\agent.exe,':raise ValueError('installed Userinit chain')
 files=[]
 for path,data in expected.items():
  actual=ntfs.mft.get(path).open().read(len(data)+1)
  if actual!=data:raise ValueError('installed bytes mismatch: '+path)
  files.append(dict(path=path,bytes=len(actual),sha256=hashlib.sha256(actual).hexdigest()))
 if before!=[identity(p) for p in layers]:raise ValueError('source changed')
 result=dict(accepted=False,verified=True,overlay=before[-1],sources=before,files=files,userinit=userinit,markers=markers,read_only=True)
 (case/'seed-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
