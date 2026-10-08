"""Consume actual workroom/CH002 pending9 and construct both native school tasks.

Allocation, embedded presentation constructors, fonts and registration remain
declared boundaries. School task bodies and initialization are not run here.
"""
import argparse
from copy import deepcopy
import hashlib

from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_ESP

from tools.workroom_return_emulation import WorkroomReturnEmulator, FONT_IMPORT
from tools.adv_chapter_emulation import CONTROLLER
from tools.scene5_script_emulation import VM
from tools.tactics_exit_emulation import ExitEmulator, ROOT, SOURCE_SHA256, report_text

GROUP_TASK, PERSON_TASK = 0xA000000, 0xA020000
SCHOOL_TASKS = ((GROUP_TASK, 0x1419C, 0x7A4AD8, 0x5A0A40, 0x4ABA70, 0x4AB570),
                (PERSON_TASK, 0x3A5E4, 0x7A4ADC, 0x5A0C18, 0x4B89A0, 0x4B8A90))
SCHOOL_NATIVE = ((0x4AB570, 0x4AB650), (0x4ABA70, 0x4ABB60),
                 (0x4B89A0, 0x4B8BE0), (0x56DDA0, 0x56DE40))
SCHOOL_STUBS = {0x439EF0: ('school_base_constructor', 0),
    0x464C60: ('school_animation_constructor', 0), 0x4075E0: ('school_render_constructor', 0),
    0x4D5FB0: ('school_text_constructor', 0), 0x4D66A0: ('school_text_constructor', 0),
    FONT_IMPORT: ('school_create_font', 56)}


class SchoolDispatchEmulator(WorkroomReturnEmulator):
    def __init__(self, **inputs):
        super().__init__(**inputs)
        self._function_ranges += SCHOOL_NATIVE
        self._stubs.update(SCHOOL_STUBS)
        self.uc.mem_map(GROUP_TASK, 0x60000)
        self.school_consumed = None
        self.school_events = []
        self.school_allocated = []
        self._ran_school = False

    def _school_dispatch_boundary(self, uc, address, size, user):
        if self.phase == 'school_dispatch':
            sp = uc.reg_read(UC_X86_REG_ESP)
            receiver = uc.reg_read(UC_X86_REG_ECX)
            if address == 0x49E2B0:
                if self.school_consumed is not None or self.read(CONTROLLER+0x2C) != 1 \
                        or self.read(CONTROLLER+0x30) != 9 or self.read(VM+4, 'B') != 0:
                    raise RuntimeError('school dispatch requires actual unconsumed request9 and inactive ADV')
                self.school_consumed = {'pending_flag': 1, 'state': 9, 'adv_active': 0,
                                        'native_dispatch_va': '0x49e2b0'}
            if address == 0x428A40:
                if len(self.school_allocated) >= 2:
                    raise RuntimeError('unexpected extra school allocation')
                pointer, count, _, _, wrapper, _ = SCHOOL_TASKS[len(self.school_allocated)]
                if self.read(sp+4) != count or self.read(sp) != wrapper+0x37:
                    raise RuntimeError('school allocation differs from native wrapper')
                uc.mem_write(pointer, bytes(count))
                self.school_allocated.append(pointer)
                self.school_events.append({'kind': 'allocation_boundary', 'pointer': hex(pointer),
                                           'size': count, 'source_wrapper': hex(wrapper)})
                self.stub_calls['isolated_school_allocation'] += 1
                self._stub_return(pointer, 0)
                return True
            if address == 0x4216C0:
                args = [self.read(sp+k) for k in (4, 8, 12)]
                registered = sum(e['kind'] == 'registration_boundary' for e in self.school_events)
                if registered >= 2:
                    raise RuntimeError('unexpected extra school registration')
                pointer, _, global_pointer, vtable, _, _ = SCHOOL_TASKS[registered]
                if args != [pointer, 0, 2] or self.read(global_pointer) != pointer \
                        or self.read(pointer) != vtable or self.read(pointer+0x28, 'B') != 1:
                    raise RuntimeError('native school registration fields mismatch')
                self.school_events.append({'kind': 'registration_boundary', 'args': args,
                    'global_pointer_va': hex(global_pointer), 'vtable': hex(vtable), 'active': 1})
                self.stub_calls['isolated_school_registration'] += 1
                self._stub_return(0, 0)
                return True
            if address == 0x56DDA0:
                args = [self.read(sp+k) for k in (4, 8, 12, 16, 20)]
                if args != [PERSON_TASK+0x19D20, 0x6424, 5, 0x4D5FB0, 0x4D6010]:
                    raise RuntimeError('undeclared school constructor vector')
                self.school_events.append({'kind': 'native_constructor_vector', 'base': hex(args[0]),
                    'stride': args[1], 'count': args[2], 'constructor': hex(args[3]), 'destructor': hex(args[4])})
            if address in SCHOOL_STUBS:
                name, pop = SCHOOL_STUBS[address]
                if name.endswith('_constructor') and not any(p <= receiver < p+n for p,n,*_ in SCHOOL_TASKS):
                    raise RuntimeError('embedded constructor outside school task allocation')
                self.school_events.append({'kind': 'presentation_constructor_boundary', 'va': hex(address),
                    'receiver': hex(receiver)})
                self.stub_calls[name] += 1
                self._stub_return(receiver if name.endswith('_constructor') else 0x2345, pop)
                return True
        return False

    def _hook(self, uc, address, size, user):
        if self._school_dispatch_boundary(uc, address, size, user):
            return
        if any(a <= address < b for a,b in SCHOOL_NATIVE):
            return ExitEmulator._hook(self, uc, address, size, user)
        return super()._hook(uc, address, size, user)

    def school_task_snapshot(self):
        return [{'pointer': hex(self.read(g)), 'allocation_pointer': hex(p), 'size': n,
                 'vtable': hex(self.read(p)), 'active': self.read(p+0x28, 'B'),
                 'source_wrapper_va': hex(w), 'source_constructor_va': hex(c)}
                for p,n,g,v,w,c in SCHOOL_TASKS]

    def run_school_dispatch(self, name):
        if self._ran_school:
            raise RuntimeError('single-run school probe cannot replay consumed request')
        self._ran_school = True
        upstream = deepcopy(super().run_return(name))
        before = self.flow_snapshot()
        start = len(self.state_requests)
        constructed = False
        if upstream['stop_reason'] is None and upstream['pending_flag'] == 1 and upstream['pending_state'] == 9:
            self.phase = 'school_dispatch'
            self.call(0x49E2B0)
            constructed = self.school_allocated == [GROUP_TASK, PERSON_TASK]
            if not constructed or self.read(CONTROLLER+0x2C) != 0:
                raise RuntimeError('native dispatcher did not construct both tasks or consume request9')
        return {'name': name, 'upstream': {k: deepcopy(upstream[k]) for k in (
            'synthetic_continue_ready', 'synthetic_visited_override', 'synthetic_school_fade_ready',
            'work_state_requests', 'ch002_state_requests', 'ch002_completed', 'pending_flag', 'pending_state', 'stop_reason')},
            'before': before, 'after': self.flow_snapshot(), 'consumed_request': self.school_consumed,
            'school_events': self.school_events, 'school_tasks': self.school_task_snapshot(),
            'person_font_handle': self.read(PERSON_TASK+0xC8C),
            'school_state_requests': self.state_requests[start:],
            'pending_flag': self.read(CONTROLLER+0x2C), 'pending_state': self.read(CONTROLLER+0x30),
            'school_constructed': constructed, 'school_initialized': False,
            'school_task_bodies_executed': False, 'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
            'stub_calls': dict(self.stub_calls), 'live_witness': False, 'authorizes_persistent_write': False}


def report():
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'evidence_kind': 'native_pending9_dispatch_and_two_school_constructors',
        'additional_native_ranges': [[hex(a),hex(b)] for a,b in SCHOOL_NATIVE],
        'stub_manifest': [{'va': hex(a), 'meaning': n, 'callee_pop_bytes': p} for a,(n,p) in SCHOOL_STUBS.items()],
        'limitations': ['All four cases execute the native CH003/week/CH001/workroom/CH002 chain in shared memory.',
            'State9 dispatcher, both task wrappers/constructors and five-element vector iterator are native.',
            'Heap allocation, embedded UI constructors, font creation, task registration and dispatcher followup are declared boundaries.',
            'School task initialization/bodies and real battle entry are not executed; construction is not initialization.'],
        'cases': [SchoolDispatchEmulator().run_school_dispatch('ch002_end_constructs_school'),
                  SchoolDispatchEmulator(visited_override=1).run_school_dispatch('visited_workroom_constructs_school'),
                  SchoolDispatchEmulator(continue_ready=False).run_school_dispatch('continue_wait_blocks_school'),
                  SchoolDispatchEmulator(school_fade_ready=False).run_school_dispatch('ch002_wait_blocks_school')],
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
