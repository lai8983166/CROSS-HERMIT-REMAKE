"""Consume real pending8, run native workroom constructor/control and CH002 END.

UI, graphics/text resource APIs and right-button input are explicit boundaries.
The real state dispatcher constructs workroom; school constructors are not run.
"""
import argparse
from copy import deepcopy
import hashlib

from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.new_week_adv_emulation import NewWeekAdvEmulator
from tools.adv_route_emulation import AdvRouteEmulator
from tools.adv_chapter_emulation import CH003, CONTROLLER
from tools.scene5_script_emulation import VM, IMPORTS
from tools.tactics_exit_emulation import ExitEmulator, ROOT, SOURCE_SHA256, STACK, RETURN, TASK, report_text

WORKROOM = TASK+0xB0000
GRAPHICS = 0x9800000
FONT_IMPORT = IMPORTS+0x50
WORK_NATIVE = ((0x4A1350, 0x4A1430), (0x4A1570, 0x4A17B0),
               (0x49F6C0, 0x49FAA0), (0x49FD50, 0x4A0020), (0x4CD810, 0x4CD8D0),
               (0x56CDA0, 0x56CE80))
WORK_STUBS = {0x439EF0: ('workroom_base_constructor', 0),
    0x464C60: ('workroom_animation_constructor', 0), 0x4075E0: ('workroom_render_constructor', 0),
    0x4D5FB0: ('workroom_text_constructor', 0), 0x4D66A0: ('workroom_text_constructor', 0),
    0x416790: ('workroom_graphics_register', 8), 0x4D6090: ('workroom_font_select', 8),
    0x4D6420: ('workroom_text_resource', 4), 0x4D64D0: ('workroom_text_select', 8),
    0x4D6150: ('workroom_news_text', 4), 0x49F660: ('workroom_animation_resource', 12),
    0x409EF0: ('workroom_animation_init', 4), 0x4077C0: ('workroom_render_reset', 0),
    0x4D2620: ('workroom_fade_draw', 28), 0x49FAA0: ('workroom_menu_draw', 0),
    0x4D67F0: ('workroom_button_animation', 40), 0x4DB2B0: ('workroom_button_sound', 0),
    FONT_IMPORT: ('workroom_create_font', 56)}


class WorkroomReturnEmulator(NewWeekAdvEmulator):
    def __init__(self, *, continue_ready=True, visited_override=None, school_fade_ready=True):
        if type(continue_ready) is not bool or type(school_fade_ready) is not bool \
                or (visited_override is not None and (type(visited_override) is not int or visited_override != 1)):
            raise ValueError('outside declared workroom inputs')
        super().__init__()
        self._function_ranges += WORK_NATIVE
        self._stubs.update(WORK_STUBS)
        self.uc.mem_map(GRAPHICS, 0x800000)
        self.write(0x5920A0, FONT_IMPORT)
        self.continue_ready = continue_ready
        self.visited_override = visited_override
        self.school_fade_ready = school_fade_ready
        self.work_consumed = None
        self.ch002_consumed = None
        self.work_events = []
        self.work_yields = 0
        self.work_allocated = False
        self._ran_work = False

    @staticmethod
    def _raw_path(uc, pointer):
        raw = bytes(uc.mem_read(pointer, 256)).split(b'\0')[0]
        if len(raw) == 256:
            raise RuntimeError('unbounded workroom resource path')
        return '/'.join(p for p in raw.decode('ascii').lower().replace('\\', '/').split('/') if p)

    def _resource(self, pointer):
        if self.phase == 'workroom':
            name = AdvRouteEmulator._path(self, pointer)
            if name != 'ch002.ybc':
                raise RuntimeError('workroom attempted an undeclared ADV load')
            source = (CH003.parent / name).read_bytes()
            if len(source) > 0x10000:
                raise RuntimeError('CH002 exceeds bounded resource workspace')
            return name, source
        return super()._resource(pointer)

    def _hook(self, uc, address, size, user):
        if self.phase == 'workroom':
            sp = uc.reg_read(UC_X86_REG_ESP)
            receiver = uc.reg_read(UC_X86_REG_ECX)
            if address == 0x49E2B0:
                if self.work_consumed is not None or self.read(CONTROLLER+0x2C) != 1 \
                        or self.read(CONTROLLER+0x30) != 8 or self.read(VM+4, 'B') != 0:
                    raise RuntimeError('workroom dispatch requires actual unconsumed next8 after CH001 END')
                self.work_consumed = {'pending_flag': 1, 'state': 8, 'adv_active': 0,
                                      'native_dispatch_va': '0x49e2b0'}
            if address == 0x428A40:
                if self.work_allocated or self.read(sp+4) != 0x14580:
                    raise RuntimeError('undeclared workroom allocation')
                self.work_allocated = True
                self.uc.mem_write(WORKROOM, bytes(0x14580))
                self.work_events.append({'kind': 'allocation_boundary', 'size': self.read(sp+4), 'pointer': hex(WORKROOM)})
                self.stub_calls['isolated_workroom_allocation'] += 1
                self._stub_return(WORKROOM, 0)
                return
            if address == 0x4216C0:
                args = [self.read(sp+k) for k in (4, 8, 12)]
                if args != [WORKROOM, 0, 2] or self.read(WORKROOM) != 0x5A0904:
                    raise RuntimeError('unexpected workroom registration')
                self.work_events.append({'kind': 'scheduler_registration_boundary', 'args': args,
                                         'vtable': hex(self.read(WORKROOM)), 'active': self.read(WORKROOM+0x28, 'B')})
                self.stub_calls['isolated_workroom_registration'] += 1
                self._stub_return(0, 0)
                return
            if address == 0x42AE20:
                path = self._raw_path(uc, self.read(sp+4))
                if path in ('data/workroom/workroom.bin', 'data/adv/bin/bg002_d.bin'):
                    source = (ROOT/'CROSS HERMIT/CROSS HERMIT'/path).read_bytes()
                    offset = 0 if path.startswith('data/workroom') else 0x400000
                    maximum = 0x400000
                    if len(source) > maximum:
                        raise RuntimeError('workroom graphics exceed bounded allocations')
                    uc.mem_write(GRAPHICS+offset, source)
                    self.work_events.append({'kind': 'graphics_resource_boundary', 'path': path,
                                             'source_sha256': hashlib.sha256(source).hexdigest()})
                    self.stub_calls['declared_workroom_graphics_bytes'] += 1
                    self._stub_return(GRAPHICS+offset, 0)
                    return
            if address == 0x4D5EC0:
                target, x, y, w, h = [self.read(sp+k) for k in (4, 8, 12, 16, 20)]
                if not STACK <= target <= STACK+0x10000-8 or x not in (0x28E, 0x34F) or (y,w,h) != (0x2D6,0x8D,0x1E):
                    raise RuntimeError('undeclared workroom button')
                clicked = self.continue_ready and x == 0x34F
                self.write(target, 0)
                self.write(target+4, int(clicked))
                self.work_events.append({'kind': 'button_input_boundary', 'x': x, 'clicked': clicked})
                self.stub_calls['declared_workroom_continue_input'] += 1
                self._stub_return(0, 20)
                return
            if address == 0x422360:
                self.work_yields += 1
                if self.work_yields > 70:
                    self.stop_reason = 'workroom_waiting_continue'
                    uc.emu_stop()
                    return
            if address == 0x4A15A0:
                self.work_events.append({'kind': 'control_phase', 'value': self.read(WORKROOM+0x30, 'h')})
            if address in WORK_STUBS:
                name, pop = WORK_STUBS[address]
                if name.endswith('_constructor') and not WORKROOM <= receiver < WORKROOM+0x14580:
                    raise RuntimeError('constructor boundary outside workroom allocation')
                self.stub_calls[name] += 1
                self._stub_return(receiver if name.endswith('_constructor') else 0x1234 if address == FONT_IMPORT else 0, pop)
                return
        if self.phase == 'ch002_adv' and address == 0x4D1A80:
            if self.ch002_consumed is not None or self.read(CONTROLLER+0x2C) != 1 \
                    or self.read(CONTROLLER+0x30) != 6 or self.active_path != 'ch002.ybc' \
                    or self.read(VM+4, 'B') != 1 or self.read(VM+0x1C) != 0 or self.read(VM+0x92DC, 'i') != 9:
                raise RuntimeError('CH002 requires actual workroom load and unconsumed request6/next9')
            self.ch002_consumed = {'state': 6, 'pending_flag': 1, 'path': 'ch002.ybc', 'next_task_state': 9,
                                   'driver_boundary': 'consume_native_request_without_adv_scheduler_constructor'}
            self.write(CONTROLLER+0x2C, 0)
        if any(a <= address < b for a, b in WORK_NATIVE):
            return ExitEmulator._hook(self, uc, address, size, user)
        return super()._hook(uc, address, size, user)

    def _thread(self, address, receiver, *, timeout=10_000_000, count=2_000_000):
        sp = STACK+0xFF00
        self.write(sp, RETURN)
        self.write(sp+4, 0)
        self.uc.reg_write(UC_X86_REG_ESP, sp)
        self.uc.reg_write(UC_X86_REG_ECX, receiver)
        self.uc.emu_start(address, RETURN, timeout=timeout, count=count)
        if self.stop_reason is None and (self.uc.reg_read(UC_X86_REG_EIP) != RETURN or self.uc.reg_read(UC_X86_REG_ESP) != sp+8):
            raise RuntimeError('workroom/CH002 task exceeded bounds or ret4 stack mismatch')

    def run_return(self, name):
        if self._ran_work:
            raise RuntimeError('single-run workroom probe cannot replay consumed request')
        self._ran_work = True
        upstream = deepcopy(super().run_new_adv(name))
        if not upstream['ch001_completed']:
            raise RuntimeError('workroom lacks native CH001 completion')
        before_override = self.flow_snapshot()
        if self.visited_override is not None:
            self.write(0x7A4E62, self.visited_override, 'h')  # Explicit alternate-branch probe only.
        before_workroom = self.flow_snapshot()
        self.phase = 'workroom'
        self.stop_reason = None
        load_start, request_start = len(self.loads), len(self.state_requests)
        self.call(0x49E2B0)
        if self.read(0x7A4AD4) != WORKROOM or self.read(WORKROOM) != 0x5A0904:
            raise RuntimeError('native workroom construction failed')
        self._thread(0x4A1570, WORKROOM)
        after_workroom = self.flow_snapshot()
        work_requests = deepcopy(self.state_requests[request_start:])
        work_loads = deepcopy(self.loads[load_start:])
        ch002_commands, ch002_requests = [], []
        if self.stop_reason is None and work_requests == [{'va': '0x439e30', 'state': 6}]:
            self.phase = 'ch002_adv'
            self.external['fade_ready'] = self.school_fade_ready
            self.frame_index = -1
            self.max_frames = 200
            start, requests = len(self.commands), len(self.state_requests)
            self._thread(0x4D1A80, TASK)
            ch002_commands = self.commands[start:]
            ch002_requests = self.state_requests[requests:]
        count = self.read(WORKROOM+0x1457C, 'h')
        return {'name': name, 'upstream': {'ch001_completed': upstream['ch001_completed'],
            'state_requests': upstream['state_requests'], 'active_path': upstream['active_path'],
            'stored_next_task_state': upstream['stored_next_task_state']},
            'synthetic_continue_ready': self.continue_ready, 'synthetic_visited_override': self.visited_override,
            'synthetic_school_fade_ready': self.school_fade_ready, 'before_override': before_override,
            'before_workroom': before_workroom, 'after_workroom': after_workroom, 'after': self.flow_snapshot(),
            'consumed_request': self.work_consumed, 'ch002_consumed_request': self.ch002_consumed,
            'work_events': self.work_events, 'work_yields': self.work_yields,
            'work_task': {'pointer': hex(self.read(0x7A4AD4)), 'vtable': hex(self.read(WORKROOM)),
                'active': self.read(WORKROOM+0x28, 'B'), 'control_phase': self.read(WORKROOM+0x30, 'h'),
                'news_count': count, 'news_entries': [[self.read(WORKROOM+0x13DAC+k*4, 'h'),
                    self.read(WORKROOM+0x13DAE+k*4, 'h')] for k in range(count)]},
            'work_script_loads': work_loads, 'work_state_requests': work_requests,
            'ch002_commands': ch002_commands, 'ch002_state_requests': ch002_requests,
            'ch002_completed': self.ch002_consumed is not None and self.stop_reason is None and self.read(VM+4, 'B') == 0,
            'pending_flag': self.read(CONTROLLER+0x2C), 'pending_state': self.read(CONTROLLER+0x30),
            'stop_reason': self.stop_reason, 'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
            'stub_calls': dict(self.stub_calls), 'school_initialized': False,
            'live_witness': False, 'authorizes_persistent_write': False}


def report():
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'evidence_kind': 'native_workroom_dispatch_initialization_control_and_ch002_end',
        'additional_native_ranges': [[hex(a), hex(b)] for a,b in WORK_NATIVE],
        'stub_manifest': [{'va': hex(a), 'meaning': n, 'callee_pop_bytes': p} for a,(n,p) in WORK_STUBS.items()],
        'limitations': ['All cases execute the complete existing CH003/new-week/CH001 chain in shared memory.',
            'State8 dispatcher, workroom allocation wrapper/constructor, news-list initialization, menu control and CH002 are native.',
            'Allocation, embedded UI constructors, graphics/text/font APIs, scheduler registration and right-button input are simulated.',
            'visited_override1 is an explicit alternate-branch input after native CH001, not produced by its first visit.',
            'Shopping/inspection UI branches and school task constructors/bodies are not executed; no preceding battle or live authority.'],
        'cases': [WorkroomReturnEmulator().run_return('first_workroom_then_ch002'),
                  WorkroomReturnEmulator(continue_ready=False).run_return('workroom_waits_for_continue'),
                  WorkroomReturnEmulator(visited_override=1).run_return('visited_workroom_direct9_control'),
                  WorkroomReturnEmulator(school_fade_ready=False).run_return('ch002_fade_wait_blocks9')],
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
