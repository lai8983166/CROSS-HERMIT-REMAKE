"""Execute the original main-context tail on one CPU per owned helper lifetime."""
import argparse
import json
import struct
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from tools.school_main_context import *
from tools.school_main_context_platform import MainPlatform
from tools.school_renderer_init_emulation import REGISTERS,buffer_evidence


def initial_cpu():
    return dict(EIP=ENTRY,ESP=SP,EBP=BP,EAX=0,ECX=0,EDX=0,EBX=0x55667788,
        ESI=0x88776655,EDI=BP,EFLAGS=2)


def initial_stack(fill):
    raw=bytearray(bytes([fill])*65536)
    store(raw,TOP-STACK,RETURN);store(raw,BP-STACK,0x11223344)
    raw[BP-0x9C-STACK:BP-STACK]=b'\xcc'*0x9C
    store(raw,BP-4-STACK,0)
    for at,value in ((BP-0xA0,0x55667788),(BP-0xA4,0x88776655),(BP-0xA8,0x44332211)):
        store(raw,at-STACK,value)
    # Declared HINSTANCE/previous-instance/command-line/show values are unconsumed.
    for i,value in enumerate((0x12340000,0,0,1)):store(raw,TOP+4+i*4-STACK,value)
    return bytes(raw)


class MainEmulator:
    def __init__(self,platform,fill):
        source_contract();self.platform,self.fill=platform,fill
        self.image=SOURCE.read_bytes();self.ranges=functions();self.uc=Uc(UC_ARCH_X86,UC_MODE_32)
        for at,n,b in ((BASE,(len(self.image)+4095)&~4095,self.image),(0,4096,bytes(4096)),
                (OWNER-4096,BACKING+8192,bytes([fill])*(BACKING+8192)),
                (STACK,65536,initial_stack(fill)),(RETURN,4096,bytes([fill])*4096)):
            self.uc.mem_map(at,n);self.uc.mem_write(at,b)
        self.uc.mem_write(OWNER,initial_owner(fill));self.foreign={};self.imports={}
        for slot,rule in IMPORTS.items():
            target=dword(self.image,slot-BASE);self.imports[target]=(slot,rule)
            page=target&~4095
            if page not in self.foreign:
                if any(a<=page<=b for a,b,p in self.uc.mem_regions()):raise ValueError('main import map overlap')
                self.uc.mem_map(page,4096);self.foreign[page]=bytearray(4096)
            self.foreign[page][target-page]=0xC3;self.uc.mem_write(target,b'\xc3')
        self.code={i.address:i for a,b in self.ranges.items() for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(self.image[a-BASE:b-BASE],a)}
        for k,v in initial_cpu().items():self.uc.reg_write(REGISTERS[k],v)
        self.allocations=[];self.all_calls=[];self.last_stack=initial_stack(fill)
        self.uc.hook_add(UC_HOOK_CODE,self._code);self.uc.hook_add(UC_HOOK_MEM_WRITE,self._write)

    def read(self,p):return struct.unpack('<I',bytes(self.uc.mem_read(p,4)))[0]
    def bytes(self,p,n):return bytes(self.uc.mem_read(p,n))
    def cpu(self):return {k:self.uc.reg_read(r) for k,r in REGISTERS.items()}

    def _write(self,uc,access,at,n,value,user):
        allowed=[(STACK,STACK+65536),(0,4)]
        if self.phase=='allocation':allowed.append((COUNTER,COUNTER+4))
        if self.phase=='constructor':allowed.append((OWNER,OWNER+SIZE))
        if self.phase=='publication':allowed.append((GLOBAL,GLOBAL+4))
        if not any(a<=at and at+n<=b for a,b in allowed):raise ValueError('main unowned original write '+hex(at))
        self.writes.append(dict(pc=uc.reg_read(REGISTERS['EIP']),pointer=at,bytes=n,value=value&((1<<(n*8))-1)))

    def _return(self,sp,eax,count):
        self.uc.reg_write(REGISTERS['EAX'],eax);self.uc.reg_write(REGISTERS['EIP'],self.read(sp))
        self.uc.reg_write(REGISTERS['ESP'],sp+4+count*4)

    def _allocate(self,sp):
        r=source_contract()['allocator'];args=[self.read(sp+4+i*4) for i in range(4)]
        if self.phase!='allocation' or self.allocations or self.read(sp)!=0x428A73 or args!=[SIZE,1,r['file'],r['line']]:raise ValueError('main exact declared CRT allocation')
        self.allocations.append(dict(va='0x56e810',return_va='0x428a73',sp=sp,args=args,pointer=OWNER,
            bytes=SIZE,initial_byte=0xCD,adapter='declared debug CRT allocation'))
        self._return(sp,OWNER,0)

    def _api(self,at,sp):
        slot,(name,desc,count,returns)=self.imports[at];ret=self.read(sp)
        if self.phase!='constructor' or ret not in returns:raise ValueError('main exact original API caller')
        args=[self.read(sp+4+i*4) for i in range(count)]
        offset=None
        if name=='InitializeCriticalSection':
            index=sum(c['name']==name for c in self.all_calls);expected=[OWNER+(0x14 if index==0 else 0x164)]
            pointer,n=args[0],24;request=dict(index=index,before_hex=self.bytes(pointer,n).hex())
        elif name=='CreateEventA':expected=[0,0,0,0];pointer,n=None,0;request=dict(args=args)
        elif name=='GetCurrentDirectoryA':
            expected=[DIRECTORY_BYTES,DIRECTORY];pointer,n=DIRECTORY,DIRECTORY_BYTES;request=dict(before_hex=self.bytes(pointer,n).hex())
        elif name=='PathAddBackslashA':
            expected=[DIRECTORY];pointer,n=DIRECTORY,DIRECTORY_BYTES;request=dict(before_hex=self.bytes(pointer,n).hex())
        else:
            index=sum(c['name']=='lstrcpyA' for c in self.all_calls)
            expected=[OWNER+PATHS[index],DIRECTORY if index==0 else OWNER+0x9EC] if name=='lstrcpyA' else [OWNER+0x1004,0x598694]
            pointer,n=args[0],260;source=self.bytes(args[1],260).split(b'\0',1)[0]+b'\0'
            request=dict(before_hex=self.bytes(pointer,n).hex(),source_hex=source.hex())
        if args!=expected:raise ValueError('main original API arguments '+name)
        result=self.platform.request(name,**request)
        if n:
            raw=bytes.fromhex(result['hex'])
            if len(raw)!=n:raise ValueError('main bounded full API output')
            self.uc.mem_write(pointer,raw)
        eax=result['eax_bits_observed'] if name=='InitializeCriticalSection' else pointer+result['return_offset'] if name in ('PathAddBackslashA','lstrcpyA','lstrcatA') else result['result']
        row=dict(name=name,slot=hex(slot),va=hex(at),return_va=hex(ret),sp=sp,args=args,request=request,result=result,
            mapped_output_pointer=pointer,mapped_output_bytes=n,observed_EAX=eax,live_host_observed=True)
        self.calls.append(row);self.all_calls.append(row);self._return(sp,eax,count)

    def _code(self,uc,at,n,user):
        if at==STOPS[self.phase]:self.boundary=at;uc.emu_stop();return
        sp=self.uc.reg_read(REGISTERS['ESP'])
        if at==0x56E810:return self._allocate(sp)
        if at in self.imports:return self._api(at,sp)
        i=self.code.get(at)
        if i is None or i.size!=n:raise ValueError('main undeclared native instruction '+hex(at))
        if self.runs and self.runs[-1]['va']==at:self.runs[-1]['count']+=1
        else:self.runs.append(dict(va=at,count=1))
        if at in self.ranges and at not in (ENTRY,0x56CE80):
            self.entries.append(dict(va=hex(at),return_va=hex(self.read(sp)),sp=sp,receiver=self.uc.reg_read(REGISTERS['ECX']),
                args=[self.read(sp+4+i*4) for i in range(ARGS.get(at,0))]))
        if i.mnemonic=='ret':self.returns.append(dict(va=hex(at),return_va=hex(self.read(sp)),sp=sp,eax=self.uc.reg_read(REGISTERS['EAX'])))

    def resume(self,phase,previous=None):
        start=ENTRY if phase=='allocation' else CTOR if phase=='constructor' else STOPS['constructor']
        before=self.cpu()
        if before['EIP']!=start or previous is not None and before!=previous['cpu']:raise ValueError('main same pending CPU')
        self.phase=phase;self.entries,self.returns,self.runs,self.calls,self.writes=[],[],[],[],[];self.boundary=None
        self.uc.emu_start(start,RETURN+1,timeout=20_000_000,count=1000000)
        if self.boundary!=STOPS[phase]:raise ValueError('main original boundary not reached')
        expected=initial_owner(self.fill) if phase=='allocation' else project_constructor(initial_owner(self.fill),self.all_calls)
        image=project_image(phase,self.all_calls)
        guarded=self.bytes(OWNER-4096,BACKING+8192)
        if guarded!=bytes([self.fill])*4096+expected+bytes([self.fill])*4096:raise ValueError('main complete constructed backing mismatch')
        if self.bytes(BASE,len(image))!=image:raise ValueError('main complete original image mismatch')
        stack=self.bytes(STACK,65536)
        if stack[:4096]!=self.last_stack[:4096] or stack[0xF100:]!=self.last_stack[0xF100:]:raise ValueError('main stack guards')
        if self.bytes(0,4096)!=bytes(4096):raise ValueError('main complete restored SEH page')
        for page,wanted in self.foreign.items():
            if self.bytes(page,4096)!=wanted:raise ValueError('main import maps unchanged')
        cpu=self.cpu();pending=dict(va=hex(STOPS[phase]),sp=cpu['ESP'],first_instruction_executed=False)
        if phase=='allocation':pending.update(return_va=hex(self.read(cpu['ESP'])),receiver=cpu['ECX'],args=[])
        else:pending.update(stack_top_dword=self.read(cpu['ESP']))
        row=dict(phase=phase,before_cpu=before,cpu=cpu,pending=pending,entries=self.entries,returns=self.returns,
            instruction_runs=self.runs,native_writes=self.writes,platform_calls=self.calls,allocations=list(self.allocations),
            state=dict(owner=buffer_evidence(expected),guarded_owner=buffer_evidence(guarded),stack=buffer_evidence(stack),
                image_sha256=hashlib.sha256(image).hexdigest(),SEH=0,null_page=buffer_evidence(self.bytes(0,4096)),
                directory=buffer_evidence(self.bytes(DIRECTORY,DIRECTORY_BYTES)),global_value=self.read(GLOBAL),counter=self.read(COUNTER),
                foreign_maps=[dict(pointer=p,**buffer_evidence(self.bytes(p,4096))) for p in sorted(self.foreign)]),
            original_global_published=phase=='publication',retained_VM_advanced=False,full_WinMain_executed=False)
        self.last_stack=stack
        return row


def generate():
    cases=[]
    for fill in (0xA5,0xCC):
        with MainPlatform() as platform:
            e=MainEmulator(platform,fill);case=dict(fill=fill,hello=platform.hello,system_modules=platform.provenance,declared_initial_cpu=initial_cpu())
            previous=None
            for phase in STOPS:case[phase]=e.resume(phase,previous);previous=case[phase]
        case.update(platform_trace=platform.trace,platform_cleanup=platform.cleanup);cases.append(case)
        print(hex(fill)+': original main allocation, full constructor and native global publication verified',flush=True)
    return dict(schema_version=1,source_contract=source_contract(),cases=cases,
        platform_build=json.loads((ROOT/'analysis/school-main-context-platform-v1-20261019.json').read_text(encoding='utf8'))['build'],
        one_continuous_CPU_per_case=True,declared_mid_WinMain_frame=True,WinMain_prelude_executed=False,
        original_IAT_changed=False,game_helpers_stubbed=False,retained_VM_advanced=False,standalone_resumable_checkpoint=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable main-context trajectory required')
    path.write_text(json.dumps(generate(),indent=2)+'\n',encoding='utf8',newline='\n')
