"""Third declared original-world prefix, first phase1 unit and restored clearing."""
import argparse,hashlib,json,pickle
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP
from tools.school_world_final_emulation import WorldFinalEmulator,UNITCTRL,STACK,RETURN,report_text
from tools.school_world_final_verification import load_verified_checkpoint as load_parent,REPORTS,SHAS
from tools.school_world_second_emulation import WorldSecondEmulator,NATIVE as PREFIX_NATIVE
from tools.school_student_action_emulation import StudentActionEmulator,NATIVE as ANIMATION_NATIVE
from tools.school_world_mode_emulation import architectural_cpu
from tools.school_world_next import *

PARENT=REPORTS['return'];PARENT_SHA=SHAS['return']
NATIVE=PREFIX_NATIVE+ANIMATION_NATIVE+ranges()


class WorldNextEmulator(WorldFinalEmulator):
    def __init__(self):self.next_loading=False;super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.next_loading:return super()._write_hook(uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.next_allowed):raise RuntimeError('next forbidden write '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.next_loading:return super()._hook(uc,address,size,context)
        if self.next_mode=='prefix':return WorldSecondEmulator._hook(self,uc,address,size,context)
        if self.next_mode=='animation':return StudentActionEmulator._hook(self,uc,address,size,context)
        if address in (0x40A100,0x40A800,0x40AB80):
            sp=uc.reg_read(UC_X86_REG_ESP)
            self.next_calls.append(dict(va=hex(address),receiver=uc.reg_read(UC_X86_REG_ECX),return_va=hex(self.read(sp)),sp=sp,args=[self.read(sp+4)]))
        if address==0x56CE80:
            from tools.tactics_exit_emulation import ExitEmulator
            return ExitEmulator._hook(self,uc,address,size,context)
        if any(a<=address<b for a,b in ranges()):self.next_visited.add(address);return
        raise RuntimeError('next release undeclared instruction '+hex(address))

    def run_clearing_probes(self):
        rows=[];cpu=self.uc.context_save();stack=bytes(self.uc.mem_read(STACK,65536));regs=architectural_cpu(self.uc)
        prior=self._function_ranges;self._function_ranges=prior+NATIVE
        self.next_loading=True;self.next_mode='clearing'
        try:
            for i in (217,247,248):
                p=UNITCTRL+0x80AEC+i*STRIDE+0x48;raw=bytes(self.uc.mem_read(p,88));wanted=clearing_project(raw);receiver=self.read(p-4)
                restore=[dict(pointer=p,bytes=88,hex=raw.hex())];retained=self.capture_scene_memory([(STACK,STACK+65536),(p,p+88)])
                self.next_allowed=[(STACK,STACK+65536),(p,p+88)];self.next_calls=[];self.next_visited=set()
                try:
                    result=self.call(0x40A100,[p],receiver=receiver);after=bytes(self.uc.mem_read(p,88))
                    if result!=1 or after!=wanted:raise RuntimeError('next original ended clearing equality')
                    row=dict(index=i,pointer=p,receiver=receiver,before_hex=raw.hex(),after_hex=after.hex(),return_eax=result,calls=self.next_calls,visited=sorted(self.next_visited),**self.verify_scene_memory(retained))
                finally:restoration=self.restore_probe(restore,cpu,stack,regs)
                row['restoration']=restoration;rows.append(row)
            return dict(declared_isolated_calls=True,live_input_captured=False,world_advanced=False,attached_node_free_executed=False,rows=rows)
        finally:self.next_loading=False;self._function_ranges=prior

    def run_prefix(self):
        if self.uc.reg_read(UC_X86_REG_EIP)!=RETURN or self.uc.reg_read(UC_X86_REG_ESP)!=STACK+0xFF00+4:raise RuntimeError('next verified second return CPU')
        before=self.second_regions();inputs=self.second_inputs();expected=prefix_project(inputs,before)
        self.next_allowed=[(STACK,STACK+65536)]+[(r['pointer'],r['pointer']+r['bytes']) for r in before]
        retained=self.capture_scene_memory(self.next_allowed);prior=self._function_ranges;self._function_ranges=prior+NATIVE
        self.next_loading=True;self.next_mode='prefix';self.second_loading=True;self.second_clear_pointer=before[7]['pointer']
        self.second_calls=[];self.second_clears=[];self.second_tested=[];self.second_visited=set();self.second_pending=None
        try:
            self.write(STACK+0xFF00,RETURN);self.uc.reg_write(UC_X86_REG_ESP,STACK+0xFF00);self.uc.reg_write(UC_X86_REG_ECX,UNITCTRL)
            self.uc.emu_start(0x46B470,RETURN,timeout=10_000_000,count=400000)
            after=self.fixed_regions(before)
            if after!=expected['after'] or self.second_pending is None:raise RuntimeError('next entire third prefix equality')
            return dict(inputs=inputs,before=before,**expected,calls=self.second_calls,native_clears=self.second_clears,tested_slots=self.second_tested,visited=sorted(self.second_visited),pending=self.second_pending,
                declared_root=True,third_world_completed=False,VM_or_AI_completed=False,owned_bodies_stubbed=False,**self.verify_scene_memory(retained))
        finally:self.next_loading=False;self.second_loading=False;self._function_ranges=prior

    def run_animation(self):
        if self.uc.reg_read(UC_X86_REG_EIP)!=0x475D60:raise RuntimeError('next verified phase1 CPU')
        before=self.following_regions();inputs=self.inputs();expected=animation_project(inputs,before)
        self.next_allowed=[(STACK,STACK+65536),(UNITCTRL+0x80AEC,UNITCTRL+0x80AEC+STRIDE)]+[(p,p+NODE) for p in expected['linked_order']]
        retained=self.capture_scene_memory(self.next_allowed);prior=self._function_ranges;self._function_ranges=prior+NATIVE
        self.next_loading=True;self.next_mode='animation';self.student_loading=True;self.student_phase='animation'
        self.student_inputs=inputs;self.student_calls=[];self.student_clears=[];self.student_returns=[];self.student_visited=set();self.student_pending=None
        try:
            self.uc.emu_start(0x475D60,RETURN,timeout=5_000_000,count=150000)
            after=self.following_regions()
            if after!=expected['after'] or self.student_pending is None or self.student_clears:raise RuntimeError('next complete phase1 animation equality')
            return dict(inputs=inputs,before=before,**expected,calls=self.student_calls,returns=self.student_returns,visited=sorted(self.student_visited),pending=self.student_pending,
                original_initialization_repeated=False,allocation_executed=False,audio_executed=False,owned_bodies_stubbed=False,**self.verify_scene_memory(retained))
        finally:self.next_loading=False;self.student_loading=False;self._function_ranges=prior

    def save_next(self,name,phase):
        path=ROOT/f'.venv-audit/world-next-{phase}-{name}.pkl'
        if path.exists():raise ValueError('fresh next checkpoint')
        eip=0x475D60 if phase=='prefix' else 0x46B760
        if self.uc.reg_read(UC_X86_REG_EIP)!=eip:raise ValueError('next checkpoint boundary')
        payload=dict(source_sha=SOURCE_SHA256,parent_report_sha=PARENT_SHA,case_name=name,phase=phase,evidence_kind='private_original_world_next_'+phase,pending_eip=eip,
            state={k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith('_audit_')},memory=[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()],cpu=self.uc.context_save())
        raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);path.write_bytes(raw)
        return dict(path=path.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pending_eip=hex(eip),runtime_or_original_save=False)


def restored(name,phase):
    if phase=='prefix':payload,cp=load_parent(name,'return')
    else:
        from tools.school_world_next_verification import load_verified_checkpoint
        payload,cp=load_verified_checkpoint(name,'prefix')
    e=WorldNextEmulator();e.__dict__.update(payload['state'])
    for at,buf in payload['memory']:
        if not any(a<=at and at+len(buf)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(buf))
        e.uc.mem_write(at,buf)
    e.uc.context_restore(payload['cpu']);return e,cp


def report(phase):
    cases=[]
    for name in ('initial','student9_waiting','fifth_class'):
        e,cp=restored(name,phase)
        if phase=='prefix':
            e.next_parent_checkpoint=cp;probes=e.run_clearing_probes();a=e.run_prefix();case=dict(name=name,parent_checkpoint=cp,actual=a,clearing_probes=probes)
        else:
            a=e.run_animation();tail=e.run_tail();case=dict(name=name,parent_checkpoint=e.next_parent_checkpoint,prefix_checkpoint=cp,actual=a,actual_tail=tail,full_after=e.following_regions())
        case['continuation_checkpoint']=e.save_next(name,phase);cases.append(case);print(name+': original next '+phase+' verified',flush=True)
    return dict(schema_version=1,phase=phase,source_contract=source_contract(),parent_report=PARENT.relative_to(ROOT).as_posix(),parent_sha256=PARENT_SHA,cases=cases,
        third_world_completed=False,original_opening_completed=False,persistent_write_authority=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--phase',choices=('prefix','unit'),required=True);p.add_argument('--out',required=True);args=p.parse_args();path=ROOT/args.out
    if path.exists():p.error('fresh immutable report')
    path.write_text(report_text(report(args.phase)),encoding='utf-8',newline='\n')
