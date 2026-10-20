"""Original startup with observed fresh inputs and nested callbacks outside emu_start."""
import argparse
import hashlib
import json
import struct
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_READ
from tools.school_window_events import *
from tools.school_window_callback_emulation import CallbackEmulator,REGISTERS,initial_cpu,buffer_evidence
from tools.school_window_events_platform import EventsPlatform
from tools.school_startup_inputs import verify_observation

HELPER=ROOT/'.venv-audit/school-window-startup-platform-v1.exe'
PLATFORM_SOURCE=ROOT/'tools/school_window_startup_platform.cs'
INPUT_REPORT='analysis/school-startup-inputs-v2-20261020.json'
INPUTS={0x7A49FC:0,0x80A398:0}
GLOBAL_HWND=0x7A0BB4


class StartupEmulator(CallbackEmulator):
    def __init__(self,p,fill):
        self.publishing=False;self.frames=[];self.records=[];self.initial_reads=[];self.prefix_instruction_count=0
        super().__init__(p,fill)
        if p.initial_globals!=INPUTS or self.cpu()!=initial_cpu():raise ValueError('observed inputs must precede original root')
        self.input_declaration=dict(before_first_original_instruction=True,cpu=self.cpu(),globals={hex(at):self.read(at) for at in INPUTS},
            image_sha256=hashlib.sha256(self.bytes(BASE,len(self.image))).hexdigest(),prefix_instruction_count=0)
        self.uc.hook_add(UC_HOOK_MEM_READ,self._read_inputs)
        self.pub_code={i.address:i for a,b in ((0x4504D5,0x4504E1),(0x56CE80,0x56CE83)) for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(self.image[a-BASE:b-BASE],a)}

    def _read_inputs(self,uc,access,at,n,value,user):
        if any(at<=p<at+n for p in INPUTS):
            self.initial_reads.append(dict(pc=uc.reg_read(REGISTERS['EIP']),pointer=at,bytes=n,hex=self.bytes(at,n).hex(),callback_id=self.frames[-1] if self.frames else None))

    def _write(self,uc,access,at,n,value,user):
        if self.publishing:
            if not (parent.STACK<=at and at+n<=parent.STACK+65536 or at==GLOBAL_HWND and n==4):raise ValueError('publication unowned write')
            self.pub_writes.append(dict(pc=uc.reg_read(REGISTERS['EIP']),pointer=at,bytes=n,value=value));return
        if self.callback_running:
            if not (STACK<=at and at+n<=STACK+65536 or parent.OWNER<=at and at+n<=parent.OWNER+parent.SIZE):raise ValueError('callback unowned write')
            self.cb_writes.append(dict(pc=uc.reg_read(REGISTERS['EIP']),pointer=at,bytes=n,value=value&((1<<(n*8))-1)));return
        super()._write(uc,access,at,n,value,user)

    def _code(self,uc,at,n,user):
        if self.callback_running:
            for slot in IMPORTS:
                if at==dword(self.image,slot-BASE):
                    self.pending_native=(at,uc.reg_read(REGISTERS['ESP']),slot);uc.emu_stop();return
            return super()._code(uc,at,n,user)
        if self.publishing:
            if at==0x4504E1:uc.emu_stop();return
            i=self.pub_code.get(at)
            if i is None or i.size!=n:raise ValueError('undeclared publication instruction')
            self.pub_runs.append(dict(va=at,count=1));return
        self.prefix_instruction_count+=1
        return super()._code(uc,at,n,user)

    def prepare_callback(self,packet):
        if packet['depth']!=len(self.frames) or packet['guest_entry']!=ENTRY or not 1<=packet['depth']<=8:raise ValueError('actual bounded nested callback depth')
        b,args=callback_stack(packet);self.uc.mem_write(STACK,b);self.uc.mem_write(SHADOW-4096,b'\xda'*12288)
        if packet['message']==129:
            raw=bytes.fromhex(packet['data_hex'])
            if len(raw)!=48 or dword(raw,0)!=parent.OWNER or dword(raw,4)!=self.module:raise ValueError('actual creation owner/module')
            self.uc.mem_write(SHADOW,raw)
        for k,v in callback_cpu().items():self.uc.reg_write(REGISTERS[k],v)
        return dict(packet=packet,cpu=self.cpu(),args=args,stack=buffer_evidence(self.bytes(STACK,65536)),guarded_shadow=buffer_evidence(self.bytes(SHADOW-4096,12288)),declared_ABI_not_host_register_capture=True)

    def callback(self,packet):
        if packet['callback_id']!=len(self.records)+1 or len(self.records)>=128:raise ValueError('bounded actual callback sequence')
        if packet['message'] in (70,71):windowpos(bytes.fromhex(packet['data_hex']),packet['hwnd'])
        saved=self.uc.context_save();caller=self.cpu();outer=bool(self.frames);stack=self.bytes(STACK,65536);shadow=self.bytes(SHADOW-4096,12288)
        fields=('cb_packet','cb_runs','cb_calls','cb_returns','cb_reads','cb_writes','pending_native')
        prior={k:getattr(self,k,None) for k in fields};parent_id=self.frames[-1] if self.frames else None;self.frames.append(packet['callback_id'])
        owner=self.bytes(parent.OWNER-4096,parent.BACKING+8192);native=self.bytes(parent.STACK,65536);image=self.bytes(BASE,len(self.image))
        setup=self.prepare_callback(packet);node=dict(setup=setup,parent_callback_id=parent_id,suspended_caller_cpu=caller,guarded_owner_before=buffer_evidence(owner));self.records.append(node)
        self.cb_packet=packet;self.cb_runs,self.cb_calls,self.cb_returns,self.cb_reads,self.cb_writes=[],[],[],[],[];self.callback_running=True
        try:
            while True:
                self.pending_native=None;self.uc.emu_start(self.cpu()['EIP'],RETURN+1,timeout=20_000_000,count=100000)
                if self.pending_native is None:break
                request=self.pending_native;old=len(self.records)
                self._callback_api(*request)
                self.cb_calls[-1]['nested_callback_ids']=[r['setup']['packet']['callback_id'] for r in self.records[old:]]
            cpu=self.cpu()
            if cpu['EIP']!=RETURN or cpu['ESP']!=TOP+20 or any(cpu[k]!=callback_cpu()[k] for k in ('EBP','EBX','ESI','EDI')):raise ValueError('callback original stdcall/callee-saved return')
            if self.bytes(BASE,len(image))!=image or self.bytes(parent.STACK,65536)!=native:raise ValueError('callback original source/native stack preservation')
            node.update(cpu=cpu,instruction_runs=self.cb_runs,native_returns=self.cb_returns,native_reads=self.cb_reads,native_writes=self.cb_writes,platform_calls=self.cb_calls,
                state=dict(guarded_owner=buffer_evidence(self.bytes(parent.OWNER-4096,len(owner))),callback_stack=buffer_evidence(self.bytes(STACK,65536)),guarded_shadow=buffer_evidence(self.bytes(SHADOW-4096,12288)),native_stack=buffer_evidence(native),image_sha256=hashlib.sha256(image).hexdigest()),result=cpu['EAX'],original_callback_executed=True)
        finally:
            self.callback_running=outer;self.frames.pop()
        self.uc.context_restore(saved)
        if outer:self.uc.mem_write(STACK,stack);self.uc.mem_write(SHADOW-4096,shadow)
        for k,v in prior.items():setattr(self,k,v)
        node['restored_caller_cpu']=self.cpu();node['outer_guest_buffers_restored']=not outer or self.bytes(STACK,65536)==stack and self.bytes(SHADOW-4096,12288)==shadow
        if self.cpu()!=caller or not node['outer_guest_buffers_restored']:raise ValueError('nested original caller restoration')
        return cpu['EAX']

    def enter_creation(self,previous):
        admission=self.admission(previous);self.creation_running=True;self.creation_runs,self.creation_writes=[],[]
        try:self.uc.emu_start(CREATE,parent.RETURN+1,timeout=20_000_000,count=20)
        finally:self.creation_running=False
        cpu=self.cpu();sp=cpu['ESP'];args=[self.read(sp+4+i*4) for i in range(12)]
        if cpu['EIP']!=dword(self.image,CREATE_SLOT-BASE) or self.read(sp)!=0x4504D5 or args!=previous['pending']['stack_args']:raise ValueError('original creation call frame')
        self.creation=dict(import_admission=admission,cpu=cpu,instruction_runs=self.creation_runs,native_writes=self.creation_writes,sp=sp,args=args,return_va='0x4504d5',native_stack=buffer_evidence(self.bytes(parent.STACK,65536)))
        self.platform.callback_handler=self.callback
        r=self.platform.request('create_window',args=args)
        if not r['original_creation_returned'] or r['result']!=self.records[0]['setup']['packet']['hwnd'] or r['callback_calls']!=len(self.records):raise ValueError('actual original native creation return')
        self.creation_result=r;self._return(sp,r['result'],12)
        before=self.cpu();self.pub_runs,self.pub_writes=[],[];self.publishing=True
        try:self.uc.emu_start(before['EIP'],parent.RETURN+1,count=1000,timeout=20_000_000)
        finally:self.publishing=False
        if self.cpu()['EIP']!=0x4504E1 or self.read(GLOBAL_HWND)!=r['result']:raise ValueError('original HWND publication not reached')
        self.publication=dict(before_cpu=before,cpu=self.cpu(),instruction_runs=self.pub_runs,native_writes=self.pub_writes,hwnd=self.read(GLOBAL_HWND),
            state=dict(image_sha256=hashlib.sha256(self.bytes(BASE,len(self.image))).hexdigest(),guarded_owner=buffer_evidence(self.bytes(parent.OWNER-4096,parent.BACKING+8192)),native_stack=buffer_evidence(self.bytes(parent.STACK,65536))))


def generate():
    inputs=json.loads((ROOT/INPUT_REPORT).read_text(encoding='utf8'));assert len(inputs['cases'])==2
    cases=[]
    for fill,observed in zip((0xA5,0xCC),inputs['cases']):
        with EventsPlatform(helper=HELPER) as p:
            p.initial_globals=verify_observation(observed);e=StartupEmulator(p,fill)
            c=dict(fill=fill,hello=p.hello,system_modules=p.provenance,declared_initial_cpu=initial_cpu(),module_input=e.module_input,initial_input_declaration=e.input_declaration)
            prior=None
            for phase in parent.STOPS:c[phase]=e.resume(phase,prior);prior=c[phase]
            for phase in ('tasks','query','branch'):c[phase]=e.resume_window(phase,prior);prior=c[phase]
            for phase in geometry.STOPS:c[phase]=e.resume_geometry(phase,prior);prior=c[phase]
            for phase in base.callback.previous.module.STOPS:c[phase]=e.resume_resources(phase,prior);prior=c[phase]
            for phase in base.callback.previous.STOPS:c[phase]=e.resume_class(phase,prior);prior=c[phase]
            e.enter_creation(prior)
            c.update(creation=e.creation,creation_result=e.creation_result,callbacks=e.records,hwnd_publication=e.publication,declared_input_reads=e.initial_reads,
                final_guarded_owner=buffer_evidence(e.bytes(parent.OWNER-4096,parent.BACKING+8192)),final_image_sha256=hashlib.sha256(e.bytes(BASE,len(e.image))).hexdigest(),platform_trace=p.trace,wire=p.wire)
            p._terminate()
            c['lifetime']=dict(owned_process_exited=p.process.poll() is not None,exit_code=p.process.returncode,CreateWindowExA_return_received=True,explicit_normal_cleanup=False,pending_native_callback=False,resources_ended_with_owned_process=True,standalone_resumable_checkpoint=False)
        cases.append(c);print(hex(fill)+': actual creation returned and HWND published; callback messages/depth '+str([(n['setup']['packet']['message'],n['setup']['packet']['depth']) for n in c['callbacks']]),flush=True)
    return dict(schema_version=1,source_image_sha256=SOURCE_SHA256,initial_inputs=INPUT_REPORT,initial_globals={hex(at):v for at,v in INPUTS.items()},cases=cases,
        original_game_code_modified=False,original_IAT_modified=False,retained_VM_advanced=False,full_WinMain_executed=False,normal_cleanup_completed=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    if out.exists():p.error('fresh startup trajectory required')
    out.write_text(json.dumps(generate(),indent=2)+'\n',encoding='utf8',newline='\n')
