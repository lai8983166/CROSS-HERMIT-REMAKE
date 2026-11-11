"""60-second headless Windows boot observation on a fresh F-backed overlay.

No network/input/capture migration. Not WOW64 or original-game admission.
Overlay must be prepared with a relative read-only VMDK backing file.
"""
import argparse,json,os,signal,subprocess,time
from pathlib import Path
from devtools.terminal_tcg_roundtrip_probe import QMP,identity

def run(a):
    out=a.output.resolve(); disk=out/'disk.qcow2'
    if not str(out).startswith('/mnt/f/') or not disk.is_file() or (out/'report.json').exists():
        raise ValueError('fresh prepared F overlay required')
    prerequisite=json.loads(a.prerequisite.read_bytes())
    if not prerequisite.get('bounded_case_passed') or prerequisite['binary']['sha256']!=identity(a.binary)['sha256']:
        raise ValueError('same-runtime compatibility restore preflight required')
    parent=out.parent/'worker.vmdk'; before=parent.stat()
    socket='chaomofa-'+out.name+'-qmp';q=None;proc=None;start=time.monotonic()
    command=[str(a.binary.resolve()),'-L',str(a.firmware.resolve()),'-machine','pc',
        '-accel','tcg,thread=single','-smp','2','-m','4G','-display','none',
        '-serial','none','-monitor','none','-nic','none','-no-reboot',
        '-device','mptsas1068,id=scsi0','-drive','file='+str(disk)+',if=none,id=os,format=qcow2',
        '-device','scsi-hd,drive=os,bus=scsi0.0','-boot','c',
        '-qmp','unix:'+socket+',abstract=on,server=on,wait=off']
    r=dict(accepted=False,windows_admitted=False,wow64_verified=False,game_starts=0,
        host_input=0,host_configuration_changes=0,command=command,binary=identity(a.binary),
        prerequisite=identity(a.prerequisite),errors=[],profile='boot-only; no icount/single-instruction replay claim')
    try:
        with (out/'stderr.log').open('xb')as log:
            proc=subprocess.Popen(command,stdout=log,stderr=log,start_new_session=True)
            while q is None:
                if proc.poll()is not None or time.monotonic()-start>8:raise RuntimeError('QMP startup failed')
                try:q=QMP(socket)
                except (FileNotFoundError,ConnectionRefusedError):time.sleep(.1)
            for second in (20,60):
                while time.monotonic()-start<second:
                    if proc.poll()is not None:raise RuntimeError('guest exited before observation')
                    if disk.stat().st_size>128*1024**2:raise RuntimeError('128 MiB overlay budget')
                    time.sleep(.2)
                r['status_'+str(second)]=q.call('query-status')
                r['screen_'+str(second)]=q.call('screendump',{'filename':str(out/('screen-'+str(second)+'.ppm'))})
            r['stop']=q.call('stop')
            r['states']=[q.call('x-query-tcg-state',{'cpu-index':i})for i in range(2)]
            r['quit']=q.call('quit');proc.wait(timeout=5)
    except Exception as exc:r['errors'].append(str(exc))
    finally:
        if proc and proc.poll()is None:os.killpg(proc.pid,signal.SIGKILL);proc.wait(timeout=3)
        if q:q.f.close();q.s.close()
        after=parent.stat()
        r.update(seconds=time.monotonic()-start,all_processes_exited=proc is None or proc.poll()is not None,
            parent_size_mtime_unchanged=(before.st_size,before.st_mtime_ns)==(after.st_size,after.st_mtime_ns),
            parent_full_hash_checked=False,overlay=identity(disk))
        (out/'report.json').write_text(json.dumps(r,indent=2))
    print(json.dumps({k:r[k]for k in ('seconds','errors','all_processes_exited','parent_size_mtime_unchanged')}))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('binary','firmware','output','prerequisite'):p.add_argument('--'+n,type=Path,required=True)
    run(p.parse_args())
