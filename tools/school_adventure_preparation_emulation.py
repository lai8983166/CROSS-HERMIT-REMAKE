"""Same fifth-week CPU executes native departure readiness and squad preparation.

Full menu timing, UI input and state10/battle execution remain explicit boundaries.
"""
import argparse
from copy import deepcopy
import hashlib
import struct

from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP
from tools.school_fifth_planning_emulation import SchoolFifthPlanningEmulator
from tools.new_game_school_movement_emulation import NewGameMovementEmulator
from tools.tactics_exit_emulation import ExitEmulator, ROOT, SOURCE, SOURCE_SHA256, TASK, STACK, report_text
from tools.new_game_school_emulation import STATE, STATE_SIZE
from tools.battle_preparation_emulation import PACKAGE_BASE, PACKAGE_STRIDE
from tools.school_course_unlock_emulation import AUTHORITY

NATIVE = ((0x4A7D30,0x4A8110),(0x4A6A10,0x4A6F90))
EVIDENCE = ROOT/'analysis/school-adventure-preparation-v1-20261008.json'
EVIDENCE_SHA256 = '9149611a96178d9412acdb4c4a36c20bca899eb367ad5705f188a7882ec8ddff'


class SchoolAdventurePreparationEmulator(SchoolFifthPlanningEmulator):
    def __init__(self):
        super().__init__()
        self._function_ranges += NATIVE

    def _write_hook(self,uc,access,address,size,value,context):
        if getattr(self,'stage',None) not in ('departure_rate','departure_ready','departure_rounds'):
            return super()._write_hook(uc,access,address,size,value,context)
        if STACK <= address and address+size <= STACK+0x10000:
            return
        if address < 0x7A5292 and address+size > 0x7A528E:
            raise RuntimeError('departure write outside finite guard: calendar')
        if address < PACKAGE_BASE+45*PACKAGE_STRIDE and address+size > PACKAGE_BASE:
            raise RuntimeError('departure write outside finite guard: role package/MVP')
        allowed = ((STATE,STATE+STATE_SIZE),(TASK+0xA0000,TASK+0xA00A0))
        if not any(a <= address and address+size <= b for a,b in allowed):
            raise RuntimeError(f'departure write outside finite guard: {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
        self.writes.append((address,size,value & ((1 << (size*8))-1)))

    def _hook(self,uc,address,size,context):
        if getattr(self,'stage',None) in ('movement','move_reconcile','move_rate'):
            # Course-result ancestors own a different button-input phase.
            return NewGameMovementEmulator._hook(self,uc,address,size,context)
        if getattr(self,'stage',None) in ('departure_rate','departure_ready','departure_rounds'):
            return ExitEmulator._hook(self,uc,address,size,context)
        return super()._hook(uc,address,size,context)

    def round_snapshot(self):
        count = self.read(0x7A5298,'h')
        if not 0 <= count <= 5:
            raise RuntimeError('round count outside source capacity')
        rows = []
        for i in range(count):
            base = 0x7A529A+0x70*i
            students = self.read(base+0x5E,'h')
            teachers = self.read(base+0x6A,'h')
            if not 0 <= students <= 20 or not 0 <= teachers <= 5:
                raise RuntimeError('squad count outside source capacity')
            rows.append({'scene_id':self.read(base+0x6E,'h'),
                'student_ids':[self.read(base+0x36+2*j,'h') for j in range(students)],
                'student_groups':[self.read(base+0xE+2*j,'h') for j in range(students)],
                'teacher_ids':[self.read(base+0x60+2*j,'h') for j in range(teachers)]})
        # Only defined rating fields: unused native stack words are not outputs.
        ratings = []
        for i in range(5):
            words = list(struct.unpack('<7h',self.uc.mem_read(0x7A529A+0x70*i,14)))
            ratings.append({'state':words[0],
                'relationship_mean':words[1] if words[0] not in (0,1) else 0,
                'relationship_rank':words[2] if words[0] not in (0,1) else 0,
                'work_fields':words[3:] if words[0] in (2,4) else []})
        return {'adventure_id':self.read(0x7A5294,'h'),'round_index':self.read(0x7A5296,'h'),
            'round_count':count,'class_ratings':ratings,'rounds':rows}

    def probe(self,name,commands=()):
        self.phase = 'departure'
        moves = [self.run_move(name+'_'+str(i),*command) for i,command in enumerate(commands)]
        before = {'school':self.school_snapshot(),'roles':self.fifth_snapshot(),'counts':self.counts()}
        self.clear_trace('departure_rate')
        ratings = [x['defined'] for x in self.rate()]
        rate_coverage = self.coverage()
        self.clear_trace('departure_ready')
        self.call(0x4A7D30)
        ready = bool(self.uc.reg_read(UC_X86_REG_EAX) & 255)
        readiness_coverage = self.coverage()
        prepared = None
        if ready:
            self.clear_trace('departure_rounds')
            self.call(0x4A6A10)
            prepared = self.round_snapshot()
        after = {'school':self.school_snapshot(),'roles':self.fifth_snapshot(),'counts':self.counts()}
        if before != after:
            raise RuntimeError('departure unexpectedly changed school, role, date or counts')
        print('Native departure case: '+name+' ready='+str(ready),flush=True)
        return {'name':name,'commands':[{'kind':c[0],'member_id':c[1],'target_group':c[2],
            'target_slot':c[3] if len(c)>3 else -1} for c in commands],
            'movement_coverage':[{'command':m['command'],'phases':m['phases']} for m in moves],
            'before':before,'after':after,'class_ratings':ratings,'ready':ready,'prepared':prepared,
            'rating_coverage':rate_coverage,'readiness_coverage':readiness_coverage,
            'preparation_coverage':self.coverage() if ready else None}


def source_rules():
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError('source image differs')
    base = 0x73BED0-0x400000+5*0x100
    record = image[base:base+0x100]
    count = record[15]
    if not 1 <= count <= 5:
        raise ValueError('round count outside supported source record')
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'adventure_id':5,
        'required_date':[4,5],'mandatory_gate':1,'table_va':'0x73bed0','record_stride':256,
        'record_sha256':hashlib.sha256(record).hexdigest(),
        'round_specs':[{'scene_id':struct.unpack_from('<H',record,16+i*4)[0],
            'selection_word':struct.unpack_from('<H',record,18+i*4)[0]} for i in range(count)],
        'required_work_fields':[record[6]-1,record[7]-1,record[0],0],
        'functions':{'readiness':'0x4a7d30','prepare_rounds':'0x4a6a10'},**AUTHORITY}


def report():
    e = SchoolAdventurePreparationEmulator()
    upstream = e.run_planning('departure_upstream')
    if not upstream['school_data_prepared']:
        raise RuntimeError('missing actual same-CPU school initialization')
    cases = [e.probe('initial'),e.probe('student9_waiting',[('student',9,-1)]),
        e.probe('fifth_class',[('teacher',101,4),('student',3,4,0),('student',4,4,1)]),
        e.probe('teacher_only',[('student',3,-1),('student',4,-1)]),
        e.probe('teacher_waiting',[('teacher',101,-1)])]
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,
        'evidence_kind':'same_cpu_fifth_week_school_readiness_and_round_preparation',
        'upstream':{'school_data_prepared':True,'after':upstream['after'],
            'state_requests':upstream['state_requests'],'source_report':'school-fifth-planning-v2-20261008.json'},
        'source_rules':source_rules(),'cases':cases,
        'limitations':['Inherited actual 4/4 course/week/Chapter018/workroom/CH002/school initialization CPU.',
            'Native movement, reconciliation, rating, readiness and round preparation execute; mouse/release is declared input.',
            'No full menu timing, school commit, pending10, scene events, live battle, completion or reward.',
            'Undefined native stack words and unused buffer tails are excluded from defined preparation output.'],**AUTHORITY}


def exported_fixture(data):
    if hashlib.sha256(EVIDENCE.read_bytes()).hexdigest() != EVIDENCE_SHA256:
        raise ValueError('frozen departure evidence differs')
    return {'schema_version':1,'source_report_sha256':hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),
        'source_image_sha256':SOURCE_SHA256,'cases':[{k:deepcopy(c[k]) for k in
        ('name','commands','before','after','class_ratings','ready','prepared')} for c in data['cases']],**AUTHORITY}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True)
    args = parser.parse_args()
    path = ROOT/args.out
    if path.exists():
        parser.error('use a new evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
