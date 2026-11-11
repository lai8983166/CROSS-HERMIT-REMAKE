"""Bounded isolated Windows lifetime for the owned no-UI wait probe."""
import argparse,json,os,signal,subprocess,time,threading
from pathlib import Path
from devtools.terminal_tcg_roundtrip_probe import QMP,identity

def run(out):
    out=out.resolve();root=Path(__file__).resolve().parents[1];w=root/'.venv-audit/native-worker'
    if not str(out).startswith('/mnt/f/')or(out/'report.json').exists():raise ValueError('fresh F case')
    manifest=json.loads((w/'tcg-cr2-build-v3/manifest.json').read_bytes());binary=Path(manifest['binary']['path'])
    if identity(binary)['sha256']!=manifest['binary']['sha256']:raise ValueError('runtime identity')
    for row in manifest['overlay']:
        if identity(Path(row['path']))['sha256']!=row['sha256']:raise ValueError('runtime source identity')
    parent=w/'tcg-windows-current-v1/disk.qcow2'
    expected=json.loads((root/'analysis/terminal-wait-tcg-windows-control-closeout-v1-20261111.json').read_bytes())['current_disk']
    if identity(parent)['sha256']!=expected['sha256']:raise ValueError('parent identity')
    parents=[w/'worker.vmdk',w/'tcg-windows-compat-v2/disk.qcow2',parent];before=[(p.stat().st_size,p.stat().st_mtime_ns)for p in parents]
    qp='chaomofa-'+out.name+'-qmp';gp='chaomofa-'+out.name+'-gdb';disk=out/'disk.qcow2'
    cmd=[str(binary),'-L',str(w/'qemu-worker/runtime/share'),'-machine','pc','-accel','tcg,thread=single','-smp','2','-m','4G',
        '-uuid','626d1a20-6383-4cd3-85d5-6c9831d6f941','-display','none','-monitor','none','-serial','none','-no-reboot',
        '-netdev','socket,id=n0,listen=127.0.0.1:15986','-device','e1000e,netdev=n0,mac=52:54:00:12:34:56,romfile=',
        '-device','mptsas1068,id=scsi0','-drive','file='+str(disk)+',if=none,id=os,format=qcow2','-device','scsi-hd,drive=os,bus=scsi0.0',
        '-qmp','unix:'+qp+',abstract=on,server=on,wait=off','-gdb','unix:'+gp+',abstract=on,server=on,wait=off']
    r=dict(accepted=False,command=cmd,binary=identity(binary),parent=expected,errors=[],host_input=0);q=p=sidecar=None;done=threading.Event();start=time.monotonic()
    def watch():
        while not done.wait(.1):
            if time.monotonic()-start>900 or disk.stat().st_size>128*1024**2:
                r['errors'].append('900s/128MiB budget');(out/'sidecar.stop').write_text('budget')
                if p and p.poll()is None:os.killpg(p.pid,signal.SIGKILL)
                return
    threading.Thread(target=watch,daemon=True).start()
    try:
        with(out/'stderr.log').open('xb')as log:
            p=subprocess.Popen(['nice','-n','10']+cmd,stdout=log,stderr=log,start_new_session=True)
            while q is None:
                if p.poll()is not None or time.monotonic()-start>8:raise RuntimeError('startup')
                try:q=QMP(qp)
                except(FileNotFoundError,ConnectionRefusedError):time.sleep(.1)
            sidecar=subprocess.Popen([str(w.parent/'Scripts/python.exe'),'-B','-m','devtools.terminal_tcg_net_sidecar_v5','F:/project/chaomofa/'+str(out.relative_to(root))],cwd=root)
            while time.monotonic()-start<180:
                if p.poll()is not None or sidecar.poll()is not None:raise RuntimeError('early exit')
                time.sleep(.2)
            r['boot_status']=q.call('query-status');q.call('screendump',{'filename':str(out/'boot.ppm')})
            r['boot_qmp']=q.receipts;q.f.close();q.s.close();q=None
            (out/'vm-ready.json').write_text(json.dumps(dict(qmp=qp,gdb=gp,pid=p.pid,seconds=time.monotonic()-start)))
            while not(out/'vm-stop').exists()and p.poll()is None and time.monotonic()-start<885:time.sleep(.2)
            q=QMP(qp);r['quit']=q.call('quit');p.wait(timeout=5)
    except Exception as exc:r['errors'].append(type(exc).__name__+': '+str(exc))
    finally:
        done.set()
        if p and p.poll()is None:os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=3)
        (out/'sidecar.stop').write_text('stop')
        if sidecar:
            try:sidecar.wait(timeout=6)
            except subprocess.TimeoutExpired:r['errors'].append('sidecar cleanup timeout')
        if q:q.f.close();q.s.close()
        r.update(seconds=time.monotonic()-start,process_exited=p is None or p.poll()is not None,
            parent_size_mtime_unchanged=before==[(x.stat().st_size,x.stat().st_mtime_ns)for x in parents],overlay=identity(disk))
        (out/'report.json').write_text(json.dumps(r,indent=2))
    print(json.dumps({k:r[k]for k in ('seconds','errors','process_exited','parent_size_mtime_unchanged')}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output',type=Path);run(p.parse_args().output)
