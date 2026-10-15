"""Complete original worlds127–181, pending mode and terminal idle pose."""
import argparse,gzip,hashlib,pickle
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EAX
from tools.school_world_third_emulation import WorldThirdEmulator,WorldFinalEmulator,NATIVE as PRIOR_NATIVE,CALL_ARGS as PRIOR_CALLS,UNITCTRL,STACK,RETURN,report_text
from tools.school_world_handoff_verification import load_verified_checkpoint as load_parent,REPORTS,SHAS
from tools.school_world_second_emulation import WorldSecondEmulator,NATIVE as PREFIX_NATIVE,ROOT_RETURNS
from tools.school_world_idle import *
from tools.school_world_life_codec import pack
from tools.school_world_countdown import audio_ranges
from tools.tactics_exit_emulation import TASK

PARENT=REPORTS['handoff'];PARENT_SHA=SHAS['handoff']
PHASES={'commit':range(127,129),'handoff':range(129,134),'wait':range(134,182)}
PREVIOUS={'handoff':'commit','wait':'handoff'}
NATIVE=PRIOR_NATIVE+audio_ranges()+lifecycle_ranges()+spawn_ranges()+handoff_ranges()+idle_ranges()
EXTRA_ARGS={0x40A520:1,0x415070:1,0x409FB0:2,0x40B990:2,0x40D390:4,0x40AB80:1,0x40B660:1,0x40B6A0:1,0x40ADA0:2,0x40B5E0:0,0x409EF0:1,0x40A400:3,0x409F70:2,0x4214F0:2,0x56CEC0:3,0x49AD90:2,0x46A4C0:1,0x468E10:1,0x467E70:0,0x570FE0:0,0x5753B0:0,0x475270:2,0x4756A0:1,0x46BEB0:6,0x40AD20:1,0x40AC90:1,0x437D90:2,0x437D10:1}


PREFIX_AUDIT_POINTS=set(ROOT_RETURNS)|{0x475D60,0x46B470,0x415070,0x43D270,0x427DE0,0x468D10,0x56CEC0,0x56CE80}
AUDIT_POINTS=set(PRIOR_CALLS)|set(EXTRA_ARGS)|{0x490FC0,0x46B760,0x468D10,0x4757A3,0x475BDD,0x475B0A,0x475A42,0x4757B7,0x46B7E1,0x46B80C,0x46B85B,0x46BA07,0x475C55,0x56CE80,0x40ADCB,0x40AF2D,0x467E92,0x49B01C,0x475734}


class IdleEmulator(WorldThirdEmulator):
    def __init__(self):self.count_loading=False;super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.count_loading:return super()._write_hook(uc,access,address,size,value,context)
        if self.count_mode=='suffix':return WorldFinalEmulator._write_hook(self,uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.count_allowed):raise RuntimeError('countdown forbidden write '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.count_loading:return super()._hook(uc,address,size,context)
        if self.count_mode=='suffix':return WorldFinalEmulator._hook(self,uc,address,size,context)
        if self.count_mode=='prefix':
            if address==0x46B760:
                sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp);args=[self.read(sp+4),self.read(sp+8)]
                if (recv,ret,sp,args)!=(UNITCTRL,0x46B584,STACK+0xFF00-100,[UNITCTRL+0x80AEC,0]):raise RuntimeError('countdown natural first unit entry')
                self.second_pending=dict(va=hex(address),receiver=recv,return_va=hex(ret),sp=sp,args=args,first_instruction_executed=False);uc.emu_stop();return
            if address not in PREFIX_AUDIT_POINTS and any(a<=address<b for a,b in PREFIX_NATIVE):self.second_visited.add(address);return
            return WorldSecondEmulator._hook(self,uc,address,size,context)
        if address in (0x40ADCB,0x40AF2D):
            self.spawn_returns.append(dict(index=self.third_entries[-1],kind='allocation' if address==0x40ADCB else 'immediate',va=hex(address),sp=uc.reg_read(UC_X86_REG_ESP),eax=uc.reg_read(UC_X86_REG_EAX)))
        if address in EXTRA_ARGS and address not in PRIOR_CALLS:
            sp=uc.reg_read(UC_X86_REG_ESP);self.third_calls.append(dict(va=hex(address),receiver=uc.reg_read(UC_X86_REG_ECX),return_va=hex(self.read(sp)),sp=sp,args=[self.read(sp+4+n*4) for n in range(EXTRA_ARGS[address])]))
        if address==0x475734:
            self.mode_returns.append(dict(index=self.third_entries[-1],va=hex(address),sp=uc.reg_read(UC_X86_REG_ESP),eax=uc.reg_read(UC_X86_REG_EAX)))
        if address==0x49AD90:self.voice_active=True
        if address==0x49B01C:self.voice_active=False
        if self.voice_active and address==0x468D10 and self.read(uc.reg_read(UC_X86_REG_ESP)) in (0x46A4E9,0x46A459,0x468E39):
            sp=uc.reg_read(UC_X86_REG_ESP);self.third_calls.append(dict(va=hex(address),receiver=uc.reg_read(UC_X86_REG_ECX),return_va=hex(self.read(sp)),sp=sp,args=[self.read(sp+4)]))
        if address==0x467E92:
            self.random_returns.append(dict(index=self.third_entries[-1],va=hex(address),sp=uc.reg_read(UC_X86_REG_ESP),eax=uc.reg_read(UC_X86_REG_EAX),seed=self.read(TLS+20)))
        if address==0x5753B0:
            sp=uc.reg_read(UC_X86_REG_ESP)
            if self.read(sp)!=0x570FE9:raise RuntimeError('handoff exact CRT adapter caller')
            self.thread_adapters.append(dict(return_va=hex(self.read(sp)),sp=sp,thread_pointer=TLS,does_not_reseed=True))
            self.third_visited.add(address);self._stub_return(TLS,0);return
        if address==0x40D4A6:raise RuntimeError('unexecuted audio backend boundary')
        if any(a<=address<b for a,b in audio_ranges()+lifecycle_ranges()[1:]+spawn_ranges()[:1]):self.third_visited.add(address);return
        # Common instructions require only visited-address evidence; preserve every
        # original call/return/slot/guard audit point before avoiding register reads.
        if address not in AUDIT_POINTS and any(a<=address<b for a,b in NATIVE):self.third_visited.add(address);return
        if any(a<=address<b for a,b in handoff_ranges()):self.third_visited.add(address);return
        if any(a<=address<b for a,b in idle_ranges()) and address not in PRIOR_CALLS:self.third_visited.add(address);return
        return WorldThirdEmulator._hook(self,uc,address,size,context)

    def following_regions(self):
        rows=super().following_regions();rows.append(dict(name='crt_thread',pointer=TLS,bytes=4096,hex=bytes(self.uc.mem_read(TLS,4096)).hex()));return rows

    def idle_inputs(self):
        inputs=self.remaining_inputs();first=self.inputs();inputs['units'].insert(0,dict(index=0,record_pointer=first['record_pointer'],record_hex=first['record_hex'],bindings=first['metadata_bindings']))
        inputs['path_manager_pointer']=UNITCTRL+0x2A634;inputs['path_manager_hex']=bytes(self.uc.mem_read(UNITCTRL+0x2A634,100)).hex();inputs['audio_manager_pointer']=TASK+0x1A98;inputs['audio_manager_hex']=bytes(self.uc.mem_read(TASK+0x1A98,20)).hex();return inputs

    def run_prefix(self,tick):
        if self.uc.reg_read(UC_X86_REG_EIP)!=RETURN or self.uc.reg_read(UC_X86_REG_ESP)!=STACK+0xFF00+4:raise RuntimeError('countdown verified preceding return')
        before=self.second_regions();inputs=self.second_inputs();expected=prefix_project(inputs,before,tick)
        self.count_allowed=[(STACK,STACK+65536)]+[(r['pointer'],r['pointer']+r['bytes']) for r in before];retained=self.capture_scene_memory(self.count_allowed)
        prior=self._function_ranges;self._function_ranges=prior+NATIVE;self.count_loading=True;self.count_mode='prefix';self.second_loading=True;self.second_clear_pointer=before[7]['pointer']
        self.second_calls=[];self.second_clears=[];self.second_tested=[];self.second_visited=set();self.second_pending=None
        try:
            self.write(STACK+0xFF00,RETURN);self.uc.reg_write(UC_X86_REG_ESP,STACK+0xFF00);self.uc.reg_write(UC_X86_REG_ECX,UNITCTRL)
            self.uc.emu_start(0x46B470,RETURN,timeout=10_000_000,count=500000)
            if self.fixed_regions(before)!=expected['after'] or self.second_pending is None:raise RuntimeError('countdown complete source prefix')
            return dict(tick=tick,inputs=inputs,before=before,**expected,calls=self.second_calls,native_clears=self.second_clears,tested_slots=self.second_tested,pending=self.second_pending,visited=sorted(self.second_visited),declared_root=True,owned_bodies_stubbed=False,**self.verify_scene_memory(retained))
        finally:self.count_loading=False;self.second_loading=False;self._function_ranges=prior

    def run_units(self,tick):
        before=self.following_regions();inputs=self.idle_inputs();expected=units_project(inputs,before,tick);tail_before=self.tail_regions()
        self.third_indices=expected['unit_indices'];self.count_allowed=[(STACK,STACK+65536),(0x7A49E0,0x7A49E4)]+[(UNITCTRL+0x80AEC+i*STRIDE,UNITCTRL+0x80AEC+(i+1)*STRIDE) for i in self.third_indices]
        self.count_allowed += [(p,p+NODE) for u in expected['units'] for p in u.get('linked_order',[])+u.get('allocated_nodes',[])+u.get('released_nodes',[])]+[(r['pointer'],r['pointer']+r['bytes']) for r in before[2:5]]+[(TLS+20,TLS+24)]
        retained=self.capture_scene_memory(self.count_allowed);prior=self._function_ranges;self._function_ranges=prior+NATIVE;self.count_loading=True;self.count_mode='units';self.third_loading=True;self.third_mode='units'
        self.third_calls=[];self.third_entries=[];self.third_tests=[];self.third_returns=[];self.third_visited=set();self.third_pending=None;self.spawn_returns=[];self.random_returns=[];self.thread_adapters=[];self.voice_active=False;self.mode_returns=[]
        try:
            self.uc.emu_start(0x46B760,RETURN,timeout=15_000_000,count=1000000);after=self.following_regions()
            if after!=expected['after']:
                diff=[]
                for a,b in zip(after,expected['after']):
                    aa,bb=bytes.fromhex(a['hex']),bytes.fromhex(b['hex']);diff.extend((a['name'],hex(a['pointer']+i),x,y) for i,(x,y) in enumerate(zip(aa,bb)) if x!=y)
                raise RuntimeError('countdown complete units source/native '+repr(diff[:24]))
            if self.tail_regions()!=tail_before or self.third_entries!=self.third_indices or self.third_tests!=list(range(1,250)) or self.third_pending is None:raise RuntimeError('countdown natural full250 loop')
            return dict(tick=tick,inputs=inputs,before=before,**expected,tail_before=tail_before,tail_after=self.tail_regions(),calls=self.third_calls,returns=self.third_returns,spawn_returns=self.spawn_returns,mode_returns=self.mode_returns,random_returns=self.random_returns,thread_adapters=self.thread_adapters,CRT_rand_executed=bool(self.random_returns),spawn_opcode_executed=any(c['va']=='0x40ada0' for c in self.third_calls),unit_entries=self.third_entries,tested_slots=self.third_tests,pending=self.third_pending,visited=sorted(self.third_visited),owned_bodies_stubbed=False,audio_backend_executed=False,attached_node_free_executed=any(c['va']=='0x40b6a0' for c in self.third_calls),repeat_opcode_executed=0x40AA71 in self.third_visited,**self.verify_scene_memory(retained))
        finally:self.count_loading=False;self.third_loading=False;self._function_ranges=prior

    def run_suffix(self,tick):
        wanted=suffix_project(self.tail_inputs(),self.tail_regions(),tick);self.count_loading=True;self.count_mode='suffix'
        try:
            a=WorldFinalEmulator.run_phase(self,'return');a['world_body_completed']=a.pop('second_46B470_body_completed');a['tick']=tick
            if a['tail_after']!=wanted:raise RuntimeError('countdown exact source idle counter suffix')
            return a
        finally:self.count_loading=False

    def run_world(self,tick):return dict(tick=tick,prefix=self.run_prefix(tick),units=self.run_units(tick),suffix=self.run_suffix(tick))

    def save_idle(self,name,phase):
        path=ROOT/f'.venv-audit/world-idle-{phase}-{name}.pkl'
        if path.exists():raise ValueError('fresh countdown checkpoint')
        payload=dict(source_sha=SOURCE_SHA256,parent_report_sha=PARENT_SHA,case_name=name,phase=phase,evidence_kind='private_original_world_idle_'+phase,pending_eip=RETURN,
            state={k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith('_audit_')},memory=[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()],cpu=self.uc.context_save())
        raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);path.write_bytes(raw)
        return dict(path=path.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pending_eip=hex(RETURN),runtime_or_original_save=False)


def restored(name,phase):
    if phase=='commit':payload,cp=load_parent(name,'handoff')
    else:
        from tools.school_world_idle_verification import load_verified_checkpoint
        payload,cp=load_verified_checkpoint(name,PREVIOUS[phase])
    e=IdleEmulator();e.__dict__.update(payload['state'])
    for at,buf in payload['memory']:
        if not any(a<=at and at+len(buf)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(buf))
        e.uc.mem_write(at,buf)
    e.uc.context_restore(payload['cpu']);return e,cp


def report(phase):
    cases=[]
    for name in ('initial','student9_waiting','fifth_class'):
        e,cp=restored(name,phase)
        if phase=='commit':e.idle_parent_checkpoint=cp
        worlds=[]
        for tick in PHASES[phase]:
            worlds.append(pack(e.run_world(tick)));print(name+': complete original world '+str(tick)+' full bytes verified',flush=True)
        c=dict(name=name,parent_checkpoint=e.idle_parent_checkpoint,worlds=worlds,continuation_checkpoint=e.save_idle(name,phase))
        if phase!='commit':c['prior_checkpoint']=cp
        cases.append(c)
    return dict(schema_version=2,encoding='full-hex-zlib-v1',phase=phase,source_contract=source_contract(),parent_report=PARENT.relative_to(ROOT).as_posix(),parent_sha256=PARENT_SHA,cases=cases,original_outer_task_frame_completed=False,original_opening_completed=False,audio_backend_executed=False,persistent_write_authority=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--phase',choices=tuple(PHASES),required=True);p.add_argument('--out',required=True);args=p.parse_args();path=ROOT/args.out
    if path.exists():p.error('fresh immutable report')
    path.write_bytes(gzip.compress(report_text(report(args.phase)).encode('utf-8'),compresslevel=6,mtime=0))
