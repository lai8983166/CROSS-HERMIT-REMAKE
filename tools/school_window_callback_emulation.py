"""Execute original genuine early WNDPROC calls while original creation is suspended."""
import argparse
import json
from unicorn import UC_HOOK_MEM_READ
from tools.school_window_callback import *
from tools.school_window_class_emulation import ClassEmulator,REGISTERS,initial_cpu,buffer_evidence
from tools.school_window_callback_platform import CallbackPlatform,CallbackBoundary


class CallbackEmulator(ClassEmulator):
    def __init__(self,p,fill):
        self.callback_running=False;self.creation_running=False
        super().__init__(p,fill);self.completed_callbacks=[];self.completed_nc=False;self.pending_callback=None
        self.callback_code={i.address:i for a,b in RANGES.items() for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(self.image[a-BASE:b-BASE],a)}
        self.uc.hook_add(UC_HOOK_MEM_READ,self._read_callback)

    def _read_callback(self,uc,access,at,n,value,user):
        if not self.callback_running:return
        if not any(a<=at and at+n<=b for a,b in ((BASE,BASE+len(self.image)),(parent.OWNER,parent.OWNER+parent.BACKING),(STACK,STACK+65536),(SHADOW-4096,SHADOW+8192))):
            raise ValueError('callback source read outside owned maps '+hex(at))
        self.cb_reads.append(dict(pc=uc.reg_read(REGISTERS['EIP']),pointer=at,bytes=n,hex=self.bytes(at,n).hex()))

    def _write(self,uc,access,at,n,value,user):
        if self.callback_running:
            if not (STACK<=at and at+n<=STACK+65536 or at in (parent.OWNER+4,parent.OWNER+12) and n==4):raise ValueError('callback unowned source write')
            self.cb_writes.append(dict(pc=uc.reg_read(REGISTERS['EIP']),pointer=at,bytes=n,value=value&((1<<(n*8))-1)));return
        if self.creation_running:
            self.creation_writes.append(dict(pc=uc.reg_read(REGISTERS['EIP']),pointer=at,bytes=n,value=value));return
        super()._write(uc,access,at,n,value,user)

    def _callback_api(self,at,sp,slot):
        name,n=IMPORTS[slot];args=[self.read(sp+4+i*4) for i in range(n)];packet=self.cb_packet
        request=dict(callback_id=packet['callback_id']);expected_hwnd=packet['hwnd']
        if name in ('GetPropA','SetPropA'):
            if args[:2]!=[expected_hwnd,0x594AB4] or self.bytes(args[1],10)!=PROPERTY:raise ValueError('callback source property args')
            request.update(hwnd=args[0],name_hex=PROPERTY.hex());op='get_prop' if name=='GetPropA' else 'set_prop'
            if name=='SetPropA':
                if args[2]!=parent.OWNER:raise ValueError('callback original opaque property data')
                request['data']=args[2]
        elif name=='GetWindowLongA':
            if args[0]!=expected_hwnd or args[1] not in (4,0xFFFFFFFC):raise ValueError('callback original window-long args')
            request.update(hwnd=args[0],index=args[1]);op='get_window_long'
        else:
            expected=[packet['hwnd'],packet['message'],packet['wParam'],SHADOW if packet['message']==129 else packet['lParam']]
            if args!=expected:raise ValueError('callback original default procedure args')
            request['args']=args;op='default_window'
        ret=self.read(sp);r=self.platform.request(op,**request)
        if name=='DefWindowProcA' and packet['message']==129:
            if self.bytes(SHADOW,48).hex()!=r['before_hex']:raise ValueError('callback exact actual CREATESTRUCT before default')
            self.uc.mem_write(SHADOW,bytes.fromhex(r['after_hex']))
        self.cb_calls.append(dict(name=name,op=op,slot=hex(slot),va=hex(at),sp=sp,return_va=hex(ret),args=args,request=request,result=r,observed_EAX=r['result'],live_host_observed=True))
        self._return(sp,r['result'],n)

    def _code(self,uc,at,n,user):
        if self.callback_running:
            if at==RETURN:uc.emu_stop();return
            sp=uc.reg_read(REGISTERS['ESP'])
            for slot in IMPORTS:
                if at==dword(self.image,slot-BASE):return self._callback_api(at,sp,slot)
            i=self.callback_code.get(at)
            if i is None or i.size!=n:raise ValueError('callback undeclared original instruction '+hex(at))
            if self.cb_runs and self.cb_runs[-1]['va']==at:self.cb_runs[-1]['count']+=1
            else:self.cb_runs.append(dict(va=at,count=1))
            if i.mnemonic=='ret':self.cb_returns.append(dict(va=hex(at),return_va=hex(self.read(sp)),sp=sp,eax=uc.reg_read(REGISTERS['EAX'])))
            return
        if self.creation_running:
            if at==dword(self.image,CREATE_SLOT-BASE):uc.emu_stop();return
            if at!=CREATE:raise ValueError('creation only original import instruction admitted')
            self.creation_runs.append(dict(va=at,count=1));return
        super()._code(uc,at,n,user)

    def admission(self,previous):
        before=self.cpu();owner=self.bytes(parent.OWNER-4096,parent.BACKING+8192);stack=self.bytes(parent.STACK,65536);image=self.bytes(BASE,len(self.image))
        prior=[dict(pointer=p,**buffer_evidence(self.bytes(p,4096))) for p in sorted(self.foreign)]
        for slot in (CREATE_SLOT,*IMPORTS):
            target=dword(self.image,slot-BASE);page=target&~4095
            if page not in self.foreign:
                if any(a<=page<=b for a,b,p in self.uc.mem_regions()):raise ValueError('callback import map overlap')
                self.uc.mem_map(page,4096);self.foreign[page]=bytearray(4096)
            if self.foreign[page][target-page] not in (0,0xC3):raise ValueError('callback import map conflict')
            self.foreign[page][target-page]=0xC3;self.uc.mem_write(target,b'\xc3')
        for at,size in ((STACK,65536),(RETURN,4096),(SHADOW-4096,12288)):
            if any(a<=at+size-1 and at<=b for a,b,p in self.uc.mem_regions()):raise ValueError('callback declared map overlap')
            self.uc.mem_map(at,size);self.uc.mem_write(at,b'\xda'*size)
        if before!=previous['cpu'] or before!=self.cpu() or owner!=self.bytes(parent.OWNER-4096,len(owner)) or stack!=self.bytes(parent.STACK,len(stack)) or image!=self.bytes(BASE,len(image)):
            raise ValueError('callback admission changed retained native state')
        return dict(slots=[hex(s) for s in (CREATE_SLOT,*IMPORTS)],before_cpu=before,after_cpu=self.cpu(),
            owner_sha256=hashlib.sha256(owner).hexdigest(),stack_sha256=hashlib.sha256(stack).hexdigest(),image_sha256=hashlib.sha256(image).hexdigest(),
            foreign_before=prior,foreign_after=[dict(pointer=p,**buffer_evidence(self.bytes(p,4096))) for p in sorted(self.foreign)],
            declared_maps=[dict(pointer=p,bytes=n,initial_byte=0xDA) for p,n in ((STACK,65536),(RETURN,4096),(SHADOW-4096,12288))])

    def prepare_callback(self,packet):
        if packet['depth']!=1 or packet['guest_entry']!=ENTRY:raise ValueError('bounded callback depth/entry')
        b,args=callback_stack(packet);self.uc.mem_write(STACK,b);self.uc.mem_write(SHADOW-4096,b'\xda'*12288)
        if packet['message']==129:
            raw=bytes.fromhex(packet['data_hex'])
            if len(raw)!=48 or dword(raw,0)!=parent.OWNER or dword(raw,4)!=self.module:raise ValueError('actual creation struct original owner/module')
            self.uc.mem_write(SHADOW,raw)
        for k,v in callback_cpu().items():self.uc.reg_write(REGISTERS[k],v)
        return dict(packet=packet,cpu=self.cpu(),args=args,stack=buffer_evidence(self.bytes(STACK,65536)),
            guarded_shadow=buffer_evidence(self.bytes(SHADOW-4096,12288)),declared_ABI_not_host_register_capture=True)

    def callback(self,packet):
        if self.completed_nc:
            self.pending_callback=self.prepare_callback(packet)
            raise CallbackBoundary(packet,'after original WM_NCCREATE; next callback first instruction unexecuted')
        saved=self.uc.context_save();caller=self.cpu();native_stack=self.bytes(parent.STACK,65536);image=self.bytes(BASE,len(self.image))
        owner_before=self.bytes(parent.OWNER-4096,parent.BACKING+8192);setup=self.prepare_callback(packet)
        self.cb_packet=packet;self.cb_runs,self.cb_calls,self.cb_returns,self.cb_reads,self.cb_writes=[],[],[],[],[];self.callback_running=True
        try:self.uc.emu_start(ENTRY,RETURN+1,timeout=20_000_000,count=100000)
        finally:self.callback_running=False
        cpu=self.cpu()
        if cpu['EIP']!=RETURN or cpu['ESP']!=TOP+20 or any(cpu[k]!=callback_cpu()[k] for k in ('EBP','EBX','ESI','EDI')):raise ValueError('original callback stdcall return/callee-save registers')
        if self.bytes(parent.STACK,65536)!=native_stack or self.bytes(BASE,len(self.image))!=image or self.bytes(0,4096)!=bytes(4096):raise ValueError('callback native caller stack/source/null modified')
        n=dict(setup=setup,suspended_caller_cpu=caller,guarded_owner_before=buffer_evidence(owner_before),
            cpu=cpu,instruction_runs=self.cb_runs,native_returns=self.cb_returns,native_reads=self.cb_reads,native_writes=self.cb_writes,platform_calls=self.cb_calls,
            state=dict(guarded_owner=buffer_evidence(self.bytes(parent.OWNER-4096,parent.BACKING+8192)),callback_stack=buffer_evidence(self.bytes(STACK,65536)),
                guarded_shadow=buffer_evidence(self.bytes(SHADOW-4096,12288)),native_stack=buffer_evidence(native_stack),image_sha256=hashlib.sha256(image).hexdigest()),
            result=cpu['EAX'],original_callback_executed=True)
        self.uc.context_restore(saved);n['restored_caller_cpu']=self.cpu()
        if self.cpu()!=caller:raise ValueError('suspended original caller CPU not restored')
        if packet['message']==129:self.completed_nc=True
        self.completed_callbacks.append(n);return cpu['EAX']

    def enter_creation(self,previous):
        admission=self.admission(previous);self.creation_running=True;self.creation_runs,self.creation_writes=[],[]
        try:self.uc.emu_start(CREATE,parent.RETURN+1,timeout=20_000_000,count=20)
        finally:self.creation_running=False
        cpu=self.cpu();sp=cpu['ESP'];args=[self.read(sp+4+i*4) for i in range(12)]
        if cpu['EIP']!=dword(self.image,CREATE_SLOT-BASE) or self.read(sp)!=0x4504D5 or args!=previous['pending']['stack_args']:raise ValueError('original creation call push/native boundary')
        self.creation=dict(import_admission=admission,cpu=cpu,instruction_runs=self.creation_runs,native_writes=self.creation_writes,
            sp=sp,args=args,return_va='0x4504d5',native_stack=buffer_evidence(self.bytes(parent.STACK,65536)))
        self.platform.callback_handler=self.callback
        try:self.platform.request('create_window',args=args)
        except CallbackBoundary:
            if not self.completed_nc or self.pending_callback is None:raise
        else:raise ValueError('creation must remain pending at callback boundary')


def generate():
    cases=[]
    for fill in (0xA5,0xCC):
        with CallbackPlatform() as p:
            e=CallbackEmulator(p,fill);c=dict(fill=fill,hello=p.hello,system_modules=p.provenance,declared_initial_cpu=initial_cpu(),module_input=e.module_input)
            prior=None
            for phase in parent.STOPS:c[phase]=e.resume(phase,prior);prior=c[phase]
            for phase in ('tasks','query','branch'):c[phase]=e.resume_window(phase,prior);prior=c[phase]
            for phase in geometry.STOPS:c[phase]=e.resume_geometry(phase,prior);prior=c[phase]
            for phase in previous.module.STOPS:c[phase]=e.resume_resources(phase,prior);prior=c[phase]
            for phase in previous.STOPS:c[phase]=e.resume_class(phase,prior);prior=c[phase]
            e.enter_creation(prior)
            c.update(creation=e.creation,callbacks=e.completed_callbacks,pending_callback=e.pending_callback,
                final_guarded_owner=buffer_evidence(e.bytes(parent.OWNER-4096,parent.BACKING+8192)),final_image_sha256=hashlib.sha256(e.bytes(BASE,len(e.image))).hexdigest(),
                platform_trace=p.trace,wire=p.wire,platform_abort=p.abort_proof,platform_cleanup=p.cleanup)
        cases.append(c);print(hex(fill)+': original callbacks '+str([n['setup']['packet']['message'] for n in c['callbacks']])+'; unanswered next '+str(c['pending_callback']['packet']['message']),flush=True)
    return dict(schema_version=1,source_contract=source_contract(),cases=cases,
        platform_build=json.loads((ROOT/'analysis/school-window-callback-platform-v1-20261020.json').read_text(encoding='utf8'))['build'],
        one_original_CPU_per_case=True,original_callback_executed=True,WM_NCCREATE_completed=True,CreateWindowExA_return_received=False,HWND_global_published=False,
        original_IAT_modified=False,game_helpers_stubbed=False,retained_VM_advanced=False,standalone_resumable_checkpoint=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    if out.exists():p.error('fresh immutable actual callback trajectory required')
    out.write_text(json.dumps(generate(),indent=2)+'\n',encoding='utf8',newline='\n')
