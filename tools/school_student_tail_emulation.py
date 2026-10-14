"""Complete original first enabled unit and restored isolated regen probes."""
import argparse,hashlib,pickle,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EAX
from tools.school_student_action_emulation import StudentActionEmulator,ROOT,UNITCTRL,TACT,STACK,RETURN,ExitEmulator,report_text,REPORTS,PHASE_SHAS
from tools.school_student_action_verification import load_verified_checkpoint
from tools.school_world_second_emulation import MAPCTRL
from tools.school_world_mode_emulation import architectural_cpu
from tools.school_world_lists import ranges as vision_ranges
from tools.school_student_tail import *

PARENT=REPORTS['animation'];PARENT_SHA=PHASE_SHAS['animation']
NATIVE=ranges()+vision_ranges()+((0x46B86D,0x46BA0A),(0x46B532,0x46B586))
ROOT_RETURNS={0x482A30:0x46B86D,0x4918D0:0x46B87D,0x493450:0x46B889,0x472370:0x46B895,
  0x472770:0x46B8BF,0x430400:0x46B8CB,0x4DDBB0:0x46B93E,0x46B2C0:0x46B967}


class StudentTailEmulator(StudentActionEmulator):
    def __init__(self):
        self.unit_tail_loading=False;super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.unit_tail_loading:return super()._write_hook(uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.unit_tail_allowed):raise RuntimeError('unit tail forbidden write '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.unit_tail_loading:return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp);w=UNITCTRL+0x80AEC
        if address==0x46B760:
            args=[self.read(sp+4),self.read(sp+8)]
            if self.unit_tail_kind!='actual' or (recv,ret,sp,args)!=(UNITCTRL,0x46B584,STACK+0xFF00-100,[w+STRIDE,1]):raise RuntimeError('next slot1 natural entry')
            self.unit_tail_pending={'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'args':args,'first_instruction_executed':False};uc.emu_stop();return
        if address in ROOT_RETURNS:
            expected=ROOT_RETURNS[address] if self.unit_tail_kind=='actual' else RETURN
            if address==0x4DDBB0:
                if ret!=expected:raise RuntimeError('unit tail original view caller')
            elif recv!=UNITCTRL or ret!=expected:raise RuntimeError('unit tail original root caller '+hex(address))
            n=2 if address in (0x482A30,0x4918D0) else 1
            self.unit_tail_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'args':[self.read(sp+4+i*4) for i in range(n)]})
        if address in (0x482AC0,0x491960):
            if recv!=UNITCTRL:raise RuntimeError('unit six-controller receiver')
            args=[self.read(sp+4+i*4) for i in range(3)];expected=[w,0,w+0x48] if len(self.unit_scans[address])==0 else [w,0,w+0xA0+(len(self.unit_scans[address])-1)*88]
            if args!=expected:raise RuntimeError('all original six controller scan arguments')
            self.unit_scans[address].append({'args':args,'return_va':hex(ret),'sp':sp})
        if address==0x472550:
            args=[self.read(sp+4+i*4) for i in range(3)]
            if self.unit_tail_kind!='probe' or recv!=UNITCTRL or args[0]!=w or args[1:] not in ([0,1],[1,1]):raise RuntimeError('declared original positive recovery call')
            self.unit_heals.append({'args':args,'return_va':hex(ret),'sp':sp})
        if address==0x43BB90:
            args=[self.read(sp+4,'i'),self.read(sp+8,'i')]
            if (recv,ret,args)!=(MAPCTRL,0x430485,[10,17]):raise RuntimeError('unit actual source map cell lookup')
            self.unit_tail_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'args':args})
        if address==0x4305C0:
            args=[self.read(sp+4),self.read(sp+8)]
            if (recv,args)!=(UNITCTRL,[w,0]):raise RuntimeError('unit source region tally caller')
            self.unit_tail_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'args':args})
        if address==0x43D270:
            args=[self.read(sp+4+i*4,'i') for i in range(3)]
            if (recv,ret,args)!=(MAPCTRL,0x46B95B,[10,17,9]):raise RuntimeError('unit source actual vision caller')
            self.unit_tail_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'args':args})
        if address==0x46BA07:
            if self.unit_tail_kind!='actual' or (ret,sp)!=(0x46B584,STACK+0xFF00-100):raise RuntimeError('first unit real ret')
            self.unit_return={'va':hex(address),'sp':sp,'return_va':hex(ret),'eax':uc.reg_read(UC_X86_REG_EAX)}
        if address==0x46B584:
            if self.unit_tail_kind!='actual' or sp!=STACK+0xFF00-88:raise RuntimeError('first unit natural returned stack')
            self.unit_returned={'va':hex(address),'sp':sp}
        if address==0x468D10 and ret==0x46B560:
            if (recv,self.read(sp+4))!=(UNITCTRL,w+STRIDE):raise RuntimeError('next original occupied-slot test')
            self.unit_next_tests.append(1)
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        if any(a<=address<b for a,b in NATIVE):self.unit_tail_visited.add(address);return
        raise RuntimeError('unit tail undeclared original instruction '+hex(address))

    def regions(self):
        w=UNITCTRL+0x80AEC;rec=self.read(w+0x258);owner=self.read(MAPCTRL+0x265A0)
        rows=[('works',w,STRIDE*COUNT),('record',rec,176),('region_stats',UNITCTRL+0x2E714,2048),
          ('fog_current',self.read(MAPCTRL+0xA4),6144),('fog_history',self.read(MAPCTRL+0xA0),6144),('occupancy',self.read(owner),12288),
          ('pool',POOL,NODE*SLOTS),('control',UNITCTRL+0x108B30,50),('task',TACT,400),('current_work',0x7A49E0,4)]
        return [{'name':n,'pointer':p,'bytes':b,'hex':bytes(self.uc.mem_read(p,b)).hex()} for n,p,b in rows]

    def reset_trace(self):
        self.unit_tail_calls=[];self.unit_scans={0x482AC0:[],0x491960:[]};self.unit_heals=[];self.unit_tail_visited=set();self.unit_return=None;self.unit_returned=None;self.unit_next_tests=[];self.unit_tail_pending=None

    def run_tail(self):
        if self.uc.reg_read(UC_X86_REG_EIP)!=0x482A30:raise RuntimeError('first-unit verified animation entry')
        before=self.regions();header=self.read(MAPCTRL+0x2659C);raw,identity=map_resource('map05.bin')
        if bytes(self.uc.mem_read(header,len(raw)))!=raw:raise RuntimeError('complete original MAP05 source binding')
        inputs={'team':self.read(UNITCTRL+0x2EF44,'B'),'map_sha256':identity['sha256'],'map_header_pointer':header,'map_all_bytes_verified':len(raw)}
        expected=project(inputs,before);w=UNITCTRL+0x80AEC;self.unit_tail_allowed=[(STACK,STACK+65536),(w+0x504,w+0x508),(w+0x4E7,w+0x4EB),
            (before[2]['pointer'],before[2]['pointer']+4)]+[(r['pointer'],r['pointer']+r['bytes']) for r in before[3:5]]
        retained=self.capture_scene_memory(self.unit_tail_allowed);prior=self._function_ranges;self._function_ranges=prior+NATIVE
        self.unit_tail_loading=True;self.unit_tail_kind='actual';self.reset_trace()
        try:
            self.uc.emu_start(0x482A30,RETURN,timeout=5_000_000,count=150000);after=self.regions()
            if after!=expected['after'] or self.unit_return is None or self.unit_returned is None or self.unit_tail_pending is None or self.unit_next_tests!=[1]:raise RuntimeError('first complete original unit/source equality')
            if any(len(v)!=6 for v in self.unit_scans.values()) or self.unit_heals:raise RuntimeError('actual six empty scans/no heal')
            return {'inputs':inputs,'before':before,**expected,'calls':self.unit_tail_calls,'effect_scans':self.unit_scans[0x482AC0],'damage_scans':self.unit_scans[0x491960],
              'native_heals':self.unit_heals,'real_ret':self.unit_return,'returned':self.unit_returned,'next_tests':self.unit_next_tests,'pending':self.unit_tail_pending,
              'visited':sorted(self.unit_tail_visited),'next_unit_executed':False,'nonempty_effect_or_damage_executed':False,'world_or_VM_or_AI_completed':False,'owned_bodies_stubbed':False,**self.verify_scene_memory(retained)}
        finally:self.unit_tail_loading=False;self._function_ranges=prior

    def run_regen_probes(self):
        original=self.regions();w=UNITCTRL+0x80AEC;rec=original[1]['pointer'];restore=[{'pointer':w,'bytes':STRIDE,'hex':original[0]['hex'][:STRIDE*2]},original[1]]
        cpu=self.uc.context_save();stack=bytes(self.uc.mem_read(STACK,65536));regs=architectural_cpu(self.uc)
        retained=self.capture_scene_memory([(r['pointer'],r['pointer']+r['bytes']) for r in restore]);prior=self._function_ranges;self._function_ranges=prior+NATIVE
        self.unit_tail_allowed=[(STACK,STACK+65536),(w+0x504,w+0x508),(rec+0x16,rec+0x18),(rec+0x1C,rec+0x1E)]
        self.unit_tail_loading=True;self.unit_tail_kind='probe';rows=[]
        try:
            for declared in PROBES:
                r=bytearray.fromhex(original[1]['hex']);r[15]=declared['state'];put(r,0x16,get(r,0x14)-declared['hp_gap']);put(r,0x1C,get(r,0x1A)-declared['mp_gap']);self.uc.mem_write(rec,bytes(r))
                self.write(w+0x504,declared['hp_counter'],'h');self.write(w+0x506,declared['mp_counter'],'h');before=self.regions();self.reset_trace()
                expected=regen(bytes.fromhex(before[0]['hex'])[:STRIDE],r);self.call(0x472370,[w],receiver=UNITCTRL);after=self.regions();wanted=deepcopy(before)
                wanted[0]['hex']=expected['work_hex']+before[0]['hex'][STRIDE*2:];wanted[1]['hex']=expected['record_hex']
                if after!=wanted or [row['args'][1:] for row in self.unit_heals]!=expected['heals']:raise RuntimeError('isolated original regeneration full equality')
                row={'declared':declared,'before':before,'after':after,'heals':self.unit_heals,'visited':sorted(self.unit_tail_visited),**self.verify_scene_memory(retained)}
                row['restoration']=self.restore_probe(restore,cpu,stack,regs);rows.append(row)
            return {'live_input_captured':False,'rows':rows,'final_restoration':self.restore_probe(restore,cpu,stack,regs)}
        finally:self.restore_probe(restore,cpu,stack,regs);self.unit_tail_loading=False;self._function_ranges=prior

    def save_checkpoint(self,name):
        path=ROOT/f'.venv-audit/student-tail-before-slot1-{name}.pkl'
        if path.exists():raise ValueError('fresh student-tail continuation path')
        payload={'source_sha':SOURCE_SHA256,'parent_report_sha':PARENT_SHA,'case_name':name,'evidence_kind':'private_actual_first_student_returned_before_slot1',
          'pending_eip':0x46B760,'state':{k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith('_audit_')},
          'memory':[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()],'cpu':self.uc.context_save()}
        raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);path.write_bytes(raw)
        return {'path':path.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'pending_eip':'0x46b760','runtime_or_original_save':False}


def report():
    cases=[]
    for name in ('initial','student9_waiting','fifth_class'):
        payload,cp=load_verified_checkpoint(name,'animation');e=StudentTailEmulator()
        e.__dict__.update({k:v for k,v in payload['state'].items() if k!='uc' and not k.startswith('_audit_')})
        for at,data in payload['memory']:
            if not any(a<=at and at+len(data)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(data))
            e.uc.mem_write(at,data)
        e.uc.context_restore(payload['cpu']);actual=e.run_tail();probes=e.run_regen_probes();saved=e.save_checkpoint(name)
        cases.append({'name':name,'parent_checkpoint':cp,'actual_tail':actual,'declared_probes':probes,'continuation_checkpoint':saved})
        print(name+': first unit returned / region+vision verified / six restored regen probes',flush=True)
    return {'schema_version':1,'source_contract':source_contract(),'parent_report':PARENT.relative_to(ROOT).as_posix(),'parent_sha256':PARENT_SHA,'cases':cases,
      'first_unit_completed':True,'second_world_completed':False,'original_opening_completed':False,'persistent_write_authority':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable evidence path required')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
