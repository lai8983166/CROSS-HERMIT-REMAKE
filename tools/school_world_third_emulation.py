"""Original third world remaining units, complete loop and natural return."""
import argparse,hashlib,pickle
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EAX
from tools.school_world_next_emulation import WorldNextEmulator,UNITCTRL,STACK,RETURN,report_text
from tools.school_world_next_verification import load_verified_checkpoint as load_parent,REPORTS,SHAS
from tools.school_world_final_emulation import WorldFinalEmulator,NATIVE as FINAL_NATIVE,CALL_ARGS as PRIOR_CALLS,ExitEmulator
from tools.school_world_next import ranges as next_ranges
from tools.school_world_third import *

PARENT=REPORTS['unit'];PARENT_SHA=SHAS['unit']
NATIVE=FINAL_NATIVE+next_ranges()+ranges()
CALL_ARGS={**PRIOR_CALLS,0x479F40:1,0x40AB80:1}


class WorldThirdEmulator(WorldNextEmulator):
    def __init__(self):self.third_loading=False;super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.third_loading:return super()._write_hook(uc,access,address,size,value,context)
        if self.third_mode=='return':return WorldFinalEmulator._write_hook(self,uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.third_allowed):raise RuntimeError('third forbidden write '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.third_loading:return super()._hook(uc,address,size,context)
        if self.third_mode=='return':return WorldFinalEmulator._hook(self,uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
        if address==0x490FC0:
            if (recv,ret,sp)!=(UNITCTRL,0x46B620,STACK+0xFF00-92):raise RuntimeError('third original suffix stack')
            self.third_pending=dict(va=hex(address),receiver=recv,return_va=hex(ret),sp=sp,args=[],first_instruction_executed=False);uc.emu_stop();return
        if address==0x46B760:
            i=self.read(sp+8)
            if i not in self.third_indices or self.third_entries!=self.third_indices[:self.third_indices.index(i)] or (recv,ret,sp,self.read(sp+4))!=(UNITCTRL,0x46B584,STACK+0xFF00-100,UNITCTRL+0x80AEC+i*STRIDE):raise RuntimeError('third original remaining unit order/stack')
            self.third_entries.append(i)
        if address in CALL_ARGS:self.third_calls.append(dict(va=hex(address),receiver=recv,return_va=hex(ret),sp=sp,args=[self.read(sp+4+n*4) for n in range(CALL_ARGS[address])]))
        if address==0x468D10 and ret==0x46B560:self.third_tests.append((self.read(sp+4)-UNITCTRL-0x80AEC)//STRIDE)
        if address in (0x4757A3,0x475BDD,0x475B0A,0x475A42,0x4757B7,0x46B7E1,0x46B80C,0x46B85B,0x46BA07) or (address==0x475C55 and self.third_entries[-1] not in INACTIVE):
            self.third_returns.append(dict(index=self.third_entries[-1],va=hex(address),sp=sp,eax=uc.reg_read(UC_X86_REG_EAX)))
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        if any(a<=address<b for a,b in NATIVE):self.third_visited.add(address);return
        raise RuntimeError('third undeclared original instruction '+hex(address))

    def remaining_inputs(self):
        before=self.following_regions();friends=self.following_inputs();scene=self.inputs217();last=self.inputs240();active={x['index']:x for x in friends['units']}
        active[217]=dict(index=217,record_pointer=scene['record_pointer'],record_hex=scene['record_hex'],bindings=[scene['main_binding']])
        active.update({x['index']:{**{k:v for k,v in x.items() if k!='binding'},'bindings':[x['binding']]} for x in last['units']});units=[]
        for i in range(1,250):
            w=UNITCTRL+0x80AEC+i*STRIDE
            if not self.read(w,'h'):continue
            rp=self.read(w+0x258);units.append(active.get(i,dict(index=i,record_pointer=rp,record_hex=bytes(self.uc.mem_read(rp,176)).hex(),bindings=[])))
        return dict(units=units,team=scene['team'],relation_matrix_hex=scene['relation_matrix_hex'],map_sha256=scene['map_sha256'],map_all_bytes_verified=scene['map_all_bytes_verified'],effect_controller=scene['effect_controller'])

    def run_units(self):
        if self.uc.reg_read(UC_X86_REG_EIP)!=0x46B760 or self.read(self.uc.reg_read(UC_X86_REG_ESP)+8)!=1:raise RuntimeError('third verifiedslot1 entry')
        before=self.following_regions();inputs=self.remaining_inputs();expected=project(inputs,before);tail_before=self.tail_regions()
        self.third_indices=expected['unit_indices'];self.third_allowed=[(STACK,STACK+65536),(0x7A49E0,0x7A49E4)]+[(UNITCTRL+0x80AEC+i*STRIDE,UNITCTRL+0x80AEC+(i+1)*STRIDE) for i in self.third_indices]
        self.third_allowed += [(p,p+NODE) for u in expected['units'] for p in u.get('linked_order',[])]+[(r['pointer'],r['pointer']+r['bytes']) for r in before[2:5]]
        retained=self.capture_scene_memory(self.third_allowed);prior=self._function_ranges;self._function_ranges=prior+NATIVE
        self.third_loading=True;self.third_mode='units';self.third_calls=[];self.third_entries=[];self.third_tests=[];self.third_returns=[];self.third_visited=set();self.third_pending=None
        try:
            self.uc.emu_start(0x46B760,RETURN,timeout=15_000_000,count=900000);after=self.following_regions()
            if after!=expected['after']:
                diff=[]
                for a,b in zip(after,expected['after']):
                    aa,bb=bytes.fromhex(a['hex']),bytes.fromhex(b['hex']);diff.extend((a['name'],hex(a['pointer']+j),x,y) for j,(x,y) in enumerate(zip(aa,bb)) if x!=y)
                raise RuntimeError('third entire source/native bytes '+repr(diff[:24]))
            if self.tail_regions()!=tail_before or self.third_entries!=self.third_indices or self.third_tests!=list(range(2,250)) or self.third_pending is None:raise RuntimeError('third complete loop/tail boundary')
            return dict(inputs=inputs,before=before,**expected,tail_before=tail_before,tail_after=self.tail_regions(),tail_inputs=self.tail_inputs(),calls=self.third_calls,returns=self.third_returns,unit_entries=self.third_entries,tested_slots=self.third_tests,pending=self.third_pending,visited=sorted(self.third_visited),
                owned_bodies_stubbed=False,audio_executed=False,attached_node_free_executed=False,VM_or_AI_completed=False,**self.verify_scene_memory(retained))
        finally:self.third_loading=False;self._function_ranges=prior

    def run_return(self):
        self.third_loading=True;self.third_mode='return'
        try:
            a=WorldFinalEmulator.run_phase(self,'return');a['third_46B470_body_completed']=a.pop('second_46B470_body_completed');return a
        finally:self.third_loading=False

    def save_third(self,name,phase):
        path=ROOT/f'.venv-audit/world-third-{phase}-{name}.pkl'
        if path.exists():raise ValueError('fresh third checkpoint')
        eip=0x490FC0 if phase=='units' else RETURN
        if self.uc.reg_read(UC_X86_REG_EIP)!=eip:raise ValueError('third exact checkpoint EIP')
        payload=dict(source_sha=SOURCE_SHA256,parent_report_sha=PARENT_SHA,case_name=name,phase=phase,evidence_kind='private_original_world_third_'+phase,pending_eip=eip,
            state={k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith('_audit_')},memory=[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()],cpu=self.uc.context_save())
        raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);path.write_bytes(raw)
        return dict(path=path.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pending_eip=hex(eip),runtime_or_original_save=False)


def restored(name,phase):
    if phase=='units':payload,cp=load_parent(name,'unit')
    else:
        from tools.school_world_third_verification import load_verified_checkpoint
        payload,cp=load_verified_checkpoint(name,'units')
    e=WorldThirdEmulator();e.__dict__.update(payload['state'])
    for at,buf in payload['memory']:
        if not any(a<=at and at+len(buf)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(buf))
        e.uc.mem_write(at,buf)
    e.uc.context_restore(payload['cpu']);return e,cp


def report(phase):
    cases=[]
    for name in ('initial','student9_waiting','fifth_class'):
        e,cp=restored(name,phase)
        if phase=='units':e.third_parent_checkpoint=cp
        a=e.run_units() if phase=='units' else e.run_return();c=dict(name=name,parent_checkpoint=e.third_parent_checkpoint,actual=a,continuation_checkpoint=e.save_third(name,phase))
        if phase=='return':c['units_checkpoint']=cp
        cases.append(c);print(name+': original third '+phase+' verified',flush=True)
    return dict(schema_version=1,phase=phase,source_contract=source_contract(),parent_report=PARENT.relative_to(ROOT).as_posix(),parent_sha256=PARENT_SHA,cases=cases,
        third_46B470_body_completed=phase=='return',original_outer_task_frame_completed=False,original_opening_completed=False,persistent_write_authority=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--phase',choices=('units','return'),required=True);p.add_argument('--out',required=True);args=p.parse_args();path=ROOT/args.out
    if path.exists():p.error('fresh immutable report')
    path.write_text(report_text(report(args.phase)),encoding='utf-8',newline='\n')
