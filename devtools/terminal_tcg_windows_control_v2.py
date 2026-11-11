"""Bounded headless boot diagnosis with isolated loopback WinRM forwarding.

Uses one 2 VP/4 GiB VM and a fresh overlay of the retained boot overlay.
No host input, TAP/bridge, network settings or original disk writes.
"""
import argparse,json,os,signal,socket,subprocess,time
from pathlib import Path
from devtools.terminal_tcg_roundtrip_probe import QMP,identity

UUID='626d1a20-6383-4cd3-85d5-6c9831d6f941'

def run(a):
    out=a.output.resolve();root=Path(__file__).resolve().parents[1];w=root/'.venv-audit/native-worker'
    disk=out/'disk.qcow2'
    if not str(out).startswith('/mnt/f/') or not disk.is_file() or (out/'report.json').exists():raise ValueError('fresh F overlay')
    manifest=json.loads(a.manifest.read_bytes());binary=Path(manifest['binary']['path'])
    if identity(binary)['sha256']!=manifest['binary']['sha256']:raise ValueError('runtime identity')
    for row in manifest['modified_source']:
        if identity(Path(row['path']))['sha256']!=row['sha256']:raise ValueError('source identity')
    parents=[w/'worker.vmdk',w/'tcg-windows-compat-v2/disk.qcow2'];before=[(p.stat().st_size,p.stat().st_mtime_ns)for p in parents]
    prior=json.loads((w/'tcg-windows-compat-v2/report.json').read_bytes())
    if identity(parents[1])['sha256']!=prior['overlay']['sha256']:raise ValueError('retained parent overlay changed')
    # Only a loopback listener; restrict=on disallows guest-initiated external routing.
    command=[str(binary),'-L',str(w/'qemu-worker/runtime/share'),'-machine','pc','-accel','tcg,thread=single',
        '-smp','2','-m','4G','-uuid',UUID,'-display','none','-serial','none','-monitor','none','-no-reboot',
        '-netdev','socket,id=n0,listen=127.0.0.1:15986',
        '-device','e1000e,netdev=n0,mac=52:54:00:12:34:56',
        '-device','mptsas1068,id=scsi0','-drive','file='+str(disk)+',if=none,id=os,format=qcow2',
        '-device','scsi-hd,drive=os,bus=scsi0.0','-boot','c',
        '-qmp','unix:chaomofa-'+out.name+',abstract=on,server=on,wait=off']
    r=dict(accepted=False,windows_admitted=False,wow64_verified=False,game_starts=0,host_input=0,host_configuration_changes=0,
        command=command,manifest=identity(a.manifest),binary=identity(binary),observations=[],errors=[])
    q=proc=sidecar=None;start=time.monotonic()
    try:
        with (out/'stderr.log').open('xb')as log:
            proc=subprocess.Popen(['nice','-n','10']+command,stdout=log,stderr=log,start_new_session=True)
            while q is None:
                if proc.poll()is not None or time.monotonic()-start>8:raise RuntimeError('QMP startup')
                try:q=QMP('chaomofa-'+out.name)
                except (FileNotFoundError,ConnectionRefusedError):time.sleep(.1)
            winout='F:/project/chaomofa/'+str(out.relative_to(root))
            sidecar=subprocess.Popen([str(w.parent/'Scripts/python.exe'),'-B','-X','utf8','-m','devtools.terminal_tcg_net_sidecar',winout],cwd=root)
            for seconds in (30,90,180):
                while time.monotonic()-start<seconds:
                    if proc.poll()is not None:raise RuntimeError('early VM exit')
                    if disk.stat().st_size>128*1024**2:raise RuntimeError('128 MiB overlay budget')
                    time.sleep(.2)
                obs=dict(seconds=time.monotonic()-start,status=q.call('query-status'),blockstats=q.call('query-blockstats'))
                obs['screen']=q.call('screendump',{'filename':str(out/f'screen-{seconds}.ppm')})
                q.call('stop');obs['states']=[q.call('x-query-tcg-state',{'cpu-index':i})for i in range(2)];q.call('cont')
                r['observations'].append(obs)
                if seconds>=90:
                    result=subprocess.run([str(w.parent/'Scripts/python.exe'),'-B','-X','utf8','-m','devtools.terminal_tcg_guest_query','status'],
                        cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=25)
                    obs['control']=json.loads(result.stdout)
                    control=obs['control']
                    good=(not control.get('errors') and not control.get('timed_out') and control.get('host_job_active_after')==0
                        and control.get('host_exit_code')==0 and control.get('remote_completion')=='observed' and control.get('response',{}).get('ok')is True)
                    if good:
                        r['control_connected']=True
                        wow=subprocess.run([str(w.parent/'Scripts/python.exe'),'-B','-X','utf8','-m','devtools.terminal_tcg_guest_query','wow64'],
                            cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=25)
                        r['wow64']=json.loads(wow.stdout);break
            r['quit']=q.call('quit');proc.wait(timeout=5)
    except Exception as exc:r['errors'].append(type(exc).__name__+': '+str(exc))
    finally:
        if proc and proc.poll()is None:os.killpg(proc.pid,signal.SIGKILL);proc.wait(timeout=3)
        (out/'sidecar.stop').write_text('stop')
        if sidecar:
            try:sidecar.wait(timeout=6)
            except subprocess.TimeoutExpired:r['errors'].append('sidecar supervision did not finish within cleanup budget')
        if q:r['qmp']=q.receipts;q.f.close();q.s.close()
        r.update(seconds=time.monotonic()-start,all_processes_exited=proc is None or proc.poll()is not None,
            parent_size_mtime_unchanged=before==[(p.stat().st_size,p.stat().st_mtime_ns)for p in parents],overlay=identity(disk))
        (out/'report.json').write_text(json.dumps(r,indent=2))
    print(json.dumps({k:r.get(k)for k in ('seconds','errors','control_connected','all_processes_exited','parent_size_mtime_unchanged')}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--manifest',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    run(p.parse_args())
