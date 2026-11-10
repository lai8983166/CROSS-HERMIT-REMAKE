"""Owned, thread-scoped kernel wait preflight. Never game/fullstate acceptance."""
import concurrent.futures as cf
import json
from pathlib import PureWindowsPath
import re
import time
from devtools.isolated_windows_vm import WORKER,VMX,vmrun,identity
from devtools.isolated_vm_kd import run_guest,validate_kd_vmx
from devtools.isolated_vm_guest_admin import STATUS
from devtools.terminal_kd_session import need
from devtools.terminal_kd_session_v3 import Session

D=WORKER/'kd-thread-v4-20261110'
G=PureWindowsPath('C:/ChaomofaWorker/kd-thread-v4-20261110')


def words(text):
    out={}
    for line in text.splitlines():
        f=line.split()
        if not f or not re.fullmatch('[0-9a-f]{8}`[0-9a-f]{8}',f[0]):continue
        a=int(f[0].replace('`',''),16)
        for i,v in enumerate(f[1:]):
            if re.fullmatch('[0-9a-f]{8}`[0-9a-f]{8}',v):out[a+i*8]=int(v.replace('`',''),16)
    return out


def evaluation(text):
    m=re.search(r'Evaluate expression:.*= ([0-9a-f`]+)',text)
    need(m,'actual debugger evaluation');return int(m[1].replace('`',''),16)


def collect(name,seconds):
    target=D/('guest-'+name);need(not target.exists(),'fresh guest transfer')
    end=time.monotonic()+seconds
    while time.monotonic()<end:
        value=run_guest("if(Test-Path -LiteralPath '"+(G/name).as_posix()+"'){[IO.File]::ReadAllText('"+(G/name).as_posix()+"')}else{'NOT_READY'}").strip()
        if value!='NOT_READY':
            obj=json.loads(value);target.write_text(value);return obj
        time.sleep(.1)
    raise TimeoutError('bounded file '+name)


def main():
    out=D/'probe.json';need(not out.exists(),'fresh native probe')
    r=dict(accepted=False,fullstate=False,fullABI=False,original_game_starts=0,host_input_actions=0,errors=[],stops=[],unrelated=[],phases=[])
    s=None;pool=cf.ThreadPoolExecutor(max_workers=3);pending=[];launch=None;t=time.monotonic()
    def phase(name):
        r['phases'].append(dict(name=name,seconds=time.monotonic()-t));(D/'progress.json').write_text(json.dumps(r,indent=2));print(name,flush=True)
    def readq(a,n):return s.execute('dq %x L%x'%(a,n))
    def query(c):return s.execute(c)
    try:
        validate_kd_vmx(VMX.read_text(encoding='utf8'))
        r['guest_before']=json.loads(run_guest(STATUS))
        r['kernel_sha256']=run_guest('(Get-FileHash C:/Windows/System32/ntoskrnl.exe -Algorithm SHA256).Hash').strip().lower()
        need(r['kernel_sha256']=='5669b9b8bfcf20f08b7d1d65dc2deccbf836279c0e3f66722d72ad33ee7f672a','fixed kernel bytes')
        launch=pool.submit(vmrun,['runProgramInGuest',VMX,'-noWait',PureWindowsPath('C:/ChaomofaWorker/Python/pythonw.exe'),'-B',G/'supervisor.py',G],guest=True,timeout=15)
        prepared=collect('supervisor-ready.json',15);r['prepared']=prepared;ready=prepared['ready'];module=prepared['module']
        need(module['sha256']=='6d3e9d039c22b58c577435ef0209d43668ef2003e284be9980e4ad1289045a66','loaded module file')
        need(ready['source_sha256']==identity(D/'fixture/terminal_vm_wait_fixture.cs')['sha256'],'fixture source binding')
        phase('fixture ready and actual native module identified')
        s=Session(D/'debugger.log');s.wait_prompt(15);r['pipe_server_pid']=s.server_pid;r['client']=s.client
        r['kernel_module']=query('lm m nt')
        m=re.search(r'([0-9a-f]+`[0-9a-f]+)\s+[0-9a-f`]+\s+nt\s',r['kernel_module']);need(m,'live kernel module base')
        base=int(m[1].replace('`',''),16);tail=base+0x6fcc6a;r['kernel_base']=base
        r['owned_process_threads']=query('!process %x 2'%ready['pid'])
        proc=re.search(r'PROCESS ([0-9a-f`]+)',r['owned_process_threads']);need(proc,'EPROCESS enumeration')
        pairs=re.findall(r'THREAD ([0-9a-f`]+)\s+Cid ([0-9a-f]+)\.([0-9a-f]+)',r['owned_process_threads'])
        match=[a for a,pid,tid in pairs if int(pid,16)==ready['pid']and int(tid,16)==ready['tid']]
        need(len(match)==1,'current ETHREAD for exact fixture PID/TID')
        ep=int(proc[1].replace('`',''),16);et=int(match[0].replace('`',''),16);r['objects']=dict(eprocess=ep,ethread=et)
        r['tail_before']=query('u %x L2'%tail)
        need('4883c438'in r['tail_before']and'c3'in r['tail_before'],'fixed kernel tail bytes')
        query('ba e 1 /p %x /t %x %x'%(ep,et,tail));r['breakpoint']=query('bl');need(' e 'in r['breakpoint'],'enabled scoped breakpoint')
        s.go();phase('scoped breakpoint armed; explicit continuation monitor active')
        gate=D/'go.txt';gate.write_text('continue')
        gate_future=pool.submit(vmrun,['CopyFileFromHostToGuest',VMX,gate,G/'go'],guest=True,timeout=15);pending.append(gate_future)
        gate_recorded=False
        end=time.monotonic()+60
        while len(r['stops'])<4 and time.monotonic()<end:
            if gate_future.done() and not gate_recorded:
                try:r['gate_transfer']=dict(result=gate_future.result(),seconds=time.monotonic()-t)
                except Exception as e:r['gate_transfer']=dict(error=repr(e),seconds=time.monotonic()-t)
                gate_recorded=True;phase('gate transfer completed')
            stop=s.poll_stop()
            if stop is None:time.sleep(.02);continue
            regtext=query('r');regs={k:int(v,16)for k,v in re.findall(r'(\w+)=([0-9a-f]{16})',regtext)}
            need(regs.get('rip')==tail,'only the owned kernel wait-tail breakpoint')
            row=dict(registers=regtext,pid=query('? @$tpid'),tid=query('? @$tid'),thread=query('? @$thread'),process=query('? @$proc'))
            need(evaluation(row['pid'])==ready['pid']and evaluation(row['tid'])==ready['tid']and evaluation(row['thread'])==et and evaluation(row['process'])==ep,'live owner at every stop')
            sp,bp=regs['rsp'],regs['rbp'];row['stack']=readq(sp,0x20);row['trap']=readq(bp-0x80,0x32)
            stack,trap=words(row['stack']),words(row['trap'])
            if trap.get(bp-0x48)!=ready['event_handle']:
                r['unrelated'].append(row);need(len(r['unrelated'])<=12,'bounded same-thread unrelated waits');s.go();continue
            i=len(r['stops']);r['stops'].append(row);row['index']=i
            need(regs['rax']==(258 if i==3 else 0),'actual kernel wait status')
            need(stack.get(sp+0x38)==base+0x428c35,'actual syscall caller')
            need(trap[bp-0x40]&0xff==0 and trap[bp+0xf0]&0xffff==0x33,'original alertable and return mode')
            need(trap[bp+0xe8]==module['image_base']+0x1cf3,'independently bound native syscall return PC')
            need(stack[sp+0x50]==sp+0x58 and stack[sp+0x58]==(0 if i==3 else 0xfffffffffeced300),'actual captured timeout value')
            row['fixture_counter']=readq(ready['data']+0x200,1)
            need(words(row['fixture_counter'])[ready['data']+0x200]&0xffffffff==i,'native postcall sequence')
            row['syscall_bytes']=query('db %x L18'%(module['image_base']+0x1ce0))
            row['debug_registers']=query('r dr0,dr1,dr2,dr3,dr6,dr7')
            # Bounded raw kernel storage: preserved as candidates, never called fullstate.
            pcr=evaluation(query('? @$pcr'));row['pcr_prcb']=readq(pcr+0x20,1);prcb=words(row['pcr_prcb'])[pcr+0x20]
            need(prcb>=0xffff000000000000,'kernel PRCB pointer')
            row['prcb_thread']=readq(prcb+8,1);need(words(row['prcb_thread'])[prcb+8]==et,'PRCB current thread')
            row['prcb_context_pointer']=readq(prcb+0x8980,2);context=words(row['prcb_context_pointer'])[prcb+0x8980]
            need(context>=0xffff000000000000,'kernel saved-context pointer')
            row['kernel_context_raw']=query('db %x L4d0'%context)
            row['special_registers_raw']=query('db %x Lf0'%(prcb+0x100))
            if 0x10000<regs['r13']<0x80000000:row['wow64_save_candidate']=query('db %x L2d0'%(regs['r13']-0x80))
            phase('captured owned wait tail '+str(i))
            if i==3:
                r['tail_after']=query('u %x L2'%tail);query('bc *');r['breakpoints_after']=query('bl')
                need(not re.search(r'^\s*\d+ e ',r['breakpoints_after'],re.M),'owned breakpoint removed')
            s.go()
        need(len(r['stops'])==4,'all four owned wait tails captured')
        future=pool.submit(collect,'supervisor.json',15);pending.append(future)
        while not future.done():
            need(s.poll_stop()is None,'unexpected stop after breakpoint cleanup');time.sleep(.05)
        r['completion']=future.result();result=r['completion']['fixture_result']
        need(r['completion']['exit_code']==0 and not r['completion']['errors']and result['error']is None and result['returns']==[0,0,0,258],'normal four fixture returns')
        need(not result['cleanup_errors']and result['handles_closed']and result['buffers_released'],'own resource cleanup')
        r['guest_after']=json.loads(run_guest(STATUS));s.close_after_resume();r['client_closed_after_guest_response']=True
        for f in pending:f.result()
        phase('four kernel boundaries and own fixture cleanup complete; fullstate unqualified')
    except Exception as exc:r['errors'].append(repr(exc));phase('refused: '+repr(exc))
    finally:
        if s:
            try:
                if s.process.poll()is None:
                    if s.observe_prompt():query('bc *');s.go()
                    end=time.monotonic()+5
                    while time.monotonic()<end:
                        stopped=s.poll_stop()
                        if stopped is not None:query('bc *');s.go()
                        time.sleep(.05)
                    r['recovery_guest']=json.loads(run_guest(STATUS));s.close_after_resume()
                r['pending_debugger_breaks']=s.pending_breaks;r['commands']=s.rows;r['transcript']=identity(s.log)
            except Exception as exc:r['errors'].append('recovery: '+repr(exc))
        if s:
            r['session_state']=s.state;r['transitions']=s.transitions;r['commands']=s.rows;r['transcript']=identity(s.log)
        pool.shutdown(wait=True)
        if launch:
            try:r['launch_command_result']=launch.result()
            except Exception as exc:r['launch_command_error']=repr(exc)
        r['elapsed_seconds']=time.monotonic()-t
        out.write_text(json.dumps(r,indent=2))
    print(json.dumps(dict(errors=r['errors'],stops=len(r['stops']),elapsed_seconds=r['elapsed_seconds'],accepted=False)))
    return bool(r['errors'])


if __name__=='__main__':raise SystemExit(main())
