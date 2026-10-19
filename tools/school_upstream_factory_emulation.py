"""Original owner factory roots through allocation, full construction and admission."""
import argparse
import json
import struct
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_EIP,UC_X86_REG_ESP
from tools.school_owner_startup_emulation import OwnerEmulator,OWNER,STACK,TOP,RETURN,REGISTERS,buffer_evidence
from tools.school_owner_platform import OwnerPlatform,HELPER,COMPILER,sha,machine
from tools.school_upstream_factory import *


class FactoryEmulator(OwnerEmulator):
    def __init__(self,platform,kind,fill,width,height):
        self.factory_running=False
        super().__init__(None,platform,fill)
        self.kind,self.width,self.height=kind,width,height
        self.factory=FACTORIES[kind];self.factory_allocations=[]
        for at,n in ((OWNER-4096,4096),(OWNER+0xC000,4096),(OUTPUT-4096,12288)):
            self.uc.mem_map(at,n);self.uc.mem_write(at,bytes([fill])*n)
        self.uc.mem_write(OUTPUT,struct.pack('<I',OUTPUT_VALUE))
        self.ranges=RANGES
        md=Cs(CS_ARCH_X86,CS_MODE_32)
        self.ret_addresses={i.address for a,b in RANGES.items() for i in md.disasm(self.image[a-BASE:b-BASE],a) if i.mnemonic=='ret'}
        args=[WINDOW,OUTPUT,width,height]
        for name,value in dict(EIP=self.factory['entry'],ESP=TOP,EBP=0x11223344,EBX=0x55667788,
                ESI=0x88776655,EDI=0x44332211,ECX=RECEIVER,EAX=0,EDX=0,EFLAGS=2).items():self.uc.reg_write(REGISTERS[name],value)
        self.uc.mem_write(TOP,struct.pack('<5I',RETURN,*args));self.root_args=args

    def _map_page(self,address):
        if (OWNER-4096<=address<OWNER or OWNER+0xC000<=address<OWNER+0xD000
                or OUTPUT-4096<=address<OUTPUT+8192):raise RuntimeError('live interface mapping collides with audit ownership')
        return super()._map_page(address)

    def _write(self,uc,access,at,size,value,user):
        if not self.factory_running:return super()._write(uc,access,at,size,value,user)
        allowed=[(STACK,STACK+65536),(0,4)]
        if self.factory_phase=='allocation':allowed.append((COUNTER,COUNTER+4))
        if self.factory_phase=='constructor':allowed += [(OWNER,OWNER+OWNER_BYTES),
            (0x765728,0x79172A),(0x799AE0,0x799AF0),(0x5FF530,0x5FF534)]
        if not any(a<=at and at+size<=b for a,b in allowed):raise RuntimeError('factory unowned original write '+hex(at))

    def _allocate(self,sp):
        rule=source_contract()['allocator'];args=[self.read(sp+4+i*4) for i in range(4)]
        if (self.factory_phase!='allocation' or self.factory_allocations or self.read(sp)!=0x428A73
                or args!=[OWNER_BYTES,rule['block_type'],rule['file'],rule['line']]):raise RuntimeError('factory exact original owner CRT allocation')
        self.uc.mem_write(OWNER,b'\xcd'*OWNER_BYTES)
        self.factory_allocations.append(dict(va='0x56e810',return_va='0x428a73',sp=sp,args=args,pointer=OWNER,
            bytes=OWNER_BYTES,initial_byte=0xCD,adapter='declared debug CRT allocation'))
        self.uc.reg_write(UC_X86_REG_EAX,OWNER);self.uc.reg_write(UC_X86_REG_ESP,sp+4);self.uc.reg_write(UC_X86_REG_EIP,self.read(sp))

    def _code(self,uc,at,size,user):
        if not self.factory_running:return super()._code(uc,at,size,user)
        if at==self.factory_stop:self.boundary=at;uc.emu_stop();return
        sp=uc.reg_read(UC_X86_REG_ESP);ret=self.read(sp)
        if at==0x56E810:return self._allocate(sp)
        if at in self.imports:
            if self.factory_phase!='constructor':raise RuntimeError('factory unexpected platform call outside constructor')
            slot,rule=self.imports[at];return self._win(at,sp,ret,slot,rule)
        if not any(a<=at and at+size<=b for a,b in RANGES.items()):raise RuntimeError('factory undeclared original body '+hex(at))
        self.visited.add(at)
        if self.instruction_runs and self.instruction_runs[-1]['va']==at:self.instruction_runs[-1]['count']+=1
        else:self.instruction_runs.append(dict(va=at,count=1))
        if at in RANGES and at!=0x56CE80:
            count=4 if at in (0x412C70,0x450570) else 1 if at==0x428A40 else ARGS.get(at,0)
            self.entries.append(dict(va=hex(at),return_va=hex(ret),sp=sp,receiver=uc.reg_read(REGISTERS['ECX']),
                args=[self.read(sp+4+i*4) for i in range(count)]))
        if at in self.ret_addresses:self.returns.append(dict(va=hex(at),return_va=hex(ret),sp=sp,eax=uc.reg_read(UC_X86_REG_EAX)))

    def resume_factory(self,phase,previous=None):
        start={'allocation':self.factory['entry'],'constructor':CTOR,'admission':self.factory['constructor_return']}[phase]
        stop={'allocation':CTOR,'constructor':self.factory['constructor_return'],'admission':self.factory['admission']}[phase]
        before={k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        if before['EIP']!=start or previous is not None and before!=previous['native']['cpu']:
            raise RuntimeError('factory same original pending CPU required')
        self.entries,self.returns,self.win_calls,self.visited,self.boundary,self.instruction_runs=[],[],[],set(),None,[]
        self.factory_phase,self.factory_stop,self.factory_running=phase,stop,True
        try:self.uc.emu_start(start,RETURN+1,timeout=20_000_000,count=1000000)
        finally:self.factory_running=False
        if self.boundary!=stop:raise RuntimeError('factory natural original boundary not reached')
        if phase=='constructor':
            api={r['name']:r['result'] for r in self.win_calls}
            owner=project_constructor(initial_owner(self.fill),api);image=bytearray(project_image(api))
        elif phase=='allocation':owner=initial_owner(self.fill);image=bytearray(self.image)
        else:owner=self.projected_owner;image=bytearray(self.projected_image)
        if phase!='admission':store(image,COUNTER-BASE,dword(image,COUNTER-BASE)+OWNER_BYTES)
        state=self.check(owner,bytes(image),TOP-16)
        expected=bytes([self.fill])*4096+owner+bytes([self.fill])*4096
        guarded=bytes(self.uc.mem_read(OWNER-4096,0xE000))
        output=bytes(self.uc.mem_read(OUTPUT-4096,12288));wanted=bytearray(bytes([self.fill])*12288);store(wanted,4096,OUTPUT_VALUE)
        if guarded!=expected or output!=wanted:raise RuntimeError('factory complete allocation/output guards changed')
        self.projected_owner,self.projected_image=owner,bytes(image)
        missing=[]
        for at in (HEAD,GAME_GLOBAL):
            pointer=self.read(at)
            if any(a<=pointer<=b for a,b,perm in self.uc.mem_regions()):raise RuntimeError('factory missing inherited heap unexpectedly mapped')
            missing.append(dict(global_va=hex(at),pointer=pointer,mapped=False))
        cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        pending=dict(va=hex(stop),sp=cpu['ESP'],return_va=hex(self.read(cpu['ESP'])),receiver=cpu['ECX'],
            args=[self.read(cpu['ESP']+4+i*4) for i in range(5 if phase=='admission' and self.kind=='window' else 1 if phase=='admission' else 0)],
            first_instruction_executed=False)
        if phase=='constructor':
            pending=dict(va=hex(stop),sp=cpu['ESP'],stack_top_dword=self.read(cpu['ESP']),first_instruction_executed=False)
        return dict(phase=phase,before_cpu=before,
            native=dict(entries=self.entries,returns=self.returns,visited=sorted(self.visited),cpu=cpu,boundary=hex(stop),platform_calls=[],live_results=[]),
            platform_calls=self.win_calls,instruction_runs=self.instruction_runs,state=state,pending=pending,
            guarded_owner=buffer_evidence(guarded),guarded_output=buffer_evidence(output),allocations=list(self.factory_allocations),
            inherited_missing_heaps=missing,owner_constructed=phase!='allocation',factory_output_published=False,
            original_device_startup_executed=False,game_context_body_executed=False,audio_COM_initialized=False,retained_VM_advanced=False)


def generate():
    cases=[]
    for kind in FACTORIES:
        for fill,width,height in ((0xA5,640,480),(0xCC,1024,768)):
            with OwnerPlatform() as platform:
                e=FactoryEmulator(platform,kind,fill,width,height);c=dict(factory=kind,fill=fill,width=width,height=height,
                    root_args=e.root_args,declared_root_receiver=RECEIVER,platform_hello=platform.hello)
                previous=None
                for phase in ('allocation','constructor','admission'):c[phase]=e.resume_factory(phase,previous);previous=c[phase]
            c.update(platform_trace=platform.trace,platform_cleanup=platform.cleanup);cases.append(c)
            print(kind+' '+hex(fill)+': original owner allocated/constructed and natural next-call entry verified',flush=True)
    return dict(schema_version=1,source_contract=source_contract(),cases=cases,
        platform_build=json.loads((ROOT/'analysis/school-owner-startup-platform-v2-20261017.json').read_text())['build'],
        one_continuous_trajectory_per_case=True,inherited_cache_and_game_globals_unchanged=True,
        CRT_adapter_executed=True,original_IAT_changed=False,game_helpers_stubbed=False,
        factory_output_published=False,original_device_startup_executed=False,retained_VM_advanced=False,full_outer_frame=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable upstream factory trajectory required')
    path.write_text(json.dumps(generate(),indent=2)+chr(10),encoding='utf8',newline=chr(10))
