"""Resume the original draw request through native cleanup, maintenance and task return."""
import argparse,gzip,hashlib,pickle,struct
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX,UC_X86_REG_ECX
from tools.school_vm_draw import *
from tools.school_vm_present_emulation import PresentEmulator,ExitEmulator,report_text
from tools.school_world_mode_emulation import architectural_cpu
from tools.school_world_life_codec import pack

class DrawEmulator(PresentEmulator):
    def __init__(self):self.draw_loading=False;super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.draw_loading:return super()._write_hook(uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.draw_allowed):raise RuntimeError('VM draw forbidden write '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.draw_loading:return super()._hook(uc,address,size,context)
        if address==self.draw_stop:uc.emu_stop();return
        sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX)
        if address in self.draw_entries:
            n=self.draw_args[address];self.draw_calls.append(dict(va=hex(address),return_va=hex(self.read(sp)),sp=sp,receiver=recv,args=[self.read(sp+4+i*4) for i in range(n)]))
        if address in (0x408124,0x4D2B83,0x4D03B6,0x454EC1):self.draw_returns.append(dict(va=hex(address),sp=sp,return_va=hex(self.read(sp)),eax=uc.reg_read(UC_X86_REG_EAX),ecx=recv))
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        if any(a<=address<b for a,b in self.draw_ranges):self.draw_visited.add(address);return
        raise RuntimeError('VM draw undeclared native instruction '+hex(address))

    def draw_regions(self):return [dict(pointer=a,bytes=n,hex=bytes(self.uc.mem_read(a,n)).hex()) for a,n in REGIONS]

    def run_draw(self,phase):
        start=START[phase];stop=STOP[phase];cpu=architectural_cpu(self.uc)
        wanted=dict(EIP=start,ESP=layout()['draw'],EBP=layout()['drawbp'],EAX=layout()['packet'],ECX=layout()['packet']) if phase=='cleanup' else cpu_expected(PREVIOUS[phase])
        if {k:cpu[k] for k in wanted}!=wanted:raise RuntimeError('VM draw actual original continuation CPU required')
        pointer=self.read(TACT+0x64);texture=self.read(BANK)
        inputs=dict(script_pointer=pointer,script_sha256=SCRIPT_SHA,driver='continuous_original_task_VM',texture_record=dict(pointer=texture,bytes=84,hex=bytes(self.uc.mem_read(texture,84)).hex()))
        before=self.draw_regions();expected=project(phase,inputs,before)
        if phase=='cleanup' and bytes(self.uc.mem_read(layout()['packet'],128)).hex()!=expected['packet']['hex']:raise RuntimeError('VM draw original parent packet required')
        self.draw_allowed=[(STACK,STACK+65536)]+[(a,a+n) for a,n in REGIONS];retained=self.capture_scene_memory(self.draw_allowed)
        self.draw_args={int(r['va'],16):r['args'] for r in source_contract()['functions']};self.draw_entries=set(self.draw_args);self.draw_stop=stop;self.draw_calls=[];self.draw_returns=[];self.draw_visited=set();self.draw_ranges=native_ranges();prior=self._function_ranges;self._function_ranges=prior+self.draw_ranges;self.draw_loading=True
        try:
            self.uc.emu_start(start,RETURN,timeout=10_000_000,count=100000);after=self.draw_regions();cpu=architectural_cpu(self.uc);cpu={k:cpu[k] for k in ('EIP','ESP','EBP','EAX','ECX')}
            packet=dict(pointer=layout()['packet'],bytes=128,hex=bytes(self.uc.mem_read(layout()['packet'],128)).hex()) if phase=='cleanup' else None
            if after!=expected['after'] or cpu!=expected['CPU'] or packet!=expected['packet']:raise RuntimeError('VM draw source/native full state/CPU/packet '+repr(cpu)+' expected '+repr(expected['CPU']))
            return dict(phase=phase,inputs=inputs,before=before,**expected,calls=self.draw_calls,returns=self.draw_returns,visited=sorted(self.draw_visited),owned_bodies_stubbed=False,platform_adapters=[],debug_stack_check_adapter=True,**self.verify_scene_memory(retained))
        finally:self.draw_loading=False;self._function_ranges=prior

    def save_draw(self,name,phase,parent_sha):
        p=ROOT/f'.venv-audit/vm-draw-{phase}-{name}.pkl'
        if p.exists():raise ValueError('VM draw fresh immutable checkpoint required')
        payload=dict(source_sha=SOURCE_SHA256,parent_report_sha=parent_sha,case_name=name,phase=phase,evidence_kind='private_original_vm_draw_'+phase,pending_eip=self.uc.reg_read(UC_X86_REG_EIP),state={k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith('_audit_')},memory=[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()],cpu=self.uc.context_save())
        raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);p.write_bytes(raw);return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pending_eip=hex(payload['pending_eip']),runtime_or_original_save=False)

def report(phase):
    from tools.school_vm_draw_verification import load_verified_checkpoint,PARENT,PARENT_SHA
    from tools.school_vm_present_verification import load_verified_checkpoint as parent_loader
    cases=[]
    for name in ('initial','student9_waiting','fifth_class'):
        payload,cp=parent_loader(name,'draw') if phase=='cleanup' else load_verified_checkpoint(name,PREVIOUS[phase])
        e=DrawEmulator();e.__dict__.update(payload['state'])
        for at,buf in payload['memory']:
            if not any(a<=at and at+len(buf)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(buf))
            e.uc.mem_write(at,buf)
        e.uc.context_restore(payload['cpu']);a=e.run_draw(phase);cases.append(dict(name=name,prior_checkpoint=cp,actual=pack(a),continuation_checkpoint=e.save_draw(name,phase,PARENT_SHA)));print(name+': native '+phase+' full bytes/CPU verified',flush=True)
    return dict(schema_version=1,phase=phase,source_contract=source_contract(),parent_report=PARENT.relative_to(ROOT).as_posix(),parent_sha256=PARENT_SHA,cases=cases,VM_returned=phase!='cleanup',selected_task_returned=phase=='task',GPU_executed=False,full_outer_frame_executed=False,persistent_write_authority=False)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--phase',choices=PHASES,required=True);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable evidence path required')
    path.write_bytes(gzip.compress(report_text(report(a.phase)).encode('utf-8'),compresslevel=6,mtime=0))
