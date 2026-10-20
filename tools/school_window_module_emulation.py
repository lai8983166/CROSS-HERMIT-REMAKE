"""Fresh genuine HINSTANCE input; original startup and resource/class continuation."""
import argparse
import json
import struct
from tools.school_window_geometry_emulation import GeometryEmulator,REGISTERS,buffer_evidence,initial_cpu
from tools.school_window_module import *
from tools.school_window_module_platform import ModulePlatform

window=geometry.window
parent=geometry.parent
CLASS_AT,RECT_AT,CLIENT_RECT=geometry.CLASS_AT,geometry.RECT_AT,geometry.CLIENT_RECT
TITLE,TITLE_BYTES,INSTANCE=window.TITLE,window.TITLE_BYTES,window.INSTANCE
CLIENT_OFFSET=geometry.CLIENT_OFFSET


class ModuleEmulator(GeometryEmulator):
    def __init__(self,platform,fill):
        self.module_running=False;self.module=platform.module
        super().__init__(platform,fill)
        if self.cpu()!=initial_cpu():raise ValueError('module instance must be declared before first original instruction')
        self.uc.mem_write(parent.TOP+4,struct.pack('<I',self.module))
        self.last_stack=self.bytes(parent.STACK,65536)
        self.module_input=dict(root_va='0x49ddc9',before_first_original_instruction=True,slot=parent.TOP+4,value=self.module,
            cpu=self.cpu(),initial_stack=buffer_evidence(self.last_stack),source='owned actual resource module in helper hello')
        self.ranges=dict(self.ranges);self.ranges.update(RANGES)
        self.code.update({i.address:i for a,b in RANGES.items() for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(self.image[a-BASE:b-BASE],a)})

    def instance_image(self,before,phase):
        result=bytearray(window.project_image(before,phase));store(result,window.INSTANCE-BASE,self.module);return self.expected_image(result)

    def instance_class(self):
        result=bytearray(geometry.partial_class());store(result,20,self.module);return bytes(result)

    def _write(self,uc,access,at,n,value,user):
        if not self.module_running:return super()._write(uc,access,at,n,value,user)
        if not parent.STACK<=at or at+n>parent.STACK+65536:raise ValueError('module original resource code unowned write')
        self.writes.append(dict(pc=uc.reg_read(REGISTERS['EIP']),pointer=at,bytes=n,value=value&((1<<(n*8))-1)))

    def admit_resources(self,previous):
        before=self.cpu();owner=self.bytes(parent.OWNER-4096,parent.BACKING+8192);stack=self.bytes(parent.STACK,65536);image=self.bytes(BASE,len(self.image))
        maps_before=[dict(pointer=p,**buffer_evidence(self.bytes(p,4096))) for p in sorted(self.foreign)]
        for slot in IMPORTS:
            target=dword(self.image,slot-BASE);page=target&~4095
            if page not in self.foreign:
                if any(a<=page<=b for a,b,p in self.uc.mem_regions()):raise ValueError('module resource import map overlap')
                self.uc.mem_map(page,4096);self.foreign[page]=bytearray(4096)
            if self.foreign[page][target-page] not in (0,0xC3):raise ValueError('module resource trap conflict')
            self.foreign[page][target-page]=0xC3;self.uc.mem_write(target,b'\xc3')
        if before!=self.cpu() or owner!=self.bytes(parent.OWNER-4096,len(owner)) or stack!=self.bytes(parent.STACK,len(stack)) or image!=self.bytes(BASE,len(image)):raise ValueError('module resource admission modifies pending state')
        return dict(slots=[hex(s) for s in IMPORTS],before_cpu=before,after_cpu=self.cpu(),retained_owner_sha256=hashlib.sha256(owner).hexdigest(),
            retained_stack_sha256=hashlib.sha256(stack).hexdigest(),retained_image_sha256=hashlib.sha256(image).hexdigest(),
            foreign_before=maps_before,foreign_after=[dict(pointer=p,**buffer_evidence(self.bytes(p,4096))) for p in sorted(self.foreign)],native_game_call=False)

    def _resource_api(self,at,sp,slot):
        name,count,returns=IMPORTS[slot];ret=self.read(sp);args=[self.read(sp+4+i*4) for i in range(count)]
        if ret not in returns:raise ValueError('module actual original resource caller')
        if name=='LoadIconA':expected=[self.module,157];op='load_icon';request=dict(module=self.module,id_value=157)
        elif name=='LoadCursorA':expected=[0,32512];op='load_cursor';request=dict(module=0,id_value=32512)
        else:expected=[4];op='stock_brush';request=dict(id_value=4)
        if args!=expected:raise ValueError('module exact actual resource call arguments')
        r=self.platform.request(op,**request)
        self.calls.append(dict(name=name,op=op,slot=hex(slot),va=hex(at),return_va=hex(ret),sp=sp,args=args,request=request,result=r,observed_EAX=r['result'],live_host_observed=True))
        self.resource_calls.append(self.calls[-1]);self._return(sp,r['result'],count)

    def _code(self,uc,at,n,user):
        if not self.module_running:return super()._code(uc,at,n,user)
        if at==STOPS[self.phase]:self.boundary=at;uc.emu_stop();return
        sp=uc.reg_read(REGISTERS['ESP'])
        for slot in IMPORTS:
            if at==dword(self.image,slot-BASE):return self._resource_api(at,sp,slot)
        i=self.code.get(at)
        if i is None or i.size!=n or not any(a<=at and at+n<=b for a,b in RANGES.items()):raise ValueError('module undeclared original instruction '+hex(at))
        if self.runs and self.runs[-1]['va']==at:self.runs[-1]['count']+=1
        else:self.runs.append(dict(va=at,count=1))
        if i.mnemonic=='ret':self.returns.append(dict(va=hex(at),return_va=hex(self.read(sp)),sp=sp,eax=uc.reg_read(REGISTERS['EAX'])))

    def resume_resources(self,phase,previous):
        start=geometry.STOPS['class'] if phase=='icons' else STOPS['icons'];before=self.cpu()
        if before!=previous['cpu'] or before['EIP']!=start:raise ValueError('module same original pending CPU required')
        admission=self.admit_resources(previous) if phase=='icons' else None
        self.phase,self.module_running=phase,True;self.entries,self.returns,self.runs,self.calls,self.writes=[],[],[],[],[];self.boundary=None
        try:self.uc.emu_start(start,parent.RETURN+1,timeout=20_000_000,count=1000000)
        finally:self.module_running=False
        if self.boundary!=STOPS[phase]:raise ValueError('module natural class boundary not reached')
        owner=geometry.project_owner(window.project_owner(parent.project_constructor(parent.initial_owner(self.fill),self.all_calls),'branch',False))
        image=self.instance_image(parent.project_image('publication',self.all_calls),'branch')
        guarded=self.bytes(parent.OWNER-4096,parent.BACKING+8192);stack=self.bytes(parent.STACK,65536)
        if guarded!=bytes([self.fill])*4096+owner+bytes([self.fill])*4096 or self.bytes(BASE,len(image))!=image:raise ValueError('module complete retained owner/image/guards')
        if self.bytes(0,4096)!=bytes(4096) or stack[:4096]!=self.last_stack[:4096] or stack[0xF100:]!=self.last_stack[0xF100:]:raise ValueError('module null page/stack guards')
        for p,b in self.foreign.items():
            if self.bytes(p,4096)!=b:raise ValueError('module exact new import shadows')
        wanted=bytearray(self.instance_class());store(wanted,24,self.resource_calls[0]['result']['result']);store(wanted,44,self.resource_calls[1]['result']['result'])
        if phase=='class_ready':store(wanted,28,self.resource_calls[2]['result']['result']);store(wanted,32,self.resource_calls[3]['result']['result']);store(wanted,36,0)
        cls=self.bytes(geometry.CLASS_AT,48)
        if cls!=wanted:raise ValueError('module complete original class resource stores')
        cpu=self.cpu();pending=dict(va=hex(STOPS[phase]),sp=cpu['ESP'],first_instruction_executed=False)
        if phase=='class_ready':pending.update(import_slot='0x592408',import_target=dword(self.image,0x592408-BASE),stack_args=[self.read(cpu['ESP'])],call_instruction_executed=False)
        else:pending['stack_top_dword']=self.read(cpu['ESP'])
        self.last_stack=stack
        return dict(phase=phase,before_cpu=before,cpu=cpu,pending=pending,entries=[],returns=self.returns,instruction_runs=self.runs,native_writes=self.writes,platform_calls=self.calls,import_admission=admission,
            state=dict(owner=buffer_evidence(owner),guarded_owner=buffer_evidence(guarded),stack=buffer_evidence(stack),class_structure=buffer_evidence(cls),image_sha256=hashlib.sha256(image).hexdigest(),
                null_page=buffer_evidence(bytes(4096)),SEH=0,foreign_maps=[dict(pointer=p,**buffer_evidence(self.bytes(p,4096))) for p in sorted(self.foreign)]),
            genuine_instance=self.module,class_registration_executed=False,callback_executed=False,window_created=False,retained_VM_advanced=False)

    def resume_window(self,phase,previous):
        start={'tasks':window.ENTRY,'query':window.STOPS['tasks'],'branch':window.STOPS['query']}[phase]
        before=self.cpu()
        if before!=previous['cpu'] or before['EIP']!=start:raise ValueError('window unchanged same pending CPU required')
        if phase=='query':self.admit_query()
        stop=window.STOPS[phase] if phase!='branch' else window.EXIT_ENTRY if self.duplicate else window.WINDOW_ENTRY
        self.phase,self.stop,self.window_running=phase,stop,True
        self.entries,self.returns,self.runs,self.calls,self.writes=[],[],[],[],[];self.boundary=None
        try:self.uc.emu_start(start,parent.RETURN+1,timeout=20_000_000,count=1000000)
        finally:self.window_running=False
        if self.boundary!=stop:raise ValueError('window original natural boundary not reached')
        original_owner=parent.project_constructor(parent.initial_owner(self.fill),self.all_calls)
        owner=window.project_owner(original_owner,phase,self.duplicate)
        image=self.instance_image(parent.project_image('publication',self.all_calls),phase)
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

    def resume_geometry(self,phase,previous):
        start={'rect':geometry.ENTRY,'adjust':geometry.STOPS['rect'],'class':geometry.STOPS['adjust']}[phase];before=self.cpu()
        if self.duplicate is not False:raise ValueError('actual duplicate gate prevents geometry; no fabricated absence permitted')
        if before!=previous['cpu'] or before['EIP']!=start:raise ValueError('geometry same original pending CPU required')
        if phase=='rect':self.admit_geometry()
        self.phase,self.geometry_running=phase,True;self.entries,self.returns,self.runs,self.calls,self.writes=[],[],[],[],[];self.boundary=None
        try:self.uc.emu_start(start,parent.RETURN+1,timeout=20_000_000,count=1000000)
        finally:self.geometry_running=False
        if self.boundary!=geometry.STOPS[phase]:raise ValueError('geometry natural original boundary not reached')
        owner=geometry.project_owner(window.project_owner(parent.project_constructor(parent.initial_owner(self.fill),self.all_calls),'branch',False))
        image=self.instance_image(parent.project_image('publication',self.all_calls),'branch')
        guarded=self.bytes(parent.OWNER-4096,parent.BACKING+8192);stack=self.bytes(parent.STACK,65536)
        if guarded!=bytes([self.fill])*4096+owner+bytes([self.fill])*4096:raise ValueError('geometry full owner/client rectangle/guards')
        if self.bytes(BASE,len(image))!=image or self.bytes(0,4096)!=bytes(4096):raise ValueError('geometry preserved original image/SEH')
        if stack[:4096]!=self.last_stack[:4096] or stack[0xF100:]!=self.last_stack[0xF100:]:raise ValueError('geometry stack guards')
        for p,b in self.foreign.items():
            if self.bytes(p,4096)!=b:raise ValueError('geometry exact import shadows')
        cls=self.bytes(CLASS_AT,48);rectangle=self.bytes(RECT_AT,16)
        if cls!=(self.instance_class() if phase=='class' else b'\xcc'*48):raise ValueError('geometry exact partial class fields')
        if rectangle!=(b'\xcc'*16 if phase=='rect' else CLIENT_RECT):raise ValueError('geometry exact local rectangle')
        cpu=self.cpu();pending=dict(va=hex(geometry.STOPS[phase]),sp=cpu['ESP'],first_instruction_executed=False)
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
        with ModulePlatform() as p:
            e=ModuleEmulator(p,fill);e.resource_calls=[]
            c=dict(fill=fill,hello=p.hello,system_modules=p.provenance,declared_initial_cpu=initial_cpu(),module_input=e.module_input)
            previous=None
            for phase in parent.STOPS:c[phase]=e.resume(phase,previous);previous=c[phase]
            for phase in ('tasks','query','branch'):c[phase]=e.resume_window(phase,previous);previous=c[phase]
            for phase in geometry.STOPS:c[phase]=e.resume_geometry(phase,previous);previous=c[phase]
            for phase in STOPS:c[phase]=e.resume_resources(phase,previous);previous=c[phase]
        c.update(platform_trace=p.trace,platform_cleanup=p.cleanup);cases.append(c)
        print(hex(fill)+': genuine module '+hex(e.module)+' propagated from root; original complete class pending45047D',flush=True)
    return dict(schema_version=1,source_contract=source_contract(),cases=cases,
        platform_build=json.loads((ROOT/'analysis/school-window-module-platform-v1-20261020.json').read_text(encoding='utf8'))['build'],
        actual_genuine_module_declared_before_first_instruction=True,one_continuous_CPU_per_case=True,
        original_IAT_changed=False,game_helpers_stubbed=False,class_registration_executed=False,callback_executed=False,window_created=False,
        retained_VM_advanced=False,standalone_resumable_checkpoint=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable genuine-module trajectory required')
    path.write_text(json.dumps(generate(),indent=2)+chr(10),encoding='utf8',newline=chr(10))
