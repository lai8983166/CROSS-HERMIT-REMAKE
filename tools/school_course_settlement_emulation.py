"""Execute assigned source classes through native course growth, without a week.

The date and clock seed are declared inputs. Native class result preparation,
all-result initialization, growth packet, skill rolls and attribute/level bodies
execute. Presentation and the earlier template loader retain explicit boundaries.
"""
import argparse
from copy import deepcopy
import hashlib
import struct

from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.school_course_planning_emulation import CoursePlanningEmulator
from tools.new_game_school_emulation import CHAR, STRIDE, origin_rules
from tools.battle_preparation_emulation import PACKAGE_BASE, PACKAGE_STRIDE, TLS
from tools.school_student_movement_emulation import WRITE_RANGES
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256, TASK, STACK, RETURN, report_text
from tools.school_course_unlock_emulation import AUTHORITY

NATIVE = ((0x4A6A10,0x4A6F80),(0x4C0400,0x4C0C10),(0x4D3600,0x4D3960))
IDS = (3,4,9)


def flatten(value):
    if isinstance(value,dict):
        return [n for v in value.values() for n in flatten(v)]
    if isinstance(value,list):
        return [n for v in value for n in flatten(v)]
    return [value]


def source_rules():
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError('source differs')
    def numbers(va,count,fmt='i'):
        return list(struct.unpack_from('<'+str(count)+fmt,image,va-0x400000))
    skills,grid = [],[[0]*7 for _ in range(12)]
    for sid in range(1,85):
        at = 0x6C2DCC+sid*72-0x400000
        category,position = image[at],image[at+3]
        if category and 1 <= position <= 7:
            grid[category-1][position-1] = sid
        skills.append({'minimum_attributes':numbers(0x74F686+sid*50,7,'h'),
            'minimum_total':numbers(0x74F694+sid*50,1,'h')[0],
            'minimum_job_sums':numbers(0x74F696+sid*50,5,'h'),
            'learned_points':numbers(0x6C2E08+sid*72,1)[0]})
    fields = {'attribute_increments':numbers(0x6E4308,136),
        'level_thresholds':numbers(0x625300,50),'skill_grid':grid,
        'job_skill_caps':[list(image[0x6E4159+j*13-0x400000:0x6E4159+j*13-0x400000+11]) for j in range(31)],
        'skills':skills,'training':[{'package':numbers(0x74BEDC+i*96,8),
            'attribute_mask':numbers(0x74BEFC+i*96,7,'h'),
            'learning_rates':list(image[0x74BF1E+i*96-0x400000:0x74BF1E+i*96-0x400000+11])} for i in range(16)]}
    signature = ':'.join(map(str,flatten(fields)))
    return {'source_image_sha256':SOURCE_SHA256,
        'settlement_fields_sha256':hashlib.sha256(signature.encode()).hexdigest(),**fields}


def runtime_rules():
    rules = source_rules()
    image = SOURCE.read_bytes()
    sums = []
    for identity in IDS:
        progress = list(struct.unpack_from('<32h',image,0x751242+identity*0x42-0x400000))
        progress = [max(0,min(100,value)) for value in progress]
        sums.append({'character_id':identity,'job_sums':[
            sum(progress[2*k+offset] for offset in (0,1,10,11,20,21)) for k in range(5)]})
    signature = ':'.join(map(str,flatten(sums)))
    return rules | {'initial_job_sums':sums,'initial_job_sums_sha256':hashlib.sha256(signature.encode()).hexdigest()}


class CourseSettlementEmulator(CoursePlanningEmulator):
    def __init__(self, *, seed=4660):
        super().__init__()
        if type(seed) is not int or not 0 <= seed <= 0x7fffffff:
            raise ValueError('invalid declared clock seed')
        self.seed = seed
        self._function_ranges += NATIVE
        self.draws = []
        self.packet_events = []
        self.pending_draw = None

    def _write_hook(self,uc,access,address,size,value,context):
        if self.stage not in ('course_result_prepare','course_settlement'):
            return super()._write_hook(uc,access,address,size,value,context)
        if STACK <= address and address+size <= STACK+0x10000:
            return
        if self.stage == 'course_result_prepare':
            allowed = list(WRITE_RANGES)+[(0x7A5294,0x7A529A)]
            allowed += [(0x7A529A+112*g,0x7A52A8+112*g) for g in range(5)]
            allowed += [(0x7A5304+112*g,0x7A5306+112*g) for g in range(5)]
        else:
            allowed = [(TLS,TLS+0x1000),(0x7E1180,0x7E11A0),(0x7A511C,0x7A5120),
                       (TASK+0x34,TASK+0x38),(TASK+0x38,TASK+0xC30),
                       (TASK+0x136E,TASK+0x1430)]
            for identity in IDS:
                base = CHAR+identity*STRIDE
                allowed += [(base+0x50,base+0x51),(PACKAGE_BASE+identity*PACKAGE_STRIDE+0x20,
                            PACKAGE_BASE+identity*PACKAGE_STRIDE+0x24)]
                for k in range(7):
                    allowed += [(base+0xC+8*k,base+0xD+8*k),(base+0x10+8*k,base+0x14+8*k)]
                allowed += [(base+0xB8+12*k,base+0xB9+12*k) for k in range(84)]
        if not any(a <= address and address+size <= b for a,b in allowed):
            raise RuntimeError(f'{self.stage} write outside finite guard: {address:#x}/{size}')
        self.writes.append((address,size,value & ((1 << (size*8))-1)))

    def _hook(self,uc,address,size,context):
        if getattr(self,'stage',None) == 'course_settlement':
            sp = uc.reg_read(UC_X86_REG_ESP)
            if self.pending_draw is not None and address == self.pending_draw:
                self.draws.append(uc.reg_read(UC_X86_REG_EAX))
                self.pending_draw = None
            if address == 0x4D1CB0:
                if self.pending_draw is not None:
                    raise RuntimeError('overlapping random return')
                self.pending_draw = self.read(sp)
            if address == 0x4D3600:
                self.packet_events.append({'character_id':self.read(sp+8,'h'),
                    'training_id':self.read(sp+12,'h'),'coefficient':self.read(sp+16,'h'),
                    'output_pointer':self.read(sp+4),'return_va':self.read(sp)})
            for event in self.packet_events:
                if address == event['return_va'] and 'packet' not in event:
                    event['packet'] = list(struct.unpack('<8i',uc.mem_read(event['output_pointer'],32)))
        return super()._hook(uc,address,size,context)

    def growth_records(self):
        records = []
        for identity in IDS:
            base,pkg = CHAR+identity*STRIDE,PACKAGE_BASE+identity*PACKAGE_STRIDE
            records.append({'character_id':identity,'job':self.read(base+6,'h'),
                'attributes':[self.read(base+0xC+8*k,'B') for k in range(7)],
                'growth_pools':[self.read(base+0x10+8*k,'I') for k in range(7)],
                'level_50':self.read(base+0x50,'B'),
                'skill_statuses':[self.read(base+0xB8+12*k,'B') for k in range(84)],
                'job_sums':[sum(self.read(pkg+offset+2*k,'b') for offset in (0xD8,0xE2,0xEC))+
                            sum(self.read(pkg+offset+2*k,'b') for offset in (0xD9,0xE3,0xED)) for k in range(5)],
                'staged_total':self.read(pkg+0x20,'i')})
        return records

    def settle(self,name):
        before = self.school_snapshot()
        records = self.growth_records()
        self.clear_trace('course_result_prepare')
        self.call(0x4A6A10)
        prepared = [[self.read(0x7A529A+g*112+2*k,'h') for k in range(7)] for g in range(5)]
        preparation = self.coverage()
        self.clear_trace('course_settlement')
        self.draws.clear()
        self.packet_events.clear()
        # Fresh zero-filled task allocation and mode0 are declared result inputs.
        self.uc.mem_write(TASK+0x34,bytes(0x4F74-0x34))
        self.write(0x7F4491,0,'B')
        sp = STACK+0xFF00
        self.write(sp,RETURN)
        self.uc.reg_write(UC_X86_REG_ESP,sp)
        self.uc.reg_write(UC_X86_REG_ECX,TASK)
        self.uc.emu_start(0x4BD870,RETURN,timeout=20_000_000,count=4_000_000)
        if self.uc.reg_read(UC_X86_REG_EIP) != RETURN or self.uc.reg_read(UC_X86_REG_ESP) != sp+4:
            raise RuntimeError('course initialization did not return in bounds')
        packets = [{k:v for k,v in event.items() if k not in ('output_pointer','return_va')} for event in self.packet_events]
        return {'name':name,'declared_clock_seed':self.seed,'before':before,'before_records':records,
            'prepared_words':prepared,'preparation_coverage':preparation,
            'after':self.school_snapshot(),'after_records':self.growth_records(),
            'packets':packets,'learning_draws':self.draws,'rand_state':self.read(TLS+0x14),
            'bonus':self.read(TASK+0x34,'i'),'skill_display_needed':self.read(TASK+0x142C,'h'),
            'settlement_coverage':self.coverage(),**AUTHORITY}


def make_case(name,course,*,seed=4660,waiting=None,group=0,probe=None):
    e = CourseSettlementEmulator(seed=seed)
    e.initialize()
    e.declare_date(4,4)
    if waiting is not None:
        e.run_move('declared_move_to_waiting','student',waiting,-1)
    if group:
        e.run_move('declared_move_teacher','teacher',101,group)
        for slot,identity in enumerate(IDS):
            e.run_move('declared_rejoin_student','student',identity,group,slot)
    e.run('teaching','mode',group=group)
    row = {12:0,11:1,10:2}[course]
    e.run('assign','course',group=group,row=row)
    if probe == 'attribute_cap':
        pool = sum(source_rules()['attribute_increments'][:101])
        e.write(CHAR+3*STRIDE+0xC,100,'B')
        e.write(CHAR+3*STRIDE+0x10,pool)
    if probe == 'total_cap':
        # Keep each attribute below its cap, but fill the total growth budget.
        for k in range(7):
            pool = 1_300_000 if k < 6 else 690_000
            e.write(CHAR+3*STRIDE+0x10+8*k,pool)
            total = 0
            increments = source_rules()['attribute_increments']
            level = 1
            while total <= pool:
                total += increments[level]
                level += 1
            e.write(CHAR+3*STRIDE+0xC+8*k,max(1,level-2),'B')
    result = e.settle(name)
    result['setup'] = {'course_id':course,'group':group,'waiting_student':waiting,'counterfactual':probe}
    return result


def report():
    cases = [make_case('course12_three_students',12),make_case('course11_three_students',11),
        make_case('course10_three_students',10),make_case('course12_seed1',12,seed=1),
        make_case('course10_waiting_student',10,waiting=9),
        make_case('course10_fifth_class',10,group=4),
        make_case('course10_attribute_cap',10,probe='attribute_cap'),
        make_case('course10_total_cap',10,probe='total_cap')]
    return {'schema_version':1,'evidence_kind':'isolated_source_assigned_course_growth',
        'rules':source_rules(),'origin_rules':origin_rules(),'cases':cases,
        'limitations':['4/4 date and clock seeds are declared inputs, not calendar chronology.',
            'Fresh zero-filled result task, mode0 and presentation/resource boundaries are explicit.',
            'Native4A6A10 and4BD870 through4C0400/4D3600 execute; no result confirmation or week.',
            'Two named cap cases modify source student3 inputs and are counterfactual probes.',
            'No full original school menu, live scene, calendar advancement or save authority.'],**AUTHORITY}


def fixture(data):
    value = deepcopy(data)
    value['source_report_sha256'] = hashlib.sha256(report_text(data).encode()).hexdigest()
    value.pop('origin_rules')
    for case in value['cases']:
        case.pop('preparation_coverage')
        case.pop('settlement_coverage')
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out')
    parser.add_argument('--godot-out')
    parser.add_argument('--rules-out')
    args = parser.parse_args()
    if args.rules_out and not args.out and not args.godot_out:
        path = ROOT/args.rules_out
        if path.exists():
            parser.error('use a new rules output path')
        payload = report_text(runtime_rules())
        with path.open('x',encoding='utf-8',newline='\n') as handle:
            handle.write(payload)
        print(f'{path}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')
        return
    if not args.out or not args.godot_out or args.rules_out:
        parser.error('use --rules-out only, or both --out and --godot-out')
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
