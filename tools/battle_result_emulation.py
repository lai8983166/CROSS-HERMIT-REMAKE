"""Bounded native result-task control replay, with preparation explicitly unresolved.

Extends the prior scene-five replay without modifying its historical evidence.
Only isolated memory is touched; preparation, resources and UI are declared
boundaries. A control-flow exit cannot authorize a character/week transaction.
"""
import argparse
import hashlib

from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.scene5_task_emulation import TaskEmulator, CONTROLLER, RESULT_TASK
from tools.tactics_exit_emulation import ROOT, STACK, RETURN, report_text, SOURCE_SHA256

PREP_TASK = 0x9401000
RESULT_NATIVE = ((0x4BAA90, 0x4BAB60), (0x4BAB60, 0x4BAE30),
                 (0x4BBCC0, 0x4BBD40), (0x4BD590, 0x4BD6F0),
                 (0x4B8F20, 0x4B8F70), (0x4B9120, 0x4B9210))
RESULT_EXTERNAL = {
    0x42AE20: ('result_resource_read', 0), 0x416790: ('result_resource_register', 8),
    0x428AD0: ('result_resource_free', 0), 0x41F4E0: ('result_resource_unload', 4),
    0x439F80: ('base_task_destructor', 0),
    # These three preparation bodies remain unresolved, including their writes.
    0x4BD210: ('unresolved_result_grade_preparation', 0),
    0x4BCA40: ('unresolved_result_loot_preparation', 0),
    0x4BBD40: ('unresolved_result_score_growth_preparation', 0),
    0x4BAE30: ('result_draw', 0), 0x4DB060: ('result_sound', 0),
    0x4D2620: ('result_fade_draw', 28), 0x4D2700: ('result_button_draw', 20),
    0x4D5EC0: ('result_button_input', 20), 0x4DB2B0: ('result_button_sound', 0),
    0x4DB120: ('result_sound_cleanup', 0),
}


class ResultEmulator(TaskEmulator):
    def __init__(self, *, skip_flag=False, special_date=False, confirm=True,
                 audio_ready=True, max_yields=100):
        super().__init__()
        if not 1 <= max_yields <= 1000:
            raise ValueError('max_yields must be 1..1000')
        self._function_ranges += RESULT_NATIVE
        self._stubs.update(RESULT_EXTERNAL)
        self.uc.mem_map(PREP_TASK, 0x1000)
        self.result_inputs = dict(skip_flag=skip_flag, special_date=special_date,
                                  confirm=confirm, audio_ready=audio_ready)
        self.max_yields = max_yields
        self.result_running = False
        self.result_stopped = False
        self.result_yields = 0
        self.result_events = []
        self.result_allocations = []

    def _hook(self, uc, address, size, user):
        sp = uc.reg_read(UC_X86_REG_ESP)
        if self.result_running and address == 0x422360:
            self.result_yields += 1
            self.result_events.append({'kind': 'result_yield',
                'phase': self.read(RESULT_TASK+0x30, 'h'),
                'caller_return_va': hex(self.read(sp))})
            if self.result_yields > self.max_yields:
                self.result_stopped = True
                uc.emu_stop()
                return
        if address in (0x4BAA90, 0x4BBCC0, 0x4BAB60, 0x4BD620, 0x4BD590, 0x4B9120):
            self.result_events.append({'kind': 'native_entry', 'va': hex(address),
                                       'caller_return_va': hex(self.read(sp))})
        if address in (0x428A40, 0x439EF0, 0x4216C0):
            if address == 0x428A40:
                length = self.read(sp+4)
                pointer = {0x1CC: RESULT_TASK, 0x30: PREP_TASK}.get(length)
                if pointer is None or pointer in self.result_allocations:
                    raise RuntimeError('unexpected or duplicate task allocation')
                self.result_allocations.append(pointer)
                value, pop, name = pointer, 0, 'isolated_task_allocation'
            elif address == 0x439EF0:
                value = uc.reg_read(UC_X86_REG_ECX)
                if value not in self.result_allocations:
                    raise RuntimeError('base constructor outside task allocation')
                pop, name = 0, 'isolated_base_task_constructor'
            else:
                args = [self.read(sp+i) for i in (4, 8, 12)]
                if args[0] not in self.result_allocations or args[1:] != [0, 2]:
                    raise RuntimeError('unexpected task scheduler registration')
                self.dispatch_events.append({'kind': 'isolated_scheduler_registration',
                    'pointer': hex(args[0]), 'vtable': hex(self.read(args[0])),
                    'active': self.read(args[0]+0x28, 'B')})
                value, pop, name = 0, 0, 'isolated_scheduler_register'
            self.stub_calls[name] += 1
            self._stub_return(value, pop)
            return
        if self.result_running and address == 0x4DB270:
            self.stub_calls['result_cleanup_timer_ready'] += 1
            self._stub_return(int(self.result_inputs['audio_ready']), 0)
            return
        if address in RESULT_EXTERNAL:
            name, pop = RESULT_EXTERNAL[address]
            self.stub_calls[name] += 1
            if name.startswith('unresolved_'):
                self.result_events.append({'kind': 'unresolved_preparation', 'va': hex(address)})
            if name == 'result_button_input':
                # Original caller checks [buffer+4], NOT [buffer].
                buffer = self.read(sp+4)
                if not STACK <= buffer <= STACK+0x10000-8:
                    raise RuntimeError('result input buffer outside isolated stack')
                self.write(buffer, 0)
                self.write(buffer+4, int(self.result_inputs['confirm']))
            self._stub_return(RETURN if name == 'result_resource_read' else 0, pop)
            return
        return super()._hook(uc, address, size, user)

    def run_result(self, name):
        battle = super().run()
        # Result flags/date are explicit synthetic inputs, not a live witness.
        self.write(0x7F4491, int(self.result_inputs['skip_flag']), 'B')
        self.write(0x7F4505, 0, 'B')
        self.write(0x7A528E, 15 if self.result_inputs['special_date'] else 4, 'h')
        self.write(0x7A5290, 4 if self.result_inputs['special_date'] else 5, 'h')
        self.result_running = True
        self.call_thread(0x4BD660, RESULT_TASK)
        self.result_running = False
        if not self.result_stopped:
            self.call(0x49E2B0)
        return {'name': name, 'synthetic_result_inputs': self.result_inputs,
            'battle_handoff': {'exit_frame': battle['frames'][-1],
                              'state11_dispatched_in_emulation': battle['state11_dispatched_in_emulation']},
            'result_events': self.result_events, 'dispatch_events': self.dispatch_events,
            'result_phase': self.read(RESULT_TASK+0x30, 'h'),
            'skip_display': self.read(RESULT_TASK+0x32, 'h'),
            'bounded_stop': self.result_stopped,
            'requested_state': self.read(CONTROLLER+0x30),
            'request_pending': self.read(CONTROLLER+0x2C),
            'preparation_task': {'pointer': hex(self.read(0x7A4AE4)),
                'vtable': hex(self.read(PREP_TASK)), 'active': self.read(PREP_TASK+0x28, 'B')},
            'stub_calls': dict(self.stub_calls),
            'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
            'preparation_resolved': False, 'live_witness': False,
            'authorizes_persistent_write': False}

    def call_thread(self, address, receiver):
        sp = STACK+0xFF00
        self.write(sp, RETURN)
        self.write(sp+4, 0)
        self.uc.reg_write(UC_X86_REG_ESP, sp)
        self.uc.reg_write(UC_X86_REG_ECX, receiver)
        self.uc.emu_start(address, RETURN, timeout=10_000_000, count=2_000_000)
        if not self.result_stopped:
            if self.uc.reg_read(UC_X86_REG_EIP) != RETURN:
                raise RuntimeError('task exceeded instruction/time bounds')
            if self.uc.reg_read(UC_X86_REG_ESP) != sp+8:
                raise RuntimeError('task thread stack mismatch')


def report():
    return {'schema_version': 1, 'evidence_kind': 'native_result_control_with_unresolved_preparation',
        'source_image_sha256': SOURCE_SHA256,
        'additional_native_ranges': [[hex(a), hex(b)] for a, b in RESULT_NATIVE],
        'additional_stub_manifest': [{'va': hex(va), 'meaning': name, 'callee_pop_bytes': pop}
            for va, (name, pop) in RESULT_EXTERNAL.items()],
        'limitations': ['Scene-five world/terminal selection and presentation are synthetic.',
            'Grade, loot and score/growth preparation bodies are skipped and unresolved.',
            'Result input, resource APIs, sound, drawing and task scheduling are simulated.',
            'State10 body, state12 and school transactions are not executed.'],
        'cases': [ResultEmulator().run_result('confirm'),
                  ResultEmulator(skip_flag=True).run_result('skip_flag'),
                  ResultEmulator(special_date=True).run_result('special_date'),
                  ResultEmulator(confirm=False, max_yields=60).run_result('confirm_missing'),
                  ResultEmulator(audio_ready=False, max_yields=70).run_result('audio_missing')],
        'authorizes_persistent_write': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    output = ROOT / args.out
    if output.exists():
        parser.error('output already exists; use a new report path')
    result = report_text(report())
    with output.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(result)
    print(f'{output}: SHA-256 {hashlib.sha256(result.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
