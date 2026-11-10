"""CPU-only RF/debug behavior contrasts; no Windows, game, UI or disk device.

Frozen return-v2 supplies the FP fixture and WHP ABI. This experiment adds an
actual guest IDT #DB handler and enabled execution breakpoint. Only the explicit
unsafe-negative arms write RFLAGS after execution; raw reports retain it.
"""
import ctypes as C
import json
from pathlib import Path
import struct
import threading
import time
from devtools.isolated_windows_vm import WORKER,identity
from devtools.terminal_whp_return_probe_v2 import Api,NAMES,fixture as parent_fixture,need,scalar,segment,u32

CASES={'ret-baseline':('ret',False,False),'ret-ept-raw':('ret',True,False),
       'ret-ept-unsafe-clear':('ret',True,True),'iret-baseline':('iret',False,False),
       'iret-ept-preserve':('iret',True,False),'iret-ept-unsafe-clear':('iret',True,True)}


def fixture(kind):
    raw,parent=parent_fixture();m=bytearray(raw)
    ret=next(x['address'] for x in parent['instructions'] if x['instruction']=='ret ')
    # Actual GDT and IDT for guest-owned #DB delivery and IRET; flat protected mode.
    m[0x6008:0x6018]=bytes.fromhex('ffff0000009bcf00ffff00000093cf00')
    m[0x6808:0x6810]=struct.pack('<HHBBH',0x4000,8,0,0x8e,0)
    # pushad; save DR6/EIP/stacked flags; set RF in the ORIGINAL #DB frame; popad;iret.
    handler=bytes.fromhex('60ff83040200000f21f08983080200008b44242089830c0200008b442428898310020000814c24280000010061cf')
    m[0x4000:0x4000+len(handler)]=handler
    if kind=='iret':
        # pop original near-return target; form a real same-CPL IRETD frame with RF=1.
        tail=bytes.fromhex('589c810c24000001000e50cf');m[ret:ret+len(tail)]=tail
    else:tail=b'\xc3'
    from capstone import Cs,CS_ARCH_X86,CS_MODE_32
    decoder=Cs(CS_ARCH_X86,CS_MODE_32)
    listing=[]
    for addr,code in ((ret,tail),(0x4000,handler)):
        instructions=list(decoder.disasm(code,addr));need(sum(i.size for i in instructions)==len(code),'complete fixture decode')
        listing.extend(dict(address=i.address,hex=i.bytes.hex(),instruction=i.mnemonic+' '+i.op_str)for i in instructions)
    return bytes(m),dict(kind=kind,parent=parent,tail_start=ret,handler=0x4000,return_pc=0x307b,listing=listing)


def run(case):
    kind,ept,clear=CASES[case];d=WORKER/('whp-rf-v3-20261110-'+case);d.mkdir(exist_ok=False)
    started=time.monotonic();api=Api();h=C.c_void_p();base=None;created=[];mapped=False;threads=[]
    r=dict(case=case,accepted=False,fullstate=False,fullABI=False,original_game_starts=0,windows_boots=0,
           host_input_actions=0,vp_count=2,reserved_address_bytes=2**32,committed_mapped_bytes=65536,
           errors=[],cleanup=[],phases=[],host_register_writes_after_start=[],injected_events=0)
    k=C.WinDLL('kernel32',use_last_error=True)
    k.VirtualAlloc.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.c_ulong];k.VirtualAlloc.restype=C.c_void_p
    k.VirtualFree.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong];k.VirtualFree.restype=C.c_int
    def save(name,b):
        p=d/name;p.write_bytes(b);return identity(p)
    def regs(vp):
        ns=(C.c_uint32*len(NAMES))(*NAMES);b=C.create_string_buffer(bytes([0xa5])*(16*len(NAMES)))
        api.call('WHvGetVirtualProcessorRegisters',h,vp,ns,len(NAMES),b)
        return {str(n):b.raw[16*i:16*i+16].hex()for i,n in enumerate(NAMES)}
    def val(reg,n):return int.from_bytes(bytes.fromhex(reg[str(n)])[:8],'little')
    def setregs(vp,values):
        ns=(C.c_uint32*len(values))(*values);b=C.create_string_buffer(b''.join(values.values()))
        api.call('WHvSetVirtualProcessorRegisters',h,vp,ns,len(values),b)
    def mapping(gpa,size,flags):api.call('WHvMapGpaRange',h,base+gpa,gpa,size,flags)
    def phase(name):
        nonlocal threads
        results=[None,None]
        def execute(vp):
            b=C.create_string_buffer(224);hr=api.dll.WHvRunVirtualProcessor(h,vp,b,224)
            results[vp]=dict(hresult=hex(hr&0xffffffff),raw=b.raw.hex(),reason=struct.unpack_from('<I',b.raw)[0],
                            rip=struct.unpack_from('<Q',b.raw,32)[0],rflags=struct.unpack_from('<Q',b.raw,40)[0],
                            access_info=struct.unpack_from('<I',b.raw,68)[0],gpa=struct.unpack_from('<Q',b.raw,72)[0])
        threads=[threading.Thread(target=execute,args=(vp,),daemon=True)for vp in (0,1)]
        for t in threads:t.start()
        deadline=time.monotonic()+2
        for t in threads:t.join(max(0,deadline-time.monotonic()))
        if any(t.is_alive()for t in threads):
            for vp in (0,1):api.call('WHvCancelRunVirtualProcessor',h,vp,0)
            for t in threads:t.join(1)
        row=dict(name=name,all_run_threads_joined=all(not t.is_alive()for t in threads),exits=results)
        r['phases'].append(row);need(row['all_run_threads_joined'],'joined before stable capture')
        row['registers']=[regs(vp)for vp in (0,1)];row['memory']=save(name+'.memory.bin',C.string_at(base,65536))
        row['xsave']=[]
        for vp in (0,1):
            b=C.create_string_buffer(16384);got=C.c_uint32();args=[h,vp]
            if api.state_name.endswith('ProcessorState'):args.append(0x1001)
            hr=getattr(api.dll,api.state_name)(*args,b,16384,C.byref(got));need(hr==0 and 576<=got.value<=16384,'bounded XSAVE')
            row['xsave'].append(save(name+'-vp%d.xsave'%vp,b.raw[:got.value]))
        need(row['registers']==[regs(vp)for vp in (0,1)],'stable register reread')
        need(Path(row['memory']['path']).read_bytes()==C.string_at(base,65536),'stable memory reread')
        row['stable_reread']=True
        (d/'progress.json').write_text(json.dumps(r,indent=2));return row
    def at(row,reason,pc):
        need(all(x and x['hresult']=='0x0' and x['reason']==reason and x['rip']==pc for x in row['exits']),'expected boundary '+row['name'])
    try:
        memory,desc=fixture(kind);r['fixture']=desc;r['initial_memory']=save('initial.memory.bin',memory)
        api.call('WHvCreatePartition',C.byref(h));count=C.c_uint32(2)
        api.call('WHvSetPartitionProperty',h,0x1fff,C.byref(count),4);api.call('WHvSetupPartition',h)
        base=k.VirtualAlloc(None,2**32,0x2000,1);need(base,'4 GiB reservation')
        need(k.VirtualAlloc(base,65536,0x1000,4)==base,'64 KiB commit');C.memmove(base,memory,len(memory))
        mapping(0,65536,3);mapped=True
        for addr in (0x1000,0x3000,0x4000,0x5000):mapping(addr,4096,5)
        mapping(0x2000,4096,1)
        for vp in (0,1):
            api.call('WHvCreateVirtualProcessor',h,vp,0);created.append(vp)
            v={n:scalar(0)for n in range(16)}
            v.update({4:scalar(0xaf00+vp*0x1000),7:scalar(0x8000+vp*0x1000),0x10:scalar(0x1000),0x11:scalar(2),
                      0x1c:scalar(0x33),0x1d:scalar(0),0x1e:scalar(0),0x1f:scalar(0x600),0x20:scalar(0),0x2001:scalar(0),
                      0x21:scalar(0x307b),0x22:scalar(0x12340022),0x23:scalar(0x12340023),0x24:scalar(0x12340024),
                      0x25:scalar(0xffff0ff0),0x26:scalar(0x401)})
            for n in (0x12,0x14,0x15,0x16,0x17):v[n]=segment(0x10,0xc093)
            v[0x13]=segment(8,0xc09b);v[0x18]=segment(0,0x82,0x6000,0xff);v[0x19]=segment(0x28,0x8b,0x7000,0x67)
            v[0x1a]=struct.pack('<HHHHQ',0,0,0,0x7ff,0x6800);v[0x1b]=struct.pack('<HHHHQ',0,0,0,0x3f,0x6000)
            setregs(vp,v)
        r['initialized']=[regs(vp)for vp in (0,1)]
        entry=phase('callee-entry');at(entry,1,0x2000)
        for vp in (0,1):
            sp=val(entry['registers'][vp],4)
            need(sp==0xaefc+vp*0x1000 and C.string_at(base+sp,4)==u32(0x307b),'actual CALL stack')
        if ept:mapping(0x3000,4096,1)
        mapping(0x2000,4096,5)
        if ept:
            returned=phase('return-ept');at(returned,1,0x307b)
            for vp in (0,1):
                reg=returned['registers'][vp];need(val(reg,4)==0xaf00+vp*0x1000,'restored stack')
                need(C.string_at(base+0x8000+vp*0x1000+0x200,4)==bytes(4),'consumer not yet executed; #DB may precede EPT')
            if clear:
                # Explicitly unsafe diagnostic control: prior #DB/IRET can make RF=1 original.
                for vp in (0,1):
                    before=regs(vp);old=val(before,17);need(old&0x10000,'observed RF one')
                    setregs(vp,{17:scalar(old&~0x10000)});after=regs(vp)
                    need(all(before[n]==after[n]for n in before if n!='17'),'only RF changed')
                    need(val(after,17)==(old&~0x10000),'exact RF delta')
                    r['host_register_writes_after_start'].append(dict(vp=vp,register=17,before=before['17'],after=after['17'],
                        intent='unsafe-negative-control; no production RF restoration authorized'))
            mapping(0x3000,4096,5)
        final=phase('after-consumer-halt');at(final,8,0x5001) # WHP HLT exit reports the retired instruction's successor.
        need(C.string_at(base+0x1000,0x5000)==memory[0x1000:0x6000],'unchanged guest code')
        r['markers']=[]
        for vp in (0,1):
            b=C.string_at(base+0x8000+vp*0x1000+0x200,20)
            r['markers'].append(dict(zip(('consumer','debug_handler','handler_dr6','handler_eip','handler_stacked_flags'),struct.unpack('<IIIII',b))))
        r['experiment_completed']=True
    except Exception as e:r['errors'].append(repr(e))
    finally:
        live=any(t.is_alive()for t in threads);r['all_runs_joined_at_cleanup']=not live
        if not live:
            for vp in reversed(created):
                try:api.call('WHvDeleteVirtualProcessor',h,vp);r['cleanup'].append('deleted VP '+str(vp))
                except Exception as e:r['errors'].append('cleanup '+repr(e))
            if mapped:
                try:api.call('WHvUnmapGpaRange',h,0,65536);r['cleanup'].append('unmapped 64 KiB')
                except Exception as e:r['errors'].append('cleanup '+repr(e))
            if h.value:
                try:api.call('WHvDeletePartition',h);r['cleanup'].append('deleted partition')
                except Exception as e:r['errors'].append('cleanup '+repr(e))
            if base:
                if k.VirtualFree(base,0,0x8000):r['cleanup'].append('released 4 GiB reservation')
                else:r['errors'].append('VirtualFree failed')
        r['elapsed_seconds']=time.monotonic()-started;r['implementation']=identity(Path(__file__))
        r['parent_implementation']=identity(Path(__file__).with_name('terminal_whp_return_probe_v2.py'))
        (d/'report.json').write_text(json.dumps(r,indent=2))
    return r
