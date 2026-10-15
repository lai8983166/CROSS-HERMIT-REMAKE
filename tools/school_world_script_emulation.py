"""Continuous original184 preflight/binding and paused184/185 execution."""
import argparse,gzip,hashlib,json,pickle,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EAX,UC_X86_REG_EBP
from tools.school_world_resume_emulation import ResumeEmulator,UNITCTRL,STACK,RETURN,WorldSecondEmulator,WorldCommandEmulator,WorldFinalEmulator,PREFIX_NATIVE,NATIVE as WORLD_NATIVE,report_text
from tools.school_world_resume_verification import load_verified_checkpoint as load_parent,REPORTS as PARENT_REPORTS,SHAS as PARENT_SHAS
from tools.school_script_preflight_emulation import NATIVE as PREFLIGHT_NATIVE
from tools.school_world_script import *
from tools.tactics_exit_emulation import ExitEmulator
from tools.school_world_life_codec import pack
from tools.school_world_mode_emulation import architectural_cpu

PARENT=PARENT_REPORTS['entry'];PARENT_SHA=PARENT_SHAS['entry']
PHASES=('preflight','binding','world184','world185')
PREVIOUS={'binding':'preflight','world184':'binding','world185':'world184'}
SCRIPT_NATIVE=PREFLIGHT_NATIVE+HELPERS
NATIVE=WORLD_NATIVE+HELPERS
ENTRIES={a for a,b in SCRIPT_NATIVE}-{0x49A0D4,0x49A146,0x49A2B3}


class ScriptEmulator(ResumeEmulator):
    def __init__(self):self.script_loading=False;super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.script_loading:return super()._write_hook(uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.script_allowed):raise RuntimeError('world script forbidden store '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.script_loading:
            if getattr(self,'script_world_prefix',False):
                if address==0x454C40:
                    sp=uc.reg_read(UC_X86_REG_ESP);self.status_calls.append(dict(va=hex(address),receiver=uc.reg_read(UC_X86_REG_ECX),return_va=hex(self.read(sp)),sp=sp,args=[]))
                if address==0x49A167:self.status_result=uc.reg_read(UC_X86_REG_EAX)
                if 0x454C40<=address<0x454C7A:self.second_visited.add(address);return
            return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
        if address==self.script_stop:
            self.script_pending=dict(va=hex(address),sp=sp,ebp=uc.reg_read(UC_X86_REG_EBP),eax=uc.reg_read(UC_X86_REG_EAX),ecx=recv,first_instruction_executed=False);uc.emu_stop();return
        if address==0x4549D0:self.script_binding_observation=dict(receiver=recv,return_va=hex(ret),sp=sp,args=[self.read(sp+4+i*4) for i in range(7)])
        if address in ENTRIES:self.script_calls.append(dict(va=hex(address),receiver=recv,return_va=hex(ret),sp=sp))
        if address in (0x4CE8F0,):
            at=self.read(VM+0x10)+self.read(VM+0x1C);op,advance=struct.unpack('<2H',uc.mem_read(at,4));self.script_commands.append(dict(offset=at-self.script_inputs['script_pointer'],opcode=op,advance=advance))
        if address in (self.script_inputs['strcmp_import'],self.script_inputs['tick_import']):
            args=[] if address==self.script_inputs['tick_import'] else [self.read(sp+4),self.read(sp+8)]
            if address==self.script_inputs['strcmp_import']:
                if ret!=0x45521C or args!=[self.script_inputs['script_pointer']+432,0x59A60C]:raise RuntimeError('world script exact strcmp adapter')
                for i in range(256):
                    left,right=self.read(args[0]+i,'B'),self.read(args[1]+i,'B')
                    if left!=right or not left:break
                else:raise RuntimeError('world script terminated source strings')
                result=(left-right)&0xFFFFFFFF;pop=8
            else:
                if ret!=0x45528D:raise RuntimeError('world script unused tick adapter caller')
                result=0;pop=0
            self.script_adapters.append(dict(va=hex(address),receiver=recv,return_va=hex(ret),sp=sp,args=args,result=result));self._stub_return(result,pop);return
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        if any(a<=address<b for a,b in SCRIPT_NATIVE):self.script_visited.add(address);return
        raise RuntimeError('world script undeclared native instruction '+hex(address))

    def script_regions(self):return [dict(pointer=a,bytes=n,hex=bytes(self.uc.mem_read(a,n)).hex()) for a,n in SCRIPT_REGIONS]

    def preflight_inputs(self):
        pointer=self.read(TACT+0x64);raw=SCRIPT.read_bytes()
        if bytes(self.uc.mem_read(pointer,len(raw)))!=raw or hashlib.sha256(raw).hexdigest()!=SCRIPT_SHA:raise ValueError('world script full source bytes')
        return dict(script_pointer=pointer,script_sha256=SCRIPT_SHA,selector=0,sub=1,strcmp_import=self.read(0x592278),tick_import=self.read(0x592210),main_owner=self.read(0x7A4A00),tick_value=0,driver='continuous_original_world184_preflight')

    def run_script(self,phase):
        start,stop=(0x4551C0,0x49A0D4) if phase=='preflight' else (0x49A0D4,0x49A0F4)
        if self.uc.reg_read(UC_X86_REG_EIP)!=start:raise RuntimeError('world script exact pending CPU')
        before=self.script_regions();self.script_inputs=self.preflight_inputs();expected=(preflight_project if phase=='preflight' else binding_project)(self.script_inputs,before)
        self.script_allowed=[(STACK,STACK+65536)]+[(r['pointer'],r['pointer']+r['bytes']) for r in before]
        retained=self.capture_scene_memory(self.script_allowed);prior=self._function_ranges;self._function_ranges=prior+SCRIPT_NATIVE
        self.script_binding_observation=None;self.script_loading=True;self.script_stop=stop;self.script_pending=None;self.script_calls=[];self.script_adapters=[];self.script_commands=[];self.script_visited=set()
        try:
            self.uc.emu_start(start,RETURN,timeout=10_000_000,count=500000);after=self.script_regions()
            if after!=expected['after']:
                diffs=[]
                for a,b in zip(after,expected['after']):
                    aa,bb=bytes.fromhex(a['hex']),bytes.fromhex(b['hex']);diffs.extend((hex(a['pointer']+i),x,y) for i,(x,y) in enumerate(zip(aa,bb)) if x!=y)
                raise RuntimeError('world script entire source/native bytes '+repr(diffs[:24]))
            if self.script_pending is None or (phase=='preflight' and self.script_commands!=expected['commands']):raise RuntimeError('world script natural return/commands')
            return dict(**(dict(binding_observation=self.script_binding_observation) if phase=='binding' else {}),phase=phase,inputs=self.script_inputs,before=before,**expected,calls=self.script_calls,adapters=self.script_adapters,pending=self.script_pending,visited=sorted(self.script_visited),owned_bodies_stubbed=False,debug_stack_check_is_declared_adapter=True,audio_backend_executed=False,**self.verify_scene_memory(retained))
        finally:self.script_loading=False;self._function_ranges=prior

    def save_script(self,name,phase):
        p=ROOT/f'.venv-audit/world-script-{phase}-{name}.pkl'
        if p.exists():raise ValueError('fresh immutable world script checkpoint')
        payload=dict(source_sha=SOURCE_SHA256,parent_report_sha=PARENT_SHA,case_name=name,phase=phase,evidence_kind='private_original_world_script_'+phase,pending_eip=self.uc.reg_read(UC_X86_REG_EIP),state={k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith('_audit_')},memory=[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()],cpu=self.uc.context_save())
        raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);p.write_bytes(raw)
        return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pending_eip=hex(payload['pending_eip']),runtime_or_original_save=False)


    def run_prefix(self,tick):
        if self.uc.reg_read(UC_X86_REG_EIP)!=(0x49A0F4 if tick==184 else RETURN) or self.uc.reg_read(UC_X86_REG_ESP)!=STACK+0xFF00+(-200 if tick==184 else 4):raise RuntimeError('countdown verified preceding return')
        before=self.second_regions();inputs=self.second_inputs();expected=prefix_project(inputs,before,tick)
        self.count_allowed=[(STACK,STACK+65536)]+[(r['pointer'],r['pointer']+r['bytes']) for r in before];retained=self.capture_scene_memory(self.count_allowed)
        prior=self._function_ranges;self._function_ranges=prior+NATIVE;self.count_loading=True;self.count_mode='prefix';self.second_loading=True;self.second_clear_pointer=before[7]['pointer']
        self.second_calls=[];self.second_clears=[];self.second_tested=[];self.second_visited=set();self.second_pending=None;self.status_calls=[];self.status_result=None;self.script_world_prefix=True
        try:
            if tick==185:self.write(STACK+0xFF00,RETURN);self.uc.reg_write(UC_X86_REG_ESP,STACK+0xFF00);self.uc.reg_write(UC_X86_REG_ECX,UNITCTRL)
            self.uc.emu_start(0x49A0F4 if tick==184 else 0x46B470,RETURN,timeout=10_000_000,count=500000)
            if self.fixed_regions(before)!=expected['after'] or self.second_pending is None:raise RuntimeError('countdown complete source prefix')
            return dict(tick=tick,inputs=inputs,before=before,**expected,calls=self.second_calls,native_clears=self.second_clears,tested_slots=self.second_tested,pending=self.second_pending,visited=sorted(self.second_visited),declared_root=tick==185,status_calls=self.status_calls,status_result=self.status_result,owned_bodies_stubbed=False,**self.verify_scene_memory(retained))
        finally:self.script_world_prefix=False;self.count_loading=False;self.second_loading=False;self._function_ranges=prior

    def run_paused(self,tick):
        before=self.following_regions();inputs=self.idle_inputs();expected=units_project(inputs,before,tick);tail_before=self.tail_regions()
        self.count_allowed=[(STACK,STACK+65536),(0x7A49E0,0x7A49E4)]+[(r['pointer'],r['pointer']+r['bytes']) for r in before[3:5]]
        for u in expected['units']:
            if not u['inactive']:
                w=UNITCTRL+0x80AEC+u['index']*STRIDE;self.count_allowed.append((w+0x4E7,w+0x4EB))
        retained=self.capture_scene_memory(self.count_allowed);prior=self._function_ranges;self._function_ranges=prior+NATIVE
        self.count_loading=True;self.count_mode='paused';self.command_loading=True;self.command_kind='actual'
        self.command_calls=[];self.command_tested=[];self.command_units=[];self.command_vision=[];self.command_cells=[];self.command_clears=[];self.command_visited=set();self.command_pending=None;self.paused_calls=[]
        try:
            self.uc.emu_start(0x46B760,RETURN,timeout=10_000_000,count=500000)
            if self.following_regions()!=expected['after'] or self.tail_regions()!=tail_before or self.command_tested!=list(range(1,250)) or self.command_units!=expected['unit_indices'] or self.command_pending is None or self.command_cells:raise RuntimeError('resume entire paused loop source equality')
            return dict(tick=tick,inputs=inputs,before=before,**expected,tail_before=tail_before,tail_after=self.tail_regions(),calls=self.paused_calls,unit_entries=self.command_units,tested_slots=self.command_tested,vision_calls=self.command_vision,pending=self.command_pending,visited=sorted(self.command_visited),owned_bodies_stubbed=False,**self.verify_scene_memory(retained))
        finally:self.count_loading=False;self.command_loading=False;self._function_ranges=prior

    def run_suffix(self,tick):
        before=self.following_regions();tail_before=self.tail_regions();inputs=self.tail_inputs();wanted=suffix_project(inputs,tail_before,tick)
        self.world_final_allowed=self.allowed();retained=self.capture_scene_memory(self.world_final_allowed);caller_bp=self.read(self.uc.reg_read(UC_X86_REG_EBP));prior=self._function_ranges;self._function_ranges=prior+NATIVE
        self.count_loading=True;self.count_mode='suffix';self.world_final_loading=True;self.world_final_phase='return';self.world_final_calls=[];self.world_final_visited=set();self.world_final_effects=[];self.world_final_effect_returns=[];self.world_final_real_ret=None
        try:
            self.uc.emu_start(0x490FC0,RETURN,timeout=10_000_000,count=500000);cpu=architectural_cpu(self.uc)
            if self.following_regions()!=before or self.tail_regions()!=wanted or cpu['EIP']!=RETURN or cpu['ESP']!=STACK+0xFF00+4 or cpu['EBP']!=caller_bp or cpu['EAX']!=0 or self.world_final_effect_returns!=[1]*10 or self.world_final_real_ret is None:raise RuntimeError('resume entire natural suffix/CPU')
            return dict(tick=tick,inputs=inputs,before=before,after=self.following_regions(),tail_before=tail_before,tail_after=self.tail_regions(),calls=self.world_final_calls,visited=sorted(self.world_final_visited),effect_calls=self.world_final_effects,effect_returns=self.world_final_effect_returns,real_ret=self.world_final_real_ret,driver_return=dict(va=hex(RETURN),sp=cpu['ESP'],ebp=cpu['EBP'],expected_caller_ebp=caller_bp,eax=cpu['EAX'],declared_audit_sentinel=True),world_body_completed=True,original_outer_task_frame_completed=False,original_opening_completed=False,VM_or_AI_completed=False,owned_bodies_stubbed=False,**self.verify_scene_memory(retained))
        finally:self.count_loading=False;self.world_final_loading=False;self._function_ranges=prior

    def run_world(self,tick):return dict(tick=tick,prefix=self.run_prefix(tick),units=self.run_paused(tick),suffix=self.run_suffix(tick))


def restored(name,phase):
    if phase=='preflight':payload,cp=load_parent(name,'entry')
    else:
        from tools.school_world_script_verification import load_verified_checkpoint
        payload,cp=load_verified_checkpoint(name,PREVIOUS[phase])
    e=ScriptEmulator();e.__dict__.update(payload['state'])
    for at,buf in payload['memory']:
        if not any(a<=at and at+len(buf)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(buf))
        e.uc.mem_write(at,buf)
    e.uc.context_restore(payload['cpu']);return e,cp


def report(phase):
    cases=[]
    for name in ('initial','student9_waiting','fifth_class'):
        e,cp=restored(name,phase)
        if phase=='preflight':e.script_parent_checkpoint=cp
        a=e.run_script(phase) if phase in ('preflight','binding') else e.run_world(184 if phase=='world184' else 185);c=dict(name=name,parent_checkpoint=e.script_parent_checkpoint,actual=pack(a),continuation_checkpoint=e.save_script(name,phase))
        if phase!='preflight':c['prior_checkpoint']=cp
        cases.append(c);print(name+': original '+phase+' full bytes/CPU verified',flush=True)
    return dict(schema_version=2,encoding='full-hex-zlib-v1',phase=phase,source_contract=source_contract(),parent_report=PARENT.relative_to(ROOT).as_posix(),parent_sha256=PARENT_SHA,cases=cases,original_outer_task_frame_completed=False,playback_vm_executed=False,persistent_write_authority=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--phase',choices=PHASES,required=True);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable evidence path required')
    path.write_bytes(gzip.compress(report_text(report(a.phase)).encode('utf-8'),compresslevel=6,mtime=0))
