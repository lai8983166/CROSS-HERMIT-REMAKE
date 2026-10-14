"""Original first student binding, linked initializer and first animation step."""
import argparse,hashlib,json,pickle,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EAX
from tools.school_world_second_emulation import WorldSecondEmulator,ROOT,UNITCTRL,TACT,STACK,RETURN,ExitEmulator,report_text
from tools.school_world_second_verification import load_verified_checkpoint,REPORT as PARENT,REPORT_SHA as PARENT_SHA
from tools.school_student_action import *
from tools.tactics_exit_emulation import SOURCE_SHA256

NATIVE=ranges()+((0x46B7E1,0x46B86D),(0x56CEC0,0x56CF18),(0x415070,0x415099))
PHASES=('binding','initializer','animation')
REPORTS={p:ROOT/f'analysis/school-student-action-{p}-v1-20261015.json' for p in PHASES}
REPORTS['binding']=ROOT/'analysis/school-student-action-binding-v2-20261015.json'
PHASE_SHAS={'binding':'22ff3c2c74fcdd344730a3ac6e2d207e3e9f2a4e02559a63c9d8470af0afa735'}
PHASE_SHAS['initializer']='d418bd9ce6fc64d4bfe546f617a0bc407a4e9a6b24bb2eded72e0429d73ee0a7'


class StudentActionEmulator(WorldSecondEmulator):
    def __init__(self):
        self.student_loading=False;super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.student_loading:return super()._write_hook(uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.student_allowed):raise RuntimeError('student forbidden write '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.student_loading:return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp);w=UNITCTRL+0x80AEC
        stop={'binding':0x465140,'initializer':0x40A100,'animation':0x482A30}[self.student_phase]
        if address==stop:
            argc={'binding':6,'initializer':1,'animation':2}[self.student_phase];args=[self.read(sp+4+i*4) for i in range(argc)]
            if self.student_phase=='binding' and (recv,args)!=(self.student_inputs['main_controller'],[w+0x48,self.student_inputs['effect_controller'],2063,0,0,7]):raise RuntimeError('student first natural attached binding')
            if self.student_phase=='initializer' and (recv,ret,sp,args)!=(self.student_inputs['main_controller'],0x46B80C,STACK+0xFF00-204,[w+0x48]):raise RuntimeError('student natural main animation boundary')
            if self.student_phase=='animation' and (recv,ret,sp,args)!=(UNITCTRL,0x46B86D,STACK+0xFF00-208,[w,0]):raise RuntimeError('student natural effect processing boundary')
            self.student_pending={'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'args':args,'first_instruction_executed':False};uc.emu_stop();return
        counts={0x475D60:1,0x46C040:2,0x46BCC0:2,0x465040:3,0x409FF0:4,0x468EB0:1,0x46BE50:4,
          0x465140:6,0x40AF40:8,0x40B5E0:0,0x409EF0:1,0x40A400:3,0x40A520:1,0x40A800:1,
          0x47A8E0:1,0x480A60:1,0x490350:2,0x490A50:3,0x40A100:1,0x415070:1}
        if address in counts:
            self.student_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'args':[self.read(sp+4+i*4) for i in range(counts[address])]})
        if address==0x40B665:raise RuntimeError('student unexpected pool release')
        if address==0x56CEC0:
            args=[self.read(sp+4+i*4) for i in range(3)]
            if ret!=0x409F1A or args[1:]!=[0,88] or args[0] not in self.student_nodes:raise RuntimeError('student exact original node clear')
            self.student_clears.append({'return_va':hex(ret),'args':args})
        if address in (0x4757A3,0x46B7E1,0x46B80C,0x46B85B):
            self.student_returns.append({'va':hex(address),'sp':sp,'eax':uc.reg_read(UC_X86_REG_EAX)})
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        if any(a<=address<b for a,b in NATIVE):self.student_visited.add(address);return
        raise RuntimeError('student undeclared original instruction '+hex(address))

    def student_regions(self):
        rows=[('works',UNITCTRL+0x80AEC,STRIDE*COUNT),('pool',POOL,NODE*SLOTS),('control',UNITCTRL+0x108B30,50),('task',TACT,400),('current_work',0x7A49E0,4)]
        return [{'name':n,'pointer':p,'bytes':b,'hex':bytes(self.uc.mem_read(p,b)).hex()} for n,p,b in rows]

    def inputs(self):
        w=UNITCTRL+0x80AEC;main=self.read(w+0x44);effect=self.read(UNITCTRL+0x2A6E8);s=source_contract();bindings=[]
        for owner,p,resource in ((main,s['main'],unit_resource()),(effect,s['attachments'][0],effect_resource())):
            meta=self.read(owner);raw,identity=resource;buf=bytes(self.uc.mem_read(meta,p['metadata_bytes']))
            if buf!=raw[:p['metadata_bytes']]:raise RuntimeError('student complete original metadata source binding')
            bindings.append({'owner':owner,'metadata_pointer':meta,'metadata_bytes':len(buf),'metadata_sha256':hashlib.sha256(buf).hexdigest(),'source_sha256':identity['sha256'],'controller_hex':bytes(self.uc.mem_read(owner,84)).hex()})
        return {'work_pointer':w,'main_controller':main,'effect_controller':effect,'main_metadata_pointer':bindings[0]['metadata_pointer'],
          'main_program_pointer':bindings[0]['metadata_pointer']+s['main']['offset'],
          'attachment_program_pointers':[bindings[1]['metadata_pointer']+p['offset'] for p in s['attachments']],
          'record_pointer':self.read(w+0x258),'record_hex':bytes(self.uc.mem_read(self.read(w+0x258),176)).hex(),'metadata_bindings':bindings}

    def run_phase(self,phase):
        if phase not in PHASES:raise ValueError('student phase')
        begin={'binding':0x475D60,'initializer':0x465140,'animation':0x40A100}[phase]
        if self.uc.reg_read(UC_X86_REG_EIP)!=begin:raise RuntimeError('student exact phase CPU entry')
        if phase=='binding':self.student_before=self.student_regions();self.student_inputs=self.inputs()
        expected={'binding':lambda: {'after':bind_project(self.student_inputs,self.student_before)},
          'initializer':lambda:initialized_project(self.student_inputs,self.student_before),
          'animation':lambda:animated_project(self.student_inputs,self.student_before)}[phase]()
        initialized=initialized_project(self.student_inputs,self.student_before);self.student_nodes=initialized['allocated_nodes']
        current=self.student_regions();self.student_allowed=[(STACK,STACK+65536),(UNITCTRL+0x80AEC,UNITCTRL+0x80AEC+STRIDE)]
        if phase!='binding':self.student_allowed += [(p,p+NODE) for p in self.student_nodes]
        retained=self.capture_scene_memory(self.student_allowed);prior=self._function_ranges;self._function_ranges=prior+NATIVE
        self.student_loading=True;self.student_phase=phase;self.student_calls=[];self.student_clears=[];self.student_returns=[];self.student_visited=set();self.student_pending=None
        try:
            self.uc.emu_start(begin,RETURN,timeout=5_000_000,count=150000)
            after=self.student_regions()
            if after!=expected['after'] or self.student_pending is None:raise RuntimeError('student complete original/source '+phase+' equality')
            return {'phase':phase,'inputs':self.student_inputs,'initial_before':self.student_before,'before':current,**expected,
              'calls':deepcopy(self.student_calls),'native_clears':self.student_clears,'returns':self.student_returns,'visited':sorted(self.student_visited),
              'pending':self.student_pending,'source_metadata_all_bytes_verified':True,'owned_bodies_stubbed':False,'GPU_rendering_executed':False,
              'full_unit_or_world_completed':False,'VM_or_AI_completed':False,**self.verify_scene_memory(retained)}
        finally:self.student_loading=False;self._function_ranges=prior

    def save_checkpoint(self,name,phase):
        path=ROOT/f'.venv-audit/student-action-{phase}-{name}.pkl'
        if path.exists():raise ValueError('fresh student checkpoint required')
        eip={'initializer':0x40A100,'animation':0x482A30}[phase]
        if self.uc.reg_read(UC_X86_REG_EIP)!=eip:raise ValueError('student next private EIP')
        payload={'source_sha':SOURCE_SHA256,'parent_report_sha':PARENT_SHA,'case_name':name,'phase':phase,'evidence_kind':'private_actual_student_action_'+phase,
          'pending_eip':eip,'state':{k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith('_audit_')},
          'memory':[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()],'cpu':self.uc.context_save()}
        raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);path.write_bytes(raw)
        return {'path':path.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'pending_eip':hex(eip),'runtime_or_original_save':False}


def restored(name):
    payload,cp=load_verified_checkpoint(name);e=StudentActionEmulator()
    e.__dict__.update({k:v for k,v in payload['state'].items() if k!='uc' and not k.startswith('_audit_')})
    for at,data in payload['memory']:
        if not any(a<=at and at+len(data)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(data))
        e.uc.mem_write(at,data)
    e.uc.context_restore(payload['cpu']);return e,cp


def report(phase):
    raw=PARENT.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=PARENT_SHA:raise ValueError('student source parent report identity')
    cases=[]
    for name in ('initial','student9_waiting','fifth_class'):
        e,cp=restored(name);steps=[]
        for p in PHASES[:PHASES.index(phase)+1]:
            actual=e.run_phase(p)
            if p!=phase:
                previous_raw=REPORTS[p].read_bytes()
                if hashlib.sha256(previous_raw).hexdigest()!=PHASE_SHAS[p]:raise ValueError('student immutable prior-phase identity')
                prev=json.loads(previous_raw);expected=next(c for c in prev['cases'] if c['name']==name)['actual']
                if actual!=expected:raise ValueError('student complete original prior phase equality')
            steps.append(p)
        case={'name':name,'parent_checkpoint':cp,'replayed_prior_phases_equal':steps[:-1],'actual':actual}
        if phase!='binding':case['continuation_checkpoint']=e.save_checkpoint(name,phase)
        cases.append(case);print(name+': original student '+phase+' full work/pool verified',flush=True)
    return {'schema_version':1,'phase':phase,'source_contract':source_contract(),'parent_report':PARENT.relative_to(ROOT).as_posix(),'parent_sha256':PARENT_SHA,
      'cases':cases,'full_unit_or_world_completed':False,'original_opening_completed':False,'persistent_write_authority':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--phase',choices=PHASES,required=True);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable report required')
    path.write_text(report_text(report(a.phase)),encoding='utf-8',newline='\n')
