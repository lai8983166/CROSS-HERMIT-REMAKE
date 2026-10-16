"""Original captured-input reset and subsequent task polls; stop before normal VM."""
import argparse,gzip,hashlib,json,pickle
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EAX,UC_X86_REG_EBP
from tools.school_task_cycle import *
from tools.school_world_script_emulation import ScriptEmulator,STACK,RETURN,HELPERS,ExitEmulator,report_text
from tools.school_world_mode_emulation import architectural_cpu
from tools.school_world_life_codec import pack

class CycleEmulator(ScriptEmulator):
    def __init__(self):self.cycle_loading=False;super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.cycle_loading:return super()._write_hook(uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.cycle_allowed):raise RuntimeError('task cycle forbidden store '+hex(address))

    def _hook(self,uc,address,size,context):
        if not self.cycle_loading:return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP);ret=self.read(sp);recv=uc.reg_read(UC_X86_REG_ECX)
        if address==0x4CE8F0:
            if self.cycle_phase!='vm_entry':raise RuntimeError('task cycle unexpected playback')
            self.cycle_calls.append(dict(va=hex(address),receiver=recv,return_va=hex(ret),sp=sp));self.cycle_pending=dict(va=hex(address),sp=sp,ebp=uc.reg_read(UC_X86_REG_EBP),eax=uc.reg_read(UC_X86_REG_EAX),ecx=recv,first_instruction_executed=False);uc.emu_stop();return
        if address in (self.cycle_imports['ime_target'],self.cycle_imports['strlen_target']):
            args=[self.read(sp+4)]
            if address==self.cycle_imports['ime_target']:
                if not self.cycle_phase.startswith('reset') or ret!=0x425C99 or args!=[0]:raise RuntimeError('task cycle null-context IME response only')
                self.cycle_adapters.append(dict(name='ImmGetOpenStatus',slot='0x5920ec',va=hex(address),return_va=hex(ret),sp=sp,args=args,result=0,declared_response=True,live_OS_observed=False));self._stub_return(0,4);return
            if ret!=0x425A7E or args!=[INPUT+0x528] or self.read(args[0],'B'):raise RuntimeError('task cycle captured empty text only')
            self.cycle_adapters.append(dict(name='lstrlenA',slot='0x5922c4',va=hex(address),return_va=hex(ret),sp=sp,args=args,result=0,read_hex='00',reads_existing_buffer_only=True));self._stub_return(0,4);return
        if address in {a for a,b in RESET_NATIVE+TASK_NATIVE}|{0x56CEC0}:self.cycle_calls.append(dict(va=hex(address),receiver=recv,return_va=hex(ret),sp=sp))
        if address in (0x425E59,0x454EC1):self.cycle_real_ret=dict(va=hex(address),return_va=hex(ret),sp=sp,eax=uc.reg_read(UC_X86_REG_EAX))
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        if any(a<=address<b for a,b in RESET_NATIVE+TASK_NATIVE+HELPERS):self.cycle_visited.add(address);return
        raise RuntimeError('task cycle undeclared native instruction '+hex(address))

    def regions(self):return [dict(pointer=a,bytes=n,hex=bytes(self.uc.mem_read(a,n)).hex()) for a,n in REGIONS]

    def run_cycle(self,phase):
        base=STACK+0xFF00
        if self.uc.reg_read(UC_X86_REG_EIP)!=RETURN or self.uc.reg_read(UC_X86_REG_ESP)!=base+4:raise RuntimeError('task cycle verified previous return required')
        self.cycle_phase=phase;before=self.regions();expected=project(phase,before)
        self.cycle_imports=dict(ime_target=self.read(0x5920EC),strlen_target=self.read(0x5922C4))
        if self.read(0x7A4A00)!=MAIN or not self.cycle_imports['ime_target'] or not self.cycle_imports['strlen_target']:raise RuntimeError('task cycle captured pointers')
        # Only map a trap page for the captured OS address; preserve the IAT value.
        target=self.cycle_imports['ime_target'];mapped=any(a<=target<=b for a,b,_ in self.uc.mem_regions());self.cycle_adapter_page=None
        if phase.startswith('reset') and not mapped:
            page=target&~4095;self.uc.mem_map(page,4096);self.cycle_adapter_page=dict(pointer=page,bytes=4096,hex=bytes(4096).hex())
        self.cycle_allowed=[(STACK,STACK+65536)]+[(a,a+n) for a,n in REGIONS];retained=self.capture_scene_memory(self.cycle_allowed)
        self.cycle_loading=True;self.cycle_calls=[];self.cycle_adapters=[];self.cycle_visited=set();self.cycle_real_ret=None;self.cycle_pending=None
        prior=self._function_ranges;self._function_ranges=prior+RESET_NATIVE+TASK_NATIVE+HELPERS
        try:
            self.write(base,RETURN);self.uc.reg_write(UC_X86_REG_ESP,base);self.uc.reg_write(UC_X86_REG_ECX,INPUT if phase.startswith('reset') else TACT)
            self.uc.emu_start(0x425DE0 if phase.startswith('reset') else 0x454CF0,RETURN,timeout=10_000_000,count=100000)
            after=self.regions();cpu=architectural_cpu(self.uc)
            if after!=expected['after']:raise RuntimeError('task cycle complete source/native bytes')
            if phase=='vm_entry':
                if self.cycle_pending is None or self.cycle_real_ret is not None:raise RuntimeError('task cycle unexecuted VM admission')
            elif self.cycle_real_ret is None or cpu['EIP']!=RETURN or cpu['ESP']!=base+4 or cpu['EAX']!=0:raise RuntimeError('task cycle natural original return')
            return dict(phase=phase,before=before,**expected,imports=self.cycle_imports,adapter_page_added=self.cycle_adapter_page,calls=self.cycle_calls,adapters=self.cycle_adapters,visited=sorted(self.cycle_visited),real_ret=self.cycle_real_ret,pending=self.cycle_pending,CPU={k:cpu[k] for k in ('EIP','ESP','EBP','EAX','ECX')},owned_bodies_stubbed=False,original_outer_task_frame_completed=False,**self.verify_scene_memory(retained))
        finally:self.cycle_loading=False;self._function_ranges=prior

    def save_cycle(self,name,phase,parent_sha):
        p=ROOT/f'.venv-audit/task-cycle-{phase}-{name}.pkl'
        if p.exists():raise ValueError('task cycle immutable new checkpoint')
        payload=dict(source_sha=SOURCE_SHA256,parent_report_sha=parent_sha,case_name=name,phase=phase,evidence_kind='private_original_task_cycle_'+phase,pending_eip=self.uc.reg_read(UC_X86_REG_EIP),state={k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith('_audit_')},memory=[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()],cpu=self.uc.context_save())
        raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);p.write_bytes(raw);return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pending_eip=hex(payload['pending_eip']),runtime_or_original_save=False)


def report(phase):
    from tools.school_task_cycle_verification import load_verified_checkpoint,PARENT,PARENT_SHA
    cases=[]
    for name in ('initial','student9_waiting','fifth_class'):
        if phase=='reset1':
            from tools.school_world_script_verification import load_verified_checkpoint as parent_loader
            payload,cp=parent_loader(name,'task')
        else:payload,cp=load_verified_checkpoint(name,PREVIOUS[phase])
        e=CycleEmulator();e.__dict__.update(payload['state'])
        for at,buf in payload['memory']:
            if not any(a<=at and at+len(buf)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(buf))
            e.uc.mem_write(at,buf)
        e.uc.context_restore(payload['cpu']);a=e.run_cycle(phase);cases.append(dict(name=name,prior_checkpoint=cp,actual=pack(a),continuation_checkpoint=e.save_cycle(name,phase,PARENT_SHA)));print(name+': native '+phase+' verified',flush=True)
    return dict(schema_version=1,phase=phase,source_contract=source_contract(),parent_report=PARENT.relative_to(ROOT).as_posix(),parent_sha256=PARENT_SHA,cases=cases,normal_VM_executed=False,live_input_sampled=False,full_outer_frame_executed=False,persistent_write_authority=False)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--phase',choices=PHASES,required=True);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable path required')
    path.write_bytes(gzip.compress(report_text(report(a.phase)).encode('utf-8'),compresslevel=6,mtime=0))
