"""Bounded execution of original x86 exit code with declared external stubs.

This is synthetic CPU emulation, not a live game witness or a save transaction.
Install tools/requirements-audit.txt in .venv-audit, then run this script.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import struct

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'analysis/hermit_game.exe'
SOURCE_SHA256 = '588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'
BASE, TASK, STACK, RETURN = 0x400000, 0x1000000, 0x2000000, 0x3000000
# Execute only these original functions. All other reached entries must be stubs.
FUNCTIONS = ((0x4549D0, 0x454AB0), (0x454C40, 0x454CF0),
             (0x454CF0, 0x454EE0), (0x453F10, 0x4547C3))
# address: (description, callee-popped argument bytes); cdecl stubs pop zero.
STUBS = {
    0x410310: ('draw_overlay', 28), 0x415040: ('fade_step', 4),
    0x4998B0: ('start_result_animation', 4), 0x499910: ('animation_ready', 0),
    0x473860: ('unitctrl_finalize', 0), 0x457830: ('script_frame_setup', 0),
    0x4563D0: ('script_frame_input', 0), 0x497C50: ('script_work_busy', 0),
    0x497980: ('start_script_work_fade', 0), 0x454EE0: ('release_animation_slots', 0),
    0x467850: ('unitctrl_pause_resume', 8), 0x41F710: ('audio_cleanup', 0),
    0x497AA0: ('script_work_tick', 0), 0x498310: ('script_work_ui_tick', 0),
    0x4CE8F0: ('vm_update', 0), 0x56CE80: ('debug_stack_check', 0),
    0x56CEC0: ('memset', 0),
}


class ExitEmulator:
    def __init__(self, *, fade_step=255, animation_ready=True, script_work_busy=False,
                 vm_busy=False):
        if not 0 <= fade_step <= 255:
            raise ValueError('fade_step must be 0..255')
        source = SOURCE.read_bytes()
        if hashlib.sha256(source).hexdigest() != SOURCE_SHA256:
            raise ValueError('source image differs from audited original')
        self.uc = Uc(UC_ARCH_X86, UC_MODE_32)
        self.uc.mem_map(BASE, (len(source)+0xfff) & ~0xfff)
        self.uc.mem_write(BASE, source)
        self.uc.mem_map(TASK, 0x120000)
        self.uc.mem_map(STACK, 0x10000)
        self.uc.mem_map(RETURN, 0x1000)
        self.external = {'fade_step': fade_step, 'animation_ready': animation_ready,
                         'script_work_busy': script_work_busy, 'vm_busy': vm_busy}
        self.stub_calls = Counter()
        self.visited = set()
        self._function_ranges = FUNCTIONS
        self._stubs = dict(STUBS)
        self._audit_code_hook = self.uc.hook_add(UC_HOOK_CODE, self._hook)
        self._audit_write_hooks = []
        self.write(0x7A49FC, TASK)  # Render-context pointer only used by stubbed calls.
        self.write(TASK+0x43, 1, 'B')
        self.write(TASK+0x59, 1, 'B')

    def read(self, address, fmt='I'):
        return struct.unpack('<'+fmt, self.uc.mem_read(address, struct.calcsize(fmt)))[0]

    def write(self, address, value, fmt='I'):
        self.uc.mem_write(address, struct.pack('<'+fmt, value))

    def _hook(self, uc, address, size, _):
        if address == RETURN:
            uc.emu_stop()
            return
        if any(start <= address < end for start, end in self._function_ranges):
            self.visited.add(address)
            return
        if address not in self._stubs:
            raise RuntimeError(f'undeclared external code at {address:#x}')
        name, pop_bytes = self._stubs[address]
        self.stub_calls[name] += 1
        sp = uc.reg_read(UC_X86_REG_ESP)
        result = 0
        if name == 'fade_step':
            result = self.external['fade_step']
        elif name in ('animation_ready', 'script_work_busy'):
            result = int(self.external[name])
        elif name == 'vm_update':
            result = int(self.external['vm_busy'])
        elif name == 'debug_stack_check':
            result = uc.reg_read(UC_X86_REG_EAX)  # Preserve original return value.
        elif name == 'memset':
            target, byte, count = struct.unpack('<III', uc.mem_read(sp+4, 12))
            if not TASK <= target <= TASK+0x120000-count or count > 0x1000:
                raise RuntimeError('memset outside bounded task workspace')
            uc.mem_write(target, bytes([byte & 255])*count)
            result = target
        uc.reg_write(UC_X86_REG_EAX, result)
        uc.reg_write(UC_X86_REG_ESP, sp+4+pop_bytes)
        uc.reg_write(UC_X86_REG_EIP, self.read(sp))

    def call(self, address, args=(), *, receiver=TASK):
        if address not in [start for start, _ in self._function_ranges]:
            raise ValueError('entry point outside audit allowlist')
        sp = STACK+0xff00
        self.write(sp, RETURN)
        for index, value in enumerate(args):
            self.write(sp+4+index*4, value)
        self.uc.reg_write(UC_X86_REG_ESP, sp)
        self.uc.reg_write(UC_X86_REG_ECX, receiver)
        self.uc.emu_start(address, RETURN, timeout=1_000_000, count=100_000)
        if self.uc.reg_read(UC_X86_REG_EIP) != RETURN:
            raise RuntimeError('function did not return within audit bounds')
        if self.uc.reg_read(UC_X86_REG_ESP) != sp+4+len(args)*4:
            raise RuntimeError('calling convention/stack mismatch')
        return self.uc.reg_read(UC_X86_REG_EAX)

    def snapshot(self):
        return {'transition_phase': self.read(TASK+0x38),
                'script_phase': self.read(TASK+0x44, 'B'),
                'script_control_active': self.read(TASK+0x43, 'B'),
                'exit_flag': self.read(TASK+0x4C),
                'script_completion_phase': self.read(TASK+0x59, 'B'),
                'fade_in_value': self.read(0x7A4184, 'h'),
                'fade_out_value': self.read(0x7A417C, 'h'),
                'finish_flags': [self.read(TASK+i, 'B') for i in (0x170, 0x171, 0x172)]}

    def frame(self):
        # Order of the two real calls in 4539B0:454CF0, then 453F10.
        script_return = self.call(0x454CF0)
        loop_return = self.call(0x453F10)
        return {**self.snapshot(), 'script_function_return': script_return,
                'transition_function_return': loop_return}


def replay_case(name, *, exit_flag=1, transition_phase=5, fade_step=255,
                animation_ready=True, frames=16, result_selector=1):
    emulator = ExitEmulator(fade_step=fade_step, animation_ready=animation_ready)
    # Use the actual request initializer, with VM execution explicitly disabled.
    emulator.call(0x4549D0, (0, 0, 2, exit_flag, 0, 0, 1))
    emulator.write(TASK+0x38, transition_phase)
    emulator.write(TASK+0x44, 5, 'B')  # Synthetic input: VM/cleanup already completed.
    emulator.write(TASK+0x174, result_selector)
    emulator.write(0x7A4184, 0, 'h')
    emulator.write(0x7A417C, 0, 'h')
    states = []
    for _ in range(frames):
        state = emulator.frame()
        states.append(state)
        if state['transition_function_return']:
            break
    return {'name': name, 'synthetic_initial_state': {'exit_flag': exit_flag,
            'transition_phase': transition_phase, 'script_phase': 5,
            'result_selector': result_selector},
            'external_inputs': emulator.external, 'states': states,
            'stub_calls': dict(emulator.stub_calls),
            'visited_original_addresses': [hex(a) for a in sorted(emulator.visited)],
            'transition_returned': bool(states[-1]['transition_function_return']),
            'state11_observed': False, 'authorizes_persistent_write': False}


def report():
    return {'schema_version': 2, 'evidence_kind': 'original_x86_with_synthetic_external_inputs',
            'source_image_sha256': SOURCE_SHA256,
            'function_ranges': [[hex(a), hex(b)] for a, b in FUNCTIONS],
            'stub_manifest': [{'va': hex(a), 'meaning': name, 'callee_pop_bytes': pop}
                              for a, (name, pop) in STUBS.items()],
            'limitations': ['VM completion and initial task phase are synthetic inputs.',
                            'Rendering, animation, clock, audio and cleanup are stubbed.',
                            '4539B0 full loop and 451670 dispatch are not emulated.',
                            '4539B0 ignores 454CF0 return; only 453F10 return controls this exit edge.',
                            'No live scene5 branch or persistent-write authorization.'],
            'cases': [replay_case('terminal_handshake'),
                      replay_case('intermediate_signal', exit_flag=0),
                      replay_case('completion_flag_overwritten', transition_phase=4),
                      replay_case('clock_stalled', fade_step=0),
                      replay_case('animation_stalled', animation_ready=False),
                      replay_case('no_result_animation', result_selector=0),
                      replay_case('other_result_selector', result_selector=5)],
            'authorizes_persistent_write': False}


def report_text(result):
    return json.dumps(result, ensure_ascii=False, indent=2)+'\n'


def godot_fixture(result):
    """Export expected frames from the original instructions, never the Godot model."""
    return {**{key: result[key] for key in ('schema_version', 'evidence_kind',
            'source_image_sha256', 'function_ranges', 'limitations',
            'authorizes_persistent_write')},
        'source_report_sha256': hashlib.sha256(report_text(result).encode('utf-8')).hexdigest(),
        'cases': [{'name': case['name'],
                   'initial_state': {**case['synthetic_initial_state'],
                       'script_control_active': 1, 'script_completion_phase': 1,
                       'finish_flags': [0, 0, 0], 'fade_in_value': 0, 'fade_out_value': 0},
                   'external_inputs': case['external_inputs'], 'states': case['states'],
                   'state11_observed': False, 'authorizes_persistent_write': False}
                  for case in result['cases']]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, help='new JSON report; refuses overwrite')
    parser.add_argument('--godot-out', type=Path, help='new fixture from same report; refuses overwrite')
    args = parser.parse_args()
    if args.out and args.godot_out and args.out.resolve() == args.godot_out.resolve():
        parser.error('report and fixture must have different paths')
    for path in (args.out, args.godot_out):
        if path and path.exists():
            parser.error(f'refusing overwrite: {path}')
    result = report()
    text = report_text(result)
    if args.out:
        with args.out.open('x', encoding='utf-8', newline='\n') as handle:
            handle.write(text)
    else:
        print(text, end='')
    if args.godot_out:
        with args.godot_out.open('x', encoding='utf-8', newline='\n') as handle:
            handle.write(report_text(godot_fixture(result)))


if __name__ == '__main__':
    main()
