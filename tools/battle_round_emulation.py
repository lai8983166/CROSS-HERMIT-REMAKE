"""Run native state10 gate after result exit; stop at state12/16 constructors.

Round tables are synthetic. Configuration scalar loads and roster/counter writes
are native; combat-unit derivation and configuration resource loading remain
unresolved. This does not finish any result or school transaction.
"""
import argparse
import hashlib

from unicorn.x86_const import UC_X86_REG_ESP

from tools.battle_result_emulation import ResultEmulator, PREP_TASK
from tools.scene5_task_emulation import CONTROLLER
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, report_text

ROUND_NATIVE = ((0x4B8FF0, 0x4B9120), (0x4B9210, 0x4B9340),
                (0x4DA860, 0x4DAB10))
ROUND_EXTERNAL = {0x4DAB10: ('unresolved_configuration_resources', 0),
                  0x4B9340: ('unresolved_combat_unit_derivation', 0),
                  0x4C1D30: ('all_result_constructor_boundary', 0),
                  0x451080: ('next_tactics_constructor_boundary', 0)}


class RoundEmulator(ResultEmulator):
    def __init__(self):
        super().__init__()
        self._function_ranges += ROUND_NATIVE
        self._stubs.update(ROUND_EXTERNAL)
        self.round_events = []

    def _hook(self, uc, address, size, user):
        sp = uc.reg_read(UC_X86_REG_ESP)
        if address in (0x4B8FF0, 0x4DA860, 0x4B9210, 0x4B9270, 0x4B92C0):
            event = {'kind': 'native_entry', 'va': hex(address),
                     'caller_return_va': hex(self.read(sp))}
            if address in (0x4DA860, 0x4B9270):
                event['argument'] = self.read(sp+4, 'h')
            self.round_events.append(event)
        if address in ROUND_EXTERNAL:
            name, pop = ROUND_EXTERNAL[address]
            self.stub_calls[name] += 1
            event = {'kind': name, 'va': hex(address),
                     'caller_return_va': hex(self.read(sp))}
            if address == 0x4B9340:
                event.update(character_id=self.read(sp+4, 'h'), ordinal=self.read(sp+8, 'h'))
            self.round_events.append(event)
            self._stub_return(0, pop)
            return
        return super()._hook(uc, address, size, user)

    def round_snapshot(self):
        return {'current': self.read(0x7A5296, 'h'), 'total': self.read(0x7A5298, 'h'),
                'temp_roster': [self.read(0x7A4AEC+i*2, 'h') for i in range(100)],
                'temp_count': self.read(0x7A4AE8, 'h'),
                'combat_count': self.read(0x7F448D, 'B'),
                'scene_id': self.read(0x7F4488, 'h')}

    def run_round(self, name, current, total, roster=(), config_id=5):
        # Audit limits, not original validations: never feed unsafe tables.
        if type(current) is not int or type(total) is not int or not 0 <= current <= total <= 5:
            raise ValueError('round counters outside isolated audit subset')
        if len(roster) > 20 or any(type(i) is not int or not 0 <= i < 68 for i in roster):
            raise ValueError('roster outside isolated audit subset')
        if config_id != 5:
            raise ValueError('only audited configuration five is supported')
        result = self.run_result(name)
        self.write(0x7A5296, current, 'h')
        self.write(0x7A5298, total, 'h')
        self.write(0x7A5308+current*0x70, config_id, 'h')
        self.write(0x7A52F8+current*0x70, len(roster), 'h')
        for i, character in enumerate(roster):
            self.write(0x7A52D0+current*0x70+i*2, character, 'h')
        # Sentinels show that equality does NOT clear/prepare a next round.
        for i in range(100):
            self.write(0x7A4AEC+i*2, 77, 'h')
        self.write(0x7A4AE8, 2, 'h')
        self.write(0x7F448D, 19, 'B')
        self.write(0x7F4488, 99, 'h')
        before = self.round_snapshot()
        self.call_thread(0x4B8FF0, PREP_TASK)
        after = self.round_snapshot()
        self.call(0x49E2B0)
        # Native call log plus original branch predicates prove control only.
        return {'name': name, 'before': before, 'after': after,
                'synthetic_round_table': {'next_roster': list(roster), 'config_id': config_id},
                'state10_dispatched_in_emulation': result['requested_state'] == 10,
                'round_events': self.round_events, 'dispatch_events': self.dispatch_events,
                'requested_state': self.read(CONTROLLER+0x30),
                'request_pending': self.read(CONTROLLER+0x2C),
                'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
                'stub_calls': dict(self.stub_calls), 'preparation_resolved': False,
                'combat_units_ready': False, 'live_witness': False,
                'authorizes_persistent_write': False}


def report():
    return {'schema_version': 1, 'evidence_kind': 'native_round_gate_with_synthetic_round_tables',
            'source_image_sha256': SOURCE_SHA256,
            'additional_native_ranges': [[hex(a), hex(b)] for a, b in ROUND_NATIVE],
            'additional_stub_manifest': [{'va': hex(va), 'meaning': name, 'callee_pop_bytes': pop}
                for va, (name, pop) in ROUND_EXTERNAL.items()],
            'limitations': ['All preceding scene/result synthetic inputs and unresolved preparation remain.',
                'Round tables and counters are explicitly synthetic, not scene-five task-table witnesses.',
                'Configuration scalar writes, temporary roster and count increment execute original code.',
                'Configuration resources and combat-unit derivation are skipped and unresolved.',
                'State12/16 constructors are boundaries; no result application or school return.'],
            'cases': [RoundEmulator().run_round('all_complete', 1, 1),
                      RoundEmulator().run_round('next_round', 1, 2, (3, 4, 9)),
                      RoundEmulator().run_round('empty_complete', 0, 0)],
            'authorizes_persistent_write': False}


def godot_fixture(result):
    return {'schema_version': 1, 'evidence_kind': result['evidence_kind'],
            'source_report_sha256': hashlib.sha256(report_text(result).encode()).hexdigest(),
            'cases': [{key: case[key] for key in ('name', 'before', 'after',
                'synthetic_round_table', 'state10_dispatched_in_emulation', 'requested_state',
                'round_events', 'combat_units_ready', 'preparation_resolved',
                'authorizes_persistent_write')} for case in result['cases']],
            'authorizes_persistent_write': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    parser.add_argument('--godot-out', required=True)
    args = parser.parse_args()
    paths = [ROOT / args.out, ROOT / args.godot_out]
    if paths[0].resolve() == paths[1].resolve() or any(p.exists() for p in paths):
        parser.error('outputs must be distinct new paths')
    result = report()
    for path, data in zip(paths, (result, godot_fixture(result))):
        payload = report_text(data)
        with path.open('x', encoding='utf-8', newline='\n') as handle:
            handle.write(payload)
        print(f'{path}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
