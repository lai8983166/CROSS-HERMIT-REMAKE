"""Bounded diskless SMP context filter proof, never Windows acceptance."""
import json,os,signal,subprocess,time,threading
from pathlib import Path
from devtools.terminal_tcg_roundtrip_probe import QMP,RSP,identity
ROOT=Path(__file__).resolve().parents[1]; WORK=ROOT/'.venv-audit/native-worker'
OUT=WORK/'tcg-context-preflight-v3'
def run(role,binary,guest,syms,filtered):
    out=OUT/role;out.mkdir(); q='context-'+role+'-q';g='context-'+role+'-g'
    cmd=[str(binary),'-L',str(WORK/'tcg-build-v1/source/pc-bios'),'-machine','pc','-accel','tcg,thread=single','-smp','2','-m','64M','-icount','shift=0,align=off,sleep=off','-rtc','clock=vm,base=2026-11-11T00:00:00','-display','none','-serial','none','-monitor','none','-nic','none','-no-reboot','-kernel',str(guest),'-debugcon','file:'+str(out/'output.bin'),'-device','isa-debug-exit,iobase=0xf4,iosize=4','-S','-qmp','unix:'+q+',abstract=on,server=on,wait=off','-gdb','unix:'+g+',abstract=on,server=on,wait=off']
    err=(out/'stderr').open('wb');p=subprocess.Popen(cmd,stdout=err,stderr=err,start_new_session=True)
    result=dict(command=cmd,binary=identity(binary),errors=[]);qmp=rsp=None;start=time.monotonic();done=threading.Event()
    def watchdog():
        if not done.wait(25):
            result['errors'].append('25s timeout')
            if p.poll() is None:os.killpg(p.pid,signal.SIGKILL)
    threading.Thread(target=watchdog,daemon=True).start()
    try:
        while qmp is None:
            if p.poll() is not None or time.monotonic()-start>5:raise RuntimeError('startup')
            try:qmp=QMP(q)
            except (FileNotFoundError,ConnectionRefusedError):time.sleep(.02)
        rsp=RSP(g)
        def call(n,a=None):
            r=qmp.call(n,a)
            if 'error'in r:raise ValueError(r)
            return r['return']
        def ctx(c):return json.loads(call('x-query-tcg-state',{'cpu-index':c})['state'])
        def bp(op,s):
            if rsp.command(f'{op}1,{syms[s]:x},1')!='OK':raise ValueError('breakpoint')
        def cont():
            r=rsp.command('c')
            if not r.startswith('T05'):raise ValueError('stop '+r)
            return [ctx(i) for i in range(2)]
        bp('Z','ctx_arm');result['start']=cont();bp('z','ctx_arm')
        if filtered:
            result['empty_arm_rejected']='error'in qmp.call('x-query-tcg-state',{'cpu-index':-4})
            bp('Z','ctx_hit');bp('Z','ctx_next');result['arm']=ctx(-4)
            result['double_arm_rejected']='error'in qmp.call('x-query-tcg-state',{'cpu-index':-4})
            result['hit']=cont();result['hit_status']=ctx(-6)
            bp('z','ctx_hit');result['refresh']=ctx(-7)
            result['next']=cont();bp('z','ctx_next')
        bp('Z','ctx_end')
        if filtered:result['refresh_end']=ctx(-7)
        result['end']=cont()
        result['checkpoint']=json.loads(call('x-query-tcg-checkpoint')['state'])
        result['hit_count']=int.from_bytes(bytes.fromhex(rsp.command(f'm{syms["hit_count"]:x},4')),'little')
        if filtered:
            result['disabled']=ctx(-5);result['double_disable_rejected']='error'in qmp.call('x-query-tcg-state',{'cpu-index':-5})
        bp('z','ctx_end');rsp.resume();result['exit']=p.wait(timeout=5)
    except Exception as exc:result['errors'].append(type(exc).__name__+': '+str(exc))
    finally:
        done.set()
        if p.poll() is None:os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=3)
        if qmp:result['qmp']=qmp.receipts;qmp.f.close();qmp.s.close()
        if rsp:rsp.s.close()
        err.close();result['process_exited']=p.poll() is not None;result['elapsed']=time.monotonic()-start
        result['output']=(out/'output.bin').read_bytes().hex() if(out/'output.bin').exists()else None
        (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

def main():
    OUT.mkdir(exist_ok=False)
    guest=WORK/'tcg-context-micro-v2/guest.elf'
    syms={r.split()[2]:int(r.split()[0],16) for r in subprocess.check_output(['nm','-n',str(guest)],text=True).splitlines()}
    a=run('baseline',WORK/'tcg-cr2-build-v4/qemu-system-x86_64',guest,syms,False)
    b=run('filtered',WORK/'tcg-context-build-v1/qemu-system-x86_64',guest,syms,True)
    status=b.get('hit_status',{})
    checks=dict(no_errors=not a['errors']and not b['errors'],endpoint_cpu=a.get('end')==b.get('end'),endpoint_checkpoint=a.get('checkpoint')==b.get('checkpoint'),natural_exits=a.get('exit')==b.get('exit')==33,output=a['output']==b['output']=='43',guest_hit_count=a.get('hit_count')==b.get('hit_count')==4,foreign_cpu=status.get('cpu_rejected')==2,foreign_cr3=status.get('cr3_rejected')==2,foreign_r13=status.get('r13_rejected')==2,foreign_total=status.get('rejected')==6,target_stop=status.get('accepted')==1 and int(b.get('hit',[{}])[0].get('eip','0'),16)==syms['ctx_hit'],adjacent_point=int(b.get('next',[{}])[0].get('eip','0'),16)==syms['ctx_next'],disabled=b.get('disabled',{}).get('active')is False,unpoisoned=b.get('disabled',{}).get('poisoned')is False,empty_arm=b.get('empty_arm_rejected',False),double_arm=b.get('double_arm_rejected',False),double_disable=b.get('double_disable_rejected',False))
    proof=dict(accepted=False,windows_admitted=False,preflight_passed=all(checks.values()),checks=checks,binary_sha256=identity(WORK/'tcg-context-build-v1/qemu-system-x86_64')['sha256'],guest=identity(guest),symbols=syms,reports=[identity(OUT/r/'report.json')for r in('baseline','filtered')])
    (OUT/'proof.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
if __name__=='__main__':main()
