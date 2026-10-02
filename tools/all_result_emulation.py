"""Native state12 application with explicit synthetic presentation boundaries.

Continues the task5 preparation instance through the real state10 gate and
state12 constructor/body. MVP/return scripts and presentation are unresolved
boundaries, not script witnesses. All writes remain in isolated CPU memory.
"""
import argparse
import hashlib

from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.battle_preparation_emulation import (PreparationEmulator, CHAR_BASE,
    CHAR_STRIDE, PACKAGE_BASE, PACKAGE_STRIDE, DEFAULT_UNITS)
from tools.battle_result_emulation import PREP_TASK
from tools.scene5_task_emulation import TaskEmulator, CONTROLLER
from tools.tactics_exit_emulation import ROOT, STACK, RETURN, SOURCE_SHA256, report_text

ALL_TASK = 0x9700000
ALL_NATIVE = ((0x4B8FF0, 0x4B9120), (0x4BD870, 0x4BE0B0),
    (0x4BF9E0, 0x4C0400), (0x4C0C10, 0x4C19A0),
    (0x4C1AA0, 0x4C1E20), (0x4D0750, 0x4D0790),
    (0x4D3960, 0x4D3A20), (0x4D5600, 0x4D56A0))
ALL_EXTERNAL = {
    0x450110: ('resource_path_lookup', 4), 0x40C780: ('audio_resource_register', 12),
    0x4D0860: ('unresolved_general_vm_resource_initialization', 0),
    0x4BD7E0: ('animation_resource_initialize', 0),
    0x409EF0: ('animation_object_initialize', 4),
    0x4077C0: ('render_context_reset', 0), 0x409FF0: ('animation_start', 12),
    0x464C60: ('embedded_animation_constructor', 0),
    0x4075E0: ('embedded_render_constructor', 0),
    0x4BE0B0: ('all_result_draw', 0), 0x40D390: ('all_result_audio_play', 16),
    0x4CE210: ('unresolved_mvp_or_school_script_load', 8),
    0x4CDED0: ('general_vm_resource_unload', 0),
}


class AllResultEmulator(PreparationEmulator):
    def __init__(self, *, confirm=True, mvp_ready=True, mode=0, special_date=False,
                 result_flag=0, max_yields=450):
        super().__init__()
        if type(mode) is not int or mode not in (0, 1) or result_flag not in (0, 1):
            raise ValueError('only declared mode/result flag 0/1 probes are supported')
        if type(max_yields) is not int or not 1 <= max_yields <= 1000:
            raise ValueError('max_yields must be 1..1000')
        self._function_ranges += ALL_NATIVE
        self._stubs.update(ALL_EXTERNAL)
        self.uc.mem_map(ALL_TASK, 0x5000)
        self.all_running = False
        self.all_stopped = False
        self.all_yields = 0
        self.stop_reason = None
        self.all_events = []
        self.all_inputs = dict(confirm=confirm, mvp_ready=mvp_ready, mode=mode,
                              special_date=special_date, result_flag=result_flag,
                              max_yields=max_yields)
        # Explicit school/participant setup, not an observed original roster.
        self.write(0x7A5260, 3, 'h')
        for group in range(5):
            self.write(0x7AAA12+group*0x1C, -1, 'h')
            self.write(0x7A529A+group*0x70, 2, 'h')
            self.write(0x7A52A0+group*0x70, 5 if group == 0 else 0, 'h')
            self.write(0x7A52A2+group*0x70, 7 if group == 0 else 0, 'h')
            for slot in range(4):
                index = slot if group == 0 and slot < 3 else -1
                character = DEFAULT_UNITS[index][0] if index >= 0 else -1
                self.write(0x7AAAE0+group*8+slot*2, index, 'h')
                self.write(0x7AAA22+group*0x1C+slot*2, character, 'h')
        self.write(0x7A5304, 0, 'h')  # No support roster in this audit subset.
        self.uc.mem_write(0x7D3D71, bytes([50])*(68*68))

    def _hook(self, uc, address, size, user):
        sp = uc.reg_read(UC_X86_REG_ESP)
        receiver = uc.reg_read(UC_X86_REG_ECX)
        if address in (0x4B8FF0, 0x4C1D30, 0x4C1910, 0x4C1AA0, 0x4BD870,
                       0x4C00C0, 0x4C0350, 0x4C0C10, 0x4BDAC0, 0x4C1350,
                       0x4BF9E0, 0x4D0750, 0x4D3510):
            event = {'va': hex(address), 'caller_return_va': hex(self.read(sp)),
                     'receiver': hex(receiver)}
            if address == 0x4C0C10:
                event['character_id'] = self.read(sp+4, 'h')
            self.all_events.append(event)
        if self.all_running and address == 0x4D3510:
            # Never replace a week transaction with a pretend successful return.
            self.all_stopped, self.stop_reason = True, 'week_transaction_boundary'
            uc.emu_stop()
            return
        if self.all_running and address == 0x422360:
            self.all_yields += 1
            if self.all_yields > self.all_inputs['max_yields']:
                self.all_stopped, self.stop_reason = True, 'presentation_yield_bound'
                uc.emu_stop()
                return
        if address == 0x428A40 and self.read(sp+4) == 0x4F74:
            if ALL_TASK in self.result_allocations:
                raise RuntimeError('duplicate all-result allocation')
            self.result_allocations.append(ALL_TASK)
            self.stub_calls['isolated_task_allocation'] += 1
            self._stub_return(ALL_TASK, 0)
            return
        if self.all_running and address == 0x4D5EC0:
            # The two buttons share the API. Only the right button confirms.
            buffer, x = self.read(sp+4), self.read(sp+8)
            if not STACK <= buffer <= STACK+0x10000-8 or x not in (0x2E1, 0x1BA):
                raise RuntimeError('unexpected all-result input buffer/button')
            self.write(buffer, 0)
            self.write(buffer+4, int(self.all_inputs['confirm'] and x == 0x2E1))
            self.stub_calls['all_result_declared_button_input'] += 1
            self._stub_return(0, 20)
            return
        if self.all_running and address == 0x4CE8F0:
            self.stub_calls['unresolved_mvp_vm_update'] += 1
            self._stub_return(int(not self.all_inputs['mvp_ready']), 0)
            return
        if address in ALL_EXTERNAL:
            name, pop = ALL_EXTERNAL[address]
            self.stub_calls[name] += 1
            if address == 0x4CE210:
                pointer = self.read(sp+4)
                raw = bytearray()
                for offset in range(256):
                    byte = self.read(pointer+offset, 'B')
                    if not byte:
                        break
                    raw.append(byte)
                else:
                    raise RuntimeError('unbounded script path')
                self.all_events.append({'boundary': name, 'path': raw.decode('ascii'),
                    'sub': self.read(sp+8, 'i'), 'caller_return_va': hex(self.read(sp))})
            self._stub_return(receiver if address in (0x464C60, 0x4075E0) else 0, pop)
            return
        if any(a <= address < b for a, b in ALL_NATIVE):
            return TaskEmulator._hook(self, uc, address, size, user)
        return super()._hook(uc, address, size, user)

    def application_snapshot(self):
        characters = []
        for c, _, _, _ in DEFAULT_UNITS:
            base, package = CHAR_BASE+c*CHAR_STRIDE, PACKAGE_BASE+c*PACKAGE_STRIDE
            job = self.read(base+6, 'h')
            characters.append({'character_id': c, 'job': job,
                'attributes': [self.read(base+0xC+k*8, 'B') for k in range(7)],
                'growth_pools': [self.read(base+0x10+k*8) for k in range(7)],
                'level_50': self.read(base+0x50, 'B'),
                'character_sha256': hashlib.sha256(bytes(self.uc.mem_read(base, CHAR_STRIDE))).hexdigest(),
                'skill_statuses': [self.read(base+0xB8+k*0xC, 'B') for k in range(84)],
                'staged_package': [self.read(package+k*4, 'i') for k in range(8)],
                'staged_total': self.read(package+0x20, 'i'),
                'job_progress': self.read(package+0xD7+job, 'B'),
                'week_records_hex': bytes(self.uc.mem_read(package+0x24, 59*3)).hex(),
                'recipient_count': self.read(package+0x120, 'h')})
        return {'characters': characters, 'month': self.read(0x7A528E, 'h'),
            'week': self.read(0x7A5290, 'h'), 'global_total_511c': self.read(0x7A511C, 'i'),
            'recipient_id': self.read(0x7E1180, 'h'),
            'relationships': [{'from': a, 'to': b, 'value': self.read(0x7D3D71+a*68+b, 'B')}
                              for a, _, _, _ in DEFAULT_UNITS for b, _, _, _ in DEFAULT_UNITS if a != b],
            'nonparticipant_character_sha256': hashlib.sha256(bytes(self.uc.mem_read(
                CHAR_BASE+5*CHAR_STRIDE, CHAR_STRIDE))).hexdigest(),
            'nonparticipant_package_hex': bytes(self.uc.mem_read(PACKAGE_BASE+5*PACKAGE_STRIDE, PACKAGE_STRIDE)).hex()}

    def replay_all(self, name):
        preparation = self.replay(name)
        self.write(0x7F4491, self.all_inputs['mode'], 'B')
        self.write(0x7F4505, self.all_inputs['result_flag'], 'B')
        if self.all_inputs['special_date']:
            self.write(0x7A528E, 15, 'h')
            self.write(0x7A5290, 4, 'h')
        before = self.application_snapshot()
        self.call_thread(0x4B8FF0, PREP_TASK)
        self.call(0x49E2B0)
        self.all_running = True
        self.call_thread(0x4C1AA0, ALL_TASK)
        self.all_running = False
        return {'name': name, 'synthetic_inputs': self.all_inputs,
            'school_setup': {'participant_ids': [3, 4, 9], 'group0_activity_type': 2,
                'group0_record_data': [5, 7], 'teacher_ids': [-1]*5,
                'support_count': 0, 'initial_relationship_value': 50,
                'unresolved_mvp_vm': 'declared ready/busy, original script not executed'},
            'preparation': {'result_summary': preparation['result_summary'],
                'native_inputs': preparation['native_result_inputs'],
                'character_templates': preparation['synthetic_inputs']['character_templates']},
            'before': before, 'after': self.application_snapshot(),
            'branch': self.read(ALL_TASK+0x30, 'h'), 'phase': self.read(ALL_TASK+0x32, 'h'),
            'constructor': {'pointer': hex(self.read(0x7A4BB8)),
                'vtable': hex(self.read(ALL_TASK)), 'active': self.read(ALL_TASK+0x28, 'B')},
            'bounded_stop': self.all_stopped, 'stop_reason': self.stop_reason,
            'yields': self.all_yields, 'requested_state': self.read(CONTROLLER+0x30),
            'events': self.all_events, 'dispatch_events': self.dispatch_events,
            'stub_calls': dict(self.stub_calls),
            'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
            'live_witness': False, 'authorizes_persistent_write': False}

    def call_thread(self, address, receiver):
        if address != 0x4C1AA0:
            return super().call_thread(address, receiver)
        sp = STACK+0xFF00
        self.write(sp, RETURN)
        self.write(sp+4, 0)
        self.uc.reg_write(UC_X86_REG_ESP, sp)
        self.uc.reg_write(UC_X86_REG_ECX, receiver)
        self.uc.emu_start(address, RETURN, timeout=10_000_000, count=2_000_000)
        if not self.all_stopped:
            if self.uc.reg_read(UC_X86_REG_EIP) != RETURN:
                raise RuntimeError('all-result thread exceeded instruction/time bounds')
            if self.uc.reg_read(UC_X86_REG_ESP) != sp+8:
                raise RuntimeError('all-result thread stack mismatch')


def report():
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'evidence_kind': 'native_all_result_with_synthetic_school_and_mvp_boundaries',
        'additional_native_ranges': [[hex(a), hex(b)] for a, b in ALL_NATIVE],
        'additional_stub_manifest': [{'va': hex(va), 'meaning': name, 'callee_pop_bytes': pop}
            for va, (name, pop) in ALL_EXTERNAL.items()]+[
                {'va': '0x4ce8f0', 'meaning': 'unresolved_mvp_vm_update',
                 'callee_pop_bytes': 0, 'only_during_all_result': True},
                {'va': '0x4d5ec0', 'meaning': 'all_result_declared_button_input',
                 'callee_pop_bytes': 20, 'only_during_all_result': True}],
        'stop_boundaries': [{'va': '0x4d3510', 'meaning': 'unresolved_week_transaction',
                             'policy': 'stop_before_instruction_no_fake_return'}],
        'limitations': ['World/terminal selection, units and school/round setup are synthetic.',
            'Preparation always uses mode0; mode1/date/flag are counterfactual inputs injected at state12.',
            'MVP VM execution and return-to-school script loading are unresolved simulated boundaries.',
            'Only battle-activity group0 with IDs3/4/9, no teacher/support, is covered.',
            'State6/13/15 are requests only; their tasks and school script are not run.',
            'Special-date path stops BEFORE the native week transaction.',
            'No persistent world, save or live game is read or modified.'],
        'cases': [AllResultEmulator().replay_all('ordinary_confirm'),
            AllResultEmulator(confirm=False, max_yields=360).replay_all('ordinary_unconfirmed'),
            AllResultEmulator(mvp_ready=False, max_yields=360).replay_all('mvp_boundary_busy'),
            AllResultEmulator(mode=1).replay_all('mode1_flag0'),
            AllResultEmulator(mode=1, result_flag=1).replay_all('mode1_flag1'),
            AllResultEmulator(special_date=True).replay_all('special_week_boundary')],
        'authorizes_persistent_write': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    path = ROOT / args.out
    if path.exists():
        parser.error('output already exists; use a new report path')
    payload = report_text(report())
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(payload)
    print(f'{path}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
