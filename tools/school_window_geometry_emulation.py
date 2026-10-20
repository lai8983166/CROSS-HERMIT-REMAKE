"""Continue the original450350 caller stack through geometry to LoadIconA admission."""
import argparse
import json
from tools.school_main_window_emulation import WindowEmulator,REGISTERS,buffer_evidence,initial_cpu
from tools.school_window_geometry import *
from tools.school_window_geometry_platform import GeometryPlatform


class GeometryEmulator(WindowEmulator):
    def __init__(self,platform,fill):
        self.geometry_running=False
        super().__init__(platform,fill)
        self.ranges=dict(self.ranges);self.ranges.update(RANGES)
        self.code.update({i.address:i for a,b in RANGES.items() for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(self.image[a-BASE:b-BASE],a)})
        self.geometry_import_admission=None

    def admit_geometry(self):
        before=self.cpu();owner=self.bytes(parent.OWNER-4096,parent.BACKING+8192)
        stack=self.bytes(parent.STACK,65536);image=self.bytes(BASE,len(self.image));null=self.bytes(0,4096)
        maps_before=[dict(pointer=p,**buffer_evidence(self.bytes(p,4096))) for p in sorted(self.foreign)]
        for slot in IMPORTS:
            target=dword(self.image,slot-BASE);page=target&~4095
            if page not in self.foreign:
                if any(a<=page<=b for a,b,p in self.uc.mem_regions()):raise ValueError('geometry import mapping overlap')
                self.uc.mem_map(page,4096);self.foreign[page]=bytearray(4096)
            if self.foreign[page][target-page] not in (0,0xC3):raise ValueError('geometry import shadow conflict')
            self.foreign[page][target-page]=0xC3;self.uc.mem_write(target,b'\xc3')
        if before!=self.cpu() or owner!=self.bytes(parent.OWNER-4096,len(owner)) or stack!=self.bytes(parent.STACK,len(stack)) or image!=self.bytes(BASE,len(image)) or null!=self.bytes(0,4096):raise ValueError('geometry import admission modified retained state')
        self.geometry_import_admission=dict(slots=[hex(s) for s in IMPORTS],before_cpu=before,after_cpu=self.cpu(),
            retained_owner_sha256=hashlib.sha256(owner).hexdigest(),retained_stack_sha256=hashlib.sha256(stack).hexdigest(),
            retained_image_sha256=hashlib.sha256(image).hexdigest(),retained_null_page_sha256=hashlib.sha256(null).hexdigest(),
            foreign_before=maps_before,foreign_after=[dict(pointer=p,**buffer_evidence(self.bytes(p,4096))) for p in sorted(self.foreign)],native_game_call=False)

    def _write(self,uc,access,at,n,value,user):
        if not self.geometry_running:return super()._write(uc,access,at,n,value,user)
        if not parent.STACK<=at or at+n>parent.STACK+65536:raise ValueError('geometry unowned original write '+hex(at))
        self.writes.append(dict(pc=uc.reg_read(REGISTERS['EIP']),pointer=at,bytes=n,value=value&((1<<(n*8))-1)))

    def _geometry_api(self,at,sp,slot):
        name,count,ret=IMPORTS[slot];args=[self.read(sp+4+i*4) for i in range(count)]
        if self.read(sp)!=ret:raise ValueError('geometry original API caller')
        if name=='SetRect':
            expected=[parent.OWNER+CLIENT_OFFSET,0,0,1024,768];op='set_rect'
            if self.phase!='rect' or args!=expected:raise ValueError('geometry original SetRect ABI')
            request=dict(before_hex=self.bytes(args[0],16).hex(),args=args[1:])
        else:
            expected=[RECT_AT,STYLE,0];op='adjust_window_rect'
            if self.phase!='adjust' or args!=expected:raise ValueError('geometry original AdjustWindowRect ABI')
            request=dict(before_hex=self.bytes(args[0],16).hex(),style=args[1],menu=args[2])
        result=self.platform.request(op,**request);raw=bytes.fromhex(result['hex'])
        if len(raw)!=16:raise ValueError('geometry complete RECT output')
        self.uc.mem_write(args[0],raw);self.calls.append(dict(name=name,op=op,slot=hex(slot),va=hex(at),return_va=hex(ret),sp=sp,args=args,
            request=request,result=result,observed_EAX=result['result'],mapped_output_pointer=args[0],mapped_output_bytes=16,live_host_observed=True))
        self._return(sp,result['result'],count)

    def _code(self,uc,at,n,user):
        if not self.geometry_running:return super()._code(uc,at,n,user)
        if at==STOPS[self.phase]:self.boundary=at;uc.emu_stop();return
        sp=uc.reg_read(REGISTERS['ESP'])
        for slot in IMPORTS:
            if at==dword(self.image,slot-BASE):return self._geometry_api(at,sp,slot)
        i=self.code.get(at)
        if i is None or i.size!=n or not any(a<=at and at+n<=b for a,b in RANGES.items()):raise ValueError('geometry undeclared original instruction '+hex(at))
        if self.runs and self.runs[-1]['va']==at:self.runs[-1]['count']+=1
        else:self.runs.append(dict(va=at,count=1))
        if at==ENTRY:self.entries.append(dict(va=hex(at),return_va=hex(self.read(sp)),sp=sp,receiver=uc.reg_read(REGISTERS['ECX']),args=[self.read(sp+4+i*4) for i in range(6)]))
        if i.mnemonic=='ret':self.returns.append(dict(va=hex(at),return_va=hex(self.read(sp)),sp=sp,eax=uc.reg_read(REGISTERS['EAX'])))

    def resume_geometry(self,phase,previous):
        start={'rect':ENTRY,'adjust':STOPS['rect'],'class':STOPS['adjust']}[phase];before=self.cpu()
        if self.duplicate is not False:raise ValueError('actual duplicate gate prevents geometry; no fabricated absence permitted')
        if before!=previous['cpu'] or before['EIP']!=start:raise ValueError('geometry same original pending CPU required')
        if phase=='rect':self.admit_geometry()
        self.phase,self.geometry_running=phase,True;self.entries,self.returns,self.runs,self.calls,self.writes=[],[],[],[],[];self.boundary=None
        try:self.uc.emu_start(start,parent.RETURN+1,timeout=20_000_000,count=1000000)
        finally:self.geometry_running=False
        if self.boundary!=STOPS[phase]:raise ValueError('geometry natural original boundary not reached')
        owner=project_owner(window.project_owner(parent.project_constructor(parent.initial_owner(self.fill),self.all_calls),'branch',False))
        image=window.project_image(parent.project_image('publication',self.all_calls),'branch')
        guarded=self.bytes(parent.OWNER-4096,parent.BACKING+8192);stack=self.bytes(parent.STACK,65536)
        if guarded!=bytes([self.fill])*4096+owner+bytes([self.fill])*4096:raise ValueError('geometry full owner/client rectangle/guards')
        if self.bytes(BASE,len(image))!=image or self.bytes(0,4096)!=bytes(4096):raise ValueError('geometry preserved original image/SEH')
        if stack[:4096]!=self.last_stack[:4096] or stack[0xF100:]!=self.last_stack[0xF100:]:raise ValueError('geometry stack guards')
        for p,b in self.foreign.items():
            if self.bytes(p,4096)!=b:raise ValueError('geometry exact import shadows')
        cls=self.bytes(CLASS_AT,48);rectangle=self.bytes(RECT_AT,16)
        if cls!=(partial_class() if phase=='class' else b'\xcc'*48):raise ValueError('geometry exact partial class fields')
        if rectangle!=(b'\xcc'*16 if phase=='rect' else CLIENT_RECT):raise ValueError('geometry exact local rectangle')
        cpu=self.cpu();pending=dict(va=hex(STOPS[phase]),sp=cpu['ESP'],first_instruction_executed=False)
        if phase=='class':pending.update(import_slot='0x5923cc',import_target=dword(self.image,0x5923CC-BASE),stack_args=[self.read(cpu['ESP']),self.read(cpu['ESP']+4)],call_instruction_executed=False)
        else:pending['stack_top_dword']=self.read(cpu['ESP'])
        self.last_stack=stack
        return dict(phase=phase,before_cpu=before,cpu=cpu,pending=pending,entries=self.entries,returns=self.returns,instruction_runs=self.runs,native_writes=self.writes,platform_calls=self.calls,
            import_admission=self.geometry_import_admission if phase=='rect' else None,
            state=dict(owner=buffer_evidence(owner),guarded_owner=buffer_evidence(guarded),stack=buffer_evidence(stack),image_sha256=hashlib.sha256(image).hexdigest(),
                client_rectangle=buffer_evidence(self.bytes(parent.OWNER+CLIENT_OFFSET,16)),local_rectangle=buffer_evidence(rectangle),class_structure=buffer_evidence(cls),
                null_page=buffer_evidence(bytes(4096)),SEH=0,foreign_maps=[dict(pointer=p,**buffer_evidence(self.bytes(p,4096))) for p in sorted(self.foreign)]),
            original_window_function_prefix_executed=True,LoadIconA_executed=False,class_registered=False,window_created=False,retained_VM_advanced=False)


def generate():
    cases=[]
    for fill in (0xA5,0xCC):
        with GeometryPlatform() as p:
            e=GeometryEmulator(p,fill);c=dict(fill=fill,hello=p.hello,system_modules=p.provenance,declared_initial_cpu=initial_cpu());previous=None
            for phase in parent.STOPS:c[phase]=e.resume(phase,previous);previous=c[phase]
            for phase in ('tasks','query','branch'):c[phase]=e.resume_window(phase,previous);previous=c[phase]
            for phase in STOPS:c[phase]=e.resume_geometry(phase,previous);previous=c[phase]
        c.update(platform_trace=p.trace,platform_cleanup=p.cleanup);cases.append(c)
        print(hex(fill)+': original SetRect/AdjustWindowRect/partial class to unexecuted450416 verified',flush=True)
    return dict(schema_version=1,source_contract=source_contract(),cases=cases,
        platform_build=json.loads((ROOT/'analysis/school-window-geometry-platform-v1-20261020.json').read_text(encoding='utf8'))['build'],
        actual_prefix_replayed_under_new_build_identity=True,one_continuous_CPU_per_case=True,declared_mid_WinMain_frame=True,
        original_IAT_changed=False,game_helpers_stubbed=False,LoadIconA_executed=False,window_created=False,retained_VM_advanced=False,standalone_resumable_checkpoint=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable geometry trajectory required')
    path.write_text(json.dumps(generate(),indent=2)+'\n',encoding='utf8',newline='\n')
