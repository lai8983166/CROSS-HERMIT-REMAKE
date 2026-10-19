"""Same original CPU/helper lifetime through task slots and actual window gate."""
import argparse
import json
from tools.school_main_context_emulation import MainEmulator,REGISTERS,buffer_evidence,initial_cpu
from tools.school_main_window import *
from tools.school_main_window_platform import MainWindowPlatform


class WindowEmulator(MainEmulator):
    def __init__(self,platform,fill):
        self.window_running=False
        super().__init__(platform,fill)
        self.ranges=dict(self.ranges)
        self.ranges.update(RANGES)
        self.code.update({i.address:i for a,b in RANGES.items() for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(self.image[a-BASE:b-BASE],a)})
        self.duplicate=None;self.import_admission=None

    def _write(self,uc,access,at,n,value,user):
        if not self.window_running:return super()._write(uc,access,at,n,value,user)
        allowed=[(parent.STACK,parent.STACK+65536)]
        if self.phase=='tasks':allowed.extend([(parent.OWNER+0x64,parent.OWNER+0x164),(INSTANCE,INSTANCE+4)])
        if self.phase=='branch' and not self.duplicate:allowed.extend([(parent.OWNER+0x5C,parent.OWNER+0x64),(parent.OWNER+0x1108,parent.OWNER+0x110C)])
        if not any(a<=at and at+n<=b for a,b in allowed):raise ValueError('window unowned original write '+hex(at))
        self.writes.append(dict(pc=uc.reg_read(REGISTERS['EIP']),pointer=at,bytes=n,value=value&((1<<(n*8))-1)))

    def admit_query(self):
        before=self.cpu();owner=self.bytes(parent.OWNER-4096,parent.BACKING+8192);stack=self.bytes(parent.STACK,65536)
        image=self.bytes(BASE,len(self.image));null=self.bytes(0,4096)
        maps_before=[dict(pointer=p,**buffer_evidence(self.bytes(p,4096))) for p in sorted(self.foreign)]
        target=dword(self.image,FIND_SLOT-BASE);page=target&~4095
        if page not in self.foreign:
            if any(a<=page<=b for a,b,p in self.uc.mem_regions()):raise ValueError('window late import overlaps owned mapping')
            self.uc.mem_map(page,4096);self.foreign[page]=bytearray(4096)
        if self.foreign[page][target-page] not in (0,0xC3):raise ValueError('window late import shadow conflict')
        self.foreign[page][target-page]=0xC3;self.uc.mem_write(target,b'\xc3')
        if (before!=self.cpu() or owner!=self.bytes(parent.OWNER-4096,len(owner)) or stack!=self.bytes(parent.STACK,len(stack))
                or image!=self.bytes(BASE,len(image)) or null!=self.bytes(0,4096)):raise ValueError('window import admission changed retained state')
        self.import_admission=dict(slot=hex(FIND_SLOT),target=target,before_cpu=before,after_cpu=self.cpu(),
            retained_owner_sha256=hashlib.sha256(owner).hexdigest(),retained_stack_sha256=hashlib.sha256(stack).hexdigest(),
            retained_image_sha256=hashlib.sha256(image).hexdigest(),retained_null_page_sha256=hashlib.sha256(null).hexdigest(),
            foreign_before=maps_before,foreign_after=[dict(pointer=p,**buffer_evidence(self.bytes(p,4096))) for p in sorted(self.foreign)],
            native_game_call=False)

    def _window_api(self,at,sp):
        ret=self.read(sp);args=[self.read(sp+4+i*4) for i in range(2)]
        if ret==0x49DE3E and at==dword(self.image,0x592294-BASE):
            if args!=[TITLE,0x598748]:raise ValueError('window original title-copy arguments')
            request=dict(before_hex=self.bytes(TITLE,TITLE_BYTES).hex(),source_hex=self.bytes(0x598748,len(TITLE_TEXT)).hex())
            op='copy_title';result=self.platform.request(op,**request);output=bytes.fromhex(result['hex'])
            if len(output)!=TITLE_BYTES:raise ValueError('window complete bounded title response')
            self.uc.mem_write(TITLE,output);eax=TITLE;pointer,n=TITLE,TITLE_BYTES;slot=0x592294;name='lstrcpyA'
        elif ret==0x42940C and at==dword(self.image,FIND_SLOT-BASE):
            if args!=[TITLE,0]:raise ValueError('window actual class/null-title arguments')
            request=dict(class_hex=self.bytes(TITLE,len(TITLE_TEXT)).hex(),window_name=0)
            op='find_window';result=self.platform.request(op,**request);eax=result['result'];pointer,n=None,0;slot=FIND_SLOT;name='FindWindowA'
            self.duplicate=eax!=0
        else:raise ValueError('window exact original external caller')
        self.calls.append(dict(name=name,op=op,slot=hex(slot),va=hex(at),return_va=hex(ret),sp=sp,args=args,
            request=request,result=result,observed_EAX=eax,mapped_output_pointer=pointer,mapped_output_bytes=n,live_host_observed=True))
        self._return(sp,eax,2)

    def _code(self,uc,at,n,user):
        if not self.window_running:return super()._code(uc,at,n,user)
        if at==self.stop:self.boundary=at;uc.emu_stop();return
        sp=uc.reg_read(REGISTERS['ESP'])
        if at in (dword(self.image,0x592294-BASE),dword(self.image,FIND_SLOT-BASE)):
            if self.phase!='query':raise ValueError('window API outside original query phase')
            return self._window_api(at,sp)
        i=self.code.get(at)
        if i is None or i.size!=n or not any(a<=at and at+n<=b for a,b in RANGES.items()):raise ValueError('window undeclared original instruction '+hex(at))
        if self.runs and self.runs[-1]['va']==at:self.runs[-1]['count']+=1
        else:self.runs.append(dict(va=at,count=1))
        if at in (0x421660,0x4293E0,0x450290):
            self.entries.append(dict(va=hex(at),return_va=hex(self.read(sp)),sp=sp,receiver=uc.reg_read(REGISTERS['ECX']),
                args=[self.read(sp+4)] if at==0x450290 else []))
        if i.mnemonic=='ret':self.returns.append(dict(va=hex(at),return_va=hex(self.read(sp)),sp=sp,eax=uc.reg_read(REGISTERS['EAX'])))

    def resume_window(self,phase,previous):
        start={'tasks':ENTRY,'query':STOPS['tasks'],'branch':STOPS['query']}[phase]
        before=self.cpu()
        if before!=previous['cpu'] or before['EIP']!=start:raise ValueError('window unchanged same pending CPU required')
        if phase=='query':self.admit_query()
        stop=STOPS[phase] if phase!='branch' else EXIT_ENTRY if self.duplicate else WINDOW_ENTRY
        self.phase,self.stop,self.window_running=phase,stop,True
        self.entries,self.returns,self.runs,self.calls,self.writes=[],[],[],[],[];self.boundary=None
        try:self.uc.emu_start(start,parent.RETURN+1,timeout=20_000_000,count=1000000)
        finally:self.window_running=False
        if self.boundary!=stop:raise ValueError('window original natural boundary not reached')
        original_owner=parent.project_constructor(parent.initial_owner(self.fill),self.all_calls)
        owner=project_owner(original_owner,phase,self.duplicate)
        image=project_image(parent.project_image('publication',self.all_calls),phase)
        guarded=self.bytes(parent.OWNER-4096,parent.BACKING+8192);stack=self.bytes(parent.STACK,65536)
        if guarded!=bytes([self.fill])*4096+owner+bytes([self.fill])*4096:raise ValueError('window full owner/backing guards')
        if self.bytes(BASE,len(image))!=image or self.bytes(0,4096)!=bytes(4096):raise ValueError('window original image/SEH')
        if stack[:4096]!=self.last_stack[:4096] or stack[0xF100:]!=self.last_stack[0xF100:]:raise ValueError('window stack guards')
        for p,b in self.foreign.items():
            if self.bytes(p,4096)!=b:raise ValueError('window import maps preserved')
        cpu=self.cpu();pending=dict(va=hex(stop),sp=cpu['ESP'],first_instruction_executed=False)
        if phase=='branch' and not self.duplicate:pending.update(return_va=hex(self.read(cpu['ESP'])),receiver=cpu['ECX'],args=[self.read(cpu['ESP']+4+i*4) for i in range(6)])
        else:pending['stack_top_dword']=self.read(cpu['ESP'])
        self.last_stack=stack
        return dict(phase=phase,before_cpu=before,cpu=cpu,pending=pending,entries=self.entries,returns=self.returns,
            instruction_runs=self.runs,native_writes=self.writes,platform_calls=self.calls,
            observed_duplicate=self.duplicate,import_admission=self.import_admission if phase=='query' else None,
            state=dict(owner=buffer_evidence(owner),guarded_owner=buffer_evidence(guarded),stack=buffer_evidence(stack),
                image_sha256=hashlib.sha256(image).hexdigest(),null_page=buffer_evidence(bytes(4096)),SEH=0,
                title=buffer_evidence(self.bytes(TITLE,TITLE_BYTES)),instance_value=self.read(INSTANCE),
                foreign_maps=[dict(pointer=p,**buffer_evidence(self.bytes(p,4096))) for p in sorted(self.foreign)]),
            window_creation_body_executed=False,exit_body_executed=False,retained_VM_advanced=False)


def generate():
    cases=[]
    for fill in (0xA5,0xCC):
        with MainWindowPlatform() as p:
            e=WindowEmulator(p,fill);c=dict(fill=fill,hello=p.hello,system_modules=p.provenance,declared_initial_cpu=initial_cpu())
            previous=None
            for phase in parent.STOPS:c[phase]=e.resume(phase,previous);previous=c[phase]
            for phase in ('tasks','query','branch'):c[phase]=e.resume_window(phase,previous);previous=c[phase]
        c.update(platform_trace=p.trace,platform_cleanup=p.cleanup);cases.append(c)
        print(hex(fill)+': original tasks/title/live query, duplicate='+str(e.duplicate)+', pending='+c['branch']['pending']['va'],flush=True)
    return dict(schema_version=1,source_contract=source_contract(),cases=cases,
        platform_build=json.loads((ROOT/'analysis/school-main-window-platform-v1-20261020.json').read_text(encoding='utf8'))['build'],
        prefix_verified_with_new_build_identity=True,one_continuous_CPU_per_case=True,declared_mid_WinMain_frame=True,
        live_query_result_fabricated=False,original_IAT_changed=False,game_helpers_stubbed=False,retained_VM_advanced=False,
        window_created=False,standalone_resumable_checkpoint=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable window trajectory required')
    path.write_text(json.dumps(generate(),indent=2)+'\n',encoding='utf8',newline='\n')
