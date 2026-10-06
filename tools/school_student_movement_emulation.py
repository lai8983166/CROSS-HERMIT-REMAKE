"""Original student drag branches, with declared mouse and presentation boundaries.

Immediate drag output and explicitly requested cleanup/rating are separate.
No teacher movement, campaign teacher migration, live menu or save write.
"""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import struct

from unicorn import UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.school_teacher_group_emulation import TeacherGroupEmulator, GROUP_BASE, STUDENTS
from tools.school_waitlist_emulation import category_rules, CHAR_BASE
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, TASK, STACK, report_text

NATIVE = ((0x4A4680, 0x4A5440), (0x4A8BF0, 0x4A95F0))
BOUNDARIES = {
    0x4D5C40: ('declared_button_state', 8),
    0x4D5EC0: ('declared_slot_hit', 20),
    0x4D2700: ('target_highlight', 20),
    0x4AADB0: ('dragged_portrait', 28),
    0x4AACF0: ('dragged_job_marker', 20),
    0x4D48A0: ('random_voice_presentation', 16),
    0x4DB2B0: ('sound_boundary', 0),
}
# Only these non-stack buffers may be changed by the audited native bodies.
WRITE_RANGES = ((GROUP_BASE, GROUP_BASE+140), (0x7AAAA4, 0x7AAB08),
                (0x7D57D8, 0x7D57E2),
                (0x7D57E2, 0x7D580A), (0x7D58AA, 0x7D58B4),
                (0x7D58B4, 0x7D58DC), (0x7D598E, 0x7D5996),
                (0x7A55F8, 0x7A55FA), (TASK+0x76C2, TASK+0x76C3),
                (TASK+0x76C6, TASK+0x76C8)) + tuple(
                    (TASK+0xA0000+32*g, TASK+0xA0000+32*g+14) for g in range(5))
PROFILES = [{'character_id': i, 'job': j, 'level_50': level, 'attributes': [value]*7}
            for i, j, level, value in zip(STUDENTS, [2,1,4,3], [10,20,30,5], [25,10,5,40])]


def patch(before, after):
    return {key: deepcopy(value) for key, value in after.items() if before[key] != value}


def apply_patch(before, changes):
    return deepcopy(before) | deepcopy(changes)


class StudentMovementEmulator(TeacherGroupEmulator):
    def __init__(self, groups, mode=0):
        super().__init__(teachers=[117,118], groups=groups)
        self._function_ranges += NATIVE
        self._stubs.update(BOUNDARIES)
        for profile in PROFILES:
            address = CHAR_BASE+profile['character_id']*0x4A0
            self.write(address+6, profile['job'], 'h')
            self.write(address+0x50, profile['level_50'], 'B')
            for index, value in enumerate(profile['attributes']):
                self.write(address+0xC+8*index, value, 'B')
        self.write(0x7D57DA, mode, 'B')
        self.write(0x7D58AA, 0, 'B')
        # Native source normalization is explicit, not a mouse/menu witness.
        self.call(0x4A5F40)
        self.rate()
        self.write(0x7D57DA, mode, 'B')
        self.write(TASK+0x76C2, 1, 'B')
        self.write(TASK+0x76C6, 14, 'h')
        self.write(0x7D5996, 4, 'h')  # source rating passed to return-to-wait voice
        self.command = None
        self.events = []
        self.writes = []
        self.uc.hook_add(UC_HOOK_MEM_WRITE, self._write_hook)

    def _write_hook(self, uc, access, address, size, value, _):
        if STACK <= address and address+size <= STACK+0x10000:
            return
        if not any(a <= address and address+size <= b for a,b in WRITE_RANGES):
            raise RuntimeError(f'undeclared student drag write at {address:#x}, size {size}')
        self.writes.append({'address': hex(address), 'size': size,
                            'value': value & ((1 << (8*size))-1)})

    def _hook(self, uc, address, size, context):
        if address not in BOUNDARIES:
            return super()._hook(uc, address, size, context)
        name, pop = BOUNDARIES[address]
        self.stub_calls[name] += 1
        sp = uc.reg_read(UC_X86_REG_ESP)
        event = {'boundary': name}
        if address == 0x4D5C40:
            pointer = self.read(sp+4)
            uc.mem_write(pointer, struct.pack('<4I', int(not self.command['released']),0,0,0))
            event['released'] = self.command['released']
        elif address == 0x4D5EC0:
            pointer, x, y, width, height = struct.unpack('<5I', uc.mem_read(sp+4,20))
            group, slot = self.command['target_group'], self.command['target_slot']
            hit = group >= 0 and (x,y,width,height) == (224+78*slot,83+97*group,68,64)
            uc.mem_write(pointer, struct.pack('<3IH', 0,0,0,int(hit)))
            event.update(rectangle=[x,y,width,height], hit=hit)
        elif address == 0x4D48A0:
            event['arguments_low16'] = [self.read(sp+4+4*i) & 65535 for i in range(4)]
        self.events.append(event)
        uc.reg_write(UC_X86_REG_EAX, 0)
        uc.reg_write(UC_X86_REG_ESP, sp+4+pop)
        uc.reg_write(UC_X86_REG_EIP, self.read(sp))

    def movement_snapshot(self):
        return super().snapshot() | {
            'idle_sort_mode': self.read(0x7D57DA,'B'),
            'teacher_sort_mode': self.read(0x7D58AA,'B'),
            'drag_kind': self.read(0x7D598E,'b'), 'drag_origin': self.read(0x7D598F,'b'),
            'drag_group': self.read(0x7D5990,'h'), 'drag_slot': self.read(0x7D5992,'h'),
            'drag_id': self.read(0x7D5994,'h'), 'drag_source_rank': self.read(0x7D5996,'h'),
            'task_drag_state': self.read(TASK+0x76C2,'B'),
            'task_command': self.read(TASK+0x76C6,'h')}

    def run_movement(self, name, source_group, source_slot, target_group, target_slot, released=True):
        if not -1 <= source_group < 5 or not -1 <= target_group < 5:
            raise ValueError('invalid declared drag group')
        waiting = self.movement_snapshot()['idle_student_ids']
        if source_group == -1:
            if not 0 <= source_slot < len(waiting):
                raise ValueError('invalid waiting source')
            identity = waiting[source_slot]
        else:
            if not 0 <= source_slot < 4:
                raise ValueError('invalid group source')
            identity = self.read(GROUP_BASE+28*source_group+16+2*source_slot,'h')
        if identity not in STUDENTS or (target_group == -1 and target_slot != -1) \
                or (target_group >= 0 and not 0 <= target_slot < 4) or type(released) is not bool:
            raise ValueError('invalid declared student selection')
        self.command = {'kind':'student', 'student_id':identity, 'source_group':source_group,
                        'source_slot':source_slot, 'target_group':target_group,
                        'target_slot':target_slot, 'released':released}
        self.write(0x7D598E,0,'b')
        self.write(0x7D598F,int(source_group >= 0),'b')
        self.write(0x7D5990,source_group,'h')
        self.write(0x7D5992,source_slot,'h')
        self.write(0x7D5994,identity,'h')
        before = self.movement_snapshot()
        self.visited.clear()
        self.stub_calls = Counter()
        self.events.clear()
        self.writes.clear()
        self.call(0x4A4680)
        after = self.movement_snapshot()
        addresses = sorted(self.visited)
        movement = {'changed_fields':patch(before,after), 'native_writes':deepcopy(self.writes),
                    'boundary_events':deepcopy(self.events), 'stub_calls':dict(self.stub_calls),
                    'visited_function_entries':[hex(a) for a,b in self._function_ranges if a in self.visited],
                    'visited_instruction_count':len(addresses),
                    'visited_addresses_sha256':hashlib.sha256(report_text(addresses).encode()).hexdigest()}
        self.writes.clear()
        self.call(0x4A5F40)
        reconciled = self.movement_snapshot()
        cleanup = {'changed_fields':patch(after,reconciled), 'native_writes':deepcopy(self.writes)}
        self.writes.clear()
        ratings = self.rate()
        rated = self.movement_snapshot()
        return {'name':name, 'command':deepcopy(self.command), 'before':before,
                'movement':movement, 'reconciliation':cleanup,
                'rating':{'changed_fields':patch(reconciled,rated),
                          'ratings':[row['defined'] for row in ratings],
                          'native_writes':deepcopy(self.writes)}}


def report():
    cases = []
    layouts = [
        ('waiting_empty', [{'teacher':117},{'teacher':118}], (-1,1,0,3)),
        ('waiting_replace', [{'teacher':117,'students':[3]},{'teacher':118}], (-1,0,0,0)),
        ('class_empty', [{'teacher':117,'students':[3,4]},{'teacher':118,'students':[9]}], (0,0,1,3)),
        ('class_exchange', [{'teacher':117,'students':[3,4]},{'teacher':118,'students':[9]}], (0,0,1,0)),
        ('same_class_empty', [{'teacher':117,'students':[3,4]},{'teacher':118}], (0,0,0,3)),
        ('same_class_exchange', [{'teacher':117,'students':[3,4]},{'teacher':118}], (0,0,0,1)),
        ('same_slot', [{'teacher':117,'students':[3,4]},{'teacher':118}], (0,0,0,0)),
        ('class_outside', [{'teacher':117,'students':[3,4]},{'teacher':118}], (0,0,-1,-1)),
        ('class_teacherless', [{'teacher':117,'students':[3,4]},{'teacher':118}], (0,0,2,0)),
        ('waiting_outside', [{'teacher':117},{'teacher':118}], (-1,0,-1,-1)),
        ('waiting_teacherless', [{'teacher':117},{'teacher':118}], (-1,0,2,0)),
    ]
    for mode in range(3):
        for name,groups,args in layouts:
            cases.append(StudentMovementEmulator(groups,mode).run_movement(f'{name}_mode{mode}',*args))
    for name,groups,args in (layouts[0],layouts[3],layouts[7],layouts[8]):
        cases.append(StudentMovementEmulator(groups).run_movement(name+'_held',*args,released=False))
    group_rules = {'source_image_sha256':SOURCE_SHA256,
                   'chapter_sha256':'dfbdb1dc1f197f2d198a9d6b71e68c12d8f8f7fb72d1b2a4328f8f164affd5cf',
                   'teacher_id':117,'script_file_offset':20,'opcode':144,
                   'relationship_thresholds':[16,31,46,61,76,91]}
    return {'schema_version':1, 'evidence_kind':'isolated_original_student_drag',
            'source_image_sha256':SOURCE_SHA256, 'group_rules':group_rules,
            'sort_rules':category_rules(), 'declared_profiles':deepcopy(PROFILES),
            'native_ranges':[[hex(a),hex(b)] for a,b in NATIVE],
            'write_ranges':[[hex(a),hex(b)] for a,b in WRITE_RANGES],
            'boundary_manifest':[{'va':hex(a),'meaning':name,'callee_pop_bytes':pop}
                                 for a,(name,pop) in BOUNDARIES.items()],
            'cases':cases,
            'limitations':['Teacher-led starting groups are declared and explicitly normalized/rated.',
                'Mouse release and slot hit are declared boundaries, not live pointer capture.',
                '4A4680 student branch, 4A8BF0 waiting sort and group/index/relationship helpers execute.',
                'Voice selection, rendering, sound and 4A2980 teacher work table are presentation boundaries.',
                'After-drag, explicitly requested 4A5F40 and five 4A95F0 calls are separate checkpoints.',
                'Snapshot excludes paging controls and inactive waiting tails, which may retain stale IDs.',
                'No teacher movement, current-campaign teacher provenance or save compatibility.'],
            'school_initialized':False,'interactive_school_ready':False,
            'live_witness':False,'authorizes_persistent_write':False}


def fixture(native):
    excluded = {'native_ranges','write_ranges','boundary_manifest'}
    result = {k:deepcopy(v) for k,v in native.items() if k not in excluded}
    for case in result['cases']:
        case['movement'] = {'changed_fields':case['movement']['changed_fields']}
        case['reconciliation'] = {'changed_fields':case['reconciliation']['changed_fields']}
        case['rating'].pop('native_writes')
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
