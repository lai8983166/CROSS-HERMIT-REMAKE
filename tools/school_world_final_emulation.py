"""Original remaining ten units and actual second46B470 suffix/return."""
import argparse,hashlib,pickle
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EAX,UC_X86_REG_EBP
from tools.school_scene_templates_emulation import SceneTemplatesEmulator,NATIVE as PRIOR_NATIVE,UNITCTRL,STACK,RETURN,ExitEmulator,report_text
from tools.school_scene_templates_verification import load_verified_checkpoint as load_parent,REPORT as PARENT,REPORT_SHA as PARENT_SHA
from tools.school_scene_first_emulation import CALL_ARGS as UNIT_CALLS,MAPCTRL
from tools.school_world_tail_emulation import NATIVE as TAIL_NATIVE,ROOTS
from tools.school_world_mode_emulation import architectural_cpu
from tools.school_world_final import *

NATIVE=PRIOR_NATIVE+TAIL_NATIVE+ranges()
CALL_ARGS={**UNIT_CALLS,0x476250:1,0x4DDBB0:1}


class WorldFinalEmulator(SceneTemplatesEmulator):
    def __init__(self):self.world_final_loading=False;super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.world_final_loading:return super()._write_hook(uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.world_final_allowed):raise RuntimeError('world final forbidden write '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.world_final_loading:return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
        if self.world_final_phase=='units':
            if address==0x490FC0:
                if (recv,ret,sp)!=(UNITCTRL,0x46B620,STACK+0xFF00-92):raise RuntimeError('world final natural suffix entry')
                self.world_final_pending={'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'args':[],'first_instruction_executed':False};uc.emu_stop();return
            if address==0x46B760:
                i=self.read(sp+8)
                if i not in INDICES or self.world_final_entries!=INDICES[:i-240] or (recv,ret,sp,self.read(sp+4))!=(UNITCTRL,0x46B584,STACK+0xFF00-100,UNITCTRL+0x80AEC+i*STRIDE):raise RuntimeError('world final natural unit order/stack')
                self.world_final_entries.append(i)
            if address in CALL_ARGS:self.world_final_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'args':[self.read(sp+4+n*4) for n in range(CALL_ARGS[address])]})
            if address==0x468D10 and ret==0x46B560:self.world_final_tests.append((self.read(sp+4)-UNITCTRL-0x80AEC)//STRIDE)
            if address in (0x4757B7,0x475A42,0x475C55,0x46B7E1,0x46B80C,0x46B85B,0x46BA07):
                self.world_final_returns.append({'index':self.world_final_entries[-1],'va':hex(address),'sp':sp,'eax':uc.reg_read(UC_X86_REG_EAX)})
        else:
            if address==RETURN:uc.emu_stop();return
            if address in ROOTS:
                if (recv,ret,sp)!=(UNITCTRL,ROOTS[address],STACK+0xFF00-92):raise RuntimeError('world final original suffix root')
                self.world_final_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp})
            nested={0x456B20:(self.read(UNITCTRL+0x117C38),0x48CE8B),0x48D5D0:(UNITCTRL,0x48CE99),0x496450:(UNITCTRL,0x48D5F5),0x427DE0:(UNITCTRL+0x2A80,0x48D618)}
            if address in nested:
                if (recv,ret)!=nested[address]:raise RuntimeError('world final original empty forwarding')
                self.world_final_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp})
            if address==0x40A100:
                anim=self.read(sp+4);index=(anim-UNITCTRL-0x10C680-0x48)//EFFECT_STRIDE
                if not 0<=index<10 or anim!=UNITCTRL+0x10C680+index*EFFECT_STRIDE+0x48 or recv!=self.read(anim-4) or ret!=0x4668DD or sp!=STACK+0xFF00-192:raise RuntimeError('world final ten idle effect callers')
                self.world_final_effects.append({'index':index,'receiver':recv,'anim':anim,'return_va':hex(ret),'sp':sp})
            if address==0x4668DD:self.world_final_effect_returns.append(uc.reg_read(UC_X86_REG_EAX))
            if address==0x46B662:
                if (ret,sp)!=(RETURN,STACK+0xFF00):raise RuntimeError('world final real ret to existing declared driver')
                self.world_final_real_ret={'va':hex(address),'return_va':hex(ret),'sp':sp,'eax':uc.reg_read(UC_X86_REG_EAX),'original_outer_caller':False}
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        if any(a<=address<b for a,b in NATIVE):self.world_final_visited.add(address);return
        raise RuntimeError('world final undeclared instruction '+hex(address))

    def inputs240(self):
        s=source_contract();units=[]
        for i in INDICES:
            w=UNITCTRL+0x80AEC+i*STRIDE;rp=self.read(w+0x258);r=bytes(self.uc.mem_read(rp,176));klass=struct.unpack_from('<H',r,12)[0];rule=s['jobs'][str(klass)];owner=self.read(w+0x44);meta=self.read(owner);n=rule['main']['metadata_bytes'];raw,identity,_=resource(klass);buf=bytes(self.uc.mem_read(meta,n))
            if buf!=raw[:n]:raise RuntimeError('world final complete source metadata')
            units.append({'index':i,'record_pointer':rp,'record_hex':r.hex(),'binding':{'owner':owner,'metadata_pointer':meta,'metadata_bytes':n,'metadata_sha256':hashlib.sha256(buf).hexdigest(),'source_sha256':identity['sha256'],'controller_hex':bytes(self.uc.mem_read(owner,84)).hex()}})
        raw,identity=map_resource('map05.bin');header=self.read(MAPCTRL+0x2659C)
        if bytes(self.uc.mem_read(header,len(raw)))!=raw:raise RuntimeError('world final complete MAP05')
        return {'units':units,'effect_controller':self.read(UNITCTRL+0x2A6E8),'team':self.read(UNITCTRL+0x2EF44,'B'),'relation_matrix_hex':bytes(self.uc.mem_read(UNITCTRL+0x115AAC,256)).hex(),'map_sha256':identity['sha256'],'map_all_bytes_verified':len(raw),'map_header_pointer':header}

    def run_phase(self,phase):
        begin=0x46B760 if phase=='units' else 0x490FC0
        if self.uc.reg_read(UC_X86_REG_EIP)!=begin:raise RuntimeError('world final exact verified phase')
        before=self.following_regions();tail_before=self.tail_regions();tail_inputs=self.tail_inputs()
        if phase=='units':
            inputs=self.inputs240();expected=units_project(inputs,before);wanted_tail=tail_before
            self.world_final_allowed=[(STACK,STACK+65536),(0x7A49E0,0x7A49E4)]+[(UNITCTRL+0x80AEC+i*STRIDE,UNITCTRL+0x80AEC+(i+1)*STRIDE) for i in INDICES]+[(r['pointer'],r['pointer']+r['bytes']) for r in before[2:5]]
        else:
            inputs=tail_inputs;expected={'after':before,'second_46B470_body_completed':True,'original_outer_task_frame_completed':False};wanted_tail=suffix_project(inputs,tail_before);self.world_final_allowed=self.allowed()
        retained=self.capture_scene_memory(self.world_final_allowed);caller_bp=self.read(self.uc.reg_read(UC_X86_REG_EBP));prior=self._function_ranges;self._function_ranges=prior+NATIVE
        self.world_final_loading=True;self.world_final_phase=phase;self.world_final_calls=[];self.world_final_entries=[];self.world_final_tests=[];self.world_final_returns=[];self.world_final_visited=set();self.world_final_pending=None;self.world_final_effects=[];self.world_final_effect_returns=[];self.world_final_real_ret=None
        try:
            self.uc.emu_start(begin,RETURN,timeout=10_000_000,count=500000);after=self.following_regions();tail_after=self.tail_regions()
            if after!=expected['after'] or tail_after!=wanted_tail:
                diffs=[]
                for a,b in zip(after+tail_after,expected['after']+wanted_tail):
                    aa,bb=bytes.fromhex(a['hex']),bytes.fromhex(b['hex']);diffs.extend((a['name'],hex(a['pointer']+j),x,y) for j,(x,y) in enumerate(zip(aa,bb)) if x!=y)
                raise RuntimeError('world final full source/native bytes '+repr(diffs[:24]))
            result={'phase':phase,'inputs':inputs,'before':before,**expected,'tail_inputs':tail_inputs,'tail_before':tail_before,'tail_after':tail_after,'calls':self.world_final_calls,'visited':sorted(self.world_final_visited),
              'owned_bodies_stubbed':False,'VM_or_AI_completed':False,'original_opening_completed':False,'180_enabled_updates_completed':False,**self.verify_scene_memory(retained)}
            if phase=='units':
                if self.world_final_entries!=INDICES or self.world_final_tests!=list(range(241,250)) or self.world_final_pending is None:raise RuntimeError('world final complete natural unit loop')
                result.update(unit_entries=self.world_final_entries,tested_slots=self.world_final_tests,returns=self.world_final_returns,pending=self.world_final_pending)
            else:
                cpu=architectural_cpu(self.uc)
                if cpu['EIP']!=RETURN or cpu['ESP']!=STACK+0xFF00+4 or cpu['EBP']!=caller_bp or cpu['EAX']!=0 or self.world_final_real_ret is None or self.world_final_effect_returns!=[1]*10:raise RuntimeError('world final original whole function return')
                result.update(effect_calls=self.world_final_effects,effect_returns=self.world_final_effect_returns,real_ret=self.world_final_real_ret,driver_return={'va':hex(RETURN),'sp':cpu['ESP'],'ebp':cpu['EBP'],'expected_caller_ebp':caller_bp,'eax':cpu['EAX'],'declared_audit_sentinel':True})
            return result
        finally:self.world_final_loading=False;self._function_ranges=prior

    def save_phase(self,name,phase):
        path=ROOT/f'.venv-audit/world-final-{phase}-{name}.pkl'
        if path.exists():raise ValueError('fresh world final checkpoint')
        eip=0x490FC0 if phase=='units' else RETURN
        payload={'source_sha':SOURCE_SHA256,'parent_report_sha':PARENT_SHA,'case_name':name,'phase':phase,'evidence_kind':'private_original_world_final_'+phase,'pending_eip':eip,
          'state':{k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith('_audit_')},'memory':[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()],'cpu':self.uc.context_save()}
        raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);path.write_bytes(raw)
        return {'path':path.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'pending_eip':hex(eip),'runtime_or_original_save':False}


def restored(name,phase='units'):
    if phase=='units':payload,cp=load_parent(name)
    else:
        from tools.school_world_final_verification import load_verified_checkpoint
        payload,cp=load_verified_checkpoint(name,'units')
    e=WorldFinalEmulator();e.__dict__.update({k:v for k,v in payload['state'].items() if k!='uc' and not k.startswith('_audit_')})
    for at,buf in payload['memory']:
        if not any(a<=at and at+len(buf)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(buf))
        e.uc.mem_write(at,buf)
    e.uc.context_restore(payload['cpu']);return e,cp


def report(phase):
    cases=[]
    for name in ('initial','student9_waiting','fifth_class'):
        e,cp=restored(name,phase)
        if phase=='units':e.world_final_parent_checkpoint=cp
        a=e.run_phase(phase);c={'name':name,'parent_checkpoint':e.world_final_parent_checkpoint,'actual':a,'continuation_checkpoint':e.save_phase(name,phase)}
        if phase=='return':c['units_checkpoint']=cp
        cases.append(c);print(name+': original world final '+phase+' verified',flush=True)
    return {'schema_version':1,'phase':phase,'source_contract':source_contract(),'parent_report':PARENT.relative_to(ROOT).as_posix(),'parent_sha256':PARENT_SHA,'cases':cases,
      'second_46B470_body_completed':phase=='return','original_outer_task_frame_completed':False,'original_opening_completed':False,'persistent_write_authority':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--phase',choices=('units','return'),required=True);p.add_argument('--out',required=True);args=p.parse_args();path=ROOT/args.out
    if path.exists():p.error('fresh immutable report required')
    path.write_text(report_text(report(args.phase)),encoding='utf-8',newline='\n')
