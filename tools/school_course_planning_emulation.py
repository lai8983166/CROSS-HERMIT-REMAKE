"""Execute original mode menu/course clicks; calendar values are declared examples."""
import argparse
from copy import deepcopy
import hashlib
import struct

from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.new_game_school_movement_emulation import NewGameMovementEmulator, work_rules, patch
from tools.school_student_movement_emulation import WRITE_RANGES
from tools.school_teacher_movement_emulation import WORK_WRITE_RANGES
from tools.new_game_school_emulation import origin_rules, course_rules
from tools.school_course_unlock_emulation import AUTHORITY
from tools.tactics_exit_emulation import ROOT, TASK, STACK, report_text

NATIVE = ((0x4A3CA0,0x4A45AB),(0x4A2DA0,0x4A3240),(0x4A8BC0,0x4A8BF0))
BOUNDARIES = {0x4AA4B0:('declared_menu_command',0),0x4AA590:('button_feedback',4),
    0x4AA6C0:('course_name_presentation',24),0x4D64D0:('course_detail_select',8),
    0x4D62F0:('course_detail_draw',12)}


class CoursePlanningEmulator(NewGameMovementEmulator):
    def __init__(self):
        super().__init__()
        self._function_ranges += NATIVE
        self._stubs.update(BOUNDARIES)
        self.menu_command = None
        self.course_click = None
        self.write(0x7D598A,0,'B')
        self.write(TASK+0x1290,-1,'h')
        self.write(TASK+0x1292,-1,'h')

    def _write_hook(self,uc,access,address,size,value,context):
        if self.stage in ('mode','course','planning_rate'):
            if STACK <= address and address+size <= STACK+0x10000:
                return
            allowed = WRITE_RANGES+WORK_WRITE_RANGES+((0x7D598A,0x7D598B),(TASK+0x1290,TASK+0x1294))
            if not any(a <= address and address+size <= b for a,b in allowed):
                raise RuntimeError(f'planning write outside finite guard: {address:#x}/{size}')
            self.writes.append((address,size,value & ((1 << (size*8))-1)))
            return
        return super()._write_hook(uc,access,address,size,value,context)

    def _hook(self,uc,address,size,context):
        if address == 0x4D5EC0 and self.stage == 'course':
            sp = uc.reg_read(UC_X86_REG_ESP)
            pointer,x,y,w,h = struct.unpack('<5I',uc.mem_read(sp+4,20))
            ordinal = self.course_click['row']
            hit = (x,y,w,h) == (664+121*(ordinal%2),446+23*(ordinal//2),112,22)
            clicked = hit and self.course_click['clicked']
            # Mouse flags are pointer+4; the hit word is pointer+12.
            uc.mem_write(pointer,struct.pack('<3IH',0,int(clicked),0,int(hit)))
            self.stub_calls['declared_course_click'] += 1
            self.boundaries.append({'boundary':'declared_course_click','rectangle':[x,y,w,h],
                                    'hit':hit,'clicked':clicked})
            self._stub_return(0,20)
            return
        if address not in BOUNDARIES:
            return super()._hook(uc,address,size,context)
        name,pop = BOUNDARIES[address]
        self.stub_calls[name] += 1
        self.boundaries.append({'boundary':name})
        self._stub_return(self.menu_command if address == 0x4AA4B0 else 0,pop)

    def planning_snapshot(self):
        return self.movement_snapshot() | {'course_category':self.read(0x7D598A,'B'),
            'detail_work_id':self.read(TASK+0x1290,'h'),
            'detail_previous_work_id':self.read(TASK+0x1292,'h')}

    def declare_date(self,month,week):
        self.write(0x7A528E,month,'h')
        self.write(0x7A5290,week,'h')
        phases = self.prepare()
        return {'declared_date':[month,week],'after':self.planning_snapshot(),
                'ratings':phases[-1]['ratings'],
                'preparation':[{'phase':r['phase'],'coverage':r['coverage']} for r in phases]}

    def run(self,name,kind,*,group=0,teaching=True,category=0,row=0,page=0,clicked=True):
        self.call(0x4A8B50,(group,))
        if kind == 'mode':
            self.menu_command = group+(6 if teaching else 1)
            command = {'kind':'mode','group':group,'teaching':teaching}
        else:
            self.write(0x7D598A,category,'B')
            self.write(0x7D6A1A+category*2,page,'h')
            self.course_click = {'row':row,'clicked':clicked}
            command = {'kind':'course','group':group,'category':category,'row':row,'page':page,'clicked':clicked}
        before = self.planning_snapshot()
        self.clear_trace(kind)
        self.call(0x4A3CA0 if kind == 'mode' else 0x4A2DA0)
        after = self.planning_snapshot()
        operation = {'changed_fields':patch(before,after),'coverage':self.coverage()}
        self.clear_trace('planning_rate')
        ratings = [r['defined'] for r in self.rate()]
        final = self.planning_snapshot()
        return {'name':name,'command':command,'before':before,'operation':operation,
            'rating':{'changed_fields':patch(after,final),'ratings':ratings,'coverage':self.coverage()},
            'canonical_after':self.school_snapshot()}


def report():
    e = CoursePlanningEmulator()
    initialized = e.initialize()
    first = e.declare_date(4,4)
    cases = [e.run('teaching','mode'),e.run('first_course','course',row=0),
        e.run('replace_course','course',row=2),e.run('hover_only','course',row=1,clicked=False),
        e.run('adventure','mode',teaching=False),e.run('adventure_click_ignored','course',row=1),
        e.run('teaching_again','mode'),e.run('empty_category','course',category=1),
        e.run('second_course','course',row=1),e.run('same_course','course',row=1)]
    e.write(0x7A55FA,1,'h')
    cases.append(e.run('gate_forces_adventure','mode'))
    e.write(0x7A55FA,0,'h')
    cases.append(e.run('gate_cleared_teaching','mode'))
    middle = e.declare_date(6,5)
    cases.append(e.run('middle_course','course',category=1))
    late = e.declare_date(11,5)
    cases.append(e.run('advanced_course','course',category=2))
    cases.append(e.run('basic_after_advanced','course',category=0,row=8))
    return {'schema_version':1,'evidence_kind':'isolated_source_class_mode_and_course_click',
        'origin_rules':origin_rules(),'course_rules':course_rules(),'work_rules':work_rules(),
        'initialized':initialized['after'],'initialization_coverage':initialized['coverage'],
        'date_checkpoints':[first,middle,late],'cases':cases,
        'limitations':['Dates4/4,6/5,11/5 are explicit inputs, not executed calendar/ADV progression.',
            'Source student templates, menu commands, mouse hits and presentation are declared boundaries.',
            'Mode menu and course click bodies execute; invalid caller states are refused by the port.',
            'No teaching completion, growth settlement, saves or full original school menu.'],**AUTHORITY}


def fixture(data):
    value = deepcopy(data)
    value['source_report_sha256'] = hashlib.sha256(report_text(data).encode()).hexdigest()
    value.pop('initialization_coverage')
    for row in value['cases']:
        row['operation'].pop('coverage')
        row['rating'].pop('coverage')
    for date in value['date_checkpoints']:
        date.pop('preparation')
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True)
    parser.add_argument('--godot-out',required=True)
    args = parser.parse_args()
    paths = [ROOT/args.out,ROOT/args.godot_out]
    if paths[0].resolve() == paths[1].resolve() or any(p.exists() for p in paths):
        parser.error('use two different new output paths')
    data = report()
    for path,value in zip(paths,[data,fixture(data)]):
        payload = report_text(value)
        with path.open('x',encoding='utf-8',newline='\n') as handle:
            handle.write(payload)
        print(f'{path}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
