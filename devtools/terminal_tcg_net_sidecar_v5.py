"""Bounded CPU-less user-network sidecar. No host network configuration."""
import argparse,json,subprocess,time,socket
from pathlib import Path
from devtools.isolated_vm_bounded_query_v3 import Job,environment
from devtools.isolated_windows_vm import WORKER
from devtools.terminal_tcg_roundtrip_probe import identity

def run(out):
    out=out.resolve()
    if not out.is_relative_to(WORKER.resolve()) or (out/'sidecar.json').exists():raise ValueError('owned fresh report')
    binary=WORKER/'qemu-worker/runtime/qemu-system-x86_64.exe'
    command=[str(binary),'-machine','none','-m','0','-nodefaults','-display','none','-monitor','none','-serial','none',
        '-qmp','tcp:127.0.0.1:15987,server=on,wait=off',
        '-netdev','socket,id=s,connect=127.0.0.1:15986',
        '-netdev','user,id=u,restrict=on,hostfwd=tcp:127.0.0.1:15985-:5985',
        '-netdev','hubport,id=hs,hubid=0,netdev=s','-netdev','hubport,id=hu,hubid=0,netdev=u']
    r=dict(binary=identity(binary),slirp=identity(binary.parent/'libslirp-0.dll'),command=command,
        virtual_cpus=0,guest_ram_bytes=0,host_input=0,errors=[]);job=Job();proc=None;start=time.monotonic()
    try:
        with (out/'sidecar.stderr').open('xb')as log:
            proc=subprocess.Popen(command,stdout=log,stderr=log,env=environment(),creationflags=subprocess.CREATE_NO_WINDOW)
            job.assign(proc)
            q=None
            while q is None and time.monotonic()-start<5:
                try:q=socket.create_connection(('127.0.0.1',15987),timeout=2)
                except ConnectionRefusedError:time.sleep(.1)
            if q is None:raise RuntimeError('sidecar QMP not ready')
            with q,q.makefile('rwb',buffering=0)as wire:
                r['greeting']=json.loads(wire.readline())
                for name in ('qmp_capabilities','query-status','query-cpus-fast','query-memory-size-summary'):
                    wire.write((json.dumps(dict(execute=name,id=name))+'\n').encode())
                    while True:
                        response=json.loads(wire.readline())
                        if response.get('id')==name:break
                    r[name]=response
            if r['query-status']['return']['running']is not True or r['query-cpus-fast']['return']!=[] or r['query-memory-size-summary']['return']['base-memory']!=0:
                raise RuntimeError('sidecar must run networking with zero CPU and RAM')
            (out/'sidecar-ready.json').write_text(json.dumps(r,indent=2))
            while proc.poll()is None and not (out/'sidecar.stop').exists() and time.monotonic()-start<910:time.sleep(.2)
            if proc.poll()is not None:r['errors'].append('sidecar exited early')
            r['stop_requested']=(out/'sidecar.stop').exists()
    finally:
        job.terminate()
        if proc:proc.wait(timeout=3)
        r.update(seconds=time.monotonic()-start,host_job_active_after=job.active(),process_exited=proc is None or proc.poll()is not None)
        job.close();(out/'sidecar.json').write_text(json.dumps(r,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output',type=Path);run(p.parse_args().output)
