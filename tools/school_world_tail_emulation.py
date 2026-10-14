"""Original paused46B470 suffix and real return to its declared audit driver."""
import argparse,hashlib,pickle,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EAX,UC_X86_REG_EBP
from tools.school_world_command_emulation import WorldCommandEmulator,ROOT,UNITCTRL,STACK,RETURN,ExitEmulator,architectural_cpu,report_text
from tools.school_world_command_verification import load_verified_checkpoint,REPORT as PARENT,REPORT_SHA as PARENT_SHA
from tools.school_world_tail import source_contract,ranges,project,idle_effects,EFFECT_STRIDE,SECONDARY_STRIDE
from tools.tactics_exit_emulation import SOURCE_SHA256

NATIVE=ranges()+((0x46B620,0x46B663),)
PROBES=(0,32767,65535)
ROOTS={0x490FC0:0x46B620,0x49CC60:0x46B628,0x49C400:0x46B630,
       0x466880:0x46B638,0x493A30:0x46B640,0x48CE60:0x46B648}


class WorldTailEmulator(WorldCommandEmulator):
    def __init__(self):
        self.tail_loading=False;super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.tail_loading:return super()._write_hook(uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.tail_allowed):raise RuntimeError('tail forbidden write '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.tail_loading:return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
        if address==RETURN:
            self.tail_returned=True;uc.emu_stop();return
        if address in ROOTS:
            wanted=(ROOTS[address],STACK+0xFF00-92) if self.tail_kind=='actual' else (RETURN,STACK+0xFF00)
            if recv!=UNITCTRL or (ret,sp)!=wanted:raise RuntimeError('tail exact original root caller')
            self.tail_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp})
        if address==0x40A100:
            anim=self.read(sp+4);index=(anim-UNITCTRL-0x10C680-0x48)//EFFECT_STRIDE
            expected_sp=STACK+0xFF00-(192 if self.tail_kind=='actual' else 100)
            if not 0<=index<10 or anim!=UNITCTRL+0x10C680+index*EFFECT_STRIDE+0x48 or recv!=self.read(anim-4) or ret!=0x4668DD or sp!=expected_sp:
                raise RuntimeError('tail ten exact effect animation calls')
            self.tail_effect_calls.append({'index':index,'receiver':recv,'anim':anim,'return_va':hex(ret),'sp':sp})
        if address==0x4668DD:
            if uc.reg_read(UC_X86_REG_EAX)!=1:raise RuntimeError('original idle animation result')
            self.tail_effect_returns.append(1)
        nested={0x456B20:(self.read(UNITCTRL+0x117C38),0x48CE8B),0x48D5D0:(UNITCTRL,0x48CE99),
                0x496450:(UNITCTRL,0x48D5F5),0x427DE0:(UNITCTRL+0x2A80,0x48D618)}
        if address in nested:
            if self.tail_kind!='actual' or (recv,ret)!=nested[address]:raise RuntimeError('tail original forwarding caller')
            self.tail_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp})
        if address==0x46B662:
            if self.tail_kind!='actual' or (ret,sp)!=(RETURN,STACK+0xFF00):raise RuntimeError('tail real world ret to declared driver')
            self.tail_real_ret={'va':hex(address),'return_va':hex(ret),'sp':sp,'eax':uc.reg_read(UC_X86_REG_EAX),'original_outer_caller':False}
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        if any(a<=address<b for a,b in NATIVE):self.tail_visited.add(address);return
        raise RuntimeError('tail undeclared instruction '+hex(address))

    def tail_regions(self):
        rows=[('cursor',UNITCTRL+0x3098C,10),('window',UNITCTRL+0x2F150,20),('menu',UNITCTRL+0x115CB8,1),
          ('effects',UNITCTRL+0x10C680,EFFECT_STRIDE*10),('secondary',UNITCTRL+0x116254,SECONDARY_STRIDE*5),
          ('control',UNITCTRL+0x108B30,50),('outgoing_queue',UNITCTRL+0x1798,20),('incoming_queue',UNITCTRL+0x2A80,20),
          ('dispatch_mode',UNITCTRL+0x117C3C,1),('script_busy',0x7F4491,1)]
        return [{'name':n,'pointer':p,'bytes':b,'hex':bytes(self.uc.mem_read(p,b)).hex()} for n,p,b in rows]

    def tail_inputs(self):
        return {'pointer_xy':[self.read(UNITCTRL+0x2A316,'h'),self.read(UNITCTRL+0x2A318,'h')],
            'selection_count':self.read(UNITCTRL+0x108B50),'effect_receivers':[self.read(UNITCTRL+0x10C680+i*EFFECT_STRIDE+0x44) for i in range(10)],
            'entry_receiver':self.read(UNITCTRL+0x117C38)}

    def allowed(self,probes=False):
        rows=[(STACK,STACK+65536)]
        if not probes:rows += [(UNITCTRL+0x30994,UNITCTRL+0x30995),(UNITCTRL+0x2F160,UNITCTRL+0x2F161),(UNITCTRL+0x115CB8,UNITCTRL+0x115CB9)]
        for i in range(10):
            p=UNITCTRL+0x10C680+i*EFFECT_STRIDE;rows += [(p+4,p+5),(p+10,p+12)]
        return rows

    def reset_trace(self):
        self.tail_calls=[];self.tail_effect_calls=[];self.tail_effect_returns=[];self.tail_visited=set();self.tail_returned=False;self.tail_real_ret=None

    def run_tail(self):
        if self.uc.reg_read(UC_X86_REG_EIP)!=0x490FC0:raise RuntimeError('tail exact checkpoint EIP')
        before=self.tail_regions();inputs=self.tail_inputs();wanted=project(inputs,before)
        bp=self.uc.reg_read(UC_X86_REG_EBP);caller_bp=self.read(bp);prior=self._function_ranges;self._function_ranges=prior+NATIVE
        self.tail_allowed=self.allowed();retained=self.capture_scene_memory(self.tail_allowed);self.tail_loading=True;self.tail_kind='actual';self.reset_trace()
        try:
            self.uc.emu_start(0x490FC0,RETURN,timeout=3_000_000,count=100000)
            after=self.tail_regions();cpu=architectural_cpu(self.uc)
            if after!=wanted or self.uc.reg_read(UC_X86_REG_EIP)!=RETURN or self.tail_real_ret is None or cpu['ESP']!=STACK+0xFF00+4 or cpu['EBP']!=caller_bp or cpu['EAX']!=0:
                raise RuntimeError('tail original full-byte/function-return equality')
            if [r['index'] for r in self.tail_effect_calls]!=list(range(10)) or self.tail_effect_returns!=[1]*10:raise RuntimeError('tail complete ten effects')
            return {'inputs':inputs,'before':before,'after':after,'calls':deepcopy(self.tail_calls),'effect_calls':deepcopy(self.tail_effect_calls),
              'effect_returns':self.tail_effect_returns,'visited':sorted(self.tail_visited),'real_ret':self.tail_real_ret,
              'driver_return':{'va':hex(RETURN),'sp':cpu['ESP'],'ebp':cpu['EBP'],'expected_caller_ebp':caller_bp,'eax':cpu['EAX'],'declared_audit_sentinel':True},
              'first_paused_46B470_body_completed':True,'enabled_gameplay_tick_completed':False,'original_outer_task_frame_completed':False,
              'active_animation_commands_executed':False,'nonempty_queue_forwarded':False,'owned_bodies_stubbed':False,**self.verify_scene_memory(retained)}
        finally:self.tail_loading=False;self._function_ranges=prior

    def run_counter_probes(self):
        original=self.tail_regions();restore=[r for r in original if r['name']=='effects'];cpu=self.uc.context_save();stack=bytes(self.uc.mem_read(STACK,65536));regs=architectural_cpu(self.uc)
        retained=self.capture_scene_memory([(r['pointer'],r['pointer']+r['bytes']) for r in restore]);prior=self._function_ranges;self._function_ranges=prior+NATIVE
        self.tail_allowed=self.allowed(True);self.tail_loading=True;self.tail_kind='probe';rows=[]
        try:
            for value in PROBES:
                for i in range(10):self.write(UNITCTRL+0x10C680+i*EFFECT_STRIDE+10,value,'H')
                before=self.tail_regions();self.reset_trace();self.call(0x466880,receiver=UNITCTRL);after=self.tail_regions();wanted=deepcopy(before);wanted[3]['hex']=idle_effects(bytes.fromhex(before[3]['hex'])).hex()
                if after!=wanted or [r['index'] for r in self.tail_effect_calls]!=list(range(10)) or self.tail_effect_returns!=[1]*10:raise RuntimeError('tail counter complete native/source equality')
                row={'declared_counter_word':value,'before':before,'after':after,'effect_calls':deepcopy(self.tail_effect_calls),'effect_returns':self.tail_effect_returns,
                    'visited':sorted(self.tail_visited),**self.verify_scene_memory(retained)}
                row['restoration']=self.restore_probe(restore,cpu,stack,regs);rows.append(row)
            return {'live_input_captured':False,'counter':rows,'final_restoration':self.restore_probe(restore,cpu,stack,regs)}
        finally:self.restore_probe(restore,cpu,stack,regs);self.tail_loading=False;self._function_ranges=prior


def restore_case(name):
    payload,cp=load_verified_checkpoint(name);e=WorldTailEmulator()
    e.__dict__.update({k:v for k,v in payload['state'].items() if k!='uc' and not k.startswith('_audit_')})
    for at,data in payload['memory']:
        if not any(a<=at and at+len(data)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(data))
        e.uc.mem_write(at,data)
    e.uc.context_restore(payload['cpu']);return e,cp


def report():
    cases=[]
    for name in ('initial','student9_waiting','fifth_class'):
        e,cp=restore_case(name);actual=e.run_tail();probes=e.run_counter_probes()
        cases.append({'name':name,'parent_checkpoint':cp,'actual_tail':actual,'declared_probes':probes})
        print(name+': original46B662 returned EAX0 to declared driver; ten idle effects / three counter probes verified',flush=True)
    return {'schema_version':1,'source_contract':source_contract(),'parent_report':PARENT.relative_to(ROOT).as_posix(),'parent_sha256':PARENT_SHA,
      'driver':'pinned verified CPU/all-memory restoration; original inner calls; declared audit RETURN sentinel',
      'cases':cases,'first_paused_46B470_body_completed':True,'enabled_gameplay_tick_completed':False,
      'original_outer_task_frame_completed':False,'original_opening_completed':False,'persistent_write_authority':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable report path required')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
