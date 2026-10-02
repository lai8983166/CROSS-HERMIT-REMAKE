"""Execute the complete native week body and its participant/item/skill helpers.

Extends state12 replay without changing historical boundary reports. School
rosters, availability, equipment and probe flags are explicit synthetic inputs.
Calendar probes are separate direct calls, never claims of a scene branch.
"""
import argparse
import hashlib

from unicorn.x86_const import UC_X86_REG_ESP

from tools.all_result_emulation import AllResultEmulator
from tools.battle_preparation_emulation import CHAR_BASE, CHAR_STRIDE, PACKAGE_BASE, PACKAGE_STRIDE
from tools.scene5_task_emulation import TaskEmulator
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, report_text

WEEK_NATIVE = ((0x4D31F0, 0x4D3510), (0x4D3510, 0x4D3600), (0x4D3AA0, 0x4D3D00),
               (0x4D46E0, 0x4D4730))
PROBE_ITEMS = {1: 0x301, 2: 0x307, 3: 0x407, 4: 0x40B, 5: 0x205}


class WeekSettlementEmulator(AllResultEmulator):
    def __init__(self):
        super().__init__(special_date=True)
        self._function_ranges += WEEK_NATIVE
        self.week_events = []
        self.week_entry_snapshot = None
        for character in range(45):
            self.write(0x7A5120+character, int(character in (3, 4, 9)), 'B')
        # Equipped and unequipped status6 probes; they are not source templates.
        base = CHAR_BASE+3*CHAR_STRIDE
        for slot in range(8):
            self.write(base+0x52+slot*2, 1 if slot == 0 else 0, 'h')
            self.write(base+0x62+slot*2, 2 if slot == 0 else 0, 'h')
        self.write(base+0xB8, 6, 'B')
        self.write(base+0xB8+0xC, 6, 'B')
        for item, flags in PROBE_ITEMS.items():
            self.write(0x7AACAA+item*2, flags, 'H')
        self.write(0x7A55FA, 9, 'h')
        self.write(0x7A4E62, 8, 'h')
        self.write(0x7A55F6, 2, 'h')
        self.write(0x7E11A0, 99, 'h')

    def _hook(self, uc, address, size, user):
        if address in (0x4D3510, 0x4D3AA0, 0x4D31F0, 0x4D34A0, 0x4D33A0):
            sp = uc.reg_read(UC_X86_REG_ESP)
            event = {'va': hex(address), 'caller_return_va': hex(self.read(sp))}
            if address in (0x4D3AA0, 0x4D33A0):
                event['character_id'] = self.read(sp+4, 'h')
            self.week_events.append(event)
            if address == 0x4D3510:
                if self.week_entry_snapshot is not None:
                    raise RuntimeError('duplicate week entry in single-transaction audit')
                self.week_entry_snapshot = self.week_snapshot()
        if any(a <= address < b for a, b in WEEK_NATIVE):
            # Bypass ONLY the old stop-before-week policy; all these bodies,
            # including availability lookup, execute original instructions.
            return TaskEmulator._hook(self, uc, address, size, user)
        return super()._hook(uc, address, size, user)

    def week_snapshot(self):
        return {'month': self.read(0x7A528E, 'h'), 'week': self.read(0x7A5290, 'h'),
            'flags': {hex(a): self.read(a, 'h') for a in (0x7A55FA, 0x7A4E62, 0x7A55F6, 0x7E11A0)},
            'participants': [{'character_id': c,
                'attributes': [self.read(CHAR_BASE+c*CHAR_STRIDE+0xC+k*8, 'B') for k in range(7)],
                'job_progress': [self.read(PACKAGE_BASE+c*PACKAGE_STRIDE+0xD7+k, 'b') for k in range(31)],
                'unlock_flags': [self.read(PACKAGE_BASE+c*PACKAGE_STRIDE+0xF9+k, 'B') for k in range(30)],
                'skill_statuses': [self.read(CHAR_BASE+c*CHAR_STRIDE+0xB8+k*0xC, 'B') for k in range(84)],
                'equipped_skills': [self.read(CHAR_BASE+c*CHAR_STRIDE+0x52+k*2, 'h') for k in range(8)],
                'equipped_items': [self.read(CHAR_BASE+c*CHAR_STRIDE+0x62+k*2, 'h') for k in range(8)]}
                for c in (3, 4, 9)],
            'availability': [self.read(0x7A5120+c, 'B') for c in range(45)],
            'item_flags': [self.read(0x7AACAA+i*2, 'H') for i in range(1, 361)],
            'nonparticipant_character_sha256': hashlib.sha256(bytes(self.uc.mem_read(
                CHAR_BASE+5*CHAR_STRIDE, CHAR_STRIDE))).hexdigest(),
            'nonparticipant_package_sha256': hashlib.sha256(bytes(self.uc.mem_read(
                PACKAGE_BASE+5*PACKAGE_STRIDE, PACKAGE_STRIDE))).hexdigest()}

    def run_all_week(self):
        result = self.replay_all('special_all_result_week')
        if self.week_entry_snapshot is None or result['bounded_stop']:
            raise RuntimeError('native week transaction did not finish')
        return {'name': result['name'], 'evidence_kind': 'state12_continuation_with_synthetic_inputs',
            'all_result': result, 'before_week': self.week_entry_snapshot,
            'after_week': self.week_snapshot(), 'week_events': self.week_events,
            'native_week_body_executed': True, 'school_task_executed': False,
            'authorizes_persistent_write': False}

    def probe_calendar(self, name, month, week):
        if type(month) is not int or type(week) is not int or not 4 <= month <= 15 or not 1 <= week <= 5:
            raise ValueError('calendar outside declared isolated probe bounds')
        self.write(0x7A528E, month, 'h')
        self.write(0x7A5290, week, 'h')
        before = self.week_snapshot()
        self.call(0x4D3510)
        return {'name': name, 'evidence_kind': 'direct_week_function_probe',
            'before_week': before, 'after_week': self.week_snapshot(),
            'week_events': self.week_events,
            'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
            'state12_executed': False, 'native_week_body_executed': True,
            'school_task_executed': False, 'authorizes_persistent_write': False}


def report():
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
        'evidence_kind': 'native_week_settlement_with_synthetic_roster_and_equipment',
        'additional_native_ranges': [[hex(a), hex(b)] for a, b in WEEK_NATIVE],
        'additional_stub_manifest': [],
        'synthetic_probe_setup': {'available_character_ids': [3, 4, 9],
            'character3_equipped_skills': [1]+[0]*7, 'character3_equipped_items': [2]+[0]*7,
            'character3_skill_status_overrides': {'1': 6, '2': 6},
            'item_flags': [{'item_id': i, 'flags': f} for i, f in PROBE_ITEMS.items()],
            'flags': {'0x7a55fa': 9, '0x7a4e62': 8, '0x7a55f6': 2, '0x7e11a0': 99}},
        'limitations': ['Inherits scene/result/MVP/script resource boundaries and synthetic school setup.',
            'State12 continuation uses the synthetic special-date branch, not a live scene witness.',
            'Calendar rollover probes call 4D3510 directly; no scene/result path is claimed for them.',
            'No school state6 task or CH003 script execution and no persistent-write authority.'],
        'cases': [WeekSettlementEmulator().run_all_week(),
            WeekSettlementEmulator().probe_calendar('ordinary_week_probe', 4, 4),
            WeekSettlementEmulator().probe_calendar('month_rollover_probe', 4, 5)],
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
