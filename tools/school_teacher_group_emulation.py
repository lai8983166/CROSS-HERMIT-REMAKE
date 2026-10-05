"""Native teacher117 registration and isolated group reconciliation/rating.

Only Chapter012's joining prefix executes. Initial assignments are declared,
not mouse actions; teacher work-table selection is an explicit stub boundary.
"""
import argparse
from copy import deepcopy
import hashlib
import struct

from tools.roster_join_emulation import RosterJoinEmulator
from tools.scene5_script_emulation import VM, SCRIPT
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, TASK, report_text

CHAPTER = ROOT / 'CROSS HERMIT/CROSS HERMIT/DATA/ADV/DAT/Chapter012.ybc'
CHAPTER_SHA = 'dfbdb1dc1f197f2d198a9d6b71e68c12d8f8f7fb72d1b2a4328f8f164affd5cf'
NATIVE = ((0x4A5F40, 0x4A6460), (0x4A8B50, 0x4A8BC0),
          (0x4AB250, 0x4AB570), (0x4A95F0, 0x4A9AB0),
          (0x4D45C0, 0x4D4730), (0x4D3A20, 0x4D3AA0))
STUDENTS = [3, 4, 9, 5]
GROUP_BASE = 0x7AAA12


class TeacherGroupEmulator(RosterJoinEmulator):
    def __init__(self, *, teachers=(), groups=(), students=STUDENTS, relation_value=50,
                 relationships=None, lecture=False, reset_groups=False):
        super().__init__()
        source = CHAPTER.read_bytes()
        if hashlib.sha256(source).hexdigest() != CHAPTER_SHA:
            raise ValueError('teacher source chapter differs')
        self.source = source
        self.uc.mem_write(SCRIPT, source)
        self.call(0x4CE560, (0, 7), receiver=VM)
        self._function_ranges += NATIVE
        self._stubs[0x4A2980] = ('teacher_work_table_boundary', 4)
        self.write(0x7A5260, len(students), 'h')
        self.write(0x7A528A, len(teachers), 'h')
        self.uc.mem_write(0x7A5120, bytes(121))
        for i in range(20):
            self.write(0x7A5210+2*i, students[i] if i < len(students) else -1, 'h')
            self.write(0x7A5262+2*i, teachers[i] if i < len(teachers) else -1, 'h')
        for i in list(students)+list(teachers):
            self.write(0x7A5120+i, 1, 'B')
        self.write(0x7A55F8, int(reset_groups), 'h')
        self.write(0x7A55FA, 0, 'h')
        self.write(0x7AAB0A, int(lecture), 'h')
        for address, value in zip((0x7AAB10,0x7AAB12,0x7AAB16,0x7AAB14), (7,2,3,4)):
            self.write(address, value, 'h')
        for g in range(5):
            # Opaque bytes retain recognizable declared values through cleanup.
            raw = bytearray([0x22]*28)
            struct.pack_into('<h', raw, 0, -1)
            raw[3] = 0
            for offset in (6,8,10,12):
                struct.pack_into('<h', raw, offset, -1)
            raw[14] = 0
            for slot in range(4):
                struct.pack_into('<h', raw, 16+slot*2, -1)
            if g < len(groups):
                spec = groups[g]
                struct.pack_into('<h', raw, 0, spec.get('teacher', -1))
                raw[3] = spec.get('activity', 0)
                for offset, value in zip((6,8,10,12), spec.get('work_fields', [-1]*4)):
                    struct.pack_into('<h', raw, offset, value)
                for slot, identity in enumerate(spec.get('students', [])):
                    struct.pack_into('<h', raw, 16+slot*2, identity)
            self.uc.mem_write(GROUP_BASE+g*28, bytes(raw))
            self.write(0x7AAAA4+2*g, -1, 'h')
            self.write(0x7AAAAE+2*g, -1, 'h')
            for slot in range(4):
                self.write(0x7AAAB8+8*g+2*slot, -1, 'h')
                self.write(0x7AAAE0+8*g+2*slot, -1, 'h')
        self.write(0x7D57D8, -1, 'b')
        self.write(0x7D57DE, 0, 'h')
        self.write(0x7D58B0, 0, 'h')
        ids = sorted(set(STUDENTS + list(teachers) + [117,118]))
        self.relationships = []
        for a in ids:
            for b in ids:
                if a == b:
                    continue
                value = (relationships or {}).get((a,b), relation_value)
                self.write(0x7D3D71+self.matrix_id(a)*68+self.matrix_id(b), value, 'B')
                self.relationships.append({'from': a, 'to': b, 'value': value})
        self.visited.clear()
        self.join_entries.clear()
        self.stub_calls.clear()
        self.commands.clear()

    @staticmethod
    def matrix_id(identity):
        return identity-55 if identity > 100 else identity

    def snapshot(self):
        return {'student_count': self.read(0x7A5260, 'h'),
                'student_ids': [self.read(0x7A5210+2*i, 'h') for i in range(20)],
                'teacher_count': self.read(0x7A528A, 'h'),
                'teacher_ids': [self.read(0x7A5262+2*i, 'h') for i in range(20)],
                'availability': list(self.uc.mem_read(0x7A5120, 121)),
                'group_raw_bytes': list(self.uc.mem_read(GROUP_BASE, 140)),
                'derived_teacher_ids': [self.read(0x7AAAA4+2*g, 'h') for g in range(5)],
                'derived_teacher_indices': [self.read(0x7AAAAE+2*g, 'h') for g in range(5)],
                'derived_student_ids': [[self.read(0x7AAAB8+8*g+2*s, 'h') for s in range(4)] for g in range(5)],
                'derived_student_indices': [[self.read(0x7AAAE0+8*g+2*s, 'h') for s in range(4)] for g in range(5)],
                'idle_student_ids': [self.read(0x7D57E2+2*i, 'h') for i in range(self.read(0x7D57DE, 'h'))],
                'idle_teacher_ids': [self.read(0x7D58B4+2*i, 'h') for i in range(self.read(0x7D58B0, 'h'))],
                'selected_group': self.read(0x7D57D8, 'b'),
                'reset_groups': self.read(0x7A55F8, 'h'),
                'adventure_gate': self.read(0x7A55FA, 'h'),
                'lecture_active': self.read(0x7AAB0A, 'h'),
                'lecture_work_fields': [self.read(a, 'h') for a in (0x7AAB10,0x7AAB12,0x7AAB16,0x7AAB14)],
                'relationships': deepcopy(self.relationships),
                'month': self.read(0x7A528E, 'h'), 'week': self.read(0x7A5290, 'h'),
                'global_total_511c': self.read(0x7A511C, 'i'),
                'student_record_sha256': {str(i): hashlib.sha256(bytes(self.uc.mem_read(0x7E17E8+i*0x4A0,0x4A0))).hexdigest()
                                          for i in STUDENTS}}

    def rate(self):
        outputs = []
        for group in range(5):
            pointer = TASK+0xA0000+32*group
            self.uc.mem_write(pointer, bytes([0xEE])*14)
            self.call(0x4A95F0, (pointer,group))
            words = list(struct.unpack('<7h', self.uc.mem_read(pointer,14)))
            defined = {'state': words[0], 'relationship_mean': words[1], 'relationship_rank': words[2],
                       'work_fields': words[3:] if words[0] in (2,4) else []}
            outputs.append({'raw_words': words, 'defined': defined})
        return outputs

    def run(self, name, *, join='none', duplicate=False, group=-1):
        before = self.snapshot()
        if join == 'chapter012_prefix':
            self.call_join_step()
        elif join == 'direct_helper':
            self.call(0x4D3E90, (117,group,0xFFFFFFFF))
        once = self.snapshot()
        if duplicate:
            self.write(VM+0x1C, 0)
            self.call_join_step()
        joined = self.snapshot()
        join_addresses = [hex(a) for a in sorted(self.visited)]
        self.call(0x4A5F40)
        reconciled = self.snapshot()
        ratings = self.rate()
        return {'name': name, 'join_context': {'kind': join, 'teacher_id': 117, 'group': group,
                'slot': -1, 'duplicate': duplicate}, 'before': before, 'after_join_once': once,
                'after_join': joined, 'after_reconcile': reconciled, 'after_ratings': self.snapshot(),
                'ratings': ratings, 'join_entries': deepcopy(self.join_entries),
                'join_visited_addresses': join_addresses,
                'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
                'stub_calls': dict(self.stub_calls), 'vm_pc': self.read(VM+0x1C),
                'vm_active': self.read(VM+4,'B')}


def report():
    led = {'teacher':117,'students':[3,4]}
    cases = [TeacherGroupEmulator(groups=[led]).run('chapter012_teacher_enables_existing_group', join='chapter012_prefix'),
             TeacherGroupEmulator().run('chapter012_teacher_duplicate', join='chapter012_prefix', duplicate=True),
             TeacherGroupEmulator(groups=[{'students':[3,4]}]).run('direct_helper_places_teacher', join='direct_helper',group=0),
             TeacherGroupEmulator(teachers=[117]).run('teacher_already_available', join='chapter012_prefix'),
             TeacherGroupEmulator(groups=[led]).run('unavailable_teacher_clears_group'),
             TeacherGroupEmulator(groups=[{'students':[3,4]}]).run('teacherless_students_clear'),
             TeacherGroupEmulator(teachers=[117],groups=[{'teacher':117}]).run('teacher_only'),
             TeacherGroupEmulator(teachers=[117],students=[3,4,5],groups=[{'teacher':117,'students':[3,9]}]).run('unavailable_student_clears'),
             TeacherGroupEmulator(teachers=[117,118],groups=[led,{'teacher':118,'students':[3,5]}]).run('duplicate_student_first_wins'),
             TeacherGroupEmulator(teachers=[117],groups=[led],lecture=True).run('active_lecture_state2'),
             TeacherGroupEmulator(teachers=[117],groups=[dict(led,activity=1)]).run('missing_adventure_state5'),
             TeacherGroupEmulator(teachers=[117],groups=[dict(led,activity=1,work_fields=[8,5,6,7])]).run('assigned_adventure_state4'),
             TeacherGroupEmulator(teachers=[117],groups=[dict(led,activity=1,work_fields=[8,5,6,7])],reset_groups=True).run('reset_groups_clears_work'),
             TeacherGroupEmulator(teachers=[117],groups=[led],relationships={(117,3):17,(3,117):84,(117,4):42,(4,117):61,(3,4):39,(4,3):58}).run('asymmetric_relationship_mean')]
    for value in (15,16,30,31,45,46,60,61,75,76,90,91):
        cases.append(TeacherGroupEmulator(teachers=[117],groups=[led],relation_value=value).run(f'rank_boundary_{value}'))
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
            'source_chapter012_sha256': CHAPTER_SHA,
            'evidence_kind': 'isolated_native_teacher_registration_group_cleanup_and_rating',
            'additional_native_ranges': [[hex(a),hex(b)] for a,b in NATIVE],
            'rules': {'source_image_sha256': SOURCE_SHA256, 'chapter_sha256': CHAPTER_SHA,
                      'teacher_id':117, 'script_file_offset':20, 'opcode':144,
                      'relationship_thresholds':[16,31,46,61,76,91]},
            'cases': cases,
            'limitations': ['Only Chapter012 opcode144 prefix executes; no chapter END or chronological campaign claim.',
                'Direct helper placement is explicitly labeled and is not the Chapter012 instruction.',
                'Initial rosters, availability, group records and directed relations are declared inputs.',
                '4A2980 teacher work-table rebuild is stubbed; no work selection or drag/drop4A4680 executes.',
                '4A5F40 and4A95F0 plus availability/index/relationship helpers execute on the same CPU.',
                'Undefined rating words are retained raw but excluded from normalized outputs.',
                'No teacher profile/growth projection, live school readiness or save writes.'],
            'school_initialized':False, 'interactive_school_ready':False,
            'live_witness':False, 'authorizes_persistent_write':False}


def fixture(native):
    return {k:native[k] for k in ('schema_version','source_image_sha256','source_chapter012_sha256',
            'evidence_kind','rules','cases','limitations','school_initialized','interactive_school_ready',
            'live_witness','authorizes_persistent_write')} | {
            'native_report_sha256':hashlib.sha256(report_text(native).encode()).hexdigest()}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True)
    parser.add_argument('--godot-out',required=True)
    args=parser.parse_args()
    paths=[ROOT/args.out,ROOT/args.godot_out]
    if paths[0].resolve()==paths[1].resolve() or any(p.exists() for p in paths):
        parser.error('use two different new output paths')
    native=report()
    for path,data in zip(paths,[native,fixture(native)]):
        payload=report_text(data)
        with path.open('x',encoding='utf-8',newline='\n') as handle:
            handle.write(payload)
        print(f'{path}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__=='__main__':
    main()
