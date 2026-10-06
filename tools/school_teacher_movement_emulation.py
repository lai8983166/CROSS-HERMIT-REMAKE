"""Execute teacher drag and real teacher work-table projection on declared data."""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import struct

from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.school_student_movement_emulation import (
    StudentMovementEmulator, PROFILES, BOUNDARIES, patch, WRITE_RANGES)
from tools.school_teacher_group_emulation import GROUP_BASE
from tools.school_waitlist_emulation import category_rules
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256, TASK, STACK, report_text

WORK_NATIVE = (0x4A2980, 0x4A2BA0)
WORK_WRITE_RANGES = ((0x7D630C,0x7D6A14),(0x7D6A14,0x7D6A1A),
                     (0x7D6A1A,0x7D6A20),(0x7D6A20,0x7D6A26))


def source_rules():
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError('original source differs')
    templates = []
    for identity in range(1,101):
        category,key = struct.unpack_from('<hh',image,0x74BED6-0x400000+identity*96)
        if category in (1,2,3) and key > 0:
            templates.append({'work_id':identity,'category':category-1,'sort_key':key-1})
    encoded = ''.join(f"{r['work_id']}:{r['category']}:{r['sort_key']};" for r in templates)
    teachers = []
    for identity in (117,118):
        base = 0x6F5088-0x400000+identity*0x4A0
        teachers.append({'teacher_id':identity,'job':struct.unpack_from('<h',image,base+6)[0],
                         'level_50':image[base+0x50],
                         'attributes':[image[base+0xC+8*i] for i in range(7)]})
    return {'source_image_sha256':SOURCE_SHA256,'templates':templates,'teacher_profiles':teachers,
            'template_fields_sha256':hashlib.sha256(encoded.encode()).hexdigest()}


def records(ids):
    return [{'slot':i,'enabled':1,'blocked':0,'work_id':identity} for i,identity in enumerate(ids)]


DEFAULT_WORK = {'117':records([9,1,7,2]),'118':records([22,3,8])}


class TeacherMovementEmulator(StudentMovementEmulator):
    def __init__(self, groups, mode=0, gate=0, work=None):
        super().__init__(groups,mode)
        self._function_ranges += (WORK_NATIVE,)
        del self._stubs[0x4A2980]
        self.work = deepcopy(DEFAULT_WORK if work is None else work)
        for identity in (117,118):
            base = 0x7A5BCA+(identity-101)*1000
            self.uc.mem_write(base,bytes(1000))
            for row in self.work[str(identity)]:
                a = base+row['slot']*10
                self.write(a,row['enabled'],'B')
                self.write(a+1,row['blocked'],'B')
                self.write(a+2,row['work_id'],'h')
        self.write(0x7A55FA,gate,'h')
        self.write(0x7D58AA,mode,'B')
        selected = self.read(0x7D57D8,'b')
        self.call(0x4A8B50,(selected & 0xFFFFFFFF,))

    def _write_hook(self,uc,access,address,size,value,context):
        if any(a <= address and address+size <= b for a,b in WORK_WRITE_RANGES):
            self.writes.append({'address':hex(address),'size':size,'value':value & ((1 << (8*size))-1)})
            return
        return super()._write_hook(uc,access,address,size,value,context)

    def _hook(self,uc,address,size,context):
        if address != 0x4D5EC0:
            return super()._hook(uc,address,size,context)
        name,pop = BOUNDARIES[address]
        self.stub_calls[name] += 1
        sp = uc.reg_read(UC_X86_REG_ESP)
        pointer,x,y,width,height = struct.unpack('<5I',uc.mem_read(sp+4,20))
        group = self.command['target_group']
        hit = group >= 0 and (x,y,width,height) == (16,83+97*group,68,64)
        uc.mem_write(pointer,struct.pack('<3IH',0,0,0,int(hit)))
        self.events.append({'boundary':name,'rectangle':[x,y,width,height],'hit':hit})
        uc.reg_write(UC_X86_REG_EAX,0)
        uc.reg_write(UC_X86_REG_ESP,sp+4+pop)
        uc.reg_write(UC_X86_REG_EIP,self.read(sp))

    def teacher_snapshot(self):
        counts = [self.read(0x7D6A14+2*i,'h') for i in range(3)]
        return self.movement_snapshot() | {
            'teacher_work_records':deepcopy(self.work),
            'teacher_work_record_sha256':hashlib.sha256(bytes(self.uc.mem_read(0x7A5BCA+16000,2000))).hexdigest(),
            'work_counts':counts,'work_pages':[self.read(0x7D6A1A+2*i,'h') for i in range(3)],
            'work_page_limits':[self.read(0x7D6A20+2*i,'h') for i in range(3)],
            'work_rows':[[[self.read(0x7D630C+600*c+6*i+2*j,'h') for j in range(3)]
                          for i in range(counts[c])] for c in range(3)]}

    def coverage(self):
        addresses = sorted(self.visited)
        return {'visited_function_entries':[hex(a) for a,b in self._function_ranges if a in self.visited],
                'visited_instruction_count':len(addresses),
                'visited_addresses_sha256':hashlib.sha256(report_text(addresses).encode()).hexdigest(),
                'native_writes':deepcopy(self.writes),'boundary_events':deepcopy(self.events),
                'stub_calls':dict(self.stub_calls)}

    def clear_trace(self):
        self.visited.clear()
        self.stub_calls = Counter()
        self.events.clear()
        self.writes.clear()

    def run_teacher(self,name,source_group,source_slot,target_group,released=True):
        if source_group == -1:
            identity = self.teacher_snapshot()['idle_teacher_ids'][source_slot]
        else:
            identity = self.read(GROUP_BASE+28*source_group,'h')
        if identity not in (117,118) or not -1 <= target_group < 5:
            raise ValueError('outside declared teacher selection')
        self.command = {'kind':'teacher','teacher_id':identity,'source_group':source_group,
                        'source_slot':source_slot,'target_group':target_group,'released':released}
        for address,value,fmt in [(0x7D598E,1,'b'),(0x7D598F,int(source_group >= 0),'b'),
                                  (0x7D5990,source_group,'h'),(0x7D5992,source_slot,'h'),(0x7D5994,identity,'h')]:
            self.write(address,value,fmt)
        before = self.teacher_snapshot()
        self.clear_trace()
        self.call(0x4A4680)
        after = self.teacher_snapshot()
        movement = self.coverage() | {'changed_fields':patch(before,after)}
        self.clear_trace()
        self.call(0x4A5F40)
        clean = self.teacher_snapshot()
        cleanup = self.coverage() | {'changed_fields':patch(after,clean)}
        self.clear_trace()
        ratings = self.rate()
        rated = self.teacher_snapshot()
        return {'name':name,'command':deepcopy(self.command),'before':before,
                'movement':movement,'reconciliation':cleanup,
                'rating':self.coverage() | {'changed_fields':patch(clean,rated),
                                          'ratings':[r['defined'] for r in ratings]}}

    def run_selection(self,name,group):
        before = self.teacher_snapshot()
        self.clear_trace()
        self.call(0x4A8B50,(group & 0xFFFFFFFF,))
        after = self.teacher_snapshot()
        return {'name':name,'group':group,'before':before,
                'selection':self.coverage() | {'changed_fields':patch(before,after)}}


def report():
    a = {'teacher':117,'students':[3,4],'activity':1,'work_fields':[8,5,6,7]}
    b = {'teacher':118,'students':[9],'activity':0,'work_fields':[11,12,13,14]}
    layouts = [('waiting_empty',[b],(-1,0,1)),('waiting_replace',[a],(-1,0,0)),
               ('class_empty',[a],(0,-1,1)),('class_exchange',[a,b],(0,-1,1)),
               ('same_group',[a],(0,-1,0)),('class_outside_no_teacher',[a],(0,-1,-1)),
               ('class_outside_other_teacher',[a,b],(0,-1,-1)),('waiting_outside',[a],(-1,0,-1))]
    cases = []
    for gate in range(2):
        for mode in range(3):
            for name,groups,args in layouts:
                cases.append(TeacherMovementEmulator(groups,mode,gate).run_teacher(
                    f'{name}_mode{mode}_gate{gate}',*args))
    for name,groups,args in layouts[:4]:
        cases.append(TeacherMovementEmulator(groups).run_teacher(name+'_held',*args,released=False))
    selections = []
    mixed = {'117':[{'slot':0,'enabled':0,'blocked':0,'work_id':0},
                    {'slot':1,'enabled':1,'blocked':1,'work_id':1},
                    {'slot':2,'enabled':1,'blocked':0,'work_id':9},
                    {'slot':5,'enabled':1,'blocked':0,'work_id':7},
                    {'slot':6,'enabled':1,'blocked':0,'work_id':2},
                    {'slot':99,'enabled':1,'blocked':0,'work_id':1}], '118':records([22])}
    for name,group in [('mixed_active',0),('teacherless',2),('cleared',-1)]:
        selections.append(TeacherMovementEmulator([a],work=mixed).run_selection(name,group))
    for count in (0,1,10,11,12,13,99,100):
        work = {'117':records([1]*count),'118':[]}
        selections.append(TeacherMovementEmulator([a],work=work).run_selection(f'page_count_{count}',0))
    return {'schema_version':1,'evidence_kind':'isolated_original_teacher_drag_and_work_lists',
            'source_image_sha256':SOURCE_SHA256,'work_rules':source_rules(),
            'group_rules':{'source_image_sha256':SOURCE_SHA256,
                'chapter_sha256':'dfbdb1dc1f197f2d198a9d6b71e68c12d8f8f7fb72d1b2a4328f8f164affd5cf',
                'teacher_id':117,'script_file_offset':20,'opcode':144,'relationship_thresholds':[16,31,46,61,76,91]},
            'sort_rules':category_rules(),'declared_student_profiles':deepcopy(PROFILES),
            'native_work_range':[hex(a) for a in WORK_NATIVE],
            'work_write_ranges':[[hex(a),hex(b)] for a,b in WORK_WRITE_RANGES],
            'cases':cases,'selections':selections,
            'limitations':['Initial rosters, groups, teacher work flags and mouse inputs are declared.',
                '4A2980 executes for real; no work-table stub is used in this new emulator.',
                'Work template/category/key and teacher sort profiles are read from the original image.',
                'Immediate drag, explicit 4A5F40 cleanup and five ratings remain separate.',
                'Only active work rows are projected; unused buffer tails are not valid work records.',
                'Voice/render/audio/mouse boundaries remain; no course selection or calendar unlock4A2BA0.',
                'No campaign teacher migration, live school, growth projection or save writes.'],
            'school_initialized':False,'interactive_school_ready':False,
            'live_witness':False,'authorizes_persistent_write':False}


def fixture(native):
    result = deepcopy(native)
    for rows in [result['cases'],result['selections']]:
        for row in rows:
            for phase in ['movement','reconciliation','rating','selection']:
                if phase in row:
                    row[phase] = {k:v for k,v in row[phase].items() if k in ('changed_fields','ratings')}
    result['native_report_sha256'] = hashlib.sha256(report_text(native).encode()).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True)
    parser.add_argument('--godot-out',required=True)
    args = parser.parse_args()
    paths = [ROOT/args.out,ROOT/args.godot_out]
    if paths[0].resolve() == paths[1].resolve() or any(p.exists() for p in paths):
        parser.error('use two different new output paths')
    native = report()
    for path,data in zip(paths,[native,fixture(native)]):
        payload = report_text(data)
        with path.open('x',encoding='utf-8',newline='\n') as handle:
            handle.write(payload)
        print(f'{path}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
