"""Execute original task-five grade/loot/score-growth preparation in isolation.

Native UnitCtrl finalization supplies keys and tactical records. Character
templates, participant mapping, round table and clock seed are declared inputs.
No save file, live world, state12 application or school transaction is accessed.
"""
import argparse
import hashlib

from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_ESP

from tools.battle_result_emulation import ResultEmulator
from tools.battle_result_inputs_emulation import (INPUT_NATIVE, DEFAULT_UNITS, initialize_units,
                                                 input_snapshot)
from tools.scene5_task_emulation import TaskEmulator, RESULT_TASK, CONTROLLER
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, report_text

TLS = 0x9600000
PREPARATION_NATIVE = ((0x4BBD40, 0x4BCA40), (0x4BCA40, 0x4BD210),
                      (0x4BD210, 0x4BD510), (0x4D1BA0, 0x4D1C00),
                      (0x4D1C60, 0x4D1CF0), (0x4D5590, 0x4D5610),
                      (0x4D56A0, 0x4D5850), (0x4D5850, 0x4D58E0),
                      (0x4D58E0, 0x4D5A70), (0x56E230, 0x56E260),
                      (0x570FD0, 0x570FE0), (0x570FE0, 0x571020))
PREPARATION_EXTERNAL = {0x571020: ('declared_clock_seed', 0),
                        0x5753B0: ('isolated_crt_thread_data', 0),
                        0x42B2D0: ('debug_log', 0)}
CHAR_BASE, CHAR_STRIDE = 0x7E17E8, 0x4A0
PACKAGE_BASE, PACKAGE_STRIDE = 0x7CF34C, 0x124


class PreparationEmulator(ResultEmulator):
    def __init__(self, *, seed=4660, cap_character=None):
        super().__init__()
        if type(seed) is not int or not 0 <= seed < 2**31:
            raise ValueError('seed outside isolated signed clock range')
        if cap_character not in (None, 3):
            raise ValueError('only character three cap probe is audited')
        self._function_ranges += INPUT_NATIVE+PREPARATION_NATIVE
        self._stubs.update(PREPARATION_EXTERNAL)
        self.uc.mem_map(TLS, 0x1000)
        self.seed = seed
        self.preparation_events = []
        self.unit_inputs = initialize_units(self)
        self.cap_character = cap_character
        self.write(0x7A5294, 5, 'h')
        self.write(0x7A5296, 1, 'h')
        self.write(0x7A5298, 1, 'h')
        self.write(0x7A528C, 0, 'h')
        self.write(0x7A528E, 4, 'h')
        self.write(0x7A5290, 5, 'h')
        self.write(0x7A529C, 10, 'h')
        self.write(0x7A511C, 1000)
        self.write(0x7A54CA+5, 5, 'B')
        self.write(0x7F4491, 0, 'B')
        self.write(0x7F4505, 0, 'B')
        self.write(0x7A52F8, 3, 'h')
        # This is the 20-slot participant mapping, not the 68-record character
        # store: extending it would overwrite nearby task/counter globals.
        for i in range(20):
            self.write(0x7A5210+i*2, -1, 'h')
        for i in range(20):
            self.write(0x7AAAE0+i*2, i, 'h')
        self.templates = []
        for ordinal, (character, _, _, _) in enumerate(DEFAULT_UNITS):
            self.write(0x7A52D0+ordinal*2, character, 'h')
            self.write(0x7A52A8+ordinal*2, 0, 'h')
            self.write(0x7A5210+ordinal*2, character, 'h')
            template_va = 0x6F5088+character*CHAR_STRIDE
            template = bytes(self.uc.mem_read(template_va, CHAR_STRIDE))
            self.uc.mem_write(CHAR_BASE+character*CHAR_STRIDE, template)
            self.uc.mem_write(PACKAGE_BASE+character*PACKAGE_STRIDE, bytes(PACKAGE_STRIDE))
            self.templates.append({'character_id': character, 'template_va': hex(template_va),
                                   'template_sha256': hashlib.sha256(template).hexdigest()})
        # Source templates are preserved separately from this cap counterfactual.
        if cap_character is not None:
            cap_pool = sum(self.read(0x6E4308+i*4) for i in range(101))
            for attribute in range(7):
                self.write(CHAR_BASE+cap_character*CHAR_STRIDE+0xC+attribute*8, 100, 'B')
                self.write(CHAR_BASE+cap_character*CHAR_STRIDE+0x10+attribute*8, cap_pool)
        self.uc.mem_write(PACKAGE_BASE+5*PACKAGE_STRIDE, bytes.fromhex('78563412')*8)
        for item in range(361):
            self.write(0x7AACAA+item*2, 0, 'H')

    def _hook(self, uc, address, size, user):
        if address in (0x473860, 0x4BD210, 0x4BCA40, 0x4BBD40):
            self.preparation_events.append({'va': hex(address),
                'receiver': hex(uc.reg_read(UC_X86_REG_ECX)),
                'caller_return_va': hex(self.read(uc.reg_read(UC_X86_REG_ESP)))})
        # Bypass the historical unresolved-preparation stubs only for these
        # allowlisted native bodies; previous tools and reports stay unchanged.
        if any(a <= address < b for a, b in INPUT_NATIVE+PREPARATION_NATIVE):
            return TaskEmulator._hook(self, uc, address, size, user)
        if address in PREPARATION_EXTERNAL:
            name, pop = PREPARATION_EXTERNAL[address]
            self.stub_calls[name] += 1
            self._stub_return(self.seed if address == 0x571020 else TLS if address == 0x5753B0 else 0, pop)
            return
        return super()._hook(uc, address, size, user)

    def preparation_snapshot(self):
        return {'task_grade': self.read(0x7A54CA+5, 'B'),
            'global_total_511c': self.read(0x7A511C, 'i'),
            'round_grade_index': self.read(0x7A5306, 'h'),
            'characters': [{'character_id': c,
                'character_record_sha256': hashlib.sha256(bytes(self.uc.mem_read(
                    CHAR_BASE+c*CHAR_STRIDE, CHAR_STRIDE))).hexdigest(),
                'growth_pools': [self.read(CHAR_BASE+c*CHAR_STRIDE+0x10+k*8) for k in range(7)],
                'staged_package': [self.read(PACKAGE_BASE+c*PACKAGE_STRIDE+k*4, 'i') for k in range(8)],
                'staged_total': self.read(PACKAGE_BASE+c*PACKAGE_STRIDE+0x20, 'i')}
                for c, _, _, _ in DEFAULT_UNITS],
            'nonparticipant_package': bytes(self.uc.mem_read(PACKAGE_BASE+5*PACKAGE_STRIDE, 32)).hex(),
            'item_flags': [{'item_id': i, 'flags': self.read(0x7AACAA+i*2, 'H')}
                           for i in range(1, 361) if self.read(0x7AACAA+i*2, 'H')]}

    def replay(self, name, *, selector=2, sub=2):
        before = self.preparation_snapshot()
        battle = TaskEmulator.run(self, selector=selector, sub=sub)
        inputs = input_snapshot(self)
        self.result_running = True
        self.call_thread(0x4BD660, RESULT_TASK)
        self.result_running = False
        self.call(0x49E2B0)
        after = self.preparation_snapshot()
        return {'name': name, 'synthetic_inputs': {'task_id': 5, 'current': 1, 'total': 1,
                'mode': 0, 'month': 4, 'week': 5, 'group_bonus': 10, 'initial_total_511c': 1000,
                'initial_grade': 5, 'clock_seed': self.seed, 'unit_inputs': self.unit_inputs,
                'character_templates': self.templates, 'cap_character': self.cap_character,
                'participant_indices': list(range(20)),
                'participant_character_ids': [3, 4, 9]+[-1]*17,
                'initial_item_flags': 'all_zero_361_slots'},
            'before': before, 'after': after, 'native_result_inputs': inputs,
            'battle_handoff': {'exit_frame': battle['frames'][-1],
                'state11_dispatched_in_emulation': battle['state11_dispatched_in_emulation']},
            'preparation_events': self.preparation_events, 'dispatch_events': self.dispatch_events,
            'result_summary': {'grade_index': self.read(RESULT_TASK+0x34, 'h'),
                'time_display': self.read(RESULT_TASK+0x36, 'h'),
                'unit_display': self.read(RESULT_TASK+0x38, 'h'),
                'total_after': self.read(RESULT_TASK+0x3C, 'i'),
                'total_delta': self.read(RESULT_TASK+0x40, 'i'),
                'total_before': self.read(RESULT_TASK+0x44, 'i'),
                'unit_count': self.read(RESULT_TASK+0x48, 'h'),
                'sum_count_field_aa': self.read(RESULT_TASK+0x4A, 'h'),
                'sum_contribution_field_ac': self.read(RESULT_TASK+0x4C, 'h'),
                'sum_status_field_ae': self.read(RESULT_TASK+0x4E, 'h'),
                'display_character_ids': [self.read(RESULT_TASK+0x50+k*2, 'h') for k in range(20)],
                'display_packages': [self.read(RESULT_TASK+0xF0+k*4, 'i') for k in range(20)],
                'loot_groups': [[self.read(RESULT_TASK+0x140+g*0x14+k*2, 'h')
                                 for k in range(10)] for g in range(7)]},
            'requested_state': self.read(CONTROLLER+0x30),
            'native_preparation_executed': True, 'native_rand_state': self.read(TLS+0x14),
            'stub_calls': dict(self.stub_calls),
            'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
            'live_witness': False, 'authorizes_persistent_write': False}


def report():
    return {'schema_version': 1, 'evidence_kind': 'native_task5_preparation_with_synthetic_inputs',
        'source_image_sha256': SOURCE_SHA256,
        'additional_native_ranges': [[hex(a), hex(b)] for a, b in PREPARATION_NATIVE],
        'additional_stub_manifest': [{'va': hex(va), 'meaning': name, 'callee_pop_bytes': pop}
            for va, (name, pop) in PREPARATION_EXTERNAL.items()],
        'limitations': ['World, terminal selection, units, participant/round tables and clock seed are synthetic.',
            'Only task5, mode0, month4/week5, three units and zero objective slots are audited.',
            'Task37 skill preparation, other modes/tasks and nonzero objectives are not covered.',
            'Native preparation writes stay in isolated memory; state12 and school application not executed.'],
        'cases': [PreparationEmulator().replay('task5_sub2'),
                  PreparationEmulator(seed=17).replay('task5_selector14_sub8', selector=14, sub=8),
                  PreparationEmulator(cap_character=3).replay('character3_cap_probe')],
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
