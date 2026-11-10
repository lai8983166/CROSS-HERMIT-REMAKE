"""Owned CPU-only WHP CALL/RET gate. No Windows boot, game or host input.

Two VPs; reserve a 4-GiB address envelope, commit/map only 64 KiB. All synthetic
register writes precede execution. Subsequent observation changes only GPA execute
permissions. This is not canonical57 or original-game acceptance.
"""
import ctypes as C
import hashlib
import json
from pathlib import Path
import struct
import threading
import time
from devtools.isolated_windows_vm import WORKER,identity

NAMES=list(range(0x28))+[0x2001]+list(range(0x1000,0x1008))+list(range(0x1010,0x101a))+[0x80000000,0x80000001,0x80000002,0x80000004,0x80000006]


def need(value,message):
    if not value:raise ValueError(message)


def u32(n):return struct.pack('<I',n&0xffffffff)


def fixture():
    memory=bytearray(0x10000)
    # Preserve the per-VP data pointer in EDI across real guest CPUID.
    start=b''
    for leaf,offset_base in((7,0x240),(1,0x250)):
        start+=b'\xb8'+u32(leaf)+bytes.fromhex('31c90fa2')
        for mod,delta in((0x87,0),(0x9f,4),(0x8f,8),(0x97,12)):
            start+=bytes([0x89,mod])+u32(offset_base+delta)
    start+=bytes.fromhex('89fb')
    start+=b'\xe9'+u32(0x3076-(0x1000+len(start)+5))
    memory[0x1000:0x1000+len(start)]=start
    helper=bytes.fromhex('dbe3d9e8d9eed9ebddc1')
    for n in range(8):helper+=bytes.fromhex('f30f6f')+bytes([0x83+n*8])+u32(0x100+n*16)
    helper+=bytes.fromhex('0fae93')+u32(0x280) # ldmxcsr [ebx+280]
    last_fp=0x2000+len(helper);helper+=bytes.fromhex('dd03') # fld qword [ebx]
    helper+=bytes.fromhex('d9ab')+u32(0x284) # fldcw: unmask only divide by zero
    last_fp=0x2000+len(helper);helper+=bytes.fromhex('dcb3')+u32(8) # pending unmasked FDIV by zero; no FWAIT/FNSTENV
    helper+=bytes.fromhex('0fae83')+u32(0x400)+b'\xc3' # fxsave32, ret
    memory[0x2000:0x2000+len(helper)]=helper
    caller=b'\xe8'+u32(0x2000-0x307b)
    after=bytes.fromhex('ff83')+u32(0x200)
    after+=b'\xe9'+u32(0x5000-(0x307b+len(after)+5))
    memory[0x3076:0x3076+len(caller+after)]=caller+after
    memory[0x5000]=0xf4
    for vp in(0,1):
        data=0x8000+vp*0x1000
        memory[data:data+8]=struct.pack('<d',2.25+vp)
        memory[data+0x100:data+0x180]=bytes((7+vp*19+n*3)&255 for n in range(128))
        memory[data+0x280:data+0x284]=u32(0x3f80)
        memory[data+0x284:data+0x286]=bytes.fromhex('7b03')
    from capstone import Cs,CS_ARCH_X86,CS_MODE_32
    dis=Cs(CS_ARCH_X86,CS_MODE_32)
    listing=[]
    for addr,code in((0x1000,start),(0x2000,helper),(0x3076,caller+after)):
        instructions=list(dis.disasm(code,addr))
        need(sum(i.size for i in instructions)==len(code),'complete fixture decode')
        listing.extend(dict(address=i.address,hex=i.bytes.hex(),instruction=i.mnemonic+' '+i.op_str)for i in instructions)
    need(list(dis.disasm(helper,0x2000))[-1].mnemonic=='ret','natural helper return')
    return bytes(memory),dict(last_fp=last_fp,return_pc=0x307b,helper=0x2000,next_pc=0x5000,instructions=listing)


class Api:
    def __init__(self):
        self.dll=C.WinDLL('C:/Windows/System32/WinHvPlatform.dll')
        h=C.c_void_p;u=C.c_uint32;q=C.c_uint64;p=C.c_void_p
        specs={'WHvCreatePartition':[C.POINTER(h)],'WHvSetupPartition':[h],'WHvDeletePartition':[h],
               'WHvSetPartitionProperty':[h,u,p,u],'WHvCreateVirtualProcessor':[h,u,u],
               'WHvDeleteVirtualProcessor':[h,u],'WHvMapGpaRange':[h,p,q,q,u],
               'WHvUnmapGpaRange':[h,q,q],'WHvRunVirtualProcessor':[h,u,p,u],
               'WHvCancelRunVirtualProcessor':[h,u,u],
               'WHvGetVirtualProcessorRegisters':[h,u,p,u,p],
               'WHvSetVirtualProcessorRegisters':[h,u,p,u,p]}
        for name,args in specs.items():
            f=getattr(self.dll,name);f.argtypes=args;f.restype=C.c_long
        self.state_name='WHvGetVirtualProcessorState' if hasattr(self.dll,'WHvGetVirtualProcessorState') else 'WHvGetVirtualProcessorXsaveState'
        f=getattr(self.dll,self.state_name);f.restype=C.c_long
        f.argtypes=[h,u,u,p,u,C.POINTER(u)] if self.state_name.endswith('ProcessorState')else[h,u,p,u,C.POINTER(u)]

    def call(self,name,*args):
        hr=getattr(self.dll,name)(*args)
        if hr:raise OSError('%s HRESULT=%08x'%(name,hr&0xffffffff))


def scalar(value):return value.to_bytes(8,'little')+bytes(8)
def segment(selector,attr,base=0,limit=0xffffffff):return struct.pack('<QIHH',base,limit,selector,attr)


def run(directory):
    d=Path(directory).resolve();need(d.parent==WORKER and d.name=='whp-return-v2-20261110','owned fresh directory')
    d.mkdir(exist_ok=False);started=time.monotonic()
    r=dict(accepted=False,fullstate=False,fullABI=False,original_game_starts=0,windows_boots=0,host_input_actions=0,errors=[],cleanup=[],phases=[],vp_count=2,reserved_address_bytes=2**32,committed_mapped_bytes=0x10000)
    api=Api();handle=C.c_void_p();base=None;created=[];mapped=False;threads=[]
    k=C.WinDLL('kernel32',use_last_error=True)
    k.VirtualAlloc.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong,C.c_ulong];k.VirtualAlloc.restype=C.c_void_p
    k.VirtualFree.argtypes=[C.c_void_p,C.c_size_t,C.c_ulong];k.VirtualFree.restype=C.c_int
    def save(name,raw):
        p=d/name;p.write_bytes(raw);return identity(p)
    def progress():
        (d/'progress.json').write_text(json.dumps(r,indent=2))
    def setregs(vp,values):
        names=(C.c_uint32*len(values))(*values);raw=b''.join(values.values());b=C.create_string_buffer(raw)
        api.call('WHvSetVirtualProcessorRegisters',handle,vp,names,len(values),b)
    def regs(vp):
        names=(C.c_uint32*len(NAMES))(*NAMES);b=C.create_string_buffer(bytes([0xa5])*(16*len(NAMES)))
        api.call('WHvGetVirtualProcessorRegisters',handle,vp,names,len(NAMES),b)
        return {str(n):b.raw[i*16:i*16+16].hex()for i,n in enumerate(NAMES)}
    def val(reg,n):return int.from_bytes(bytes.fromhex(reg[str(n)])[:8],'little')
    def mapping(gpa,size,flags):api.call('WHvMapGpaRange',handle,base+gpa,gpa,size,flags)
    def xsave(vp,name):
        b=C.create_string_buffer(bytes([0xa5])*16384);got=C.c_uint32()
        args=[handle,vp]
        if api.state_name.endswith('ProcessorState'):args.append(0x1001)
        hr=getattr(api.dll,api.state_name)(*args,b,16384,C.byref(got))
        row=dict(api=api.state_name,hresult=hex(hr&0xffffffff),written=got.value)
        need(hr==0 and 576<=got.value<=16384,'actual bounded XSAVE state')
        row['file']=save(name,b.raw[:got.value]);return row
    def phase(name,target):
        nonlocal threads
        results=[None,None]
        def execute(vp):
            b=C.create_string_buffer(224)
            hr=api.dll.WHvRunVirtualProcessor(handle,vp,b,224)
            results[vp]=dict(hresult=hex(hr&0xffffffff),raw=b.raw.hex(),reason=struct.unpack_from('<I',b.raw)[0],rip=struct.unpack_from('<Q',b.raw,32)[0],access_info=struct.unpack_from('<I',b.raw,68)[0],gpa=struct.unpack_from('<Q',b.raw,72)[0],gva=struct.unpack_from('<Q',b.raw,80)[0])
        threads=[threading.Thread(target=execute,args=(vp,),daemon=True)for vp in(0,1)]
        for t in threads:t.start()
        until=time.monotonic()+2
        for t in threads:t.join(max(0,until-time.monotonic()))
        if any(t.is_alive()for t in threads):
            for vp in(0,1):api.call('WHvCancelRunVirtualProcessor',handle,vp,0)
            for t in threads:t.join(1)
        row=dict(name=name,all_run_threads_joined=all(not t.is_alive()for t in threads),exits=results,seconds=time.monotonic()-started)
        r['phases'].append(row);progress();need(row['all_run_threads_joined'],'both VP run calls returned')
        for a in results:
            need(a and a['hresult']=='0x0' and a['reason']==1 and a['rip']==target and a['gpa']==target,'exact GPA execute exit at target')
            need(a['access_info']&3==2,'execute access violation')
            if a['access_info']&8:need(a['gva']==target,'reported valid GVA')
        row['registers']=[regs(vp)for vp in(0,1)]
        row['xsave']=[xsave(vp,name+'-vp%d.xsave'%vp)for vp in(0,1)]
        row['memory']=save(name+'.memory.bin',C.string_at(base,0x10000))
        again=[regs(vp)for vp in(0,1)]
        need(again==row['registers'],'unchanged all-stopped raw register reread')
        need(C.string_at(base,0x10000)==Path(row['memory']['path']).read_bytes(),'unchanged all-stopped memory reread')
        row['xsave_reread']=[xsave(vp,name+'-vp%d-reread.xsave'%vp)for vp in(0,1)]
        need(all(a['file']['sha256']==b['file']['sha256']for a,b in zip(row['xsave'],row['xsave_reread'])),'unchanged all-stopped raw XSAVE reread')
        row['stable_registers_memory_xsave']=True;progress();return row
    try:
        memory,manifest=fixture();r['fixture']=manifest;r['initial_memory']=save('initial.memory.bin',memory)
        api.call('WHvCreatePartition',C.byref(handle));r['partition_created']=True
        count=C.c_uint32(2);api.call('WHvSetPartitionProperty',handle,0x1fff,C.byref(count),4)
        api.call('WHvSetupPartition',handle)
        base=k.VirtualAlloc(None,2**32,0x2000,1);need(base,'4-GiB reservation')
        need(k.VirtualAlloc(base,0x10000,0x1000,4)==base,'64-KiB committed backing')
        C.memmove(base,memory,len(memory));mapping(0,0x10000,3);mapped=True
        mapping(0x1000,0x1000,5);mapping(0x3000,0x1000,5);mapping(0x2000,0x1000,1);mapping(0x5000,0x1000,1)
        for vp in(0,1):
            api.call('WHvCreateVirtualProcessor',handle,vp,0);created.append(vp)
            values={n:scalar(0)for n in range(16)}
            values.update({4:scalar(0xaf00+vp*0x1000),7:scalar(0x8000+vp*0x1000),0x10:scalar(0x1000),0x11:scalar(2),0x1c:scalar(0x33),0x1d:scalar(0),0x1e:scalar(0),0x1f:scalar(0x600),0x20:scalar(0),0x2001:scalar(0),0x25:scalar(0xffff0ff0),0x26:scalar(0x400)})
            for n in(0x12,0x14,0x15,0x16,0x17):values[n]=segment(0x10,0xc093)
            values[0x13]=segment(8,0xc09b);values[0x18]=segment(0,0x82,0x6000,0xff);values[0x19]=segment(0x28,0x8b,0x7000,0x67)
            values[0x1a]=struct.pack('<HHHHQ',0,0,0,0x7ff,0x6800);values[0x1b]=struct.pack('<HHHHQ',0,0,0,0x3f,0x6000)
            for n in range(0x21,0x25):values[n]=scalar(0x12340000+n+vp*0x100)
            setregs(vp,values)
        r['registers_initialized']=[regs(vp)for vp in(0,1)];progress()
        first=phase('callee-entry',0x2000)
        for vp in(0,1):
            sp=val(first['registers'][vp],4)
            need(sp==0xaefc+vp*0x1000 and C.string_at(base+sp,4)==u32(0x307b),'natural CALL return stack')
        mapping(0x3000,0x1000,1);mapping(0x2000,0x1000,5)
        returned=phase('natural-return',0x307b)
        for vp in(0,1):
            reg=returned['registers'][vp];data=0x8000+vp*0x1000
            need(val(reg,4)==0xaf00+vp*0x1000,'RET restored original SP')
            need(C.string_at(base+data+0x200,4)==bytes(4),'consumer has not executed')
            for n in list(range(0x21,0x27))+[0x80000000,0x80000001,0x80000002,0x80000004,0x80000006]:
                need(reg[str(n)]==r['registers_initialized'][vp][str(n)],'observer preserved DR/pending state')
        mapping(0x3000,0x1000,5)
        consumed=phase('after-consumer',0x5000)
        for vp in(0,1):need(C.string_at(base+0x8000+vp*0x1000+0x200,4)==u32(1),'natural consumer exactly once')
        need(C.string_at(base+0x1000,0x3000)==memory[0x1000:0x4000],'unchanged guest code bytes')
        for vp in(0,1):
            for n in list(range(0x1000,0x1008))+list(range(0x1010,0x101a)):
                need(returned['registers'][vp][str(n)]==consumed['registers'][vp][str(n)],'FP/XMM unchanged through integer-only consumer')
        r['full_rflags_transparency']=False
        r['rf_saved_as_one_at_execute_exit']=True
        r['natural_return_execute_gate_passed']=True
        r['register_write_calls_after_first_run']=0;r['injected_guest_events']=0
    except Exception as exc:r['errors'].append(repr(exc))
    finally:
        live=any(t.is_alive()for t in threads)
        r['all_runs_joined_at_cleanup']=not live
        if not live:
            for vp in reversed(created):
                try:api.call('WHvDeleteVirtualProcessor',handle,vp);r['cleanup'].append('deleted VP '+str(vp))
                except Exception as e:r['errors'].append('cleanup: '+repr(e))
            if mapped:
                try:api.call('WHvUnmapGpaRange',handle,0,0x10000);r['cleanup'].append('unmapped 64 KiB')
                except Exception as e:r['errors'].append('cleanup: '+repr(e))
            if handle.value:
                try:api.call('WHvDeletePartition',handle);r['cleanup'].append('deleted partition')
                except Exception as e:r['errors'].append('cleanup: '+repr(e))
            if base:
                if k.VirtualFree(base,0,0x8000):r['cleanup'].append('released 4 GiB reservation')
                else:r['errors'].append('VirtualFree failed')
        r['elapsed_seconds']=time.monotonic()-started;r['implementation']=identity(Path(__file__))
        (d/'report.json').write_text(json.dumps(r,indent=2))
    return r
