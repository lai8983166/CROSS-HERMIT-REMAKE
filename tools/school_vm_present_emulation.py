"""Continue original normal VM, native overlay constructor and resource binding."""
import argparse,gzip,hashlib,pickle,struct
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX
from tools.school_vm_present import *
from tools.school_task_cycle_emulation import CycleEmulator,ExitEmulator,report_text
from tools.school_world_mode_emulation import architectural_cpu
from tools.school_world_life_codec import pack

class PresentEmulator(CycleEmulator):
    def __init__(self):self.present_loading=False;super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.present_loading:return super()._write_hook(uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.present_allowed):raise RuntimeError('VM present forbidden write '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.present_loading:return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
        if address in self.present_entries or address==self.present_stop:
            n=self.present_args.get(address,2 if address==0x407AD0 else 0);c=dict(va=hex(address),receiver=recv,return_va=hex(ret),sp=sp,args=[self.read(sp+4+i*4) for i in range(n)]);self.present_calls.append(c)
            if address==self.present_stop:
                self.present_pending=dict(**c,ebp=uc.reg_read(UC_X86_REG_EBP),eax=uc.reg_read(UC_X86_REG_EAX),first_instruction_executed=False);uc.emu_stop();return
        if address==0x4CE9C5:
            pointer=self.read(VM+0x10)+self.read(VM+0x1C);op,n=struct.unpack('<HH',uc.mem_read(pointer,4));self.present_commands.append(dict(offset=pointer-self.present_inputs['script_pointer'],opcode=op,advance=n))
        if address in (0x496DE6,0x41F667,0x4142DC):self.present_returns.append(dict(va=hex(address),return_va=hex(ret),sp=sp,eax=uc.reg_read(UC_X86_REG_EAX)))
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        if any(a<=address<b for a,b in NATIVE):self.present_visited.add(address);return
        raise RuntimeError('VM present undeclared native instruction '+hex(address))

    def present_regions(self):return [dict(pointer=a,bytes=n,hex=bytes(self.uc.mem_read(a,n)).hex()) for a,n in REGIONS]

    def run_present(self,phase):
        start={'command':0x4CE8F0,'packet':0x4D29E0,'draw':0x407870}[phase];stop={'command':0x4D29E0,'packet':0x407870,'draw':0x407AD0}[phase];l=layout()
        if self.uc.reg_read(UC_X86_REG_EIP)!=start or self.uc.reg_read(UC_X86_REG_ESP)!=l[{'command':'vm','packet':'overlay','draw':'resource'}[phase]]:raise RuntimeError('VM present original pending CPU required')
        pointer=self.read(TACT+0x64);script=SCRIPT.read_bytes()
        if bytes(self.uc.mem_read(pointer,len(script)))!=script:raise ValueError('VM present complete original script bytes')
        self.present_inputs=dict(script_pointer=pointer,script_sha256=SCRIPT_SHA,driver='continuous_original_task_VM',texture_record=dict(pointer=self.read(BANK),bytes=84,hex=bytes(self.uc.mem_read(self.read(BANK),84)).hex()));before=self.present_regions();expected=project(phase,self.present_inputs,before)
        packet_before=None if phase!='draw' else dict(pointer=l['packet'],bytes=128,hex=bytes(self.uc.mem_read(l['packet'],128)).hex())
        self.present_allowed=[(STACK,STACK+65536)]+[(a,a+n) for a,n in REGIONS];retained=self.capture_scene_memory(self.present_allowed)
        self.present_args={int(x['va'],16):x['args'] for x in source_contract()['functions']};self.present_entries=set(self.present_args);self.present_stop=stop;self.present_calls=[];self.present_returns=[];self.present_commands=[];self.present_pending=None;self.present_visited=set();self.present_loading=True;prior=self._function_ranges;self._function_ranges=prior+NATIVE
        try:
            self.uc.emu_start(start,RETURN,timeout=10_000_000,count=100000);after=self.present_regions();cpu=architectural_cpu(self.uc)
            packet=None if phase=='command' else dict(pointer=l['packet'],bytes=128,hex=bytes(self.uc.mem_read(l['packet'],128)).hex())
            if after!=expected['after'] or packet!=expected['packet'] or self.present_pending!=expected['pending']:raise RuntimeError('VM present entire source/native state, packet and pending CPU '+repr(self.present_pending))
            seh=None if phase=='command' else bytes(self.uc.mem_read(l['seh'],12)).hex()
            return dict(phase=phase,inputs=self.present_inputs,before=before,**expected,packet_before=packet_before,seh_record=seh,calls=self.present_calls,returns=self.present_returns,commands=self.present_commands,visited=sorted(self.present_visited),CPU={k:cpu[k] for k in ('EIP','ESP','EBP','EAX','ECX')},owned_bodies_stubbed=False,platform_adapters=[],debug_stack_check_adapter=True,original_outer_task_frame_completed=False,**self.verify_scene_memory(retained))
        finally:self.present_loading=False;self._function_ranges=prior

    def save_present(self,name,phase,parent_sha):
        p=ROOT/f'.venv-audit/vm-present-{phase}-{name}.pkl'
        if p.exists():raise ValueError('VM present fresh immutable checkpoint')
        payload=dict(source_sha=SOURCE_SHA256,parent_report_sha=parent_sha,case_name=name,phase=phase,evidence_kind='private_original_vm_present_'+phase,pending_eip=self.uc.reg_read(UC_X86_REG_EIP),state={k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith('_audit_')},memory=[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()],cpu=self.uc.context_save())
        raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);p.write_bytes(raw);return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pending_eip=hex(payload['pending_eip']),runtime_or_original_save=False)


def report(phase):
    from tools.school_vm_present_verification import load_verified_checkpoint,PARENT,PARENT_SHA
    cases=[]
    for name in ('initial','student9_waiting','fifth_class'):
        if phase=='command':
            from tools.school_task_cycle_verification import load_verified_checkpoint as parent_loader
            payload,cp=parent_loader(name,'vm_entry')
        else:payload,cp=load_verified_checkpoint(name,PREVIOUS[phase])
        e=PresentEmulator();e.__dict__.update(payload['state'])
        for at,buf in payload['memory']:
            if not any(a<=at and at+len(buf)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(buf))
            e.uc.mem_write(at,buf)
        e.uc.context_restore(payload['cpu']);a=e.run_present(phase);cases.append(dict(name=name,prior_checkpoint=cp,actual=pack(a),continuation_checkpoint=e.save_present(name,phase,PARENT_SHA)));print(name+': native '+phase+' full bytes/CPU verified',flush=True)
    return dict(schema_version=1,phase=phase,source_contract=source_contract(),parent_report=PARENT.relative_to(ROOT).as_posix(),parent_sha256=PARENT_SHA,cases=cases,normal_first_opcode_executed=True,VM_returned=False,full_outer_frame_executed=False,live_rendering=False,persistent_write_authority=False)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--phase',choices=PHASES,required=True);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable evidence path required')
    path.write_bytes(gzip.compress(report_text(report(a.phase)).encode('utf-8'),compresslevel=6,mtime=0))
