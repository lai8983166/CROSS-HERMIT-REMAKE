"""Native course confirmation fields after source growth; no MVP/ADV/week."""
import argparse
from copy import deepcopy
import hashlib
import struct

from unicorn.x86_const import UC_X86_REG_ESP
from tools.school_course_settlement_emulation import CourseSettlementEmulator, IDS, flatten
from tools.new_game_school_emulation import CHAR, STRIDE
from tools.battle_preparation_emulation import PACKAGE_BASE, PACKAGE_STRIDE
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256, TASK, STACK, report_text
from tools.school_course_unlock_emulation import AUTHORITY

NATIVE = ((0x4C1350,0x4C1910),(0x4BF9E0,0x4BFFC0),(0x4D3960,0x4D3A20))


def source_rules():
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError('source differs')
    fields = {'job_categories':[image[0x6B2D8A+job*64-0x400000] for job in range(31)],
        'initial_records':[{'character_id':identity,
            'job_progress':[0]+[max(0,min(100,n)) for n in struct.unpack_from('<32h',image,0x751242+identity*66-0x400000)],
            'week_records':[0]*177} for identity in IDS]}
    signature = ':'.join(map(str,flatten(fields)))
    return {'source_image_sha256':SOURCE_SHA256,
        'confirmation_fields_sha256':hashlib.sha256(signature.encode()).hexdigest(),**fields}


class CourseConfirmationEmulator(CourseSettlementEmulator):
    def __init__(self):
        super().__init__()
        self._function_ranges += NATIVE
        self.relationship_calls = []

    def _write_hook(self,uc,access,address,size,value,context):
        if self.stage != 'course_confirmation':
            return super()._write_hook(uc,access,address,size,value,context)
        if STACK <= address and address+size <= STACK+0x10000:
            return
        allowed = [(TASK+0x1138,TASK+0x136E)]
        for identity in IDS:
            base = PACKAGE_BASE+identity*PACKAGE_STRIDE
            job = self.read(CHAR+identity*STRIDE+6,'h')
            allowed += [(base+0xD7+job,base+0xD8+job),(base+0x24+9,base+0x24+12)]
        for relation in self.origin['relationships']:
            a = relation['from']-55 if relation['from'] > 100 else relation['from']
            b = relation['to']-55 if relation['to'] > 100 else relation['to']
            at = 0x7D3D71+a*68+b
            allowed.append((at,at+1))
        if not any(a <= address and address+size <= b for a,b in allowed):
            raise RuntimeError(f'confirmation write outside finite guard: {address:#x}/{size}')
        self.writes.append((address,size,value & ((1 << (size*8))-1)))

    def _hook(self,uc,address,size,context):
        if getattr(self,'stage',None) == 'course_confirmation' and address == 0x4D3960:
            sp = uc.reg_read(UC_X86_REG_ESP)
            self.relationship_calls.append({'from':self.read(sp+4,'h'),'to':self.read(sp+8,'h'),
                'delta':self.read(sp+12,'h')})
        return super()._hook(uc,address,size,context)

    def confirmation_records(self):
        return [{'character_id':identity,
            'job_progress':list(self.uc.mem_read(PACKAGE_BASE+identity*PACKAGE_STRIDE+0xD7,33)),
            'week_records':list(self.uc.mem_read(PACKAGE_BASE+identity*PACKAGE_STRIDE+0x24,177))} for identity in IDS]

    def confirm(self):
        before,records = self.school_snapshot(),self.confirmation_records()
        growth = self.growth_records()
        self.clear_trace('course_confirmation')
        self.relationship_calls.clear()
        self.call(0x4C1350,receiver=TASK)
        after = self.school_snapshot()
        after_records = self.confirmation_records()
        coverage = self.coverage()
        self.clear_trace('planning_rate')
        ratings = [r['defined'] for r in self.rate()]
        return {'before':before,'before_records':records,'growth_records':growth,
            'after':after,'after_records':after_records,'after_growth_records':self.growth_records(),
            'relationship_calls':deepcopy(self.relationship_calls),'confirmation_coverage':coverage,
            'rated_after':self.school_snapshot(),'ratings':ratings,'rating_coverage':self.coverage()}


def make_case(name,course=10,*,waiting=(),group=0,probe=None):
    e = CourseConfirmationEmulator()
    e.initialize()
    initial = e.confirmation_records()
    e.declare_date(4,4)
    for identity in waiting:
        e.run_move('declared_waiting','student',identity,-1)
    if group:
        e.run_move('declared_teacher_move','teacher',101,group)
        for slot,identity in enumerate(IDS):
            e.run_move('declared_student_join','student',identity,group,slot)
    e.run('teaching','mode',group=group)
    e.run('assign','course',group=group,row={12:0,11:1,10:2}[course])
    growth = e.settle(name)
    if probe:
        # Explicit post-growth job/level inputs exercise both waiting-peer bonuses.
        e.write(CHAR+9*STRIDE+6,6,'h')
        for identity,value in zip(IDS,(99,100,127)):
            job = e.read(CHAR+identity*STRIDE+6,'h')
            e.write(PACKAGE_BASE+identity*PACKAGE_STRIDE+0xD7+job,value,'B')
            e.uc.mem_write(PACKAGE_BASE+identity*PACKAGE_STRIDE+0x24+9,bytes((7,8,9)))
        # Explicit post-growth counterfactual: waiting peers have equal level.
        e.write(CHAR+9*STRIDE+0x50,8,'B')
        for relation in e.origin['relationships']:
            a = relation['from']-55 if relation['from'] > 100 else relation['from']
            b = relation['to']-55 if relation['to'] > 100 else relation['to']
            e.write(0x7D3D71+a*68+b,100 if a == 3 else 1,'B')
    return {'name':name,'setup':{'course_id':course,'waiting_students':list(waiting),'group':group,
            'counterfactual':probe},'initial_records':initial,
        'growth_checkpoint':growth['after'],'growth_coverage':growth['settlement_coverage'],
        **e.confirm(),**AUTHORITY}


def report():
    return {'schema_version':1,'evidence_kind':'isolated_source_course_confirmation_fields',
        'rules':source_rules(),'cases':[
            make_case('course10_confirmation'),make_case('course12_confirmation',12),
            make_case('waiting9_confirmation',waiting=(9,)),
            make_case('two_waiting_confirmation',waiting=(4,9)),
            make_case('fifth_class_confirmation',group=4),
            make_case('signed_career_relationship_and_history_probe',waiting=(4,9),probe='post_growth_caps')],
        'limitations':['4/4 date, mode0, seed4660, zero result task and presentation/resource inputs are declared.',
            'Native4C1350/4BF9E0/4D3960 execute after original initialization/planning/growth in one CPU.',
            'Confirmation button/MVP VM, recipient count/rewards, ADV and weekly progression do not execute.',
            'The final named case explicitly modifies post-growth inputs and is counterfactual.',
            'No live menu witness, full school chronology or original save authority.'],**AUTHORITY}


def fixture(data):
    value = deepcopy(data)
    value['source_report_sha256'] = hashlib.sha256(report_text(data).encode()).hexdigest()
    for case in value['cases']:
        for key in ('growth_coverage','confirmation_coverage','rating_coverage'):
            case.pop(key)
    return value


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out')
    p.add_argument('--godot-out')
    p.add_argument('--rules-out')
    a = p.parse_args()
    if a.rules_out and not a.out and not a.godot_out:
        outputs = [(ROOT/a.rules_out,source_rules())]
    elif a.out and a.godot_out and not a.rules_out:
        paths = [ROOT/a.out,ROOT/a.godot_out]
        if paths[0].resolve() == paths[1].resolve() or any(path.exists() for path in paths):
            p.error('use different new output paths')
        data = report()
        outputs = list(zip(paths,(data,fixture(data))))
    else:
        p.error('use --rules-out alone, or --out with --godot-out')
    for path,value in outputs:
        if path.exists():
            p.error('use a new output path')
        payload = report_text(value)
        with path.open('x',encoding='utf-8',newline='\n') as f:
            f.write(payload)
        print(f'{path}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
