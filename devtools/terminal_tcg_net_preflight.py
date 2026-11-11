"""Five-second real ARP exchange through CPU-less QEMU network sidecar."""
import argparse,json,socket,struct,subprocess,sys,time
from pathlib import Path
from devtools.isolated_windows_vm import WORKER

def run(out):
    out=out.resolve();out.mkdir(exist_ok=False);proc=None;start=time.monotonic();r=dict(accepted=False,errors=[])
    try:
        with socket.socket()as server:
            server.bind(('127.0.0.1',15986));server.listen(1);server.settimeout(5)
            proc=subprocess.Popen([sys.executable,'-B','-m','devtools.terminal_tcg_net_sidecar_v2',str(out)],creationflags=subprocess.CREATE_NO_WINDOW)
            conn,_=server.accept()
            with conn:
                conn.settimeout(5);mac=bytes.fromhex('525400123456')
                frame=b'\xff'*6+mac+bytes.fromhex('08060001080006040001')+mac+bytes([10,0,2,15])+b'\0'*6+bytes([10,0,2,2])
                conn.sendall(struct.pack('!I',len(frame))+frame)
                def read(n):
                    data=b''
                    while len(data)<n:
                        part=conn.recv(n-len(data))
                        if not part:raise EOFError('network stream')
                        data+=part
                    return data
                size=struct.unpack('!I',read(4))[0]
                if size>2048:raise ValueError('packet budget')
                reply=read(size);r.update(request_hex=frame.hex(),response_hex=reply.hex())
                r['arp_reply_valid']=(reply[:6]==mac and reply[12:14]==bytes.fromhex('0806') and reply[20:22]==b'\0\2' and reply[28:32]==bytes([10,0,2,2]))
                if not r['arp_reply_valid']:raise ValueError('unexpected ARP response')
    except Exception as exc:r['errors'].append(type(exc).__name__+': '+str(exc))
    finally:
        (out/'sidecar.stop').write_text('stop')
        if proc:proc.wait(timeout=8)
        r['seconds']=time.monotonic()-start
        r['sidecar']=json.loads((out/'sidecar.json').read_bytes())if (out/'sidecar.json').exists()else None
        r['passed']=bool(r.get('arp_reply_valid')and not r['errors'] and r['sidecar'] and r['sidecar']['host_job_active_after']==0)
        (out/'report.json').write_text(json.dumps(r,indent=2))
    print(json.dumps({k:r.get(k)for k in ('passed','seconds','errors')}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output',type=Path);run(p.parse_args().output)
