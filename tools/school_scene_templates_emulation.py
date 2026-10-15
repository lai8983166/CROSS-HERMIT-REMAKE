"""Original contiguous218–239 template loop, stop before scene240."""
import argparse,hashlib,pickle
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EAX
from tools.school_scene_first_emulation import SceneFirstEmulator,NATIVE,UNITCTRL,STACK,RETURN,ExitEmulator,report_text
from tools.school_scene_first_verification import load_verified_checkpoint,REPORTS,SHAS
from tools.school_deferred_units_emulation import CALL_ARGS
from tools.school_following_students_verification import pending
from tools.school_scene_templates import *

PARENT=REPORTS['complete'];PARENT_SHA=SHAS['complete']


class SceneTemplatesEmulator(SceneFirstEmulator):
    def __init__(self):self.templates_loading=False;super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.templates_loading:return super()._write_hook(uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.templates_allowed):raise RuntimeError('template batch forbidden write '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.templates_loading:return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
        if address==0x46B760:
            i=self.read(sp+8);p=pending(i)
            if (recv,ret,sp,[self.read(sp+4),i])!=(p['receiver'],int(p['return_va'],16),p['sp'],p['args']):raise RuntimeError('template batch original entry stack')
            if i==240:self.templates_pending=p;uc.emu_stop();return
            if i not in INDICES or self.templates_entries!=INDICES[:i-218]:raise RuntimeError('template batch exact natural order')
            self.templates_entries.append(i)
        if address in CALL_ARGS:self.templates_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'args':[self.read(sp+4+n*4) for n in range(CALL_ARGS[address])]})
        if address==0x468D10 and ret==0x46B560:self.templates_tests.append((self.read(sp+4)-UNITCTRL-0x80AEC)//STRIDE)
        if address in (0x475B0A,0x46BA07):self.templates_returns.append({'index':self.templates_entries[-1],'va':hex(address),'sp':sp,'eax':uc.reg_read(UC_X86_REG_EAX)})
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        if any(a<=address<b for a,b in NATIVE):self.templates_visited.add(address);return
        raise RuntimeError('template batch undeclared original instruction '+hex(address))

    def run_templates(self):
        if self.uc.reg_read(UC_X86_REG_EIP)!=0x46B760 or self.read(self.uc.reg_read(UC_X86_REG_ESP)+8)!=218:raise RuntimeError('template batch verified218 start')
        before=self.following_regions();expected=project(before);self.templates_allowed=[(STACK,STACK+65536),(0x7A49E0,0x7A49E4)]
        for i in INDICES:
            w=UNITCTRL+0x80AEC+i*STRIDE;self.templates_allowed += [(w+6,w+9),(w+10,w+12),(w+0x293,w+0x294)]
        retained=self.capture_scene_memory(self.templates_allowed);prior=self._function_ranges;self._function_ranges=prior+NATIVE
        self.templates_loading=True;self.templates_calls=[];self.templates_returns=[];self.templates_entries=[];self.templates_tests=[];self.templates_visited=set();self.templates_pending=None
        try:
            self.uc.emu_start(0x46B760,RETURN,timeout=8_000_000,count=250000)
            if self.following_regions()!=expected['after'] or self.templates_entries!=INDICES or self.templates_tests!=list(range(219,241)) or self.templates_pending!=pending(240):raise RuntimeError('template batch complete source/loop equality')
            return {'before':before,**expected,'calls':self.templates_calls,'returns':self.templates_returns,'tested_slots':self.templates_tests,'pending':self.templates_pending,'visited':sorted(self.templates_visited),
              'owned_bodies_stubbed':False,'next_unit_executed':False,'VM_or_AI_completed':False,**self.verify_scene_memory(retained)}
        finally:self.templates_loading=False;self._function_ranges=prior

    def save_templates(self,name):
        path=ROOT/f'.venv-audit/scene-templates-before240-{name}.pkl'
        if path.exists():raise ValueError('fresh template batch checkpoint')
        payload={'source_sha':SOURCE_SHA256,'parent_report_sha':PARENT_SHA,'case_name':name,'evidence_kind':'private_original_scene_templates_before240','pending_eip':0x46B760,
          'state':{k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith('_audit_')},'memory':[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()],'cpu':self.uc.context_save()}
        raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);path.write_bytes(raw)
        return {'path':path.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'pending_eip':'0x46b760','runtime_or_original_save':False}


def report():
    cases=[]
    for name in ('initial','student9_waiting','fifth_class'):
        payload,cp=load_verified_checkpoint(name,'complete');e=SceneTemplatesEmulator();e.__dict__.update({k:v for k,v in payload['state'].items() if k!='uc' and not k.startswith('_audit_')})
        for at,buf in payload['memory']:
            if not any(a<=at and at+len(buf)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(buf))
            e.uc.mem_write(at,buf)
        e.uc.context_restore(payload['cpu']);a=e.run_templates();cases.append({'name':name,'parent_checkpoint':cp,'actual':a,'continuation_checkpoint':e.save_templates(name)})
        print(name+':22 inactive templates returned; stopped before240',flush=True)
    return {'schema_version':1,'source_contract':source_contract(),'parent_report':PARENT.relative_to(ROOT).as_posix(),'parent_sha256':PARENT_SHA,'cases':cases,'templates_activated':0,'world_completed':False,'persistent_write_authority':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);args=p.parse_args();path=ROOT/args.out
    if path.exists():p.error('fresh immutable evidence required')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
