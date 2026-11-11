"""Short actual #DB -> handler -> IRETD -> RF=1 observer -> consumption test."""
import argparse,json,os,signal,threading,time
from pathlib import Path
from devtools.terminal_tcg_ram_event_probe_v2 import VM,image
from devtools.terminal_tcg_roundtrip_probe import identity


def run(a):
    out=a.output.resolve();out.mkdir(exist_ok=False)
    elf,expected=image(Path(__file__).resolve().parents[1],'rf_return');(out/'guest.elf').write_bytes(elf)
    r=dict(accepted=False,windows_admitted=False,binary=identity(a.binary),errors=[]);vm=None;done=threading.Event();start=time.monotonic()
    def watch():
        if not done.wait(15):
            r['errors'].append('15 second deadline')
            if vm and vm.proc.poll()is None:os.killpg(vm.proc.pid,signal.SIGKILL)
    threading.Thread(target=watch,daemon=True).start()
    try:
        vm=VM(a,out,'source',expected)
        vm.bp('Z',0x100433);vm.stop()
        r['at_iret']=json.loads(vm.call('x-query-tcg-state',{'cpu-index':0})['state'])
        esp=int(r['at_iret']['gpr'][4],16)
        r['iret_frame']=vm.rsp.command(f'm{esp:x},c')
        vm.bp('z',0x100433);vm.bp('Z',expected['a']);vm.stop()
        r['at_rf']=json.loads(vm.call('x-query-tcg-state',{'cpu-index':0})['state'])
        r['db_count_at_rf']=int.from_bytes(bytes.fromhex(vm.rsp.command('m102000,4')),'little')
        vm.bp('z',expected['a']);vm.bp('Z',expected['b']);vm.stop()
        r['at_b']=json.loads(vm.call('x-query-tcg-state',{'cpu-index':0})['state'])
        r['db_count_at_b']=int.from_bytes(bytes.fromhex(vm.rsp.command('m102000,4')),'little')
        r['exit_code']=vm.exit()
        r['checks']=dict(iret_pc=int(r['at_iret']['eip'],16)==0x100433,
            actual_frame_rf=bool(int.from_bytes(bytes.fromhex(r['iret_frame'])[8:12],'little')&0x10000),
            rf_pc=int(r['at_rf']['eip'],16)==0x100305,
            rf_preserved=bool(int(r['at_rf']['eflags'],16)&0x10000),
            no_extra_db=r['db_count_at_rf']==r['db_count_at_b']==1,
            consumed=(out/'source.bin').read_bytes().endswith(b'R1E'),
            natural_exit=r['exit_code']==33,stderr_empty=not(out/'source.stderr').read_bytes())
    except Exception as e:r['errors'].append(str(e))
    finally:
        done.set()
        if vm:r['qmp']=vm.qmp.receipts;r['command']=vm.command;vm.close()
        r['seconds']=time.monotonic()-start;r['bounded_case_passed']=bool(r.get('checks'))and all(r['checks'].values())and not r['errors']
        r['files']=[identity(p)for p in out.iterdir()if p.is_file()]
        (out/'report.json').write_text(json.dumps(r,indent=2))
    print(json.dumps({k:r.get(k)for k in ('bounded_case_passed','checks','errors','seconds')},indent=2))
    return r['bounded_case_passed']
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('binary','firmware','output'):p.add_argument('--'+name,type=Path,required=True)
    raise SystemExit(not run(p.parse_args()))
