"""Execute state7's original week body and fade gate; CH001 is a load boundary.

This isolated task probe does not substitute for the preceding ADV completion.
"""
import argparse
import hashlib

from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.week_settlement_emulation import WeekSettlementEmulator
from tools.scene5_task_emulation import CONTROLLER
from tools.tactics_exit_emulation import ROOT, SOURCE_SHA256, STACK, RETURN, TASK, report_text


class WeekStartEmulator(WeekSettlementEmulator):
    def __init__(self, *, fade_ready=True):
        super().__init__()
        self._function_ranges += ((0x49F4E0, 0x49F570),)
        self.fade_ready = fade_ready
        self.start_events = []
        self.start_yields = 0
        self.start_stopped = False

    def _hook(self, uc, address, size, user):
        sp = uc.reg_read(UC_X86_REG_ESP)
        if address in (0x4DB230, 0x4DB270, 0x4DB120):
            name = {0x4DB230: 'fade_start', 0x4DB270: 'fade_ready', 0x4DB120: 'fade_release'}[address]
            event = {'kind': name, 'va': hex(address)}
            if address == 0x4DB230:
                event['frames'] = self.read(sp+4)
            self.start_events.append(event)
            self.stub_calls['declared_'+name] += 1
            self._stub_return(int(self.fade_ready) if address == 0x4DB270 else 0, 0)
            return
        if address == 0x422360:
            self.start_yields += 1
            if self.start_yields > 4:
                self.start_stopped = True
                uc.emu_stop()
                return
        if address == 0x4CE210:
            raw = bytes(self.uc.mem_read(self.read(sp+4), 256)).split(b'\0')[0]
            self.start_events.append({'kind': 'script_load_boundary', 'path': raw.decode('ascii'),
                                      'next_task_state': self.read(sp+8)})
        if address == 0x439E30:
            self.start_events.append({'kind': 'state_request', 'state': self.read(sp+4)})
        return super()._hook(uc, address, size, user)

    def run(self, name, month, week):
        if type(month) is not int or type(week) is not int or not 4 <= month <= 14 or not 1 <= week <= 5:
            raise ValueError('outside isolated week-start calendar subset')
        self.write(0x7A528E, month, 'h')
        self.write(0x7A5290, week, 'h')
        self.write(CONTROLLER+0x2C, 0)
        self.write(CONTROLLER+0x30, 7)
        before = self.week_snapshot()
        sp = STACK+0xFF00
        self.write(sp, RETURN)
        self.write(sp+4, 0)
        self.uc.reg_write(UC_X86_REG_ESP, sp)
        self.uc.reg_write(UC_X86_REG_ECX, TASK)
        self.uc.emu_start(0x49F4E0, RETURN, timeout=10_000_000, count=2_000_000)
        if not self.start_stopped:
            if self.uc.reg_read(UC_X86_REG_EIP) != RETURN or self.uc.reg_read(UC_X86_REG_ESP) != sp+8:
                raise RuntimeError('week-start task exceeded bounds or ret4 stack mismatch')
        return {'name': name, 'synthetic_task_state': 7, 'synthetic_fade_ready': self.fade_ready,
                'before_week': before, 'after_week': self.week_snapshot(),
                'week_events': self.week_events, 'start_events': self.start_events,
                'pending_flag': self.read(CONTROLLER+0x2C), 'requested_state': self.read(CONTROLLER+0x30),
                'bounded_stop': self.start_stopped, 'native_week_body_executed': True,
                'visited_original_addresses': [hex(a) for a in sorted(self.visited)],
                'stub_calls': dict(self.stub_calls), 'adv_script_executed': False,
                'school_initialized': False, 'live_witness': False, 'authorizes_persistent_write': False}


def report():
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256,
            'evidence_kind': 'native_state7_week_start_with_synthetic_task_entry',
            'additional_native_ranges': [['0x49f4e0', '0x49f570']],
            'limitations': ['State7 entry is a direct isolated probe, not observed ADV completion.',
                            'Fade APIs are declared ready/busy; CH001 loading is a boundary.',
                            'School rosters, availability, equipment and flags inherit the explicit week probe setup.',
                            'No ADV chapter or school constructor is executed.'],
            'cases': [WeekStartEmulator().run('ordinary_week_start', 4, 4),
                      WeekStartEmulator().run('month_rollover_week_start', 4, 5),
                      WeekStartEmulator(fade_ready=False).run('fade_busy_after_week', 4, 5)],
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
