"""Same original scratch CPU: real class atom and native creation preparation."""
import argparse
import json
from tools.school_window_class import *
from tools.school_window_module_emulation import ModuleEmulator,REGISTERS,buffer_evidence,initial_cpu
from tools.school_window_class_platform import ClassPlatform


class ClassEmulator(ModuleEmulator):
    def __init__(self,platform,fill):
        self.class_running=False
        super().__init__(platform,fill)
        self.resource_calls=[]
        self.ranges=dict(self.ranges);self.ranges.update(RANGES)
        self.code.update({i.address:i for a,b in RANGES.items() for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(self.image[a-BASE:b-BASE],a)})

    def admit_registration(self):
        cpu=self.cpu();owner=self.bytes(parent.OWNER-4096,parent.BACKING+8192);stack=self.bytes(parent.STACK,65536);image=self.bytes(BASE,len(self.image))
        before=[dict(pointer=p,**buffer_evidence(self.bytes(p,4096))) for p in sorted(self.foreign)]
        target=dword(self.image,SLOT-BASE);page=target&~4095
        if page not in self.foreign:
            if any(a<=page<=b for a,b,p in self.uc.mem_regions()):raise ValueError('class import shadow overlap')
            self.uc.mem_map(page,4096);self.foreign[page]=bytearray(4096)
        if self.foreign[page][target-page] not in (0,0xC3):raise ValueError('class import shadow conflict')
        self.foreign[page][target-page]=0xC3;self.uc.mem_write(target,b'\xc3')
        if cpu!=self.cpu() or owner!=self.bytes(parent.OWNER-4096,len(owner)) or stack!=self.bytes(parent.STACK,len(stack)) or image!=self.bytes(BASE,len(image)) or self.bytes(0,4096)!=bytes(4096):
            raise ValueError('class import admission changed pending state')
        return dict(slots=[hex(SLOT)],before_cpu=cpu,after_cpu=self.cpu(),retained_owner_sha256=hashlib.sha256(owner).hexdigest(),
            retained_stack_sha256=hashlib.sha256(stack).hexdigest(),retained_image_sha256=hashlib.sha256(image).hexdigest(),
            foreign_before=before,foreign_after=[dict(pointer=p,**buffer_evidence(self.bytes(p,4096))) for p in sorted(self.foreign)],native_game_call=False)

    def _write(self,uc,access,at,n,value,user):
        if not self.class_running:return super()._write(uc,access,at,n,value,user)
        if not geometry.FRAME_SP-64<=at or at+n>geometry.ENTRY_SP:raise ValueError('class unowned native caller write')
        self.writes.append(dict(pc=uc.reg_read(REGISTERS['EIP']),pointer=at,bytes=n,value=value&((1<<(n*8))-1)))

    def _code(self,uc,at,n,user):
        if not self.class_running:return super()._code(uc,at,n,user)
        if at==STOPS[self.phase]:self.boundary=at;uc.emu_stop();return
        sp=uc.reg_read(REGISTERS['ESP'])
        if at==dword(self.image,SLOT-BASE):
            ret=self.read(sp);args=[self.read(sp+4)]
            if ret!=STOPS['registered'] or args!=[geometry.CLASS_AT]:raise ValueError('class actual original registration ABI')
            guest=self.bytes(geometry.CLASS_AT,48);name=self.bytes(window.TITLE,len(NAME_BYTES))
            if name!=NAME_BYTES:raise ValueError('class original ANSI name bytes')
            request=dict(class_hex=guest.hex(),class_name_hex=name.hex());r=self.platform.request('register_class',**request)
            self.calls.append(dict(name='RegisterClassExA',op='register_class',slot=hex(SLOT),va=hex(at),return_va=hex(ret),sp=sp,args=args,
                request=request,result=r,observed_EAX=r['eax_bits_observed'],live_host_observed=True))
            self._return(sp,r['eax_bits_observed'],1);return
        i=self.code.get(at)
        if i is None or i.size!=n or not any(a<=at and at+n<=b for a,b in RANGES.items()):raise ValueError('class undeclared original instruction '+hex(at))
        if self.runs and self.runs[-1]['va']==at:self.runs[-1]['count']+=1
        else:self.runs.append(dict(va=at,count=1))
        if i.mnemonic=='ret':self.returns.append(dict(va=hex(at),return_va=hex(self.read(sp)),sp=sp,eax=uc.reg_read(REGISTERS['EAX'])))

    def resume_class(self,phase,previous):
        start=ENTRY if phase=='registered' else STOPS['registered'];before=self.cpu()
        if before!=previous['cpu'] or before['EIP']!=start:raise ValueError('class same original pending CPU required')
        admission=self.admit_registration() if phase=='registered' else None
        if phase=='create_ready' and not before['EAX']&0xFFFF:raise ValueError('real registration failure; never synthesize success')
        self.phase,self.class_running=phase,True;self.entries,self.returns,self.runs,self.calls,self.writes=[],[],[],[],[];self.boundary=None
        try:self.uc.emu_start(start,parent.RETURN+1,timeout=20_000_000,count=1000000)
        finally:self.class_running=False
        if self.boundary!=STOPS[phase]:raise ValueError('class natural boundary not reached')
        guarded=self.bytes(parent.OWNER-4096,parent.BACKING+8192);stack=self.bytes(parent.STACK,65536);cls=self.bytes(geometry.CLASS_AT,48)
        if buffer_evidence(guarded)!=previous['state']['guarded_owner'] or hashlib.sha256(self.bytes(BASE,len(self.image))).hexdigest()!=previous['state']['image_sha256'] or buffer_evidence(cls)!=previous['state']['class_structure']:
            raise ValueError('class complete retained owner/image/raw class')
        if self.bytes(0,4096)!=bytes(4096) or stack[:4096]!=self.last_stack[:4096] or stack[0xF100:]!=self.last_stack[0xF100:]:raise ValueError('class null/stack guards')
        for p,b in self.foreign.items():
            if self.bytes(p,4096)!=b:raise ValueError('class exact foreign import shadows')
        cpu=self.cpu();pending=dict(va=hex(STOPS[phase]),sp=cpu['ESP'],first_instruction_executed=False)
        if phase=='create_ready':
            args=[self.read(cpu['ESP']+i*4) for i in range(12)]
            if args!=creation_args(self.module):raise ValueError('class actual original12 creation arguments')
            pending.update(import_slot='0x59240c',import_target=dword(self.image,0x59240C-BASE),stack_args=args,call_instruction_executed=False)
        else:pending['stack_top_dword']=self.read(cpu['ESP'])
        self.last_stack=stack
        return dict(phase=phase,before_cpu=before,cpu=cpu,pending=pending,entries=[],returns=self.returns,instruction_runs=self.runs,
            native_writes=self.writes,platform_calls=self.calls,import_admission=admission,
            state=dict(owner=buffer_evidence(self.bytes(parent.OWNER,parent.BACKING)),guarded_owner=buffer_evidence(guarded),stack=buffer_evidence(stack),
                class_structure=buffer_evidence(cls),image_sha256=hashlib.sha256(self.bytes(BASE,len(self.image))).hexdigest(),null_page=buffer_evidence(bytes(4096)),SEH=0,
                foreign_maps=[dict(pointer=p,**buffer_evidence(self.bytes(p,4096))) for p in sorted(self.foreign)]),
            class_registration_executed=True,callback_executed=False,window_created=False,retained_VM_advanced=False)


def generate():
    cases=[]
    for fill in (0xA5,0xCC):
        with ClassPlatform() as p:
            e=ClassEmulator(p,fill)
            c=dict(fill=fill,hello=p.hello,system_modules=p.provenance,declared_initial_cpu=initial_cpu(),module_input=e.module_input)
            previous=None
            for phase in parent.STOPS:c[phase]=e.resume(phase,previous);previous=c[phase]
            for phase in ('tasks','query','branch'):c[phase]=e.resume_window(phase,previous);previous=c[phase]
            for phase in geometry.STOPS:c[phase]=e.resume_geometry(phase,previous);previous=c[phase]
            for phase in module.STOPS:c[phase]=e.resume_resources(phase,previous);previous=c[phase]
            for phase in STOPS:c[phase]=e.resume_class(phase,previous);previous=c[phase]
            if p.callback_packets:raise ValueError('registration unexpectedly invoked native callback')
        c.update(platform_trace=p.trace,platform_cleanup=p.cleanup,callback_packets=p.callback_packets);cases.append(c)
        print(hex(fill)+': original class registered atom '+hex(c['registered']['platform_calls'][0]['result']['atom'])+'; native creation pending4504CF',flush=True)
    return dict(schema_version=1,source_contract=source_contract(),cases=cases,
        platform_build=json.loads((ROOT/'analysis/school-window-class-platform-v1-20261020.json').read_text(encoding='utf8'))['build'],
        actual_genuine_module_declared_before_first_instruction=True,one_continuous_CPU_per_case=True,original_IAT_changed=False,
        game_helpers_stubbed=False,class_registration_executed=True,callback_executed=False,window_created=False,retained_VM_advanced=False,standalone_resumable_checkpoint=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    if out.exists():p.error('fresh immutable native class trajectory required')
    out.write_text(json.dumps(generate(),indent=2)+'\n',encoding='utf8',newline='\n')
