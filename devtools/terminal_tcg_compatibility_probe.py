"""Observe an actual long-to-compatibility transition without Windows or inputs."""
import argparse,json,os,signal,struct,threading,time
from pathlib import Path
from devtools.terminal_tcg_longmode_image import image as long_image
from devtools.terminal_tcg_ram_event_probe_v3 import VM
from devtools.terminal_tcg_roundtrip_probe import identity
from devtools.terminal_tcg_canonical57 import from_tcg,Canonical57Error


def image(root):
    raw,prior=long_image(root);elf=bytearray(raw)
    offset=4096+prior['stop']-0x100000000-0x100000
    # Preserve high x87 pointers, FS base and XMM15 from actual long-mode code.
    # Set a real nonzero extended register, then execute a far return to CS=8.
    code=bytes.fromhex('49b8')+struct.pack('<Q',0x123456789abcdef0)
    code+=bytes.fromhex('6a08680006100048cb')
    elf[offset:offset+len(code)]=code
    elf[4096+0x600:4096+0x60e]=bytes.fromhex('90b043e6e9b810000000e7f4f4ebfd')
    return bytes(elf),dict(a=0x100600,b=0x100600,prior=prior)


def run(a):
    out=a.output.resolve();out.mkdir(exist_ok=False)
    elf,e=image(Path(__file__).resolve().parents[1]);(out/'guest.elf').write_bytes(elf)
    r=dict(accepted=False,windows_admitted=False,errors=[],binary=identity(a.binary));vm=None;done=threading.Event();start=time.monotonic()
    def watch():
        if not done.wait(15):
            r['errors'].append('15 second deadline')
            if vm and vm.proc.poll()is None:os.killpg(vm.proc.pid,signal.SIGKILL)
    threading.Thread(target=watch,daemon=True).start()
    try:
        vm=VM(a,out,'source',e);vm.bp('Z',e['a']);vm.stop()
        s=json.loads(vm.call('x-query-tcg-state',{'cpu-index':0})['state']);r['state']=s
        cs=s['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'][1]
        try:
            from_tcg(s,expected_cpu=0,expected_vcpus=2);r['adapter_rejected']=False
        except Canonical57Error as error:r['adapter_rejected']=True;r['adapter_reason']=str(error)
        r['exit_code']=vm.exit()
        r['checks']=dict(actual_eip=int(s['eip'],16)==e['a'],lma=bool(int(s['efer'],16)&0x400),
            cs32=int(cs[0],16)==8 and bool(int(cs[3],16)&0x400000)and not int(cs[3],16)&0x200000,
            real_extended_gpr=int(s['gpr'][8],16)==0x123456789abcdef0,
            preserved_high_fip=int(s['fip'],16)==e['prior']['fip'],
            preserved_high_fdp=int(s['fdp'],16)==e['prior']['fdp'],
            preserved_high_fs=int(s['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'][4][1],16)==0x100000000,
            natural_exit=r['exit_code']==33,output=(out/'source.bin').read_bytes()==b'C',strict_adapter_refusal=r['adapter_rejected'])
    except Exception as error:r['errors'].append(str(error))
    finally:
        done.set()
        if vm:r['qmp']=vm.qmp.receipts;r['command']=vm.command;vm.close()
        r['seconds']=time.monotonic()-start;r['bounded_mode_observation_passed']=bool(r.get('checks'))and all(r['checks'].values())and not r['errors']
        r['files']=[identity(p)for p in out.iterdir()if p.is_file()]
        (out/'report.json').write_text(json.dumps(r,indent=2))
    print(json.dumps({k:r.get(k)for k in ('bounded_mode_observation_passed','adapter_reason','checks','errors','seconds')},indent=2))
    return r['bounded_mode_observation_passed']
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('binary','firmware','output'):p.add_argument('--'+name,type=Path,required=True)
    raise SystemExit(not run(p.parse_args()))
