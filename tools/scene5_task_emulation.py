"""Run scene-5 VM work completion, the task loop and state dispatch in isolation.

This extends scene5_script_emulation without changing its historical reports.
Battle/world initial state and presentation are synthetic; persistent writes remain
unauthorized. No game process, save file or external UI is accessed.
"""
import argparse
import hashlib
from pathlib import Path

from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.scene5_script_emulation import (Scene5Emulator, VM, WORK, IMPORTS, EXTERNAL,
                                         NATIVE, SCRIPT_SHA256)
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, FUNCTIONS, STUBS, TASK, STACK, RETURN, report_text

WORLD, MAP, CONTROLLER, RESULT_TASK = 0x9000000, 0x9200000, 0x9300000, 0x9400000
WORK_NATIVE = ((0x4977A0, 0x4977D0), (0x4978C0, 0x497A40),
               (0x497AA0, 0x497C50), (0x497C50, 0x497C90),
               (0x497D10, 0x497DF0), (0x497DF0, 0x497EC0),
               (0x498010, 0x498280), (0x499560, 0x499750),
               (0x56CFCC, 0x56CFF3))
TASK_NATIVE = ((0x451670, 0x4519A3), (0x451A60, 0x451B10),
               (0x4539B0, 0x453CFC), (0x439E30, 0x439EE4),
               (0x49E2B0, 0x49E4D3), (0x4BD540, 0x4BD590),
               (0x4BD6F0, 0x4BD7E0))
# These are explicitly skipped setup/parallel/rendering bodies, not verified
# world behavior. They do not select a terminal script or modify completion flags.
TASK_EXTERNAL = {
    0x41E500: ('audio_stop', 0),
    0x419240: ('menu_resource_cleanup', 0), 0x417CC0: ('menu_resource_cleanup', 0),
    0x45E8D0: ('menu_task_boundary', 0),
    0x415480: ('render_mode', 8), 0x415420: ('render_flush', 0),
    0x451D40: ('skip_task_setup', 0), 0x451E20: ('skip_task_setup', 0),
    0x496390: ('skip_unitctrl_setup', 4), 0x452040: ('skip_task_setup', 0),
    0x451B10: ('skip_task_setup', 0), 0x451BF0: ('skip_task_setup', 0),
    0x4519C0: ('skip_parallel_initialization', 0),
    0x46B470: ('skip_parallel_tick', 0), 0x432100: ('skip_scene_events', 0),
    0x457AA0: ('skip_task_input', 0), 0x455560: ('skip_task_input', 0),
    0x455950: ('skip_task_input', 0), 0x455EC0: ('skip_task_input', 0),
    0x456B20: ('network_mode', 0),
    0x453E10: ('render_task', 0), 0x43D970: ('render_task', 0),
    0x43FD20: ('render_task', 4), 0x43B3C0: ('render_task', 0),
    0x46B670: ('render_task', 0), 0x440F00: ('render_task', 4),
    0x454F50: ('render_vm', 0), 0x457C40: ('skip_task_input', 0),
    0x422360: ('scheduler_yield', 4), 0x4967B0: ('unitctrl_cleanup', 0),
    0x451F00: ('render_task_cleanup', 0), 0x40D610: ('resource_cleanup', 0),
    0x465E60: ('unitctrl_cleanup', 0), 0x4DB230: ('cleanup_timer_start', 0),
    0x4DB270: ('cleanup_timer_ready', 0),
    0x428A40: ('result_heap_allocation', 0), 0x439EF0: ('base_task_constructor', 0),
    0x4216C0: ('scheduler_register_result', 0),
    0x49E540: ('skip_dispatch_followup', 0),
    IMPORTS+0x20: ('critical_section_enter', 4),
    IMPORTS+0x30: ('critical_section_leave', 4),
}


class TaskEmulator(Scene5Emulator):
    def __init__(self, *, key_ready=True, ui_ready=True, max_frames=1000, freeze_fade=False,
                 animation_ready=True, exit_to_menu=False):
        super().__init__(key_ready=key_ready, ui_ready=ui_ready, release_work=False)
        if not 1 <= max_frames <= 2000:
            raise ValueError('max_frames must be 1..2000')
        self.max_frames = max_frames
        self.task_timeout_us = 20_000_000
        self.freeze_fade = freeze_fade
        self._function_ranges += WORK_NATIVE+TASK_NATIVE
        self._stubs.update(TASK_EXTERNAL)
        for base, size in ((WORLD, 0x120000), (MAP, 0x1000), (CONTROLLER, 0x2000),
                           (RESULT_TASK, 0x1000), (0, 0x1000)):
            self.uc.mem_map(base, size)
        self.write(0x7A49F4, WORLD)
        self.write(WORLD+0x2A494, MAP)
        self.write(MAP+4, 64, 'h')
        self.write(MAP+6, 64, 'h')
        self.write(0x7A4A00, CONTROLLER)
        self.write(0x7A4BB4, 0)
        self.write(0x592234, IMPORTS+0x20)
        self.write(0x592238, IMPORTS+0x30)
        self.write(0x7F448A, 0, 'h')
        self.write(TASK+0x34, 2)
        self.write(TASK+0x31, int(exit_to_menu), 'B')
        self.frames = []
        self.work_events = []
        self.dispatch_events = []
        self.allocations = 0
        self.script_return = 0
        self.bounded_stop = False
        # Remove the inherited completion policy: no timed 4CDF80 calls are made.
        for key in ('work_delay', 'release_work', 'script_work_busy'):
            self.external.pop(key)
        self.external.update(freeze_fade=freeze_fade, network_mode=False,
                             animation_ready=animation_ready, exit_to_menu=exit_to_menu)

    def snapshot(self):
        return {**super().snapshot(),
                'exit_to_menu': self.read(TASK+0x31, 'B'),
                'work_fade_value': self.read(WORK+0x2490, 'i'),
                'work_fade_delta': self.read(WORK+0x2494, 'i'),
                'work_fade_active': self.read(WORK+0x2499, 'B'),
                'work_fade_status': self.read(WORK+0x249A, 'B'),
                'work_fade_remaining': self.read(WORK+0x249C, 'i'),
                'request_pending': self.read(CONTROLLER+0x2C),
                'requested_state': self.read(CONTROLLER+0x30)}

    def _hook(self, uc, address, size, user):
        if address == 0x454CF0:
            self.frame_index += 1
            if self.frame_index >= self.max_frames:
                self.bounded_stop = True
                uc.emu_stop()
                return
        if address == 0x4539F1:
            self.script_return = uc.reg_read(UC_X86_REG_EAX)
        if address == 0x453A00:
            self.frames.append({**self.snapshot(), 'frame': self.frame_index,
                                'script_function_return': self.script_return,
                                'transition_function_return': uc.reg_read(UC_X86_REG_EAX)})
        if address == 0x4977B8:
            self.work_events.append({'frame': self.frame_index, 'write_va': hex(address),
                'target': '0x7e0f08', 'previous': self.read(VM+0x92E0, 'B'),
                'caller_return_va': hex(self.read(uc.reg_read(UC_X86_REG_ESP)+0x50))})
        if address == 0x439E30:
            self.dispatch_events.append({'kind': 'state_request', 'va': hex(address),
                'frame': self.frame_index, 'state': self.read(uc.reg_read(UC_X86_REG_ESP)+4),
                'receiver': hex(uc.reg_read(UC_X86_REG_ECX)),
                'caller_return_va': hex(self.read(uc.reg_read(UC_X86_REG_ESP)))})
        if address == 0x4BD6F0:
            self.dispatch_events.append({'kind': 'result_constructor_enter', 'va': hex(address),
                'state': self.read(CONTROLLER+0x30),
                'caller_return_va': hex(self.read(uc.reg_read(UC_X86_REG_ESP)))})
        if address == 0x497AA0 and self.freeze_fade:
            self.stub_calls['counterfactual_fade_tick_frozen'] += 1
            self._stub_return(0, 0)
            return
        if any(a <= address < b for a, b in self._function_ranges):
            return super()._hook(uc, address, size, user)
        if address in TASK_EXTERNAL:
            name, pop = TASK_EXTERNAL[address]
            self.stub_calls[name] += 1
            result = int(name == 'cleanup_timer_ready')
            sp = uc.reg_read(UC_X86_REG_ESP)
            if name == 'result_heap_allocation':
                if self.allocations or self.read(sp+4) != 0x1CC:
                    raise RuntimeError('unexpected allocation at result constructor')
                self.allocations += 1
                result = RESULT_TASK
            elif name == 'base_task_constructor':
                if uc.reg_read(UC_X86_REG_ECX) != RESULT_TASK:
                    raise RuntimeError('base constructor outside result allocation')
                result = RESULT_TASK
            elif name == 'scheduler_register_result':
                args = [self.read(sp+offset) for offset in (4, 8, 12)]
                if args != [RESULT_TASK, 0, 2]:
                    raise RuntimeError('unexpected result scheduler registration')
                self.dispatch_events.append({'kind': name, 'va': hex(address), 'args': args,
                    'vtable': hex(self.read(RESULT_TASK)),
                    'active': self.read(RESULT_TASK+0x28, 'B')})
            self._stub_return(result, pop)
            return
        return super()._hook(uc, address, size, user)

    def run(self, *, selector=2, sub=2, name='terminal_sub2'):
        initial = self.request(selector, sub)
        preflight = list(self.commands)
        sp = STACK+0xFF00
        self.write(sp, RETURN)
        self.write(sp+4, 0)  # Task thread's opaque argument, unused on this path.
        self.uc.reg_write(UC_X86_REG_ESP, sp)
        self.uc.reg_write(UC_X86_REG_ECX, TASK)
        self.uc.emu_start(0x451670, RETURN, timeout=self.task_timeout_us, count=5_000_000)
        if not self.bounded_stop:
            if self.uc.reg_read(UC_X86_REG_EIP) != RETURN:
                raise RuntimeError('task loop exceeded instruction/time bounds')
            if self.uc.reg_read(UC_X86_REG_ESP) != sp+8:
                raise RuntimeError('task thread stack mismatch')
            self.call(0x49E2B0)
        return {'name': name, 'selector': selector, 'sub': sub, 'initial_state': initial,
                'preflight_commands': preflight, 'commands': self.commands[len(preflight):],
                'frames': self.frames, 'final_state': self.snapshot(),
                'work_completions': self.work_events, 'dispatch_events': self.dispatch_events,
                'stub_calls': dict(self.stub_calls),
                'result_task': {'pointer': hex(self.read(0x7A4BB4)),
                    'vtable': hex(self.read(RESULT_TASK)),
                    'active': self.read(RESULT_TASK+0x28, 'B')},
                'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
                'synthetic_external_inputs': self.external,
                'counterfactual_overrides': ['0x497aa0'] if self.freeze_fade else [],
                'bounded_stop': self.bounded_stop, 'live_state11_observed': False,
                'state11_dispatched_in_emulation': any(event['kind'] == 'result_constructor_enter'
                    for event in self.dispatch_events),
                'authorizes_persistent_write': False}


def report():
    ranges = FUNCTIONS+NATIVE+WORK_NATIVE+TASK_NATIVE
    stubs = {va: spec for va, spec in {**STUBS, **EXTERNAL, **TASK_EXTERNAL}.items()
             if not any(a <= va < b for a, b in ranges)}
    return {'schema_version': 1, 'evidence_kind': 'original_task_loop_with_synthetic_world',
            'source_image_sha256': SOURCE_SHA256,
            'script_sha256': SCRIPT_SHA256,
            'native_function_ranges': [[hex(a), hex(b)] for a, b in ranges],
            'effective_stub_manifest': [{'va': hex(va), 'meaning': name, 'callee_pop_bytes': pop}
                for va, (name, pop) in stubs.items()],
            'synthetic_world': {'map_width': 64, 'map_height': 64, 'camera_pixels': [0, 0],
                                'unit0_fixed_point_position': [0, 0],
                                'task_phase': 2, 'transition_phase': 5, 'next_scene': 0,
                                'exit_to_menu': 'explicit_per_case_input'},
            'limitations': ['Terminal selection, world state and task setup are synthetic.',
                'UI, input, audio, drawing, scheduler and parallel events remain simulated.',
                'Result allocation, base-task setup and scheduler registration are simulated.',
                'No live scene witness, result body, state10/12 transaction or persistent writes.'],
            'cases': [TaskEmulator().run(), TaskEmulator().run(selector=14, sub=8,
                          name='terminal_selector14_sub8'),
                      TaskEmulator(key_ready=False, max_frames=150).run(name='key_missing'),
                      TaskEmulator(freeze_fade=True, max_frames=150).run(name='fade_tick_frozen'),
                      TaskEmulator(ui_ready=False, max_frames=150).run(name='ui_missing'),
                      TaskEmulator(animation_ready=False, max_frames=400).run(name='result_animation_missing'),
                      TaskEmulator(exit_to_menu=True).run(name='menu_exit')],
            'authorizes_persistent_write': False}


def godot_fixture(result):
    cases = []
    for case in result['cases']:
        start = next((i for i, frame in enumerate(case['frames']) if frame['script_phase'] == 5), None)
        cases.append({'name': case['name'], 'sub': case['sub'],
            'commands': case['commands'], 'work_completions': case['work_completions'],
            'post_vm_initial': case['frames'][start] if start is not None else {},
            'post_vm_frames': case['frames'][start+1:] if start is not None else [],
            'exit_frame': case['frames'][-1],
            'dispatch_context': {'scene_id': 5, 'next_scene': 0, 'network_mode': False,
                                 'task_phase': 2, 'request_pending': 0,
                                 'exit_to_menu': case['synthetic_external_inputs']['exit_to_menu']},
            'dispatch_events': case['dispatch_events'], 'result_task': case['result_task'],
            'bounded_stop': case['bounded_stop'],
            'state11_dispatched_in_emulation': case['state11_dispatched_in_emulation'],
            'external_inputs': case['synthetic_external_inputs'],
            'live_state11_observed': False, 'authorizes_persistent_write': False})
    return {'schema_version': 1, 'evidence_kind': result['evidence_kind'],
            'source_report_sha256': hashlib.sha256(report_text(result).encode('utf-8')).hexdigest(),
            'source_image_sha256': SOURCE_SHA256, 'script_sha256': SCRIPT_SHA256,
            'limitations': result['limitations'], 'cases': cases,
            'authorizes_persistent_write': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--godot-out', type=Path)
    args = parser.parse_args()
    if args.godot_out and args.out.resolve() == args.godot_out.resolve():
        parser.error('report and fixture must have different paths')
    for path in (args.out, args.godot_out):
        if path and path.exists():
            parser.error('refusing to overwrite existing output')
    result = report()
    with args.out.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(report_text(result))
    if args.godot_out:
        with args.godot_out.open('x', encoding='utf-8', newline='\n') as handle:
            handle.write(report_text(godot_fixture(result)))


if __name__ == '__main__':
    main()
