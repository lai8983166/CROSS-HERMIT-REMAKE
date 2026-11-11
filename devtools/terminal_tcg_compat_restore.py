"""Bounded compatibility32 -> long64 consumption after complete RAM restore."""
import argparse,hashlib,json,os,signal,struct,threading,time
from pathlib import Path
from devtools.terminal_tcg_longmode_image import image as long_image
from devtools.terminal_tcg_ram_event_probe_v3 import VM
from devtools.terminal_tcg_roundtrip_probe import identity


def image(root):
    raw,p=long_image(root);elf=bytearray(raw)
    w=lambda n:struct.pack('<I',n)
    def put(off,data):elf[4096+off:4096+off+len(data)]=data
    # Separate the high alias physically: high virtual 0x100100000 -> 0x300000.
    # The guest itself creates its mapping and copies its executable page.
    put(0x300,b'\xe9'+struct.pack('<i',0xa00-0x305))
    setup=bytes.fromhex('c70425')+w(0x102020)+w(0x104003)
    setup+=bytes.fromhex('c70425')+w(0x104000)+w(0x200083)
    setup+=bytes.fromhex('fcbe00001000bf00003000b900040000f3a5')
    setup+=bytes.fromhex('48b8')+struct.pack('<Q',0x100100320)+bytes.fromhex('ffe0')
    put(0xa00,setup)
    high=0x13579bdf2468ace0;low=0xfedcba9876543210;r8=0x123456789abcdef0
    offset=p['stop']-0x100000000-0x100000
    code=bytes.fromhex('48b8')+struct.pack('<Q',high)+bytes.fromhex('48890425')+w(0x300980)
    code+=bytes.fromhex('48b8')+struct.pack('<Q',low)+bytes.fromhex('48890425')+w(0x100980)
    code+=bytes.fromhex('49b8')+struct.pack('<Q',r8)+bytes.fromhex('6a08680006100048cb')
    put(offset,code)
    put(0x600,bytes.fromhex('90ea000710001800'))
    consumer=bytes.fromhex('4c890425')+w(0x109000)
    consumer+=bytes.fromhex('64488b0425')+w(0x100980)+bytes.fromhex('48890425')+w(0x109008)
    consumer+=bytes.fromhex('f3440f7f3c25')+w(0x109010)
    consumer+=bytes.fromhex('b9000100c00f3248c1e2204809d048890425')+w(0x109020)
    consumer+=bytes.fromhex('480fae0425')+w(0x109100)
    if len(consumer)>0x80:raise ValueError('consumer overlap')
    put(0x700,consumer+b'\x90'*(0x80-len(consumer)))
    tail=b''
    for address,size in ((0x109000,40),(0x109100,512)):
        tail+=b'\xbe'+w(address)+b'\xb9'+w(size)+bytes.fromhex('ace6e9e2fb')
    tail+=bytes.fromhex('b810000000e7f4f4ebfd')
    put(0x780,tail)
    if len(elf)!=len(raw)or 0x780+len(tail)>0x800:raise ValueError('ELF overlap/extent')
    return bytes(elf),dict(a=0x100600,b=0x100780,r8=r8,high_value=high,low_decoy=low,
        fip=p['fip'],fdp=p['fdp'],fs_base=0x100000000,xmm15=p['xmm_patterns']['15'])


def run(a):
    out=a.output.resolve()
    if not str(out).startswith('/mnt/f/'):raise ValueError('F-backed output required')
    out.mkdir(exist_ok=False);elf,e=image(Path(__file__).resolve().parents[1]);(out/'guest.elf').write_bytes(elf)
    stream=out/'checkpoint.bin';vms=[];done=threading.Event();start=time.monotonic()
    r=dict(accepted=False,windows_admitted=False,errors=[],expected=e,binary=identity(a.binary),short=a.short)
    def watch():
        while not done.wait(.1):
            if time.monotonic()-start>(15 if a.short else 120)or(stream.exists()and stream.stat().st_size>64*1024**2):
                r['errors'].append('time/64 MiB budget')
                for vm in vms:
                    if vm.proc.poll()is None:os.killpg(vm.proc.pid,signal.SIGKILL)
                return
    def sample(vm,pc):
        if a.short:
            s=[json.loads(vm.call('x-query-tcg-state',{'cpu-index':i})['state'])for i in range(2)]
            if int(s[0]['eip'],16)!=pc:raise ValueError('wrong PC')
            return dict(states=s)
        return vm.sample(pc)
    threading.Thread(target=watch,daemon=True).start()
    try:
        source=VM(a,out,'source',e);vms.append(source);source.bp('Z',e['a']);source.stop()
        r['source_a']=sample(source,e['a']);source.bp('z',e['a'])
        if not a.short:
            source.call('migrate-set-parameters',{'max-bandwidth':1073741824})
            source.call('migrate',{'uri':'file:'+str(stream)});r['outgoing']=source.migration_done();r['checkpoint']=identity(stream)
        source.bp('Z',e['b']);source.stop();r['source_b']=sample(source,e['b']);r['source_exit']=source.exit();source.close()
        output=(out/'source.bin').read_bytes();r['output_hex']=output.hex()
        s=r['source_a']['states'][0]
        r['checks']=dict(compat_lma=bool(int(s['efer'],16)&0x400),
            compat_cs=int(s['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'][1][0],16)==8,
            high_fs=int(s['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'][4][1],16)==e['fs_base'],
            real_r8=int(s['gpr'][8],16)==e['r8'],
            consumer_r8=len(output)==552 and int.from_bytes(output[:8],'little')==e['r8'],
            consumer_high_mapping=len(output)==552 and int.from_bytes(output[8:16],'little')==e['high_value']!=e['low_decoy'],
            consumer_xmm15=output[16:32].hex()==e['xmm15'],
            consumer_fs_base=int.from_bytes(output[32:40],'little')==e['fs_base'],
            consumer_fip=int.from_bytes(output[48:56],'little')==e['fip'],
            consumer_fdp=int.from_bytes(output[56:64],'little')==e['fdp'],source_exit=r['source_exit']==33)
        if not all(r['checks'].values()):raise ValueError('guest consumer mismatch')
        if not a.short:
            target=VM(a,out,'target',e,incoming=True);vms.append(target)
            target.call('migrate-incoming',{'uri':'file:'+str(stream)});r['incoming']=target.migration_done()
            if target.call('query-status')['running']:raise ValueError('premature run')
            r['target_a']=sample(target,e['a']);target.bp('Z',e['b']);target.stop()
            r['target_b']=sample(target,e['b']);r['target_exit']=target.exit();target.close()
            r['checks'].update(full_a=r['source_a']==r['target_a'],full_b=r['source_b']==r['target_b'],
                target_output=(out/'target.bin').read_bytes()==output,target_exit=r['target_exit']==33,
                ram_changed=r['source_a']['observation']['ram_blocks']!=r['source_b']['observation']['ram_blocks'])
    except Exception as error:r['errors'].append(str(error))
    finally:
        done.set()
        for vm in vms:r[vm.role+'_qmp']=vm.qmp.receipts;r[vm.role+'_command']=vm.command;vm.close()
        r['all_processes_exited']=all(vm.proc.poll()is not None for vm in vms)
        r['seconds']=time.monotonic()-start;r['bounded_case_passed']=bool(r.get('checks'))and all(r['checks'].values())and not r['errors']and r['all_processes_exited']
        r['files']=[identity(p)for p in out.iterdir()if p.is_file()]
        (out/'report.json').write_text(json.dumps(r,indent=2))
    print(json.dumps({k:r.get(k)for k in ('bounded_case_passed','seconds','checks','errors')},indent=2));return r['bounded_case_passed']
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ('binary','firmware','output'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--short',action='store_true');raise SystemExit(not run(p.parse_args()))
