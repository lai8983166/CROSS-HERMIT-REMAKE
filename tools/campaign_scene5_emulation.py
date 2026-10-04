"""Native scene5 predicates select the terminal script in one returning CPU.

The end-world and event invocation are declared inputs. No tactical simulation,
parallel event scheduler, live witness or save authority is inferred.
"""
import argparse
from copy import deepcopy
import hashlib

from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_ESP

from tools.campaign_school_boot_emulation import CampaignSchoolBootEmulator
from tools.battle_result_inputs_emulation import UNITCTRL, input_snapshot
from tools.scene5_script_emulation import SCRIPT_SHA256
from tools.tactics_exit_emulation import ROOT, TASK, SOURCE_SHA256, report_text

EVENT_RECORDS = 0xE000000
EVENT_NATIVE = ((0x4337F0, 0x43396A), (0x431D40, 0x431DC8),
                (0x469170, 0x46921C), (0x4E2720, 0x4E275B), (0x4E2760, 0x4E2989))


class CampaignScene5Emulator(CampaignSchoolBootEmulator):
    def __init__(self, *, event_bit=0):
        if type(event_bit) is not int or event_bit not in (0, 1):
            raise ValueError('event bit outside captured scene5 subset')
        super().__init__()
        # The combined instruction policies cost more than the old task-only
        # hook. Instruction/frame bounds and actual ret4 checks are unchanged.
        self.task_timeout_us = 60_000_000
        self._function_ranges += EVENT_NATIVE
        self.uc.mem_map(EVENT_RECORDS, 0x1000)
        self.event_bit = event_bit
        self.event_trace = []
        self.event_before = self.event_after = None
        self.native_preparation = None
        self.result_entry_inputs = None
        self.round_before = self.round_after = None
        # Declared terminal world, established before any tactical script/result.
        # Enemy numbers are reverse wrapper indices, not persistent role IDs.
        for ordinal, number in enumerate((3, 11)):
            wrapper = UNITCTRL+0x80AEC+(250-number)*0x520
            record = EVENT_RECORDS+ordinal*0xB0
            self.write(wrapper, 1, 'h')
            self.write(wrapper+0x258, record)
            self.write(record+2, 49+ordinal, 'h')
            self.write(record+0xA4, 1, 'B')  # Opposite side to own_side0.
            self.write(record+0xF, 0, 'B')
        self.write(0x8093C0, event_bit << 31)

    def event_snapshot(self):
        return {'scene_id': self.read(0x7F4488, 'h'), 'own_side': self.read(UNITCTRL+0x2EF44, 'B'),
            'field_2e6f4': self.read(UNITCTRL+0x2E6F4),
            'event_bit3_0_word': self.read(0x8093C0),
            'units': [{'enemy_number': number, 'wrapper_index': 250-number,
                'used': self.read(UNITCTRL+0x80AEC+(250-number)*0x520, 'h'),
                'character_id': self.read(EVENT_RECORDS+ordinal*0xB0+2, 'h'),
                'side_a4': self.read(EVENT_RECORDS+ordinal*0xB0+0xA4, 'B'),
                'field_f': self.read(EVENT_RECORDS+ordinal*0xB0+0xF, 'B')}
                for ordinal,number in enumerate((3,11))], 'task': self.snapshot()}

    def request(self, selector=2, sub=2):
        # Inherited driver defaults are not terminal selection inputs here.
        if (selector, sub) != (2, 2) or self.event_before is not None:
            raise RuntimeError('one native scene event invocation required')
        self.write(TASK+0x38, 5)  # Declared phase, not completion.
        self.event_before = self.event_snapshot()
        self.call(0x4337F0, receiver=UNITCTRL)
        self.event_after = self.event_snapshot()
        if self.read(TASK+0x4C) != 1:
            raise RuntimeError('native event did not choose terminal request')
        return self.snapshot()

    def _hook(self, uc, address, size, user):
        if address == 0x4B8FF0:
            self.round_before = self.round_snapshot()
        if address == 0x4C1D30:
            self.round_after = self.round_snapshot()
        if address in (0x4337F0, 0x431D40, 0x46A430, 0x469170, 0x4E2720, 0x454AF0, 0x454BB0):
            sp = uc.reg_read(UC_X86_REG_ESP)
            entry = {'va': hex(address), 'caller_return_va': hex(self.read(sp)),
                'receiver': hex(uc.reg_read(UC_X86_REG_ECX))}
            count = {0x431D40: 1, 0x46A430: 1, 0x469170: 1,
                     0x4E2720: 2, 0x454AF0: 2, 0x454BB0: 3}.get(address, 0)
            entry['args'] = [self.read(sp+4+i*4) for i in range(count)]
            self.event_trace.append(entry)
        if address in (0x433826, 0x43387C, 0x4338E3):
            self.event_trace.append({'predicate_return_va': hex(address),
                                    'value': uc.reg_read(UC_X86_REG_EAX)})
        if address == 0x4BD660:
            self.result_entry_inputs = input_snapshot(self)
        return super()._hook(uc, address, size, user)

    def round_snapshot(self):
        return {'current': self.read(0x7A5296, 'h'), 'total': self.read(0x7A5298, 'h'),
            'temp_roster': [self.read(0x7A4AEC+i*2, 'h') for i in range(100)],
            'temp_count': self.read(0x7A4AE8, 'h'), 'combat_count': self.read(0x7F448D, 'B'),
            'scene_id': self.read(0x7F4488, 'h')}

    def replay(self, name, **kwargs):
        if kwargs:
            raise RuntimeError('terminal selector override is not supported')
        preparation = super().replay(name)
        self.native_preparation = deepcopy(preparation)
        return preparation

    def run_scene5_campaign(self, name):
        before_world = self.canonical_snapshot()
        result = self.run_campaign_boot(name)
        return {'name': name, 'declared_end_world': self.unit_inputs,
            'declared_scene_event_invocation': {'va': '0x4337f0', 'receiver': hex(UNITCTRL),
                'parallel_dispatcher_executed': False}, 'before_world': before_world,
            'event_before': self.event_before, 'event_after': self.event_after,
            'event_trace': self.event_trace, 'tactical_frames': deepcopy(self.frames),
            'work_completions': deepcopy(self.work_events), 'dispatch_events': deepcopy(self.dispatch_events),
            'state11_entry_inputs': self.result_entry_inputs, 'preparation': self.native_preparation,
            'round_before': self.round_before, 'round_after': self.round_after,
            'campaign': result, 'school_initialized': False, 'interactive_school_ready': False,
            'live_witness': False, 'authorizes_persistent_write': False}


def report():
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256, 'script_sha256': SCRIPT_SHA256,
        'evidence_kind': 'same_cpu_native_scene5_condition_selection_to_captured_school_boot',
        'additional_native_ranges': [[hex(a),hex(b)] for a,b in EVENT_NATIVE],
        'limitations': ['End-world units, event bit, phase5 and the direct scene5 event invocation are declared inputs.',
            '4337F0 executes original predicates and selects 11/11 or 8/8; no terminal selector is injected.',
            'The same UnitCtrl, tactical task, result buffers and role catalog continue into the returning campaign.',
            'Tactical simulation, parallel event scheduling, MVP and presentation remain boundaries.',
            'Captured school boot stops before menu interaction; no full school initialization or live/save authority.'],
        'cases': [CampaignScene5Emulator(event_bit=0).run_scene5_campaign('scene5_bit0_sub11_school'),
                  CampaignScene5Emulator(event_bit=1).run_scene5_campaign('scene5_bit1_sub8_school')],
        'live_witness': False, 'authorizes_persistent_write': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    payload = report_text(report())
    path = ROOT / args.out
    with path.open('x', encoding='utf-8', newline='\n') as handle:
        handle.write(payload)
    print(f'{path}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
