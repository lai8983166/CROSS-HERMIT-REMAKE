"""Original215/216 mode11 early returns, before first scene unit217."""
import argparse,hashlib,pickle
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EAX
from tools.school_following_students_emulation import FollowingStudentsEmulator,NATIVE as FRIENDLY_NATIVE,ROOT,UNITCTRL,STACK,RETURN,ExitEmulator,report_text
from tools.school_following_students_verification import load_verified_checkpoint,REPORT as PARENT,REPORT_SHA as PARENT_SHA,pending
from tools.school_deferred_units import *

NATIVE=FRIENDLY_NATIVE+ranges()
CALL_ARGS={0x46B760:2,0x48D720:2,0x48E2A0:1,0x475700:1,0x4751F0:1,0x4697F0:1,0x479F40:1,0x46B0B0:2,0x46B0F0:2}


class DeferredUnitsEmulator(FollowingStudentsEmulator):
    def __init__(self):self.deferred_loading=False;super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.deferred_loading:return super()._write_hook(uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.deferred_allowed):raise RuntimeError('deferred forbidden write '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.deferred_loading:return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
        if address==0x46B760:
            index=self.read(sp+8);p=pending(index)
            if (recv,ret,sp,[self.read(sp+4),index])!=(p['receiver'],int(p['return_va'],16),p['sp'],p['args']):raise RuntimeError('deferred original unit entry')
            if index==217:self.deferred_pending=p;uc.emu_stop();return
            if index not in (215,216) or index in self.deferred_entries:raise RuntimeError('deferred exact original order')
            self.deferred_entries.append(index)
        if address in CALL_ARGS:
            self.deferred_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'args':[self.read(sp+4+n*4) for n in range(CALL_ARGS[address])]})
        if address==0x468D10 and ret==0x46B560:self.deferred_tests.append((self.read(sp+4)-UNITCTRL-0x80AEC)//STRIDE)
        if address in (0x475B0A,0x46BA07):
            self.deferred_returns.append({'index':self.deferred_entries[-1],'va':hex(address),'sp':sp,'return_va':hex(ret) if address==0x46BA07 else None,'eax':uc.reg_read(UC_X86_REG_EAX)})
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        if any(a<=address<b for a,b in NATIVE):self.deferred_visited.add(address);return
        raise RuntimeError('deferred undeclared original instruction '+hex(address))

    def run_deferred(self):
        if self.uc.reg_read(UC_X86_REG_EIP)!=0x46B760 or self.read(self.uc.reg_read(UC_X86_REG_ESP)+8)!=215:raise RuntimeError('deferred verifiedslot215 start')
        before=self.following_regions();expected=project(before);self.deferred_allowed=[(STACK,STACK+65536),(0x7A49E0,0x7A49E4)]
        for i in (215,216):
            w=UNITCTRL+0x80AEC+i*STRIDE;self.deferred_allowed += [(w+6,w+9),(w+10,w+12),(w+0x293,w+0x294)]
        retained=self.capture_scene_memory(self.deferred_allowed);prior=self._function_ranges;self._function_ranges=prior+NATIVE
        self.deferred_loading=True;self.deferred_entries=[];self.deferred_calls=[];self.deferred_tests=[];self.deferred_returns=[];self.deferred_visited=set();self.deferred_pending=None
        try:
            self.uc.emu_start(0x46B760,RETURN,timeout=5_000_000,count=40000)
            if self.following_regions()!=expected['after'] or self.deferred_entries!=[215,216] or self.deferred_tests!=[216,217] or self.deferred_pending!=pending(217):raise RuntimeError('deferred full source/loop equality')
            return {'before':before,**expected,'calls':self.deferred_calls,'unit_entries':self.deferred_entries,'tested_slots':self.deferred_tests,'returns':self.deferred_returns,
              'pending':self.deferred_pending,'visited':sorted(self.deferred_visited),'owned_bodies_stubbed':False,'scene_unit_executed':False,'VM_or_AI_completed':False,**self.verify_scene_memory(retained)}
        finally:self.deferred_loading=False;self._function_ranges=prior

    def save_deferred(self,name):
        path=ROOT/f'.venv-audit/deferred-units-before-scene217-{name}.pkl'
        if path.exists():raise ValueError('fresh deferred private path')
        payload={'source_sha':SOURCE_SHA256,'parent_report_sha':PARENT_SHA,'case_name':name,'evidence_kind':'private_original_deferred_units_before_scene217','pending_eip':0x46B760,
          'state':{k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith('_audit_')},'memory':[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()],'cpu':self.uc.context_save()}
        raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);path.write_bytes(raw)
        return {'path':path.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'pending_eip':'0x46b760','runtime_or_original_save':False}


def report():
    cases=[]
    for name in ('initial','student9_waiting','fifth_class'):
        payload,cp=load_verified_checkpoint(name);e=DeferredUnitsEmulator();e.__dict__.update({k:v for k,v in payload['state'].items() if k!='uc' and not k.startswith('_audit_')})
        for at,buf in payload['memory']:
            if not any(a<=at and at+len(buf)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(buf))
            e.uc.mem_write(at,buf)
        e.uc.context_restore(payload['cpu']);a=e.run_deferred();cases.append({'name':name,'parent_checkpoint':cp,'actual':a,'continuation_checkpoint':e.save_deferred(name)})
        print(name+': inactive215/216 returned early; stopped before scene217',flush=True)
    return {'schema_version':1,'source_contract':source_contract(),'parent_report':PARENT.relative_to(ROOT).as_posix(),'parent_sha256':PARENT_SHA,'cases':cases,'templates_activated':0,'world_completed':False,'original_opening_completed':False,'persistent_write_authority':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);args=p.parse_args();path=ROOT/args.out
    if path.exists():p.error('fresh immutable evidence required')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
