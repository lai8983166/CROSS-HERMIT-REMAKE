"""Continuous native grouping from complete source-backed new-game initialization."""
import argparse
from copy import deepcopy
import hashlib
import struct

from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.new_game_school_emulation import NewGameSchoolEmulator, origin_rules
from tools.school_student_movement_emulation import NATIVE, BOUNDARIES, WRITE_RANGES, patch
from tools.school_teacher_movement_emulation import WORK_WRITE_RANGES, source_rules as legacy_work_rules
from tools.school_waitlist_emulation import category_rules
from tools.school_course_unlock_emulation import AUTHORITY
from tools.tactics_exit_emulation import ROOT, TASK, STACK, report_text

CONTROLS = {'idle_sort_mode':(0x7D57DA,'B'), 'teacher_sort_mode':(0x7D58AA,'B'),
    'drag_kind':(0x7D598E,'b'), 'drag_origin':(0x7D598F,'b'),
    'drag_group':(0x7D5990,'h'), 'drag_slot':(0x7D5992,'h'),
    'drag_id':(0x7D5994,'h'), 'drag_source_rank':(0x7D5996,'h'),
    'task_drag_state':(TASK+0x76C2,'B'), 'task_command':(TASK+0x76C6,'h')}


def work_rules():
    source = origin_rules()
    result = legacy_work_rules()
    teacher = source['member_profiles'][0]
    result['teacher_profiles'] = [{'teacher_id':101, **{k:teacher[k] for k in ('job','level_50','attributes')}}]
    result['origin_fields_sha256'] = source['origin_fields_sha256']
    return result


class NewGameMovementEmulator(NewGameSchoolEmulator):
    def __init__(self):
        super().__init__()
        self._function_ranges += NATIVE
        self._stubs.update(BOUNDARIES)
        self.command = None

    def _write_hook(self,uc,access,address,size,value,context):
        if self.stage in ('movement','move_reconcile','move_rate'):
            if STACK <= address and address+size <= STACK+0x10000:
                return
            if not any(a <= address and address+size <= b for a,b in WRITE_RANGES+WORK_WRITE_RANGES):
                raise RuntimeError(f'movement write outside finite guard: {address:#x}/{size}')
            self.writes.append((address,size,value & ((1 << (size*8))-1)))
            return
        return super()._write_hook(uc,access,address,size,value,context)

    def _hook(self,uc,address,size,context):
        if address not in BOUNDARIES:
            return super()._hook(uc,address,size,context)
        name,pop = BOUNDARIES[address]
        self.stub_calls[name] += 1
        sp = uc.reg_read(UC_X86_REG_ESP)
        event = {'boundary':name}
        if address == 0x4D5C40:
            uc.mem_write(self.read(sp+4),struct.pack('<4I',int(not self.command['released']),0,0,0))
            event['released'] = self.command['released']
        elif address == 0x4D5EC0:
            pointer,x,y,width,height = struct.unpack('<5I',uc.mem_read(sp+4,20))
            group = self.command['target_group']
            left = 16 if self.command['kind'] == 'teacher' else 224+78*self.command['target_slot']
            hit = group >= 0 and (x,y,width,height) == (left,83+97*group,68,64)
            uc.mem_write(pointer,struct.pack('<3IH',0,0,0,int(hit)))
            event.update(rectangle=[x,y,width,height],hit=hit)
        elif address == 0x4D48A0:
            event['arguments_low16'] = [self.read(sp+4+4*i) & 65535 for i in range(4)]
        self.boundaries.append(event)
        uc.reg_write(UC_X86_REG_EAX,0)
        uc.reg_write(UC_X86_REG_ESP,sp+4+pop)
        uc.reg_write(UC_X86_REG_EIP,self.read(sp))

    def movement_snapshot(self):
        result = self.school_snapshot()
        result.update({key:self.read(*spec) for key,spec in CONTROLS.items()})
        result['teacher_work_records'] = {'101':[
            {'slot':i,'enabled':self.read(0x7A5BCA+10*i,'B'),
             'blocked':self.read(0x7A5BCB+10*i,'B'),'work_id':self.read(0x7A5BCC+10*i,'h')}
            for i in range(100) if any(self.uc.mem_read(0x7A5BCA+10*i,10))]}
        return result

    def run_move(self,name,kind,identity,target_group,target_slot=-1,released=True):
        old = self.school_snapshot()
        waiting = old['idle_teacher_ids' if kind == 'teacher' else 'idle_student_ids']
        source,slot = -1,waiting.index(identity) if identity in waiting else -1
        if slot == -1:
            for group in range(5):
                if kind == 'teacher' and self.read(0x7AAA12+28*group,'h') == identity:
                    source,slot = group,-1
                    break
                if kind == 'student':
                    for cell in range(4):
                        if self.read(0x7AAA12+28*group+16+2*cell,'h') == identity:
                            source,slot = group,cell
                            break
                    if source >= 0:
                        break
        if source == -1 and slot == -1:
            raise ValueError('member absent from current source school')
        self.command = {'kind':kind, kind+'_id':identity, 'source_group':source,'source_slot':slot,
                        'target_group':target_group,'released':released}
        if kind == 'student':
            self.command['target_slot'] = target_slot
        rating = self.rate()[source]['defined']['relationship_rank'] if source >= 0 else 0
        controls = {'idle_sort_mode':0,'teacher_sort_mode':0,'drag_kind':int(kind == 'teacher'),
                    'drag_origin':int(source >= 0),'drag_group':source,'drag_slot':slot,'drag_id':identity,
                    'drag_source_rank':rating,'task_drag_state':1,'task_command':14}
        for key,value in controls.items():
            self.write(CONTROLS[key][0],value,CONTROLS[key][1])
        before = self.movement_snapshot()
        phases = []
        for stage,address in [('movement',0x4A4680),('move_reconcile',0x4A5F40),('move_rate',None)]:
            self.clear_trace(stage)
            ratings = None
            if address:
                self.call(address)
            else:
                ratings = [r['defined'] for r in self.rate()]
            after = self.movement_snapshot()
            phase = {'phase':stage,'changed_fields':patch(before if not phases else previous,after),
                     'coverage':self.coverage()}
            if ratings is not None:
                phase['ratings'] = ratings
            phases.append(phase)
            previous = after
        return {'name':name,'command':deepcopy(self.command),'before':before,'phases':phases,
                'canonical_after':self.school_snapshot()}


def report():
    emulator = NewGameMovementEmulator()
    initialized = emulator.initialize()
    prepared = emulator.prepare()[-1]
    sequence = [
        ('student_exchange','student',3,0,1), ('student_empty','student',4,0,3),
        ('student_outside','student',9,-1), ('waiting_replace','student',9,0,1),
        ('waiting_empty','student',3,0,0), ('teacher_empty','teacher',101,1),
        ('teacher_held','teacher',101,2,-1,False), ('teacher_outside','teacher',101,-1),
        ('teacher_waiting_outside','teacher',101,-1), ('teacher_waiting_empty','teacher',101,4),
        ('rejoin_student3','student',3,4,0), ('rejoin_student4','student',4,4,1),
        ('waiting_teacherless','student',9,0,0), ('student_held','student',9,4,2,False),
        ('rejoin_student9','student',9,4,2), ('class_teacherless','student',3,0,0),
        ('waiting_fill_last','student',3,4,3), ('teacher_same_group','teacher',101,4),
        ('teacher_back_to_first','teacher',101,0), ('student_back_to_first','student',3,0,0),
    ]
    cases = [emulator.run_move(*args) for args in sequence]
    return {'schema_version':1,'evidence_kind':'source_initialized_continuous_school_movement',
        'origin_rules':origin_rules(),'sort_rules':category_rules(),'work_rules':work_rules(),
        'prepared':prepared['after'],'initialization_coverage':initialized['coverage'],
        'prepared_ratings':prepared['ratings'],'cases':cases,
        'limitations':['Same isolated CPU executes initializer, preparation and continuous moves.',
            'Student templates and mouse/release/presentation boundaries remain declared inputs.',
            'Held probes explicitly receive cleanup/rating; prototype command API publishes releases only.',
            'No original menu chronology, saves or returned-campaign teacher migration.'],**AUTHORITY}


def fixture(data):
    result = deepcopy(data)
    result['source_report_sha256'] = hashlib.sha256(report_text(data).encode()).hexdigest()
    result.pop('initialization_coverage')
    for row in result['cases']:
        for phase in row['phases']:
            phase.pop('coverage')
    return result


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
