"""Actual fifth-school first-round CPU executes original combat record derivation.

4DAB10 resets work memory; it is not a scene resource loader. Pending16 remains
unconsumed, so prepared records are not a constructed tactical battlefield.
"""
import argparse
from copy import deepcopy
import hashlib
import json
import struct

from unicorn.x86_const import UC_X86_REG_EIP, UC_X86_REG_ESP, UC_X86_REG_ECX
from tools.school_adventure_handoff_emulation import SchoolAdventureHandoffEmulator
from tools.school_dispatch_emulation import GROUP_TASK
from tools.tactics_exit_emulation import BASE, ROOT, SOURCE, SOURCE_SHA256, TASK, STACK, RETURN, ExitEmulator, report_text
from tools.battle_preparation_emulation import CHAR_BASE, CHAR_STRIDE
from tools.school_course_unlock_emulation import AUTHORITY

NATIVE = ((0x4DAB10,0x4DAB50),(0x4B9340,0x4B93C0),(0x4B93C0,0x4BAA90),(0x4DB340,0x4DB420),
          (0x4DCF00,0x4DD510),(0x56CFCC,0x56CFF3))
WORK, WORK_SIZE = 0x8093F8,0x29A
UNITS = 0x7F4518
EVIDENCE = ROOT/'analysis/school-combat-records-v2-20261009.json'
EVIDENCE_SHA256 = 'ac743212f773dc2aa2daee6aa3ee2278239d384b47532610cb144a4ed4807e6f'


def combat_input(e, identity):
    at=CHAR_BASE+identity*CHAR_STRIDE
    return {'character_id':identity,'job':e.read(at+6,'H'),'level':e.read(at+0x50,'B'),
        'attributes':[e.read(at+0xC+8*i,'B') for i in range(7)],
        'equipped_items':[e.read(at+0x62+2*i,'H') for i in range(8)],
        'equipped_skills':[e.read(at+0x52+2*i,'H') for i in range(8)]}


def limits_snapshot(e, at):
    return {'character_id':e.read(at+2,'H'),'attributes':list(e.uc.mem_read(at+4,7)),
        'job':e.read(at+0xC,'H'),'level':e.read(at+0xE,'B'),
        'hp_max':e.read(at+0x14,'H'),'hp':e.read(at+0x16,'H'),'hp_recovery':e.read(at+0x18,'H'),
        'mp_max':e.read(at+0x1A,'H'),'mp':e.read(at+0x1C,'H'),'mp_recovery':e.read(at+0x1E,'H'),
        'engage_initial':e.read(at+0x20),'engage_left':e.read(at+0x24)}


class SchoolCombatRecordsEmulator(SchoolAdventureHandoffEmulator):
    def __init__(self):
        super().__init__()
        self._function_ranges += NATIVE
        self.combat_records=[]
        self.current_combat=None
        self.work_resets=[]
        self.record_writes=[]

    def _write_hook(self,uc,access,address,size,value,context):
        if getattr(self,'stage','') == 'handoff_round' and UNITS <= address and address+size <= UNITS+3*0xB0:
            if self.current_combat is None or not self.current_combat['destination'] <= address \
                    or address+size > self.current_combat['destination']+0xB0:
                raise RuntimeError('combat record write outside current ordinal')
            self.record_writes.append((address,size))
            self.writes.append((address,size,value & ((1 << (size*8))-1)))
            return
        return super()._write_hook(uc,access,address,size,value,context)

    def _hook(self,uc,address,size,context):
        if getattr(self,'stage','') != 'handoff_round':
            return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP)
        if address == 0x4B9340:
            identity,ordinal=self.read(sp+4,'H'),self.read(sp+8,'H')
            if identity not in (3,4,9) or not 0 <= ordinal < 3:
                raise RuntimeError('combat derivation outside owned current students')
            owned=combat_input(self,identity)
            if owned['equipped_items'] != [0]*8:
                raise RuntimeError('item handlers outside verified no-item subset: '+repr(owned))
            self.current_combat={'input':owned,'ordinal':ordinal,'destination':UNITS+ordinal*0xB0}
            self.record_writes=[]
            self.handoff_events.append({'kind':'native_combat_record','va':hex(address),
                'character_id':identity,'ordinal':ordinal})
            return ExitEmulator._hook(self,uc,address,size,context)
        if address == 0x4DB340:
            self.current_combat['modifier_pointer']=self.read(sp+8)
        if address == 0x4DCF00:
            identity=self.read(sp+4)
            if identity not in (20,29,31,57,59) or self.read(0x738998+4*identity) != 0:
                raise RuntimeError('skill modifier outside verified callback-free subset')
        if address == 0x4DB412:
            self.current_combat['modifier_hex']=bytes(uc.mem_read(self.current_combat['modifier_pointer'],0x4C)).hex()
        if address == 0x4B93B0:
            entry=deepcopy(self.current_combat)
            at=entry['destination']
            offsets=sorted({a+i-at for a,n in self.record_writes for i in range(n)})
            entry.update(limits=limits_snapshot(self,at),raw_record_hex=bytes(uc.mem_read(at,0xB0)).hex(),
                         defined_offsets=offsets)
            del entry['modifier_pointer']
            self.combat_records.append(entry)
        if address == 0x4DAB10:
            self.handoff_events.append({'kind':'native_work_reset_body','va':hex(address)})
            return ExitEmulator._hook(self,uc,address,size,context)
        if address == 0x56CEC0:
            target,byte,count=[self.read(sp+i) for i in (4,8,12)]
            work=(target,byte,count)==(WORK,0,WORK_SIZE)
            local=STACK <= target and target+count <= STACK+0x10000 and byte==0 and count in (0x4C,0x24)
            if not work and not local:
                raise RuntimeError('combat memset outside exact source ranges')
            uc.mem_write(target,bytes(count))
            if work:
                self.work_resets.append({'target':hex(target),'count':count,'caller_return_va':hex(self.read(sp))})
                # Explicit primitive writes are not delivered to Unicorn's CPU write hook.
                self.writes.extend((target+i,1,0) for i in range(count))
            self.stub_calls['bounded_combat_memset'] += 1
            self._stub_return(target,0)
            return
        if any(a <= address < b for a,b in NATIVE):
            return ExitEmulator._hook(self,uc,address,size,context)
        return super()._hook(uc,address,size,context)

    def handoff(self,name,commands=()):
        self.combat_records=[]
        self.work_resets=[]
        before=hashlib.sha256(bytes(self.uc.mem_read(CHAR_BASE,UNITS-CHAR_BASE-0x90))).hexdigest()
        result=super().handoff(name,commands)
        after=hashlib.sha256(bytes(self.uc.mem_read(CHAR_BASE,UNITS-CHAR_BASE-0x90))).hexdigest()
        if before != after:
            raise RuntimeError('combat derivation changed persistent character bytes')
        result.update(combat_records=deepcopy(self.combat_records),work_resets=deepcopy(self.work_resets),
            persistent_character_sha256=before,combat_records_prepared=result['ready'],
            combat_units_ready=result['ready'],battle_world_constructed=False,
            resource_loading_executed=False)
        if result['ready']:
            expected=result['prepared']['rounds'][0]['student_ids']
            if [r['input']['character_id'] for r in self.combat_records] != expected or len(self.work_resets)!=1:
                raise RuntimeError('source records do not match current first round')
        return result

    def probe_limits(self,name,identity,attributes,level,skills):
        at=CHAR_BASE+identity*CHAR_STRIDE
        old=bytes(self.uc.mem_read(at,CHAR_STRIDE))
        if len(attributes)!=7 or len(skills)!=8 or any(not 0 <= a <=255 for a in attributes) \
                or not 0 <= level <=255 or any(s not in (0,20,29,31,57,59) for s in skills):
            raise ValueError('counterfactual outside bounded limits subset')
        for i,a in enumerate(attributes): self.write(at+0xC+8*i,a,'B')
        self.write(at+0x50,level,'B')
        for i,s in enumerate(skills): self.write(at+0x52+2*i,s,'H')
        self.combat_records=[]
        self.clear_trace('handoff_round')
        # 4B9340 is cdecl: the isolated driver checks the native RET's stack.
        sp=STACK+0xFF00
        for i,value in enumerate((RETURN,identity,0)): self.write(sp+4*i,value)
        self.uc.reg_write(UC_X86_REG_ESP,sp)
        self.uc.reg_write(UC_X86_REG_ECX,TASK)
        self.uc.emu_start(0x4B9340,RETURN,timeout=1_000_000,count=100_000)
        if self.uc.reg_read(UC_X86_REG_EIP)!=RETURN or self.uc.reg_read(UC_X86_REG_ESP)!=sp+4:
            raise RuntimeError('native cdecl combat probe did not return')
        result={'name':name,'declared_counterfactual_input':combat_input(self,identity),
            'record':deepcopy(self.combat_records[0]),'coverage':self.coverage()}
        self.uc.mem_write(at,old)
        return result


def source_rules():
    image=SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest()!=SOURCE_SHA256: raise ValueError('source image differs')
    jobs=[]
    for identity in (6,7,10):
        raw=image[0x6B2D88-BASE+identity*64:0x6B2D88-BASE+(identity+1)*64]
        jobs.append({'job_id':identity,'record_hex':raw.hex(),'record_sha256':hashlib.sha256(raw).hexdigest(),
            'hp_coefficient':struct.unpack_from('<H',raw,6)[0],
            'hp_recovery_base':struct.unpack_from('<H',raw,8)[0],
            'mp_coefficient':struct.unpack_from('<H',raw,10)[0],
            'mp_recovery_base':struct.unpack_from('<H',raw,12)[0]})
    skills=[]
    for identity in (20,29,31,57,59):
        raw=image[0x6C2DC8-BASE+identity*72:0x6C2DC8-BASE+(identity+1)*72]
        skills.append({'skill_id':identity,'record_hex':raw.hex(),'record_sha256':hashlib.sha256(raw).hexdigest(),
            'modifier_callback':struct.unpack_from('<I',image,0x738998-BASE+identity*4)[0]})
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'supported_jobs':[6,7,10],
        'supported_skills':[0,20,29,31,57,59],'items':'zero_slots_only','jobs':jobs,'skills':skills,
        'engagement_minutes':list(struct.unpack_from('<51i',image,0x6E4528-BASE)),
        'half_coefficient':struct.unpack_from('<d',image,0x5A0CC0-BASE)[0],
        'work_reset':{'function':'0x4dab10','target':'0x8093f8','size':666},
        'functions':['0x4b9340','0x4b93c0','0x4db340','0x4dcf00','0x56cfcc'],**AUTHORITY}


def report():
    e=SchoolCombatRecordsEmulator()
    upstream=e.run_planning('combat_records_upstream')
    if not upstream['school_data_prepared']:raise RuntimeError('missing actual fifth school')
    ranges=[(BASE,(SOURCE.stat().st_size+0xFFF)&~0xFFF),(TASK,0x120000),(GROUP_TASK,0x60000),(STACK,0x10000)]
    checkpoint=[(a,bytes(e.uc.mem_read(a,n))) for a,n in ranges];cpu=e.uc.context_save()
    cases=[]
    for name,commands in [('initial',()),('student9_waiting',[('student',9,-1)]),
        ('fifth_class',[('teacher',101,4),('student',3,4,0),('student',4,4,1),('student',9,-1)]),
        ('teacher_only',[('student',3,-1),('student',4,-1),('student',9,-1)]),('teacher_waiting',[('teacher',101,-1)])]:
        for address,data in checkpoint:e.uc.mem_write(address,data)
        e.uc.context_restore(cpu)
        cases.append(e.handoff(name,commands))
        print('Native combat records '+name+': '+str(len(cases[-1]['combat_records'])),flush=True)
    probes=[e.probe_limits('clamped_attributes_level',3,[0,255,1,135,50,255,0],255,[0]*8),
        e.probe_limits('lowest_without_skills',4,[1]*7,0,[0]*8),
        e.probe_limits('max_attributes_repeated_verified_skills',9,[135]*7,50,[59,31,20,29,57,59,31,29])]
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,
        'evidence_kind':'actual_fifth_school_native_work_reset_and_complete_student_combat_records',
        'upstream':{'school_data_prepared':True,'state_requests':upstream['state_requests']},
        'source_rules':source_rules(),'cases':cases,'counterfactuals':probes,
        'limitations':['Same actual fifth-school checkpoint, with inherited confirmation/menu/scheduler boundaries.',
            'Original work reset, skill composition, record derivation and floating conversion execute.',
            'Current items are zero; item handlers and other jobs/skills are outside the verified subset.',
            'Counterfactual probes explicitly replace isolated attributes/level/skills and restore role bytes.',
            'Pending16 remains: no resource loader, tactical constructor, event simulation or live battlefield.'],**AUTHORITY}


def fixture(data):
    if hashlib.sha256(EVIDENCE.read_bytes()).hexdigest()!=EVIDENCE_SHA256 \
            or hashlib.sha256(report_text(data).encode()).hexdigest()!=EVIDENCE_SHA256:
        raise ValueError('frozen combat records evidence differs')
    return {'schema_version':1,'source_report_sha256':hashlib.sha256(report_text(data).encode()).hexdigest(),
        'cases':[{k:deepcopy(c[k]) for k in ('name','commands','ready','before','combat_records',
            'combat_records_prepared','battle_world_constructed','work_resets')} for c in data['cases']],
        'counterfactuals':[{k:deepcopy(c[k]) for k in ('name','declared_counterfactual_input','record')} for c in data['counterfactuals']],**AUTHORITY}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',required=True)
    args=parser.parse_args();path=ROOT/args.out
    if path.exists():parser.error('use a new evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
