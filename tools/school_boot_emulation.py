"""Execute native school group initialization and personal task resource/idle loop.

The shared CPU reaches the source group-menu entry and the source person idle
yield. Interactive menus, drawing and personal selection remain boundaries.
"""
import argparse
from copy import deepcopy
import hashlib

from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_ESP

from tools.school_dispatch_emulation import SchoolDispatchEmulator, GROUP_TASK, PERSON_TASK
from tools.workroom_return_emulation import FONT_IMPORT
from tools.adv_chapter_emulation import CONTROLLER
from tools.tactics_exit_emulation import ExitEmulator, ROOT, SOURCE_SHA256, report_text

BOOT_GRAPHICS = 0xB000000
BOOT_NATIVE = ((0x4AB7A0, 0x4ABA30), (0x4B8D50, 0x4B8F20),
    (0x4A5A60, 0x4A6460), (0x4A8B50, 0x4A8BC0), (0x4A8BF0, 0x4A95F0),
    (0x4A1C70, 0x4A1FF0), (0x4A17B0, 0x4A1920), (0x4A2BA0, 0x4A2D60),
    (0x4A2980, 0x4A2BA0), (0x4A9AB0, 0x4AA0E0), (0x4A24A0, 0x4A2700),
    (0x4AB250, 0x4AB570), (0x4A8140, 0x4A81A0), (0x4D0860, 0x4D0900), (0x4D46E0, 0x4D4730))
BOOT_STUBS = {0x416790: ('school_graphics_register', 8), 0x4D6090: ('school_font_select', 8),
    0x4D6420: ('school_text_resource', 4), 0x409EF0: ('school_animation_init', 4),
    0x4077C0: ('school_render_reset', 0), 0x4CDE10: ('school_board_resource', 8),
    0x416B80: ('school_animation_resource', 8), 0x450110: ('school_audio_key', 4),
    0x40C780: ('school_audio_resource', 12), 0x4DB010: ('school_music_play', 0),
    FONT_IMPORT: ('school_create_font', 56)}


class SchoolBootEmulator(SchoolDispatchEmulator):
    def __init__(self, **inputs):
        super().__init__(**inputs)
        self._stubs.update(BOOT_STUBS)
        self.uc.mem_map(BOOT_GRAPHICS, 0x2800000)
        self.boot_events = []
        self.group_started = False
        self.group_initialized = False
        self.person_started = False
        self.person_resource_initialized = False
        self.person_idle_yields = 0
        self._ran_boot = False

    def _source_resource_event(self, path, kind, **extra):
        source = (ROOT/'CROSS HERMIT/CROSS HERMIT'/path).read_bytes()
        self.boot_events.append({'kind': kind, 'path': path,
                                'source_sha256': hashlib.sha256(source).hexdigest(), **extra})
        return source

    def _school_boot_boundary(self, uc, address, size, user):
        if self.phase in ('school_group_boot', 'school_person_boot'):
            sp = uc.reg_read(UC_X86_REG_ESP)
            receiver = uc.reg_read(UC_X86_REG_ECX)
            if address == 0x4AB7A0:
                if self.group_started or self.school_consumed is None or receiver != GROUP_TASK \
                        or self.read(CONTROLLER+0x2C) != 0 or self.read(CONTROLLER+0x30) != 9 \
                        or self.read(GROUP_TASK) != 0x5A0A40 or self.read(PERSON_TASK) != 0x5A0C18:
                    raise RuntimeError('group boot requires both actual school constructors and consumed9')
                self.group_started = True
                self.boot_events.append({'kind': 'native_group_body', 'va': hex(address)})
            if address == 0x4A7C40:
                if not self.group_started or receiver != GROUP_TASK or self.read(sp) != 0x4AB7F1:
                    raise RuntimeError('school group menu lacks completed native initialization prefix')
                self.group_initialized = True
                self.stop_reason = 'school_group_menu_boundary'
                self.boot_events.append({'kind': 'group_menu_entry_boundary', 'va': hex(address),
                    'body_executed': False})
                uc.emu_stop()
                return True
            if address == 0x4B8D50:
                if self.person_started or not self.group_initialized or receiver != PERSON_TASK \
                        or self.read(0x7A4AD8) != GROUP_TASK or self.read(0x7A4ADC) != PERSON_TASK:
                    raise RuntimeError('person boot requires native group initialization and both source tasks')
                self.person_started = True
                self.boot_events.append({'kind': 'native_person_body', 'va': hex(address)})
            if address == 0x42AE20:
                path = self._raw_path(uc, self.read(sp+4))
                expected = 'data/menu/handata.bin' if self.phase == 'school_group_boot' else 'data/menu/kojindata.bin'
                if path != expected:
                    raise RuntimeError('undeclared school graphic resource')
                source = self._source_resource_event(path, 'graphics_bytes_boundary')
                offset = 0 if self.phase == 'school_group_boot' else 0x800000
                if len(source) > (0x800000 if offset == 0 else 0x2000000):
                    raise RuntimeError('school graphics exceed bounded workspace')
                uc.mem_write(BOOT_GRAPHICS+offset, source)
                self.stub_calls['declared_school_graphics_bytes'] += 1
                self._stub_return(BOOT_GRAPHICS+offset, 0)
                return True
            if address == 0x422360:
                if self.phase != 'school_person_boot' or self.read(sp) != 0x4B8EE2 \
                        or self.read(0x7A4E60, 'h') != 0 or self.read(PERSON_TASK+0x391DA, 'h') != -1 \
                        or self.read(0x7A4AE0, 'B') != 1:
                    raise RuntimeError('school person loop is not at the declared native idle point')
                self.person_idle_yields += 1
                if self.person_idle_yields == 2:
                    self.person_resource_initialized = True
                    self.stop_reason = 'school_person_idle_boundary'
                    uc.emu_stop()
                    return True
            if address in BOOT_STUBS:
                name, pop = BOOT_STUBS[address]
                if address in (0x4D6420, 0x4CDE10, 0x416B80):
                    pointer = self.read(sp+8) if address == 0x416B80 else self.read(sp+4)
                    path = self._raw_path(uc, pointer)
                    expected = {0x4D6420: ('data/ystext/tacticsexp.ybc', 'data/ystext/lectureexp.ybc'),
                                0x4CDE10: ('data/adv/bin/gybc_00.bin',),
                                0x416B80: ('data/menu/anmhan.bin',)}[address]
                    if path not in expected:
                        raise RuntimeError('undeclared school presentation resource')
                    self._source_resource_event(path, name+'_boundary', body_executed=False)
                if address == 0x4DB010:
                    self.boot_events.append({'kind': 'music_api_boundary', 'music': self.read(sp+4, 'i')})
                self.stub_calls[name] += 1
                self._stub_return(0x3456 if address == FONT_IMPORT else 0, pop)
                return True
        return False

    def _hook(self, uc, address, size, user):
        if self._school_boot_boundary(uc, address, size, user):
            return
        if self.phase in ('school_group_boot', 'school_person_boot') and any(a <= address < b for a,b in BOOT_NATIVE):
            return ExitEmulator._hook(self, uc, address, size, user)
        return super()._hook(uc, address, size, user)

    def boot_snapshot(self):
        result = self.flow_snapshot()
        result['school_control'] = self.boot_control_snapshot()
        return result

    def boot_control_snapshot(self):
        count = self.read(0x7D57DE, 'h')
        teacher_count = self.read(0x7D58B0, 'h')
        if not 0 <= count <= 20 or not 0 <= teacher_count <= 20:
            raise RuntimeError('school wait-list count outside declared bound')
        adventure_counts = [self.read(0x7D62FA+k*2, 'h') for k in range(3)]
        if any(not 0 <= n <= 80 for n in adventure_counts):
            raise RuntimeError('school adventure count outside source table stride')
        return {'selected_group': self.read(0x7D57D8, 'b'),
            'person_phase': self.read(0x7A4E60, 'h'), 'person_ready': self.read(0x7A4AE0, 'B'),
            'idle_student_ids': [self.read(0x7D57E2+k*2, 'h') for k in range(count)],
            'idle_teacher_ids': [self.read(0x7D58B4+k*2, 'h') for k in range(teacher_count)],
            'adventure_counts': adventure_counts,
            'adventure_entries': [[[self.read(0x7D599A+category*800+k*10+j*2, 'h') for j in range(5)]
                for k in range(n)] for category,n in enumerate(adventure_counts)],
            'lecture_counts': [self.read(0x7D6A14+k, 'B') for k in range(3)],
            'adventure_unlock_flags': list(self.uc.mem_read(0x7A55FD, 100)),
            'lecture_unlock_flags': list(self.uc.mem_read(0x7A5B65, 100)),
            'group_raw_bytes': list(self.uc.mem_read(0x7AAA12, 5*0x1C)),
            'group_rankings': [[self.read(GROUP_TASK+0x76CA+k*0x10+j*2, 'h') for j in range(8)] for k in range(4)],
            'group_task_controls': [self.read(GROUP_TASK+k, 'h') for k in (0x76BC,0x76BE,0x76C0,0x76C6,0x76C8)],
            'person_selection': self.read(PERSON_TASK+0x391DA, 'h')}

    def run_boot(self, name):
        if self._ran_boot:
            raise RuntimeError('single-run school boot cannot replay task initialization')
        self._ran_boot = True
        upstream = deepcopy(super().run_school_dispatch(name))
        before = self.boot_snapshot()
        start = len(self.state_requests)
        if upstream['school_constructed']:
            self._function_ranges += BOOT_NATIVE
            self.phase = 'school_group_boot'
            self.stop_reason = None
            self._thread(0x4AB7A0, GROUP_TASK)
            if not self.group_initialized:
                raise RuntimeError('native group initialization did not reach menu boundary')
            self.phase = 'school_person_boot'
            self.stop_reason = None
            self._thread(0x4B8D50, PERSON_TASK)
            if not self.person_resource_initialized:
                raise RuntimeError('native person task did not reach idle boundary')
        return {'name': name, 'upstream': {k: deepcopy(upstream[k]) for k in (
            'upstream', 'consumed_request', 'school_constructed', 'school_tasks', 'pending_flag', 'pending_state')},
            'before': before, 'after': self.boot_snapshot(), 'boot_events': self.boot_events,
            'group_initialized': self.group_initialized, 'person_resource_initialized': self.person_resource_initialized,
            'person_idle_yields': self.person_idle_yields, 'stop_reason': self.stop_reason,
            'school_state_requests': self.state_requests[start:], 'pending_flag': self.read(CONTROLLER+0x2C),
            'pending_state': self.read(CONTROLLER+0x30), 'school_initialized': False,
            'interactive_school_ready': False, 'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
            'stub_calls': dict(self.stub_calls), 'live_witness': False, 'authorizes_persistent_write': False}


def report():
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'evidence_kind': 'native_school_group_initialization_and_person_resource_idle',
        'additional_native_ranges': [[hex(a),hex(b)] for a,b in BOOT_NATIVE],
        'stub_manifest': [{'va': hex(a), 'meaning': n, 'callee_pop_bytes': p} for a,(n,p) in BOOT_STUBS.items()],
        'limitations': ['All predecessors and school constructors execute in the same CPU and roster.',
            'Group body executes the complete source 4A5CE0 initialization and stops before 4A7C40 interactive menu body.',
            'Person body loads its graphics and executes two native idle iterations; personal selection/detail initialization is not run.',
            'Graphics/text/font/animation/audio APIs and scheduler yielding are declared boundaries; no actual school interaction or persistent authority.'],
        'cases': [SchoolBootEmulator().run_boot('first_school_boot'),
                  SchoolBootEmulator(visited_override=1).run_boot('visited_school_boot'),
                  SchoolBootEmulator(school_fade_ready=False).run_boot('ch002_wait_blocks_boot')],
        'live_witness': False, 'authorizes_persistent_write': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    path = ROOT / args.out
    if path.exists():
        parser.error('output already exists; use a new path')
    payload = report_text(report())
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(payload)
    print(f'{path}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
