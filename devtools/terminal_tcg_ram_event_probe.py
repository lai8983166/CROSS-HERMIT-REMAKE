"""Full RAM migration plus native guest #DB/IRETD/RF continuation, bounded.

Own diskless ELF only. Source and fresh destination run sequentially, never
two 4 GiB machines at once. This does not validate original game lifetimes.
"""
import argparse,ast,hashlib,json,os,signal,struct,subprocess,threading,time
from pathlib import Path
from devtools.terminal_tcg_roundtrip_probe import QMP,RSP,identity


def image(root,point):
    tree=ast.parse((root/'devtools/terminal_tcg_predecessor_probe_v3.py').read_text())
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='image')
    scope={'struct':struct};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<frozen-event-builder>','exec'),scope)
    elf=bytearray(scope['image']())
    # Add an ordinary guest RAM store after natural result consumption. This
    # makes A/B distinguishable without host memory/register injection.
    end=bytes.fromhex('b052e6e9a0002010000430e6e9b045e6e9')
    end+=bytes.fromhex('c7050021100001adc0de')
    b=0x100305+len(end)
    end+=bytes.fromhex('b810000000e7f4f4ebfd')
    elf[4096+0x305:4096+0x305+len(end)]=end
    points={'before_call':0x100300,'before_iret':0x100433,'rf_return':0x100305}
    if elf[4096+0x433]!=0xcf:raise ValueError('frozen IRETD address')
    return bytes(elf),dict(a=points[point],b=b,point=point,ram_marker=0x102100)


class VM:
    def __init__(self,args,out,role,expected,incoming=False):
        self.out=out;self.role=role;self.expected=expected
        qp,gp=['chaomofa-'+out.name+'-'+role+'-'+s for s in ('qmp','gdb')]
        self.command=[str(args.binary.resolve()),'-L',str(args.firmware.resolve()),'-machine','pc',
            '-accel','tcg,thread=single,one-insn-per-tb=on','-smp','2','-m','4G',
            '-display','none','-serial','none','-monitor','none','-nic','none','-no-reboot',
            '-kernel',str(out/'guest.elf'),'-debugcon','file:'+str(out/(role+'.bin')),
            '-device','isa-debug-exit,iobase=0xf4,iosize=4','-S',
            '-qmp','unix:'+qp+',abstract=on,server=on,wait=off',
            '-gdb','unix:'+gp+',abstract=on,server=on,wait=off',
            '-d','exec,int,nochain','-dfilter','0x100000..0x105000','-D',str(out/(role+'.trace'))]
        if incoming:self.command+=['-incoming','defer']
        self.err=(out/(role+'.stderr')).open('wb')
        self.proc=subprocess.Popen(self.command,stdout=self.err,stderr=self.err,start_new_session=True)
        self.qmp=self.rsp=None;start=time.monotonic()
        while self.qmp is None:
            if self.proc.poll()is not None or time.monotonic()-start>5:raise RuntimeError('startup failed')
            try:self.qmp=QMP(qp)
            except (FileNotFoundError,ConnectionRefusedError):time.sleep(.05)
        self.qmp.s.settimeout(45);self.rsp=RSP(gp)
    def call(self,name,args=None):
        r=self.qmp.call(name,args)
        if 'error'in r:raise ValueError(r)
        return r['return']
    def bp(self,op,pc):
        if self.rsp.command(f'{op}1,{pc:x},1')!='OK':raise ValueError('breakpoint refused')
    def stop(self):
        if not self.rsp.command('c').startswith('T05'):raise ValueError('unexpected stop')
    def sample(self,pc):
        states=[json.loads(self.call('x-query-tcg-state',{'cpu-index':i})['state'])for i in range(2)]
        if int(states[0]['eip'],16)!=pc:raise ValueError('wrong stopped PC')
        if any(s['cpu']!=i or s['vp_stopped']!=[dict(cpu=0,stopped=True),dict(cpu=1,stopped=True)]for i,s in enumerate(states)):
            raise ValueError('VP identity/stopped')
        observation=json.loads(self.call('x-query-tcg-checkpoint')['state'])
        memory=bytes.fromhex(self.rsp.command('m102000,200'))
        return dict(states=states,observation=observation,guest_memory=memory.hex())
    def migration_done(self):
        start=time.monotonic()
        while time.monotonic()-start<45:
            status=self.call('query-migrate')
            if status.get('status')=='completed':return status
            if status.get('status')in ('failed','cancelled'):raise ValueError(status)
            time.sleep(.1)
        raise TimeoutError('migration 45 second budget')
    def exit(self):
        self.bp('z',self.expected['b']);self.rsp.resume()
        return self.proc.wait(timeout=5)
    def close(self):
        if self.proc.poll()is None:os.killpg(self.proc.pid,signal.SIGKILL);self.proc.wait(timeout=3)
        if self.qmp:self.qmp.f.close();self.qmp.s.close()
        if self.rsp:self.rsp.s.close()
        self.err.close()


def run(args):
    root=Path(__file__).resolve().parents[1];out=args.output.resolve()
    if not str(out).startswith('/mnt/f/'):raise ValueError('F-backed output only')
    out.mkdir(exist_ok=False);elf,expected=image(root,args.point);(out/'guest.elf').write_bytes(elf)
    stream=out/'checkpoint.bin';vms=[];done=threading.Event();started=time.monotonic()
    report=dict(accepted=False,full57=False,windows_admitted=False,windows_boots=0,game_starts=0,
        binary=identity(args.binary),expected=expected,errors=[],deadline_seconds=120,
        migration_budget_bytes=64*1024**2,trace_budget_bytes=2*1024**2,simultaneous_vms=1)
    def watchdog():
        while not done.wait(.1):
            over=stream.exists()and stream.stat().st_size>64*1024**2
            over|=any(p.stat().st_size>2*1024**2 for p in out.glob('*.trace'))
            if over or time.monotonic()-started>120:
                report['errors'].append('size/time budget exceeded')
                for vm in vms:
                    if vm.proc.poll()is None:os.killpg(vm.proc.pid,signal.SIGKILL)
                return
    threading.Thread(target=watchdog,daemon=True).start()
    try:
        source=VM(args,out,'source',expected);vms.append(source)
        source.bp('Z',expected['a']);source.stop();report['source_a']=source.sample(expected['a'])
        report['prefix_bytes']=(out/'source.bin').stat().st_size
        source.bp('z',expected['a'])
        # Standard complete migration path writes configuration, RAM and devices.
        source.call('migrate-set-parameters',{'max-bandwidth':1073741824})
        source.call('migrate',{'uri':'file:'+str(stream)})
        report['outgoing']=source.migration_done();report['checkpoint']=identity(stream)
        source.bp('Z',expected['b']);source.stop();report['source_b']=source.sample(expected['b'])
        report['source_exit']=source.exit();source.close()
        # The source is already gone: no shared RAM or live-handle shortcut.
        target=VM(args,out,'target',expected,incoming=True);vms.append(target)
        target.call('migrate-incoming',{'uri':'file:'+str(stream)})
        report['incoming']=target.migration_done()
        report['target_status']=target.call('query-status')
        if report['target_status']['running']:raise ValueError('incoming ran before observation')
        report['target_a']=target.sample(expected['a'])
        target.bp('Z',expected['b']);target.stop();report['target_b']=target.sample(expected['b'])
        report['target_exit']=target.exit();target.close()
        a,b,c,d=[report[n]for n in ('source_a','source_b','target_a','target_b')]
        report['differences']={p:[k for k in report[p]if report[p][k]!=report[q][k]]
                              for p,q in [('source_a','target_a'),('source_b','target_b')]}
        raw=(out/'source.bin').read_bytes();resumed=(out/'target.bin').read_bytes()
        ram=lambda s:sorted(s['observation']['ram_blocks'],key=lambda x:x['id'])
        report['checks']=dict(cpu_a=a['states']==c['states'],cpu_b=b['states']==d['states'],
            events_a=a['observation']['events']==c['observation']['events'],
            events_b=b['observation']['events']==d['observation']['events'],
            full_ram_a=ram(a)==ram(c),full_ram_b=ram(b)==ram(d),
            pc_ram_4g=any(x['id']=='pc.ram'and x['bytes']==4*1024**3 for x in ram(a)),
            ram_actually_changed=ram(a)!=ram(b),small_ram_a=a['guest_memory']==c['guest_memory'],
            small_ram_b=b['guest_memory']==d['guest_memory'],
            guest_marker=bytes.fromhex(b['guest_memory'])[256:260]==bytes.fromhex('01adc0de'),
            natural_output=raw[report['prefix_bytes']:]==resumed and raw.endswith(b'R1E'),
            clean_exits=report['source_exit']==report['target_exit']==33,
            no_stderr=not(out/'source.stderr').read_bytes()and not(out/'target.stderr').read_bytes())
        if args.point=='rf_return':report['checks']['actual_rf_set']=bool(int(a['states'][0]['eflags'],16)&0x10000)
    except Exception as exc:report['errors'].append(str(exc))
    finally:
        done.set()
        for vm in vms:
            report[vm.role+'_command']=vm.command;report[vm.role+'_qmp']=vm.qmp.receipts if vm.qmp else []
            vm.close()
        report['all_processes_exited']=all(v.proc.poll()is not None for v in vms)
        report['seconds']=time.monotonic()-started
        report['bounded_case_passed']=bool(report.get('checks'))and all(report['checks'].values())and not report['errors']and report['all_processes_exited']
        report['files']=[identity(p)for p in out.iterdir()if p.is_file()]
        (out/'report.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:report.get(k)for k in ('bounded_case_passed','seconds','errors','checks','differences')},indent=2))
    return report['bounded_case_passed']


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('binary','firmware','output'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--point',choices=['before_call','before_iret','rf_return'],required=True)
    raise SystemExit(not run(p.parse_args()))
