"""Execute native UnitCtrl finalization on declared synthetic unit records.

Integrated cases retain the original scene-five VM/task path. Predicate probes
are separate direct calls. No live battle, persistence or school transaction.
"""
import argparse
import hashlib

from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_ESP

from tools.scene5_task_emulation import TaskEmulator
from tools.tactics_exit_emulation import ROOT, TASK, SOURCE_SHA256, report_text

UNITCTRL, UNIT_DATA = TASK+0x190, 0x9500000
INPUT_NATIVE = ((0x473860, 0x473940), (0x473940, 0x473AB0), (0x473AB0, 0x473DC0),
                (0x4307B0, 0x430980), (0x468D10, 0x468D80), (0x468E10, 0x468EB0),
                (0x46A430, 0x46A4C0), (0x46A4C0, 0x46A550),
                (0x46A550, 0x46A5E0), (0x46A950, 0x46AA22),
                (0x469AD0, 0x469B90), (0x469B90, 0x469C60), (0x469C60, 0x469D30))
DEFAULT_UNITS = ((3, 10, 40, 0), (4, 20, 60, 1), (9, 0, 0, 2))


def initialize_units(emulator, units=DEFAULT_UNITS, *, elapsed=60, thresholds=(120, 240),
                     hostile_survivor=False):
    """Explicit audit setup shared with result preparation replay, not game setup."""
    if not 1 <= len(units) <= 20 or len({unit[0] for unit in units}) != len(units):
        raise ValueError('audit requires 1..20 distinct character IDs')
    for character, count, contribution, state in units:
        if any(type(value) is not int for value in (character, count, contribution, state)) \
                or not 1 <= character <= 45 or not 0 <= count <= 1000 \
                or not 0 <= contribution <= 1000 or not 0 <= state <= 127:
            raise ValueError('unit record outside audited playable subset')
    if not 0 <= elapsed <= 10000 or len(thresholds) != 2 \
            or not 0 <= thresholds[0] <= thresholds[1] <= 10000:
        raise ValueError('time predicate outside audit bounds')
    emulator.uc.mem_map(UNIT_DATA, 0x2000)
    emulator.write(UNITCTRL+0x117C38, TASK)
    emulator.write(UNITCTRL+0x2E6F4, 0)
    emulator.write(UNITCTRL+0x2E6FC, elapsed)
    emulator.write(UNITCTRL+0x2EF44, 0, 'B')
    emulator.write(UNITCTRL+0x2EF14, 7, 'h')
    emulator.write(0x7F44AC, thresholds[0])
    emulator.write(0x7F44B0, thresholds[1])
    for i in range(16):
        emulator.write(0x7F44BE+i, 0, 'B')
    for ordinal, (character, count, contribution, state) in enumerate(units):
        record = UNIT_DATA+ordinal*0xB0
        wrapper = UNITCTRL+0x80AEC+ordinal*0x520
        emulator.write(wrapper, 1, 'h')
        emulator.write(wrapper+0x258, record)
        for offset, value in ((0, ordinal), (2, character), (0xAA, count), (0xAC, contribution)):
            emulator.write(record+offset, value, 'h')
        emulator.write(record+0xAE, state, 'B')
        emulator.write(record+0xA4, 0, 'B')
        # Existing tactical records must match identities before native copying.
        emulator.write(0x7F4518+ordinal*0xB0, ordinal, 'h')
        emulator.write(0x7F451A+ordinal*0xB0, character, 'h')
    emulator.write(UNITCTRL+0xDC8EC, int(hostile_survivor))
    if hostile_survivor:
        wrapper = UNITCTRL+0x80AEC+20*0x520
        record = UNIT_DATA+20*0xB0
        emulator.write(wrapper, 1, 'h')
        emulator.write(wrapper+0x258, record)
        emulator.write(record+2, 50, 'h')
        emulator.write(record+0xA4, 1, 'B')
        emulator.write(UNITCTRL+0x115AAC+1, 1, 'B')
        emulator.write(UNITCTRL+0xDC8EC+4, wrapper)
    emulator.write(UNITCTRL+0xDCCD8, 0)
    return {'units': [{'character_id': c, 'count_field_aa': n,
                      'contribution_field_ac': k, 'status_field_ae': s}
                     for c, n, k, s in units],
            'elapsed': elapsed, 'thresholds': list(thresholds),
            'hostile_survivor': hostile_survivor, 'objective_slots': [0]*16,
            'own_side': 0, 'field_2ef14': 7, 'unitctrl_task_pointer': hex(TASK)}


def input_snapshot(emulator, units=DEFAULT_UNITS):
    return {'result_selector': emulator.read(0x7F450C, 'h'),
            'time_key': emulator.read(0x7F450E, 'h'),
            'unit_condition_key': emulator.read(0x7F4510, 'h'),
            'field_4512': emulator.read(0x7F4512, 'h'),
            'units': [{'ordinal': i, 'character_id': emulator.read(0x7F451A+i*0xB0, 'h'),
                       'count_field_aa': emulator.read(0x7F45C2+i*0xB0, 'h'),
                       'contribution_field_ac': emulator.read(0x7F45C4+i*0xB0, 'h'),
                       'status_field_ae': emulator.read(0x7F45C6+i*0xB0, 'B')}
                      for i in range(len(units))]}


class InputEmulator(TaskEmulator):
    def __init__(self, **inputs):
        super().__init__()
        self._function_ranges += INPUT_NATIVE
        self.units = inputs.get('units', DEFAULT_UNITS)
        self.synthetic_unit_inputs = initialize_units(self, **inputs)
        self.input_events = []

    def _hook(self, uc, address, size, user):
        if address in (0x473860, 0x4307B0, 0x473940, 0x473AB0):
            self.input_events.append({'va': hex(address),
                'receiver': hex(uc.reg_read(UC_X86_REG_ECX)),
                'caller_return_va': hex(self.read(uc.reg_read(UC_X86_REG_ESP)))})
        return super()._hook(uc, address, size, user)

    def replay(self, name, *, selector=2, sub=2, integrated=True):
        if integrated:
            battle = self.run(selector=selector, sub=sub)
            handoff = {'exit_frame': battle['frames'][-1],
                       'dispatch_events': battle['dispatch_events'],
                       'state11_dispatched_in_emulation': battle['state11_dispatched_in_emulation']}
        else:
            self.write(TASK+0x174, selector)
            self.call(0x473860, receiver=UNITCTRL)
            handoff = None
        return {'name': name, 'integrated_task_run': integrated,
                'synthetic_unit_inputs': self.synthetic_unit_inputs,
                'task_result_selector': self.read(TASK+0x174),
                'result_inputs': input_snapshot(self, self.units), 'native_input_events': self.input_events,
                'battle_handoff': handoff, 'stub_calls': dict(self.stub_calls),
                'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
                'live_witness': False, 'authorizes_persistent_write': False}


def report():
    return {'schema_version': 1, 'evidence_kind': 'native_result_inputs_with_synthetic_units',
            'source_image_sha256': SOURCE_SHA256,
            'additional_native_ranges': [[hex(a), hex(b)] for a, b in INPUT_NATIVE],
            'limitations': ['World, terminal selector and unit records are synthetic.',
                'Integrated cases execute original VM/task; predicate probes are separate direct calls.',
                'Objective reward slots are zero; their nonzero branches are not exercised.',
                'No result preparation, persistent application or school transaction.'],
            'cases': [InputEmulator().replay('terminal_sub2'),
                      InputEmulator(hostile_survivor=True).replay('terminal_selector14_sub8', selector=14, sub=8),
                      InputEmulator(thresholds=(0, 0)).replay('time_disabled', integrated=False),
                      InputEmulator(elapsed=120).replay('time_first_boundary', integrated=False),
                      InputEmulator(elapsed=180).replay('time_middle', integrated=False),
                      InputEmulator(elapsed=240).replay('time_second_boundary', integrated=False),
                      InputEmulator(elapsed=300).replay('time_late', integrated=False)],
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
