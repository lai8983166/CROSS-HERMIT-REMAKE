"""Execute all of49E930 on declared source-loaded student templates.

The preceding template loader and full new-game/menu chronology are not run.
"""
import argparse
from copy import deepcopy
import hashlib
import struct

from unicorn import UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.school_teacher_group_emulation import TeacherGroupEmulator
from tools.school_student_movement_emulation import WRITE_RANGES
from tools.school_teacher_movement_emulation import WORK_NATIVE, WORK_WRITE_RANGES
from tools.school_course_unlock_emulation import (
    FLAGS, RECORDS, COUNTS, AUTHORITY, NATIVE as COURSE_NATIVE, source_rules as course_rules)
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256, STACK, RETURN, TASK, report_text

STATE, STATE_SIZE = 0x7A50E8, 0x306D4
CHAR, STRIDE = 0x7E17E8, 0x4A0
INIT_NATIVE = ((0x49E930,0x49EE30),(0x4D3D00,0x4D3E90),
               (0x4E1CA0,0x4E1D70),(0x4E3170,0x4E3210))
IDS = [101,3,4,9]
CALLS = [0x49EDA8,0x49EDB8,0x49EDC8,0x49EDD8]


def origin_rules():
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError('source differs')
    calls,profiles,relations,level_inputs = [],[],[],[]
    for address,identity,slot in zip(CALLS,IDS,[-1,0,1,2]):
        off = address-0x400000
        expected = bytes([0x6A,slot & 255,0x6A,0,0x6A,identity])
        if image[off-11:off-5] != expected or image[off] != 0xE8 or \
                address+5+struct.unpack_from('<i',image,off+1)[0] != 0x4D3E90:
            raise ValueError('initializer call bytes differ')
        calls.append({'call_va':address,'member_id':identity,'group':0,'slot':slot})
    for identity in IDS:
        off = 0x6F5088-0x400000+identity*STRIDE
        raw = image[off:off+STRIDE]
        profiles.append({'member_id':identity,'job':struct.unpack_from('<h',raw,6)[0],
            'level_50':raw[0x50],'attributes':[raw[0xC+8*i] for i in range(7)],
            'storage_kind':'static_teacher_template' if identity > 100 else 'student_record',
            'template_sha256':hashlib.sha256(raw).hexdigest()})
        if identity < 101:
            level_inputs.append({'member_id':identity,
                'growth_pools':[struct.unpack_from('<I',raw,0x10+8*i)[0] for i in range(7)],
                'skill_statuses':[raw[0xB8+12*i] for i in range(84)],
                'equipped_skills':list(struct.unpack_from('<8h',raw,0x52))})
    for a in IDS:
        for b in IDS:
            if a != b:
                row = a-55 if a > 100 else a
                column = b-55 if b > 100 else b
                relations.append({'from':a,'to':b,'value':image[0x74E4B0-0x400000+row*68+1+column]})
    encoded = ''.join(':'.join(map(str,[r[k] for k in ('call_va','member_id','group','slot')]))+';' for r in calls)
    encoded += '|'+''.join(':'.join(map(str,[p['member_id'],p['job'],p['level_50'],*p['attributes']]))+
                          ':'+p['storage_kind']+':'+p['template_sha256']+';' for p in profiles)
    encoded += '|'+''.join(f"{r['from']}:{r['to']}:{r['value']};" for r in relations)
    thresholds = list(struct.unpack_from('<50i',image,0x625300-0x400000))
    learned = [struct.unpack_from('<i',image,0x6C2E08-0x400000+sid*72)[0] for sid in range(1,85)]
    encoded += '|'+''.join(':'.join(map(str,[r['member_id'],*r['growth_pools'],
        *r['skill_statuses'],*r['equipped_skills']]))+';' for r in level_inputs)
    encoded += '|'+':'.join(map(str,thresholds))+'|'+':'.join(map(str,learned))
    return {'source_image_sha256':SOURCE_SHA256,'initializer_va':0x49E930,
            'calls':calls,'member_profiles':profiles,'relationships':relations,
            'student_level_inputs':level_inputs,'level_thresholds':thresholds,'learned_points':learned,
            'origin_fields_sha256':hashlib.sha256(encoded.encode()).hexdigest()}


class NewGameSchoolEmulator(TeacherGroupEmulator):
    def __init__(self, *, dirty=False):
        super().__init__(students=())
        self._function_ranges += INIT_NATIVE+COURSE_NATIVE+(WORK_NATIVE,)
        del self._stubs[0x4A2980]
        self._stubs[0x56CEC0] = ('bounded_new_game_state_memset',0)
        self.origin = origin_rules()
        self.stage = 'setup'
        # This represents the preceding template load, not an executed loader.
        for identity in range(45):
            self.uc.mem_write(CHAR+identity*STRIDE,bytes(self.uc.mem_read(0x6F5088+identity*STRIDE,STRIDE)))
        self.uc.mem_write(STATE,bytes([0xA5 if dirty else 0])*STATE_SIZE)
        # These UI/workspace controls are outside49E930 and explicitly declared.
        self.uc.mem_write(0x7D57D8,bytes(0x90))
        self.uc.mem_write(0x7D58AA,bytes(0x32))
        self.uc.mem_write(0x7D630C,bytes(0x71A))
        self.write(0x7D57D8,-1,'b')
        self.join_entries.clear()
        self.visited.clear()
        self.stub_calls.clear()
        self.writes,self.boundaries = [],[]
        self.uc.hook_add(UC_HOOK_MEM_WRITE,self._write_hook)

    def _hook(self,uc,address,size,context):
        if address == 0x56CEC0:
            sp = uc.reg_read(UC_X86_REG_ESP)
            target,byte,count = struct.unpack('<III',uc.mem_read(sp+4,12))
            if self.stage != 'initialize' or (target,byte,count) != (STATE,0,STATE_SIZE):
                raise RuntimeError('memset outside exact new-game state boundary')
            self.boundaries.append({'name':'bounded_new_game_state_memset',
                                    'target':hex(target),'byte':byte,'count':count,
                                    'caller_return_va':hex(self.read(sp))})
            self.stub_calls['bounded_new_game_state_memset'] += 1
            uc.mem_write(target,bytes(count))
            self._stub_return(target,0)
            return
        return super()._hook(uc,address,size,context)

    def _write_hook(self,uc,access,address,size,value,context):
        if STACK <= address and address+size <= STACK+0x10000:
            return
        if self.stage == 'initialize':
            ranges = [(STATE,STATE+STATE_SIZE),(0x7D6A34,0x7D6A36)]
            ranges += [(CHAR+i*STRIDE,CHAR+(i+1)*STRIDE) for i in (3,4,9)]
        else:
            ranges = list(WRITE_RANGES)+list(WORK_WRITE_RANGES)+[(FLAGS+1,FLAGS+101),(COUNTS,COUNTS+40)]
            ranges += [(TASK+0xA0000+32*g,TASK+0xA0000+32*g+14) for g in range(5)]
            if self.stage == 'unlock' and RECORDS <= address and address+size <= RECORDS+20000 \
                    and (address-RECORDS)%10+size <= 8:
                ranges.append((RECORDS,RECORDS+20000))
        if not any(a <= address and address+size <= b for a,b in ranges):
            raise RuntimeError(f'{self.stage} write outside finite guard: {address:#x}/{size}')
        self.writes.append((address,size,value & ((1 << (size*8))-1)))

    def clear_trace(self,stage):
        self.stage = stage
        self.visited.clear()
        self.stub_calls.clear()
        self.writes.clear()
        self.boundaries.clear()
        self.join_entries.clear()

    def coverage(self):
        touched = sorted({a+i for a,s,v in self.writes for i in range(s)})
        merged = []
        for address in touched:
            if merged and address == merged[-1][1]:
                merged[-1][1] += 1
            else:
                merged.append([address,address+1])
        raw = b''.join(struct.pack('<IIQ',*w) for w in self.writes)
        return {'native_write_count':len(self.writes),'native_writes_sha256':hashlib.sha256(raw).hexdigest(),
                'native_written_ranges':[[hex(a),hex(b)] for a,b in merged],
                'visited_function_entries':[hex(a) for a,b in self._function_ranges if a in self.visited],
                'visited_instruction_count':len(self.visited),
                'visited_addresses_sha256':hashlib.sha256(report_text(sorted(self.visited)).encode()).hexdigest(),
                'boundary_events':deepcopy(self.boundaries),'stub_calls':dict(self.stub_calls),
                'join_entries':deepcopy(self.join_entries),
                'state_region_sha256':hashlib.sha256(bytes(self.uc.mem_read(STATE,STATE_SIZE))).hexdigest(),
                'member_record_sha256':{str(i):hashlib.sha256(bytes(self.uc.mem_read(CHAR+i*STRIDE,STRIDE))).hexdigest()
                                        for i in (3,4,9)},
                'teacher_template_sha256':hashlib.sha256(bytes(self.uc.mem_read(0x6F5088+101*STRIDE,STRIDE))).hexdigest()}

    def school_snapshot(self):
        student_count,teacher_count = self.read(0x7A5260,'h'),self.read(0x7A528A,'h')
        raw_students = [self.read(0x7A5210+2*i,'h') for i in range(40)]
        raw_teachers = [self.read(0x7A5262+2*i,'h') for i in range(20)]
        buffers = []
        for teacher in range(20):
            rows = []
            for slot in range(100):
                raw = bytes(self.uc.mem_read(RECORDS+1000*teacher+10*slot,10))
                if any(raw):
                    rows.append([slot,*struct.unpack('<BBhhhBB',raw)])
            buffers.append(rows)
        profiles = deepcopy(self.origin['member_profiles'])
        for profile in profiles:
            if profile['member_id'] < 101:
                base = CHAR+profile['member_id']*STRIDE
                profile['job'] = self.read(base+6,'h')
                profile['level_50'] = self.read(base+0x50,'B')
                profile['attributes'] = [self.read(base+0xC+8*i,'B') for i in range(7)]
        relationships = []
        for row in self.origin['relationships']:
            a = row['from']-55 if row['from'] > 100 else row['from']
            b = row['to']-55 if row['to'] > 100 else row['to']
            relationships.append(row | {'value':self.read(0x7D3D71+a*68+b,'B')})
        return {'month':self.read(0x7A528E,'h'),'week':self.read(0x7A5290,'h'),
            'global_total_511c':self.read(0x7A511C,'i'),'difficulty':self.read(0x7A528C,'h'),
            'student_count':student_count,'teacher_count':teacher_count,
            'student_ids':[raw_students[i] if i < student_count else -1 for i in range(20)],
            'teacher_ids':[raw_teachers[i] if i < teacher_count else -1 for i in range(20)],
            'raw_student_ids':raw_students,'raw_teacher_ids':raw_teachers,
            'availability':list(self.uc.mem_read(0x7A5120,121)),
            'group_raw_bytes':list(self.uc.mem_read(0x7AAA12,140)),
            'derived_teacher_ids':[self.read(0x7AAAA4+2*g,'h') for g in range(5)],
            'derived_teacher_indices':[self.read(0x7AAAAE+2*g,'h') for g in range(5)],
            'derived_student_ids':[[self.read(0x7AAAB8+8*g+2*s,'h') for s in range(4)] for g in range(5)],
            'derived_student_indices':[[self.read(0x7AAAE0+8*g+2*s,'h') for s in range(4)] for g in range(5)],
            'idle_student_ids':[self.read(0x7D57E2+2*i,'h') for i in range(self.read(0x7D57DE,'h'))],
            'idle_teacher_ids':[self.read(0x7D58B4+2*i,'h') for i in range(self.read(0x7D58B0,'h'))],
            'selected_group':self.read(0x7D57D8,'b'),'reset_groups':self.read(0x7A55F8,'h'),
            'adventure_gate':self.read(0x7A55FA,'h'),'lecture_active':self.read(0x7AAB0A,'h'),
            'lecture_work_fields':[self.read(a,'h') for a in (0x7AAB10,0x7AAB12,0x7AAB16,0x7AAB14)],
            'relationships':relationships,'member_profiles':profiles,
            'course_unlocked_flags':list(self.uc.mem_read(FLAGS,101)),
            'course_counts':[self.read(COUNTS+2*i,'h') for i in range(20)],'course_buffers':buffers,
            'work_counts':[self.read(0x7D6A14+2*i,'h') for i in range(3)],
            'work_pages':[self.read(0x7D6A1A+2*i,'h') for i in range(3)],
            'work_page_limits':[self.read(0x7D6A20+2*i,'h') for i in range(3)],
            'work_rows':[[[self.read(0x7D630C+600*c+6*i+2*j,'h') for j in range(3)]
                          for i in range(self.read(0x7D6A14+2*c,'h'))] for c in range(3)]}

    def initialize(self):
        self.clear_trace('initialize')
        self.call(0x49E930)
        return {'after':self.school_snapshot(),'coverage':self.coverage()}

    def call(self,address,args=(),*,receiver=TASK):
        if address not in (0x49E930,0x4A2BA0,0x4A5F40,0x4A95F0):
            return super().call(address,args,receiver=receiver)
        sp = STACK+0xFF00
        self.write(sp,RETURN)
        for index,value in enumerate(args):
            self.write(sp+4+4*index,value)
        self.uc.reg_write(UC_X86_REG_ESP,sp)
        self.uc.reg_write(UC_X86_REG_ECX,receiver)
        self.uc.emu_start(address,RETURN,timeout=20_000_000,count=4_000_000)
        if self.uc.reg_read(UC_X86_REG_EIP) != RETURN or self.uc.reg_read(UC_X86_REG_ESP) != sp+4+len(args)*4:
            raise RuntimeError(f'native{address:#x} failed bounded return/stack check')

    def prepare(self):
        phases = []
        for stage,address in [('unlock',0x4A2BA0),('reconcile',0x4A5F40),('rate',None)]:
            self.clear_trace(stage)
            if address:
                self.call(address)
                ratings = None
            else:
                ratings = [r['defined'] for r in self.rate()]
            phase = {'phase':stage,'after':self.school_snapshot(),'coverage':self.coverage()}
            if ratings is not None:
                phase['ratings'] = ratings
            phases.append(phase)
        return phases


def report():
    cases = []
    for dirty in (False,True):
        emulator = NewGameSchoolEmulator(dirty=dirty)
        initialized = emulator.initialize()
        prepared = emulator.prepare()
        cases.append({'name':'dirty_state' if dirty else 'pristine_state',
                      'initialized':initialized,'preparation':prepared})
    emulator = NewGameSchoolEmulator()
    first = emulator.initialize()
    emulator.prepare()
    emulator.write(FLAGS+1,255,'B')
    emulator.write(COUNTS,1,'h')
    emulator.uc.mem_write(RECORDS,struct.pack('<BBhhhBB',1,1,1,2,99,4,5))
    second = emulator.initialize()
    cases.append({'name':'reinitialize_after_prepared_and_changed_course',
                  'initialized':first,'reinitialized':second,'preparation':emulator.prepare()})
    return {'schema_version':1,'evidence_kind':'complete_initializer_with_declared_source_template_load',
        'source_image_sha256':SOURCE_SHA256,'origin_rules':origin_rules(),'course_rules':course_rules(),
        'cases':cases,'limitations':['The complete49E930 function and native dependencies execute.',
            'Student templates are copied from source before entry; the predecessor loader is not executed.',
            'Memset is a boundary accepting only target7A50E8, zero and size306D4.',
            'Outside-initializer workspace controls are declared zero and selected_group=-1.',
            'Only the defined school subset and member profile fields are ported, not all student growth/package state.',
            'Native preparation calls are explicit data operations, not full school boot/menu/ADV execution.',
            'No teacher is inserted into the existing returned campaign.'],**AUTHORITY}


def fixture(data):
    result = deepcopy(data)
    result['source_report_sha256'] = hashlib.sha256(report_text(data).encode()).hexdigest()
    for case in result['cases']:
        for key in ('initialized','reinitialized'):
            if key in case:
                case[key].pop('coverage')
        for phase in case['preparation']:
            phase.pop('coverage')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True)
    parser.add_argument('--godot-out',required=True)
    args = parser.parse_args()
    paths = [ROOT/args.out,ROOT/args.godot_out]
    if paths[0].resolve() == paths[1].resolve() or any(p.exists() for p in paths):
        parser.error('refusing existing or identical output paths')
    data = report()
    for path,value in zip(paths,[data,fixture(data)]):
        path.write_bytes(report_text(value).encode())
    print('3 native origin cases exported; fields '+data['origin_rules']['origin_fields_sha256'])


if __name__ == '__main__':
    main()
