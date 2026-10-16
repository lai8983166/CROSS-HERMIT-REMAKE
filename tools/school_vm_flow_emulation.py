"""Original reset/task calls, normal opening commands and complete fixed-point fade."""
import argparse,gzip,hashlib,pickle
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EBP,UC_X86_REG_EAX,UC_X86_REG_ECX
from tools.school_vm_flow import *
from tools.school_vm_draw_emulation import DrawEmulator,ExitEmulator,report_text
from tools.school_world_mode_emulation import architectural_cpu
from tools.school_world_life_codec import pack

RETURNS=(0x425E59,0x4C1F26,0x4C2103,0x56CFF2,0x408124,0x4D03B6,0x454EC1)

class FlowEmulator(DrawEmulator):
    def __init__(self):self.vm_flow_loading=False;super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.vm_flow_loading:return super()._write_hook(uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.vm_flow_allowed):raise RuntimeError('VM flow forbidden write '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.vm_flow_loading:return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
        if address in (self.vm_flow_inputs['ime_target'],self.vm_flow_inputs['strlen_target']):
            args=[self.read(sp+4)]
            if address==self.vm_flow_inputs['ime_target']:
                if self.vm_flow_root!=0x425DE0 or ret!=0x425C99 or args!=[0]:raise RuntimeError('VM flow inherited closed-null-IME response only')
                row=dict(name='ImmGetOpenStatus',slot='0x5920ec',va=hex(address),return_va=hex(ret),sp=sp,args=args,result=0,declared_response=True,live_OS_observed=False)
            else:
                if self.vm_flow_root!=0x454CF0 or ret!=0x425A7E or args!=[INPUT+0x528] or self.read(args[0],'B'):raise RuntimeError('VM flow captured empty string only')
                row=dict(name='lstrlenA',slot='0x5922c4',va=hex(address),return_va=hex(ret),sp=sp,args=args,result=0,read_hex='00',reads_existing_buffer_only=True)
            self.vm_flow_adapters.append(row);self._stub_return(0,4);return
        if address in self.vm_flow_entries:
            n=self.vm_flow_args[address];self.vm_flow_calls.append(dict(va=hex(address),return_va=hex(ret),sp=sp,receiver=recv,args=[self.read(sp+4+i*4) for i in range(n)]))
        if address in RETURNS:self.vm_flow_returns.append(dict(va=hex(address),return_va=hex(ret),sp=sp,eax=uc.reg_read(UC_X86_REG_EAX),ecx=recv))
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        if any(a<=address<b for a,b in self.vm_flow_ranges):self.vm_flow_visited.add(address);return
        raise RuntimeError('VM flow undeclared original instruction '+hex(address))

    def flow_regions(self):return [dict(pointer=a,bytes=n,hex=bytes(self.uc.mem_read(a,n)).hex()) for a,n in REGIONS]

    def flow_cpu(self):
        c=architectural_cpu(self.uc);return {k:c[k] for k in ('EIP','ESP','EBP','EAX','ECX')}

    def run_flow(self,phase):
        if self.flow_cpu()!=dict(EIP=RETURN,ESP=BASE_SP+4,EBP=BASE_SP-4,EAX=0,ECX=0):raise RuntimeError('VM flow verified prior original task return required')
        pointer=self.read(TACT+0x64);texture=self.read(BANK)
        self.vm_flow_inputs=dict(script_pointer=pointer,script_sha256=SCRIPT_SHA,driver='explicit_original_reset_and_selected_task_calls_after_verified_return',texture_record=dict(pointer=texture,bytes=84,hex=bytes(self.uc.mem_read(texture,84)).hex()),ime_target=self.read(0x5920EC),strlen_target=self.read(0x5922C4))
        if self.read(0x7A4A00)!=MAIN or self.read(0x7A49F8)!=WORK or self.read(0x7A49FC)!=TASK or bytes(self.uc.mem_read(pointer,SCRIPT.stat().st_size))!=SCRIPT.read_bytes():raise RuntimeError('VM flow actual owner/import/script capture')
        before=self.flow_regions();self.vm_flow_allowed=[(STACK,STACK+65536)]+[(a,a+n) for a,n in REGIONS];retained=self.capture_scene_memory(self.vm_flow_allowed)
        self.vm_flow_ranges=native_ranges();self.vm_flow_args={int(r['va'],16):r['args'] for r in source_contract()['functions']};self.vm_flow_entries=set(self.vm_flow_args);prior=self._function_ranges;self._function_ranges=prior+self.vm_flow_ranges;self.vm_flow_loading=True;steps=[]
        try:
            current=before
            for index,kind in enumerate(KINDS[phase]):
                expected=project_step(kind,self.vm_flow_inputs,current);self.vm_flow_calls=[];self.vm_flow_returns=[];self.vm_flow_adapters=[];self.vm_flow_visited=set();declarations=[]
                for root,receiver in ((0x425DE0,INPUT),(0x454CF0,TACT)):
                    prior_cpu=self.flow_cpu()
                    if prior_cpu['EIP']!=RETURN or prior_cpu['ESP']!=BASE_SP+4:raise RuntimeError('VM flow completed previous call before declared next invocation')
                    declarations.append(dict(entry=hex(root),receiver=receiver,return_va=hex(RETURN),sp=BASE_SP,previous_CPU=prior_cpu,driver_declared=True,original_outer_callsite_observed=False))
                    self.vm_flow_root=root;self.write(BASE_SP,RETURN);self.uc.reg_write(UC_X86_REG_ESP,BASE_SP);self.uc.reg_write(UC_X86_REG_ECX,receiver);self.uc.emu_start(root,RETURN,timeout=10_000_000,count=100000)
                    if root==0x425DE0:
                        reset_cpu=self.flow_cpu()
                        if reset_cpu!=expected['reset_CPU']:raise RuntimeError('VM flow native reset return CPU')
                after=self.flow_regions();cpu=self.flow_cpu();packet=dict(pointer=layout()['packet'],bytes=128,hex=bytes(self.uc.mem_read(layout()['packet'],128)).hex())
                if after!=expected['after'] or cpu!=expected['CPU'] or packet!=expected['packet']:
                    bad=[(hex(a['pointer']),next((i for i,(x,y) in enumerate(zip(bytes.fromhex(a['hex']),bytes.fromhex(b['hex']))) if x!=y),None)) for a,b in zip(after,expected['after']) if a!=b]
                    raise RuntimeError('VM flow source/native '+phase+'/'+str(index)+' '+kind+' full bytes/CPU/packet '+repr(bad)+' '+repr(cpu))
                steps.append(dict(index=index,**expected,declarations=declarations,calls=self.vm_flow_calls,returns=self.vm_flow_returns,adapters=self.vm_flow_adapters,visited=sorted(self.vm_flow_visited),owned_bodies_stubbed=False,debug_stack_check_adapter=True));current=after
            return dict(phase=phase,inputs=self.vm_flow_inputs,before=before,after=current,steps=steps,declared_task_calls=len(steps),declared_reset_calls=len(steps),live_OS_observed=False,GPU_executed=False,full_outer_frame_executed=False,persistent_write_authority=False,**self.verify_scene_memory(retained))
        finally:self.vm_flow_loading=False;self._function_ranges=prior

    def save_flow(self,name,phase,parent_sha):
        p=ROOT/f'.venv-audit/vm-flow-{phase}-{name}.pkl'
        if p.exists():raise ValueError('VM flow fresh immutable checkpoint required')
        payload=dict(source_sha=SOURCE_SHA256,parent_report_sha=parent_sha,case_name=name,phase=phase,evidence_kind='private_original_vm_flow_'+phase,pending_eip=self.uc.reg_read(UC_X86_REG_EIP),state={k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith(('_audit_','vm_flow_'))},memory=[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()],cpu=self.uc.context_save())
        raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);p.write_bytes(raw);return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pending_eip=hex(RETURN),runtime_or_original_save=False)

def restore(payload):
    e=FlowEmulator();e.__dict__.update(payload['state'])
    for at,buf in payload['memory']:
        if not any(a<=at and at+len(buf)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(buf))
        e.uc.mem_write(at,buf)
    e.uc.context_restore(payload['cpu']);return e

def generate(phases):
    from tools.school_vm_flow_verification import load_verified_checkpoint,PARENT,PARENT_SHA,REPORTS
    from tools.school_vm_draw_verification import load_verified_checkpoint as parent_loader
    names=('initial','student9_waiting','fifth_class');engines={};cps={}
    first=phases[0]
    for name in names:
        payload,cp=parent_loader(name,'task') if first=='branch' else load_verified_checkpoint(name,PREVIOUS[first]);engines[name]=restore(payload);cps[name]=cp
    for phase in phases:
        path=REPORTS[phase]
        if path.exists():raise ValueError('VM flow immutable report already exists')
        rows=[]
        for name in names:
            a=engines[name].run_flow(phase);rows.append(dict(name=name,prior_checkpoint=cps[name],actual=pack(a)));print(name+': native '+phase+' '+str(a['declared_task_calls'])+' task/reset pairs source bytes/CPU verified',flush=True)
        for c in rows:c['continuation_checkpoint']=engines[c['name']].save_flow(c['name'],phase,PARENT_SHA);cps[c['name']]=c['continuation_checkpoint']
        r=dict(schema_version=1,phase=phase,source_contract=source_contract(),parent_report=PARENT.relative_to(ROOT).as_posix(),parent_sha256=PARENT_SHA,cases=rows,live_OS_observed=False,GPU_executed=False,full_outer_frame_executed=False,persistent_write_authority=False)
        path.write_bytes(gzip.compress(report_text(r).encode('utf-8'),compresslevel=6,mtime=0));print('Wrote '+path.name,flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True);g.add_argument('--phase',choices=PHASES);g.add_argument('--all',action='store_true');a=p.parse_args();generate(PHASES if a.all else (a.phase,))
